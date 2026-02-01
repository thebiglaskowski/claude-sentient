# Claude Conductor 2.0 — Complete Redesign Blueprint

## Executive Summary

Claude Conductor 2.0 is a ground-up reimagining of the AI-assisted development platform. Built on lessons learned from v1, this version treats the platform as a **proper framework** with schemas, typed interfaces, dependency management, and tooling—not just a collection of prompts.

### Design Philosophy

1. **Schema-First** — Every component defined by JSON Schema before implementation
2. **Explicit Dependencies** — Formal dependency graph with version constraints
3. **Modular Composition** — Small, focused components that compose into larger behaviors
4. **Structured State** — JSON state with Markdown rendering, not parsed Markdown
5. **Event-Driven** — Publish/subscribe architecture for loose coupling
6. **Generated Artifacts** — Documentation and indexes are build outputs, not source files
7. **Local Extensibility** — First-class support for project-specific customization

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Directory Structure](#directory-structure)
3. [Schema System](#schema-system)
4. [Core Components](#core-components)
5. [Dependency Management](#dependency-management)
6. [Event System](#event-system)
7. [State Management](#state-management)
8. [Configuration Hierarchy](#configuration-hierarchy)
9. [Extension System](#extension-system)
10. [Tooling](#tooling)
11. [Migration Path](#migration-path)
12. [Implementation Phases](#implementation-phases)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        CLAUDE CONDUCTOR 2.0 ARCHITECTURE                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│  │   SCHEMAS    │───▶│  VALIDATOR   │───▶│   LOADER     │                  │
│  │  (JSON/YAML) │    │  (Build-time)│    │  (Runtime)   │                  │
│  └──────────────┘    └──────────────┘    └──────┬───────┘                  │
│                                                  │                          │
│         ┌────────────────────────────────────────┼──────────────────┐       │
│         │                                        ▼                  │       │
│         │  ┌─────────────────────────────────────────────────────┐ │       │
│         │  │                    EVENT BUS                        │ │       │
│         │  │  (publish/subscribe, async, typed payloads)         │ │       │
│         │  └─────────────────────────────────────────────────────┘ │       │
│         │         │              │              │              │    │       │
│         │         ▼              ▼              ▼              ▼    │       │
│         │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │       │
│         │  │  SKILLS  │  │ COMMANDS │  │  AGENTS  │  │  GATES   │ │       │
│         │  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │       │
│         │         │              │              │              │    │       │
│         │         └──────────────┴──────────────┴──────────────┘    │       │
│         │                              │                            │       │
│         │                              ▼                            │       │
│         │  ┌─────────────────────────────────────────────────────┐ │       │
│         │  │                 ORCHESTRATOR                        │ │       │
│         │  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   │ │       │
│         │  │  │ Phase 1 │→│ Phase 2 │→│ Phase N │→│ Gates   │   │ │       │
│         │  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘   │ │       │
│         │  └─────────────────────────────────────────────────────┘ │       │
│         │                              │                            │       │
│         │                              ▼                            │       │
│         │  ┌─────────────────────────────────────────────────────┐ │       │
│         │  │                   STATE STORE                       │ │       │
│         │  │  (JSON storage, Markdown rendering, versioned)      │ │       │
│         │  └─────────────────────────────────────────────────────┘ │       │
│         │                                                          │       │
│         │                      RUNTIME LAYER                       │       │
│         └──────────────────────────────────────────────────────────┘       │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                           CONFIG HIERARCHY                            │  │
│  │  CLI flags > ENV vars > Project config > User config > Defaults       │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                          EXTENSION LAYER                              │  │
│  │  Local skills, custom gates, project patterns, overrides             │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Key Architectural Decisions

| Decision | Rationale |
|----------|-----------|
| JSON Schema for all components | Enables validation, IDE autocomplete, type safety |
| Event bus for communication | Loose coupling, easy to extend, testable |
| Phases as separate files | Independent versioning, easier maintenance |
| JSON state with MD rendering | Reliable parsing, human-readable output |
| Config hierarchy | Predictable precedence, easy debugging |
| Local extensions first-class | Projects can customize without forking |

---

## Directory Structure

```
claude-conductor-2/
├── README.md                    # Quick start guide
├── CLAUDE.md                    # Platform instructions (generated)
├── package.json                 # Version, dependencies, scripts
├── conductor.config.json        # Platform configuration schema
│
├── schemas/                     # JSON Schemas (source of truth)
│   ├── skill.schema.json
│   ├── command.schema.json
│   ├── agent.schema.json
│   ├── pattern.schema.json
│   ├── gate.schema.json
│   ├── phase.schema.json
│   ├── event.schema.json
│   ├── state.schema.json
│   └── config.schema.json
│
├── core/                        # Core orchestration (minimal)
│   ├── orchestrator.md          # Main loop skeleton (~100 lines)
│   ├── classifier.md            # Query classification
│   ├── synthesizer.md           # Result synthesis
│   └── recovery.md              # Error recovery strategies
│
├── phases/                      # Modular phases (each ~50-100 lines)
│   ├── _phase.schema.json       # Phase interface definition
│   ├── 01-classify.md           # Query classification
│   ├── 02-contextualize.md      # Context loading
│   ├── 03-assess.md             # Current state assessment
│   ├── 04-plan.md               # Work planning
│   ├── 05-execute.md            # Implementation
│   ├── 06-verify.md             # Testing & validation
│   ├── 07-quality.md            # Quality gates
│   ├── 08-checkpoint.md         # Commit verified work
│   ├── 09-evaluate.md           # Completion check
│   └── 10-recover.md            # Error recovery
│
├── gates/                       # Quality gates (modular)
│   ├── _gate.schema.json        # Gate interface definition
│   ├── code/
│   │   ├── lint.gate.json
│   │   ├── type-check.gate.json
│   │   ├── test-coverage.gate.json
│   │   └── security-scan.gate.json
│   ├── work/
│   │   ├── queue-empty.gate.json
│   │   ├── issues-resolved.gate.json
│   │   └── docs-complete.gate.json
│   └── custom/                  # Extension point
│       └── .gitkeep
│
├── skills/                      # Auto-triggered behaviors
│   ├── _skill.schema.json       # Skill interface definition
│   ├── orchestration/
│   │   ├── task-router.skill.yaml
│   │   ├── query-classifier.skill.yaml
│   │   ├── evaluator-optimizer.skill.yaml
│   │   ├── swarm-coordinator.skill.yaml
│   │   └── dependency-resolver.skill.yaml
│   ├── optimization/
│   │   ├── context-manager.skill.yaml
│   │   ├── cache-controller.skill.yaml
│   │   └── budget-monitor.skill.yaml
│   ├── quality/
│   │   ├── gate-runner.skill.yaml
│   │   ├── severity-classifier.skill.yaml
│   │   └── definition-of-done.skill.yaml
│   └── workflow/
│       ├── pre-commit.skill.yaml
│       ├── pre-merge.skill.yaml
│       └── checkpoint.skill.yaml
│
├── commands/                    # Explicit invocations (/cc-*)
│   ├── _command.schema.json
│   ├── planning/
│   │   ├── plan.cmd.yaml
│   │   ├── spike.cmd.yaml
│   │   └── audit.cmd.yaml
│   ├── execution/
│   │   ├── loop.cmd.yaml
│   │   ├── daily.cmd.yaml
│   │   └── analyze.cmd.yaml
│   ├── quality/
│   │   ├── review.cmd.yaml
│   │   ├── test.cmd.yaml
│   │   ├── secure.cmd.yaml
│   │   └── assess.cmd.yaml
│   ├── git/
│   │   ├── commit.cmd.yaml
│   │   ├── pr.cmd.yaml
│   │   └── revert.cmd.yaml
│   └── docs/
│       ├── changelog.cmd.yaml
│       ├── adr.cmd.yaml
│       └── docs.cmd.yaml
│
├── agents/                      # Specialized expert agents
│   ├── _agent.schema.json
│   ├── code-reviewer.agent.yaml
│   ├── security-analyst.agent.yaml
│   ├── test-engineer.agent.yaml
│   ├── researcher.agent.yaml
│   └── ui-expert.agent.yaml
│
├── patterns/                    # Reusable architecture patterns
│   ├── _pattern.schema.json
│   ├── architecture/
│   │   ├── repository.pattern.yaml
│   │   ├── service-layer.pattern.yaml
│   │   └── clean-architecture.pattern.yaml
│   ├── resilience/
│   │   ├── retry-backoff.pattern.yaml
│   │   └── circuit-breaker.pattern.yaml
│   └── api/
│       ├── pagination.pattern.yaml
│       └── rate-limiting.pattern.yaml
│
├── rules/                       # Topic-specific standards
│   ├── _rule.schema.json
│   ├── security.rule.yaml
│   ├── testing.rule.yaml
│   ├── git-workflow.rule.yaml
│   └── code-quality.rule.yaml
│
├── events/                      # Event definitions
│   ├── _event.schema.json
│   ├── lifecycle.events.yaml    # Session, phase, iteration events
│   ├── quality.events.yaml      # Gate pass/fail events
│   ├── context.events.yaml      # Budget, compaction events
│   └── work.events.yaml         # Queue, task, dependency events
│
├── state/                       # State schemas and defaults
│   ├── session.state.schema.json
│   ├── loop.state.schema.json
│   ├── queue.state.schema.json
│   └── defaults/
│       ├── session.default.json
│       ├── loop.default.json
│       └── queue.default.json
│
├── config/                      # Configuration
│   ├── defaults.config.json     # Platform defaults
│   ├── thresholds.config.json   # Quality thresholds
│   └── models.config.json       # Model selection rules
│
├── templates/                   # Project scaffolding
│   ├── project/
│   │   ├── .claude/
│   │   │   ├── config.json      # Project config template
│   │   │   ├── extensions/      # Local extension point
│   │   │   └── state/           # Project state storage
│   │   ├── CLAUDE.md            # Generated for project
│   │   └── STATUS.md            # Project status template
│   └── extension/
│       ├── skill.template.yaml
│       ├── gate.template.yaml
│       └── command.template.yaml
│
├── tools/                       # CLI tooling
│   ├── validate.py              # Schema validation
│   ├── generate-docs.py         # Documentation generator
│   ├── check-deps.py            # Dependency graph analysis
│   ├── render-state.py          # JSON → Markdown rendering
│   ├── migrate.py               # v1 → v2 migration
│   └── init.py                  # Project initialization
│
├── tests/                       # Test infrastructure
│   ├── conftest.py
│   ├── validators/
│   ├── integration/
│   └── fixtures/
│
└── docs/                        # Generated documentation
    ├── README.md                # (generated)
    ├── skills.md                # (generated from skill schemas)
    ├── commands.md              # (generated from command schemas)
    ├── events.md                # (generated from event schemas)
    ├── api.md                   # (generated from all schemas)
    └── architecture.md          # (generated from dependency graph)
```

---

## Schema System

### Design Principles

1. **Single Source of Truth** — Schemas define structure, docs generated from them
2. **Composable** — Schemas reference each other via `$ref`
3. **Validated at Build Time** — CI fails if component doesn't match schema
4. **Self-Documenting** — `title`, `description`, `examples` in schema

### Base Component Schema

All components extend this base:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://claude-conductor.dev/schemas/base.schema.json",
  "title": "Base Component",
  "type": "object",
  "required": ["name", "version", "description"],
  "properties": {
    "name": {
      "type": "string",
      "pattern": "^[a-z][a-z0-9-]*$",
      "description": "Unique identifier (kebab-case)"
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$",
      "description": "Semantic version"
    },
    "description": {
      "type": "string",
      "minLength": 10,
      "maxLength": 200,
      "description": "One-line description"
    },
    "deprecated": {
      "type": "boolean",
      "default": false
    },
    "deprecatedMessage": {
      "type": "string"
    },
    "tags": {
      "type": "array",
      "items": { "type": "string" }
    },
    "metadata": {
      "type": "object",
      "additionalProperties": true
    }
  }
}
```

### Skill Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://claude-conductor.dev/schemas/skill.schema.json",
  "title": "Skill Definition",
  "allOf": [{ "$ref": "base.schema.json" }],
  "properties": {
    "triggers": {
      "type": "array",
      "items": {
        "oneOf": [
          { "type": "string", "description": "Simple phrase trigger" },
          {
            "type": "object",
            "properties": {
              "pattern": { "type": "string", "description": "Regex pattern" },
              "priority": { "type": "integer", "minimum": 0, "maximum": 100 }
            }
          }
        ]
      },
      "description": "Phrases or patterns that activate this skill"
    },
    "model": {
      "type": "string",
      "enum": ["haiku", "sonnet", "opus"],
      "default": "sonnet"
    },
    "depends": {
      "type": "object",
      "additionalProperties": {
        "type": "string",
        "pattern": "^[<>=^~]*\\d+\\.\\d+\\.\\d+$"
      },
      "description": "Required skills with version constraints"
    },
    "provides": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Capabilities this skill provides"
    },
    "conflicts": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Skills that cannot be active simultaneously"
    },
    "subscribes": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "event": { "type": "string" },
          "handler": { "type": "string" }
        },
        "required": ["event", "handler"]
      },
      "description": "Events this skill responds to"
    },
    "publishes": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Events this skill emits"
    },
    "config": {
      "type": "object",
      "description": "Configuration schema for this skill"
    },
    "content": {
      "type": "string",
      "description": "Markdown content with instructions"
    }
  },
  "required": ["triggers"]
}
```

### Command Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://claude-conductor.dev/schemas/command.schema.json",
  "title": "Command Definition",
  "allOf": [{ "$ref": "base.schema.json" }],
  "properties": {
    "command": {
      "type": "string",
      "pattern": "^cc-[a-z][a-z0-9-]*$",
      "description": "Slash command name (must start with cc-)"
    },
    "aliases": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Alternative command names"
    },
    "arguments": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "type": { "type": "string", "enum": ["string", "number", "boolean", "array"] },
          "required": { "type": "boolean", "default": false },
          "default": {},
          "description": { "type": "string" }
        },
        "required": ["name", "type"]
      }
    },
    "flags": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "short": { "type": "string", "maxLength": 1 },
          "type": { "type": "string", "enum": ["boolean", "string", "number"] },
          "default": {},
          "description": { "type": "string" }
        },
        "required": ["name"]
      }
    },
    "model": {
      "type": "string",
      "enum": ["haiku", "sonnet", "opus"],
      "default": "sonnet"
    },
    "category": {
      "type": "string",
      "enum": ["planning", "execution", "quality", "git", "docs", "operations"]
    },
    "invokes": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Skills or commands this command invokes"
    },
    "content": {
      "type": "string",
      "description": "Markdown content with instructions"
    }
  },
  "required": ["command", "category"]
}
```

### Gate Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://claude-conductor.dev/schemas/gate.schema.json",
  "title": "Quality Gate Definition",
  "allOf": [{ "$ref": "base.schema.json" }],
  "properties": {
    "category": {
      "type": "string",
      "enum": ["code", "work", "custom"],
      "description": "Gate category"
    },
    "blocking": {
      "type": "boolean",
      "default": true,
      "description": "Whether failure blocks progress"
    },
    "check": {
      "type": "object",
      "properties": {
        "type": {
          "type": "string",
          "enum": ["command", "file", "metric", "custom"]
        },
        "command": { "type": "string" },
        "file": { "type": "string" },
        "metric": { "type": "string" },
        "threshold": {},
        "operator": {
          "type": "string",
          "enum": ["eq", "ne", "gt", "gte", "lt", "lte", "contains", "matches"]
        }
      },
      "required": ["type"]
    },
    "fix": {
      "type": "object",
      "properties": {
        "auto": { "type": "boolean", "default": false },
        "skill": { "type": "string" },
        "maxAttempts": { "type": "integer", "default": 3 }
      },
      "description": "Auto-fix configuration"
    },
    "severity": {
      "type": "string",
      "enum": ["S0", "S1", "S2", "S3"],
      "description": "Severity if gate fails"
    },
    "appliesTo": {
      "type": "array",
      "items": { "type": "string" },
      "description": "File patterns this gate applies to"
    }
  },
  "required": ["category", "check"]
}
```

### Event Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://claude-conductor.dev/schemas/event.schema.json",
  "title": "Event Definition",
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "pattern": "^[a-z]+\\.[a-z]+\\.[a-z]+$",
      "description": "Event name (category.entity.action)"
    },
    "description": { "type": "string" },
    "payload": {
      "type": "object",
      "description": "JSON Schema for event payload"
    },
    "emitters": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Components that emit this event"
    },
    "subscribers": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Components that handle this event"
    }
  },
  "required": ["name", "payload"]
}
```

### State Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://claude-conductor.dev/schemas/loop-state.schema.json",
  "title": "Loop State",
  "type": "object",
  "properties": {
    "version": { "type": "string", "const": "2.0" },
    "sessionId": { "type": "string", "format": "uuid" },
    "startedAt": { "type": "string", "format": "date-time" },
    "iteration": { "type": "integer", "minimum": 0 },
    "phase": {
      "type": "string",
      "enum": ["classify", "contextualize", "assess", "plan", "execute", "verify", "quality", "checkpoint", "evaluate", "recover"]
    },
    "classification": {
      "type": "object",
      "properties": {
        "type": { "type": "string", "enum": ["depth-first", "breadth-first", "straightforward"] },
        "complexity": { "type": "string", "enum": ["simple", "medium", "complex"] },
        "subagentCount": { "type": "integer", "minimum": 0 },
        "orchestrationMode": { "type": "string", "enum": ["standard", "swarm", "pipeline"] }
      }
    },
    "workQueue": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "priority": { "type": "string", "enum": ["S0", "S1", "S2", "S3"] },
          "title": { "type": "string" },
          "status": { "type": "string", "enum": ["pending", "in-progress", "blocked", "done", "failed"] },
          "blockedBy": { "type": "array", "items": { "type": "string" } },
          "blocks": { "type": "array", "items": { "type": "string" } },
          "assignedTo": { "type": "string" },
          "createdAt": { "type": "string", "format": "date-time" },
          "updatedAt": { "type": "string", "format": "date-time" }
        },
        "required": ["id", "priority", "title", "status"]
      }
    },
    "gates": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "properties": {
          "status": { "type": "string", "enum": ["pending", "passed", "failed", "skipped"] },
          "lastCheck": { "type": "string", "format": "date-time" },
          "value": {},
          "threshold": {},
          "attempts": { "type": "integer" },
          "error": { "type": "string" }
        }
      }
    },
    "context": {
      "type": "object",
      "properties": {
        "budgetUsed": { "type": "number", "minimum": 0, "maximum": 1 },
        "level": { "type": "string", "enum": ["green", "yellow", "orange", "red"] },
        "compactionReady": { "type": "boolean" },
        "lastCompaction": { "type": "string", "format": "date-time" }
      }
    },
    "metrics": {
      "type": "object",
      "properties": {
        "iterationsTotal": { "type": "integer" },
        "gatesPassed": { "type": "integer" },
        "gatesFailed": { "type": "integer" },
        "tasksCompleted": { "type": "integer" },
        "pivotsCount": { "type": "integer" },
        "agentsSpawned": { "type": "integer" }
      }
    },
    "history": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "iteration": { "type": "integer" },
          "phase": { "type": "string" },
          "action": { "type": "string" },
          "result": { "type": "string" },
          "timestamp": { "type": "string", "format": "date-time" }
        }
      }
    }
  },
  "required": ["version", "sessionId", "iteration", "phase", "workQueue", "gates"]
}
```

