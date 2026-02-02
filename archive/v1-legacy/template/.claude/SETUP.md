# Complete Setup Guide

Everything you need to set up Claude Code with this template, from scratch.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [API Key Setup](#api-key-setup)
3. [Install Claude Code CLI](#install-claude-code-cli)
4. [Install Template to Project](#install-template-to-project)
5. [GitHub Actions Setup](#github-actions-setup)
6. [MCP Servers Setup](#mcp-servers-setup)
7. [Plugins Setup](#plugins-setup)
8. [Verification](#verification)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required

| Tool | Version | Check Command | Install |
|------|---------|---------------|---------|
| Node.js | 18+ | `node --version` | [nodejs.org](https://nodejs.org) |
| npm | 8+ | `npm --version` | Comes with Node.js |
| Git | 2.0+ | `git --version` | [git-scm.com](https://git-scm.com) |

### Optional (for specific features)

| Tool | Required For | Install |
|------|--------------|---------|
| Python 3.8+ | Python projects, some MCP servers | [python.org](https://python.org) |
| Prettier | Auto-formatting JS/TS | `npm install -g prettier` |
| GitHub CLI | `/scout-skills`, GitHub Actions | [cli.github.com](https://cli.github.com) |

---

## API Key Setup

### Step 1: Get Anthropic API Key

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign in or create an account
3. Navigate to **API Keys**
4. Click **Create Key**
5. Copy the key (starts with `sk-ant-...`)

> **Important:** Save this key securely. You won't be able to see it again.

### Step 2: Set Environment Variable

The API key must be available as `ANTHROPIC_API_KEY`.

#### Windows (PowerShell - Permanent)

```powershell
# Set for current user (persists across sessions)
[Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-ant-your-key-here", "User")

# Restart terminal for changes to take effect
```

#### Windows (CMD - Session Only)

```cmd
set ANTHROPIC_API_KEY=sk-ant-your-key-here
```

#### macOS/Linux (Permanent)

```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'export ANTHROPIC_API_KEY="sk-ant-your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

#### macOS/Linux (Session Only)

```bash
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

### Step 3: Verify API Key

```bash
# Should not show "not set" error
echo $ANTHROPIC_API_KEY  # macOS/Linux
echo %ANTHROPIC_API_KEY% # Windows CMD
$env:ANTHROPIC_API_KEY   # Windows PowerShell
```

---

## Install Claude Code CLI

### Option A: npm (Recommended)

```bash
npm install -g @anthropic-ai/claude-code
```

### Option B: Direct Download

Visit [Claude Code releases](https://github.com/anthropics/claude-code/releases) and download for your platform.

### Verify Installation

```bash
claude --version
```

Expected output: `claude-code version X.X.X`

---

## Install Template to Project

### Option A: Install Script (Recommended)

```bash
# Navigate to prompts library
cd /path/to/prompts

# Run installer
./install.sh /path/to/your/project

# Windows PowerShell
.\install.ps1 -TargetDir "C:\path\to\your\project"
```

### Option B: Manual Copy

```bash
# Copy .claude folder
cp -r /path/to/prompts/template/.claude your-project/.claude

# Copy project state files
cp /path/to/prompts/template/STATUS.md your-project/
cp /path/to/prompts/template/CHANGELOG.md your-project/
cp /path/to/prompts/template/KNOWN_ISSUES.md your-project/

# Copy GitHub Actions (optional)
mkdir -p your-project/.github/workflows
cp -r /path/to/prompts/template/.github/workflows/* your-project/.github/workflows/
```

### Initialize Project

```bash
# Start Claude Code
cd your-project
claude

# Inside Claude Code, say:
# "initialize this project"
```

---

## GitHub Actions Setup

The template includes two GitHub Actions workflows for automated code review and security scanning.

### Step 1: Copy Workflows to Your Repository

```bash
# From your project root
mkdir -p .github/workflows
cp /path/to/prompts/template/.github/workflows/*.yml .github/workflows/
```

### Step 2: Add Repository Secret

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `ANTHROPIC_API_KEY`
5. Value: Your API key (same one from earlier)
6. Click **Add secret**

### Step 3: Verify Workflows

After pushing to your repository:

1. Go to **Actions** tab
2. You should see:
   - **Claude Code Review** - Triggers on PRs
   - **Claude Security Scan** - Triggers on push to main and PRs

### Workflow Configuration

#### claude-review.yml

| Setting | Default | Description |
|---------|---------|-------------|
| Trigger | PR open/sync | When workflow runs |
| File types | js, ts, py, go, rs, java, rb | Files that trigger review |
| Blocking | Warn on S0/S1 | Optionally fail on critical issues |

#### security-scan.yml

| Setting | Default | Description |
|---------|---------|-------------|
| Trigger | Push to main, PRs | When workflow runs |
| Manual trigger | Yes | Can run with custom scope |
| Blocking | Fail on S0 | Fails build on critical vulnerabilities |

### Cost Considerations

Each workflow run uses API tokens. To manage costs:

```yaml
# In workflow file, add token limit
env:
  CLAUDE_MAX_TOKENS: 4000  # Limit tokens per run
```

Or limit which files trigger workflows:

```yaml
paths:
  - 'src/**'  # Only src folder changes
  - '!**/*.test.*'  # Exclude test files
```

---

## MCP Servers Setup

MCP servers extend Claude Code with external tools. See `MCP_SERVERS.md` for complete guide.

### Quick Setup: Context7 (Documentation Lookup)

1. Create/edit `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@context7/mcp-server"]
    }
  }
}
```

2. Restart Claude Code

### Quick Setup: GitHub Integration

1. Create GitHub personal access token at [github.com/settings/tokens](https://github.com/settings/tokens)
2. Add to settings.json:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_your_token_here"
      }
    }
  }
}
```

---

## Plugins Setup

Plugins extend Claude Code with additional capabilities. See `PLUGINS.md` for complete guide.

### Quick Setup: Supermemory (Persistent Memory)

Supermemory gives Claude persistent memory across sessions.

**Step 1: Get API Key**

1. Go to [console.supermemory.ai](https://console.supermemory.ai)
2. Sign up (requires Pro plan or above)
3. Create an API key (starts with `sm_`)

**Step 2: Set Environment Variable**

**Windows (PowerShell - Permanent):**
```powershell
[Environment]::SetEnvironmentVariable("SUPERMEMORY_CC_API_KEY", "sm_your_key_here", "User")
```

**macOS/Linux (Permanent):**
```bash
echo 'export SUPERMEMORY_CC_API_KEY="sm_your_key_here"' >> ~/.zshrc
source ~/.zshrc
```

**Step 3: Install Plugin**

```bash
claude plugin marketplace add supermemoryai/claude-supermemory
claude plugin install claude-supermemory
```

**Step 4: Restart Claude Code**

Close and reopen for the plugin to activate.

**Step 5: Index Codebase (Optional)**

Inside Claude Code:
```
/claude-supermemory:index
```

---

## Verification

### Checklist

Run through this checklist to verify everything is set up:

```
□ API Key
  □ ANTHROPIC_API_KEY environment variable set
  □ Key starts with "sk-ant-"

□ Claude Code CLI
  □ `claude --version` shows version number
  □ `claude` command opens Claude Code

□ Template Installation
  □ .claude/ folder exists in project
  □ .claude/CLAUDE.md exists
  □ .claude/commands/ has .md files
  □ .claude/skills/ has .md files

□ GitHub Actions (if using)
  □ ANTHROPIC_API_KEY secret added to repository
  □ .github/workflows/ contains workflow files
  □ Actions tab shows workflows

□ MCP Servers (if using)
  □ ~/.claude/settings.json exists
  □ Required tokens/credentials set

□ Plugins (if using)
  □ SUPERMEMORY_CC_API_KEY environment variable set
  □ Plugin installed: claude plugin list shows enabled
```

### Test Commands

```bash
# Test Claude Code
cd your-project
claude

# Inside Claude Code:
# 1. Check template loaded
/help

# 2. Test a command
/assess

# 3. Check skills
scout-skills --dry-run
```

---

## Troubleshooting

### "ANTHROPIC_API_KEY not set"

**Cause:** Environment variable not found.

**Fix:**
1. Verify key is set: `echo $ANTHROPIC_API_KEY`
2. If empty, set it (see [API Key Setup](#api-key-setup))
3. Restart terminal
4. Try again

### "claude: command not found"

**Cause:** Claude Code CLI not installed or not in PATH.

**Fix:**
```bash
# Reinstall
npm install -g @anthropic-ai/claude-code

# If still not found, check npm global bin
npm bin -g
# Add that path to your PATH environment variable
```

### GitHub Actions failing with "API key invalid"

**Cause:** Secret not set correctly or key is invalid.

**Fix:**
1. Go to repository Settings → Secrets → Actions
2. Delete existing ANTHROPIC_API_KEY secret
3. Create new secret with correct key
4. Re-run workflow

### MCP Server not connecting

**Cause:** Configuration error or missing dependencies.

**Fix:**
1. Check settings.json syntax (valid JSON)
2. Verify paths and commands exist
3. Check environment variables are set
4. Restart Claude Code
5. See `MCP_SERVERS.md` for server-specific troubleshooting

### "Permission denied" on install script

**Cause:** Script not executable.

**Fix:**
```bash
chmod +x install.sh
./install.sh /path/to/project
```

---

## Quick Reference

| What | Where | Format |
|------|-------|--------|
| API Key (local) | Environment variable | `ANTHROPIC_API_KEY=sk-ant-...` |
| API Key (CI/CD) | GitHub Secrets | Repository → Settings → Secrets |
| MCP Config (global) | `~/.claude/settings.json` | JSON |
| MCP Config (project) | `.claude/settings.json` | JSON |
| GitHub Token | GitHub Settings | Personal Access Token |

---

## Getting Help

- **Documentation:** `.claude/` folder contains all guides
- **Troubleshooting:** `.claude/TROUBLESHOOTING.md`
- **Configuration:** `.claude/CONFIGURATION.md`
- **MCP Servers:** `.claude/MCP_SERVERS.md`
