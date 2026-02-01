# Project Orchestrator

## Prompt Library

**Location:** `C:\scripts\prompts\`

> Update this path if your prompts library is elsewhere.

---

## Platform Overview (v4.3)

This is an **intelligent, self-aware** development platform with strict quality enforcement:

```
USER REQUEST → HOOKS → ORCHESTRATOR → META-COGNITION → LOOP (10 phases) → DoD → DONE
                ↑                           │                    ↓
           context-injector        CAPABILITY INVENTORY   15 Quality Gates
                                   + PATTERNS + SNIPPETS    (ALL BLOCKING)
```

| Component | Role | Count |
|-----------|------|-------|
| Commands | Namespaced workflows (`/cc-*`) | 37 |
| Skills | Auto-loading behavioral guidance | 67 |
| Rules | Topic-specific standards | 13 |
| Agents | Specialized expert analysis | 15 |
| Patterns | Reusable architecture patterns | 15+ |
| Snippets | Indexed code templates | 9 |
| Hooks | Automated lifecycle events | 12 |
| Registries | External skill sources | 2 |

**See `_system.md` for complete platform architecture.**
**See `SWARM_ARCHITECTURE.md` for multi-agent orchestration.**

### v4.3 Features (Multi-Registry Discovery)
- **Multi-Registry Support**: Search skills.sh AND aitmpl.com simultaneously
- **Intelligent Scoring**: Rank resources by technology match, reputation, specificity
- **Resource Types**: Skills, agents, commands, hooks, MCPs, and settings
- **Auto-Install**: High-confidence matches (≥80 score) install automatically
- **Deduplication**: Best resource selected when duplicates exist across registries
- **Extensible**: Add new registries via `.claude/config/registries.md`

### v4.2 Features (Plugin Support)
- **Supermemory Plugin**: Persistent memory across sessions
- **Plugin Marketplace**: Install third-party plugins via CLI
- **Memory Search**: Search past work with super-search skill

### v4.1 Features (Swarm Orchestration)
- **Task Dependencies**: `blockedBy`/`blocks` with automatic pipeline unblocking
- **Swarm Mode**: Self-organizing workers claim tasks from shared pool
- **Plan Approval**: Leader approval workflow before risky changes
- **Enhanced Queue**: Dependency-aware prioritization and worker claiming

### v4.0 Features
- **Namespaced Commands**: All commands use `/cc-*` prefix to avoid conflicts
- **Pattern Library**: Reusable architecture patterns (`@patterns/repository`)
- **Snippet Registry**: Indexed code snippets (`snippet:express-route`)
- **Smart Revert**: Git revert that understands logical work units
- **Brownfield Analyzer**: Auto-detect existing project patterns
- **10 Loop Phases**: Including META-COGNITION (2.5), CHECKPOINT (6.25), and REASSESS (6.5)
- **15 Quality Gates**: All BLOCKING - no warnings, no exceptions
- **Meta-Cognition**: Self-aware decision making, knows all available tools
- **Capability Inventory**: Full catalog of commands, agents, rules, patterns
- **Parallel Agents**: Run multiple specialized agents simultaneously
- **Context Budget Monitor**: Prevents context window bloat, suggests sub-agents
- **Parallel Task Decomposer**: Breaks complex tasks into concurrent units
- **Decision Logger**: Tracks significant decisions with rationale for traceability
- **Commit Checkpoints**: Creates verified commits for easy rollback

---

## How This Works

1. **Orchestrate** — Task type determines rules, agents, context automatically
2. **Execute** — Work through autonomous loop with quality gates
3. **Verify** — Definition of Done ensures completion criteria met
4. **Iterate** — Continue until all gates pass and queue empty

Use namespaced slash commands (`/cc-command`) for quick access to common workflows.

---

## Quick Command Reference

All commands use the `cc-` namespace to avoid conflicts with other tools.

### Core Commands
| Command | Purpose |
|---------|---------|
| `/cc-plan` | Create feature specification |
| `/cc-audit-blueprint` | Validate plan before building |
| `/cc-daily` | Continue development work |
| `/cc-spike` | Technical research |
| `/cc-review` | Code review |
| `/cc-test` | Test coverage gate |
| `/cc-secure` | Security audit |
| `/cc-assess` | Full codebase audit |
| `/cc-analyze` | Brownfield codebase analysis |

### Quality & Performance
| Command | Purpose |
|---------|---------|
| `/cc-refactor` | Safe refactoring |
| `/cc-fix` | Bug hunting |
| `/cc-perf` | Performance audit |
| `/cc-deps` | Dependency audit |
| `/cc-debt` | Track technical debt |

### UI/UX & Frontend
| Command | Purpose |
|---------|---------|
| `/cc-ui` | UI/UX audit |
| `/cc-terminal` | Terminal UI audit |
| `/cc-seo` | SEO audit |
| `/cc-sync` | Frontend-backend sync check |

### Operations
| Command | Purpose |
|---------|---------|
| `/cc-release` | Release checklist |
| `/cc-postmortem` | Incident analysis |
| `/cc-migrate` | Migration planning |
| `/cc-closeout` | Complete milestone |
| `/cc-loop` | Autonomous work loop |
| `/cc-revert` | Smart git revert |

### Git & Workflow
| Command | Purpose |
|---------|---------|
| `/cc-commit` | Create well-formatted commit |
| `/cc-pr` | Create pull request |
| `/cc-standup` | Generate standup summary |
| `/cc-retro` | Run sprint retrospective |
| `/cc-changelog` | Update changelog |

### Documentation & Setup
| Command | Purpose |
|---------|---------|
| `/cc-adr` | Document decisions |
| `/cc-onboard` | Create onboarding docs |
| `/cc-docs` | Generate/update documentation |
| `/cc-scaffold` | Generate project structure |
| `/cc-scout-skills` | Install skills from skills.sh |
| `/cc-map-project` | Generate project context map |
| `/cc-gitignore` | Update .gitignore for tech stack |
| `/cc-claude-md` | Create/improve project CLAUDE.md |

---

## Project Initialization

When starting work on a new or existing project:

1. Run `/cc-analyze` to detect existing patterns (brownfield)
2. Run `/cc-claude-md` to create/improve project-specific CLAUDE.md
3. Run `/cc-gitignore` to ensure .gitignore covers tech stack
4. Run `/cc-scout-skills` to install relevant skills from skills.sh
5. Run `/cc-map-project` to generate project context
6. Read STATUS.md for current state

Or just say "initialize this project" to run all steps automatically.

---

## Core Principles

1. **Evidence over assumption** — Verify, don't guess
2. **Test before changing** — No changes without test coverage
3. **Document what you change** — Update Bundle required
4. **Small incremental steps** — Commit often, revert easily
5. **No guessing** — Ask if requirements are unclear
6. **Blueprint is law** — Don't deviate without approval

---

## Modular Rules

Load topic-specific guidance with `@rules/[name]`:

| Rule | Purpose |
|------|---------|
| `@rules/security` | OWASP, authentication, secrets |
| `@rules/testing` | Coverage, TDD, mocks |
| `@rules/git-workflow` | Commits, branches, PRs |
| `@rules/documentation` | README, changelog, comments |
| `@rules/code-quality` | Complexity, naming, deps |
| `@rules/api-design` | REST, errors, versioning |
| `@rules/error-handling` | Hierarchy, logging, recovery |
| `@rules/ui-ux-design` | Spacing, typography, accessibility |
| `@rules/terminal-ui` | Spinners, progress bars, colors |
| `@rules/performance` | Optimization, caching, Web Vitals |
| `@rules/database` | Schema, indexing, migrations |
| `@rules/logging` | Structured logs, levels, context |
| `@rules/prompt-engineering` | AI prompts, best practices |

See `.claude/rules/_index.md` for full documentation.

---

## Specialized Agents

Spawn focused agents for specific tasks:

| Agent | Model | Use Case |
|-------|-------|----------|
| `code-reviewer` | sonnet | Code review tasks |
| `security-analyst` | opus | Security audits |
| `test-engineer` | sonnet | Test writing/analysis |
| `documentation-writer` | sonnet | Documentation tasks |
| `researcher` | sonnet | Technical research |
| `ui-ux-expert` | sonnet | Web interface design |
| `terminal-ui-expert` | sonnet | CLI/terminal polish |
| `seo-expert` | sonnet | Search engine optimization |
| `database-expert` | sonnet | Database optimization |
| `devops-engineer` | sonnet | CI/CD, Docker, K8s |
| `accessibility-expert` | sonnet | WCAG compliance |

Usage: "Spawn code-reviewer agent to review the auth module"

See `.claude/agents/_index.md` for full documentation.

---

## Pattern Library

Load reusable architecture patterns with `@patterns/[name]`:

| Pattern | Category | Use Case |
|---------|----------|----------|
| `@patterns/repository` | Architecture | Data access abstraction |
| `@patterns/service-layer` | Architecture | Business logic organization |
| `@patterns/retry-with-backoff` | Resilience | Handle transient failures |
| `@patterns/circuit-breaker` | Resilience | Prevent cascade failures |
| `@patterns/error-boundary` | Error Handling | Contain failures |
| `@patterns/pagination` | API | Large dataset handling |
| `@patterns/strategy` | Behavioral | Interchangeable algorithms |
| `@patterns/feature-flag` | Operations | Gradual rollout |

See `.claude/patterns/_index.md` for full documentation.

---

## Snippet Registry

Request code snippets with `snippet:[name]`:

| Snippet | Language | Category |
|---------|----------|----------|
| `snippet:express-route` | TypeScript | API |
| `snippet:react-component` | TypeScript | React |
| `snippet:jest-test` | TypeScript | Testing |
| `snippet:dockerfile` | Docker | DevOps |
| `snippet:error-class` | TypeScript | Utility |

Usage: "Give me snippet:express-route" or "Use the React component snippet"

See `.claude/snippets/_index.md` for full documentation.

---

## Project State Files

| File | Purpose |
|------|---------|
| `STATUS.md` | Current state, next steps |
| `CHANGELOG.md` | Version history |
| `KNOWN_ISSUES.md` | Tracked limitations |
| `docs/decisions/` | ADRs |

---

## Skills (Auto-Loaded)

Skills are organized by category in `.claude/skills/[category]/`.

**Total:** 67 skills across 9 categories

### Quick Reference

| Category | Skills | Key Triggers |
|----------|--------|--------------|
| `orchestration/` | 22 | "start work", "/cc-loop", "swarm", "depends on", "approval" |
| `quality/` | 6 | Severity levels, commits, testing |
| `workflow/` | 5 | Pre-commit, pre-merge, pre-release |
| `optimization/` | 11 | Context, memory, errors, metrics |
| `project-mgmt/` | 10 | Initialize, health, dependencies, brownfield |
| `automation/` | 5 | Changelog, docs, snippets |
| `collaboration/` | 3 | Patterns, sharing, registries |
| `ci-cd/` | 2 | Pipelines, prompt testing |
| `environment/` | 1 | Conda, packages |

### Most Important Skills

| Skill | Purpose |
|-------|---------|
| `orchestration/task-orchestrator` | Auto-selects rules/agents for task |
| `orchestration/autonomous-loop` | Iterate until complete |
| `orchestration/meta-cognition` | Self-aware tool selection from capability inventory |
| `quality/definition-of-done` | Universal completion criteria |
| `orchestration/queue-manager` | Manage work queue |
| `orchestration/browser-verification` | Verify UI changes |
| `optimization/smart-context` | Load relevant context only |
| `optimization/prompt-feedback` | Learn from failures |

**Full index:** `.claude/skills/_index.md`

---

## Autonomous Development

### Starting Work
```
"Implement user authentication"
→ task-orchestrator classifies as Security-Critical Feature
→ Loads @rules/security, @rules/api-design, @rules/testing
→ Surfaces @patterns/repository, @patterns/error-boundary
→ Suggests security-analyst agent
→ Creates work queue
→ Begins autonomous loop
```

### The Loop
```
/cc-loop [task]

