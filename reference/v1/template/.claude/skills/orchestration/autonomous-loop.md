---
name: autonomous-loop
description: Continuously cycle through quality gates until all issues resolved
argument-hint: "[focus area] [--max-iterations=N]"
model: opus
version: 3.2.0
tags: [orchestration, workflow, autonomous]
---

# Autonomous Development Loop v3.2

Continuously cycle through 10 phases and 15 quality gates until every issue is resolved and every checklist passes. Integrates with hooks for automated context injection, error recovery, and agent coordination.

**v3.2 Enhancements:**
- Context budget monitoring (prevents context bloat)
- Parallel task decomposition (faster execution)
- Decision logging (traceability)
- Commit checkpoints (easy rollback)

## Description

This skill implements an exhaustive development loop with **STRICT ENFORCEMENT**:
- Runs all 12 quality gates (security, testing, code quality, etc.)
- Identifies and fixes issues automatically
- Uses hooks for context injection and error recovery
- Coordinates parallel agents for comprehensive analysis
- **CANNOT EXIT until ALL thresholds are met**
- Verifies Definition of Done with actual test/coverage runs
- No warnings, no exceptions — every gate must pass

**STRICT MODE**: The loop will continue indefinitely until:
- Test coverage >= 80%
- 0 lint errors, 0 type errors
- 0 security vulnerabilities (S0/S1)
- All tests passing
- Documentation complete

Triggers on: "autonomous loop", "keep working", "work until done", "exhaustive mode", "/loop"

## Arguments

```
$1 - Optional: focus area (security, testing, features, all)
     Default: all

--max-iterations=N  Maximum loop iterations (default: 50)
--pause-on=S0|S1    Pause for user on severity level (default: S0 only)
--modern            Force modern tech alternatives check
--parallel          Enable parallel agent execution
--dry-run           Show what would be done without doing it
```

## STRICT MODE THRESHOLDS (Non-Negotiable)

The loop CANNOT exit until ALL of these are met:

### Code Quality Gates

| Metric | Threshold | Verified By |
|--------|-----------|-------------|
| Test Coverage (overall) | >= 80% | Running tests with coverage |
| Test Coverage (new code) | >= 90% | Running tests with coverage |
| Lint Errors | 0 | Running linter |
| Lint Warnings | 0 | Running linter |
| Type Errors | 0 | Running type checker |
| Security S0 | 0 | Running security audit |
| Security S1 | 0 | Running security audit |
| Failing Tests | 0 | Running test suite |

### Work Completion Gates

| Metric | Threshold | Verified By |
|--------|-----------|-------------|
| Work Queue | Empty | Parsing LOOP_STATE.md, STATUS.md |
| Pending Tasks | 0 | Counting ⏳/[ ] markers |
| In-Progress Tasks | 0 | Counting 🔄/[-] markers |
| Blocked Tasks | 0 | Counting blocked items |
| S0 Issues | 0 unresolved | Parsing KNOWN_ISSUES.md |
| S1 Issues | 0 unresolved | Parsing KNOWN_ISSUES.md |
| README.md | Exists | File check |
| CHANGELOG.md | Updated | Content check |
| Git State | Clean | Running git status |

**These thresholds are enforced by `dod-verifier.py` (Stop hook).**

The hook checks EVERYTHING:
- Runs test/lint/type/security commands and parses output
- Parses LOOP_STATE.md for pending work
- Parses KNOWN_ISSUES.md for unresolved S0/S1
- Checks git status for uncommitted changes
- Verifies documentation exists

**Exit code 1 = loop continues (work incomplete)**
**Exit code 0 = loop may exit (ALL gates pass)**

## The Loop (10 Phases - With Intelligence)

