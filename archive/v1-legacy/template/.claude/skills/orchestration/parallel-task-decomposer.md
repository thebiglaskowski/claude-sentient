---
name: parallel-task-decomposer
description: Breaks tasks into independent units for parallel agent execution
version: 1.0.0
triggers:
  - "break this down"
  - "parallelize"
  - "work on multiple things"
  - "speed this up"
  - "decompose task"
model: sonnet
tags: [orchestration, parallelization, efficiency]
---

# Parallel Task Decomposer

Analyzes tasks and breaks them into smaller independent units that can be executed by parallel agents simultaneously.

## Why This Matters

> "Break down tasks into smaller independent units and assign agents to work on them simultaneously."

Serial execution wastes time when tasks are independent. Proper decomposition can reduce total execution time by 3-5x.

---

## Task Decomposition Framework

### Step 1: Identify Task Boundaries

For any complex task, identify natural boundaries:

```
TASK BOUNDARY ANALYSIS:
├── By Module/Component
│   └── Each module can be worked on independently
├── By Layer
│   └── Frontend, backend, database can parallelize
├── By Feature
│   └── Independent features don't block each other
├── By Type
│   └── Testing, docs, implementation can parallelize
└── By File
    └── Different files can be edited simultaneously
```

### Step 2: Check Independence

Two tasks are independent if:

| Criterion | Independent | Dependent |
|-----------|-------------|-----------|
| Shared files | No overlap | Same files |
| Data flow | No dependencies | Output feeds input |
| Order matters | Can swap order | Must be sequential |
| Shared state | No shared state | Modifies same state |

### Step 3: Assign to Agents

| Task Type | Best Agent | Model |
|-----------|------------|-------|
| Code review | code-reviewer | sonnet |
| Security check | security-analyst | opus |
| Test writing | test-engineer | sonnet |
| Documentation | documentation-writer | sonnet |
| Research | researcher | sonnet |
| UI audit | ui-ux-expert | sonnet |
| Performance | performance-optimizer | sonnet |

---

## Decomposition Patterns

### Pattern 1: Module-Based Parallelization

```
Task: "Review the entire codebase"

Decomposition:
├── Agent 1: Review src/auth/ module
├── Agent 2: Review src/api/ module
├── Agent 3: Review src/database/ module
├── Agent 4: Review src/utils/ module
└── Agent 5: Review src/ui/ module

Synthesis: Merge all findings by severity
```

### Pattern 2: Concern-Based Parallelization

```
Task: "Audit the application"

Decomposition:
├── Agent 1 (security-analyst): Security audit
├── Agent 2 (code-reviewer): Code quality audit
├── Agent 3 (test-engineer): Test coverage audit
├── Agent 4 (performance-optimizer): Performance audit
└── Agent 5 (accessibility-expert): Accessibility audit

Synthesis: Unified audit report with all concerns
```

### Pattern 3: Layer-Based Parallelization

```
Task: "Add user profile feature"

Decomposition:
├── Agent 1: Database schema + migrations
├── Agent 2: API endpoints (waits for schema)
├── Agent 3: UI components (can start with mocks)
└── Agent 4: Tests (waits for implementation)

Dependencies: Schema → API → Integration
             UI can start in parallel with mocks
```

### Pattern 4: Test-Implementation Parallelization

```
Task: "Implement and test payment flow"

Decomposition:
├── Agent 1: Write test specifications first
├── Agent 2: Implement payment logic
├── Agent 3: Implement error handling
└── Merge: Connect tests to implementation

TDD approach with parallel spec writing
```

### Pattern 5: Documentation Parallelization

```
Task: "Document the API"

Decomposition:
├── Agent 1: Document auth endpoints
├── Agent 2: Document user endpoints
├── Agent 3: Document payment endpoints
├── Agent 4: Document admin endpoints
└── Agent 5: Generate OpenAPI spec

Synthesis: Merge into unified API documentation
```

---

## Decomposition Decision Tree

```
START: Complex task received
│
├── Can it be split by module/component?
│   └── YES → Module-based parallelization
│
├── Can it be split by concern (security, quality, etc.)?
│   └── YES → Concern-based parallelization
│
├── Can it be split by layer (frontend, backend, db)?
│   └── YES → Layer-based parallelization
│
├── Can tests be written in parallel with implementation?
│   └── YES → Test-implementation parallelization
│
├── Is it documentation that covers multiple areas?
│   └── YES → Documentation parallelization
│
└── None of the above?
    └── Execute sequentially, but look for micro-parallelization
```

---

## Work Queue Format

When decomposing, create structured work queue entries:

