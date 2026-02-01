#!/bin/bash
#
# MCP Server Setup Script for Claude Code v4.0 (macOS/Linux)
#
# Installs and configures MCP (Model Context Protocol) servers:
# - context7: Documentation lookup via Upstash
# - memory: Persistent memory across sessions
# - github: GitHub integration for issues, PRs, etc.
# - filesystem: Secure file operations with configurable access
# - puppeteer: Browser automation capabilities
#
# Usage:
#   ./setup-mcp-servers.sh
#   ./setup-mcp-servers.sh --skip-github
#   ./setup-mcp-servers.sh --github-token "ghp_xxxx"
#   ./setup-mcp-servers.sh --filesystem-dirs "/path/to/dir1,/path/to/dir2"
#   GITHUB_TOKEN="ghp_xxxx" ./setup-mcp-servers.sh
#
# Requirements: Node.js 18+, npm
#

set -e

# ============================================================================
# Configuration
# ============================================================================
SKIP_GITHUB=false
SKIP_FILESYSTEM=false
SKIP_PUPPETEER=false
SKIP_VERIFY=false
GITHUB_TOKEN_ARG=""
FILESYSTEM_DIRS=""
VERBOSE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-github)
            SKIP_GITHUB=true
            shift
            ;;
        --skip-filesystem)
            SKIP_FILESYSTEM=true
            shift
            ;;
        --skip-puppeteer)
            SKIP_PUPPETEER=true
            shift
            ;;
        --skip-verify)
            SKIP_VERIFY=true
            shift
            ;;
        --github-token)
            GITHUB_TOKEN_ARG="$2"
            shift 2
            ;;
        --filesystem-dirs)
            FILESYSTEM_DIRS="$2"
            shift 2
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --skip-github        Don't configure GitHub integration"
            echo "  --skip-filesystem    Don't configure filesystem server"
            echo "  --skip-puppeteer     Don't configure puppeteer server"
            echo "  --skip-verify        Skip verification step"
            echo "  --github-token       Provide GitHub token"
            echo "  --filesystem-dirs    Comma-separated directories for filesystem access"
            echo "  --verbose, -v        Verbose output"
            echo "  --help, -h           Show this help"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# ============================================================================
# Colors and Output Functions
# ============================================================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
GRAY='\033[0;90m'
NC='\033[0m' # No Color

step() {
    echo -e "\n${CYAN}==> $1${NC}"
}

success() {
    echo -e "  ${GREEN}[OK]${NC} $1"
}

warn() {
    echo -e "  ${YELLOW}[!]${NC} $1"
}

error() {
    echo -e "  ${RED}[X]${NC} $1"
}

info() {
    echo -e "  ${GRAY}$1${NC}"
}

# ============================================================================
# Banner
# ============================================================================
echo -e "${BLUE}"
cat << 'EOF'

╔══════════════════════════════════════════════════════════════════╗
║           MCP Server Setup for Claude Code v4.0                  ║
║                      macOS / Linux                                ║
╚══════════════════════════════════════════════════════════════════╝

EOF
echo -e "${NC}"

# ============================================================================
# STEP 1: Check Prerequisites
# ============================================================================
step "Checking prerequisites..."

# Check Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    NODE_MAJOR=$(echo "$NODE_VERSION" | sed 's/v\([0-9]*\).*/\1/')

    if [ "$NODE_MAJOR" -ge 18 ]; then
        success "Node.js $NODE_VERSION (>= 18 required)"
    else
        error "Node.js $NODE_VERSION is too old. Version 18+ required."
        info "Install via nvm: nvm install 18"
        info "Or download from: https://nodejs.org/"
        exit 1
    fi
else
    error "Node.js is not installed"
    info "Install via nvm: curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash"
    info "Or download from: https://nodejs.org/"
    exit 1
fi

# Check npm
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    success "npm $NPM_VERSION"
else
    error "npm is not installed"
    exit 1
