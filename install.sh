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
cp "$TEMP_DIR"/.claude/commands/cs-*.md .claude/commands/

echo "Installing profiles..."
mkdir -p profiles
cp "$TEMP_DIR"/profiles/*.yaml profiles/

echo "Installing rules..."
mkdir -p rules
cp "$TEMP_DIR"/rules/*.md rules/

echo "Installing templates..."
mkdir -p templates
cp "$TEMP_DIR"/templates/*.md templates/
cp "$TEMP_DIR"/templates/settings.json templates/ 2>/dev/null || true

echo "Installing hooks..."
mkdir -p .claude/hooks
cp "$TEMP_DIR"/.claude/hooks/*.js .claude/hooks/
cp "$TEMP_DIR"/.claude/hooks/README.md .claude/hooks/
echo "  Installed hook scripts"

echo "Installing settings..."
if [ ! -f ".claude/settings.json" ]; then
    cp "$TEMP_DIR"/.claude/settings.json .claude/settings.json
    echo "  Created .claude/settings.json with hooks"
else
    echo "  Preserved existing .claude/settings.json (review .claude/hooks/README.md to add hooks)"
fi

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
echo "  .claude/commands/cs-*.md  (9 commands)"
echo "  .claude/hooks/*.js        (10 hook scripts)"
echo "  .claude/settings.json     (hook configuration)"
echo "  profiles/*.yaml           (9 profiles)"
echo "  rules/*.md                (14 topic rules)"
echo "  templates/*.md            (4 templates)"
echo "  .claude/rules/learnings.md"
echo ""
echo "Next steps:"
echo "  1. Run /cs-validate to verify installation"
echo "  2. Run /cs-mcp --fix to register MCP servers"
echo "  3. Run /cs-status to see detected profile"
echo "  4. Run /cs-loop \"your task\" to start working"
echo ""
