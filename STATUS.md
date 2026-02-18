# STATUS.md — Claude Sentient

> **Last Updated:** 2026-02-18
> **Current Phase:** Phase 4 — Enhancement & Integration
> **Version:** 1.3.0

---

## Current State

### Implementation Progress

```
Foundation          [████████████████████] 100% ✓
Commands            [████████████████████] 100% ✓ (12 commands)
Profiles            [████████████████████] 100% ✓ (9 profiles + infrastructure)
Templates           [████████████████████] 100% ✓
Documentation       [████████████████████] 100% ✓
Hooks               [████████████████████] 100% ✓ (13 hooks, enhanced)
Agent Teams         [████████████████████] 100% ✓ (cs-team + 6 agent roles)
Self-Healing        [████████████████████] 100% ✓ (auto-fix sub-loop)
Agent Roles         [████████████████████] 100% ✓ (6 specialized agents)
Collective Intel    [████████████████████] 100% ✓ (scoped memory)
Context Arch        [████████████████████] 100% ✓ (predictive + map)
Infrastructure      [████████████████████] 100% ✓ (CI + deploy)
Testing             [████████████████████] 100% ✓ (727 total across 6 suites)
```

---

## What's Done

### Native-First Architecture (2026-02-01)
- [x] Decided to use Claude Code native tools instead of reimplementing
- [x] Updated CLAUDE.md to document native-first approach
- [x] Captured decision in `.claude/rules/learnings.md`

### Commands
- [x] `/cs-loop` - Autonomous development loop (with PR workflow, memory search, code search)
- [x] `/cs-plan` - Plan before executing (chains to cs-loop)
- [x] `/cs-status` - Show current status (can resume work)
- [x] `/cs-learn` - Save learnings to file + MCP memory (searchable)
- [x] `/cs-validate` - Validate configuration (can auto-fix)
- [x] `/cs-mcp` - Check/register/validate MCP servers
- [x] `/cs-review` - Review pull requests with automated analysis
- [x] `/cs-assess` - Full codebase health audit (6+ dimensions, ultrathink mode)
- [x] `/cs-init` - Create/optimize nested CLAUDE.md context architecture
- [x] `/cs-ui` - UI/UX audit for web projects (modern design, accessibility)
- [x] `/cs-team` - Create/manage Agent Teams for parallel multi-instance work
- [x] `/cs-deploy` - Deployment readiness check (CI, Docker, env, migrations)

### Profiles
- [x] `python.yaml` - Python project profile
- [x] `typescript.yaml` - TypeScript project profile
- [x] `shell.yaml` - Shell/PowerShell script profile
- [x] `go.yaml` - Go project profile
- [x] `rust.yaml` - Rust project profile
- [x] `java.yaml` - Java project profile
- [x] `cpp.yaml` - C/C++ project profile
- [x] `ruby.yaml` - Ruby project profile
- [x] `general.yaml` - Fallback profile

### Documentation
- [x] CLAUDE.md - Main instructions (updated for native-first)
- [x] `.claude/rules/learnings.md` - Native memory
- [x] STATUS.md - Current progress
- [x] CHANGELOG.md - Version history
- [x] DECISIONS.md - ADRs (DEC-010 added)
- [x] README.md - Project overview

### Templates
- [x] `templates/STATUS.md` - Status template for new projects
- [x] `templates/CHANGELOG.md` - Changelog template
- [x] `templates/DECISIONS.md` - Decisions template
- [x] `templates/learnings.md` - Learnings template

---

## What's Next

### Testing the Commands
- [ ] Test `/cs-status` on this project
- [x] Test `/cs-loop` on a real task (Shell profile)
- [ ] Test `/cs-plan` on a complex task

### Apply to Another Project
- [ ] Try Claude Sentient on a Python project
- [ ] Try Claude Sentient on a TypeScript project
- [ ] Validate profile detection works

### Polish
- [x] Update README.md for public consumption
- [x] Add Go profile
- [x] Add Shell profile

---

## Architecture

### Native Claude Code Features Used

