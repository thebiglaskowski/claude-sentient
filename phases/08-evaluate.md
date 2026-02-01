# Phase 8: Evaluate

> **Purpose:** Determine if work is complete or needs more iterations
> **Duration:** ~30 seconds
> **Triggers:** After commit phase

---

## Overview

The evaluate phase assesses whether we're done or need another loop iteration. It checks completion criteria and decides the next action.

---

## Process

### 1. Check Work Queue

```
SCAN work_queue:
  pending_s0 = count(status == "pending" AND priority == "S0")
  pending_s1 = count(status == "pending" AND priority == "S1")
  pending_s2 = count(status == "pending" AND priority == "S2")
  pending_s3 = count(status == "pending" AND priority == "S3")
  blocked = count(status == "blocked")
```

### 2. Check Completion Criteria

```
COMPLETE IF:
  ✓ All S0 tasks complete
  ✓ All S1 tasks complete
  ✓ All S2 tasks complete (or deferred by user)
  ✓ Quality gates passed (current iteration)
  ✓ No blocked tasks
  ✓ Git state clean

CONTINUE IF:
  - Pending tasks remain
  - Blocked tasks can be unblocked
  - Quality gates need retry
```

### 3. Handle Blocked Tasks

```
FOR task IN blocked_tasks:
  IF blocker resolved:
    SET task.status = "pending"

  IF blocker unresolvable:
    ASK user: "Task X is blocked by Y. How to proceed?"
    OPTIONS:
      - Skip task (defer to S3)
      - Provide guidance
      - Cancel loop
```

### 4. Decide Next Action

```
IF complete:
  PROCEED to completion

ELIF has_pending_work:
  LOOP back to execute phase

ELIF all_blocked:
  ASK user for guidance

ELIF max_iterations_reached:
  WARN user, ask to continue or stop
```

### 5. Update Metrics

```
RECORD:
  iterations_total: +1
  tasks_completed: count
  time_elapsed: duration
  gates_passed: count
```

---

## Completion States

| State | Meaning | Action |
|-------|---------|--------|
| **COMPLETE** | All work done, gates pass | Exit loop, report success |
| **CONTINUE** | More work to do | Loop to phase 4 (execute) |
| **BLOCKED** | Cannot proceed | Ask user |
| **FAILED** | Unrecoverable error | Exit with error |
| **TIMEOUT** | Max iterations reached | Ask user |

---

## Exit Report

When complete:

```
# Loop Complete

## Summary
- Tasks completed: 5/5
- Iterations: 3
- Duration: 12 minutes
- Final coverage: 87%

## Changes Made
- Created user authentication system
- Added login/register endpoints
- Implemented JWT tokens
- Added comprehensive tests

## Checkpoints Created
- CP-001: User model
- CP-002: Auth service
- CP-003: Routes and tests

## What's Next
- Consider adding password reset
- Consider adding OAuth providers
- Review security recommendations
```

---

## Outputs

| Output | Description |
|--------|-------------|
| `evaluation_result` | COMPLETE, CONTINUE, BLOCKED, etc. |
| `pending_count` | Remaining tasks |
| `next_action` | What happens next |
| `metrics` | Loop statistics |

---

## Loop Limits

```
MAX_ITERATIONS: 50 (configurable)
MAX_RETRIES_PER_TASK: 3
MAX_GATE_RETRIES: 3

IF limit reached:
  WARN user
  ASK: Continue, stop, or adjust limits?
```

---

## Recovery Actions

```
IF evaluation fails:
  1. Check for corrupted state
  2. Attempt state repair
  3. If unrepairable, offer rollback to checkpoint
  4. Ask user for guidance
```

---

## Example (Continue)

```
[EVALUATE] Checking completion status...

Work Queue:
  ✓ T001: Create User model         [complete]
  ✓ T002: Create AuthService        [complete]
  → T003: Add login routes          [pending]
  → T004: Add auth middleware       [pending]
  → T005: Write tests              [pending]

Completion: 2/5 tasks (40%)

Decision: CONTINUE
Next: Execute phase (T003)
```

---

## Example (Complete)

```
[EVALUATE] Checking completion status...

Work Queue:
  ✓ T001: Create User model         [complete]
  ✓ T002: Create AuthService        [complete]
  ✓ T003: Add login routes          [complete]
  ✓ T004: Add auth middleware       [complete]
  ✓ T005: Write tests              [complete]

Quality Gates: 8/8 passed
Completion: 5/5 tasks (100%)

Decision: COMPLETE

Generating final report...
```
