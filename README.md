<p align="center">
  <img src="assets/claude-sentient.png" alt="Claude Sentient" width="400">
</p>

# Claude Sentient

> **Autonomous development orchestration for Claude Code**

Claude Sentient coordinates Claude Code's native capabilities into an autonomous development workflow. It's not a replacement — it's a thin orchestration layer that makes built-in tools work together cohesively.

[![Version](https://img.shields.io/badge/version-1.3.0-blue.svg)](CHANGELOG.md)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Compatible-green.svg)](https://claude.ai)
[![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)](LICENSE)
[![Profiles](https://img.shields.io/badge/profiles-9-orange.svg)](profiles/)

---

## ⚠️ Important Notice

**This is an experimental orchestration framework.** Claude Sentient provides prompts, profiles, and configurations designed to enhance Claude Code workflows. Results may vary.

- **Not a guarantee** — These prompts guide Claude but don't guarantee specific outcomes
- **Your responsibility** — Always review Claude's output before committing changes
- **Evolving project** — Expect changes between versions
- **Native-first** — Uses Claude Code's built-in tools, not custom replacements

---

## 🤖 What is Claude Sentient?

Claude Sentient transforms Claude Code sessions into **autonomous development loops**:

```
USER REQUEST → INIT → PLAN → EXECUTE → VERIFY → COMMIT → DONE
                ↓        ↓         ↓         ↓
           Profile   TaskCreate  Work    Quality
           Detection            Items    Gates
```

**Philosophy:** Claude Code already has task management, planning modes, sub-agents, and memory. We don't reinvent these — we orchestrate them.

---

## ⚡ Quick Start

### One-Line Install

**Bash (Linux/Mac):**
```bash
curl -fsSL https://raw.githubusercontent.com/thebiglaskowski/claude-sentient/main/install.sh | bash
```

**PowerShell (Windows):**
```powershell
iwr -useb https://raw.githubusercontent.com/thebiglaskowski/claude-sentient/main/install.ps1 | iex
```

### After Installation

```bash
/cs-validate              # Verify setup
/cs-status                # See detected profile
/cs-loop "your task"      # Start working
```

### Uninstall

**Bash (Linux/Mac):**
```bash
curl -fsSL https://raw.githubusercontent.com/thebiglaskowski/claude-sentient/main/uninstall.sh | bash
```

**PowerShell (Windows):**
```powershell
iwr -useb https://raw.githubusercontent.com/thebiglaskowski/claude-sentient/main/uninstall.ps1 | iex
```

**Or run locally:**
```bash
./uninstall.sh                # Standard uninstall
./uninstall.sh --dry-run      # Preview what would be removed
./uninstall.sh --purge        # Also remove learnings.md
./uninstall.sh --keep-settings  # Don't touch .claude/settings.json
```

By default, `learnings.md` (your decisions/patterns) is preserved and `settings.json` is backed up to `.bak`. `CLAUDE.md` is left for manual removal.

---

## 📊 By the Numbers

| Component | Count | Purpose |
|-----------|-------|---------|
| 🎯 Commands | 12 | Slash commands (`/cs-*`) |
| 📋 Profiles | 9 | Language-specific quality gates |
| 📏 Rules | 15 | Topic-specific standards |
| 📄 Templates | 4 | Governance file templates |
| 🚦 Quality Gates | 4 | Lint, test, build, git (with auto-fix) |
| 🔄 Loop Phases | 7 | INIT → EVALUATE |
| 🎣 Hooks | 12 | Session lifecycle, security, teams, tracking |
| 🧪 Tests | 761 | Profiles (242), agents (108), hooks (125), commands (81), schemas (166), integration (39) |
| 🤖 Agent Roles | 6 | Security, devops, frontend, backend, tester, architect |

---

## 🎯 Commands

| Command | Purpose | Docs |
|---------|---------|------|
| `/cs-loop` | Autonomous loop: understand → plan → execute → verify → commit | [Details](CLAUDE.md#the-loop) |
| `/cs-plan` | Plan complex tasks before executing (chains to cs-loop) | [Command](.claude/commands/cs-plan.md) |
| `/cs-status` | Show tasks, git state, profile (can resume work) | [Command](.claude/commands/cs-status.md) |
| `/cs-validate` | Validate configuration (can auto-fix issues) | [Command](.claude/commands/cs-validate.md) |
| `/cs-learn` | Save learnings to file + MCP memory (searchable) | [Memory System](CLAUDE.md#memory-system) |
| `/cs-mcp` | Check, register, and validate MCP servers | [MCP Integration](CLAUDE.md#mcp-server-integration) |
| `/cs-review` | Review pull requests with automated analysis | [Command](.claude/commands/cs-review.md) |
| `/cs-assess` | Full codebase health audit (6+ dimensions) | [Command](.claude/commands/cs-assess.md) |
| `/cs-init` | Create/optimize nested CLAUDE.md architecture | [Command](.claude/commands/cs-init.md) |
| `/cs-ui` | UI/UX audit for web projects | [Command](.claude/commands/cs-ui.md) |
| `/cs-team` | Create/manage Agent Teams for parallel work | [Command](.claude/commands/cs-team.md) |
| `/cs-deploy` | Deployment readiness check (CI, Docker, env, migrations) | [Command](.claude/commands/cs-deploy.md) |

---

## 📋 Profile Detection

Sentient auto-detects your project type and loads appropriate tooling. See [`profiles/`](profiles/) for full configurations.

| Profile | Detected By | Tools | Config |
|---------|-------------|-------|--------|
| Python | `pyproject.toml`, `*.py` | ruff, pytest, pyright | [python.yaml](profiles/python.yaml) |
| TypeScript | `tsconfig.json`, `*.ts` | eslint, vitest, tsc | [typescript.yaml](profiles/typescript.yaml) |
| Go | `go.mod`, `*.go` | golangci-lint, go test | [go.yaml](profiles/go.yaml) |
| Rust | `Cargo.toml` | clippy, cargo test | [rust.yaml](profiles/rust.yaml) |
| Java | `pom.xml`, `build.gradle` | checkstyle, JUnit | [java.yaml](profiles/java.yaml) |
| C/C++ | `CMakeLists.txt`, `Makefile` | clang-tidy, ctest | [cpp.yaml](profiles/cpp.yaml) |
| Ruby | `Gemfile` | rubocop, rspec | [ruby.yaml](profiles/ruby.yaml) |
| Shell | `*.sh`, `*.ps1` | shellcheck | [shell.yaml](profiles/shell.yaml) |
| General | (fallback) | auto-detect | [general.yaml](profiles/general.yaml) |

### Python Environment Detection

For Python projects, Sentient detects and uses the correct environment:

| Indicator | Environment | How Commands Run |
|-----------|-------------|------------------|
| `environment.yml` | Conda | `conda run -n <env> pytest` |
| `.venv/`, `venv/` | Virtualenv | Uses venv's Python |
| `poetry.lock` | Poetry | `poetry run pytest` |
| `pdm.lock` | PDM | `pdm run pytest` |

---

## 🔄 The Loop

When you run `/cs-loop`, Claude Sentient orchestrates:

```
Phase 1: INIT       → Detect profile, load rules, check governance
Phase 2: UNDERSTAND → Classify complexity (simple/moderate/complex)
Phase 3: PLAN       → Create tasks via TaskCreate
Phase 4: EXECUTE    → Work through tasks, update status
Phase 5: VERIFY     → Run quality gates (lint, test, build)
Phase 6: COMMIT     → Create checkpoint commit
Phase 7: EVALUATE   → Done? Exit. More work? Loop.
```

### 🚦 Quality Gates

All gates must pass before committing:

| Gate | Requirement |
|------|-------------|
| ✅ LINT | Zero errors from linter |
| ✅ TEST | All tests pass |
| ✅ BUILD | Project builds successfully |
| ✅ GIT | Clean working state |

---

## 🔌 Native Tools Used

Claude Sentient leverages built-in Claude Code features:

| Feature | Native Tool | How Used |
|---------|-------------|----------|
| Task Queue | `TaskCreate`, `TaskUpdate`, `TaskList`, `TaskGet` | Work tracking |
| Task Control | `TaskStop`, `TaskOutput` | Background task timeouts |
| Planning | `EnterPlanMode`, `ExitPlanMode` | Complex tasks |
| Sub-agents | `Task` with `subagent_type` | Parallel work |
| Memory (File) | `.claude/rules/*.md` | Persistent learnings |
| Memory (MCP) | `search_nodes`, `open_nodes` | Searchable prior decisions |
| Skill Chaining | `Skill` tool | Commands invoke each other |
| Agent Teams | Team lead + teammates | Parallel multi-instance work |
| Web Tools | `WebSearch`, `WebFetch` | Find fixes, fetch changelogs |
| GitHub PR | `get_pull_request*`, `create_review` | Full PR workflow |
| GitHub Search | `search_code` | Find reference implementations |
| Questions | `AskUserQuestion` | Structured decision options |
| MCP Servers | `mcp__*` tools | Library docs, GitHub, memory |

---

## 🔗 MCP Server Integration

Claude Sentient can leverage MCP (Model Context Protocol) servers for extended capabilities. See [full MCP documentation](CLAUDE.md#mcp-server-integration) for details.

| Server | Purpose | Auto-Used By |
|--------|---------|--------------|
| **context7** | Library documentation | `/cs-loop` INIT (fetches docs for imports) |
| **github** | GitHub API (PRs, issues, code search) | `/cs-loop` INIT/VERIFY, `/cs-review` |
| **memory** | Searchable knowledge graph | `/cs-loop` INIT (search prior decisions), `/cs-learn` |
| **filesystem** | File system access | Manual |
| **puppeteer** | Browser automation | `/cs-loop` VERIFY (web projects) |

### Setup MCP Servers

```bash
/cs-mcp              # Check what's configured vs connected
/cs-mcp --fix        # Auto-register servers from settings.json
/cs-mcp --test       # Validate servers are responding
```

**Note:** MCP servers are registered at the user level (`~/.claude.json`). Once registered, they're available in all projects.

---

## 🔌 Plugins

The installer auto-installs recommended plugins from the Claude Code official marketplace when the `claude` CLI is available. Plugin installation is non-fatal — if `claude` isn't found or a plugin fails to install, setup continues normally.

### Auto-Installed Plugins

**Security Guidance** (all projects, user scope):

`security-guidance@claude-plugins-official` scans file content for security anti-patterns like `eval()`, `pickle.loads()`, unsanitized HTML injection, and hardcoded secrets. It complements the bash-validator and file-validator hooks that ship with Claude Sentient by catching patterns at the content level rather than the command level.

**LSP Plugins** (profile-dependent, project scope):

Each language profile declares a recommended LSP plugin that gives Claude deeper understanding of your code — real-time type information, symbol resolution, and diagnostics that go beyond static file reading.

| Profile | Plugin | What It Adds |
|---------|--------|-------------|
| Python | `pyright-lsp` | Type inference, import resolution, missing attribute detection |
| TypeScript | `typescript-lsp` | Type checking, module resolution, refactoring support |
| Go | `gopls-lsp` | Type analysis, interface satisfaction, unused variable detection |
| Rust | `rust-analyzer-lsp` | Borrow checker insights, trait resolution, macro expansion |
| Java | `jdtls-lsp` | Class hierarchy, dependency analysis, annotation processing |
| C/C++ | `clangd-lsp` | Header resolution, compile command awareness, memory safety hints |
| Ruby, Shell, General | — | No LSP plugin (profile tools handle linting directly) |

### Recommended Plugins (Optional)

These are not auto-installed but are shown in the installer summary for manual setup:

```bash
claude plugin install pr-review-toolkit@claude-plugins-official   # Enhanced PR review workflows
claude plugin install ralph-loop@claude-plugins-official           # Advanced loop orchestration
```

### Checking Plugin Status

Run `/cs-validate` to see which plugins are installed and which are missing. The PLUGINS advisory section shows installed, missing, and optional plugins with one-liner install commands.

---

## 📁 Project Structure

```
your-project/
├── .claude/
│   ├── commands/cs-*.md    # 12 slash commands
│   ├── hooks/*.cjs         # 13 hook scripts (security, teams, tracking)
│   ├── settings.json       # Hook + team configuration
│   └── rules/*.md          # Path-scoped rules + learnings
├── profiles/*.yaml          # 9 language profiles + schema
├── agents/*.yaml            # 6 specialized agent roles
├── schemas/*.json           # 9 JSON schemas (validation)
├── templates/*.md           # Governance templates
├── test-utils.js            # Shared test infrastructure
└── rules/*.md               # 15 topic rules
```

---

## 🛠️ Common Workflows

### Workflow 1: Feature Development

```bash
# 1. Start with planning for complex features
/cs-plan "add JWT authentication"

# Claude explores codebase, creates a plan, asks for approval
# After approval, you can execute immediately or later:

# 2. Execute the plan
/cs-loop "implement the JWT auth plan"

# Claude: INIT → detects TypeScript profile
#         PLAN → creates tasks with dependencies
#         EXECUTE → implements auth module, tests, docs
#         VERIFY → runs eslint, vitest
#         COMMIT → creates checkpoint "feat: add JWT authentication"
```

### Workflow 2: Bug Fix

```bash
# For simpler bugs, go straight to loop
/cs-loop "fix the race condition in user login #142"

# Claude automatically:
# - Fetches issue #142 details via MCP github
# - Investigates the code
# - Creates minimal fix
# - Runs tests
# - Commits with "fix: resolve login race condition (closes #142)"
```

### Workflow 3: Code Review + Fix

```bash
# 1. Review a PR
/cs-review 47

# Claude analyzes PR #47, provides detailed feedback with file:line refs

# 2. If issues found, fix them
/cs-loop "address review comments on PR #47"
```

### Workflow 4: Codebase Health Check

```bash
# 1. Full assessment
/cs-assess

# Claude provides scores (1-10) for:
# - Architecture, Code Quality, Security
# - Performance, Tech Debt, Test Coverage
# - UI/UX (for web projects)

# 2. Address issues
/cs-loop "fix all immediate priority items from assessment"
```

### Workflow 5: Learning from Mistakes

```bash
# Claude makes a mistake, you correct it
> "Don't use any types in this project"

# Save the learning for future sessions
/cs-learn pattern "No any types" "Use explicit types, never any"

# Or Claude proposes it after correction:
# "Should I add a rule to prevent this?"
```

### Workflow 6: Resuming Work

```bash
# Check where you left off
/cs-status

# Shows: Profile, Tasks (3 pending, 1 in progress), Git state

# Continue from where you stopped
/cs-loop "continue"  # Or just describe what's next
```

### Workflow 7: UI/UX Audit (Web Projects)

```bash
# For React/Vue/Next.js projects
/cs-ui

# Claude audits against modern design standards:
# - Spacing (8px grid), Typography, Colors
# - Components, Accessibility, Responsiveness
# - Provides before/after code examples
```

### Workflow 8: Context Architecture

```bash
# Create CLAUDE.md for a new project
/cs-init

# Claude analyzes project, detects tech stack, creates:
# - Root CLAUDE.md (overview, quality philosophy, tech stack)
# - Nested CLAUDE.md files for significant directories
# - Zero-tolerance quality philosophy injected by default

# Or optimize an existing monolithic CLAUDE.md
/cs-init  # Detects existing CLAUDE.md, offers to split into nested files
```

### Workflow 9: Parallel Work with Agent Teams

```bash
# For large tasks across multiple packages/modules
/cs-loop "refactor auth across all packages"

# cs-loop detects 6 independent tasks across 3 packages
# Offers team mode: "3 parallel teammates. Use Agent Teams?"
# If yes: spawns teammates, each owns a package
# Lead coordinates, teammates work in parallel
# Quality gates enforced via TeammateIdle/TaskCompleted hooks

# Or create a team manually
/cs-team "investigate performance bottleneck from 3 angles"

# Check team status
/cs-team --status

# Stop and cleanup
/cs-team --stop
```

### Workflow 10: MCP Server Setup

```bash
# First time setup
/cs-mcp --fix      # Auto-register servers from settings.json
/cs-mcp --test     # Verify all servers respond

# Now /cs-loop will:
# - Fetch library docs via Context7
# - Link commits to GitHub issues
# - Search prior decisions from Memory
```

---

## 🎣 Hooks

Claude Sentient includes 13 hook scripts that integrate with Claude Code's hook system:

| Hook | Event | Purpose |
|------|-------|---------|
| `session-start.cjs` | SessionStart | Initialize session, detect profile, create state |
| `session-end.cjs` | SessionEnd | Archive session, cleanup state files |
| `context-injector.cjs` | UserPromptSubmit | Detect topics (auth, test, API), inject context |
| `bash-validator.cjs` | PreToolUse (Bash) | Block dangerous commands (`rm -rf /`, fork bombs) |
| `file-validator.cjs` | PreToolUse (Write/Edit) | Protect system paths, SSH keys, credentials |
| `post-edit.cjs` | PostToolUse (Write/Edit) | Track file changes, suggest lint |
| `agent-tracker.cjs` | SubagentStart | Track subagent spawning |
| `agent-synthesizer.cjs` | SubagentStop | Synthesize agent results, record history |
| `pre-compact.cjs` | PreCompact | Backup state before context compaction |
| `dod-verifier.cjs` | Stop | Verify Definition of Done, save final state |
| `teammate-idle.cjs` | TeammateIdle | Quality check before teammate goes idle |
| `task-completed.cjs` | TaskCompleted | Validate deliverables before task completion |

Hooks are configured in `.claude/settings.json` and installed automatically.

---

## 🧪 Tests

Test suites validate hooks, profiles, commands, agents, schemas, and cross-module integrity:

```bash
# Profile validation (242 tests) — schema compliance, gates, infrastructure, cross-profile consistency
node profiles/__tests__/test-profiles.js

# Agent validation (108 tests) — YAML schema, roles, expertise, spawn_prompts
node agents/__tests__/test-agents.js

# Hook tests (101 tests) — security, I/O contracts, Agent Teams, context predictions
node .claude/hooks/__tests__/test-hooks.js

# Command validation (81 tests) — frontmatter, structure, auto-fix, deploy, skill chaining
node .claude/commands/__tests__/test-commands.js

# Schema validation (166 tests) — JSON schema structure, profile/agent/gate compliance, cross-module integrity
node schemas/__tests__/test-schemas.js

# Integration tests (29 tests) — cross-file references, hook chain flow, install/uninstall parity, doc consistency, plugin parity
node integration/__tests__/test-integration.js
```

All core test suites use shared `test-utils.js` with built-in `assert` — zero external dependencies.

---

## 📄 Governance Files

Created automatically on first `/cs-loop` run:

| File | Purpose |
|------|---------|
| `STATUS.md` | Current progress, what's done/next |
| `CHANGELOG.md` | Version history |
| `DECISIONS.md` | Architecture decisions (ADRs) |
| `.claude/rules/learnings.md` | Decisions, patterns, learnings |

---

## 🧠 Self-Improvement

Claude Sentient includes a self-improvement mechanism. See [Self-Improvement](CLAUDE.md#self-improvement) for details.

> *"After every correction, Claude proposes a rule update so it doesn't make that mistake again."*

Learnings are stored in [`.claude/rules/learnings.md`](.claude/rules/learnings.md) and persist across sessions.

---

## 📚 Documentation

### Core Docs
| File | Purpose |
|------|---------|
| [CLAUDE.md](CLAUDE.md) | Main instructions (comprehensive reference) |
| [STATUS.md](STATUS.md) | Current progress |
| [CHANGELOG.md](CHANGELOG.md) | Version history |
| [DECISIONS.md](DECISIONS.md) | Architecture decisions |

### Reference
| Directory | Contents |
|-----------|----------|
| [profiles/](profiles/) | Language-specific quality gate configurations |
| [rules/](rules/) | Topic-specific coding standards (API design, security, etc.) |
| [templates/](templates/) | Governance file templates |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run `/cs-validate` to verify
5. Submit a pull request

---

## 📜 License

MIT — Use freely, contribute back.

See [LICENSE](LICENSE) for details.

---

## ⚠️ Disclaimer

This software is provided "as is", without warranty of any kind. Claude Sentient is an experimental tool that provides prompts and configurations for Claude Code. The developers are not responsible for any issues arising from its use, including but not limited to code changes, data loss, or unintended behavior. Always review AI-generated output before applying changes to your codebase.

---

<p align="center">
  <strong>🧠 Claude Sentient — Orchestrating Claude Code's native capabilities for autonomous development</strong>
</p>
