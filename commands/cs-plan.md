---
description: Plan a complex task before executing
argument-hint: <task description>
allowed-tools: Read, Glob, Grep, Task, EnterPlanMode, ExitPlanMode, TaskCreate, TaskUpdate, AskUserQuestion
---

# /cs-plan

Plan a complex task before executing. Uses Claude Code's native `EnterPlanMode` with project-aware context.

## Arguments

- `task`: Description of what to plan (required)

## Behavior

### 1. Gather Context

Before entering plan mode, gather relevant context:

1. **Detect profile**: Scan for `pyproject.toml`, `package.json`, etc.
2. **Load learnings**: Read `.claude/rules/learnings.md`
3. **Explore codebase**: Use `Task` with `subagent_type=Explore` to understand:
   - Existing patterns
   - Related code
   - Potential impact areas

### 2. Enter Plan Mode

Invoke `EnterPlanMode` to transition into planning.

In plan mode:
- Explore the codebase thoroughly
- Identify files that need changes
- Consider architectural implications
- Document the approach

### 3. Write Plan

Create a structured plan covering:

```markdown
## Task
{What we're trying to accomplish}

## Approach
{High-level strategy}

## Changes Required
1. {File/component} - {What changes}
2. {File/component} - {What changes}
...

## Dependencies
- {What needs to happen first}

## Risks
- {Potential issues and mitigations}

## Quality Gates
- {What tests/checks will verify success}
```

### 4. Exit Plan Mode

Use `ExitPlanMode` to present the plan to the user for approval.

### 5. After Approval (Optional)

If the user approves and wants to proceed:
- Use `TaskCreate` to create work items from the plan
- Set dependencies with `TaskUpdate`
- Report: `[PLAN] Ready to execute. Run /cs-loop to begin.`

## Example

```
User: /cs-plan "refactor authentication to use JWT"

[PLAN] Gathering context...
  Profile: TypeScript
  Learnings: 3 relevant decisions loaded

[PLAN] Exploring codebase...
  Found: src/auth/session.ts (current session-based auth)
  Found: src/middleware/auth.ts (auth middleware)
  Found: src/routes/login.ts (login endpoint)

[PLAN] Entering plan mode...

## Task
Replace session-based authentication with JWT tokens.

## Approach
1. Add JWT library and token utilities
2. Update login to issue JWT instead of session
3. Replace session middleware with JWT verification
4. Update protected routes to use new middleware
5. Add token refresh endpoint

## Changes Required
1. package.json - Add jsonwebtoken dependency
2. src/auth/jwt.ts - New JWT utility module
3. src/auth/session.ts - Remove (deprecated)
4. src/middleware/auth.ts - JWT verification
5. src/routes/login.ts - Issue JWT on login
6. src/routes/refresh.ts - New refresh endpoint

## Dependencies
- JWT utilities must exist before middleware update
- Middleware must work before route updates

## Risks
- Breaking change for existing sessions
- Need migration strategy for active users

## Quality Gates
- All auth tests pass
- Manual test: login → access protected route → refresh

[Waiting for approval...]
```

## Structured Decisions

When multiple approaches exist, use `AskUserQuestion` to let the user choose:

```
AskUserQuestion:
  question: "Which approach should we use for the refactor?"
  header: "Approach"
  options:
    - label: "Incremental migration (Recommended)"
      description: "Lower risk, can ship in stages"
    - label: "Complete rewrite"
      description: "Cleaner result, higher risk"
    - label: "Adapter pattern"
      description: "Wrap old code, minimal changes"
```

**Common architecture decisions:**

| Decision | Header | Options |
|----------|--------|---------|
| API style | "API" | REST (standard), GraphQL (flexible queries), gRPC (high perf) |
| Data layer | "Data" | ORM (convenient), Query builder (control), Raw SQL (performance) |
| Async pattern | "Async" | Callbacks, Promises/async-await, Reactive streams |
| Caching | "Cache" | In-memory (simple), Redis (distributed), CDN (edge) |
| Deployment | "Deploy" | Containers (portable), Serverless (scaling), VMs (control) |

This is better than free-form questions because:
- User sees all options at once
- Clear descriptions help decision-making
- Faster to click than type

## When to Use

Use `/cs-plan` instead of `/cs-loop` when:
- Task involves architectural decisions
- Multiple approaches are possible
- Changes affect many files
- Risk of breaking existing functionality
- You want to review before execution

## Notes

- This leverages native `EnterPlanMode` - not a custom implementation
- The plan is presented for user approval before any changes
- After approval, work items can be created for `/cs-loop`