```markdown
## Parallel Work Units

### Unit 1: Auth Module Review
- **Agent:** code-reviewer
- **Scope:** src/auth/**
- **Dependencies:** None
- **Output:** Findings report
- **Can parallelize:** Yes

### Unit 2: API Module Review
- **Agent:** code-reviewer
- **Scope:** src/api/**
- **Dependencies:** None
- **Output:** Findings report
- **Can parallelize:** Yes

### Unit 3: Security Audit
- **Agent:** security-analyst
- **Scope:** Full codebase
- **Dependencies:** None
- **Output:** Security findings
- **Can parallelize:** Yes

### Synthesis Task
- **Agent:** Main orchestrator
- **Dependencies:** Units 1, 2, 3
- **Action:** Merge findings, prioritize by severity
```

---

## Integration with Autonomous Loop

### Enhanced PLAN Phase

```
PLAN PHASE (Enhanced):
├── Assess work queue
├── **DECOMPOSITION ANALYSIS** ← NEW
│   ├── Identify task boundaries
│   ├── Check independence criteria
│   ├── Group parallelizable tasks
│   └── Create parallel work units
├── Prioritize by dependencies
├── Assign agents to parallel units
└── Begin parallel execution
```

### Parallel Execution Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    PARALLEL EXECUTION                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  DECOMPOSE → SPAWN → EXECUTE → SYNTHESIZE → VERIFY              │
│      │          │        │          │          │                │
│      ▼          ▼        ▼          ▼          ▼                │
│  Identify   Launch    Agents     Merge      Check               │
│  parallel   agents    work in    results    quality             │
│  units      async     parallel   together   gates               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Spawning Parallel Agents

### Command Format

```
Spawn in parallel:
1. "Spawn code-reviewer agent to review src/auth/ module"
2. "Spawn code-reviewer agent to review src/api/ module"
3. "Spawn security-analyst agent to audit authentication"

All three agents work simultaneously.
```

### Background Execution

For truly parallel execution, use background mode:

```
Spawn agents in background:
├── code-reviewer (module 1) → runs in background
├── code-reviewer (module 2) → runs in background
├── security-analyst → runs in background
└── Continue with other work while waiting
```

---

## Synthesis Strategies

### Strategy 1: Severity-Based Merge

```
Collect findings from all agents
├── Group by severity (S0, S1, S2, S3)
├── Deduplicate overlapping findings
├── Create unified work queue
└── Address S0/S1 first
```

### Strategy 2: Category-Based Merge

```
Collect findings from all agents
├── Group by category (Security, Quality, Performance)
├── Identify cross-cutting concerns
├── Create categorized report
└── Address by category priority
```

### Strategy 3: Action-Based Merge

```
Collect findings from all agents
├── Extract actionable items
├── Group by action type (fix, refactor, document)
├── Estimate effort for each
└── Prioritize by impact/effort ratio
```

---

## Example: Full Decomposition

### Input Task
```
"Prepare the authentication module for production"
```

### Decomposition Output

```
TASK DECOMPOSITION ANALYSIS
═══════════════════════════

Original Task: Prepare authentication module for production

Identified Parallel Units:
─────────────────────────

UNIT 1: Security Audit
├── Agent: security-analyst (opus)
├── Scope: src/auth/**, src/middleware/auth.ts
├── Focus: OWASP, token handling, session management
├── Dependencies: None
├── Background: Yes
└── Expected output: Security findings with severity

UNIT 2: Code Quality Review
├── Agent: code-reviewer (sonnet)
├── Scope: src/auth/**
├── Focus: Code quality, patterns, maintainability
├── Dependencies: None
├── Background: Yes
└── Expected output: Quality findings

UNIT 3: Test Coverage Analysis
├── Agent: test-engineer (sonnet)
├── Scope: src/auth/**, tests/auth/**
├── Focus: Coverage gaps, edge cases, error paths
├── Dependencies: None
├── Background: Yes
└── Expected output: Test recommendations

UNIT 4: Performance Review
├── Agent: performance-optimizer (sonnet)
├── Scope: src/auth/**
├── Focus: Token validation speed, caching, DB queries
├── Dependencies: None
├── Background: Yes
└── Expected output: Performance recommendations

UNIT 5: Documentation Check
├── Agent: documentation-writer (sonnet)
├── Scope: src/auth/**, docs/auth.md
├── Focus: API docs, security notes, setup guide
├── Dependencies: None
├── Background: Yes
└── Expected output: Documentation gaps

SYNTHESIS:
├── Merge all findings by severity
├── Create unified remediation plan
├── Prioritize S0/S1 issues
└── Execute fixes sequentially (they may touch same files)

ESTIMATED TIME SAVINGS:
├── Sequential execution: ~25 minutes
├── Parallel execution: ~8 minutes
└── Savings: ~68%
```

---

## Usage

### Automatic Integration
The autonomous loop should invoke decomposition:
- At PLAN phase for complex tasks
- When work queue has multiple independent items
- When task scope spans multiple modules

### Manual Invocation
```
"Decompose this task for parallel execution"
"How can I parallelize this work?"
"Break this down into independent units"
```

---

## Key Principle

> **Independent tasks should never wait in line. Parallel agents = faster completion.**

If tasks don't share files or state, they should run simultaneously.
