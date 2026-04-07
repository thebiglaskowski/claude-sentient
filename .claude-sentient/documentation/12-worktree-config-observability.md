---
feature: Worktree & Config Observability
version: "1.0"
last_updated: 2026-03-04
dependencies:
  - "02-session-lifecycle.md"
routes: []
status: draft
---

# Worktree & Config Observability

> Two lightweight async hooks that provide observability into git worktree lifecycles and settings changes. `worktree-lifecycle.cjs` bootstraps new worktrees with session context; `config-watcher.cjs` logs every Claude Code settings change.

## worktree-lifecycle.cjs

Handles both `WorktreeCreate` and `WorktreeRemove` events. Async (fire-and-forget).

### WorktreeCreate

When a new git worktree is created, the hook writes a context file into the worktree's `.claude/state/` directory so `/cs-sessions` can show lineage and the worktree inherits profile detection.

**Output file**: `{worktreePath}/.claude/state/worktree-context.json`

**Shape:**

```json
{
  "worktreePath": "/path/to/worktree",
  "parentSessionId": "session-uuid",
  "parentProjectRoot": "/path/to/project",
  "profile": "typescript",
  "createdAt": "2026-03-04T10:00:00.000Z"
}
```

| Field | Source |
|-------|--------|
| `worktreePath` | `tool_input.worktreePath` from hook input |
| `parentSessionId` | `session_start.json`.sessionId |
| `parentProjectRoot` | `getProjectRoot()` |
| `profile` | `session_start.json`.profile (may be null) |
| `createdAt` | `new Date().toISOString()` |

**Procedure:**
1. Parse hook input (`tool_input.worktreePath`, `tool_input.branchName`)
2. Read `session_start.json` for parent session metadata
3. Ensure `{worktreePath}/.claude/state/` directory exists (create if needed)
4. Write `worktree-context.json` to worktree state dir

### WorktreeRemove

When a worktree is removed, the hook records the removal in the parent session's archive entry.

**Procedure:**
1. Parse hook input (`tool_input.worktreePath`)
2. Read `{worktreePath}/.claude/state/worktree-context.json` for lineage data
3. Load parent session archive at `archive/{parentSessionId}.json`
4. Append removal record: `{ worktreePath, removedAt, durationMs }`
5. Write updated archive

**durationMs calculation**: `Date.now() - new Date(worktreeContext.createdAt).getTime()`

If `worktree-context.json` doesn't exist (e.g., pre-hook worktree), the hook exits gracefully without error.

## config-watcher.cjs

Handles `ConfigChange` events. Async (fire-and-forget).

### What It Tracks

Every change to Claude Code settings (`.claude/settings.json`, `~/.claude/settings.json`, etc.) is logged as an entry in `config_changes.json`.

**State file**: `.claude/state/config_changes.json`

**Entry shape:**

```json
{
  "changedFile": ".claude/settings.json",
  "changeType": "hooks",
  "timestamp": "2026-03-04T10:00:00.000Z",
  "sessionId": "session-uuid"
}
```

**Cap**: `MAX_CONFIG_CHANGES = 20` (oldest entries pruned via `appendCapped()`)

### Hooks Section Alert

If the changed file is `settings.json` AND the `changeType` is `hooks`, the hook outputs a context string to Claude's conversation:

```json
{
  "context": "Settings change detected: hooks section of settings.json was modified. If hooks are behaving unexpectedly, this change may be the cause. Review .claude/state/config_changes.json for history."
}
```

This surfaces hook configuration changes that might explain unexpected hook behavior in the current session.

### Procedure

1. Parse hook input (`changedFile`, `changeType`)
2. Build log entry with timestamp and current sessionId
3. `appendCapped('config_changes.json', entry, MAX_CONFIG_CHANGES, [])`
4. If `changedFile.includes('settings.json') && changeType === 'hooks'`: output context JSON
5. Exit 0

## Settings Configuration

Both hooks are registered in `templates/settings.json` as async:

```json
"WorktreeCreate": [{ "hooks": [{ "type": "command", "command": "node .claude/hooks/worktree-lifecycle.cjs", "timeout": 3000, "async": true }] }],
"WorktreeRemove": [{ "hooks": [{ "type": "command", "command": "node .claude/hooks/worktree-lifecycle.cjs", "timeout": 3000, "async": true }] }],
"ConfigChange":   [{ "hooks": [{ "type": "command", "command": "node .claude/hooks/config-watcher.cjs",    "timeout": 2000, "async": true }] }]
```

The same `worktree-lifecycle.cjs` script handles both WorktreeCreate and WorktreeRemove — it branches on the event type from hook input.

## Business Rules

- **Async hooks**: Both are fire-and-forget. Claude Code continues immediately; results deliver on the next turn if any context is output.
- **Non-blocking on missing data**: WorktreeRemove gracefully handles missing `worktree-context.json` (pre-hook worktrees).
- **Config changes capped at 20**: Rolling log. Oldest pruned automatically.
- **Hooks-section alert is context-only**: The output is informational, not a permission decision. Hook exits 0 unconditionally.
- **Parent archive update**: WorktreeRemove updates the parent session's archive entry, not a separate file — keeps lineage collocated with the session record.

## State Files

| File | Written By | Contents |
|------|-----------|---------|
| `{worktree}/.claude/state/worktree-context.json` | WorktreeCreate | Worktree lineage (parent session, profile) |
| `.claude/state/config_changes.json` | ConfigChange | Rolling log of settings changes (cap 20) |
| `archive/{sessionId}.json` | WorktreeRemove | Appended worktree removal record |

## Edge Cases

- **WorktreeCreate with no session_start.json**: `parentSessionId` and `profile` will be null. File still written with nulls — no crash.
- **WorktreeRemove before WorktreeCreate hook ran**: `worktree-context.json` missing. Hook reads, gets null, skips archive update, exits 0.
- **Multiple worktrees from same session**: Each gets its own `worktree-context.json`. Archive entries are appended (not overwritten) per removal.
- **Config change for non-hooks section**: Entry logged to `config_changes.json` but no context output.
- **Timeout**: Both hooks have short timeouts (2-3s). If the file write takes longer (slow disk), hook is killed but Claude Code continues unaffected (async).