```
┌─────────────────────────────────────────────────────────────────────────┐
│               INTELLIGENT AUTONOMOUS LOOP v3.2 (10 Phases)               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ┌───────────────┐    ┌─────────┐    ┌───────────────┐                │
│   │ CONTEXTUALIZE │───▶│ ASSESS  │───▶│ META-COGNITION│                │
│   └───────────────┘    └─────────┘    └───────┬───────┘                │
│          ▲                                     │                         │
│          │              ┌─────────────────────┘                         │
│          │              ▼                                                │
│          │        ┌─────────┐    ┌─────────┐    ┌─────────┐            │
│          │        │  PLAN   │───▶│  BUILD  │───▶│  TEST   │            │
│          │        │+DECOMP  │    │+DECIDE  │    └─────────┘            │
│          │        └─────────┘    └─────────┘         │                  │
│          │                                           ▼                   │
│   ┌─────────┐    ┌──────────┐    ┌──────────┐   ┌─────────┐           │
│   │  DONE   │◀───│ EVALUATE │◀───│CHECKPOINT│◀──│ QUALITY │           │
│   └─────────┘    └──────────┘    └──────────┘   └────┬────┘           │
│          ▲              │              │              │                  │
│          │         ALL PASS?      GIT COMMIT    REASSESS?               │
│          │              │              │              │                  │
│   ┌─────────┐      YES  │              │        YES   │                 │
│   │ RECOVER │◀──────────┴──────────────┴──────────────┘                │
│   └────┬────┘                                                           │
│        │ Smart recovery using capability inventory                      │
│        └─────────────▶ Back to CONTEXTUALIZE with new strategy         │
│                                                                          │
│   ENHANCED PHASES:                                                       │
│   • PLAN+DECOMP: Parallel task decomposition for efficiency             │
│   • BUILD+DECIDE: Decision logging for traceability                     │
│   • CHECKPOINT: Git commits after verified features                     │
│   • META-COGNITION: Context budget monitoring, approach selection       │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Quality Gates (All Blocking)

```
┌─────────────────────────────────────────────────────────────────────────┐
│              QUALITY GATES - ALL BLOCKING (NO EXCEPTIONS)                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  CODE QUALITY GATES:                                                     │
│  GATE 1:  PRE-FLIGHT      Environment, dependencies, git state         │
│  GATE 2:  LINT            0 errors, 0 warnings                         │
│  GATE 3:  TYPE            0 type errors                                │
│  GATE 4:  UNIT TEST       100% pass, coverage >= 80%                   │
│  GATE 5:  INTEGRATION     100% pass                                    │
│  GATE 6:  SECURITY        0 S0/S1 vulnerabilities                      │
│  GATE 7:  PERFORMANCE     Bundle size, N+1, Core Web Vitals           │
│  GATE 8:  BROWSER         Visual verification, responsive             │
│  GATE 9:  ACCESSIBILITY   axe-core, keyboard nav                      │
│  GATE 10: DOCUMENTATION   README + CHANGELOG present                   │
│  GATE 11: MODERN TECH     No deprecated APIs                          │
│                                                                          │
│  WORK COMPLETION GATES:                                                  │
│  GATE 12: WORK QUEUE      0 pending/in-progress tasks                  │
│  GATE 13: KNOWN ISSUES    0 S0/S1 unresolved                          │
│  GATE 14: GIT STATE       All changes committed                        │
│  GATE 15: DEFINITION OF DONE  dod-verifier.py exit code 0             │
│                                                                          │
│  Loop CANNOT exit until ALL gates pass. No warnings. No exceptions.    │
└─────────────────────────────────────────────────────────────────────────┘
```

## Hook Integration

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    HOOK INTEGRATION                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  SessionStart       → session-start.sh      Initialize session state    │
│  UserPromptSubmit   → context-injector.py   Load relevant context       │
│  PreToolUse         → bash-auto-approve.py  Auto-approve safe commands  │
│  PreToolUse         → file-validator.py     Validate file operations    │
│  PostToolUse        → post-edit.sh          Format/lint after edits     │
│  PostToolUseFailure → error-recovery.py     Classify & recover errors   │
│  SubagentStart      → agent-tracker.py      Track parallel agents       │
│  SubagentStop       → agent-synthesizer.py  Merge agent results         │
│  PreCompact         → pre-compact.sh        Backup before compaction    │
│  Stop               → dod-verifier.py       Verify Definition of Done   │
│  SessionEnd         → session-end.sh        Cleanup and metrics         │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Loop Phases (Detailed)

### Phase 1: CONTEXTUALIZE (NEW in v3.0)
```
Load appropriate context for the task:

