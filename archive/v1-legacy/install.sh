#!/bin/bash
# Claude Code Template Installer
# Usage: ./install.sh [target-directory]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get script directory (where the template lives)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_DIR="$SCRIPT_DIR/template/.claude"

# Target directory (default: current directory)
TARGET_DIR="${1:-.}"
TARGET_CLAUDE="$TARGET_DIR/.claude"

echo -e "${GREEN}Claude Code Template Installer${NC}"
echo "================================"
echo ""

# Check if template exists
if [ ! -d "$TEMPLATE_DIR" ]; then
    echo -e "${RED}Error: Template not found at $TEMPLATE_DIR${NC}"
    exit 1
fi

# Check if target already has .claude
if [ -d "$TARGET_CLAUDE" ]; then
    echo -e "${YELLOW}Warning: .claude folder already exists in $TARGET_DIR${NC}"
    read -p "Overwrite? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 0
    fi
    rm -rf "$TARGET_CLAUDE"
fi

# Copy template
echo "Copying template to $TARGET_CLAUDE..."
cp -r "$TEMPLATE_DIR" "$TARGET_CLAUDE"

# Copy project state files if they don't exist
if [ ! -f "$TARGET_DIR/STATUS.md" ]; then
    echo "Creating STATUS.md..."
    cp "$SCRIPT_DIR/template/STATUS.md" "$TARGET_DIR/STATUS.md"
fi

if [ ! -f "$TARGET_DIR/CHANGELOG.md" ]; then
    echo "Creating CHANGELOG.md..."
    cp "$SCRIPT_DIR/template/CHANGELOG.md" "$TARGET_DIR/CHANGELOG.md"
fi

if [ ! -f "$TARGET_DIR/KNOWN_ISSUES.md" ]; then
    echo "Creating KNOWN_ISSUES.md..."
    cp "$SCRIPT_DIR/template/KNOWN_ISSUES.md" "$TARGET_DIR/KNOWN_ISSUES.md"
fi

# Update the prompts library path if needed
CLAUDE_MD="$TARGET_CLAUDE/CLAUDE.md"
if [ -f "$CLAUDE_MD" ]; then
    # Detect OS for sed compatibility
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s|C:\\\\scripts\\\\prompts\\\\|$SCRIPT_DIR/|g" "$CLAUDE_MD"
    else
        # Linux/Windows Git Bash
        sed -i "s|C:\\\\scripts\\\\prompts\\\\|$SCRIPT_DIR/|g" "$CLAUDE_MD"
    fi
fi

echo ""
echo -e "${GREEN}✓ Template installed successfully!${NC}"
echo ""
echo "Next steps (run in your terminal):"
echo ""
echo "  ${YELLOW}cd $TARGET_DIR${NC}"
echo "  ${YELLOW}claude --init${NC}"
echo ""
echo "Then, inside Claude Code, type:"
echo ""
echo "  ${GREEN}initialize this project${NC}"
echo ""
echo "This will automatically install skills and generate project context."
echo ""
