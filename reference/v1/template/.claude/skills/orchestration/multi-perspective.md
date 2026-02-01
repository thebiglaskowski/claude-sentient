---
name: multi-perspective
description: Analyze decisions from multiple expert viewpoints simultaneously
model: opus
version: 1.0.0
tags: [orchestration, analysis, decision-making]
---

# Multi-Perspective Analysis

Analyze complex decisions from multiple expert viewpoints simultaneously to catch blind spots and make better choices.

## Description

This skill implements **Role Stacking** - instead of a single perspective, the AI assumes multiple expert roles simultaneously, creating an internal "debate" that surfaces considerations a single viewpoint would miss.

Research shows 60% improvement on complex tasks when using multi-perspective analysis.

Triggers on: "analyze from multiple perspectives", "what would experts say", "pros and cons", "trade-offs", architectural decisions, technology choices

---

## When to Use

### Ideal Scenarios

| Scenario | Why Multi-Perspective |
|----------|----------------------|
| Architecture decisions | Different stakeholders have different needs |
| Technology choices | Trade-offs aren't obvious from one angle |
| Code review | Security, performance, and maintainability conflict |
| Feature prioritization | Business, UX, and engineering see differently |
| Incident analysis | Multiple factors usually contribute |
| Risk assessment | Different experts spot different risks |

### Standard Perspectives

| Perspective | Focus | Asks |
|-------------|-------|------|
| **Architect** | System design, scalability | "How does this affect the whole system?" |
| **Security Engineer** | Vulnerabilities, threats | "How could this be exploited?" |
| **Performance Engineer** | Speed, resources | "What's the performance impact?" |
| **UX Designer** | User experience | "How does this affect users?" |
| **DevOps Engineer** | Operations, reliability | "How do we deploy and monitor this?" |
| **Business Analyst** | Value, cost, ROI | "What's the business impact?" |
| **QA Engineer** | Testing, edge cases | "How do we verify this works?" |
| **Junior Developer** | Clarity, maintainability | "Can someone new understand this?" |

---

## Analysis Framework

### Three-Perspective Minimum

For any significant decision, analyze from at least three perspectives:

```markdown
## Multi-Perspective Analysis: [Decision]

### Perspective 1: [Role]
**Focus:** [What this role cares about]

**Assessment:**
[Analysis from this viewpoint]

**Concerns:**
- [Specific concern 1]
- [Specific concern 2]

**Recommendation:**
[What this role would advise]

---

### Perspective 2: [Role]
**Focus:** [What this role cares about]

**Assessment:**
[Analysis from this viewpoint]

**Concerns:**
- [Specific concern 1]
- [Specific concern 2]

**Recommendation:**
[What this role would advise]

---

### Perspective 3: [Role]
**Focus:** [What this role cares about]

**Assessment:**
[Analysis from this viewpoint]

**Concerns:**
- [Specific concern 1]
- [Specific concern 2]

**Recommendation:**
[What this role would advise]

---

## Synthesis

### Points of Agreement
[Where all perspectives align]

### Points of Tension
[Where perspectives conflict and why]

### Balanced Recommendation
[Decision that accounts for all viewpoints]

### Trade-offs Accepted
[What we're consciously sacrificing and why]
```

---

## Perspective Combinations

### For Architecture Decisions
1. **Systems Architect** - Overall design, patterns
2. **Security Engineer** - Attack surface, vulnerabilities
3. **DevOps Engineer** - Deployment, operations

### For Code Changes
1. **Senior Developer** - Code quality, patterns
2. **Security Engineer** - Vulnerabilities
3. **Performance Engineer** - Efficiency

### For Feature Decisions
1. **Product Manager** - User value, business goals
2. **UX Designer** - User experience
3. **Tech Lead** - Technical feasibility

### For Incident Response
1. **SRE** - System stability, recovery
2. **Security Engineer** - Breach implications
3. **Customer Success** - User impact

---

## Examples

### Example 1: Database Choice

**Question:** "Should we use PostgreSQL or MongoDB for our new service?"

