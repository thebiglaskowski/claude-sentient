# Phase 4: Execute

> **Purpose:** Implement the changes for current work items
> **Duration:** Variable (bulk of work happens here)
> **Triggers:** After plan phase or loop iteration

---

## Overview

The execute phase does the actual work — writing code, making changes, creating files. It processes work items from the queue, respecting dependencies and running incremental tests.

---

## Process

### 1. Claim Next Task

```
FROM work_queue:
  FIND first task WHERE:
    - status == "pending"
    - blockedBy all have status == "complete"

  IF no task available:
    PROCEED to verify phase

  SET task.status = "in_progress"
```

### 2. Load Task Context

```
FOR current task:
  - Load relevant files
  - Load applicable patterns
  - Load applicable rules
  - Check for related memory
```

### 3. Implement Changes

```
BASED ON task.type:

  implement:
    - Create new code following patterns
    - Add necessary imports
    - Update related files

  fix:
    - Locate the issue
    - Apply minimal fix
    - Verify fix addresses root cause

  refactor:
    - Preserve behavior
    - Apply pattern
    - Update all references

  test:
    - Write tests for new/changed code
    - Aim for coverage threshold

  docs:
    - Update relevant documentation
    - Add docstrings/comments
```

### 4. Run Incremental Checks

```
AFTER each significant change:
  RUN quick checks:
    - Lint (should pass)
    - Type check (should pass)
    - Related tests (should pass)

  IF check fails:
    FIX immediately before continuing
```

### 5. Mark Complete

```
WHEN task implementation done:
  SET task.status = "complete"
  UPDATE work_queue

  IF task.checkpoint:
    SKIP to commit phase first
    THEN return to execute
```

---

## Execution Rules

### Code Quality
- Follow project conventions (from profile)
- Apply relevant patterns
- Keep changes focused (single responsibility)
- Don't over-engineer

### Testing
- Write tests for new functionality
- Update tests for changed behavior
- Run tests before marking complete

### Safety
- Don't delete without explicit instruction
- Create checkpoint before risky changes
- Ask if unsure about breaking changes

---

## Subagent Usage

```
SPAWN subagent WHEN:
  - Task requires specialist knowledge
  - Parallel execution would help
  - Context would benefit from isolation

SUBAGENT TYPES:
  - security-analyst: For auth, crypto, input validation
  - test-engineer: For test writing
  - code-reviewer: For review during refactor
```

---

## Outputs

| Output | Description |
|--------|-------------|
| `files_changed` | List of modified files |
| `tests_added` | New tests created |
| `tasks_completed` | Count of completed tasks |
| `incremental_results` | Quick check results |

---

## Error Handling

```
IF implementation error:
  1. Identify error type
  2. Attempt auto-fix (up to 3 times)
  3. If still failing, mark task blocked
  4. Add error details to task
  5. Continue with next task

IF stuck on task:
  - Try alternative approach
  - Spawn specialist agent
  - Ask user for guidance
```

---

## Example

```
[EXECUTE] Starting task T001: Create User model

Loading context:
  - Pattern: python-model
  - Rule: security (password hashing)
  - Related: existing models in src/models/

Implementing:
  + Created src/models/user.py
  + Added password hashing with bcrypt
  + Added email validation
  + Created migration file

Running quick checks:
  ✓ Lint: passed
  ✓ Type: passed
  ✓ Tests: skipped (no tests yet)

Task T001 complete. Checkpoint requested.
```
