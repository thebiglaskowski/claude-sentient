---
feature: Memory & Learning
version: "1.0"
last_updated: 2026-03-04
dependencies: []
routes: []
status: draft
---

# Memory & Learning

> `/cs-learn` captures decisions, patterns, and learnings to `learnings.md` (and optionally to MCP memory). Ensures Claude doesn't re-litigate settled questions or repeat corrected mistakes across sessions. Pre-compact summarization preserves context across compaction boundaries.

## `/cs-learn` Command

### Entry Types

| Type | Meaning | Confidence Applied |
|------|---------|-------------------|
| `decision` | Architectural or design choice | `rule` |
| `pattern` | Coding convention or recurring pattern | `pattern` |
| `learning` | Correction or lesson from a mistake | `observed` |

### Confidence Levels

| Level | Meaning |
|-------|---------|
| `observed` | Seen once — tentative |
| `pattern` | Seen multiple times — likely true |
| `rule` | Established — treat as standard |
| `instinct` | Strong conviction, hard to cite |

### Scopes

| Scope | Storage Location | Applies To |
|-------|-----------------|-----------|
| `project` | `.claude/rules/learnings.md` | This project only |
| `global` | `~/.claude/rules/learnings.md` | All projects |
| `org` | MCP memory (org-scoped) | Organization-wide |
| `personal` | MCP memory (user-scoped) | Personal preferences |

Default scope: `project`.

### Invocation

```
/cs-learn decision "Use PostgreSQL" "JSON already in stack, Redis would be redundant"
/cs-learn pattern "Early returns for guard clauses" "Reduces nesting depth"
/cs-learn learning "Always use bash --norc for tests" "zsh nvm FUNCNEST breaks node"
```

### Storage Format

Entries are appended to `learnings.md` under the appropriate section:

```markdown
### YYYY-MM-DD: [Short title]
- **Context**: What happened or what was decided
- **Decision/Correction/Pattern**: The actual learning
- **Rule**: What to do differently (for `learning` type)
```

### Contradiction Check

Before saving, `/cs-learn` scans existing entries for contradictions:
- If a conflicting entry exists, surface it and ask the user to confirm the update
- Old contradicting entry is either superseded or kept with a note

### Dual Storage

When MCP memory server is connected:
1. Write to `learnings.md` (primary, always)
2. Write to MCP memory with entity name `{project}-{title-slug}` (secondary)

MCP storage enables cross-project memory queries. File storage is the canonical record.

## Anchored Summarization (Pre-Compact)

`pre-compact.cjs` runs synchronously before Claude Code compacts the context window. It builds a structured `sessionSummary` to anchor the resumed session.

**Output file**: `.claude/state/compact-context.json`

### Summary Shape

```json
{
  "sessionIntent": "Implement HTTP hooks modernization",
  "filesModified": ["file1.cjs", "file2.md"],
  "decisionsMade": ["Use hookSpecificOutput format", "Mark observer hooks async"],
  "currentState": "VERIFY phase — all gates passing",
  "nextSteps": ["Update CHANGELOG", "Commit", "Push"],
  "contextManifest": { ... },
  "sessionSummary": { ... }
}
```

### sessionIntent Priority

`buildSessionSummary()` resolves session intent from best available source:

1. Current task subject (from `current_task.json`)
2. Session intent from `session_start.json`
3. Profile name (fallback)

### Recovery on Resume

During INIT, cs-loop checks for `compact-context.json`:

1. If exists: load `sessionSummary`, reconstruct task context, report `[RESUME] Recovering from compaction...`
2. Restore `filesModified`, `decisionsMade`, `currentState`, `nextSteps` into working context
3. Continue from where work left off without re-doing completed work

## learnings.md Structure

`learnings.md` in `.claude/rules/` is divided into three sections:

```markdown
## Decisions
{Architecture and technology choices}

## Patterns
{Recurring coding conventions}

## Learnings
{Corrections and lessons from mistakes}
```

### Special Status

`learnings.md` is the **only rule file** that lives only in `.claude/rules/` (project-specific). It does NOT have a copy in `rules/` (reference copies). Integration tests know about this exception.

### Auto-Load

`learnings.md` is one of the 3 always-loaded rules — it loads every session regardless of task keywords. This ensures prior decisions are always in context before any work begins.

## Business Rules

- **learnings.md overrides rules**: When `learnings.md` contains a project-specific decision that conflicts with a general rule file, `learnings.md` wins.
- **Self-improvement rule**: When Claude is corrected, it should propose a `learning` entry. Format is standardized (date, context, correction, rule).
- **Contradiction check required**: Never append a learning that directly contradicts an existing one without surfacing the conflict first.
- **Compact recovery**: If `compact-context.json` exists at INIT, always attempt recovery before starting fresh. Do not ask the user if they want to recover — just do it.
- **Dual storage is additive**: Writing to both file and MCP. MCP failure doesn't prevent file write.
- **Entity naming for MCP**: `{project-name}-{slug}` format. Enables querying all learnings for a project without full scan.

## Edge Cases

- **No MCP memory connected**: Only file storage. No error.
- **Conflicting entries in learnings.md**: Surface conflict, ask user which takes precedence, then update accordingly.
- **compact-context.json with no current_task.json**: Use session intent from `session_start.json` instead.
- **Empty learnings.md**: Valid state for new projects. Still loaded (just empty).
- **Very long learnings.md**: Context cost is managed by loading only relevant sections in some commands (cs-plan, cs-loop INIT reads the whole file; cs-execute reads on demand).
