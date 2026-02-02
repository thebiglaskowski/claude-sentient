# Intelligent Autonomous Loop Workflow (v3.1)

Complete end-to-end documentation of the `/loop` command with **meta-cognition** and **strict enforcement**.

---

## Quick Reference

```
/loop "implement user authentication"

┌─────────────────────────────────────────────────────────────────────────────┐
│                    INTELLIGENT /loop EXECUTION (v3.1)                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  START                                                                       │
│    │                                                                         │
│    ▼                                                                         │
│  ┌───────────────┐ ┌─────────┐ ┌───────────────┐ ┌─────────┐              │
│  │ CONTEXTUALIZE │→│ ASSESS  │→│META-COGNITION │→│  PLAN   │              │
│  └───────────────┘ └─────────┘ └───────────────┘ └─────────┘              │
│         │              (2.5: Choose best approach)        │                 │
│         │                                                 ▼                 │
│         │                              ┌─────────┐  ┌─────────┐            │
│         │                              │  BUILD  │→ │  TEST   │            │
│         │                              └─────────┘  └─────────┘            │
│         │                                                 │                 │
│         │                                                 ▼                 │
│         │              ┌──────────┐  ┌──────────┐  ┌─────────┐            │
│         │              │ EVALUATE │←─│ REASSESS │←─│ QUALITY │            │
│         │              └────┬─────┘  └──────────┘  └─────────┘            │
│         │                   │       (6.5: Pivot if stuck)                   │
│         │              ┌────┴────┐                                          │
│         │              │         │                                          │
│         │           PASS      FAIL                                          │
│         │              │         │                                          │
│         │              ▼         ▼                                          │
│         │         ┌───────┐ ┌─────────┐                                    │
│         │         │ DONE  │ │ RECOVER │                                    │
│         │         └───────┘ └────┬────┘                                    │
│         │                        │ (Smart recovery with capability inventory)│
│         └────────────────────────┘                                          │
│                                                                              │
│  15 QUALITY GATES (ALL BLOCKING - NO EXCEPTIONS):                           │
│  CODE:  PRE-FLIGHT → LINT → TYPE → UNIT → INTEGRATION → SECURITY →         │
│         PERFORMANCE → BROWSER → A11Y → DOCS → MODERN                        │
│  WORK:  WORK_QUEUE → KNOWN_ISSUES → GIT_STATE → DOD                        │
│                                                                              │
│  Loop CANNOT exit until ALL gates pass. Strict enforcement.                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Complete Execution Flow

### 1. Command Invocation

```
User: /loop "implement user authentication"
      │
      ▼
Arguments parsed:
├── Task: "implement user authentication"
├── --max-iterations: 50 (default)
├── --pause-on: S0 (default)
├── --parallel: false (default)
└── --dry-run: false (default)
```

---

### 2. Phase 1: CONTEXTUALIZE

**Purpose:** Load relevant context for the task

**Hooks Fired:**
- `UserPromptSubmit` → `context-injector.py`

**Actions:**
```
1. context-injector.py analyzes "implement user authentication"
   ├── Keywords detected: "auth", "user"
   ├── Paths suggested: src/auth/, middleware/auth
   ├── Rules suggested: @rules/security, @rules/api-design
   └── Agents suggested: security-analyst

2. task-orchestrator skill classifies task
   ├── Task type: Feature Development (Security-Critical)
   ├── Loads: @rules/security, @rules/testing, @rules/api-design
   └── Recommends: security-analyst agent

3. smart-context-v3 loads files
   ├── Checks existing auth files
   ├── Loads user model/schema
   └── Loads environment config

4. LOOP_STATE.md initialized
   ├── Current Iteration: 1
   ├── Status: IN_PROGRESS
   └── Work Queue: [initial task]
```

**Output:**
```
[Context] Relevant paths: src/auth/, middleware/auth | Rules: @rules/security | Agents: security-analyst

Task Type: Feature Development (Security-Critical)
Loading rules: @rules/security, @rules/api-design, @rules/testing
```

---

### 3. Phase 2: ASSESS

**Purpose:** Understand current state and spawn initial agents

**Hooks Fired:**
- `SubagentStart` → `agent-tracker.py` (if agents spawned)
- `SubagentStop` → `agent-synthesizer.py` (when agents complete)

**Actions:**
```
1. Run /assess to check codebase health
   ├── Existing issues by severity
   ├── Test coverage gaps
   ├── Security vulnerabilities
   └── Tech debt items

