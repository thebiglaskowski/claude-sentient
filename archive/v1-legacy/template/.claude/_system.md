# System Orchestration Guide v3.2

This document defines how all platform components work together as a unified development team. Version 3.2 introduces context budget monitoring, parallel task decomposition, decision logging, and commit checkpoints for rollback capability.

---

## Platform Architecture v3.2

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER REQUEST                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        HOOKS LAYER                               │
│  SessionStart → session-start.sh (initialize + show capabilities)│
│  UserPromptSubmit → context-injector.py (load context)          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   TASK ORCHESTRATOR                              │
│  • Classifies task type                                          │
│  • Checks context budget (spawn sub-agents if >70%)              │
│  • Decomposes into parallel units (if applicable)                │
│  • Selects rules, agents, patterns, snippets                     │
│  • Sets quality gates (15 gates - ALL BLOCKING)                  │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        ┌─────────┐     ┌─────────┐     ┌───────────────┐
        │  RULES  │     │ AGENTS  │     │  CAPABILITY   │
        │(13 refs)│     │(15 exp) │     │  INVENTORY    │
        └─────────┘     └─────────┘     │ + PATTERNS    │
                                        │ + SNIPPETS    │
                                        └───────────────┘
              │               │               │
              └───────────────┼───────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│          INTELLIGENT AUTONOMOUS LOOP v3.2 (10 Phases)            │
│                                                                  │
│  Phase 1: CONTEXTUALIZE → Phase 2: ASSESS                       │
│      ↓                                                           │
│  Phase 2.5: META-COGNITION (choose best approach from inventory)│
│      ↓                                                           │
│  Phase 3: PLAN (+ decompose into parallel units)                │
│      ↓                                                           │
│  Phase 4: BUILD (+ log decisions to DECISIONS_LOG.md)           │
│      ↓                                                           │
│  Phase 5: TEST → Phase 6: QUALITY                               │
│      ↓                                                           │
│  Phase 6.25: CHECKPOINT (create verified commit for rollback)   │
│      ↓                                                           │
│  Phase 6.5: REASSESS (pivot if stuck, spawn specialists)        │
│      ↓                                                           │
│  Phase 7: EVALUATE → Phase 8: RECOVER → Loop or DONE            │
├─────────────────────────────────────────────────────────────────┤
│               15 QUALITY GATES (ALL BLOCKING)                    │
│  CODE QUALITY: PRE-FLIGHT → LINT → TYPE → UNIT → INTEGRATION   │
│                SECURITY → PERFORMANCE → BROWSER → A11Y → DOCS   │
│                MODERN                                            │
│  WORK COMPLETION: WORK_QUEUE → KNOWN_ISSUES → GIT_STATE → DoD   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│         DEFINITION OF DONE (dod-verifier.py) - STRICT           │
│  • Actually runs tests, lint, coverage, security commands        │
│  • Verifies work queue empty (parses LOOP_STATE.md)             │
│  • Verifies no unresolved S0/S1 (parses KNOWN_ISSUES.md)        │
│  • Verifies git state clean                                      │
│  • Exit code 0 = pass, Exit code 1 = loop continues             │
│  • NO WARNINGS, NO EXCEPTIONS - all thresholds must be met      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   COMPLETE ✓    │
                    └─────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     HOOKS (12 Total)                             │
├─────────────────────────────────────────────────────────────────┤
│  Setup           → setup-init.sh       (one-time init)          │
│  SessionStart    → session-start.sh    (session init + caps)    │
│  UserPromptSubmit→ context-injector.py (context loading)        │
│  PreToolUse      → bash-auto-approve.py (auto-approve safe)     │
│  PreToolUse      → file-validator.py   (validate writes)        │
│  PostToolUse     → post-edit.sh        (format/lint)            │
│  PostToolUseFailure → error-recovery.py (error handling)        │
│  SubagentStart   → agent-tracker.py    (track agents)           │
│  SubagentStop    → agent-synthesizer.py (merge results)         │
│  PreCompact      → pre-compact.sh      (backup state)           │
│  Stop            → dod-verifier.py     (STRICT verification)    │
│  SessionEnd      → session-end.sh      (cleanup/metrics)        │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Relationships

### Commands → Skills → Rules

| Command | Auto-Loads Skills | Default Rules |
|---------|-------------------|---------------|
| `/cc-loop` | autonomous-loop, task-orchestrator, definition-of-done, meta-cognition, context-budget-monitor, parallel-task-decomposer, decision-logger, commit-checkpoint | Per task type |
| `/cc-review` | pre-commit, severity-levels | code-quality, testing, security |
| `/cc-secure` | severity-levels | security |
| `/cc-test` | test-first | testing |
| `/cc-refactor` | test-first | code-quality, testing |
| `/cc-plan` | - | documentation |
| `/cc-daily` | session-memory, smart-context, context-budget-monitor | Per task |
| `/cc-fix` | error-recovery, decision-logger | error-handling, testing |
| `/cc-perf` | - | performance, database |
| `/cc-ui` | - | ui-ux-design |
| `/cc-terminal` | - | terminal-ui |
| `/cc-pr` | pre-merge | git-workflow |
| `/cc-commit` | commit-style, pre-commit, commit-checkpoint | git-workflow |
| `/cc-release` | pre-release | documentation |

