# MCP Servers - Complete Setup Guide

Model Context Protocol (MCP) servers extend Claude Code with external tools and services.

---

## Table of Contents

1. [Understanding MCP](#understanding-mcp)
2. [System-Wide vs Per-Project](#system-wide-vs-per-project)
3. [Prerequisites](#prerequisites)
4. [Step-by-Step Setup](#step-by-step-setup)
5. [Available MCP Servers](#available-mcp-servers)
6. [Environment Variables](#environment-variables)
7. [Troubleshooting](#troubleshooting)
8. [FAQ](#faq)

---

## Understanding MCP

### What is MCP?

MCP (Model Context Protocol) allows Claude Code to connect to external tools and services:
- **Databases** - Query PostgreSQL, SQLite, etc.
- **APIs** - GitHub, Slack, custom APIs
- **File Systems** - Access files outside the project
- **Memory** - Persistent storage across sessions
- **Documentation** - Live documentation lookup (Context7)

### How It Works

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Claude Code │ ←→  │ MCP Server  │ ←→  │  External   │
│             │     │  (Bridge)   │     │  Service    │
└─────────────┘     └─────────────┘     └─────────────┘
```

Claude Code communicates with MCP servers, which translate requests to external services.

---

## System-Wide vs Per-Project

### System-Wide Configuration (Recommended for Most Servers)

**Location:** `~/.claude/settings.json` (your home directory)

- Windows: `C:\Users\YourName\.claude\settings.json`
- macOS: `/Users/YourName/.claude/settings.json`
- Linux: `/home/YourName/.claude/settings.json`

**Use for:**
- Servers you want available in ALL projects
- Context7 (documentation lookup)
- GitHub (if using same account everywhere)
- Memory server

**Example:**
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

### Per-Project Configuration

**Locations (either works):**
- `your-project/.mcp.json` — In project root (common convention)
- `your-project/.claude/settings.json` — Inside .claude folder

**Note:** The `.mcp.json` file is often placed in the **project root** rather than inside `.claude/`. Both locations work—Claude Code checks both.

**Use for:**
- Project-specific databases
- Project-specific APIs
- Custom MCP servers for this project only

**Example:**
```json
{
  "mcpServers": {
    "project-db": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "postgresql://localhost:5432/myproject"
      }
    }
  }
}
```

### Precedence

If the same server is defined in both locations:
1. **Per-project config takes priority** over system-wide
2. Servers merge (you get servers from both)

---

## Prerequisites

### Required Software

#### 1. Node.js (Required for all MCP servers)

**Check if installed:**
```bash
node --version
# Should show v18.0.0 or higher
```

**Install Node.js:**

**Windows:**
```powershell
# Using winget
winget install OpenJS.NodeJS.LTS

# Or download from https://nodejs.org
```

**macOS:**
```bash
# Using Homebrew
brew install node

# Or download from https://nodejs.org
```

**Linux (Ubuntu/Debian):**
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

#### 2. npx (Included with Node.js)

**Verify:**
```bash
npx --version
```

---

## Step-by-Step Setup

### Step 1: Create Settings Directory

**Windows (PowerShell):**
```powershell
# Create .claude directory in your home folder
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude"

# Create empty settings file
New-Item -ItemType File -Force -Path "$env:USERPROFILE\.claude\settings.json"
```

**macOS/Linux:**
```bash
# Create .claude directory in your home folder
mkdir -p ~/.claude

# Create empty settings file
touch ~/.claude/settings.json
```

### Step 2: Open Settings File

**Windows:**
```powershell
notepad "$env:USERPROFILE\.claude\settings.json"
```

**macOS:**
```bash
open -e ~/.claude/settings.json
# Or use: code ~/.claude/settings.json (VS Code)
```

**Linux:**
```bash
nano ~/.claude/settings.json
# Or use: code ~/.claude/settings.json (VS Code)
```

### Step 3: Add MCP Server Configuration

Copy and paste this starter configuration:

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

### Step 4: Save and Restart Claude Code

1. Save the file
2. Close Claude Code completely
3. Reopen Claude Code
4. The MCP server should now be available

### Step 5: Verify Installation

In Claude Code, type:
```
use context7 to look up React hooks documentation
```

If Context7 is working, you'll get up-to-date documentation.

---

## Available MCP Servers

### Context7 (Documentation Lookup) ⭐ Recommended

Look up current library documentation and code examples.

**Configuration:**
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

**Usage in Claude Code:**
```
"use context7 to look up Next.js App Router documentation"
"use context7 to find React Query examples"
```

**Why use it:**
- Gets current documentation (Claude's training data may be outdated)
- Finds accurate code examples
- Checks for deprecated APIs

---

### GitHub

Direct GitHub API access for issues, PRs, and repositories.

**Step 1: Create GitHub Token**
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo`, `read:org`
4. Copy the token (starts with `ghp_`)

**Step 2: Set Environment Variable**

**Windows (PowerShell - Run as Administrator):**
```powershell
[Environment]::SetEnvironmentVariable("GITHUB_TOKEN", "ghp_your_token_here", "User")
```

**macOS/Linux:**
```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'export GITHUB_TOKEN="ghp_your_token_here"' >> ~/.zshrc
source ~/.zshrc
```

**Step 3: Add to settings.json:**
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

**Usage:**
```
"Create an issue in my-repo for the login bug"
"List open PRs in my-org/my-repo"
```

---

### Memory (Persistent Knowledge)

Store information that persists across Claude Code sessions.

**Configuration:**
```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
```

**Usage:**
```
"Remember that this project uses PostgreSQL 15"
"What did you remember about this project?"
```

**Use cases:**
- Store project conventions
- Remember user preferences
- Track decisions made in previous sessions

---

### Filesystem (Extended File Access)

Access files outside the current project directory.

**Configuration:**
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/path/to/allowed/directory"
      ]
    }
  }
}
```

**Important:** Only directories you specify in `args` are accessible.

**Windows example:**
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:\\Users\\YourName\\Documents",
        "C:\\Projects"
      ]
    }
  }
}
```

---

### PostgreSQL

Direct database queries.

**Step 1: Set Database URL**

**Windows:**
```powershell
[Environment]::SetEnvironmentVariable("DATABASE_URL", "postgresql://user:password@localhost:5432/dbname", "User")
```

**macOS/Linux:**
```bash
echo 'export DATABASE_URL="postgresql://user:password@localhost:5432/dbname"' >> ~/.zshrc
source ~/.zshrc
```

**Step 2: Add to settings.json:**
```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

**Usage:**
```
"Show me the users table schema"
"Query the last 10 orders"
```

**⚠️ Security:** Be careful with production databases. Use read-only credentials when possible.

---

### SQLite

Local SQLite database access.

**Configuration:**
```json
{
  "mcpServers": {
    "sqlite": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-sqlite",
        "./database.db"
      ]
    }
  }
}
```

Use absolute path for reliability:
```json
{
  "mcpServers": {
    "sqlite": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-sqlite",
        "C:\\Projects\\myapp\\database.db"
      ]
    }
  }
}
```

---

### Puppeteer (Browser Automation)

Web scraping and browser automation.

**Configuration:**
```json
{
  "mcpServers": {
    "puppeteer": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
    }
  }
}
```

**Note:** Requires Chrome/Chromium installed.

**Usage:**
```
"Take a screenshot of https://example.com"
"Scrape the product titles from this page"
```

---

## Environment Variables

### Why Use Environment Variables?

- **Security:** Tokens aren't stored in config files
- **Flexibility:** Easy to change without editing configs
- **Sharing:** Config files can be shared without exposing secrets

### Setting Environment Variables

#### Windows (Permanent)

**PowerShell (Run as Administrator):**
```powershell
# Set for current user
[Environment]::SetEnvironmentVariable("VARIABLE_NAME", "value", "User")

