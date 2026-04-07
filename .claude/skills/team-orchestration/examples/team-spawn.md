# Example: Spawning a 3-Agent Team

## Scenario
Task: "Refactor auth - new JWT middleware, update DB schema, add login form"

## Eligibility Check
- 3 independent tasks: middleware (backend), schema (database), form (frontend)
- Non-overlapping scopes: src/middleware/, migrations/, src/components/
- Complexity: moderate
- CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS: set

## Work Stream Partition

| Stream | Agent | Files | Branch |
|--------|-------|-------|--------|
| 1 | backend | src/middleware/auth.ts, src/routes/login.ts | team/backend-auth |
| 2 | database | migrations/003-jwt.sql, src/models/session.ts | team/database-jwt |
| 3 | frontend | src/components/LoginForm.tsx, src/hooks/useAuth.ts | team/frontend-login |

## Merge Order
1. Database first (schema is foundational)
2. Backend second (depends on schema)
3. Frontend last (depends on API)

## Result
3 clean branches, each passing gates, merged in dependency order.
