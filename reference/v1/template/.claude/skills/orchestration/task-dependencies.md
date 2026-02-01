---
name: task-dependencies
description: Manage task dependencies with automatic unblocking when predecessors complete
version: 1.0.0
triggers:
  - "depends on"
  - "blocked by"
  - "blocks"
  - "after task"
  - "pipeline"
  - "sequence"
model: haiku
tags: [orchestration, dependencies, workflow, pipeline]
context: inherit
---

# Task Dependencies

Manage task dependencies with automatic pipeline unblocking. When a task completes, all tasks that were waiting on it automatically become available.

---

## Overview

Task dependencies enable:

- **Pipeline workflows** - Tasks execute in proper order
- **Automatic unblocking** - No manual intervention needed
- **Parallel optimization** - Independent tasks run simultaneously
- **Clear visibility** - See what's blocking what

---

## Dependency Syntax

### In Work Queue (LOOP_STATE.md)

```markdown
## Work Queue

### Tasks
| ID | Subject | Severity | Status | Blocked By | Blocks | Owner |
|----|---------|----------|--------|------------|--------|-------|
| T001 | Design schema | S1 | complete | — | T002, T003 | — |
| T002 | Implement service | S1 | in_progress | — | T004 | main |
| T003 | Create endpoints | S1 | pending | — | T004 | — |
| T004 | Integration tests | S2 | blocked | T002, T003 | — | — |
```

### Dependency Rules

1. **blocked** status = has unresolved `Blocked By` items
2. **pending** status = no blockers, ready to claim
3. When blocker completes → remove from `Blocked By` list
4. When `Blocked By` becomes empty → status changes to `pending`

---

## How Dependencies Work

### Adding Dependencies

When creating a task:

```
Add task: "Write integration tests"
  - Depends on: T002 (Implement service), T003 (Create endpoints)
  - Severity: S2

Result:
| T004 | Write integration tests | S2 | blocked | T002, T003 | — | — |
```

### Automatic Unblocking

```
BEFORE: T002 completes
─────────────────────────────────────
T002 | Implement service | complete | — | T004
T003 | Create endpoints | pending | — | T004
T004 | Integration tests | blocked | T002, T003 | —

AFTER: T002 completes
─────────────────────────────────────
T002 | Implement service | complete | — | T004
T003 | Create endpoints | pending | — | T004
T004 | Integration tests | blocked | T003 | —
          ↑ T002 removed from Blocked By

AFTER: T003 completes
─────────────────────────────────────
T002 | Implement service | complete | — | T004
T003 | Create endpoints | complete | — | T004
T004 | Integration tests | pending | — | —
          ↑ Blocked By empty → status becomes pending
```

---

## Dependency Patterns

### Pattern 1: Linear Pipeline

```
T001 → T002 → T003 → T004

| ID | Subject | Blocked By | Blocks |
|----|---------|------------|--------|
| T001 | Schema design | — | T002 |
| T002 | Service impl | T001 | T003 |
| T003 | API endpoints | T002 | T004 |
| T004 | Integration | T003 | — |
```

### Pattern 2: Fan-Out (Parallel after single)

```
        ┌→ T002
T001 ──┼→ T003
        └→ T004

| ID | Subject | Blocked By | Blocks |
|----|---------|------------|--------|
| T001 | Foundation | — | T002, T003, T004 |
| T002 | Module A | T001 | — |
| T003 | Module B | T001 | — |
| T004 | Module C | T001 | — |

When T001 completes: T002, T003, T004 all become pending (parallel!)
```

### Pattern 3: Fan-In (Single after parallel)

```
T001 ──┐
T002 ──┼→ T004
T003 ──┘

| ID | Subject | Blocked By | Blocks |
|----|---------|------------|--------|
| T001 | Research A | — | T004 |
| T002 | Research B | — | T004 |
| T003 | Research C | — | T004 |
| T004 | Synthesize | T001, T002, T003 | — |

T004 waits until ALL of T001, T002, T003 complete
```

