# Phase 3: Plan

> **Purpose:** Decompose work into actionable items with dependencies
> **Duration:** 2-5 minutes
> **Triggers:** After understand phase

---

## Overview

The plan phase breaks down the work into discrete tasks, establishes dependencies, and creates a work queue. For complex tasks, it may spawn a planning subagent.

---

## Process

### 1. Decompose into Work Items

```
FOR each identified piece of work:
  CREATE task:
    id: "T001"
    title: "Brief description"
    type: implement | fix | refactor | test | docs
    priority: S0 | S1 | S2 | S3
    status: pending
    blockedBy: [task_ids]
    blocks: [task_ids]
```

### 2. Establish Dependencies

```
ANALYZE task relationships:
  - Which tasks must complete before others?
  - Which tasks can run in parallel?
  - What's the critical path?

BUILD dependency graph:
  T001 (Create user model)
    └── T002 (Add auth service)
        └── T003 (Add login route)
            └── T004 (Add tests)
```

### 3. Prioritize

```
PRIORITY LEVELS:
  S0 - Critical: Blocks everything, security issue
  S1 - High: Core functionality, blocking others
  S2 - Medium: Important but not blocking
  S3 - Low: Nice to have, can defer

SORT work queue by:
  1. Priority (S0 first)
  2. Dependency order (unblocked first)
  3. Complexity (simpler first when equal)
```

### 4. Identify Checkpoints

```
CHECKPOINT after:
  - Each S0/S1 task completion
  - Every 3 S2 tasks
  - Before risky changes
  - At logical boundaries

CHECKPOINT = verified commit for rollback
```

### 5. Plan Approval (Complex Tasks)

```
IF complexity == "complex" OR security_sensitive:
  DISPLAY plan summary to user
  ASK: "Proceed with this plan?"

  OPTIONS:
    - Proceed
    - Modify (ask for changes)
    - Cancel
```

---

## Work Queue Format

```yaml
work_queue:
  - id: "T001"
    title: "Create User model with password hashing"
    type: implement
    priority: S1
    status: pending
    blockedBy: []
    blocks: ["T002", "T003"]
    estimated: moderate
    checkpoint: true

  - id: "T002"
    title: "Create AuthService with JWT tokens"
    type: implement
    priority: S1
    status: pending
    blockedBy: ["T001"]
    blocks: ["T003"]
    estimated: moderate
    checkpoint: true
```

---

## Outputs

| Output | Description |
|--------|-------------|
| `work_queue` | Ordered list of tasks |
| `dependency_graph` | Task relationships |
| `checkpoints` | Where to create commits |
| `estimated_iterations` | Expected loop count |

---

## Skip Conditions

```
SKIP IF:
  - Work queue already exists and valid
  - Resuming from checkpoint

CANNOT SKIP IF:
  - New request
  - Previous plan completed
```

---

## Example Output

```
[PLAN] Decomposing "Add user authentication"

Work Queue (5 items):

  #  | Task                           | Pri | Blocks | Status
  ---|--------------------------------|-----|--------|--------
  T1 | Create User model              | S1  | T2, T3 | pending
  T2 | Create AuthService             | S1  | T3     | pending
  T3 | Add login/register routes      | S1  | T4     | pending
  T4 | Add auth middleware            | S1  | T5     | pending
  T5 | Write tests for auth           | S2  | —      | pending

Checkpoints: After T1, T3, T5
Estimated iterations: 3-4

Proceed? [Y/n]
```
