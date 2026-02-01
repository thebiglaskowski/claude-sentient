---
name: orchestrator
version: 2.0.0
description: Minimal loop coordinator that executes phases in sequence
---

# Orchestrator

The orchestrator is the minimal core that coordinates phase execution. It delegates all logic to phases.

## Responsibilities

1. Execute phases in order
2. Emit lifecycle events
3. Track iteration count
4. Coordinate recovery

## NOT Responsibilities

- Classification (Phase 1)
- Context management (Phase 2)
- Quality checking (Phase 7)
- Recovery logic (Phase 10)

## Loop Algorithm

```
INITIALIZE:
  state = load_or_create_state()
  emit("session.started", { sessionId: state.sessionId })

LOOP:
  WHILE state.status != "complete":
    state.iteration++
    emit("loop.iteration.start", { iteration: state.iteration })

    FOR phase IN get_phases_in_order():
      IF phase.canSkip(state):
        emit("loop.phase.skipped", { phase: phase.name })
        CONTINUE

      TRY:
        emit("loop.phase.start", { phase: phase.name })
        result = phase.execute(state, context)
        state = merge(state, result.stateUpdates)
        emit("loop.phase.complete", { phase: phase.name, result })

        IF result.next:
          jump_to_phase(result.next)

      CATCH error:
        emit("loop.phase.error", { phase: phase.name, error })
        state.phase = "recover"
        break

    # Check completion after all phases
    IF check_completion(state):
      state.consecutivePasses++
      IF state.consecutivePasses >= 2:
        state.status = "complete"
        emit("loop.complete", { metrics: state.metrics })
    ELSE:
      state.consecutivePasses = 0

  save_state(state)
  emit("session.ended", { sessionId: state.sessionId, metrics: state.metrics })
```

## Phase Interface

Each phase must implement:

```typescript
interface Phase {
  name: string;
  order: number;

  canSkip(state: LoopState): { skip: boolean; reason?: string };

  execute(
    state: LoopState,
    context: ExecutionContext
  ): Promise<{
    stateUpdates: Partial<LoopState>;
    events: Event[];
    next?: string; // Jump to specific phase
  }>;
}
```

## Completion Check

```
check_completion(state):
  RETURN (
    all_gates_passed(state.gates) AND
    queue_empty(state.workQueue) AND
    no_blocked_tasks(state.workQueue) AND
    state.consecutivePasses >= 1
  )
```

## Event Flow

```
session.started
  │
  ▼
loop.iteration.start
  │
  ├── loop.phase.start (classify)
  ├── loop.phase.complete (classify)
  │
  ├── loop.phase.start (contextualize)
  ├── loop.phase.complete (contextualize)
  │
  ├── ... (other phases)
  │
  ├── loop.phase.start (evaluate)
  ├── loop.phase.complete (evaluate)
  │
  ▼
loop.iteration.complete
  │
  ├── (if not complete) → loop.iteration.start
  │
  ▼
loop.complete
  │
  ▼
session.ended
```

## Configuration

From resolved config:

```json
{
  "loop": {
    "maxIterations": 50,
    "consecutivePassesRequired": 2,
    "pauseOnSeverity": "S0"
  }
}
```
