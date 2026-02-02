---
description: Autonomous development loop - init, plan, execute, verify, commit
argument-hint: <task description>
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, TaskCreate, TaskUpdate, TaskList, TaskGet, EnterPlanMode, AskUserQuestion, mcp__plugin_context7_context7__resolve-library-id, mcp__plugin_context7_context7__query-docs, mcp__github__get_issue, mcp__github__list_issues, mcp__github__create_pull_request, mcp__github__add_issue_comment, mcp__memory__read_graph, mcp__memory__create_entities, mcp__memory__add_observations, mcp__puppeteer__puppeteer_navigate, mcp__puppeteer__puppeteer_screenshot
---

# /cs-loop

Autonomous development loop: understand → plan → execute → verify → commit.

## MCP Server Integration

This command leverages available MCP servers for enhanced capabilities:

| Server | Phase | Usage |
|--------|-------|-------|
| **context7** | INIT | Auto-fetch library docs for detected imports |
| **github** | INIT, COMMIT | Fetch issue details, create PRs, link commits |
| **memory** | INIT, COMMIT | Persist session state for resumability |
| **puppeteer** | VERIFY | Screenshot web apps after changes (web projects) |

## Phases

### 1. INIT

1. **Detect profile** by scanning for project files:

   | Files | Profile | Tools |
   |-------|---------|-------|
   | `pyproject.toml`, `*.py` | Python | ruff, pytest |
   | `package.json`, `tsconfig.json` | TypeScript | eslint, vitest |
   | `go.mod` | Go | golangci-lint, go test |
   | `Cargo.toml` | Rust | clippy, cargo test |
   | `pom.xml`, `build.gradle` | Java | checkstyle, JUnit |
   | `CMakeLists.txt`, `Makefile` | C/C++ | clang-tidy, ctest |
   | `Gemfile` | Ruby | rubocop, rspec |
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

4. **MCP: Context7** — Fetch library documentation:
   ```
   - Scan task-related files for imports/dependencies
   - For each unfamiliar library:
     1. mcp__plugin_context7_context7__resolve-library-id(libraryName, query)
     2. mcp__plugin_context7_context7__query-docs(libraryId, query)
   - Inject relevant docs into context
   ```

5. **MCP: GitHub** — If task references issues:
   ```
   - Detect patterns: "fix #123", "closes #456", "issue 789"
   - Fetch issue details: mcp__github__get_issue(owner, repo, issue_number)
   - Extract requirements, acceptance criteria from issue body
   - Report: [INIT] Loaded GitHub issue #123: {title}
   ```

6. **MCP: Memory** — Check for previous session state:
   ```
   - mcp__memory__read_graph() to check for prior context
   - If found: load previous tasks, decisions, blockers
   - Report: [INIT] Resumed from previous session (if applicable)
   ```

7. Report: `[INIT] Profile: {name}, Tools: {lint}, {test}, MCP: {servers}`

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

**MCP: Puppeteer** — For web projects (detected by `package.json` with web framework):
```
- If significant UI changes were made:
  1. mcp__puppeteer__puppeteer_navigate(url) to dev server
  2. mcp__puppeteer__puppeteer_screenshot(name) for visual verification
  3. Report: [VERIFY] Screenshot saved: {name}
- Skip if no dev server running or not a web project
```

If gate fails: attempt fix, retry twice, then stop and report.

### 6. COMMIT

1. Stage changes: `git add <files>`
2. Create commit with conventional message (`feat:`, `fix:`, etc.)
3. **Auto-update STATUS.md** with session progress
4. **Auto-update CHANGELOG.md** for `feat:` and `fix:` commits

**MCP: GitHub** — Link commits to issues and optionally create PRs:
```
- If task referenced an issue:
  1. Include "Fixes #123" or "Closes #123" in commit message
  2. Optionally: mcp__github__add_issue_comment with progress update
- If on feature branch and task is complete:
  1. Ask user: "Create PR for this branch?"
  2. If yes: mcp__github__create_pull_request(owner, repo, title, head, base)
  3. Report: [COMMIT] PR created: {url}
```

**MCP: Memory** — Persist session state for resumability:
```
- mcp__memory__create_entities or mcp__memory__add_observations:
  - Current task progress
  - Decisions made during session
  - Any blockers encountered
- Enables `/cs-loop` to resume where it left off
```

5. Report: `[COMMIT] Created checkpoint: {hash}`

### 7. EVALUATE

- All tasks complete? → `[DONE] {summary}` and exit
- More work? → `[LOOP] Continuing...` and return to EXECUTE

**MCP: Memory** — On completion, save final state:
```
- mcp__memory__add_observations with:
  - Session summary
  - What was accomplished
  - Any follow-up tasks identified
```

## Error Handling

| Situation | Response |
|-----------|----------|
| Complex task | `EnterPlanMode`, wait for approval |
| Gate failure | Fix, retry twice, then stop |
| Ambiguous | `AskUserQuestion` with options |
| Stuck > 3 attempts | Stop and report |

## Notes

- Uses native Claude Code tools (`TaskCreate`, `EnterPlanMode`, etc.)
- MCP servers are used when available; gracefully skipped if not connected
- Quality gates must pass before committing
- Each commit is a checkpoint for rollback
