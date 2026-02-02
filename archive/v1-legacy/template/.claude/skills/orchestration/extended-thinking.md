---
name: extended-thinking
description: Enable deep analysis mode (ultrathink) for complex problems
model: opus
---

# Extended Thinking ("Ultrathink")

Enable deep analysis mode for complex problems requiring thorough reasoning.

## Overview

Extended thinking activates a deeper analysis mode where Claude:
- Takes more time to reason through problems
- Considers more edge cases and alternatives
- Produces more thorough analysis
- Uses structured thinking patterns

---

## When to Use

### Ideal Scenarios

| Scenario | Why Extended Thinking |
|----------|----------------------|
| Security audits | Need to think through attack vectors |
| Architecture decisions | Multiple trade-offs to consider |
| Complex debugging | Root cause may be non-obvious |
| Incident analysis | Need thorough understanding |
| Risk assessment | Must consider many factors |

### Trigger Phrases

Say any of these to activate:
- "ultrathink this"
- "think deeply about"
- "analyze thoroughly"
- "extended analysis"
- "take your time analyzing"

### Commands with --ultrathink

Some commands support the `--ultrathink` flag:

```
/secure --ultrathink
/audit-blueprint --ultrathink
/postmortem --ultrathink
/assess --ultrathink
```

---

## What Changes

### Standard Analysis

```markdown
**Quick Assessment:** [Problem]

Findings:
1. Issue A
2. Issue B

Recommendation: Fix A first.
```

### Extended Thinking Analysis

```markdown
## Deep Analysis: [Problem]

### Initial Assessment
[What we observe on the surface]

### Exploring Hypotheses

**Hypothesis 1: [Description]**
- Supporting evidence: ...
- Counter evidence: ...
- Likelihood: Medium

**Hypothesis 2: [Description]**
- Supporting evidence: ...
- Counter evidence: ...
- Likelihood: High

### Edge Cases Considered
- What if [edge case 1]?
- What if [edge case 2]?
- What if [edge case 3]?

### Trade-off Analysis

| Option | Pros | Cons | Risk |
|--------|------|------|------|
| A | ... | ... | Low |
| B | ... | ... | Medium |

### Second-Order Effects
[Consequences of consequences]

### Confidence Assessment
- High confidence: [aspects]
- Medium confidence: [aspects]
- Low confidence: [aspects]

### Recommended Approach
[Justified recommendation with reasoning chain]

### Alternatives if Wrong
[Fallback plans]
```

---

## Usage Examples

### Example 1: Security Analysis

**Standard:**
```
/secure src/auth

Finding: SQL injection possible in userQuery
Severity: S0
Fix: Use parameterized query
```

**With ultrathink:**
```
/secure src/auth --ultrathink

## Deep Security Analysis: src/auth

### Attack Surface Mapping
1. Login endpoint - accepts user input
2. Token validation - parses JWT
3. Session management - cookie handling
4. Password reset - email generation

### Vulnerability Analysis

**SQL Injection (S0)**
- Location: userQuery.ts:45
- Attack vector: email parameter
- Exploitation difficulty: Low
- Impact: Full database access
- Remediation: Parameterized queries
- Verification: Add SQL injection tests

**JWT Algorithm Confusion (S1)**
- Potential for 'none' algorithm
- Current check may be bypassable
- Recommendation: Explicit algorithm whitelist

### Attack Scenarios
1. Attacker sends malicious email...
2. If JWT validation bypassed...
3. Combined with...

### Defense in Depth Recommendations
1. Input validation layer
2. Parameterized queries
3. JWT strict validation
4. Rate limiting
5. Audit logging

### Confidence: High
Based on static analysis and known patterns.
```

### Example 2: Architecture Decision

**Standard:**
```
Should we use microservices?

Microservices add complexity but offer scalability.
For a team of 5, probably stick with monolith.
```

**With ultrathink:**
```
Ultrathink: Should we use microservices?

## Architecture Analysis: Microservices vs Monolith

### Current Context Assessment
- Team size: 5 developers
- Current codebase: 50K LOC
- Deployment: Single Kubernetes pod
- Growth projection: 2x team in 12 months

### Option Analysis

**Option A: Continue Monolith**
Pros:
- Simpler deployment (current)
- Easier debugging
- Lower operational overhead
- Faster feature development

Cons:
- Scaling limitations eventually
- Deployment = entire system
- Technology lock-in

Risk assessment: Low short-term, Medium long-term

**Option B: Microservices Now**
Pros:
- Independent scaling
- Technology flexibility
- Team autonomy (when team grows)

Cons:
- Significant migration effort (~3 months)
- Operational complexity
- Distributed debugging
- Network latency considerations

Risk assessment: High short-term, Low long-term

**Option C: Modular Monolith**
Pros:
- Clear boundaries without distribution
- Easy extraction later
- Simpler than microservices
- Team can learn patterns

Cons:
- Discipline required
- Not as flexible as microservices
- Still single deployment

Risk assessment: Low short-term, Low-Medium long-term

### Decision Framework

| Factor | Weight | Monolith | Microservices | Modular |
|--------|--------|----------|---------------|---------|
| Dev velocity | 30% | 9/10 | 5/10 | 8/10 |
| Scalability | 20% | 5/10 | 9/10 | 6/10 |
| Operations | 25% | 9/10 | 4/10 | 8/10 |
| Future flex | 25% | 4/10 | 9/10 | 7/10 |
| **Weighted** | | **6.9** | **6.5** | **7.3** |

### Recommendation

**Modular Monolith** with clear domain boundaries.

Reasoning:
1. Team of 5 can't sustain microservices ops overhead
2. Modular design enables future extraction
3. Faster iteration now, optionality later
4. Lower risk during critical growth phase

### Implementation Path
1. Define domain boundaries (Week 1)
2. Establish module interfaces (Week 2)
3. Gradually enforce boundaries (Ongoing)
4. Extract first service when: [criteria]

### Review Trigger
Reassess when:
- Team > 15 people
- Need to scale single domain 10x
- Deployment frequency needs differ significantly
```

---

## Configuration

### Enabling Extended Thinking

In skill frontmatter:
```yaml
extended_thinking: true
```

In conversation:
```
Use extended thinking for this analysis
```

### Model Recommendation

Extended thinking works best with:
- **Opus**: Complex reasoning, security, architecture
- **Sonnet**: Standard deep analysis
- **Haiku**: Not recommended for extended thinking

---

## Best Practices

### Do

- Use for high-stakes decisions
- Allow extra time for analysis
- Request specific aspects to analyze deeply
- Ask follow-up questions

### Don't

- Use for simple lookups
- Rush the analysis
- Skip the reasoning (just want answer)
- Use for every question (expensive)

---

## Integration

### With Commands

Commands that benefit from extended thinking:

| Command | Use Case |
|---------|----------|
| `/secure --ultrathink` | Deep security audit |
| `/audit-blueprint --ultrathink` | Thorough plan validation |
| `/postmortem --ultrathink` | Complete incident analysis |
| `/assess --ultrathink` | Comprehensive codebase audit |

### With Skills

Skills with `extended_thinking: true`:
- `smart-context.md` - For complex context decisions
- `health-dashboard.md` - For detailed health analysis
- `cross-project-patterns.md` - For pattern analysis
