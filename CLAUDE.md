# CLAUDE.md — Claude Sentient

> **Project:** Claude Sentient
> **Version:** 0.1.0
> **Type:** Autonomous Development Orchestration Layer

---

## What Is This?

Claude Sentient is an **orchestration layer** that makes Claude Code's capabilities work together cohesively. It's not a replacement for Claude Code — it's a system that helps you leverage everything Claude Code offers in an organized, autonomous way.

### Core Philosophy

1. **Autonomous by Default** — Only pause for ambiguity or risk
2. **Profile-Aware** — Adapts to project type (Python, TypeScript, Shell, Go, etc.)
3. **Quality-Enforced** — 8 blocking gates + 4 advisory gates
4. **Memory-Enabled** — Uses claude-mem for persistent context
5. **Checkpoint-Safe** — Verified commits enable easy rollback

---

## Quick Start

```bash
# Main autonomous loop (core command)
/cs-loop "implement user authentication"

# Plan before executing (for complex tasks)
/cs-plan "refactor the API layer"

# Check current status
/cs-status
```

---

## The 8-Phase Loop

```
1. INIT       → Load profile, context, memory
2. UNDERSTAND → Classify request, assess state
3. PLAN       → Decompose work, set dependencies
4. EXECUTE    → Implement changes
5. VERIFY     → Run tests, type check, lint
6. QUALITY    → Run all quality gates
7. COMMIT     → Create checkpoint commit
8. EVALUATE   → Done? Exit. More work? Loop.
```

---

## Project Profiles

Sentient auto-detects project type and loads appropriate tooling:

| Profile | Detected By | Tools |
|---------|-------------|-------|
| Python | `pyproject.toml`, `*.py` | ruff, pytest, pyright |
| TypeScript | `tsconfig.json`, `*.ts` | eslint, vitest, tsc |
| Shell | `*.sh`, `*.ps1` | shellcheck, bats |
| Go | `go.mod`, `*.go` | golangci-lint, go test |
| General | (fallback) | auto-detect |

---

## Quality Gates

### MVP Blocking (Phase 1)
- **LINT** — Zero errors
- **TEST** — Tests pass
- **BUILD** — Project builds
- **GIT** — Clean state

### Future Blocking (Phase 2+)
- **TYPE** — Type checking passes
- **SECURITY** — No high/critical vulnerabilities
- **QUEUE** — No S0/S1 items remaining
- **DOD** — Definition of done met

### Advisory (Report Only)
- **DOCS** — Documentation present
- **PERF** — No performance regressions
- **A11Y** — Accessibility (if UI)
- **MODERN** — No deprecated APIs

---

## Key Commands

### MVP (Phase 1)
| Command | Purpose |
|---------|---------|
| `/cs-loop [task]` | Autonomous work loop |
| `/cs-plan [task]` | Plan before executing |
| `/cs-status` | Show current state |

### Future (Phase 2+)
| Command | Purpose |
|---------|---------|
| `/cs-review` | Code review |
| `/cs-test` | Run tests |
| `/cs-commit` | Create checkpoint |
| `/cs-fix [issue]` | Fix a specific issue |

---

## Directory Structure

```
claude-sentient/
├── profiles/           # Project type profiles (python, typescript, etc.)
├── phases/             # 8 phase definitions
├── skills/             # Auto-triggered behaviors (25-30)
├── commands/           # /cs-* commands (20-25)
├── agents/             # Specialist agents (10-12)
├── gates/              # Quality gates (12 total)
│   ├── blocking/       # 8 blocking gates
│   └── advisory/       # 4 advisory gates
├── patterns/           # Reusable architecture patterns
├── rules/              # Topic-specific standards
├── schemas/            # JSON schemas for validation
├── tools/              # Python CLI tools
├── docs/               # Vision and planning docs
├── reference/          # V1, planning docs, deferred features
└── .claude/            # Runtime state
```

---

## Memory & Learning

Claude Sentient uses **claude-mem** for persistent memory:

- Automatic capture via hooks
- Semantic search across sessions
- View at http://localhost:37777
- Query with `mem-search` skill

No complex learning engine — just persistent memory that helps maintain context.

---

## Sub-Agents & Model Selection

Claude Sentient uses sub-agents with appropriate models for different tasks:

| Model | Use For | Examples |
|-------|---------|----------|
| **Haiku** | Fast lookups, simple operations | File searches, quick checks, status queries |
| **Sonnet** | Most development work | Code generation, reviews, test writing |
| **Opus** | Complex decisions, critical reviews | Architecture decisions, security audits, learning from failures |

### Agent Types

| Agent | Model | Purpose |
|-------|-------|---------|
| researcher | Sonnet | Explore codebase, answer questions |
| code-reviewer | Sonnet | Review changes for quality |
| test-writer | Sonnet | Generate tests for code |
| security-auditor | Opus | Security analysis (future) |

---

## Development Standards

### File Naming
- Profiles: `name.profile.yaml`
- Phases: `##-name.md`
- Skills: `name.skill.md`
- Commands: `cs-name.md`
- Gates: `name.gate.yaml`

### Quality Rules
- All blocking gates must pass
- Checkpoints before risky changes
- Tests for new functionality
- Follow project conventions (from profile)

---

## Hard Rules

1. **Never skip blocking gates** — Fix issues, don't bypass
2. **Create checkpoints** — Before risky changes
3. **Respect profile conventions** — Match existing code style
4. **Ask when ambiguous** — One clarifying question, then proceed
5. **Use specialists** — Spawn agents for security, testing, etc.

---

## Getting Help

- Phases: `phases/*.md`
- Profiles: `profiles/*.yaml`
- Deferred features: `reference/DEFERRED_FEATURES.md`
- V1 reference: `reference/v1/`

---

*Claude Sentient: Orchestrating Claude Code for autonomous development*