---

## Core Components

### Orchestrator (core/orchestrator.md)

The orchestrator is minimal—it only coordinates phase execution:

```yaml
# core/orchestrator.md
name: orchestrator
version: 2.0.0
description: Minimal loop coordinator that executes phases in sequence

# The orchestrator is ~100 lines, delegating everything to phases
content: |
  # Orchestrator

  Execute phases in sequence until completion criteria met.

  ## Loop

  ```
  WHILE not complete:
    FOR phase IN phases:
      result = execute_phase(phase)
      IF result.error:
        emit("loop.phase.error", { phase, error })
        phase = "recover"
      emit("loop.phase.complete", { phase, result })

    IF all_gates_passed AND queue_empty:
      emit("loop.complete", { metrics })
      complete = true
  ```

  ## Responsibilities

  - Execute phases in order
  - Emit lifecycle events
  - Track iteration count
  - Delegate all logic to phases

  ## NOT Responsible For

  - Classification (phase 1)
  - Context management (phase 2)
  - Quality checks (phase 7)
  - Recovery logic (phase 10)
```

### Phase Interface

Each phase implements a standard interface:

```yaml
# phases/_phase.interface.yaml
interface: Phase
version: 1.0.0

methods:
  execute:
    input:
      state: LoopState
      context: ExecutionContext
    output:
      state: LoopState
      events: Event[]
      next: string | null  # Next phase or null to continue

  canSkip:
    input:
      state: LoopState
    output:
      skip: boolean
      reason: string

properties:
  name: string
  order: integer
  timeout: duration
  retryable: boolean
```

