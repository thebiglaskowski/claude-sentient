# Phase 6: Quality

> **Purpose:** Run quality gates and enforce standards
> **Duration:** 2-5 minutes
> **Triggers:** After verify phase

---

## Overview

The quality phase runs all quality gates. Blocking gates must pass; advisory gates report but don't block. If gates fail, the system attempts auto-fix before returning to execute.

---

## Gates

### Blocking Gates (Must Pass)

| Gate | Check | Threshold |
|------|-------|-----------|
| **LINT** | Zero lint errors | 0 errors |
| **TYPE** | Type checking passes | 0 errors |
| **TEST** | Tests pass, coverage met | >= profile threshold |
| **SECURITY** | No high/critical vulns | 0 high/critical |
| **BUILD** | Project builds | Exit code 0 |
| **GIT** | Clean git state | No uncommitted changes |
| **QUEUE** | No S0/S1 items left | 0 pending S0/S1 |
| **DOD** | Definition of done | All criteria met |

### Advisory Gates (Report Only)

| Gate | Check | Notes |
|------|-------|-------|
| **DOCS** | Documentation present | Warn if missing |
| **PERF** | No perf regressions | Warn if detected |
| **A11Y** | Accessibility check | Warn if issues |
| **MODERN** | No deprecated APIs | Warn if found |

---

## Process

### 1. Run Blocking Gates

```
FOR gate IN blocking_gates:
  result = RUN gate.check

  IF result.failed:
    ATTEMPT auto_fix (if available)
    result = RUN gate.check again

  IF still failed:
    RECORD failure
    SET gate.status = "failed"
  ELSE:
    SET gate.status = "passed"
```

### 2. Run Advisory Gates

```
FOR gate IN advisory_gates:
  result = RUN gate.check

  IF result.failed:
    LOG warning
    SET gate.status = "warning"
  ELSE:
    SET gate.status = "passed"

# Advisory failures don't block progress
```

### 3. Evaluate Results

```
IF any blocking_gate.status == "failed":
  SET quality_status = "FAILED"
  RETURN to execute phase with issues

ELSE:
  SET quality_status = "PASSED"
  PROCEED to commit phase
```

---

## Auto-Fix Capabilities

| Gate | Auto-Fix Available |
|------|-------------------|
| LINT | Yes - `ruff --fix`, `eslint --fix` |
| TYPE | No - requires code changes |
| TEST | No - requires investigation |
| SECURITY | Partial - can update deps |
| BUILD | No - requires investigation |
| GIT | Yes - `git add` for expected changes |

---

## Definition of Done (DOD)

The DOD gate checks:
```
CRITERIA:
  - All work queue items complete
  - No failing tests
  - Coverage threshold met
  - Documentation updated (if applicable)
  - Changelog entry (if applicable)
  - No S0/S1 known issues
```

---

## Outputs

| Output | Description |
|--------|-------------|
| `gates_passed` | Count of passed gates |
| `gates_failed` | Count of failed gates |
| `gate_details` | Per-gate results |
| `quality_status` | PASSED or FAILED |
| `advisory_warnings` | Non-blocking issues |

---

## Failure Recovery

```
IF quality failed:
  1. Identify failing gates
  2. Attempt auto-fix
  3. If still failing, create fix tasks
  4. Add to work queue as S0/S1
  5. Return to execute phase

MAX retries: 3 per gate
AFTER max retries: Ask user for guidance
```

---

## Example

```
[QUALITY] Running quality gates...

Blocking Gates:
  ✓ LINT      0 errors
  ✓ TYPE      0 errors
  ✓ TEST      87% coverage (>80%)
  ✓ SECURITY  No vulnerabilities
  ✓ BUILD     Success
  ✓ GIT       Clean
  ✓ QUEUE     0 S0/S1 items
  ✓ DOD       All criteria met

Advisory Gates:
  ✓ DOCS      Present
  ⚠ PERF      No baseline (skipped)
  ✓ A11Y      No issues
  ✓ MODERN    No deprecated APIs

Quality: PASSED (8/8 blocking, 3/4 advisory)

Ready for checkpoint.
```
