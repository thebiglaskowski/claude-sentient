---
name: queue-manager
description: Visualize, manage, and prioritize work queue with dependency tracking and query classification
version: 4.0.0
triggers:
  - "show queue"
  - "work queue"
  - "what's next"
  - "prioritize"
  - "add to queue"
  - "remove from queue"
  - "queue status"
  - "depends on"
  - "blocked by"
model: haiku
tags: [workflow, queue, management, loop, dependencies, orchestration]
context: inherit
---

# Work Queue Manager v4.0

Visualize, manage, and prioritize the work queue during autonomous development loops. Now with **task dependency support**, **query classification**, and **intelligent subagent allocation**.

**v4.0 Enhancements (from Anthropic Cookbook):**
- Query classification: depth-first vs breadth-first vs straightforward
- Subagent count guidelines based on task complexity
- Intelligent delegation with clear task boundaries
- Enhanced synthesis responsibility

**v3.0 Features (maintained):**
- Task dependencies (`blockedBy`/`blocks`)
- Automatic unblocking when predecessors complete
- Dependency-aware prioritization
- Swarm mode integration
- Claimed-by tracking for workers

---

## Query Classification

Before populating the queue, classify the incoming request to determine optimal parallelization strategy.

### Query Types

| Type | Characteristics | Strategy |
|------|-----------------|----------|
| **Depth-First** | Single topic, multiple perspectives | Parallel agents explore different angles of same question |
| **Breadth-First** | Multiple distinct sub-questions | Parallel agents each handle separate sub-topics |
| **Straightforward** | Focused, well-defined, single answer | One agent or direct execution |

### Classification Decision Tree

```
Is the query about a single topic requiring multiple viewpoints?
├── YES → DEPTH-FIRST
│   Examples:
│   ├── "What's the best approach to auth in this codebase?"
│   ├── "Review this PR from security, performance, and maintainability angles"
│   └── "What caused this bug?" (needs multiple investigation angles)
│
└── NO → Can the query be split into independent sub-questions?
    ├── YES → BREADTH-FIRST
    │   Examples:
    │   ├── "Review all files in src/api/"
    │   ├── "Audit auth, database, and API modules"
    │   └── "Compare React, Vue, and Svelte for this project"
    │
    └── NO → STRAIGHTFORWARD
        Examples:
        ├── "What's in package.json?"
        ├── "Fix this typo"
        └── "Add a loading spinner to the button"
```

### Classification Output

```markdown
## Query Classification

**Query:** "Review the entire codebase for security issues"

**Classification:** Breadth-First
**Reasoning:** Can split by directory/module, each reviewable independently
**Parallelization:** Yes (by module)
**Suggested Subagent Count:** 4-6 (one per major module)

**Task Decomposition:**
├── Review src/auth/** (security-analyst)
├── Review src/api/** (security-analyst)
├── Review src/database/** (security-analyst)
├── Review src/utils/** (code-reviewer)
├── Check dependencies (dependency-audit)
└── Final synthesis (leader)
```

---

## Subagent Count Guidelines

Based on query classification and complexity, allocate appropriate resources:

### Guidelines Table

| Complexity | Subagent Count | When to Use |
|------------|----------------|-------------|
| **Simple/Straightforward** | 1 | Single fact-finding, direct answer, quick fix |
| **Standard** | 2-3 | Multiple perspectives or small decomposition |
| **Medium** | 3-5 | Multi-faceted questions, different methodological approaches |
| **High** | 5-10 | Broad queries with many distinct components |
| **Very High** | 10-20 (max) | Large-scale reviews, comprehensive audits |

### Hard Limit

**Never exceed 20 subagents.** If a task seems to require more:
1. Restructure approach to consolidate similar sub-tasks
2. Be more efficient in decomposition
3. Prefer fewer, more capable agents over many narrow ones

### Examples

