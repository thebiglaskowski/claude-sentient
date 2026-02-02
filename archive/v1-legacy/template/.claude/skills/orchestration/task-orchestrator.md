---
name: task-orchestrator
description: Automatically selects rules, agents, and context based on task type
version: 2.0.0
triggers:
  - "start work on"
  - "begin task"
  - "working on"
  - "implement"
  - "build"
  - "fix"
  - "refactor"
  - "review"
  - "audit"
model: sonnet
tags: [orchestration, workflow, automation]
context: inherit
---

# Task Orchestrator

Automatically analyzes task type and orchestrates the appropriate rules, agents, and context for optimal execution.

---

## How It Works

When you describe a task, this skill:

1. **Classifies** the task type
2. **Loads** relevant rules automatically
3. **Suggests** appropriate agents to spawn
4. **Configures** context loading strategy
5. **Sets** quality gates for completion

---

## Task Type Classification

### Feature Development
**Triggers:** "add", "create", "implement", "build new"

```
Rules to Load:
├── @rules/code-quality
├── @rules/testing
├── @rules/documentation
└── @rules/[domain-specific]  # API, UI, database based on feature

Patterns to Surface:
├── @patterns/repository (if data access)
├── @patterns/strategy (if business logic)
├── @patterns/error-boundary (if error handling)
└── @patterns/[domain-specific]

Snippets to Suggest:
├── snippet:express-route (if API)
├── snippet:react-component (if UI)
├── snippet:jest-test (for tests)
└── snippet:error-class (for custom errors)

Agents to Consider:
├── code-reviewer (after implementation)
├── test-engineer (for test strategy)
└── [domain-expert] (ui-ux, database, etc.)

Context Priority:
├── Blueprint/spec (if exists)
├── Related existing code
├── Test files for similar features
└── API contracts (if integration)
```

### Bug Fixing
**Triggers:** "fix", "bug", "issue", "broken", "doesn't work"

```
Rules to Load:
├── @rules/testing (regression tests)
├── @rules/error-handling
├── @rules/logging
└── @rules/[affected-domain]

Agents to Consider:
├── code-reviewer (verify fix doesn't break other things)
└── test-engineer (ensure regression test added)

Context Priority:
├── Error logs/stack traces
├── Affected file(s)
├── Related test files
├── Recent changes to affected area
```

### Security Work
**Triggers:** "security", "vulnerability", "CVE", "auth", "permission"

```
Rules to Load:
├── @rules/security (ALWAYS)
├── @rules/error-handling
├── @rules/logging
└── @rules/api-design (if API-related)

Agents to Spawn:
├── security-analyst (REQUIRED for security work)
└── code-reviewer (with security focus)

Context Priority:
├── Security-sensitive files (auth, encryption, input handling)
├── Environment/config files
├── Dependency manifests
└── Previous security audit findings
```

### Performance Optimization
**Triggers:** "slow", "performance", "optimize", "speed up", "latency"

```
Rules to Load:
├── @rules/performance
├── @rules/database (if DB-related)
├── @rules/logging (for profiling)
└── @rules/code-quality

Agents to Consider:
├── database-expert (if query-related)
└── code-reviewer (verify no regression)

Context Priority:
├── Profiling data (if available)
├── Database queries
├── Hot paths identified
└── Caching configuration
```

### API Development
**Triggers:** "API", "endpoint", "REST", "GraphQL", "route"

```
Rules to Load:
├── @rules/api-design
├── @rules/security
├── @rules/error-handling
├── @rules/documentation

Patterns to Surface:
├── @patterns/pagination (for list endpoints)
├── @patterns/retry-with-backoff (for external calls)
├── @patterns/error-boundary (for error handling)

Snippets to Suggest:
├── snippet:express-route (Express.js)
├── snippet:jest-test (for API tests)
├── snippet:error-class (for API errors)

Agents to Consider:
├── security-analyst (authentication/authorization)
├── documentation-writer (API docs)
└── code-reviewer

Context Priority:
├── Existing API patterns
├── OpenAPI/Swagger specs
├── Authentication middleware
├── Request/response schemas
```

### UI/Frontend Work
**Triggers:** "UI", "frontend", "component", "page", "form", "button"

```
Rules to Load:
├── @rules/ui-ux-design
├── @rules/performance (Core Web Vitals)
├── @rules/testing
└── @rules/code-quality

Patterns to Surface:
├── @patterns/error-boundary (React/Vue)
├── @patterns/strategy (for rendering)

Snippets to Suggest:
├── snippet:react-component (components)
├── snippet:jest-test (component tests)

Agents to Consider:
├── ui-ux-expert
├── accessibility-expert
└── seo-expert (if public pages)

Context Priority:
├── Design system/component library
├── Existing similar components
├── Style files (CSS/SCSS)
├── State management patterns

Browser Verification:
├── Visual check after changes
├── Responsive breakpoints
├── Accessibility audit
```

