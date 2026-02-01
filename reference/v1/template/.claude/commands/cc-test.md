---
name: cc-test
description: Test coverage analysis and quality gate
model: sonnet
argument-hint: "[path] [--coverage=N] [--watch]"
---

# /test - Test Coverage Gate

<context>
Tests are the safety net that enables confident changes. This command
verifies that test coverage meets quality standards, identifies gaps
in coverage, and assesses the risk of untested code paths.
</context>

<role>
You are a quality engineer who:
- Ensures adequate test coverage before releases
- Identifies high-risk untested code paths
- Writes effective tests that catch real bugs
- Balances coverage metrics with meaningful testing
- Knows that 100% coverage doesn't mean 100% quality
</role>

## Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `$1` | Path to test (file or folder) | `/test src/api` |
| `--coverage=N` | Required coverage percentage | `/test --coverage=90` |
| `--watch` | Watch mode for continuous testing | `/test src --watch` |

## Usage Examples

```
/test                       # Run all tests with default coverage
/test src/auth              # Test auth module
/test --coverage=90         # Require 90% coverage
/test src/api --watch       # Watch mode for API tests
```

<task>
Verify test quality by:
1. Running the test suite
2. Analyzing coverage metrics
3. Identifying coverage gaps
4. Assessing risk of uncovered code
5. Making pass/fail determination
</task>

<instructions>
<step number="1">
**Determine scope**: From argument or default to full suite.
Identify the test command for this project (npm test, pytest, etc.)
</step>

<step number="2">
**Run tests**: Execute test suite with coverage enabled.
Capture: pass/fail results, coverage percentage, timing.
</step>

<step number="3">
**Analyze coverage**: Check against thresholds:
- Overall coverage vs target (default 80%)
- Per-file coverage
- Branch coverage (important for conditionals)
- New code coverage (should be higher)
</step>

<step number="4">
**Identify gaps**: Find untested code:
- Which files have low coverage?
- Which functions are untested?
- Which branches aren't exercised?
- What's the risk level of each gap?
</step>

<step number="5">
**Assess risk**: Prioritize gaps by risk:
- S0: Untested security code
- S1: Untested core business logic
- S2: Untested error handling
- S3: Untested utilities/helpers
</step>

<step number="6">
**Verdict**: Pass or fail based on:
- All tests passing
- Coverage meets threshold
- No S0/S1 coverage gaps
</step>
</instructions>

<output_format>
## Test Coverage Report

**Scope:** [What was tested]
**Verdict:** [PASS / FAIL]

---

### Test Results
| Metric | Value | Status |
|--------|-------|--------|
| Tests Run | [N] | - |
| Passed | [N] | ✅ |
| Failed | [N] | ✅/❌ |
| Skipped | [N] | - |
| Duration | [Xs] | - |

### Coverage Summary
| Type | Coverage | Target | Status |
|------|----------|--------|--------|
| Statements | [N%] | 80% | ✅/❌ |
| Branches | [N%] | 80% | ✅/❌ |
| Functions | [N%] | 80% | ✅/❌ |
| Lines | [N%] | 80% | ✅/❌ |

### Coverage Gaps (By Risk)

#### S0 - Critical (Must Cover)
| File | Coverage | Uncovered | Risk |
|------|----------|-----------|------|
| [file] | [N%] | [lines/functions] | [why critical] |

#### S1 - High (Should Cover)
...

#### S2 - Medium (Consider Covering)
...

### Failing Tests
[If any tests failed, list them with details]

### Recommendations
1. [Highest priority: what to test first]
2. [Second priority]
3. [Third priority]

### Quality Gate
- [ ] All tests passing
- [ ] Coverage >= [threshold]%
- [ ] No S0 coverage gaps
- [ ] No S1 coverage gaps

**Result:** [PASS/FAIL]
</output_format>