```markdown
| Query | Classification | Count | Reasoning |
|-------|----------------|-------|-----------|
| "What's the tax deadline?" | Straightforward | 1 | Simple fact-finding |
| "Compare top 3 cloud providers" | Breadth-First | 3 | One per provider |
| "Analyze AI impact on healthcare" | Depth-First | 4 | Regulatory, clinical, economic, tech angles |
| "Review all 50 API endpoints" | Breadth-First | 5-10 | Group by domain, not one per endpoint |
| "Full codebase security audit" | Breadth-First | 6-8 | By module, with specialist overlap |
```

---

## Delegation Instructions

When spawning subagents, provide clear, specific task descriptions:

### Required Elements

Every subagent task description must include:

1. **Specific objective** — One core goal per subagent
2. **Expected output format** — Report, list, analysis, or code
3. **Background context** — How this contributes to the main goal
4. **Key questions to answer** — What must be determined
5. **Suggested sources/tools** — What to use
6. **Scope boundaries** — What NOT to explore (prevent drift)

### Example Task Description

```markdown
**Subagent Task: Review src/auth/ for security vulnerabilities**

**Objective:** Identify security issues in the authentication module.

**Context:** This is part of a full codebase security audit. Your findings
will be synthesized with reviews of other modules.

**Key Questions:**
1. Are passwords hashed correctly (bcrypt, Argon2)?
2. Is session management secure?
3. Are there injection vulnerabilities?
4. Is rate limiting implemented for auth endpoints?

**Expected Output:** Findings report with:
- Issue description
- Severity (S0-S3)
- File and line number
- Remediation suggestion

**Tools:** Read files in src/auth/, check for OWASP patterns.

**Scope:** Only src/auth/. Do not review API endpoints outside auth.
```

### Anti-Patterns

| Bad Delegation | Why It's Bad | Better Approach |
|----------------|--------------|-----------------|
| "Review the code" | Too vague | "Review src/auth/ for SQL injection and XSS" |
| "Find all bugs" | Unbounded | "Check for null pointer issues in payment module" |
| Overlapping scopes | Duplicated work | Clear directory/concern boundaries |
| No output format | Inconsistent results | Specify table, report, or list format |

---

## Synthesis Responsibility

**The leader's primary role is to coordinate and synthesize, not conduct primary research.**

### Leader Responsibilities

```markdown
✓ Plan the research/work approach
✓ Classify the query type
✓ Decompose into tasks with clear boundaries
✓ Spawn subagents with detailed instructions
✓ Synthesize findings into unified output
✓ Identify gaps and spawn follow-up agents
✓ Make final decisions on conflicting findings
✓ Write the final report/output

✗ Do all the research directly
✗ Duplicate subagent work
✗ Delegate final synthesis to subagents
```

### Synthesis Pattern

```markdown
1. Collect all subagent results
2. Identify themes and patterns
3. Resolve conflicts (note when sources disagree)
4. Prioritize findings by impact
5. Create unified output (not just concatenation)
6. Add leader analysis and recommendations
```

---

## Queue Structure

The work queue in LOOP_STATE.md follows this structure:

### Standard Format (Backwards Compatible)

```markdown
## Work Queue

### S0 — Critical (Do Now)
| ID | Item | Status | Added | Notes |
|----|------|--------|-------|-------|
| Q001 | Fix SQL injection in login | pending | iter-1 | Security scan finding |

### S1 — High (Before Features)
| ID | Item | Status | Added | Notes |
|----|------|--------|-------|-------|
| Q002 | Add input validation | in-progress | iter-1 | From security audit |

### S2 — Medium (Do Soon)
| ID | Item | Status | Added | Notes |
|----|------|--------|-------|-------|
| Q003 | Improve error messages | pending | iter-2 | UX feedback |

### S3 — Low (When Convenient)
| ID | Item | Status | Added | Notes |
|----|------|--------|-------|-------|
| Q004 | Add loading spinners | deferred | iter-1 | Nice to have |
```

### Enhanced Format (With Dependencies)

