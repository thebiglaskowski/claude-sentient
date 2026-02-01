---
name: meta-cognition
description: Self-aware decision making - knows all available tools and chooses wisely
argument-hint: "[situation description]"
model: opus
version: 1.1.0
tags: [orchestration, intelligence, decision-making]
---

# Meta-Cognition System v1.1

This skill provides **self-awareness** about available capabilities and intelligent decision-making about which tools to use when.

**v1.1 Enhancements:**
- Leader/Worker role transitions based on query classification
- Subagent count guidelines by classification type
- Integration with Phase 1 query classification

## Description

The meta-cognition system enables the autonomous loop to:
- Know ALL available tools, commands, agents, and skills
- Evaluate which approach is best for the current situation
- Reassess and pivot when an approach isn't working
- Learn from what's working and what isn't
- Make intelligent decisions, not just follow scripts

Triggers on: "what tools do I have", "reassess approach", "is there a better way", "evaluate strategy"

---

## Capability Inventory

### Available Commands (37+)

All commands use the `cc-` namespace to avoid conflicts.

| Category | Commands | Use When |
|----------|----------|----------|
| **Planning** | `/cc-plan`, `/cc-audit-blueprint`, `/cc-spike`, `/cc-analyze` | Starting new work, need clarity |
| **Execution** | `/cc-daily`, `/cc-loop`, `/cc-scaffold`, `/cc-revert` | Active development |
| **Execution (Swarm)** | `/cc-loop --swarm` | Many independent tasks |
| **Quality** | `/cc-review`, `/cc-test`, `/cc-secure`, `/cc-assess` | Verification needed |
| **Performance** | `/cc-perf`, `/cc-deps`, `/cc-debt` | Optimization needed |
| **UI/UX** | `/cc-ui`, `/cc-terminal`, `/cc-seo`, `/cc-sync` | Frontend work |
| **Operations** | `/cc-release`, `/cc-postmortem`, `/cc-migrate`, `/cc-closeout` | Shipping/incidents |
| **Git** | `/cc-commit`, `/cc-pr`, `/cc-standup`, `/cc-retro`, `/cc-changelog` | Version control |
| **Documentation** | `/cc-adr`, `/cc-onboard`, `/cc-docs`, `/cc-claude-md` | Docs needed |

### Available Patterns (15+)

Load with `@patterns/[name]`:

| Category | Patterns | Use When |
|----------|----------|----------|
| **Architecture** | `repository`, `service-layer`, `clean-architecture` | Data/business logic |
| **Resilience** | `retry-with-backoff`, `circuit-breaker` | External calls |
| **Error Handling** | `error-boundary`, `result-type` | Failure containment |
| **API** | `pagination`, `rate-limiting` | Endpoints |
| **Behavioral** | `strategy`, `observer`, `state-machine` | Complex logic |
| **Testing** | `arrange-act-assert`, `test-doubles` | Test structure |
| **Operations** | `feature-flag`, `blue-green` | Deployment |

### Available Snippets (9)

Request with `snippet:[name]`:

| Category | Snippets | Use When |
|----------|----------|----------|
| **API** | `express-route`, `fastapi-endpoint`, `go-handler` | New endpoints |
| **React** | `react-component`, `react-hook`, `react-context` | Frontend components |
| **Testing** | `jest-test`, `pytest-test`, `go-test` | Writing tests |
| **DevOps** | `dockerfile`, `github-action` | Infrastructure |
| **Utility** | `error-class`, `logger`, `config` | Common utilities |

### Available Agents (15)

| Agent | Model | Use When |
|-------|-------|----------|
| `code-reviewer` | sonnet | Need code review |
| `security-analyst` | opus | Security concerns |
| `test-engineer` | sonnet | Test gaps |
| `documentation-writer` | sonnet | Docs needed |
| `researcher` | sonnet | Need to investigate |
| `ui-ux-expert` | sonnet | UI work |
| `terminal-ui-expert` | sonnet | CLI polish |
| `seo-expert` | sonnet | SEO work |
| `database-expert` | sonnet | DB optimization |
| `devops-engineer` | sonnet | CI/CD, infra |
| `accessibility-expert` | sonnet | A11y compliance |
| `performance-optimizer` | sonnet | Speed issues |
| `api-designer` | sonnet | API work |
| `migration-specialist` | sonnet | Migrations |
| `prompt-engineer` | sonnet | AI prompts |

### Available Rules (13)

