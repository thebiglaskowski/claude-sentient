# Claude Code Plugins Guide

Plugins extend Claude Code with additional capabilities beyond MCP servers.

---

## Table of Contents

1. [Understanding Plugins](#understanding-plugins)
2. [Plugin Management](#plugin-management)
3. [Available Plugins](#available-plugins)
4. [Supermemory Setup](#supermemory-setup)
5. [Troubleshooting](#troubleshooting)

---

## Understanding Plugins

### Plugins vs MCP Servers

| Feature | Plugins | MCP Servers |
|---------|---------|-------------|
| Purpose | Extend Claude Code behavior | Connect to external services |
| Installation | `claude plugin install` | Configure in settings.json |
| Hooks | Can hook into session lifecycle | No lifecycle hooks |
| Skills | Can add custom skills | Provide tools only |
| Examples | Supermemory, custom workflows | Context7, GitHub, databases |

### How Plugins Work

```
┌─────────────────────────────────────────────────────────┐
│                     Claude Code                          │
├─────────────────────────────────────────────────────────┤
│  Hooks:                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ SessionStart │  │ PromptSubmit │  │    Stop      │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                 │                 │          │
│         ▼                 ▼                 ▼          │
│  ┌─────────────────────────────────────────────────┐   │
│  │              Plugin (e.g., Supermemory)         │   │
│  │  • Injects context on session start            │   │
│  │  • Captures conversations                       │   │
│  │  • Creates summaries on stop                   │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## Plugin Management

### List Installed Plugins

```bash
claude plugin list
```

### Install a Plugin

```bash
# From marketplace
claude plugin marketplace add <repo>
claude plugin install <plugin-name>

# Example
claude plugin marketplace add supermemoryai/claude-supermemory
claude plugin install claude-supermemory
```

### Enable/Disable Plugins

```bash
claude plugin disable <plugin-name>
claude plugin enable <plugin-name>
```

### Update a Plugin

```bash
claude plugin update <plugin-name>
```

### Uninstall a Plugin

```bash
claude plugin uninstall <plugin-name>
```

### Manage Marketplaces

```bash
# List marketplaces
claude plugin marketplace list

# Add marketplace
claude plugin marketplace add <github-repo>

# Remove marketplace
claude plugin marketplace remove <name>

# Update marketplace
claude plugin marketplace update [name]
```

---

## Available Plugins

### Supermemory (Persistent Memory) ⭐ Recommended

Gives Claude persistent memory across sessions using Supermemory's AI memory service.

| Feature | Description |
|---------|-------------|
| Context Injection | Loads relevant memories on session start |
| Auto Capture | Captures conversation turns automatically |
| Session Summaries | Creates summaries when sessions end |
| Super Search | Skill to search past work and sessions |
| Codebase Indexing | Index project architecture and patterns |

**Requires:** [Supermemory Pro](https://console.supermemory.ai/billing) subscription

---

## Supermemory Setup

### Step 1: Get API Key

1. Go to [console.supermemory.ai](https://console.supermemory.ai)
2. Sign up or log in
3. Navigate to API Keys
4. Create a new key (starts with `sm_`)

### Step 2: Set Environment Variable

#### Windows (PowerShell - Permanent)

```powershell
[Environment]::SetEnvironmentVariable("SUPERMEMORY_CC_API_KEY", "sm_your_key_here", "User")
```

#### macOS/Linux (Permanent)

```bash
echo 'export SUPERMEMORY_CC_API_KEY="sm_your_key_here"' >> ~/.zshrc
source ~/.zshrc
```

### Step 3: Install Plugin

```bash
# Add the marketplace
claude plugin marketplace add supermemoryai/claude-supermemory

# Install the plugin
claude plugin install claude-supermemory

# Verify installation
claude plugin list
```

### Step 4: Restart Claude Code

Close and reopen Claude Code for the plugin hooks to activate.

### Step 5: Index Your Codebase (Optional)

Inside Claude Code:
```
/claude-supermemory:index
```

This indexes your project's architecture, patterns, and conventions into memory.

### Using Supermemory

Once installed, Supermemory works automatically:

| When | What Happens |
|------|--------------|
| Session start | Relevant memories loaded into context |
| After prompts | Conversation captured |
| After tool use | Observations captured (Edit, Write, Bash, Task) |
| Session end | Summary created |

**To search memories:**
```
"What did we work on last week?"
"Search my memories for authentication"
"What decisions did we make about the database?"
```

### Configuration (Optional)

Create `~/.supermemory-claude/settings.json`:

```json
{
  "skipTools": ["Read", "Glob", "Grep", "TodoWrite"],
  "captureTools": ["Edit", "Write", "Bash", "Task"],
  "maxProfileItems": 5,
  "debug": false
}
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SUPERMEMORY_CC_API_KEY` | Yes | Your Supermemory API key |
| `SUPERMEMORY_SKIP_TOOLS` | No | Comma-separated tools to not capture |
| `SUPERMEMORY_DEBUG` | No | Enable debug logging |

---

## Troubleshooting

### Plugin Not Found

**Symptom:** `claude plugin install` says plugin not found

**Solutions:**
1. Add the marketplace first:
   ```bash
   claude plugin marketplace add supermemoryai/claude-supermemory
   ```
2. Check marketplace was added:
   ```bash
   claude plugin marketplace list
   ```

### Plugin Installed But Not Working

**Symptom:** Plugin shows as enabled but features don't work

**Solutions:**
1. Restart Claude Code (plugins load at startup)
2. Check API key is set:
   ```powershell
   # Windows
   $env:SUPERMEMORY_CC_API_KEY
   ```
   ```bash
   # macOS/Linux
   echo $SUPERMEMORY_CC_API_KEY
   ```
3. Verify plugin status:
   ```bash
   claude plugin list
   ```

### API Key Not Recognized

**Symptom:** "Unauthorized" or "Invalid API key" errors

**Solutions:**
1. Verify key starts with `sm_`
2. Check environment variable is set correctly
3. Restart terminal after setting variable
4. On Windows, may need to restart computer

### Memories Not Loading

**Symptom:** Session starts without memory context

**Solutions:**
1. Check Supermemory has indexed content
2. Run `/claude-supermemory:index` to index codebase
3. Have a few conversations first to build up memories
4. Check debug logs: `SUPERMEMORY_DEBUG=true`

### Plugin Conflicts

**Symptom:** Multiple plugins causing issues

**Solutions:**
1. Disable plugins one by one to identify conflict
2. Check plugin versions are compatible
3. Report issues to plugin maintainers

---

## Quick Reference

### Commands

| Command | Purpose |
|---------|---------|
| `claude plugin list` | List installed plugins |
| `claude plugin install <name>` | Install a plugin |
| `claude plugin uninstall <name>` | Remove a plugin |
| `claude plugin enable <name>` | Enable a disabled plugin |
| `claude plugin disable <name>` | Disable a plugin |
| `claude plugin update <name>` | Update a plugin |
| `claude plugin marketplace list` | List marketplaces |
| `claude plugin marketplace add <repo>` | Add a marketplace |

### Supermemory Commands

| Command | Purpose |
|---------|---------|
| `/claude-supermemory:index` | Index your codebase |
| `/claude-supermemory:logout` | Clear credentials |

---

## Resources

- [Supermemory](https://supermemory.ai)
- [Supermemory Console](https://console.supermemory.ai)
- [claude-supermemory GitHub](https://github.com/supermemoryai/claude-supermemory)
- [Claude Code Plugins Documentation](https://docs.anthropic.com/claude-code/plugins)
