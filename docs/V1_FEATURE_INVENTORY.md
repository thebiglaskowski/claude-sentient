# Claude Conductor v1 — Complete Feature Inventory

> **Version:** v4.3 (Multi-Registry Discovery)
> **Total Components:** 188+ markdown files
> **Purpose:** Reference for v2 feature parity and migration planning

---

## Table of Contents

1. [Summary Statistics](#summary-statistics)
2. [Skills (68)](#skills-68-total)
3. [Commands (37)](#commands-37-total)
4. [Agents (15)](#agents-15-total)
5. [Patterns (30+)](#patterns-30-total)
6. [Snippets (28)](#snippets-28-total)
7. [Rules (13)](#rules-13-total)
8. [Quality Gates (15)](#quality-gates-15-total)
9. [Autonomous Loop (10 Phases)](#autonomous-loop-10-phases)
10. [Swarm Orchestration](#swarm-orchestration)
11. [Registries & Discovery](#registries--multi-registry-discovery)
12. [Hooks System (12)](#hooks-system-12-total)
13. [Plugins System](#plugins-system)
14. [Context Management](#context-management)
15. [Configuration & State](#configuration--state-management)
16. [Advanced Features](#advanced-features)
17. [Documentation](#documentation--support)
18. [Version History](#version-history)

---

## Summary Statistics

| Category | Count | Location |
|----------|-------|----------|
| **Skills** | 68 | `.claude/skills/[category]/` |
| **Commands** | 37 | `.claude/commands/` |
| **Agents** | 15 | `.claude/agents/` |
| **Patterns** | 30+ | `.claude/patterns/[category]/` |
| **Snippets** | 28 | `.claude/snippets/[category]/` |
| **Rules** | 13 | `.claude/rules/` |
| **Quality Gates** | 15 | `QUALITY_GATES.md` |
| **Loop Phases** | 10 | `LOOP_WORKFLOW.md` |
| **Hooks** | 12 | `HOOKS_REFERENCE.md` |
| **Registries** | 2 | `config/registries.md` |
| **Documentation Files** | 19 | `.claude/*.md` |
| **Total .md Files** | 188+ | `.claude/` (recursive) |

---

## Skills (68 total)

Skills are auto-triggered behaviors that activate based on context patterns.

### Orchestration Skills (22)

| Skill | Description | File |
|-------|-------------|------|
| `task-orchestrator` | Auto-selects rules/agents based on task type | `orchestration/task-orchestrator.md` |
| `requirements-clarifier` | Asks clarifying questions before major work | `orchestration/requirements-clarifier.md` |
| `autonomous-loop` | Core 10-phase execution loop with 15 quality gates | `orchestration/autonomous-loop.md` |
| `meta-cognition` | Self-aware tool selection from capability inventory | `orchestration/meta-cognition.md` |
| `multi-perspective` | Analyzes from multiple expert viewpoints | `orchestration/multi-perspective.md` |
| `queue-manager` | Manages work items with dependency tracking | `orchestration/queue-manager.md` |
| `definition-of-done` | Universal completion criteria verification | `orchestration/definition-of-done.md` |
| `browser-verification` | UI verification with screenshots/accessibility | `orchestration/browser-verification.md` |
| `visual-diff` | Screenshot comparison and visual regression detection | `orchestration/visual-diff.md` |
| `result-synthesizer` | Merges agent/worker outputs | `orchestration/result-synthesizer.md` |
| `parallel-task-decomposer` | Breaks tasks into parallel units | `orchestration/parallel-task-decomposer.md` |
| `decision-logger` | Captures decisions for traceability | `orchestration/decision-logger.md` |
| `extended-thinking` | Deep reasoning with extended context | `orchestration/extended-thinking.md` |
| `parallel-exploration` | Multiple concurrent explorations | `orchestration/parallel-exploration.md` |
| `subagent-research` | Isolated research via subagents | `orchestration/subagent-research.md` |
| `argument-parser` | CLI argument parsing ($1, --flag syntax) | `orchestration/argument-parser.md` |
| `smart-context-v3` | Enhanced context loading with !command syntax | `orchestration/smart-context-v3.md` |
| `error-classifier` | Classifies errors and suggests recovery | `orchestration/error-classifier.md` |
| `parallel-agents` | Coordinates parallel agent execution | `orchestration/parallel-agents.md` |
| `swarm-mode` | Self-organizing workers claiming from task pool | `orchestration/swarm-mode.md` |
| `task-dependencies` | Automatic pipeline unblocking (blockedBy/blocks) | `orchestration/task-dependencies.md` |
| `plan-approval` | Leader approval workflow for risky changes | `orchestration/plan-approval.md` |
| `evaluator-optimizer` | Iterative refinement feedback loops | `orchestration/evaluator-optimizer.md` |

### Quality Skills (7)

| Skill | Description | File |
|-------|-------------|------|
| `definition-of-done` | Completion criteria (DoD verification) | `quality/definition-of-done.md` |
| `self-critique` | Auto-critiques own code, identifies issues | `quality/self-critique.md` |
| `severity-levels` | S0-S3 issue classification | `quality/severity-levels.md` |
| `model-routing` | Choose haiku/sonnet/opus based on task | `quality/model-routing.md` |
| `commit-style` | Conventional commits formatting | `quality/commit-style.md` |
| `test-first` | TDD approach enforcement | `quality/test-first.md` |
| `no-guessing` | Require clarification for ambiguous requirements | `quality/no-guessing.md` |

### Workflow Skills (6)

| Skill | Description | File |
|-------|-------------|------|
| `pre-commit` | Pre-commit checklist | `workflow/pre-commit.md` |
| `pre-merge` | PR checklist | `workflow/pre-merge.md` |
| `pre-release` | Release checklist | `workflow/pre-release.md` |
| `commit-checkpoint` | Create verified commits for rollback | `workflow/commit-checkpoint.md` |
| `phase-workflow` | Project phase guidance | `workflow/phase-workflow.md` |
| `update-bundle-guide` | Update bundle creation helper | `workflow/update-bundle-guide.md` |

### Automation Skills (5)

| Skill | Description | File |
|-------|-------------|------|
| `changelog-automation` | Auto-update CHANGELOG.md | `automation/changelog-automation.md` |
| `docs-generator` | Auto-generate documentation | `automation/docs-generator.md` |
| `compound-commands` | Command chaining (/ship, /quick-fix) | `automation/compound-commands.md` |
| `snippet-library` | Boilerplate code access | `automation/snippet-library.md` |
| `modern-tech-checker` | Technology modernization suggestions | `automation/modern-tech-checker.md` |

### Optimization Skills (12)

| Skill | Description | File |
|-------|-------------|------|
| `smart-context` | Load relevant context only | `optimization/smart-context.md` |
| `context-budget-monitor` | Prevent context bloat, suggest sub-agents | `optimization/context-budget-monitor.md` |
| `session-memory` | Avoid re-reading files | `optimization/session-memory.md` |
| `dry-run-mode` | Preview changes without executing | `optimization/dry-run-mode.md` |
| `error-recovery` | Recovery strategies | `optimization/error-recovery.md` |
| `metrics-logger` | Usage tracking display | `optimization/metrics-logger.md` |
| `metrics-writer` | Write JSONL metrics | `optimization/metrics-writer.md` |
| `undo-history` | Rollback changes (git revert) | `optimization/undo-history.md` |
| `file-watcher` | Auto-run on file changes | `optimization/file-watcher.md` |
| `dependency-checker` | Check dependencies | `optimization/dependency-checker.md` |
| `auto-update-checker` | Template update detection | `optimization/auto-update-checker.md` |
| `prompt-feedback` | Self-improvement loop | `optimization/prompt-feedback.md` |

### Project Management Skills (10)

| Skill | Description | File |
|-------|-------------|------|
| `project-init` | Full project setup | `project-management/project-init.md` |
| `claude-md-manager` | Create/improve CLAUDE.md | `project-management/claude-md-manager.md` |
| `skill-scout` | Multi-registry discovery (skills.sh + aitmpl.com) | `project-management/skill-scout.md` |
| `gitignore-manager` | Manage .gitignore | `project-management/gitignore-manager.md` |
| `health-dashboard` | Project status overview | `project-management/health-dashboard.md` |
| `dependency-tracker` | Check outdated/vulnerable dependencies | `project-management/dependency-tracker.md` |
| `frontmatter-generator` | Add v2.0 frontmatter | `project-management/frontmatter-generator.md` |
| `frontend-backend-sync` | API change sync check | `project-management/frontend-backend-sync.md` |
| `project-templates` | Project scaffolding | `project-management/project-templates.md` |
| `brownfield-analyzer` | Detect existing patterns/conventions | `project-management/brownfield-analyzer.md` |

### CI/CD Skills (2)

| Skill | Description | File |
|-------|-------------|------|
| `ci-cd-integration` | CI/CD pipeline configuration | `ci-cd/ci-cd-integration.md` |
| `prompt-testing` | Prompt quality testing | `ci-cd/prompt-testing.md` |

### Collaboration Skills (3)

| Skill | Description | File |
|-------|-------------|------|
| `cross-project-patterns` | Share patterns between projects | `collaboration/cross-project-patterns.md` |
| `team-sharing` | Sync prompts with team | `collaboration/team-sharing.md` |
| `template-registry` | Manual registry browsing | `collaboration/template-registry.md` |

### Environment Skills (1)

| Skill | Description | File |
|-------|-------------|------|
| `conda-aware` | Conda environment handling | `environment/conda-aware.md` |

---

## Commands (37 total)

Commands are explicit user invocations using the `/cc-*` namespace.

### Planning Commands (3)

| Command | Description | Usage |
|---------|-------------|-------|
| `/cc-plan` | Create feature specification | `/cc-plan [feature]` |
| `/cc-audit-blueprint` | Validate plan before building | `/cc-audit-blueprint` |
| `/cc-spike` | Technical research and investigation | `/cc-spike [topic]` |

### Execution Commands (3)

| Command | Description | Usage |
|---------|-------------|-------|
| `/cc-daily` | Continue development work | `/cc-daily` |
| `/cc-loop` | Autonomous work loop (10 phases, 15 gates) | `/cc-loop [task]` |
| `/cc-analyze` | Brownfield codebase analysis | `/cc-analyze` |

### Quality Commands (9)

| Command | Description | Usage |
|---------|-------------|-------|
| `/cc-review` | Code review with patterns/tests | `/cc-review [file\|PR]` |
| `/cc-test` | Test coverage gate | `/cc-test` |
| `/cc-secure` | Security audit (OWASP) | `/cc-secure` |
| `/cc-assess` | Full codebase audit | `/cc-assess` |
| `/cc-fix` | Bug hunting and fixing | `/cc-fix [issue]` |
| `/cc-refactor` | Safe refactoring | `/cc-refactor [target]` |
| `/cc-perf` | Performance audit | `/cc-perf` |
| `/cc-deps` | Dependency audit | `/cc-deps` |
| `/cc-debt` | Technical debt tracking | `/cc-debt` |

### Frontend Commands (4)

| Command | Description | Usage |
|---------|-------------|-------|
| `/cc-ui` | UI/UX audit | `/cc-ui` |
| `/cc-terminal` | Terminal UI audit | `/cc-terminal` |
| `/cc-seo` | SEO audit | `/cc-seo` |
| `/cc-sync` | Frontend-backend sync check | `/cc-sync` |

### Git & Version Control Commands (3)

| Command | Description | Usage |
|---------|-------------|-------|
| `/cc-commit` | Create well-formatted commit | `/cc-commit` |
| `/cc-pr` | Create pull request with GitHub CLI | `/cc-pr` |
| `/cc-revert` | Smart git revert (logical units) | `/cc-revert [commit]` |

### Operations Commands (4)

| Command | Description | Usage |
|---------|-------------|-------|
| `/cc-release` | Release checklist | `/cc-release [version]` |
| `/cc-postmortem` | Incident analysis | `/cc-postmortem [incident]` |
| `/cc-migrate` | Migration planning | `/cc-migrate [target]` |
| `/cc-closeout` | Complete milestone | `/cc-closeout` |

### Documentation Commands (4)

| Command | Description | Usage |
|---------|-------------|-------|
| `/cc-changelog` | Update CHANGELOG.md | `/cc-changelog` |
| `/cc-adr` | Document architecture decisions | `/cc-adr [decision]` |
| `/cc-docs` | Generate/update documentation | `/cc-docs` |
| `/cc-onboard` | Create onboarding guide | `/cc-onboard` |

### Team Commands (2)

| Command | Description | Usage |
|---------|-------------|-------|
| `/cc-standup` | Generate standup summary | `/cc-standup` |
| `/cc-retro` | Run sprint retrospective | `/cc-retro` |

### Setup Commands (6)

| Command | Description | Usage |
|---------|-------------|-------|
| `/cc-scaffold` | Generate project structure | `/cc-scaffold [type]` |
| `/cc-scout-skills` | Install skills from registries | `/cc-scout-skills [query]` |
| `/cc-map-project` | Generate project context map | `/cc-map-project` |
| `/cc-gitignore` | Update .gitignore for tech stack | `/cc-gitignore` |
| `/cc-claude-md` | Create/improve CLAUDE.md | `/cc-claude-md` |
| `/cc-prompt` | Generate well-structured prompts | `/cc-prompt [type]` |

---

## Agents (15 total)

Specialized subagents for focused domain expertise.

| Agent | Model | Specialty |
|-------|-------|-----------|
| `code-reviewer` | sonnet | Code review, patterns, tests |
| `security-analyst` | opus | OWASP, STRIDE, vulnerabilities |
| `test-engineer` | sonnet | Test writing, coverage analysis |
| `documentation-writer` | sonnet | README, API docs |
| `researcher` | sonnet | Technical research, spikes |
| `ui-ux-expert` | sonnet | Modern UI, accessibility |
| `terminal-ui-expert` | sonnet | CLI polish, spinners |
| `seo-expert` | sonnet | SEO optimization |
| `database-expert` | sonnet | Database optimization |
| `devops-engineer` | sonnet | CI/CD, Docker, K8s |
| `accessibility-expert` | sonnet | WCAG, ARIA |
| `performance-optimizer` | sonnet | Profiling, caching |
| `api-designer` | sonnet | REST/GraphQL design |
| `migration-specialist` | sonnet | DB migrations, upgrades |
| `prompt-engineer` | sonnet | AI prompt optimization |

---

## Patterns (30+ total)

Reusable architecture and design patterns.

### Architecture Patterns

| Pattern | Description |
|---------|-------------|
| `@patterns/repository` | Data access abstraction |
| `@patterns/service-layer` | Business logic organization |
| `@patterns/cqrs` | Read/write separation |
| `@patterns/event-sourcing` | Event-based state, audit trail |
| `@patterns/clean-architecture` | Dependency inversion |

### Creational Patterns

| Pattern | Description |
|---------|-------------|
| `@patterns/factory` | Encapsulate object creation |
| `@patterns/singleton` | Single instance guarantee |
| `@patterns/builder` | Complex construction |

### Structural Patterns

| Pattern | Description |
|---------|-------------|
| `@patterns/adapter` | Interface translation |
| `@patterns/decorator` | Add behavior dynamically |
| `@patterns/facade` | Simplify interface |
| `@patterns/composite` | Tree structures |

### Behavioral Patterns

| Pattern | Description |
|---------|-------------|
| `@patterns/observer` | Event subscription |
| `@patterns/strategy` | Swap algorithms |
| `@patterns/command` | Encapsulate actions |
| `@patterns/state-machine` | State transitions |

### Resilience Patterns

| Pattern | Description |
|---------|-------------|
| `@patterns/retry-with-backoff` | Handle transient failures |
| `@patterns/circuit-breaker` | Prevent cascade failures |
| `@patterns/bulkhead` | Isolate failures |
| `@patterns/timeout` | Bound wait time |

### Error Handling Patterns

| Pattern | Description |
|---------|-------------|
| `@patterns/error-boundary` | Contain failures gracefully |
| `@patterns/result-type` | Explicit error handling |
| `@patterns/global-handler` | Centralized error handling |

### API Patterns

| Pattern | Description |
|---------|-------------|
| `@patterns/pagination` | Large dataset handling |
| `@patterns/rate-limiting` | Throttle requests |
| `@patterns/versioning` | API evolution |
| `@patterns/hateoas` | Discoverable APIs |

### Testing Patterns

| Pattern | Description |
|---------|-------------|
| `@patterns/arrange-act-assert` | Test structure |
| `@patterns/test-doubles` | Mocks, stubs, fakes |
| `@patterns/fixture-factory` | Test data creation |

### Operations Patterns

| Pattern | Description |
|---------|-------------|
| `@patterns/feature-flag` | Toggle features |
| `@patterns/blue-green` | Zero-downtime deploy |
| `@patterns/canary` | Gradual rollout |

---

## Snippets (28 total)

Ready-to-use code templates.

### API Snippets (4)

| Snippet | Description |
|---------|-------------|
| `snippet:express-route` | Express.js handler |
| `snippet:fastapi-endpoint` | FastAPI endpoint |
| `snippet:go-handler` | Go HTTP handler |
| `snippet:nest-controller` | NestJS controller |

### React Snippets (4)

| Snippet | Description |
|---------|-------------|
| `snippet:react-component` | Functional component |
| `snippet:react-hook` | Custom hook |
| `snippet:react-context` | Context provider |
| `snippet:react-form` | Form with validation |

### Database Snippets (4)

| Snippet | Description |
|---------|-------------|
| `snippet:prisma-model` | Prisma schema model |
| `snippet:sql-migration` | SQL migration template |
| `snippet:typeorm-entity` | TypeORM entity |
| `snippet:sqlalchemy-model` | SQLAlchemy model |

### Testing Snippets (4)

| Snippet | Description |
|---------|-------------|
| `snippet:jest-test` | Jest test suite |
| `snippet:pytest-test` | Pytest test |
| `snippet:go-test` | Go testing |
| `snippet:vitest-test` | Vitest test |

### DevOps Snippets (3)

| Snippet | Description |
|---------|-------------|
| `snippet:dockerfile` | Multi-stage Dockerfile |
| `snippet:github-action` | GitHub Actions workflow |
| `snippet:docker-compose` | Docker Compose file |

### Utility Snippets (4)

| Snippet | Description |
|---------|-------------|
| `snippet:error-class` | Custom error class |
| `snippet:logger` | Structured logger |
| `snippet:env-config` | Environment config |
| `snippet:retry-helper` | Retry with backoff |

### Validation Snippets (3)

| Snippet | Description |
|---------|-------------|
| `snippet:zod-schema` | Zod schema |
| `snippet:pydantic-model` | Pydantic model |
| `snippet:joi-schema` | Joi schema |

---

## Rules (13 total)

Topic-specific guidance loaded on-demand via `@rules/[name]`.

| Rule | Topics Covered |
|------|----------------|
| `@rules/security` | OWASP, authentication, secrets, cryptography |
| `@rules/testing` | Coverage, naming, mocks, TDD |
| `@rules/git-workflow` | Commits, branches, PRs, merges |
| `@rules/documentation` | README, comments, changelog |
| `@rules/code-quality` | Complexity, naming, dependencies |
| `@rules/api-design` | REST, errors, versioning, pagination |
| `@rules/error-handling` | Error hierarchy, logging, recovery |
| `@rules/ui-ux-design` | Spacing, typography, accessibility |
| `@rules/terminal-ui` | Spinners, colors, progress bars |
| `@rules/performance` | Optimization, caching, Core Web Vitals |
| `@rules/database` | Schema, indexing, migrations |
| `@rules/logging` | Structured logs, levels, correlation |
| `@rules/prompt-engineering` | AI prompts, techniques, Chain-of-Thought |

---

## Quality Gates (15 total)

All gates are **BLOCKING** — no exceptions allowed.

### Code Quality Gates (11)

| # | Gate | Description | Criteria |
|---|------|-------------|----------|
| 1 | **PRE-FLIGHT** | Environment ready | Git clean, deps installed |
| 2 | **LINT** | Code style | Zero lint errors |
| 3 | **TYPE** | Type safety | TypeScript/mypy pass |
| 4 | **UNIT** | Unit tests | Coverage threshold met |
| 5 | **INTEGRATION** | Integration tests | All passing |
| 6 | **SECURITY** | Vulnerability scan | No high/critical |
| 7 | **PERFORMANCE** | Speed benchmarks | Within thresholds |
| 8 | **BROWSER** | UI verification | Screenshots match |
| 9 | **A11Y** | Accessibility | WCAG compliant |
| 10 | **DOCS** | Documentation | Complete and current |
| 11 | **MODERN** | Tech currency | No deprecated APIs |

### Work Completion Gates (4)

| # | Gate | Description | Criteria |
|---|------|-------------|----------|
| 12 | **WORK_QUEUE** | Tasks complete | All items done |
| 13 | **KNOWN_ISSUES** | Issues resolved | No S0/S1 open |
| 14 | **GIT_STATE** | Git status | Clean, committed |
| 15 | **DOD** | Definition of Done | All criteria met |

---

## Autonomous Loop (10 Phases)

The core execution engine with meta-cognition and checkpoints.

```
Phase 1: CONTEXTUALIZE
    ├── Load relevant context
    ├── Query classification (v4.4)
    └── Inject rules/patterns

Phase 2: ASSESS
    ├── Understand current state
    └── Identify gaps

Phase 2.5: META-COGNITION
    ├── Review capability inventory
    └── Select optimal tools/agents

Phase 3: PLAN
    ├── Prioritize work
    ├── Decompose into parallel units
    └── Define dependencies

Phase 4: BUILD
    ├── Implement changes
    ├── Use patterns/snippets
    └── Apply rules

Phase 5: TEST
    ├── Run test suite
    └── Browser verification

Phase 6: QUALITY
    ├── Execute all 15 gates
    └── Trigger evaluator-optimizer if failed

Phase 6.25: CHECKPOINT
    ├── Create verified commit
    └── Enable rollback point

Phase 6.5: REASSESS
    ├── Check if stuck
    └── Spawn specialists if needed

Phase 7: EVALUATE
    ├── Check completion criteria
    └── Update work queue

Phase 8: RECOVER (if needed)
    ├── Classify error
    └── Apply recovery strategy
```

### Loop Exit Criteria

- All 15 quality gates pass (2 consecutive iterations)
- Work queue empty
- Definition of Done complete
- No S0/S1 severity issues
- Clean git state

---

## Swarm Orchestration

Advanced multi-agent coordination (v4.1).

### Task Dependencies

```markdown
| Task | Status | Blocked By | Blocks |
|------|--------|------------|--------|
| T001 | complete | — | T002, T003 |
| T002 | pending | — | T004 |
| T003 | pending | — | T004 |
| T004 | blocked | T002, T003 | — |
```

- `blockedBy` / `blocks` syntax for pipelines
- Automatic unblocking when dependencies complete
- Priority-aware task claiming

### Swarm Mode

- Self-organizing workers claim from shared pool
- No coordinator bottleneck
- Parallel execution with result synthesis
- Trigger: `/cc-loop --swarm "task"`

### Plan Approval

- Detects risky changes (security, breaking)
- Leader approval required
- Audit trail in DECISIONS_LOG.md
- Pauses loop until approval

### Inter-Agent Messaging

- Lightweight coordination
- Message board for findings
- Worker discovery and status

---

## Registries & Multi-Registry Discovery

Intelligent skill discovery across multiple sources (v4.3).

### Active Registries

| Registry | Priority | Content |
|----------|----------|---------|
| **aitmpl.com** | 1 (Primary) | 200+ skills, 48+ agents, 21+ commands, hooks, MCPs |
| **skills.sh** | 2 (Secondary) | 33,000+ multi-agent skills |

### Intelligent Scoring (0-100)

| Factor | Weight |
|--------|--------|
| Technology Match | 30% |
| Source Reputation | 25% |
| Specificity | 20% |
| Completeness | 15% |
| Recency | 10% |

### Auto-Install Thresholds

| Score | Action |
|-------|--------|
| ≥ 80 | Auto-install |
| 50-79 | Recommend (ask user) |
| 30-49 | Mention (low confidence) |
| < 30 | Skip |

---

## Hooks System (12 total)

Automated lifecycle event handlers.

### Setup & Session Lifecycle

| Hook | Event | Description |
|------|-------|-------------|
| `setup-init.sh` | Setup | One-time project initialization |
| `session-start.sh` | SessionStart | Per-session init + capabilities |
| `context-injector.py` | UserPromptSubmit | Load context on prompt |
| `session-end.sh` | SessionEnd | Cleanup + metrics |

### Tool Execution

| Hook | Event | Description |
|------|-------|-------------|
| `bash-auto-approve.py` | PreToolUse | Auto-approve safe commands |
| `file-validator.py` | PreToolUse | Validate file writes |
| `post-edit.sh` | PostToolUse | Format/lint after edits |

### Error & Recovery

| Hook | Event | Description |
|------|-------|-------------|
| `error-recovery.py` | PostToolUseFailure | Classify and recover |
| `pre-compact.sh` | PreCompact | Backup state |

### Agent Coordination

| Hook | Event | Description |
|------|-------|-------------|
| `agent-tracker.py` | PreToolUse | Track subagent spawning |
| `agent-synthesizer.py` | PostToolUse | Merge subagent results |

### Verification

| Hook | Event | Description |
|------|-------|-------------|
| `dod-verifier.py` | — | STRICT DoD verification |

---

## Plugins System

Extend Claude Code with persistent memory (v4.2).

### Supermemory Plugin

| Feature | Description |
|---------|-------------|
| Persistent Memory | Cross-session knowledge |
| Auto-Inject Context | Relevant context loading |
| Capture Conversations | Save important exchanges |
| Session Summaries | Create summaries on end |

### Plugin Management

```bash
claude plugin install <plugin>
claude plugin list
```

---

## Context Management

### Context Files

| File | Purpose |
|------|---------|
| `CAPABILITY_INVENTORY.md` | Full tool/skill/pattern catalog |
| `CHECKPOINTS.md` | Verified commits for rollback |
| `DECISIONS_LOG.md` | Decision traceability |
| `LOOP_STATE_TEMPLATE.md` | Current work state |
| `PROJECT_MAP.md` | Generated project context |
| `SESSION_HISTORY.md` | Cross-session persistence |

### Smart Context Loading

| Feature | Description |
|---------|-------------|
| `!files` syntax | Selective file loading |
| `!recent` | Recent changes only |
| Auto-load rules | Based on task type |
| Budget monitoring | Spawn sub-agents if >70% |
| Session memory | Avoid re-reading files |

### Feedback System

| Directory | Content |
|-----------|---------|
| `feedback/successes/` | Positive outcomes |
| `feedback/failures/` | What went wrong |
| `feedback/improvements/` | Optimization suggestions |

---

## Configuration & State Management

### Configuration Files

| File | Purpose |
|------|---------|
| `.claude/CLAUDE.md` | Project-specific instructions |
| `.claude/settings.json` | Project settings |
| `.claude/config/registries.md` | Registry configuration |
| `.claude/.version` | Template version tracking |

### State Files

| File | Purpose |
|------|---------|
| `STATUS.md` | Current project state |
| `CHANGELOG.md` | Version history |
| `KNOWN_ISSUES.md` | Tracked limitations |
| `docs/decisions/` | Architecture Decision Records |

### Metrics & Feedback

| Directory | Purpose |
|-----------|---------|
| `.claude/metrics/` | Usage metrics (gitignored) |
| `.claude/history/` | Undo history (gitignored) |
| `.claude/feedback/` | Prompt improvement data |

---

## Advanced Features

### Extended Thinking

- Deep reasoning capabilities
- Multi-step analysis
- Complex problem solving
- Integrated with meta-cognition

### Parallel Task Decomposition

- Break tasks into parallel units
- Execute simultaneously
- Merge results efficiently
- Respect task dependencies

### Visual Regression Detection

- Screenshot comparison
- Multi-viewport testing
- Accessibility audit
- Layout shift detection (CLS)

### Brownfield Analysis

- Detect existing patterns
- Identify conventions
- Reverse-engineer architecture
- Generate project map

### Decision Logging

- Capture significant decisions
- Log rationale and alternatives
- Traceability for audit
- Review at closeout

### Query Classification (v4.4)

- Classify incoming requests
- Route to appropriate handlers
- Optimize resource allocation
- Adjust agent count

### Evaluator-Optimizer (v4.4)

- Iterative refinement loops
- Self-evaluation scoring
- Automated improvement
- Quality gate integration

### Instant Compaction (v4.4)

- Proactive context management
- Cache-aware optimization
- Background compaction
- Level-based triggers

---

## Documentation & Support

### Core Documentation (19 files)

| Document | Purpose |
|----------|---------|
| `_system.md` | System architecture v3.2 |
| `LOOP_WORKFLOW.md` | Complete /loop execution |
| `QUALITY_GATES.md` | All 15 gates with criteria |
| `SWARM_ARCHITECTURE.md` | Multi-agent coordination |
| `HOOKS_REFERENCE.md` | All 12 hooks |
| `PLUGINS.md` | Plugin system |
| `MCP_SERVERS.md` | MCP setup and integration |
| `CONFIGURATION.md` | Config reference |
| `PROMPT_TEMPLATE.md` | Prompt best practices |
| `QUICK_REFERENCE.md` | Cheat sheet |
| `TROUBLESHOOTING.md` | Common issues |
| `UPGRADE_GUIDE.md` | Migration guide |
| `V3_IMPLEMENTATION_BLUEPRINT.md` | Implementation status |
| `MCP_SETUP.md` | MCP installation |
| `ERROR_RECOVERY.md` | Error handling |
| `STATE_FILES.md` | State file schemas |
| `EXAMPLES.md` | Usage examples |
| `CAPABILITY_INVENTORY.md` | Full tool catalog |
| `REGISTRIES.md` | Registry documentation |

### Index Files

| Index | Content |
|-------|---------|
| `commands/_index.md` | Command reference |
| `skills/_index.md` | Skill index (searchable) |
| `agents/_index.md` | Agent definitions |
| `patterns/_index.md` | Pattern library |
| `snippets/_index.md` | Code snippets |
| `rules/_index.md` | Rule collection |

---

## Version History

| Version | Release | Key Features |
|---------|---------|--------------|
| **v4.4** | Latest | Anthropic Cookbook patterns (instant compaction, query classification, evaluator-optimizer) |
| **v4.3** | Current | Multi-registry discovery (skills.sh + aitmpl.com), intelligent scoring |
| **v4.2** | — | Plugin support, Supermemory integration |
| **v4.1** | — | Swarm orchestration, task dependencies, plan approval |
| **v4.0** | — | Namespaced commands, pattern library, snippet registry, 10-phase loop, 15 quality gates |
| **v3.x** | — | Initial skill system, autonomous loop |

---

## Migration Checklist for V2

All features listed above must be preserved and enhanced in V2:

- [ ] 68 skills → YAML format with schema validation
- [ ] 37 commands → YAML format with argument schemas
- [ ] 15 agents → Agent definition schema
- [ ] 30+ patterns → Pattern schema with examples
- [ ] 28 snippets → Snippet schema with templates
- [ ] 13 rules → Rule schema with validation
- [ ] 15 quality gates → Gate definition JSON
- [ ] 10 loop phases → Modular phase files
- [ ] 12 hooks → Event-driven subscriptions
- [ ] 2 registries → Extensible registry system
- [ ] Plugin system → First-class plugin support
- [ ] All context files → JSON state with Markdown rendering
- [ ] All documentation → Generated from schemas

---

*Generated from claude-conductor v4.3 codebase analysis*
