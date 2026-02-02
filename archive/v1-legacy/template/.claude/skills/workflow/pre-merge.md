---
name: pre-merge
description: Verification checklist before merging PRs to main branch
model: sonnet
---

# Pre-Merge Checklist

Verification before merging to main branch.

## Description

Use before merging a PR or branch to main. Ensures code review, tests, and documentation are complete.
Triggers on: "merge", "ready to merge", "merge PR", "merge to main", "approve PR", "pre-merge check".

## Trigger

Activates when:
- About to merge a PR
- User asks "is this ready to merge?"
- Reviewing a PR for final approval
- User says "merge this" or "approve this PR"

## Checklist

### Code Review
- [ ] Code has been reviewed by at least one person
- [ ] All review comments addressed
- [ ] No unresolved conversations
- [ ] Reviewer has approved

### Tests
- [ ] All CI checks pass (green build)
- [ ] Test coverage maintained or improved
- [ ] Integration tests pass
- [ ] Manual testing completed (if applicable)
- [ ] No flaky tests introduced

### Documentation
- [ ] CHANGELOG.md updated with changes
- [ ] README.md updated (if user-facing changes)
- [ ] API docs updated (if API changes)
- [ ] ADR created (if architectural decision)

### Compatibility
- [ ] No breaking changes (or properly versioned)
- [ ] Migration path documented (if breaking)
- [ ] Backwards compatibility verified
- [ ] Deprecation warnings added (if deprecating)

### Security
- [ ] No secrets in code
- [ ] Input validation in place
- [ ] Authentication/authorization verified
- [ ] No new vulnerabilities introduced

### Final Checks
- [ ] Branch is up to date with target branch
- [ ] Merge conflicts resolved cleanly
- [ ] Squash commits if needed (clean history)
- [ ] PR description is accurate

## Quick Verification Commands

```bash
# Update branch
git fetch origin && git rebase origin/main

# Check CI status
gh pr checks

# View PR
gh pr view

# Check for conflicts
git merge --no-commit --no-ff origin/main && git merge --abort
```

## Merge Strategies

| Strategy | When to Use |
|----------|-------------|
| **Squash** | Multiple small commits → clean single commit |
| **Merge commit** | Preserve full history, feature branches |
| **Rebase** | Linear history, small changes |

## If Any Item Fails

1. **Don't merge** until resolved
2. **Request changes** on the PR
3. **Communicate** blockers to the author

## Ready to Merge?

Only when ALL items pass. A bad merge affects everyone on the team.
