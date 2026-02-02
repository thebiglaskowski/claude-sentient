---
description: Check, register, and validate MCP servers
argument-hint: [--test] [--fix]
allowed-tools: Bash, Read, Glob, mcp__*
---

# /cs-mcp

Check MCP server status, auto-register missing servers, and validate connections.

## Arguments

| Arg | Purpose |
|-----|---------|
| `--test` | Test each connected server with a real call |
| `--fix` | Auto-register servers found in settings.json but not in `claude mcp` |

## Execution Flow

### Phase 1: Gather State

**1.1 Read settings.json for configured servers:**

```bash
# Locations to check (in order)
$HOME/.claude/settings.json     # User-level
.claude/settings.json           # Project-level
```

Parse the `mcpServers` key to find configured servers. Note the command, args, and env for each.

**1.2 Check registered servers:**

```bash
claude mcp list
```

This shows servers registered with Claude Code (not just configured in settings.json).

**1.3 Check enabled plugins:**

Look for `enabledPlugins` in settings.json. Plugins (like context7, claude-in-chrome) work differently than MCP servers.

### Phase 2: Compare & Report

**2.1 Build status table:**

For each server found in settings.json `mcpServers`:
- Check if registered: `claude mcp get <name>` (exit 0 = registered)
- Check if connected: appears in `claude mcp list` with ✓

```
MCP Server Status:
┌──────────────┬────────────┬────────────┬───────────┬─────────────────────────┐
│ Server       │ Configured │ Registered │ Connected │ Action Needed           │
├──────────────┼────────────┼────────────┼───────────┼─────────────────────────┤
│ context7     │ plugin     │ plugin     │ ✓         │ None                    │
│ github       │ ✓          │ ✗          │ ✗         │ Run --fix to register   │
│ memory       │ ✓          │ ✗          │ ✗         │ Run --fix to register   │
│ filesystem   │ ✓          │ ✗          │ ✗         │ Run --fix to register   │
│ puppeteer    │ ✓          │ ✗          │ ✗         │ Run --fix to register   │
└──────────────┴────────────┴────────────┴───────────┴─────────────────────────┘
```

### Phase 3: Auto-Register (if --fix)

If `--fix` is passed, register missing servers using `claude mcp add`.

**Registration commands by server type:**

For servers WITHOUT env vars, use `claude mcp add`:
```bash
claude mcp add <name> -- npx -y <package> [args]
```

For servers WITH env vars, use `claude mcp add-json` (more reliable):
```bash
claude mcp add-json <name> '{"command":"npx","args":["-y","<package>"],"env":{"KEY":"value"}}'
```

| Server | Registration Command |
|--------|---------------------|
| github | `claude mcp add-json github '{"command":"npx","args":["-y","@modelcontextprotocol/server-github"],"env":{"GITHUB_TOKEN":"<token>"}}'` |
| memory | `claude mcp add memory -- npx -y @modelcontextprotocol/server-memory` |
| filesystem | `claude mcp add filesystem -- npx -y @modelcontextprotocol/server-filesystem "<path>"` |
| puppeteer | `claude mcp add puppeteer -- npx -y @modelcontextprotocol/server-puppeteer` |
| postgres | `claude mcp add-json postgres '{"command":"npx","args":["-y","@modelcontextprotocol/server-postgres"],"env":{"DATABASE_URL":"<url>"}}'` |
| sqlite | `claude mcp add sqlite -- npx -y @modelcontextprotocol/server-sqlite "<db-path>"` |
| brave-search | `claude mcp add-json brave-search '{"command":"npx","args":["-y","@modelcontextprotocol/server-brave-search"],"env":{"BRAVE_API_KEY":"<key>"}}'` |
| fetch | `claude mcp add fetch -- npx -y @modelcontextprotocol/server-fetch` |

**Generic pattern for unknown servers:**

Parse from settings.json:
```json
"<name>": {
  "command": "cmd",
  "args": ["/c", "npx", "-y", "<package>"],
  "env": { "KEY": "value" }
}
```

Convert to (using add-json for reliability):
```bash
claude mcp add-json <name> '{"command":"npx","args":["-y","<package>"],"env":{"KEY":"value"}}'
```

**After registration:**
- Run `claude mcp list` to verify
- Report success/failure for each

### Phase 4: Test Servers (if --test)

Test each connected server with a real API call:

| Server | Test Call | Success Criteria |
|--------|-----------|------------------|
| context7 | `mcp__plugin_context7_context7__resolve-library-id` with "react" | Returns library results |
| claude-in-chrome | `mcp__claude-in-chrome__tabs_context_mcp` | Returns tab info or "extension not connected" |
| github | `mcp__github__*` tool call | Returns data without auth error |
| memory | `mcp__memory__*` read/write test | Completes without error |
| filesystem | `mcp__filesystem__*` list directory | Returns file list |
| puppeteer | `mcp__puppeteer__*` screenshot | Returns image data |

Report test results:
```
Test Results:
  ✓ context7: Returned 5 React libraries
  ✗ claude-in-chrome: Extension not connected
  ✓ github: Authenticated as <username>
  ✓ memory: Read/write successful
```

### Phase 5: Summary

```
[MCP] Summary:
  Configured: 5 servers (in settings.json mcpServers)
  Plugins:    2 (context7, claude-in-chrome)
  Registered: 4 servers (in claude mcp)
  Connected:  3 servers

[MCP] Actions Taken:
  • Registered: github, memory, filesystem, puppeteer

[MCP] Still Needs Attention:
  • claude-in-chrome: Open Chrome with extension active
  • Restart Claude Code to connect newly registered servers

[MCP] For /cs-loop:
  • Context7 available → Library docs will be auto-fetched
  • GitHub available → Can create PRs and issues
```

## Known Servers Reference

| Server | Package | Env Vars | Purpose |
|--------|---------|----------|---------|
| context7 | `@upstash/context7-mcp` | - | Library documentation |
| claude-in-chrome | Plugin | - | Browser automation |
| github | `@modelcontextprotocol/server-github` | GITHUB_TOKEN | GitHub API |
| memory | `@modelcontextprotocol/server-memory` | - | Key-value store |
| filesystem | `@modelcontextprotocol/server-filesystem` | - | File access |
| puppeteer | `@modelcontextprotocol/server-puppeteer` | - | Browser automation |
| postgres | `@modelcontextprotocol/server-postgres` | DATABASE_URL | PostgreSQL |
| sqlite | `@modelcontextprotocol/server-sqlite` | - | SQLite DB |
| brave-search | `@modelcontextprotocol/server-brave-search` | BRAVE_API_KEY | Web search |
| fetch | `@modelcontextprotocol/server-fetch` | - | HTTP requests |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Server configured but not registered | Run `/cs-mcp --fix` |
| Server registered but not connected | Restart Claude Code |
| github auth fails | Check GITHUB_TOKEN env var |
| claude-in-chrome not connected | Open Chrome, check extension is active |
| puppeteer fails | May need Chrome/Chromium installed |
| filesystem access denied | Check path permissions |