| Rule | Load When |
|------|-----------|
| `@rules/security` | Auth, secrets, OWASP |
| `@rules/testing` | Tests, TDD, coverage |
| `@rules/git-workflow` | Commits, PRs, branches |
| `@rules/documentation` | Docs, README, changelog |
| `@rules/code-quality` | Complexity, naming |
| `@rules/api-design` | REST, endpoints |
| `@rules/error-handling` | Errors, logging |
| `@rules/ui-ux-design` | Web UI |
| `@rules/terminal-ui` | CLI UI |
| `@rules/performance` | Speed, caching |
| `@rules/database` | Schema, queries |
| `@rules/logging` | Logs, observability |
| `@rules/prompt-engineering` | AI prompts |

### Available Hooks (12)

| Hook | Fires When | Does What |
|------|------------|-----------|
| `setup-init` | Project init | One-time setup |
| `session-start` | Session begins | Load state |
| `context-injector` | Prompt submitted | Add context |
| `bash-auto-approve` | Bash command | Auto-approve safe |
| `file-validator` | File write | Validate changes |
| `post-edit` | After edit | Format/lint |
| `error-recovery` | Tool fails | Classify & recover |
| `agent-tracker` | Agent starts | Track parallel |
| `agent-synthesizer` | Agent stops | Merge results |
| `pre-compact` | Before compact | Backup state |
| `dod-verifier` | Loop exit attempt | Verify complete |
| `session-end` | Session ends | Save metrics |

### Available MCP Servers (Dynamic)

MCP servers provide external integrations. **Check at session start** what's available:

| Server | Tools Prefix | Use When |
|--------|--------------|----------|
| `context7` | `mcp__context7__*` | Need current library docs |
| `memory` | `mcp__memory__*` | Cross-session persistence |
| `github` | `mcp__github__*` | GitHub operations |
| `postgres` | `mcp__postgres__*` | Database queries |
| `sqlite` | `mcp__sqlite__*` | Local database |

**Discovery:** Check `.mcp.json` (project root) or `.claude/settings.json` for project-specific servers.

---

## Decision Engine

### Situation Assessment

Before choosing an approach, evaluate:

```
1. WHAT is the task type?
   - Feature, bugfix, refactor, security, docs, chore?

2. WHAT is the current state?
   - Green (all tests pass) or Red (failures)?
   - Coverage level?
   - Known issues?

3. WHAT is the context budget?
   - < 50%: Green - continue normally
   - 50-70%: Yellow - consider sub-agents for heavy tasks
   - 70-85%: Orange - spawn sub-agents for all new tasks
   - > 85%: Red - delegate everything, main context is full

4. CAN tasks be parallelized?
   - Check for independent work units
   - Consider module/concern/layer decomposition
   - Spawn parallel agents for simultaneous execution

3. WHAT has been tried?
   - Previous approaches this session
   - What worked / what didn't

4. WHAT are the constraints?
   - Time pressure?
   - Complexity?
   - Dependencies?

5. WHAT MCP servers are available?
   - Check .mcp.json in project root
   - Check .claude/settings.json
   - Note any mcp__* tools in available toolkit
   - Project may have custom database, API, or tool servers
```

### Tool Selection Matrix

| Situation | Best Approach | Patterns/Snippets |
|-----------|---------------|-------------------|
| Starting fresh, unclear requirements | `/cc-spike` → research first | — |
| Existing codebase, need to understand | `/cc-analyze` → detect patterns | — |
| Clear requirements, no plan | `/cc-plan` → create blueprint | — |
| Plan exists, need validation | `/cc-audit-blueprint` → verify plan | — |
| Plan approved, need to build | `/cc-loop` → autonomous execution | Surface relevant patterns |
| **Many independent tasks** | `/cc-loop --swarm` → self-organizing | `swarm-mode` skill |
| **Pipeline with dependencies** | `/cc-loop` with `task-dependencies` | `task-dependencies` skill |
| **Risky change detected** | Trigger `plan-approval` workflow | `plan-approval` skill |
| Tests failing | Focus on fixing tests before new work | `@patterns/arrange-act-assert` |
| Coverage < 80% | Add tests before continuing | `snippet:jest-test` |
| Security vulnerabilities | Spawn `security-analyst`, fix first | — |
| Performance issues | Spawn `performance-optimizer` | `@patterns/retry-with-backoff` |
| UI looks wrong | Spawn `ui-ux-expert` or `terminal-ui-expert` | `snippet:react-component` |
| Stuck on problem | Spawn `researcher` to investigate | — |
| Code smells | `/cc-review` with `code-reviewer` agent | — |
| Documentation gaps | Spawn `documentation-writer` | — |
| Database slow | Spawn `database-expert` | `@patterns/repository` |
| API work | Spawn `api-designer` | `@patterns/pagination`, `snippet:express-route` |
| CI/CD broken | Spawn `devops-engineer` | `snippet:dockerfile` |
| Accessibility issues | Spawn `accessibility-expert` | — |
| Need to undo changes | `/cc-revert` → smart revert | — |

### Orchestration Mode Selection

