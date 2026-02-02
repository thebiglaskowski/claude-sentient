# 🧠 Claude Sentient

> **Autonomous development orchestration for Claude Code**

Claude Sentient coordinates Claude Code's native capabilities into an autonomous development workflow. It's not a replacement — it's a thin orchestration layer that makes built-in tools work together cohesively.

[![Version](https://img.shields.io/badge/version-0.3.0-blue.svg)](CHANGELOG.md)
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

## 🎯 What is Claude Sentient?

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

---

## 📊 By the Numbers

| Component | Count | Purpose |
|-----------|-------|---------|
| 🎯 Commands | 6 | Slash commands (`/cs-*`) |
| 📋 Profiles | 9 | Language-specific quality gates |
| 📏 Rules | 12 | Topic-specific standards |
| 📄 Templates | 4 | Governance file templates |
| 🚦 Quality Gates | 4 | Lint, test, build, git |
| 🔄 Loop Phases | 7 | INIT → EVALUATE |

---

## 🎯 Commands

| Command | Purpose |
|---------|---------|
| `/cs-loop` | Autonomous loop: understand → plan → execute → verify → commit |
| `/cs-plan` | Plan complex tasks before executing |
| `/cs-status` | Show tasks, git state, detected profile |
| `/cs-validate` | Validate profiles, commands, rules, governance |
| `/cs-learn` | Save learnings to persistent memory |
| `/cs-mcp` | Check, register, and validate MCP servers |

---

## 📋 Profile Detection

Sentient auto-detects your project type and loads appropriate tooling:

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

| Feature | Native Tool |
|---------|-------------|
| Task Queue | `TaskCreate`, `TaskUpdate`, `TaskList` |
| Planning | `EnterPlanMode`, `ExitPlanMode` |
| Sub-agents | `Task` with `subagent_type` |
| Memory | `.claude/rules/*.md` |
| Commands | `commands/*.md` + `Skill` |
| MCP Servers | `mcp__*` tools (context7, github, etc.) |

---

## 🔗 MCP Server Integration

Claude Sentient can leverage MCP (Model Context Protocol) servers for extended capabilities:

| Server | Purpose | Auto-Used By |
|--------|---------|--------------|
| **context7** | Library documentation | `/cs-loop` (fetches docs for imports) |
| **github** | GitHub API (PRs, issues) | `/cs-loop` (when creating PRs) |
| **memory** | Persistent key-value store | Manual |
| **filesystem** | File system access | Manual |
| **puppeteer** | Browser automation | Manual |

### Setup MCP Servers

```bash
/cs-mcp              # Check what's configured vs connected
/cs-mcp --fix        # Auto-register servers from settings.json
/cs-mcp --test       # Validate servers are responding
```

**Note:** MCP servers are registered at the user level (`~/.claude.json`). Once registered, they're available in all projects.

---

## 🔧 Two Ways to Use Claude Sentient

### CLI Mode vs SDK Mode

| Aspect | CLI Mode | SDK Mode |
|--------|----------|----------|
| **Entry point** | `/cs-loop "task"` | `ClaudeSentient.loop("task")` |
| **Install** | One-line script | `pip install -e` / `npm install` |
| **Use case** | Interactive development | CI/CD, automation, scripts |
| **Session** | Per-terminal | Persists to disk, resumable |

### CLI Mode (Interactive)

Use the one-line install (see Quick Start above). Then run commands in Claude Code:

```bash
/cs-loop "add user authentication"   # Interactive loop
/cs-plan "refactor the API"          # Plan first, execute later
```

Best for: Daily development, exploring code, tasks where you want to guide Claude.

### SDK Mode (Programmatic)

```bash
# Python
pip install -e sdk/python/

# TypeScript
cd sdk/typescript && npm install && npm run build
```

```python
from claude_sentient import ClaudeSentient

async def main():
    sentient = ClaudeSentient(cwd="./my-project")

    # Run the loop
    async for result in sentient.loop("Add user authentication"):
        print(f"Phase: {result.phase}, Tasks: {result.tasks_completed}")

    # Or resume a previous session
    async for result in sentient.resume():
        print(f"Resumed from: {result.phase}")
```

Best for: CI/CD pipelines, scheduled tasks, webhooks, headless automation.

### SDK Features

| Feature | Description |
|---------|-------------|
| **Session Persistence** | Resume work across terminal closures (`.claude/state/`) |
| **Programmatic Control** | Run from scripts, pipelines, webhooks |
| **Quality Gate Hooks** | Lint/test run automatically on file changes |
| **Profile Detection** | Auto-detect Python, TypeScript, Go, etc. |

See [`CLAUDE.md`](CLAUDE.md#cli-vs-sdk-two-ways-to-use-claude-sentient) for comprehensive documentation on when to use each mode.

---

## 📁 Project Structure

```
your-project/
├── .claude/
│   ├── commands/cs-*.md    # 5 slash commands
│   └── rules/learnings.md  # Persistent memory
├── profiles/*.yaml          # 9 language profiles
├── templates/*.md           # Governance templates
└── rules/*.md               # 12 topic rules
```

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

Claude Sentient includes a self-improvement mechanism:

> *"After every correction, Claude proposes a rule update so it doesn't make that mistake again."*

Learnings are stored in `.claude/rules/learnings.md` and persist across sessions.

---

## 📚 Documentation

| File | Purpose |
|------|---------|
| [CLAUDE.md](CLAUDE.md) | Main instructions |
| [STATUS.md](STATUS.md) | Current progress |
| [CHANGELOG.md](CHANGELOG.md) | Version history |
| [DECISIONS.md](DECISIONS.md) | Architecture decisions |

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