```markdown
## Multi-Perspective Analysis: Database Selection

### Perspective 1: Data Architect
**Focus:** Data modeling, query patterns, consistency

**Assessment:**
- PostgreSQL: Strong ACID guarantees, complex queries, mature tooling
- MongoDB: Flexible schema, horizontal scaling, document model

**Concerns:**
- Our data has relationships (users → orders → items) favoring relational
- But schema may evolve rapidly in early stages

**Recommendation:** PostgreSQL with JSONB columns for flexible fields

---

### Perspective 2: DevOps Engineer
**Focus:** Operations, scaling, maintenance

**Assessment:**
- PostgreSQL: Well-understood ops, many hosting options, predictable performance
- MongoDB: More complex sharding, replica set management

**Concerns:**
- Team has PostgreSQL experience, none with MongoDB
- MongoDB ops burden higher for small team

**Recommendation:** PostgreSQL - easier to operate with current team

---

### Perspective 3: Performance Engineer
**Focus:** Speed, resource usage, scalability

**Assessment:**
- PostgreSQL: Excellent read performance with proper indexing, connection pooling needed
- MongoDB: Better write throughput, but our workload is read-heavy

**Concerns:**
- Current scale doesn't require MongoDB's horizontal scaling
- PostgreSQL can handle 10x current load with proper setup

**Recommendation:** PostgreSQL - matches our read-heavy workload

---

## Synthesis

### Points of Agreement
All perspectives favor PostgreSQL for this use case.

### Points of Tension
- Schema flexibility (MongoDB) vs. data integrity (PostgreSQL)
- Resolved by using JSONB for flexible fields

### Balanced Recommendation
**PostgreSQL** with:
- JSONB columns for evolving schema parts
- Proper indexing strategy
- Connection pooling (PgBouncer)

### Trade-offs Accepted
- Less schema flexibility (mitigated by JSONB)
- Vertical scaling limits (acceptable for 3-year horizon)
```

### Example 2: Code Review

**Code:** New authentication middleware

```markdown
## Multi-Perspective Review: Auth Middleware

### Perspective 1: Security Engineer
**Focus:** Vulnerabilities, attack vectors

**Assessment:**
- JWT validation looks correct
- Token expiry checked properly
-

**Concerns:**
- No rate limiting on auth endpoints (brute force risk)
- Error messages reveal too much ("user not found" vs "invalid credentials")
- Missing audit logging for failed attempts

**Recommendation:** Add rate limiting, generic error messages, audit logging

---

### Perspective 2: Performance Engineer
**Focus:** Latency, resource usage

**Assessment:**
- JWT verification is synchronous (OK, fast operation)
- Database lookup on every request

**Concerns:**
- User lookup on every request adds 5-10ms latency
- Could cache user data with short TTL

**Recommendation:** Add Redis cache for user lookups, 5-minute TTL

---

### Perspective 3: Maintainability (Junior Dev Lens)
**Focus:** Readability, debugging

**Assessment:**
- Code is well-structured
- Good separation of concerns

**Concerns:**
- Magic numbers (token expiry: 3600)
- No comments explaining security decisions
- Error handling could be clearer

**Recommendation:** Extract constants, add security decision comments

---

## Synthesis

### Agreed Changes
1. Add rate limiting (security)
2. Cache user lookups (performance)
3. Extract magic numbers (maintainability)

### Prioritized Recommendations
| Priority | Change | Perspective |
|----------|--------|-------------|
| S1 | Rate limiting | Security |
| S1 | Generic error messages | Security |
| S2 | User caching | Performance |
| S2 | Audit logging | Security |
| S3 | Extract constants | Maintainability |
```

---

## Integration

### With Commands

Commands that benefit from multi-perspective:

```
/cc-review --perspectives security,performance,maintainability
/cc-audit-blueprint --multi-perspective
/cc-assess --perspectives architect,security,devops
```

### With Agents

Can spawn multiple agents for deeper analysis:

```
Spawn security-analyst, performance-optimizer, and code-reviewer
to analyze this change from their perspectives.
```

---

## Configuration

### Default Perspectives by Task

| Task Type | Default Perspectives |
|-----------|---------------------|
| Code review | Security, Performance, Maintainability |
| Architecture | Architect, Security, DevOps |
| Feature | Product, UX, Engineering |
| Incident | SRE, Security, Customer |

### Custom Perspectives

```
Analyze this from the perspectives of:
1. A first-time user
2. A power user
3. An accessibility advocate
```

---

## Best Practices

### Do
- Use at least 3 perspectives for major decisions
- Choose perspectives relevant to the decision
- Look for conflicts between perspectives
- Synthesize into actionable recommendations

### Don't
- Use for trivial decisions (overkill)
- Pick perspectives that all agree (no value)
- Skip synthesis (perspectives alone aren't enough)
- Ignore minority perspectives (they catch blind spots)
