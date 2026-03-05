---
feature: Planning
version: "1.0"
last_updated: 2026-03-04
dependencies: []
routes: []
status: draft
---

# Planning

> `/cs-plan` orchestrates structured pre-implementation planning using Claude Code's native `EnterPlanMode`/`ExitPlanMode`. Creates tasks with dependencies after approval; optionally chains directly into `/cs-loop` for execution.

## When to Use `/cs-plan` vs `/cs-loop`

| Situation | Use |
|-----------|-----|
| Architectural decisions exist | `/cs-plan` |
| Multiple approaches possible | `/cs-plan` |
| Changes affect many files | `/cs-plan` |
| Risk of breaking existing functionality | `/cs-plan` |
| Simple, clear-cut task | `/cs-loop` directly |
| Already have a clear plan | `/cs-loop` directly |

`/cs-loop` also enters plan mode automatically for complex tasks detected during UNDERSTAND phase.

## Planning Flow

```
/cs-plan "task description"
  → Gather context (profile, learnings, explore codebase)
  → EnterPlanMode
    → Explore codebase with Glob/Grep/Read
    → AskUserQuestion for architectural decisions (if needed)
    → Write plan to plan file
  → ExitPlanMode (presents plan for user approval)
  → [User approves]
  → TaskCreate for each work item
  → TaskUpdate(addBlockedBy) for dependencies
  → AskUserQuestion: "Execute now?"
  → [If yes] Skill("cs-loop", args=task)
```

## Plan Structure

Plans follow a standard Markdown structure:

```markdown
## Task
{What we're trying to accomplish — specific, not vague}

## Approach
{High-level strategy — why this approach vs alternatives}

## Changes Required
1. {File/component} — {What changes and why}
2. {File/component} — {What changes and why}
...

## Dependencies
- {What must happen before what}

## Risks
- {What could go wrong and mitigation}

## Quality Gates
- {What tests/checks verify success}
```

## Task Creation After Approval

After user approves the plan:

1. `TaskCreate` for each work item in "Changes Required"
2. `TaskUpdate(addBlockedBy: [taskId])` for dependency chains
3. Report: `[PLAN] Created {n} tasks`
4. Offer execution via `AskUserQuestion`

### Dependency Patterns

```
Task A → Task B → Task C     (sequential)
Task A → Task B              (parallel from A)
       → Task C
```

Tasks marked `addBlockedBy` won't appear as available until their dependencies complete.

## Architectural Decision Questions

When multiple valid approaches exist, `AskUserQuestion` presents options:

| Decision | Header | Typical Options |
|----------|--------|----------------|
| API style | "API" | REST / GraphQL / gRPC |
| Data layer | "Data" | ORM / Query builder / Raw SQL |
| Async pattern | "Async" | Promises / Observables / Callbacks |
| Caching | "Cache" | In-memory / Redis / CDN |
| Deployment | "Deploy" | Containers / Serverless / VMs |

**Business rule**: Present options rather than asking open-ended questions. Users click faster than they type.

## Flags

| Flag | Effect |
|------|--------|
| `--fork` | Create a fork of the current session for experimental planning |
| `--model opus` | Force opus for planning (default: sonnet) |

**Model selection**: Defaults to sonnet. Use `--model opus` for the most complex or high-stakes architectural plans.

## Context Gathering (Pre-Plan)

Before entering plan mode, `/cs-plan` gathers:

1. **Profile**: scan for `session_start.json`, fall back to file scanning
2. **Learnings**: read `.claude/rules/learnings.md` for prior decisions
3. **Codebase exploration**: spawn `Explore` subagent for existing patterns and potential impact areas

This ensures the plan respects existing architecture rather than inventing conflicting patterns.

## Auto-Capture of Decisions

Architecture choices made during planning are automatically saved via `/cs-learn`:

```
Skill("cs-learn", args="decision 'Use PostgreSQL for session storage' 'Considered Redis but PostgreSQL already in stack'")
```

This prevents re-litigating the same decisions in future sessions.

## Business Rules

- **EnterPlanMode is mandatory**: `/cs-plan` must use native `EnterPlanMode` — not a simulated plan in prose. The native tool presents the plan to the user for approval before any files are changed.
- **No code before approval**: `/cs-plan` is a planning command. No file edits happen until the user approves the plan via `ExitPlanMode`.
- **Explore before proposing**: Never propose changes to code you haven't read. Always explore before writing the plan.
- **Task granularity**: One task per logical work unit. Don't bundle unrelated changes into a single task — it makes progress tracking meaningless.
- **Dependencies are load-bearing**: If Task B truly cannot start until Task A completes (e.g., a utility function must exist before callers are written), model this with `addBlockedBy`. Don't leave implicit ordering to chance.

## Edge Cases

- **User rejects plan**: Revise and re-present. Don't start implementing anyway.
- **Plan reveals more complexity**: Add tasks during execution. The task list is a living document.
- **No codebase to explore**: New project — plan based on requirements alone, note assumptions clearly.
- **Ambiguous task**: Use `AskUserQuestion` during planning (not after) to clarify before writing the plan.
- **--fork flag**: Creates an isolated session branch so experimental plans don't affect the main session state.