### Database Work
**Triggers:** "database", "schema", "migration", "query", "index"

```
Rules to Load:
├── @rules/database
├── @rules/performance
├── @rules/security
└── @rules/testing

Patterns to Surface:
├── @patterns/repository (data access)
├── @patterns/pagination (for queries)
├── @patterns/retry-with-backoff (for connections)

Snippets to Suggest:
├── snippet:prisma-model (if Prisma)
├── snippet:migration (SQL migrations)

Agents to Spawn:
├── database-expert (REQUIRED)
└── code-reviewer

Context Priority:
├── Schema files
├── Existing migrations
├── Query patterns
├── Index definitions
```

### DevOps/Infrastructure
**Triggers:** "CI", "CD", "deploy", "Docker", "Kubernetes", "pipeline"

```
Rules to Load:
├── @rules/security
├── @rules/logging
└── @rules/documentation

Agents to Spawn:
├── devops-engineer (REQUIRED)
└── security-analyst (for secrets/permissions)

Context Priority:
├── CI/CD configuration
├── Docker files
├── Infrastructure as code
├── Environment configs
```

### Code Review
**Triggers:** "review", "PR", "pull request", "check this"

```
Rules to Load:
├── @rules/code-quality
├── @rules/testing
├── @rules/security
├── @rules/documentation

Agents to Spawn:
├── code-reviewer (REQUIRED)
├── security-analyst (if auth/data changes)
└── test-engineer (if test gaps)

Context Priority:
├── Changed files
├── Related tests
├── PR description
├── Linked issues/specs
```

### Refactoring
**Triggers:** "refactor", "clean up", "restructure", "reorganize"

```
Rules to Load:
├── @rules/code-quality
├── @rules/testing
├── @rules/documentation
└── @rules/[affected-domain]

Agents to Consider:
├── code-reviewer
└── test-engineer (ensure coverage first)

Context Priority:
├── Files to refactor
├── ALL tests for affected code
├── Dependents (what uses this code)
├── Dependencies (what this code uses)

Pre-Condition:
└── Tests must exist before refactoring begins
```

### Documentation
**Triggers:** "document", "README", "docs", "explain", "guide"

```
Rules to Load:
├── @rules/documentation
└── @rules/[topic-being-documented]

Agents to Spawn:
├── documentation-writer (REQUIRED)
└── [domain-expert] (for accuracy review)

Context Priority:
├── Code being documented
├── Existing documentation
├── API contracts
├── User-facing behavior
```

---

## Orchestration Commands

### Auto-Orchestrate
```
"Start work on [task description]"
→ Orchestrator analyzes, loads rules, suggests agents
```

### Manual Override
```
"Work on [task] using @rules/security @rules/api-design"
→ Uses specified rules instead of auto-selection
```

### Check Orchestration
```
"What rules and agents should I use for [task]?"
→ Returns recommendation without loading
```

---

## Context Loading Strategy

### By Task Scope

| Scope | Context Strategy |
|-------|------------------|
| Single file | File + tests + dependents |
| Single feature | Feature files + tests + API |
| Cross-cutting | Affected modules + integration tests |
| System-wide | Architecture docs + key files only |

### Context Budget

```
Target: ~3000 tokens of context
├── Primary files: 60% (code being changed)
├── Test files: 20%
├── Reference files: 15%
└── Documentation: 5%
```

---

## Agent Spawning Strategy

### When to Spawn Agents

| Situation | Action |
|-----------|--------|
| Security-sensitive | Always spawn security-analyst |
| Code review needed | Spawn code-reviewer |
| Complex domain | Spawn domain expert |
| Multiple concerns | Spawn agents in parallel |
| Context budget > 70% | Delegate new tasks to sub-agents |
| Task has independent units | Use parallel-task-decomposer |

### Context Budget Check

Before heavy operations, check context budget:
```
CHECK CONTEXT BUDGET:
├── < 50% (Green): Continue in main context
├── 50-70% (Yellow): Consider spawning for heavy tasks
├── 70-85% (Orange): Spawn sub-agents for all new tasks
└── > 85% (Red): Delegate everything, context is full

Skill: context-budget-monitor
```

### Task Decomposition

For complex tasks, decompose into parallel units:
```
DECOMPOSITION CHECK:
├── Can task be split by module? → Module-based parallelization
├── Can task be split by concern? → Concern-based parallelization
├── Can task be split by layer? → Layer-based parallelization
├── Can tests run while implementing? → Test-implementation parallel
└── None apply? → Execute sequentially

Skill: parallel-task-decomposer
```

### Parallel Agent Pattern

For comprehensive audits:
```
Spawn in parallel:
├── security-analyst → Security findings
├── code-reviewer → Quality findings
└── test-engineer → Coverage findings

Then: Synthesize results into unified work queue
```

