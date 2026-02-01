# Claude Conductor V2 — Vision

> **The Autonomous Meta-Cognitive Development Engine**

---

## The North Star

Claude Conductor V2 is a **fully autonomous, self-aware development engine** that can:

1. **Start from scratch** — Scaffold and build entire projects autonomously
2. **Drop into any codebase** — Understand, adapt, and enhance existing projects
3. **Handle E2E development** — From concept to deployment with minimal human interaction
4. **Self-orchestrate** — Know what tools to use, when, and why
5. **Continuously self-improve** — Get smarter as the project progresses

**One sentence:** *"Drop it in, tell it what you want, walk away, come back to a finished product."*

---

## Core Philosophy

### 1. Autonomous by Default

The engine should **assume autonomy** and only pause for:
- Ambiguous requirements that could go multiple directions
- Risky/destructive operations (security, data loss, breaking changes)
- Explicit user checkpoints

Everything else? **Just do it.**

### 2. Self-Aware Meta-Cognition

The engine must know:
- **What it can do** — Full inventory of capabilities, tools, patterns, agents
- **What it's doing** — Current phase, progress, blockers
- **What it should do next** — Intelligent prioritization and planning
- **When it's stuck** — Recognize loops, failures, and pivot automatically
- **How well it's doing** — Self-evaluation and scoring

### 3. Swiss Army Knife

One engine for **any project type**:
- Web apps (React, Vue, Angular, Svelte)
- APIs (REST, GraphQL, gRPC)
- CLIs and developer tools
- Mobile apps (React Native, Flutter)
- Backend services (Node, Python, Go, Rust)
- Data pipelines and ML
- Infrastructure and DevOps
- Documentation and technical writing

The engine **detects** what's needed and **adapts**.

### 4. Brownfield Intelligence

When dropped into an existing project:
1. **Scan** — Understand the codebase structure, patterns, conventions
2. **Map** — Build a mental model of architecture and dependencies
3. **Adapt** — Match existing code style, patterns, naming
4. **Enhance** — Improve without breaking, add without disrupting
5. **Document** — Fill in gaps in documentation as it learns

### 5. Continuous Self-Improvement

