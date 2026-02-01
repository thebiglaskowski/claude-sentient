# Claude Sentient

> **A thin orchestration layer for Claude Code**

Claude Sentient coordinates Claude Code's native capabilities into an autonomous development workflow. It's not a replacement — it's a lightweight wrapper that makes built-in tools work together.

---

## Philosophy

**Native-first.** Claude Code already has task management, planning modes, sub-agents, and memory. We don't reinvent these — we orchestrate them.

---

## What You Get

### 4 Commands

| Command | What It Does |
|---------|--------------|
| `/cs-loop` | Autonomous loop: understand → plan → execute → verify → commit |
| `/cs-plan` | Plan complex tasks before executing |
| `/cs-status` | Show tasks, git state, detected profile |
| `/cs-learn` | Save learnings to persistent memory |

### Profile Detection

Sentient detects your project type and loads appropriate tooling:

| Profile | Detected By | Tools |
|---------|-------------|-------|
| Python | `pyproject.toml`, `*.py` | ruff, pytest, pyright |
| TypeScript | `tsconfig.json`, `*.ts` | eslint, vitest, tsc |
| Shell | `*.sh`, `*.ps1` | shellcheck |
| Go | `go.mod`, `*.go` | golangci-lint, go test |
| General | (fallback) | auto-detect |

### Quality Gates

Before committing, these must pass:
- **LINT** — Zero errors
- **TEST** — All tests pass
- **BUILD** — Project builds
- **GIT** — Clean state

---

## How It Works

```
/cs-loop "add input validation"

[INIT] Profile: Python | Tools: ruff, pytest
[PLAN] Created 3 tasks via TaskCreate
[EXECUTE] Working through tasks...
[VERIFY] Running gates: lint ✓ test ✓
[COMMIT] Checkpoint: a1b2c3d
[DONE] Added validation to 2 endpoints
```

Under the hood, `/cs-loop` orchestrates:
- `TaskCreate` / `TaskUpdate` for work tracking
- `EnterPlanMode` for complex decisions
- `Task` subagents for parallel work
- Native git workflow for commits

---

## Native Tools Used

| Feature | Claude Code Tool |
|---------|------------------|
| Task Queue | `TaskCreate`, `TaskUpdate`, `TaskList` |
| Planning | `EnterPlanMode`, `ExitPlanMode` |
| Sub-agents | `Task` with `subagent_type` |
| Memory | `.claude/rules/*.md` |
| Commands | `commands/*.md` + `Skill` |

---

## Project Structure

```
claude-sentient/
├── .claude/
│   ├── commands/       # Active commands (loaded by Claude Code)
│   └── rules/          # Persistent memory (learnings.md)
├── commands/           # /cs-* command definitions
├── profiles/           # Project type profiles (5 profiles)
├── templates/          # Governance file templates
├── phases/             # Phase documentation
├── reference/          # Planning docs, hook examples
└── rules/              # Topic-specific standards
```

---

## Governance Files

Claude Sentient creates and maintains these files for continuity across sessions:

| File | Purpose |
|------|---------|
| `STATUS.md` | Current progress, what's done/next |
| `CHANGELOG.md` | Version history |
| `DECISIONS.md` | Architecture decisions (ADRs) |
| `.claude/rules/learnings.md` | Quick decisions, patterns |

When `/cs-loop` runs on a new project, it creates these from templates if missing.

---

## Installation

Copy the `commands/` and `profiles/` directories to your project, or reference them from your `CLAUDE.md`.

No external dependencies. No custom scripts. Just markdown and yaml files.

---

## Documentation

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Main instructions |
| `STATUS.md` | Current progress |
| `CHANGELOG.md` | Version history |
| `DECISIONS.md` | Architecture decisions |

---

## Status

**v0.2.0** — Native-first architecture complete

See `STATUS.md` for details.

---

## License

MIT

---

*Claude Sentient: Orchestrating Claude Code's native capabilities*