| Feature | Tool | Status |
|---------|------|--------|
| Task Queue | `TaskCreate`, `TaskUpdate`, `TaskList`, `TaskGet` | ✓ Working |
| Task Control | `TaskStop`, `TaskOutput` | ✓ Working |
| Planning | `EnterPlanMode`, `ExitPlanMode` | ✓ Working |
| Sub-agents | `Task` with `subagent_type` | ✓ Working |
| Memory (File) | `.claude/rules/*.md` | ✓ Working |
| Memory (MCP) | `search_nodes`, `open_nodes` | ✓ Working |
| Skill Chaining | `Skill` tool | ✓ Working |
| Web Tools | `WebSearch`, `WebFetch` | ✓ Working |
| GitHub PR | `get_pull_request*`, `create_review` | ✓ Working |
| GitHub Search | `search_code` | ✓ Working |
| Questions | `AskUserQuestion` (structured) | ✓ Working |
| Commands | `commands/*.md` | ✓ Working |

### Custom Components

| Component | Files | Status |
|-----------|-------|--------|
| Commands | `commands/cs-*.md` | ✓ 12 created |
| Profiles | `profiles/*.yaml` | ✓ 9 created (+ infrastructure) |
| Agent Roles | `agents/*.yaml` | ✓ 6 created |
| Hooks | `.claude/hooks/*.cjs` | ✓ 12 created + utils.cjs |
| Hook Tests | `.claude/hooks/__tests__/` | ✓ 101 tests |
| Profile Tests | `profiles/__tests__/` | ✓ 242 tests |
| Command Tests | `.claude/commands/__tests__/` | ✓ 81 tests |
| Agent Tests | `agents/__tests__/` | ✓ 108 tests |
| Schema Tests | `schemas/__tests__/` | ✓ 166 tests |
| Integration Tests | `integration/__tests__/` | ✓ 30 tests |
| Quality Gates | (embedded in profiles) | ✓ Defined + auto-fix |

---

## Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Commands | 12 | 12 ✓ |
| Profiles | 9 | 9 ✓ |
| Agent Roles | 6 | 6 ✓ |
| Hooks | 13 | 13 ✓ |
| Hook Tests | 101 | 101 ✓ |
| Profile Tests | 242 | 242 ✓ |
| Command Tests | 81 | 81 ✓ |
| Agent Tests | 108 | 108 ✓ |
| Schema Tests | 166 | 166 ✓ |
| Integration Tests | 29 | 29 ✓ |
| Native tools leveraged | All | ✓ |
| External dependencies | 0 | 0 ✓ |
| GitHub tools integrated | 13 | 13 ✓ |
| Memory tools integrated | 5 | 5 ✓ |

---

## Recent Activity

### 2026-02-18 (Session 18)
- **v1.3.0 — Dashboard & SDK Removal + Quality Hardening:**
  - Removed `dashboard/`, `sdk/`, `tools/` directories (no longer part of project)
  - Removed stub directories: `gates/`, `skills/`, `patterns/`, `archive/`, `docs/`, `phases/`
  - Fixed `generate-checksums.sh`: *.js → *.cjs glob, version bump
  - Wired `validateFilePath()` into `file-validator.cjs` (was defined but unused)
  - Fixed `session-end.cjs` and `pre-compact.cjs`: `process.cwd()` → `getProjectRoot()`
  - Consolidated `session-start.cjs` git detection: 4 subprocesses → 2
  - Reduced `agent-tracker.cjs` nesting from 5 to 3 levels
  - Removed redundant `ensureStateDir()` call in `utils.cjs`
  - Fixed trivially-true test assertions in `test-hooks.js`
  - Updated install/uninstall scripts (bash + PowerShell)
  - Updated all documentation: README, CLAUDE.md, STATUS, CHANGELOG, DECISIONS, ISSUES_FOUND
  - Fixed all .js → .cjs references in hooks README

### 2026-02-10 (Session 15)
- **Assessment Remediation (v1.2.0):**
  - Ran `/cs-assess` — scored 7.9/10 overall
  - Promoted curl|sh and wget|sh from warning to blocked (supply-chain attack vector)
  - Added base64-encoded command injection detection to bash-validator
  - Added error logging to utils.js loadJsonFile for corrupt JSON files
  - Standardized all 8 schema $id domains to claude-sentient.dev
  - Added fix_command to Java profile lint gate (mvn spotless:apply)
  - Added build gate to security agent quality_gates
  - Increased command audit truncation from 100 to 500 chars
  - Updated tests: 2 new bash-validator tests (wget|sh block, base64 detection), changed curl|sh test to expect block
  - Updated CHANGELOG, STATUS, README