2. If --parallel or security-critical:
   ├── Spawn security-analyst
   ├── agent-tracker.py registers agent
   ├── Agent performs analysis
   ├── agent-synthesizer.py merges results
   └── Findings added to work queue

3. Build initial work queue
   ├── [S1] Implement auth endpoints
   ├── [S1] Add session management
   ├── [S2] Create auth middleware
   └── [S2] Write auth tests
```

**LOOP_STATE.md Updated:**
```markdown
## Current Iteration: 1
## Status: ASSESSING

## Work Queue
| Priority | Item | Status |
|----------|------|--------|
| S1 | Implement auth endpoints | ⏳ Pending |
| S1 | Add session management | ⏳ Pending |
| S2 | Create auth middleware | ⏳ Pending |
```

---

### 3.5. Phase 2.5: META-COGNITION (Intelligence Layer)

**Purpose:** Consult capability inventory and choose best approach

**Actions:**
```
1. Load CAPABILITY_INVENTORY.md
   ├── Know all 35 commands available
   ├── Know all 15 agents available
   ├── Know all 13 rules available
   └── Know decision matrix (situation → best tool)

2. Evaluate current situation
   ├── What type of work is this?
   ├── What's the current state? (coverage, issues, blockers)
   ├── What's been tried before? (check LOOP_STATE.md)
   └── Are we making progress?

3. Select strategy from decision matrix
   ├── Coverage < 80% → Spawn test-engineer agent
   ├── Security concerns → Spawn security-analyst agent
   ├── UI work → Spawn ui-ux-expert agent
   ├── Stuck after 2 iterations → Spawn researcher agent
   └── Normal feature → Continue direct implementation

4. Load relevant rules
   └── @rules/security, @rules/testing, etc. based on task type

5. Document decision rationale in LOOP_STATE.md
```

**LOOP_STATE.md Updated:**
```markdown
## Approaches Tried (Meta-Cognition)
| Iteration | Approach | Result | Next Action |
|-----------|----------|--------|-------------|
| 1 | Direct implementation | Starting | Continue |

## Strategy Selected
- Primary: Direct implementation with security-analyst oversight
- Rules loaded: @rules/security, @rules/api-design
- Agents queued: security-analyst (will spawn for review)
- Rationale: Security-critical feature, standard approach first
```

---

### 4. Phase 3: PLAN

**Purpose:** Prioritize work and create execution plan

**Actions:**
```
1. Check for existing blueprint
   └── If exists, follow blueprint requirements

2. Prioritize work queue:
   Priority Order:
   ├── 1. S0 Critical (security, crashes)
   ├── 2. S1 High (major bugs, blockers)
   ├── 3. Test coverage gaps (<80%)
   ├── 4. S2 Medium
   ├── 5. Tech debt
   ├── 6. S3 Low
   └── 7. Modernization

3. User checkpoint (if direction needed):
   ├── "Multiple valid approaches exist"
   ├── "Breaking change required"
   └── Wait for user input
```

**Output:**
```
## Plan for Iteration 1

Working on: [S1] Implement auth endpoints

Approach:
1. Create /api/auth/login endpoint
2. Create /api/auth/logout endpoint
3. Add JWT token generation
4. Add session validation middleware
```

---

### 5. Phase 4: BUILD

**Purpose:** Implement changes

**Hooks Fired:**
- `PreToolUse` → `file-validator.py` (before writes)
- `PostToolUse` → `post-edit.sh` (after writes)
- `PostToolUseFailure` → `error-recovery.py` (on errors)

**Actions:**
```
1. For each item in priority order:
   ├── Implement fix/feature
   ├── Follow existing patterns
   ├── Use modern tech (check via context7)
   ├── Create/update tests
   └── Document changes

2. file-validator.py checks each write:
   ├── Not a protected file? ✓
   ├── No secrets in content? ✓
   └── Allow write

3. post-edit.sh formats after each write:
   └── [Post-Edit] Formatted: src/auth/login.ts

4. If error occurs:
   ├── error-recovery.py classifies error
   ├── Network error? → Retry with backoff
   ├── Syntax error? → Add to queue as S0
   └── Permission error? → Escalate to user
```

**LOOP_STATE.md Updated:**
```markdown
## Current Iteration: 1
## Status: BUILDING

