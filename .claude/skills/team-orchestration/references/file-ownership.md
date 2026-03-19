# File Ownership & Partitioning Strategy

Reference for preventing edit conflicts during Agent Teams execution.

## Partitioning Rules

1. **Each file has exactly one owner** — the teammate whose task scope includes it
2. **Shared files must be pre-assigned** — files needed by multiple teammates (e.g., `index.ts`, `CHANGELOG.md`) must be assigned to one owner; others read-only
3. **Directory-level partitioning preferred** — assign whole directories when possible (`src/auth/` → security teammate, `src/api/` → backend teammate)

## Conflict Detection

The `task-completed.cjs` hook maintains a file ownership map in `team-state.json`:

```json
{
  "file_ownership": {
    "src/auth/login.ts": "security-agent",
    "src/api/routes.ts": "backend-agent"
  }
}
```

When a task completes, the hook checks each modified file against the ownership map. If a file was modified by a different teammate than its owner, the task is rejected (exit code 2) with feedback.

## Common Conflict Patterns

| Pattern | Example | Solution |
|---------|---------|----------|
| Shared config | Both teammates edit `tsconfig.json` | Assign to one; other requests changes via message |
| Re-exports | Teammate A adds export, teammate B imports | Assign `index.ts` to one teammate |
| Test + source | Tester edits source to add test hooks | Tester owns tests only; source owner adds hooks |
| Documentation | Both update README | Assign docs to one teammate or split by section |

## Recovery from Conflicts

If "File modified since read" error occurs:
1. Re-read the file to get latest content
2. Merge your intended changes with the teammate's changes
3. If merge is complex, send a message to the lead for arbitration

## Caps

- `file_ownership` map: capped at 200 entries (MAX_FILE_OWNERSHIP)
- `completed_tasks` array: capped at 100 entries (MAX_COMPLETED_TASKS)