Phase 1: ASSESS → Understand current state
Phase 2: PLAN   → Prioritize work queue
Phase 3: BUILD  → Implement changes (using patterns/snippets)
Phase 4: TEST   → Run tests + browser verification
Phase 5: QUALITY → Run all quality gates
Phase 6: EVALUATE → Check Definition of Done

Loop exits when:
✓ All quality gates pass (2 consecutive iterations)
✓ Verification iteration confirms stability
✓ Work queue empty
✓ Definition of Done complete
```

### Browser Verification
For UI work, the loop automatically:
- Screenshots at multiple viewports
- Runs accessibility audits
- Tests forms and interactions
- Checks for visual regressions

---

## Swarm Orchestration (v4.1)

Advanced multi-agent coordination for complex tasks.

### Task Dependencies

Define dependencies between tasks for automatic pipeline progression:

```markdown
## Work Queue
| ID | Task | Status | Blocked By | Blocks |
|----|------|--------|------------|--------|
| T001 | Design schema | complete | — | T002, T003 |
| T002 | Implement service | pending | — | T004 |
| T003 | Create endpoints | pending | — | T004 |
| T004 | Integration tests | blocked | T002, T003 | — |
```

When T002 and T003 complete → T004 automatically unblocks.

### Swarm Mode

Self-organizing workers for many independent tasks:

```
/cc-loop --swarm "Review entire codebase"

