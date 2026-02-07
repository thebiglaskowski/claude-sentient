# Hooks — Claude Sentient

> Context for working on hook scripts in `.claude/hooks/`.

## Hook Scripts (13 hooks)

| Script | Event | Purpose |
|--------|-------|---------|
| `session-start.js` | SessionStart | Initialize session, detect profile |
| `session-end.js` | SessionEnd | Archive session, cleanup state |
| `context-injector.js` | UserPromptSubmit | Detect topics, inject context |
| `bash-validator.js` | PreToolUse (Bash) | Block dangerous commands |
| `file-validator.js` | PreToolUse (Write/Edit) | Validate protected paths |
| `post-edit.js` | PostToolUse (Write/Edit) | Track changes, suggest lint |
| `agent-tracker.js` | SubagentStart | Track agent spawning |
| `agent-synthesizer.js` | SubagentStop | Synthesize agent results |
| `pre-compact.js` | PreCompact | Backup state before compaction |
| `dod-verifier.js` | Stop | Verify DoD, save final state |
| `teammate-idle.js` | TeammateIdle | Quality check before teammate goes idle |
| `task-completed.js` | TaskCompleted | Validate deliverables, file ownership |

All hooks use shared `utils.js` for JSON I/O, state management, and logging.

---

## Configuration

Hooks are configured in `.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [{ "hooks": [{ "type": "command", "command": "node .claude/hooks/session-start.js", "timeout": 5000 }] }],
    "PreToolUse": [
      { "matcher": "Bash", "hooks": [{ "type": "command", "command": "node .claude/hooks/bash-validator.js" }] },
      { "matcher": "Write|Edit", "hooks": [{ "type": "command", "command": "node .claude/hooks/file-validator.js" }] }
    ],
    "PostToolUse": [{ "matcher": "Write|Edit", "hooks": [{ "type": "command", "command": "node .claude/hooks/post-edit.js" }] }],
    "SubagentStart": [{ "hooks": [{ "type": "command", "command": "node .claude/hooks/agent-tracker.js" }] }],
    "SubagentStop": [{ "hooks": [{ "type": "command", "command": "node .claude/hooks/agent-synthesizer.js" }] }],
    "PreCompact": [{ "hooks": [{ "type": "command", "command": "node .claude/hooks/pre-compact.js" }] }],
    "Stop": [{ "hooks": [{ "type": "command", "command": "node .claude/hooks/dod-verifier.js" }] }],
    "SessionEnd": [{ "hooks": [{ "type": "command", "command": "node .claude/hooks/session-end.js" }] }],
    "TeammateIdle": [{ "hooks": [{ "type": "command", "command": "node .claude/hooks/teammate-idle.js" }] }],
    "TaskCompleted": [{ "hooks": [{ "type": "command", "command": "node .claude/hooks/task-completed.js" }] }]
  }
}
```

---

## Security Patterns

**Bash Validator** blocks dangerous patterns:
- `rm -rf /` or `rm -rf ~` — Recursive delete
- `> /dev/sd*` — Direct disk writes
- `mkfs` — Filesystem creation
- `chmod -R 777 /` — Dangerous permissions
- Fork bombs and reverse shells

**File Validator** protects sensitive paths:
- System directories (`/etc`, `/usr`, `C:\Windows`)
- SSH keys (`.ssh/`)
- Credentials (`.env.production`, `secrets.*`)
- Git internals (`.git/objects`)

---

## State Files

Hooks read/write to `.claude/state/`:

| File | Purpose |
|------|---------|
| `session_start.json` | Current session metadata |
| `file_changes.json` | Files modified this session |
| `active_agents.json` | Currently running subagents |
| `agent_history.json` | Completed subagent history |
| `prompts.json` | Recent prompt metadata |
| `last_verification.json` | Last DoD verification |
| `team-state.json` | Agent Teams: teammate tracking, file ownership |

---

## Agent Teams Hooks

**TeammateIdle** (`teammate-idle.js`):
- Checks if teammate has completed any tasks before going idle
- Exit code 0: allow idle. Exit code 2: send feedback (keep working)
- Tracks idle count per teammate

**TaskCompleted** (`task-completed.js`):
- Validates file count per task (max 20 files)
- Detects file ownership conflicts between teammates
- Maintains file ownership map to prevent overwrites
- Exit code 0: allow completion. Exit code 2: reject with feedback

---

## Hook Input/Output

Hooks receive input via `HOOK_INPUT` environment variable (JSON):

```javascript
const input = JSON.parse(process.env.HOOK_INPUT || '{}');
// input.tool_input - the tool's parameters
// input.tool_name - which tool triggered
```

Output JSON to stdout:

```javascript
// Block an operation
console.log(JSON.stringify({ decision: 'block', reason: 'Why' }));

// Allow with warnings
console.log(JSON.stringify({ decision: 'allow', warnings: ['Warning'] }));
```

---

## Shared Utilities (`utils.js`)

| Function | Purpose |
|----------|---------|
| `parseHookInput()` | Parse from HOOK_INPUT env var or stdin |
| `loadState(filename)` | Load from `.claude/state/` |
| `saveState(filename, data)` | Save to `.claude/state/` |
| `logMessage(msg, level)` | Append to `.claude/session.log` |
| `ensureStateDir()` | Create state directory if missing |

Named constants: `MAX_PROMPT_HISTORY` (50), `MAX_FILE_CHANGES` (100), `MAX_AGENT_HISTORY` (50).
