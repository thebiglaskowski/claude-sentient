# Changelog

All notable changes to the Prompts Library will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

#### Anthropic Cookbook Patterns (v4.4)
Integrated patterns from [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks):

**Instant Context Compaction (`smart-context.md` v2.0)**
- Proactive background summarization before hitting limits
- Soft thresholds at 50/70/85% trigger background work
- Pre-built summaries swap in instantly (zero wait time)
- Prompt caching reduces compaction cost by ~80%
- Preserves user corrections verbatim as preferences

**Query Classification (`queue-manager.md` v4.0)**
- Depth-first vs breadth-first vs straightforward classification
- Subagent count guidelines (1 for simple, 3-5 medium, 5-20 complex)
- Intelligent delegation with clear task boundaries
- Synthesis responsibility stays with leader (never delegate final output)

**Evaluator-Optimizer Pattern (NEW SKILL)**
- Evaluate-refine feedback loops until quality threshold met
- Works with any quality gate (tests, security audit, etc.)
- Configurable thresholds, max iterations, exit conditions
- Tracks iteration history with score progression

**Metaprompt Generator (NEW COMMAND)**
- `/cc-prompt` generates well-structured prompts from task descriptions
- Uses metaprompt technique to solve "blank page problem"
- Outputs in claude-conductor format (Role, Steps, Output, Rules)
- Includes variable placeholders and usage notes

**Prompt Evaluation (NEW QUALITY PROMPT)**
- `PROMPT_EVAL.md` for systematic prompt testing
- Three grading methods: code-based, model-based, human
- Test case categories: happy path, edge cases, adversarial
- Iteration tracking for prompt refinement

#### New Files
- `skills/orchestration/evaluator-optimizer.md` — Evaluate-improve feedback loops
- `commands/cc-prompt.md` — Metaprompt generator command
- `quality/PROMPT_EVAL.md` — Prompt evaluation framework

### Changed
- `skills/optimization/smart-context.md` → v2.0 with instant compaction
- `skills/orchestration/queue-manager.md` → v4.0 with query classification
- Skills count: 68 (was 67)
- Commands count: 38 (was 37)

#### Integration Tightening (v4.4.1)
Improved cohesion between new v4.4 features and existing autonomous workflow:

- **Query Classification in Phase 1** — Classification now happens at the start of CONTEXTUALIZE
  before context loading, enabling smarter context decisions
- **Evaluator-Optimizer in Phase 6** — Quality gate failures now trigger evaluator-optimizer
  feedback loops (max 3 iterations) before adding to work queue
- **Cache Availability Config** — `smart-context.md` now includes deployment-specific cache
  availability checks (API, Bedrock, Vertex, self-hosted)
- **Leader/Worker Role Transitions** — `meta-cognition.md` now documents how query classification
  maps to orchestration roles (Leader, Coordinator, Worker, Direct Executor)
- **Autonomous Loop Skills Table** — Added `evaluator-optimizer` and `queue-manager` to
  integrated skills list

---