### 2026-02-10 (Session 14)
- **Native Memory Integration (v1.1.0):**
  - Copied 15 rules to `.claude/rules/` with `paths:` frontmatter for native path-scoped loading
  - 12 conditional rules load only when working on matching file paths
  - 3 universal rules always loaded (anthropic-patterns, code-quality, learnings)
  - Added `@rules/_index.md` import to root CLAUDE.md
  - Updated `/cs-init` to generate `@rules/` imports in nested CLAUDE.md files
  - Added `--scope personal` to `/cs-learn` for auto memory storage
  - Updated installers, tests, and documentation
  - Used Agent Teams with 4 parallel teammates

### 2026-02-10 (Session 13)
- **v0.6–v1.0 Enhancement Plan (5 phases implemented in parallel):**
  - **Phase 1 — Self-Healing (v0.6.0):**
    - Added AUTO-FIX sub-loop to cs-loop VERIFY phase
    - Added `fix_command` to Go, Rust, C++ profiles
    - Updated gate.schema.json with `fix_command` field
    - Added profile tests for fix_command validation
  - **Phase 2 — Specialized Agent Roles (v0.7.0):**
    - Created 6 agent definitions in `agents/*.yaml` (security, devops, frontend, backend, tester, architect)
    - Created `schemas/agent.schema.json` and `agents/CLAUDE.md`
    - Updated cs-team.md for dynamic agent loading
    - Updated cs-loop.md team mode for agent definitions
    - Enhanced agent-tracker.js with role tracking
    - Created agent test suite
  - **Phase 3 — Collective Intelligence (v0.8.0):**
    - Added `--scope` flag to cs-learn (project/global/org)
    - Added cross-project memory search to cs-loop INIT
    - Added dynamic profile generation to cs-init
  - **Phase 4 — Context Architecture (v0.9.0):**
    - Added file path prediction to context-injector.js
    - Added `--map` mode to cs-assess
    - Added compact context preservation to pre-compact.js
  - **Phase 5 — Infrastructure (v1.0.0):**
    - Added CI monitoring to cs-loop COMMIT phase
    - Added infrastructure sections to all 9 profiles
    - Created `/cs-deploy` command
  - Used Agent Teams to parallelize work across 4 teammates

### 2026-02-07 (Session 12)
- **Full Assessment Remediation (21 issues → 21 fixed):**
  - **Security (3):**
    - Fixed shell injection in TypeScript gates (`shell: true` → parsed args)
    - Added command normalization to bash-validator (strips variable substitution, full paths, quoting tricks)
    - Added symlink detection and path traversal prevention to file-validator
  - **Code Quality (5):**
    - Extracted 8+ magic numbers to named constants across hooks and SDK
    - Added `sanitizeJson()` to prevent JSON prototype pollution
    - Added `redactSecrets()` for API key/token redaction in logs
    - Refactored `detectProfile()` from 58 lines/5 nesting levels to 4 small functions
    - Fixed silent error suppression — YAML/file errors now warn to stderr
  - **Architecture (4):**
    - Extracted `ClaudeSentientClient` from orchestrator.py → client.py
    - Made `_build_*` methods public to fix tight coupling
    - Created `shared/dangerous-patterns.json` and `shared/protected-paths.json` (centralized config)
    - Added `_detection_cache` for profile detection performance
  - **Tech Debt (3):**
    - Created `validators.py` with `validate_state()` and `validate_profile_yaml()`, wired into ProfileLoader and SessionManager
    - Removed `archive/v1-legacy/` (310 files, 3.4MB deprecated code)
    - Replaced 6 `.gitkeep` files with descriptive README.md files
  - **Test Coverage (105 new tests across 5 files):**
    - Extended hook tests: +15 tests (Agent Teams, security utils, normalization) → 83 total
    - New command validation tests: 48 tests
    - New TypeScript orchestrator tests: 17 tests
    - New install script tests: 14 tests
    - New tools/schema tests: 11 tests
    - Total test count: 584 (up from 479)
  - Added `jsonschema>=4.0` dependency to Python SDK
  - Updated commands CLAUDE.md with missing `/cs-assess`, `/cs-review`, `/cs-learn`, `/cs-mcp`, `/cs-ui` references

