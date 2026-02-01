# CLAUDE.md — Claude Sentient Development Guidelines

> **Project:** Claude Sentient
> **Version:** 0.1.0 (Development)
> **Type:** Autonomous Meta-Cognitive Development Engine

---

## Project Overview

Claude Sentient is a ground-up redesign of the AI-assisted development platform. It is a **self-improving autonomous development engine** that learns from every action, knows its own capabilities, and requires minimal human intervention.

### Core Philosophy

1. **Autonomous by Default** — Only pause for ambiguity or risk
2. **Self-Aware Meta-Cognition** — Know what we can do, are doing, and should do
3. **Continuous Self-Improvement** — Every action feeds back into learning
4. **Swiss Army Knife** — One engine for any project type
5. **Partner, Not Tool** — A development partner that builds with you

### Key Documents

| Document | Purpose |
|----------|---------|
| `docs/VISION.md` | North star philosophy |
| `docs/GAMEPLAN.md` | Master integration plan |
| `docs/BLUEPRINT.md` | Technical architecture |
| `docs/V1_FEATURE_INVENTORY.md` | V1 features to migrate |
| `STATUS.md` | Current project state |
| `DECISIONS.md` | Architecture decisions |

---

## Development Standards

### File Naming

- **Schemas:** `kebab-case.schema.json`
- **Skills:** `kebab-case.skill.yaml`
- **Commands:** `kebab-case.cmd.yaml`
- **Agents:** `kebab-case.agent.yaml`
- **Gates:** `kebab-case.gate.json`
- **Phases:** `##-name.md` (e.g., `01-classify.md`)
- **Events:** `category.events.yaml`

### Code Style

- YAML for content-heavy files (skills, commands, agents)
- JSON for structured data (schemas, gates, state, config)
- Markdown for documentation and phase content
- Python for tooling (validate, migrate, render)

### Component Structure

Every component must have:
```yaml
name: kebab-case-name
version: "1.0.0"
description: "One-line description (10-200 chars)"
```

Skills also need:
```yaml
triggers:
  - "phrase that activates"
  - pattern: "regex pattern"
    priority: 80
```

Commands also need:
```yaml
command: cc-name
category: planning|execution|quality|git|docs|operations
```

### Event-Driven Architecture

- All components communicate via events
- Never call components directly — publish events
- Subscribe to events to react
- Every action emits events for learning capture

### State Management

- JSON is the source of truth
- Markdown is rendered from JSON, not parsed into it
- State schema validates all state changes
- Learning data captured in state

---

## Quality Standards

### All Changes Must

1. Pass schema validation (`python tools/validate.py`)
2. Include appropriate event emissions
3. Feed into learning system
4. Have tests (where applicable)
5. Update relevant documentation

### Quality Gates

All 18 gates are **blocking** — no exceptions:
- Code: lint, type, unit, integration, security, performance
- UI: browser, accessibility
- Docs: documentation complete
- Work: queue empty, issues resolved, git clean, DoD met
- V2: learning captured, approval obtained, self-review passed

---

## Required Plugins

### Claude-Mem (Persistent Memory)

Claude Sentient requires the **claude-mem** plugin for persistent memory across sessions.

**Installation:**
```bash
/plugin marketplace add thedotmack/claude-mem
/plugin install claude-mem
```

**Features:**
- Automatic capture via lifecycle hooks (no manual intervention)
- AI-powered compression (~10x token savings)
- SQLite + Chroma vector DB (semantic + keyword search)
- Web interface at `http://localhost:37777`
- Privacy controls with `<private>` tags

**Usage:**
- Use `mem-search` skill to query project history
- View memories at localhost:37777
- Wrap sensitive content in `<private>` tags to exclude

---

## Learning System

### The Core Differentiator

Every action must:
1. **Capture** — Automatic via claude-mem hooks
2. **Analyze** — Success or failure, why
3. **Learn** — Generate rules, update weights
4. **Apply** — Use learnings in future actions

### Rule Generation

When the same mistake happens 3+ times:
1. Detect the pattern (query claude-mem for similar issues)
2. Generate a prevention rule
3. Add to auto-generated rules
4. Track effectiveness
5. Prune if <50% effective

### Memory & Rules

- **Session memory**: Handled by claude-mem (automatic)
- **Generated rules**: Stored in `.claude/knowledge/rules/auto-generated/`
- **Search history**: Use `mem-search` skill for natural language queries

---

## Project Structure

```
claude-sentient/
├── CLAUDE.md              # This file
├── README.md              # Project overview
├── STATUS.md              # Current state
├── CHANGELOG.md           # Version history
├── KNOWN_ISSUES.md        # Limitations, bugs
├── DECISIONS.md           # Architecture decisions
│
├── docs/                  # Planning & design docs
├── schemas/               # JSON Schemas (source of truth)
├── core/                  # Orchestrator
├── phases/                # 10 modular phases
├── skills/                # Auto-triggered behaviors
├── commands/              # /cc-* commands
├── agents/                # Specialist agents
├── gates/                 # Quality gates
├── patterns/              # Architecture patterns
├── rules/                 # Topic standards
├── snippets/              # Code templates
├── events/                # Event definitions
├── state/                 # State schemas
├── config/                # Configuration
├── templates/             # Project scaffolding
├── tools/                 # Python CLI tools
├── tests/                 # Test infrastructure
├── .claude/               # Runtime data
│   ├── extensions/        # Local extensions
│   ├── state/             # Session state
│   └── knowledge/         # Learned knowledge
└── reference/v1/          # V1 for reference
```

---

## Commands

### Development Commands

```bash
# Validate all components
python tools/validate.py

# Render state to Markdown
python tools/render-state.py

# Check what needs migration from V1
python tools/migrate.py --dry-run --input=reference/v1
```

### Git Workflow

- Commits: Use conventional commits (`feat:`, `fix:`, `docs:`, etc.)
- Branches: `main` for stable, feature branches for development
- PRs: Required for significant changes

---

## Implementation Phases

Current phase: **Phase 0 — Foundation**

| Phase | Status | Focus |
|-------|--------|-------|
| 0. Foundation | 🔄 Active | Schemas, events, state |
| 1. Core Loop | ⏳ Pending | 10 phases, orchestrator |
| 2. Quality Gates | ⏳ Pending | 18 gates |
| 3. Learning Engine | ⏳ Pending | Self-improvement |
| 4. Advanced Features | ⏳ Pending | Boris integrations |
| 5. Full Migration | ⏳ Pending | V1 parity + V2 |
| 6. Polish | ⏳ Pending | Docs, performance |

---

## Hard Rules

1. **Never skip quality gates** — All must pass
2. **Never lose learnings** — Every action feeds learning
3. **Never assume context** — Load and verify
4. **Always emit events** — No silent actions
5. **Schema-first** — Validate before use
6. **Checkpoint before risk** — Create rollback points

---

## Reference

V1 source code is available in `reference/v1/` for:
- Understanding existing implementations
- Migrating skills, commands, agents
- Ensuring feature parity

**Do not modify** files in `reference/v1/` — it's read-only reference.

---

*Claude Sentient: The Autonomous Meta-Cognitive Development Engine*
