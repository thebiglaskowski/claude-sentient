# State Files Reference (v3.0)

Complete manifest of all state files used by the v3.0 system.

---

## Directory Structure

```
.claude/
├── state/                    # Runtime state (gitignored)
│   ├── agents/               # Agent tracking
│   │   ├── active.json       # Currently running agents
│   │   └── results/          # Agent output files
│   ├── loop/                 # Loop state
│   │   ├── LOOP_STATE.md     # Current loop status
│   │   └── work_queue.json   # Prioritized work items
│   ├── session/              # Session tracking
│   │   ├── current.json      # Current session info
│   │   └── metrics.json      # Session metrics
│   ├── errors/               # Error tracking
│   │   └── classified.json   # Classified errors for retry
│   └── compaction/           # Pre-compaction backups
│       └── backup_*.json     # Timestamped backups
├── settings.json             # Hook configuration (committed)
└── CLAUDE.md                 # Project instructions (committed)
```

---

## State Files Detail

### 1. Agent State Files

#### `.claude/state/agents/active.json`

**Purpose:** Track currently running parallel agents

**Created by:** `agent-tracker.py` (SubagentStart hook)

**Updated by:** `agent-synthesizer.py` (SubagentStop hook)

**Schema:**
```json
{
  "agents": [
    {
      "id": "agent-uuid-1234",
      "type": "security-analyst",
      "task": "Audit authentication implementation",
      "started": "2026-01-29T10:30:00Z",
      "status": "running",
      "parent_task": "implement user authentication"
    }
  ],
  "total_spawned": 3,
  "total_completed": 1,
  "session_id": "session-uuid"
}
```

**Lifecycle:**
1. Created when first agent spawns in session
2. Updated on each SubagentStart/SubagentStop
3. Cleared on SessionEnd

---

#### `.claude/state/agents/results/{agent-id}.json`

**Purpose:** Store individual agent results for synthesis

**Created by:** `agent-synthesizer.py` (SubagentStop hook)

**Schema:**
```json
{
  "agent_id": "agent-uuid-1234",
  "type": "security-analyst",
  "task": "Audit authentication implementation",
  "started": "2026-01-29T10:30:00Z",
  "completed": "2026-01-29T10:35:00Z",
  "duration_seconds": 300,
  "status": "success",
  "findings": [
    {
      "severity": "S1",
      "category": "security",
      "title": "Missing rate limiting on login endpoint",
      "details": "...",
      "recommendation": "..."
    }
  ],
  "recommendations": ["..."],
  "files_analyzed": ["src/auth/login.ts", "src/middleware/auth.ts"],
  "metrics": {
    "files_read": 12,
    "issues_found": 3
  }
}
```

**Lifecycle:**
1. Created when agent completes
2. Read by synthesizer to merge findings
3. Archived or deleted on session end

---

### 2. Loop State Files

#### `.claude/state/loop/LOOP_STATE.md`

**Purpose:** Human-readable loop status for debugging

**Created by:** `/loop` command (CONTEXTUALIZE phase)

**Updated by:** Each loop phase

**Format:**
```markdown
# Loop State

## Meta
- Started: 2026-01-29T10:00:00Z
- Current Iteration: 3
- Status: BUILDING
- Task: "implement user authentication"

## Quality Gates
| Gate | Status | Last Check | Issues |
|------|--------|------------|--------|
| Pre-flight | PASS | 10:45:00 | 0 |
| Lint | PASS | 10:45:00 | 0 |
| Type | PASS | 10:45:00 | 0 |
| Tests | PASS | 10:45:00 | 0 |
| Security | WARN | 10:45:00 | 1 (S2) |

## Work Queue
| Priority | Item | Status |
|----------|------|--------|
| S1 | Implement auth endpoints | DONE |
| S1 | Add session management | IN_PROGRESS |
| S2 | Update CHANGELOG | PENDING |

## History
- Iteration 1: Fixed 2 items, 1 new issue found
- Iteration 2: Fixed 1 item, gates passing
```