```markdown
## Work Queue

### Tasks
| ID | Item | Sev | Status | Blocked By | Blocks | Owner | Added |
|----|------|-----|--------|------------|--------|-------|-------|
| Q001 | Design auth schema | S1 | complete | — | Q002, Q003 | — | iter-1 |
| Q002 | Implement auth service | S1 | in_progress | — | Q004 | main | iter-1 |
| Q003 | Create auth middleware | S1 | pending | — | Q004 | — | iter-1 |
| Q004 | Integration tests | S2 | blocked | Q002, Q003 | — | — | iter-1 |

### Dependency Graph
Q001 ──┬──▶ Q002 ──┬──▶ Q004
       │          │
       └──▶ Q003 ─┘
```

---

## Task Dependencies

### Adding Dependencies

When creating a task with dependencies:

```
"Add task: Write integration tests"
"  - Severity: S2"
"  - Depends on: Q002 (service), Q003 (middleware)"

Result:
| Q004 | Write integration tests | S2 | blocked | Q002, Q003 | — | — |
```

### Automatic Unblocking

When a task completes:

```
Q002 completes → Q002 removed from Q004's Blocked By list
Q003 completes → Q003 removed from Q004's Blocked By list
Q004's Blocked By now empty → Status changes to "pending"
```

### Dependency Commands

```
"Q004 depends on Q002"
"Q002 blocks Q004"
"Remove dependency Q001 from Q002"
"What's blocking Q004?"
"What does Q001 unblock?"
```

---

## Status Values

| Status | Meaning | Selectable |
|--------|---------|------------|
| `pending` | Ready to work, no blockers | Yes |
| `in_progress` | Currently being worked | No (already claimed) |
| `blocked` | Has unresolved dependencies | No (wait for blockers) |
| `complete` | Finished | No |
| `deferred` | Explicitly postponed | No (skipped) |

### Status Transitions

```
pending ──▶ in_progress ──▶ complete
    │                           │
    │                           └──▶ triggers unblocking
    │
    └──▶ deferred (explicit skip)

blocked ──▶ pending (when blockers complete)
```

### Enhancements (If Time)
| ID | Item | Status | Added | Notes |
|----|------|--------|-------|-------|
| Q005 | Dark mode support | backlog | iter-1 | Future consideration |
```

---

## Queue Commands

### View Queue
```
"Show work queue"
"What's in the queue?"
"Queue status"
```

**Output:**
```
Work Queue Status (Iteration 5)
═══════════════════════════════

S0 Critical: 0 items ✓
S1 High:     1 item (1 in progress)
S2 Medium:   3 items (2 pending, 1 complete)
S3 Low:      2 items (deferred)
Backlog:     4 items

Next up: Q002 - Add input validation (S1, in-progress)

Progress: ████████░░░░ 42% complete
```

### Add Item
```
"Add to queue: [description]"
"Queue: [description] as S2"
```

**Process:**
1. Classify severity (or use specified)
2. Assign next queue ID
3. Add to appropriate section
4. Update LOOP_STATE.md

### Remove/Complete Item
```
"Complete Q002"
"Remove Q005 from queue"
"Mark Q003 done"
```

**Process:**
1. Find item by ID
2. Update status to complete/removed
3. Move to completed section
4. Update LOOP_STATE.md

### Reprioritize
```
"Promote Q003 to S1"
"Demote Q002 to S2"
"Move Q005 to S0"
```

**Process:**
1. Find item by ID
2. Remove from current section
3. Add to new severity section
4. Update LOOP_STATE.md

### Defer Item
```
"Defer Q004"
"Skip Q005 for now"
```

**Process:**
1. Mark status as "deferred"
2. Add deferral note
3. Keep in queue but don't count toward completion

---

## Queue Visualization

### Compact View
```
Queue: [S0: 0] [S1: 2] [S2: 5] [S3: 3] | 10 total, 4 complete
```

### Progress Bar
```
S0 ░░░░░░░░░░ 0/0
S1 ████████░░ 8/10
S2 ██████░░░░ 6/10
S3 ██░░░░░░░░ 2/10
   ──────────────
   16/30 (53%)
