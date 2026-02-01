---
name: decision-logger
description: Automatically captures decisions made during development for traceability
version: 1.0.0
triggers:
  - "document this decision"
  - "log decision"
  - "why did we"
  - "decision made"
model: haiku
tags: [orchestration, documentation, traceability]
---

# Decision Logger

Automatically captures and documents decisions made during development execution, ensuring traceability and clean commits.

## Why This Matters

> "We always ask Claude to document the decisions that were made so commits are clean and ready to be shipped."

Undocumented decisions lead to:
- "Why was this done this way?" questions
- Difficulty reverting specific changes
- Lost context when revisiting code
- Messy commit history

---

## Decision Categories

### Technical Decisions
- Architecture choices
- Library/framework selections
- Algorithm implementations
- Data structure choices
- API design decisions

### Trade-off Decisions
- Performance vs. readability
- Security vs. convenience
- Completeness vs. time
- Flexibility vs. simplicity

### Problem-Solving Decisions
- Bug fix approaches
- Workaround implementations
- Alternative solutions rejected
- Why X instead of Y

### Scope Decisions
- What to include/exclude
- Deferred work
- Out-of-scope items
- Future considerations

---

## Decision Log Format

Decisions are logged to `.claude/context/DECISIONS_LOG.md`:

```markdown
# Decisions Log

## Session: 2026-01-30

### [TECH-001] Use bcrypt for password hashing
- **Time:** 14:23
- **Context:** Implementing user authentication
- **Decision:** Use bcrypt with cost factor 12
- **Alternatives Considered:**
  - Argon2id (better but less library support)
  - scrypt (good but bcrypt more familiar to team)
- **Rationale:** Industry standard, well-tested, good library support
- **Implications:** Slightly slower than Argon2 but acceptable for our scale
- **Commit:** abc1234

### [TRADE-002] Prioritize readability over micro-optimization
- **Time:** 15:45
- **Context:** Refactoring payment processing
- **Decision:** Keep explicit null checks instead of optional chaining chain
- **Alternatives Considered:**
  - Single line with `?.` chains (shorter but harder to debug)
- **Rationale:** Easier to set breakpoints, clearer error messages
- **Implications:** Slightly more verbose code
- **Commit:** def5678

### [SCOPE-003] Defer rate limiting to next sprint
- **Time:** 16:30
- **Context:** API security hardening
- **Decision:** Focus on authentication first, rate limiting in sprint 12
- **Rationale:** Auth is higher priority, rate limiting requires Redis setup
- **Implications:** API vulnerable to abuse until rate limiting added
- **Ticket:** AUTH-456
```

---

## When to Log Decisions

### Always Log

| Trigger | Example |
|---------|---------|
| Choosing between alternatives | "Using PostgreSQL instead of MongoDB" |
| Implementing workarounds | "Bypassing X due to bug in library Y" |
| Deviating from blueprint | "Added extra validation not in spec" |
| Scope changes | "Deferring feature X to next sprint" |
| Performance trade-offs | "Accepting N+1 for simpler code" |
| Security decisions | "Using JWT instead of sessions" |

### Don't Log

| Situation | Why Not |
|-----------|---------|
| Obvious implementation choices | No alternatives to consider |
| Following established patterns | Already documented in rules |
| Trivial fixes | Not worth the overhead |
| Standard library usage | Expected behavior |

---

## Integration with Autonomous Loop

### Enhanced BUILD Phase

```
BUILD PHASE (Enhanced):
├── Implement changes
├── **DECISION CAPTURE** ← NEW
│   ├── After each significant choice
│   ├── Log decision with context
│   ├── Note alternatives considered
│   └── Link to relevant code/commit
├── Continue implementation
└── Update decision log before commit
```

### Enhanced QUALITY Phase

```
QUALITY PHASE (Enhanced):
├── Run quality gates
├── **REVIEW DECISIONS** ← NEW
│   ├── Check decisions align with rules
│   ├── Verify trade-offs are acceptable
│   └── Flag decisions needing review
└── Proceed to evaluation
```