#### Comprehensive Test Suite
New pytest-based test infrastructure validating all prompt components:
- **validators/** — Core validation logic (frontmatter, markdown, code blocks, cross-references)
- **schemas/** — Component-specific validation schemas
- **1,496 tests** covering structure, content quality, and edge cases
- Test execution time: ~9 seconds

Test files:
- `test_commands.py` — 37 commands with frontmatter and XML sections
- `test_skills.py` — 61 skills with triggers and content depth
- `test_agents.py` — 15 agents with tools and required sections
- `test_patterns.py` — 7 patterns with code examples
- `test_snippets.py` — 10 snippets with syntax validation
- `test_rules.py` — 13 rules with section requirements
- `test_cross_references.py` — Validates @rules/, @patterns/, snippet: references
- `test_cohesiveness.py` — Platform integration and meta-cognition validation
- `test_quality.py` — TODO markers, placeholders, broken links
- `test_consistency.py` — Project-wide naming and structure consistency
- `test_negative_cases.py` — Edge case and error handling validation

#### New Snippets
- `api/fastapi-endpoint.md` — Python FastAPI endpoint with Pydantic validation
- `api/go-handler.md` — Go HTTP handlers with middleware patterns
- `devops/github-action.md` — CI/CD workflows (Node, Python, Docker)
- `testing/go-test.md` — Go table-driven tests with mocks and testcontainers

#### Command Index
- `commands/_index.md` — Organized index of all 37 commands by category

### Changed
- **tests/README.md** — Complete rewrite documenting new test architecture
- **Snippet count** — Now 9 snippets (was 5)

---

## [4.3.0] - 2026-01-31

### Added

#### Multi-Registry Discovery System
- **Multi-Registry Support** — `/cc-scout-skills` now searches multiple registries simultaneously
  - skills.sh (33,000+ skills, multi-agent ecosystem)
  - aitmpl.com (Claude Code-specific: 200+ skills, 48+ agents, commands, hooks, MCPs)
- **Intelligent Scoring Algorithm** — Resources ranked 0-100 based on:
  - Technology match (30%): Exact, partial, or related matches
  - Source reputation (25%): Official, trusted, or community sources
  - Specificity (20%): Claude Code-specific vs multi-agent
  - Completeness (15%): Full stack vs skills only
  - Recency (10%): How recently updated
- **Auto-Install Tiers** — Tiered installation based on confidence:
  - Auto-install (≥80): High confidence, install with confirmation
  - Recommend (50-79): Good match, user selects
  - Mention (30-49): Low confidence, noted only
  - Skip (<30): Poor match, hidden
- **Deduplication** — Best resource selected when duplicates exist across registries
- **Resource Types** — Discovers skills, agents, commands, hooks, MCPs, and settings
- **Registry Configuration** — `.claude/config/registries.md` for extensible registry management
- **Automation Clarity** — All documentation clearly indicates automated vs manual steps

#### New Configuration
- `.claude/config/registries.md` — Registry definitions, scoring weights, trusted sources

### Changed
- **skill-scout.md** upgraded to v2.0 with multi-registry support
- **cc-scout-skills.md** expanded with scoring, deduplication, and new flags
- **template-registry.md** aligned (manual browsing vs automated discovery)
- **CLAUDE.md** updated to v4.3 with multi-registry features
- **QUICK_REFERENCE.md** updated with Skill Registries section

---

## [4.2.0] - 2026-01-31

### Added

#### Plugin Support
- **PLUGINS.md** — Complete guide for Claude Code plugins
- **Supermemory Integration** — Persistent memory across sessions
  - Automatic context injection on session start
  - Conversation capture and session summaries
  - Codebase indexing with `/claude-supermemory:index`
  - Super-search skill for memory queries
- Plugin troubleshooting section in TROUBLESHOOTING.md
- Plugin quick reference in QUICK_REFERENCE.md

### Changed
- Updated SETUP.md with plugin installation section
- Updated CLAUDE.md with v4.2 features and plugin references
- Updated TROUBLESHOOTING.md table of contents

---

## [4.1.0] - 2026-01-31

### Added

#### Swarm Orchestration
- **Swarm Mode** (`--swarm` flag) — Self-organizing workers for parallel task execution
  - Workers claim tasks from shared pool
  - No coordinator bottleneck
  - Configurable worker count with `--workers=N`
- **Task Dependencies** — `blockedBy`/`blocks` fields for automatic pipeline unblocking
  - Linear, fan-out, fan-in, and diamond patterns
  - Automatic status transitions when dependencies complete
- **Plan Approval** — Leader approval workflow for risky/breaking changes
  - Auto-triggers for schema changes, breaking APIs, security configs
  - Configurable approval thresholds

#### New Skills (3)
- `swarm-mode` — Self-organizing worker coordination
- `task-dependencies` — Automatic pipeline progression
- `plan-approval` — Safety gates for risky changes

#### Documentation
- `SWARM_ARCHITECTURE.md` — Master architecture document for swarm components
- Swarm mode examples in EXAMPLES.md
- Swarm troubleshooting in TROUBLESHOOTING.md

### Changed
- **queue-manager** upgraded to v3.0 with dependency support
- **meta-cognition** enhanced with orchestration decision tree
- **cc-loop command** now supports `--swarm` and `--workers` flags
- Skills count: 67 (was 64)

---

## [4.0.0] - 2026-01-30

### ⚠️ BREAKING CHANGES

- **All commands now namespaced with `cc-` prefix** — Prevents conflicts with other tools
  - `/review` → `/cc-review`
  - `/loop` → `/cc-loop`
  - `/commit` → `/cc-commit`
  - All 37 commands renamed with `cc-` prefix

### Added

#### Pattern Library (`@patterns/*`)
New reusable architecture and design patterns system:
- `@patterns/repository` — Data access abstraction (TypeScript, Python, Go)
- `@patterns/service-layer` — Business logic organization
- `@patterns/retry-with-backoff` — Handle transient failures with exponential backoff
- `@patterns/circuit-breaker` — Prevent cascade failures
- `@patterns/error-boundary` — Contain failures (React, Vue, Node)
- `@patterns/pagination` — Cursor and offset pagination
- `@patterns/strategy` — Interchangeable algorithms
- `@patterns/feature-flag` — Gradual feature rollout
- `@patterns/arrange-act-assert` — Testing pattern
- Pattern index at `.claude/patterns/_index.md`

#### Snippet Registry (`snippet:*`)
New indexed code templates system:
- `snippet:express-route` — Express.js route with Zod validation
- `snippet:react-component` — Multiple React component patterns
- `snippet:jest-test` — Jest test templates
- `snippet:error-class` — Custom error hierarchy
- `snippet:dockerfile` — Multi-stage Dockerfiles (Node, Python, Go, React)
- Snippet index at `.claude/snippets/_index.md`

#### New Commands
- `/cc-revert` — Smart git revert that understands logical work units
  - Analyzes commit relationships and dependencies
  - Reverts complete features, not partial changes
  - Preview mode shows impact before reverting
  - Supports: commit hash, feature branch, time window ("last 2 hours")
- `/cc-analyze` — Brownfield codebase analysis
  - Auto-detects tech stack and dependencies
  - Maps architectural patterns
  - Discovers coding conventions
  - Identifies testing patterns and coverage
  - Flags issues and technical debt

#### New Skills
- `brownfield-analyzer` — Auto-triggers on existing codebases
  - Detects conventions, architecture, tech stack
  - Generates PROJECT_PROFILE.md

#### Context Management (AIABS-Inspired)
- **Context Budget Monitor** (`context-budget-monitor`) — Prevents context window bloat
  - Tracks estimated context usage with visual indicators
  - Thresholds: Green (<50%), Yellow (50-70%), Orange (70-85%), Red (>85%)
  - Auto-suggests spawning sub-agents when context is constrained
  - Strategies: summarization, agent offloading, incremental reading

#### Parallel Execution
- **Parallel Task Decomposer** (`parallel-task-decomposer`) — Breaks complex tasks into concurrent units
  - Module-based decomposition (split by feature/module)
  - Concern-based decomposition (frontend/backend/database)
  - Layer-based decomposition (API/service/repository)
  - Test-Implementation parallel (write tests while implementing)
  - Decision tree for when to parallelize vs. sequence

#### Traceability
- **Decision Logger** (`decision-logger`) — Tracks significant decisions with rationale
  - Categories: TECH, ARCH, TRADE, SCOPE, SEC, PERF, FIX, DEFER
  - Structured format with context, alternatives, rationale, implications
  - Links decisions to implementing commits
  - State file: `DECISIONS_LOG.md`

#### Rollback Capability
- **Commit Checkpoint** (`commit-checkpoint`) — Creates verified commits for easy rollback
  - Creates checkpoint commits after verified features
  - Includes decision references in commit messages
  - Enables easy rollback to known-good state
  - State file: `CHECKPOINTS.md`

#### Loop Enhancements
- **Phase 6.25: CHECKPOINT** — New loop phase after quality gates pass
  - Creates verified commit when feature passes all gates
  - Updates CHECKPOINTS.md with rollback point
  - References relevant decisions

#### New State Files
- `DECISIONS_LOG.md` — Template for decision tracking
- `CHECKPOINTS.md` — Template for checkpoint history with rollback guide
- `LOOP_STATE_TEMPLATE.md` — Enhanced loop state with context budget, decisions, checkpoints

### Changed

- **Version bump to 4.0.0** — Major version due to breaking command changes
- **README.md** — Complete rewrite for v4.0
  - Updated all command references to use `cc-` prefix
  - Added Pattern Library section with examples
  - Added Snippet Registry section with categories
  - Updated component counts (37 commands, 15+ patterns, 20+ snippets)
- **CLAUDE.md** — Updated to v4.0
  - Added Pattern Library and Snippet Registry sections
  - Updated all command references
  - Added new workflows with patterns/snippets
- **QUICK_REFERENCE.md** — Complete rewrite
  - All commands now show `cc-` prefix
  - Added Patterns section with category table
  - Added Snippets section with usage examples
  - Updated quick workflows
- **All 37 command files** — Updated `name` field to include `cc-` prefix

### Migration Guide

To migrate from v3.x to v4.0:

1. **Update command usage** — Add `cc-` prefix to all commands
   ```
   # Before (v3.x)
   /review, /loop, /commit

   # After (v4.0)
   /cc-review, /cc-loop, /cc-commit
   ```

2. **Use new features**
   ```
   # Load patterns
   @patterns/repository

   # Request snippets
   snippet:express-route

   # Analyze existing code
   /cc-analyze

   # Smart revert
   /cc-revert feature-auth --preview
   ```

---

## [3.1.0] - 2026-01-29

### Added
- **MCP Server Awareness** — System now detects and inventories available MCP servers
  - CAPABILITY_INVENTORY.md includes comprehensive MCP discovery guidance
  - meta-cognition skill checks for MCP servers at session start
  - Documented `.mcp.json` location in project root (common convention)
- **Project Logo** — Added claude-conductor.png logo to README
- **Archive Folder** — Added `archive/` folder for deprecated prompts per CLAUDE.md process
- **LICENSE File** — Added MIT license file

### Changed
- **README.md**
  - Added warning/disclaimer section for experimental nature
  - Clarified "By the Numbers" scope (includes template folder)
  - Added all 27 prompts to Prompts Library section (was missing 10+)
  - Added Documentation and Refactoring sections
- **MCP Documentation**
  - MCP_SERVERS.md clarifies `.mcp.json` can be in project root
  - CONFIGURATION.md updated with all MCP config locations
  - QUICK_REFERENCE.md now includes MCP section

### Fixed
- Missing prompts in README (BUG_HUNT, DEPENDENCY_AUDIT, FINAL_COMPLETION_AUDIT, PERFORMANCE_AUDIT, TECH_DEBT_TRACKER, all Documentation prompts, REFACTORING_ENGINE)

---

## [1.2.0] - 2026-01-28

### Added

#### New Skills (21 new)
- **Automation Skills**
  - `changelog-automation` - Auto-generate CHANGELOG from git commits
  - `docs-generator` - Generate documentation from code
  - `compound-commands` - Chain commands (/ship, /quick-fix, etc.)
  - `snippet-library` - Reusable code patterns and boilerplate

- **Optimization Skills**
  - `dependency-checker` - Verify tools before running commands
  - `auto-update-checker` - Check for prompts library updates
  - `metrics-logger` - Track usage patterns
  - `session-memory` - Avoid redundant work within session
  - `error-recovery` - Auto-retry and smart recovery
  - `smart-context` - Load only relevant context
  - `dry-run-mode` - Preview changes before applying
  - `undo-history` - Track and revert changes
  - `file-watcher` - React to file changes automatically

- **Project Management Skills**
  - `health-dashboard` - Project health metrics overview
  - `dependency-tracker` - Track outdated/vulnerable dependencies
  - `project-templates` - Scaffold new projects
  - `claude-md-manager` - Create/improve project-specific CLAUDE.md

- **Collaboration Skills**
  - `cross-project-patterns` - Share patterns across projects
  - `team-sharing` - Sync prompts/skills with team

- **CI/CD Skills**
  - `ci-cd-integration` - Use prompts in pipelines
  - `prompt-testing` - Validate prompt quality

#### New Commands
- `/gitignore` - Smart gitignore management based on tech stack
- `/claude-md` - Create or improve project-specific CLAUDE.md

#### Documentation
- Comprehensive MCP_SERVERS.md rewrite with step-by-step setup
- Platform-specific instructions (Windows, macOS, Linux)
- Quick reference card
- Configuration reference
- Troubleshooting guide
- Example workflows
- Contributing guide
- Upgrade guide

### Changed
- CLAUDE.md reorganized with skill categories
- READMEs updated with accurate counts and features
- Model routing expanded with detailed command mapping

---

## [1.1.0] - 2026-01-28

### Added

#### New Skills (10 new)
- `gitignore-manager` - Auto-manage .gitignore for tech stack
- `project-init` - Full project initialization automation
- `dependency-checker` - Verify required tools
- `auto-update-checker` - Check for updates
- `metrics-logger` - Usage tracking
- `session-memory` - Avoid redundant analysis
- `error-recovery` - Smart error handling
- `smart-context` - Context pruning
- `dry-run-mode` - Preview changes
- `project-templates` - Project scaffolding

#### New Commands
- `/gitignore` - Update .gitignore for tech stack
- `/map-project` - Generate project context map
- `/scout-skills` - Install skills from skills.sh

#### Automation
- Install scripts (install.sh, install.ps1)
- Setup and SessionStart hooks
- PostToolUse hooks for Prettier formatting
- Pre-commit gitignore checks

### Changed
- Model routing added to all commands (Haiku/Sonnet/Opus recommendations)
- Checklists converted to auto-loading skills
- CLAUDE.md split into smaller on-demand skills

---

## [1.0.0] - 2026-01-28

### Added

#### Initial Release
- **28 Prompts** across 7 categories
- **14 Skills** for Claude Code
- **17 Commands** for quick access

#### Categories
- Planning: BLUEPRINT_AUDITOR, FEATURE_SPEC_WRITER
- Execution: PROJECT_EXECUTION, DAILY_BUILD, SPIKE_RESEARCH
- Quality: CODE_REVIEW, SECURITY_AUDIT, TEST_COVERAGE_GATE, etc.
- Documentation: ADR_WRITER, ONBOARDING_GUIDE, etc.
- Operations: RELEASE_CHECKLIST, MIGRATION_PLANNER, etc.
- Refactoring: REFACTORING_ENGINE
- Skills: pre-commit, pre-merge, model-routing, etc.

#### Features
- Context7 MCP integration for documentation lookup
- Drop-in .claude template for projects
- Severity levels (S0-S3) standardized
- Update Bundle pattern for documentation

---

## Version History

| Version | Date | Skills | Commands | Highlights |
|---------|------|--------|----------|------------|
| 4.4.0 | 2026-01-31 | 68 | 38 | Anthropic Cookbook patterns: instant compaction, query classification, evaluator-optimizer, metaprompt, prompt eval |
| 4.3.0 | 2026-01-31 | 67 | 37 | Multi-registry discovery (skills.sh + aitmpl.com), intelligent scoring, auto-install tiers |
| 4.2.0 | 2026-01-31 | 67 | 37 | Plugin support, Supermemory integration, persistent memory |
| 4.1.0 | 2026-01-31 | 67 | 37 | Swarm orchestration, task dependencies, plan approval |
| 4.0.0 | 2026-01-30 | 64 | 37 | Namespaced commands, patterns, snippets, context budget, parallel decomposition, decision logging, checkpoints |
| 3.1.0 | 2026-01-29 | 58 | 35 | MCP awareness, project logo, archive folder |
| 1.2.0 | 2026-01-28 | 34 | 21 | Full automation, collaboration |
| 1.1.0 | 2026-01-28 | 24 | 20 | Automation, model routing |
| 1.0.0 | 2026-01-28 | 14 | 17 | Initial release |