### Pattern 4: Diamond

```
        ┌→ T002 ─┐
T001 ──┤        ├→ T004
        └→ T003 ─┘

| ID | Subject | Blocked By | Blocks |
|----|---------|------------|--------|
| T001 | Init | — | T002, T003 |
| T002 | Path A | T001 | T004 |
| T003 | Path B | T001 | T004 |
| T004 | Merge | T002, T003 | — |
```

---

## Integration with Queue Manager

### Enhanced Task Creation

```
"Add task: Implement auth service"
"  - Severity: S1"
"  - Depends on: T001 (schema design)"
"  - Blocks: T003 (endpoints), T004 (tests)"

Queue Manager creates:
| T002 | Implement auth service | S1 | blocked | T001 | T003, T004 | — |
```

### Enhanced Task Completion

```
"Complete T001"

Queue Manager:
1. Marks T001 as complete
2. Finds all tasks where T001 is in Blocked By
3. Removes T001 from their Blocked By lists
4. For each task with now-empty Blocked By: status → pending
5. Updates LOOP_STATE.md
```

### Dependency-Aware Prioritization

When selecting next task:

```
SELECTION ORDER:
1. Tasks with status = pending (unblocked)
2. Within pending: Order by severity (S0 → S1 → S2 → S3)
3. Within severity: Order by "blocks count" (tasks that unblock most others first)
4. Skip tasks with status = blocked

Example:
| ID | Severity | Status | Blocks Count |
|----|----------|--------|--------------|
| T005 | S1 | pending | 3 | ← First (unblocks most)
| T006 | S1 | pending | 1 | ← Second
| T007 | S2 | pending | 0 | ← Third
| T008 | S1 | blocked | 2 | ← Skip (blocked)
```

---

## Visualization

### Dependency Graph (Text)

```
"Show dependency graph"

Output:
┌──────────────────────────────────────────┐
│           TASK DEPENDENCY GRAPH           │
├──────────────────────────────────────────┤
│                                          │
│  [T001] Schema ✓                         │
│      │                                   │
│      ├──▶ [T002] Service ●               │
│      │        │                          │
│      │        └──▶ [T004] Tests ○        │
│      │                 ▲                 │
│      └──▶ [T003] API ○─┘                 │
│                                          │
│  Legend: ✓ complete  ● in_progress       │
│          ○ pending   ◌ blocked           │
│                                          │
└──────────────────────────────────────────┘
```

### Critical Path

```
"Show critical path"

Output:
Critical Path (longest dependency chain):
T001 → T002 → T004

Total tasks: 4
On critical path: 3
Parallelizable: T003 (can run with T002)

Estimated time if sequential: 4 units
Estimated time with parallelism: 3 units
Savings: 25%
```

---

## Commands

### Add Dependency

```
"T004 depends on T002 and T003"
"Add blocker T001 to T002"
"T002 blocks T003"
```

### Remove Dependency

```
"Remove dependency T001 from T002"
"T002 no longer blocks T003"
```

### Check Dependencies

```
"What's blocking T004?"
→ "T004 is blocked by: T002 (in_progress), T003 (pending)"

"What does T001 unblock?"
→ "When T001 completes, it will unblock: T002, T003"
```

### Visualize

```
"Show dependency graph"
"Show critical path"
"What can run in parallel?"
```

---

## Error Handling

### Circular Dependency Detection

```
Attempted: T001 → T002 → T003 → T001

ERROR: Circular dependency detected!
  T001 → T002 → T003 → T001 (cycle)

Resolution: Remove one dependency to break the cycle.
```

### Self-Dependency

```
Attempted: T001 depends on T001

ERROR: Task cannot depend on itself.
```

### Missing Task Reference

```
Attempted: T005 depends on T099

ERROR: Task T099 does not exist.
Available tasks: T001, T002, T003, T004, T005
```

---

## Integration with Autonomous Loop

