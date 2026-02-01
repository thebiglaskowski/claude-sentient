# Quality Gates Reference (v3.0)

Complete documentation of all quality gates in the autonomous loop.
**STRICT MODE**: All gates are BLOCKING. Loop cannot exit until every gate passes.

---

## Quality Gates Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     QUALITY GATES (ALL BLOCKING)                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  CODE QUALITY GATES (1-11):                                                  │
│  ┌───────────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌─────────────┐              │
│  │PRE-FLIGHT │→│ LINT │→│ TYPE │→│ UNIT │→│ INTEGRATION │              │
│  └───────────┘  └──────┘  └──────┘  └──────┘  └─────────────┘              │
│                                         │                                    │
│                                         ▼                                    │
│  ┌──────────┐  ┌───────────┐  ┌─────────┐  ┌───────┐  ┌──────┐  ┌────────┐│
│  │ SECURITY │→│PERFORMANCE│→│ BROWSER │→│ A11Y  │→│ DOCS │→│ MODERN ││
│  └──────────┘  └───────────┘  └─────────┘  └───────┘  └──────┘  └────────┘│
│                                                                              │
│  WORK COMPLETION GATES (12-15):                                              │
│  ┌────────────┐  ┌──────────────┐  ┌───────────┐  ┌─────┐                  │
│  │ WORK QUEUE │→│ KNOWN ISSUES │→│ GIT STATE │→│ DoD │                  │
│  └────────────┘  └──────────────┘  └───────────┘  └─────┘                  │
│                                                                              │
│  ALL GATES MUST PASS. NO EXCEPTIONS. NO WARNINGS.                           │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Gate 1: PRE-FLIGHT

### Purpose
Verify environment is ready for work.

### Checks

| Check | Pass Criteria | Fail Action |
|-------|---------------|-------------|
| Git clean | No uncommitted changes | Stash or commit |
| Dependencies | All installed | Run install |
| Environment | Required vars set | Prompt for config |
| Tools | Required tools present | Install or skip |

### Commands

```bash
# Git status
git status --porcelain

# Dependencies (Node.js)
npm ci

# Dependencies (Python)
pip install -r requirements.txt

# Environment check
[[ -f .env ]] && source .env
```

### Output

```
Gate 1: PRE-FLIGHT
  ✓ Git working tree clean
  ✓ Dependencies installed (node_modules)
  ✓ Environment variables loaded
  ✓ Required tools present (eslint, tsc, jest)
  PASS
```

### Failure Handling

```
If uncommitted changes:
  → Offer to stash
  → Or prompt user to commit

If dependencies missing:
  → Auto-run npm ci / pip install
  → Re-check after install

If env vars missing:
  → List required vars
  → Prompt user to set
```

---

## Gate 2: LINT

### Purpose
Enforce code style and catch common issues.

### Checks

| Tool | Languages | Config |
|------|-----------|--------|
| ESLint | JS/TS | .eslintrc |
| Prettier | All | .prettierrc |
| Pylint/Ruff | Python | pyproject.toml |
| Rubocop | Ruby | .rubocop.yml |

### Commands

```bash
# JavaScript/TypeScript
npx eslint src/ --max-warnings=0

# Python
ruff check .
# or
pylint src/

# Auto-fix (if enabled)
npx eslint src/ --fix
npx prettier --write .
```

### Pass Criteria

```
- 0 errors
- 0 warnings (configurable)
- All fixable issues auto-fixed
```

### Output

```
Gate 2: LINT
  Running ESLint...
  ✓ src/auth/login.ts - clean
  ✓ src/auth/logout.ts - clean
  ⚠ src/utils/helpers.ts - 1 warning (unused variable)

  Errors: 0
  Warnings: 1
  PASS (warnings allowed)
```

### Failure Handling

```
If auto-fixable errors:
  → Apply fixes
  → Re-run lint
  → Continue if clean

If non-fixable errors:
  → Add to work queue as S0
  → List specific issues
  → BLOCK - loop cannot exit until resolved
```

---

## Gate 3: TYPE

### Purpose
Verify type safety and catch type errors.

### Checks

| Tool | Languages | Config |
|------|-----------|--------|
| TypeScript | TS | tsconfig.json |
| mypy | Python | mypy.ini |
| Flow | JS | .flowconfig |

