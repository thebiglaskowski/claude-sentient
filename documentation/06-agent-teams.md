---
feature: Agent Teams
version: "1.0"
last_updated: 2026-03-04
dependencies:
  - "08-agent-roles.md"
routes: []
status: draft
---

# Agent Teams

> Parallel execution using Claude Code's experimental Agent Teams feature. Invoked via `/cs-team "task"` or auto-offered by cs-loop when team eligibility criteria pass.

## Components

| Component | Purpose |
|-----------|---------|
| `cs-team.md` | Command: create teams, spawn agents, monitor progress |
| `teammate-idle.cjs` | Hook: track idle teammates, cap at MAX_TEAMMATES=50 |
| `task-completed.cjs` | Hook: record task completions, update team-state.json |

## Team Eligibility (Auto-Offer from cs-loop)

All three signals must pass:
1. **Scope**: 3+ independent tasks in the plan
2. **Independence**: no overlapping file scopes between tasks
3. **Complexity**: more than a simple bug fix

Requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` environment variable set. If not set, cs-loop skips team mode offer silently.

## Team Config Location

```
~/.claude/teams/{team-name}/config.json     # Team members, agent IDs
~/.claude/tasks/{team-name}/                # Shared task list directory
```

### config.json Shape

```json
{
  "teamName": "my-team",
  "description": "Refactoring auth module",
  "members": [
    {
      "name": "backend",
      "agentId": "uuid",
      "agentType": "backend"
    },
    {
      "name": "tester",
      "agentId": "uuid",
      "agentType": "tester"
    }
  ]
}
```

**Always refer to teammates by `name`**, never by `agentId`. Names are used for `target_agent_id` in SendMessage and for TaskUpdate `owner` field.

## team-state.json Shape

Stored at `.claude/state/team-state.json`. Identical defaults required in both teammate-idle and task-completed hooks:

```json
{
  "teammates": {},
  "completed_tasks": [],
  "file_ownership": {}
}
```

| Field | Cap | Written By |
|-------|-----|-----------|
| `teammates` | MAX_TEAMMATES=50 | teammate-idle (idle events) |
| `completed_tasks` | MAX_COMPLETED_TASKS=100 | task-completed (task done events) |
| `file_ownership` | MAX_FILE_OWNERSHIP=200 | agent-tracker (spawn events) |

**Critical**: teammate-idle and task-completed must use identical default shapes. Mismatched defaults cause crashes when the wrong hook creates the file first.

## teammate-idle.cjs

Sync hook. Fires on TeammateIdle events.

1. Load or initialize `team-state.json`
2. Update `teammates[agentName] = {lastIdle: timestamp, agentType}`
3. Prune `teammates` to `MAX_TEAMMATES = 50` (removes oldest entries)
4. Write state
5. Exit 0 (no stdout — exit-code-only hook)

## task-completed.cjs

Sync hook. Fires on TaskCompleted events.

1. Load or initialize `team-state.json`
2. Append `{taskId, agentName, completedAt, subject}` to `completed_tasks`
3. Cap `completed_tasks` at `MAX_COMPLETED_TASKS = 100`
4. Write state
5. Exit 0 (no stdout — exit-code-only hook)

## agent-tracker.cjs (SubagentStart)

Async hook. Fires when a subagent spawns.

1. Parse agent type from spawn input
2. Fast-path: if type matches `KNOWN_ROLES` (implementer, reviewer, researcher, tester, architect, general-purpose) → skip YAML scan
3. Otherwise: scan `agents/*.yaml` to resolve role
4. Update `file_ownership` in `team-state.json`
5. Exit 0

Uses `__dirname`-based agents/ resolution (not `getProjectRoot()` — breaks test isolation).

## agent-synthesizer.cjs (SubagentStop)

Async hook. Fires when a subagent completes.

Records agent completion to state, persists results for team lead to synthesize. Fire-and-forget.

## Workflow

```
cs-team "refactor auth" (or cs-loop offers team mode)
  → TeamCreate (creates config.json + task dir)
  → TaskCreate for each work stream
  → Task(subagent_type="backend") × N spawns teammates
  → agent-tracker.cjs fires (SubagentStart) — tracks file ownership
  → Teammates claim tasks, work in parallel
  → teammate-idle.cjs fires as agents complete turns
  → task-completed.cjs fires as tasks finish
  → agent-synthesizer.cjs fires (SubagentStop) as agents complete
  → Team lead monitors, redirects scope drift
  → SendMessage(type="shutdown_request") to each teammate
  → TeamDelete after all shutdown_approved
```

## Quality Gate Enforcement

Agent quality gates are enforced via hooks. Each agent's `quality_gates` from `agents/*.yaml` define which gates must pass. Gates checked at TeammateIdle and TaskCompleted events.

## Business Rules

- **File partition required**: When parallelizing, partition file ownership carefully — edit conflicts on shared files cause errors (teammates must re-read before editing after another agent modifies)
- **Shutdown protocol**: Send `shutdown_request`, wait for `shutdown_approved`. `TeamDelete` fails if any members still active
- **Task ordering**: Prefer lowest-ID tasks first — earlier tasks set up context for later ones
- **No JSON status messages**: Teammates communicate via SendMessage plain text, not `{"type":"idle",...}` structs
- **Idle is normal**: Teammates go idle after every turn. Idle != unavailable. Sending a message to an idle teammate wakes them
