---
feature: Quality Gates
version: "1.0"
last_updated: 2026-03-04
dependencies:
  - "02-session-lifecycle.md"
  - "07-profile-system.md"
routes: []
status: draft
---

# Quality Gates

> Two hooks enforce quality: gate-monitor (async PostToolUse) observes gate command outcomes and records them; dod-verifier (sync Stop hook) checks that gates actually ran against changed code before the session ends.

## Hook Overview

| Hook | Event | Sync | Purpose |
|------|-------|------|---------|
| `gate-monitor.cjs` | PostToolUse/Bash | async | Record gate command outcomes to gate_history.json |
| `dod-verifier.cjs` | Stop | sync | Verify gates ran against code files modified this session |

---

## gate-monitor.cjs

### Gate Pattern Detection

Only commands matching `GATE_PATTERNS` are processed. Non-gate commands trigger an early exit before any disk I/O:

| Tool | Pattern Examples |
|------|-----------------|
| Python lint | `ruff`, `flake8`, `pylint` |
| Python test | `pytest`, `python -m pytest` |
| JS/TS lint | `eslint`, `tsc --noEmit` |
| JS/TS test | `vitest`, `jest`, `mocha` |
| Go | `go test`, `golangci-lint` |
| Rust | `cargo test`, `cargo clippy` |
| Build | `npm run build`, `cargo build`, `go build` |

### gate_history.json Entry Shape

```json
{
  "timestamp": "2026-03-04T00:00:00.000Z",
  "command": "pytest tests/",
  "exitCode": 0,
  "passed": true,
  "tool": "Bash",
  "outputRef": null,
  "outputPreview": "5 passed in 0.42s"
}
```

`passed: null` when `exit_code` is absent from Claude Code's PostToolUse payload (inconclusive, not failure).

### Large Output Masking

Gate stdout exceeding `MAX_OBSERVATION_SIZE = 8000` chars is saved to a file instead of inline:

```json
{
  "outputRef": ".claude/state/gate-output/gate-output-1709510400000.txt",
  "outputLines": 342,
  "outputPreview": "first 200 chars..."
}
```

`gate-output/` directory pruned to `MAX_GATE_OUTPUTS = 20` files (oldest removed).

### Async Delivery

gate-monitor is `async: true` — it fires after the Bash command completes and does not block Claude's next turn. Gate results are available in `gate_history.json` for dod-verifier to read.

---

## dod-verifier.cjs

Runs synchronously on every Stop event (before Claude concludes a response).

### Integrity Check Algorithm

1. Read `gate_history.json` — find all gate runs this session
2. Read `file_changes.json` — find all files modified this session
3. Filter changed files to code files: `.py`, `.ts`, `.js`, `.go` (and their test variants)
4. For each extension category (Python, TypeScript/JS, Go), check if a matching gate ran after the last code change
5. Check `git status` for uncommitted changes

### dod-verifier Output

If gates ran and no uncommitted changes: exits 0 silently.

If gates did not run against changed code files, outputs a report:

```json
{
  "context": "Warning: Code files modified without quality gates: src/auth.py (Python lint/test not run)"
}
```

If uncommitted changes exist:

```json
{
  "context": "Warning: Uncommitted changes detected. Run git add/commit before concluding."
}
```

### File Extension Categorization

| Category | Extensions | Gates Required |
|----------|-----------|---------------|
| Python | `.py` | ruff/flake8/pylint + pytest |
| TypeScript/JS | `.ts`, `.tsx`, `.js`, `.jsx` | eslint/tsc + vitest/jest |
| Go | `.go` | golangci-lint + go test |
| Rust | `.rs` | cargo clippy + cargo test |

---

## gate_history.json Structure

Append-only array stored at `.claude/state/gate_history.json`:

```json
[
  {
    "timestamp": "...",
    "command": "ruff check .",
    "exitCode": 0,
    "passed": true,
    "outputPreview": "All checks passed."
  },
  {
    "timestamp": "...",
    "command": "pytest",
    "exitCode": 1,
    "passed": false,
    "outputLines": 89,
    "outputRef": ".claude/state/gate-output/gate-output-123.txt"
  }
]
```

## Business Rules

- **gate-monitor early exit**: Non-gate commands return immediately — eliminates 3-4 sync file ops per Bash PostToolUse
- **null exit_code**: Treated as `passed: null` (inconclusive), not failure — prevents spurious "Gate failed (exit null)" log entries
- **dod-verifier always exits 0**: It reports warnings but never blocks Claude from responding
- **Async delivery semantics**: With `async: true`, HookResult delivers on the next turn. gate-monitor errors are silent — kept minimal (pure state writer) to avoid silent failures
- **Quality gate sources**: Gate definitions come from `profiles/*.yaml`, not hard-coded in hooks
