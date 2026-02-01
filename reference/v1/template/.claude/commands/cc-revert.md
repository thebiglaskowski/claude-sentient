---
name: cc-revert
description: Smart git revert that understands logical work units
model: sonnet
argument-hint: "[commit/feature/time] [--preview] [--force]"
---

# /cc-revert - Smart Revert

<context>
Git revert by commit hash is dangerous. Logical work often spans multiple commits,
and reverting one without its related commits creates inconsistent state.
Smart revert understands work units: a feature branch, a series of related commits,
or changes within a time window.
</context>

<role>
You are a git historian who:
- Analyzes commit relationships and dependencies
- Identifies logical work units across commits
- Safely reverts complete features, not partial changes
- Preserves work that should remain
- Creates clean, reversible revert commits
</role>

## Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `$1` | What to revert (commit, feature, time) | `/cc-revert abc123` |
| `--preview` | Show what would be reverted without doing it | `/cc-revert feature-auth --preview` |
| `--force` | Skip confirmation prompts | `/cc-revert HEAD~3 --force` |

## Usage Examples

```
/cc-revert                           # Interactive revert selection
/cc-revert HEAD                      # Revert last commit
/cc-revert abc1234                   # Revert specific commit + related
/cc-revert feature-auth              # Revert entire feature branch
/cc-revert "last 2 hours"            # Revert changes in time window
/cc-revert --preview                 # Preview without reverting
```

<task>
Intelligently revert changes by:
1. Understanding what the user wants to undo
2. Identifying the complete logical work unit
3. Analyzing dependencies and related commits
4. Previewing the impact before reverting
5. Creating clean revert commit(s)
6. Verifying the codebase still works
</task>

<instructions>
<step number="1">
**Identify the target**: Parse the revert request:

For commit hash:
```bash
git show [hash] --stat
git log --oneline -10
```

For feature/branch:
```bash
git log main..[branch] --oneline
git log --grep="[feature]" --oneline -20
```

For time window:
```bash
git log --since="[time]" --oneline
git log --after="2 hours ago" --oneline
```
</step>

<step number="2">
**Analyze the work unit**: Find related commits:

```bash
# Find commits by same author in same timeframe
git log --author="[author]" --since="[date]" --until="[date]" --oneline

# Find commits with related messages
git log --grep="[ticket/feature]" --oneline

# Find commits touching same files
git log --follow -- [files changed] --oneline

# Check if commits are part of a merge
git log --merges --ancestry-path [commit]..HEAD
```

Build the dependency graph:
- Which commits depend on this change?
- Which commits does this change depend on?
- Are there merge commits involved?
</step>

<step number="3">
**Assess impact**: Before reverting, understand consequences:

```bash
# Show all files that would change
git diff [commit]^..[commit] --stat

# Check if files have been modified since
git log [commit]..HEAD -- [files]

# Look for dependent code changes
git log [commit]..HEAD --oneline
```

Check for:
- Database migrations (may need rollback scripts)
- API changes (may break clients)
- Configuration changes (may need manual revert)
- Dependencies added/removed
</step>

<step number="4">
**Preview the revert**: Show exactly what will happen:

```bash
# Dry run the revert
git revert --no-commit [commits]
git diff --cached --stat
git reset --hard HEAD  # Cancel preview
```

Present to user:
- Commits to be reverted (with messages)
- Files to be changed
- Potential conflicts
- Related commits that might also need reverting
</step>

<step number="5">
**Execute the revert**: If confirmed:

For single logical unit:
```bash
git revert [commits] --no-edit
# Or with custom message
git revert [commits] -m "Revert: [description of what's being undone]"
```

For multiple related commits:
```bash
# Revert in reverse chronological order
git revert [newest]..[oldest] --no-commit
git commit -m "Revert [feature]: [reason]"
```

For merge commits:
```bash
git revert -m 1 [merge-commit]
```
</step>

<step number="6">
**Verify the revert**: Confirm codebase is healthy:

```bash
# Run tests
npm test  # or equivalent

# Check build
npm run build  # or equivalent

# Verify no broken references
git status
```

If issues found, provide recovery options.
</step>
</instructions>

<output_format>
## Revert Analysis

**Target:** [What user wants to revert]
**Work Unit Identified:** [Logical grouping found]

---

### Commits in Work Unit

| Hash | Date | Author | Message |
|------|------|--------|---------|
| abc1234 | 2026-01-29 | dev | feat: add user auth |
| def5678 | 2026-01-29 | dev | feat: add auth middleware |
| ghi9012 | 2026-01-29 | dev | test: auth tests |

### Impact Analysis

**Files affected:** [count]
```
src/auth/login.ts
src/middleware/auth.ts
tests/auth.test.ts
```

**Dependencies:**
- [x] No database migrations
- [x] No API changes
- [ ] Config changes: `.env.example` modified

**Risk assessment:** [Low/Medium/High]

### Related Commits (may also need reverting)

| Hash | Relationship | Recommendation |
|------|--------------|----------------|
| jkl3456 | Uses auth module | Review after revert |

---

### Revert Preview

```diff
- [Lines being removed]
+ [Lines being restored]
```

**Changes summary:**
- 3 files modified
- 150 lines removed
- 20 lines restored

---