## Work Queue
| Priority | Item | Status |
|----------|------|--------|
| S1 | Implement auth endpoints | 🔄 In Progress |
| S1 | Add session management | ⏳ Pending |
```

---

### 6. Phase 5: TEST

**Purpose:** Run comprehensive testing

**Quality Gates Run:**
- GATE 2: LINT
- GATE 3: TYPE
- GATE 4: UNIT TEST
- GATE 5: INTEGRATION
- GATE 8: BROWSER (if UI)

**Actions:**
```
1. Run unit tests
   ├── npm test (or pytest, etc.)
   ├── Target: 90%+ coverage on new code
   └── Result: 45 tests, 88% coverage

2. Run type checking
   ├── tsc --noEmit
   └── Result: 0 errors

3. Run linting
   ├── eslint src/
   └── Result: 2 warnings

4. If UI changes detected:
   ├── browser-verification activates
   ├── Screenshots at viewports
   ├── Accessibility audit
   └── Form testing
```

**Output:**
```
## Test Results

✅ Unit Tests: 45 passing
✅ Type Check: 0 errors
⚠️ Lint: 2 warnings
✅ Coverage: 88% (target: 80%)
```

---

### 7. Phase 6: QUALITY

**Purpose:** Run all 15 quality gates (ALL BLOCKING)

**Quality Gates (Code Quality):**

| Gate | Check | Pass Criteria | Blocking |
|------|-------|---------------|----------|
| 1. PRE-FLIGHT | Environment, deps, git | Clean state | YES |
| 2. LINT | ESLint, Prettier | 0 errors, 0 warnings | YES |
| 3. TYPE | TypeScript strict | 0 errors | YES |
| 4. UNIT TEST | All tests pass, coverage | 100% pass, >= 80% | YES |
| 5. INTEGRATION | API tests | 100% pass | YES |
| 6. SECURITY | S0/S1 vulns, secrets | 0 S0, 0 S1 | YES |
| 7. PERFORMANCE | N+1, bundle, CWV | Within limits | YES |
| 8. BROWSER | Visual, responsive | Pass | YES (if UI) |
| 9. ACCESSIBILITY | axe-core, keyboard | Pass | YES (if UI) |
| 10. DOCUMENTATION | CHANGELOG, README | Present | YES |
| 11. MODERN TECH | Deprecated APIs | None | YES |

**Quality Gates (Work Completion):**

| Gate | Check | Pass Criteria | Blocking |
|------|-------|---------------|----------|
| 12. WORK QUEUE | Pending/in-progress tasks | 0 | YES |
| 13. KNOWN ISSUES | Unresolved S0/S1 | 0 | YES |
| 14. GIT STATE | Uncommitted changes | 0 | YES |
| 15. DOD | dod-verifier.py | Exit code 0 | YES |

**STRICT ENFORCEMENT:**
```
ALL gates are blocking. NO exceptions. NO warnings.
If ANY gate fails → Loop CANNOT exit.
```

---

### 7.5. Phase 6.5: REASSESS (Pivot Check)

**Purpose:** Check if approach is working, pivot if stuck

**Trigger Conditions:**
```
Reassess triggers if ANY of these are true:
├── Same gate failed 3+ times
├── No improvement for 2 iterations
├── Coverage not increasing
├── Issues count not decreasing
├── Error recovery failed
└── User requested reassessment
```

**Actions (if triggered):**
```
1. Analyze current state
   ├── What was the goal?
   ├── What approach was taken?
   ├── Where are we stuck?
   └── Why isn't it working?

2. Consult CAPABILITY_INVENTORY.md
   ├── What other tools could address this?
   ├── Is there a specialist agent for this problem?
   ├── Is there a rule with specific guidance?
   └── Can we break the problem down differently?

3. Select new strategy
   ├── Choose alternative from decision matrix
   ├── Spawn specialist agent if not already tried
   ├── Load additional rules for guidance
   └── If truly stuck → Ask user (last resort)

4. Log and pivot
   ├── Document current approach result in LOOP_STATE.md
   ├── Document new strategy selection
   ├── Reset stuck counter
   └── Return to CONTEXTUALIZE with fresh strategy
