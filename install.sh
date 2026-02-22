#!/usr/bin/env bash
set -euo pipefail

# Claude Sentient Installer
# Installs claude-sentient into the current project

REPO_URL="https://github.com/thebiglaskowski/claude-sentient.git"
TEMP_DIR=".claude-sentient-temp"

FORCE_INSTALL=false
for arg in "$@"; do [[ "$arg" == "--force" ]] && FORCE_INSTALL=true; done

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
    # Read from /dev/tty so the prompt works when piped via curl | bash
    read -p "Reinstall/update? (y/N): " -n 1 -r < /dev/tty
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 0
    fi
fi

echo ""
echo "Downloading claude-sentient..."
# Clean up any leftover temp directory from a previous run
rm -rf "$TEMP_DIR"
git clone --depth 1 --quiet "$REPO_URL" "$TEMP_DIR"

# Verify file integrity
if [ -f "$TEMP_DIR/CHECKSUMS.sha256" ]; then
    echo "Verifying file integrity..."
    if (cd "$TEMP_DIR" && sha256sum -c CHECKSUMS.sha256 --quiet 2>/dev/null); then
        echo "✓ All file checksums verified"
    else
        if [ "$FORCE_INSTALL" = false ]; then
            echo "✗ Checksum verification failed. Use --force to bypass." >&2
            rm -rf "$TEMP_DIR"
            exit 1
        fi
        echo "⚠ Checksum mismatch — continuing (--force)" >&2
    fi
fi

echo "Installing shared test infrastructure..."
cp "$TEMP_DIR"/test-utils.js ./test-utils.js

echo "Installing commands..."
mkdir -p .claude/commands
cp "$TEMP_DIR"/.claude/commands/cs-*.md .claude/commands/
cp "$TEMP_DIR"/.claude/commands/CLAUDE.md .claude/commands/

echo "Installing profiles..."
mkdir -p profiles/__tests__
cp "$TEMP_DIR"/profiles/*.yaml profiles/
cp "$TEMP_DIR"/profiles/CLAUDE.md profiles/
cp "$TEMP_DIR"/profiles/__tests__/*.js profiles/__tests__/

echo "Installing rules..."
mkdir -p rules
cp "$TEMP_DIR"/rules/*.md rules/

echo "Installing templates..."
mkdir -p templates
cp "$TEMP_DIR"/templates/*.md templates/
cp "$TEMP_DIR"/templates/settings.json templates/ 2>/dev/null || true

echo "Installing hooks..."
mkdir -p .claude/hooks/__tests__
cp "$TEMP_DIR"/.claude/hooks/*.cjs .claude/hooks/
cp "$TEMP_DIR"/.claude/hooks/README.md .claude/hooks/
cp "$TEMP_DIR"/.claude/hooks/__tests__/*.js .claude/hooks/__tests__/
echo "  Installed hook scripts + tests"

echo "Installing agents..."
mkdir -p agents/__tests__
cp "$TEMP_DIR"/agents/*.yaml agents/
cp "$TEMP_DIR"/agents/CLAUDE.md agents/
cp "$TEMP_DIR"/agents/__tests__/*.js agents/__tests__/
echo "  Installed agent definitions + tests"

echo "Installing native agents..."
mkdir -p .claude/agents
cp "$TEMP_DIR"/.claude/agents/*.md .claude/agents/
echo "  Installed native agent definitions (.claude/agents/*.md)"

echo "Installing skills..."
for skill_dir in "$TEMP_DIR"/.claude/skills/*/; do
    skill_name=$(basename "$skill_dir")
    mkdir -p ".claude/skills/$skill_name"
    cp "$skill_dir"SKILL.md ".claude/skills/$skill_name/"
done
echo "  Installed skills (.claude/skills/)"