### Agent Result Integration

After agent completes:
1. Extract findings by severity
2. Convert to work queue items
3. Prioritize S0/S1 first
4. Continue loop with enriched queue

---

## Quality Gate Selection

### By Task Type

| Task Type | Primary Gates |
|-----------|---------------|
| Feature | Tests + Coverage + Acceptance |
| Bug Fix | Regression test + Root cause |
| Security | Security scan + Penetration test |
| Performance | Metrics before/after |
| Refactoring | Behavior unchanged + Tests pass |
| Documentation | Accuracy + Completeness |

---

## Browser Verification Triggers

### When to Use Browser

| Trigger | Browser Action |
|---------|----------------|
| UI changes | Screenshot before/after |
| Responsive work | Check breakpoints |
| Form work | Test submission flow |
| Visual regression | Compare screenshots |
| User flow | End-to-end walkthrough |

### Browser Commands
```
"Verify in browser" → Opens localhost, takes screenshot
"Check responsive" → Tests at mobile/tablet/desktop
"Visual diff" → Compares to baseline screenshot
```

---

## Example Orchestration

### Input
```
"Implement user authentication with OAuth"
```

### Orchestration Response
```
Task Type: Feature Development (Security-Critical)

Context Budget Check:
├── Current usage: ~35% (Green)
├── Action: Continue in main context
├── Heavy analysis: Delegate to security-analyst

Task Decomposition:
├── Decomposable: Yes (by layer)
├── Units identified:
│   ├── Unit 1: Database schema (user, sessions)
│   ├── Unit 2: Auth service logic
│   ├── Unit 3: API endpoints
│   ├── Unit 4: Tests (can parallel with implementation)
├── Parallel execution: Units 1-3 sequential, Unit 4 parallel

Loading Rules:
├── @rules/security (authentication work)
├── @rules/api-design (OAuth endpoints)
├── @rules/testing (auth test coverage)
├── @rules/error-handling (auth failures)
└── @rules/logging (security events)

Surfacing Patterns:
├── @patterns/repository (user data access)
├── @patterns/error-boundary (auth error handling)
├── @patterns/retry-with-backoff (OAuth provider calls, handle failures)

Suggesting Snippets:
├── snippet:express-route (auth endpoints)
├── snippet:error-class (AuthError, TokenError)
├── snippet:jest-test (auth flow tests)

Recommended Agents:
├── security-analyst (REQUIRED - auth is security-critical)
├── test-engineer (parallel - write tests while implementing)
└── code-reviewer (after implementation)

Context Loading:
├── Existing auth files (if any)
├── User model/schema
├── Environment config (.env.example)
├── OAuth provider docs (via context7)

Quality Gates:
├── All tests passing
├── Security scan clean
├── OAuth flow tested end-to-end
├── Token refresh verified
├── Logout/session invalidation verified

DoD Focus:
├── Feature DoD
├── + Security Fix DoD (because auth)

Decision Logging:
├── Log: Auth approach (JWT vs sessions)
├── Log: Token storage strategy
├── Log: Refresh token rotation policy

Checkpoint Strategy:
├── Checkpoint 1: After schema complete
├── Checkpoint 2: After auth service complete
├── Checkpoint 3: After endpoints complete
├── Checkpoint 4: After all tests pass
```

---

## Integration with /cc-loop

The autonomous loop uses this orchestrator:

```
/cc-loop "implement user authentication"

1. CHECK CONTEXT BUDGET
   └── Determine if main context or sub-agents

2. ORCHESTRATE
   ├── Classify task → Security-Critical Feature
   ├── Load rules (@rules/security, etc.)
   ├── Surface patterns (@patterns/repository, etc.)
   └── Suggest snippets (snippet:express-route, etc.)

3. DECOMPOSE (parallel-task-decomposer)
   ├── Identify independent units
   ├── Check dependencies between units
   └── Plan parallel execution

4. SPAWN AGENTS
   ├── security-analyst for initial assessment
   ├── test-engineer in parallel (writes tests while implementing)
   └── Track in LOOP_STATE.md

5. BUILD WITH DECISION LOGGING
   ├── Implement each unit
   ├── Log significant decisions to DECISIONS_LOG.md
   └── Reference patterns/snippets

6. CHECKPOINT AFTER EACH VERIFIED UNIT
   ├── Run tests for completed unit
   ├── Create checkpoint commit
   ├── Update CHECKPOINTS.md
   └── Enable rollback to this state

7. QUALITY + EVALUATE
   ├── Run all 15 quality gates
   ├── Verify against DoD (Feature + Security)
   └── Check 2 consecutive passes

8. EXIT
   ├── All gates pass
   ├── Work queue empty
   ├── Final checkpoint created
   └── Decisions documented
```
