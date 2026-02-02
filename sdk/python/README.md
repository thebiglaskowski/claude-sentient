# Claude Sentient Python SDK

Autonomous Development Orchestration Layer for Claude Code.

## When to Use the SDK

The SDK is for **programmatic automation**. Use it when you need to:

- Run Claude Sentient from CI/CD pipelines
- Schedule tasks (nightly maintenance, dependency updates)
- Trigger via webhooks or external events
- Resume work across terminal sessions
- Run headless without user interaction

For **interactive development**, use the CLI instead:
```bash
curl -fsSL https://raw.githubusercontent.com/thebiglaskowski/claude-sentient/main/install.sh | bash
/cs-loop "your task"
```

## Installation

```bash
# From local repo (editable install)
pip install -e sdk/python/

# Or add to Python path directly (no install)
import sys
sys.path.insert(0, "path/to/claude-sentient/sdk/python")
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

## API Reference

### ClaudeSentient

Main orchestrator class.

```python
ClaudeSentient(
    cwd: str = ".",              # Working directory
    profile: str | None = None,  # Profile name (auto-detected)
    permission_mode: str = "acceptEdits",
    profiles_dir: str | None = None,
)
```

#### Methods

- `loop(task, resume=False)` - Run the autonomous development loop
- `plan(task)` - Plan without executing
- `resume()` - Resume the last session
- `get_session_state()` - Get current session state
- `get_gate_results()` - Get quality gate results

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