### PLAN Phase Enhancement

```
PLAN PHASE:
├── Load work queue
├── **PARSE DEPENDENCIES** ← New
│   ├── Build dependency graph
│   ├── Identify blocked vs pending
│   ├── Calculate critical path
│   └── Identify parallel opportunities
├── Select next task (dependency-aware)
└── Proceed to BUILD
```

### On Task Completion

```
After completing task T001:
├── Mark T001 as complete
├── **UNBLOCK DEPENDENTS** ← New
│   ├── Find tasks blocked by T001
│   ├── Remove T001 from their Blocked By
│   └── Update status if now unblocked
├── Check if new tasks became parallel-eligible
└── Update LOOP_STATE.md
```

---

## Configuration

### In .claude/settings.json

```json
{
  "orchestration": {
    "dependencies": {
      "enabled": true,
      "detectCircular": true,
      "visualizeOnChange": false,
      "prioritizeUnblockers": true
    }
  }
}
```

---

## Example: Full Pipeline

### Initial Setup

```
User: "Build authentication feature"

Task decomposition with dependencies:

T001: Design auth schema
      └─ Blocks: T002, T003

T002: Implement auth service
      ├─ Blocked By: T001
      └─ Blocks: T004, T005

T003: Create auth middleware
      ├─ Blocked By: T001
      └─ Blocks: T004

T004: Build auth endpoints
      ├─ Blocked By: T002, T003
      └─ Blocks: T005

T005: Write integration tests
      └─ Blocked By: T002, T004
```

### LOOP_STATE.md

```markdown
## Work Queue

### Tasks
| ID | Subject | Sev | Status | Blocked By | Blocks | Owner |
|----|---------|-----|--------|------------|--------|-------|
| T001 | Design auth schema | S1 | pending | — | T002, T003 | — |
| T002 | Implement auth service | S1 | blocked | T001 | T004, T005 | — |
| T003 | Create auth middleware | S1 | blocked | T001 | T004 | — |
| T004 | Build auth endpoints | S1 | blocked | T002, T003 | T005 | — |
| T005 | Write integration tests | S2 | blocked | T002, T004 | — | — |

### Dependency Graph
```
T001 ──┬──▶ T002 ──┬──▶ T004 ──▶ T005
       │          │      ▲        ▲
       └──▶ T003 ─┘──────┘        │
                  └───────────────┘
```

### Execution Order
1. T001 (only unblocked)
2. T002, T003 (parallel after T001)
3. T004 (after T002 AND T003)
4. T005 (after T002 AND T004)
```

### Execution Flow

```
Iteration 1: Execute T001 (only pending task)
            T001 completes → T002, T003 unblock

Iteration 2: Execute T002 AND T003 in parallel
            T002 completes → removes from T004, T005 Blocked By
            T003 completes → removes from T004 Blocked By
            T004 unblocks (both T002, T003 done)

Iteration 3: Execute T004
            T004 completes → removes from T005 Blocked By
            T005 unblocks

Iteration 4: Execute T005
            T005 completes → Pipeline complete!
```

---

## Best Practices

### Do

- Define dependencies when creating tasks
- Keep dependency chains short (< 5 deep)
- Look for parallel opportunities (fan-out patterns)
- Verify no circular dependencies

### Don't

- Create long linear chains when parallelism is possible
- Add unnecessary dependencies
- Forget to update dependencies when requirements change
- Block low-priority tasks on high-priority (usually wrong direction)

---

## Summary

Task dependencies transform work queue from a flat list to an intelligent pipeline:

| Without Dependencies | With Dependencies |
|---------------------|-------------------|
| Severity-only ordering | Dependency + severity |
| Manual sequencing | Automatic unblocking |
| No visibility into blockers | Clear blocker tracking |
| All tasks compete | Blocked tasks wait |
| Random parallel execution | Optimized parallel execution |

Dependencies are the foundation for swarm mode and efficient multi-agent coordination.
