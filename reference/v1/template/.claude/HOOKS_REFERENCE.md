# Hooks Reference (v3.0)

Complete reference documentation for all 12 lifecycle hooks.

---

## Hook Overview

Hooks are automated scripts that execute at specific points in the Claude Code lifecycle. They enable:
- Context injection based on task keywords
- Auto-approval of safe commands
- Error classification and recovery
- Parallel agent coordination
- Session state management
- Definition of Done verification

---

## Hook Lifecycle Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           HOOK LIFECYCLE                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  PROJECT START                                                               │
│       │                                                                      │
│       ▼                                                                      │
│  ┌─────────┐                                                                │
│  │  Setup  │ ──▶ setup-init.sh (one-time initialization)                   │
│  └────┬────┘                                                                │
│       │                                                                      │
│  SESSION START                                                               │
│       │                                                                      │
│       ▼                                                                      │
│  ┌──────────────┐                                                           │
│  │ SessionStart │ ──▶ session-start.sh (per-session init)                  │
│  └──────┬───────┘                                                           │
│         │                                                                    │
│  ┌──────┴────────────────────────────────────────────────────────────┐     │
│  │                        MESSAGE LOOP                                 │     │
│  │                                                                     │     │
│  │  USER PROMPT                                                        │     │
│  │       │                                                             │     │
│  │       ▼                                                             │     │
│  │  ┌──────────────────┐                                              │     │
│  │  │ UserPromptSubmit │ ──▶ context-injector.py                      │     │
│  │  └────────┬─────────┘                                              │     │
│  │           │                                                         │     │
│  │  TOOL CALLS                                                         │     │
│  │           │                                                         │     │
│  │           ▼                                                         │     │
│  │  ┌────────────┐     ┌─────────────────────┐                        │     │
│  │  │ PreToolUse │ ──▶ │ bash-auto-approve.py│ (if Bash)              │     │
│  │  │            │ ──▶ │ file-validator.py   │ (if Write/Edit)        │     │
│  │  └─────┬──────┘     └─────────────────────┘                        │     │
│  │        │                                                            │     │
│  │        ▼                                                            │     │
│  │  ┌─────────────┐                                                   │     │
│  │  │ Tool Executes│                                                  │     │
│  │  └──────┬──────┘                                                   │     │
│  │         │                                                           │     │
│  │    ┌────┴────┐                                                     │     │
│  │    │         │                                                      │     │
│  │ SUCCESS   FAILURE                                                   │     │
│  │    │         │                                                      │     │
│  │    ▼         ▼                                                      │     │
│  │  ┌─────────────┐  ┌─────────────────────┐                          │     │
│  │  │ PostToolUse │  │ PostToolUseFailure  │                          │     │
│  │  │ post-edit.sh│  │ error-recovery.py   │                          │     │
│  │  └─────────────┘  └─────────────────────┘                          │     │
│  │                                                                     │     │
│  │  AGENT SPAWNING                                                     │     │
│  │       │                                                             │     │
│  │       ▼                                                             │     │
│  │  ┌───────────────┐        ┌───────────────┐                        │     │
│  │  │ SubagentStart │ ──▶    │ SubagentStop  │                        │     │
│  │  │agent-tracker  │        │agent-synthesizer│                       │     │
│  │  └───────────────┘        └───────────────┘                        │     │
│  │                                                                     │     │
│  └─────────────────────────────────────────────────────────────────────┘     │
│                                                                              │
│  CONTEXT MANAGEMENT                                                          │
│       │                                                                      │
│       ▼                                                                      │
│  ┌────────────┐                                                             │
│  │ PreCompact │ ──▶ pre-compact.sh (before context compaction)             │
│  └────────────┘                                                             │
│                                                                              │
│  STOP REQUESTED                                                              │
│       │                                                                      │
│       ▼                                                                      │
│  ┌─────────┐                                                                │
│  │  Stop   │ ──▶ dod-verifier.py (verify completion)                       │
│  └─────────┘                                                                │
│                                                                              │
│  SESSION END                                                                 │
│       │                                                                      │
│       ▼                                                                      │
│  ┌────────────┐                                                             │
│  │ SessionEnd │ ──▶ session-end.sh (cleanup, metrics)                      │
│  └────────────┘                                                             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Hook Configuration (settings.json)

