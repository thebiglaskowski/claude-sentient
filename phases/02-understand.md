# Phase 2: Understand

> **Purpose:** Classify the request and assess current state
> **Duration:** 1-3 minutes
> **Triggers:** After init phase

---

## Overview

The understand phase analyzes what's being asked and the current state of the codebase. It determines the type of work, complexity, and what needs to be done.

---

## Process

### 1. Classify Request Type

```
ANALYZE request for:
  - Action type: implement, fix, refactor, review, research
  - Scope: single file, module, codebase-wide
  - Complexity: simple, moderate, complex

CLASSIFICATION MATRIX:
  | Request Pattern          | Type       | Complexity |
  |--------------------------|------------|------------|
  | "add X to Y"             | implement  | varies     |
  | "fix bug in X"           | fix        | moderate   |
  | "refactor X"             | refactor   | complex    |
  | "review X"               | review     | simple     |
  | "why does X"             | research   | simple     |
  | "build entire X"         | implement  | complex    |
```

### 2. Assess Current State

```
SCAN codebase:
  - Existing files and structure
  - Test coverage status
  - Lint/type check status
  - Recent changes (git log)

IDENTIFY:
  - What exists
  - What's missing
  - What's broken
```

### 3. Identify Dependencies

```
FOR the requested work:
  - What files will be touched?
  - What depends on those files?
  - What tests cover this area?
  - Are there related open issues?
```

### 4. Check for Blockers

```
BLOCKERS:
  - Missing dependencies
  - Failing tests in affected area
  - Uncommitted changes
  - Unclear requirements

IF blockers found:
  ADD to work queue as prerequisites
```

### 5. Determine Approach

```
BASED ON classification and state:
  - Use subagents? (complex tasks)
  - Need specialist agent? (security, performance)
  - Sequential or parallel execution?
  - Estimated work items
```

---

## Outputs

| Output | Description |
|--------|-------------|
| `type` | Request classification |
| `complexity` | simple/moderate/complex |
| `scope` | Files and modules affected |
| `blockers` | Prerequisites to address |
| `approach` | Execution strategy |

---

## Clarification Triggers

Ask user for clarification when:
- Multiple valid interpretations exist
- Security-sensitive changes implied
- Breaking changes would be required
- Scope is ambiguous

```
IF ambiguous:
  ASK ONE clarifying question
  WAIT for response
  CONTINUE
```

---

## Skip Conditions

```
SKIP IF:
  - Continuing previous loop (state.phase > 2)
  - Simple continuation command

CANNOT SKIP IF:
  - New task request
  - Significant time since last session
```

---

## Example

```
[UNDERSTAND] Analyzing request: "Add user authentication"

Classification:
  Type: implement
  Complexity: complex
  Scope: auth module, user model, routes

Current State:
  - No auth system exists
  - User model present but minimal
  - 85% test coverage

Approach:
  - Use security-analyst agent for review
  - 5 work items identified
  - Sequential execution (dependencies)

Ready for planning.
```
