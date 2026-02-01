# Swarm Orchestration Architecture v1.0

> Unified multi-agent coordination with task dependencies, self-organizing workers, and intelligent collaboration.

## Overview

This document describes the **Swarm Orchestration** layer that enhances claude-conductor with:

1. **Task Dependencies** - Automatic pipeline unblocking with `blockedBy`/`blocks`
2. **Swarm Mode** - Self-organizing workers that claim tasks from a shared pool
3. **Plan Approval** - Leader approval workflow before risky actions
4. **Visible Backends** - Optional tmux/terminal visibility for debugging
5. **Inter-Agent Messaging** - Lightweight coordination between workers

These features are **opt-in** and **backwards compatible** with existing workflows.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     CLAUDE-CONDUCTOR SWARM ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                        ORCHESTRATION LAYER                             │  │
│  │  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐  ┌────────────┐  │  │
│  │  │    task-    │  │    meta-     │  │  autonomous │  │   swarm-   │  │  │
│  │  │ orchestrator│─▶│  cognition   │─▶│    loop     │─▶│    mode    │  │  │
│  │  └─────────────┘  └──────────────┘  └─────────────┘  └────────────┘  │  │
│  │         │                │                 │               │          │  │
│  │         ▼                ▼                 ▼               ▼          │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐ │  │
│  │  │                      TASK POOL (Enhanced)                        │ │  │
│  │  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐            │ │  │
│  │  │  │ Task 1  │  │ Task 2  │  │ Task 3  │  │ Task 4  │            │ │  │
│  │  │  │ pending │  │ blocked │  │ claimed │  │ pending │            │ │  │
│  │  │  │         │  │ by: [1] │  │ by: W1  │  │         │            │ │  │
│  │  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘            │ │  │
│  │  │         │           ▲           │                               │ │  │
│  │  │         │    auto-unblock       │                               │ │  │
│  │  │         └───────────────────────┘                               │ │  │
│  │  └─────────────────────────────────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                    │                                         │
│                                    ▼                                         │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                          WORKER LAYER                                  │  │
│  │                                                                        │  │
│  │   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐      │  │
│  │   │ Worker 1 │    │ Worker 2 │    │ Worker 3 │    │ Worker 4 │      │  │
│  │   │ security │    │  code-   │    │  test-   │    │  docs-   │      │  │
│  │   │ analyst  │    │ reviewer │    │ engineer │    │  writer  │      │  │
│  │   └────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘      │  │
│  │        │               │               │               │             │  │
│  │        └───────────────┴───────────────┴───────────────┘             │  │
│  │                                │                                      │  │
│  │                                ▼                                      │  │
│  │                    ┌───────────────────────┐                         │  │
│  │                    │    Message Board      │                         │  │
│  │                    │  (Inter-Agent Comms)  │                         │  │
│  │                    └───────────────────────┘                         │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                    │                                         │
│                                    ▼                                         │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                        SYNTHESIS LAYER                                 │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                │  │
│  │  │   result-    │  │    plan-     │  │   unified    │                │  │
│  │  │  synthesizer │  │   approval   │  │ work queue   │                │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘                │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Component Integration

### How Components Work Together

| Component | Existing? | Enhancement | Integration Point |
|-----------|-----------|-------------|-------------------|
| `queue-manager` | Yes | Add `blockedBy`/`blocks` | LOOP_STATE.md |
| `parallel-agents` | Yes | Add swarm claiming | Agent spawning |
| `result-synthesizer` | Yes | Handle swarm results | Synthesis phase |
| `meta-cognition` | Yes | Know about swarm mode | Decision matrix |
| `swarm-mode` | **NEW** | Self-organizing workers | Loop phase 3 |
| `plan-approval` | **NEW** | Leader approval workflow | Build phase |
| `message-board` | **NEW** | Inter-agent coordination | Worker communication |

### State File Evolution

**LOOP_STATE.md** gains new sections:

