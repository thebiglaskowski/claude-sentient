# SDK — Claude Sentient

> Context for working on the Python and TypeScript SDKs.

## CLI vs SDK: Two Ways to Use Claude Sentient

| Aspect | CLI Mode | SDK Mode |
|--------|----------|----------|
| **Entry point** | `/cs-loop "task"` in terminal | `ClaudeSentient.loop("task")` in code |
| **Installation** | One-line install script | `pip install -e` or `npm install` |
| **Use case** | Interactive development | Automation, CI/CD, scripts |
| **Session persistence** | Per-terminal session | Persists to `.claude/state/` |
| **User interaction** | Claude asks questions via terminal | Programmatic control, no prompts |
| **Best for** | Day-to-day development | Production pipelines, scheduled tasks |

### Key Differences

**Session Persistence:**
- CLI: Session lives in terminal. Close terminal = lose context.
- SDK: Session saved to `.claude/state/session.json`. Resume anytime with `sentient.resume()`.

**User Interaction:**
- CLI: Claude can ask you questions, you see output in real-time.
- SDK: Non-interactive by default. Configure hooks for custom behavior.

**Quality Gates:**
- CLI: Gates run as part of the loop, Claude reports results.
- SDK: Gates run as hooks (`PostToolUse`, `PreToolUse`), can block commits programmatically.

**Installation Scope:**
- CLI: Installs into a specific project (`.claude/commands/`).
- SDK: Installed globally or per-environment via pip/npm.

### Using Both Together

Both modes share the same `profiles/*.yaml`, `.claude/rules/learnings.md` memory, and quality gate definitions.

---

## SDK Installation

**Python (from repo):**
```bash
pip install -e sdk/python/
```

For CLI commands (`claude-sentient`, `cs`), add the Scripts directory to PATH:
```bash
# Windows PowerShell
$env:PATH += ";C:\Users\<you>\AppData\Local\...\Python313\Scripts"

# Linux/Mac
export PATH="$HOME/.local/bin:$PATH"
```

**TypeScript (from repo):**
```bash
cd sdk/typescript && npm install && npm run build
```

To use in other projects:
```bash
npm link                          # In sdk/typescript/
npm link @claude-sentient/sdk     # In consuming project
```

**Direct import (no install):**
```python
import sys
sys.path.insert(0, "path/to/claude-sentient/sdk/python")
from claude_sentient import ClaudeSentient
```

---

## Basic Usage

**Python:**
```python
from claude_sentient import ClaudeSentient

async def main():
    sentient = ClaudeSentient(cwd="./my-project")

    # Run the autonomous loop
    async for result in sentient.loop("Add user authentication"):
        print(f"Phase: {result.phase}, Tasks: {result.tasks_completed}")
        if result.success:
            print(f"Done! Commit: {result.commit_hash}")

    # Or plan without executing
    plan = await sentient.plan("Refactor the API layer")

    # Resume a previous session
    async for result in sentient.resume():
        print(f"Resumed: {result.phase}")
```

**TypeScript:**
```typescript
import { ClaudeSentient } from "@claude-sentient/sdk";

const sentient = new ClaudeSentient({ cwd: "./my-project" });

for await (const result of sentient.loop("Add user authentication")) {
  console.log(`Phase: ${result.phase}, Tasks: ${result.tasksCompleted}`);
  if (result.success) {
    console.log(`Done! Commit: ${result.commitHash}`);
  }
}
```

---

## Example Use Cases

```python
# CI/CD: Run on every PR
async def ci_check(pr_branch: str):
    sentient = ClaudeSentient(cwd="./repo")
    async for result in sentient.loop(f"Review changes in {pr_branch}"):
        if not result.gates_passed.get("lint"):
            raise Exception("Lint failed")
        if not result.gates_passed.get("test"):
            raise Exception("Tests failed")

# Scheduled: Nightly maintenance
async def nightly_maintenance():
    sentient = ClaudeSentient(cwd="./repo")
    async for result in sentient.loop("Update dependencies and fix deprecations"):
        print(f"Completed: {result.commit_hash}")

# Resumable: Long-running task
async def long_task():
    sentient = ClaudeSentient(cwd="./repo")
    try:
        async for result in sentient.resume():
            print(f"Resumed from {result.phase}")
    except ValueError:
        async for result in sentient.loop("Large refactoring task"):
            print(f"Phase: {result.phase}")
```

---

## SDK Features

| Feature | Description |
|---------|-------------|
| **Session Persistence** | Resume work across terminal closures via `.claude/state/session.json` |
| **Programmatic Control** | SDK-based orchestration for CI/CD, webhooks, scheduled tasks |
| **Quality Gate Hooks** | Automated lint/test enforcement as SDK hooks |
| **Profile Detection** | Auto-detect project type from files |
| **Subagent Definitions** | Pre-configured agents for exploration, testing, lint-fixing |

---

## SDK Directory Structure

```
sdk/
├── python/
│   ├── claude_sentient/
│   │   ├── __init__.py       # Package exports
│   │   ├── orchestrator.py   # Main ClaudeSentient class
│   │   ├── session.py        # Session persistence
│   │   ├── profiles.py       # Profile detection/loading
│   │   ├── gates.py          # Quality gate execution
│   │   ├── hooks.py          # Custom hook definitions
│   │   └── types.py          # Dataclasses
│   ├── pyproject.toml
│   └── README.md
│
└── typescript/
    ├── src/
    │   ├── index.ts          # Package exports
    │   ├── orchestrator.ts   # Main class
    │   ├── session.ts        # Session persistence
    │   ├── profiles.ts       # Profile detection
    │   ├── gates.ts          # Quality gates
    │   ├── hooks.ts          # Hook definitions
    │   └── types.ts          # Type definitions
    ├── package.json
    └── README.md
```

See `sdk/python/README.md` and `sdk/typescript/README.md` for full API documentation.
