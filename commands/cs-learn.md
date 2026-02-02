---
description: Save a learning, decision, or pattern to project memory
argument-hint: <type> <title> <content>
allowed-tools: Read, Edit, Write, mcp__memory__create_entities, mcp__memory__create_relations, mcp__memory__add_observations
---

# /cs-learn

Save important learnings to `.claude/rules/learnings.md` for future sessions.

## Arguments

- `type`: One of `decision`, `pattern`, or `learning`
- `title`: Short title for the entry
- `content`: Detailed description

## Behavior

### 1. Save to File (learnings.md)

1. Read the current `.claude/rules/learnings.md` file (create if missing)
2. Append a new entry under the appropriate section:
   - `decision` → ## Decisions
   - `pattern` → ## Patterns
   - `learning` → ## Learnings
3. Format the entry with today's date:
   ```markdown
   ### YYYY-MM-DD: {title}
   - **Context**: [infer from conversation if not provided]
   - **{Type}**: {content}
   ```

### 2. Save to MCP Memory (searchable)

Also save to MCP memory for searchable retrieval:

```
mcp__memory__create_entities([{
  name: "{type}_{topic}_{date}",
  entityType: "{type}",
  observations: [
    "type: {type}",
    "topic: {title}",
    "content: {content}",
    "date: {YYYY-MM-DD}",
    "project: {current project name}"
  ]
}])
```

**Entity naming convention:**

| Type | Name Pattern | Example |
|------|--------------|---------|
| Decision | `decision_{topic}_{date}` | `decision_auth_jwt_2026_02_02` |
| Pattern | `pattern_{name}` | `pattern_error_shape` |
| Learning | `learning_{topic}_{date}` | `learning_orm_performance_2026_02_02` |

**Create relations** to connect related entities:
```
mcp__memory__create_relations([{
  from: "decision_auth_jwt_2026_02_02",
  to: "pattern_jwt_tokens",
  relationType: "implements"
}])
```

### 3. Confirm

Report what was saved to both locations

## Examples

```
/cs-learn decision "Use PostgreSQL" "Chose over MySQL for better JSON support"
/cs-learn pattern "API errors" "All errors return {error, message, code} shape"
/cs-learn learning "Avoid N+1" "Use eager loading for related entities"
```

## Notes

- Learnings are loaded automatically at session start via Claude Code's rules system
- Keep entries concise — these are reminders, not documentation
- When running `/cs-loop`, significant learnings should be captured automatically
