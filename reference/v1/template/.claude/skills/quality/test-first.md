---
name: test-first
description: Write tests before implementation guidance
model: sonnet
---

# Test-First Development

Write tests before implementation.

## Description

Use when implementing features, fixing bugs, or modifying behavior.
Triggers on: "implement", "add feature", "fix bug", "write code", "build", "create function".

## Trigger

Activates when:
- Implementing new functionality
- Fixing bugs
- Modifying existing behavior
- User asks to "add", "create", "build", or "implement" something

## Core Process

```
1. Write failing test → 2. Implement minimally → 3. Refactor while green
```

## For Bug Fixes

1. **Reproduce first:** Write a test that fails (proves the bug exists)
2. **Fix the bug:** Make the test pass
3. **Verify:** Run full test suite
4. **Commit together:** Test and fix in same commit

## For New Features

1. **Happy path test:** Write test for basic success case
2. **Implement:** Make it pass with minimal code
3. **Edge cases:** Add tests for boundaries, errors, empty states
4. **Handle edges:** Implement edge case handling
5. **Refactor:** Clean up while tests are green

## Test Structure

```typescript
describe('featureName', () => {
  it('should [expected behavior] when [condition]', () => {
    // Arrange
    const input = ...

    // Act
    const result = featureName(input)

    // Assert
    expect(result).toBe(expected)
  })
})
```

## When to Skip

- **Spike/exploration:** Throwaway code (but note: promote to real code = add tests)
- **Pure refactoring:** Existing tests cover behavior (run them frequently)
- **Config changes:** No behavior change

## Red Flags

If you can't write a test:
- Requirement is unclear → Ask for clarification
- Code is untestable → Refactor for testability first
- Too complex → Break into smaller pieces

## Reminder

Tests are documentation that verifies itself. Write them first.
