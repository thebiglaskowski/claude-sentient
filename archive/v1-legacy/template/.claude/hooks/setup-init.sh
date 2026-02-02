#!/bin/bash
# Setup Init Hook
#
# One-time project initialization for Claude Code.
# Creates required directories and default configuration.
#
# Hook Type: Setup
# Output: Initialization status

set -e

echo "[Setup] Initializing Claude Code environment..." >&2

# Create required directories
DIRS=(
    ".claude/state"
    ".claude/state/backups"
    ".claude/metrics"
    ".claude/feedback"
    ".claude/baselines"
)

for dir in "${DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        echo "  Created: $dir" >&2
    fi
done

# Create default state file
if [ ! -f ".claude/state/initialized.json" ]; then
    cat > ".claude/state/initialized.json" << EOF
{
    "initialized": "$(date -Iseconds)",
    "version": "3.0",
    "platform": "$(uname -s)"
}
EOF
    echo "  Created: .claude/state/initialized.json" >&2
fi

# Create .gitignore entries for Claude state
GITIGNORE=".gitignore"
CLAUDE_IGNORES=(
    ".claude/state/"
    ".claude/metrics/"
    ".claude/state/backups/"
)

if [ -f "$GITIGNORE" ]; then
    for ignore in "${CLAUDE_IGNORES[@]}"; do
        if ! grep -qF "$ignore" "$GITIGNORE" 2>/dev/null; then
            echo "$ignore" >> "$GITIGNORE"
            echo "  Added to .gitignore: $ignore" >&2
        fi
    done
fi

# Check for project context files
if [ ! -f "STATUS.md" ]; then
    echo "[Setup] Note: STATUS.md not found - consider running /map-project" >&2
fi

if [ ! -f "CHANGELOG.md" ]; then
    echo "[Setup] Note: CHANGELOG.md not found - will be created on first release" >&2
fi

echo "[Setup] Initialization complete" >&2

exit 0
