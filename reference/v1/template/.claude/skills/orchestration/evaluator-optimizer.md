---
name: evaluator-optimizer
description: Refine outputs through evaluate-improve feedback loops until quality threshold met
version: 1.0.0
triggers:
  - "refine this"
  - "improve until"
  - "iterate on"
  - "not good enough"
  - "keep improving"
  - "evaluate and fix"
model: sonnet
tags: [orchestration, quality, feedback, refinement, iteration]
context: inherit
---

# Evaluator-Optimizer Pattern v1.0

A feedback loop where one agent produces output, another evaluates it, and refinement continues until quality threshold is met.

**Based on:** Anthropic Cookbook patterns/agents/evaluator_optimizer.ipynb

---

## Overview

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Producer   │────▶│  Evaluator  │────▶│  Decision   │
│   Agent     │     │   Agent     │     │   Point     │
└─────────────┘     └─────────────┘     └──────┬──────┘
      ▲                                        │
      │                                        │
      │         ┌──────────────────────────────┤
      │         │                              │
      │         ▼                              ▼
      │   ┌─────────────┐              ┌─────────────┐
      └───│  Optimizer  │              │   Accept    │
          │   Agent     │              │   Output    │
          └─────────────┘              └─────────────┘
```

---

## When to Use

| Scenario | Why Evaluator-Optimizer |
|----------|-------------------------|
| Code doesn't pass tests | Evaluate failures → Optimize until green |
| Output quality uncertain | Score output → Refine until score > threshold |
| Multiple quality criteria | Check each criterion → Fix violations |
| User rejected output | Capture feedback → Improve based on it |
| Complex generation | Generate draft → Critique → Refine iteratively |

---

## Components

### 1. Producer Agent

Generates the initial output or refinements.

```markdown
**Role:** Generate [output type]

**Instructions:**
- Produce [specific deliverable]
- If this is a refinement round, incorporate previous feedback
- Focus on addressing specific issues raised by evaluator

**Output:** [The generated content]
```

### 2. Evaluator Agent

Assesses output against quality criteria.

```markdown
**Role:** Evaluate [output type] against quality criteria

**Criteria:**
1. [Criterion 1] — How to assess, what's acceptable
2. [Criterion 2] — How to assess, what's acceptable
3. [Criterion 3] — How to assess, what's acceptable

**Output Format:**
{
  "score": 0-100,
  "passed": true/false,
  "issues": [
    {
      "criterion": "name",
      "severity": "S0/S1/S2/S3",
      "issue": "description",
      "suggestion": "how to fix"
    }
  ],
  "strengths": ["what's working well"]
}
```

### 3. Optimizer Agent

Transforms evaluation feedback into specific improvements.

```markdown
**Role:** Improve [output] based on evaluator feedback

**Input:**
- Original output
- Evaluator issues and suggestions