### Commands

```bash
# TypeScript
npx tsc --noEmit

# Python
mypy src/

# Strict mode (recommended)
npx tsc --noEmit --strict
```

### Pass Criteria

```
- 0 type errors
- No implicit any (if strict)
- All types resolve
```

### Output

```
Gate 3: TYPE
  Running TypeScript compiler...
  ✓ 127 files checked
  ✓ 0 errors
  PASS
```

### Failure Handling

```
If type errors:
  → List all errors with locations
  → Add to work queue as S0
  → Group related errors
  → BLOCK - loop cannot exit until 0 type errors

Common fixes added to queue:
  - Missing type annotations
  - Incorrect return types
  - Null/undefined handling
```

---

## Gate 4: UNIT TEST

### Purpose
Verify unit test suite passes with adequate coverage.

### Checks

| Metric | Threshold | Target |
|--------|-----------|--------|
| Tests passing | 100% | Required |
| Line coverage | 80% | Required |
| Branch coverage | 70% | Recommended |
| New code coverage | 90% | Required |

### Commands

```bash
# JavaScript/TypeScript (Jest)
npm test -- --coverage --watchAll=false

# Python (pytest)
pytest --cov=src --cov-report=term-missing

# With coverage threshold
npm test -- --coverage --coverageThreshold='{"global":{"lines":80}}'
```

### Pass Criteria

```
- All tests pass
- Coverage >= threshold
- No skipped tests (except documented)
- No flaky tests detected
```

### Output

```
Gate 4: UNIT TEST
  Running 127 tests...

  ✓ auth/login.test.ts (12 tests)
  ✓ auth/logout.test.ts (8 tests)
  ✓ utils/helpers.test.ts (24 tests)
  ...

  Tests:     127 passed, 0 failed
  Coverage:  88% lines, 82% branches

  PASS
```

### Failure Handling

```
If tests fail:
  → List failing tests with output
  → Add test fixes to queue as S0
  → BLOCK - loop cannot exit until fixed

If coverage low (< 80%):
  → List uncovered lines/functions
  → Add coverage tasks to queue as S1
  → BLOCK - loop cannot exit until coverage >= 80%
```

---

## Gate 5: INTEGRATION

### Purpose
Verify components work together correctly.

### Checks

| Type | Scope | Tools |
|------|-------|-------|
| API tests | Endpoints | Supertest, httpx |
| DB tests | Queries | Test containers |
| Service tests | Integrations | Mock servers |

### Commands

```bash
# API tests
npm run test:integration

# With test database
docker-compose -f docker-compose.test.yml up -d
npm run test:integration
docker-compose -f docker-compose.test.yml down

# Python
pytest tests/integration/
```

### Pass Criteria

```
- All integration tests pass
- External services mocked appropriately
- No test pollution (isolated)
```

### Output

```
Gate 5: INTEGRATION
  Starting test database...
  Running integration tests...

  ✓ API: /auth/login (3 tests)
  ✓ API: /auth/logout (2 tests)
  ✓ API: /users (8 tests)

  Tests: 13 passed
  PASS
```

### Failure Handling

```
If integration tests fail:
  → Check if infrastructure issue
  → If yes: Retry after fix
  → If test bug: Add to queue as S0
  → BLOCK - loop cannot exit until tests pass

If test environment unavailable:
  → Attempt to set up environment
  → If truly unavailable: Document in KNOWN_ISSUES.md
  → BLOCK unless environment is genuinely not applicable
```

---

## Gate 6: SECURITY

### Purpose
Identify security vulnerabilities.

### Checks

| Type | Tool | Severity |
|------|------|----------|
| Dependencies | npm audit / safety | S0-S2 |
| SAST | Semgrep / Bandit | S0-S2 |
| Secrets | Gitleaks / truffleHog | S0 |
| OWASP | Custom checks | S0-S1 |

### Commands

```bash
# Dependency audit
npm audit --audit-level=high
pip-audit

# Static analysis
semgrep --config auto .
bandit -r src/

# Secret scanning
gitleaks detect --source .
```

### Pass Criteria

```
- No S0 (critical) vulnerabilities
- No S1 (high) vulnerabilities
- No secrets in code
- Dependencies up to date (warning for outdated)
```

### Output