**Lifecycle:**
1. Created at loop start
2. Updated after each phase
3. Final status written on loop completion
4. Preserved for debugging (not auto-deleted)

---

#### `.claude/state/loop/work_queue.json`

**Purpose:** Machine-readable prioritized work queue

**Created by:** `/loop` command (ASSESS phase)

**Updated by:** BUILD, RECOVER phases

**Schema:**
```json
{
  "version": 1,
  "task": "implement user authentication",
  "iteration": 3,
  "consecutive_passes": 1,
  "items": [
    {
      "id": "work-001",
      "priority": "S1",
      "title": "Implement auth endpoints",
      "description": "Create /api/auth/login and /api/auth/logout",
      "status": "done",
      "added_iteration": 1,
      "completed_iteration": 2
    },
    {
      "id": "work-002",
      "priority": "S2",
      "title": "Update CHANGELOG",
      "description": "Add entry for auth feature",
      "status": "pending",
      "added_iteration": 2,
      "completed_iteration": null
    }
  ],
  "gate_results": {
    "lint": { "status": "pass", "timestamp": "..." },
    "type": { "status": "pass", "timestamp": "..." },
    "test": { "status": "pass", "timestamp": "..." }
  }
}
```

---

### 3. Session State Files

#### `.claude/state/session/current.json`

**Purpose:** Track current session metadata

**Created by:** `session-start.sh` (SessionStart hook)

**Updated by:** Various hooks throughout session

**Schema:**
```json
{
  "session_id": "session-uuid-5678",
  "started": "2026-01-29T09:00:00Z",
  "git_branch": "feature/user-auth",
  "git_commit_start": "abc123",
  "working_directory": "/project",
  "hooks_version": "3.0",
  "commands_executed": ["loop", "assess"],
  "agents_spawned": 2,
  "files_modified": ["src/auth/login.ts", "src/auth/logout.ts"],
  "errors_encountered": 1,
  "errors_recovered": 1
}
```

**Lifecycle:**
1. Created at session start
2. Updated throughout session
3. Archived to metrics on session end

---

#### `.claude/state/session/metrics.json`

**Purpose:** Aggregate session metrics for analysis

**Created by:** `session-end.sh` (SessionEnd hook)

**Schema:**
```json
{
  "sessions": [
    {
      "session_id": "session-uuid-5678",
      "date": "2026-01-29",
      "duration_minutes": 45,
      "commands": {
        "loop": 1,
        "assess": 2,
        "fix": 3
      },
      "agents": {
        "spawned": 2,
        "completed": 2,
        "failed": 0
      },
      "quality": {
        "issues_found": 5,
        "issues_fixed": 4,
        "coverage_delta": "+8%"
      },
      "errors": {
        "total": 3,
        "recovered": 2,
        "escalated": 1
      }
    }
  ]
}
```

---

### 4. Error State Files

#### `.claude/state/errors/classified.json`

**Purpose:** Track classified errors for retry logic

**Created by:** `error-recovery.py` (PostToolUseFailure hook)

**Schema:**
```json
{
  "errors": [
    {
      "id": "error-uuid-001",
      "timestamp": "2026-01-29T10:30:00Z",
      "classification": "network",
      "tool": "WebFetch",
      "message": "Connection timeout",
      "retry_count": 1,
      "max_retries": 3,
      "status": "pending_retry",
      "next_retry": "2026-01-29T10:30:30Z",
      "context": {
        "url": "https://api.example.com",
        "operation": "fetch documentation"
      }
    }
  ],
  "summary": {
    "total": 5,
    "recovered": 3,
    "pending": 1,
    "escalated": 1
  }
}
```

**Error Classifications:**
| Classification | Retry Strategy | Max Retries |
|----------------|----------------|-------------|
| `network` | Exponential backoff | 3 |
| `rate_limit` | Wait for reset | 3 |
| `timeout` | Immediate retry | 2 |
| `syntax` | Add to work queue | 0 |
| `permission` | Escalate to user | 0 |
| `resource` | Wait and retry | 2 |
| `unknown` | Log and continue | 1 |

