---
feature: Autonomous Loop
version: "1.0"
last_updated: 2026-03-04
dependencies: []
routes: []
status: draft
---

# Autonomous Loop

> The core 7-phase engine that drives all autonomous development work in Claude Sentient. Invoked via `/cs-loop "task"`.

## Phases

| Phase | Model | Purpose |
|-------|-------|---------|
| INIT | haiku | Detect profile, load context, fetch library docs via MCP |
| UNDERSTAND | sonnet | Classify complexity (simple/moderate/complex) |
| PLAN | sonnet (opus for security/auth/vulnerability) | Create TaskCreate work items, evaluate team eligibility |
| EXECUTE | sonnet | Work through tasks solo or via Agent Teams |
| VERIFY | sonnet (opus for security) | Run quality gates: lint, test, build, git |
| COMMIT | haiku | Stage, commit, update governance docs, link to GitHub issues |
| EVALUATE | haiku | All done → exit; more work → loop back to EXECUTE |

## Model Routing

Default model per phase is derived from the active profile (`profiles/*.yaml`, `models.by_phase`). The cs-multi command can override this per phase and stores configuration in `.claude/state/multi-model.json`.

Security/auth/vulnerability keywords during PLAN and VERIFY force opus model.

## INIT Phase Details

1. Compact recovery: if `.claude/state/compact-context.json` exists, reload prior session intent
2. Load profile from `.claude/state/session_start.json` (written by session-start hook); fall back to file scanning
3. Python environment detection: conda (`environment.yml`) → prefix; venv (`.venv/`) → activate; poetry/pdm (`*.lock`) → prefix
4. Rule auto-loading: keyword matching on task text → rules from `rules/_index.md`; then semantic pass for additional relevance
5. Web project detection → auto-load `ui-ux-design` rule
6. Governance file check: `STATUS.md`, `CHANGELOG.md`, `DECISIONS.md` — create from `templates/` if missing
7. CLAUDE.md check: suggest `/cs-init` if missing
8. MCP: context7 (library docs for detected imports), github (issue/PR details), memory (prior decisions)
9. WebFetch dependency changelogs for update/upgrade/migrate tasks

## PLAN Phase: Team Eligibility

Three signals must all pass for team mode to be offered:
- Scope: 3+ independent tasks in the plan
- Independence: no overlapping file scopes between tasks
- Complexity: more than a simple bug fix

Requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` env var. If not set, skips silently.

## EXECUTE Phase

Standard mode:
1. `TaskList` → pick first unblocked task
2. `TaskGet(taskId)` → fetch full description
3. `TaskUpdate(status: in_progress)` → save `{taskId, subject, startedAt}` to `.claude/state/current_task.json`
4. Do work
5. `TaskUpdate(status: completed)`
6. Repeat

The task list is a living document — tasks may be added, split, or reordered during execution.

## VERIFY Phase: Auto-Fix Sub-Loop

Max 3 attempts per gate:
1. Classify error
2. Run `fix_command` from profile or manual fix
3. Re-verify

If error count increases → revert immediately. After 3 failures → WebSearch (2 attempts max).

**Hard constraints**: Never modify test assertions. Never skip gates.

## COMMIT Phase

1. Stage changes: `git add <files>`
2. Conventional commit message (`feat:`, `fix:`, `chore:`, etc.)
3. Doc sync check: if changed files match a feature in `documentation/`, offer to run `/cs-docs "feature"`
4. Auto-update `STATUS.md` and `CHANGELOG.md` for `feat:`/`fix:` commits
5. MCP: github (link commits to issues, create PRs), memory (persist session state)
6. Auto-capture learnings via `/cs-learn`

## EVALUATE Phase

- All tasks complete → `[DONE] {summary}` and exit
- More work found → `[LOOP] Continuing...` → return to EXECUTE
- Context > 50% → compact before next iteration

## State Files

| File | Written By | Purpose |
|------|-----------|---------|
| `.claude/state/session_start.json` | session-start hook | Profile, project root, session ID |
| `.claude/state/current_task.json` | cs-loop EXECUTE | Currently active task |
| `.claude/state/compact-context.json` | pre-compact hook | Session summary for continuity |
| `.claude/state/multi-model.json` | cs-multi | Per-phase model overrides |

## Business Rules

- **Context management**: Never stop early due to context. Save state before compaction.
- **Error ownership**: Never claim errors are "pre-existing" without git blame proof.
- **Test integrity**: Never hard-code values or modify test assertions.
- **Architecture alignment**: Check DECISIONS.md before implementing. Match existing patterns.