fi

# Check Claude Code
if command -v claude &> /dev/null; then
    success "Claude Code installed"
else
    warn "Claude Code CLI not found in PATH"
    info "Install with: npm install -g @anthropic-ai/claude-code"
fi

# ============================================================================
# STEP 2: Create Claude Config Directory
# ============================================================================
step "Setting up Claude configuration directory..."

CLAUDE_CONFIG_DIR="$HOME/.claude"
if [ ! -d "$CLAUDE_CONFIG_DIR" ]; then
    mkdir -p "$CLAUDE_CONFIG_DIR"
    success "Created $CLAUDE_CONFIG_DIR"
else
    success "Config directory exists: $CLAUDE_CONFIG_DIR"
fi

# ============================================================================
# STEP 3: Pre-cache MCP Packages
# ============================================================================
step "Pre-caching MCP packages..."

info "This will download the following packages:"
info "  - @upstash/context7-mcp (documentation lookup)"
info "  - @modelcontextprotocol/server-memory (persistent memory)"
if [ "$SKIP_GITHUB" = false ]; then
    info "  - @modelcontextprotocol/server-github (GitHub integration)"
fi
if [ "$SKIP_FILESYSTEM" = false ]; then
    info "  - @modelcontextprotocol/server-filesystem (file operations)"
fi
if [ "$SKIP_PUPPETEER" = false ]; then
    info "  - @modelcontextprotocol/server-puppeteer (browser automation)"
fi
echo ""

# Pre-cache packages using npm cache add (doesn't run servers)
info "Caching packages (download only)..."

# Context7
info "  Caching context7..."
if npm cache add @upstash/context7-mcp@latest &> /dev/null; then
    success "context7 cached"
else
    warn "context7 will be downloaded on first use"
fi

# Memory
info "  Caching memory server..."
if npm cache add @modelcontextprotocol/server-memory &> /dev/null; then
    success "memory server cached"
else
    warn "memory server will be downloaded on first use"
fi

# GitHub
if [ "$SKIP_GITHUB" = false ]; then
    info "  Caching GitHub server..."
    if npm cache add @modelcontextprotocol/server-github &> /dev/null; then
        success "GitHub server cached"
    else
        warn "GitHub server will be downloaded on first use"
    fi
fi

# Filesystem
if [ "$SKIP_FILESYSTEM" = false ]; then
    info "  Caching filesystem server..."
    if npm cache add @modelcontextprotocol/server-filesystem &> /dev/null; then
        success "filesystem server cached"
    else
        warn "filesystem server will be downloaded on first use"
    fi
fi

# Puppeteer
if [ "$SKIP_PUPPETEER" = false ]; then
    info "  Caching puppeteer server..."
    if npm cache add @modelcontextprotocol/server-puppeteer &> /dev/null; then
        success "puppeteer server cached"
    else
        warn "puppeteer server will be downloaded on first use"
    fi
fi

