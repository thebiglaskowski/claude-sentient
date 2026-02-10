# CHANGELOG.md — Claude Sentient

All notable changes to this project will be documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.2.0] — 2026-02-10

### Fixed
- **Security: curl|sh and wget|sh now blocked** — Promoted from warning to dangerous pattern in bash-validator. Piping remote scripts to shell is the most common supply-chain attack vector.
- **Security: Base64-encoded command injection detection** — Added pattern to detect `base64 -d | sh` command injection bypass attempts.
- **Security: Error logging in loadJsonFile** — Corrupt JSON files now log a warning instead of silently returning defaults, making debugging easier.
- **Schema $id domain standardization** — Updated 7 schema files from legacy `claude-conductor.dev` to `claude-sentient.dev` domain.
- **Java profile missing fix_command** — Added `fix_command: mvn spotless:apply` to Java lint gate, enabling auto-fix in VERIFY phase.
- **Security agent missing build gate** — Added `build` to security agent's quality_gates for consistency with other agents.

### Changed
- bash-validator: Increased command truncation in audit output from 100 to 500 characters.
- bash-validator: Removed curl|sh and wget|sh from WARNING_PATTERNS (now in DANGEROUS_PATTERNS).

---

## [1.1.0] — 2026-02-10

### Added
- **Path-scoped rules** — 15 rules now in `.claude/rules/` with `paths:` frontmatter for conditional loading
  - 12 rules with path-specific triggers (security, testing, api-design, database, ui-ux-design, error-handling, performance, logging, terminal-ui, documentation, prompt-structure, git-workflow)
  - 3 universal rules always loaded (anthropic-patterns, code-quality, learnings)
  - Claude Code natively loads relevant rules when working on matching file paths
- **CLAUDE.md `@import`** — Root CLAUDE.md now imports `@rules/_index.md` for rule visibility
- **cs-init `@import` generation** — Nested CLAUDE.md files now include `@rules/` imports based on directory purpose
- **`/cs-learn --scope personal`** — New scope writes to auto memory (`~/.claude/projects/`) instead of shared `.claude/rules/learnings.md`
- Path-scoped rules validation tests (14+ new tests)
- Installers now copy path-scoped rules to `.claude/rules/`

### Changed
- cs-loop INIT notes that path-scoped rules load automatically via Claude Code
- Updated `rules/_index.md` with path-scoping note
- Rewritten `.claude/rules/README.md` to document all rule files and frontmatter format

---

## [1.0.0] — 2026-02-10

### Added
- **Proactive Self-Healing (v0.6.0)** — VERIFY phase auto-fix sub-loop
  - Gate failures trigger automatic repair (max 3 attempts per gate)
  - Classifies error type: lint, import ordering, type errors, test failures, build errors
  - Runs `fix_command` from profile gates when available
  - Reverts if error count increases after fix attempt
  - Falls back to WebSearch strategy after 3 failed attempts
  - Added `fix_command` to Go (`golangci-lint run --fix`), Rust (`cargo clippy --fix --allow-dirty`), C++ (`clang-tidy --fix`) profiles
  - Updated `gate.schema.json` with `fix_command` field definition

- **Specialized Agent Roles (v0.7.0)** — Domain-expert agents for Agent Teams
  - 6 agent role definitions in `agents/*.yaml`: security, devops, frontend, backend, tester, architect
  - Each agent has: expertise areas, spawn_prompt, rules_to_load, quality_gates, file_scope_hints
  - `schemas/agent.schema.json` for agent YAML validation
  - `/cs-team` now loads agent definitions dynamically, matching expertise to work streams
  - `/cs-loop` team mode uses agent spawn_prompts for teammate initialization
  - `agent-tracker.js` enhanced to track agent role definitions and loaded rules
  - `agents/CLAUDE.md` documentation for the agent system
  - `agents/__tests__/test-agents.js` test suite

- **Cross-Project Collective Intelligence (v0.8.0)** — Scoped memory sharing
  - `/cs-learn` now supports `--scope` flag: `project` (default), `global`, `org`
  - Global learnings shared across all projects via MCP memory
  - Org learnings shared within organization via MCP memory with `scope:org:{name}` tag
  - `/cs-loop` INIT phase searches global/org learnings relevant to current task
  - `/cs-init` generates custom profiles for non-standard languages (Elixir, Swift, Kotlin, etc.)

- **Seamless Context for Massive Repos (v0.9.0)** — Predictive context architecture
  - `context-injector.js` now predicts relevant file paths based on detected topics
  - `/cs-assess --map` mode: structured codebase inventory (directory tree, dependency graph, entry points, hotspot analysis)
  - `pre-compact.js` generates `compact-context.json` summary for cs-loop recovery after context compaction
  - Map output saved to `.claude/state/codebase-map.json`