```

### Kanban View
```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│   PENDING   │ IN PROGRESS │   BLOCKED   │  COMPLETE   │
├─────────────┼─────────────┼─────────────┼─────────────┤
│ Q003 (S2)   │ Q002 (S1)   │ Q007 (S2)   │ Q001 (S0)   │
│ Q004 (S3)   │ Q006 (S2)   │             │ Q005 (S2)   │
│ Q008 (S3)   │             │             │ Q009 (S3)   │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

---

## Automatic Queue Population

### From Agent Reports

When agents complete analysis:
```
security-analyst report:
├── S0: SQL injection found → Add Q001
├── S1: Missing auth check → Add Q002
└── S2: Weak password policy → Add Q003
```

### From Test Failures

When tests fail:
```
Test failure: user.login.test.js
├── Extract failing test name
├── Create queue item
└── Assign severity based on test type
```

### From Code Review

When code-reviewer finds issues:
```
Code review findings:
├── Must fix → S1
├── Should fix → S2
└── Consider → S3
```

---

## Queue Rules

### Ordering (Enhanced with Dependencies)

**Priority Order:**
1. Tasks with `pending` status only (skip `blocked`)
2. S0 severity first (critical)
3. Within same severity: Tasks that unblock the most others first
4. Within same unblock count: Oldest task first

```
SELECTION ALGORITHM:
├── Filter: status = pending (excludes blocked, complete, deferred)
├── Sort by: severity (S0 > S1 > S2 > S3)
├── Tiebreaker 1: blocks_count descending (unblock more = higher priority)
├── Tiebreaker 2: added_date ascending (older = higher priority)
└── Select: First item in sorted list
```

**Example:**
| ID | Severity | Status | Blocks | Selection Order |
|----|----------|--------|--------|-----------------|
| Q005 | S1 | pending | Q007, Q008, Q009 | 1st (S1 + 3 unblocks) |
| Q006 | S1 | pending | Q008 | 2nd (S1 + 1 unblock) |
| Q003 | S2 | pending | — | 3rd (S2, no unblocks) |
| Q004 | S1 | blocked | Q009 | Skip (blocked) |

### Legacy Ordering (Backwards Compatible)
1. S0 items block ALL other work
2. S1 items block new features
3. S2/S3 items processed by priority within severity
4. Enhancements only after queue empty

### Completion Criteria
- Queue is "empty" when:
  - All S0 items complete
  - All S1 items complete
  - S2/S3 items either complete or explicitly deferred
  - No blocked items remain (dependencies satisfied or deferred)

### Item Lifecycle (Enhanced)
```
pending → in_progress → complete → [triggers unblocking]
                                        │
                                        ▼
                            blocked items check:
                            - Remove completed task from Blocked By
                            - If Blocked By empty → status = pending

pending → deferred (skip this iteration)
pending → removed (no longer needed)
blocked → pending (when all blockers complete)
```

### On Task Completion (Dependency Processing)

```
Task Q001 marked complete:
├── Find tasks where Q001 is in Blocked By list
│   └── Found: Q002, Q003
├── For each found task:
│   ├── Remove Q001 from Blocked By
│   └── If Blocked By now empty → status = pending
├── Update LOOP_STATE.md
└── Log: "Q001 complete. Unblocked: Q002, Q003"
```

---

## Integration with Loop

### Start of Iteration
```
1. Read LOOP_STATE.md
2. Parse work queue
3. Display current status
4. Pick highest priority pending item
5. Mark as in-progress
```

### During Work
```
1. Work on current item
2. If blocked, mark blocked + reason
3. If new issues found, add to queue
4. When done, mark complete
```

### End of Iteration
```
1. Update all item statuses
2. Recalculate progress
3. Check completion criteria
4. Save LOOP_STATE.md
```

---

## Example Session

