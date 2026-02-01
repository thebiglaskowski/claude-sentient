#!/bin/bash
# Session Start Hook
#
# Initialize session state and load context.
# Records session start and prepares working environment.
#
# Hook Type: SessionStart
# Output: Session initialization status

set -e

STATE_DIR=".claude/state"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Ensure state directory exists
mkdir -p "$STATE_DIR"

# Record session start
cat > "$STATE_DIR/session_start.json" << EOF
{
    "timestamp": "$TIMESTAMP",
    "cwd": "$(pwd)",
    "git_branch": "$(git branch --show-current 2>/dev/null || echo 'none')",
    "git_status": "$(git status --porcelain 2>/dev/null | wc -l || echo '0') changes"
}
EOF

# Check for existing loop state
if [ -f "LOOP_STATE.md" ]; then
    echo "[Session Start] Found existing LOOP_STATE.md - resuming previous work" >&2
    # Extract current iteration if present
    iteration=$(grep -o "Current Iteration: [0-9]*" LOOP_STATE.md 2>/dev/null | grep -o "[0-9]*" || echo "0")
    if [ "$iteration" != "0" ]; then
        echo "  Resuming from iteration: $iteration" >&2
    fi
fi

# Check for pending work in STATUS.md
if [ -f "STATUS.md" ]; then
    pending=$(grep -c "⏳\|Pending\|TODO\|WIP" STATUS.md 2>/dev/null || echo "0")
    if [ "$pending" != "0" ]; then
        echo "[Session Start] Found $pending pending items in STATUS.md" >&2
    fi
fi

# Load previous session context if exists
if [ -f "$STATE_DIR/session_memory.json" ]; then
    echo "[Session Start] Loaded session memory from previous session" >&2
fi

# Check git status
if command -v git &> /dev/null && git rev-parse --git-dir > /dev/null 2>&1; then
    branch=$(git branch --show-current 2>/dev/null || echo "detached")
    uncommitted=$(git status --porcelain 2>/dev/null | wc -l)
    echo "[Session Start] Git: $branch ($uncommitted uncommitted changes)" >&2

    # Warn about uncommitted changes
    if [ "$uncommitted" -gt 10 ]; then
        echo "  ⚠ Many uncommitted changes - consider committing" >&2
    fi
fi

# Check for capability inventory (meta-cognition)
if [ -f ".claude/context/CAPABILITY_INVENTORY.md" ]; then
    echo "[Session Start] Capability inventory available for intelligent decisions" >&2
    echo "  Use meta-cognition skill to consult available tools" >&2
fi

# Remind about available capabilities
echo "" >&2
echo "[Session Start] AVAILABLE CAPABILITIES:" >&2
echo "  35 commands (/plan, /loop, /review, etc.)" >&2
echo "  15 specialized agents (code-reviewer, security-analyst, etc.)" >&2
echo "  13 rules (@rules/security, @rules/testing, etc.)" >&2
echo "  Consult CAPABILITY_INVENTORY.md for full list" >&2

# Output session info
echo "" >&2
echo "[Session Start] Session initialized at $TIMESTAMP" >&2
echo "  Working directory: $(pwd)" >&2

exit 0
