---
description: Save a learning, decision, or pattern to project memory
argument-hint: <type> <title> <content>
allowed-tools: Read, Edit, Write
---

# /cs-learn

Save important learnings to `.claude/rules/learnings.md` for future sessions.

## Arguments

- `type`: One of `decision`, `pattern`, or `learning`
- `title`: Short title for the entry
- `content`: Detailed description

## Behavior

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
4. Confirm what was saved

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
