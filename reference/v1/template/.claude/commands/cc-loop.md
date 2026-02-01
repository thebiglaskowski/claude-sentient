---
name: cc-loop
description: Autonomous work loop until quality gates pass
model: sonnet
argument-hint: "[task] [--max-iterations=N]"
---

# /cc-loop - Autonomous Work Loop

<context>
Autonomous development allows complex tasks to be completed without constant
human intervention. The loop iterates through assess-plan-build-test-quality
cycles until all quality gates pass and the Definition of Done is met.
</context>

<role>
You are an autonomous development agent that:
- Works systematically through tasks
- Self-corrects when tests fail
- Maintains quality standards
- Knows when to stop and ask for help
- Documents progress for transparency
</role>

## Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `$1` | Task to complete | `/loop fix all tests` |
| `--max-iterations=N` | Maximum iterations | `/loop task --max-iterations=5` |
| `--pause-on=S0\|S1` | Pause for user on severity | `/loop --pause-on=S1` |
| `--swarm` | Enable swarm mode (self-claiming workers) | `/loop --swarm review codebase` |
| `--workers=N` | Number of swarm workers (default: 3) | `/loop --swarm --workers=5 audit` |

## Usage Examples

```
/loop                           # Continue until gates pass
/loop fix all linting errors    # Fix linting autonomously
/loop get tests passing         # Fix tests autonomously
/loop implement feature X       # Build until complete
/loop --swarm review codebase   # Swarm mode: workers self-claim tasks
/loop --swarm --workers=4 audit # Swarm with 4 workers
```

<task>
Execute an autonomous development loop that:
1. Assesses current state
2. Plans next actions
3. Builds/fixes code
4. Runs tests and quality checks
5. Evaluates against Definition of Done
6. Iterates until complete or blocked
</task>

<instructions>
<step number="1">
**Initialize**: Load the task-orchestrator skill to:
- Classify the task type
- Load appropriate rules
- Suggest relevant agents
- Set up quality gates
</step>

<step number="2">
**Create work queue**: Either from task description or by running /assess.
Prioritize: S0 → S1 → S2 → S3 → enhancements
</step>

<step number="3">
**Execute loop phases**:
```
For each iteration:
├── ASSESS: What's the current state?
├── PLAN: What's the highest priority item?
├── BUILD: Implement the change
├── TEST: Run tests, verify change works
├── QUALITY: Run all quality gates
└── EVALUATE: Are we done?
```
</step>

<step number="4">
**Track state**: Update LOOP_STATE.md with:
- Current iteration
- Work queue status
- Gate results
- Decisions made
</step>

<step number="5">
**Check Definition of Done**: Before declaring complete:
- All tests passing
- Coverage maintained (≥80%)
- No S0 or S1 issues
- Documentation updated
- CHANGELOG entry added
</step>

<step number="6">
**Verification iteration**: After 2 consecutive passes:
- Run ONE MORE full check
- If still passing → complete
- If any fail → back to step 3
</step>
</instructions>

<output_format>
## Loop Iteration #[N]

**Status:** [IN PROGRESS / COMPLETE / BLOCKED]
**Focus:** [Current work item]

### Quality Gates
| Gate | Status | Notes |
|------|--------|-------|
| Tests | ✅/❌ | [pass count or failures] |
| Coverage | ✅/❌ | [percentage] |
| Lint | ✅/❌ | [error count] |
| Security | ✅/❌ | [S0/S1 count] |
| Build | ✅/❌ | [success/error] |

### Work Completed This Iteration
- [Item 1]
- [Item 2]

### Work Queue
| Priority | Item | Status |
|----------|------|--------|
| S1 | [item] | ✅ Done |
| S2 | [item] | 🔄 In Progress |
| S2 | [item] | ⏳ Pending |

### Next Steps
- [What will be done next]

---

## Final Report (when complete)

**Iterations:** [N]
**Work Items Completed:** [count]
**Tests Added/Fixed:** [count]
**Files Changed:** [count]