---

### 5. Compaction State Files

#### `.claude/state/compaction/backup_{timestamp}.json`

**Purpose:** Preserve critical state before context compaction

**Created by:** `pre-compact.sh` (PreCompact hook)

**Schema:**
```json
{
  "timestamp": "2026-01-29T10:45:00Z",
  "reason": "context_limit_approaching",
  "preserved": {
    "loop_state": { /* LOOP_STATE snapshot */ },
    "work_queue": { /* work_queue.json snapshot */ },
    "active_agents": { /* active.json snapshot */ },
    "session": { /* current.json snapshot */ }
  },
  "context_tokens_before": 180000,
  "files_in_context": [
    "src/auth/login.ts",
    "src/auth/logout.ts"
  ]
}
```

**Lifecycle:**
1. Created immediately before compaction
2. Kept for session duration
3. Cleaned up on session end (keeping last 3)

---

## Gitignore Configuration

Add to `.gitignore`:

```gitignore
# Claude Code state files (runtime only)
.claude/state/

# Keep configuration
!.claude/settings.json
!.claude/CLAUDE.md
!.claude/agents/
!.claude/skills/
!.claude/hooks/
```

---

## State File Best Practices

### 1. Always Check Existence

```python
import os
import json

state_file = ".claude/state/loop/work_queue.json"
if os.path.exists(state_file):
    with open(state_file) as f:
        state = json.load(f)
else:
    state = {"items": [], "iteration": 0}
```

### 2. Use Atomic Writes

```python
import tempfile
import shutil

def atomic_write(filepath, data):
    """Write atomically to prevent corruption."""
    dir_path = os.path.dirname(filepath)
    os.makedirs(dir_path, exist_ok=True)

    with tempfile.NamedTemporaryFile(
        mode='w',
        dir=dir_path,
        delete=False
    ) as tmp:
        json.dump(data, tmp, indent=2)
        tmp_path = tmp.name

    shutil.move(tmp_path, filepath)
```

### 3. Handle Concurrent Access

```python
import fcntl

def read_with_lock(filepath):
    """Read with file locking for concurrent access."""
    with open(filepath) as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_SH)
        data = json.load(f)
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    return data
```

### 4. Validate on Read

```python
def validate_work_queue(data):
    """Validate work queue schema."""
    required = ["version", "task", "iteration", "items"]
    for field in required:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
    return data
```

---

## Cleanup Procedures

### Session End Cleanup

```bash
# Performed by session-end.sh
rm -rf .claude/state/agents/results/*
rm -rf .claude/state/errors/*
# Keep loop state for debugging
# Keep metrics for analysis
# Keep last 3 compaction backups
```

### Manual Cleanup

```bash
# Full state reset
rm -rf .claude/state/

# Reset just loop state
rm -rf .claude/state/loop/

# Reset just agent state
rm -rf .claude/state/agents/
```

---

## Troubleshooting

### State File Corruption

**Symptom:** JSON parse errors

**Fix:**
```bash
# Remove corrupted file
rm .claude/state/loop/work_queue.json
# Loop will recreate on next iteration
```

### Stale State

**Symptom:** Loop references completed work

**Fix:**
```bash
# Reset loop state
rm -rf .claude/state/loop/
# Restart loop
/loop "task" --reset
```

### Missing State Directory

**Symptom:** Hooks fail to write state

**Fix:**
```bash
# Ensure directories exist
mkdir -p .claude/state/{agents/results,loop,session,errors,compaction}
```

---

## See Also

| Document | Purpose |
|----------|---------|
| [HOOKS_REFERENCE](HOOKS_REFERENCE.md) | Hook implementation details |
| [LOOP_WORKFLOW](LOOP_WORKFLOW.md) | Loop execution flow |
| [ERROR_RECOVERY](ERROR_RECOVERY.md) | Error handling details |
