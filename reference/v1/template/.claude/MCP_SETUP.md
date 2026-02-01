# MCP Server Setup Guide

Complete guide for setting up Model Context Protocol (MCP) servers with Claude Code v3.0.

---

## Overview

MCP servers extend Claude Code with additional capabilities:

| Server | Purpose | Use Case |
|--------|---------|----------|
| **context7** | Documentation lookup | Query up-to-date docs for libraries/frameworks |
| **memory** | Persistent memory | Remember information across sessions |
| **github** | GitHub integration | Work with issues, PRs, repos directly |

---

## Quick Start

### Windows (PowerShell)

```powershell
# Navigate to scripts directory
cd template\.claude\scripts

# Run setup (interactive)
.\setup-mcp-servers.ps1

# Or with GitHub token
.\setup-mcp-servers.ps1 -GitHubToken "ghp_your_token_here"

# Skip GitHub integration
.\setup-mcp-servers.ps1 -SkipGitHub
```

### macOS / Linux (Bash)

```bash
# Make script executable
chmod +x template/.claude/scripts/setup-mcp-servers.sh

# Run setup (interactive)
./template/.claude/scripts/setup-mcp-servers.sh

# Or with GitHub token
./setup-mcp-servers.sh --github-token "ghp_your_token_here"

# Skip GitHub integration
./setup-mcp-servers.sh --skip-github
```

---

## Prerequisites

### Required

| Requirement | Minimum Version | Check Command |
|-------------|-----------------|---------------|
| Node.js | 18.0+ | `node --version` |
| npm | 8.0+ | `npm --version` |

### Optional

| Requirement | Purpose |
|-------------|---------|
| Claude Code CLI | Run `claude` command |
| jq (macOS/Linux) | JSON merging in settings |
| GitHub Token | GitHub MCP server |

### Installing Node.js

**Windows:**
```powershell
# Using winget
winget install OpenJS.NodeJS.LTS

# Or download from https://nodejs.org/
```

**macOS:**
```bash
# Using Homebrew
brew install node@18

# Using nvm (recommended)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
nvm use 18
```

**Linux:**
```bash
# Using nvm (recommended)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 18
nvm use 18

# Or using package manager (Ubuntu/Debian)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

---

## Manual Setup

If you prefer to set up manually without scripts:

### Step 1: Create Config Directory

**Windows:**
```powershell
mkdir "$env:USERPROFILE\.claude" -Force
```

**macOS/Linux:**
```bash
mkdir -p ~/.claude
```

### Step 2: Create settings.json

Create/edit `~/.claude/settings.json`:

```json
{
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
    },
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

### Step 3: Set GitHub Token (Optional)

**Windows (PowerShell):**
```powershell
# Current session
$env:GITHUB_TOKEN = "ghp_your_token_here"

# Permanent (user level)
[Environment]::SetEnvironmentVariable("GITHUB_TOKEN", "ghp_your_token_here", "User")
```

**macOS/Linux:**
```bash
# Current session
export GITHUB_TOKEN="ghp_your_token_here"

# Permanent (add to ~/.bashrc or ~/.zshrc)
echo 'export GITHUB_TOKEN="ghp_your_token_here"' >> ~/.bashrc
source ~/.bashrc
```

### Step 4: Pre-cache Packages (Optional)

```bash
# Pre-download to speed up first use
npx -y @upstash/context7-mcp@latest --help
npx -y @modelcontextprotocol/server-memory --help
npx -y @modelcontextprotocol/server-github --help
```

---

## GitHub Token Setup

The GitHub MCP server requires a Personal Access Token (PAT).

### Creating a Token

