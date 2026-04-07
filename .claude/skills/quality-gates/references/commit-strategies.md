# Commit Strategies

## Strategies

| Strategy | Behavior | Best For |
|----------|----------|----------|
| `atomic` | One commit per checkpoint (all changed files) | Fast iteration, feature branches |
| `per-file` | Separate commit per modified file | Clean git blame, easy per-file revert |
| `per-task` | One commit per completed task | Task-level traceability |

## Atomic (default)
```
git add <all-changed-files>
git commit -m "feat: implement feature X"
```

## Per-File
```
# For each modified file:
git add src/auth.ts
git commit -m "feat(auth): add token validation"
git add src/middleware.ts
git commit -m "feat(middleware): integrate auth check"
```

Rules for per-file commits:
- Each commit must pass lint independently
- Commit message scopes match the file's module/directory
- If files are tightly coupled (changing one without the other breaks build), commit them together

## Per-Task
```
# After each TaskUpdate(status: completed):
git add <files-modified-for-this-task>
git commit -m "feat: complete task - <task subject>"
```

## Configuration

Set via (checked in order):
1. `/cs-loop --commit-strategy per-file` (argument)
2. `.claude/state/session_start.json` field `commitStrategy`
3. `CLAUDE.local.md` personal default
4. Default: `atomic`