### Task Types → Agents

| Task Type | Primary Agent | Secondary Agents |
|-----------|---------------|------------------|
| Security | security-analyst | code-reviewer |
| API | code-reviewer | security-analyst |
| UI/Frontend | ui-ux-expert | accessibility-expert, seo-expert |
| Database | database-expert | code-reviewer |
| Performance | code-reviewer | database-expert |
| Documentation | documentation-writer | - |
| Infrastructure | devops-engineer | security-analyst |
| Testing | test-engineer | code-reviewer |
| Research | researcher | - |
| Terminal/CLI | terminal-ui-expert | - |

### Severity → Response

| Severity | Blocks Completion | Required Action |
|----------|-------------------|-----------------|
| S0 Critical | YES | Fix immediately, no other work |
| S1 High | YES | Fix before any feature work |
| S2 Medium | NO | Add to work queue, prioritize |
| S3 Low | NO | Track, fix when convenient |

---

## Execution Modes

### 1. Single Command Mode
```
User: /review src/auth
→ Loads code-reviewer perspective
→ Loads @rules/code-quality, @rules/testing, @rules/security
→ Produces findings report
→ Done
```

### 2. Autonomous Loop Mode
```
User: /loop "implement user dashboard"
→ Orchestrator analyzes task
→ Loads relevant rules
→ Creates work queue
→ Iterates: BUILD → TEST → QUALITY → EVALUATE
→ Spawns agents as needed
→ Continues until DoD met
→ Done
```

### 3. Agent-Assisted Mode
```
User: Spawn security-analyst to audit auth module
→ Forks context
→ Agent performs deep analysis
→ Returns structured report
→ Main context receives summary
→ Continue with findings
```

---

## Context Management Strategy

### Token Budget Allocation

```
Total Budget: ~100K tokens (varies by model)

Allocation Strategy:
├── 40% - Active working files
├── 25% - Test files and coverage
├── 15% - Rules and reference docs
├── 10% - Agent reports and findings
└── 10% - Conversation history

Context Budget Thresholds (context-budget-monitor skill):
├── < 50%: 🟢 Green - Continue normally
├── 50-70%: 🟡 Yellow - Consider sub-agents for heavy tasks
├── 70-85%: 🟠 Orange - Spawn sub-agents for all new tasks
└── > 85%: 🔴 Red - Delegate everything, context is full
```

### Context Optimization Skills

| Skill | Purpose | Activation |
|-------|---------|------------|
| smart-context | Load only relevant context | Task start |
| session-memory | Avoid re-reading files | Continuous |
| context-fork | Isolate agent exploration | Agent spawn |
| context-budget-monitor | Track usage, suggest sub-agents | Heavy operations |

### Preventing Context Exhaustion

1. **Proactive Summarization**
   - Summarize findings before context fills
   - Store summaries in LOOP_STATE.md
   - Reference summaries, not full content

2. **Agent Offloading**
   - Complex analysis → Spawn agent
   - Agent works in isolated context
   - Returns summary only

3. **Incremental File Reading**
   - Read relevant sections, not entire files
   - Use PROJECT_MAP.md for navigation
   - Cache file understanding in session

4. **Work Queue Chunking**
   - Process 3-5 items per iteration
   - Complete, commit, summarize
   - Fresh context for next chunk

---

## Agent Coordination

### Parallel Agent Strategy

When multiple perspectives needed:
```
┌─────────────────────────────────────────┐
│           COORDINATOR                    │
│  (main conversation)                     │
└─────────────────────────────────────────┘
              │
    ┌─────────┼─────────┐
    ▼         ▼         ▼
┌───────┐ ┌───────┐ ┌───────┐
│Agent A│ │Agent B│ │Agent C│
│(fork) │ │(fork) │ │(fork) │
└───────┘ └───────┘ └───────┘
    │         │         │
    └─────────┼─────────┘
              ▼
┌─────────────────────────────────────────┐
│        RESULT SYNTHESIZER                │
│  • Merge findings                        │
│  • Deduplicate issues                    │
│  • Prioritize by severity                │
│  • Create unified work queue             │
└─────────────────────────────────────────┘
```

### Agent Communication Protocol

