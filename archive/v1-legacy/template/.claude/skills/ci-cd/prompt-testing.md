---
name: prompt-testing
description: Validate that prompts and commands work correctly
context: fork
model: sonnet
---

# Prompt Testing

Validate that prompts and commands work correctly.

## Description

Framework for testing prompts to ensure they produce expected outputs and behaviors.
Triggers on: "test prompts", "validate prompts", "prompt quality", "QA prompts".

## Why Test Prompts

- Ensure prompts produce consistent outputs
- Catch regressions when prompts are updated
- Validate edge cases are handled
- Document expected behavior
- Build confidence in prompt quality

## Test Types

### 1. Smoke Tests
Basic "does it work" tests:
- Does the command load without error?
- Does it produce any output?
- Does it follow the basic structure?

### 2. Output Validation
Check output format:
- Required sections present?
- Correct markdown structure?
- Expected fields populated?

### 3. Behavioral Tests
Check logic and decisions:
- Correct model recommended?
- Right severity assigned?
- Appropriate actions suggested?

### 4. Edge Case Tests
Handle unusual inputs:
- Empty input
- Very large input
- Malformed input
- Missing context

## Test Specification Format

```yaml
# tests/commands/daily.test.yaml
name: "/daily command tests"
command: "/daily"

tests:
  - name: "produces status update"
    setup:
      files:
        - STATUS.md: "## Current: Working on feature X"
    input: "Continue working"
    expect:
      contains:
        - "STATUS.md"
        - "next steps"
      format: "markdown"

  - name: "handles missing STATUS.md"
    setup:
      files: []
    input: "Continue working"
    expect:
      contains:
        - "STATUS.md not found"
        - "create"

  - name: "uses sonnet model"
    input: "What model should I use?"
    expect:
      contains:
        - "Sonnet"
```

## Test Categories

### Command Tests
```markdown
## /daily Command Tests

### Test: Basic Usage
**Input:** "Continue working on the project"
**Expected:**
- [ ] Reads STATUS.md
- [ ] Identifies current task
- [ ] Provides next steps
- [ ] Uses Sonnet model

### Test: No STATUS.md
**Input:** "Continue working" (no STATUS.md present)
**Expected:**
- [ ] Notes missing STATUS.md
- [ ] Offers to create one
- [ ] Asks about current focus

### Test: Stale STATUS.md
**Input:** "Continue" (STATUS.md >7 days old)
**Expected:**
- [ ] Warns about stale status
- [ ] Suggests refresh
```

### Skill Tests
```markdown
## pre-commit Skill Tests

### Test: Triggers on "commit"
**Input:** "Let's commit these changes"
**Expected:**
- [ ] Skill activates
- [ ] Checklist displayed
- [ ] All items checked

### Test: Catches debug code
**Input:** (staged file with console.log)
**Expected:**
- [ ] Warns about debug code
- [ ] Lists locations
- [ ] Blocks commit recommendation
```

### Integration Tests
```markdown
## Workflow Integration Tests

### Test: Feature Development Flow
**Sequence:**
1. /plan - Create spec
2. /audit-blueprint - Validate
3. /daily - Implement
4. /test - Verify coverage
5. /review - Code review
6. /closeout - Complete

**Expected:**
- [ ] Each step produces valid output
- [ ] Output from one step usable in next
- [ ] Final state is complete feature
```

## Test Runner (Conceptual)

```bash
#!/bin/bash
# prompt-test.sh - Run prompt tests

TESTS_DIR="tests/prompts"
RESULTS=""

for test_file in $TESTS_DIR/*.test.md; do
  echo "Running: $test_file"

  # Parse test cases
  # Run each test
  # Check expectations
  # Record results

  RESULTS+="$test_file: PASS\n"
done

echo -e "\n=== Results ===\n$RESULTS"
```

## Manual Testing Checklist

When updating a prompt, manually verify:

### Before Changes
- [ ] Document current behavior
- [ ] Note any known issues
- [ ] Identify test cases to verify

### After Changes
- [ ] Run smoke test (basic usage)
- [ ] Run edge case tests
- [ ] Compare output to previous version
- [ ] Verify formatting unchanged
- [ ] Check no regressions

### Sign-off
- [ ] Works as expected
- [ ] No new issues introduced
- [ ] Documentation updated if behavior changed

## Test Evidence Format

```markdown
## Test Run: /review command
**Date:** 2024-01-15
**Version:** v1.2.0
**Tester:** Claude

### Test Cases

| # | Test | Input | Expected | Actual | Pass |
|---|------|-------|----------|--------|------|
| 1 | Basic review | PR diff | Findings list | Findings list | ✅ |
| 2 | No issues | Clean code | "No issues" | "No issues" | ✅ |
| 3 | Security issue | SQL injection | S0 finding | S0 finding | ✅ |
| 4 | Empty diff | (empty) | Graceful handling | Helpful message | ✅ |

### Summary
**Passed:** 4/4
**Status:** Ready for release
```

## Regression Testing

When prompts library is updated:

1. **Identify changed prompts**
   ```bash
   git diff --name-only HEAD~1 | grep -E "\.(md)$"
   ```

2. **Run tests for changed prompts**
   ```bash
   # Test each changed prompt
   ```

3. **Run integration tests**
   ```bash
   # Verify workflows still work
   ```

4. **Document results**
   ```markdown
   ## Regression Test: v1.2.0 → v1.3.0

   Changed: /review, /test, pre-commit skill

   Results:
   - /review: ✅ All tests pass
   - /test: ✅ All tests pass
   - pre-commit: ✅ All tests pass
   - Integration: ✅ Feature workflow works
   ```

## Quality Metrics

Track over time:
- Test coverage (prompts with tests / total prompts)
- Pass rate (passing tests / total tests)
- Regression rate (tests that broke after updates)
- Time to fix (how long regressions take to fix)

## Continuous Improvement

After each significant usage:
1. Note any unexpected behavior
2. Add test case for that scenario
3. Fix prompt if needed
4. Verify fix with new test
