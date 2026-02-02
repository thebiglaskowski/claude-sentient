# CLAUDE.md — Claude Sentient

> **Project:** Claude Sentient
> **Version:** 0.3.0
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
| **Task Queue** | `TaskCreate`, `TaskUpdate`, `TaskList`, `TaskGet` | Work item tracking with dependencies |
| **Task Control** | `TaskStop`, `TaskOutput` | Background task timeouts and monitoring |
| **Planning** | `EnterPlanMode`, `ExitPlanMode` | Architecture decisions, complex tasks |
| **Sub-agents** | `Task` with `subagent_type` | Parallel research, exploration, background tasks |
| **Memory (File)** | `.claude/rules/*.md` | Persistent learnings across sessions |
| **Memory (MCP)** | `mcp__memory__search_nodes`, `open_nodes` | Searchable prior decisions |
| **Commands** | `commands/*.md` + `Skill` tool | Custom `/cs-*` commands |
| **Skill Chaining** | `Skill` tool | Commands invoke other commands |
| **Git** | Built-in git workflow | Commits, branches, PRs |
| **GitHub PR** | `mcp__github__get_pull_request*` | PR context, status, reviews |
| **GitHub Search** | `mcp__github__search_code` | Find reference implementations |
| **Web Tools** | `WebSearch`, `WebFetch` | Search for solutions, fetch changelogs |
| **Notebooks** | `NotebookEdit` | Jupyter notebook cell editing |
| **Questions** | `AskUserQuestion` (structured) | Decision points with predefined options |
| **MCP Servers** | `mcp__*` tools | Library docs, GitHub API, browser automation |

---

## Quick Start

```bash
# Main autonomous loop
/cs-loop "implement user authentication"

# Plan before executing (complex tasks)
/cs-plan "refactor the API layer"

# Check current status
/cs-status

# Validate configuration
/cs-validate

# Save a learning
/cs-learn decision "Use PostgreSQL" "Chose for JSON support"

# Check and fix MCP servers
/cs-mcp --fix

# Review a pull request
/cs-review 42

# UI/UX audit (web projects)
/cs-ui
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
| Python | `pyproject.toml`, `*.py`, `*.ipynb` | ruff, pytest, pyright, nbqa |
| TypeScript | `tsconfig.json`, `*.ts` | eslint, vitest, tsc |
| Go | `go.mod`, `*.go` | golangci-lint, go test |
| Rust | `Cargo.toml` | clippy, cargo test |
| Java | `pom.xml`, `build.gradle` | checkstyle, JUnit |
| C/C++ | `CMakeLists.txt`, `Makefile` | clang-tidy, ctest |
| Ruby | `Gemfile` | rubocop, rspec |
| Shell | `*.sh`, `*.ps1` | shellcheck |
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
| `/cs-validate` | Validate configuration |
| `/cs-learn [type] [title] [content]` | Save to memory (file + MCP) |
| `/cs-mcp [--test] [--fix]` | Check, register, and validate MCP servers |
| `/cs-review [PR]` | Review a pull request |
| `/cs-assess [dir] [--ultrathink]` | Full codebase health audit (6+ dimensions) |
| `/cs-ui [dir] [--full]` | UI/UX audit for web projects |

### Skill Chaining

Commands can invoke each other via the `Skill` tool:

| From | To | When |
|------|----|------|
| `/cs-plan` | `/cs-loop` | After plan approval, user chooses to execute |
| `/cs-status` | `/cs-loop` | When pending tasks exist, user chooses to continue |
| `/cs-validate` | `/cs-loop` | When issues found, user chooses to auto-fix |

---

## MCP Server Integration

MCP (Model Context Protocol) servers extend Claude Code with additional capabilities. `/cs-mcp` manages these servers.

### How MCP Servers Work

```
settings.json (configured)  →  claude mcp add (registered)  →  Available in session
      ↓                              ↓                              ↓
 User defines servers         Claude Code knows about them    mcp__* tools work
