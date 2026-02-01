#!/bin/bash
# Pre-Compact Hook
#
# Backs up important state before context compaction.
# Saves session memory and loop state to preserve continuity.
#
# Hook Type: PreCompact
# Output: Backup confirmation

set -e

STATE_DIR=".claude/state"
BACKUP_DIR=".claude/state/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Ensure backup directory exists
mkdir -p "$BACKUP_DIR"

# Files to backup before compaction
FILES_TO_BACKUP=(
    "$STATE_DIR/active_agents.json"
    "$STATE_DIR/agent_results.json"
    "$STATE_DIR/session_memory.json"
    "LOOP_STATE.md"
    "STATUS.md"
)

backup_count=0

for file in "${FILES_TO_BACKUP[@]}"; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        cp "$file" "$BACKUP_DIR/${filename%.${file##*.}}_${TIMESTAMP}.${file##*.}"
        ((backup_count++))
    fi
done

# Write compaction marker
echo "{\"timestamp\": \"$TIMESTAMP\", \"files_backed_up\": $backup_count}" > "$STATE_DIR/last_compact.json"

# Output status
echo "[Pre-Compact] Backed up $backup_count state files" >&2
echo "[Pre-Compact] Backup location: $BACKUP_DIR" >&2

# Clean old backups (keep last 10)
cd "$BACKUP_DIR" 2>/dev/null && ls -t | tail -n +31 | xargs -r rm -- 2>/dev/null || true

exit 0
