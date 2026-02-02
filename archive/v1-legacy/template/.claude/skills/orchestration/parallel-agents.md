---
name: parallel-agents
description: Coordinate parallel agent execution for comprehensive analysis and faster results
version: 3.0.0
triggers:
  - "parallel"
  - "comprehensive"
  - "full audit"
  - "all checks"
  - "spawn agents"
model: sonnet
tags: [orchestration, agents, parallelism]
context: inherit
---

# Parallel Agents

Coordinate multiple specialized agents running in parallel for comprehensive analysis and faster results. Manages agent lifecycle, prevents conflicts, and synthesizes combined results.

---

## When to Use Parallel Agents

### High-Value Scenarios
```
Full Codebase Audit:
├── security-analyst → Security findings
├── code-reviewer → Quality findings
├── test-engineer → Coverage gaps
└── performance-optimizer → Performance issues

Pre-Release Check:
├── security-analyst → Security sign-off
├── test-engineer → Test verification
├── documentation-writer → Docs complete
└── accessibility-expert → A11y compliance

Complex Feature Review:
├── code-reviewer → Code quality
├── security-analyst → Security implications
├── ui-ux-expert → UX review
└── database-expert → Data model review
```

### Cost-Benefit Analysis
```
Parallel is worth it when:
✓ Task requires multiple expertise areas
✓ Combined analysis improves accuracy
✓ Speed is important (parallel faster than sequential)
✓ Findings from one agent inform another

Sequential is better when:
✗ Single-focus task
✗ Budget constraints
✗ Simple verification needed
✗ High context dependency between checks
```

---

## Parallel Execution Model

```
┌─────────────────────────────────────────────────────────────────┐
│                    PARALLEL AGENT EXECUTION                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  User Request: "Full security and quality audit"                │
│                          │                                       │
│                          ▼                                       │
│                  ┌───────────────┐                              │
│                  │  Coordinator  │                              │
│                  └───────┬───────┘                              │
│          ┌───────────────┼───────────────┐                      │
│          │               │               │                       │
│          ▼               ▼               ▼                       │
│   ┌─────────────┐ ┌─────────────┐ ┌─────────────┐              │
│   │  Security   │ │    Code     │ │    Test     │              │
│   │  Analyst    │ │  Reviewer   │ │  Engineer   │              │
│   └──────┬──────┘ └──────┬──────┘ └──────┬──────┘              │
│          │               │               │                       │
│          ▼               ▼               ▼                       │
│   ┌─────────────┐ ┌─────────────┐ ┌─────────────┐              │
│   │  Findings   │ │  Findings   │ │  Findings   │              │
│   └──────┬──────┘ └──────┬──────┘ └──────┬──────┘              │
│          │               │               │                       │
│          └───────────────┼───────────────┘                      │
│                          ▼                                       │
│                  ┌───────────────┐                              │
│                  │  Synthesizer  │                              │
│                  └───────┬───────┘                              │
│                          ▼                                       │
│                  ┌───────────────┐                              │
│                  │ Unified Queue │                              │
│                  └───────────────┘                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Agent Coordination Patterns

### Pattern 1: Full Coverage Audit
```
Purpose: Comprehensive codebase analysis
Agents: security-analyst, code-reviewer, test-engineer

Coordination:
1. All agents analyze same codebase
2. No dependencies between agents
3. Run fully in parallel
4. Synthesize all findings at end

Expected Output:
├── Combined severity counts
├── Unified work queue
├── Cross-cutting concerns identified
└── Priority-sorted remediation plan
```

### Pattern 2: Pipeline Analysis
```
Purpose: Deep-dive with informed second pass
Agents: code-reviewer → security-analyst

Coordination:
1. code-reviewer identifies hot spots
2. security-analyst focuses on flagged areas
3. Sequential but informed

Expected Output:
├── Targeted security analysis
├── Higher signal-to-noise
└── More efficient token usage
```

### Pattern 3: Specialized Parallel
```
Purpose: Multi-domain feature review
Agents: ui-ux-expert + database-expert + security-analyst

Coordination:
1. Each focuses on their domain
2. Share common findings
3. Identify cross-domain issues

Expected Output:
├── Domain-specific findings
├── Integration concerns
└── Complete feature assessment
```

---

## Agent Lifecycle Management

### State Tracking
```json
{
  "agents": {
    "agent_001": {
      "type": "security-analyst",
      "status": "running",
      "started": "2024-01-15T10:00:00Z",
      "scope": "src/auth/**"
    },
    "agent_002": {
      "type": "code-reviewer",
      "status": "completed",
      "started": "2024-01-15T10:00:00Z",
      "completed": "2024-01-15T10:02:30Z",
      "findings": 12
    }
  },
  "total_active": 1,
  "total_completed": 1
}
```

### Lifecycle Events
```
SubagentStart → agent-tracker.py records agent
             → Updates active count
             → Provides coordination hints

SubagentStop → agent-synthesizer.py processes results
            → Extracts findings
            → Updates state
            → Triggers synthesis when all complete
