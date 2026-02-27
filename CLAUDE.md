# CLAUDE.md — Claude Sentient

> **Project:** Claude Sentient
> **Version:** 1.4.0
> **Type:** Autonomous Development Orchestration Layer

---

## What Is This?

Claude Sentient is an **orchestration layer** that leverages Claude Code's native capabilities to work cohesively. It's not a replacement for Claude Code — it's a thin coordination layer that makes Claude Code's built-in features work together autonomously.

### Core Philosophy

1. **Native-First** — Use Claude Code's built-in tools, don't reinvent
2. **Autonomous by Default** — Only pause for ambiguity or risk
3. **Profile-Aware** — Adapts to project type (Python, TypeScript, Shell, Go, etc.)
4. **Quality-Enforced** — Blocking gates before commits
5. **Checkpoint-Safe** — Verified commits enable easy rollback

---

## Quick Start

```bash
/cs-loop "implement user authentication"    # Autonomous work loop
/cs-plan "refactor the API layer"           # Plan before executing
/cs-status                                  # Show tasks, git state, profile
/cs-validate                                # Verify configuration
/cs-learn decision "Use PostgreSQL" "JSON"  # Save to memory
/cs-mcp --fix                              # Register MCP servers
/cs-review 42                              # Review a pull request
/cs-init                                   # Create nested CLAUDE.md architecture
/cs-ui                                     # UI/UX audit (web projects)
/cs-team "refactor auth across packages"   # Parallel Agent Teams
/cs-assess                                 # Full codebase health audit
/cs-deploy                                 # Deployment readiness check
```

---

## The Loop

When you invoke `/cs-loop`, Claude Sentient orchestrates:

```
1. INIT       → Detect profile, load context, fetch library docs
2. UNDERSTAND → Classify complexity (simple/moderate/complex)
3. PLAN       → Create tasks (TaskCreate), evaluate team eligibility
4. EXECUTE    → Work through tasks (solo or team mode)
5. VERIFY     → Run quality gates (lint, test, build)
6. COMMIT     → Create checkpoint commit
7. EVALUATE   → Done? Exit. More work? Loop.
```

---

## Commands

| Command | Purpose |
|---------|---------|
| `/cs-loop [task]` | Autonomous work loop |
| `/cs-plan [task]` | Plan before executing |
| `/cs-status` | Show tasks, git state, profile |
| `/cs-validate` | Validate configuration |
| `/cs-learn [type] [title] [content]` | Save to memory (file + MCP) |
| `/cs-mcp [--test] [--fix]` | Check, register, validate MCP servers |
| `/cs-review [PR]` | Review a pull request |
| `/cs-assess [dir] [--ultrathink]` | Full codebase health audit |
| `/cs-init [dir]` | Create/optimize nested CLAUDE.md architecture |
| `/cs-ui [dir] [--full]` | UI/UX audit for web projects |
| `/cs-team [task] [--status] [--stop]` | Create/manage Agent Teams |
| `/cs-deploy [--ci] [--docker] [--env]` | Deployment readiness check |

> Detailed command structure and skill chaining: `.claude/commands/CLAUDE.md`

---

## Project Profiles

| Profile | Detected By | Tools |
|---------|-------------|-------|
| Python | `pyproject.toml`, `*.py` | ruff, pytest, pyright |
| TypeScript | `tsconfig.json`, `*.ts` | eslint, vitest, tsc |
| Go | `go.mod` | golangci-lint, go test |
| Rust | `Cargo.toml` | clippy, cargo test |
| Java | `pom.xml`, `build.gradle` | checkstyle, JUnit |
| C/C++ | `CMakeLists.txt`, `Makefile` | clang-tidy, ctest |
| Ruby | `Gemfile` | rubocop, rspec |
| Shell | `*.sh`, `*.ps1` | shellcheck |
| General | (fallback) | auto-detect |

> Profile details, model routing, gate structure: `profiles/CLAUDE.md`

---

## Quality Gates

Before committing, these must pass:

| Gate | Requirement | Auto-Fix |
|------|-------------|----------|
| **LINT** | Zero errors from linter | `fix_command` from profile (up to 3 attempts) |
| **TEST** | All tests pass | Read test + source, fix logic (never modify assertions) |
| **BUILD** | Project builds successfully | Read error, fix compilation |
| **GIT** | Clean working state | Stage changes |

Advisory (report only): TYPE, DOCS, SECURITY.

> Gate definitions live in each `profiles/*.yaml` file. See `profiles/CLAUDE.md` for structure.

---

## Hard Rules

1. **Use native tools** — TaskCreate not custom queue, EnterPlanMode not custom planning
2. **Never skip gates** — Fix issues, don't bypass
3. **Create checkpoints** — Before risky changes
4. **Respect profiles** — Match existing code style
5. **Ask when ambiguous** — One question, then proceed

> Integrity rules: `.claude/rules/anthropic-patterns.md` | Self-improvement: `.claude/rules/learnings.md`

---

## Reference

| Topic | Location |
|-------|----------|
| Memory system | `/cs-learn` command, `.claude/rules/learnings.md` |
| Governance files | `STATUS.md`, `CHANGELOG.md`, `DECISIONS.md` |
| Native tools used | `TaskCreate`, `EnterPlanMode`, `Task`, `.claude/hooks/*.cjs`, MCP servers |

See @rules/_index.md for keyword-to-rule mappings and the full rules catalog.

---

## Nested Context Architecture

Detailed documentation lives in nested CLAUDE.md files that load only when needed:

| Location | Content | When Loaded |
|----------|---------|-------------|
| `.claude/hooks/CLAUDE.md` | All 13 hooks, configuration, security patterns, state files | Editing hooks |
| `profiles/CLAUDE.md` | Profile detection, model routing, gate structure, conventions | Editing profiles |
| `.claude/commands/CLAUDE.md` | Command structure, documentation policy, rule auto-loading | Editing commands |
| `agents/CLAUDE.md` | Agent role definitions, YAML structure, custom agents | Editing agent configs |

---

*Claude Sentient: Orchestrating Claude Code's native capabilities for autonomous development*
