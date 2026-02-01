---
name: commit-checkpoint
description: Creates git commit checkpoints after verified features for easy rollback
version: 1.0.0
triggers:
  - "checkpoint"
  - "save progress"
  - "commit checkpoint"
  - "feature verified"
model: haiku
tags: [workflow, git, safety]
---

# Commit Checkpoint

Creates git commit checkpoints after each verified feature, enabling easy rollback and clean commit history.

## Why This Matters

> "Git lets us roll back easily... commits are clean and ready to be shipped."

Without checkpoints:
- Large, monolithic commits are hard to revert
- Rollback means losing all progress
- Debugging which change broke things is difficult
- History becomes a single "implement everything" commit

With checkpoints:
- Each feature is a separate commit
- Rollback to any verified state
- Bisect to find breaking changes
- Clean, reviewable history

---

## Checkpoint Strategy

### When to Create Checkpoints

| Event | Checkpoint? | Why |
|-------|-------------|-----|
| Feature implemented + tests pass | Yes | Verified working state |
| Bug fixed + regression test added | Yes | Known good state |
| Refactoring complete + tests pass | Yes | Behavior preserved |
| Configuration change verified | Yes | System still works |
| Documentation updated | Optional | No functional change |
| Work in progress | No | Not verified |

### Checkpoint Criteria

Before creating a checkpoint, verify:

```
CHECKPOINT CRITERIA:
├── [ ] Tests pass (all relevant tests green)
├── [ ] Linting passes (no errors, no new warnings)
├── [ ] Type checking passes (if applicable)
├── [ ] Feature works as intended (manual or automated verification)
├── [ ] No debug code left behind
├── [ ] No console.log or print statements
└── [ ] Changes are logically complete (not half-done)
```

---

## Integration with Autonomous Loop

### Enhanced Loop Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                 LOOP WITH COMMIT CHECKPOINTS                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  BUILD → TEST → QUALITY → **CHECKPOINT** → EVALUATE → NEXT      │
│                               │                                  │
│                               ▼                                  │
│                    ┌─────────────────────┐                      │
│                    │ If tests pass:      │                      │
│                    │ • Stage changes     │                      │
│                    │ • Create commit     │                      │
│                    │ • Tag checkpoint    │                      │
│                    │ • Log decisions     │                      │
│                    └─────────────────────┘                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Phase 6.5: CHECKPOINT (New)

```
CHECKPOINT PHASE:
├── Verify all tests pass
├── Verify quality gates green
├── Stage relevant changes (not all files)
├── Create descriptive commit message
├── Include decision references
├── Tag if significant milestone
└── Update LOOP_STATE.md with checkpoint
```

---

## Commit Message Format

### Standard Checkpoint Commit

```
feat(auth): implement JWT token refresh

- Add refresh token endpoint
- Store refresh tokens in Redis with 7-day expiry
- Add token rotation on refresh
- Prevent token reuse after rotation

Tests: 12 new tests, all passing
Coverage: auth module 94%

Decisions: TECH-015, SEC-021

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Checkpoint with Verification Notes

```
fix(payment): handle Stripe webhook signature validation

- Add signature verification for all webhooks
- Return 400 on invalid signature
- Log validation failures for monitoring

Verified:
- Stripe CLI webhook testing: PASS
- Invalid signature rejection: PASS
- Replay attack prevention: PASS

Fixes: PAY-234
Decisions: SEC-025

Co-Authored-By: Claude <noreply@anthropic.com>
```

---

## Checkpoint Workflow

### Step 1: Verify Before Commit

```bash
# Run tests
npm test

# Run linting
npm run lint

# Run type checking
npm run typecheck

# If all pass, proceed to commit
```

### Step 2: Stage Specific Files

```bash
# Stage only files related to this feature
git add src/auth/refresh.ts
git add src/auth/refresh.test.ts
git add src/routes/auth.ts