```
ORCHESTRATION DECISION TREE:
│
├── Are there > 5 independent tasks?
│   └── YES → Consider swarm mode
│       ├── Tasks share no files? → Use swarm mode
│       └── Tasks may conflict? → Use coordinator pattern
│
├── Do tasks have dependencies?
│   └── YES → Use task-dependencies
│       ├── Linear pipeline? → Dependencies auto-unblock
│       └── Fan-out/fan-in? → Parallel with dependencies
│
├── Is the change risky?
│   └── YES → Trigger plan-approval
│       ├── Schema change? → Require approval
│       ├── Breaking API? → Require user approval
│       └── Security config? → Require user approval
│
└── None of above?
    └── Use standard /cc-loop
```

### Leader/Worker Role Transitions (v4.4)

Based on query classification (from Phase 1: CONTEXTUALIZE), determine role:

```
QUERY CLASSIFICATION → ROLE ASSIGNMENT:
│
├── DEPTH-FIRST (complex, single focus)
│   └── ROLE: Leader
│       ├── Uses opus model for deep reasoning
│       ├── May spawn specialist sub-agents
│       ├── Synthesizes findings personally
│       └── Maintains full context of problem
│
├── BREADTH-FIRST (many independent subtasks)
│   └── ROLE: Coordinator spawning Workers
│       ├── Coordinator: Divides work, assigns to pool
│       ├── Workers: Claim tasks, execute independently
│       ├── Workers use sonnet/haiku for efficiency
│       ├── Results synthesized by coordinator
│       └── Swarm mode optional for > 5 tasks
│
└── STRAIGHTFORWARD (simple, direct)
    └── ROLE: Direct Executor
        ├── No sub-agents needed
        ├── Execute task directly
        └── Fastest path to completion

ROLE TRANSITIONS DURING EXECUTION:
├── Worker discovers complex subtask → Escalate to Leader review
├── Leader identifies parallelizable work → Spawn Workers
├── Coordinator detects dependency conflict → Switch to sequential
└── Direct Executor hits complexity → Upgrade to Leader mode
```

### Subagent Count by Query Classification

| Classification | Task Complexity | Subagent Count | Model |
|----------------|-----------------|----------------|-------|
| Straightforward | Simple | 0 | Current |
| Depth-first | Complex | 1 (specialist) | opus |
| Breadth-first | Simple tasks × many | 3-5 | haiku |
| Breadth-first | Medium tasks × many | 5-10 | sonnet |
| Breadth-first | Complex tasks × many | 10-20 | sonnet |

### Approach Evaluation

After each iteration, evaluate:

```
PROGRESS CHECK:
├── Are quality gates improving? (coverage going up?)
├── Are issues being resolved? (count going down?)
├── Is the work queue shrinking?
├── Are we making forward progress?

IF STUCK (no progress for 2 iterations):
├── Log current approach and results
├── Trigger REASSESSMENT phase
├── Consider alternative approaches
├── Spawn specialist agent for help
└── Update strategy and continue
```

---

## Reassessment Phase

### When to Reassess

Automatic reassessment triggers:
- Same issue fails 3 times
- No progress for 2 iterations
- Quality gates not improving
- User requests reassessment
- Error recovery fails

### Reassessment Process

```
STEP 1: CAPTURE CURRENT STATE
├── What was the goal?
├── What approach was taken?
├── What worked?
├── What didn't work?
├── What's blocking progress?

STEP 2: ANALYZE ALTERNATIVES
├── What other tools could help?
├── Is there a specialist agent for this?
├── Is there a rule with guidance?
├── Has this been solved before? (check context7)
├── Should we break the problem down differently?

STEP 3: CHOOSE NEW STRATEGY
├── Select different tool/approach
├── Spawn specialist agent
├── Load additional rules
├── Simplify the problem
├── Ask user for guidance (last resort)

STEP 4: DOCUMENT AND CONTINUE
├── Log the pivot in LOOP_STATE.md
├── Update work queue with new approach
├── Reset stuck counter
├── Continue loop with new strategy
```

---

## Strategy Patterns

### Pattern: Divide and Conquer
```
When: Large complex task
Do: Break into smaller subtasks
    Tackle one at a time
    Verify each before moving on
```

### Pattern: Specialist Delegation
```
When: Need deep expertise
Do: Spawn specialist agent
    Let them analyze in isolation
    Integrate their findings
```

### Pattern: Research First
```
When: Unfamiliar territory
Do: Spawn researcher agent
    Check context7 for docs (if available)
    Check project MCP servers for relevant tools
    Understand before implementing
```

### Pattern: MCP Discovery
```
When: Starting work on a project
Do: Check .mcp.json in project root
    Check .claude/settings.json
    Note available mcp__* tools
    Use project-specific servers (databases, APIs) when relevant
```

