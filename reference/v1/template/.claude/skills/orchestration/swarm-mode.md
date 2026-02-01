---
name: swarm-mode
description: Self-organizing workers that autonomously claim and complete tasks from a shared pool
version: 1.0.0
triggers:
  - "swarm mode"
  - "self-organizing"
  - "workers claim"
  - "--swarm"
  - "spawn swarm"
model: sonnet
tags: [orchestration, swarm, parallel, autonomous, workers]
context: inherit
---

# Swarm Mode

Self-organizing workers that autonomously claim tasks from a shared pool, execute them, and return for more—no central coordinator needed.

---

## Overview

**Traditional (Coordinator Pattern):**
```
Coordinator assigns Task A to Worker 1
Coordinator assigns Task B to Worker 2
Workers execute
Workers return results
Coordinator assigns next tasks
```

**Swarm (Self-Organizing Pattern):**
```
Task pool contains Tasks A, B, C, D, E
Workers spawn and claim tasks autonomously
Workers complete, immediately claim next
No coordination bottleneck
Pool empties → Swarm completes
```

---

## When to Use Swarm Mode

### Ideal Scenarios

| Scenario | Why Swarm Works |
|----------|-----------------|
| Code review of many files | Each file is independent |
| Batch documentation | Each doc is independent |
| Multi-module testing | Modules can test in parallel |
| Large-scale audit | Many independent checks |
| Migration of many items | Each item independent |

### When NOT to Use

| Scenario | Why Not |
|----------|---------|
| Tight file dependencies | Workers might conflict |
| Sequential pipeline | Use dependencies instead |
| Single complex task | Single agent is better |
| High coordination needs | Use coordinator pattern |

---

## Swarm Architecture

### Components

```
┌─────────────────────────────────────────────────────────────────┐
│                        SWARM ARCHITECTURE                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                      TASK POOL                           │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐       │   │
│  │  │ pending │ │ pending │ │ claimed │ │ complete│       │   │
│  │  │         │ │         │ │ by: W1  │ │         │       │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                   │
│              ┌───────────────┼───────────────┐                  │
│              ▼               ▼               ▼                   │
│       ┌──────────┐    ┌──────────┐    ┌──────────┐             │
│       │ Worker 1 │    │ Worker 2 │    │ Worker 3 │             │
│       │ (busy)   │    │ (idle)   │    │ (busy)   │             │
│       │ Task: 3  │    │ claiming │    │ Task: 5  │             │
│       └──────────┘    └──────────┘    └──────────┘             │
│              │               │               │                   │
│              └───────────────┴───────────────┘                  │
│                              │                                   │
│                              ▼                                   │
│                    ┌──────────────────┐                         │
│                    │   Message Board  │                         │
│                    │  (coordination)  │                         │
│                    └──────────────────┘                         │
│                              │                                   │
│                              ▼                                   │
│                    ┌──────────────────┐                         │
│                    │   Synthesizer    │                         │
│                    └──────────────────┘                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Worker Lifecycle

```
SPAWN → CLAIM → EXECUTE → COMPLETE → CLAIM → ... → SHUTDOWN

1. SPAWN
   - Worker starts with agent type and ID
   - Registers in swarm state

2. CLAIM
   - Worker queries task pool
   - Finds highest-priority unblocked, unclaimed task
   - Atomically claims it (prevents double-claim)

3. EXECUTE
   - Worker performs the task
   - Can post to message board if needs to share info

4. COMPLETE
   - Worker marks task complete
   - Triggers dependency unblocking
   - Returns to CLAIM step

5. SHUTDOWN
   - No more claimable tasks
   - Worker posts final findings
   - Worker terminates
```

---

## Activating Swarm Mode

### Via Command

```
/cc-loop --swarm "Review the entire codebase"
```

### Via Natural Language

```
"Use swarm mode to audit all modules"
"Spawn a swarm of workers to review this"
"Have workers self-organize to complete these tasks"
```

### Via Configuration

```json
// .claude/settings.json
{
  "orchestration": {
    "swarmMode": {
      "enabled": true,
      "defaultWorkerCount": 3,
      "maxWorkerCount": 5,
      "workerTypes": ["code-reviewer", "security-analyst", "test-engineer"]
    }
  }
}
```

---

## Swarm State in LOOP_STATE.md

### Task Pool Section

```markdown
## Swarm State

### Mode
Active: Yes
Started: 2024-01-15T10:00:00Z

### Workers
| ID | Type | Model | Status | Current Task | Completed | Findings |
|----|------|-------|--------|--------------|-----------|----------|
| W1 | code-reviewer | sonnet | busy | T003 | 2 | 5 |
| W2 | security-analyst | opus | busy | T007 | 1 | 3 |
| W3 | test-engineer | sonnet | idle | claiming | 3 | 8 |