1. Go to [GitHub Settings > Tokens](https://github.com/settings/tokens)
2. Click **"Generate new token (classic)"**
3. Set expiration (recommend 90 days)
4. Select scopes:
   - `repo` - Full repository access
   - `read:org` - Read org membership
   - `read:user` - Read user profile
5. Click **"Generate token"**
6. Copy the token immediately (won't be shown again)

### Token Scopes Reference

| Scope | Required For |
|-------|--------------|
| `repo` | Reading/writing issues, PRs, code |
| `read:org` | Listing organization repos |
| `read:user` | Getting user information |
| `workflow` | Triggering GitHub Actions (optional) |
| `read:project` | Reading project boards (optional) |

### Fine-Grained Tokens (Alternative)

For better security, use fine-grained tokens:

1. Go to [GitHub Settings > Fine-grained tokens](https://github.com/settings/tokens?type=beta)
2. Click **"Generate new token"**
3. Select repositories (all or specific)
4. Set permissions:
   - Repository: Read and Write
   - Issues: Read and Write
   - Pull requests: Read and Write
5. Generate and copy token

---

## Using MCP Servers

### Context7 (Documentation Lookup)

Query up-to-date documentation for any library:

```
User: "use context7 to look up React 18 useEffect best practices"
User: "check context7 for Next.js 14 app router documentation"
User: "use context7 to find TypeScript 5.0 new features"
```

**How it works:**
1. Claude queries the Context7 API
2. Retrieves latest documentation
3. Uses it to provide accurate answers

### Memory (Persistent Storage)

Store and retrieve information across sessions:

```
User: "remember that our API uses v2 endpoints"
User: "what did I tell you about our API?"
User: "store this: deployment requires VPN access"
```

**How it works:**
1. Claude stores facts in the memory server
2. Information persists between sessions
3. Can be queried later

### GitHub (Repository Integration)

Work directly with GitHub:

```
User: "list open issues in myorg/myrepo"
User: "create a PR for the current branch"
User: "show me the last 5 commits"
User: "what's the status of PR #123?"
```

**Capabilities:**
- List/create/update issues
- List/create/review pull requests
- Read repository contents
- View commit history
- Check CI/CD status

---

## Project-Level Configuration

For project-specific MCP settings, create `.claude/settings.json` in your project:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"],
      "env": {}
    }
  }
}
```

This overrides global settings for that project only.

---

## Troubleshooting

### MCP Server Not Starting

**Symptom:** "MCP server failed to start" error

**Solutions:**
1. Check Node.js version: `node --version` (need 18+)
2. Clear npm cache: `npm cache clean --force`
3. Reinstall package: `npx -y @upstash/context7-mcp@latest --help`
4. Check settings.json syntax (valid JSON)

### GitHub Token Not Working

**Symptom:** "Unauthorized" or "Bad credentials" error

**Solutions:**
1. Verify token is set: `echo $GITHUB_TOKEN` (Unix) or `echo $env:GITHUB_TOKEN` (PowerShell)
2. Check token hasn't expired on GitHub
3. Verify token has required scopes
4. Regenerate token if needed

### Context7 Queries Failing

**Symptom:** Documentation not found

**Solutions:**
1. Check library name spelling
2. Use official package names (e.g., `react` not `reactjs`)
3. Try more specific queries
4. Check internet connectivity

### Memory Not Persisting

**Symptom:** Stored facts not remembered

**Solutions:**
1. Check `~/.claude/memory/` directory exists
2. Verify write permissions
3. Check for disk space
4. Memory resets if server crashes - retry

### Settings Not Applied

**Symptom:** MCP servers not loading

**Solutions:**
1. Verify settings.json location:
   - Global: `~/.claude/settings.json`
   - Project: `.claude/settings.json`
2. Validate JSON syntax: `cat settings.json | jq .`
3. Restart Claude Code after changes
4. Check for conflicting settings files

---

## Verification Commands

### Check MCP Status

MCP servers run as stdio servers, not CLI tools. To verify they're installed:

```bash
# Verify packages can be resolved (downloads if needed)
npm show @upstash/context7-mcp version
npm show @modelcontextprotocol/server-memory version
npm show @modelcontextprotocol/server-github version

# Test GitHub token works (requires token)
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user
```

### Verify Inside Claude Code

The real test is using them in Claude Code:
```
"use context7 to look up React hooks"    → Should return documentation
"remember that this project uses Go"     → Should confirm stored
"list my GitHub repositories"            → Should list repos (if token set)
```

### Check Settings

**Windows:**
```powershell
Get-Content "$env:USERPROFILE\.claude\settings.json" | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

**macOS/Linux:**
```bash
cat ~/.claude/settings.json | jq .
```

---

## Security Considerations

### Token Security

- Never commit tokens to git
- Use environment variables, not hardcoded values
- Rotate tokens periodically (90 days recommended)
- Use fine-grained tokens when possible
- Revoke unused tokens

### .gitignore Recommendations

```gitignore
# Claude Code
.claude/state/
.claude/memory/
.claude/settings.local.json

# Never commit
*.token
*.secret
.env.local
```

### Environment Variable Security

**Windows:** User-level environment variables are stored in the registry and readable by processes running as your user.

**macOS/Linux:** Variables in shell profiles are readable by your user. For sensitive tokens, consider using a secrets manager or keychain.

---

## Advanced Configuration

### Custom MCP Server

Add your own MCP server:

```json
{
  "mcpServers": {
    "custom": {
      "command": "node",
      "args": ["/path/to/your/mcp-server.js"],
      "env": {
        "CUSTOM_API_KEY": "${CUSTOM_API_KEY}"
      }
    }
  }
}
```

### Conditional Loading

Use project-level settings to load different servers per project:

```
project-a/.claude/settings.json  → context7, memory
project-b/.claude/settings.json  → context7, github
```

### Debugging MCP

Enable verbose logging:

```bash
# Set debug environment
DEBUG=mcp:* claude

# Or in settings.json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"],
      "env": {
        "DEBUG": "1"
      }
    }
  }
}
```

---

## See Also

| Resource | Link |
|----------|------|
| MCP Specification | https://modelcontextprotocol.io |
| Claude Code Docs | https://docs.anthropic.com/claude-code |
| Context7 | https://github.com/upstash/context7-mcp |
| MCP Servers | https://github.com/modelcontextprotocol/servers |
| GitHub API | https://docs.github.com/en/rest |
