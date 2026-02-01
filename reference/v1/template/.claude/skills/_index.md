# Skills Index

Searchable index of all skills organized by category.

---

## Quick Search

| Looking for... | Use Skill | Category |
|----------------|-----------|----------|
| Refine until good | `evaluator-optimizer` | orchestration |
| Start a task | `task-orchestrator` | orchestration |
| Clarify requirements | `requirements-clarifier` | orchestration |
| Check if done | `definition-of-done` | quality |
| Run until complete | `autonomous-loop` | orchestration |
| Choose best approach | `meta-cognition` | orchestration |
| Multiple perspectives | `multi-perspective` | orchestration |
| Self-critique code | `self-critique` | quality |
| Verify UI changes | `browser-verification` | orchestration |
| Compare screenshots | `visual-diff` | orchestration |
| Manage work queue | `queue-manager` | orchestration |
| Combine agent results | `result-synthesizer` | orchestration |
| Break into parallel tasks | `parallel-task-decomposer` | orchestration |
| **Swarm self-organizing** | `swarm-mode` | orchestration |
| **Task dependencies** | `task-dependencies` | orchestration |
| **Approve risky changes** | `plan-approval` | orchestration |
| Before committing | `pre-commit` | workflow |
| Before merging | `pre-merge` | workflow |
| Before releasing | `pre-release` | workflow |
| Create verified commits | `commit-checkpoint` | workflow |
| Classify issue severity | `severity-levels` | quality |
| Choose model | `model-routing` | quality |
| Format commits | `commit-style` | quality |
| Write tests first | `test-first` | quality |
| Handle uncertainty | `no-guessing` | quality |
| Update changelog | `changelog-automation` | automation |
| Generate docs | `docs-generator` | automation |
| Use code snippets | `snippet-library` | automation |
| Chain commands | `compound-commands` | automation |
| Modernize tech | `modern-tech-checker` | automation |
| Optimize context | `smart-context` | optimization |
| Monitor context budget | `context-budget-monitor` | optimization |
| Avoid re-reading | `session-memory` | optimization |
| Preview changes | `dry-run-mode` | optimization |
| Recover from errors | `error-recovery` | optimization |
| Track metrics | `metrics-logger` | optimization |
| Write JSONL metrics | `metrics-writer` | optimization |
| Undo changes | `undo-history` | optimization |
| Watch files | `file-watcher` | optimization |
| Check dependencies | `dependency-checker` | optimization |
| Check for updates | `auto-update-checker` | optimization |
| Log decisions | `decision-logger` | orchestration |
| Share patterns | `cross-project-patterns` | collaboration |
| Share with team | `team-sharing` | collaboration |
| Find templates | `template-registry` | collaboration |
| Setup CI/CD | `ci-cd-integration` | ci-cd |
| Test prompts | `prompt-testing` | ci-cd |
| Conda environments | `conda-aware` | environment |
| Initialize project | `project-init` | project-mgmt |
| Create CLAUDE.md | `claude-md-manager` | project-mgmt |
| Multi-registry discovery | `skill-scout` | project-mgmt |
| Manage .gitignore | `gitignore-manager` | project-mgmt |
| Project health | `health-dashboard` | project-mgmt |
| Track dependencies | `dependency-tracker` | project-mgmt |
| Add frontmatter | `frontmatter-generator` | project-mgmt |
| Sync frontend/backend | `frontend-backend-sync` | project-mgmt |
| Analyze existing code | `brownfield-analyzer` | project-mgmt |
| Deep analysis | `extended-thinking` | orchestration |
| Parallel exploration | `parallel-exploration` | orchestration |
| Subagent research | `subagent-research` | orchestration |
| Parse arguments | `argument-parser` | orchestration |

---

## By Category

### orchestration/ (21 skills)
Core platform orchestration and autonomous operation.

