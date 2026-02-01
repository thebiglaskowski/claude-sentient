---
name: classify
version: 1.0.0
description: Classify task type and determine orchestration strategy
order: 1
timeout: 30000
retryable: false

subscribes:
  - event: loop.iteration.start
    handler: onIterationStart

publishes:
  - loop.task.classified

output:
  classification:
    type: object
    properties:
      type:
        enum: [depth-first, breadth-first, straightforward]
      complexity:
        enum: [simple, medium, complex]
      subagentCount:
        type: integer
      orchestrationMode:
        enum: [standard, swarm, pipeline]

tags:
  - orchestration
  - classification
---

# Phase 1: Classify

Analyze the task and determine the optimal execution strategy.

## Purpose

Before loading context or doing any work, understand:
1. What kind of task is this?
2. How complex is it?
3. How should we orchestrate execution?

## Process

### Step 1: Parse Task Intent

Extract signals from the task description:

```
SIGNALS:
├── Action Verbs: implement, fix, review, refactor, test, document
├── Scope Indicators: file, module, codebase, entire
├── Complexity Markers: simple, complex, comprehensive, thorough
├── Mode Hints: parallel, swarm, sequential
└── Constraints: security, performance, deadline
```

### Step 2: Determine Classification Type

| Signals | Classification |
|---------|----------------|
| Single file, simple change, quick fix | `straightforward` |
| Deep analysis, complex problem, one focus | `depth-first` |
| Many files, review, comprehensive, parallel | `breadth-first` |

### Step 3: Calculate Complexity

```
complexity = assess_complexity(task)

IF file_count <= 2:
  complexity = "simple"
ELSE IF file_count <= 10:
  complexity = "medium"
ELSE:
  complexity = "complex"

# Adjust for task type
IF task.includes("security") OR task.includes("audit"):
  complexity = increase(complexity)
```

### Step 4: Determine Subagent Count

```
IF classification == "straightforward":
  subagentCount = 0

ELSE IF classification == "depth-first":
  subagentCount = 1  # Single specialist

ELSE IF classification == "breadth-first":
  base = ceil(task_count / 3)
  subagentCount = clamp(base, 3, 20)

  # Adjust by complexity
  IF complexity == "simple":
    subagentCount = min(subagentCount, 5)
  ELSE IF complexity == "complex":
    subagentCount = max(subagentCount, 5)
```

### Step 5: Select Orchestration Mode

```
IF classification == "straightforward":
  mode = "standard"

ELSE IF classification == "depth-first":
  mode = "standard"

ELSE IF classification == "breadth-first":
  IF has_dependencies(tasks):
    mode = "pipeline"
  ELSE IF task_count > 5:
    mode = "swarm"
  ELSE:
    mode = "standard"
```

### Step 6: Emit Classification

```json
{
  "event": "loop.task.classified",
  "payload": {
    "type": "breadth-first",
    "complexity": "medium",
    "subagentCount": 5,
    "orchestrationMode": "swarm",
    "signals": {
      "actionVerb": "review",
      "scope": "codebase",
      "markers": ["comprehensive"]
    }
  }
}
```

## Skip Conditions

This phase can be skipped when:
- Resuming with existing classification
- Classification provided in flags

```yaml
skipConditions:
  - condition: state.classification != null AND flags.resume
    reason: Resuming with existing classification
  - condition: flags.orchestrationMode != null
    reason: Mode provided via flags
```

## Output

Updates `state.classification`:

```json
{
  "classification": {
    "type": "breadth-first",
    "complexity": "medium",
    "subagentCount": 5,
    "orchestrationMode": "swarm"
  }
}
```

## Decision Matrix

| Task Description | Type | Complexity | Agents | Mode |
|------------------|------|------------|--------|------|
| "fix typo in README" | straightforward | simple | 0 | standard |
| "debug authentication issue" | depth-first | medium | 1 | standard |
| "review all API endpoints" | breadth-first | complex | 8 | swarm |
| "implement feature with tests" | depth-first | medium | 1 | standard |
| "refactor database layer" | depth-first | complex | 1 | standard |
| "security audit codebase" | breadth-first | complex | 10 | pipeline |
