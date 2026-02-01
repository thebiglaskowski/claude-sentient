---
description: Autonomous development loop - init, plan, execute, verify, commit
argument-hint: <task description>
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, TaskCreate, TaskUpdate, TaskList, TaskGet, EnterPlanMode, AskUserQuestion
---

# /cs-loop

Autonomous development loop: understand → plan → execute → verify → commit.

## Phases

### 1. INIT

1. **Detect profile** by scanning for project files:

   | Files | Profile | Tools |
   |-------|---------|-------|
   | `pyproject.toml`, `*.py` | Python | ruff, pytest |
   | `package.json`, `tsconfig.json` | TypeScript | eslint, vitest |
   | `go.mod` | Go | golangci-lint, go test |
   | `*.sh`, `*.ps1` | Shell | shellcheck |
   | (fallback) | General | auto-detect |

2. **Load rules** based on task keywords:

   | Keywords | Rules |
   |----------|-------|
   | auth, login, jwt | security, api-design |
   | test, coverage | testing |
   | api, endpoint | api-design, error-handling |
   | database, query | database |
   | refactor, quality | code-quality |
   | cli, command | terminal-ui |

3. **Check governance files** — create from `templates/` if missing:
   - `STATUS.md`, `CHANGELOG.md`, `DECISIONS.md`, `.claude/rules/learnings.md`

4. **Load Context7 docs** for unfamiliar libraries (if available)

5. Report: `[INIT] Profile: {name}, Tools: {lint}, {test}`

### 2. UNDERSTAND

Classify complexity:
- **Simple**: Single file → proceed
- **Moderate**: Multiple files, clear path → proceed
- **Complex**: Architecture decisions → use `EnterPlanMode`

### 3. PLAN

1. Break task into work items using `TaskCreate`
2. Set dependencies with `TaskUpdate(addBlockedBy: [...])`
3. Report: `[PLAN] Created {n} tasks`

### 4. EXECUTE

1. `TaskList` → pick first unblocked task
2. `TaskUpdate(status: in_progress)`
3. Do the work
4. `TaskUpdate(status: completed)`
5. Repeat until all complete

Use `Task` tool with `run_in_background: true` for parallel work (e.g., running tests while continuing).

### 5. VERIFY

Run quality gates from profile:

| Gate | Action |
|------|--------|
| LINT | Run lint command, expect 0 errors |
| TEST | Run test command, all must pass |
| BUILD | Run build command if defined |
| GIT | Check `git status` is clean |

If gate fails: attempt fix, retry twice, then stop and report.

### 6. COMMIT

1. Stage changes: `git add <files>`
2. Create commit with conventional message (`feat:`, `fix:`, etc.)
3. **Auto-update STATUS.md** with session progress
4. **Auto-update CHANGELOG.md** for `feat:` and `fix:` commits
5. Report: `[COMMIT] Created checkpoint: {hash}`

### 7. EVALUATE

- All tasks complete? → `[DONE] {summary}` and exit
- More work? → `[LOOP] Continuing...` and return to EXECUTE

## Error Handling

| Situation | Response |
|-----------|----------|
| Complex task | `EnterPlanMode`, wait for approval |
| Gate failure | Fix, retry twice, then stop |
| Ambiguous | `AskUserQuestion` with options |
| Stuck > 3 attempts | Stop and report |

## Notes

- Uses native Claude Code tools (`TaskCreate`, `EnterPlanMode`, etc.)
- Quality gates must pass before committing
- Each commit is a checkpoint for rollback