| Skill | Triggers | Purpose |
|-------|----------|---------|
| `task-orchestrator` | "start work on", "implement" | Auto-select rules/agents for task |
| `requirements-clarifier` | "implement", "build", "create" | Ask clarifying questions before major work |
| `autonomous-loop` | "/cc-loop", "work until done" | Iterate until complete (10 phases, 15 gates) |
| `meta-cognition` | "which tool", "best approach" | Self-aware decision making from capability inventory |
| `multi-perspective` | "analyze", "trade-offs", "pros cons" | Analyze from multiple expert viewpoints |
| `queue-manager` | "show queue", "work queue" | Manage work items with dependencies |
| `definition-of-done` | "am I done?", "verify complete" | Completion criteria |
| `browser-verification` | "verify in browser" | UI verification |
| `visual-diff` | "visual diff", "compare screenshots" | Screenshot comparison |
| `result-synthesizer` | "combine findings" | Merge agent outputs |
| `parallel-task-decomposer` | "parallelize", "break down" | Break tasks into parallel units |
| `decision-logger` | "log decision", "document choice" | Capture decisions for traceability |
| `extended-thinking` | "ultrathink", "deep analysis" | Extended reasoning |
| `parallel-exploration` | "explore in parallel" | Multiple explorations |
| `subagent-research` | "spawn researcher" | Isolated research |
| `argument-parser` | Command arguments | Parse $1, --flag |
| `smart-context-v3` | "!files", "!recent", "load context" | Enhanced context with !command syntax |
| `error-classifier` | error, failed, exception | Classify errors, suggest recovery |
| `parallel-agents` | "parallel", "comprehensive", "full audit" | Coordinate parallel agent execution |
| **`swarm-mode`** | "swarm", "--swarm", "self-organizing" | Self-organizing workers claim from pool |
| **`task-dependencies`** | "depends on", "blocked by", "pipeline" | Automatic pipeline unblocking |
| **`plan-approval`** | "requires approval", "risky change" | Leader approval before risky actions |
| **`evaluator-optimizer`** | "refine this", "improve until", "iterate on" | Evaluate-improve feedback loops until quality met |

### quality/ (7 skills)
Quality standards and verification.

| Skill | Triggers | Purpose |
|-------|----------|---------|
| `definition-of-done` | "is this done?" | Universal completion criteria |
| `self-critique` | Code generation | Critique own code, identify issues, fix before presenting |
| `severity-levels` | Audits, reviews | S0-S3 classification |
| `model-routing` | Model selection | Choose haiku/sonnet/opus |
| `commit-style` | Git commits | Conventional commits |
| `test-first` | Writing code | TDD approach |
| `no-guessing` | Unclear requirements | Ask don't assume |

### workflow/ (6 skills)
Git workflow and checkpoints.

| Skill | Triggers | Purpose |
|-------|----------|---------|
| `pre-commit` | Before commit | Pre-commit checklist |
| `pre-merge` | Before merge | PR checklist |
| `pre-release` | Before release | Release checklist |
| `commit-checkpoint` | "checkpoint", "feature verified" | Create verified commits for rollback |
| `phase-workflow` | Project phases | Phase guidance |
| `update-bundle-guide` | After work | Update bundle creation |

### automation/ (5 skills)
Automated generation and updates.

| Skill | Triggers | Purpose |
|-------|----------|---------|
| `changelog-automation` | "update changelog" | Auto changelog |
| `docs-generator` | "generate docs" | Auto documentation |
| `compound-commands` | "/ship", "/quick-fix" | Command chains |
| `snippet-library` | "snippet" | Boilerplate code |
| `modern-tech-checker` | "modernize" | Tech updates |

### optimization/ (11 skills)
Performance and context optimization.

| Skill | Triggers | Purpose |
|-------|----------|---------|
| `smart-context` | Task start | Load relevant context |
| `context-budget-monitor` | Heavy operations | Prevent context bloat, suggest sub-agents |
| `session-memory` | Continuous | Avoid re-reading files |
| `dry-run-mode` | "preview", "simulate" | Preview changes |
| `error-recovery` | Errors occur | Recovery strategies |
| `metrics-logger` | "show metrics" | Usage tracking |
| `metrics-writer` | "log metric", "record metric" | Write JSONL metrics |
| `undo-history` | "undo", "revert" | Rollback changes |
| `file-watcher` | "watch files" | Auto-run on change |
| `dependency-checker` | Session start | Check dependencies |
| `auto-update-checker` | "check updates" | Template updates |
| `prompt-feedback` | "prompt failed", "improve prompt" | Self-improvement loop |