# ============================================================================
# STEP 4: Configure GitHub Token (if needed)
# ============================================================================
if [ "$SKIP_GITHUB" = false ]; then
    step "Configuring GitHub integration..."

    # Check for token sources
    if [ -n "$GITHUB_TOKEN_ARG" ]; then
        info "Using provided GitHub token"
        GITHUB_TOKEN="$GITHUB_TOKEN_ARG"
    elif [ -n "$GITHUB_TOKEN" ]; then
        success "GITHUB_TOKEN already set in environment"
    else
        warn "No GitHub token found"
        echo ""
        echo -e "  ${NC}To use GitHub integration, you need a Personal Access Token:"
        info "  1. Go to https://github.com/settings/tokens"
        info "  2. Click 'Generate new token (classic)'"
        info "  3. Select scopes: repo, read:org, read:user"
        info "  4. Copy the token"
        echo ""

        read -p "  Enter your GitHub token (or press Enter to skip): " TOKEN_INPUT
        if [ -n "$TOKEN_INPUT" ]; then
            GITHUB_TOKEN="$TOKEN_INPUT"
        else
            warn "Skipping GitHub integration (no token provided)"
            SKIP_GITHUB=true
        fi
    fi

    if [ "$SKIP_GITHUB" = false ] && [ -n "$GITHUB_TOKEN" ]; then
        # Export for current session
        export GITHUB_TOKEN

        # Offer to persist the token
        echo ""
        read -p "  Add GITHUB_TOKEN to shell profile? (y/N): " PERSIST_ANSWER
        if [[ "$PERSIST_ANSWER" =~ ^[Yy]$ ]]; then
            # Detect shell profile
            SHELL_PROFILE=""
            if [ -f "$HOME/.zshrc" ]; then
                SHELL_PROFILE="$HOME/.zshrc"
            elif [ -f "$HOME/.bashrc" ]; then
                SHELL_PROFILE="$HOME/.bashrc"
            elif [ -f "$HOME/.bash_profile" ]; then
                SHELL_PROFILE="$HOME/.bash_profile"
            fi

            if [ -n "$SHELL_PROFILE" ]; then
                # Check if already exists
                if grep -q "GITHUB_TOKEN" "$SHELL_PROFILE"; then
                    warn "GITHUB_TOKEN already exists in $SHELL_PROFILE"
                    info "Please update it manually if needed"
                else
                    echo "" >> "$SHELL_PROFILE"
                    echo "# GitHub token for Claude Code MCP" >> "$SHELL_PROFILE"
                    echo "export GITHUB_TOKEN=\"$GITHUB_TOKEN\"" >> "$SHELL_PROFILE"
                    success "Added GITHUB_TOKEN to $SHELL_PROFILE"
                    info "Run 'source $SHELL_PROFILE' or restart terminal"
                fi
            else
                warn "Could not detect shell profile"
                info "Add manually: export GITHUB_TOKEN=\"$GITHUB_TOKEN\""
            fi
        fi
    fi
fi

# ============================================================================
# STEP 5: Configure Filesystem Directories
# ============================================================================
if [ "$SKIP_FILESYSTEM" = false ]; then
    step "Configuring filesystem access..."

    if [ -z "$FILESYSTEM_DIRS" ]; then
        # Default to home directory
        FILESYSTEM_DIRS="$HOME"
        info "Using default filesystem directory: $FILESYSTEM_DIRS"
        echo ""
        read -p "  Add additional directories? (comma-separated, or Enter for default): " EXTRA_DIRS
        if [ -n "$EXTRA_DIRS" ]; then
            FILESYSTEM_DIRS="$FILESYSTEM_DIRS,$EXTRA_DIRS"
        fi
    fi

    success "Filesystem directories: $FILESYSTEM_DIRS"
fi

# ============================================================================
# STEP 6: Create/Update Claude Code Settings
# ============================================================================
step "Configuring Claude Code MCP settings..."

SETTINGS_PATH="$CLAUDE_CONFIG_DIR/settings.json"

# Build filesystem args array
FS_ARGS='["-y", "@modelcontextprotocol/server-filesystem"'
if [ -n "$FILESYSTEM_DIRS" ]; then
    IFS=',' read -ra DIRS <<< "$FILESYSTEM_DIRS"
    for dir in "${DIRS[@]}"; do
        FS_ARGS="$FS_ARGS, \"$dir\""
    done
fi
FS_ARGS="$FS_ARGS]"

# Build MCP config JSON
MCP_CONFIG='{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"],
      "env": {}
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"],
      "env": {}
    }'

if [ "$SKIP_GITHUB" = false ]; then
    MCP_CONFIG="$MCP_CONFIG"',
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }'
fi

if [ "$SKIP_FILESYSTEM" = false ]; then
    MCP_CONFIG="$MCP_CONFIG"',
    "filesystem": {
      "command": "npx",
      "args": '"$FS_ARGS"',
      "env": {}
    }'
