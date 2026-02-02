# 🎼 Claude Conductor

<p align="center">
  <img src="assets/claude-conductor.png" alt="Claude Conductor Logo" width="400">
</p>

> **The intelligent orchestration platform for Claude Code** — Transform Claude into a self-aware development team with 37 namespaced commands (`/cc-*`), 61 skills, 15 specialized agents, pattern library, snippet registry, context budget monitoring, parallel task decomposition, decision logging, commit checkpoints, and strict quality enforcement.

---

## ⚠️ Important Notice

**This is an experimental orchestration framework.** Claude Conductor provides prompts, templates, and configurations designed to enhance Claude Code workflows. Results may vary based on your project, Claude's responses, and how you apply these tools.

- **Not a guarantee** — These prompts guide Claude but don't guarantee specific outcomes
- **Your responsibility** — Always review Claude's output before committing changes
- **Evolving project** — Expect breaking changes between versions
- **Community-driven** — Contributions and feedback welcome

[![Version](https://img.shields.io/badge/version-4.0.0-blue.svg)](CHANGELOG.md)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Compatible-green.svg)](https://claude.ai)
[![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)](LICENSE)

---

## 🎯 What is Claude Conductor?

Claude Conductor transforms Claude Code from a coding assistant into a **self-aware development orchestration system**. It provides:

- 🧠 **Meta-Cognition** — Claude knows what tools it has and chooses the best approach
- 🔄 **Autonomous Loop** — Works until the job is actually done (10 phases, 15 quality gates)
- 🚫 **Strict Enforcement** — No warnings, no exceptions. All quality gates are blocking.
- 👥 **Parallel Agents** — Spawn security-analyst, code-reviewer, test-engineer simultaneously
- 📊 **Full Visibility** — Track progress, metrics, and quality across the entire lifecycle
- 📏 **Context Budget Monitor** — Prevents context window bloat, auto-suggests sub-agents
- ⚡ **Parallel Task Decomposition** — Breaks complex tasks into concurrent work units
- 📝 **Decision Logging** — Captures decisions with rationale for traceability
- 🔖 **Commit Checkpoints** — Creates verified commits for easy rollback to known-good states

```
USER REQUEST → HOOKS → ORCHESTRATOR → META-COGNITION → LOOP (10 phases) → DoD → DONE
                ↑                           │                    ↓
           context-injector        CAPABILITY INVENTORY   15 Quality Gates
                                   + PATTERNS + SNIPPETS   (ALL BLOCKING)
                                   + CONTEXT BUDGET MON.   + CHECKPOINTS
```

---

## ⚡ Quick Start

### 1️⃣ Install Template

```bash
# In your normal terminal (not inside Claude Code)
cd C:\scripts\prompts
./install.sh /path/to/your/project

# Or PowerShell (Windows)
.\install.ps1 -TargetDir "C:\path\to\your\project"
```

### 2️⃣ Start Claude Code

```bash
cd /path/to/your/project
claude --init
```

### 3️⃣ Initialize Project

Inside Claude Code, type:
```
initialize this project
```

Claude will automatically detect your tech stack, install relevant skills, and generate project context.

---

## 📦 What's Included

```
your-project/
└── .claude/
    ├── 📜 CLAUDE.md           # Orchestrator brain
    ├── ⚙️ settings.json       # Permissions & config
    ├── 🎯 commands/           # 37 namespaced slash commands (/cc-*)
    ├── 🧠 skills/             # 58 auto-loading skills
    ├── 📏 rules/              # 13 modular rule sets
    ├── 👤 agents/             # 15 specialized experts
    ├── 🪝 hooks/              # 12 lifecycle hooks
    ├── 📊 context/            # Capability inventory
    ├── 🎨 patterns/           # Reusable architecture patterns
    ├── 📋 snippets/           # Indexed code snippets
    └── 📝 docs/               # Reference documentation
```

### 📊 By the Numbers

> **Note:** These counts reflect the complete Claude Conductor system when installed via `install.sh`. The `/template/` folder contains the full `.claude/` configuration that gets copied to your project.

| Component | Count | Purpose |
|-----------|-------|---------|
| 🎯 Commands | 37 | Namespaced slash commands (`/cc-*`) |
| 🧠 Skills | 61 | Auto-loading behavioral guidance |
| 📏 Rules | 13 | Topic-specific standards |
| 👤 Agents | 15 | Specialized expert analysis |
| 🪝 Hooks | 12 | Automated lifecycle events |
| 🎨 Patterns | 15+ | Reusable architecture patterns |
| 📋 Snippets | 9 | Indexed code snippets |
| 🧪 Tests | 1,496 | Component validation tests |
| 🚦 Quality Gates | 15 | All blocking — no exceptions |
| 🔄 Loop Phases | 10 | Including META-COGNITION, CHECKPOINT & REASSESS |

Additionally, this repository includes **27 standalone prompts** in the root folders (`planning/`, `execution/`, `quality/`, etc.) that can be used independently of the template system.

---

## 🎯 Core Commands

All commands use the `cc-` namespace to avoid conflicts with other tools.

### 🏗️ Planning & Setup
| Command | Purpose |
|---------|---------|
| `/cc-plan` | Create feature specification |
| `/cc-audit-blueprint` | Validate plan before building |
| `/cc-scaffold` | Generate project structure |
| `/cc-claude-md` | Create/improve project CLAUDE.md |
| `/cc-analyze` | 🆕 Brownfield codebase analysis |

### 🔨 Development
| Command | Purpose |
|---------|---------|
| `/cc-daily` | Continue development work |
| `/cc-loop` | 🔄 Autonomous work until done |
| `/cc-spike` | Technical research |
| `/cc-fix` | Bug hunting |
| `/cc-revert` | 🆕 Smart git revert (logical work units) |

### ✅ Quality
| Command | Purpose |
|---------|---------|
| `/cc-review` | Code review |
| `/cc-test` | Test coverage gate |
| `/cc-secure` | Security audit |
| `/cc-assess` | Full codebase audit |
| `/cc-perf` | Performance audit |

### 🚀 Deployment
| Command | Purpose |
|---------|---------|
| `/cc-commit` | Create well-formatted commit |
| `/cc-pr` | Create pull request |
| `/cc-release` | Release checklist |

---

## 🔄 The Intelligent Loop

When you run `/cc-loop`, Claude Conductor executes a **10-phase autonomous loop** with **15 quality gates**:

```
Phase 1:   CONTEXTUALIZE  → Understand codebase & constraints
Phase 2:   ASSESS         → Analyze current state
Phase 2.5: META-COGNITION → Choose best approach from capability inventory
Phase 3:   PLAN           → Prioritize work queue
Phase 4:   BUILD          → Implement changes
Phase 5:   TEST           → Run tests + browser verification
Phase 6:   QUALITY        → Run all quality gates
Phase 6.5: REASSESS       → Pivot strategy if stuck
Phase 7:   EVALUATE       → Check Definition of Done
Phase 8:   RECOVER        → Handle errors gracefully
```

### 🚦 Quality Gates (ALL BLOCKING)

The loop **cannot exit** until ALL gates pass:

| Gate | Threshold |
|------|-----------|
| ✅ Lint | 0 errors, 0 warnings |
| ✅ Type Check | 0 type errors |
| ✅ Unit Tests | 100% pass, ≥80% coverage |
| ✅ Integration | 100% pass |
| ✅ Security | 0 S0/S1 vulnerabilities |
| ✅ Performance | Bundle size, N+1, Web Vitals |
| ✅ Browser | Visual verification (if UI) |
| ✅ Accessibility | axe-core audit (if UI) |
| ✅ Documentation | README + CHANGELOG present |
| ✅ Work Queue | 0 pending tasks |
| ✅ Known Issues | 0 unresolved S0/S1 |
| ✅ Git State | All changes committed |

---

## 👤 Specialized Agents

Spawn focused experts for deep analysis:

| Agent | Model | Use Case |
|-------|-------|----------|
| 🔒 `security-analyst` | opus | Security audits, threat modeling |
| 👀 `code-reviewer` | sonnet | Code review, best practices |
| 🧪 `test-engineer` | sonnet | Test writing, coverage analysis |
| 📚 `documentation-writer` | sonnet | Documentation tasks |
| 🔬 `researcher` | sonnet | Technical research |
| 🎨 `ui-ux-expert` | sonnet | Web interface design |
| 💻 `terminal-ui-expert` | sonnet | CLI/terminal polish |
| 🔍 `seo-expert` | sonnet | Search engine optimization |
| 🗄️ `database-expert` | sonnet | Database optimization |
| 🚀 `devops-engineer` | sonnet | CI/CD, Docker, K8s |
| ♿ `accessibility-expert` | sonnet | WCAG compliance |

**Usage:** `"Spawn security-analyst agent to audit the auth module"`

---

## 🎨 Pattern Library

Reusable architecture and design patterns surfaced contextually during implementation:

| Category | Patterns |
|----------|----------|
| Architecture | Repository, Service Layer, CQRS, Clean Architecture |
| Resilience | Retry with Backoff, Circuit Breaker, Bulkhead |
| Error Handling | Error Boundary, Result Type |
| API | Pagination, Rate Limiting, Versioning |
| Behavioral | Strategy, Observer, State Machine |
| Testing | Arrange-Act-Assert, Test Doubles |
| Operations | Feature Flag, Blue-Green Deploy |

**Usage:** `@patterns/repository` or ask "What patterns apply here?"

---

## 📋 Snippet Registry

Indexed, searchable code snippets for rapid development:

| Category | Snippets |
|----------|----------|
| API | Express routes, FastAPI endpoints, Go handlers |
| React | Components, hooks, context |
| Testing | Jest, pytest, Go tests |
| Database | Prisma models, migrations |
| DevOps | Dockerfile, GitHub Actions |
| Utility | Error classes, loggers, config |

**Usage:** `snippet:express-route` or "Give me the React component snippet"

---

## 📏 Modular Rules

Load topic-specific guidance with `@rules/[name]`:

| Rule | Topics |
|------|--------|
| `@rules/security` | OWASP, authentication, secrets |
| `@rules/testing` | Coverage, TDD, mocks |
| `@rules/git-workflow` | Commits, branches, PRs |
| `@rules/documentation` | README, changelog, comments |
| `@rules/code-quality` | Complexity, naming, deps |
| `@rules/api-design` | REST, errors, versioning |
| `@rules/performance` | Optimization, caching, Web Vitals |
| `@rules/database` | Schema, indexing, migrations |
| `@rules/ui-ux-design` | Spacing, typography, accessibility |
| `@rules/terminal-ui` | Spinners, progress bars, colors |

---

## 🧠 Meta-Cognition

Claude Conductor is **self-aware**. It maintains a **Capability Inventory** of all available tools and uses a **Decision Engine** to choose the best approach:

```
"I need to verify security..."
    → Consult CAPABILITY_INVENTORY.md
    → Decision: Spawn security-analyst agent + load @rules/security
    → Execute with full context
```

When stuck, the **REASSESS** phase automatically:
- Detects lack of progress (2 iterations with no change)
- Reviews approaches already tried
- Pivots to alternative strategies
- Spawns specialist agents if needed

---

## 🔌 MCP Server Support

Claude Conductor integrates with MCP servers for extended capabilities:

| Server | Purpose |
|--------|---------|
| 🔍 **Context7** | Up-to-date library documentation |
| 🐙 **GitHub** | Issues, PRs, repository management |
| 🧠 **Memory** | Persistent storage across sessions |
| 📁 **Filesystem** | Access files outside project directory |
| 🗄️ **PostgreSQL/SQLite** | Database queries |
| 🌐 **Puppeteer** | Browser automation and screenshots |

### 📖 MCP Documentation

| Guide | Description |
|-------|-------------|
| [MCP Setup Guide](template/.claude/MCP_SETUP.md) | Quick start, prerequisites, installation scripts |
| [MCP Servers Reference](template/.claude/MCP_SERVERS.md) | Complete server configurations, environment variables, troubleshooting |

**Quick Setup:**
```bash
# Windows
.\template\.claude\scripts\setup-mcp-servers.ps1

# macOS/Linux
./template/.claude/scripts/setup-mcp-servers.sh
```

---

## 📚 Documentation

Comprehensive guides for using Claude Conductor effectively:

### Getting Started
| Guide | Description |
|-------|-------------|
| [Setup Guide](template/.claude/SETUP.md) | Initial installation and configuration |
| [Quick Reference](template/.claude/QUICK_REFERENCE.md) | One-page cheat sheet for commands and features |
| [Configuration](template/.claude/CONFIGURATION.md) | All configuration options explained |
| [Examples](template/.claude/EXAMPLES.md) | Real-world usage examples |

### Core Concepts
| Guide | Description |
|-------|-------------|
| [System Architecture](template/.claude/_system.md) | How all components work together |
| [Loop Workflow](template/.claude/LOOP_WORKFLOW.md) | Complete `/cc-loop` execution flow |
| [Quality Gates](template/.claude/QUALITY_GATES.md) | All 15 gates with pass/fail criteria |
| [Hooks Reference](template/.claude/HOOKS_REFERENCE.md) | All 12 hooks with I/O schemas |

### Troubleshooting & Maintenance
| Guide | Description |
|-------|-------------|
| [Troubleshooting](template/.claude/TROUBLESHOOTING.md) | Common issues and solutions |
| [Error Recovery](template/.claude/ERROR_RECOVERY.md) | Error classification and recovery strategies |
| [Upgrade Guide](template/.claude/UPGRADE_GUIDE.md) | How to upgrade between versions |
| [State Files](template/.claude/STATE_FILES.md) | State file schemas and locations |

### Authoring
| Guide | Description |
|-------|-------------|
| [Prompt Template](template/.claude/PROMPT_TEMPLATE.md) | Best practices for writing prompts |
| [CLAUDE.md Guide](CLAUDE.md) | Project-level guidelines |

### Testing
| Guide | Description |
|-------|-------------|
| [Test Suite README](template/.claude/tests/README.md) | Test architecture and usage |

**Quick test run:**
```bash
cd template/.claude/tests
pip install pytest pyyaml
pytest -v
```

---

## 📁 Prompts Library

Claude Conductor also includes a collection of standalone prompts:

### 📋 Planning
| Prompt | Purpose |
|--------|---------|
| [BLUEPRINT_AUDITOR](planning/BLUEPRINT_AUDITOR.md) | Audit plans for execution readiness |
| [BLUEPRINT_AUDITOR_RERUN](planning/BLUEPRINT_AUDITOR_RERUN.md) | Re-audit after changes |
| [FEATURE_SPEC_WRITER](planning/FEATURE_SPEC_WRITER.md) | Transform requirements into specs |

### 🔨 Execution
| Prompt | Purpose |
|--------|---------|
| [PROJECT_EXECUTION](execution/PROJECT_EXECUTION.md) | Execute blueprint work |
| [DAILY_BUILD](execution/DAILY_BUILD.md) | Continue daily work |
| [SPIKE_RESEARCH](execution/SPIKE_RESEARCH.md) | Time-boxed technical research |

### ✅ Quality
| Prompt | Purpose |
|--------|---------|
| [BUG_HUNT](quality/BUG_HUNT.md) | Systematic bug investigation |
| [CODE_REVIEW](quality/CODE_REVIEW.md) | Structured code review |
| [CODEBASE_AUDIT](quality/CODEBASE_AUDIT.md) | Comprehensive codebase audit |
| [DEPENDENCY_AUDIT](quality/DEPENDENCY_AUDIT.md) | Dependency security & health |
| [FINAL_COMPLETION_AUDIT](quality/FINAL_COMPLETION_AUDIT.md) | Project completion verification |
| [PERFORMANCE_AUDIT](quality/PERFORMANCE_AUDIT.md) | Performance analysis & optimization |
| [SECURITY_AUDIT](quality/SECURITY_AUDIT.md) | Security-focused audit |
| [TEST_COVERAGE_GATE](quality/TEST_COVERAGE_GATE.md) | Test coverage verification |

### 🚀 Operations
| Prompt | Purpose |
|--------|---------|
| [INCIDENT_POSTMORTEM](operations/INCIDENT_POSTMORTEM.md) | Learn from incidents |
| [MIGRATION_PLANNER](operations/MIGRATION_PLANNER.md) | Safe migration planning |
| [RELEASE_CHECKLIST](operations/RELEASE_CHECKLIST.md) | Pre-release validation |
| [TECH_DEBT_TRACKER](operations/TECH_DEBT_TRACKER.md) | Track and manage technical debt |

### 📝 Documentation
| Prompt | Purpose |
|--------|---------|
| [ADR_WRITER](documentation/ADR_WRITER.md) | Architecture Decision Records |
| [CANONICAL_README](documentation/CANONICAL_README.md) | README template & guidelines |
| [DOCS_AND_CHANGELOG_POLICY](documentation/DOCS_AND_CHANGELOG_POLICY.md) | Documentation standards |
| [ONBOARDING_GUIDE](documentation/ONBOARDING_GUIDE.md) | New contributor onboarding |
| [UNIT_CLOSEOUT_CHECKLIST](documentation/UNIT_CLOSEOUT_CHECKLIST.md) | Work unit completion checklist |

### 🔧 Refactoring
| Prompt | Purpose |
|--------|---------|
| [REFACTORING_ENGINE](refactoring/REFACTORING_ENGINE.md) | Safe, incremental code refactoring |

---

## 🔄 Project Lifecycle

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           🎼 CLAUDE CONDUCTOR                                │
├────────────┬────────────┬────────────┬────────────┬────────────┬───────────┤
│  📋 PLAN   │  🔨 BUILD  │  ✅ VERIFY │  🚀 SHIP   │  🔧 MAINT  │ 📊 TRACK  │
├────────────┼────────────┼────────────┼────────────┼────────────┼───────────┤
│ /cc-plan   │ /cc-daily  │ /cc-review │ /cc-release│ /cc-fix    │ /cc-assess│
│ /cc-audit- │ /cc-loop   │ /cc-test   │ /cc-commit │ /cc-debt   │ /cc-perf  │
│ blueprint  │ /cc-spike  │ /cc-secure │ /cc-pr     │ /cc-refact │ /cc-deps  │
│ /cc-adr    │            │            │            │ /cc-revert │           │
└────────────┴────────────┴────────────┴────────────┴────────────┴───────────┘
```

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Quick summary:**
1. Place in appropriate category folder
2. Follow naming conventions
3. Include clear instructions
4. Update this README
5. Update CHANGELOG.md

---

## 📜 License

MIT — Use freely, contribute back.

---

## 📊 Version

| Metric | Value |
|--------|-------|
| **Version** | 4.0.0 |
| **Last Updated** | 2026-01-30 |
| **Commands** | 37 (namespaced `/cc-*`) |
| **Skills** | 61 |
| **Agents** | 15 |
| **Rules** | 13 |
| **Patterns** | 15+ |
| **Snippets** | 9 |
| **Tests** | 1,496 |
| **Hooks** | 12 |
| **Quality Gates** | 15 |
| **Loop Phases** | 10 |

---

<p align="center">
  <strong>🎼 Claude Conductor — Because great software deserves great orchestration.</strong>
</p>