### Task Pool
| ID | Subject | Severity | Status | Blocked By | Claimed By |
|----|---------|----------|--------|------------|------------|
| T001 | Review auth.ts | S2 | complete | — | W1 |
| T002 | Review api.ts | S2 | complete | — | W2 |
| T003 | Review db.ts | S2 | in_progress | — | W1 |
| T004 | Review utils.ts | S2 | pending | — | — |
| T005 | Security audit auth | S1 | complete | — | W2 |
| T006 | Test auth coverage | S2 | complete | — | W3 |
| T007 | Security audit api | S1 | in_progress | — | W2 |
| T008 | Test api coverage | S2 | pending | T007 | — |

### Message Board
- [W2 10:05] Found SQL injection risk in api.ts:45, flagging for priority
- [W1 10:07] auth.ts clean, good patterns used
- [W3 10:10] Coverage at 65% for auth module, needs improvement
```

---

## Worker Behavior

### Claim Algorithm

```python
def claim_next_task(worker_id, task_pool):
    """
    Find and claim the highest priority available task.
    """
    claimable = [
        task for task in task_pool
        if task.status == 'pending'
        and task.claimed_by is None
        and not task.blocked_by  # No unresolved blockers
    ]

    if not claimable:
        return None  # No tasks available

    # Sort by: severity, then blocks_count (unblock others first)
    claimable.sort(key=lambda t: (
        severity_rank(t.severity),  # S0=0, S1=1, S2=2, S3=3
        -len(t.blocks)  # More blocks = higher priority
    ))

    task = claimable[0]
    task.claimed_by = worker_id
    task.status = 'in_progress'
    return task
```

### Double-Claim Prevention

Since state is file-based, prevent race conditions:

```markdown
## Claim Lock
Claiming: W3
Claim Time: 2024-01-15T10:12:00Z
Claim Timeout: 5 seconds

If claim lock exists and not expired:
  → Other workers wait before claiming
```

In practice with claude-conductor:
- Workers run sequentially or with coordination
- File-based state is updated atomically
- Minimal collision risk in normal operation

---

## Worker Types and Assignment

### Automatic Type Selection

```
Task: "Review src/auth/**"
→ Best worker: code-reviewer

Task: "Security audit of auth module"
→ Best worker: security-analyst

Task: "Check test coverage for auth"
→ Best worker: test-engineer

Task: "Document auth API"
→ Best worker: documentation-writer
```

### Heterogeneous Swarm

Different worker types for different tasks:

```
Spawn swarm:
├── 2x code-reviewer (for code review tasks)
├── 1x security-analyst (for security tasks)
└── 1x test-engineer (for test tasks)

Tasks auto-route to appropriate worker type
```

### Worker Model Selection

```yaml
# Worker type to model mapping
code-reviewer: sonnet      # Fast, good quality
security-analyst: opus     # Deep analysis needed
test-engineer: sonnet      # Fast, good coverage
documentation-writer: haiku  # Simple, fast
researcher: sonnet         # Research depth
```

---

## Message Board

### Purpose

Lightweight coordination without complex inbox infrastructure.

### Message Types

```markdown
### Message Board

#### Priority Alerts (Workers read these first)
- [W2 10:05] ALERT: SQL injection in api.ts:45, prioritize this file

#### Findings Share (For synthesis)
- [W1 10:07] auth.ts: 2 S2 issues (complexity, naming)
- [W2 10:08] api.ts: 1 S0 issue (SQL injection), 2 S2 issues

#### Info Exchange (Help other workers)
- [W3 10:10] FYI: auth tests need mocking setup in beforeEach
```

### Reading Messages

Workers should check message board before starting new task:

```
Worker W3 claims task "Test api module"
W3 reads message board:
  → Sees W2's SQL injection alert for api.ts
  → Adjusts test focus to include security tests
```

---

## Swarm Commands

### Start Swarm

```
"Start swarm with 3 workers for codebase review"
"/cc-loop --swarm --workers=3 'Audit the codebase'"
```

### Check Swarm Status

```
"Swarm status"
"How are the workers doing?"

Output:
═══════════════════════════════════════
SWARM STATUS
═══════════════════════════════════════
Active Workers: 3/3
Tasks: 12 total, 5 complete, 2 in-progress, 5 pending
Progress: ███████░░░░░ 42%

Workers:
├── W1 (code-reviewer): Completing T003 [60%]
├── W2 (security-analyst): Completing T007 [80%]
└── W3 (test-engineer): Claiming next task...

Recent Messages:
- [W2] Found critical issue in api.ts
- [W1] auth.ts clean

Estimated completion: ~5 minutes
═══════════════════════════════════════
```

### Add Task to Pool

```
"Add to swarm pool: Review src/payments/**"