```json
{
  "hooks": {
    "HookName": [
      {
        "matcher": "optional condition",
        "hooks": [
          {
            "type": "command",
            "command": "script path",
            "timeout": 5000
          }
        ]
      }
    ]
  }
}
```

### Matcher Syntax

| Pattern | Description | Example |
|---------|-------------|---------|
| `tool == "X"` | Match specific tool | `tool == "Bash"` |
| `tool_input.X matches "Y"` | Match tool input | `tool_input.command matches "git push"` |
| `||` | OR condition | `tool == "Write" \|\| tool == "Edit"` |
| `&&` | AND condition | `tool == "Bash" && tool_input.command matches "rm"` |

---

## Hook Reference

### 1. Setup (`setup-init.sh`)

**Event:** First time Claude Code runs in a project
**Purpose:** One-time project initialization
**Script:** `hooks/setup-init.sh`

#### Input
None (no stdin)

#### Actions
- Creates `.claude/state/` directory structure
- Creates `.claude/metrics/` directory
- Writes `.claude/state/initialized.json`
- Updates `.gitignore` with Claude state paths

#### Output
```
[Setup] Initializing Claude Code environment...
  Created: .claude/state
  Created: .claude/metrics
  Created: .claude/state/initialized.json
[Setup] Initialization complete
```