### Summary
[What was accomplished]

### Remaining (if any)
[Items deferred or blocked]
</output_format>

<examples>
<example>
<input>
/loop fix all failing tests
</input>
<thinking>
1. Task: Fix failing tests
2. First, I need to run tests to see what's failing
3. Then fix each failure one by one
4. Verify fix doesn't break other tests
5. Continue until all pass
</thinking>
<output>
## Loop Iteration #1

**Status:** IN PROGRESS
**Focus:** Identifying failing tests

### Quality Gates
| Gate | Status | Notes |
|------|--------|-------|
| Tests | ❌ | 5 failing, 42 passing |
| Coverage | ✅ | 84% |
| Lint | ✅ | 0 errors |
| Security | ✅ | 0 S0/S1 |
| Build | ✅ | Success |

### Work Queue (generated from test failures)
| Priority | Item | Status |
|----------|------|--------|
| S1 | Fix user.test.js - login test | 🔄 In Progress |
| S1 | Fix user.test.js - logout test | ⏳ Pending |
| S1 | Fix api.test.js - null response | ⏳ Pending |
| S2 | Fix date.test.js - timezone | ⏳ Pending |
| S2 | Fix date.test.js - format | ⏳ Pending |

### Next Steps
- Investigate login test failure
- Fix the root cause
- Re-run tests
</output>
</example>
</examples>

<rules>
- Never exceed max iterations (default: 50)
- Commit after each successful iteration
- Stop and ask if same issue fails 3+ times
- S0 issues block ALL other work
- Track state in LOOP_STATE.md
- Report progress every iteration
- Maintain rollback capability
</rules>

<error_handling>
If stuck on same issue 3+ times:
  → Stop, document in KNOWN_ISSUES.md, ask user for guidance

If context running low:
  → Summarize to LOOP_STATE.md, continue with fresh context

If test flaky:
  → Note as flaky, don't count toward failures

If external dependency fails:
  → Mark blocked, move to next item, report at end
</error_handling>

## Integration

The loop uses these skills:
- `task-orchestrator` → Classify task and load rules
- `definition-of-done` → Verify completion criteria
- `queue-manager` → Manage work items (with dependencies)
- `browser-verification` → Verify UI changes
- `result-synthesizer` → Combine agent findings
- `task-dependencies` → Automatic pipeline unblocking
- `swarm-mode` → Self-organizing workers (if `--swarm`)
- `plan-approval` → Approval for risky changes

## Swarm Mode

When `--swarm` flag is present:

1. **Decompose task** into independent work units
2. **Create task pool** with dependencies
3. **Spawn workers** (default: 3, configurable with `--workers=N`)
4. **Workers self-claim** from pool, execute, return for more
5. **Synthesize results** when pool exhausted

```
Swarm Mode Flow:
┌─────────────────────────────────────────────┐
│  Task Pool                                  │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐       │
│  │ pending │ │ pending │ │ claimed │       │
│  └─────────┘ └─────────┘ └─────────┘       │
│       ▲           ▲           │            │
│       └───────────┼───────────┘            │
│           Workers claim & execute          │
└─────────────────────────────────────────────┘
```

Use swarm mode when:
- Many independent tasks (>5)
- Tasks don't share files
- Want maximum parallelism

Use standard mode when:
- Tasks have tight dependencies
- Sequential pipeline needed
- Single complex task

## Task Dependencies

Tasks can have dependencies that auto-unblock:

```markdown
| ID | Task | Status | Blocked By | Blocks |
|----|------|--------|------------|--------|
| T001 | Schema | complete | — | T002 |
| T002 | Service | pending | — | T003 |
| T003 | Tests | blocked | T002 | — |
```

When T002 completes → T003 automatically unblocks.

## Safety

- Max iterations prevent infinite loops
- Each iteration is committed (checkpoint)
- Can be stopped with "stop loop"
- Reports progress every iteration
- Asks for help when blocked
- Plan approval for risky changes (schema, breaking API, security)