Added: T009 - Review src/payments/**
Status: pending
Will be claimed by next available worker
```

### Stop Swarm

```
"Stop swarm gracefully"

Stopping swarm:
├── Waiting for in-progress tasks to complete...
├── W1 completed T003
├── W2 completed T007
├── No new claims allowed
├── Synthesizing results...
└── Swarm stopped. 7/12 tasks completed.
```

---

## Integration with Autonomous Loop

### Swarm-Enabled Loop Phases

```
┌─────────────────────────────────────────────────────────────────┐
│            AUTONOMOUS LOOP WITH SWARM MODE                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  CONTEXTUALIZE → ASSESS → META-COGNITION                        │
│                               │                                  │
│                   ┌───────────┴───────────┐                     │
│                   ▼                       ▼                      │
│            [Standard Mode]          [Swarm Mode]                │
│                   │                       │                      │
│                   ▼                       ▼                      │
│              PLAN (single)      DECOMPOSE + CREATE POOL         │
│                   │                       │                      │
│                   ▼                       ▼                      │
│              BUILD (self)         SPAWN WORKERS                 │
│                   │                       │                      │
│                   ▼                       ▼                      │
│               TEST              WORKERS CLAIM & EXECUTE          │
│                   │                       │                      │
│                   ▼                       ▼                      │
│              QUALITY             SYNTHESIZE RESULTS              │
│                   │                       │                      │
│                   ▼                       ▼                      │
│              EVALUATE ◄───────────────────┘                     │
│                   │                                              │
│                   ▼                                              │
│                 DONE                                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### When Loop Chooses Swarm Mode

Meta-cognition evaluates:

```
SWARM MODE DECISION:
├── Task has multiple independent units? → Consider swarm
├── Units can be assigned to different workers? → Consider swarm
├── Little shared state between units? → Consider swarm
├── > 5 independent tasks? → Swarm likely faster
│
├── Tasks have tight dependencies? → Use standard mode
├── All tasks touch same files? → Use standard mode
├── Sequential pipeline? → Use dependencies, not swarm
└── Single complex task? → Use single agent
```

---

## Synthesis

### When Swarm Completes

```
All tasks complete OR stop requested

SYNTHESIS PROCESS:
├── Collect all worker findings
├── Merge findings by severity
├── Deduplicate overlapping issues
├── Resolve conflicts (highest severity wins)
├── Generate unified report
└── Populate work queue for fixes
```

### Synthesis Output

```markdown
## Swarm Synthesis Report

### Summary
- Workers deployed: 3
- Tasks completed: 12
- Total findings: 23
- Duration: 8 minutes

### Findings by Severity
| Severity | Count | Source |
|----------|-------|--------|
| S0 | 1 | W2 (security-analyst) |
| S1 | 4 | W2 (2), W1 (2) |
| S2 | 12 | W1 (6), W3 (4), W2 (2) |
| S3 | 6 | W1 (4), W3 (2) |

### Critical Findings (S0-S1)
1. [S0] SQL injection in api.ts:45 (W2)
2. [S1] Missing auth check in payments.ts (W2)
3. [S1] Uncaught exception in utils.ts (W1)
...

### Work Queue (Ready for Fixes)
| ID | Finding | Severity | Source |
|----|---------|----------|--------|
| F001 | Fix SQL injection | S0 | W2 |
| F002 | Add auth check | S1 | W2 |
...
```

---

## Best Practices

### Do

- Use swarm for truly independent tasks
- Start with 3 workers, scale up if needed
- Let workers self-organize
- Check message board for coordination
- Trust the synthesis process

### Don't

- Use swarm for tightly coupled tasks
- Spawn more than 5 workers (diminishing returns)
- Manually assign tasks (defeats purpose)
- Ignore message board alerts
- Skip synthesis step

---

## Configuration Reference

```json
{
  "orchestration": {
    "swarmMode": {
      "enabled": true,
      "defaultWorkerCount": 3,
      "maxWorkerCount": 5,
      "workerTypes": {
        "default": ["code-reviewer"],
        "security": ["security-analyst"],
        "testing": ["test-engineer"],
        "docs": ["documentation-writer"]
      },
      "claimTimeout": 5000,
      "messageBoard": true,
      "synthesizeOnComplete": true,
      "verbose": false
    }
  }
}
```

---

## Summary

Swarm mode transforms multi-agent execution from:

**Coordinator Pattern:**
- Central assignment bottleneck
- Workers wait for instructions
- Sequential task distribution

**Swarm Pattern:**
- Self-organizing workers
- No coordination bottleneck
- Maximum parallelism
- Automatic load balancing

Use swarm mode when tasks are independent and numerous. Use standard mode when tasks are tightly coupled or sequential.
