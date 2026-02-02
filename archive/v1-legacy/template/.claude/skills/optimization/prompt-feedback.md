---
name: prompt-feedback
description: Self-improvement feedback loop for prompts - learn from failures and successes
version: 1.0.0
triggers:
  - "prompt failed"
  - "prompt worked well"
  - "improve this prompt"
  - "prompt feedback"
model: sonnet
tags: [optimization, quality, self-improvement]
context: inherit
---

# Prompt Feedback Loop

Continuous improvement system for prompts based on real-world usage.

---

## Purpose

Prompts should improve over time through:
- Recording failures and their causes
- Noting successes and what made them work
- Identifying patterns across feedback
- Suggesting and implementing improvements

---

## Feedback Recording

### When a Prompt Fails

```markdown
## Prompt Failure Report

**Prompt:** [name]
**Date:** [timestamp]
**Task:** [what was attempted]

### What Happened
[Description of the failure]

### Expected Outcome
[What should have happened]

### Actual Outcome
[What actually happened]

### Root Cause Analysis
- [ ] Unclear instructions
- [ ] Missing context
- [ ] Wrong model selection
- [ ] Insufficient examples
- [ ] Edge case not handled
- [ ] Conflicting rules
- [ ] Other: [describe]

### Suggested Fix
[How to improve the prompt]

### Severity
- [ ] Critical: Prompt unusable
- [ ] High: Major functionality broken
- [ ] Medium: Works but suboptimal
- [ ] Low: Minor improvement opportunity
```

### When a Prompt Succeeds

```markdown
## Prompt Success Report

**Prompt:** [name]
**Date:** [timestamp]
**Task:** [what was accomplished]

### What Worked Well
[Description of success factors]

### Key Elements
- [Element 1 that contributed to success]
- [Element 2]

### Replicable Pattern
[Pattern that could apply to other prompts]
```

---

## Feedback Storage

Store feedback in `.claude/feedback/`:

```
.claude/feedback/
├── failures/
│   ├── 2026-01-29-code-review-failure.md
│   └── 2026-01-28-security-scan-edge-case.md
├── successes/
│   ├── 2026-01-29-refactor-perfect.md
│   └── 2026-01-27-deploy-smooth.md
└── improvements/
    ├── code-review-v2.md
    └── security-scan-edge-cases.md
```

---

## Pattern Analysis

Periodically analyze feedback for patterns:

### Common Failure Patterns

| Pattern | Frequency | Prompts Affected | Fix |
|---------|-----------|------------------|-----|
| Missing examples | High | code-review, security | Add few-shot examples |
| Ambiguous output | Medium | test, docs | Add output_format |
| Edge cases | Medium | all | Add error_handling |

### Success Patterns

| Pattern | Effect | Prompts Using It |
|---------|--------|------------------|
| Step-by-step thinking | Better analysis | security, refactor |
| Explicit output format | Consistent results | review, test |
| Few-shot examples | Fewer errors | all classification |

---

## Improvement Workflow

### 1. Collect Feedback
```
During usage:
├── Note when prompts fail
├── Note when prompts excel
├── Record context and details
└── Tag with root cause
```

### 2. Analyze Patterns
```
Weekly review:
├── Group failures by root cause
├── Identify most impactful issues
├── Find common success elements
└── Prioritize improvements
```

### 3. Implement Fixes
```
For each high-priority issue:
├── Draft improved prompt
├── Test with known failure cases
├── Verify success cases still work
├── Update prompt with version bump
└── Document change in changelog
```

### 4. Validate Improvements
```
After changes:
├── Monitor for regressions
├── Track new failure rates
├── Compare to baseline
└── Iterate if needed
```

---

## Auto-Improvement Triggers

The system suggests improvements when:

| Trigger | Action |
|---------|--------|
| Same prompt fails 3+ times | Flag for review |
| New edge case discovered | Add to error handling |
| User provides correction | Learn preference |
| Pattern succeeds repeatedly | Apply to similar prompts |

---

## Improvement Checklist

Before applying a prompt improvement:

- [ ] Root cause understood
- [ ] Fix addresses root cause (not symptoms)
- [ ] Tested with original failure case
- [ ] Tested with existing success cases
- [ ] No regressions introduced
- [ ] Version bumped
- [ ] Changelog updated
- [ ] Feedback entry linked

---

## Integration with Platform

### With Autonomous Loop

```
If prompt produces poor result:
├── Loop detects quality issue
├── Records in feedback/failures/
├── Adjusts approach for this session
└── Flags for prompt improvement review
```

### With Session History

```
Feedback informs session history:
├── "This prompt struggled with X"
├── "Workaround: do Y instead"
└── "TODO: improve prompt Z"
```

### With Metrics

```
Track prompt effectiveness:
├── Success rate per prompt
├── Average iterations to success
├── Most common failure modes
└── Improvement over time
```

---

## Example Improvement Cycle

### Failure Detected
```
Prompt: /secure
Task: Scan authentication module
Failure: Missed SQL injection in parameterized query edge case

Root Cause: Examples only showed basic injection
Fix Needed: Add edge case examples
```

### Improvement Made
```markdown
<!-- Added to /secure -->
<examples>
<example>
<input>
// Edge case: Parameterized but with dynamic table name
const table = req.query.table;
const query = `SELECT * FROM ${table} WHERE id = $1`;
db.query(query, [id]);
</input>
<output>
**S0 - SQL Injection (Edge Case)**

While the WHERE clause is parameterized, the table name
is directly interpolated, allowing injection.

Fix: Whitelist allowed table names
```javascript
const ALLOWED_TABLES = ['users', 'orders', 'products'];
if (!ALLOWED_TABLES.includes(table)) {
  throw new Error('Invalid table');
}
```
</output>
</example>
</examples>
```

### Validation
```
Tested with:
✓ Original failure case (now detected)
✓ Basic injection cases (still detected)
✓ Safe parameterized queries (no false positives)
✓ Other edge cases (XSS, etc. still work)
```

### Result
```
/secure v1.2.0 → v1.3.0
- Added edge case examples for SQL injection
- Now detects dynamic table/column name injection
- Feedback: 2026-01-29-secure-edge-case.md
```

---

## Commands

```
"Record prompt failure for [prompt name]"
→ Opens failure report template

"Record prompt success for [prompt name]"
→ Opens success report template

"Analyze prompt feedback"
→ Reviews recent feedback, identifies patterns

"Improve prompt [name] based on feedback"
→ Drafts improvement based on failure patterns

"Show prompt health"
→ Success/failure rates for all prompts
```