fi

if [ "$SKIP_PUPPETEER" = false ]; then
    MCP_CONFIG="$MCP_CONFIG"',
    "puppeteer": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-puppeteer"],
      "env": {}
    }'
fi

MCP_CONFIG="$MCP_CONFIG"'
  }
}'

# Check if jq is available for JSON merging
if command -v jq &> /dev/null; then
    if [ -f "$SETTINGS_PATH" ]; then
        info "Existing settings.json found"
        # Merge with existing settings
        EXISTING=$(cat "$SETTINGS_PATH")
        NEW_MCP=$(echo "$MCP_CONFIG" | jq '.mcpServers')

        # Backup existing
        cp "$SETTINGS_PATH" "$SETTINGS_PATH.backup"

        # Merge
        echo "$EXISTING" | jq --argjson mcp "$NEW_MCP" '.mcpServers = (.mcpServers // {}) + $mcp' > "$SETTINGS_PATH"
        success "Updated existing settings.json with MCP servers"
        info "Backup saved to $SETTINGS_PATH.backup"
    else
        echo "$MCP_CONFIG" | jq '.' > "$SETTINGS_PATH"
        success "Created new settings.json"
    fi
else
    # No jq - simple write (may overwrite existing)
    if [ -f "$SETTINGS_PATH" ]; then
        warn "jq not installed - creating backup and writing new settings"
        cp "$SETTINGS_PATH" "$SETTINGS_PATH.backup"
        info "Backup saved to $SETTINGS_PATH.backup"
        info "Install jq for better merging: brew install jq"
    fi
    echo "$MCP_CONFIG" > "$SETTINGS_PATH"
    success "Created settings.json"
fi

info "Settings file: $SETTINGS_PATH"

# ============================================================================
# STEP 7: Summary
# ============================================================================
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                    Setup Complete!                                ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${NC}MCP Servers Configured:${NC}"
echo -e "  ${GREEN}●${NC} context7    - Documentation lookup"
echo -e "  ${GREEN}●${NC} memory      - Persistent memory"

if [ "$SKIP_GITHUB" = false ]; then
    echo -e "  ${GREEN}●${NC} github      - GitHub integration"
else
    echo -e "  ${GRAY}○${NC} github      - Skipped"
fi

if [ "$SKIP_FILESYSTEM" = false ]; then
    echo -e "  ${GREEN}●${NC} filesystem  - File operations"
else
    echo -e "  ${GRAY}○${NC} filesystem  - Skipped"
fi

if [ "$SKIP_PUPPETEER" = false ]; then
    echo -e "  ${GREEN}●${NC} puppeteer   - Browser automation"
else
    echo -e "  ${GRAY}○${NC} puppeteer   - Skipped"
fi

echo ""
echo -e "${NC}Configuration file:${NC}"
echo -e "  ${GRAY}$SETTINGS_PATH${NC}"

echo ""
echo -e "${NC}Next Steps:${NC}"
echo -e "  ${GRAY}1. Restart Claude Code for changes to take effect${NC}"
echo -e "  ${GRAY}2. MCP servers will auto-start when needed${NC}"
echo -e "  ${GRAY}3. Use 'context7' for documentation lookups${NC}"
echo -e "  ${GRAY}4. Memory persists across sessions automatically${NC}"

if [ "$SKIP_GITHUB" = false ] && [ -z "$GITHUB_TOKEN" ]; then
    echo ""
    echo -e "${YELLOW}To enable GitHub integration later:${NC}"
    echo -e "  ${GRAY}export GITHUB_TOKEN='your_token_here'${NC}"
fi

echo ""
echo -e "${NC}For troubleshooting, see:${NC}"
echo -e "  ${GRAY}https://modelcontextprotocol.io/docs${NC}"
echo ""
