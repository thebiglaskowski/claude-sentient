---
name: cross-project-patterns
description: Share and learn patterns across multiple projects
model: sonnet
---

# Cross-Project Patterns

Share and learn patterns across multiple projects.

## Description

Captures reusable patterns from projects and applies them to new projects.
Triggers on: "use pattern from", "apply pattern", "share pattern", "best practice", "how did we do this before".

## Pattern Library Location

Global patterns stored in:
```
C:\scripts\prompts\patterns\
├── api/
│   ├── authentication.md
│   ├── error-handling.md
│   └── pagination.md
├── frontend/
│   ├── form-validation.md
│   ├── state-management.md
│   └── component-structure.md
├── database/
│   ├── migrations.md
│   ├── indexing.md
│   └── soft-delete.md
├── testing/
│   ├── mocking.md
│   ├── fixtures.md
│   └── integration.md
└── devops/
    ├── docker.md
    ├── ci-cd.md
    └── monitoring.md
```

## Pattern Format

```markdown
# Pattern: [Name]

## Problem
[What problem does this solve?]

## Solution
[How to implement]

## Code Example
```typescript
// Example implementation
```

## When to Use
- [Scenario 1]
- [Scenario 2]

## When NOT to Use
- [Anti-pattern scenario]

## Variations
- [Variation for different contexts]

## Projects Using This
- project-a (src/auth/...)
- project-b (lib/auth/...)

## Related Patterns
- [Related pattern 1]
- [Related pattern 2]
```

## Capturing Patterns

### Automatic Detection
When implementing something well-structured, offer to save:

```markdown
I notice you've implemented a clean authentication pattern.
Would you like to save this as a reusable pattern?

**Pattern detected:** JWT Authentication with Refresh Tokens
**Files involved:**
- src/auth/jwt.ts
- src/middleware/auth.ts
- src/routes/auth.ts

[Save Pattern] [Skip]
```

### Manual Capture
```
"Save this as a pattern called 'pagination'"
"Create pattern from our error handling"
```

### Pattern Extraction
```markdown
## Extracting Pattern: API Error Handling

**Source Project:** my-api
**Files:**
- src/middleware/errorHandler.ts
- src/utils/errors.ts
- src/types/errors.ts

**Generalized Pattern:**
```typescript
// Generic error handler pattern
export class AppError extends Error {
  constructor(
    public statusCode: number,
    public message: string,
    public code: string
  ) {
    super(message)
  }
}

export const errorHandler = (err, req, res, next) => {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: { code: err.code, message: err.message }
    })
  }
  // ... generic error handling
}
```

**Saved to:** patterns/api/error-handling.md
```

## Applying Patterns

### Search Patterns
```
"How did we handle pagination before?"
"Show me authentication patterns"
"Find patterns for form validation"
```

### Apply to Current Project
```
"Apply the pagination pattern here"
"Use our standard error handling pattern"
```

### Customization on Apply
```markdown
## Applying Pattern: Pagination

**Pattern:** API Pagination
**Target:** src/routes/users.ts

**Customization needed:**
- Default page size: [10] → [20]
- Max page size: [100] → [50]
- Cursor vs offset: [offset] → [cursor]

**Files to create/modify:**
- src/utils/pagination.ts (create)
- src/routes/users.ts (modify)
- src/types/pagination.ts (create)

[Apply with customizations] [Apply as-is] [Cancel]
```

## Pattern Categories

### Code Patterns
- Authentication flows
- Error handling
- Data validation
- API design
- State management

### Architecture Patterns
- Project structure
- Module organization
- Dependency injection
- Event-driven design

### Testing Patterns
- Test organization
- Mocking strategies
- Fixture management
- Integration test setup

### DevOps Patterns
- Docker configurations
- CI/CD pipelines
- Deployment strategies
- Monitoring setup

## Learning from Projects

### Pattern Analysis
When working on a project, learn from it:

```markdown
## Patterns Observed in [Project Name]

**Strong Patterns (consider saving):**
- Clean error handling with custom error classes
- Consistent API response format
- Well-organized test fixtures

**Potential Patterns:**
- Interesting caching strategy
- Custom logging approach

**Anti-Patterns (avoid repeating):**
- Inconsistent naming in models
- Missing input validation in some routes
```

### Cross-Project Insights
```markdown
## Pattern Usage Across Projects

**Most Used Patterns:**
1. JWT Authentication (5 projects)
2. API Error Handling (5 projects)
3. Pagination (4 projects)
4. Form Validation (3 projects)

**Patterns Needing Update:**
- Old Redux pattern → Update to Redux Toolkit
- Class components → Update to Hooks

**Gaps (no pattern exists):**
- Real-time subscriptions
- File upload handling
```

## Syncing Patterns

### Export from Project
```bash
# Export project patterns to global library
claude-patterns export --project ./my-project --to patterns/
```

### Import to Project
```bash
# Import patterns from library to project
claude-patterns import --pattern api/authentication --to ./new-project
```

### Team Sharing
```markdown
## Team Pattern Library

Location: git@github.com:team/patterns.git

**Sync patterns:**
```bash
cd C:\scripts\prompts\patterns
git pull origin main
```

**Contribute pattern:**
```bash
git add patterns/api/new-pattern.md
git commit -m "Add new-pattern for API caching"
git push
```
```

## Pattern Versioning

Track pattern evolution:
```markdown
# Pattern: Authentication

## Version History
- v3 (current): JWT with refresh tokens, httpOnly cookies
- v2: JWT with localStorage (deprecated - security)
- v1: Session-based auth (legacy)

## Migration Guide (v2 → v3)
[Steps to upgrade from v2 to v3]
```

## Integration

### Project Init
When initializing project, suggest relevant patterns:
```markdown
**Detected:** Express.js API project

**Recommended patterns:**
- api/error-handling ⭐ (used in 5 projects)
- api/authentication (used in 4 projects)
- api/pagination (used in 4 projects)
- testing/integration (used in 3 projects)

Apply recommended patterns? [Yes] [Select] [Skip]
```

### Code Review
During review, compare to patterns:
```markdown
**Pattern Compliance Check:**
- ✅ Error handling follows standard pattern
- ⚠️ Pagination differs from pattern (missing total count)
- ❌ Authentication missing refresh token handling
```
