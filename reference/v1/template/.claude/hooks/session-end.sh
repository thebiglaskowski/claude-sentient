#!/bin/bash
# Session End Hook
#
# Cleanup and metrics collection at session end.
# Saves session summary and cleans temporary state.
#
# Hook Type: SessionEnd
# Output: Session summary

set -e

STATE_DIR=".claude/state"
METRICS_DIR=".claude/metrics"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SESSION_FILE="$METRICS_DIR/session_${TIMESTAMP}.json"

# Ensure metrics directory exists
mkdir -p "$METRICS_DIR"

# Collect session metrics
session_start=""
if [ -f "$STATE_DIR/session_start.json" ]; then
    session_start=$(cat "$STATE_DIR/session_start.json" | grep -o '"timestamp":[^,}]*' | cut -d'"' -f4 2>/dev/null || echo "")
fi

# Count completed work items
completed_items=0
if [ -f "LOOP_STATE.md" ]; then
    completed_items=$(grep -c "✅\|Done\|Completed" LOOP_STATE.md 2>/dev/null || echo "0")
fi

# Count agents used
agents_used=0
if [ -f "$STATE_DIR/agent_results.json" ]; then
    agents_used=$(grep -c '"agent_id"' "$STATE_DIR/agent_results.json" 2>/dev/null || echo "0")
fi

# Count files changed (if git available)
files_changed=0
if command -v git &> /dev/null && git rev-parse --git-dir > /dev/null 2>&1; then
    files_changed=$(git diff --name-only HEAD~1 2>/dev/null | wc -l || echo "0")
fi

# Write session metrics
cat > "$SESSION_FILE" << EOF
{
    "session_end": "$TIMESTAMP",
    "session_start": "$session_start",
    "completed_items": $completed_items,
    "agents_used": $agents_used,
    "files_changed": $files_changed
}
EOF

# Clean up temporary state files
rm -f "$STATE_DIR/active_agents.json" 2>/dev/null || true
rm -f "$STATE_DIR/agent_results.json" 2>/dev/null || true
rm -f "$STATE_DIR/session_start.json" 2>/dev/null || true

# Update session history
HISTORY_FILE=".claude/context/SESSION_HISTORY.md"
if [ -f "$HISTORY_FILE" ]; then
    echo "" >> "$HISTORY_FILE"
    echo "## Session $TIMESTAMP" >> "$HISTORY_FILE"
    echo "- Completed items: $completed_items" >> "$HISTORY_FILE"
    echo "- Agents used: $agents_used" >> "$HISTORY_FILE"
    echo "- Files changed: $files_changed" >> "$HISTORY_FILE"
fi

# Output summary
echo "[Session End] Session completed at $TIMESTAMP" >&2
echo "  Completed items: $completed_items" >&2
echo "  Agents used: $agents_used" >&2
echo "  Files changed: $files_changed" >&2
echo "  Metrics saved: $SESSION_FILE" >&2

exit 0
