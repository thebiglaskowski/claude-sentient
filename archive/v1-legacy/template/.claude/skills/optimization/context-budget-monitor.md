---
name: context-budget-monitor
description: Monitors context window usage and prevents bloat by suggesting sub-agent spawning
version: 1.0.0
triggers:
  - "context getting large"
  - "running out of context"
  - "should I spawn an agent"
  - "context budget"
model: haiku
tags: [optimization, context, agents]
---

# Context Budget Monitor

Prevents context window bloat by tracking usage and proactively suggesting when to spawn sub-agents.

## Why This Matters

> "A single context window got bloated fast because there was too much information in its working memory making it lose focus."

When context windows fill up:
- Model loses focus on the current task
- Earlier instructions get "forgotten"
- Quality of output degrades
- Risk of compaction losing important state

---

## Context Budget Guidelines

### Estimated Token Budgets

| Content Type | Typical Tokens | Budget % |
|--------------|----------------|----------|
| System prompt + CLAUDE.md | ~3,000 | 15% |
| Current task context | ~4,000 | 20% |
| Code files (active) | ~6,000 | 30% |
| Conversation history | ~4,000 | 20% |
| Tool results | ~3,000 | 15% |
| **Total Safe Budget** | ~20,000 | 100% |

### Warning Thresholds

| Level | Estimated Usage | Action |
|-------|-----------------|--------|
| Green | < 50% | Continue normally |
| Yellow | 50-70% | Consider spawning sub-agents |
| Orange | 70-85% | Spawn sub-agents for new tasks |
| Red | > 85% | Stop adding context, delegate everything |

---

## When to Spawn Sub-Agents

### Spawn When:

1. **Task is self-contained**
   - Code review of a specific module
   - Security audit of a component
   - Test writing for a feature
   - Documentation generation

2. **Task requires deep focus**
   - Complex algorithm implementation
   - Debugging intricate issues
   - Performance optimization

3. **Task has clear inputs/outputs**
   - Input: Files to analyze
   - Output: Findings, code, or report

4. **Multiple independent tasks exist**
   - Parallel agents can work simultaneously
   - Results synthesized afterward

### Don't Spawn When:

1. **Task requires conversation history**
   - Needs context from earlier discussion
   - Building on previous decisions

2. **Task is quick**
   - Simple file edits
   - Quick lookups
   - Single commands

3. **Task requires human interaction**
   - Clarifying questions needed
   - Approval required mid-task

---

## Context-Saving Strategies

### Strategy 1: Delegate to Sub-Agents

```
Instead of:
├── Read 10 files into main context
├── Analyze all of them
└── Context bloated

Do:
├── Spawn code-reviewer agent
├── Agent reads and analyzes in isolation
├── Returns summary findings only
└── Main context stays lean
```

### Strategy 2: Incremental File Reading

```
Instead of:
├── Read entire codebase at once
└── Context overwhelmed

Do:
├── Read only files needed for current task
├── Release files when done
├── Read next set for next task
```

### Strategy 3: Summarize Before Storing

```
Instead of:
├── Store full tool output
└── Context fills with verbose results

Do:
├── Extract key findings
├── Summarize results
├── Store only what's needed
```

### Strategy 4: Use State Files

```
Instead of:
├── Keep everything in conversation
└── Context fills with history

Do:
├── Write decisions to DECISIONS_LOG.md
├── Write state to LOOP_STATE.md
├── Reference files instead of repeating
```

---

## Monitoring Checklist

During long-running tasks, periodically check:

```
CONTEXT HEALTH CHECK:
├── How many files are currently loaded?
│   └── If > 5 large files → Consider releasing some
├── How deep is the conversation?
│   └── If > 20 turns → Consider summarizing or spawning
├── Are there pending tasks that could be parallelized?
│   └── If yes → Spawn sub-agents
├── Is the same information being repeated?
│   └── If yes → Write to state file, reference it
└── Is focus being lost on the main goal?
    └── If yes → Context is likely bloated
```

---

## Integration with Autonomous Loop

### Phase 2.5: META-COGNITION (Enhanced)

```
META-COGNITION PHASE:
├── Review capability inventory
├── Evaluate current situation
├── **CHECK CONTEXT BUDGET** ← NEW
│   ├── Estimate current usage
│   ├── If Yellow/Orange/Red → plan delegation
│   └── Identify tasks suitable for sub-agents
├── Consider specialist agents
├── Load relevant rules
└── Decide on strategy
```

### Before Each Major Task

```
PRE-TASK CHECK:
├── Is this task self-contained? → Consider sub-agent
├── Will this add significant context? → Consider sub-agent
├── Can this run in parallel with other work? → Spawn background agent
└── Proceed with awareness of budget
```

---

## Example: Context-Aware Task Handling

### Scenario: Review and refactor 5 modules

**Without Context Monitoring:**
```
1. Load module 1, review, refactor
2. Load module 2, review, refactor
3. Load module 3, review, refactor
4. Load module 4... context bloated, quality drops
5. Load module 5... model loses focus
```

**With Context Monitoring:**
```
1. Assess: 5 modules, each self-contained
2. Strategy: Spawn parallel agents
3. Execute:
   ├── Spawn code-reviewer for module 1 (background)
   ├── Spawn code-reviewer for module 2 (background)
   ├── Spawn code-reviewer for module 3 (background)
   ├── Spawn code-reviewer for module 4 (background)
   └── Spawn code-reviewer for module 5 (background)
4. Synthesize: Collect all findings
5. Main context: Stays lean, high quality maintained
```

---

## Usage

### Automatic Integration
This skill integrates with:
- `meta-cognition` (context check during strategy selection)
- `autonomous-loop` (pre-task context assessment)
- `parallel-agents` (delegation decisions)

### Manual Invocation
```
"Check my context budget"
"Should I spawn a sub-agent for this?"
"How can I reduce context usage?"
```

---

## Key Principle

> **Lean context = Focused agent = Higher quality output**

When in doubt, spawn a sub-agent. The orchestrator pattern exists precisely to keep each agent focused on a specific task with minimal context overhead.
