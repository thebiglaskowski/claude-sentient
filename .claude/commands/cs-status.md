---
description: Show current project status - tasks, git state, profile
argument-hint: (no arguments)
allowed-tools: Read, Bash, Glob, TaskList
---

# /cs-status

Display the current status of the project including active tasks, git state, and detected profile.

## Arguments

None.

## Behavior

### 1. Detect Profile

Scan for project indicators:
- `pyproject.toml` → Python
- `package.json` / `tsconfig.json` → TypeScript
- `go.mod` → Go
- `*.sh` / `*.ps1` → Shell
- Fallback → General

### 2. Get Task Status

Use `TaskList` to show current work items:
- Pending tasks
- In-progress tasks
- Blocked tasks (and what blocks them)
- Recently completed

### 3. Get Git Status

Run `git status --short` and `git log --oneline -3` to show:
- Current branch
- Uncommitted changes
- Recent commits

### 4. Check Quality Gates

Quick check of gate status:
- Can lint run? (tool exists)
- Can tests run? (test files exist)
- Any obvious issues?

### 5. Check Governance Files

Check for required project files:
- `STATUS.md` — ✓ exists or ✗ missing
- `CHANGELOG.md` — ✓ exists or ✗ missing
- `DECISIONS.md` — ✓ exists or ✗ missing
- `.claude/rules/learnings.md` — ✓ exists or ✗ missing

If any are missing, suggest: `Run /cs-loop to create missing files`

### 6. Show Learnings Summary

Count entries in `.claude/rules/learnings.md`:
- Decisions
- Patterns
- Learnings

## Output Format

```
=== Claude Sentient Status ===

PROFILE: Python
  Lint: ruff
  Test: pytest
  Build: python -m build

TASKS:
  #3 [in_progress] Implement validation schemas
  #4 [pending] Add endpoint tests [blocked by #3]
  #5 [pending] Update documentation [blocked by #4]

  Completed today: 2
  Remaining: 3

GIT:
  Branch: feature/validation
  Status: 2 files modified, 1 untracked

  Recent commits:
  a1b2c3d Add user model
  b2c3d4e Initial project setup

QUALITY:
  Lint: ready (ruff installed)
  Test: ready (15 test files found)
  Build: ready

GOVERNANCE:
  STATUS.md: ✓ exists
  CHANGELOG.md: ✓ exists
  DECISIONS.md: ✓ exists
  learnings.md: ✓ exists

MEMORY:
  Decisions: 3
  Patterns: 1
  Learnings: 2

=== Ready for /cs-loop ===
```

## Example

```
User: /cs-status

=== Claude Sentient Status ===

PROFILE: TypeScript
  Lint: eslint
  Test: vitest
  Build: tsc

TASKS:
  No active tasks.

  Run /cs-loop "task" to start work.

GIT:
  Branch: main
  Status: clean

  Recent commits:
  f4e5d6c feat: Add authentication
  d3c2b1a fix: Handle edge case

QUALITY:
  Lint: ready
  Test: ready (23 test files)
  Build: ready

MEMORY:
  Decisions: 5
  Patterns: 2
  Learnings: 3

=== Ready for /cs-loop ===
```

## Notes

- This is a read-only command - it doesn't modify anything
- Useful to run before starting work to understand current state
- Shows what tools are available based on detected profile
