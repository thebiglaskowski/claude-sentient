---
name: dependency-tracker
description: Track outdated and vulnerable dependencies
model: sonnet
---

# Dependency Update Tracker

Track outdated and vulnerable dependencies.

## Description

Monitor project dependencies for updates, security vulnerabilities, and compatibility issues.
Triggers on: "check dependencies", "outdated packages", "security vulnerabilities", "update dependencies", "npm audit".

## Dependency Analysis

### Quick Check
```markdown
## Dependency Status

**Last checked:** 2024-01-15

### Summary
| Status | Count |
|--------|-------|
| ✅ Up to date | 45 |
| ⚠️ Minor update | 12 |
| 🔶 Major update | 3 |
| 🔴 Security issue | 2 |

### Action Required
- 🔴 2 packages have security vulnerabilities
- 🔶 3 packages have breaking changes available
```

### Detailed Report
```markdown
## Dependency Report

### 🔴 Security Vulnerabilities

| Package | Current | Issue | Severity | Fix |
|---------|---------|-------|----------|-----|
| lodash | 4.17.20 | Prototype pollution | High | 4.17.21 |
| axios | 0.21.0 | SSRF vulnerability | Medium | 0.21.1 |

**Recommendation:** Update immediately

---

### 🔶 Major Updates Available

| Package | Current | Latest | Breaking Changes |
|---------|---------|--------|------------------|
| express | 4.18.2 | 5.0.0 | Yes - see migration guide |
| typescript | 4.9.5 | 5.3.3 | Minor - strict checks |
| jest | 28.1.3 | 29.7.0 | Config changes needed |

**Recommendation:** Plan migration, test thoroughly

---

### ⚠️ Minor/Patch Updates

| Package | Current | Latest | Type |
|---------|---------|--------|------|
| react | 18.2.0 | 18.2.1 | Patch |
| @types/node | 20.10.0 | 20.11.0 | Minor |
| eslint | 8.55.0 | 8.56.0 | Minor |
| ... | ... | ... | ... |

**Recommendation:** Update in next maintenance window

---

### ✅ Up to Date (45 packages)
All other dependencies are at their latest compatible versions.
```

## Check Commands

### NPM/Yarn
```bash
# Check outdated
npm outdated

# Security audit
npm audit

# Detailed audit
npm audit --json
```

### Python
```bash
# Check outdated
pip list --outdated

# Security check
pip-audit
safety check
```

### Other Package Managers
```bash
# Go
go list -u -m all

# Rust
cargo outdated

# Ruby
bundle outdated
```

## Automated Checks

### On Session Start
Light check for critical issues:
```markdown
⚠️ Dependency Alert

2 security vulnerabilities found:
- lodash (High severity)
- axios (Medium severity)

Run `/check-deps` for full report.
```

### Weekly Full Scan
Comprehensive dependency analysis:
```markdown
## Weekly Dependency Report

**Project:** my-app
**Date:** 2024-01-15

[Full detailed report...]

**Action Items:**
1. [ ] Fix 2 security vulnerabilities (Critical)
2. [ ] Update 12 minor versions (Low priority)
3. [ ] Plan TypeScript 5 migration (Medium priority)
```

## Update Strategies

### Safe Updates (Patch/Minor)
```markdown
## Safe Update Plan

These updates are low-risk:

```bash
npm update
```

**Will update:**
- react: 18.2.0 → 18.2.1
- @types/node: 20.10.0 → 20.11.0
- eslint: 8.55.0 → 8.56.0
... (12 packages)

**After update:**
1. Run tests
2. Quick smoke test
3. Commit: "chore: update dependencies"
```

### Breaking Updates (Major)
```markdown
## Major Update: TypeScript 4 → 5

**Package:** typescript
**Current:** 4.9.5
**Target:** 5.3.3

### Breaking Changes
1. Stricter type checking
2. New `verbatimModuleSyntax` default
3. Decorator changes

### Migration Steps
1. Update tsconfig.json
2. Fix new type errors
3. Update build scripts
4. Test thoroughly

### Estimated Impact
- Files to modify: ~5
- New errors to fix: ~20
- Risk: Medium

[Generate Migration PR] [Skip for now]
```

### Security Updates
```markdown
## Security Update Required

**Package:** lodash
**Vulnerability:** Prototype Pollution (CVE-2021-23337)
**Severity:** High
**CVSS:** 7.4

### Fix
```bash
npm install lodash@4.17.21
```

### If Breaking
If update causes issues:
```bash
# Use resolution/override
npm pkg set resolutions.lodash=4.17.21
```

**Apply fix now?** [Yes] [Skip]
```

## Compatibility Tracking

### Peer Dependencies
```markdown
## Peer Dependency Issues

⚠️ Potential conflicts detected:

| Package | Requires | You Have |
|---------|----------|----------|
| react-dom | react@^18.0.0 | react@18.2.0 ✅ |
| @testing-library/react | react@^18.0.0 | react@18.2.0 ✅ |
| old-package | react@^17.0.0 | react@18.2.0 ❌ |

**Recommendation:**
- Update `old-package` or find alternative
- Or use `--legacy-peer-deps` (not recommended)
```

### Engine Requirements
```markdown
## Engine Compatibility

**Project requires:**
- Node: >=18.0.0
- npm: >=9.0.0

**Your environment:**
- Node: 20.10.0 ✅
- npm: 10.2.3 ✅

**Dependencies requiring newer Node:**
- None ✅
```

## Notifications

### Critical (Immediate)
- Security vulnerabilities (High/Critical)
- Deprecated packages with no alternative

### Warning (Weekly)
- Major version updates available
- Security vulnerabilities (Medium/Low)
- Deprecated packages

### Info (Monthly)
- Minor/patch updates available
- New recommended packages

## Integration

### Pre-Commit Check
```markdown
Before commit, verify:
- [ ] No new security vulnerabilities introduced
- [ ] Lock file is up to date
- [ ] No deprecated package warnings
```

### CI/CD Integration
```yaml
- name: Dependency Check
  run: |
    npm audit --audit-level=high
    npm outdated || true
```

### Dependabot/Renovate
Works alongside automated tools:
```markdown
**Dependabot PRs waiting:**
- #123: Bump lodash from 4.17.20 to 4.17.21 (security)
- #124: Bump typescript from 4.9.5 to 5.3.3 (major)

Review PRs? [Open in browser]
```

## Configuration

```json
{
  "dependencyTracker": {
    "checkOnStart": true,
    "securityAlertsOnly": false,
    "ignoredPackages": ["internal-package"],
    "autoUpdatePatch": false,
    "weeklyReport": true
  }
}
```