### Pattern: Test-Driven
```
When: Behavior must be preserved
Do: Write tests first (use @patterns/arrange-act-assert)
    Ensure tests pass
    Then make changes
```

### Pattern: Incremental Improvement
```
When: Large gap to close (e.g., 40% → 80% coverage)
Do: Don't try to do it all at once
    Set intermediate targets (50%, 60%, 70%)
    Verify each milestone
```

### Pattern: Parallel Analysis
```
When: Need multiple perspectives
Do: Spawn multiple agents in parallel
    security-analyst + code-reviewer + test-engineer
    Synthesize findings
```

### Pattern: Swarm Execution
```
When: Many independent tasks (> 5)
Do: Activate swarm mode
    Workers self-claim from task pool
    No coordination bottleneck
    Automatic load balancing
```

### Pattern: Pipeline with Dependencies
```
When: Tasks must execute in order
Do: Define task dependencies
    blockedBy: [predecessor tasks]
    Automatic unblocking when predecessors complete
    Parallel execution where dependencies allow
```

### Pattern: Approval Gates
```
When: Risky or breaking changes
Do: Trigger plan-approval workflow
    Submit plan for review
    Wait for approval/rejection
    Proceed only when approved
```

### Pattern: Pattern-First Development
```
When: Building new features
Do: Check pattern library for applicable patterns
    Load @patterns/[name] for guidance
    Use snippet:[name] for boilerplate
    Follow established conventions
```

### Pattern: Brownfield Analysis
```
When: Working on existing codebase
Do: Run /cc-analyze first
    Detect existing conventions
    Match new code to existing patterns
    Don't introduce inconsistencies
```

---

## Self-Improvement Metrics

Track in `.claude/metrics/session-metrics.json`:

```json
{
  "session_id": "...",
  "approaches_tried": [
    {
      "approach": "direct implementation",
      "outcome": "stuck at 40% coverage",
      "iterations": 3
    },
    {
      "approach": "spawned test-engineer",
      "outcome": "coverage improved to 75%",
      "iterations": 2
    }
  ],
  "pivots": 1,
  "total_iterations": 12,
  "final_outcome": "success",
  "lessons": [
    "test-engineer agent effective for coverage gaps",
    "direct implementation insufficient for large coverage gaps"
  ]
}
```

---

## Integration with Autonomous Loop

### Enhanced Loop Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    ENHANCED AUTONOMOUS LOOP                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  CONTEXTUALIZE → ASSESS → [META-COGNITION] → PLAN → BUILD → TEST       │
│       ▲                         │                              │        │
│       │                         ▼                              ▼        │
│       │              ┌─────────────────────┐              QUALITY       │
│       │              │ DECISION ENGINE     │                  │        │
│       │              │                     │                  ▼        │
│       │              │ • What tools exist? │              EVALUATE      │
│       │              │ • What's best here? │                  │        │
│       │              │ • Is this working?  │                  ▼        │
│       │              │ • Should we pivot?  │            [REASSESS?]     │
│       │              └─────────────────────┘                  │        │
│       │                                                       │        │
│       └──────────────────── RECOVER ◀─────────────────────────┘        │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Phase 2.5: META-COGNITION (New)

After ASSESS, before PLAN:

```
META-COGNITION PHASE:
├── Review capability inventory
├── Evaluate current situation against tool matrix
├── Check if current approach is working
├── Consider specialist agents
├── Load relevant rules
├── Decide on strategy
└── Document decision rationale
```

### Phase 7.5: REASSESSMENT CHECK (New)

After EVALUATE, before RECOVER:

```
REASSESSMENT CHECK:
├── Is progress being made?
│   ├── YES: Continue to next iteration
│   └── NO: Enter REASSESSMENT
│
├── REASSESSMENT:
│   ├── Analyze what's not working
│   ├── Consult capability inventory
│   ├── Select alternative approach
│   ├── Spawn specialist if needed
│   └── Update strategy
│
└── Continue with new approach
```

---

## Usage

### Invoke Directly
```
"Use meta-cognition to evaluate my options"
"What tools do I have available for this?"
"Should I be using a different approach?"
"Reassess the current strategy"
```

### Automatic Integration
The autonomous loop should invoke meta-cognition:
- At the start of each session (inventory check)
- After ASSESS phase (strategy selection)
- When stuck (reassessment trigger)
- After failed approaches (pivot evaluation)

---

## Final Directive

The meta-cognition system ensures the autonomous loop is not just following a script, but **actively reasoning** about:
- What tools and capabilities exist
- Which approach is best for this situation
- Whether the current approach is working
- When and how to pivot to a better strategy

This transforms the loop from a rigid checklist into an **intelligent, adaptive system**.