### collaboration/ (3 skills)
Team sharing and external resources.

| Skill | Triggers | Purpose |
|-------|----------|---------|
| `cross-project-patterns` | "pattern from" | Share patterns |
| `team-sharing` | "share with team" | Sync prompts |
| `template-registry` | "browse templates", "list registries" | Manual registry browsing |

### project-mgmt/ (10 skills)
Project setup and management.

| Skill | Triggers | Purpose |
|-------|----------|---------|
| `project-init` | "initialize project" | Full project setup |
| `claude-md-manager` | "create CLAUDE.md" | Project instructions |
| `skill-scout` | "scout skills", "install skills", "aitmpl" | Multi-registry discovery (skills.sh + aitmpl.com) |
| `gitignore-manager` | "update gitignore" | Manage .gitignore |
| `health-dashboard` | "project health" | Status overview |
| `dependency-tracker` | "check dependencies" | Outdated/vulnerable |
| `frontmatter-generator` | "add frontmatter" | Upgrade to v2.0 |
| `frontend-backend-sync` | API changes | Sync check |
| `project-templates` | "new project" | Project scaffolding |
| `brownfield-analyzer` | "existing project", "/cc-analyze" | Detect existing patterns/conventions |

### ci-cd/ (2 skills)
Continuous integration and deployment.

| Skill | Triggers | Purpose |
|-------|----------|---------|
| `ci-cd-integration` | Pipeline setup | CI/CD configuration |
| `prompt-testing` | "test prompts" | Prompt quality testing |

### environment/ (1 skill)
Environment and package management.

| Skill | Triggers | Purpose |
|-------|----------|---------|
| `conda-aware` | "pip install" | Conda environment handling |

---

## Skill Counts

| Category | Count |
|----------|-------|
| orchestration | 22 |
| optimization | 12 |
| project-mgmt | 10 |
| quality | 7 |
| workflow | 6 |
| automation | 5 |
| collaboration | 3 |
| ci-cd | 2 |
| environment | 1 |
| **Total** | **68** |

---

## Skill Dependencies

```
task-orchestrator
├── loads → rules (based on task type)
├── suggests → agents (based on task type)
├── triggers → autonomous-loop (if /loop)
└── decides → swarm-mode vs coordinator (if many tasks)

autonomous-loop
├── uses → meta-cognition (intelligent tool selection)
├── uses → queue-manager (work queue with dependencies)
├── uses → task-dependencies (pipeline unblocking)
├── uses → swarm-mode (if --swarm flag)
├── uses → plan-approval (if risky change)
├── uses → definition-of-done (completion check)
├── uses → browser-verification (if UI)
├── uses → result-synthesizer (if multi-agent)
└── uses → smart-context (context optimization)

queue-manager
├── uses → task-dependencies (blockedBy/blocks)
├── uses → swarm-mode (worker claiming)
└── provides → work selection to autonomous-loop

swarm-mode
├── uses → queue-manager (task pool)
├── uses → task-dependencies (respects blockedBy)
├── uses → result-synthesizer (merge worker findings)
└── uses → parallel-agents (worker spawning)

plan-approval
├── triggered-by → risky change detection
├── pauses → autonomous-loop (wait for approval)
└── logs-to → decision-logger (audit trail)

pre-commit
├── uses → test-first (verify tests)
├── uses → commit-style (format message)
└── uses → severity-levels (if issues found)

pre-merge
├── uses → pre-commit (all commit checks)
├── uses → definition-of-done (completion)
└── uses → security check (if changes)

pre-release
├── uses → pre-merge (all merge checks)
├── uses → changelog-automation (update changelog)
└── uses → health-dashboard (final status)
```

---

## Adding New Skills

1. Determine category based on purpose
2. Create file in appropriate subfolder
3. Add YAML frontmatter (see prompt-template.md)
4. Add to this index
5. Add to dependency graph if connected
