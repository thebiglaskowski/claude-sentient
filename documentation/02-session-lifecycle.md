---
feature: Session Lifecycle
version: "1.0"
last_updated: 2026-03-04
dependencies: []
routes: []
status: draft
---

# Session Lifecycle

> Three hooks manage session bookkeeping: session-start (sync), session-end (async), and pre-compact (sync). Together they provide session continuity, archiving, and context summarization.

## Hook Overview

| Hook | Event | Sync | Purpose |
|------|-------|------|---------|
| `session-start.cjs` | SessionStart | sync | Initialize state, fix hook paths, detect profile |
| `session-end.cjs` | SessionEnd | async | Archive session, prune old archives |
| `pre-compact.cjs` | PreCompact | sync | Build structured session summary for continuity |

## session-start.cjs

Runs synchronously at every session start. Actions:

1. **Fix hook paths** (`fixHookPaths()`): If `settings.json` contains bare `node .claude/hooks/` references, replaces them with `process.execPath + absolutePath`. Prevents nvm FUNCNEST errors and MODULE_NOT_FOUND when Claude opens from a subdirectory.
2. **Ensure state dir**: Creates `.claude/state/` if missing (cached module-level flag after first call).
3. **Write session_start.json**: Captures `{sessionId, projectRoot, timestamp, profile}`.
4. **Profile detection**: Scans project files for profile signals (pyproject.toml, tsconfig.json, go.mod, Cargo.toml, etc.).

## session_start.json Shape

```json
{
  "sessionId": "uuid-v4",
  "projectRoot": "/absolute/path/to/project",
  "timestamp": "2026-03-04T00:00:00.000Z",
  "profile": "python"
}
```

Used by: `getProjectRoot()` fast-path in all hooks, cs-loop INIT profile loading.

## session-end.cjs

Runs async (fire-and-forget) at SessionEnd. Actions:

1. Load `session_start.json` to get sessionId and timestamp
2. Build archive entry: `{sessionId, projectRoot, profile, startedAt, endedAt, durationMs}`
3. Append to `archive/{sessionId}.json` (individual file per session)
4. Prune archive directory to `MAX_ARCHIVES` (100) — removes oldest entries via `pruneDirectory()`
5. Rotate `session.log` at `MAX_LOG_SIZE` (1MB)

## Archive Shape

```json
{
  "sessionId": "uuid",
  "projectRoot": "/path",
  "profile": "typescript",
  "startedAt": "2026-03-04T00:00:00.000Z",
  "endedAt": "2026-03-04T01:00:00.000Z",
  "durationMs": 3600000
}
```

Stored at: `.claude/state/archive/{sessionId}.json`

Worktree removal records are appended to this file by `worktree-lifecycle.cjs` when a worktree derived from this session is removed.

## pre-compact.cjs

Runs synchronously before context compaction. Builds a structured `compact-context.json` for session continuity:

### buildSessionSummary() Fields

| Field | Source | Purpose |
|-------|--------|---------|
| `sessionIntent` | current_task.json subject → session intent → profile name | What was being worked on |
| `filesModified` | file_changes.json (deduplicated) | Which files changed this session |
| `decisionsMade` | Unique topics from learnings written this session | Architecture decisions captured |
| `currentState` | TaskList status | Pending/in-progress/completed task counts |
| `nextSteps` | Incomplete tasks | What to resume after compaction |

### compact-context.json Shape

```json
{
  "sessionId": "uuid",
  "compactedAt": "2026-03-04T00:30:00.000Z",
  "sessionIntent": "Implement HTTP hooks modernization",
  "filesModified": [".claude/hooks/bash-validator.cjs"],
  "decisionsMade": ["hookSpecificOutput format migration"],
  "currentState": {"pending": 2, "inProgress": 1, "completed": 3},
  "nextSteps": ["Fix test assertions", "Update docs"]
}
```

cs-loop INIT reads this file at startup if it exists, restoring session context after compaction.

## State Directory Structure

```
.claude/state/
  session_start.json       # Written by session-start (every session)
  current_task.json        # Written by cs-loop EXECUTE
  compact-context.json     # Written by pre-compact
  file_changes.json        # Written by post-edit
  gate_history.json        # Written by gate-monitor
  team-state.json          # Written by teammate-idle/task-completed
  context_degradation.json # Written by context-injector
  config_changes.json      # Written by config-watcher (capped at 20)
  worktree-context.json    # Written by worktree-lifecycle (in worktree)
  gate-output/             # Large gate stdout (>8000 chars), pruned to 20 files
  archive/                 # Per-session archive files, pruned to 100
```

## Business Rules

- **Archive cap**: `MAX_ARCHIVES = 100` — oldest files pruned by mtime
- **Log rotation**: `session.log` rotated at `MAX_LOG_SIZE = 1MB`
- **fixHookPaths early-return**: Checks `content.includes('"node ')` to detect both relative paths and already-absolute paths that still use bare `node` binary
- **getProjectRoot() fast-path**: Reads `project_root` from `session_start.json` first; falls back to `git rev-parse --show-toplevel`
- **Hook self-protection**: file-validator blocks writes to `.claude/hooks/*.cjs` during active sessions
