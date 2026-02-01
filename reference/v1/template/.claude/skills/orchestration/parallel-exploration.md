---
name: parallel-exploration
description: Run multiple isolated explorations simultaneously
argument-hint: "<topics to explore>"
context: fork
model: sonnet
---

# Parallel Exploration

Run multiple isolated research tasks simultaneously for efficient exploration.

## Overview

When you need to research multiple topics or compare approaches, parallel exploration spawns multiple subagents that work simultaneously. Each agent:

- Works in complete isolation
- Explores its assigned topic deeply
- Returns a focused summary
- Doesn't see other agents' work

---

## When to Use

### Ideal Scenarios

1. **Comparing implementation approaches**
   ```
   In parallel, research:
   - REST vs GraphQL for our use case
   - PostgreSQL vs MongoDB for this data
   - JWT vs Session-based auth
   ```

2. **Multi-area analysis**
   ```
   Simultaneously investigate:
   - Frontend architecture
   - Backend structure
   - Database schema
   ```

3. **Broad codebase survey**
   ```
   Explore in parallel:
   - Authentication system
   - API layer
   - Data access patterns
   ```

4. **Technology evaluation**
   ```
   Research simultaneously:
   - React Query
   - SWR
   - Apollo Client
   ```

---

## Usage Patterns

### Pattern 1: Compare Approaches

```
Compare in parallel:
1. Approach A: Microservices architecture
2. Approach B: Modular monolith
3. Approach C: Serverless functions

For each, evaluate: complexity, cost, scalability, team fit
```

### Pattern 2: Multi-Area Survey

```
Explore simultaneously:
- Security: How is auth handled?
- Performance: Where are the bottlenecks?
- Testing: What's the test coverage?
```

### Pattern 3: Technology Research

```
In parallel, research these libraries:
1. Zod - for validation
2. Yup - for validation
3. io-ts - for validation

Compare: API design, TypeScript support, performance, community
```

---

## Execution Model

### Parallel Spawn

```
┌─────────────────────────────────────────────┐
│              Main Conversation              │
│                     │                       │
│        ┌───────────┼───────────┐            │
│        ▼           ▼           ▼            │
│   ┌─────────┐ ┌─────────┐ ┌─────────┐       │
│   │ Agent 1 │ │ Agent 2 │ │ Agent 3 │       │
│   │ Topic A │ │ Topic B │ │ Topic C │       │
│   └────┬────┘ └────┬────┘ └────┬────┘       │
│        │           │           │            │
│        ▼           ▼           ▼            │
│   [Summary A] [Summary B] [Summary C]       │
│        │           │           │            │
│        └───────────┼───────────┘            │
│                    ▼                        │
│         ┌─────────────────────┐             │
│         │  Combined Summary   │             │
│         │  + Comparison       │             │
│         └─────────────────────┘             │
└─────────────────────────────────────────────┘
```

### Isolation Guarantee

Each agent:
- Cannot see other agents' findings
- Has fresh context
- Works independently
- Returns only its summary

---

## Output Format

### Individual Agent Summaries

```markdown
## Agent 1: [Topic A]

### Findings
- Point 1
- Point 2

### Key Files
- file1.ts
- file2.ts

### Assessment
[Brief assessment]
```

### Combined Report

```markdown
## Parallel Exploration Summary

### Topic A Findings
[Summary from Agent 1]

### Topic B Findings
[Summary from Agent 2]

### Topic C Findings
[Summary from Agent 3]

---

## Comparison

| Aspect | Topic A | Topic B | Topic C |
|--------|---------|---------|---------|
| Complexity | Low | Medium | High |
| Time to implement | 2 days | 5 days | 2 weeks |
| Risk | Low | Medium | Low |

## Recommendation

Based on the parallel analysis, [Topic B] is recommended because:
1. Reason 1
2. Reason 2
```

---

## Configuration

### Parallel Settings

```yaml
parallel_exploration:
  max_agents: 5              # Max concurrent agents
  agent_model: "sonnet"      # Model for agents
  timeout_per_agent: 120     # Seconds per agent
  combine_summaries: true    # Auto-combine results
```

### Resource Allocation

| Agents | Recommended Model |
|--------|-------------------|
| 2-3 | sonnet |
| 4-5 | haiku |
| 1 (deep) | opus |

---

## Examples

### Example 1: Architecture Comparison

**Request:**
```
In parallel, evaluate:
1. Microservices - separate services per domain
2. Modular monolith - single app, clear boundaries
3. Hybrid - core monolith + specific microservices

Consider: team size (5), deployment complexity, development speed
```

**Returns:**
```markdown
## Parallel Analysis: Architecture Options

### Microservices
- ✅ Independent scaling
- ✅ Technology flexibility
- ❌ Operational overhead high for team of 5
- ❌ Network complexity
- **Score for team: 6/10**

### Modular Monolith
- ✅ Simple deployment
- ✅ Easy debugging
- ✅ Good for team size
- ❌ Must be disciplined about boundaries
- **Score for team: 8/10**

### Hybrid
- ✅ Flexibility where needed
- ✅ Simpler for core
- ⚠️ Requires clear criteria for extraction
- **Score for team: 7/10**

## Recommendation

**Modular Monolith** is recommended for:
- Team of 5 (easier to manage)
- Faster initial development
- Can extract services later if needed
```

### Example 2: Library Comparison

**Request:**
```
Research in parallel for form validation:
1. Zod
2. Yup
3. Valibot

Evaluate: bundle size, TypeScript support, API ergonomics
```

**Returns:**
```markdown
## Library Comparison: Form Validation

| Criteria | Zod | Yup | Valibot |
|----------|-----|-----|---------|
| Bundle size | 12KB | 25KB | 6KB |
| TypeScript | Excellent | Good | Excellent |
| API | Declarative | Method chain | Declarative |
| Tree-shaking | Good | Poor | Excellent |
| Community | Growing | Established | New |

### Zod
Best for: TypeScript-first projects
Pros: Great inference, good ecosystem
Cons: Larger than Valibot

### Yup
Best for: Existing projects already using it
Pros: Mature, lots of examples
Cons: Larger size, weaker types

### Valibot
Best for: Bundle-size sensitive apps
Pros: Smallest, tree-shakeable
Cons: Smaller community, newer

## Recommendation
**Zod** for most TypeScript projects (best balance)
**Valibot** if bundle size is critical
```

---

## Best Practices

### Structuring Parallel Tasks

1. **Make tasks independent** - No agent should need another's output
2. **Similar scope** - Each task should take roughly the same time
3. **Clear deliverables** - Specify what each agent should return
4. **Comparison criteria** - Define how results will be compared

### Avoiding Issues

- Don't spawn more than 5 agents (diminishing returns)
- Don't use for tasks that need iteration
- Don't expect agents to coordinate
- Don't include implementation in exploration tasks