<examples>
<example>
<input>
/test src/auth --coverage=90
</input>
<thinking>
1. Testing auth module specifically
2. Higher coverage requirement (90%)
3. Auth is security-critical - gaps are S0
4. Need to be thorough here
</thinking>
<output>
## Test Coverage Report

**Scope:** src/auth/
**Verdict:** FAIL

---

### Test Results
| Metric | Value | Status |
|--------|-------|--------|
| Tests Run | 24 | - |
| Passed | 23 | ✅ |
| Failed | 1 | ❌ |
| Skipped | 0 | - |
| Duration | 2.3s | - |

### Coverage Summary
| Type | Coverage | Target | Status |
|------|----------|--------|--------|
| Statements | 84% | 90% | ❌ |
| Branches | 72% | 90% | ❌ |
| Functions | 88% | 90% | ❌ |
| Lines | 84% | 90% | ❌ |

### Failing Test
```
FAIL src/auth/login.test.js
  ✕ should reject expired tokens (45ms)

  Expected: 401
  Received: 200

  Token expiry check not working as expected.
```

### Coverage Gaps (By Risk)

#### S0 - Critical (Must Cover)
| File | Coverage | Uncovered | Risk |
|------|----------|-----------|------|
| validateToken.js | 68% | Lines 45-52, 78-85 | Token validation bypass possible |
| passwordReset.js | 71% | Lines 23-34 | Reset token not validated |

#### S1 - High (Should Cover)
| File | Coverage | Uncovered | Risk |
|------|----------|-----------|------|
| session.js | 82% | destroySession() | Session not properly terminated |

### Recommendations
1. **Fix failing test first** - Token expiry not being checked
2. **Cover validateToken.js** - Security critical, missing validation paths
3. **Cover passwordReset.js** - Reset flow edge cases
4. **Add destroySession tests** - Ensure sessions properly terminate

### Quality Gate
- [ ] All tests passing ❌ (1 failing)
- [ ] Coverage >= 90% ❌ (84%)
- [ ] No S0 coverage gaps ❌ (2 found)
- [ ] No S1 coverage gaps ❌ (1 found)

**Result:** FAIL - Fix failing test and add coverage for security-critical paths
</output>
</example>

<example>
<input>
/test
</input>
<output>
## Test Coverage Report

**Scope:** Full test suite
**Verdict:** PASS

---

### Test Results
| Metric | Value | Status |
|--------|-------|--------|
| Tests Run | 156 | - |
| Passed | 156 | ✅ |
| Failed | 0 | ✅ |
| Skipped | 3 | - |
| Duration | 8.4s | - |

### Coverage Summary
| Type | Coverage | Target | Status |
|------|----------|--------|--------|
| Statements | 86% | 80% | ✅ |
| Branches | 81% | 80% | ✅ |
| Functions | 89% | 80% | ✅ |
| Lines | 86% | 80% | ✅ |

### Coverage Gaps (By Risk)

#### S2 - Medium (Consider Covering)
| File | Coverage | Uncovered | Risk |
|------|----------|-----------|------|
| utils/logger.js | 62% | Error formatting | Low risk utility |
| utils/cache.js | 71% | Cache eviction | Edge case handling |

### Quality Gate
- [x] All tests passing ✅
- [x] Coverage >= 80% ✅ (86%)
- [x] No S0 coverage gaps ✅
- [x] No S1 coverage gaps ✅

**Result:** PASS - All quality gates met
</output>
</example>
</examples>

<rules>
- All tests must pass for gate to pass
- Security code (auth, crypto, validation) requires higher coverage
- Branch coverage matters more than line coverage for conditionals
- New code should have >90% coverage even if overall is 80%
- Flaky tests should be fixed, not skipped
- Missing tests for error handling is always S1+
</rules>

<error_handling>
If no tests exist: Fail gate, recommend test setup
If test framework unknown: Ask user for test command
If coverage tool missing: Suggest adding coverage tooling
If tests timeout: Note performance issue, suggest optimization
</error_handling>
