# Claude Conductor V2 — Master Gameplan

> **The Comprehensive Integration Plan**
> *How everything works together to create the Autonomous Meta-Cognitive Development Engine*

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [System Overview](#system-overview)
3. [The Learning Core](#the-learning-core)
4. [Complete Architecture](#complete-architecture)
5. [Component Inventory](#component-inventory)
6. [The Autonomous Loop (Detailed)](#the-autonomous-loop-detailed)
7. [Self-Improvement Engine](#self-improvement-engine)
8. [Integration Points](#integration-points)
9. [Gap Analysis](#gap-analysis)
10. [Implementation Phases](#implementation-phases)
11. [Success Criteria](#success-criteria)
12. [Risk Mitigation](#risk-mitigation)

---

## Executive Summary

Claude Conductor V2 is not just a collection of prompts—it's a **self-improving autonomous development engine**. The key differentiator from V1 is the **learning core**: every action feeds back into improving the system.

### The Three Pillars

```
┌─────────────────────────────────────────────────────────────────┐
│                     CLAUDE CONDUCTOR V2                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│   │   AUTONOMY      │  │  INTELLIGENCE   │  │   LEARNING      │ │
│   │                 │  │                 │  │                 │ │
│   │ • Self-driving  │  │ • Meta-cognition│  │ • Self-improve  │ │
│   │ • Minimal input │  │ • Tool selection│  │ • Pattern detect│ │
│   │ • Auto-recover  │  │ • Context aware │  │ • Rule generate │ │
│   │ • Decision make │  │ • Multi-agent   │  │ • Feedback loop │ │
│   └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│            │                    │                    │           │
│            └────────────────────┼────────────────────┘           │
│                                 │                                │
│                    ┌────────────▼────────────┐                   │
│                    │    UNIFIED ENGINE       │                   │
│                    │  "Drop in → Walk away   │                   │
│                    │   → Come back to done"  │                   │
│                    └─────────────────────────┘                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### What We Have

| Document | Purpose | Status |
|----------|---------|--------|
| `VISION.md` | North star philosophy | ✅ Complete |
| `V1_FEATURE_INVENTORY.md` | All V1 features (884 lines) | ✅ Complete |
| `BORIS_CHERNY.md` | Tips from Claude Code creator | ✅ Complete |
| `BORIS_INTEGRATION.md` | Integration plan for tips | ✅ Complete |
| `BLUEPRINT.md` | Technical architecture | ✅ Complete |
| `PLANNING.md` | Priority questionnaire | ✅ Complete |
| Schemas | 7 JSON schemas | ✅ Complete |
| Tools | validate, migrate, render | ✅ Complete |
| **GAMEPLAN.md** | This document | 🔄 Creating |

---

## System Overview

### The Complete Picture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        CLAUDE CONDUCTOR V2 - COMPLETE SYSTEM                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  INPUT LAYER                                                                 │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  User Request  │  Existing Codebase  │  Bug Report  │  CI Failure    │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                    │                                         │
│                                    ▼                                         │
│  PERCEPTION LAYER                                                            │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  Query         │  Brownfield      │  Context        │  Environment   │   │
│  │  Classifier    │  Analyzer        │  Loader         │  Detector      │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                    │                                         │
│                                    ▼                                         │
│  INTELLIGENCE LAYER                                                          │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                         META-COGNITION                                │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐     │   │
│  │  │ Capability │  │   Tool     │  │  Strategy  │  │   Stuck    │     │   │
│  │  │ Inventory  │  │ Selection  │  │  Chooser   │  │ Detection  │     │   │
│  │  └────────────┘  └────────────┘  └────────────┘  └────────────┘     │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                    │                                         │
│                                    ▼                                         │
│  EXECUTION LAYER                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                      10-PHASE AUTONOMOUS LOOP                         │   │
│  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐    │   │
│  │  │ 1.CL │→│ 2.CX │→│ 3.AS │→│ 4.PL │→│ 5.EX │→│ 6.VE │→│ 7.QA │    │   │
│  │  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘ └──────┘ └──────┘    │   │
│  │       ┌──────┐ ┌──────┐ ┌──────┐                                     │   │
│  │    →  │ 8.CK │→│ 9.EV │→│10.RC │ → (loop or exit)                   │   │
│  │       └──────┘ └──────┘ └──────┘                                     │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                    │                                         │
│                                    ▼                                         │
│  QUALITY LAYER                                                               │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  15 QUALITY GATES (ALL BLOCKING)                                      │   │
│  │  ┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐           │   │
│  │  │LINT ││TYPE ││UNIT ││INTG ││SECR ││PERF ││BRWS ││A11Y │           │   │
│  │  └─────┘└─────┘└─────┘└─────┘└─────┘└─────┘└─────┘└─────┘           │   │
│  │  ┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐                  │   │
│  │  │DOCS ││MODR ││WQUE ││ISSU ││GIT  ││DOD  ││APPR │                  │   │
│  │  └─────┘└─────┘└─────┘└─────┘└─────┘└─────┘└─────┘                  │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                    │                                         │
│                                    ▼                                         │
│  LEARNING LAYER  ◀──────────────────────────────────────────────────────┐   │
│  ┌──────────────────────────────────────────────────────────────────────┐│  │
│  │                    SELF-IMPROVEMENT ENGINE                           ││  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐    ││  │
│  │  │  Success   │  │  Failure   │  │   Rule     │  │  Prompt    │    ││  │
│  │  │  Patterns  │  │  Analysis  │  │ Generator  │  │ Optimizer  │    ││  │
│  │  └────────────┘  └────────────┘  └────────────┘  └────────────┘    ││  │
│  │         │              │              │              │              ││  │
│  │         └──────────────┴──────────────┴──────────────┘              ││  │
│  │                              │                                       ││  │
│  │                    ┌─────────▼─────────┐                            ││  │
│  │                    │  KNOWLEDGE BASE   │────────────────────────────┘│  │
│  │                    │  (Persistent)     │                              │  │
│  │                    └───────────────────┘                              │  │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                    │                                         │
│                                    ▼                                         │
│  OUTPUT LAYER                                                                │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  Working Code  │  Tests  │  Docs  │  PR  │  Deployment  │  Report    │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## The Learning Core

**This is the heart of V2.** Everything feeds into learning.

### The Feedback Loop

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE LEARNING CORE                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Every Action                                                    │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    CAPTURE                               │    │
│  │  • What was attempted?                                   │    │
│  │  • What was the context?                                 │    │
│  │  • What tools were used?                                 │    │
│  │  • What was the outcome?                                 │    │
│  └─────────────────────────────────────────────────────────┘    │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    ANALYZE                               │    │
│  │  • Did it succeed or fail?                               │    │
│  │  • Why did it succeed/fail?                              │    │
│  │  • Is this a pattern we've seen before?                  │    │
│  │  • What could have been done better?                     │    │
│  └─────────────────────────────────────────────────────────┘    │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    LEARN                                 │    │
│  │  • Generate rule if new mistake                          │    │
│  │  • Reinforce if success pattern                          │    │
│  │  • Update probability weights                            │    │
│  │  • Prune ineffective rules                               │    │
│  └─────────────────────────────────────────────────────────┘    │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    APPLY                                 │    │
│  │  • Update CLAUDE.md with new rules                       │    │
│  │  • Adjust tool selection weights                         │    │
│  │  • Modify prompting strategies                           │    │
│  │  • Inform future decisions                               │    │
│  └─────────────────────────────────────────────────────────┘    │
│       │                                                          │
│       └──────────────────────────────────────────────────────┐  │
│                                                              │  │
│  Next Action ◀───────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### What Gets Learned

| Category | Examples | Storage |
|----------|----------|---------|
| **Mistake Patterns** | "Don't hardcode secrets" | `rules/auto-generated/` |
| **Success Patterns** | "This prompting style works" | `feedback/successes/` |
| **Tool Effectiveness** | "Use subagents for parallel work" | `metrics/tool-usage.jsonl` |
| **Project Knowledge** | "This codebase uses X pattern" | `.claude/knowledge/` |
| **User Preferences** | "User prefers verbose output" | `.claude/preferences.json` |
| **Recovery Strategies** | "When X fails, try Y" | `strategies/recovery/` |

### Rule Generation System

```yaml
# Auto-generated rule example
name: no-hardcoded-secrets
version: 1.0.0
auto_generated: true
generated_at: "2024-01-15T10:30:00Z"
trigger_event: "user_correction"

context:
  mistake: "Committed API key to repository"
  correction: "Use environment variables"
  frequency: 3  # Happened 3 times

rule: |
  NEVER include API keys, tokens, passwords, or secrets in code.
  Always use environment variables or secret management.
  Check: grep -r "sk-" "api_key" "password=" before commit.

effectiveness:
  opportunities: 12
  prevented: 12
  rate: 1.0
  confidence: high

actions:
  - Add to pre-commit checks
  - Warn when pattern detected
  - Block commit if found
```

---

## Complete Architecture

### Event-Driven Core

Everything communicates through events:

```yaml
# Event flow example
events:
  # User makes request
  - request.received:
      payload: { request: "Add user authentication", project: "/app" }

  # Classification
  - classify.complete:
      payload: { type: "feature", complexity: "high", agents: 3 }

  # Context loaded
  - context.loaded:
      payload: { files: 47, patterns: ["service-layer"], rules: ["security"] }

  # Planning
  - plan.created:
      payload: { tasks: 8, dependencies: 3, estimated_phases: 4 }

  # Approval (if needed)
  - plan.approval.requested:
      payload: { reason: "security_sensitive", reviewer: "staff-engineer" }

  - plan.approved:
      payload: { reviewer: "staff-engineer", conditions: [] }

  # Execution
  - task.started:
      payload: { id: "T001", title: "Create user model" }

  - task.completed:
      payload: { id: "T001", duration: "2m", files_changed: 3 }

  # Quality
  - gate.passed:
      payload: { gate: "unit-tests", coverage: 0.94 }

  - gate.failed:
      payload: { gate: "security", issues: 2, severity: "medium" }

  # Learning
  - learning.pattern.detected:
      payload: { pattern: "success", action: "used-subagent", outcome: "faster" }

  - learning.rule.generated:
      payload: { rule: "prefer-subagents-for-parallel", confidence: 0.85 }
```

### Component Communication

```
┌─────────────────────────────────────────────────────────────────┐
│                        EVENT BUS                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Publishers                              Subscribers             │
│  ──────────                              ───────────             │
│                                                                  │
│  Orchestrator ─────┐                 ┌───── Skills               │
│  Phases ───────────┼────── EVENTS ───┼───── Commands            │
│  Gates ────────────┤    (typed,      ├───── Agents              │
│  User Actions ─────┤     async,      ├───── Learning Engine     │
│  External ─────────┘     logged)     └───── State Store         │
│                                                                  │
│  Event Types:                                                    │
│  • lifecycle.* (session, phase, iteration)                      │
│  • quality.* (gate pass/fail, metrics)                          │
│  • work.* (task start/complete, queue changes)                  │
│  • context.* (budget, compaction, loading)                      │
│  • learning.* (patterns, rules, feedback)                       │
│  • agent.* (spawn, complete, synthesize)                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### State Management

```json
{
  "$schema": "state.schema.json",
  "version": "2.0",
  "sessionId": "abc-123",
  "startedAt": "2024-01-15T10:00:00Z",

  "classification": {
    "type": "feature",
    "complexity": "high",
    "subagentCount": 3,
    "orchestrationMode": "swarm"
  },

  "phase": {
    "current": 5,
    "name": "execute",
    "iteration": 2,
    "progress": 0.65
  },

  "workQueue": [
    {
      "id": "T001",
      "title": "Create user model",
      "status": "complete",
      "blockedBy": [],
      "blocks": ["T002", "T003"]
    },
    {
      "id": "T002",
      "title": "Add authentication endpoints",
      "status": "in-progress",
      "blockedBy": [],
      "blocks": ["T004"]
    }
  ],

  "gates": {
    "lint": { "status": "passed", "value": 0 },
    "type-check": { "status": "passed", "value": 0 },
    "unit-tests": { "status": "pending" },
    "security": { "status": "pending" }
  },

  "context": {
    "budgetUsed": 0.45,
    "level": "green",
    "compactionReady": false,
    "loadedRules": ["security", "testing"],
    "loadedPatterns": ["service-layer", "repository"]
  },

  "learning": {
    "sessionsToday": 3,
    "rulesGenerated": 1,
    "patternsDetected": 5,
    "effectivenessScore": 0.87
  },

  "decisions": [
    {
      "timestamp": "2024-01-15T10:05:00Z",
      "decision": "Use JWT for authentication",
      "rationale": "Stateless, scalable, industry standard",
      "alternatives": ["Sessions", "OAuth only"],
      "approved": true
    }
  ],

  "metrics": {
    "iterationsTotal": 5,
    "gatesPassed": 8,
    "gatesFailed": 2,
    "tasksCompleted": 4,
    "recoveries": 1
  }
}
```

---

## Component Inventory

### Complete V2 Component List

#### Skills (Target: 75+)

| Category | V1 Count | V2 Count | New in V2 |
|----------|----------|----------|-----------|
| Orchestration | 22 | 28 | +6 (learning skills) |
| Quality | 7 | 10 | +3 (auto-improvement) |
| Workflow | 6 | 8 | +2 (Boris patterns) |
| Automation | 5 | 7 | +2 (analytics) |
| Optimization | 12 | 15 | +3 (smarter context) |
| Project Management | 10 | 12 | +2 (skill wizard) |
| CI/CD | 2 | 4 | +2 (broader coverage) |
| Collaboration | 3 | 4 | +1 (worktree) |
| Environment | 1 | 3 | +2 (terminal setup) |
| **Learning** (NEW) | 0 | 8 | +8 (core V2 feature) |
| **Total** | **68** | **99** | **+31** |

#### New Learning Skills

```yaml
learning-skills:
  - self-rule-generator      # Generate rules from corrections
  - pattern-detector         # Identify recurring patterns
  - effectiveness-tracker    # Track rule/strategy effectiveness
  - knowledge-builder        # Build project knowledge base
  - feedback-collector       # Capture success/failure feedback
  - prompt-optimizer         # Improve prompts based on outcomes
  - strategy-evolver         # Evolve recovery/approach strategies
  - preference-learner       # Learn user preferences
```

#### Commands (Target: 45+)

| Category | V1 Count | V2 Count | New in V2 |
|----------|----------|----------|-----------|
| Planning | 3 | 4 | +1 (staff review) |
| Execution | 3 | 5 | +2 (worktree, analytics) |
| Quality | 9 | 10 | +1 (auto-fix) |
| Frontend | 4 | 4 | — |
| Git | 3 | 4 | +1 (worktree sync) |
| Operations | 4 | 4 | — |
| Documentation | 4 | 5 | +1 (presentation) |
| Team | 2 | 2 | — |
| Setup | 6 | 8 | +2 (skill wizard, env) |
| **Learning** (NEW) | 0 | 4 | +4 |
| **Total** | **37** | **50** | **+13** |

#### New Commands

```yaml
new-commands:
  # Learning commands
  - /cc-learn          # Show what's been learned this session
  - /cc-rules          # Manage auto-generated rules
  - /cc-patterns       # View detected patterns
  - /cc-improve        # Trigger self-improvement cycle

  # Boris-inspired
  - /cc-staff-review   # Adversarial plan review
  - /cc-worktree       # Git worktree management
  - /cc-analytics      # Database/metrics queries
  - /cc-fix-zero       # Zero-config "just fix it"
  - /cc-skill-wizard   # Create skills from patterns
  - /cc-present        # Generate code presentations
  - /cc-env-setup      # Terminal/environment optimization
```

#### Agents (Target: 20+)

| Agent | V1 | V2 | Notes |
|-------|----|----|-------|
| code-reviewer | ✅ | ✅ | Enhanced |
| security-analyst | ✅ | ✅ | Enhanced |
| test-engineer | ✅ | ✅ | Enhanced |
| documentation-writer | ✅ | ✅ | Enhanced |
| researcher | ✅ | ✅ | Enhanced |
| ui-ux-expert | ✅ | ✅ | Enhanced |
| terminal-ui-expert | ✅ | ✅ | Enhanced |
| seo-expert | ✅ | ✅ | Enhanced |
| database-expert | ✅ | ✅ | Enhanced |
| devops-engineer | ✅ | ✅ | Enhanced |
| accessibility-expert | ✅ | ✅ | Enhanced |
| performance-optimizer | ✅ | ✅ | Enhanced |
| api-designer | ✅ | ✅ | Enhanced |
| migration-specialist | ✅ | ✅ | Enhanced |
| prompt-engineer | ✅ | ✅ | Enhanced |
| **staff-engineer** | — | ✅ | NEW: Adversarial reviewer |
| **learning-analyst** | — | ✅ | NEW: Pattern detection |
| **data-analyst** | — | ✅ | NEW: Database/metrics |
| **brownfield-expert** | — | ✅ | NEW: Codebase analysis |
| **permission-guardian** | — | ✅ | NEW: Opus gateway |

#### Quality Gates (Target: 18)

| Gate | V1 | V2 | Notes |
|------|----|----|-------|
| PRE-FLIGHT | ✅ | ✅ | Enhanced |
| LINT | ✅ | ✅ | Enhanced |
| TYPE | ✅ | ✅ | Enhanced |
| UNIT | ✅ | ✅ | Enhanced |
| INTEGRATION | ✅ | ✅ | Enhanced |
| SECURITY | ✅ | ✅ | Enhanced |
| PERFORMANCE | ✅ | ✅ | Enhanced |
| BROWSER | ✅ | ✅ | Enhanced |
| A11Y | ✅ | ✅ | Enhanced |
| DOCS | ✅ | ✅ | Enhanced |
| MODERN | ✅ | ✅ | Enhanced |
| WORK_QUEUE | ✅ | ✅ | Enhanced |
| KNOWN_ISSUES | ✅ | ✅ | Enhanced |
| GIT_STATE | ✅ | ✅ | Enhanced |
| DOD | ✅ | ✅ | Enhanced |
| **LEARNING** | — | ✅ | NEW: Did we learn? |
| **APPROVAL** | — | ✅ | NEW: Staff review passed? |
| **SELF-REVIEW** | — | ✅ | NEW: Self-critique passed? |

---

## The Autonomous Loop (Detailed)

### Phase-by-Phase Breakdown

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      V2 AUTONOMOUS LOOP - 10 PHASES                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  PHASE 1: CLASSIFY                                                   │    │
│  │  ─────────────────                                                   │    │
│  │  • Parse incoming request                                            │    │
│  │  • Classify type (feature, bug, refactor, research, maintenance)     │    │
│  │  • Determine complexity (simple, moderate, complex, epic)            │    │
│  │  • Calculate resource needs (agents, context budget, model)          │    │
│  │  • Emit: classify.complete                                           │    │
│  │                                                                       │    │
│  │  Inputs: User request, codebase state                                │    │
│  │  Outputs: Classification object                                      │    │
│  │  Duration: <30 seconds                                               │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                      │                                       │
│                                      ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  PHASE 2: CONTEXTUALIZE                                              │    │
│  │  ──────────────────────                                              │    │
│  │  • Analyze codebase (brownfield) or requirements (greenfield)        │    │
│  │  • Load relevant rules based on task type                            │    │
│  │  • Load relevant patterns based on detected architecture             │    │
│  │  • Load project knowledge from previous sessions                     │    │
│  │  • Load auto-generated rules from learning system                    │    │
│  │  • Emit: context.loaded                                              │    │
│  │                                                                       │    │
│  │  Inputs: Classification, codebase                                    │    │
│  │  Outputs: Loaded context (rules, patterns, knowledge)                │    │
│  │  Duration: 1-3 minutes                                               │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                      │                                       │
│                                      ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  PHASE 2.5: META-COGNITION                                           │    │
│  │  ─────────────────────────                                           │    │
│  │  • Review capability inventory (all tools, skills, agents)           │    │
│  │  • Select optimal tools for this task                                │    │
│  │  • Determine if subagents needed (and which)                         │    │
│  │  • Assess confidence level                                           │    │
│  │  • Check for stuck patterns (have we tried this before?)             │    │
│  │  • Emit: metacognition.complete                                      │    │
│  │                                                                       │    │
│  │  Inputs: Classification, context, capability inventory               │    │
│  │  Outputs: Tool selection, agent roster, confidence score             │    │
│  │  Duration: <1 minute                                                 │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                      │                                       │
│                                      ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  PHASE 3: ASSESS                                                     │    │
│  │  ─────────────                                                       │    │
│  │  • Understand current state (what exists?)                           │    │
│  │  • Identify gaps (what's missing?)                                   │    │
│  │  • Find dependencies (what needs to happen first?)                   │    │
│  │  • Detect risks (what could go wrong?)                               │    │
│  │  • Emit: assessment.complete                                         │    │
│  │                                                                       │    │
│  │  Inputs: Context, codebase, requirements                             │    │
│  │  Outputs: Gap analysis, risk assessment, dependency map              │    │
│  │  Duration: 1-5 minutes                                               │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                      │                                       │
│                                      ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  PHASE 4: PLAN                                                       │    │
│  │  ───────────                                                         │    │
│  │  • Decompose into work items                                         │    │
│  │  • Prioritize (S0 > S1 > S2 > S3)                                    │    │
│  │  • Identify parallelizable tasks                                     │    │
│  │  • Create dependency graph (blockedBy/blocks)                        │    │
│  │  • Generate checkpoints for rollback                                 │    │
│  │  • [V2] Spawn staff-engineer for adversarial review                  │    │
│  │  • Emit: plan.created (or plan.approval.requested)                   │    │
│  │                                                                       │    │
│  │  Inputs: Assessment, classification, meta-cognition output           │    │
│  │  Outputs: Work queue, dependency graph, checkpoints                  │    │
│  │  Duration: 2-10 minutes (includes review if needed)                  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                      │                                       │
│                                      ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  PHASE 5: EXECUTE                                                    │    │
│  │  ──────────────                                                      │    │
│  │  • Claim next available task from queue                              │    │
│  │  • Apply relevant patterns and snippets                              │    │
│  │  • Implement changes                                                 │    │
│  │  • Run incremental tests                                             │    │
│  │  • [V2] Spawn parallel workers if swarm mode                         │    │
│  │  • [V2] Capture learning data (what worked, what didn't)             │    │
│  │  • Emit: task.complete (per task)                                    │    │
│  │                                                                       │    │
│  │  Inputs: Work queue, patterns, snippets, rules                       │    │
│  │  Outputs: Code changes, test results, learning data                  │    │
│  │  Duration: Variable (bulk of time spent here)                        │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                      │                                       │
│                                      ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  PHASE 6: VERIFY                                                     │    │
│  │  ─────────────                                                       │    │
│  │  • Run full test suite                                               │    │
│  │  • Browser verification (if UI changes)                              │    │
│  │  • Visual diff (if applicable)                                       │    │
│  │  • Accessibility check                                               │    │
│  │  • Emit: verification.complete                                       │    │
│  │                                                                       │    │
│  │  Inputs: Code changes, test suite                                    │    │
│  │  Outputs: Test results, verification status                          │    │
│  │  Duration: 1-5 minutes                                               │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                      │                                       │
│                                      ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  PHASE 7: QUALITY                                                    │    │
│  │  ──────────────                                                      │    │
│  │  • Execute all 18 quality gates                                      │    │
│  │  • No exceptions — all must pass                                     │    │
│  │  • [V2] If gate fails, trigger evaluator-optimizer                   │    │
│  │  • [V2] Track gate pass/fail for learning                            │    │
│  │  • Emit: gate.passed or gate.failed (per gate)                       │    │
│  │                                                                       │    │
│  │  Inputs: Code changes, test results                                  │    │
│  │  Outputs: Gate status, issues found, learning data                   │    │
│  │  Duration: 2-10 minutes                                              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                      │                                       │
│                                      ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  PHASE 8: CHECKPOINT                                                 │    │
│  │  ─────────────────                                                   │    │
│  │  • Create verified commit                                            │    │
│  │  • Tag with checkpoint ID                                            │    │
│  │  • Record in CHECKPOINTS.md                                          │    │
│  │  • Enable easy rollback                                              │    │
│  │  • Emit: checkpoint.created                                          │    │
│  │                                                                       │    │
│  │  Inputs: Passed gates, code changes                                  │    │
│  │  Outputs: Git commit, checkpoint record                              │    │
│  │  Duration: <1 minute                                                 │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                      │                                       │
│                                      ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  PHASE 9: EVALUATE                                                   │    │
│  │  ──────────────                                                      │    │
│  │  • Is work queue empty?                                              │    │
│  │  • Is Definition of Done met?                                        │    │
│  │  • Are there unresolved S0/S1 issues?                                │    │
│  │  • [V2] Self-critique: "Is this actually good?"                      │    │
│  │  • [V2] Trigger learning capture                                     │    │
│  │  • Decision: Continue loop or exit?                                  │    │
│  │  • Emit: evaluation.complete                                         │    │
│  │                                                                       │    │
│  │  Inputs: Work queue, gate status, DoD criteria                       │    │
│  │  Outputs: Continue/exit decision, remaining work                     │    │
│  │  Duration: <1 minute                                                 │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                      │                                       │
│                        ┌─────────────┴─────────────┐                        │
│                        │                           │                        │
│                        ▼                           ▼                        │
│                   CONTINUE                       EXIT                       │
│                   (Phase 10)                  (Complete)                    │
│                        │                           │                        │
│                        ▼                           ▼                        │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  PHASE 10: RECOVER (if needed)                                       │    │
│  │  ─────────────────────────────                                       │    │
│  │  • Classify the error/blockage                                       │    │
│  │  • Consult recovery strategies                                       │    │
│  │  • [V2] Check learning: "Have we solved this before?"                │    │
│  │  • [V2] Generate new strategy if novel problem                       │    │
│  │  • Apply recovery and return to appropriate phase                    │    │
│  │  • Emit: recovery.applied                                            │    │
│  │                                                                       │    │
│  │  Inputs: Error state, recovery strategies, learning history          │    │
│  │  Outputs: Recovery action, updated state                             │    │
│  │  Duration: Variable                                                  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                      │                                       │
│                                      ▼                                       │
│                          Return to Phase 3, 4, or 5                         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Exit Criteria

```yaml
exit_criteria:
  required:
    - all_gates_passed: true
    - consecutive_passes: 2
    - work_queue_empty: true
    - dod_complete: true
    - no_s0_s1_issues: true
    - git_state_clean: true

  v2_additions:
    - self_critique_passed: true     # "Is this actually good?"
    - learning_captured: true        # Did we capture learnings?
    - staff_review_passed: true      # If risky, was it reviewed?
```

---

## Self-Improvement Engine

### How V2 Gets Smarter

```
┌─────────────────────────────────────────────────────────────────┐
│                   SELF-IMPROVEMENT ENGINE                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                     INPUT SOURCES                         │   │
│  │                                                           │   │
│  │  • User corrections ("No, do it this way")               │   │
│  │  • Gate failures (security, tests, lint)                 │   │
│  │  • Recovery events (what went wrong)                     │   │
│  │  • Successful completions (what worked)                  │   │
│  │  • Time metrics (what was fast/slow)                     │   │
│  │  • User preferences (explicit and inferred)              │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│                              ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    PATTERN DETECTION                      │   │
│  │                                                           │   │
│  │  Detect recurring patterns:                               │   │
│  │  • Same mistake made 3+ times → Generate rule             │   │
│  │  • Same recovery works 3+ times → Promote strategy        │   │
│  │  • Same tool selection succeeds → Reinforce weight        │   │
│  │  • Same approach fails → Demote / warn                    │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│                              ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    RULE GENERATION                        │   │
│  │                                                           │   │
│  │  Auto-generate rules:                                     │   │
│  │  1. Identify mistake pattern                              │   │
│  │  2. Generate prevention rule                              │   │
│  │  3. Add to CLAUDE.md (auto-generated section)             │   │
│  │  4. Track effectiveness over time                         │   │
│  │  5. Prune rules below 50% effectiveness                   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│                              ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                  PROMPT OPTIMIZATION                      │   │
│  │                                                           │   │
│  │  Improve prompts based on outcomes:                       │   │
│  │  • A/B test different phrasings                           │   │
│  │  • Track success rates per prompt variant                 │   │
│  │  • Evolve toward higher-performing prompts                │   │
│  │  • Boris: "elegant-redo" pattern for mediocre outputs     │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│                              ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                  STRATEGY EVOLUTION                       │   │
│  │                                                           │   │
│  │  Evolve recovery and approach strategies:                 │   │
│  │  • Track which strategies work for which error types      │   │
│  │  • Generate new strategies from successful ad-hoc fixes   │   │
│  │  • Deprecate strategies that consistently fail            │   │
│  │  • Share strategies across projects (if enabled)          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│                              ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                   KNOWLEDGE BASE                          │   │
│  │                                                           │   │
│  │  Persist and share learnings:                             │   │
│  │  • Project-specific knowledge (.claude/knowledge/)        │   │
│  │  • Cross-project patterns (if enabled)                    │   │
│  │  • User preference profiles                               │   │
│  │  • Supermemory integration for persistence                │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Learning Metrics

```yaml
learning_metrics:
  session:
    - patterns_detected: int
    - rules_generated: int
    - rules_triggered: int
    - rules_effective: float  # % that prevented repeat mistakes
    - recoveries_successful: int
    - recoveries_failed: int

  project:
    - total_rules: int
    - rule_effectiveness_avg: float
    - knowledge_entries: int
    - improvement_score: float  # Overall improvement trend

  cross_project:
    - shared_patterns: int
    - shared_rules: int
    - adoption_rate: float
```

---

## Integration Points

### How Components Connect

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         INTEGRATION MAP                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  USER                                                                        │
│    │                                                                         │
│    ▼                                                                         │
│  ┌──────────────┐                                                           │
│  │   REQUEST    │                                                           │
│  └──────────────┘                                                           │
│         │                                                                    │
│         │  "/cc-loop add user auth"                                         │
│         │                                                                    │
│         ▼                                                                    │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐                │
│  │   COMMAND    │────▶│    SKILL     │────▶│    AGENT     │                │
│  │  /cc-loop    │     │ query-class  │     │ staff-engr   │                │
│  └──────────────┘     └──────────────┘     └──────────────┘                │
│         │                    │                    │                         │
│         │                    │                    │                         │
│         ▼                    ▼                    ▼                         │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                           EVENT BUS                                   │  │
│  │  request.received → classify.complete → plan.created → ...           │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│         │                    │                    │                         │
│         ▼                    ▼                    ▼                         │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐                │
│  │   PATTERN    │     │    RULE      │     │    GATE      │                │
│  │ service-layer│     │  security    │     │  unit-tests  │                │
│  └──────────────┘     └──────────────┘     └──────────────┘                │
│         │                    │                    │                         │
│         │                    │                    │                         │
│         ▼                    ▼                    ▼                         │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                          STATE STORE                                  │  │
│  │  { phase: 5, tasks: [...], gates: {...}, learning: {...} }           │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│         │                                                                   │
│         ▼                                                                   │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                        LEARNING ENGINE                                │  │
│  │  Capture → Analyze → Learn → Apply                                   │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│         │                                                                   │
│         ▼                                                                   │
│  ┌──────────────┐                                                          │
│  │   OUTPUT     │                                                          │
│  │  Code, Tests │                                                          │
│  │  Docs, PR    │                                                          │
│  └──────────────┘                                                          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Key Integration Rules

1. **Everything emits events** — No silent actions
2. **Learning captures everything** — Every action feeds learning
3. **State is single source of truth** — All components read/write state
4. **Components are loosely coupled** — Communicate via events only
5. **Extensions integrate seamlessly** — Same interfaces as core

---

## Gap Analysis

### What's Missing for V2 Vision

| Gap | Impact | Priority | Solution |
|-----|--------|----------|----------|
| **Learning persistence** | Learning lost between sessions | P0 | Supermemory integration + local knowledge base |
| **Automatic rule generation** | Manual rule creation | P0 | self-rule-generator skill |
| **Staff engineer review** | No adversarial review | P0 | staff-engineer agent + review skill |
| **Zero-config fix** | Requires context specification | P0 | Context auto-detection skill |
| **Opus permission gateway** | Manual permission handling | P0 | permission-guardian agent |
| **Worktree orchestration** | No native parallel support | P1 | worktree-orchestrator skill |
| **Database analytics** | No data analysis capability | P1 | data-analyst agent + skills |
| **Skill wizard** | Manual skill creation | P1 | repetition-detector + skill-wizard |
| **Prompting patterns** | Ad-hoc prompting | P1 | Prompting patterns library |
| **Learning mode** | No explanatory output | P2 | Output style configuration |
| **Presentation generator** | Manual documentation | P2 | presentation-generator skill |
| **Environment setup** | Manual terminal config | P2 | env-setup skill |

### New Components Needed

```yaml
new_components:
  skills:
    # P0 - Critical
    - self-rule-generator       # Generate rules from corrections
    - zero-config-fixer         # "Just fix" with auto-detection
    - adversarial-reviewer      # Staff engineer review trigger
    - permission-guardian       # Opus permission gateway
    - learning-persister        # Save learnings across sessions

    # P1 - High Value
    - worktree-orchestrator     # Parallel worktree management
    - repetition-detector       # Detect repeated patterns
    - skill-scaffolder          # Generate skills from patterns
    - database-connector        # Universal DB interface
    - prompting-optimizer       # Apply prompting patterns

    # P2 - Nice to Have
    - presentation-generator    # Code explanation slides
    - environment-optimizer     # Terminal/shell setup
    - learning-mode-handler     # Explanatory output

  agents:
    - staff-engineer            # Adversarial plan reviewer
    - learning-analyst          # Pattern detection specialist
    - data-analyst              # Database/metrics specialist
    - brownfield-expert         # Codebase analysis specialist
    - permission-guardian       # Opus-level permission evaluator

  gates:
    - learning-gate             # Did we capture learnings?
    - approval-gate             # Staff review passed?
    - self-review-gate          # Self-critique passed?

  events:
    - learning.*                # Learning system events
    - approval.*                # Approval workflow events
    - worktree.*                # Worktree management events
```

---

## Implementation Phases

### Phase 0: Foundation (Week 1-2)

**Goal:** Core infrastructure that everything builds on.

```yaml
tasks:
  - Finalize all JSON schemas
  - Implement schema validator (Python CLI)
  - Create event bus specification
  - Define state schema and defaults
  - Set up test infrastructure
  - Create project template

deliverables:
  - schemas/*.schema.json (complete)
  - tools/validate.py (complete)
  - events/*.events.yaml (complete)
  - state/*.schema.json (complete)
  - tests/conftest.py (complete)
  - templates/project/ (complete)

success_criteria:
  - All schemas validate correctly
  - Test suite runs
  - Template initializes
```

### Phase 1: Core Loop (Week 3-4)

**Goal:** Basic autonomous loop working.

```yaml
tasks:
  - Implement 10 modular phases
  - Implement core orchestrator
  - Implement basic event emission
  - Implement state management
  - Migrate essential V1 skills (top 20)

deliverables:
  - phases/01-10.md (complete)
  - core/orchestrator.md (complete)
  - skills/orchestration/* (20 skills)
  - Working /cc-loop command

success_criteria:
  - Loop completes simple tasks
  - Events emit correctly
  - State updates properly
```

### Phase 2: Quality Gates (Week 5-6)

**Goal:** All 18 gates working.

```yaml
tasks:
  - Implement 15 V1 gates
  - Implement 3 new V2 gates (learning, approval, self-review)
  - Implement gate runner skill
  - Implement evaluator-optimizer integration

deliverables:
  - gates/code/*.gate.json (11 gates)
  - gates/work/*.gate.json (4 gates)
  - gates/v2/*.gate.json (3 gates)
  - skills/quality/gate-runner.skill.yaml

success_criteria:
  - All gates execute
  - Failures trigger evaluator-optimizer
  - Learning data captured
```

### Phase 3: Learning Engine (Week 7-8)

**Goal:** Self-improvement working.

```yaml
tasks:
  - Implement pattern detector
  - Implement rule generator
  - Implement effectiveness tracker
  - Implement knowledge base
  - Implement Supermemory integration

deliverables:
  - skills/learning/* (8 skills)
  - agents/learning-analyst.agent.yaml
  - .claude/knowledge/ structure
  - Supermemory hooks

success_criteria:
  - Rules generate from corrections
  - Effectiveness tracked
  - Knowledge persists across sessions
```

### Phase 4: Advanced Features (Week 9-10)

**Goal:** Boris integrations and advanced capabilities.

```yaml
tasks:
  - Implement staff-engineer agent
  - Implement adversarial review pattern
  - Implement zero-config fixer
  - Implement Opus permission gateway
  - Implement worktree orchestrator

deliverables:
  - agents/staff-engineer.agent.yaml
  - agents/permission-guardian.agent.yaml
  - skills/orchestration/adversarial-reviewer.skill.yaml
  - skills/orchestration/zero-config-fixer.skill.yaml
  - skills/orchestration/worktree-orchestrator.skill.yaml

success_criteria:
  - Plans get adversarial review
  - "Just fix" works without context
  - Safe operations auto-approve
  - Parallel worktrees function
```

### Phase 5: Full Migration (Week 11-12)

**Goal:** Complete V1 parity plus V2 enhancements.

```yaml
tasks:
  - Migrate remaining 48 skills
  - Migrate all 37 commands
  - Migrate all 15 agents
  - Migrate all patterns, snippets, rules
  - Implement skill wizard
  - Implement database analytics

deliverables:
  - All 99 skills complete
  - All 50 commands complete
  - All 20 agents complete
  - All patterns, snippets, rules
  - /cc-skill-wizard command
  - /cc-analytics command

success_criteria:
  - V1 feature parity achieved
  - V2 enhancements functional
  - All tests pass
```

### Phase 6: Polish & Documentation (Week 13-14)

**Goal:** Production-ready with full documentation.

```yaml
tasks:
  - Generate all documentation from schemas
  - Create migration guide
  - Implement learning mode
  - Implement presentation generator
  - Performance optimization
  - Edge case handling

deliverables:
  - docs/*.md (all generated)
  - MIGRATION_GUIDE.md
  - /cc-present command
  - Learning mode toggle
  - Performance benchmarks

success_criteria:
  - Docs 100% generated
  - Migration path clear
  - Performance acceptable
  - Ready for release
```

---

## Success Criteria

### Quantitative Metrics

| Metric | V1 Baseline | V2 Target |
|--------|-------------|-----------|
| Autonomy Rate | ~70% | >90% |
| Questions per Task | ~5 | <3 |
| Gate Pass Rate (first try) | ~60% | >80% |
| Self-Recovery Rate | ~50% | >80% |
| Learning Effectiveness | 0% | >70% |
| User Satisfaction | N/A | "It just works" |

### Qualitative Criteria

- [ ] Drop into any codebase and understand it
- [ ] Complete E2E development with minimal input
- [ ] Learn from mistakes and not repeat them
- [ ] Know when to ask and when to decide
- [ ] Get better over time within a project
- [ ] Feel like a "development partner"

### The Ultimate Test

**Greenfield Test:**
```
Input: "Build me a SaaS for X"
Expected: 2-4 hours later, deployed app with tests, docs, CI/CD
Actual: ___
```

**Brownfield Test:**
```
Input: "Fix the performance issues" (dropped into unknown codebase)
Expected: Identifies issues, fixes safely, documents changes
Actual: ___
```

**Learning Test:**
```
Input: Correct the same mistake 3 times
Expected: Rule generated, mistake never happens again
Actual: ___
```

---

## Risk Mitigation

### Identified Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Learning produces bad rules | High | Medium | Effectiveness tracking, auto-pruning |
| Autonomy causes damage | High | Low | Opus permission gateway, checkpoints |
| Complexity overwhelms | Medium | Medium | Modular phases, clear interfaces |
| V1 migration breaks things | Medium | Medium | Comprehensive tests, gradual migration |
| Performance degrades | Medium | Low | Event-driven, lazy loading |

### Guardrails

```yaml
guardrails:
  autonomy:
    - Never delete without confirmation
    - Always create checkpoints before risky changes
    - Escalate security-sensitive operations
    - Pause if stuck for >3 iterations

  learning:
    - Require 3 occurrences before rule generation
    - Track effectiveness, prune below 50%
    - Never learn from unverified corrections
    - Separate project vs global learning

  quality:
    - All 18 gates must pass (no exceptions)
    - 2 consecutive passes required for exit
    - Self-critique before marking complete
    - Staff review for complex/risky changes
```

---

## Summary

### V2 is V1 + Learning + Autonomy

```
V2 = V1 Features (all 68 skills, 37 commands, etc.)
   + Learning Engine (pattern detection, rule generation, knowledge base)
   + Enhanced Autonomy (zero-config, self-recovery, minimal questions)
   + Boris Integrations (staff review, worktrees, prompting patterns)
   + Quality Upgrades (18 gates, self-critique, approval workflow)
```

### The Key Differentiators

1. **It learns** — Every action feeds back into improvement
2. **It knows itself** — Meta-cognition drives tool selection
3. **It requires less** — Minimal input, maximum output
4. **It gets better** — Improves over time within each project
5. **It's a partner** — Not a tool you use, a partner that builds with you

### Next Steps

1. Review this gameplan
2. Fill out PLANNING.md priorities (optional)
3. Begin Phase 0: Foundation
4. Iterate based on learnings (practicing what we preach)

---

*This is the master plan. Every implementation decision should trace back to this document.*