System spawns workers that:
├── Claim tasks from shared pool
├── Execute independently
├── Return for more when done
└── No coordinator bottleneck
```

### Plan Approval

Safety checkpoint for risky changes:

```
Worker: "Need to change JWT algorithm"
System: ⚠️ Security change requires approval

Plan submitted → Leader reviews → Approve/Reject → Proceed
```

### When to Use

| Scenario | Mode |
|----------|------|
| Many independent reviews | Swarm mode |
| Sequential pipeline | Dependencies |
| Breaking/risky change | Plan approval |
| Standard feature | Regular loop |

**See `SWARM_ARCHITECTURE.md` for full documentation.**

---

## Context Management

- Load ONE prompt at a time
- Complete its process fully
- Skills auto-load when relevant (pre-commit, pre-merge, etc.)
- Full prompts available in the prompts library

---

## v3.0 Documentation

Comprehensive E2E documentation for the v3.0 platform:

| Document | Purpose |
|----------|---------|
| [HOOKS_REFERENCE](HOOKS_REFERENCE.md) | All 12 hooks with I/O schemas, exit codes |
| [LOOP_WORKFLOW](LOOP_WORKFLOW.md) | Complete /loop execution flow |
| [QUALITY_GATES](QUALITY_GATES.md) | All 12 gates with pass/fail criteria |
| [STATE_FILES](STATE_FILES.md) | State file schemas and locations |
| [ERROR_RECOVERY](ERROR_RECOVERY.md) | Error classification and recovery |
| [MCP_SETUP](MCP_SETUP.md) | MCP server installation and configuration |
| [V3_IMPLEMENTATION_BLUEPRINT](V3_IMPLEMENTATION_BLUEPRINT.md) | Implementation status |

---

## Getting Help

| Resource | Location | Purpose |
|----------|----------|---------|
| Platform Architecture | `_system.md` | How components work together |
| Skill Index | `skills/_index.md` | Searchable skill directory |
| Prompt Template | `PROMPT_TEMPLATE.md` | Best practices for prompts |
| Quick Reference | `QUICK_REFERENCE.md` | One-page cheat sheet |
| Troubleshooting | `TROUBLESHOOTING.md` | Common issues and fixes |
| Plugins | `PLUGINS.md` | Plugin installation and config |
| MCP Servers | `MCP_SERVERS.md` | External tool integration |
| Commands | `commands/` | Slash command definitions |
| Skills | `skills/[category]/` | Auto-loading behaviors |
| Rules | `rules/` | Topic-specific standards |
| Agents | `agents/` | Expert definitions |
| Session History | `context/SESSION_HISTORY.md` | Cross-session persistence |
| Metrics | `metrics/` | Quality tracking |
| Feedback | `feedback/` | Prompt improvement |
| Full Prompts | `PROMPTS_PATH` below | Complete prompt library |

---

## Configuration

**Prompts Library Path:**
Update this to match your system:
```
PROMPTS_PATH = C:\scripts\prompts\   # Windows
PROMPTS_PATH = ~/scripts/prompts/    # macOS/Linux
```

Full prompts are at: `{PROMPTS_PATH}/[category]/[PROMPT].md`
