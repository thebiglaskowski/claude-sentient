---
description: Autonomous development loop - init, plan, execute, verify, commit
argument-hint: <task description>
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, TaskCreate, TaskUpdate, TaskList, TaskGet, EnterPlanMode
---

# /cs-loop

The main autonomous development command. Runs a complete cycle: understand the task, plan the work, execute, verify quality, and commit.

## Arguments

- `task`: Description of what to accomplish (required)

## Behavior

### Phase 1: INIT

1. Detect project type by scanning for:
   - `pyproject.toml` or `requirements.txt` → Python
   - `package.json` or `tsconfig.json` → TypeScript
   - `go.mod` → Go
   - `*.sh` or `*.ps1` → Shell
   - Fallback → General

2. Load the matching profile from `profiles/` to get:
   - Lint command
   - Test command
   - Build command (if applicable)

3. Read `.claude/rules/learnings.md` for project-specific context

4. **Auto-load rules based on task keywords:**

   Scan the task description and load matching rules from `rules/`:

   | Keywords | Rules Loaded |
   |----------|--------------|
   | auth, login, password, jwt, oauth | `security`, `api-design` |
   | test, spec, coverage, mock | `testing` |
   | api, endpoint, route, rest | `api-design`, `error-handling` |
   | database, query, schema, migration | `database` |
   | performance, optimize, cache, slow | `performance` |
   | ui, component, css, style | `ui-ux-design` |
   | cli, terminal, command | `terminal-ui` |
   | docs, readme, changelog | `documentation` |
   | refactor, cleanup, quality | `code-quality` |
   | git, commit, branch, pr | `git-workflow` |
   | log, debug, trace | `logging` |
   | error, exception, catch | `error-handling` |

   For each matched rule, read `rules/{rule}.md` and apply those standards.

   Report: `[INIT] Loaded rules: security, api-design`

5. **Check for project governance files** and create if missing:
   - `STATUS.md` — Current progress (create from template if missing)
   - `CHANGELOG.md` — Version history (create from template if missing)
   - `DECISIONS.md` — Architecture decisions (create from template if missing)
   - `.claude/rules/learnings.md` — Session learnings (create if missing)

6. Read `STATUS.md` to understand current project state

7. **Fetch library documentation (if Context7 available):**
   - Scan imports/dependencies in the task-related files
   - For unfamiliar libraries, use Context7 MCP:
     ```
     mcp__context7__resolve-library-id(libraryName: "fastapi")
     mcp__context7__query-docs(libraryId: "/tiangolo/fastapi", query: "routing")
     ```
   - Load relevant documentation into context
   - Report: `[INIT] Loaded docs for: fastapi, sqlalchemy`

8. Report: `[INIT] Profile: {profile}, Tools: {lint}, {test}`

### Phase 2: UNDERSTAND

1. Analyze the task description
2. Classify complexity:
   - **Simple**: Single file, obvious change
   - **Moderate**: Multiple files, clear path
   - **Complex**: Architecture decisions needed → trigger `EnterPlanMode`

3. If complex, use `EnterPlanMode` and wait for user approval before continuing

### Phase 3: PLAN

1. Break the task into discrete work items
2. Use `TaskCreate` for each work item with clear descriptions
3. Use `TaskUpdate` to set dependencies (`addBlockedBy`) where needed
4. Report the plan: `[PLAN] Created {n} tasks`

### Phase 4: EXECUTE

1. Use `TaskList` to see available work
2. Pick the first unblocked pending task
3. Use `TaskUpdate` to mark it `in_progress`
4. Do the work (read files, make changes, etc.)
5. Use `TaskUpdate` to mark it `completed`
6. Repeat until all tasks complete

**Parallel Execution:**

For parallel work, use `Task` tool with appropriate options:

```yaml
# Foreground subagent (wait for result)
Task:
  subagent_type: Explore
  prompt: "Find all API endpoints"

# Background subagent (continue while it runs)
Task:
  subagent_type: general-purpose
  prompt: "Run the test suite"
  run_in_background: true
```

**Background Task Pattern:**
1. Start tests in background after completing a task
2. Continue to next task while tests run
3. Check background task output before commit phase
4. Use `TaskOutput` to retrieve results when ready

Example:
```
[EXECUTE] Task #1 complete
[BACKGROUND] Started test runner (task_id: abc123)
[EXECUTE] Starting task #2...
... (continue working) ...
[EXECUTE] Checking background tasks...
[BACKGROUND] Tests passed (task abc123)
```

### Phase 5: VERIFY

Run quality gates based on detected profile:

```
[VERIFY] Running quality gates...
```

**Check background tasks first:**
If tests were started in background during execute phase:
1. Use `TaskOutput` to check status: `TaskOutput(task_id, block=true)`
2. Wait for completion if still running
3. Fail fast if background tests failed

**Blocking gates** (must pass):
1. **LINT**: Run lint command, expect zero errors
2. **TEST**: Run test command (or use background result), expect all pass
3. **BUILD**: Run build command if defined
4. **GIT**: Check `git status` for clean state

If any gate fails:
- Report the failure clearly
- Attempt to fix (if obvious)
- Re-run the failed gate
- If still failing after 2 attempts, stop and report

