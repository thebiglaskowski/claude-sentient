---
name: no-guessing
description: Ask instead of assuming when requirements are unclear
model: sonnet
---

# No Guessing

Ask instead of assume when requirements are unclear.

## Description

Use when facing ambiguous requirements, unclear specifications, or uncertain decisions.
Triggers on: "unclear", "ambiguous", "not sure", "assume", "probably", "I think", "might mean".

## Trigger

Activates when:
- Requirements are ambiguous
- Multiple interpretations are possible
- Business logic is unclear
- User intent is uncertain

## Red Flags (Stop and Ask)

When you find yourself thinking:
- "I think they meant..."
- "This probably should..."
- "It makes sense to..."
- "Users would expect..."
- "The obvious choice is..."

**STOP.** These are guesses, not requirements.

## The Protocol

1. **State the ambiguity clearly**
   > "The spec doesn't clarify how to handle empty input"

2. **List the possible interpretations**
   > "This could mean: (A) return null, (B) throw error, (C) return empty array"

3. **Ask for clarification**
   > "Which behavior is correct for this case?"

4. **Document the decision**
   > Update spec/ADR with the answer

## Acceptable Assumptions

These are OK to assume without asking:
- Following existing patterns in the codebase
- Using established project conventions
- Matching documented standards (CLAUDE.md)
- Technical implementation details (algorithm choice)

## Not Acceptable to Assume

These require explicit clarification:
- Business logic and rules
- User-facing behavior
- Error handling strategy
- Data validation rules
- Security requirements
- Performance requirements

## Example

**Bad:**
```
User: "Add a delete button"
Claude: *Adds button that permanently deletes without confirmation*
```

**Good:**
```
User: "Add a delete button"
Claude: "Before I add this, I need to clarify:
1. Should deletion require confirmation?
2. Should it be soft delete (recoverable) or hard delete?
3. Who should have permission to delete?"
```

## Mantra

> "Wrong assumptions cost more than questions."

When in doubt, ask. A 30-second clarification prevents hours of rework.