### 2026-02-07 (Session 11)
- **Agent Teams Integration:**
  - Created `/cs-team` command for manual Agent Teams management
  - Added team eligibility detection to `/cs-loop` PLAN phase
  - Added team execution mode to `/cs-loop` EXECUTE phase (Standard + Team)
  - Created `teammate-idle.js` hook (TeammateIdle quality enforcement)
  - Created `task-completed.js` hook (TaskCompleted validation + file ownership)
  - Updated `.claude/settings.json` with team hooks and env var
  - Updated all documentation (CLAUDE.md, README.md, CHANGELOG.md, STATUS.md)
  - Updated installer scripts for new file counts

### 2026-02-07 (Session 10)
- **Assessment Remediation (remaining items):**
  - Standardized build command patterns across all profiles
    - Java: `maven_command`/`gradle_command` → `command`/`alternative`
    - C++: `cmake_command`/`make_command` → `command`/`alternative`
    - Shell: `powershell_command` → `alternative`
  - Created hook test harness (`.claude/hooks/__tests__/test-hooks.js`)
    - 68 tests covering all 10 hook scripts + utils.js
    - Security tests: 12 bash-validator, 8 file-validator
    - Lifecycle tests: session-start, session-end, context-injector
    - Tracking tests: post-edit, agent-tracker, agent-synthesizer
  - Created profile schema validation test (`profiles/__tests__/test-profiles.js`)
    - 203 tests validating all 9 profiles
    - Required fields, gates, models, thinking, conventions
    - Cross-profile consistency, non-standard key detection
  - Extracted `_make_error_result()` in orchestrator.py
- **Documentation Updates:**
  - README.md: v0.4.0, added hooks section, tests section, cs-init workflow
  - CHANGELOG.md: comprehensive v0.4.0 release notes
  - STATUS.md: updated metrics, added session 10 activity
  - Fixed C/C++ profile link in README (c-cpp.yaml → cpp.yaml)

### 2026-02-07 (Session 10 - earlier)
- **Implemented `/cs-init` command:**
  - Nested CLAUDE.md architecture creation/optimization
  - 6-phase flow: DETECT → ANALYZE → PLAN → APPROVE → GENERATE → VERIFY
  - Monorepo-aware, auto-detects tech stack, zero-tolerance quality philosophy
  - Updated all docs (CLAUDE.md, install scripts, cs-validate, cs-loop)
- **Ran `/cs-assess`:** Scored 7.4/10 overall
- **Fixed 10 immediate/short-term assessment issues:**
  - Fixed state.schema.json phase enum (v1 → v2)
  - Added description field to all 9 profiles
  - Deleted duplicate archive tools
  - Standardized hook utils.js usage + named constants
  - Added models/thinking/web_indicators to 5 profiles
  - Fixed SDK type issues (orchestrator.py, profiles.ts)
  - Removed cost_tracking.json phantom reference

### 2026-02-02 (Session 9)
- **Codebase Health Fixes (from /cs-assess):**
  - **Security:** Fixed `shell=True` vulnerability in `gates.py`
    - Now uses `shlex.split()` on Unix to avoid command injection
    - Falls back to shell mode only on Windows or malformed commands
  - **Test Coverage:** Added 30 tests for `hooks.py` (was 0% coverage)
    - HookMatcher dataclass tests
    - HookManager class tests
    - Built-in hook tests (track_file_changes, track_commands, save_final_state)
    - Default hooks and merge_hooks tests
  - **Performance:** Added session write batching
    - Dirty flag pattern reduces 50+ file writes to 1-2 per session
    - New `auto_flush` parameter (True for legacy behavior)
    - Context manager support for automatic flush
    - Added 7 tests for batching functionality
  - **Tech Debt:** Removed 5 duplicate `*.profile.yaml` files
    - Kept only `*.yaml` versions used by SDK
  - **Code Quality:** Refactored `_run_with_agent_sdk()` method
    - Split 155-line method into smaller focused helpers
    - Extracted: `_build_sdk_agents()`, `_build_sandbox_config()`, `_build_merged_hooks()`, `_build_sdk_options()`, `_process_message()`
    - Main method now ~50 lines
  - **Tests:** Total SDK tests: 208 (up from 171)

