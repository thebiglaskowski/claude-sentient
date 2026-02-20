# Hooks — Claude Sentient

> Context for working on hook scripts in `.claude/hooks/`.

## Hook Scripts (13 hooks)

| Script | Event | Purpose |
|--------|-------|---------|
| `session-start.cjs` | SessionStart | Initialize session, detect profile |
| `session-end.cjs` | SessionEnd | Archive session, cleanup state |
| `context-injector.cjs` | UserPromptSubmit | Detect topics, inject context |
| `bash-validator.cjs` | PreToolUse (Bash) | Block dangerous commands |
| `file-validator.cjs` | PreToolUse (Write/Edit) | Validate protected paths |
| `post-edit.cjs` | PostToolUse (Write/Edit) | Track changes, suggest lint |
| `agent-tracker.cjs` | SubagentStart | Track agent spawning |
| `agent-synthesizer.cjs` | SubagentStop | Synthesize agent results |
| `pre-compact.cjs` | PreCompact | Backup state before compaction |
| `dod-verifier.cjs` | Stop | Verify DoD, save final state |
| `teammate-idle.cjs` | TeammateIdle | Quality check before teammate goes idle |
| `task-completed.cjs` | TaskCompleted | Validate deliverables, file ownership |
| `gate-monitor.cjs` | PostToolUse (Bash) | Record gate exit codes and durations |

All hooks use shared `utils.cjs` for JSON I/O, state management, and logging.

---

## Configuration

Hooks are configured in `.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [{ "hooks": [{ "type": "command", "command": "node .claude/hooks/session-start.cjs", "timeout": 5000 }] }],
    "PreToolUse": [
      { "matcher": "Bash", "hooks": [{ "type": "command", "command": "node .claude/hooks/bash-validator.cjs" }] },
      { "matcher": "Write|Edit", "hooks": [{ "type": "command", "command": "node .claude/hooks/file-validator.cjs" }] }
    ]
  }
}
```

> Hook commands use simple relative paths. Claude Code runs hooks from the project root directory, so `.claude/hooks/` resolves correctly. Each hook uses `getProjectRoot()` from `utils.cjs` internally for any file operations that need the project root path.
>
> **Important**: Do NOT use shell substitutions like `$(...)` in hook commands — Claude Code passes commands through `cmd.exe` on Windows, which does not interpret bash syntax. Keep commands as plain `node <path>` invocations.

---

## Security Patterns

**Bash Validator** blocks dangerous patterns:
- Any `rm` with combined `-r`/`-f` flags (any path — named dirs, `../` traversal, absolute)
- `> /dev/sd*` — Direct disk writes
- `mkfs` — Filesystem creation
- `chmod -R 777 /` — Dangerous permissions
- Fork bombs and reverse shells
- `curl|sh`, `wget|sh` — Supply-chain attacks (pipe-to-interpreter)
- `bash -c "$(curl ...)"` — Supply-chain bypass via command substitution
- `curl url > x.sh && bash x.sh` — Download-then-execute chains
- `base64 -d | sh` — Encoded command injection
- `eval` — Shell eval execution
- `sudo bash/sh`, `sudo su` — Privilege escalation
- `find / -exec rm` or `find|xargs rm` — Bulk deletion from root
- Python/Perl/Ruby/Node one-liners with dangerous imports
- Oversized `HOOK_INPUT` (>1MB) — fail-closed, blocks rather than allowing empty command through

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
| `gate_history.json` | Quality gate exit codes and durations |
| `compact-context.json` | State snapshot before context compaction |
| `team-state.json` | Agent Teams: teammate tracking, file ownership |

---

## Agent Teams Hooks

**TeammateIdle** (`teammate-idle.cjs`):
- Checks if teammate has completed any tasks before going idle
- Exit code 0: allow idle. Exit code 2: send feedback (keep working)
- Tracks idle count per teammate

**TaskCompleted** (`task-completed.cjs`):
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

## Shared Utilities (`utils.cjs`)

| Function | Purpose |
|----------|---------|
| `getProjectRoot()` | Resolve project root via git (cached per process) |
| `parseHookInput()` | Parse from HOOK_INPUT env var or stdin |
| `loadState(filename)` | Load from `.claude/state/` |
| `saveState(filename, data)` | Save to `.claude/state/` |
| `logMessage(msg, level)` | Append to `.claude/session.log` |
| `ensureStateDir()` | Create state directory if missing |

Named constants: `MAX_PROMPT_HISTORY` (50), `MAX_FILE_CHANGES` (100), `MAX_AGENT_HISTORY` (50), `MAX_FILES_PER_TASK` (20), `LARGE_FILE_THRESHOLD` (100KB).