```
Gate 6: SECURITY
  Dependency audit...
  ✓ No critical vulnerabilities
  ⚠ 2 moderate vulnerabilities (S2)

  Static analysis...
  ✓ No hardcoded secrets
  ✓ No SQL injection patterns
  ✓ No XSS vulnerabilities

  S0: 0
  S1: 0
  S2: 2

  PASS (S2 tracked but not blocking)
```

### Failure Handling

```
If S0 found:
  → STOP immediately
  → Add fix to queue as S0
  → Alert user
  → BLOCK - loop cannot exit

If S1 found:
  → Add to queue as S0 (elevated priority)
  → BLOCK - loop cannot exit until resolved

If secrets detected:
  → Remove immediately
  → Rotate exposed credentials
  → Add to .gitignore
  → BLOCK - loop cannot exit until clean
```

---

## Gate 7: PERFORMANCE

### Purpose
Identify performance issues before deployment.

### Checks

| Type | Metric | Threshold |
|------|--------|-----------|
| Bundle size | KB | <250 KB |
| Load time | LCP | <2.5s |
| N+1 queries | Count | 0 |
| Memory leaks | Growth | None |

### Commands

```bash
# Bundle analysis
npx webpack-bundle-analyzer stats.json

# Lighthouse (web)
npx lighthouse http://localhost:3000 --output=json

# N+1 detection (Rails)
bundle exec bullet

# Memory profiling
node --inspect app.js
```

### Pass Criteria

```
- Bundle size within limits
- No N+1 queries
- Core Web Vitals in "Good" range
- No obvious memory leaks
```

### Output

```
Gate 7: PERFORMANCE
  Bundle analysis...
  ✓ Main bundle: 187 KB (limit: 250 KB)
  ✓ Vendor bundle: 89 KB

  Query analysis...
  ✓ No N+1 queries detected

  PASS
```

### Failure Handling

```
If bundle too large:
  → List largest dependencies
  → Suggest code splitting
  → Add optimization tasks as S1
  → BLOCK - loop cannot exit until within limits

If N+1 detected:
  → List queries with locations
  → Add fixes to queue as S1
  → BLOCK - loop cannot exit

If Core Web Vitals fail:
  → List specific metrics
  → Suggest optimizations
  → Add fixes to queue as S1
  → BLOCK - loop cannot exit until in "Good" range
```

---

## Gate 8: BROWSER (UI Only)

### Purpose
Verify visual correctness and responsiveness.

### Checks

| Type | Tool | Viewports |
|------|------|-----------|
| Screenshots | Playwright | 320, 768, 1280 |
| Visual diff | Percy | All |
| Responsive | Manual | All breakpoints |

### Commands

```bash
# Screenshot tests
npx playwright test --project=chromium

# Visual regression
npx percy snapshot ./snapshots

# Browser tests
npm run test:e2e
```

### Pass Criteria

```
- Screenshots match baseline (or approved diff)
- No layout breaks at any viewport
- Interactive elements work
```

### Output

```
Gate 8: BROWSER
  Screenshot capture...
  ✓ Homepage @ 320px
  ✓ Homepage @ 768px
  ✓ Homepage @ 1280px
  ✓ Login page @ all viewports
  ✓ Dashboard @ all viewports

  Visual diff: 0 changes

  PASS
```

### When to Skip

```
- Backend-only changes
- No UI modifications
- CI without display
```

---

## Gate 9: ACCESSIBILITY (A11Y)

### Purpose
Ensure accessibility compliance.

### Checks

| Standard | Level | Tool |
|----------|-------|------|
| WCAG 2.1 | AA | axe-core |
| Keyboard | Full | Manual |
| Screen reader | Compatible | NVDA/VoiceOver |

### Commands

```bash
# Automated a11y testing
npx axe-core-cli http://localhost:3000

# In tests
import { axe } from 'jest-axe';
expect(await axe(container)).toHaveNoViolations();
```

### Pass Criteria

```
- No critical a11y violations
- Color contrast >= 4.5:1
- All interactive elements keyboard accessible
- ARIA labels present where needed
```

### Output

```
Gate 9: ACCESSIBILITY
  Running axe-core audit...

  ✓ Color contrast: Pass
  ✓ ARIA labels: Pass
  ✓ Keyboard navigation: Pass
  ⚠ Image alt text: 1 warning

  Critical: 0
  Serious: 0
  Moderate: 1

  PASS
```