### Example Phase: Classify

```yaml
# phases/01-classify.md
name: classify
version: 1.0.0
order: 1
description: Classify task type and determine orchestration strategy

interface: Phase

config:
  defaultClassification: straightforward
  complexityThresholds:
    simple: 2
    medium: 10

subscribes:
  - event: loop.iteration.start
    handler: onIterationStart

publishes:
  - loop.task.classified

content: |
  # Phase 1: Classify

  Analyze the task and determine the optimal execution strategy.

  ## Process

  1. **Parse Task Intent**
     - Extract action verbs (implement, fix, review, refactor)
     - Identify scope (single file, module, codebase)
     - Detect constraints (security, performance, deadline)

  2. **Determine Classification**

     | Signals | Classification |
     |---------|----------------|
     | Single file, simple change | straightforward |
     | Deep analysis, complex problem | depth-first |
     | Many independent tasks, review | breadth-first |

  3. **Calculate Subagent Count**

     ```
     IF straightforward: 0
     IF depth-first: 1 (specialist)
     IF breadth-first:
       count = ceil(task_count / 3)
       count = clamp(count, 3, 20)
     ```

  4. **Select Orchestration Mode**

     | Classification | Dependencies | Mode |
     |----------------|--------------|------|
     | straightforward | - | standard |
     | depth-first | - | standard |
     | breadth-first | no | swarm |
     | breadth-first | yes | pipeline |

  5. **Emit Classification Event**

     ```json
     {
       "event": "loop.task.classified",
       "payload": {
         "type": "breadth-first",
         "complexity": "medium",
         "subagentCount": 5,
         "orchestrationMode": "swarm"
       }
     }
     ```

  ## Output

  Update state.classification with results.
```

### Example Phase: Quality

```yaml
# phases/07-quality.md
name: quality
version: 1.0.0
order: 7
description: Run all quality gates with evaluator-optimizer retry loops

interface: Phase

depends:
  evaluator-optimizer: ">=1.0.0"

config:
  maxRetries: 3
  parallelGates: true

subscribes:
  - event: loop.phase.verify.complete
    handler: onVerifyComplete

publishes:
  - quality.gate.started
  - quality.gate.passed
  - quality.gate.failed
  - quality.gate.retry

content: |
  # Phase 7: Quality

  Run all quality gates. Failed gates trigger evaluator-optimizer loops.

  ## Gate Execution

  ```
  FOR gate IN gates:
    emit("quality.gate.started", { gate })

    result = run_gate(gate)

    IF result.passed:
      emit("quality.gate.passed", { gate, value: result.value })
      state.gates[gate].status = "passed"
    ELSE:
      # Trigger evaluator-optimizer loop
      FOR attempt IN 1..maxRetries:
        emit("quality.gate.retry", { gate, attempt })

        fix = evaluate_failure(gate, result)
        apply_fix(fix)
        result = run_gate(gate)

        IF result.passed:
          emit("quality.gate.passed", { gate, value: result.value })
          break

      IF not result.passed:
        emit("quality.gate.failed", { gate, error: result.error })
        add_to_queue(gate.failure_as_task)
  ```

  ## Gates

  ### Code Quality (blocking)
  - lint: 0 errors, 0 warnings
  - type-check: 0 errors
  - test-coverage: >= 80%
  - security-scan: 0 S0/S1

  ### Work Completion (blocking)
  - queue-empty: 0 pending tasks
  - issues-resolved: 0 S0/S1 open
  - docs-complete: README + CHANGELOG present

  ## Evaluator-Optimizer Integration

  When a gate fails:
  1. **Evaluate**: Identify root cause of failure
  2. **Optimize**: Generate minimal fix
  3. **Re-evaluate**: Run gate again
  4. **Iterate**: Up to 3 attempts
  5. **Escalate**: Add to queue if still failing
```

---

## Dependency Management

### Dependency Declaration

```yaml
# skills/orchestration/evaluator-optimizer.skill.yaml
name: evaluator-optimizer
version: 1.0.0
description: Feedback loops that iterate until quality threshold met

depends:
  severity-classifier: ">=1.0.0"
  gate-runner: ">=1.0.0"

provides:
  - feedback-loop
  - quality-iteration

conflicts:
  - legacy-retry  # Old retry mechanism

# ...
```

### Dependency Resolution