STEP 1: QUERY CLASSIFICATION (NEW in v3.2)
├── Analyze task complexity and scope
├── Classify as: depth-first, breadth-first, or straightforward
│   ├── Depth-first: Complex problem needing deep analysis (1 agent, opus)
│   ├── Breadth-first: Many independent subtasks (3-20 agents, haiku/sonnet)
│   └── Straightforward: Simple task, execute directly (no subagents)
├── Determine subagent count based on complexity:
│   ├── Simple (1-2 files): 1 agent or none
│   ├── Medium (3-10 files): 3-5 agents
│   └── Complex (10+ files): 5-20 agents
└── Set orchestration mode (standard/swarm/pipeline)

STEP 2: CONTEXT LOADING
├── context-injector.py analyzes prompt keywords
├── Load relevant files via smart-context-v3
├── Load rules based on task type (task-orchestrator)
├── Check context budget before heavy operations
└── Initialize LOOP_STATE.md

STEP 3: AGENT SPAWNING (if breadth-first)
├── Spawn parallel agents based on classification
└── agent-tracker.py monitors parallel execution

Hooks Involved:
├── UserPromptSubmit → context-injector.py
├── SubagentStart → agent-tracker.py (if parallel)
└── smart-context-v3 skill activated

Skills Involved:
├── queue-manager (query classification)
└── smart-context (context loading)
```

### Phase 2: ASSESS
```
Run /assess to understand current state:
- Codebase health score
- Existing issues by severity
- Test coverage gaps
- Security vulnerabilities
- Tech debt items
- Outdated dependencies
- Agent findings (if parallel agents used)

Hooks Involved:
└── SubagentStop → agent-synthesizer.py (merges findings)
```

### Phase 2.5: META-COGNITION (Intelligence Layer)
```
Consult capability inventory and make intelligent decisions:

STEP 1: LOAD CAPABILITY INVENTORY
├── Read context/CAPABILITY_INVENTORY.md
├── Know all 35 commands available
├── Know all 15 agents available
├── Know all 13 rules available
└── Know decision matrix

STEP 2: EVALUATE SITUATION
├── What type of work is this? (feature/bug/security/etc.)
├── What's the current state? (coverage, issues, blockers)
├── What's been tried before? (check LOOP_STATE.md)
├── What's working? What's not?
└── Are we making progress?