### When to Skip

```
- CLI tools only
- Backend services
- Non-user-facing code
```

---

## Gate 10: DOCUMENTATION

### Purpose
Verify documentation is complete and current.

### Checks

| Item | Required | File |
|------|----------|------|
| README | Yes | README.md |
| CHANGELOG | For releases | CHANGELOG.md |
| API docs | For public APIs | docs/api/ |
| Comments | For complex logic | In code |

### Commands

```bash
# Check files exist
[[ -f README.md ]] && echo "✓ README"
[[ -f CHANGELOG.md ]] && echo "✓ CHANGELOG"

# Generate API docs
npm run docs:generate

# Check for TODO/FIXME
grep -r "TODO\|FIXME" src/
```

### Pass Criteria

```
- README exists and is current
- CHANGELOG updated for changes
- API docs generated (if applicable)
- No stale documentation
```

### Output

```
Gate 10: DOCUMENTATION
  ✓ README.md present and recent
  ✓ CHANGELOG.md updated
  ✓ API docs generated
  ⚠ 3 TODO comments in code

  PASS
```

### Failure Handling

```
If CHANGELOG missing:
  → Generate entry from commits
  → Add to queue as S1
  → BLOCK - loop cannot exit without CHANGELOG

If README outdated:
  → Flag sections needing update
  → Add to queue as S1
  → BLOCK - loop cannot exit without updated docs
```

---

## Gate 11: MODERN TECH

### Purpose
Ensure modern patterns and no deprecated APIs.

### Checks

| Type | Check | Action |
|------|-------|--------|
| Deprecated APIs | Library warnings | Update code |
| Old patterns | Linter rules | Refactor |
| Outdated deps | Version check | Update |

### Commands

```bash
# Check for deprecation warnings
npm outdated
npm run build 2>&1 | grep -i deprecat

# Python
pip list --outdated
python -W all app.py 2>&1 | grep -i deprecat
```

### Pass Criteria

```
- No deprecated API usage
- Dependencies within 2 major versions
- Modern patterns used
```

### Output

```
Gate 11: MODERN TECH
  Checking for deprecations...
  ✓ No deprecated APIs in use
  ✓ All dependencies within support window

  Outdated but not deprecated:
  - lodash: 4.17.0 → 4.18.0 (minor)

  PASS
```

### Failure Handling

```
If deprecated APIs found:
  → List usage locations
  → Provide migration path
  → Add to queue as S1
  → BLOCK - loop cannot exit with deprecated APIs

If dependencies very outdated:
  → Check for security updates
  → Add upgrade to queue as S1
  → BLOCK if security-related updates pending
```

---

## Gate 12: WORK QUEUE (NEW)

### Purpose
Verify all planned work is complete.

### Checks

| Check | Threshold | Source |
|-------|-----------|--------|
| Pending tasks | 0 | LOOP_STATE.md |
| In-progress tasks | 0 | LOOP_STATE.md |
| Blocked tasks | 0 | LOOP_STATE.md |
| TODO markers | 0 | STATUS.md |

### Pass Criteria

```
- Work queue is completely empty
- No pending tasks
- No in-progress tasks
- No blocked tasks
```

### Failure Handling

```
If pending work exists:
  → List all pending items
  → Add to active queue
  → BLOCK - loop cannot exit

If tasks blocked:
  → Identify blockers
  → Add blocker resolution to queue
  → BLOCK - loop cannot exit
```

---

## Gate 13: KNOWN ISSUES

### Purpose
Verify no critical/high issues remain unresolved.

### Checks

| Severity | Threshold | Action |
|----------|-----------|--------|
| S0 (Critical) | 0 unresolved | BLOCKING |
| S1 (High) | 0 unresolved | BLOCKING |
| S2 (Medium) | Tracked | Non-blocking |
| S3 (Low) | Tracked | Non-blocking |

### Pass Criteria

```
- Zero S0 issues unresolved
- Zero S1 issues unresolved
- S2/S3 may exist but must be documented
```

### Failure Handling

```
If S0/S1 unresolved:
  → List all critical/high issues
  → Add fixes to queue as top priority
  → BLOCK - loop cannot exit until resolved
```

---

