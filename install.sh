#!/usr/bin/env bash
set -euo pipefail

# Claude Sentient Installer
# Installs claude-sentient into the current project

REPO_URL="https://github.com/thebiglaskowski/claude-sentient.git"
TEMP_DIR=".claude-sentient-temp"

echo "=== Claude Sentient Installer ==="
echo ""

# Check if we're in a git repo (recommended but not required)
if [ -d ".git" ]; then
    echo "✓ Git repository detected"
else
    echo "⚠ Not a git repository (optional)"
fi

# Check if already installed
if [ -d ".claude/commands" ] && [ -f ".claude/commands/cs-loop.md" ]; then
    echo ""
    echo "⚠ Claude Sentient appears to be already installed."
    read -p "Reinstall/update? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 0
    fi
fi

echo ""
echo "Downloading claude-sentient..."
git clone --depth 1 --quiet "$REPO_URL" "$TEMP_DIR"

echo "Installing commands..."
mkdir -p .claude/commands
cp "$TEMP_DIR"/commands/cs-*.md .claude/commands/

echo "Installing profiles..."
mkdir -p profiles
cp "$TEMP_DIR"/profiles/*.yaml profiles/

echo "Installing templates..."
mkdir -p templates
cp "$TEMP_DIR"/templates/*.md templates/

echo "Initializing memory..."
mkdir -p .claude/rules
if [ ! -f ".claude/rules/learnings.md" ]; then
    cp "$TEMP_DIR"/templates/learnings.md .claude/rules/learnings.md
    echo "  Created .claude/rules/learnings.md"
else
    echo "  Preserved existing .claude/rules/learnings.md"
fi

echo "Cleaning up..."
rm -rf "$TEMP_DIR"

echo ""
echo "=== Installation Complete ==="
echo ""
echo "Installed:"
echo "  .claude/commands/cs-*.md  (5 commands)"
echo "  profiles/*.yaml           (5 profiles)"
echo "  templates/*.md            (4 templates)"
echo "  .claude/rules/learnings.md"
echo ""
echo "Next steps:"
echo "  1. Run /cs-validate to verify installation"
echo "  2. Run /cs-status to see detected profile"
echo "  3. Run /cs-loop \"your task\" to start working"
echo ""