Agents return structured reports:
```markdown
## Agent Report: [Agent Type]

### Summary
[One paragraph overview]

### Findings by Severity
#### S0 - Critical
[Findings with evidence]

#### S1 - High
[Findings with evidence]

### Recommendations
[Prioritized action items]

### Files Analyzed
[List of files reviewed]
```

---

## Parallel Task Decomposition

### When to Decompose (parallel-task-decomposer skill)

Complex tasks can be broken into independent units for faster execution:

| Decomposition Type | Pattern | Example |
|-------------------|---------|---------|
| Module-based | Split by module/feature | User module + Order module |
| Concern-based | Split by responsibility | Frontend + Backend + Database |
| Layer-based | Split by architecture layer | API + Service + Repository |
| Test-Implementation | Tests parallel with implementation | Write tests while coding |

### Decomposition Decision Tree

```
CAN TASK BE DECOMPOSED?
├── Check for independent modules → Module-based
├── Check for separate concerns → Concern-based
├── Check for distinct layers → Layer-based
├── Can tests run while implementing? → Test-Implementation parallel
└── None apply? → Execute sequentially
```

### Parallel Execution Rules

1. **Independence Required** — Units must not depend on each other
2. **Shared State Forbidden** — No concurrent writes to same files
3. **Synthesis Required** — Results must be merged after completion
4. **Conflict Resolution** — Plan for merge conflicts upfront

---

## Decision Logging

### When to Log Decisions (decision-logger skill)

Log significant decisions that:
- Affect architecture or design
- Choose between multiple valid approaches
- Involve trade-offs (performance vs. simplicity)
- Defer work or scope changes
- Have security implications

### Decision Categories

| Category | ID Prefix | Examples |
|----------|-----------|----------|
| Technology | TECH- | Framework, library, tool choices |
| Architecture | ARCH- | Patterns, structure, layers |
| Trade-offs | TRADE- | Performance vs. simplicity |
| Scope | SCOPE- | Feature additions/deferrals |
| Security | SEC- | Auth, encryption, validation |
| Performance | PERF- | Caching, optimization strategies |
| Bug Fixes | FIX- | Root cause, chosen solution |
| Deferrals | DEFER- | Postponed work with rationale |

### Decision Format

```markdown
## [CATEGORY-XXX] Brief Title

**Context:** Why this decision was needed
**Decision:** What was decided
**Alternatives:** Other options considered
**Rationale:** Why this option was chosen
**Implications:** Consequences and follow-up
**Commit:** Reference to implementing commit
```

---

## Commit Checkpoints

### When to Create Checkpoints (commit-checkpoint skill)

Create checkpoint commits after:
- Feature implementation verified working
- Tests pass for completed unit
- Quality gates pass
- Before starting risky changes

### Checkpoint Benefits

1. **Easy Rollback** — Return to known-good state
2. **Clear History** — Understand what was verified
3. **Session Continuity** — Resume from verified point
4. **Decision Traceability** — Link commits to decisions

### Checkpoint Commit Format

```
checkpoint: [feature-name] verified

- Tests passing
- [Quality gates status]
- [Decision references]

Decisions: [ARCH-001], [TECH-002]
```

---

## Browser Integration

### When Browser Verification Activates

| Trigger | Browser Action |
|---------|----------------|
| UI component created | Screenshot at viewports |
| Style changes | Visual diff vs baseline |
| Form implemented | Test submission flow |
| Responsive work | Check all breakpoints |
| Accessibility work | Run axe-core audit |
| E2E test needed | Automated flow check |

### Browser Verification Flow

```
Code Change (UI)
      │
      ▼
Start Local Server
      │
      ▼
Navigate to Page
      │
      ▼
Capture Screenshots
├── Desktop (1280px)
├── Tablet (768px)
└── Mobile (375px)
      │
      ▼
Run Accessibility Audit
      │
      ▼
Compare to Baseline (if exists)
      │
      ▼
Report Findings
```

### MCP Browser Tools

Available tools for verification:
- `mcp__claude-in-chrome__navigate` - Go to URL
- `mcp__claude-in-chrome__computer` - Screenshot, click, type
- `mcp__claude-in-chrome__read_page` - Get accessibility tree
- `mcp__claude-in-chrome__javascript_tool` - Run tests in page

---

## Quality Gate Cascade (15 Gates - ALL BLOCKING)

### Gate Execution Order

