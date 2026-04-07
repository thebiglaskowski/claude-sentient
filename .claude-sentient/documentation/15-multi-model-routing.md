---
feature: Multi-Model Routing
version: "1.0"
last_updated: 2026-03-04
dependencies:
  - "01-autonomous-loop.md"
routes: []
status: draft
---

# Multi-Model Routing

> `/cs-multi` configures which Claude model handles each phase of the cs-loop. Default routing balances cost (haiku for simple phases) and capability (sonnet/opus for complex reasoning). Keyword-based overrides switch to opus for security-sensitive tasks.

## Default Routing

| Phase | Default Model | Rationale |
|-------|--------------|-----------|
| INIT | haiku | Fast context loading; no reasoning required |
| UNDERSTAND | sonnet | Standard analysis and complexity classification |
| PLAN | sonnet | Architecture reasoning and trade-off analysis |
| EXECUTE | sonnet | Code generation and implementation |
| VERIFY | sonnet | Quality analysis and error diagnosis |
| COMMIT | haiku | Simple git operations; no reasoning required |
| EVALUATE | haiku | Quick pass/fail assessment |

## Model IDs

| Alias | Model ID |
|-------|---------|
| haiku | `claude-haiku-4-5-20251001` |
| sonnet | `claude-sonnet-4-6` |
| opus | `claude-opus-4-6` |

## Keyword Overrides

Certain task keywords upgrade models for specific phases:

| Keywords | Phases Upgraded | Upgraded To |
|----------|----------------|-------------|
| `security`, `auth`, `vulnerability` | PLAN, VERIFY | opus |

This ensures security-sensitive tasks get maximum reasoning capability where it matters most (architecture planning and verification).

## state/multi-model.json

Custom routing is persisted in `.claude/state/multi-model.json`:

```json
{
  "version": "1.0",
  "routing": {
    "INIT": "haiku",
    "UNDERSTAND": "sonnet",
    "PLAN": "sonnet",
    "EXECUTE": "sonnet",
    "VERIFY": "sonnet",
    "COMMIT": "haiku",
    "EVALUATE": "haiku"
  },
  "overrides": {
    "keywords": {
      "security": { "PLAN": "opus", "VERIFY": "opus" },
      "auth": { "PLAN": "opus", "VERIFY": "opus" },
      "vulnerability": { "PLAN": "opus", "VERIFY": "opus" }
    }
  }
}
```

If this file doesn't exist, cs-loop uses the defaults from the profile (`models.by_phase`).

## `/cs-multi` Command

### Flags

| Flag | Effect |
|------|--------|
| `--show` | Display current routing configuration |
| `--set PHASE=model` | Set model for a specific phase |
| `--reset` | Reset all routing to defaults |

### Examples

```bash
/cs-multi --show                    # Show current config
/cs-multi --set PLAN=opus           # Use opus for planning
/cs-multi --set EXECUTE=haiku       # Use haiku for execution (cost saving)
/cs-multi --reset                   # Back to defaults
```

### Cost Estimates

Routing affects token cost significantly:

| Scenario | Relative Cost |
|----------|--------------|
| All haiku | ~1x (baseline) |
| Default routing | ~3-5x |
| All sonnet | ~8-10x |
| All opus | ~25-30x |
| Security task (opus for PLAN+VERIFY) | ~15-20x |

## Profile-Level Defaults

Each profile YAML declares `models.by_phase` as the base defaults. `/cs-multi` overrides apply on top:

```yaml
models:
  by_phase:
    init: haiku
    understand: sonnet
    plan: sonnet
    execute: sonnet
    verify: sonnet
    commit: haiku
    evaluate: haiku
```

The profile defaults and `multi-model.json` overrides are merged at runtime. `multi-model.json` wins on conflict.

## `/cs-loop --model opus` Flag

Passing `--model opus` to `/cs-loop` forces opus for the **entire loop** (all phases). Intended for the most complex or high-stakes tasks where cost is not a concern.

## Business Rules

- **State persistence**: `multi-model.json` persists across sessions. Changes made via `--set` apply to all future cs-loop invocations until `--reset`.
- **Profile defaults take precedence over hardcoded defaults**: Profile `models.by_phase` values are the base; `multi-model.json` overrides apply on top.
- **Keyword overrides are additive**: Keyword-triggered upgrades apply on top of the configured routing without modifying `multi-model.json`.
- **`--model opus` flag is session-scoped**: Affects only the current cs-loop invocation. Does not modify `multi-model.json`.

## Edge Cases

- **No multi-model.json**: Use profile defaults. No error.
- **Unknown model alias**: Warn and fall back to sonnet.
- **Keyword in task but not in override map**: No upgrade applied.
- **INIT phase always haiku**: Cost optimization. INIT is pure context loading — no complex reasoning. Override is allowed but wasteful.
- **Haiku for security tasks**: If user has set VERIFY=haiku but task triggers security keyword override, the keyword override wins (opus > haiku for security verification).
