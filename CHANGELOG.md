# CHANGELOG.md — Claude Sentient

All notable changes to this project will be documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.3.9] — 2026-02-20

### Security
- **`bash-validator.cjs`** — Added reverse shell patterns: socat EXEC/TCP, openssl s_client pipe, ncat -e flag
- **`bash-validator.cjs`** — Added cron persistence patterns: `crontab -e/-l/-i` and pipe-to-crontab
- **`bash-validator.cjs`** — Added `LD_PRELOAD` library injection detection
- **`utils.cjs`** — Fixed Anthropic key redaction pattern to include hyphens (`sk-ant-api03-` format)
- **`utils.cjs`** — Expanded `redactSecrets()` with 4 new patterns: GCP tokens (`ya29.`), Azure Storage keys (`AccountKey=`), npm tokens (`npm_`), PyPI tokens (`pypi-`)
- **`utils.cjs`** — Reordered `SECRET_PATTERNS` so specific prefixed secrets run before the generic AWS base64 catch-all, preventing partial token corruption

### Fixed
- **`file-validator.cjs`** — `checkHookSelfProtection()` now uses `absolutePath` instead of `resolvedPath`, fixing self-protection when path is relative (e.g. in test environments where the file/parent dir doesn't exist yet)

### Added
- **`schemas/`** — Formalized 3 state-file schemas: `session-state.schema.json`, `team-state.schema.json`, `gate-history.schema.json`
- **`schemas/`** — Marked aspirational schemas as `[Planned]` in their titles: `skill.schema.json`, `phase.schema.json`, `event.schema.json`
- **`utils.cjs`** — Extracted `GIT_TIMEOUT_MS = 3000` named constant; added `isInputTooLarge()` helper reducing `parseHookInput` nesting depth
- **`pre-compact.cjs`** — Flattened `collectStateFiles` from 4-level to 3-level nesting
- **`agent-tracker.cjs`** — JSDoc for `parseYamlListSections()`
- **`settings.json`** — Added `sentient.mcpServers` listing expected MCP servers

### Tests
- Added 52 new tests (hooks 181→235, schemas 166→188, integration 63→69)
- Covers: reverse shell variants, persistence patterns, expanded secret redaction, hook self-protection, state schema structure, MCP degradation
- Total: **923 tests**
- Version bump: 1.3.8 → 1.3.9

---

## [1.3.8] — 2026-02-20

### Fixed
- **Bug: `agent-synthesizer.cjs`** — Guard against invalid `startTime` producing `NaN` in `durationSeconds` (was `endTime - InvalidDate = NaN`)

### Changed
- **Quality: `file-validator.cjs`** — Refactored monolithic `main()` (104 lines, cyclomatic complexity 14) into 4 named sub-functions: `resolveToAbsolutePath()`, `checkProjectBoundaries()`, `checkHookSelfProtection()`, `checkProtectedPaths()`, `collectWarnings()` — reduces `main()` to ~22 lines / complexity ~6
- **Security: `bash-validator.cjs`** — Expanded `node -e` block pattern to cover 6 additional dangerous `fs` methods: `fs.chmod`, `fs.mkdir`, `fs.rename`, `fs.copyFile`, `fs.symlink`, `fs.createWriteStream`
- **Quality: `utils.cjs`** — Removed dead `LOG_ROTATION_CHECK_INTERVAL` export (constant defined as `1` but never read; log rotation uses a `_logRotationChecked` boolean)

### Tests
- Added 27 new tests (hooks 154→181): 8 bash-validator block patterns, 7 allow-side tests, 12 file-validator `PROTECTED_PATHS` coverage
- Total: **841 tests** (hooks 154→181)
- Version bump: 1.3.7 → 1.3.8

---

## [1.3.7] — 2026-02-20

### Fixed
- **Security: `bash-validator.cjs`** — Block any `rm` with combined `-r`/`-f` flags regardless of path (named dirs, `../traversal`); previous pattern only caught paths beginning with `/`, `~`, `.`, or `*`
- **Security: `bash-validator.cjs`** — Added pattern to catch `bash -c "$(curl ...)"` supply-chain bypass; fires on `rawCommand` before `$()` normalizer strips pipe context
- **Security: `bash-validator.cjs`** — Fail closed when `HOOK_INPUT` exceeds `MAX_INPUT_SIZE` — previous behavior silently returned `{}` (fail-open), allowing an empty command through

### Tests
- Added 15 new security tests to hook test suite
- Total: **814 tests** (hooks 139→154)
- Version bump: 1.3.6 → 1.3.7

---

## [1.3.6] — 2026-02-20

### Fixed
- **Performance: `utils.cjs`** — Log rotation guard now checks once per process (boolean flag) instead of never firing (`% 100` counter reset to 0 per process)
- **Quality: `context-injector.cjs`, `post-edit.cjs`** — Fixed zero-indentation in `main()` body (inconsistent with all other hooks)
- **Performance: `file-validator.cjs`** — Eliminated duplicate `fs.existsSync(filePath)` call; reuse stored result
- **Quality: `file-validator.cjs`** — Hook self-protection block now uses `blockPath()` helper (was inline duplicate)
- **Deprecated API: `session-start.cjs`** — Replaced `String.prototype.substr` with `.slice()` (ES2015 deprecation)
- **Docs** — Fixed stale test counts, version numbers, and CHANGELOG gaps

### Added
- **Security: `file-validator.cjs`** — Block writes to `~/.claude/commands/` and `~/.claude/rules/` (cross-project poisoning prevention)
- **Security: `bash-validator.cjs`** — Iterative `$()` stripping, `eval` blocking, broader `sudo` patterns, multi-word quote normalization
- **Security: `file-validator.cjs`** — Protected `.bashrc`, `.zshrc`, `.bash_profile`, `.profile`, `.gitconfig`, `.aws/config`
- **Quality: `utils.cjs`** — `appendCapped()` DRY helper, `LOG_ROTATION_CHECK_INTERVAL` constant
- **Performance: `gate-monitor.cjs`** — Early exit before disk I/O for non-gate commands
- **Performance: `agent-tracker.cjs`** — `KNOWN_ROLES` fast-path skips YAML scan (includes `general-purpose`)
- **Performance: `utils.cjs`** — `getProjectRoot()` fast-path reads `project_root` from `session_start.json`
- **Tests** — 22 new tests: redactSecrets (AWS/JWT/Stripe/DB), session-start not-a-repo, rules content-parity, gate-monitor smoke

### Changed
- All 11 top-level hooks wrapped in `main()` for consistent structure
- `appendCapped()` adopted in `context-injector.cjs` and `agent-synthesizer.cjs`
- Named constants `MIN_SHELL_FILES`, `SESSION_ID_SUFFIX_LEN` replace magic numbers
- Removed `pattern` field from bash-validator block response (no longer leaks regex)
- Extracted `resolveRealPath()` and `blockPath()` helpers in `file-validator.cjs`

### Tests
- Total: **799 tests** (hooks 125→139, integration 39→63)
- Version bump: 1.3.4 → 1.3.6

---

## [1.3.5] — 2026-02-20

### Fixed
- **Security: `utils.cjs`** — `sanitizeJson()` depth truncation returns `null` (not raw object) at `MAX_SANITIZE_DEPTH`
- **Security: `bash-validator.cjs`** — `normalizeCommand()` strips `$(...)` wrapping (was only stripping `${}`/backticks)
- **Reliability: `teammate-idle.cjs`, `task-completed.cjs`** — Null-guards before first field access; identical `team-state.json` defaults

### Added
- **Quality: `utils.cjs`** — `pruneDirectory()` shared utility for DRY archive pruning
- **Quality: `utils.cjs`** — Centralized named constants for all hooks (27 total)

### Tests
- Total: **777 tests** (hooks 125→134)
- Version bump: 1.3.4 → 1.3.5

---

## [1.3.4] — 2026-02-19

### Fixed
- **Bug: `session-start.cjs`** — Phantom `'javascript'` profile fallback replaced with `'general'` (no `javascript.yaml` exists)
- **Bug: `session-start.cjs`** — Added `requirements.txt` to Python profile detection (profile claims it but hook didn't check)
- **Bug: `file-validator.cjs`** — `startsWith` boundary: appended `path.sep` to prevent sibling-directory prefix confusion (`/project-foo` matching `/project` root)
- **Bug: MCP tool names in commands** — `mcp__github__get_issue` → `mcp__github__issue_read`; `mcp__github__get_pull_request` → `mcp__github__pull_request_read`; `mcp__github__create_pull_request_review` → `mcp__github__pull_request_review_write`; removed 4 non-existent tools (`get_pull_request_files`, `get_pull_request_status`, `get_pull_request_comments`, `get_pull_request_reviews`) from cs-loop.md and cs-review.md allowed-tools
- **Security: `bash-validator.cjs`** — Expanded Node one-liner pattern to block `writeFileSync`, `rmdirSync`, `unlinkSync`, `appendFileSync`
- **Security: `bash-validator.cjs`** — Added 4 chained download+execute patterns (`curl url > x.sh && bash x.sh`, wget variants, chmod+execute)
- **Security: `file-validator.cjs`** — Added `~/.claude/projects/` write warning (prompt injection persistence vector)
- **Docs: `README.md`** — Fixed hook count 12 → 13 and template count 4 → 5
- **Docs: `install.sh`, `install.ps1`** — Fixed template count 4 → 5 in summary output
- **Tests: `test-hooks.js`** — Fixed test isolation: `.gitignore: .claude/` → `.gitignore: *` so marker files (pyproject.toml, go.mod, etc.) don't make git status dirty and trigger dod-verifier enforcement

### Added
- **Feature: `gate-monitor.cjs`** — New PostToolUse Bash hook (13th hook) that records gate exit codes, command summaries, and durations to `.claude/state/gate_history.json` (max 200 entries); read-only observer, always allows
- **Feature: `cs-loop.md`** — INIT step 1 now reads `.claude/state/compact-context.json` for session recovery after context compaction
- **Feature: `cs-loop.md`** — EXECUTE writes `current_task.json` to state so `pre-compact.cjs` can capture the active task

### Changed
- **Architecture: `utils.cjs`** — Centralized `GIT_EXEC_OPTIONS` constant `{ encoding: 'utf8', stdio: ['pipe','pipe','pipe'], timeout: 3000 }` (eliminated 5 duplicate copies across hooks)
- **Enforcement: `dod-verifier.cjs`** — Now exits with code 2 when `gitClean === false && fileChanges.length > 0`, giving Claude feedback to commit before session ends
- **Allowed-tools: `cs-loop.md`** — Added `ExitPlanMode`, `TeamCreate`, `TeamDelete`, `SendMessage`
- **Allowed-tools: `cs-team.md`** — Added `TeamCreate`, `TeamDelete`, `SendMessage`

### Tests
- Test count unchanged at **761** (fixes improved reliability, not coverage)
- Version bump: 1.3.3 → 1.3.4

---

## [1.3.3] — 2026-02-19

### Fixed
- **Security: `bash-validator.cjs`** — Fixed `$HOME` normalization bypass (`[\/~]` → `[\/~$]` in rm pattern)
- **Security: `file-validator.cjs`** — Added `.git/hooks/` to PROTECTED_PATHS; block writes to `~/.claude/settings.json` (was incorrectly allowed via `~/.claude` allowlist)
- **Security: `file-validator.cjs`** — Added `.env.development` and `.env.test` to SENSITIVE_FILES
- **Reliability: all hooks** — Added `timeout: 3000` to every `execSync` call to prevent hangs on network filesystems

### Changed
- **Code quality: `utils.cjs`** — Named magic numbers `MAX_COMPACT_FILE_HISTORY` (10), `MAX_COMPACT_DECISION_HISTORY` (5), `MS_PER_MINUTE` (60000)
- **Code quality: `agent-tracker.cjs`** — Extracted `parseYamlListSections()` helper; reduced nesting from 4 to 3 levels
- **Docs: `CLAUDE.md`** — Fixed hook count framing: "12 hooks + utils" → "13 hook scripts"
- **Docs: install.sh, install.ps1** — Fixed `.claude/rules/` count from 14 to 15
- **Cleanup: `reference/prompts-index.md`** — Deleted (referenced non-existent `reference/v1/` directory)

### Tests
- Added 6 profile detection tests: go, rust, java, cpp, ruby, shell (session-start.cjs)
- Strengthened 3 weak team hook assertions with state-level verification
- Total: **761 tests** (hooks 119→125)
- Version bump: 1.3.2 → 1.3.3

---

## [1.3.2] — 2026-02-19

### Added
- **Feature: auto-configure global permissions** — `install.sh`, `install.ps1`, and `/cs-init` now merge the full auto-approve allow list into `~/.claude/settings.json`. Safe merge, non-fatal if node unavailable.

### Fixed
- **Security: `bash-validator.cjs`** — `normalizeCommand()` strips `$(cmd)` substitution before pattern matching
- **Security: `bash-validator.cjs`** — Fixed `validateFilePath` tab+control char bypass bug
- **Security: `file-validator.cjs`** — Added `.env.staging`, `.netrc`, `.npmrc` to SENSITIVE_FILES
- **Code quality: `utils.cjs`** — Named magic number 500 as `MAX_LOGGED_COMMAND_LENGTH`
- **Code quality: `utils.cjs`** — Extracted shared `pruneDirectory()` utility (DRY: session-end + pre-compact)
- **Code quality: `task-completed.cjs`** — Refactored `main()` into focused sub-functions
- **Reliability: `teammate-idle.cjs`** — Capped teammates map at `MAX_TEAMMATES` (50)

### Tests
- Added 18 new hook unit tests (101→119) and 10 integration smoke tests (29→39)
- Total: **755 tests** across 6 suites
- Version bump: 1.3.1 → 1.3.2

---

## [1.3.1] — 2026-02-18

### Fixed
- **Security: `utils.cjs`** — `parseHookInput()` now calls `sanitizeJson()` to prevent prototype pollution from hook input
- **Security: `utils.cjs`** — `validateFilePath()` blocks newline/carriage-return chars (log injection, path confusion)
- **Security: `bash-validator.cjs`** — `normalizeCommand()` strips backtick substitution before pattern matching
- **Cross-platform: `file-validator.cjs`** — Removed hardcoded `/tmp` check; `os.tmpdir()` already covers Linux/macOS/Windows
- **Performance: `utils.cjs`** — `ensureStateDir()` caches result to skip redundant `fs.existsSync()` per `saveJsonFile()` call
- **Reliability: `task-completed.cjs`** — `team-state.json` now capped (`MAX_COMPLETED_TASKS=100`, `MAX_FILE_OWNERSHIP=200`)

### Changed
- Removed stale `reference/v1/template/` footers from all 24 rule files in `rules/` and `.claude/rules/`
- Hook test count corrected: 93→101 in install.sh and install.ps1
- Version bump: 1.3.0 → 1.3.1

---

## [1.3.0] — 2026-02-18

### Removed
- **Dashboard** (`dashboard/`) — Real-time web dashboard removed to reduce project scope
- **Python SDK** (`sdk/python/`) — SDK removed; Claude Sentient is CLI-only
- **TypeScript SDK** (`sdk/typescript/`) — SDK removed; Claude Sentient is CLI-only
- **Tools** (`tools/`) — Standalone utility scripts removed (functionality covered by hooks)
- **Stub directories** — `gates/`, `skills/`, `patterns/`, `archive/`, `docs/`, `phases/` removed (empty/placeholder)
- SDK CLAUDE.md from nested context architecture
- Dashboard and SDK references from all documentation and install/uninstall scripts

### Fixed
- **Security: `generate-checksums.sh`** — Hook file glob changed from `*.js` to `*.cjs` (hooks weren't being checksummed after .js→.cjs rename)
- **Security: `file-validator.cjs`** — Wired `validateFilePath()` into the validation flow (was defined in utils.cjs but never called)
- **Code quality: `session-start.cjs`** — Consolidated 4 git subprocess calls into 2
- **Code quality: `session-end.cjs`** — Changed `process.cwd()` to `getProjectRoot()` for consistency
- **Code quality: `pre-compact.cjs`** — Changed `process.cwd()` to `getProjectRoot()` for consistency
- **Code quality: `utils.cjs`** — Removed redundant `ensureStateDir()` call in `saveState()` (already called by `saveJsonFile`)
- **Code quality: `agent-tracker.cjs`** — Reduced nesting from 5 to 3 levels, hoisted requires to top of file
- **Tests: `test-hooks.js`** — Fixed 3 trivially-true assertions (`result || true` → proper JSON validation)
- **Docs: `.claude/hooks/README.md`** — Fixed all `.js` references to `.cjs`, removed phantom `cost_tracking.json`

### Changed
- DEC-012 (Agent SDK Integration) marked as Superseded in DECISIONS.md
- Total test count: 727 across 6 core suites (removed dashboard, SDK, tools, install test suites)
- Version bump: 1.2.2 → 1.3.0

---

## [1.2.2] — 2026-02-16

### Added
- **Plugin auto-installation** — Installer now auto-installs Claude Code plugins from the official marketplace
  - `security-guidance@claude-plugins-official` (user scope, all projects)
  - Profile-matched LSP plugin (project scope): pyright-lsp, typescript-lsp, gopls-lsp, rust-analyzer-lsp, jdtls-lsp, clangd-lsp
  - Non-fatal: missing `claude` CLI or install failures don't block setup
- **Profile `plugins` property** — Added `plugins.lsp` to `profile.schema.json` and all 9 profile YAML files
- **Plugin parity tests** — 4 new integration tests ensure install.sh, install.ps1, uninstall scripts, and profiles all reference identical plugin sets
- **PLUGINS advisory in `/cs-validate`** — New step checks installed plugins against profile expectations
- **Uninstaller plugin cleanup** — Removes project-scoped LSP plugins on uninstall, preserves user-scoped security-guidance

### Fixed
- **`templates/settings.json` sync** — Added missing `TeammateIdle`, `TaskCompleted` hooks and `env` block to match `.claude/settings.json`
- **README.md accuracy** — Updated test counts (720+), added Plugins documentation section

### Changed
- Total test count: 716+ → 720+ (integration tests: 26 → 30)
- Installer summary now shows installed plugins and recommended optional plugins
- Next steps in installer updated to include plugin review step

---

## [1.2.1] — 2026-02-14

### Added
- **Integration test suite** — 26 cross-module integrity tests (`integration/__tests__/test-integration.js`)
  - Cross-file reference integrity: commands ↔ CLAUDE.md, profiles ↔ CLAUDE.md, rules ↔ _index.md
  - Hook chain state flow: session-start → state file → downstream hooks
  - Install/uninstall parity: bash and PowerShell scripts install/remove same components
  - Documentation consistency: version, counts, and references match actual files
- **Schema test suite** — 166 tests for JSON schema validation (`schemas/__tests__/test-schemas.js`)
  - Validates all 9 JSON schemas are parseable with correct structure
  - Cross-validates profiles, agents, and gates against their respective schemas
  - Verifies command chaining integrity (Skill in allowed-tools)
- **`profile.schema.json`** — New schema for profile YAML validation (detection, gates, models, conventions)
- **`generate-checksums.sh`** — SHA-256 checksum generation for installer verification
- **`CHECKSUMS.sha256`** — Pre-computed checksums for all installable files
- **Installer checksum verification** — Both `install.sh` and `install.ps1` verify file integrity after download
- **Shared test infrastructure** — `test-utils.js` consolidates test/suite/skip/summary across all 6 test suites
- **Command chaining** — cs-assess, cs-review, cs-ui, cs-team, cs-init now chain to cs-loop via Skill tool
- **Auto-learning in cs-loop** — PLAN phase captures architecture decisions, COMMIT phase captures insights
- **Unified profile detection** — Commands read from `.claude/state/session_start.json` (session-start hook output)
- **Contradiction detection in cs-learn** — Checks existing learnings before saving to prevent conflicts
- **Command chaining validation in cs-validate** — Verifies allowed-tools includes Skill for chaining commands

### Fixed
- **Security: file-validator.js** — Now blocks writes outside project root (previously empty condition block)
  - Allows exceptions for /tmp, os.tmpdir(), and ~/.claude/
- **Security: bash-validator.js** — Added 8 new patterns for `find -delete`, scripting one-liners (python -c, perl -e, ruby -e, node -e)
- **Security: Secret redaction** — Expanded SECRET_PATTERNS for Stripe keys, DB connection strings, private key headers
- **Atomic state writes** — `saveJsonFile()` in utils.js now uses temp-file-plus-rename pattern to prevent corruption
- **Path validation** — New `validateFilePath()` checks null bytes, control chars, excessive path length
- **Profile version consistency** — All 9 profiles updated to version "1.2.0" (was mix of 1.0, 1.1, 1.2)
- **Schema version pattern** — `base.schema.json` now accepts both `X.Y` and `X.Y.Z` versions
- **Gate schema completeness** — Added 16 missing optional properties to `gate.schema.json`
- **Agent versions** — All 6 agents updated to version "1.2.0" (was 0.5.1)
- **Install scripts** — Now install test-utils.js, schemas/, .claude/commands/CLAUDE.md, profiles/CLAUDE.md
- **Uninstall scripts** — Now remove test-utils.js and .claude/commands/CLAUDE.md

### Changed
- **Documentation deduplication** — cs-loop references profiles/CLAUDE.md and rules/_index.md instead of inline tables
- **rules/_index.md** — Added "Always-Loaded Rules" section documenting unconditional rules
- **Hook constants centralized** — MAX_FILES_PER_TASK and LARGE_FILE_THRESHOLD moved to utils.js
- **session-start.js** — Added comment noting commands depend on state output
- Total test count: 503+ → 716+ (242 profiles + 108 agents + 93 hooks + 81 commands + 166 schemas + 26 integration)
- Install scripts updated: schema count 8 → 9, schema test count 152 → 166

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
| 1.3.7 | 2026-02-20 | Security gap closures in bash-validator, 15 new tests, 814 total |
| 1.3.4 | 2026-02-19 | Assessment fixes: MCP tool names, boundary bugs, DoD enforcement, gate-monitor hook, 761 tests |
| 1.3.3 | 2026-02-19 | Security hardening, test coverage gaps filled, doc cleanup, 761 tests |
| 1.3.2 | 2026-02-19 | Auto-configure global permissions, security+quality fixes, 755 tests |
| 1.3.1 | 2026-02-18 | Prototype pollution fix, backtick blocking, caching, cross-platform |
| 1.3.0 | 2026-02-18 | Dashboard/SDK removal, security & quality hardening, 727 tests |
| 1.2.1 | 2026-02-14 | Cognitive coherence, integration tests, schema validation, security hardening, installer checksums, 716+ tests |
| 1.2.0 | 2026-02-10 | Security fixes, schema standardization, Java/security agent fixes |
| 1.1.0 | 2026-02-10 | Path-scoped rules, @imports, --scope personal, native memory integration |
| 1.0.0 | 2026-02-10 | Self-healing, agent roles, collective intelligence, context architecture, infrastructure, 12 commands, 503+ tests |
| 0.5.1 | 2026-02-07 | Security hardening, JSON schema validation, 584 tests, v1-legacy removal |
| 0.5.0 | 2026-02-07 | Agent Teams, /cs-team, team hooks, 11 commands, 13 hooks |
| 0.4.0 | 2026-02-07 | Hooks, tests, /cs-init, SDK integration, 10 commands, 9 profiles |
| 0.2.0 | 2026-02-01 | Native-first pivot, 4 commands, 3 profiles |
| 0.1.0 | 2026-02-01 | Foundation, memory pattern, simplified scope |
| 0.0.1 | 2026-02-01 | Initial setup |