## Gate 14: GIT STATE

### Purpose
Verify all work is committed and tracked.

### Checks

| Check | Threshold | Verification |
|-------|-----------|--------------|
| Uncommitted changes | 0 | git status |
| Staged but not committed | 0 | git status |

### Pass Criteria

```
- All changes committed
- Working tree clean
- No staged changes pending
```

### Failure Handling

```
If uncommitted changes:
  → List modified files
  → Prompt to commit or explain
  → BLOCK - loop cannot exit with uncommitted work
```

---

## Gate 15: DEFINITION OF DONE (DoD)

### Purpose
Final comprehensive checklist before completion.

### Checks (by Work Type)

#### Feature

```
- [ ] Code complete and working
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] No S0/S1 issues
- [ ] Reviewed by peer (if required)
- [ ] CHANGELOG entry added
```

#### Bug Fix

```
- [ ] Bug fixed and verified
- [ ] Regression test added
- [ ] Root cause documented
- [ ] No new issues introduced
```

#### Refactor

```
- [ ] Behavior unchanged (tests prove)
- [ ] Code cleaner/simpler
- [ ] No performance regression
- [ ] Documentation updated if needed
```

### Commands

```bash
# dod-verifier.py runs checklist
python .claude/hooks/dod-verifier.py
```

### Output

```
Gate 12: DEFINITION OF DONE

Work Type: Feature
Checklist:
  ✓ Code Quality: Lint and type check pass
  ✓ Testing: 92% coverage, all tests pass
  ✓ Security: No S0/S1 vulnerabilities
  ✓ Documentation: README, CHANGELOG updated
  ✓ Git: Atomic commits, clear messages
  ✓ Verification: Two consecutive passes

PASS - All criteria met
```

---

## Gate Execution Order

### Mandatory Sequence

```
PRE-FLIGHT → LINT → TYPE → UNIT TEST → SECURITY → DoD
```

### Conditional Gates (Still Blocking When Triggered)

```
INTEGRATION: Run if integration tests exist → BLOCKING
PERFORMANCE: Run if performance tests exist → BLOCKING
BROWSER: Run if UI changes detected → BLOCKING
A11Y: Run if UI changes detected → BLOCKING
DOCUMENTATION: Run if public API changes → BLOCKING
MODERN TECH: Run if dependencies updated → BLOCKING

When a conditional gate is triggered, it becomes BLOCKING.
The loop cannot exit until it passes.
```

### Skip Conditions

| Gate | Skip When |
|------|-----------|
| BROWSER | No UI, no display |
| A11Y | No UI |
| PERFORMANCE | No perf tests |
| INTEGRATION | No integration tests |

---

## Gate Configuration

### settings.json

```json
{
  "quality_gates": {
    "enabled": true,
    "strict_mode": true,
    "fail_fast": false,
    "gates": {
      "preflight": { "enabled": true, "blocking": true },
      "lint": { "enabled": true, "blocking": true, "max_errors": 0, "max_warnings": 0 },
      "type": { "enabled": true, "blocking": true, "max_errors": 0 },
      "unit_test": { "enabled": true, "blocking": true, "coverage": 80, "coverage_new": 90 },
      "integration": { "enabled": true, "blocking": true },
      "security": { "enabled": true, "blocking": true, "max_s0": 0, "max_s1": 0 },
      "performance": { "enabled": true, "blocking": true, "max_bundle_kb": 250 },
      "browser": { "enabled": "auto", "blocking": true },
      "a11y": { "enabled": "auto", "blocking": true },
      "docs": { "enabled": true, "blocking": true },
      "modern": { "enabled": true, "blocking": true },
      "dod": { "enabled": true, "blocking": true }
    }
  }
}
```

**STRICT MODE**: When `strict_mode: true`, ALL gates are blocking. The loop cannot exit until every gate passes its threshold. No warnings, no exceptions.

---

## See Also

| Document | Purpose |
|----------|---------|
| [LOOP_WORKFLOW](LOOP_WORKFLOW.md) | Loop execution flow |
| [ERROR_RECOVERY](ERROR_RECOVERY.md) | Error handling |
| [HOOKS_REFERENCE](HOOKS_REFERENCE.md) | Hook details |
| [definition-of-done](skills/quality/definition-of-done.md) | DoD skill |
