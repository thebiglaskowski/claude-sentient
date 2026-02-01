# Phase 5: Verify

> **Purpose:** Run full test suite and comprehensive checks
> **Duration:** 1-5 minutes
> **Triggers:** After execute phase or before checkpoint

---

## Overview

The verify phase runs comprehensive tests and checks to ensure the changes work correctly. Unlike the incremental checks in execute, this runs the full suite.

---

## Process

### 1. Run Full Test Suite

```
USING profile.commands.run_tests:
  RUN complete test suite
  CAPTURE:
    - Pass/fail status
    - Coverage percentage
    - Failed test details
    - Timing information
```

### 2. Run Type Checking

```
USING profile.tools.type_check:
  RUN full type check
  CAPTURE:
    - Error count
    - Error locations
    - Warning count (if applicable)
```

### 3. Run Linting

```
USING profile.tools.lint:
  RUN full lint check
  CAPTURE:
    - Error count
    - Warning count
    - Auto-fixable issues
```

### 4. Browser Verification (If UI)

```
IF project has UI components:
  - Take screenshots of affected pages
  - Check for console errors
  - Verify responsive layouts
  - Run accessibility quick check
```

### 5. Compile Verification Report

```
REPORT:
  tests:
    passed: 142
    failed: 0
    skipped: 3
    coverage: 87%

  types:
    errors: 0

  lint:
    errors: 0
    warnings: 2

  status: PASS | FAIL
```

---

## Pass Criteria

```
PASS IF:
  - All tests pass (or failures are pre-existing)
  - Type check has 0 errors
  - Lint has 0 errors (warnings OK)
  - Coverage >= threshold (from profile)

FAIL IF:
  - Any new test failures
  - New type errors introduced
  - New lint errors introduced
  - Coverage dropped below threshold
```

---

## Failure Handling

```
IF verification fails:
  1. Identify which check failed
  2. Return to execute phase
  3. Fix the issues
  4. Return to verify phase
  5. Repeat until pass (max 3 iterations)

IF still failing after 3 iterations:
  - Log the issue
  - Ask for user guidance
  - Option to continue anyway (for non-blocking issues)
```

---

## Outputs

| Output | Description |
|--------|-------------|
| `verification_status` | PASS or FAIL |
| `test_results` | Detailed test output |
| `coverage` | Coverage percentage |
| `issues_found` | List of problems |

---

## Skip Conditions

```
SKIP IF:
  - No code changes in this iteration
  - Only documentation changes

CANNOT SKIP IF:
  - Code was modified
  - Before checkpoint
```

---

## Example

```
[VERIFY] Running full verification...

Test Suite:
  Running pytest...
  ✓ 142 passed, 0 failed, 3 skipped
  Coverage: 87% (threshold: 80%)

Type Check:
  Running pyright...
  ✓ 0 errors

Lint:
  Running ruff...
  ✓ 0 errors, 2 warnings

Verification: PASS

Ready for quality gates.
```
