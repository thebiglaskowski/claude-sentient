---
name: definition-of-done
description: Universal completion criteria for all work types
version: 3.0.0
triggers:
  - "is this done"
  - "am I done"
  - "completion check"
  - "verify complete"
  - "definition of done"
  - "DoD"
model: haiku
tags: [quality, workflow, completion]
disable_model_invocation: true
---

# Definition of Done (DoD) v3.0

Universal completion criteria that must be verified before any work is considered complete.

## Hook Integration

The `Stop` hook triggers `dod-verifier.py` which automatically verifies DoD criteria:

```
Stop Hook → dod-verifier.py
├── Detects work type from context
├── Selects applicable DoD checklist
├── Checks file indicators (tests, changelog, coverage)
├── Returns PASS/FAIL with missing items
└── Generates verification prompt if needed
```

---

## Global DoD — All Work Must Pass

Every piece of work, regardless of type, must satisfy these criteria:

### Code Quality
- [ ] All tests passing (zero failures)
- [ ] Coverage maintained or improved (≥80% overall, ≥90% new code)
- [ ] No S0 (Critical) issues
- [ ] No S1 (High) issues
- [ ] Linting passes with zero errors
- [ ] No TypeScript/type errors

### Security
- [ ] No hardcoded secrets
- [ ] No new security vulnerabilities introduced
- [ ] Input validation on all external data
- [ ] Authentication/authorization verified (if applicable)

### Documentation
- [ ] Code comments for non-obvious logic
- [ ] README updated (if user-facing changes)
- [ ] CHANGELOG.md entry added
- [ ] API documentation updated (if endpoints changed)

### Git & Version Control
- [ ] Commits are atomic and well-messaged
- [ ] Branch is rebased on latest main
- [ ] No merge conflicts
- [ ] PR description complete (if applicable)
- [ ] Checkpoint commits created for verified features
- [ ] Commit messages reference relevant decisions (if applicable)

### Project State
- [ ] STATUS.md reflects current state
- [ ] KNOWN_ISSUES.md updated (if limitations exist)
- [ ] Work queue is empty or items deferred intentionally
- [ ] Decisions logged in DECISIONS_LOG.md (for significant choices)
- [ ] Checkpoints recorded in CHECKPOINTS.md

---

## Feature DoD — New Functionality

All Global DoD items, plus:

- [ ] Acceptance criteria from spec/blueprint met
- [ ] Edge cases identified and handled
- [ ] Error states have user-friendly messages
- [ ] Loading/pending states implemented (if async)
- [ ] Mobile/responsive verified (if UI)
- [ ] Accessibility basics checked (if UI)
- [ ] Performance acceptable (no obvious bottlenecks)
- [ ] User documentation written (if user-facing)
- [ ] Migration guide provided (if breaking changes)

---

## Bug Fix DoD — Defect Resolution

All Global DoD items, plus:

- [ ] Root cause identified and documented
- [ ] Regression test added (proves bug is fixed)
- [ ] Related areas scanned for similar issues
- [ ] Original reporter's scenario verified working
- [ ] No new bugs introduced by fix

---

## Refactoring DoD — Code Improvement

All Global DoD items, plus:

- [ ] Behavior unchanged (verified by tests)
- [ ] Performance metrics same or better
- [ ] No new dependencies added (unless justified)
- [ ] Old code fully removed (no dead code)
- [ ] Deprecation warnings added (if applicable)

---

## Security Fix DoD — Vulnerability Resolution

All Global DoD items, plus:

- [ ] Vulnerability fully patched
- [ ] Attack vector verified closed
- [ ] Similar patterns scanned codebase-wide
- [ ] Security test added to prevent regression
- [ ] Incident documented (if production impact)
- [ ] Disclosure timeline followed (if external)

---

## Performance Fix DoD — Optimization

All Global DoD items, plus:

- [ ] Baseline metrics captured (before)
- [ ] Target metrics achieved (after)
- [ ] No functionality regression
- [ ] Improvement measured in production-like environment
- [ ] Caching invalidation verified (if caching added)

---

## Documentation DoD — Content Updates

- [ ] Technically accurate
- [ ] Grammar and spelling checked
- [ ] Code examples tested and working
- [ ] Links validated
- [ ] Screenshots current (if UI documentation)
- [ ] Version numbers accurate

---

## Verification Process

### Before Declaring Done

1. **Self-Review**
   - Read through all changes
   - Check against applicable DoD checklist
   - Run full test suite locally

2. **Automated Checks**
   - CI pipeline passes
   - Coverage gates pass
   - Security scan passes
   - Lint checks pass

3. **Manual Verification**
   - Test happy path manually
   - Test error scenarios
   - Verify in browser (if UI)
   - Check mobile/responsive (if UI)

4. **Documentation Check**
   - CHANGELOG has entry
   - STATUS.md is current
   - README updated if needed

### DoD Verification Command

Run `/verify-done` or ask:
```
Is this work complete? Check against Definition of Done.
```

---

## When to Skip Items

Some DoD items may not apply. Document why:

```markdown
## DoD Exceptions for [Work Item]

- [ ] ~~Mobile responsive~~ — Backend-only change
- [ ] ~~User documentation~~ — Internal tooling only
- [ ] ~~Migration guide~~ — Non-breaking change
```

Always document exceptions, never silently skip.

---

## Quality Gate Integration

The autonomous loop (`/cc-loop`) uses this DoD automatically:

```
Phase 6: QUALITY
├── Run all 15 quality gates
├── All gates must pass (no exceptions)

Phase 6.25: CHECKPOINT (if quality passes)
├── Create checkpoint commit for verified feature
├── Include decision references in commit message
├── Update CHECKPOINTS.md
├── Enable rollback to this known-good state

Phase 7: EVALUATE
├── Run DoD checklist for work type
├── All items must pass
├── Two consecutive passing iterations required
└── Then verify one more time before exit
```

### Checkpoint Criteria

Before creating a checkpoint commit:
- [ ] Tests pass for the completed feature
- [ ] Linting passes (no errors, no warnings)
- [ ] Type checking passes
- [ ] Feature works as intended (verified)
- [ ] No debug code left behind
- [ ] Changes are logically complete

---

## Severity Reminder

| Severity | Definition | DoD Impact |
|----------|------------|------------|
| S0 Critical | Blocker, security, data loss | Cannot be done with S0 open |
| S1 High | Major functionality broken | Cannot be done with S1 open |
| S2 Medium | Degraded but functional | Can defer, must document |
| S3 Low | Minor, polish | Can defer, must document |

---

## Final Check

Before saying "done," ask yourself:

1. Would I be proud to show this code to a senior engineer?
2. Could a new team member understand this without asking me?
3. If this breaks in production at 3 AM, is there enough logging to debug?
4. Have I tested the ways a user might misuse this?
5. Is this the simplest solution that works?

If any answer is "no," it's not done yet.
