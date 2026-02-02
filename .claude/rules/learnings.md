# Project Learnings

> Decisions, patterns, and learnings captured during development.
> This file is automatically appended to by `/cs-learn` and by Claude when corrected.

**Self-Improvement Rule**: When the user corrects Claude, Claude should propose adding a rule here to prevent the same mistake. Format:

```markdown
### YYYY-MM-DD: [Short title]
- **Context**: What happened
- **Correction**: What the user said
- **Rule**: What to do differently
```

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

### 2026-02-01: Deep MCP server integration in /cs-loop
- **Context**: MCP servers (context7, github, memory, puppeteer) were connected but only context7 was being used
- **Decision**: Integrate all available MCP servers into /cs-loop phases:
  - **INIT**: context7 for library docs, github for issue details, memory for session resumability
  - **VERIFY**: puppeteer for web project screenshots
  - **COMMIT**: github for PR creation and issue linking, memory for state persistence
- **Rationale**: MCP servers are native Claude Code capabilities — use them to their full potential rather than leaving features on the table

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

### 2026-02-01: Update all docs when adding commands
- **Context**: Added `/cs-validate` command, updated CLAUDE.md and STATUS.md but missed README.md
- **Correction**: User pointed out README.md still said "4 Commands"
- **Rule**: When adding a new command, update ALL documentation: README.md, CLAUDE.md, STATUS.md, CHANGELOG.md

### 2026-02-01: Simplify command files with tables
- **Context**: `/cs-loop` was 320 lines with verbose prose explanations and examples
- **Learning**: Tables are more scannable than prose for phase/rule documentation
- **Result**: Reduced to 106 lines (67% reduction) while preserving all functionality

### 2026-02-01: MCP servers in settings.json must be registered with `claude mcp add`
- **Context**: User had 5 MCP servers configured in `~/.claude/settings.json` under `mcpServers` key, but only Context7 (a plugin) was working
- **Discovery**: The `mcpServers` section in settings.json is NOT automatically loaded by Claude Code. Servers must be registered using `claude mcp add` command.
- **Solution**: Use `claude mcp add <name> -- npx -y <package>` for simple servers, or `claude mcp add-json <name> '{...}'` for servers with environment variables (the `-e` flag parsing is buggy)
- **Rule**: `/cs-mcp --fix` should detect servers in settings.json that aren't registered and offer to register them

### 2026-02-01: Use `claude mcp add-json` for servers with env vars
- **Context**: `claude mcp add -e GITHUB_TOKEN=$TOKEN github -- npx ...` failed with "Invalid environment variable format"
- **Discovery**: The `-e` flag parser has issues with certain token formats
- **Solution**: Use `claude mcp add-json github '{"command":"npx","args":["-y","@modelcontextprotocol/server-github"],"env":{"GITHUB_TOKEN":"<token>"}}'`
- **Rule**: Always prefer `add-json` for servers that require environment variables

### 2026-02-01: Detect Python environments (conda, venv, poetry)
- **Context**: User ran `/cs-loop` on a project that uses a specific conda environment, but commands ran in system Python
- **Problem**: Profile commands like `pytest` and `ruff` ran without the correct environment
- **Solution**: Added environment detection to Python profile:
  - Check for `environment.yml` → use `conda run -n <env> --no-capture-output` prefix
  - Check for `.venv/` or `venv/` → activate or use venv python directly
  - Check for `poetry.lock` → use `poetry run` prefix
  - Check for `pdm.lock` → use `pdm run` prefix
- **Rule**: Always detect and report the Python environment during INIT phase

<!-- Mistakes and their fixes will be added here -->

---