```python
# tools/check-deps.py (simplified)

def resolve_dependencies(component):
    """
    Resolve all dependencies for a component.
    Returns ordered list for loading or raises on conflict.
    """
    resolved = []
    seen = set()

    def visit(name, version_constraint):
        if name in seen:
            return  # Already resolved

        component = load_component(name)

        # Check version constraint
        if not satisfies(component.version, version_constraint):
            raise VersionConflict(name, version_constraint, component.version)

        # Check conflicts
        for conflict in component.conflicts:
            if conflict in seen:
                raise ConflictError(name, conflict)

        # Resolve dependencies first
        for dep_name, dep_version in component.depends.items():
            visit(dep_name, dep_version)

        seen.add(name)
        resolved.append(component)

    visit(component.name, f">={component.version}")
    return resolved
```

### Dependency Graph Visualization

```
# Generated by tools/check-deps.py --graph

evaluator-optimizer@1.0.0
├── severity-classifier@1.0.0
└── gate-runner@1.0.0
    └── definition-of-done@1.0.0

swarm-coordinator@1.0.0
├── task-router@1.0.0
│   └── query-classifier@1.0.0
├── dependency-resolver@1.0.0
└── result-synthesizer@1.0.0
```

---

## Event System

### Event Categories

```yaml
# events/lifecycle.events.yaml
events:
  - name: session.started
    description: New session began
    payload:
      sessionId: { type: string, format: uuid }
      startedAt: { type: string, format: date-time }
    emitters: [orchestrator]
    subscribers: [context-manager, metrics-logger]

  - name: loop.iteration.start
    description: Loop iteration beginning
    payload:
      iteration: { type: integer }
      phase: { type: string }
    emitters: [orchestrator]
    subscribers: [budget-monitor, checkpoint]

  - name: loop.phase.complete
    description: Phase finished execution
    payload:
      phase: { type: string }
      duration: { type: number }
      result: { type: object }
    emitters: [orchestrator]
    subscribers: [metrics-logger, decision-logger]

  - name: loop.complete
    description: Loop finished successfully
    payload:
      iterations: { type: integer }
      duration: { type: number }
      metrics: { type: object }
    emitters: [orchestrator]
    subscribers: [session-end, changelog-automation]
```

```yaml
# events/quality.events.yaml
events:
  - name: quality.gate.started
    payload:
      gate: { type: string }
      iteration: { type: integer }
    emitters: [phase-quality]
    subscribers: [metrics-logger]

  - name: quality.gate.passed
    payload:
      gate: { type: string }
      value: {}
      threshold: {}
    emitters: [phase-quality]
    subscribers: [checkpoint, metrics-logger]

  - name: quality.gate.failed
    payload:
      gate: { type: string }
      error: { type: string }
      attempts: { type: integer }
    emitters: [phase-quality]
    subscribers: [evaluator-optimizer, decision-logger, queue-manager]

  - name: quality.gate.retry
    payload:
      gate: { type: string }
      attempt: { type: integer }
      fix: { type: object }
    emitters: [evaluator-optimizer]
    subscribers: [metrics-logger]
```

```yaml
# events/context.events.yaml
events:
  - name: context.threshold.crossed
    payload:
      level: { type: string, enum: [green, yellow, orange, red] }
      usage: { type: number }
      previousLevel: { type: string }
    emitters: [budget-monitor]
    subscribers: [context-manager, orchestrator]

  - name: context.compaction.started
    payload:
      triggerLevel: { type: string }
      estimatedSavings: { type: number }
    emitters: [context-manager]
    subscribers: [metrics-logger]

  - name: context.compaction.complete
    payload:
      tokensSaved: { type: number }
      duration: { type: number }
    emitters: [context-manager]
    subscribers: [budget-monitor]
```

### Event Subscription in Skills

```yaml
# skills/optimization/context-manager.skill.yaml
name: context-manager
version: 2.0.0

subscribes:
  - event: context.threshold.crossed
    handler: onThresholdCrossed
  - event: loop.iteration.start
    handler: onIterationStart
  - event: session.started
    handler: onSessionStart

publishes:
  - context.compaction.started
  - context.compaction.complete

content: |
  # Context Manager

  ## Event Handlers

  ### onThresholdCrossed

  ```
  IF level == "yellow":
    start_background_compaction()

  IF level == "orange":
    ensure_compaction_ready()

  IF level == "red":
    swap_to_compacted_context()
    emit("context.compaction.complete", { tokensSaved })
  ```

  ### onIterationStart

  ```
  check_budget()
  IF budget > 50%:
    emit("context.threshold.crossed", { level: calculate_level() })
  ```
```

---

## State Management

### JSON State with Markdown Rendering

State is stored as JSON but rendered as Markdown for human readability:

```json
// .claude/state/loop.state.json
{
  "version": "2.0",
  "sessionId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "startedAt": "2026-01-31T10:00:00Z",
  "iteration": 7,
  "phase": "quality",
  "classification": {
    "type": "breadth-first",
    "complexity": "medium",
    "subagentCount": 5,
    "orchestrationMode": "swarm"
  },
  "workQueue": [
    {
      "id": "WQ-001",
      "priority": "S1",
      "title": "Fix authentication bypass",
      "status": "done",
      "blockedBy": [],
      "blocks": ["WQ-003"],
      "updatedAt": "2026-01-31T10:15:00Z"
    },
    {
      "id": "WQ-002",
      "priority": "S2",
      "title": "Add input validation",
      "status": "in-progress",
      "blockedBy": [],
      "blocks": [],
      "assignedTo": "worker-2",
      "updatedAt": "2026-01-31T10:20:00Z"
    },
    {
      "id": "WQ-003",
      "priority": "S2",
      "title": "Integration tests for auth",
      "status": "pending",
      "blockedBy": ["WQ-001"],
      "blocks": [],
      "updatedAt": "2026-01-31T10:10:00Z"
    }
  ],
  "gates": {
    "lint": { "status": "passed", "lastCheck": "2026-01-31T10:18:00Z", "value": 0 },
    "type-check": { "status": "passed", "lastCheck": "2026-01-31T10:18:00Z", "value": 0 },
    "test-coverage": { "status": "failed", "lastCheck": "2026-01-31T10:19:00Z", "value": 72, "threshold": 80, "attempts": 1 },
    "security-scan": { "status": "passed", "lastCheck": "2026-01-31T10:17:00Z", "value": 0 }
  },
  "context": {
    "budgetUsed": 0.62,
    "level": "yellow",
    "compactionReady": true,
    "lastCompaction": null
  },
  "metrics": {
    "iterationsTotal": 7,
    "gatesPassed": 9,
    "gatesFailed": 3,
    "tasksCompleted": 4,
    "pivotsCount": 1,
    "agentsSpawned": 5
  }
}
```

### Rendered Markdown (Generated)

```markdown
# Loop State

**Session:** a1b2c3d4 | **Started:** 2026-01-31T10:00:00Z | **Iteration:** 7

## Classification

| Property | Value |
|----------|-------|
| Type | breadth-first |
| Complexity | medium |
| Subagents | 5 |
| Mode | swarm |

## Work Queue

| ID | Priority | Title | Status | Blocked By |
|----|----------|-------|--------|------------|
| WQ-001 | S1 | Fix authentication bypass | ✅ Done | — |
| WQ-002 | S2 | Add input validation | 🔄 In Progress | — |
| WQ-003 | S2 | Integration tests for auth | ⏳ Pending | WQ-001 |

## Quality Gates

| Gate | Status | Value | Threshold |
|------|--------|-------|-----------|
| lint | ✅ Pass | 0 | 0 |
| type-check | ✅ Pass | 0 | 0 |
| test-coverage | ❌ Fail | 72% | 80% |
| security-scan | ✅ Pass | 0 | 0 |

## Context Budget

```
[████████████░░░░░░░░] 62% (Yellow)
Compaction: Ready
```

## Metrics

- Iterations: 7
- Gates Passed: 9
- Gates Failed: 3
- Tasks Completed: 4
- Pivots: 1
- Agents Spawned: 5
```

### State Operations

```python
# tools/render-state.py

def render_state_to_markdown(state_path: str) -> str:
    """Convert JSON state to human-readable Markdown."""
    with open(state_path) as f:
        state = json.load(f)

    # Validate against schema
    validate(state, load_schema("loop-state.schema.json"))

    # Render using template
    template = load_template("loop-state.md.jinja2")
    return template.render(state=state)

def update_state(state_path: str, updates: dict) -> dict:
    """Update state with validation and event emission."""
    with open(state_path) as f:
        state = json.load(f)

    # Deep merge updates
    new_state = deep_merge(state, updates)

    # Validate
    validate(new_state, load_schema("loop-state.schema.json"))

    # Write
    with open(state_path, 'w') as f:
        json.dump(new_state, f, indent=2)

    # Re-render Markdown
    md_path = state_path.replace('.json', '.md')
    with open(md_path, 'w') as f:
        f.write(render_state_to_markdown(state_path))

    return new_state
```

---

## Configuration Hierarchy