### 2026-02-02 (Session 8)
- **Claude Agent SDK Documentation Review:**
  - Reviewed all Agent SDK documentation guides:
    - Permissions: permission modes, canUseTool callback, allowedTools
    - Custom Tools: @tool decorator, create_sdk_mcp_server
    - MCP Integration: mcp_servers, tool naming conventions
    - Skills: filesystem-based Skills, setting_sources
    - Slash Commands: built-in and custom commands
    - User Input: AskUserQuestion, clarifying questions
    - Streaming Input: ClaudeSDKClient for continuous conversations
    - Hooks: PreToolUse, PostToolUse, UserPromptSubmit, Stop, etc.
    - Sessions: continue_conversation, resume, fork_session
    - Subagents: AgentDefinition, parallel execution
    - File Checkpointing: rewind_files for rollback
    - Sandbox: secure command execution

- **SDK Architecture Improvements:**
  - Updated `orchestrator.py` to fully leverage Claude Agent SDK:
    - Added ClaudeSDKClient integration for continuous conversations
    - Added canUseTool callback support for custom permission handling
    - Added proper hook integration with HookMatcher
    - Added setting_sources for filesystem settings control
    - Added file checkpointing support with rewind_files
    - Added sandbox configuration (SandboxConfig dataclass)
    - Added budget control with max_budget_usd
    - Added cost tracking from ResultMessage
    - Improved message type handling (ResultMessage, AssistantMessage, etc.)
    - Added system prompt preset with append pattern
    - Added reviewer subagent for code review tasks
  - Added ClaudeSentientClient class for multi-turn conversations
  - Added SandboxConfig dataclass
  - Updated AgentDefinition to match SDK spec
  - Updated exports in __init__.py

- **Documentation Updates:**
  - Updated Python SDK README with new features:
    - Continuous conversation mode example
    - Custom permission handling example
    - Sandbox mode example
    - File checkpointing example
    - Budget control example
  - All documentation now links to official Agent SDK docs

### 2026-02-02 (Session 7)
- **Codebase Assessment & Remediation:**
  - Ran `/cs-assess` for E2E codebase health audit
  - Assessment scores before remediation:
    - Architecture: 8/10, Code Quality: 7/10, Security: 9/10
    - Performance: 8/10, Tech Debt: 6/10, Test Coverage: 3/10
    - Overall: 6.8/10
  - **Created comprehensive SDK test suite (162 tests):**
    - `test_types.py` - 17 tests for enums and dataclasses
    - `test_profiles.py` - 20 tests for profile detection and loading
    - `test_session.py` - 18 tests for session persistence
    - `test_gates.py` - 17 tests for quality gate execution
    - `test_orchestrator.py` - 23 tests for ClaudeSentient class
    - `test_commands.py` - 67 tests for command file validation
  - **Added workflow examples to README.md:**
    - 8 common workflows with step-by-step examples
    - Feature development, bug fix, code review, codebase health
    - Learning from mistakes, resuming work, UI audits, MCP setup
  - **Documented SDK experimental status:**
    - Added experimental notices to Python SDK README
    - Added experimental notices to TypeScript SDK README
  - **Fixed minor issues:**
    - Updated rules count from 13 to 14 in README
  - All tests passing: 162/162

### 2026-02-02 (Session 6)
- **XML Prompt Structure Integration:**
  - Created `rules/prompt-structure.md` - comprehensive XML prompting standards
  - Updated `rules/_index.md` with prompt-related keywords
  - Refactored ALL 9 commands to use XML structure tags:
    - `<role>` - Define Claude's expertise/persona
    - `<task>` - Clear statement of objective
    - `<context>` - Background info, nested data
    - `<steps>` - Ordered procedure with `<thinking>` blocks
    - `<criteria>` - Success metrics
    - `<output_format>` - Response structure
    - `<constraints>` - Rules and limitations
    - `<examples>` - Sample inputs/outputs
  - All commands now follow consistent XML-first pattern

- **Negative Prompting / Anti-Prompt Integration:**
  - Created `rules/anthropic-patterns.md` - comprehensive reference of Anthropic's tested patterns
  - Added `<avoid>` sections to ALL 9 commands with command-specific DON'Ts:
    - cs-loop: Overengineering, speculation, test hacking, premature abstractions
    - cs-plan: Premature implementation, skipping exploration, vague plans
    - cs-assess: Making changes, speculation, score inflation/deflation
    - cs-review: Modifying code, nitpicking style, blocking for minor issues
    - cs-ui: AI slop aesthetics, overengineering fixes, ignoring context
    - cs-status: Making changes, incomplete reporting, stale information
    - cs-learn: Duplicate entries, verbose entries, wrong section
    - cs-mcp: Registering without --fix, exposing tokens, wrong registration method
    - cs-validate: Auto-fixing without asking, shallow validation, vague errors
  - Updated `rules/prompt-structure.md` with negative prompting guidance
  - Synced all commands to `.claude/commands/`

