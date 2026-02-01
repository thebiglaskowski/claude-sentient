---
name: subagent-research
description: Spawn isolated research agents to explore without polluting main context
argument-hint: "<research topic>"
context: fork
model: sonnet
---

# Subagent Research

Spawn isolated research agents that explore without polluting the main conversation context.

## Overview

When you need to explore a complex topic, search through many files, or investigate multiple approaches, spawning a subagent keeps your main context clean. The subagent:

- Has its own isolated context
- Can read files and explore extensively
- Returns only a summary to the main conversation
- Doesn't add exploration noise to your context

---

## When to Use

### Good Use Cases

1. **Exploring unfamiliar codebases**
   - "Research how authentication works in this project"
   - Large-scale file searches

2. **Comparing approaches**
   - "Investigate 3 ways to implement caching"
   - Each approach explored separately

3. **Deep documentation analysis**
   - "Find all API endpoints and their usage"
   - Extensive file reading

4. **Security analysis**
   - "Scan for potential vulnerabilities"
   - Thorough but context-heavy

5. **Dependency analysis**
   - "Understand what depends on this module"
   - Graph traversal through imports

### When NOT to Use

- Simple file lookups (just read the file)
- Tasks requiring immediate code changes
- When you need iterative feedback
- Quick questions with known locations

---

## Usage

### Spawn Research Agent

```
Research in background: How does the payment processing work?
```

or

```
Fork investigation: What testing patterns does this codebase use?
```

### With Specific Focus

```
Spawn agent to find all usages of UserService and summarize patterns
```

### Multiple Parallel Agents

```
In parallel, research:
1. Authentication flow
2. Database schema
3. API structure
```

---

## How It Works

### 1. Context Isolation

Main conversation:
```
[Message 1] User request
[Message 2] Claude spawns subagent
[Message 3] Subagent returns summary
[Message 4] Conversation continues (clean context)
```

Subagent context:
```
[M1] Research task
[M2] Read file A (500 lines)
[M3] Read file B (800 lines)
[M4] Read file C (400 lines)
[M5] Analyze patterns
[M6] Generate summary
→ Return summary only
```

### 2. Information Flow

```
Main Context           Subagent Context
     │                      │
     │─── Task ────────────>│
     │                      │ (extensive exploration)
     │                      │ (file reading)
     │                      │ (analysis)
     │<── Summary ──────────│
     │                      │
     ▼                      X (discarded)
(continues clean)
```

### 3. Summary Format

Subagent returns structured summary:

```markdown
## Research Summary: [Topic]

### Key Findings
- Finding 1
- Finding 2
- Finding 3

### Relevant Files
- `path/to/file1.ts` - Description
- `path/to/file2.ts` - Description

### Patterns Discovered
[Brief description of patterns]

### Recommendations
[Based on findings]

### Further Investigation
[If more research needed]
```

---

## Configuration

### Subagent Settings

```yaml
subagent:
  model: "sonnet"           # Model for research
  max_files: 50             # Max files to read
  max_tokens: 10000         # Max exploration tokens
  timeout: 300              # Timeout in seconds
  summary_length: 500       # Max summary length
```

### Model Selection

| Task Type | Recommended Model |
|-----------|-------------------|
| File search | haiku |
| Code analysis | sonnet |
| Security review | opus |
| Pattern discovery | sonnet |
| Architecture analysis | opus |

---

## Examples

### Example 1: Code Pattern Research

**Request:**
```
Research in background: How does error handling work across this codebase?
```

**Subagent explores:**
- Searches for try/catch patterns
- Reads error handling utilities
- Analyzes error middleware
- Checks test error cases

**Returns:**
```markdown
## Research Summary: Error Handling Patterns

### Key Findings
- Custom `AppError` class in `src/utils/errors.ts`
- Express middleware at `src/middleware/errorHandler.ts`
- Consistent use of error codes (E001, E002, etc.)

### Relevant Files
- `src/utils/errors.ts` - Error class definitions
- `src/middleware/errorHandler.ts` - Global handler
- `src/types/errors.ts` - Error type definitions

### Patterns Discovered
1. All errors extend `AppError`
2. Errors have `code`, `message`, `statusCode`
3. Validation errors use `ValidationError` subclass

### Recommendations
- Follow existing pattern for new errors
- Use error codes from `ERROR_CODES` enum
```

### Example 2: Dependency Analysis

**Request:**
```
Fork investigation: What would break if we refactored UserService?
```

**Subagent explores:**
- Finds all imports of UserService
- Traces call chains
- Identifies tight couplings
- Checks test coverage

**Returns:**
```markdown
## Research Summary: UserService Dependencies

### Direct Dependents (15 files)
- Controllers: 5 files
- Other services: 4 files
- Tests: 6 files

### Impact Analysis
- High impact: Authentication flow
- Medium impact: Profile management
- Low impact: Admin utilities

### Safe Refactoring Path
1. Extract interface first
2. Update controllers to use interface
3. Refactor implementation
4. Update tests

### Risk Areas
- `src/auth/login.ts` - Direct property access
- `src/admin/users.ts` - Assumes sync methods
```

---

## Best Practices

### Do

- Give clear, specific research goals
- Request structured summaries
- Specify what information you need
- Use for exploration, not implementation

### Don't

- Use for simple lookups
- Request code changes from subagent
- Spawn too many parallel agents
- Expect real-time interaction

---

## Integration

### With Commands

Some commands automatically use subagents:

- `/assess` - Spawns multiple analysis agents
- `/secure --deep` - Spawns security research agent
- `/map-project` - Spawns exploration agent

### With Extended Thinking

For complex analysis, combine:

```
Research with ultrathink: Analyze the architectural patterns
```

This gives the subagent extended thinking for deeper analysis.
