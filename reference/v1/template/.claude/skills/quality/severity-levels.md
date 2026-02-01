---
name: severity-levels
description: Standard severity classification for audits and issue tracking
disable-model-invocation: true
---

# Severity Levels

Standard severity classification for all audits and issue tracking.

## Trigger

Use when:
- Conducting any audit (code, security, performance)
- Classifying bugs or issues
- Prioritizing work
- Creating findings reports

## Severity Definitions

| Level | Name | Meaning | Action Required |
|-------|------|---------|-----------------|
| **S0** | Critical | Blocker, security vulnerability, data loss risk | Fix immediately, stop other work |
| **S1** | High | Major functionality broken, significant impact | Fix before proceeding with features |
| **S2** | Medium | Degraded but functional, workaround exists | Fix soon, within current sprint |
| **S3** | Low | Minor issue, polish, nice-to-have | Fix when convenient |

## Classification Guidelines

### S0 — Critical
- Security vulnerabilities (injection, auth bypass, data exposure)
- Data loss or corruption
- Complete feature breakage with no workaround
- Production system down
- Compliance violations

### S1 — High
- Major feature not working as specified
- Performance degradation >50%
- Breaking changes to public APIs
- Test suite completely failing
- Missing critical documentation

### S2 — Medium
- Feature works but with issues
- Performance degradation 20-50%
- Non-critical test failures
- Documentation gaps
- Code quality issues

### S3 — Low
- Visual/cosmetic issues
- Minor performance improvements
- Code style inconsistencies
- Nice-to-have enhancements
- Documentation polish

## SLA Guidelines

| Severity | Response Time | Resolution Target |
|----------|---------------|-------------------|
| S0 | Immediate | Same day |
| S1 | Within hours | 1-3 days |
| S2 | Within 1 day | 1-2 weeks |
| S3 | Best effort | When convenient |