```

**Example Pivot:**
```
Coverage stuck at 50% after 3 iterations:
├── Previous approach: Direct test writing
├── Issue: Complex untested code, unclear behavior
├── New approach: Spawn test-engineer agent
├── Rationale: Specialist can generate comprehensive suite
└── Result: Coverage improved to 80% in next 2 iterations
```

**LOOP_STATE.md Updated (if pivot):**
```markdown
## Pivots Made
- **Iteration 4**: Pivoted from direct implementation to test-engineer agent
  - Reason: Coverage stuck at 50% for 3 iterations
  - Result: Immediate improvement
```

---

### 8. Phase 7: EVALUATE (STRICT ENFORCEMENT)

**Purpose:** Verify ALL thresholds met before exit

**Hooks Fired:**
- `Stop` → `dod-verifier.py` (STRICT verification)

**Actions:**
```
1. dod-verifier.py ACTUALLY RUNS checks:
   ├── Runs test suite, parses pass/fail counts
   ├── Runs coverage, parses percentage
   ├── Runs linter, counts errors/warnings
   ├── Runs type checker, counts errors
   ├── Runs security audit, counts vulnerabilities
   ├── Parses LOOP_STATE.md for pending work
   ├── Parses KNOWN_ISSUES.md for unresolved S0/S1
   ├── Runs git status for uncommitted changes
   └── Checks README.md and CHANGELOG.md exist

2. Check STRICT completion criteria:
   ALL MUST BE TRUE:
   ├── Coverage >= 80%? → ✅ 88%
   ├── Lint errors = 0? → ✅
   ├── Type errors = 0? → ✅
   ├── Security S0/S1 = 0? → ✅
   ├── Tests 100% pass? → ✅
   ├── Work queue empty? → ❌ 1 pending
   ├── Known issues S0/S1 = 0? → ✅
   ├── Git state clean? → ✅
   ├── Documentation exists? → ✅
   └── 2 consecutive passes? → ❌

   Result: EXIT CODE 1 (FAIL - loop continues)
```

**Decision:**
```
IF dod-verifier.py exit code = 0:
    → ALL thresholds met, go to DONE
ELSE (exit code = 1):
    → Thresholds NOT met, go to RECOVER
    → Loop CANNOT exit until ALL pass

NO WARNINGS. NO EXCEPTIONS. STRICT ENFORCEMENT.
```

---

### 9. Phase 8: RECOVER

**Purpose:** Handle failures and continue

**Hooks Fired:**
- `PostToolUseFailure` → `error-recovery.py` (if errors during recovery)

**Actions:**
```
1. Identify what failed:
   ├── Gate 10 (DOCUMENTATION): CHANGELOG not updated
   └── Gate 12 (DOD): Documentation requirement

2. Add recovery tasks to queue:
   └── [S2] Update CHANGELOG with auth feature

3. Reset pass counter:
   └── consecutive_passes = 0

4. Return to Phase 1 (CONTEXTUALIZE)
```

**LOOP_STATE.md Updated:**
```markdown
## Current Iteration: 2
## Status: RECOVERING

## Quality Gates
| Gate | Status | Last Check | Issues |
|------|--------|------------|--------|
| Tests | ✅ PASS | 10:45:00 | 0 |
| Docs | ⚠️ WARN | 10:45:00 | CHANGELOG |

## Work Queue
| Priority | Item | Status |
|----------|------|--------|
| S1 | Implement auth endpoints | ✅ Done |
| S2 | Update CHANGELOG | ⏳ Pending |
```

---

### 10. Loop Continuation

The loop repeats Phases 1-8 until exit conditions met:

**Iteration 2:**
```
Phase 1: CONTEXTUALIZE
  └── Reload context (minimal, focused on CHANGELOG)

Phase 2: ASSESS
  └── Only CHANGELOG update needed

Phase 3: PLAN
  └── Single task: Update CHANGELOG

Phase 4: BUILD
  └── Add CHANGELOG entry for auth feature

Phase 5: TEST
  └── All gates pass (CHANGELOG now updated)

Phase 6: QUALITY
  └── 12/12 gates passing ✅

Phase 7: EVALUATE
  └── Check DoD → PASS
  └── consecutive_passes = 1

Phase 8: (Skip - going to Iteration 3 for verification)
```

**Iteration 3 (Verification):**
```
Phase 1-6: Re-run all checks

Phase 7: EVALUATE
  └── All gates still passing
  └── consecutive_passes = 2
  └── Work queue empty
  └── Result: COMPLETE → Go to DONE
