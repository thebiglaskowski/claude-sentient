---
name: model-routing
description: Automatically route tasks to appropriate models using Task tool subagents
---

# Model Routing (Functional)

This skill provides ACTUAL model routing using the Task tool's subagent capabilities.

## How Model Routing Actually Works

The ONLY way to use different models in Claude Code is via the **Task tool**:

```javascript
Task({
  prompt: "...",
  subagent_type: "Bash",  // or other agent type
  model: "haiku"          // THIS IS THE KEY - specifies model
})
```

## Routing Guidelines

When processing user requests, route to appropriate models:

### Use Haiku (Fast, Cheap) For:
```
- File listing and simple searches
- Formatting and linting
- Simple git operations
- Status checks
- Generating boilerplate
- Simple text transformations

Example - spawn Haiku subagent:
Task tool with model: "haiku"
```

### Use Sonnet (Balanced) For:
```
- Code review
- Test writing
- Bug fixing
- Feature implementation
- Documentation generation
- Refactoring

Example - spawn Sonnet subagent:
Task tool with model: "sonnet"
```

### Use Opus (Deep Reasoning) For:
```
- Security audits
- Architecture decisions
- Complex debugging
- Incident analysis
- Planning and strategy
- Anything requiring deep analysis

Stay in current Opus context OR:
Task tool with model: "opus"
```

## Implementation Pattern

When a skill/command should use a specific model, it must explicitly spawn a subagent:

```markdown
## For Haiku Tasks

When this skill activates, spawn a Haiku subagent:

Use the Task tool with:
- subagent_type: "general-purpose" (or appropriate type)
- model: "haiku"
- prompt: [the actual task]

This ensures Haiku is actually used, not just recommended.
```

## Cost Optimization

| Task Type | Model | Relative Cost |
|-----------|-------|---------------|
| Simple queries | Haiku | 1x |
| Standard dev | Sonnet | 10x |
| Deep analysis | Opus | 30x |

**Routing properly can reduce costs by 80%+ for routine tasks.**

## Active Routing Commands

When user says:
- "quick check" / "simple task" → Spawn Haiku subagent
- "review this" / "fix this" → Spawn Sonnet subagent
- "deep analysis" / "security audit" → Use Opus (or spawn Opus subagent)

## Important

The `model:` field in YAML frontmatter is **metadata only**.
To actually use a different model, you MUST use the Task tool with the `model` parameter.
