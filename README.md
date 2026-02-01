# Claude Sentient

> **A thin orchestration layer for Claude Code**

Claude Sentient coordinates Claude Code's native capabilities into an autonomous development workflow. It's not a replacement — it's a lightweight wrapper that makes built-in tools work together.

---

## Philosophy

**Native-first.** Claude Code already has task management, planning modes, sub-agents, and memory. We don't reinvent these — we orchestrate them.

---

## What You Get

### 5 Commands

| Command | What It Does |
|---------|--------------|
| `/cs-loop` | Autonomous loop: understand → plan → execute → verify → commit |
| `/cs-plan` | Plan complex tasks before executing |
| `/cs-status` | Show tasks, git state, detected profile |
| `/cs-validate` | Validate profiles, commands, rules, governance |
| `/cs-learn` | Save learnings to persistent memory |

### Profile Detection

Sentient detects your project type and loads appropriate tooling:

| Profile | Detected By | Tools |
|---------|-------------|-------|
| Python | `pyproject.toml`, `*.py` | ruff, pytest, pyright |
| TypeScript | `tsconfig.json`, `*.ts` | eslint, vitest, tsc |
| Go | `go.mod`, `*.go` | golangci-lint, go test |
| Rust | `Cargo.toml` | clippy, cargo test |
| Java | `pom.xml`, `build.gradle` | checkstyle, JUnit |
| C/C++ | `CMakeLists.txt`, `Makefile` | clang-tidy, ctest |
| Ruby | `Gemfile` | rubocop, rspec |
| Shell | `*.sh`, `*.ps1` | shellcheck |
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

### One-Line Install

**Bash (Linux/Mac):**
```bash
curl -fsSL https://raw.githubusercontent.com/thebiglaskowski/claude-sentient/main/install.sh | bash
```

**PowerShell (Windows):**
```powershell
iwr -useb https://raw.githubusercontent.com/thebiglaskowski/claude-sentient/main/install.ps1 | iex
```

### Manual Install

```bash
# Clone and run installer
git clone https://github.com/thebiglaskowski/claude-sentient.git
cd claude-sentient
./install.sh  # or .\install.ps1 on Windows
```

### What the Installer Does

```bash
# From your project root, the installer:
mkdir -p .claude/commands
cp commands/cs-*.md .claude/commands/     # Slash commands

mkdir -p profiles
cp profiles/*.yaml ./profiles/             # Quality gate definitions

mkdir -p templates
cp templates/*.md ./templates/             # Governance templates

mkdir -p .claude/rules
cp templates/learnings.md .claude/rules/   # Persistent memory
```

### What Gets Installed

| Location | Purpose |
|----------|---------|
| `.claude/commands/cs-*.md` | Slash commands (`/cs-loop`, etc.) |
| `profiles/*.yaml` | Quality gate definitions |
| `templates/` | Templates for governance files |
| `.claude/rules/learnings.md` | Persistent memory |

### After Installation

1. Run `/cs-validate` to verify everything is set up correctly
2. Run `/cs-status` to see detected profile
3. Run `/cs-loop "your task"` to start working

### Updating

To update to the latest version, re-run the copy commands above. Your `.claude/rules/learnings.md` will be preserved.

### No Dependencies

No npm, pip, or external tools required. Just markdown and YAML files that Claude Code reads directly.

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