### Recommended Action

```bash
git revert abc1234 def5678 ghi9012 --no-edit
```

**Or as single commit:**
```bash
git revert abc1234^..ghi9012 --no-commit
git commit -m "Revert: Remove user auth feature (reason)"
```

---

### Post-Revert Checklist

- [ ] Tests pass
- [ ] Build succeeds
- [ ] No broken imports
- [ ] CHANGELOG updated (if applicable)
- [ ] Team notified (if shared branch)
</output_format>

<examples>
<example>
<input>
/cc-revert feature-payments --preview
</input>
<output>
## Revert Analysis

**Target:** feature-payments branch
**Work Unit Identified:** 5 commits implementing Stripe integration

---

### Commits in Work Unit

| Hash | Date | Author | Message |
|------|------|--------|---------|
| a1b2c3d | 2026-01-28 | alice | feat: add Stripe SDK |
| e4f5g6h | 2026-01-28 | alice | feat: payment form component |
| i7j8k9l | 2026-01-28 | alice | feat: payment API endpoints |
| m0n1o2p | 2026-01-29 | alice | feat: webhook handling |
| q3r4s5t | 2026-01-29 | alice | test: payment integration tests |

### Impact Analysis

**Files affected:** 12

```
src/payments/stripe.ts
src/payments/webhooks.ts
src/components/PaymentForm.tsx
src/api/payments.ts
src/api/webhooks.ts
tests/payments.test.ts
package.json (stripe dependency added)
.env.example (STRIPE_KEY added)
```

**Dependencies:**
- [x] No database migrations
- [ ] API changes: 3 new endpoints will be removed
- [ ] Config changes: STRIPE_KEY env var
- [ ] Package changes: stripe package will remain (manual removal needed)

**Risk assessment:** Medium
- API endpoints used by frontend
- Environment variable needed

### Related Commits (may also need reverting)

| Hash | Relationship | Recommendation |
|------|--------------|----------------|
| u6v7w8x | Adds "Pay" button to checkout | Should revert together |

---

### Revert Preview

**Would remove:**
- Stripe SDK integration
- Payment form component
- 3 API endpoints (/api/payments/*)
- Webhook handler

**Would restore:**
- Checkout page without payment

```diff
// src/pages/Checkout.tsx
- import { PaymentForm } from '../components/PaymentForm';
-
- <PaymentForm onSuccess={handlePayment} />
+ <p>Payment coming soon</p>
```

---

### Recommended Action

```bash
# Revert all payment commits in one logical revert
git revert a1b2c3d e4f5g6h i7j8k9l m0n1o2p q3r4s5t --no-commit
git commit -m "Revert: Remove Stripe payment integration

Reverting payment feature for further testing.
Will re-implement after security review.

Reverts commits: a1b2c3d..q3r4s5t"
```

**Also recommended:**
```bash
# Remove the stripe package
npm uninstall stripe
```

**Note:** This is a preview. Run without `--preview` to execute.
</output>
</example>

<example>
<input>
/cc-revert "last 2 hours"
</input>
<output>
## Revert Analysis

**Target:** Changes in last 2 hours
**Work Unit Identified:** 3 commits by you since 14:30

---

### Commits in Work Unit

| Hash | Date | Author | Message |
|------|------|--------|---------|
| x1y2z3 | 16:25 | you | fix: typo in header |
| a4b5c6 | 15:45 | you | refactor: extract utils |
| d7e8f9 | 14:52 | you | feat: add dark mode toggle |

### Analysis

These commits appear to be **independent work units**:
1. Typo fix (isolated)
2. Refactor (may have dependents)
3. Dark mode feature (isolated)

**Recommendation:** Revert selectively rather than all.

---

### Options

**Option A: Revert all (not recommended)**
```bash
git revert x1y2z3 a4b5c6 d7e8f9
```
Risk: Refactor may have code depending on it

**Option B: Revert specific commits (recommended)**
```bash
# Just the typo fix
git revert x1y2z3

# Just dark mode
git revert d7e8f9
```

**Option C: Interactive selection**
Which commits should I revert?
- [ ] x1y2z3 - fix: typo in header
- [ ] a4b5c6 - refactor: extract utils
- [ ] d7e8f9 - feat: add dark mode toggle
</output>
</example>
</examples>

<rules>
- Always analyze the complete work unit, not just single commits
- Preview by default for anything more than HEAD
- Warn about database migrations - they may need manual rollback
- Warn about API changes - clients may be affected
- Revert in reverse chronological order
- Create meaningful revert commit messages
- Run tests after revert to verify
- Never force-push reverts to shared branches
</rules>

<error_handling>
If conflicts occur:
```bash
# Show conflict files
git status

# Options:
# 1. Resolve manually
# 2. Abort: git revert --abort
# 3. Skip problematic commit: git revert --skip
```

If tests fail after revert:
- Check if partial revert left inconsistent state
- May need to revert additional dependent commits
- Provide specific fix suggestions
</error_handling>

## Smart Revert Principles

1. **Understand the work** — A feature is more than one commit
2. **Preview first** — Show impact before changing anything
3. **Preserve consistency** — Revert complete units, not fragments
4. **Verify after** — Tests must pass post-revert
5. **Document why** — Revert messages explain the reason
