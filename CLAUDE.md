# CLAUDE.md — Claude Sentient

> **Project:** Claude Sentient
> **Version:** 1.3.0
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

> Canonical reference for detection rules, gates, and conventions: `profiles/CLAUDE.md`

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

When a gate fails, the VERIFY phase runs an auto-fix sub-loop (max 3 attempts) before falling back to WebSearch.

> Gate definitions live in each `profiles/*.yaml` file. See `profiles/CLAUDE.md` for structure.

---

## Native Features We Use

| Feature | Native Tool |
|---------|-------------|
| Task Queue | `TaskCreate`, `TaskUpdate`, `TaskList`, `TaskGet` |
| Planning | `EnterPlanMode`, `ExitPlanMode` |
| Sub-agents | `Task` with `subagent_type` |
| Agent Teams | Team lead + teammates (experimental) |
| Memory | `.claude/rules/*.md` + MCP memory |
| Commands | `commands/*.md` + `Skill` tool |
| Hooks | `.claude/hooks/*.cjs` (13 hook scripts) |
| MCP Servers | context7, github, memory, filesystem, puppeteer |
| Web Tools | `WebSearch`, `WebFetch` |
| Vision | Screenshot analysis |

---

## Memory System

Uses the **official Claude Code pattern** — `.claude/rules/*.md` files are automatically loaded at session start.

| Location | Purpose | Shared? |
|----------|---------|---------|
| `.claude/rules/learnings.md` | Decisions, patterns, learnings | Yes (git) |
| `CLAUDE.md` | Project instructions | Yes (git) |
| `CLAUDE.local.md` | Personal preferences | No (gitignored) |
| `~/.claude/projects/<project>/memory/MEMORY.md` | Personal insights | No (auto memory) |

```bash
/cs-learn decision "Use PostgreSQL" "Chose for JSON support"
/cs-learn pattern "Error shape" "All errors return {error, message, code}"
/cs-learn learning "Avoid ORM" "Raw SQL 10x faster for bulk ops"
/cs-learn decision "Auth pattern" "Use JWT" --scope global    # Share across projects
/cs-learn learning "Docker" "Multi-stage builds" --scope org  # Share within org
```

---

## Rules Reference

@rules/_index.md

> Domain-specific rules in `.claude/rules/` use `paths:` frontmatter for conditional loading — they only load when Claude works on matching files. Universal rules (anthropic-patterns, code-quality, learnings) load every session.

---

## Governance Files

| File | Purpose | Updated By |
|------|---------|------------|
| `STATUS.md` | Current progress, what's done/next | `/cs-loop` (on complete) |
| `CHANGELOG.md` | Version history | Manual or on release |
| `DECISIONS.md` | Architecture Decision Records | `/cs-learn decision` |
| `.claude/rules/learnings.md` | Quick decisions, patterns | `/cs-learn` |

---

## Hard Rules

1. **Use native tools** — TaskCreate not custom queue, EnterPlanMode not custom planning
2. **Never skip gates** — Fix issues, don't bypass
3. **Create checkpoints** — Before risky changes
4. **Respect profiles** — Match existing code style
5. **Ask when ambiguous** — One question, then proceed

---

## Integrity Rules

**These rules prevent the most common Claude failure modes that frustrate users.**

### 1. Never Dismiss Errors as "Pre-existing"

- **Own it.** Investigate whether your changes caused or exposed it.
- **Never say** "this error was pre-existing" without proof (git blame, commit history).
- **If truly pre-existing:** Still report it clearly, don't use it as an excuse to skip quality gates.
- **Fix it or flag it** — either fix the issue or explicitly add it to a TODO with context.

### 2. No Workarounds or Quick Fixes

- **Solve the root cause**, not the symptom.
- **Never hard-code values** to make tests pass.
- **Never create "temporary" workarounds** — they become permanent.
- **If a proper fix is complex**, explain why and get user approval before proceeding.

### 3. Re-read CLAUDE.md Periodically

- Re-read `CLAUDE.md` and `.claude/rules/learnings.md` to refresh context.
- Check for architecture decisions in `DECISIONS.md` that affect your approach.
- **Never assume** you remember the rules — verify.

### 4. Verify Architecture Alignment

- Check if the change aligns with documented architecture decisions.
- Look for patterns in the existing codebase — match them, don't invent new ones.
- If your approach conflicts with existing patterns, **stop and ask** rather than proceeding.

### 5. Admit Mistakes Immediately

- **Acknowledge it clearly** — "I made a mistake" not "there was an issue."
- **Don't deflect** — no blaming "context limitations" or "the code was confusing."
- **Fix it and capture a learning** to prevent recurrence.

### 6. Never Gaslight

- **Don't claim** you said something you didn't.
- **Don't claim** the code does something it doesn't.
- **Don't claim** a test passes when it doesn't.
- **If uncertain**, say "I'm not sure" rather than making confident wrong statements.

---

## Self-Improvement

**When the user corrects you, update your rules so you don't make that mistake again.**

After any correction:
1. Acknowledge the correction
2. Fix the immediate issue
3. Propose a rule to prevent recurrence:
   - For project-specific patterns → append to `.claude/rules/learnings.md`
   - For fundamental behavior changes → propose edit to `CLAUDE.md`
4. Apply the rule update (with user confirmation for CLAUDE.md changes)

**Format for learnings.md:**
```markdown
### YYYY-MM-DD: [Short title]
- **Context**: What happened
- **Correction**: What the user said
- **Rule**: What to do differently
```

---

## Nested Context Architecture

Detailed documentation lives in nested CLAUDE.md files that load only when needed:

| Location | Content | When Loaded |
|----------|---------|-------------|
| `.claude/hooks/CLAUDE.md` | All 13 hooks, configuration, security patterns, state files | Editing hooks |
| `profiles/CLAUDE.md` | Profile detection, model routing, gate structure, conventions | Editing profiles |
| `.claude/commands/CLAUDE.md` | Command structure, documentation policy, rule auto-loading | Editing commands |
| `agents/CLAUDE.md` | Agent role definitions, YAML structure, custom agents | Editing agent configs |

This reduces root context from ~1000 lines to ~250 lines while keeping all detail accessible.

---

*Claude Sentient: Orchestrating Claude Code's native capabilities for autonomous development*
