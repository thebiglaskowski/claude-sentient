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

### 2026-02-02: Integrity Rules to prevent common Claude failure modes
- **Context**: User saw X post complaining about Claude "destroying codebases" with workarounds, dismissing errors as "pre-existing", gaslighting, ignoring CLAUDE.md, ignoring architecture
- **Decision**: Added explicit "Integrity Rules" section to CLAUDE.md covering:
  1. Never dismiss errors as "pre-existing" without proof (git blame)
  2. No workarounds or quick fixes - solve root causes
  3. Re-read CLAUDE.md periodically during significant work
  4. Verify architecture alignment before implementing
  5. Admit mistakes immediately and clearly
  6. Never gaslight - don't claim things that aren't true
- **Implementation**: Added to CLAUDE.md, anthropic-patterns.md, and cs-loop `<avoid>` section
- **Rationale**: These are the most frustrating Claude behaviors - explicit rules help prevent them

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

### 2026-02-02: XML prompt structure for commands
- **Pattern**: All commands use XML tags to structure instructions
- **Core tags**:
  - `<role>` — Define Claude's expertise/persona
  - `<task>` — Clear statement of what to do (REQUIRED)
  - `<context>` — Background info, nested data
  - `<steps>` — Ordered procedure
  - `<thinking>` — Request reasoning steps
  - `<criteria>` — Success metrics
  - `<output_format>` — How to structure response
  - `<constraints>` — Rules and limitations
  - `<examples>` — Sample inputs/outputs
- **Rationale**: XML tags separate WHAT from HOW, improve parsing, and enable structured reasoning
- **Reference**: Full guidelines in `rules/prompt-structure.md`

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

### 2026-02-02: Windows MCP servers require `cmd /c` wrapper
- **Context**: `/doctor` showed warnings that MCP servers (memory, filesystem, puppeteer, github) need Windows wrapper
- **Problem**: Direct `npx` command doesn't work on Windows for MCP servers - causes connection failures
- **Solution**: Use `cmd /c` wrapper in MCP config:
  ```json
  {
    "command": "cmd",
    "args": ["/c", "npx", "-y", "@modelcontextprotocol/server-memory"]
  }
  ```
- **Rule**: On Windows, always use `cmd /c npx` instead of direct `npx` for MCP servers. Updated `/cs-mcp` command to document this.

### 2026-02-02: Never dismiss lint warnings as "pre-existing"
- **Context**: During /cs-loop, encountered a ruff lint warning (import sorting) and said "The only lint issue is an import sorting warning which is pre-existing"
- **Correction**: User said "pre-existing or not its an issue, why would we not want to fix it?"
- **Rule**: Fix ALL lint issues during VERIFY phase - never dismiss warnings as "pre-existing" or non-blocking. If ruff reports it, fix it. This is an Integrity Rule violation.

### 2026-02-16: Never use shell substitutions in hook commands
- **Context**: Hook commands in settings.json used `$(git rev-parse --show-toplevel 2>/dev/null || echo .)` to resolve project root
- **Problem**: Claude Code passes hook commands through `cmd.exe` on Windows, which treats `$(...)` as a literal string. Node then looks for a file at `<cwd>\$(git rev-parse ...)\.claude\hooks\foo.js` which doesn't exist. This broke ALL hooks on Windows.
- **Root cause**: Commit e8f295c tried to fix subdirectory cwd by adding bash shell substitution, but Claude Code's hook executor doesn't guarantee bash on all platforms
- **Solution**: Use simple relative paths (`node .claude/hooks/foo.js`). Claude Code runs hooks from the project root. Each hook uses `getProjectRoot()` from `utils.js` internally for file operations.
- **Rule**: Hook commands in settings.json must be plain cross-platform invocations (`node <path>`). Never use bash-specific syntax (`$(...)`, backticks, pipes). If a hook needs the project root, resolve it inside the JS script using `getProjectRoot()`.

### 2026-02-16: Auto-install Claude Code plugins during setup
- **Context**: Claude Code has an official plugin marketplace with LSP plugins and security tools
- **Decision**: The installer auto-installs two categories of plugins:
  1. `security-guidance@claude-plugins-official` (user scope, universal)
  2. Profile-matched LSP plugin (project scope): pyright-lsp, typescript-lsp, gopls-lsp, rust-analyzer-lsp, jdtls-lsp, or clangd-lsp
- **Non-fatal**: Plugin installs use `2>/dev/null || true` — missing `claude` CLI or install failures don't block setup
- **Uninstall**: Only project-scoped LSP plugins are removed; user-scoped security-guidance is preserved
- **Profile schema**: Added `plugins.lsp` property to `profile.schema.json` so each profile declares its recommended LSP plugin
- **Parity**: Integration tests enforce that install.sh and install.ps1 reference identical plugin sets
- **Rule**: When adding a new language profile, set `plugins.lsp` to the matching LSP plugin identifier (or `null` if none)

### 2026-02-18: bash-validator blocks its own commit messages
- **Context**: Commit messages documenting blocked security patterns (e.g. "blocks double-dash deletion" or "pipe-to-interpreter") trigger the very patterns they describe
- **Rule**: When committing changes that reference security patterns, write the message to `/tmp/commit-msg.txt` and use `git commit -F /tmp/commit-msg.txt` instead of inline heredoc

<!-- Mistakes and their fixes will be added here -->

---