### Precedence Order (Highest to Lowest)

1. **Command-line flags** — `--max-iterations=10`
2. **Environment variables** — `CONDUCTOR_MAX_ITERATIONS=10`
3. **Project config** — `.claude/config.json`
4. **User config** — `~/.claude/conductor.config.json`
5. **Platform defaults** — `config/defaults.config.json`

### Configuration Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://claude-conductor.dev/schemas/config.schema.json",
  "title": "Conductor Configuration",
  "type": "object",
  "properties": {
    "loop": {
      "type": "object",
      "properties": {
        "maxIterations": { "type": "integer", "default": 50, "minimum": 1 },
        "pauseOnSeverity": { "type": "string", "enum": ["S0", "S1", "S2"], "default": "S0" },
        "parallelAgents": { "type": "boolean", "default": true },
        "consecutivePassesRequired": { "type": "integer", "default": 2 }
      }
    },
    "context": {
      "type": "object",
      "properties": {
        "softThreshold": { "type": "number", "default": 0.50 },
        "warnThreshold": { "type": "number", "default": 0.70 },
        "hardThreshold": { "type": "number", "default": 0.85 },
        "backgroundCompaction": { "type": "boolean", "default": true },
        "cacheReuse": { "type": "boolean", "default": true }
      }
    },
    "gates": {
      "type": "object",
      "properties": {
        "testCoverage": { "type": "number", "default": 80 },
        "newCodeCoverage": { "type": "number", "default": 90 },
        "maxRetries": { "type": "integer", "default": 3 }
      }
    },
    "models": {
      "type": "object",
      "properties": {
        "default": { "type": "string", "enum": ["haiku", "sonnet", "opus"], "default": "sonnet" },
        "security": { "type": "string", "enum": ["haiku", "sonnet", "opus"], "default": "opus" },
        "workers": { "type": "string", "enum": ["haiku", "sonnet"], "default": "sonnet" }
      }
    },
    "extensions": {
      "type": "object",
      "properties": {
        "skillsPath": { "type": "string", "default": ".claude/extensions/skills" },
        "gatesPath": { "type": "string", "default": ".claude/extensions/gates" },
        "overridesPath": { "type": "string", "default": ".claude/extensions/overrides" }
      }
    }
  }
}
```

### Example Configurations

```json
// Platform defaults: config/defaults.config.json
{
  "loop": {
    "maxIterations": 50,
    "pauseOnSeverity": "S0",
    "parallelAgents": true,
    "consecutivePassesRequired": 2
  },
  "context": {
    "softThreshold": 0.50,
    "warnThreshold": 0.70,
    "hardThreshold": 0.85,
    "backgroundCompaction": true,
    "cacheReuse": true
  },
  "gates": {
    "testCoverage": 80,
    "newCodeCoverage": 90,
    "maxRetries": 3
  }
}
```

```json
// Project config: .claude/config.json
{
  "gates": {
    "testCoverage": 90,  // Stricter for this project
    "newCodeCoverage": 95
  },
  "models": {
    "default": "opus"  // Use opus for this complex project
  }
}
```

### Config Resolution

```python
# tools/config.py

def resolve_config() -> dict:
    """Resolve configuration with proper precedence."""

    # Start with platform defaults
    config = load_json("config/defaults.config.json")

    # Merge user config
    user_config_path = Path.home() / ".claude" / "conductor.config.json"
    if user_config_path.exists():
        config = deep_merge(config, load_json(user_config_path))

    # Merge project config
    project_config_path = Path(".claude/config.json")
    if project_config_path.exists():
        config = deep_merge(config, load_json(project_config_path))

    # Apply environment variables
    for key, value in os.environ.items():
        if key.startswith("CONDUCTOR_"):
            config_key = key[10:].lower().replace("_", ".")
            set_nested(config, config_key, parse_value(value))

    # Apply CLI flags (passed in)
    # config = deep_merge(config, cli_flags)

    # Validate final config
    validate(config, load_schema("config.schema.json"))

    return config
```

---

## Extension System

### Extension Types

1. **Local Skills** — Project-specific skills
2. **Custom Gates** — Project-specific quality gates
3. **Pattern Overrides** — Modify platform patterns
4. **Phase Overrides** — Customize phase behavior

### Extension Structure

```
.claude/
├── config.json              # Project configuration
├── extensions/
│   ├── skills/              # Local skills
│   │   └── team-standup.skill.yaml
│   ├── gates/               # Custom gates
│   │   └── e2e-tests.gate.json
│   ├── patterns/            # Additional patterns
│   │   └── our-api-style.pattern.yaml
│   └── overrides/           # Platform overrides
│       └── test-coverage.gate.patch.json
└── state/                   # Project state
    ├── loop.state.json
    └── session.state.json
```

### Creating a Local Skill

```yaml
# .claude/extensions/skills/team-standup.skill.yaml
name: team-standup
version: 1.0.0
description: Generate standup summary in our team's format

triggers:
  - "standup"
  - "daily standup"
  - "what did I do"

model: haiku

content: |
  # Team Standup Generator

  Generate standup in our team's format:

  ## Format

  ```
  **Yesterday:**
  - [Completed tasks]

  **Today:**
  - [Planned tasks]

  **Blockers:**
  - [Any blockers or none]

  **PR Reviews Needed:**
  - [List or none]
  ```

  ## Process

  1. Check git log for yesterday's commits
  2. Check work queue for today's tasks
  3. Check for any blocked items
  4. Check for open PRs awaiting review
```

### Creating a Custom Gate

```json
// .claude/extensions/gates/e2e-tests.gate.json
{
  "name": "e2e-tests",
  "version": "1.0.0",
  "description": "Run end-to-end tests with Playwright",
  "category": "custom",
  "blocking": true,
  "check": {
    "type": "command",
    "command": "npm run test:e2e",
    "successExitCode": 0
  },
  "fix": {
    "auto": false,
    "skill": "test-engineer"
  },
  "severity": "S1",
  "appliesTo": ["**/*.tsx", "**/*.ts"]
}
```

### Overriding Platform Components

```json
// .claude/extensions/overrides/test-coverage.gate.patch.json
{
  "target": "gates/code/test-coverage.gate.json",
  "patch": [
    { "op": "replace", "path": "/check/threshold", "value": 95 },
    { "op": "add", "path": "/check/excludePatterns", "value": ["**/*.test.ts", "**/mocks/**"] }
  ]
}
```

### Extension Loading

```python
# Extension loading priority:
# 1. Platform components (base)
# 2. Local extensions (additions)
# 3. Overrides (patches)

def load_components():
    components = {}

    # Load platform components
    for path in glob("skills/**/*.skill.yaml"):
        component = load_yaml(path)
        components[component["name"]] = component

    # Load local extensions (additions)
    for path in glob(".claude/extensions/skills/**/*.skill.yaml"):
        component = load_yaml(path)
        components[component["name"]] = component

    # Apply overrides (patches)
    for path in glob(".claude/extensions/overrides/**/*.patch.json"):
        patch = load_json(path)
        target = components.get(patch["target"])
        if target:
            components[patch["target"]] = apply_patch(target, patch["patch"])

    return components
```

---

## Tooling

### CLI Commands

```bash
# Validation
conductor validate                    # Validate all components
conductor validate --schema skill     # Validate only skills
conductor validate path/to/file.yaml  # Validate specific file

# Documentation
conductor docs generate               # Generate all documentation
conductor docs serve                  # Serve docs locally

# Dependencies
conductor deps check                  # Check for conflicts
conductor deps graph                  # Show dependency graph
conductor deps graph --format=dot     # Export as Graphviz

# State
conductor state show                  # Show current state (Markdown)
conductor state show --json           # Show raw JSON
conductor state reset                 # Reset to default state
conductor state export                # Export state for debugging

# Migration
conductor migrate --from=v1           # Migrate from v1
conductor migrate --dry-run           # Show what would be migrated

# Project
conductor init                        # Initialize project
conductor init --template=minimal     # Use minimal template
conductor extension create skill      # Create new skill
conductor extension create gate       # Create new gate
```

### Validation Tool

```python
# tools/validate.py

import json
import yaml
from jsonschema import validate, ValidationError
from pathlib import Path
import sys

SCHEMAS = {
    "skill": "schemas/skill.schema.json",
    "command": "schemas/command.schema.json",
    "agent": "schemas/agent.schema.json",
    "gate": "schemas/gate.schema.json",
    "pattern": "schemas/pattern.schema.json",
    "event": "schemas/event.schema.json",
}

def load_schema(schema_type: str) -> dict:
    with open(SCHEMAS[schema_type]) as f:
        return json.load(f)