#### Exit Codes
| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (logged, doesn't block) |

---

### 2. SessionStart (`session-start.sh`)

**Event:** Beginning of each Claude Code session
**Purpose:** Initialize session state, check for pending work
**Script:** `hooks/session-start.sh`

#### Input
None (no stdin)

#### Actions
- Creates `session_start.json` with timestamp, cwd, git branch
- Checks for existing `LOOP_STATE.md` (resume previous work)
- Checks `STATUS.md` for pending items
- Loads session memory if exists

#### Output
```
[Session Start] Session initialized at 20260129_143000
  Working directory: /path/to/project
[Session Start] Git: main (3 uncommitted changes)
[Session Start] Found existing LOOP_STATE.md - resuming previous work
  Resuming from iteration: 7
```

#### State Files Created
- `.claude/state/session_start.json`

#### Exit Codes
| Code | Meaning |
|------|---------|
| 0 | Success |

---

### 3. UserPromptSubmit (`context-injector.py`)

**Event:** User submits a prompt
**Purpose:** Analyze prompt and inject relevant context
**Script:** `hooks/context-injector.py`

#### Input (stdin)
```json
{
  "user_prompt": "Fix the login timeout issue",
  "conversation_history": [...]
}
```

#### Actions
- Analyzes prompt for keywords (auth, api, db, test, security, ui, etc.)
- Maps keywords to:
  - Relevant file paths
  - Rules to load (@rules/security, etc.)
  - Agents to suggest
- Filters paths to only those that exist

#### Output (stderr)
```
[Context] Relevant paths: src/auth/, middleware/auth | Recommended rules: @rules/security | Consider agents: security-analyst
```

#### Keyword Mappings

| Keywords | Paths | Rules | Agents |
|----------|-------|-------|--------|
| auth, login, session, password | src/auth/, middleware/auth | @rules/security | security-analyst |
| api, endpoint, route | src/api/, routes/ | @rules/api-design | code-reviewer |
| database, db, query, migration | prisma/, models/ | @rules/database | database-expert |
| test, coverage, jest | tests/, *.test.* | @rules/testing | test-engineer |
| security, vuln, xss | src/auth/ | @rules/security | security-analyst |
| ui, component, page | src/components/ | @rules/ui-ux-design | ui-ux-expert |
| perf, optimize, slow | src/ | @rules/performance | - |
| doc, readme | README.md, docs/ | @rules/documentation | documentation-writer |
| error, exception | src/, lib/ | @rules/error-handling | - |
| ci, deploy, docker | .github/, Dockerfile | - | devops-engineer |
| cli, terminal | src/cli/, bin/ | @rules/terminal-ui | terminal-ui-expert |

#### Exit Codes
| Code | Meaning |
|------|---------|
| 0 | Success (context injected or nothing to inject) |

---

### 4. PreToolUse - Bash (`bash-auto-approve.py`)

**Event:** Before a Bash command executes
**Purpose:** Auto-approve safe commands, block dangerous ones
**Script:** `hooks/bash-auto-approve.py`
**Matcher:** `tool == "Bash"`

#### Input (stdin)
```json
{
  "tool": "Bash",
  "tool_input": {
    "command": "git status"
  }
}
```

#### Actions
- Checks command against dangerous patterns (block)
- Checks command against safe patterns (auto-approve)
- Returns approval/denial via exit code

#### Safe Patterns (Auto-Approved)
```
ls, cat, head, tail, pwd, which
git status/log/diff/show/branch
npm list/outdated/audit/test
pytest, jest, vitest, cargo test
eslint, prettier --check, tsc --noEmit
node/npm/python --version
```

#### Dangerous Patterns (Always Blocked)
```
rm -rf /
sudo
chmod 777
git push --force
npm publish
curl|sh, wget|sh
```

#### Exit Codes
| Code | Meaning |
|------|---------|
| 0 | Auto-approve command |
| 1 | Require manual approval |

---

### 5. PreToolUse - Files (`file-validator.py`)

**Event:** Before Write/Edit/NotebookEdit
**Purpose:** Validate file operations, protect sensitive files
**Script:** `hooks/file-validator.py`
**Matcher:** `tool == "Write" || tool == "Edit" || tool == "NotebookEdit"`

#### Input (stdin)
```json
{
  "tool": "Write",
  "tool_input": {
    "file_path": "/path/to/file.ts",
    "content": "..."
  }
}
```

#### Actions
- Checks if file is protected (blocks)
- Checks if file matches caution patterns (blocks)
- Checks if file is important (warns)
- Scans content for secrets (blocks)
- Checks content size (blocks if >10MB)

#### Protected Files (Blocked)
```
.git/config, .git/HEAD, .git/index
package-lock.json, yarn.lock, Cargo.lock
.env, .env.local, .env.production
*.pem, *.key, id_rsa
```

#### Caution Patterns (Blocked)
```
*.lock
*.min.js, *.min.css
node_modules/*, vendor/*, dist/*
__pycache__/*
```

#### Warning Files (Allowed with Warning)
```
README.md, CHANGELOG.md, LICENSE
package.json, tsconfig.json
```

#### Exit Codes
| Code | Meaning |
|------|---------|
| 0 | Allow operation |
| 1 | Block operation |

---

### 6. PostToolUse (`post-edit.sh`)

**Event:** After successful Write/Edit
**Purpose:** Auto-format and lint edited files
**Script:** `hooks/post-edit.sh`
**Matcher:** `tool == "Edit" || tool == "Write"`

#### Input (stdin)
```json
{
  "tool": "Edit",
  "tool_input": {
    "file_path": "/path/to/file.ts"
  }
}
```

#### Actions
By file extension:
- `.js/.jsx/.ts/.tsx/.json/.md/.css/.html` → Prettier
- `.py` → Ruff or Black
- `.rs` → rustfmt
- `.go` → gofmt
- `.sh` → shfmt

Also runs quick lint check (non-blocking).

#### Output (stderr)
```
[Post-Edit] Formatted: src/utils/helpers.ts
[Post-Edit] ⚠ 2 lint errors in src/utils/helpers.ts
```

#### Exit Codes
| Code | Meaning |
|------|---------|
| 0 | Always (formatting is best-effort) |

---

### 7. PostToolUseFailure (`error-recovery.py`)

**Event:** After a tool fails
**Purpose:** Classify error and suggest recovery
**Script:** `hooks/error-recovery.py`

#### Input (stdin)
```json
{
  "tool": "Bash",
  "error": "ETIMEDOUT: connect timed out",
  "tool_input": {...},
  "retry_attempt": 0
}
```

#### Actions
- Classifies error type (network, rate limit, auth, type, syntax, permission, etc.)
- Determines recovery strategy (retry, suggest, queue, escalate)
- Outputs recovery instruction

#### Error Classification

| Error Pattern | Type | Strategy | Max Retries |
|---------------|------|----------|-------------|
| ETIMEDOUT, ECONNRESET | Network | Retry | 3 |
| 429, rate limit | Rate Limit | Retry | 3 |
| EBUSY, lock | Resource Lock | Retry | 5 |
| MODULE_NOT_FOUND | Missing Dep | Suggest | - |
| TypeError, TS\d{4} | Type Error | Queue | - |
| SyntaxError | Syntax | Queue (S0) | - |
| EACCES, EPERM | Permission | Escalate | - |
| ENOSPC, ENOMEM | Resource | Escalate | - |

#### Output (stdout - JSON)
```json
{
  "action": "retry",
  "delay": 4.0,
  "attempt": 2,
  "max_retries": 3
}
```

#### Exit Codes
| Code | Meaning |
|------|---------|
| 0 | Recovery handled (suggestion, queue) |
| 1 | Escalate to user |
| 2 | Retry requested |

---

### 8. SubagentStart (`agent-tracker.py`)

**Event:** When a subagent is spawned
**Purpose:** Track parallel agent execution
**Script:** `hooks/agent-tracker.py`

#### Input (stdin)
```json
{
  "agent_id": "agent_001",
  "subagent_type": "security-analyst",
  "prompt": "Audit src/auth for vulnerabilities",
  "model": "opus"
}
```

#### Actions
- Registers agent in state file
- Tracks agent type, task, start time
- Provides coordination hints for parallel execution

#### State File
`.claude/state/active_agents.json`:
```json
{
  "started": "2026-01-29T14:30:00Z",
  "agents": {
    "agent_001": {
      "type": "security-analyst",
      "task": "Audit src/auth for vulnerabilities",
      "model": "opus",
      "started": "2026-01-29T14:30:00Z",
      "status": "running"
    }
  }
}
```

#### Output (stderr)
```
[Agent Tracker] Registered agent_001
  Active agents: 3
  Hint: Multiple security-analyst agents active - ensure non-overlapping scope
```

#### Exit Codes
| Code | Meaning |
|------|---------|
| 0 | Success |

---

### 9. SubagentStop (`agent-synthesizer.py`)

**Event:** When a subagent completes
**Purpose:** Merge results from completed agents
**Script:** `hooks/agent-synthesizer.py`

#### Input (stdin)
```json
{
  "agent_id": "agent_001",
  "result": "## Findings\n- S1: Auth bypass in login.ts\n- S2: Missing rate limiting"
}
```

#### Actions
- Marks agent complete in state
- Extracts findings (issues, recommendations, severities)
- When all agents complete: synthesizes unified results
- Creates merged severity counts
- Deduplicates findings

#### State Files
- Updates `.claude/state/active_agents.json`
- Creates `.claude/state/agent_results.json`

#### Output (stderr)
```
[Synthesizer] Agent agent_001 completed
  Findings: 5 issues (S0:0 S1:2 S2:3 S3:0)
  Remaining agents: 1

  === All Agents Complete - Synthesis ===
  Total agents: 3
  Combined: S0:1 S1:4 S2:8 S3:2
  Unique issues: 12
  Recommendations: 5
```

#### Exit Codes
| Code | Meaning |
|------|---------|
| 0 | Success |

---

### 10. PreCompact (`pre-compact.sh`)

**Event:** Before context compaction
**Purpose:** Backup state before context is compressed
**Script:** `hooks/pre-compact.sh`

#### Input
None

#### Actions
- Backs up state files to `.claude/state/backups/`
- Files backed up:
  - `active_agents.json`
  - `agent_results.json`
  - `session_memory.json`
  - `LOOP_STATE.md`
  - `STATUS.md`
- Writes `last_compact.json` marker
- Cleans old backups (keeps last 10)

#### Output (stderr)
```
[Pre-Compact] Backed up 4 state files
[Pre-Compact] Backup location: .claude/state/backups
```

#### Exit Codes
| Code | Meaning |
|------|---------|
| 0 | Success |

---

### 11. Stop (`dod-verifier.py`)

**Event:** When user requests stop or work claims complete
**Purpose:** Verify Definition of Done criteria
**Script:** `hooks/dod-verifier.py`

#### Input (stdin)
```json
{
  "task": "Implement user authentication",
  "claimed_complete": ["testing", "security"]
}
```

#### Actions
- Detects work type (feature, bugfix, refactor, security, docs)
- Selects applicable DoD checklist
- Checks file indicators (tests exist, changelog updated, etc.)
- Generates verification prompt if needed

#### Work Type → DoD Categories

| Work Type | Required Categories |
|-----------|---------------------|
| feature | code_quality, testing, security, documentation, git, verification |
| bugfix | code_quality, testing, git, verification |
| refactor | code_quality, testing, git |
| security | code_quality, testing, security, documentation, git, verification |
| docs | documentation, git |
| chore | git |

#### Output (stderr)
```
[DoD Verifier] Work type: feature
  Status: ✗ NEEDS WORK
  Missing: Test files
  Warnings: CHANGELOG not detected as updated
  Categories verified: 6
```

#### Output (stdout - JSON)
```json
{
  "work_type": "feature",
  "passed": false,
  "missing": ["Test files"],
  "warnings": ["CHANGELOG not detected as updated"],
  "verification_prompt": "Please verify the following..."
}
```

#### Exit Codes
| Code | Meaning |
|------|---------|
| 0 | DoD passed |
| 1 | DoD failed (missing items) |

---

### 12. SessionEnd (`session-end.sh`)

**Event:** When Claude Code session ends
**Purpose:** Cleanup and collect metrics
**Script:** `hooks/session-end.sh`

#### Input
None

#### Actions
- Collects session metrics:
  - Session duration
  - Items completed
  - Agents used
  - Files changed
- Saves metrics to `.claude/metrics/session_TIMESTAMP.json`
- Updates `SESSION_HISTORY.md`
- Cleans up temporary state files

#### Output (stderr)
```
[Session End] Session completed at 20260129_163000
  Completed items: 12
  Agents used: 3
  Files changed: 15
  Metrics saved: .claude/metrics/session_20260129_163000.json
```

#### Metrics File
`.claude/metrics/session_TIMESTAMP.json`:
```json
{
  "session_end": "20260129_163000",
  "session_start": "20260129_143000",
  "completed_items": 12,
  "agents_used": 3,
  "files_changed": 15
}
```

#### Exit Codes
| Code | Meaning |
|------|---------|
| 0 | Success |

---

## State Files Reference

| File | Purpose | Managed By |
|------|---------|------------|
| `.claude/state/initialized.json` | First-run marker | setup-init.sh |
| `.claude/state/session_start.json` | Session info | session-start.sh |
| `.claude/state/active_agents.json` | Running agents | agent-tracker.py |
| `.claude/state/agent_results.json` | Agent findings | agent-synthesizer.py |
| `.claude/state/last_compact.json` | Compaction marker | pre-compact.sh |
| `.claude/state/backups/` | State backups | pre-compact.sh |
| `.claude/metrics/session_*.json` | Session metrics | session-end.sh |
| `.claude/context/SESSION_HISTORY.md` | Session log | session-end.sh |

---

## Creating Custom Hooks

### Step 1: Create Script

```python
#!/usr/bin/env python3
"""
My Custom Hook (HookEvent)

Purpose description here.

Hook Type: HookEvent
Input: JSON with {...}
Output: {...}
"""

import json
import sys

def main():
    # Read input
    input_data = sys.stdin.read()
    data = json.loads(input_data) if input_data.strip() else {}

    # Your logic here

    # Output to stderr (displayed to user)
    print("[My Hook] Message", file=sys.stderr)

    # Output to stdout (JSON for Claude)
    print(json.dumps({"result": "..."}))

    # Exit code
    sys.exit(0)  # 0=success, 1=block/fail, 2=retry

if __name__ == "__main__":
    main()
```

### Step 2: Register in settings.json

```json
{
  "hooks": {
    "HookEvent": [
      {
        "matcher": "optional condition",
        "hooks": [
          {
            "type": "command",
            "command": "python .claude/hooks/my-hook.py",
            "timeout": 5000
          }
        ]
      }
    ]
  }
}
```

### Available Hook Events

| Event | When Fired |
|-------|------------|
| Setup | First run in project |
| SessionStart | Each session begins |
| UserPromptSubmit | User sends message |
| PreToolUse | Before tool executes |
| PostToolUse | After tool succeeds |
| PostToolUseFailure | After tool fails |
| SubagentStart | Agent spawned |
| SubagentStop | Agent completes |
| PreCompact | Before context compression |
| Stop | User requests stop |
| SessionEnd | Session ends |

---

## Troubleshooting

### Hook Not Firing
1. Check `settings.json` syntax
2. Verify script path is correct
3. Check script has execute permissions
4. Look for timeout issues (increase timeout)

### Hook Blocking Operations
1. Check exit codes in script
2. Verify matcher conditions
3. Check for exceptions in script

### State File Issues
1. Ensure `.claude/state/` exists
2. Check file permissions
3. Look for JSON parse errors

### Performance Issues
1. Reduce hook timeout
2. Optimize script logic
3. Consider disabling non-essential hooks
