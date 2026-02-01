# CLAUDE.md — Claude Sentient

> **Project:** Claude Sentient
> **Version:** 0.2.0
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

## Native Features We Use

Claude Sentient leverages these **built-in Claude Code capabilities**:

| Feature | Native Tool | How We Use It |
|---------|-------------|---------------|
| **Task Queue** | `TaskCreate`, `TaskUpdate`, `TaskList` | Work item tracking with dependencies |
| **Planning** | `EnterPlanMode`, `ExitPlanMode` | Architecture decisions, complex tasks |
| **Sub-agents** | `Task` with `subagent_type` | Parallel research, exploration, background tasks |
| **Memory** | `.claude/rules/*.md` | Persistent learnings across sessions |
| **Commands** | `commands/*.md` + `Skill` tool | Custom `/cs-*` commands |
| **Git** | Built-in git workflow | Commits, branches, PRs |

---

## Quick Start

```bash
# Main autonomous loop
/cs-loop "implement user authentication"

# Plan before executing (complex tasks)
/cs-plan "refactor the API layer"

# Check current status
/cs-status

# Save a learning
/cs-learn decision "Use PostgreSQL" "Chose for JSON support"
```

---

## The Loop

When you invoke `/cs-loop`, Claude Sentient orchestrates:

```
1. INIT       → Detect profile, load context
2. UNDERSTAND → Classify request, assess scope
3. PLAN       → Create tasks (TaskCreate), set dependencies
4. EXECUTE    → Work through tasks, update status
5. VERIFY     → Run quality gates (lint, test, build)
6. COMMIT     → Create checkpoint commit
7. EVALUATE   → Done? Exit. More work? Loop.
```

---

## Project Profiles

Sentient auto-detects project type and loads appropriate tooling:

| Profile | Detected By | Tools |
|---------|-------------|-------|
| Python | `pyproject.toml`, `*.py` | ruff, pytest, pyright |
| TypeScript | `tsconfig.json`, `*.ts` | eslint, vitest, tsc |
| Shell | `*.sh`, `*.ps1` | shellcheck |
| Go | `go.mod`, `*.go` | golangci-lint, go test |
| General | (fallback) | auto-detect |

Profiles live in `profiles/*.yaml` and define:
- Detection rules
- Lint/test/build commands
- Quality thresholds
- Conventions

---

## Quality Gates

Before committing, these must pass:

### Blocking (MVP)
- **LINT** — Zero errors from linter
- **TEST** — All tests pass
- **BUILD** — Project builds successfully
- **GIT** — Clean working state

### Advisory (Report Only)
- **TYPE** — Type checking (if applicable)
- **DOCS** — Documentation present
- **SECURITY** — No obvious vulnerabilities

---

## Commands

| Command | Purpose |
|---------|---------|
| `/cs-loop [task]` | Autonomous work loop |
| `/cs-plan [task]` | Plan before executing |
| `/cs-status` | Show tasks, git state, profile |
| `/cs-learn [type] [title] [content]` | Save to memory |

---

## Memory System

Uses the **official Claude Code pattern** — `.claude/rules/*.md` files are automatically loaded at session start.

### Locations

| Location | Purpose | Shared? |
|----------|---------|---------|
| `.claude/rules/learnings.md` | Decisions, patterns, learnings | Yes (git) |
| `CLAUDE.md` | Project instructions | Yes (git) |
| `CLAUDE.local.md` | Personal preferences | No (gitignored) |

### Capturing Learnings

```bash
/cs-learn decision "Use PostgreSQL" "Chose for JSON support"
/cs-learn pattern "Error shape" "All errors return {error, message, code}"
/cs-learn learning "Avoid ORM" "Raw SQL 10x faster for bulk ops"
```

---

## Directory Structure

```
claude-sentient/
├── commands/           # /cs-* command definitions
│   ├── cs-loop.md
│   ├── cs-plan.md
│   ├── cs-status.md
│   └── cs-learn.md
├── profiles/           # Project type profiles
│   ├── python.yaml
│   ├── typescript.yaml
│   └── general.yaml
├── templates/          # Templates for governance files
│   ├── STATUS.md
│   ├── CHANGELOG.md
│   ├── DECISIONS.md
│   └── learnings.md
├── phases/             # Phase documentation
├── reference/          # Planning docs, deferred features
└── .claude/
    ├── rules/          # Memory (learnings.md)
    └── settings.json   # Hooks and permissions
```

---

## Governance Files

Claude Sentient creates and maintains these files for project continuity:

| File | Purpose | Updated By |
|------|---------|------------|
| `STATUS.md` | Current progress, what's done/next | `/cs-loop` (on complete) |
| `CHANGELOG.md` | Version history | Manual or on release |
| `DECISIONS.md` | Architecture Decision Records | `/cs-learn decision` or manual |
| `.claude/rules/learnings.md` | Quick decisions, patterns | `/cs-learn` |

These files bridge session gaps — when Claude starts fresh, it reads these to understand context.

---

## Hooks