- **Infrastructure Orchestration (v1.0.0)** — CI monitoring and deployment readiness
  - `/cs-loop` COMMIT phase monitors CI status via GitHub MCP, auto-fixes on failure
  - All 9 profiles now include optional `infrastructure` sections (Docker, CI, platform-specific)
  - `/cs-deploy` command: deployment readiness check (CI status, Docker build, env vars, migrations, dependencies)
  - Commands: 11 → 12

### Changed
- Version bump: 0.5.1 → 1.0.0
- `/cs-loop` VERIFY section now includes AUTO-FIX sub-loop before WebSearch fallback
- `/cs-loop` INIT phase now includes cross-project memory search (step 10)
- `/cs-loop` EXECUTE team mode references agent definitions from `agents/*.yaml`
- `/cs-loop` COMMIT phase now includes CI monitoring
- `/cs-team` loads specialized agent definitions dynamically instead of static 4-role table
- `context-injector.js` outputs `filePredictions` array
- `pre-compact.js` generates `compact-context.json` alongside existing backups
- `agent-tracker.js` tracks `agentRole`, `rulesLoaded`, and `expertise` fields
- Updated Quality Gates documentation to show auto-fix capability

---

## [0.5.1] — 2026-02-07

### Security
- Fixed shell injection in TypeScript gates — replaced `shell: true` with parsed command arguments
- Added command normalization to `bash-validator.js` — strips variable substitution, full binary paths, quoting tricks, and backslash continuations before pattern matching
- Added symlink detection and path traversal prevention to `file-validator.js` — resolves symlinks with `realpathSync()`, validates parent directories, checks project root boundaries
- Added `sanitizeJson()` to `utils.js` — prevents JSON prototype pollution by removing `__proto__`, `constructor`, `prototype` keys
- Added `redactSecrets()` to `utils.js` — redacts API keys, GitHub tokens, Bearer tokens, AWS keys, Slack tokens, JWTs in log output

### Added
- `sdk/python/claude_sentient/validators.py` — JSON schema validation module
  - `validate_state()` validates session state against `state.schema.json`
  - `validate_profile_yaml()` validates profile data structure, gates, models, thinking config
  - Wired into `ProfileLoader.load()` and `SessionManager.load()`
- `shared/dangerous-patterns.json` — centralized bash validation patterns (extracted from bash-validator.js)
- `shared/protected-paths.json` — centralized file validation patterns (extracted from file-validator.js)
- `sdk/python/claude_sentient/client.py` — extracted `ClaudeSentientClient` from orchestrator.py
- Profile detection caching (`_detection_cache`) with `clear_detection_cache()` for testing
- **5 new test suites (105 new tests):**
  - Command validation tests (48 tests) — `.claude/commands/__tests__/test-commands.js`
  - TypeScript orchestrator tests (17 tests) — `sdk/typescript/src/orchestrator.test.ts`
  - Install script tests (14 tests) — `tests/test-install.sh`
  - Tools/schema tests (11 tests) — `tools/test_tools.py`
  - Extended hook tests (+15 new tests for Agent Teams hooks, security utils, normalization)
- README.md files in `agents/`, `patterns/`, `gates/blocking/`, `gates/advisory/`, `skills/` (replacing `.gitkeep` files)
- `jsonschema>=4.0` added to Python SDK dependencies

### Changed
- `orchestrator.py` — made `_build_sdk_agents`, `_build_sandbox_config`, `_build_merged_hooks` public methods
- `session-start.js` — refactored `detectProfile()` from 58 lines/5 nesting levels into 4 focused functions
- `utils.js` — `loadJsonFile()` now sanitizes parsed JSON; `logMessage()` now redacts secrets and writes to stderr on failure
- Named constants extracted across all hooks and SDK modules (8+ magic numbers replaced)
- Silent YAML parse errors in `profiles.py` now warn to stderr instead of being suppressed
- Commands CLAUDE.md now references all 11 commands (was missing 5)
- Total test count: 479 → 584

### Removed
- `archive/v1-legacy/` — 310 files (3.4MB) of deprecated V1 code (preserved in git history)
- 6 `.gitkeep` placeholder files (replaced with descriptive README.md files)
- `rules/.gitkeep` (directory already contains 15+ rule files)

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
| 1.1.0 | 2026-02-10 | Path-scoped rules, @imports, --scope personal, native memory integration |
| 1.0.0 | 2026-02-10 | Self-healing, agent roles, collective intelligence, context architecture, infrastructure, 12 commands, 503+ tests |
| 0.5.1 | 2026-02-07 | Security hardening, JSON schema validation, 584 tests, v1-legacy removal |
| 0.5.0 | 2026-02-07 | Agent Teams, /cs-team, team hooks, 11 commands, 13 hooks |
| 0.4.0 | 2026-02-07 | Hooks, tests, /cs-init, SDK integration, 10 commands, 9 profiles |
| 0.2.0 | 2026-02-01 | Native-first pivot, 4 commands, 3 profiles |
| 0.1.0 | 2026-02-01 | Foundation, memory pattern, simplified scope |
| 0.0.1 | 2026-02-01 | Initial setup |
