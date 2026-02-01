# Phase 7: Commit

> **Purpose:** Create verified checkpoint commits for rollback
> **Duration:** ~30 seconds
> **Triggers:** After quality gates pass

---

## Overview

The commit phase creates a verified commit that serves as a checkpoint. If something goes wrong later, we can roll back to this known-good state.

---

## Process

### 1. Stage Changes

```
IDENTIFY changed files:
  - New files created
  - Modified files
  - Deleted files (if any)

STAGE appropriate files:
  git add <specific files>

EXCLUDE:
  - .claude/state/* (session-specific)
  - Files in .gitignore
```

### 2. Generate Commit Message

```
FORMAT: Conventional Commits

<type>(<scope>): <description>

[body with details]

[CHECKPOINT: <checkpoint_id>]

TYPES:
  feat: New feature
  fix: Bug fix
  refactor: Code restructuring
  test: Adding tests
  docs: Documentation
  chore: Maintenance
```

### 3. Create Commit

```
git commit -m "<message>"

IF hooks fail:
  FIX issue
  RETRY commit

IF still failing:
  LOG error
  CONTINUE without commit (warn user)
```

### 4. Record Checkpoint

```
ADD to .claude/state/checkpoints.json:
  {
    "id": "CP-001",
    "commit": "<sha>",
    "timestamp": "<iso8601>",
    "tasks_completed": ["T001", "T002"],
    "gates_passed": ["LINT", "TYPE", "TEST", ...],
    "description": "Added user authentication"
  }
```

### 5. Update State

```
UPDATE work_queue:
  - Mark checkpointed tasks as committed

UPDATE loop state:
  - last_checkpoint: "<sha>"
  - checkpoints_count: +1
```

---

## Commit Message Examples

```
feat(auth): add user model with password hashing

- Created User model with email validation
- Added bcrypt password hashing
- Created database migration
- Added basic user tests

[CHECKPOINT: CP-001]
```

```
fix(api): resolve null pointer in user lookup

- Added null check before accessing user.email
- Added test case for missing user scenario

[CHECKPOINT: CP-003]
```

---

## Checkpoint Triggers

Checkpoints are created:
- After each S0/S1 task completes
- After every 3 S2 tasks complete
- Before risky changes
- At logical boundaries (e.g., feature complete)
- When explicitly requested

---

## Rollback Capability

```
TO ROLLBACK to checkpoint:
  git revert --no-commit <checkpoint_sha>..HEAD

OR for hard reset:
  git reset --hard <checkpoint_sha>

RESTORE state:
  Load .claude/state/ from that commit
```

---

## Outputs

| Output | Description |
|--------|-------------|
| `commit_sha` | Git commit hash |
| `checkpoint_id` | Checkpoint identifier |
| `files_committed` | List of committed files |
| `rollback_available` | Boolean |

---

## Skip Conditions

```
SKIP IF:
  - No changes since last commit
  - Only state file changes

CANNOT SKIP IF:
  - Code changes exist
  - Task marked for checkpoint
```

---

## Error Handling

| Error | Recovery |
|-------|----------|
| Pre-commit hook fails | Fix issue, retry |
| Merge conflict | Cannot happen (single branch) |
| Commit fails | Log error, continue, warn user |

---

## Example

```
[COMMIT] Creating checkpoint...

Staging files:
  + src/models/user.py
  + src/services/auth.py
  + tests/test_user.py
  M src/routes/api.py

Commit message:
  feat(auth): add user model and auth service

  - Created User model with bcrypt password hashing
  - Created AuthService with JWT token generation
  - Added comprehensive tests

  [CHECKPOINT: CP-001]

Created commit: a1b2c3d
Checkpoint CP-001 recorded.

Ready for evaluation.
```
