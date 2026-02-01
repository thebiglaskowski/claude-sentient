# Claude Sentient

> **The Autonomous Development Orchestration Layer for Claude Code**

Claude Sentient makes Claude Code's capabilities work together cohesively. It's an orchestration system that helps you leverage everything Claude Code offers in an organized, autonomous way.

---

## What It Does

- **Auto-detects project type** and loads appropriate tooling
- **Runs an 8-phase autonomous loop** for structured development
- **Enforces quality gates** before considering work complete
- **Creates checkpoints** for easy rollback
- **Maintains context** across sessions via claude-mem

---

## Quick Start

```bash
# Install claude-mem for persistent memory
/plugin marketplace add thedotmack/claude-mem
/plugin install claude-mem

# Run the autonomous loop
/cs-loop "implement user authentication"

# Plan before executing (for complex tasks)
/cs-plan "refactor the API layer"

# Review code quality
/cs-review
```

---

## The 8-Phase Loop

```
INIT       → Detect project, load profile, inject memory
UNDERSTAND → Classify request, assess current state
PLAN       → Decompose work, establish dependencies
EXECUTE    → Implement changes, run incremental tests
VERIFY     → Full test suite, type check, lint
QUALITY    → Run all quality gates
COMMIT     → Create checkpoint commit
EVALUATE   → Done? Exit. More work? Loop back.
```

---

## Project Profiles

Sentient auto-detects and adapts to your project:

| Profile | Detection | Tooling |
|---------|-----------|---------|
| Python | `pyproject.toml`, `*.py` | ruff, pytest, pyright |
| TypeScript | `tsconfig.json`, `*.tsx` | eslint, vitest, tsc |
| Shell | `*.sh`, `*.ps1` | shellcheck, PSScriptAnalyzer |
| Go | `go.mod` | golangci-lint, go test |
| General | (fallback) | auto-detect |

---

## Quality Gates

### Blocking (8)
Must pass before work is considered complete:
- Lint, Type Check, Tests, Security
- Build, Git Clean, Queue Empty, Definition of Done

### Advisory (4)
Report issues but don't block:
- Documentation, Performance, Accessibility, Modern APIs

---

## Directory Structure

```
claude-sentient/
├── profiles/           # Project type profiles
├── phases/             # 8 phase definitions
├── skills/             # Auto-triggered behaviors
├── commands/           # /cs-* commands
├── agents/             # Specialist agents
├── gates/              # Quality gate definitions
│   ├── blocking/       # 8 blocking gates
│   └── advisory/       # 4 advisory gates
├── patterns/           # Architecture patterns
├── rules/              # Topic standards
├── schemas/            # JSON schemas for validation
├── docs/               # Vision docs
└── reference/          # V1, planning, deferred features
```

---

## Philosophy

1. **Autonomous by Default** — Only pause for ambiguity or risk
2. **Profile-Aware** — Adapt to the project, not the other way around
3. **Quality-Enforced** — Gates ensure standards are met
4. **Memory-Enabled** — Context persists across sessions
5. **Checkpoint-Safe** — Always able to roll back

---

## Status

**Phase 0: Foundation** — Complete

See `STATUS.md` for current progress.

---

## Documentation

- `CLAUDE.md` — Main instructions and quick reference
- `phases/*.md` — Detailed phase documentation
- `profiles/*.yaml` — Project type configurations
- `reference/DEFERRED_FEATURES.md` — Features for future versions

---

## License

MIT

---

*Claude Sentient: Orchestrating Claude Code for autonomous development*