```

---

## Scope Management

### Avoiding Overlap
```
Bad: Both agents analyze everything
├── Wasted tokens
├── Duplicate findings
└── Longer execution

Good: Scoped analysis
├── security-analyst: "Focus on auth, input validation, crypto"
├── code-reviewer: "Focus on patterns, complexity, maintainability"
├── test-engineer: "Focus on coverage, test quality"
└── Clear boundaries, complementary findings
```

### Scope Assignment
```yaml
full-audit:
  security-analyst:
    focus: "Security vulnerabilities, OWASP, auth"
    skip: "Code style, naming, documentation"

  code-reviewer:
    focus: "Code quality, patterns, complexity"
    skip: "Security (handled by security-analyst)"

  test-engineer:
    focus: "Test coverage, test quality, edge cases"
    skip: "Implementation details"
```

---

## Result Synthesis

### Merging Findings
```
Agent Results:
├── security-analyst: 3 S1, 5 S2
├── code-reviewer: 8 S2, 12 S3
└── test-engineer: 2 S1, 4 S2

Synthesis Process:
1. Collect all findings
2. Deduplicate (same file:line)
3. Merge severity (take highest)
4. Cross-reference (security + quality on same code)
5. Build unified queue

Unified Queue:
├── S1: 5 items (3 security, 2 testing)
├── S2: 15 items (5 security, 8 quality, 2 testing)
└── S3: 12 items (all quality)
```

### Synthesis Output
```markdown
## Parallel Analysis Complete

### Agent Summary
| Agent | Duration | Findings | S0 | S1 | S2 | S3 |
|-------|----------|----------|----|----|----|----|
| security-analyst | 45s | 8 | 0 | 3 | 5 | 0 |
| code-reviewer | 62s | 20 | 0 | 0 | 8 | 12 |
| test-engineer | 38s | 6 | 0 | 2 | 4 | 0 |

### Cross-Cutting Concerns
- Auth module flagged by both security + quality
- Payment handler needs security + tests

### Unified Work Queue (Priority Order)
1. [S1-SEC] Fix auth bypass in login.ts
2. [S1-SEC] Add rate limiting to API
3. [S1-TEST] Add tests for payment flow
4. [S2-SEC] Improve input validation
...
```

---

## Parallel Commands

### Explicit Parallel Execution
```
"Run parallel audit with security-analyst, code-reviewer, test-engineer"
→ Spawns all three agents
→ Tracks progress
→ Synthesizes on completion
```

### Scoped Parallel
```
"Parallel security and quality review of src/auth/**"
→ Both agents focus on auth directory
→ Combined findings for auth module
```

### Add Agent to Running Parallel
```
"Also run test-engineer"
→ Adds to current parallel session
→ Synthesizer waits for new agent
```

### Check Parallel Status
```
"Agent status" or "!agents"
→ Shows all running agents
→ Shows completed agents
→ Shows pending synthesis
```

---

## Integration with Hooks

### agent-tracker.py (SubagentStart)
```
Records agent start
├── Assigns agent ID
├── Tracks scope and type
├── Updates active count
└── Provides parallel hints
```

### agent-synthesizer.py (SubagentStop)
```
Processes completion
├── Records completion time
├── Extracts findings
├── Checks if all agents done
├── Triggers synthesis if complete
└── Builds unified queue
```

---

## Best Practices

### Do
```
✓ Assign clear, non-overlapping scopes
✓ Use parallel for multi-domain tasks
✓ Let synthesizer merge findings
✓ Trust agent specialization
✓ Review unified queue before acting
```

### Don't
```
✗ Run same agent type multiple times
✗ Overlap scopes without reason
✗ Act on individual agent findings before synthesis
✗ Spawn more than 5 agents (diminishing returns)
✗ Use parallel for simple, single-focus tasks
```

---

## Configuration

```json
{
  "parallelAgents": {
    "enabled": true,
    "maxConcurrent": 5,
    "defaultScope": "full",
    "autoSynthesize": true,
    "presets": {
      "full-audit": ["security-analyst", "code-reviewer", "test-engineer"],
      "pre-release": ["security-analyst", "test-engineer", "documentation-writer"],
      "ui-review": ["ui-ux-expert", "accessibility-expert", "seo-expert"]
    }
  }
}
```

---

## Example Session

```
User: "Full audit of the codebase before release"

Coordinator: Starting parallel audit with preset: pre-release
├── Spawning: security-analyst (scope: security concerns)
├── Spawning: test-engineer (scope: test coverage)
├── Spawning: documentation-writer (scope: docs completeness)

[45 seconds later]

Synthesizer: All agents complete
├── security-analyst: 5 findings (1 S1, 4 S2)
├── test-engineer: 8 findings (2 S1, 6 S2)
├── documentation-writer: 3 findings (0 S1, 3 S2)

Unified Queue (13 items):
├── S1: 3 items (security: 1, testing: 2)
├── S2: 10 items (security: 4, testing: 6)

Ready to proceed with fixes in priority order.
```
