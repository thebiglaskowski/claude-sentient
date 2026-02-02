# Claude Sentient Python SDK

Autonomous Development Orchestration Layer for Claude Code.

> **Note**: This SDK integrates with the official [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview). Install it for full autonomous capabilities, or run in simulation mode for testing.

## When to Use the SDK

The SDK is for **programmatic automation**. Use it when you need to:

- Run Claude Sentient from CI/CD pipelines
- Schedule tasks (nightly maintenance, dependency updates)
- Trigger via webhooks or external events
- Resume work across terminal sessions
- Run headless without user interaction
- Build custom applications on top of Claude's capabilities

For **interactive development**, use the CLI instead:
```bash
curl -fsSL https://raw.githubusercontent.com/thebiglaskowski/claude-sentient/main/install.sh | bash
/cs-loop "your task"
```

## Installation

```bash
# From local repo (editable install)
pip install -e sdk/python/

# With full Claude Agent SDK support (recommended)
pip install -e "sdk/python/[sdk]"

# Or install claude-agent-sdk separately
pip install claude-agent-sdk
```

> **Requires**: Claude Code installed and `ANTHROPIC_API_KEY` set for full functionality. Without these, the SDK runs in simulation mode.

### Library Usage (No PATH Change Needed)

After installation, you can import directly in Python scripts:

```python
from claude_sentient import ClaudeSentient
```

### CLI Usage (Requires PATH)

The install creates CLI commands (`claude-sentient`, `cs`). If you see a warning about scripts not being on PATH:

```bash
# Windows PowerShell - add to current session
$env:PATH += ";C:\Users\<you>\AppData\Local\...\Python313\Scripts"

# Windows - permanent (System Properties → Environment Variables)
# Add the Scripts directory shown in the pip warning

# Linux/Mac - add to ~/.bashrc or ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"
```

### Direct Import (No Install)

```python
import sys
sys.path.insert(0, "path/to/claude-sentient/sdk/python")
from claude_sentient import ClaudeSentient
```

## Quick Start

```python
from claude_sentient import ClaudeSentient

async def main():
    # Initialize with auto-detected profile
    sentient = ClaudeSentient(cwd="./my-project")

    # Run the autonomous development loop
    async for result in sentient.loop("Add user authentication"):
        print(f"Phase: {result.phase}")
        print(f"Tasks completed: {result.tasks_completed}")

        if result.success:
            print(f"Done! Commit: {result.commit_hash}")
```

## Features

### Session Persistence

Resume work across terminal closures:

```python
# Start a session
async for result in sentient.loop("Refactor API"):
    if should_pause:
        break  # Session state is saved

# Later, resume
async for result in sentient.resume():
    print(f"Resumed from: {result.phase}")
```

### Quality Gates

Automatic linting and testing:

```python
# Gates are configured per-profile (python, typescript, etc.)
result = sentient.get_gate_results()
print(result)
# {'lint': True, 'test': True, 'type': False}
```

### Profile Detection

Auto-detects project type:

```python
sentient = ClaudeSentient(cwd="./my-python-project")
print(sentient.profile_name)  # "python"

# Or specify explicitly
sentient = ClaudeSentient(cwd=".", profile="typescript")
```

### Continuous Conversation Mode

Use `client()` for multi-turn conversations where Claude remembers context:

```python
async with sentient.client() as client:
    await client.query("What files are in this project?")
    async for msg in client.receive_response():
        print(msg)

    # Follow-up in same conversation - Claude remembers context
    await client.query("Which one handles authentication?")
    async for msg in client.receive_response():
        print(msg)

    # Interrupt if needed
    await client.interrupt()
```

### Custom Permission Handling

Use `can_use_tool` callback for custom permission logic:

```python
async def my_permission_handler(tool_name, input_data, context):
    # Block dangerous commands
    if tool_name == "Bash" and "rm -rf" in input_data.get("command", ""):
        return PermissionResultDeny(message="Dangerous command blocked")
    # Allow everything else
    return PermissionResultAllow(updated_input=input_data)

sentient = ClaudeSentient(
    cwd="./my-project",
    can_use_tool=my_permission_handler
)
```

### Sandbox Mode

Run commands in a sandbox for security:

```python
from claude_sentient import ClaudeSentient, SandboxConfig

sentient = ClaudeSentient(
    cwd="./my-project",
    sandbox=SandboxConfig(
        enabled=True,
        auto_allow_bash_if_sandboxed=True
    )
)
```

### File Checkpointing

Enable file rollback to undo changes:

```python
sentient = ClaudeSentient(
    cwd="./my-project",
    enable_file_checkpointing=True
)

async with sentient.client() as client:
    await client.query("Refactor the auth module")
    # ... some work happens ...

    # Oops, need to rollback!
    await client.rewind_files(user_message_uuid)
```

### Budget Control

Set a maximum budget for API costs:

```python
sentient = ClaudeSentient(
    cwd="./my-project",
    max_budget_usd=5.00  # Stop if cost exceeds $5
)

async for result in sentient.loop("Large refactoring task"):
    print(f"Cost so far: ${result.cost_usd:.2f}")
```

## API Reference

### ClaudeSentient

Main orchestrator class.

```python
ClaudeSentient(
    cwd: str = ".",                    # Working directory
    profile: str | None = None,        # Profile name (auto-detected)
    permission_mode: str = "acceptEdits",  # default, acceptEdits, plan, bypassPermissions
    profiles_dir: str | None = None,
    setting_sources: list[str] | None = None,  # ["user", "project", "local"]
    can_use_tool: Callable | None = None,      # Custom permission callback
    hooks: dict | None = None,                  # Hook configurations
    sandbox: SandboxConfig | None = None,       # Sandbox settings
    enable_file_checkpointing: bool = False,    # Enable file rollback
    max_budget_usd: float | None = None,        # Budget limit
    model: str | None = None,                   # Model override
)
```

#### Methods

- `loop(task, resume=False)` - Run the autonomous development loop
- `plan(task)` - Plan without executing (uses plan permission mode)
- `resume()` - Resume the last session
- `get_session_state()` - Get current session state
- `get_gate_results()` - Get quality gate results
- `get_total_cost()` - Get total API cost in USD
- `client()` - Get a continuous conversation client

### LoopResult

Result of each loop iteration.

```python
@dataclass
class LoopResult:
    success: bool
    session_id: str
    phase: str
    iteration: int
    tasks_completed: int
    tasks_remaining: int
    gates_passed: dict[str, bool]
    commit_hash: str | None
    duration_ms: float
    cost_usd: float
    message: str
```

## CLI Usage

```bash
# Run the loop
claude-sentient loop "Add user authentication"

# Or use the short alias
cs loop "Add user authentication"

# Plan without executing
cs plan "Refactor the API layer"

# Resume a session
cs resume

# Check status
cs status
```

## Configuration

The SDK reads configuration from:

1. `profiles/*.yaml` - Profile definitions
2. `CLAUDE.md` - Project instructions
3. `.claude/state/session.json` - Session persistence

## License

MIT