The engine gets **better over time** within each project:
- Learn from successes (what worked)
- Learn from failures (what didn't)
- Refine prompts based on feedback
- Build project-specific knowledge
- Optimize tool selection based on results

---

## The Autonomous Loop

```
┌─────────────────────────────────────────────────────────────────┐
│                    AUTONOMOUS DEVELOPMENT ENGINE                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐  │
│   │ PERCEIVE│────▶│  PLAN   │────▶│ EXECUTE │────▶│ EVALUATE│  │
│   └─────────┘     └─────────┘     └─────────┘     └─────────┘  │
│        │                                                │        │
│        │                                                │        │
│        │         ┌─────────────────────┐               │        │
│        └────────▶│   META-COGNITION    │◀──────────────┘        │
│                  │  (Self-Awareness)   │                         │
│                  └─────────────────────┘                         │
│                           │                                      │
│                           ▼                                      │
│                  ┌─────────────────────┐                         │
│                  │   SELF-IMPROVEMENT  │                         │
│                  │  (Learn & Adapt)    │                         │
│                  └─────────────────────┘                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Phase Breakdown

#### PERCEIVE — Understand the World
- Scan codebase (brownfield) or understand requirements (greenfield)
- Classify the request (what kind of work is this?)
- Load relevant context (rules, patterns, project knowledge)
- Identify constraints and dependencies

#### PLAN — Decide What to Do
- Decompose into work items
- Prioritize by value and dependencies
- Select tools, agents, patterns for each task
- Estimate complexity and resource needs
- Create checkpoints for rollback

#### EXECUTE — Do the Work
- Implement changes using selected tools
- Run tests continuously
- Verify with quality gates
- Create commits at checkpoints
- Parallelize where possible (swarm mode)

#### EVALUATE — Assess Results
- Did it work? (tests pass, gates pass)
- Is it complete? (definition of done)
- Is it good? (self-critique, quality score)
- What's next? (update work queue)

#### META-COGNITION — Stay Self-Aware
- Am I stuck in a loop?
- Am I using the right tools?
- Should I spawn specialists?
- Do I need human input?
- What's my confidence level?

#### SELF-IMPROVEMENT — Get Better
- What worked? (capture success patterns)
- What failed? (avoid in future)
- How can prompts improve?
- What knowledge should persist?

---

## Key Capabilities

### 1. Intelligent Project Bootstrap

**Greenfield:** "Build me a SaaS for X"
```
1. Clarify requirements (minimal questions)
2. Select technology stack
3. Generate project structure
4. Set up development environment
5. Implement core features
6. Add tests, docs, CI/CD
7. Deploy to staging
8. Iterate based on feedback
```

**Brownfield:** "Improve this codebase"
```
1. Analyze existing structure
2. Detect patterns and conventions
3. Identify tech debt and issues
4. Prioritize improvements
5. Implement changes safely
6. Maintain compatibility
7. Update documentation
```

### 2. Tool Orchestration

The engine has access to **everything**:

| Category | Tools |
|----------|-------|
| **Analysis** | Code scanning, pattern detection, dependency analysis |
| **Planning** | Spec writing, blueprint creation, task decomposition |
| **Execution** | Code generation, refactoring, testing |
| **Quality** | Linting, type checking, security scanning, performance |
| **Verification** | Unit tests, integration tests, browser tests, accessibility |
| **Documentation** | README, API docs, architecture docs, changelogs |
| **Operations** | CI/CD, deployment, monitoring, incident response |
| **Collaboration** | Git workflows, PR creation, code review |

**It knows which to use and when.**

### 3. Multi-Agent Swarm

For complex work, spawn specialists:

```
┌─────────────────────────────────────────────────────────────────┐
│                         LEADER AGENT                             │
│                    (Orchestrates, Decides)                       │
└─────────────────────────────────────────────────────────────────┘
         │              │              │              │
         ▼              ▼              ▼              ▼
    ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
    │ Code    │   │ Test    │   │ Security│   │ Docs    │
    │ Writer  │   │ Engineer│   │ Analyst │   │ Writer  │
    └─────────┘   └─────────┘   └─────────┘   └─────────┘
         │              │              │              │
         └──────────────┴──────────────┴──────────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │  RESULT SYNTHESIS   │
                    │  (Merge, Validate)  │
                    └─────────────────────┘
```

Workers claim tasks, execute in parallel, results merge automatically.

### 4. Quality Gate Enforcement

**Non-negotiable standards:**

```
PRE-FLIGHT ─▶ LINT ─▶ TYPE ─▶ UNIT ─▶ INTEGRATION ─▶ SECURITY
     │                                                    │
     │         ┌──────────────────────────────────────────┘
     │         │
     │         ▼
     │    PERFORMANCE ─▶ BROWSER ─▶ A11Y ─▶ DOCS ─▶ MODERN
     │                                                 │
     │         ┌───────────────────────────────────────┘
     │         │
     ▼         ▼
WORK_QUEUE ─▶ KNOWN_ISSUES ─▶ GIT_STATE ─▶ DOD ─▶ ✅ DONE
```

**All gates must pass. No exceptions. No shortcuts.**

### 5. Continuous Learning

```yaml
Session Start:
  - Load project knowledge
  - Load success/failure patterns
  - Load improved prompts

During Session:
  - Track what works
  - Track what fails
  - Note patterns

Session End:
  - Persist learnings
  - Update prompts
  - Build knowledge base
```

---

## User Interaction Model

### Minimal Intervention

The user should only need to:

1. **Start** — "Build X" or "Fix Y" or "Improve Z"
2. **Approve** (optional) — Risky operations, major decisions
3. **Receive** — Finished work, status updates

### Interaction Points

| Situation | Engine Behavior |
|-----------|-----------------|
| Clear requirement | Execute autonomously |
| Ambiguous requirement | Ask ONE clarifying question |
| Multiple valid approaches | Pick best, document decision |
| Risky operation | Request approval |
| Stuck/looping | Pivot strategy, notify if persists |
| Complete | Report results, suggest next steps |

### Status Communication

```markdown
## Current Status

**Phase:** EXECUTE (4/10)
**Progress:** ████████░░ 80%
**Current Task:** Implementing user authentication

### Completed
- [x] Project scaffold
- [x] Database schema
- [x] API endpoints

### In Progress
- [ ] Authentication (80%)

### Upcoming
- [ ] Frontend components
- [ ] Testing
- [ ] Documentation

### Blockers
None

### Decisions Made
- Selected JWT over sessions (stateless, scalable)
- Using PostgreSQL (relational data, complex queries)
```

---

## Architecture Principles

### 1. Event-Driven Core

Everything is an event:
```
request.received → classify.complete → plan.created →
task.started → task.complete → gate.passed →
checkpoint.created → iteration.complete → work.done
```

Components subscribe to events, react independently, publish results.

### 2. Schema-First Design

Every component has a schema:
- Skills, commands, agents, patterns, rules
- Events, state, configuration
- IDE autocomplete, validation, documentation

### 3. Modular Phases

Each phase is independent:
- Can be extended, replaced, or skipped
- Clear inputs and outputs
- Testable in isolation

### 4. Extensible Everything

```
.claude/extensions/
├── skills/          # Add custom skills
├── commands/        # Add custom commands
├── agents/          # Add custom agents
├── patterns/        # Add custom patterns
├── gates/           # Add custom quality gates
└── hooks/           # Add custom event handlers
```

Drop in extensions, they're automatically discovered and integrated.

### 5. State as Truth

JSON state is the single source of truth:
- Current phase, progress, work queue
- Decisions made, checkpoints created
- Metrics, history, learnings

Markdown is rendered from state, not parsed into it.

---

## Success Metrics

### For the Engine

| Metric | Target |
|--------|--------|
| Autonomy Rate | >90% of work without human input |
| Quality Gate Pass Rate | 100% (first or second attempt) |
| Loop Completion Rate | >95% reach "done" state |
| Self-Recovery Rate | >80% recover from errors automatically |
| Time to First Commit | <5 minutes from start |

### For Users

| Metric | Target |
|--------|--------|
| Questions Asked | <3 per task |
| Approval Requests | <2 per task |
| Manual Interventions | <1 per task |
| Satisfaction | "It just works" |

---

## The Ultimate Test

**Scenario 1: Greenfield**
```
User: "Build me a task management SaaS with team collaboration"
Engine: [2 hours later] "Done. Here's your deployed app with:
- User authentication
- Team workspaces
- Task CRUD with assignments
- Real-time updates
- 95% test coverage
- Full documentation
- CI/CD pipeline
- Staging deployment

What would you like to add or change?"
```

**Scenario 2: Brownfield**
```
User: "Fix the performance issues in this legacy codebase"
Engine: [4 hours later] "Done. I:
- Identified 12 performance bottlenecks
- Fixed 10 automatically (2 need architectural decisions)
- Improved load time from 8s to 1.2s
- Added performance monitoring
- Created PERFORMANCE.md with ongoing recommendations
- All tests pass, no regressions

Here are the 2 items that need your input..."
```

**Scenario 3: Enhancement**
```
User: "Add dark mode"
Engine: [30 minutes later] "Done. Added:
- System preference detection
- Manual toggle with persistence
- Smooth transition animations
- All components themed
- Tests for both modes
- Updated accessibility compliance

Preview it here: [link]"
```

---

## V2 vs V1

| Aspect | V1 | V2 |
|--------|----|----|
| **Autonomy** | Guided loop | True autonomy |
| **Self-Awareness** | Capability inventory | Active meta-cognition |
| **Learning** | Feedback files | Continuous improvement |
| **Brownfield** | Manual analysis | Automatic adaptation |
| **State** | Parsed Markdown | JSON truth |
| **Events** | Fixed hooks | Pub/sub everything |
| **Extensions** | Fork and modify | Drop-in extensions |
| **Quality** | Gate checking | Gate enforcement |
| **Multi-Agent** | Parallel execution | Swarm intelligence |

---

## Guiding Questions for V2 Development

1. **Does this increase autonomy?** — If yes, do it.
2. **Does this reduce user friction?** — If yes, do it.
3. **Does this make the engine smarter?** — If yes, do it.
4. **Is this self-aware?** — The engine should know about everything it does.
5. **Is this self-improving?** — Every action should feed back into learning.
6. **Does this work on any project?** — Generic over specific.
7. **Is this extensible?** — Can users add their own?

---

## Final Vision Statement

> **Claude Conductor V2 is an autonomous development partner that understands your project, knows its own capabilities, makes intelligent decisions, executes with quality, learns from every action, and continuously improves — transforming "build this" into "here it is" with minimal human intervention.**

It's not a tool you use. It's a **partner that builds with you**.

---

*This is the north star. Every design decision in V2 should serve this vision.*
