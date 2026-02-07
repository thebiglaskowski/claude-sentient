# CHANGELOG.md — Claude Sentient

All notable changes to this project will be documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [0.5.0] — 2026-02-07

### Added
- **Agent Teams integration** — Parallel multi-instance work via Claude Code's experimental Agent Teams
  - `/cs-loop` PLAN phase now detects team eligibility (3+ independent tasks, non-overlapping files)
  - Auto-suggests team mode via `AskUserQuestion` when conditions are met
  - Team execution mode: spawns teammates, uses delegate mode, enforces quality gates
  - Graceful fallback to solo mode when Agent Teams not enabled
- `/cs-team` command — Manual Agent Teams management
  - Create teams with role-specific teammates for any task
  - Monitor team status and teammate progress
  - Stop and cleanup team resources
  - Supports 2-4 teammates with distinct file ownership scopes
- `teammate-idle.js` hook — TeammateIdle event handler
  - Checks if teammate has completed tasks before going idle
  - Sends feedback to keep teammates productive
  - Tracks idle counts per teammate
- `task-completed.js` hook — TaskCompleted event handler
  - Validates file count per task (max 20)
  - Detects file ownership conflicts between teammates
  - Tracks file ownership map to prevent overwrites
- Agent Teams env var (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`) auto-configured in settings.json
- Commands: 10 → 11, Hooks: 11 → 13

### Changed
- `/cs-loop` PLAN phase now includes team eligibility evaluation
- `/cs-loop` EXECUTE phase supports dual mode (Standard + Team)
- `.claude/settings.json` now includes TeammateIdle and TaskCompleted hooks
- Updated all documentation for v0.5.0

---

## [0.4.0] — 2026-02-07

### Added
- `/cs-init` command — Create or optimize nested CLAUDE.md context architecture
  - Auto-detects project tech stack, monorepo structure, significant directories
  - Create mode (no CLAUDE.md) and optimize mode (split monolithic CLAUDE.md)
  - Injects zero-tolerance quality philosophy into every project
  - Nested CLAUDE.md files for components, API, tests, packages
- `/cs-loop` INIT phase now checks for CLAUDE.md and suggests `/cs-init` if missing
- **Hook system** — 11 JavaScript hooks for Claude Code lifecycle events
  - `bash-validator.js` — blocks dangerous commands (rm -rf /, fork bombs, etc.)
  - `file-validator.js` — protects system paths, SSH keys, credentials
  - `context-injector.js` — detects topics and injects relevant context
  - `session-start.js` / `session-end.js` — session lifecycle management
  - `post-edit.js` — tracks file changes, suggests lint
  - `agent-tracker.js` / `agent-synthesizer.js` — subagent tracking
  - `pre-compact.js` — state backup before context compaction
  - `dod-verifier.js` — Definition of Done verification
  - Shared `utils.js` with named constants and common I/O functions
- **Hook test suite** — 68 tests covering all hooks (`.claude/hooks/__tests__/test-hooks.js`)
  - Security: 12 bash-validator tests (blocking dangerous commands)
  - Protection: 8 file-validator tests (protected paths, sensitive files)
  - Lifecycle: session-start, session-end, pre-compact tests
  - Tracking: post-edit, agent-tracker, agent-synthesizer tests
- **Profile validation test suite** — 203 tests (`profiles/__tests__/test-profiles.js`)
  - Schema compliance for all 9 profiles
  - Required fields, gate structure, models/thinking config
  - Cross-profile consistency checks
  - Non-standard gate key detection
- **Claude Agent SDK Integration** (`sdk/`)
  - Python SDK (`sdk/python/`) — `pip install claude-sentient`
  - TypeScript SDK (`sdk/typescript/`) — `npm install @claude-sentient/sdk`
  - Session persistence across terminal closures
  - Programmatic orchestration via `ClaudeSentient` class
  - Quality gate hooks, profile detection, subagent definitions
  - `ClaudeSentientClient` for continuous multi-turn conversations
  - Sandbox configuration, file checkpointing, budget control
- Model routing configuration in all profiles (haiku/sonnet/opus by phase)
- Extended thinking configuration in all profiles
- Web project detection (`web_indicators`) in all applicable profiles
- Rust, Java, C/C++, Ruby profiles
- `install.sh` and `install.ps1` installer scripts
- `/cs-mcp` command for MCP server management

### Changed
- Standardized gate command keys across all profiles (`command`/`alternative` pattern)
  - Java: `maven_command`/`gradle_command` → `command`/`alternative`
  - C++: `cmake_command`/`make_command` → `command`/`alternative`
  - Shell: `powershell_command` → `alternative`
- Extracted `_make_error_result()` in orchestrator.py to reduce duplication
- Simplified TypeScript SDK profile loading architecture
- Fixed state.schema.json phase enum (v1 → v2 phase names)
- Fixed Python SDK PermissionResult type (conditional union type)
- Hooks now use shared `utils.js` for all JSON I/O and logging
- All profiles now have `description`, `models`, `thinking` sections
- Removed phantom `cost_tracking.json` reference from pre-compact hook
- Deleted duplicate tools from archive (migrate.py, render-state.py, validate.py)
- Profiles: 5 → 9, Commands: 4 → 10, Rules: 12 → 15
- README.md comprehensively updated with hooks, tests, workflows

---

## [0.2.0] — 2026-02-01

### Added
- `/cs-loop` command - Autonomous development loop
- `/cs-plan` command - Plan before executing (uses native `EnterPlanMode`)
- `/cs-status` command - Show project status
- `/cs-learn` command - Save learnings to memory
- Python profile (`profiles/python.yaml`)
- TypeScript profile (`profiles/typescript.yaml`)
- General fallback profile (`profiles/general.yaml`)
- Governance file system (STATUS.md, CHANGELOG.md, DECISIONS.md)
- Templates for governance files (`templates/`)
- Governance file checks in `/cs-status`
- Auto-creation of governance files in `/cs-loop` init
- AskUserQuestion support for structured decision-making
- Hooks system with UserPromptSubmit and Stop hooks
- Background subagent support for parallel task execution
- Context7 integration for automatic library documentation
- reference/HOOKS.md with hook documentation and examples

### Changed
- **Major pivot to native-first architecture**
- Now uses Claude Code's built-in `TaskCreate`/`TaskUpdate` instead of custom work queue
- Now uses Claude Code's built-in `EnterPlanMode` instead of custom planning
- Now uses Claude Code's built-in `Task` subagents instead of custom agents
- Updated CLAUDE.md to v0.2.0 documenting native-first approach
- Simplified from 99 planned skills to 4 focused commands

### Removed
- Plans for custom event bus (not needed)
- Plans for custom task queue (using native)
- Plans for custom planning mode (using native)
- Plans for custom sub-agent system (using native)

---

## [0.1.0] — 2026-02-01

### Added
- Initial project structure
- Official Claude Code memory pattern (`.claude/rules/*.md`)
- Phase definitions (8 phases)
- Decision to use `cs-` prefix for commands
- CLAUDE.md, STATUS.md, DECISIONS.md

### Changed
- Removed claude-mem dependency (unreliable)
- Simplified scope from original V2 GAMEPLAN

---

## [0.0.1] — 2026-02-01

### Added
- Project initialization
- V1 reference clone in `reference/v1/`
- Original planning documents in `reference/v2-planning/`
- JSON schemas (from original vision)

---

## Version Summary

| Version | Date | Highlights |
|---------|------|------------|
| 0.5.0 | 2026-02-07 | Agent Teams, /cs-team, team hooks, 11 commands, 13 hooks |
| 0.4.0 | 2026-02-07 | Hooks, tests, /cs-init, SDK integration, 10 commands, 9 profiles |
| 0.2.0 | 2026-02-01 | Native-first pivot, 4 commands, 3 profiles |
| 0.1.0 | 2026-02-01 | Foundation, memory pattern, simplified scope |
| 0.0.1 | 2026-02-01 | Initial setup |