```markdown
## Work Queue (Enhanced)

### Task Dependencies
| ID | Subject | Status | Blocked By | Blocks | Claimed By |
|----|---------|--------|------------|--------|------------|
| T001 | Implement auth | complete | — | T002, T003 | — |
| T002 | Add auth tests | pending | T001 | T004 | — |
| T003 | Auth middleware | in_progress | T001 | T004 | worker-1 |
| T004 | Integration tests | blocked | T002, T003 | — | — |

### Swarm State
| Worker | Type | Status | Current Task | Completed |
|--------|------|--------|--------------|-----------|
| worker-1 | security-analyst | busy | T003 | 2 |
| worker-2 | code-reviewer | idle | — | 3 |

### Message Board
[Messages appear here for inter-agent coordination]
```

---

## Feature Details

### 1. Task Dependencies

**Purpose:** Enable automatic pipeline unblocking when predecessor tasks complete.

**How it works:**
```
T001 completes → System checks "what does T001 block?"
               → T002, T003 have T001 in blockedBy
               → Remove T001 from their blockedBy lists
               → T002, T003 become unblocked (claimable)
```

**Integration:**
- Enhanced `queue-manager.md` handles dependency logic
- LOOP_STATE.md stores dependency relationships
- Existing severity ordering still applies within unblocked tasks

### 2. Swarm Mode

**Purpose:** Workers autonomously claim tasks instead of central assignment.

**How it works:**
```
1. Task pool contains pending tasks
2. Workers continuously check for claimable tasks
3. Worker claims task (marks as claimed, sets owner)
4. Worker completes task, marks complete
5. Worker looks for next task
6. Repeat until pool empty
```

**Integration:**
- New `swarm-mode.md` skill
- Works with existing `parallel-agents.md`
- Optional mode (can still use coordinator-assigned)

### 3. Plan Approval

**Purpose:** Require explicit approval before executing risky changes.

**How it works:**
```
1. Worker identifies risky action (schema change, breaking API, etc.)
2. Worker posts plan to approval queue
3. Leader (main orchestrator) reviews plan
4. Leader approves or rejects with feedback
5. Worker proceeds or revises based on response
```

**Integration:**
- New `plan-approval.md` skill
- Integrates with BUILD phase of autonomous loop
- Uses LOOP_STATE.md for approval queue

### 4. Visible Backends

**Purpose:** Debug multi-agent workflows by seeing agent output in terminal.

**Options:**
- `in-process` (default): Invisible, fastest
- `background`: Uses Task tool background mode, check with Read
- `verbose`: Logs to `.claude/logs/agents/`

**Integration:**
- Configuration in `.claude/settings.json`
- No code changes needed (leverages existing Task tool)

### 5. Inter-Agent Messaging

**Purpose:** Lightweight coordination without full inbox infrastructure.

**How it works:**
```
Message Board in LOOP_STATE.md:
- Workers can post findings to board
- Other workers can read board before starting
- No real-time communication (file-based)
- Leader synthesizes at end
```

**Integration:**
- Simple text section in LOOP_STATE.md
- No external files or complex infrastructure
- Works with existing file-based state management

---

## Migration Path

### From Current to Swarm-Enhanced

1. **No breaking changes** - All new features are additive
2. **Opt-in activation** - Use `--swarm` flag or explicit trigger
3. **Gradual adoption** - Can use dependencies without swarm mode
4. **Fallback available** - Can always revert to coordinator-assigned

### Enabling Features

| Feature | How to Enable |
|---------|---------------|
| Task dependencies | Just use `blockedBy: [T001]` in queue |
| Swarm mode | `/cc-loop --swarm` or "use swarm mode" |
| Plan approval | Automatic for risky actions, or "require approval for X" |
| Visible backends | Set `CLAUDE_SWARM_VERBOSE=true` or configure settings |
| Message board | Automatic when swarm mode active |

---

## Design Principles

### 1. File-Based State (Maintained)

All state remains in markdown files for:
- Human readability
- Git tracking
- Easy debugging
- No external dependencies

### 2. Backwards Compatibility

Existing workflows continue to work:
- `/cc-loop` without `--swarm` uses coordinator pattern
- Queue without dependencies uses severity ordering
- No swarm state = standard parallel agent behavior

### 3. Progressive Enhancement