# NOT: git add -A (too broad)
```

### Step 3: Create Descriptive Commit

```bash
git commit -m "feat(auth): implement JWT token refresh

- Add refresh token endpoint
- Store refresh tokens in Redis with 7-day expiry
- Add token rotation on refresh

Decisions: TECH-015

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Step 4: Tag Milestones (Optional)

```bash
# For significant milestones
git tag -a checkpoint-auth-complete -m "Authentication feature complete"
```

### Step 5: Update Loop State

```markdown
## Last Checkpoint
- **Commit:** abc1234
- **Feature:** JWT token refresh
- **Time:** 2026-01-30 14:30
- **Status:** Verified working
```

---

## Rollback Strategy

### Scenario: New feature breaks something

```bash
# Find last working checkpoint
git log --oneline

# Output:
# abc1234 feat(auth): implement JWT token refresh ← last checkpoint
# def5678 feat(auth): add login endpoint
# ghi9012 feat(auth): add user model

# Rollback to last checkpoint
git revert HEAD

# Or reset if not pushed
git reset --hard abc1234
```

### Scenario: Need to undo specific feature

```bash
# Find the checkpoint commit
git log --oneline --grep="token refresh"

# Revert that specific commit
git revert abc1234

# Commit history preserved, feature removed
```

---

## Checkpoint Naming Conventions

### Commit Type Prefixes

| Prefix | Use For |
|--------|---------|
| `feat` | New feature checkpoint |
| `fix` | Bug fix checkpoint |
| `refactor` | Refactoring checkpoint |
| `test` | Test-only checkpoint |
| `docs` | Documentation checkpoint |
| `perf` | Performance improvement |
| `security` | Security fix |

### Scope Examples

```
feat(auth): ...      # Authentication module
feat(api): ...       # API endpoints
feat(ui): ...        # User interface
fix(payment): ...    # Payment processing
refactor(db): ...    # Database layer
```

---

## Integration with Decision Logger

Each checkpoint should reference relevant decisions:

```
Commit Message:
feat(cache): add Redis caching for user profiles

- Implement cache-aside pattern
- Set 5-minute TTL
- Invalidate on profile update

Decisions: TECH-015, PERF-016, TECH-017
```

This creates bidirectional traceability:
- Commit → Decisions (in commit message)
- Decisions → Commit (in DECISIONS_LOG.md)

---

## Checkpoint State File

Track checkpoints in `.claude/context/CHECKPOINTS.md`:

```markdown
# Checkpoint History

## Current Session: 2026-01-30

### Checkpoint 1: abc1234
- **Time:** 14:30
- **Feature:** JWT token refresh
- **Files:** 3 changed
- **Tests:** 12 new, all pass
- **Status:** Verified

### Checkpoint 2: def5678
- **Time:** 15:45
- **Feature:** Rate limiting middleware
- **Files:** 2 changed
- **Tests:** 8 new, all pass
- **Status:** Verified

## Rollback Points
- If auth breaks: revert to abc1234
- If rate limiting breaks: revert to def5678
- Clean slate: reset to session start (xyz9876)
```

---

## Automatic Checkpoint Triggers

The autonomous loop should checkpoint when:

1. **Feature Complete**
   - Work queue item marked done
   - Tests pass for that feature
   - Verification successful

2. **Quality Gate Milestone**
   - Coverage target reached
   - All S0/S1 issues resolved
   - Security audit clean

3. **Phase Completion**
   - End of major implementation phase
   - Before starting new feature
   - Before risky changes

---

## Usage

### Automatic Integration
The loop creates checkpoints:
- After each verified feature
- Before risky operations
- At quality gate milestones

### Manual Invocation
```
"Create a checkpoint for this feature"
"Commit and checkpoint current progress"
"Save this as a rollback point"
```

---

## Key Principle

> **Every verified feature should be a commit. Every commit should be a potential rollback point.**

Small, verified checkpoints beat large, risky commits every time.