**Instructions:**
- Address each issue in priority order (S0 first)
- Preserve strengths identified by evaluator
- Make minimal changes to fix issues (don't over-revise)

**Output:** Improved version of the content
```

---

## Loop Configuration

### Thresholds

```markdown
## Evaluator-Optimizer Settings

| Setting | Value | Description |
|---------|-------|-------------|
| Quality Threshold | 80 | Minimum score to accept |
| Max Iterations | 5 | Stop after N refinement rounds |
| S0 Must Fix | true | Never accept with S0 issues |
| S1 Must Fix | true | Never accept with S1 issues |
| Improvement Threshold | 5 | Minimum score gain per iteration |
```

### Exit Conditions

The loop exits when ANY of these are met:

```markdown
1. ✅ Score >= Quality Threshold AND no S0/S1 issues
2. ⏹️ Max iterations reached
3. 📉 Score not improving (< Improvement Threshold for 2 rounds)
4. 🛑 Evaluator returns "unfixable" status
```

---

## Implementation Pattern

### Loop State Tracking

```markdown
## Evaluator-Optimizer State

**Target:** [What's being refined]
**Quality Threshold:** 80
**Current Iteration:** 3 of 5

### Iteration History
| Round | Score | S0 | S1 | S2 | Change | Status |
|-------|-------|----|----|----|---------|----|
| 1 | 45 | 2 | 3 | 5 | — | Continue |
| 2 | 62 | 0 | 2 | 4 | +17 | Continue |
| 3 | 78 | 0 | 1 | 2 | +16 | Continue |

### Current Issues
- [S1] Input validation missing on email field
- [S2] Could add rate limiting
- [S2] Error messages could be more specific

### Next Refinement Focus
1. Add email validation
2. Consider rate limiting
```

### Execution Flow

```markdown
## Round [N]

### Step 1: Produce/Refine
[Producer/Optimizer generates output]

### Step 2: Evaluate
Score: [X]/100
Issues: [list]
Strengths: [list]

### Step 3: Decision
□ Score >= 80 AND no S0/S1? → ACCEPT
□ Iteration < max AND improving? → CONTINUE
□ Otherwise → STOP (return best attempt)

### Step 4: (If continuing)
Feed issues to optimizer for next round
```

---

## Use Cases

### 1. Code Until Tests Pass

```markdown
**Producer:** Write code for [feature]
**Evaluator:** Run test suite, report failures
**Optimizer:** Fix failing tests

**Exit:** All tests pass OR max iterations

Loop:
1. Produce: Write auth middleware
2. Evaluate: Run `npm test` → 3 failures
3. Optimize: Fix the 3 failures
4. Evaluate: Run `npm test` → 1 failure
5. Optimize: Fix the 1 failure
6. Evaluate: Run `npm test` → All pass ✅
```

### 2. Documentation Quality

```markdown
**Producer:** Write API documentation
**Evaluator:** Check completeness, accuracy, clarity

**Criteria:**
- All endpoints documented
- Request/response examples present
- Error codes explained
- No broken links

**Exit:** Score >= 90 (docs need high quality)
```

### 3. Security Review Remediation

```markdown
**Producer:** Implement security fixes
**Evaluator:** Security audit agent
**Optimizer:** Address audit findings

**Exit:** No S0/S1 security issues
```

### 4. Prompt Refinement

```markdown
**Producer:** Write prompt for [task]
**Evaluator:** Test prompt against sample inputs
**Optimizer:** Improve based on test results

**Criteria:**
- Correct output format
- Handles edge cases
- Consistent results
- No hallucinations

**Exit:** Score >= 85 AND passes all test cases
```

---

## Integration with Quality Gates

The evaluator-optimizer can wrap existing quality gates:

```markdown
Quality Gate Integration:

1. Run standard quality gate (CODE_REVIEW, SECURITY_AUDIT, etc.)
2. If gate fails → Enter evaluator-optimizer loop
3. Evaluator = the quality gate
4. Optimizer = targeted fix agent
5. Loop until gate passes
```

---

## Commands

### Start Refinement Loop

```
"Refine this code until tests pass"
"Improve the documentation until it scores above 80"
"Keep iterating on security fixes until no S0/S1 issues"
```

### Check Loop Status

```
"What's the refinement status?"
"How many iterations so far?"
"What issues remain?"
```

### Force Exit

```
"Stop refining, use current best"
"Accept current output"
"Skip remaining iterations"
```

---

## Configuration

### In .claude/settings.json

```json
{
  "orchestration": {
    "evaluatorOptimizer": {
      "defaultThreshold": 80,
      "maxIterations": 5,
      "requireS0Fix": true,
      "requireS1Fix": true,
      "minImprovementPerRound": 5,
      "verboseLogging": false
    }
  }
}
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| No exit condition | Infinite loop | Always set max iterations |
| Threshold too high | Never exits | Use realistic thresholds |
| Vague evaluation criteria | Inconsistent scoring | Define specific, measurable criteria |
| Full rewrite each round | Loses good parts | Minimal targeted fixes |
| Ignoring score trends | Misses plateaus | Exit if not improving |

---

## Related Skills

| Skill | Integration |
|-------|-------------|
| `autonomous-loop` | Triggers evaluator-optimizer when gates fail |
| `quality-gates` | Provides evaluation criteria |
| `result-synthesizer` | Merges multiple evaluation rounds |
| `prompt-feedback` | Captures refinement patterns for learning |
