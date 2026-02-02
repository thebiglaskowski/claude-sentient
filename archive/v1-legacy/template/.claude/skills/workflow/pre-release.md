---
name: pre-release
description: Comprehensive verification before any release to production
model: sonnet
---

# Pre-Release Checklist

Verification before any release to production.

## Description

Use before releasing to production. Comprehensive check of build, tests, docs, and operations readiness.
Triggers on: "release", "deploy", "ship", "go live", "push to production", "pre-release check", "ready to release".

## Trigger

Activates when:
- About to release/deploy to production
- User asks "is this ready to release?"
- Running `/release` command
- User says "let's ship this" or "deploy to prod"

## Checklist

### Build
- [ ] Build succeeds in production mode
- [ ] No build warnings (or all acknowledged)
- [ ] Assets optimized (minified, compressed)
- [ ] Environment variables configured
- [ ] Build artifacts generated correctly

### Tests
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] E2E tests pass
- [ ] Performance benchmarks acceptable
- [ ] Load testing completed (if applicable)
- [ ] No test regressions

### Documentation
- [ ] CHANGELOG.md has release entry with version
- [ ] Version number updated in package.json/etc.
- [ ] Release notes prepared
- [ ] README reflects current state
- [ ] API documentation current
- [ ] Breaking changes documented

### Operations
- [ ] Deployment steps documented
- [ ] Rollback plan ready and tested
- [ ] Monitoring dashboards ready
- [ ] Alerts configured
- [ ] On-call team notified
- [ ] Database migrations ready (if applicable)
- [ ] Feature flags configured (if applicable)

### Security
- [ ] Dependencies scanned for vulnerabilities
- [ ] No known critical/high vulnerabilities
- [ ] Secrets properly managed (not in code)
- [ ] Security headers configured
- [ ] SSL/TLS certificates valid

### Communication
- [ ] Stakeholders notified of release window
- [ ] Breaking changes communicated to users
- [ ] Support team briefed
- [ ] Status page ready (if applicable)

### Go/No-Go
- [ ] All S0/S1 issues resolved
- [ ] Team sign-off obtained
- [ ] Release window confirmed
- [ ] No conflicting deployments scheduled

## Quick Verification Commands

```bash
# Production build
npm run build

# Run all tests
npm test && npm run test:e2e

# Check for vulnerabilities
npm audit

# Check version
cat package.json | grep version

# View changelog
head -50 CHANGELOG.md
```

## Release Process

```
1. Final checklist review (this document)
2. Create release tag/branch
3. Deploy to staging
4. Smoke test staging
5. Deploy to production
6. Smoke test production
7. Monitor for 15-30 minutes
8. Announce release
```

## Rollback Triggers

Initiate rollback if:
- Error rate > 1% (or baseline + 0.5%)
- Response time > 2x baseline
- Critical functionality broken
- Data integrity issues

## If Any Item Fails

1. **Stop** — Do not release
2. **Fix** the blocking issue
3. **Re-run** the full checklist
4. **Communicate** delay to stakeholders

## Ready to Release?

Only when ALL items pass. A bad release affects all users.

> "If in doubt, don't ship."