### Phase 6: COMMIT

Only if all gates pass:

1. Stage changes: `git add <specific files>`
2. Create commit with descriptive message

3. **Auto-update STATUS.md** (Fully Automatic):
   ```markdown
   ## Current Status
   **Last Updated:** {timestamp}
   **Phase:** {current phase}

   ### Completed This Session
   - {what was just done}

   ### In Progress
   - {current work}

   ### Next Steps
   - {what remains}
   ```

4. **Auto-update CHANGELOG.md** (Auto + Confirm for significant changes):

   **Trigger conditions** (any match triggers):
   - New feature added (`feat:` commits)
   - Breaking change made
   - Bug fixed (`fix:` commits)
   - User explicitly requested version bump

   **Process:**
   - Analyze commits since last version tag
   - Group by type (Added, Changed, Fixed, Removed)
   - Generate entry in Keep a Changelog format
   - If significant changes detected, ask user:
     ```
     AskUserQuestion:
       question: "Ready to update CHANGELOG with these changes?"
       header: "Changelog"
       options:
         - label: "Yes, add to Unreleased (Recommended)"
           description: "Add entries without version bump"
         - label: "Yes, bump to {next_version}"
           description: "Create new version entry"
         - label: "Skip for now"
           description: "Don't update changelog"
     ```

   **Generated format:**
   ```markdown
   ## [Unreleased]

   ### Added
   - Input validation for user API endpoint

   ### Changed
   - Improved error messages for auth failures
   ```

5. Stage governance files: `git add STATUS.md CHANGELOG.md`
6. Amend or create new commit including governance updates
7. Report: `[COMMIT] Created checkpoint: {hash}`

### Phase 7: EVALUATE

1. Check `TaskList` for remaining work
2. If all tasks complete and gates pass:
   - Report: `[DONE] Task complete. {summary}`
   - Exit loop
3. If more work remains:
   - Report: `[LOOP] Continuing with remaining tasks...`
   - Return to Phase 4 (EXECUTE)

## Example Session

```
User: /cs-loop "add input validation to the API"

[INIT] Profile: Python, Tools: ruff, pytest
[INIT] Loaded rules: api-design, error-handling, security
[UNDERSTAND] Moderate complexity - multiple endpoints need validation
[PLAN] Created 4 tasks:
  #1 Add validation schemas
  #2 Update user endpoint [blocked by #1]
  #3 Update order endpoint [blocked by #1]
  #4 Add validation tests [blocked by #2, #3]

[EXECUTE] Starting task #1: Add validation schemas
... (work happens) ...
[EXECUTE] Task #1 complete
[EXECUTE] Starting task #2: Update user endpoint
... (work happens) ...

[VERIFY] Running quality gates...
  LINT: passed
  TEST: passed (12 tests)
  GIT: clean

[COMMIT] Updated STATUS.md
[COMMIT] Updated CHANGELOG.md (Added: Input validation for API)
[COMMIT] Created checkpoint: a1b2c3d

[DONE] Added input validation to 2 API endpoints with 12 tests.
```

## Structured Decisions with AskUserQuestion

When decisions are needed, use `AskUserQuestion` with predefined options instead of free-form questions:

### Example: Approach Selection
```
AskUserQuestion:
  question: "How should we handle authentication?"
  header: "Auth"
  options:
    - label: "JWT tokens (Recommended)"
      description: "Stateless, scalable, industry standard"
    - label: "Session cookies"
      description: "Traditional, requires session store"
    - label: "OAuth only"
      description: "Delegate to external provider"
```

### Example: Risk Confirmation
```
AskUserQuestion:
  question: "This will modify 15 files. Proceed?"
  header: "Confirm"
  options:
    - label: "Yes, proceed"
      description: "Apply all changes"
    - label: "Show me the plan first"
      description: "Review before executing"
```

### When to Use
- Choosing between approaches (2-4 clear options)
- Confirming risky actions
- Gathering preferences
- Resolving ambiguity

Always include a recommended option first with "(Recommended)" suffix when there's a clear best choice.

## Error Handling

| Situation | Response |
|-----------|----------|
| Complex task detected | Use `EnterPlanMode`, wait for approval |
| Gate failure | Attempt fix, retry twice, then stop |
| Ambiguous requirement | Use `AskUserQuestion` with options |
| Stuck > 3 attempts | Stop and report what was tried |

## Governance Files

On first run, `/cs-loop` creates these files if missing (using templates from `templates/`):

| File | Purpose |
|------|---------|
| `STATUS.md` | Project progress, current state |
| `CHANGELOG.md` | Version history (Keep a Changelog format) |
| `DECISIONS.md` | Architecture Decision Records |
| `.claude/rules/learnings.md` | Session learnings (native Claude Code) |

These files provide continuity across sessions and help both humans and Claude understand project context.

## Notes

- This command orchestrates native Claude Code tools - it doesn't replace them
- All work items are tracked via `TaskCreate`/`TaskUpdate`
- Quality gates must pass before committing
- Each commit is a checkpoint for easy rollback
- Governance files are updated at the end of each successful loop