---

## Decision Log Template

When making a decision, capture:

```markdown
### [CATEGORY-NNN] Brief description

- **Time:** HH:MM
- **Context:** What were you working on?
- **Decision:** What did you decide?
- **Alternatives Considered:**
  - Alternative 1 (why rejected)
  - Alternative 2 (why rejected)
- **Rationale:** Why this choice?
- **Implications:** What are the consequences?
- **Reversibility:** Easy / Moderate / Difficult
- **Commit:** (added after commit)
```

---

## Decision Categories with Prefixes

| Prefix | Category | Example |
|--------|----------|---------|
| TECH | Technical implementation | TECH-001 |
| ARCH | Architecture | ARCH-001 |
| TRADE | Trade-off | TRADE-001 |
| SCOPE | Scope change | SCOPE-001 |
| SEC | Security | SEC-001 |
| PERF | Performance | PERF-001 |
| FIX | Bug fix approach | FIX-001 |
| DEFER | Deferred work | DEFER-001 |

---

## Linking Decisions to Commits

### Commit Message Format

```
feat(auth): implement password hashing with bcrypt

- Use bcrypt with cost factor 12 for password hashing
- Add password validation before hashing
- Include timing-safe comparison for verification

Decisions: TECH-001, SEC-002

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Git Integration

The decision log enables:
- Finding why a commit was made
- Understanding trade-offs at that point in time
- Reverting with full context
- Onboarding new team members

---

## Querying Decisions

### Find decisions by category
```
grep "### \[TECH-" DECISIONS_LOG.md
```

### Find decisions in date range
```
grep -A 10 "## Session: 2026-01" DECISIONS_LOG.md
```

### Find decisions by commit
```
grep -B 5 "abc1234" DECISIONS_LOG.md
```

---

## Session Initialization

At session start, if working on ongoing tasks:

```
DECISION LOG CHECK:
├── Read recent decisions from DECISIONS_LOG.md
├── Understand context from previous session
├── Note any decisions flagged for review
└── Continue with full context
```

---

## Example: Decision Logging in Practice

### Scenario: Implementing caching

```
Task: Add caching to user profile endpoint

During implementation:
1. Need to choose cache backend → LOG DECISION
2. Need to set TTL → LOG DECISION
3. Need to handle cache invalidation → LOG DECISION

Decision Log Entries:

### [TECH-015] Use Redis for caching
- **Time:** 10:15
- **Context:** Adding caching to user profile endpoint
- **Decision:** Use Redis instead of in-memory cache
- **Alternatives Considered:**
  - In-memory Map (lost on restart)
  - Memcached (Redis has more features)
- **Rationale:** Already have Redis for sessions, consistent stack
- **Implications:** Additional Redis queries, but distributed cache

### [PERF-016] Set 5-minute TTL for user profiles
- **Time:** 10:22
- **Context:** Cache TTL for user profile data
- **Decision:** 5-minute TTL with cache-aside pattern
- **Alternatives Considered:**
  - 1 hour (too stale for active users)
  - 30 seconds (too many cache misses)
- **Rationale:** Balance freshness vs. database load
- **Implications:** Profile updates visible within 5 minutes

### [TECH-017] Invalidate on profile update
- **Time:** 10:35
- **Context:** Cache invalidation strategy
- **Decision:** Delete cache key on any profile write
- **Alternatives Considered:**
  - Write-through (more complex)
  - Time-based only (stale data on update)
- **Rationale:** Simple, correct, profile updates are rare
- **Implications:** One extra Redis call on profile update
```

---

## Usage

### Automatic Integration
The autonomous loop captures decisions:
- During BUILD phase when making choices
- During QUALITY phase when accepting trade-offs
- During EVALUATE phase when scoping

### Manual Invocation
```
"Log this decision: chose X because Y"
"Document why we went with this approach"
"Add to decision log: deferred Z to next sprint"
```

---

## Key Principle

> **Every non-obvious choice should be documented. Future you will thank present you.**

Good decision logs make code review easier, debugging faster, and onboarding smoother.