```

**Key insight:** Servers in `settings.json` must be registered with `claude mcp add` to work. The `/cs-mcp --fix` command detects this mismatch and fixes it.

### Available MCP Servers

| Server | Package | Env Vars | Purpose |
|--------|---------|----------|---------|
| context7 | `@upstash/context7-mcp` | - | Library documentation (used by `/cs-loop`) |
| github | `@modelcontextprotocol/server-github` | GITHUB_TOKEN | GitHub API (PRs, issues) |
| memory | `@modelcontextprotocol/server-memory` | - | Persistent key-value store |
| filesystem | `@modelcontextprotocol/server-filesystem` | - | File system access |
| puppeteer | `@modelcontextprotocol/server-puppeteer` | - | Browser automation |
| postgres | `@modelcontextprotocol/server-postgres` | DATABASE_URL | PostgreSQL database |
| brave-search | `@modelcontextprotocol/server-brave-search` | BRAVE_API_KEY | Web search |

### `/cs-mcp` Command

```bash
/cs-mcp              # Show status of all servers
/cs-mcp --test       # Test each connected server with real API call
/cs-mcp --fix        # Auto-register servers from settings.json
```

**What `--fix` does:**

1. Reads `~/.claude/settings.json` for `mcpServers` entries
2. Checks which are registered with `claude mcp get <name>`
3. For missing servers, runs `claude mcp add` or `claude mcp add-json`
4. Reports what was registered

**Registration commands:**

```bash
# Servers WITHOUT env vars
claude mcp add <name> -- npx -y <package> [args]

# Servers WITH env vars (use add-json for reliability)
claude mcp add-json <name> '{"command":"npx","args":["-y","<package>"],"env":{"KEY":"value"}}'
```

### MCP Server Scope

MCP servers are registered at the **user level** (`~/.claude.json`), not per-project:

- Register once → available in all projects
- `/cs-mcp --fix` only needed once per machine
- New projects automatically have access to registered servers

### Integration with `/cs-loop`

When Context7 is available, `/cs-loop` auto-fetches library documentation:

```
[INIT] Detected imports: fastapi, sqlalchemy, pydantic
[INIT] Loading docs from Context7...
[INIT] Loaded: FastAPI routing, SQLAlchemy ORM basics
```

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
├── .claude/
│   ├── commands/       # Active /cs-* commands (Claude Code loads these)
│   │   ├── cs-loop.md
│   │   ├── cs-plan.md
│   │   ├── cs-status.md
│   │   └── cs-learn.md
│   ├── rules/          # Memory (learnings.md)
│   └── settings.json   # Hooks and permissions
├── commands/           # Command source (copied to .claude/commands/)
├── profiles/           # Project type profiles (referenced by commands)
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
├── rules/              # Topic-specific standards (auto-loaded)
└── templates/          # Templates for governance files
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

## Integrity Rules

**These rules prevent the most common Claude failure modes that frustrate users.**

### 1. Never Dismiss Errors as "Pre-existing"

If you encounter an error during your work:
- **Own it.** Investigate whether your changes caused or exposed it.
- **Never say** "this error was pre-existing" without proof (git blame, commit history).
- **If truly pre-existing:** Still report it clearly, don't use it as an excuse to skip quality gates.
- **Fix it or flag it** — either fix the issue or explicitly add it to a TODO with context.

### 2. No Workarounds or Quick Fixes

When facing a problem:
- **Solve the root cause**, not the symptom.
- **Never hard-code values** to make tests pass.
- **Never create "temporary" workarounds** — they become permanent.
- **If a proper fix is complex**, explain why and get user approval before proceeding.

### 3. Re-read CLAUDE.md Periodically

At the start of significant work:
- Re-read `CLAUDE.md` and `.claude/rules/learnings.md` to refresh context.
- Check for architecture decisions in `DECISIONS.md` that affect your approach.
- **Never assume** you remember the rules — verify.

### 4. Verify Architecture Alignment

Before implementing changes:
- Check if the change aligns with documented architecture decisions.
- Look for patterns in the existing codebase — match them, don't invent new ones.
- If your approach conflicts with existing patterns, **stop and ask** rather than proceeding.

### 5. Admit Mistakes Immediately

When you make an error:
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

**Examples:**

| Correction | Rule Added |
|------------|------------|
| "Don't use `any` types" | Pattern: "Use explicit types, never `any`" |
| "Always run tests before committing" | Decision: "Run `npm test` before every commit" |
| "We use snake_case here" | Learning: "This project uses snake_case for variables" |

**Format for learnings.md:**
```markdown
### YYYY-MM-DD: [Short title]
- **Context**: What happened
- **Correction**: What the user said
- **Rule**: What to do differently
```

This is the Boris Cherny pattern: *"Claude is eerily good at writing rules for itself."*

---

## For Projects Using Claude Sentient

When applied to any project:

1. Claude Sentient commands become available (`/cs-loop`, etc.)
2. Project type is auto-detected
3. Learnings are stored in `.claude/rules/learnings.md`
4. Quality gates use profile-appropriate tools

No external dependencies. No custom scripts. Just Claude Code + thin orchestration.

---

## CLI vs SDK: Two Ways to Use Claude Sentient

Claude Sentient offers two modes of operation for different use cases.

### Overview

| Aspect | CLI Mode | SDK Mode |
|--------|----------|----------|
| **Entry point** | `/cs-loop "task"` in terminal | `ClaudeSentient.loop("task")` in code |
| **Installation** | One-line install script | `pip install -e` or `npm install` |
| **Use case** | Interactive development | Automation, CI/CD, scripts |
| **Session persistence** | Per-terminal session | Persists to `.claude/state/` |
| **User interaction** | Claude asks questions via terminal | Programmatic control, no prompts |
| **Best for** | Day-to-day development | Production pipelines, scheduled tasks |

### CLI Mode (Interactive Development)

**What it is:** Slash commands (`/cs-loop`, `/cs-plan`, etc.) that you run in Claude Code's terminal.

**How to install:**
```bash
# Linux/Mac
curl -fsSL https://raw.githubusercontent.com/thebiglaskowski/claude-sentient/main/install.sh | bash

