# Claude Conductor 2.0

> A ground-up redesign of the AI-assisted development platform

## Overview

Claude Conductor 2.0 treats the platform as a **proper framework** with:

- **JSON Schemas** for validation and IDE support
- **Explicit dependencies** with version constraints
- **Event-driven architecture** for loose coupling
- **Structured state** (JSON with Markdown rendering)
- **First-class extensions** for project customization
- **Generated documentation** from schemas

## Quick Start

```bash
# Validate all components
conductor validate

# Generate documentation
conductor docs generate

# Check dependencies
conductor deps check

# Initialize a project
conductor init

# Migrate from v1
conductor migrate --from=v1
```

## Architecture

```
User Request
     │
     ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  CLASSIFY   │────▶│   EXECUTE   │────▶│   QUALITY   │
│  (Phase 1)  │     │  (Phase 5)  │     │  (Phase 7)  │
└─────────────┘     └─────────────┘     └─────────────┘
     │                    │                    │
     │                    │                    │
     ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────┐
│                     EVENT BUS                        │
│  (publish/subscribe, typed payloads, async)         │
└─────────────────────────────────────────────────────┘
     │                    │                    │
     ▼                    ▼                    ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   SKILLS    │     │   AGENTS    │     │    GATES    │
│  (auto)     │     │ (specialist)│     │ (quality)   │
└─────────────┘     └─────────────┘     └─────────────┘
```

## Key Differences from V1

| Aspect | V1 | V2 |
|--------|----|----|
| Format | Markdown + YAML frontmatter | YAML/JSON + Markdown content |
| Validation | Convention-based | Schema-enforced |
| Dependencies | Implicit | Explicit with versions |
| Events | Fixed hooks | Pub/sub events |
| State | Parsed Markdown | JSON + rendered Markdown |
| Config | Scattered | Hierarchical with precedence |
| Extensions | Fork and modify | First-class extension points |
| Documentation | Manual | Generated from schemas |

## Documentation

- [BLUEPRINT.md](BLUEPRINT.md) — Complete design specification (2000+ lines)
- [PLANNING.md](PLANNING.md) — Priority questionnaire and decision log
- [docs/skills.md](docs/skills.md) — Skill reference (generated)
- [docs/commands.md](docs/commands.md) — Command reference (generated)
- [docs/events.md](docs/events.md) — Event reference (generated)
- [docs/api.md](docs/api.md) — Full API reference (generated)

## Getting Started

1. **Review the planning questionnaire**: Fill out [PLANNING.md](PLANNING.md) to establish priorities
2. **Read the blueprint**: [BLUEPRINT.md](BLUEPRINT.md) has the complete architecture
3. **Check feature parity**: Blueprint includes full V1→V2 migration checklist

## Project Structure

```
claude-conductor-2/
├── schemas/          # JSON Schemas (source of truth)
├── core/             # Minimal orchestrator
├── phases/           # Modular phases (10 files)
├── gates/            # Quality gates (modular)
├── skills/           # Auto-triggered behaviors
├── commands/         # Explicit invocations
├── agents/           # Specialist agents
├── patterns/         # Architecture patterns
├── rules/            # Topic standards
├── events/           # Event definitions
├── state/            # State schemas
├── config/           # Configuration
├── templates/        # Project scaffolding
├── tools/            # CLI tooling
├── tests/            # Test infrastructure
└── docs/             # Generated documentation
```

## Implementation Status

See [BLUEPRINT.md](BLUEPRINT.md) for the 8-phase implementation plan.

| Phase | Status | Description |
|-------|--------|-------------|
| 1. Foundation | 🔲 | Schemas, validation, config |
| 2. Core Loop | 🔲 | Orchestrator, phases, state |
| 3. Event System | 🔲 | Pub/sub, wiring |
| 4. Full Phases | 🔲 | All 10 phases |
| 5. Skills & Commands | 🔲 | Migration, enhancement |
| 6. Extensions | 🔲 | Custom gates, overrides |
| 7. Documentation | 🔲 | Generators, CI |
| 8. Migration | 🔲 | V1 migration tool |

## License

MIT
