# Claude Sentient Rules

This directory uses the official Claude Code memory pattern for persistent context.

## Files

| File | Purpose |
|------|---------|
| `learnings.md` | Decisions, patterns, and learnings captured via `/cs-learn` |

## How It Works

1. All `.md` files in `.claude/rules/` are loaded at session start
2. Claude reads these as project-specific instructions
3. `/cs-learn` appends new entries to `learnings.md`

## For Projects Using Claude Sentient

When Claude Sentient is applied to a project, it will:
1. Create `.claude/rules/` if it doesn't exist
2. Use `learnings.md` to store project-specific learnings
3. Load all rules at the start of each `/cs-loop` iteration

This follows the official Claude Code pattern - no custom scripts or external dependencies.