```
CODE QUALITY GATES:
1.  PRE-FLIGHT    → Environment, dependencies, git state
2.  LINT          → 0 errors, 0 warnings (BLOCKING)
3.  TYPE          → 0 type errors (BLOCKING)
4.  UNIT TEST     → 100% pass, coverage >= 80% (BLOCKING)
5.  INTEGRATION   → 100% pass (BLOCKING)
6.  SECURITY      → 0 S0/S1 vulnerabilities (BLOCKING)
7.  PERFORMANCE   → Bundle size, N+1, Web Vitals (BLOCKING)
8.  BROWSER       → Visual verification (BLOCKING if UI)
9.  ACCESSIBILITY → axe-core audit (BLOCKING if UI)
10. DOCUMENTATION → README + CHANGELOG present (BLOCKING)
11. MODERN TECH   → No deprecated APIs (BLOCKING)

WORK COMPLETION GATES:
12. WORK QUEUE    → 0 pending/in-progress tasks (BLOCKING)
13. KNOWN ISSUES  → 0 unresolved S0/S1 (BLOCKING)
14. GIT STATE     → All changes committed (BLOCKING)
15. DoD           → dod-verifier.py exit code 0 (BLOCKING)

STRICT ENFORCEMENT: Loop CANNOT exit until ALL gates pass.
```

### Gate Failure Response

```
Gate Fails
    │
    ▼
Identify Failure Reason
    │
    ▼
Add to Work Queue (S0/S1 priority)
    │
    ▼
Return to BUILD phase
    │
    ▼
Fix Issue
    │
    ▼
Re-run Gates
```

---

## Session Continuity

### State Files

| File | Purpose | Updated When |
|------|---------|--------------|
| STATUS.md | Current project state | After each significant change |
| LOOP_STATE.md | Autonomous loop progress | Each iteration |
| DECISIONS_LOG.md | Significant decisions with rationale | When decisions made |
| CHECKPOINTS.md | Verified commit history for rollback | After verified features |
| KNOWN_ISSUES.md | Tracked limitations | When issues deferred |
| CHANGELOG.md | Version history | Before release |

### Session Handoff

When context is exhausted or session ends:
```
1. Update LOOP_STATE.md with:
   - Current work queue
   - Completed items
   - Next steps
   - Context budget status
   - Approaches tried (meta-cognition)

2. Update DECISIONS_LOG.md with:
   - Significant decisions made this session
   - Rationale and alternatives considered
   - Links to relevant commits

3. Update CHECKPOINTS.md with:
   - Verified feature commits
   - Rollback points

4. Update STATUS.md with:
   - What was accomplished
   - What remains
   - Blockers identified

5. Create checkpoint commit (commit-checkpoint skill)
   - Include decision references in message
   - Mark as rollback point if feature verified

6. Next session reads state files first
   - Resume from last checkpoint if needed
```

---

## Model Routing

### Task → Model Selection

| Task Complexity | Model | Use Cases |
|-----------------|-------|-----------|
| Quick lookup | haiku | File search, simple questions |
| Standard work | sonnet | Most development tasks |
| Complex analysis | opus | Security audits, architecture |
| Deep reasoning | opus + ultrathink | Critical decisions |

### When to Escalate

- Security decisions → Use opus
- Architecture choices → Use opus
- Unclear requirements → Use opus
- Performance critical → Use opus + ultrathink
- Standard implementation → sonnet is fine

---

## Error Recovery

### When Errors Occur

```
Error Detected
      │
      ▼
Classify Error Type
├── Transient (retry)
├── Configuration (fix config)
├── Code bug (add to queue)
└── External (wait/workaround)
      │
      ▼
Apply Recovery Strategy
      │
      ▼
Document in KNOWN_ISSUES.md (if unresolved)
      │
      ▼
Continue or Escalate to User
```

### Stall Detection

If same error 3+ times:
1. Stop attempting same fix
2. Document in LOOP_STATE.md
3. Add to KNOWN_ISSUES.md
4. Ask user for guidance or skip

---

## Summary: The Team Working Together

```
ORCHESTRATOR (Task Orchestrator)
"I analyze what kind of work this is and assemble the right team"
    │
    ├── STANDARDS (Rules + Patterns)
    │   "We define how things should be done"
    │
    ├── EXPERTS (Agents)
    │   "We provide deep expertise in specific areas"
    │
    ├── WORKERS (Commands + Snippets)
    │   "We execute specific tasks efficiently"
    │
    ├── QUALITY (DoD + Gates)
    │   "We verify work meets standards"
    │
    ├── MEMORY (Skills + Session State)
    │   "We optimize how we work and remember what we learned"
    │
    ├── INTELLIGENCE (Meta-Cognition + Context Budget)
    │   "We choose the best approach and manage resources wisely"
    │
    ├── PARALLELIZATION (Task Decomposer + Parallel Agents)
    │   "We break complex work into concurrent units"
    │
    ├── TRACEABILITY (Decision Logger + Checkpoints)
    │   "We document decisions and create rollback points"
    │
    └── VERIFICATION (Browser + Tests)
        "We check that it actually works as intended"
```

**Result:** A coordinated, self-aware team that iterates until the work is genuinely complete, with intelligent resource management, parallel execution capabilities, decision traceability, and easy rollback to verified checkpoints.