STEP 3: SELECT STRATEGY
├── Consult decision matrix (situation → best tool)
├── Choose primary approach
├── Identify backup approaches
├── Determine if specialists needed
├── Load relevant rules (@rules/*)
└── Document decision rationale

STEP 4: PREPARE EXECUTION
├── Queue specialists agents to spawn
├── Load rules for context
├── Set success metrics
└── Define pivot triggers

Example Decisions:
├── Coverage at 40% → Spawn test-engineer agent
├── Security issue found → Spawn security-analyst, load @rules/security
├── UI work needed → Spawn ui-ux-expert, load @rules/ui-ux-design
├── Stuck after 2 iterations → Spawn researcher, try different approach
└── Performance problem → Spawn performance-optimizer, load @rules/performance
```

### Phase 3: PLAN (Enhanced with Decomposition)
```
If no active plan exists:
- Check for existing blueprint
- If features needed, ask user for direction (CHECKPOINT)
- Create prioritized work list

PARALLEL TASK DECOMPOSITION (NEW):
├── Analyze work queue for independent tasks
├── Identify parallelizable work units
├── Group by: module, concern, layer, or type
├── Assign appropriate agents to each unit
├── Mark dependencies between units
└── Execute independent units in parallel

Priority order:
1. S0 Critical issues (security, crashes)
2. S1 High issues (major bugs, blockers)
3. Test coverage gaps (< 80%)
4. S2 Medium issues
5. Tech debt items
6. S3 Low issues
7. Modernization opportunities

Skills Involved:
├── parallel-task-decomposer (identifies parallel units)
└── context-budget-monitor (checks if spawning needed)
```

### Phase 4: BUILD (Enhanced with Decision Logging)
```
For each item in priority order:
- Implement fix/feature
- Follow existing patterns (use @patterns/* when applicable)
- Use modern tech (check with context7)
- Use code snippets (snippet:* for boilerplate)
- Create/update tests
- Document changes

DECISION LOGGING (NEW):
├── After each significant choice, log to DECISIONS_LOG.md
├── Capture: decision, alternatives, rationale
├── Link decisions to code locations
├── Reference decisions in commit messages
└── Categories: TECH, ARCH, TRADE, SCOPE, SEC, PERF, FIX, DEFER

CONTEXT MONITORING (NEW):
├── Check context budget before heavy operations
├── If > 70% utilized → spawn sub-agent
├── Delegate self-contained tasks to agents
├── Keep main context lean and focused

Hooks Involved:
├── PreToolUse → file-validator.py (validate writes)
├── PostToolUse → post-edit.sh (format/lint)
└── PostToolUseFailure → error-recovery.py (handle errors)

Skills Involved:
├── decision-logger (captures decisions)
├── context-budget-monitor (prevents bloat)
└── pattern/snippet surfacing (from task-orchestrator)
```

### Phase 5: TEST (Thresholds Enforced)
```
Run comprehensive testing with STRICT thresholds:
- Unit tests: ALL must pass (0 failures allowed)
- Coverage: >= 80% overall, >= 90% for new code
- Integration tests: ALL must pass
- Type checking: 0 errors allowed
- Lint checks: 0 errors, 0 warnings
- Build verification: Must succeed
- Browser verification (if UI changes)

Quality Gates Checked (ALL BLOCKING):
├── GATE 2: LINT (0 errors, 0 warnings)
├── GATE 3: TYPE (0 errors)
├── GATE 4: UNIT TEST (100% pass, 80% coverage)
├── GATE 5: INTEGRATION (100% pass)
└── GATE 8: BROWSER (if applicable)

If ANY gate fails, add to work queue and continue loop.
```

### Phase 6: QUALITY (ALL GATES BLOCKING)
```
Run all quality gates — EVERY GATE IS BLOCKING:

CODE QUALITY GATES:
GATE 1:  □ PRE-FLIGHT      Environment, dependencies, git state
GATE 2:  □ LINT            0 errors, 0 warnings (BLOCKING)
GATE 3:  □ TYPE            0 type errors (BLOCKING)
GATE 4:  □ UNIT TEST       100% pass, coverage >= 80% (BLOCKING)
GATE 5:  □ INTEGRATION     100% pass (BLOCKING)
GATE 6:  □ SECURITY        0 S0/S1 vulnerabilities (BLOCKING)
GATE 7:  □ PERFORMANCE     Within limits (BLOCKING)
GATE 8:  □ BROWSER         Pass visual check (BLOCKING if UI)
GATE 9:  □ ACCESSIBILITY   Pass a11y audit (BLOCKING if UI)
GATE 10: □ DOCUMENTATION   README + CHANGELOG present (BLOCKING)
GATE 11: □ MODERN TECH     No deprecated APIs (BLOCKING)

WORK COMPLETION GATES:
GATE 12: □ WORK QUEUE      0 pending, 0 in-progress tasks (BLOCKING)
GATE 13: □ KNOWN ISSUES    0 S0/S1 unresolved (BLOCKING)
GATE 14: □ GIT STATE       All changes committed (BLOCKING)
GATE 15: □ DEFINITION OF DONE  dod-verifier.py exit code 0 (BLOCKING)

If ANY gate fails → Trigger evaluator-optimizer loop:
├── EVALUATE: Identify which gate(s) failed and why
├── OPTIMIZE: Generate fix for the failing condition
├── RE-EVALUATE: Run gate again after fix
├── ITERATE: Continue until gate passes or max iterations (3)
└── If still failing after 3 iterations → Add to work queue, continue loop

Skills Involved:
├── evaluator-optimizer (quality gate retry loops)
└── definition-of-done (completion criteria)
```

### Phase 6.25: CHECKPOINT (Commit Verified Work)
```
After quality gates pass for a feature, create a checkpoint commit:

CHECKPOINT CRITERIA (all must be true):
├── Tests pass for the feature
├── Linting passes (no errors, no warnings)
├── Type checking passes
├── Feature works as intended
├── No debug code left behind
└── Changes are logically complete

CHECKPOINT PROCESS:
├── Stage relevant files (not all files)
├── Create descriptive commit message
├── Include decision references (Decisions: TECH-001, etc.)
├── Update CHECKPOINTS.md with checkpoint info
├── Tag milestone if significant
└── Update LOOP_STATE.md with last checkpoint

COMMIT MESSAGE FORMAT:
├── Type: feat/fix/refactor/test/docs
├── Scope: (module)
├── Description: what was done
├── Details: bullet points
├── Decisions: references to DECISIONS_LOG.md
└── Co-Author tag

ROLLBACK SAFETY:
├── Each checkpoint is a potential rollback point
├── If next feature breaks something → revert to checkpoint
├── Clean history enables git bisect
└── Easy to identify which change caused issues

Skills Involved:
└── commit-checkpoint (creates verified commits)
```

### Phase 6.5: REASSESS (Pivot Check)
```
Check if current approach is working, pivot if needed:

TRIGGER CONDITIONS (any of these = reassess):
├── Same gate failed 3+ times
├── No improvement for 2 iterations
├── Coverage not increasing
├── Issues count not decreasing
├── Error recovery failed
└── User requested reassessment

REASSESSMENT PROCESS:

STEP 1: ANALYZE CURRENT STATE
├── What was the goal?
├── What approach was taken?
├── What's the actual result?
├── Where are we stuck?
└── Why isn't it working?

STEP 2: CONSULT CAPABILITY INVENTORY
├── What other tools could address this?
├── Is there a specialist agent for this problem?
├── Is there a rule with specific guidance?
├── Has context7 docs on this topic?
└── Can we break the problem down differently?

STEP 3: SELECT NEW STRATEGY
├── Choose alternative from decision matrix
├── Spawn specialist agent if not already tried
├── Load additional rules for guidance
├── Consider simplifying the problem
├── If truly stuck → Ask user (last resort)

STEP 4: LOG AND PIVOT
├── Document current approach result in LOOP_STATE.md
├── Document new strategy selection
├── Reset stuck counter
├── Update work queue with new approach
└── Return to CONTEXTUALIZE with fresh strategy

EXAMPLE PIVOTS:
├── Coverage stuck at 50% after 3 tries
│   → Spawn test-engineer agent
│   → "Generate comprehensive test suite for uncovered modules"
│
├── Lint errors keep reappearing
│   → Load @rules/code-quality
│   → Spawn code-reviewer for deeper analysis
│
├── Security issue won't resolve
│   → Spawn security-analyst (opus model)
│   → Load @rules/security for OWASP guidance
│
└── Build keeps failing
    → Spawn researcher to investigate root cause
    → Check context7 for framework-specific docs
```

### Phase 7: EVALUATE (STRICT ENFORCEMENT)
```
Check completion criteria with dod-verifier.py:

ALL MUST BE TRUE — NO EXCEPTIONS:
├── Coverage >= 80% overall (VERIFIED by running tests)
├── Coverage >= 90% for new code
├── Lint errors = 0 (VERIFIED by running linter)
├── Lint warnings = 0
├── Type errors = 0 (VERIFIED by running type checker)
├── S0 vulnerabilities = 0 (VERIFIED by security scan)
├── S1 vulnerabilities = 0
├── Failing tests = 0 (VERIFIED by running tests)
├── README.md exists and current
├── CHANGELOG.md updated
├── All 12 quality gates passing
├── Work queue empty (no pending items)
└── 2 consecutive passing iterations

IF ANY THRESHOLD NOT MET:
├── dod-verifier.py returns exit code 1
├── Add missing items to work queue
├── Go back to Phase 1 (CONTEXTUALIZE)
├── Loop continues — NO EXIT ALLOWED

Hooks Involved:
└── Stop → dod-verifier.py (exit code 0 = pass, 1 = fail)
```

### Phase 8: RECOVER (NEW in v3.0)
```
Handle errors and recover gracefully:
- Classify error type (error-classifier skill)
- Apply recovery strategy:
  ├── Transient: Retry with backoff
  ├── Actionable: Add fix to queue
  ├── Blocking: Pause for user
- Update work queue with discovered issues
- Return to Phase 1 (CONTEXTUALIZE)

Hooks Involved:
└── PostToolUseFailure → error-recovery.py

Recovery Actions:
├── Network errors → Retry with exponential backoff
├── Module not found → Suggest npm install
├── Type errors → Add to queue as S1
├── Syntax errors → Add to queue as S0 (priority)
├── Permission errors → Pause for user intervention
└── Rate limits → Wait and retry
```

## Dynamic Work Queue

**The loop continues when new work is discovered:**

```
┌─────────────────────────────────────────────────────────────┐
│                  WORK QUEUE MANAGEMENT                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  During any phase, if new issues/features are discovered:  │
│                                                             │
│  1. Add to work queue with appropriate priority            │
│  2. Continue current iteration                              │
│  3. Process new items in subsequent iterations             │
│                                                             │
│  Examples:                                                  │
│  - Fixing bug A reveals bug B → Add B to queue             │
│  - Security fix needs new tests → Add tests to queue       │
│  - Modernization reveals deprecated API → Add to queue     │
│  - User requests feature mid-loop → Add to queue           │
│                                                             │
│  The loop ONLY exits when:                                  │
│  ✅ Work queue is completely empty                          │
│  ✅ All quality gates pass                                  │
│  ✅ No new issues discovered in final iteration            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Work Queue Priority

New items are inserted by priority:
```
Priority Order:
1. S0 Critical (security, crashes) → Top of queue
2. S1 High (major bugs, blockers) → After S0
3. Blocking dependencies → After S1
4. S2 Medium → Middle
5. Test coverage gaps → Middle
6. S3 Low → Bottom
7. Enhancements/modernization → Bottom

Example queue evolution:

Iteration 1:
  [S1] Fix auth bypass
  [S2] Add input validation
  [S3] Refactor utils

Iteration 2 (discovered new issue while fixing auth):
  [S1] Fix session handling ← NEW (discovered)
  [S2] Add input validation
  [S2] Add tests for auth fix ← NEW (required)
  [S3] Refactor utils

Iteration 3 (user added feature request):
  [S2] Add input validation
  [S2] Add tests for auth fix
  [S2] Implement caching ← NEW (user request)
  [S3] Refactor utils
  [S3] Modernize date handling ← NEW (discovered)
```

### Accepting New Work Mid-Loop

The loop accepts new work from:

1. **Discovered Issues**
   - Bugs found while fixing other bugs
   - Security issues revealed by fixes
   - Test gaps identified during coverage push

2. **User Requests**
   - "Also add rate limiting"
   - "Include this feature too"
   - New requirements mid-session

3. **Modernization Discoveries**
   - Deprecated APIs found during review
   - Outdated patterns identified
   - Vulnerable dependencies discovered

4. **Quality Gate Failures**
   - Test failures create fix tasks
   - Review findings become work items
   - Security scan results added to queue

**The loop continues until the queue is empty AND all gates pass.**

## State Tracking

Create/update `LOOP_STATE.md`:

```markdown
# Autonomous Loop State

## Current Iteration: 7
## Started: 2024-01-15T10:00:00Z
## Status: IN_PROGRESS

## Quality Gates
| Gate | Status | Last Check | Issues |
|------|--------|------------|--------|
| Tests | ✅ PASS | 10:45:00 | 0 |
| Coverage | ❌ FAIL | 10:45:00 | 78% (need 80%) |
| Security | ✅ PASS | 10:42:00 | 0 S0/S1 |
| Lint | ✅ PASS | 10:40:00 | 0 |
| Work Queue | ❌ FAIL | 10:45:00 | 2 pending |
| Documentation | ✅ PASS | 10:35:00 | Complete |

## Work Queue
| Priority | Item | Status |
|----------|------|--------|
| S1 | Fix auth bypass | ✅ Done |
| S2 | Add input validation | 🔄 In Progress |
| S2 | Increase test coverage | ⏳ Pending |
| S3 | Refactor utils | ⏳ Pending |

## Approaches Tried (Meta-Cognition)
| Iteration | Approach | Result | Next Action |
|-----------|----------|--------|-------------|
| 1-3 | Direct implementation | Stuck at 40% coverage | Pivot to specialist |
| 4-5 | Spawned test-engineer | Coverage 40%→65% | Continue |
| 6-7 | Continue with test-engineer | Coverage 65%→78% | Continue |

## Pivots Made
- **Iteration 4**: Pivoted from direct implementation to test-engineer agent
  - Reason: Coverage stuck at 40% for 3 iterations
  - Result: Immediate improvement

## Agents Spawned
| Agent | Iteration | Purpose | Outcome |
|-------|-----------|---------|---------|
| test-engineer | 4 | Generate tests for coverage | +38% coverage |
| security-analyst | 5 | Audit auth module | Found 1 S1 issue |

## Iteration History
- #7: Coverage 75%→78%, added 3 more tests
- #6: Coverage 65%→75%, test-engineer added 8 tests
- #5: Fixed S1 security issue found by security-analyst
- #4: Pivoted to test-engineer agent
- #3: Stuck - coverage still 40%
- #2: Coverage still 40%, attempted direct test writing
- #1: Initial assessment - coverage 40%

## Stuck Counter
- Current streak without improvement: 0
- Trigger reassessment at: 2 iterations

## Checkpoints (User Input Required)
- [ ] Iteration 3: Confirmed feature direction
- [ ] Iteration 5: Approved breaking change
```

## User Checkpoints

The loop PAUSES for user input when:

1. **Direction Needed**
   - No clear next feature to implement
   - Multiple valid approaches exist
   - Breaking change required

2. **S0 Critical Decision**
   - Security issue with multiple fix strategies
   - Data migration required
   - External service decision

3. **Resource Question**
   - New dependency needed
   - Infrastructure change required
   - Cost implications

4. **Explicit Request**
   - User previously said "ask before X"

## Modern Tech Awareness

Each iteration checks:

```
1. Use context7 to verify current patterns
2. Check if dependencies have newer major versions
3. Identify deprecated APIs in use
4. Suggest modern alternatives when beneficial

Example triggers:
- Using moment.js → Suggest date-fns or dayjs
- Using request → Suggest fetch or axios
- Using callback patterns → Suggest async/await
- Using var → Suggest const/let
```

## Exit Conditions (STRICT ENFORCEMENT)

### Success Exit — ALL THRESHOLDS MUST BE MET
```
The loop CANNOT exit until ALL of the following are true:

MANDATORY THRESHOLDS (non-negotiable):
├── Test coverage >= 80% overall
├── Test coverage >= 90% for new/changed code
├── 0 lint errors
├── 0 lint warnings
├── 0 type errors
├── 0 S0 (critical) security vulnerabilities
├── 0 S1 (high) security vulnerabilities
├── 0 failing tests
├── Documentation complete (README + CHANGELOG)
├── All 12 quality gates passing
├── 2 consecutive passing iterations
├── Verification iteration confirms stability

VERIFICATION PROCESS:
├── After 2 consecutive passes, run ONE MORE full check
├── Re-run all 12 quality gates with dod-verifier.py
├── dod-verifier.py actually runs tests/lint/coverage
├── If exit code 0 (all pass) → EXIT SUCCESS
├── If exit code 1 (any fail) → Back to Phase 1 (reset counter)

Hook: Stop → dod-verifier.py returns exit code 0 or 1
```

### NO EXCEPTIONS
```
There are NO warnings. There are NO "continue anyway" options.
Every threshold must be met. Period.

If a threshold cannot be met:
├── Add work items to fix the issue
├── Loop continues
├── User can adjust thresholds in dod-verifier.py THRESHOLDS dict
├── But default thresholds are the standard
```

### Forced Exit
```
--max-iterations reached
OR user types "stop loop" / "pause"
OR unrecoverable error (RECOVER phase escalates)
OR loop detects no progress (same issues 3 iterations)

Session cleanup:
Hook: SessionEnd → session-end.sh
├── Save metrics to .claude/metrics/
├── Update SESSION_HISTORY.md
├── Clean up temporary state
└── Report session summary
```

## Output

Each iteration produces:
```markdown
## Loop Iteration #N Summary

### Quality Gate Status
[Table of all gates with pass/fail]

### Work Completed
- [List of items fixed/implemented]

### Remaining Issues
- [Prioritized list]

### Next Iteration Plan
- [What will be attempted next]

### Time Elapsed: Xm Ys
### Estimated Remaining: ~N iterations
```

## Final Report

When loop completes:
```markdown
# Autonomous Loop Complete

## Summary
- Total iterations: 12
- Total time: 45 minutes
- Issues fixed: 23
- Tests added: 15
- Coverage: 72% → 91%

## Quality Gates - ALL PASSING
✅ Tests: 156 passing
✅ Coverage: 91%
✅ Security: 0 vulnerabilities
✅ Code Quality: A rating
✅ Documentation: Complete

## Changes Made
[Detailed list with file references]

## Recommendations
[Any remaining S3/optional improvements]
```

## Safety Guardrails

1. **No destructive operations without confirmation**
2. **Git commit after each successful iteration**
3. **Rollback capability if iteration fails**
4. **Max iterations prevent infinite loops**
5. **Stall detection (no progress = pause)**
6. **Resource limits respected**

---

## Integrated Skills

The autonomous loop coordinates with these skills:

| Skill | Role in Loop |
|-------|--------------|
| `task-orchestrator` | Classifies task, loads rules/agents at start |
| `definition-of-done` | Provides completion criteria in Phase 6 |
| `queue-manager` | Manages and visualizes work queue |
| `result-synthesizer` | Combines multi-agent findings |
| `browser-verification` | Verifies UI changes in Phase 4/5 |
| `smart-context` | Optimizes context loading |
| `session-memory` | Prevents redundant file reads |
| `context-budget-monitor` | Prevents context bloat, suggests sub-agents |
| `parallel-task-decomposer` | Breaks tasks into parallel work units |
| `decision-logger` | Captures decisions for traceability |
| `commit-checkpoint` | Creates verified commits for rollback |
| `evaluator-optimizer` | Feedback loops for quality gate failures |
| `queue-manager` | Query classification and work queue |

### Loop Startup Sequence

```
/loop "implement user authentication"
      │
      ▼
1. task-orchestrator analyzes task
   ├── Classifies: Security-Critical Feature
   ├── Loads: @rules/security, @rules/api-design, @rules/testing
   └── Suggests: security-analyst agent
      │
      ▼
2. Spawn recommended agents (if applicable)
   └── security-analyst reviews codebase
      │
      ▼
3. result-synthesizer combines findings
   └── Creates unified work queue
      │
      ▼
4. queue-manager initializes LOOP_STATE.md
      │
      ▼
5. Begin Phase 1: ASSESS
```

### Browser Verification Integration

For UI-related tasks:

```
Phase 4: TEST (extended for UI)
├── Run unit tests
├── Run integration tests
└── IF UI changes detected:
    └── browser-verification activates
        ├── Screenshot at viewports
        ├── Accessibility audit
        ├── Form testing (if forms)
        └── Report visual issues

Phase 5: QUALITY (extended for UI)
├── Standard quality gates
└── IF UI changes:
    ├── Visual regression check
    └── Add visual issues to queue
```

### Context Optimization

To prevent context exhaustion during long loops:

```
Every 5 iterations:
├── Summarize progress to LOOP_STATE.md
├── Clear completed item details from context
├── Keep only active work item context
└── Reference summaries instead of full content

When context > 70% utilized:
├── Offload analysis to forked agent
├── Agent returns summary only
└── Main context stays lean

For complex analysis:
├── Spawn specialized agent
├── Agent explores in isolation
├── Returns structured findings
└── Main loop continues with findings
```

---

## Reference

See `_system.md` for complete platform architecture and component relationships.
