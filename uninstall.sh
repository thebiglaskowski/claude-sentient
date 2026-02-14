#!/usr/bin/env bash
set -euo pipefail

# Claude Sentient Uninstaller
# Cleanly removes claude-sentient from a project

KEEP_LEARNINGS=true
KEEP_SETTINGS=false
DRY_RUN=false

# Parse arguments
for arg in "$@"; do
    case $arg in
        --purge)
            KEEP_LEARNINGS=false
            ;;
        --keep-settings)
            KEEP_SETTINGS=true
            ;;
        --dry-run)
            DRY_RUN=true
            ;;
        --help|-h)
            echo "Usage: ./uninstall.sh [OPTIONS]"
            echo ""
            echo "Removes claude-sentient from the current project."
            echo ""
            echo "Options:"
            echo "  --purge          Remove everything including learnings.md"
            echo "  --keep-settings  Don't touch .claude/settings.json"
            echo "  --dry-run        Show what would be removed without removing"
            echo "  --help, -h       Show this help"
            exit 0
            ;;
        *)
            echo "Unknown option: $arg"
            echo "Run with --help for usage"
            exit 1
            ;;
    esac
done

echo "=== Claude Sentient Uninstaller ==="
echo ""

# Detect installation
if [ ! -f ".claude/commands/cs-loop.md" ]; then
    echo "Claude Sentient does not appear to be installed in this directory."
    exit 0
fi

if [ "$DRY_RUN" = true ]; then
    echo "[DRY RUN] Showing what would be removed..."
    echo ""
fi

# Confirm (skip for dry run)
if [ "$DRY_RUN" = false ]; then
    read -p "Remove Claude Sentient from this project? (y/N): " -n 1 -r < /dev/tty
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 0
    fi
    echo ""
fi

removed=0
backed_up=0

remove_file() {
    local file="$1"
    if [ -f "$file" ]; then
        if [ "$DRY_RUN" = true ]; then
            echo "  [remove] $file"
        else
            rm "$file"
        fi
        removed=$((removed + 1))
    fi
}

remove_dir() {
    local dir="$1"
    if [ -d "$dir" ]; then
        if [ "$DRY_RUN" = true ]; then
            echo "  [remove] $dir/"
        else
            rm -rf "$dir"
        fi
        removed=$((removed + 1))
    fi
}

remove_dir_if_empty() {
    local dir="$1"
    if [ -d "$dir" ] && [ -z "$(ls -A "$dir" 2>/dev/null)" ]; then
        if [ "$DRY_RUN" = true ]; then
            echo "  [remove] $dir/ (empty)"
        else
            rmdir "$dir"
        fi
    fi
}

# --- Shared test infrastructure ---
remove_file "test-utils.js"

# --- Commands ---
echo "Removing commands..."
for f in .claude/commands/cs-*.md; do
    [ -f "$f" ] && remove_file "$f"
done
remove_file ".claude/commands/CLAUDE.md"

# --- Hooks ---
echo "Removing hooks..."
for f in .claude/hooks/*.js; do
    [ -f "$f" ] && remove_file "$f"
done
remove_file ".claude/hooks/README.md"
remove_dir ".claude/hooks/__tests__"
remove_dir_if_empty ".claude/hooks"

# --- Profiles ---
echo "Removing profiles..."
remove_dir "profiles"

# --- Agents ---
echo "Removing agents..."
remove_dir "agents"

# --- Rules (project root) ---
echo "Removing rules..."
remove_dir "rules"

# --- Templates ---
echo "Removing templates..."
remove_dir "templates"

# --- Schemas ---
echo "Removing schemas..."
remove_dir "schemas"

# --- Path-scoped rules (.claude/rules/) ---
echo "Removing path-scoped rules..."
SCOPED_RULES=(
    security.md testing.md api-design.md database.md
    ui-ux-design.md error-handling.md performance.md logging.md
    terminal-ui.md documentation.md prompt-structure.md git-workflow.md
    anthropic-patterns.md code-quality.md README.md
)
for rule in "${SCOPED_RULES[@]}"; do
    remove_file ".claude/rules/$rule"
done

# --- Learnings ---
if [ "$KEEP_LEARNINGS" = true ]; then
    if [ -f ".claude/rules/learnings.md" ]; then
        echo "Preserving .claude/rules/learnings.md (use --purge to remove)"
    fi
else
    echo "Removing learnings..."
    remove_file ".claude/rules/learnings.md"
fi

# --- Settings ---
if [ "$KEEP_SETTINGS" = true ]; then
    if [ -f ".claude/settings.json" ]; then
        echo "Preserving .claude/settings.json (--keep-settings)"
    fi
else
    if [ -f ".claude/settings.json" ]; then
        echo "Backing up and removing settings..."
        if [ "$DRY_RUN" = true ]; then
            echo "  [backup] .claude/settings.json → .claude/settings.json.bak"
            echo "  [remove] .claude/settings.json"
        else
            cp ".claude/settings.json" ".claude/settings.json.bak"
            rm ".claude/settings.json"
            backed_up=$((backed_up + 1))
        fi
        removed=$((removed + 1))
    fi
fi

# --- State directory ---
remove_dir ".claude/state"

# --- Clean up empty directories ---
echo "Cleaning up..."
remove_dir_if_empty ".claude/rules"
remove_dir_if_empty ".claude/commands"
remove_dir_if_empty ".claude"

echo ""
echo "=== Uninstall Complete ==="
echo ""
echo "Removed $removed items."
if [ "$backed_up" -gt 0 ]; then
    echo "Backed up: .claude/settings.json → .claude/settings.json.bak"
fi
if [ "$KEEP_LEARNINGS" = true ] && [ -f ".claude/rules/learnings.md" ]; then
    echo "Preserved: .claude/rules/learnings.md"
fi
echo ""
echo "Note: CLAUDE.md was not modified. Remove it manually if desired."
echo ""
