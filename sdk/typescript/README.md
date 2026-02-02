# Claude Sentient TypeScript SDK

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
# From local repo
cd sdk/typescript
npm install
npm run build

# Then import in your project
import { ClaudeSentient } from "./path/to/sdk/typescript/src";
```

## Quick Start

```typescript
import { ClaudeSentient } from "@claude-sentient/sdk";

async function main() {
  // Initialize with auto-detected profile
  const sentient = new ClaudeSentient({ cwd: "./my-project" });

  // Run the autonomous development loop
  for await (const result of sentient.loop("Add user authentication")) {
    console.log(`Phase: ${result.phase}`);
    console.log(`Tasks completed: ${result.tasksCompleted}`);

    if (result.success) {
      console.log(`Done! Commit: ${result.commitHash}`);
    }
  }
}

main();
```

## Features

### Session Persistence

Resume work across terminal closures:

```typescript
// Start a session
for await (const result of sentient.loop("Refactor API")) {
  if (shouldPause) {
    break; // Session state is saved
  }
}

// Later, resume
for await (const result of sentient.resume()) {
  console.log(`Resumed from: ${result.phase}`);
}
```

### Quality Gates

Automatic linting and testing:

```typescript
// Gates are configured per-profile (python, typescript, etc.)
const result = sentient.getGateResults();
console.log(result);
// { lint: true, test: true, type: false }
```

### Profile Detection

Auto-detects project type:

```typescript
const sentient = new ClaudeSentient({ cwd: "./my-ts-project" });
console.log(sentient.profileName); // "typescript"

// Or specify explicitly
const sentient2 = new ClaudeSentient({ cwd: ".", profile: "python" });
```

## API Reference

### ClaudeSentient

Main orchestrator class.

```typescript
new ClaudeSentient({
  cwd?: string;              // Working directory (default: ".")
  profile?: string;          // Profile name (auto-detected)
  permissionMode?: string;   // Permission mode (default: "acceptEdits")
  profilesDir?: string;      // Directory for profile YAML files
});
```

#### Methods

- `loop(task, options?)` - Run the autonomous development loop
- `plan(task)` - Plan without executing
- `resume()` - Resume the last session
- `getSessionState()` - Get current session state
- `getGateResults()` - Get quality gate results

### LoopResult

Result of each loop iteration.

```typescript
interface LoopResult {
  success: boolean;
  sessionId: string;
  phase: Phase;
  iteration: number;
  tasksCompleted: number;
  tasksRemaining: number;
  gatesPassed: Record<string, boolean>;
  commitHash?: string;
  durationMs: number;
  costUsd: number;
  message: string;
}
```

## Configuration

The SDK reads configuration from:

1. `profiles/*.yaml` - Profile definitions
2. `CLAUDE.md` - Project instructions
3. `.claude/state/session.json` - Session persistence

## License

MIT
