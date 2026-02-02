---
name: health-dashboard
description: Generate comprehensive project health overview with metrics
model: sonnet
---

# Project Health Dashboard

Overview metrics and status in STATUS.md.

## Description

Generates and maintains a comprehensive project health overview.
Triggers on: "project health", "dashboard", "status overview", "how healthy is this project".

## Health Dashboard Format

Add to STATUS.md or generate separate HEALTH.md:

```markdown
# Project Health Dashboard

> Last updated: 2024-01-15 10:30 AM

## Quick Status

| Metric | Status | Trend |
|--------|--------|-------|
| Build | ✅ Passing | → |
| Tests | ✅ 156/156 | ↑ |
| Coverage | ⚠️ 78% | ↓ |
| Security | ✅ 0 issues | → |
| Dependencies | ⚠️ 2 outdated | → |
| Tech Debt | 🔶 Medium | ↑ |

## Test Coverage

```
Overall: ████████░░ 78%

src/api/      ██████████ 95%
src/services/ ████████░░ 82%
src/utils/    ██████░░░░ 65%
src/ui/       █████░░░░░ 52%  ⚠️
```

## Recent Activity

| Date | Change | Impact |
|------|--------|--------|
| Today | Added auth module | +500 LOC |
| Yesterday | Fixed login bug | -2 issues |
| 3 days ago | Refactored utils | -200 LOC |

## Open Issues

| Priority | Count | Oldest |
|----------|-------|--------|
| 🔴 Critical | 0 | - |
| 🟠 High | 2 | 5 days |
| 🟡 Medium | 8 | 14 days |
| 🟢 Low | 12 | 30 days |

## Tech Debt

**Debt Score:** 35/100 (Medium)

| Area | Items | Priority |
|------|-------|----------|
| Testing | 3 | High |
| Documentation | 5 | Medium |
| Refactoring | 4 | Low |

## Dependencies

| Status | Count |
|--------|-------|
| ✅ Current | 45 |
| ⚠️ Outdated | 12 |
| 🔴 Vulnerable | 0 |

## Performance

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Build time | 45s | <60s | ✅ |
| Test time | 2m 15s | <3m | ✅ |
| Bundle size | 250KB | <300KB | ✅ |

## Recommendations

1. **Increase test coverage in src/ui/** - Currently 52%, target 80%
2. **Address 2 high-priority issues** - Oldest is 5 days
3. **Update 12 outdated dependencies** - No security issues, but stay current
```

## Health Metrics

### Code Quality

```markdown
## Code Quality Metrics

### Complexity
| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Avg cyclomatic complexity | 4.2 | <10 | ✅ |
| Max complexity | 15 | <20 | ✅ |
| Files >100 LOC | 8 | - | Info |

### Maintainability
| Metric | Value | Status |
|--------|-------|--------|
| Duplicated code | 2.3% | ✅ |
| TODO comments | 12 | ⚠️ |
| Deprecated usage | 0 | ✅ |

### Type Safety (TypeScript)
| Metric | Value | Status |
|--------|-------|--------|
| any usage | 5 | ⚠️ |
| Type coverage | 94% | ✅ |
| Strict mode | Yes | ✅ |
```

### Test Health

```markdown
## Test Health

### Coverage Breakdown
| Type | Coverage | Tests |
|------|----------|-------|
| Unit | 85% | 120 |
| Integration | 72% | 28 |
| E2E | 60% | 8 |

### Test Performance
| Metric | Value |
|--------|-------|
| Total tests | 156 |
| Avg test time | 0.8s |
| Flaky tests | 2 |
| Skipped tests | 3 |

### Untested Areas
- src/ui/components/Chart.tsx
- src/services/legacy/oldApi.ts
- src/utils/experimental/*
```

### Security Health

```markdown
## Security Health

### Vulnerabilities
| Severity | Count | Action |
|----------|-------|--------|
| Critical | 0 | - |
| High | 0 | - |
| Medium | 0 | - |
| Low | 1 | Monitor |

### Security Practices
| Practice | Status |
|----------|--------|
| Dependencies audited | ✅ |
| Secrets in env vars | ✅ |
| Input validation | ✅ |
| Auth implemented | ✅ |
| HTTPS enforced | ✅ |
```

## Dashboard Generation

### Automatic Update
Update dashboard on:
- Session start
- After major changes
- Weekly scheduled

### Data Sources

```markdown
## Data Collection

**Tests:**
```bash
npm test -- --coverage --json
```

**Dependencies:**
```bash
npm outdated --json
npm audit --json
```

**Git stats:**
```bash
git log --oneline --since="1 week ago" | wc -l
git diff --stat HEAD~10
```

**Code metrics:**
```bash
npx cloc src/
npx complexity-report src/
```
```

## Trend Tracking

### Historical Data
Store in `.claude/metrics/health-history.json`:

```json
{
  "history": [
    {
      "date": "2024-01-15",
      "coverage": 78,
      "tests": 156,
      "issues": 22,
      "techDebt": 35
    },
    {
      "date": "2024-01-08",
      "coverage": 80,
      "tests": 150,
      "issues": 24,
      "techDebt": 32
    }
  ]
}
```

### Trend Indicators
- ↑ Improving (good for coverage, bad for debt)
- ↓ Declining (bad for coverage, good for issues)
- → Stable

## Health Score

### Overall Score Calculation

```markdown
## Health Score: 72/100

**Components:**
| Category | Score | Weight | Contribution |
|----------|-------|--------|--------------|
| Tests | 85 | 25% | 21.25 |
| Coverage | 78 | 20% | 15.60 |
| Security | 100 | 20% | 20.00 |
| Dependencies | 70 | 15% | 10.50 |
| Tech Debt | 65 | 20% | 13.00 |

**Rating:** Good (70-84)

**To improve:**
1. Increase coverage to 85% (+7 points)
2. Clear tech debt items (+5 points)
3. Update dependencies (+3 points)
```

### Score Thresholds
| Score | Rating | Color |
|-------|--------|-------|
| 90-100 | Excellent | 🟢 |
| 70-89 | Good | 🟡 |
| 50-69 | Fair | 🟠 |
| 0-49 | Poor | 🔴 |

## Commands

### Generate Dashboard
```
"Generate health dashboard"
"Show project health"
```

### Update Specific Section
```
"Update test coverage metrics"
"Refresh dependency status"
```

### Compare Over Time
```
"Compare health to last week"
"Show health trends"
```

## Integration

### STATUS.md
Include summary at top of STATUS.md:
```markdown
## Health: 72/100 🟡

Quick: ✅ Build | ✅ Tests | ⚠️ Coverage 78% | ✅ Security

[Full dashboard →](HEALTH.md)
```

### CI/CD
Fail build if health drops:
```yaml
- name: Health Check
  run: |
    SCORE=$(cat .claude/metrics/health-score.json | jq '.score')
    if [ $SCORE -lt 60 ]; then
      echo "Health score below threshold: $SCORE"
      exit 1
    fi
```
