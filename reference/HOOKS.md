# Claude Sentient Hooks

Claude Code supports hooks at 12 lifecycle points. Claude Sentient uses these for session logging and can be extended for more advanced automation.

## Default Hooks

These are included in `.claude/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "type": "command",
        "command": "echo '[cs] Prompt received' >> .claude/session.log 2>/dev/null || true"
      }
    ],
    "Stop": [
      {
        "type": "command",
        "command": "echo \"[cs] Session ended: $(date)\" >> .claude/session.log 2>/dev/null || true"
      }
    ]
  }
}
```

## Available Hook Points

| Hook | When It Fires | Use Case |
|------|---------------|----------|
| `SessionStart` | Session begins/resumes | Load environment, inject context |
| `SessionEnd` | Session terminates | Cleanup, final logging |
| `UserPromptSubmit` | User sends a message | Validate input, inject context |
| `PreToolUse` | Before any tool runs | Safety checks, logging |
| `PostToolUse` | After tool succeeds | Logging, side effects |
| `PostToolUseFailure` | After tool fails | Error handling |
| `Stop` | Claude finishes responding | Session summary, logging |
| `PreCompact` | Before context compaction | Save important context |
| `SubagentStart` | Subagent spawns | Logging, resource tracking |
| `SubagentStop` | Subagent finishes | Collect results |
| `PermissionRequest` | Permission dialog shown | Auto-approve patterns |
| `Notification` | Claude sends notification | External integrations |

## Hook Types

### Command Hooks
Execute shell commands:
```json
{
  "type": "command",
  "command": "echo 'Hello' >> log.txt"
}
```

### Prompt Hooks
Send to Claude model for decision:
```json
{
  "type": "prompt",
  "prompt": "Should this action be allowed? Respond ALLOW or DENY."
}
```

### Matcher (for PreToolUse)
Filter which tools trigger the hook:
```json
{
  "type": "command",
  "matcher": "Bash",
  "command": "./validate-bash-command.sh"
}
```

## Advanced Hook Examples

### Context Injection on Prompt
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "type": "command",
        "command": "cat STATUS.md | head -50"
      }
    ]
  }
}
```

### Safety Check for Destructive Commands
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "type": "prompt",
        "matcher": "Bash(rm *)",
        "prompt": "This command will delete files. Are you sure? ALLOW or DENY."
      }
    ]
  }
}
```

### Session Summary on Stop
```json
{
  "hooks": {
    "Stop": [
      {
        "type": "command",
        "command": "echo \"Session: $(git log --oneline -1 2>/dev/null || echo 'no commits')\" >> .claude/session.log"
      }
    ]
  }
}
```

## Platform Notes

- Commands use shell syntax (`/bin/sh` on Unix, `cmd` on Windows)
- Use `2>/dev/null || true` to suppress errors gracefully
- Hook output is visible to Claude and can influence responses
- Hooks that fail don't block Claude (unless they return specific exit codes)

## Adding Custom Hooks

1. Edit `.claude/settings.json`
2. Add your hook under the appropriate lifecycle point
3. Test with a simple echo command first
4. For complex logic, create a script file and call it from the hook

## Disabling Hooks

Remove or comment out hooks in `.claude/settings.json`. The schema is validated, so use proper JSON syntax.