```

---

### 11. DONE

**Final Actions:**
```
1. Generate final report
2. Update LOOP_STATE.md with COMPLETE status
3. Update STATUS.md
4. Commit checkpoint (if configured)
```

**Final Report:**
```markdown
# Autonomous Loop Complete

## Summary
- Total iterations: 3
- Total time: 15 minutes
- Issues fixed: 4
- Tests added: 8
- Coverage: 72% → 88%

## Quality Gates - ALL PASSING
✅ Pre-flight: Clean environment
✅ Lint: 0 errors
✅ Type: 0 errors
✅ Tests: 53 passing
✅ Integration: Pass
✅ Security: 0 vulnerabilities
✅ Performance: Acceptable
⏭️ Browser: N/A
⏭️ Accessibility: N/A
✅ Documentation: Complete
✅ Modern Tech: Current
✅ Definition of Done: Complete

## Changes Made
- Created src/auth/login.ts
- Created src/auth/logout.ts
- Created src/middleware/auth.ts
- Updated src/api/routes.ts
- Added 8 new tests
- Updated CHANGELOG.md

## Recommendations
- Consider adding rate limiting (S3)
- Consider adding OAuth support (S3)
```

---

## Exit Conditions

### Success Exit
```
All 12 quality gates pass for 2 consecutive iterations
AND no pending work items
AND Definition of Done checklist complete
AND verification iteration confirms stability
```

### Forced Exit
```
--max-iterations reached (default: 50)
OR user types "stop loop" / "pause"
OR unrecoverable error (RECOVER phase escalates)
OR loop detects no progress (same issues 3 iterations)
```

---

## User Checkpoints

The loop PAUSES for user input when:

| Situation | Example |
|-----------|---------|
| Direction needed | "Multiple valid approaches - which one?" |
| S0 Critical decision | "Security issue - confirm fix approach?" |
| Resource question | "Need to add dependency - approve?" |
| Breaking change | "This will break existing API - proceed?" |
| Explicit request | User said "ask before X" |

---

## Work Queue Management

### Priority Order
```
1. S0 Critical (security, crashes) → Top of queue
2. S1 High (major bugs, blockers) → After S0
3. Blocking dependencies → After S1
4. S2 Medium → Middle
5. Test coverage gaps → Middle
6. S3 Low → Bottom
7. Enhancements/modernization → Bottom
```

### Dynamic Queue Updates
```
During any phase, new work is discovered:

Fixing bug A reveals bug B → Add B to queue
Security fix needs tests → Add tests to queue
Agent finds new issues → Add to queue
User requests feature → Add to queue
```

---

## Hook Integration Summary

| Phase | Hooks Fired |
|-------|-------------|
| CONTEXTUALIZE | UserPromptSubmit (context-injector) |
| ASSESS | SubagentStart (agent-tracker), SubagentStop (agent-synthesizer) |
| PLAN | (none) |
| BUILD | PreToolUse (file-validator), PostToolUse (post-edit), PostToolUseFailure (error-recovery) |
| TEST | (none) |
| QUALITY | (none) |
| EVALUATE | Stop (dod-verifier) |
| RECOVER | PostToolUseFailure (error-recovery) |

---

## Configuration

### settings.json Options
```json
{
  "hooks": {
    "UserPromptSubmit": [...],
    "PreToolUse": [...],
    "PostToolUse": [...],
    "PostToolUseFailure": [...],
    "SubagentStart": [...],
    "SubagentStop": [...],
    "Stop": [...]
  }
}
```

### Loop Arguments
```
/loop "task" [options]

Options:
  --max-iterations=N    Maximum iterations (default: 50)
  --pause-on=S0|S1      Pause for severity level (default: S0)
  --parallel            Enable parallel agents
  --modern              Force modern tech check
  --dry-run             Preview without executing
  --confirm             Require user confirmation at end
```

---

## Troubleshooting

### Loop Not Starting
- Check if LOOP_STATE.md exists (might resume old loop)
- Run `/loop --reset` to start fresh

### Loop Stuck
- Check for unresolvable S0 issues
- Check if waiting for user input
- Check --max-iterations limit

### Gates Always Failing
- Run individual gate command to diagnose
- Check if tools (eslint, tsc, etc.) are installed
- Verify test configuration

### Agents Not Spawning
- Check agent-tracker.py for errors
- Verify agent files exist in .claude/agents/
- Check settings.json SubagentStart hooks