Start simple, add complexity as needed:
```
Level 0: Single agent, sequential work
Level 1: Parallel agents, coordinator assigned
Level 2: Parallel agents with task dependencies
Level 3: Full swarm with self-claiming workers
```

### 4. Cohesive Integration

New components use existing:
- Hooks for lifecycle events
- LOOP_STATE.md for state
- Meta-cognition for decision making
- Result synthesizer for merging findings

---

## Files Modified/Created

### Modified (Enhancement)

| File | Change |
|------|--------|
| `skills/orchestration/queue-manager.md` | Add dependency support |
| `skills/orchestration/parallel-agents.md` | Add swarm mode option |
| `skills/orchestration/meta-cognition.md` | Know about swarm capabilities |
| `skills/orchestration/autonomous-loop.md` | Integrate swarm phases |

### Created (New)

| File | Purpose |
|------|---------|
| `SWARM_ARCHITECTURE.md` | This document |
| `skills/orchestration/swarm-mode.md` | Self-claiming worker behavior |
| `skills/orchestration/plan-approval.md` | Leader approval workflow |
| `skills/orchestration/task-dependencies.md` | Dependency management |

---

## Usage Examples

### Example 1: Pipeline with Dependencies

```
User: "Build user authentication with tests"

System creates task pool:
├── T001: Design auth schema (pending)
├── T002: Implement auth service (blockedBy: T001)
├── T003: Create auth endpoints (blockedBy: T002)
├── T004: Write unit tests (blockedBy: T002)
├── T005: Write integration tests (blockedBy: T003, T004)

Execution:
1. T001 executes (only unblocked task)
2. T001 completes → T002 unblocks
3. T002 executes
4. T002 completes → T003, T004 unblock (PARALLEL!)
5. T003, T004 execute in parallel
6. Both complete → T005 unblocks
7. T005 executes
8. Done
```

### Example 2: Swarm Code Review

```
User: "/cc-loop --swarm 'Review entire codebase'"

System creates task pool:
├── Review src/auth/** (pending)
├── Review src/api/** (pending)
├── Review src/database/** (pending)
├── Review src/utils/** (pending)
├── Security audit (pending)
├── Test coverage check (pending)

System spawns 3 workers:
├── worker-1 (code-reviewer)
├── worker-2 (code-reviewer)
├── worker-3 (security-analyst)

Execution (self-organizing):
├── worker-1 claims "Review src/auth/**"
├── worker-2 claims "Review src/api/**"
├── worker-3 claims "Security audit"
├── worker-1 finishes, claims "Review src/database/**"
├── worker-2 finishes, claims "Review src/utils/**"
├── worker-3 finishes, claims "Test coverage check"
├── All workers finish → Synthesis
└── Unified report generated
```

### Example 3: Plan Approval for Schema Change

```
Worker: "I need to add a 'sessions' table with foreign key to users."

System: Plan approval required for schema changes.

┌─────────────────────────────────────────┐
│ PLAN APPROVAL REQUEST                   │
├─────────────────────────────────────────┤
│ Worker: worker-1 (database-expert)      │
│ Action: Schema migration                │
│                                         │
│ Plan:                                   │
│ 1. Create sessions table                │
│ 2. Add FK to users(id)                  │
│ 3. Add indexes for lookup               │
│                                         │
│ Risk: Medium (new table, no data loss)  │
│                                         │
│ [Approve] [Reject] [Modify]             │
└─────────────────────────────────────────┘

Leader: [Approves]

Worker: Proceeds with migration.
```

---

## Next Steps

See individual skill files for detailed implementation:

1. `skills/orchestration/task-dependencies.md` - Dependency management
2. `skills/orchestration/swarm-mode.md` - Self-claiming workers
3. `skills/orchestration/plan-approval.md` - Approval workflow

---

## Summary

The Swarm Orchestration layer transforms claude-conductor from:

**Before:** Coordinator assigns tasks → Agents execute → Return results

**After:** Tasks have dependencies → Workers self-organize → Coordinate via message board → Require approval for risky actions → Return unified results

This enables more efficient parallel execution, automatic pipeline progression, and safer handling of risky operations—all while maintaining the cohesive, file-based, self-aware nature of the platform.