Claude Sentient uses Claude Code's hook system for session logging:

```json
// .claude/settings.json
{
  "hooks": {
    "UserPromptSubmit": [{ "command": "echo '[cs] Prompt received' >> .claude/session.log" }],
    "Stop": [{ "command": "echo '[cs] Session ended' >> .claude/session.log" }]
  }
}
```

Available hook points:
- `SessionStart` / `SessionEnd` — Session lifecycle
- `UserPromptSubmit` — When user sends message (inject context)
- `PreToolUse` / `PostToolUse` — Before/after tools (safety checks)
- `Stop` — When Claude finishes (session summary)

See `reference/HOOKS.md` for advanced examples.

---

## Sub-agents

Claude Sentient uses Claude Code's Task tool for parallel and background work:

| Subagent Type | Use For | Model |
|---------------|---------|-------|
| `Explore` | Fast codebase search, file finding | Haiku |
| `Plan` | Research before planning decisions | Read-only |
| `general-purpose` | Complex multi-step tasks | Sonnet |
| `Bash` | Command execution in isolation | - |

**Background execution:**
```yaml
Task:
  subagent_type: general-purpose
  prompt: "Run the full test suite"
  run_in_background: true  # Don't wait, continue working
```

Use `TaskOutput(task_id)` to check results later.

---

## Library Documentation (Context7)

When the Context7 MCP server is available, `/cs-loop` auto-fetches documentation for libraries:

```
[INIT] Detected imports: fastapi, sqlalchemy, pydantic
[INIT] Loading docs from Context7...
[INIT] Loaded: FastAPI routing, SQLAlchemy ORM basics
```

**How it works:**
1. Scan task-related files for imports
2. Identify unfamiliar libraries
3. Call `mcp__context7__resolve-library-id` to find the library
4. Call `mcp__context7__query-docs` with relevant query
5. Inject documentation into context

**Manual usage:**
```
/cs-loop "add OAuth to the API"
# Context7 auto-fetches OAuth library docs
```

This reduces hallucination and ensures up-to-date API usage.

---

## How It Works

### 1. You invoke `/cs-loop "add user auth"`

### 2. Init Phase
- Detect project type (finds `pyproject.toml` → Python)
- Load profile (ruff, pytest, pyright)
- Load memory from `.claude/rules/`

### 3. Plan Phase
- Use `TaskCreate` to create work items
- Set dependencies with `TaskUpdate`
- For complex tasks, use `EnterPlanMode`

### 4. Execute Phase
- Work through tasks in dependency order
- Update status with `TaskUpdate`
- Use `Task` subagents for parallel work

### 5. Verify Phase
- Run lint: `ruff check .`
- Run tests: `pytest`
- Run build: `python -m build` (if applicable)

### 6. Commit Phase
- Create checkpoint commit
- Follow git commit guidelines

### 7. Evaluate Phase
- Check `TaskList` for remaining work
- If empty and gates pass → Done
- If more work → Loop to Execute

---

## Documentation Policy

Claude Sentient automates documentation based on task context:

### Automation Levels

| Level | When | Examples |
|-------|------|----------|
| **Fully Auto** | Low risk, high value | Rule loading, STATUS.md updates |
| **Auto + Confirm** | Significant changes | CHANGELOG entries, version bumps |
| **On Request** | User preference | Full docs rewrites, ADRs |

### Auto-Update Triggers

| Change Type | STATUS.md | CHANGELOG.md | DECISIONS.md |
|-------------|-----------|--------------|--------------|
| Feature added | ✓ Auto | ✓ Confirm | Only if architectural |
| Bug fixed | ✓ Auto | ✓ Confirm | — |
| Refactoring | ✓ Auto | — | If significant |
| Breaking change | ✓ Auto | ✓ Confirm (required) | ✓ Required |
| Config change | ✓ Auto | — | — |

### Rule Auto-Loading

During `/cs-loop` INIT, rules are loaded based on task keywords:

| Task Keywords | Rules Loaded |
|---------------|--------------|
| auth, login, jwt | `security`, `api-design` |
| test, coverage, mock | `testing` |
| api, endpoint, rest | `api-design`, `error-handling` |
| database, query | `database` |
| performance, cache | `performance` |
| ui, component | `ui-ux-design` |

Full mapping: `rules/_index.md`

---

## Hard Rules

1. **Use native tools** — TaskCreate not custom queue, EnterPlanMode not custom planning
2. **Never skip gates** — Fix issues, don't bypass
3. **Create checkpoints** — Before risky changes
4. **Respect profiles** — Match existing code style
5. **Ask when ambiguous** — One question, then proceed

---

## For Projects Using Claude Sentient

When applied to any project:

1. Claude Sentient commands become available (`/cs-loop`, etc.)
2. Project type is auto-detected
3. Learnings are stored in `.claude/rules/learnings.md`
4. Quality gates use profile-appropriate tools

No external dependencies. No custom scripts. Just Claude Code + thin orchestration.

---

*Claude Sentient: Orchestrating Claude Code's native capabilities for autonomous development*