def validate_file(file_path: Path) -> list[str]:
    """Validate a single file. Returns list of errors."""
    errors = []

    # Determine schema type from file extension/path
    schema_type = determine_schema_type(file_path)
    if not schema_type:
        return [f"Unknown file type: {file_path}"]

    try:
        # Load file
        if file_path.suffix in [".yaml", ".yml"]:
            with open(file_path) as f:
                content = yaml.safe_load(f)
        else:
            with open(file_path) as f:
                content = json.load(f)

        # Validate against schema
        schema = load_schema(schema_type)
        validate(content, schema)

    except ValidationError as e:
        errors.append(f"{file_path}: {e.message} at {e.json_path}")
    except Exception as e:
        errors.append(f"{file_path}: {str(e)}")

    return errors

def validate_all() -> tuple[int, int]:
    """Validate all components. Returns (passed, failed)."""
    passed = 0
    failed = 0

    patterns = [
        "skills/**/*.skill.yaml",
        "commands/**/*.cmd.yaml",
        "agents/**/*.agent.yaml",
        "gates/**/*.gate.json",
        "patterns/**/*.pattern.yaml",
        "events/**/*.events.yaml",
    ]

    for pattern in patterns:
        for file_path in Path(".").glob(pattern):
            errors = validate_file(file_path)
            if errors:
                failed += 1
                for error in errors:
                    print(f"❌ {error}")
            else:
                passed += 1
                print(f"✅ {file_path}")

    return passed, failed

if __name__ == "__main__":
    passed, failed = validate_all()
    print(f"\n{passed} passed, {failed} failed")
    sys.exit(1 if failed > 0 else 0)
```

### Documentation Generator

```python
# tools/generate-docs.py

from pathlib import Path
import yaml
import json
from jinja2 import Environment, FileSystemLoader

def generate_skill_docs():
    """Generate skills.md from all skill definitions."""
    skills = []

    for path in Path("skills").glob("**/*.skill.yaml"):
        with open(path) as f:
            skill = yaml.safe_load(f)
            skill["_path"] = str(path)
            skill["_category"] = path.parent.name
            skills.append(skill)

    # Group by category
    by_category = {}
    for skill in skills:
        cat = skill["_category"]
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(skill)

    # Render template
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("skills.md.jinja2")

    output = template.render(
        skills=skills,
        by_category=by_category,
        total=len(skills)
    )

    Path("docs/skills.md").write_text(output)
    print(f"Generated docs/skills.md ({len(skills)} skills)")

def generate_event_docs():
    """Generate events.md from all event definitions."""
    events = []

    for path in Path("events").glob("**/*.events.yaml"):
        with open(path) as f:
            content = yaml.safe_load(f)
            events.extend(content.get("events", []))

    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("events.md.jinja2")

    output = template.render(events=events, total=len(events))

    Path("docs/events.md").write_text(output)
    print(f"Generated docs/events.md ({len(events)} events)")

def generate_all():
    """Generate all documentation."""
    generate_skill_docs()
    generate_command_docs()
    generate_event_docs()
    generate_gate_docs()
    generate_api_docs()
    generate_architecture_docs()

if __name__ == "__main__":
    generate_all()
```

---

## Migration Path

### V1 to V2 Migration

```python
# tools/migrate.py

"""
Migrate claude-conductor v1 to v2.

Converts:
- Markdown skills to YAML skills
- Markdown commands to YAML commands
- LOOP_STATE.md to loop.state.json
- Various conventions to new schema
"""

import re
from pathlib import Path
import yaml
import json

def migrate_skill(v1_path: Path) -> dict:
    """Convert v1 skill (Markdown) to v2 skill (YAML)."""
    content = v1_path.read_text()

    # Parse frontmatter
    frontmatter_match = re.match(r"---\n(.+?)\n---", content, re.DOTALL)
    if frontmatter_match:
        frontmatter = yaml.safe_load(frontmatter_match.group(1))
        body = content[frontmatter_match.end():]
    else:
        frontmatter = {}
        body = content

    # Build v2 structure
    v2_skill = {
        "name": frontmatter.get("name", v1_path.stem),
        "version": frontmatter.get("version", "1.0.0"),
        "description": frontmatter.get("description", "Migrated from v1"),
        "triggers": frontmatter.get("triggers", []),
        "model": frontmatter.get("model", "sonnet"),
        "tags": frontmatter.get("tags", ["migrated"]),
        "content": body.strip()
    }

    # Parse dependencies from content
    deps = extract_dependencies(body)
    if deps:
        v2_skill["depends"] = deps

    # Parse events from content
    events = extract_events(body)
    if events.get("subscribes"):
        v2_skill["subscribes"] = events["subscribes"]
    if events.get("publishes"):
        v2_skill["publishes"] = events["publishes"]

    return v2_skill

def migrate_loop_state(v1_path: Path) -> dict:
    """Convert LOOP_STATE.md to loop.state.json."""
    content = v1_path.read_text()

    # Parse Markdown tables and sections into structured data
    state = {
        "version": "2.0",
        "sessionId": generate_uuid(),
        "iteration": extract_iteration(content),
        "phase": extract_phase(content),
        "workQueue": extract_work_queue(content),
        "gates": extract_gates(content),
        "context": extract_context(content),
        "metrics": extract_metrics(content)
    }

    return state

def migrate_project(v1_root: Path, v2_root: Path):
    """Migrate entire project from v1 to v2."""

    # Create v2 structure
    (v2_root / "skills").mkdir(parents=True, exist_ok=True)
    (v2_root / "commands").mkdir(parents=True, exist_ok=True)
    (v2_root / ".claude/state").mkdir(parents=True, exist_ok=True)

    # Migrate skills
    for v1_skill in (v1_root / "template/.claude/skills").glob("**/*.md"):
        if v1_skill.name.startswith("_"):
            continue
        v2_skill = migrate_skill(v1_skill)

        # Determine output path
        category = v1_skill.parent.name
        output_path = v2_root / "skills" / category / f"{v2_skill['name']}.skill.yaml"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            yaml.dump(v2_skill, f, default_flow_style=False)

        print(f"Migrated: {v1_skill} → {output_path}")

    # Migrate commands
    # ... similar process

    # Migrate state
    if (v1_root / "LOOP_STATE.md").exists():
        state = migrate_loop_state(v1_root / "LOOP_STATE.md")
        with open(v2_root / ".claude/state/loop.state.json", "w") as f:
            json.dump(state, f, indent=2)
        print(f"Migrated state to JSON")

    # Generate config
    generate_default_config(v2_root)

    print("\nMigration complete!")
    print("Run 'conductor validate' to check the migration.")
```

### Migration Checklist

```markdown
## V1 → V2 Migration Checklist

### Automated (run `conductor migrate`)
- [ ] Skills converted to YAML format
- [ ] Commands converted to YAML format
- [ ] State files converted to JSON
- [ ] Dependencies extracted from content
- [ ] Events inferred from patterns

### Manual Review Required
- [ ] Verify triggers are correct
- [ ] Add missing dependencies
- [ ] Define custom events
- [ ] Create extension overrides for customizations
- [ ] Update project documentation

