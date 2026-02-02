---
name: smart-context-v3
description: Enhanced context management with !command syntax for dynamic context injection
version: 3.0.0
triggers:
  - "!files"
  - "!recent"
  - "!related"
  - "!deps"
  - "!tests"
  - "context"
  - "load context"
model: sonnet
tags: [orchestration, context, optimization]
context: minimal
---

# Smart Context v3

Enhanced context management system that dynamically loads relevant files and data based on task needs. Uses `!command` syntax for explicit context requests.

---

## Quick Commands

| Command | Description | Example |
|---------|-------------|---------|
| `!files <pattern>` | Load files matching pattern | `!files src/auth/*.ts` |
| `!recent [n]` | Load n most recently modified files | `!recent 5` |
| `!related <file>` | Load files related to specified file | `!related src/api/users.ts` |
| `!deps <file>` | Load dependencies of a file | `!deps src/index.ts` |
| `!tests <file>` | Load test files for a source file | `!tests src/auth/login.ts` |
| `!imports <file>` | Load files that import this file | `!imports src/utils/helpers.ts` |
| `!changed` | Load files changed in current branch | `!changed` |
| `!staged` | Load files staged for commit | `!staged` |
| `!search <query>` | Load files containing query | `!search "TODO"` |
| `!context clear` | Clear loaded context | `!context clear` |
| `!context show` | Show currently loaded context | `!context show` |

---

## Automatic Context Loading

Smart Context automatically loads relevant files based on:

### 1. Task Keywords
```
Task mentions "auth" → Load src/auth/, middleware/auth*, tests/auth/
Task mentions "api"  → Load src/api/, routes/, openapi.yaml
Task mentions "db"   → Load prisma/, models/, migrations/
```

### 2. Error Messages
```
Error in "src/foo.ts:42" → Load src/foo.ts + related tests
Import error for "bar"   → Load files defining "bar"
Type error in interface  → Load type definition file
```

### 3. File References
```
User mentions "login.ts"   → Load src/**/login.ts + tests
User shares stack trace    → Load files in trace
User pastes code snippet   → Find matching file
```

---

## Context Budget Management

### Token Allocation
```
Total budget: 4000 tokens (configurable)

Allocation by priority:
├── Primary files (70%): Files being modified
├── Test files (15%): Related tests
├── Reference (10%): Types, interfaces, utils
└── Docs (5%): README, comments

When over budget:
├── Summarize large files
├── Load function signatures only
├── Defer low-priority files
└── Offer to load more on request
```

### Budget Commands
```
!context budget         → Show current usage
!context budget 6000    → Increase budget
!context compress       → Summarize loaded context
```

---

## Relationship Detection

### File Relationships
```
Source → Test:
  src/auth/login.ts → tests/auth/login.test.ts
  src/utils/format.ts → src/utils/__tests__/format.test.ts

Import Graph:
  src/index.ts imports src/app.ts imports src/routes/index.ts

Type Dependencies:
  src/api/users.ts uses types from src/types/user.ts
```

### Relationship Commands
```
!graph <file>     → Show import/export graph
!dependents <file> → Files that depend on this
!dependencies <file> → Files this depends on
```

---

## Context Profiles

### Profile Definitions
```yaml
security:
  include:
    - src/auth/**
    - src/middleware/auth*
    - src/utils/crypto*
  rules:
    - "@rules/security"

api:
  include:
    - src/api/**
    - src/routes/**
    - openapi.yaml
  rules:
    - "@rules/api-design"

frontend:
  include:
    - src/components/**
    - src/pages/**
    - src/styles/**
  rules:
    - "@rules/ui-ux-design"
```

### Profile Commands
```
!profile security   → Load security-focused context
!profile api        → Load API-focused context
!profile frontend   → Load frontend-focused context
!profile save <name> → Save current context as profile
!profile list       → List available profiles
```

---

## Session Memory Integration

### Persistent Context
```
Across messages, remember:
├── Files already loaded
├── User preferences
├── Project structure
├── Common patterns

This prevents:
├── Re-reading same files
├── Re-discovering structure
├── Redundant searches
```

### Memory Commands
```
!remember <file>  → Add to persistent context
!forget <file>    → Remove from persistent context
!memory show      → Show persistent context
!memory clear     → Clear session memory
```

---

## Smart Loading Strategies

### Lazy Loading
```
Don't load everything upfront:

1. Start with file signatures (function names, exports)
2. Load full implementation on demand
3. Expand context as work progresses
4. Compress completed sections
```

### Predictive Loading
```
Based on task type, preload:

Bug fix: Error location + related tests + recent changes
Feature: Similar features + design patterns + types
Refactor: All dependents + full test suite
Review: Changed files + related tests + style guide
```

### Incremental Context
```
As work progresses:

Phase 1: Overview (structure, exports)
Phase 2: Relevant sections
Phase 3: Implementation details
Phase 4: Edge cases and tests
```

---

## Context Output Format

### When showing loaded context:
```markdown
## Loaded Context (2,450 / 4,000 tokens)

### Primary (1,750 tokens)
- src/auth/login.ts (450 tokens) ✓
- src/auth/session.ts (380 tokens) ✓
- src/middleware/auth.ts (420 tokens) ✓
- src/types/user.ts (500 tokens, summarized)

### Tests (400 tokens)
- tests/auth/login.test.ts (400 tokens) ✓

### Reference (300 tokens)
- src/utils/crypto.ts (signatures only)
- src/config/auth.ts (150 tokens)

### Available on request:
- tests/auth/session.test.ts
- src/api/users.ts
```

---

## Integration with Hooks

### Context Injector Hook
```
UserPromptSubmit → context-injector.py analyzes prompt
                → Suggests context based on keywords
                → Auto-loads if within budget
```

### Usage with Orchestrator
```
Task Orchestrator → Classifies task type
                 → Invokes smart-context profile
                 → Loads appropriate context
                 → Adjusts budget per task
```

---

## Examples

### Example 1: Bug Fix
```
User: "Fix the login timeout issue"

Smart Context:
1. Detects "login" + "timeout" keywords
2. Loads: src/auth/login.ts, src/auth/session.ts
3. Loads: Related tests
4. Loads: Recent commits touching these files
5. Shows: !recent changes to auth/*
```

### Example 2: New Feature
```
User: "Add rate limiting to the API"

Smart Context:
1. Detects "API" + "rate limiting" keywords
2. Loads: src/api/**, middleware/*
3. Loads: Similar middleware patterns
4. Suggests: !search "rate limit" for existing attempts
5. Offers: context7 lookup for rate limiting patterns
```

### Example 3: Explicit Context
```
User: "!files src/utils/*.ts !tests src/utils"

Smart Context:
1. Loads all src/utils/*.ts files
2. Loads all test files in src/utils/
3. Shows: Token usage summary
4. Offers: !related for related files
```

---

## Configuration

### settings.json
```json
{
  "smartContext": {
    "enabled": true,
    "defaultBudget": 4000,
    "autoLoad": true,
    "profiles": {
      "minimal": { "budget": 2000 },
      "standard": { "budget": 4000 },
      "comprehensive": { "budget": 8000 }
    }
  }
}
```

---

## Optimization Tips

1. **Start small**: Use `!context budget 2000` for simple tasks
2. **Be specific**: `!files src/auth/login.ts` beats `!files src/**`
3. **Use profiles**: Pre-defined profiles load faster
4. **Clear unused**: `!forget` files no longer needed
5. **Trust caching**: Don't re-request already-loaded files
