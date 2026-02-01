# Claude Sentient

> **The Autonomous Meta-Cognitive Development Engine**

[![Version](https://img.shields.io/badge/version-0.1.0--dev-blue.svg)](CHANGELOG.md)
[![Status](https://img.shields.io/badge/status-development-yellow.svg)](STATUS.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## What is Claude Sentient?

Claude Sentient is a **self-improving autonomous development engine** that:

- **Learns from every action** — Mistakes become rules, successes become patterns
- **Knows its own capabilities** — Meta-cognition drives tool selection
- **Requires minimal input** — "Build X" → Done
- **Works on any project** — Greenfield or brownfield, any tech stack
- **Gets better over time** — Continuous improvement within each project

**One sentence:** *"Drop it in, tell it what you want, walk away, come back to a finished product."*

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/thebiglaskowski/claude-sentient.git
cd claude-sentient

# Validate all components
python tools/validate.py

# Initialize in your project
# (coming soon)
```

### Required Plugin

Claude Sentient uses **claude-mem** for persistent memory across sessions:

```bash
# In Claude Code
/plugin marketplace add thedotmack/claude-mem
/plugin install claude-mem
```

This enables automatic capture, AI-powered compression, and semantic search of project history.

---

## The Vision

### Three Pillars

| Pillar | Description |
|--------|-------------|
| **Autonomy** | Self-driving, minimal input, auto-recover, make decisions |
| **Intelligence** | Meta-cognition, tool selection, context aware, multi-agent |
| **Learning** | Self-improve, pattern detect, rule generate, feedback loop |

### How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                      CLAUDE SENTIENT                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   User Request                                                   │
│        │                                                         │
│        ▼                                                         │
│   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐        │
│   │ PERCEIVE│──▶│  PLAN   │──▶│ EXECUTE │──▶│EVALUATE │        │
│   └─────────┘   └─────────┘   └─────────┘   └─────────┘        │
│        │                                          │             │
│        │         ┌─────────────────┐              │             │
│        └────────▶│ META-COGNITION  │◀─────────────┘             │
│                  └─────────────────┘                            │
│                           │                                      │
│                           ▼                                      │
│                  ┌─────────────────┐                            │
│                  │ SELF-IMPROVEMENT│                            │
│                  └─────────────────┘                            │
│                           │                                      │
│                           ▼                                      │
│                      KNOWLEDGE                                   │
│                       (persists)                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Features

### From V1 (68 Skills, 37 Commands, 15 Agents)
- 10-phase autonomous loop
- 15 quality gates (all blocking)
- Swarm orchestration
- Task dependencies
- Multi-registry skill discovery
- Plugin support

### New in V2
- **Learning Engine** — Auto-generate rules from corrections
- **Staff Engineer Review** — Adversarial plan review
- **Zero-Config Fixes** — "Just fix" without context
- **Opus Permission Gateway** — AI-powered auto-approve
- **Worktree Orchestration** — Parallel development
- **Database Analytics** — Query any database via CLI

---

## Documentation

| Document | Description |
|----------|-------------|
| [VISION.md](docs/VISION.md) | North star philosophy |
| [GAMEPLAN.md](docs/GAMEPLAN.md) | Master integration plan |
| [BLUEPRINT.md](docs/BLUEPRINT.md) | Technical architecture |
| [V1_FEATURE_INVENTORY.md](docs/V1_FEATURE_INVENTORY.md) | V1 features reference |
| [STATUS.md](STATUS.md) | Current project state |
| [DECISIONS.md](DECISIONS.md) | Architecture decisions |
| [CHANGELOG.md](CHANGELOG.md) | Version history |

---

## Project Structure

```
claude-sentient/
├── docs/                  # Planning & design
├── schemas/               # JSON Schemas (source of truth)
├── core/                  # Orchestrator
├── phases/                # 10 modular phases
├── skills/                # Auto-triggered behaviors
├── commands/              # /cc-* commands
├── agents/                # Specialist agents
├── gates/                 # Quality gates
├── patterns/              # Architecture patterns
├── rules/                 # Topic standards
├── events/                # Event definitions
├── state/                 # State schemas
├── config/                # Configuration
├── tools/                 # Python CLI tools
├── tests/                 # Test infrastructure
├── .claude/               # Runtime data
└── reference/v1/          # V1 source (read-only)
```

---

## Development Status

| Phase | Status | Description |
|-------|--------|-------------|
| 0. Foundation | 🔄 Active | Schemas, events, state |
| 1. Core Loop | ⏳ Pending | 10 phases, orchestrator |
| 2. Quality Gates | ⏳ Pending | 18 gates |
| 3. Learning Engine | ⏳ Pending | Self-improvement |
| 4. Advanced Features | ⏳ Pending | Boris integrations |
| 5. Full Migration | ⏳ Pending | V1 parity + V2 |
| 6. Polish | ⏳ Pending | Docs, performance |

---

## Contributing

See [CLAUDE.md](CLAUDE.md) for development guidelines.

---

## License

MIT

---

## Acknowledgments

- V1 foundation: [claude-conductor](https://github.com/thebiglaskowski/claude-conductor)
- Tips and patterns: Boris Cherny and the Claude Code team
- Built with: [Claude Code](https://claude.ai/code)

---

*Claude Sentient: The Autonomous Meta-Cognitive Development Engine*