```
User: Show work queue

Queue Status (Iteration 3 of /loop)
════════════════════════════════════

S0 Critical: 0 ✓
S1 High:     2 (1 pending, 1 in-progress)
S2 Medium:   4 (3 pending, 1 complete)
S3 Low:      2 (deferred)

Current: Q002 - Add input validation (S1)
Next:    Q003 - Fix error handling (S1)

[████████████░░░░░░░░] 35%

---

User: Add to queue: Update API rate limiting as S2

Added: Q009 - Update API rate limiting
Severity: S2 (Medium)
Status: pending
Position: 5th in S2 queue

---

User: Promote Q009 to S1

Moved: Q009 - Update API rate limiting
From: S2 (Medium)
To:   S1 (High)
New position: 3rd in S1 queue

---

User: Complete Q002

Completed: Q002 - Add input validation
Duration: 2 iterations
Moving to: Q003 - Fix error handling (S1)

Progress: [████████████████░░░░] 42%
```

---

## Queue File Format

In LOOP_STATE.md:

```markdown
## Work Queue

Last Updated: 2026-01-29T10:30:00Z
Iteration: 5

### Summary
- Total: 12 items
- Complete: 5 items (42%)
- Blocked: 1 item
- Deferred: 2 items

### Queue Items

#### S0 - Critical
(empty)

#### S1 - High
- [x] Q001: Fix SQL injection (complete, iter-2)
- [ ] Q002: Add input validation (in-progress, iter-3)
- [ ] Q003: Fix error handling (pending)

#### S2 - Medium
- [x] Q004: Improve error messages (complete, iter-4)
- [ ] Q005: Add retry logic (pending)
- [ ] Q006: Update API docs (pending)
- [ ] Q007: Refactor auth module (blocked: needs Q002)

#### S3 - Low
- [ ] Q008: Add loading spinners (deferred)
- [ ] Q009: Improve logging (deferred)

#### Backlog
- [ ] Q010: Dark mode support
- [ ] Q011: Export to CSV
```

---

## Swarm Mode Integration

When swarm mode is active, the queue gains additional tracking:

### Enhanced Queue Format (Swarm)

```markdown
## Work Queue (Swarm Mode)

### Swarm Status
- Mode: Active
- Workers: 3 (2 busy, 1 claiming)
- Pool: 8 tasks (3 complete, 2 in-progress, 3 pending)

### Tasks
| ID | Item | Sev | Status | Blocked By | Blocks | Claimed By |
|----|------|-----|--------|------------|--------|------------|
| Q001 | Review auth.ts | S2 | complete | — | — | W1 |
| Q002 | Review api.ts | S2 | in_progress | — | Q005 | W2 |
| Q003 | Security audit | S1 | in_progress | — | Q005 | W3 |
| Q004 | Review utils.ts | S2 | pending | — | — | — |
| Q005 | Integration tests | S2 | blocked | Q002, Q003 | — | — |
```

### Worker Claiming

```
Worker W2 requests next task:
├── Filter: status = pending, claimed_by = null
├── Apply dependency filter: blocked_by empty
├── Apply severity + unblock priority
├── Claim: Q004 (highest priority unclaimed)
├── Update: Q004.claimed_by = W2, Q004.status = in_progress
└── Return Q004 to worker
```

### Concurrent Access

File-based state with atomic updates:
```
Worker claims:
├── Read LOOP_STATE.md
├── Check claim lock (5 second expiry)
├── If lock exists → Wait and retry
├── Acquire lock
├── Claim task
├── Release lock
└── Proceed with task
```

---

## Related Skills

| Skill | Integration |
|-------|-------------|
| `task-dependencies` | Provides blockedBy/blocks logic |
| `swarm-mode` | Enables self-claiming workers |
| `result-synthesizer` | Merges findings from workers |
| `autonomous-loop` | Uses queue for work selection |
| `parallel-agents` | Populates queue from agent findings |
| `evaluator-optimizer` | Refine outputs through feedback loops |
| `smart-context` | Manages context budget during synthesis |

---

## Configuration

### In .claude/settings.json

```json
{
  "orchestration": {
    "queue": {
      "dependenciesEnabled": true,
      "prioritizeUnblockers": true,
      "swarmClaimTimeout": 5000,
      "autoUnblock": true
    }
  }
}
```