### Validation
- [ ] Run `conductor validate`
- [ ] Run `conductor deps check`
- [ ] Test each command manually
- [ ] Verify state rendering
```

---

## Implementation Phases

### Phase 1: Foundation (Week 1-2)

**Goal:** Core infrastructure that everything builds on

- [ ] Define all JSON Schemas
- [ ] Build validation tooling
- [ ] Create project structure
- [ ] Implement config hierarchy
- [ ] Set up test infrastructure

**Deliverables:**
- All schema files in `schemas/`
- `tools/validate.py` working
- `config/defaults.config.json`
- Test suite skeleton

### Phase 2: Core Loop (Week 3-4)

**Goal:** Minimal working orchestrator

- [ ] Implement orchestrator skeleton
- [ ] Create phase interface
- [ ] Build 3 core phases (classify, execute, quality)
- [ ] Implement state management (JSON + render)
- [ ] Create basic gates (lint, tests)

**Deliverables:**
- `core/orchestrator.md`
- `phases/01-classify.md`, `05-execute.md`, `07-quality.md`
- `state/loop.state.schema.json`
- `tools/render-state.py`

### Phase 3: Event System (Week 5)

**Goal:** Loose coupling via events

- [ ] Define core events
- [ ] Implement event bus
- [ ] Wire phases to events
- [ ] Create event documentation generator

**Deliverables:**
- `events/*.events.yaml`
- Event subscription in skills
- `docs/events.md` (generated)

### Phase 4: Full Phases (Week 6-7)

**Goal:** Complete phase set

- [ ] Implement all 10 phases
- [ ] Add evaluator-optimizer integration
- [ ] Implement checkpoint phase
- [ ] Add recovery phase

**Deliverables:**
- All `phases/*.md` files
- Full gate set in `gates/`
- Integration tests

### Phase 5: Skills & Commands (Week 8-9)

**Goal:** Migrate and enhance v1 components

- [ ] Migrate core skills to YAML
- [ ] Migrate commands to YAML
- [ ] Add dependency declarations
- [ ] Add event subscriptions

**Deliverables:**
- All skills in `skills/`
- All commands in `commands/`
- Dependency graph

### Phase 6: Extensions (Week 10)

**Goal:** Project customization

- [ ] Implement extension loading
- [ ] Create override system
- [ ] Build extension templates
- [ ] Document extension creation

**Deliverables:**
- `templates/extension/`
- Extension loading in tools
- Extension documentation

### Phase 7: Documentation (Week 11)

**Goal:** Self-documenting system

- [ ] Build all doc generators
- [ ] Create doc templates
- [ ] Generate initial docs
- [ ] Add to CI pipeline

**Deliverables:**
- `tools/generate-docs.py`
- All `docs/*.md` (generated)
- CI integration

### Phase 8: Migration & Polish (Week 12)

**Goal:** V1 users can migrate

- [ ] Build migration tool
- [ ] Test migration on real projects
- [ ] Write migration guide
- [ ] Performance optimization

**Deliverables:**
- `tools/migrate.py`
- Migration documentation
- Performance benchmarks

---

## Success Metrics

### Technical Metrics

| Metric | Target |
|--------|--------|
| Schema coverage | 100% of components |
| Validation pass rate | 100% on CI |
| Doc generation | Automatic, no manual updates |
| Extension test coverage | 90%+ |
| Migration success rate | 95%+ |

### Developer Experience

| Metric | Target |
|--------|--------|
| Time to add new skill | <10 minutes |
| Time to create custom gate | <5 minutes |
| IDE autocomplete | Works for all YAML |
| Error messages | Actionable, with fix suggestions |
| Documentation freshness | Always current (generated) |

### Performance

| Metric | Target |
|--------|--------|
| Validation time (all) | <5 seconds |
| Doc generation | <10 seconds |
| State render | <100ms |
| Extension load | <500ms |

---

## Appendix: Key Differences from V1

| Aspect | V1 | V2 |
|--------|----|----|
| **Format** | Markdown with YAML frontmatter | YAML/JSON with Markdown content field |
| **Validation** | Convention-based | Schema-enforced |
| **Dependencies** | Implicit (mentioned in text) | Explicit (version constraints) |
| **Events** | Hooks (fixed points) | Pub/sub (flexible) |
| **State** | Markdown (parsed) | JSON (structured) + Markdown (rendered) |
| **Config** | Scattered | Hierarchical with precedence |
| **Extensions** | Fork and modify | First-class extension points |
| **Documentation** | Manual maintenance | Generated from schemas |
| **Phases** | One large file | Modular, independent files |
| **Gates** | Embedded in loop | Standalone, composable |

---

## Appendix: V1 Feature Parity Checklist

**V2 must do everything V1 does.** This section tracks complete feature parity.

### Commands (37 total)

All commands must be migrated to YAML format with proper schemas.

| Command | Category | V2 Status |
|---------|----------|-----------|
| `/cc-plan` | Planning | ⬜ Not started |
| `/cc-audit-blueprint` | Planning | ⬜ Not started |
| `/cc-spike` | Planning | ⬜ Not started |
| `/cc-daily` | Execution | ⬜ Not started |
| `/cc-loop` | Execution | ✅ Example created |
| `/cc-analyze` | Execution | ⬜ Not started |
| `/cc-review` | Quality | ⬜ Not started |
| `/cc-test` | Quality | ⬜ Not started |
| `/cc-secure` | Quality | ⬜ Not started |
| `/cc-assess` | Quality | ⬜ Not started |
| `/cc-fix` | Quality | ⬜ Not started |
| `/cc-refactor` | Quality | ⬜ Not started |
| `/cc-perf` | Quality | ⬜ Not started |
| `/cc-deps` | Quality | ⬜ Not started |
| `/cc-debt` | Quality | ⬜ Not started |
| `/cc-ui` | Frontend | ⬜ Not started |
| `/cc-terminal` | Frontend | ⬜ Not started |
| `/cc-seo` | Frontend | ⬜ Not started |
| `/cc-sync` | Frontend | ⬜ Not started |
| `/cc-commit` | Git | ⬜ Not started |
| `/cc-pr` | Git | ⬜ Not started |
| `/cc-revert` | Git | ⬜ Not started |
| `/cc-release` | Operations | ⬜ Not started |
| `/cc-postmortem` | Operations | ⬜ Not started |
| `/cc-migrate` | Operations | ⬜ Not started |
| `/cc-closeout` | Operations | ⬜ Not started |
| `/cc-changelog` | Documentation | ⬜ Not started |
| `/cc-adr` | Documentation | ⬜ Not started |
| `/cc-docs` | Documentation | ⬜ Not started |
| `/cc-onboard` | Documentation | ⬜ Not started |
| `/cc-standup` | Team | ⬜ Not started |
| `/cc-retro` | Team | ⬜ Not started |
| `/cc-scaffold` | Setup | ⬜ Not started |
| `/cc-scout-skills` | Setup | ⬜ Not started |
| `/cc-map-project` | Setup | ⬜ Not started |
| `/cc-gitignore` | Setup | ⬜ Not started |
| `/cc-claude-md` | Setup | ⬜ Not started |
| `/cc-prompt` | Setup | ⬜ Not started |

### Skills (68 total)

All skills must be migrated to YAML format with event subscriptions.

#### Orchestration (22 skills)
| Skill | V2 Status |
|-------|-----------|
| `task-orchestrator` | ⬜ Not started |
| `requirements-clarifier` | ⬜ Not started |
| `autonomous-loop` | ⬜ Not started |
| `meta-cognition` | ⬜ Not started |
| `multi-perspective` | ⬜ Not started |
| `queue-manager` | ⬜ Not started |
| `definition-of-done` | ⬜ Not started |
| `browser-verification` | ⬜ Not started |
| `visual-diff` | ⬜ Not started |
| `result-synthesizer` | ⬜ Not started |
| `parallel-task-decomposer` | ⬜ Not started |
| `decision-logger` | ⬜ Not started |
| `extended-thinking` | ⬜ Not started |
| `parallel-exploration` | ⬜ Not started |
| `subagent-research` | ⬜ Not started |
| `argument-parser` | ⬜ Not started |
| `smart-context-v3` | ⬜ Not started |
| `error-classifier` | ⬜ Not started |
| `parallel-agents` | ⬜ Not started |
| `swarm-mode` | ⬜ Not started |
| `task-dependencies` | ⬜ Not started |
| `plan-approval` | ⬜ Not started |
| `evaluator-optimizer` | ✅ Example created |

#### Quality (7 skills)
| Skill | V2 Status |
|-------|-----------|
| `definition-of-done` | ⬜ Not started |
| `self-critique` | ⬜ Not started |
| `severity-levels` | ⬜ Not started |
| `model-routing` | ⬜ Not started |
| `commit-style` | ⬜ Not started |
| `test-first` | ⬜ Not started |
| `no-guessing` | ⬜ Not started |

#### Workflow (6 skills)
| Skill | V2 Status |
|-------|-----------|
| `pre-commit` | ⬜ Not started |
| `pre-merge` | ⬜ Not started |
| `pre-release` | ⬜ Not started |
| `commit-checkpoint` | ⬜ Not started |
| `phase-workflow` | ⬜ Not started |
| `update-bundle-guide` | ⬜ Not started |

#### Optimization (12 skills)
| Skill | V2 Status |
|-------|-----------|
| `smart-context` | ⬜ Not started |
| `context-budget-monitor` | ⬜ Not started |
| `session-memory` | ⬜ Not started |
| `dry-run-mode` | ⬜ Not started |
| `error-recovery` | ⬜ Not started |
| `metrics-logger` | ⬜ Not started |
| `metrics-writer` | ⬜ Not started |
| `undo-history` | ⬜ Not started |
| `file-watcher` | ⬜ Not started |
| `dependency-checker` | ⬜ Not started |
| `auto-update-checker` | ⬜ Not started |
| `prompt-feedback` | ⬜ Not started |

#### Project Management (10 skills)
| Skill | V2 Status |
|-------|-----------|
| `project-init` | ⬜ Not started |
| `claude-md-manager` | ⬜ Not started |
| `skill-scout` | ⬜ Not started |
| `gitignore-manager` | ⬜ Not started |
| `health-dashboard` | ⬜ Not started |
| `dependency-tracker` | ⬜ Not started |
| `frontmatter-generator` | ⬜ Not started |
| `frontend-backend-sync` | ⬜ Not started |
| `project-templates` | ⬜ Not started |
| `brownfield-analyzer` | ⬜ Not started |

#### Automation (5 skills)
| Skill | V2 Status |
|-------|-----------|
| `changelog-automation` | ⬜ Not started |
| `docs-generator` | ⬜ Not started |
| `compound-commands` | ⬜ Not started |
| `snippet-library` | ⬜ Not started |
| `modern-tech-checker` | ⬜ Not started |

#### Collaboration (3 skills)
| Skill | V2 Status |
|-------|-----------|
| `cross-project-patterns` | ⬜ Not started |
| `team-sharing` | ⬜ Not started |
| `template-registry` | ⬜ Not started |

#### CI/CD (2 skills)
| Skill | V2 Status |
|-------|-----------|
| `ci-cd-integration` | ⬜ Not started |
| `prompt-testing` | ⬜ Not started |

#### Environment (1 skill)
| Skill | V2 Status |
|-------|-----------|
| `conda-aware` | ⬜ Not started |

### Agents (15 total)

| Agent | V2 Status |
|-------|-----------|
| `code-reviewer` | ⬜ Not started |
| `security-analyst` | ⬜ Not started |
| `test-engineer` | ⬜ Not started |
| `documentation-writer` | ⬜ Not started |
| `researcher` | ⬜ Not started |
| `ui-ux-expert` | ⬜ Not started |
| `terminal-ui-expert` | ⬜ Not started |
| `seo-expert` | ⬜ Not started |
| `database-expert` | ⬜ Not started |
| `devops-engineer` | ⬜ Not started |
| `accessibility-expert` | ⬜ Not started |
| `performance-optimizer` | ⬜ Not started |
| `api-designer` | ⬜ Not started |
| `migration-specialist` | ⬜ Not started |
| `prompt-engineer` | ⬜ Not started |

### Patterns (15+ total)

| Pattern | Category | V2 Status |
|---------|----------|-----------|
| `repository` | Architecture | ⬜ Not started |
| `service-layer` | Architecture | ⬜ Not started |
| `clean-architecture` | Architecture | ⬜ Not started |
| `retry-with-backoff` | Resilience | ⬜ Not started |
| `circuit-breaker` | Resilience | ⬜ Not started |
| `error-boundary` | Error Handling | ⬜ Not started |
| `result-type` | Error Handling | ⬜ Not started |
| `pagination` | API | ⬜ Not started |
| `rate-limiting` | API | ⬜ Not started |
| `strategy` | Behavioral | ⬜ Not started |
| `observer` | Behavioral | ⬜ Not started |
| `state-machine` | Behavioral | ⬜ Not started |
| `arrange-act-assert` | Testing | ⬜ Not started |
| `test-doubles` | Testing | ⬜ Not started |
| `feature-flag` | Operations | ⬜ Not started |
| `blue-green` | Operations | ⬜ Not started |

### Rules (13 total)

| Rule | V2 Status |
|------|-----------|
| `security` | ⬜ Not started |
| `testing` | ⬜ Not started |
| `git-workflow` | ⬜ Not started |
| `documentation` | ⬜ Not started |
| `code-quality` | ⬜ Not started |
| `api-design` | ⬜ Not started |
| `error-handling` | ⬜ Not started |
| `ui-ux-design` | ⬜ Not started |
| `terminal-ui` | ⬜ Not started |
| `performance` | ⬜ Not started |
| `database` | ⬜ Not started |
| `logging` | ⬜ Not started |
| `prompt-engineering` | ⬜ Not started |

### Snippets (9 total)

| Snippet | V2 Status |
|---------|-----------|
| `express-route` | ⬜ Not started |
| `fastapi-endpoint` | ⬜ Not started |
| `go-handler` | ⬜ Not started |
| `react-component` | ⬜ Not started |
| `react-hook` | ⬜ Not started |
| `jest-test` | ⬜ Not started |
| `pytest-test` | ⬜ Not started |
| `go-test` | ⬜ Not started |
| `dockerfile` | ⬜ Not started |

### Core Features

| Feature | V1 Status | V2 Status | Notes |
|---------|-----------|-----------|-------|
| 10-phase autonomous loop | ✅ Working | ⬜ 1/10 phases | Need all 10 phases |
| 15 quality gates | ✅ Working | ⬜ 1/15 gates | Need all 15 gates |
| Query classification | ✅ Working | ✅ In Phase 1 | Part of classify phase |
| Evaluator-optimizer | ✅ Working | ✅ Example skill | Need integration |
| Swarm orchestration | ✅ Working | ⬜ Not started | Event-based in v2 |
| Task dependencies | ✅ Working | ⬜ Not started | In state schema |
| Plan approval | ✅ Working | ⬜ Not started | Event-based in v2 |
| Context compaction | ✅ Working | ⬜ Not started | Proactive in v2 |
| Multi-registry discovery | ✅ Working | ⬜ Not started | |
| Plugin support | ✅ Working | ⬜ Not started | Extension system |

---

## Appendix: Full Migration Plan

### Phase 0: Preparation

Before migration begins:

1. **Complete PLANNING.md questionnaire**
   - Establish priorities
   - Identify pain points
   - Define success criteria

2. **Set up v2 tooling**
   - Validate schemas work
   - Test migration script on samples
   - Set up CI for v2

3. **Establish migration testing**
   - Create test cases for critical v1 behaviors
   - Define "feature parity" tests

### Phase 1: Foundation (Week 1-2)

Focus: Core infrastructure

- [ ] Finalize all JSON schemas
- [ ] Complete validation tooling
- [ ] Complete state rendering tooling
- [ ] Set up documentation generation
- [ ] Create extension loading system

### Phase 2: Core Loop (Week 3-4)

Focus: Orchestrator and phases

- [ ] Complete orchestrator
- [ ] Implement all 10 phases
- [ ] Wire event system
- [ ] Implement all 15 gates
- [ ] Test loop execution

### Phase 3: Migrate Commands (Week 5-6)

Focus: All 37 commands

- [ ] Run migration script
- [ ] Review and fix each command
- [ ] Add proper argument/flag definitions
- [ ] Test each command
- [ ] Generate command documentation

### Phase 4: Migrate Skills (Week 7-8)

Focus: All 68 skills

- [ ] Run migration script
- [ ] Add dependency declarations
- [ ] Add event subscriptions
- [ ] Test trigger matching
- [ ] Generate skill documentation

### Phase 5: Migrate Supporting Components (Week 9-10)

Focus: Agents, patterns, rules, snippets

- [ ] Migrate 15 agents
- [ ] Migrate 15+ patterns
- [ ] Migrate 13 rules
- [ ] Migrate 9 snippets
- [ ] Generate all documentation

### Phase 6: Advanced Features (Week 11)

Focus: V1 advanced features

- [ ] Swarm orchestration
- [ ] Task dependencies
- [ ] Plan approval
- [ ] Multi-registry discovery
- [ ] Plugin/extension support

### Phase 7: Testing & Polish (Week 12)

Focus: Quality assurance

- [ ] Full integration testing
- [ ] Performance benchmarking
- [ ] Documentation review
- [ ] Migration guide finalization
- [ ] Release preparation

### Migration Tooling

```bash
# Full migration command
python tools/migrate.py --from=v1 --input=../claude-conductor --output=./

# Dry run first
python tools/migrate.py --from=v1 --dry-run

# Validate after migration
python tools/validate.py

# Generate documentation
python tools/generate-docs.py

# Check dependencies
python tools/check-deps.py
```

### Rollback Plan

If migration issues arise:

1. V1 remains fully functional throughout
2. V2 can be abandoned without affecting v1
3. Partial migrations can be reverted per-component
4. Git history preserves all v1 state

---

## Conclusion

Claude Conductor 2.0 is designed to be:

1. **Maintainable** — Schema-first, validated, generated docs
2. **Extensible** — First-class extensions, event-driven
3. **Reliable** — Typed state, dependency resolution
4. **Performant** — Modular loading, efficient tooling
5. **Migratable** — Clear path from v1
6. **Complete** — Everything v1 does, but better

This is not just a refactor—it's a reimagining of the platform as a proper framework with the rigor that entails.

---

## Related Documents

| Document | Purpose |
|----------|---------|
| [PLANNING.md](PLANNING.md) | Priority questionnaire and decision log |
| [README.md](README.md) | Quick start guide |
| [schemas/](schemas/) | JSON Schema definitions |
| [tools/](tools/) | CLI tooling |
