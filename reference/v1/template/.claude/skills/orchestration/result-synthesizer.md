---
name: result-synthesizer
description: Combine and synthesize findings from multiple agents into unified recommendations
version: 2.0.0
triggers:
  - "synthesize results"
  - "combine findings"
  - "merge agent reports"
  - "unified recommendations"
model: sonnet
tags: [agents, synthesis, coordination, workflow]
context: inherit
---

# Result Synthesizer

Combine findings from multiple agents into a unified, prioritized set of recommendations and work items.

---

## Purpose

When multiple agents analyze the same codebase:
- security-analyst finds security issues
- code-reviewer finds quality issues
- test-engineer finds coverage gaps
- accessibility-expert finds a11y issues

These findings may overlap, conflict, or have different priorities. The synthesizer creates a unified view.

---

## Synthesis Process

### Step 1: Collect Agent Reports

Gather all agent outputs:
```
Inputs:
├── security-analyst report
├── code-reviewer report
├── test-engineer report
└── [any other agent reports]
```

### Step 2: Normalize Findings

Convert all findings to standard format:
```markdown
## Finding
- **ID:** [auto-generated]
- **Source:** [agent name]
- **Severity:** S0/S1/S2/S3
- **Category:** security/quality/testing/performance/accessibility
- **Location:** [file:line or general area]
- **Description:** [what's wrong]
- **Impact:** [why it matters]
- **Recommendation:** [how to fix]
```

### Step 3: Deduplicate

Identify findings that refer to same issue:
```
Example:
├── security-analyst: "Missing input validation on /api/login"
├── code-reviewer: "No sanitization in login endpoint"
└── → MERGE: Same issue, keep security-analyst (higher authority)
```

### Step 4: Resolve Conflicts

When agents disagree:
```
Conflict Resolution Priority:
1. Security concerns trump convenience
2. Correctness trumps performance
3. User safety trumps developer experience
4. Explicit rules trump agent opinions
5. Higher severity trumps lower

Example:
├── code-reviewer: "Simplify by removing input validation" (S3)
├── security-analyst: "Input validation is required" (S1)
└── → KEEP: Security recommendation (higher priority)
```

### Step 5: Prioritize

Order findings by:
1. Severity (S0 → S1 → S2 → S3)
2. Dependencies (fixes that unblock others first)
3. Effort vs. impact (quick wins early)
4. Category grouping (related fixes together)

### Step 6: Generate Work Queue

Convert to actionable work items:
```markdown
## Synthesized Work Queue

### S0 - Critical (Fix Immediately)
| ID | Finding | Source | Action |
|----|---------|--------|--------|
| SYN-001 | SQL injection in login | security-analyst | Parameterize query |

### S1 - High (Fix Before Proceeding)
| ID | Finding | Source | Action |
|----|---------|--------|--------|
| SYN-002 | Missing auth check | security-analyst | Add middleware |
| SYN-003 | No error boundaries | code-reviewer | Add React error boundary |

### S2 - Medium (Fix Soon)
...
```

---

## Output Format

### Synthesis Report

```markdown
# Agent Synthesis Report

**Generated:** [timestamp]
**Agents Consulted:** security-analyst, code-reviewer, test-engineer
**Files Analyzed:** 42
**Total Findings:** 23
**After Deduplication:** 18

---

## Summary

| Category | S0 | S1 | S2 | S3 | Total |
|----------|----|----|----|----|-------|
| Security | 1 | 3 | 2 | 1 | 7 |
| Quality | 0 | 2 | 4 | 3 | 9 |
| Testing | 0 | 1 | 1 | 0 | 2 |
| **Total** | **1** | **6** | **7** | **4** | **18** |

---

## Critical Path

These must be addressed in order:

1. **SYN-001** (S0): Fix SQL injection
   - Blocks: All other work
   - Effort: 1 hour

2. **SYN-002** (S1): Add authentication middleware
   - Blocks: SYN-005, SYN-008
   - Effort: 2 hours

3. **SYN-003** (S1): Add error boundaries
   - Blocks: None
   - Effort: 1 hour

---

## Findings by Category

### Security (7 findings)

#### S0 - Critical
**SYN-001: SQL Injection in Login**
- Source: security-analyst
- Location: src/api/auth.js:45
- Description: User input directly interpolated into SQL query
- Impact: Full database compromise possible
- Fix: Use parameterized queries
```javascript
// Before (vulnerable)
db.query(`SELECT * FROM users WHERE email = '${email}'`)

// After (safe)
db.query('SELECT * FROM users WHERE email = $1', [email])
```

#### S1 - High
...

### Quality (9 findings)
...

### Testing (2 findings)
...

---

## Deduplication Log

| Kept | Merged From | Reason |
|------|-------------|--------|
| SYN-002 (security) | QUA-007 (quality) | Same issue, security takes precedence |
| SYN-005 (quality) | SEC-012 (security) | Quality finding more specific |

---

## Conflict Resolution Log

| Winner | Loser | Reason |
|--------|-------|--------|
| SEC-003: Keep validation | QUA-015: Remove validation | Security > convenience |

---

## Recommended Work Order

1. Fix all S0 items (SYN-001)
2. Fix S1 security items (SYN-002, SYN-004)
3. Fix S1 quality items (SYN-003, SYN-006)
4. Fix S1 testing items (SYN-007)
5. Proceed with S2 items by category
6. Address S3 items as time permits

**Estimated Total Effort:** 8-12 hours
```

---

## Integration with Loop

### Auto-Synthesis Trigger

After parallel agent execution:
```
/loop with agents

1. Spawn security-analyst, code-reviewer, test-engineer in parallel
2. Wait for all to complete
3. AUTO-TRIGGER: result-synthesizer
4. Synthesized queue becomes work queue
5. Continue loop with unified priorities
```

### Manual Synthesis

```
User: Synthesize results from recent agent runs

[Reads agent reports from context]
[Performs synthesis]
[Outputs unified report]
[Optionally updates LOOP_STATE.md work queue]
```

---

## Handling Contradictions

### Example: Performance vs Security

```
Agent A (code-reviewer):
"Cache user permissions for performance"

Agent B (security-analyst):
"Don't cache permissions - stale cache = security risk"

Resolution:
├── Security concern is valid (S1)
├── Performance concern is valid (S2)
├── Synthesis: "Implement short-TTL permission cache (5 min)
│              with immediate invalidation on permission change"
└── Satisfies both with acceptable tradeoff
```

### Example: DRY vs Clarity

```
Agent A: "Extract common code to reduce duplication"
Agent B: "Keep code inline for better readability"

Resolution:
├── If duplication is 3+ places → Extract (DRY wins)
├── If duplication is 2 places → Keep inline (clarity wins)
└── Document decision in synthesis notes
```

---

## Best Practices

1. **Always synthesize before acting** - Don't cherry-pick from individual reports
2. **Document deduplication** - Track what was merged and why
3. **Explain conflicts** - Future maintainers need context
4. **Order matters** - Dependencies should drive work order
5. **Keep agent attributions** - Know which expert said what
6. **Review synthesis** - Human should validate critical decisions