### 2026-02-02 (Session 5)
- **UI/UX Design Standards Integration:**
  - Expanded `rules/ui-ux-design.md` with comprehensive v1 content (~340 lines)
  - Added Modern Aesthetic DO's/DON'Ts, spacing system, typography scale
  - Added shadow system, component standards, responsive breakpoints
  - Added accessibility checklist, animation guidelines, framework-specific guidance
  - Created `/cs-ui` command for on-demand UI/UX audits
  - Added UI/UX as optional 7th dimension in `/cs-assess` for web projects
- **Web Project Detection:**
  - Updated `profiles/typescript.yaml` with web pattern detection (React, Vue, Svelte, etc.)
  - Updated `profiles/python.yaml` with web pattern detection (Django, Flask, templates/)
  - Added auto-load of ui-ux-design rules for web projects in `/cs-loop`
  - Updated `rules/_index.md` with web-related keywords
- Created `reference/prompts-index.md` - V1 prompt reference for deep guidance
- All commands synced to `.claude/commands/`

### 2026-02-02 (Session 4)
- **Native Tools Integration (Phase 1):** WebSearch, WebFetch, TaskStop, TaskGet, NotebookEdit, AskUserQuestion structured patterns, claude-code-guide subagent
- **High-Value Native Integration (Phase 2):**
  - Memory search: `search_nodes`, `open_nodes` in cs-loop INIT
  - GitHub PR workflow: Full PR context loading, status checks, reviews
  - Created `/cs-review` command for PR review automation
  - Skill chaining: cs-plan→cs-loop, cs-status→cs-loop, cs-validate→cs-loop
  - GitHub code search: Reference implementations in UNDERSTAND phase
- Created `/cs-assess` command - Full codebase health audit:
  - 6 dimensions: Architecture, Code Quality, Security, Performance, Tech Debt, Tests
  - Weighted scoring (1-10 scale) with overall health score
  - Prioritized recommendations (Immediate, Short-term, Long-term)
  - `--ultrathink` mode for parallel deep analysis
  - Memory integration for prior decisions context
  - Profile-specific checks per language
- Updated `/cs-learn` to save to both file and MCP memory (searchable)
- All documentation updated (CLAUDE.md, README.md, STATUS.md)

### 2026-02-01 (Session 3 - continued)
- Added AskUserQuestion support for structured decisions
- Added hooks system (UserPromptSubmit, Stop) with documentation
- Added background subagent support for parallel execution
- Added Context7 integration for library documentation
- Created reference/HOOKS.md with advanced hook examples
- Added governance file system (STATUS.md, CHANGELOG.md, DECISIONS.md)
- Created templates for governance files (`templates/`)
- Updated commands to create/check governance files
- Updated all documentation to reflect changes
- Added DEC-010 for native-first architecture decision

### 2026-02-01 (Session 3)
- Major pivot: adopted native-first approach
- Removed plans for custom task queue, planning mode, sub-agents
- Leveraging Claude Code's built-in `TaskCreate`, `EnterPlanMode`, `Task`
- Created 4 commands: `/cs-loop`, `/cs-plan`, `/cs-status`, `/cs-learn`
- Created 3 profiles: Python, TypeScript, General
- Updated CLAUDE.md to v0.2.0

### 2026-02-01 (Session 2)
- Adopted official Claude Code memory pattern (`.claude/rules/*.md`)
- Removed claude-mem dependency
- Changed command prefix to `cs-`

### 2026-02-01 (Session 1)
- Initial project setup
- Created phase definitions
- Created initial profiles

---

## Blockers

None currently.

---

## Links

- **Main Instructions:** `CLAUDE.md`
- **Commands:** `commands/cs-*.md`
- **Profiles:** `profiles/*.yaml`
- **Memory:** `.claude/rules/learnings.md`
- **Decisions:** `DECISIONS.md`