echo "Installing schemas..."
mkdir -p schemas/__tests__
cp "$TEMP_DIR"/schemas/*.json schemas/
cp "$TEMP_DIR"/schemas/__tests__/*.js schemas/__tests__/
echo "  Installed JSON schemas + tests"

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

echo "Installing path-scoped rules..."
for rule in "$TEMP_DIR"/.claude/rules/*.md; do
    rulename=$(basename "$rule")
    if [ "$rulename" != "learnings.md" ] && [ "$rulename" != "README.md" ]; then
        cp "$rule" ".claude/rules/$rulename"
    fi
done
echo "  Installed path-scoped rules to .claude/rules/"

echo "Cleaning up..."
rm -rf "$TEMP_DIR"

# --- Plugins ---
PLUGINS_INSTALLED=""
if command -v claude &>/dev/null; then
    echo ""
    echo "Installing Claude Code plugins..."

    # Universal: security-guidance (user scope)
    if claude plugin install security-guidance@claude-plugins-official --scope user 2>/dev/null; then
        echo "  ✓ security-guidance (user scope)"
        PLUGINS_INSTALLED="security-guidance"
    else
        echo "  ⚠ Could not install security-guidance plugin (non-fatal)"
    fi

    # Profile-dependent: LSP plugin (project scope)
    LSP_PLUGIN=""
    if [ -f "pyproject.toml" ] || [ -f "requirements.txt" ] || [ -f "setup.py" ]; then
        LSP_PLUGIN="pyright-lsp@claude-plugins-official"
    elif [ -f "tsconfig.json" ]; then
        LSP_PLUGIN="typescript-lsp@claude-plugins-official"
    elif [ -f "go.mod" ]; then
        LSP_PLUGIN="gopls-lsp@claude-plugins-official"
    elif [ -f "Cargo.toml" ]; then
        LSP_PLUGIN="rust-analyzer-lsp@claude-plugins-official"
    elif [ -f "pom.xml" ] || [ -f "build.gradle" ]; then
        LSP_PLUGIN="jdtls-lsp@claude-plugins-official"
    elif [ -f "CMakeLists.txt" ] || [ -f "Makefile" ]; then
        LSP_PLUGIN="clangd-lsp@claude-plugins-official"
    fi

    if [ -n "$LSP_PLUGIN" ]; then
        if claude plugin install "$LSP_PLUGIN" --scope project 2>/dev/null; then
            echo "  ✓ $LSP_PLUGIN (project scope)"
            PLUGINS_INSTALLED="${PLUGINS_INSTALLED:+$PLUGINS_INSTALLED, }$LSP_PLUGIN"
        else
            echo "  ⚠ Could not install $LSP_PLUGIN (non-fatal)"
        fi
    fi
else
    echo ""
    echo "⚠ claude CLI not found — skipping plugin installation"
    echo "  Install plugins manually after setting up Claude Code"
fi

# --- Global Permissions ---
echo ""
echo "Configuring global Claude Code permissions..."
PERMISSIONS_CONFIGURED=""
if command -v node &>/dev/null; then
    if node << 'NODEEOF'
const fs = require('fs'), path = require('path'), os = require('os');
const settingsPath = path.join(os.homedir(), '.claude', 'settings.json');
const ALLOW = ['Bash','Read','Write','Edit','Glob','Grep','Task','WebFetch','WebSearch',
  'NotebookEdit','ToolSearch','ListMcpResourcesTool','ReadMcpResourceTool',
  'TaskCreate','TaskUpdate','TaskList','TaskGet','TaskOutput','TaskStop',
  'TeamCreate','TeamDelete','SendMessage','Skill','AskUserQuestion','EnterPlanMode','ExitPlanMode'];
let s = {};
try { s = JSON.parse(fs.readFileSync(settingsPath, 'utf8')); } catch (_) {}
if (!s.permissions) s.permissions = {};
const existing = new Set(s.permissions.allow || []);
ALLOW.forEach(t => existing.add(t));
s.permissions.allow = [...existing];
fs.mkdirSync(path.dirname(settingsPath), { recursive: true });
fs.writeFileSync(settingsPath, JSON.stringify(s, null, 2) + '\n');
NODEEOF
    then
        echo "  ✓ ~/.claude/settings.json permissions configured"
        PERMISSIONS_CONFIGURED="true"
    else
        echo "  ⚠ Could not update global permissions (non-fatal)"
    fi
else
    echo "  ⚠ node not found — skipping global permissions setup"
    echo "    Manually add permissions.allow to ~/.claude/settings.json"
fi

echo ""
echo "=== Installation Complete ==="
echo ""
echo "Installed:"
echo "  .claude/commands/cs-*.md       (12 commands)"
echo "  .claude/hooks/*.cjs             (13 hook scripts)"
echo "  .claude/hooks/__tests__/       (235 hook tests)"
echo "  .claude/settings.json          (hook configuration)"
echo "  profiles/*.yaml                (9 profiles + schema)"
echo "  profiles/__tests__/            (242 profile tests)"
echo "  agents/*.yaml                  (6 agent roles)"
echo "  .claude/agents/*.md            (6 native agent definitions)"
echo "  agents/__tests__/              (108 agent tests)"
echo "  .claude/skills/                (3 skills)"
echo "  schemas/*.json                 (12 JSON schemas)"
echo "  schemas/__tests__/             (188 schema tests)"
echo "  rules/*.md                     (15 topic rules)"
echo "  templates/                     (4 templates + settings.json)"
echo "  test-utils.js                  (shared test infrastructure)"
echo "  .claude/rules/*.md              (15 path-scoped rules)"
if [ -n "$PLUGINS_INSTALLED" ]; then
    echo "  plugins                        ($PLUGINS_INSTALLED)"
fi
if [ -n "$PERMISSIONS_CONFIGURED" ]; then
    echo "  ~/.claude/settings.json        (global auto-approve permissions)"
fi
echo ""
echo "Recommended plugins (optional):"
echo "  claude plugin install pr-review-toolkit@claude-plugins-official"
echo "  claude plugin install ralph-loop@claude-plugins-official"
echo ""
echo "Next steps:"
echo "  1. Run /cs-validate to verify installation"
echo "  2. Run /cs-mcp --fix to register MCP servers"
echo "  3. Review recommended plugins above"
echo "  4. Run /cs-status to see detected profile"
echo "  5. Run /cs-loop \"your task\" to start working"
echo ""