# Windows PowerShell
iwr -useb https://raw.githubusercontent.com/thebiglaskowski/claude-sentient/main/install.ps1 | iex
```

**What gets installed:**
```
your-project/
├── .claude/commands/cs-*.md   # 5 slash commands
├── .claude/rules/learnings.md # Persistent memory
├── profiles/*.yaml            # Language profiles
└── templates/*.md             # Governance templates
```

**How it works:**
1. You type `/cs-loop "add user authentication"` in Claude Code
2. Claude reads the command file (`.claude/commands/cs-loop.md`)
3. Claude executes the loop: init → plan → execute → verify → commit
4. You interact with Claude as it works (answering questions, approving commits)
5. Session ends when you close the terminal

**When to use:**
- Daily development work
- Exploring a codebase
- Interactive code reviews
- Tasks where you want to guide Claude's decisions

---

### SDK Mode (Programmatic Automation)

**What it is:** Python/TypeScript libraries that let you run Claude Sentient from code.

**How to install:**
```bash
# Python (from claude-sentient repo)
pip install -e sdk/python/

# TypeScript (from claude-sentient repo)
cd sdk/typescript && npm install && npm run build

# Or direct import without install
import sys
sys.path.insert(0, "path/to/claude-sentient/sdk/python")
```

**How it works:**
1. Your script creates a `ClaudeSentient` instance
2. Calls `loop()`, `plan()`, or `resume()` methods
3. SDK manages session state in `.claude/state/session.json`
4. Quality gates run as hooks (lint on file change, test before commit)
5. Session can be resumed later, even after terminal closes

**When to use:**
- CI/CD pipelines (run Claude Sentient on every PR)
- Scheduled tasks (nightly refactoring, dependency updates)
- Webhooks (trigger Claude Sentient from external events)
- Scripts that need to resume work across sessions
- Headless/automated environments

**Example use cases:**

```python
# CI/CD: Run on every PR
async def ci_check(pr_branch: str):
    sentient = ClaudeSentient(cwd="./repo")
    async for result in sentient.loop(f"Review changes in {pr_branch}"):
        if not result.gates_passed.get("lint"):
            raise Exception("Lint failed")
        if not result.gates_passed.get("test"):
            raise Exception("Tests failed")

# Scheduled: Nightly maintenance
async def nightly_maintenance():
    sentient = ClaudeSentient(cwd="./repo")
    async for result in sentient.loop("Update dependencies and fix deprecations"):
        print(f"Completed: {result.commit_hash}")

# Resumable: Long-running task
async def long_task():
    sentient = ClaudeSentient(cwd="./repo")

    # Start or resume
    try:
        async for result in sentient.resume():
            print(f"Resumed from {result.phase}")
    except ValueError:
        async for result in sentient.loop("Large refactoring task"):
            print(f"Phase: {result.phase}")
```

---

### Key Differences

**Session Persistence:**
- CLI: Session lives in terminal. Close terminal = lose context.
- SDK: Session saved to `.claude/state/session.json`. Resume anytime with `sentient.resume()`.

**User Interaction:**
- CLI: Claude can ask you questions, you see output in real-time.
- SDK: Non-interactive by default. Configure hooks for custom behavior.

**Quality Gates:**
- CLI: Gates run as part of the loop, Claude reports results.
- SDK: Gates run as hooks (`PostToolUse`, `PreToolUse`), can block commits programmatically.

**Installation Scope:**
- CLI: Installs into a specific project (`.claude/commands/`).
- SDK: Installed globally or per-environment via pip/npm.

---

### Using Both Together

You can use both modes on the same project:

1. **Install CLI** for interactive development:
   ```bash
   curl -fsSL .../install.sh | bash
   ```

2. **Use SDK** for automation:
   ```python
   # CI pipeline
   sentient = ClaudeSentient(cwd="./my-project")
   async for result in sentient.loop("Run pre-merge checks"):
       ...
   ```

Both share:
- Same `profiles/*.yaml` configuration
- Same `.claude/rules/learnings.md` memory
- Same quality gate definitions

---

## SDK Reference

### Installation

**Python (from repo):**
```bash
pip install -e sdk/python/
```

For library usage (`from claude_sentient import ClaudeSentient`), no PATH change is needed.

For CLI commands (`claude-sentient`, `cs`), add the Scripts directory to PATH:
```bash
# Windows PowerShell (use path from pip warning)
$env:PATH += ";C:\Users\<you>\AppData\Local\...\Python313\Scripts"

# Linux/Mac
export PATH="$HOME/.local/bin:$PATH"
```

**TypeScript (from repo):**
```bash
cd sdk/typescript && npm install && npm run build
```

To use in other projects, link the package:
```bash
# In sdk/typescript directory
npm link

# In your consuming project
npm link @claude-sentient/sdk
```

Or add to your project's `package.json`:
```json
{ "dependencies": { "@claude-sentient/sdk": "file:/path/to/sdk/typescript" } }
```

**Direct import (no install):**
```python
import sys
sys.path.insert(0, "path/to/claude-sentient/sdk/python")
from claude_sentient import ClaudeSentient
```

### Basic Usage

**Python:**
```python
from claude_sentient import ClaudeSentient

async def main():
    sentient = ClaudeSentient(cwd="./my-project")

    # Run the autonomous loop
    async for result in sentient.loop("Add user authentication"):
        print(f"Phase: {result.phase}, Tasks: {result.tasks_completed}")
        if result.success:
            print(f"Done! Commit: {result.commit_hash}")

    # Or plan without executing
    plan = await sentient.plan("Refactor the API layer")

    # Resume a previous session
    async for result in sentient.resume():
        print(f"Resumed: {result.phase}")
```

**TypeScript:**
```typescript
import { ClaudeSentient } from "@claude-sentient/sdk";

const sentient = new ClaudeSentient({ cwd: "./my-project" });

for await (const result of sentient.loop("Add user authentication")) {
  console.log(`Phase: ${result.phase}, Tasks: ${result.tasksCompleted}`);
  if (result.success) {
    console.log(`Done! Commit: ${result.commitHash}`);
  }
}
```

### SDK Features

| Feature | Description |
|---------|-------------|
| **Session Persistence** | Resume work across terminal closures via `.claude/state/session.json` |
| **Programmatic Control** | SDK-based orchestration for CI/CD, webhooks, scheduled tasks |
| **Quality Gate Hooks** | Automated lint/test enforcement as SDK hooks |
| **Profile Detection** | Auto-detect project type from files |
| **Subagent Definitions** | Pre-configured agents for exploration, testing, lint-fixing |

### Dual-Mode Architecture

| Mode | Entry Point | Use Case |
|------|-------------|----------|
| CLI | `/cs-loop`, `/cs-plan` | Interactive development |
| SDK | `ClaudeSentient.loop()` | Production automation |

Both modes share the same profiles, quality gates, and session state.

### SDK Directory Structure

```
sdk/
├── python/
│   ├── claude_sentient/
│   │   ├── __init__.py       # Package exports
│   │   ├── orchestrator.py   # Main ClaudeSentient class
│   │   ├── session.py        # Session persistence
│   │   ├── profiles.py       # Profile detection/loading
│   │   ├── gates.py          # Quality gate execution
│   │   ├── hooks.py          # Custom hook definitions
│   │   └── types.py          # Dataclasses
│   ├── pyproject.toml
│   └── README.md
│
└── typescript/
    ├── src/
    │   ├── index.ts          # Package exports
    │   ├── orchestrator.ts   # Main class
    │   ├── session.ts        # Session persistence
    │   ├── profiles.ts       # Profile detection
    │   ├── gates.ts          # Quality gates
    │   ├── hooks.ts          # Hook definitions
    │   └── types.ts          # Type definitions
    ├── package.json
    └── README.md
```

See `sdk/python/README.md` and `sdk/typescript/README.md` for full API documentation.

---

*Claude Sentient: Orchestrating Claude Code's native capabilities for autonomous development*