# Verify
[Environment]::GetEnvironmentVariable("VARIABLE_NAME", "User")
```

**Or via GUI:**
1. Search "Environment Variables" in Start menu
2. Click "Edit environment variables for your account"
3. Click "New" under User variables
4. Add name and value

#### macOS/Linux (Permanent)

**Add to shell config:**
```bash
# For zsh (default on macOS)
echo 'export VARIABLE_NAME="value"' >> ~/.zshrc
source ~/.zshrc

# For bash
echo 'export VARIABLE_NAME="value"' >> ~/.bashrc
source ~/.bashrc
```

### Referencing in Config

Use `${VARIABLE_NAME}` syntax:
```json
{
  "mcpServers": {
    "github": {
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

---

## Troubleshooting

### Server Not Starting

**Symptoms:** MCP commands don't work, "server not found" errors

**Solutions:**

1. **Check Node.js is installed:**
   ```bash
   node --version
   npm --version
   npx --version
   ```

2. **Check settings.json syntax:**
   - Valid JSON (no trailing commas)
   - Correct file path

3. **Check file location:**
   - System-wide: `~/.claude/settings.json`
   - Per-project: `.claude/settings.json`

4. **Restart Claude Code:**
   - Close completely and reopen
   - MCP servers load at startup

### Environment Variables Not Working

**Check variable is set:**

**Windows:**
```powershell
echo $env:GITHUB_TOKEN
```

**macOS/Linux:**
```bash
echo $GITHUB_TOKEN
```

**If empty:**
- Restart terminal after setting
- On Windows, may need to restart computer
- Check for typos in variable name

### Permission Errors

**Symptoms:** "Access denied", "Permission denied"

**Solutions:**
1. Check file/directory permissions
2. For GitHub: Verify token has required scopes
3. For filesystem: Verify path is in allowed list
4. For database: Check credentials are correct

### Server Crashes

**View logs:**
```bash
# Most MCP servers log to stderr
# Check Claude Code's output panel for errors
```

**Common causes:**
- Invalid configuration
- Missing dependencies
- Network issues (for remote services)

---

## FAQ

### Q: Do I need to install each MCP server separately?

**A:** No. Using `npx -y @package` automatically downloads and runs the server. The `-y` flag accepts prompts automatically.

### Q: Can I use multiple MCP servers at once?

**A:** Yes. Add multiple entries to `mcpServers`:
```json
{
  "mcpServers": {
    "context7": { ... },
    "github": { ... },
    "memory": { ... }
  }
}
```

### Q: Where should I put project-specific servers?

**A:** Either location works:
- `.mcp.json` in your **project root** (common convention)
- `.claude/settings.json` in your project

The project root `.mcp.json` is often preferred because it's more visible and easier to share with team members.

### Q: How do I remove an MCP server?

**A:** Remove its entry from settings.json and restart Claude Code.

### Q: Are MCP servers safe?

**A:** Official servers from `@modelcontextprotocol/*` are maintained by Anthropic. Third-party servers should be reviewed before use. Always use environment variables for secrets.

### Q: Do MCP servers use my API quota?

**A:** MCP servers themselves don't use Claude API quota. They provide tools that Claude can call during conversations.

### Q: Can I create my own MCP server?

**A:** Yes. See [MCP SDK documentation](https://modelcontextprotocol.io/docs/sdk).

---

## Complete Example Configuration

Here's a full system-wide configuration with multiple servers:

**~/.claude/settings.json:**
```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@context7/mcp-server"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
```

---

## Quick Reference

| Server | Purpose | Requires Token |
|--------|---------|----------------|
| context7 | Documentation lookup | No |
| github | GitHub API | Yes (GITHUB_TOKEN) |
| memory | Persistent storage | No |
| filesystem | File access | No |
| postgres | PostgreSQL queries | Yes (DATABASE_URL) |
| sqlite | SQLite queries | No |
| puppeteer | Browser automation | No |

---

## Resources

- [MCP Specification](https://modelcontextprotocol.io/)
- [Official MCP Servers](https://github.com/modelcontextprotocol/servers)
- [Context7](https://context7.com/)
- [Claude Code Documentation](https://docs.anthropic.com/claude-code)
