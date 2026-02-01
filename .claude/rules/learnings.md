# Project Learnings

> Decisions, patterns, and learnings captured during development.
> This file is automatically appended to by `/cs-learn`.

---

## Decisions

### 2026-02-01: Use official Claude Code memory pattern
- **Context**: Evaluated third-party memory solutions (claude-mem, Supermemory) - neither worked reliably
- **Decision**: Use `.claude/rules/*.md` files as the official Claude Code documentation recommends
- **Rationale**: Works with Claude Code's architecture, no external dependencies, portable to any project

### 2026-02-01: Use `cs-` prefix for commands
- **Context**: Needed a namespace for Claude Sentient commands
- **Decision**: Use `cs-` prefix (e.g., `/cs-loop`, `/cs-plan`)
- **Rationale**: Short, memorable, avoids conflicts with other tools

### 2026-02-01: Native-first approach - use built-in Claude Code features
- **Context**: Original V2 GAMEPLAN proposed custom implementations for task queues, planning modes, sub-agents
- **Decision**: Use native Claude Code tools instead of reimplementing:
  - `TaskCreate`/`TaskUpdate`/`TaskList` for work queues
  - `EnterPlanMode`/`ExitPlanMode` for planning
  - `Task` tool with `subagent_type` for sub-agents
  - `.claude/rules/*.md` for memory (already decided)
- **Rationale**: Don't reinvent the wheel. Native tools are tested, maintained, and work out of the box. Claude Sentient becomes a thin orchestration layer, not a parallel implementation.

---

## Patterns

### 2026-02-01: Command file structure
- **Pattern**: Commands in `commands/cs-*.md` with YAML frontmatter
- **Format**:
  ```markdown
  ---
  description: What it does
  argument-hint: <args>
  allowed-tools: Tool1, Tool2
  ---
  # /command-name
  Instructions...
  ```

<!-- Established patterns will be added here -->

---

## Learnings

<!-- Mistakes and their fixes will be added here -->

---
