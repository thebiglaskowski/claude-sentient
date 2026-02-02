# Configuration Reference

Complete reference for all configuration options.

---

## Table of Contents

1. [File Locations](#file-locations)
2. [settings.json](#settingsjson)
3. [Hooks Configuration](#hooks-configuration)
4. [MCP Servers](#mcp-servers)
5. [Skills Configuration](#skills-configuration)
6. [Project Files](#project-files)

---

## File Locations

### System-Wide (All Projects)

| File | Location | Purpose |
|------|----------|---------|
| `settings.json` | `~/.claude/settings.json` | Global MCP servers, permissions |

**Platform paths:**
- Windows: `C:\Users\YourName\.claude\settings.json`
- macOS: `/Users/YourName/.claude/settings.json`
- Linux: `/home/YourName/.claude/settings.json`

### Per-Project

| File | Location | Purpose |
|------|----------|---------|
| `CLAUDE.md` | `.claude/CLAUDE.md` | Project instructions |
| `settings.json` | `.claude/settings.json` | Project-specific settings |
| `MCP_SERVERS.md` | `.claude/MCP_SERVERS.md` | MCP setup documentation |
| `QUICK_REFERENCE.md` | `.claude/QUICK_REFERENCE.md` | Cheat sheet |
| `CONFIGURATION.md` | `.claude/CONFIGURATION.md` | This file |
| `.version` | `.claude/.version` | Template version |

### Subdirectories

| Directory | Purpose |
|-----------|---------|
| `.claude/commands/` | Slash commands |
| `.claude/skills/` | Auto-loading skills |
| `.claude/rules/` | Modular rule files (v2.0+) |
| `.claude/agents/` | Specialized agent definitions (v2.0+) |
| `.claude/scripts/` | CI/CD automation scripts (v2.0+) |
| `.claude/context/` | Generated context (PROJECT_MAP.md) |
| `.claude/metrics/` | Usage metrics (gitignored) |
| `.claude/history/` | Undo history (gitignored) |
| `.claude/snippets/` | Custom code snippets |

---

## settings.json

### Full Structure

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git *)",
      "Bash(npx prettier *)"
    ],
    "deny": [
      "Bash(rm -rf /)"
    ]
  },
  "hooks": {
    "PreToolUse": [],
    "PostToolUse": [],
    "Setup": [],
    "SessionStart": []
  },
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@package/name"],
      "env": {
        "VAR_NAME": "${VAR_NAME}"
      }
    }
  },
  "model": {
    "default": "sonnet",
    "override": {}
  },
  "metrics": {
    "enabled": true
  },
  "changelog": {
    "skipPrefixes": ["docs:", "test:", "chore:"],
    "includeLinks": true
  },
  "dependencyTracker": {
    "checkOnStart": true,
    "weeklyReport": true
  }
}
```

### Permissions

Control what Claude can execute:

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git add *)",
      "Bash(git commit *)",
      "Bash(git push)",
      "Bash(npx prettier *)",
      "Bash(npx eslint *)"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(git push --force)"
    ]
  }
}
```

**Patterns:**
- `*` matches anything
- Exact strings for specific commands
- `deny` takes precedence over `allow`

---

## Hooks Configuration

### Hook Types

| Hook | When It Runs |
|------|--------------|
| `Setup` | Once when Claude Code initializes |
| `SessionStart` | At start of each conversation |
| `PreToolUse` | Before a tool is used |
| `PostToolUse` | After a tool completes |

### Hook Structure

```json
{
  "hooks": {
    "HookType": [
      {
        "matcher": "condition",
        "hooks": [
          {
            "type": "command",
            "command": "shell command here"
          }
        ]
      }
    ]
  }
}
```

### Matcher Syntax

```javascript
// Match specific tool
"tool == \"Edit\""

// Match tool with file pattern
"tool == \"Edit\" && tool_input.file_path matches \"\\.tsx?$\""

// Match tool with content
"tool == \"Bash\" && tool_input.command contains \"npm\""
```

### Example Hooks

#### Auto-Format After Edit
```json
{
  "PostToolUse": [
    {
      "matcher": "tool == \"Edit\" && tool_input.file_path matches \"\\.(ts|tsx|js|jsx)$\"",
      "hooks": [
        {
          "type": "command",
          "command": "npx prettier --write \"$FILE_PATH\""
        }
      ]
    }
  ]
}
```

#### Warn About console.log
```json
{
  "PostToolUse": [
    {
      "matcher": "tool == \"Edit\" && tool_input.file_path matches \"\\.(ts|tsx|js|jsx)$\"",
      "hooks": [
        {
          "type": "command",
          "command": "grep -n 'console.log' \"$FILE_PATH\" && echo '⚠️ console.log detected' || true"
        }
      ]
    }
  ]
}
```

#### Session Start Warning
```json
{
  "SessionStart": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "[ ! -f .claude/context/PROJECT_MAP.md ] && echo '⚠️ Run /map-project to generate context' || true"
        }
      ]
    }
  ]
}
```

#### Block Force Push
```json
{
  "PreToolUse": [
    {
      "matcher": "tool == \"Bash\" && tool_input.command contains \"--force\"",
      "hooks": [
        {
          "type": "command",
          "command": "echo '🛑 Force push blocked. Use with caution.' && exit 1"
        }
      ]
    }
  ]
}
```

---

## MCP Servers

### Configuration Locations

MCP servers can be configured in multiple places:

| Location | Scope | Notes |
|----------|-------|-------|
| `~/.claude/settings.json` | System-wide | Available in all projects |
| `.mcp.json` | Project root | Common convention for project-specific servers |
| `.claude/settings.json` | Project | Alternative project-specific location |

**Note:** The `.mcp.json` file is commonly placed in the **project root** (not inside `.claude/`). Both locations work for project-specific configuration.

### Server Structure

```json
{
  "mcpServers": {
    "server-name": {
      "command": "executable",
      "args": ["arg1", "arg2"],
      "env": {
        "VAR": "value",
        "SECRET": "${ENV_VAR}"
      }
    }
  }
}
```

### Common Servers

#### Context7
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

#### GitHub
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

#### Memory
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

#### PostgreSQL
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

See [MCP_SERVERS.md](MCP_SERVERS.md) for complete setup instructions.

---

## Skills Configuration (v2.0)

### Skill File Structure with YAML Frontmatter

Skills use YAML frontmatter for metadata. Keep it minimal - only include fields you need:

```markdown
---
name: skill-name
description: One-line description of what the skill does
model: sonnet
---

# Skill Name

[Skill content here]
```

### Official Frontmatter Fields (Claude Code)

These fields are processed by Claude Code:

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | string | Required | Skill identifier (kebab-case) |
| `description` | string | Required | One-line description |
| `argument-hint` | string | - | Hint for skill arguments (e.g., `"<path>"`) |
| `disable-model-invocation` | boolean | false | True for reference-only skills (saves context) |
| `user-invocable` | boolean | true | Can be called with `/command` |
| `allowed-tools` | array | all | Tools this skill can use |
| `model` | string | inherit | `haiku`, `sonnet`, or `opus` |
| `context` | string | inherit | `fork` for isolated subagent execution |
| `agent` | string | - | Agent to delegate to (from `.claude/agents/`) |
| `hooks` | object | - | Skill-specific hooks |

### Important: Use Hyphens, Not Underscores

Claude Code uses hyphenated field names:
- ✅ `disable-model-invocation`
- ❌ `disable_model_invocation`

### Context Fork

Use `context: fork` to run a skill in an isolated subagent:

```yaml
---
name: research-task
description: Research in isolated context
context: fork
model: sonnet
---
```

The subagent has its own context, explores freely, and returns only a summary.

### Reference-Only Skills

For pure documentation (not actionable), use:

```yaml
---
name: severity-levels
description: Standard severity classification reference
disable-model-invocation: true
---
```

This prevents the skill from consuming context tokens.

### Trigger Keywords

Skills auto-load when conversation contains trigger words:

| Skill | Triggers |
|-------|----------|
| `pre-commit` | "commit", "git commit", "ready to commit" |
| `pre-merge` | "merge", "PR", "pull request" |
| `dry-run-mode` | "dry run", "preview", "simulate" |
| `error-recovery` | "error", "failed", "retry" |
| `extended-thinking` | "ultrathink", "think deeply" |

### Creating Custom Skills

1. Create `.claude/skills/my-skill.md`
2. Add YAML frontmatter with required fields
3. Add guidance content
4. Skill auto-loads when triggers match

---

## Rules System (v2.0)

Rules provide modular, topic-specific guidance loaded with `@rules/[name]`.

### Available Rules

| Rule | Purpose |
|------|---------|
| `security` | OWASP Top 10, authentication, secrets |
| `testing` | Coverage, TDD, mocking strategies |
| `git-workflow` | Commits, branches, PR standards |
| `documentation` | README, changelog, comments |
| `code-quality` | Complexity, naming, dependencies |
| `api-design` | REST, errors, versioning |
| `error-handling` | Error hierarchy, logging, recovery |

### Using Rules

**In conversation:**
```
Load @rules/security for this review
```

**In skill frontmatter:**
```yaml
rules:
  - security
  - testing
```

### Creating Custom Rules

Create `.claude/rules/my-rule.md`:

```markdown
# My Rule

## Core Principles
[3-5 guiding principles]

## Standards
[Specific requirements with examples]

## Anti-Patterns
[What NOT to do]

## Checklist
[Quick verification list]
```

---

## Agents System (v2.0)

Agents are specialized subagents that can be spawned for focused tasks.

### Available Agents

| Agent | Model | Expertise |
|-------|-------|-----------|
| `code-reviewer` | sonnet | Quality, patterns, tests |
| `security-analyst` | opus | OWASP, STRIDE, vulnerabilities |
| `test-engineer` | sonnet | Coverage, mocks, TDD |
| `documentation-writer` | sonnet | README, API docs |
| `researcher` | sonnet | Tech research, evaluation |

### Spawning Agents

```
Spawn code-reviewer agent to review src/auth
```

```
Use security-analyst to audit the API
```

### Agent Output

Agents return structured summaries:
```markdown
## Agent Report: [Agent Name]

### Findings
[Structured findings]

### Recommendations
[Actionable recommendations]
```

### Creating Custom Agents

Create `.claude/agents/my-agent.md`:

```yaml
---
name: my-agent
description: What this agent does in one line
tools: Read, Grep, Glob, Bash
disallowedTools: Write, Edit
model: sonnet
---

# Agent: My Agent

## Expertise
[Specializations]

## Process
[How the agent works]

## Output Format
[What it returns]
```

### Official Agent Frontmatter Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Agent identifier (kebab-case) |
| `description` | string | One-line description |
| `tools` | string | Comma-separated allowed tools |
| `disallowedTools` | string | Tools agent cannot use |
| `model` | string | `haiku`, `sonnet`, or `opus` |
| `permissionMode` | string | Permission handling mode |
| `skills` | array | Skills available to agent |
| `hooks` | object | Agent-specific hooks |

---

## Command Arguments (v2.0)

Commands can now accept arguments using special variables.

### Argument Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `$ARGUMENTS` | Full argument string | `"src/api --deep"` |
| `$0` | Command name | `review` |
| `$1` | First argument | `src/api` |
| `$2` | Second argument | `--deep` |
| `$@` | All as array | `["src/api", "--deep"]` |

### Usage Examples

```
/review src/api --deep --security
/test src/utils --coverage=90
/refactor src/old.ts --type=extract --dry-run
/secure src/auth --severity=S0 --ultrathink
```

### Commands with Arguments

| Command | Arguments |
|---------|-----------|
| `/review` | `[path]` `--deep` `--security` `--quick` |
| `/test` | `[path]` `--coverage=N` `--watch` |
| `/refactor` | `[path]` `--type=rename\|extract` `--dry-run` |
| `/secure` | `[scope]` `--severity=S0\|S1` `--ultrathink` |
| `/debt` | `[category]` |
| `/release` | `[version]` |

---

## Extended Thinking (v2.0)

Enable deep analysis mode for complex problems.

### Activation

**In conversation:**
```
Ultrathink this problem
Think deeply about the architecture
```

**With commands:**
```
/secure --ultrathink
/audit-blueprint --ultrathink
```

### When to Use

- Security audits
- Architecture decisions
- Complex debugging
- Incident analysis
- Risk assessment

### Configuration

In skill frontmatter:
```yaml
extended_thinking: true
```

---

## Context Fork (v2.0)

Spawn isolated research agents that don't pollute main context.

### Usage

```
Research in background: How does authentication work?
Fork investigation: Compare caching approaches
```

### How It Works

```
Main Context           Subagent Context
     │                      │
     │─── Task ────────────>│
     │                      │ (extensive exploration)
     │<── Summary ──────────│
     ▼                      X (discarded)
(continues clean)
```

### Configuration

In skill frontmatter:
```yaml
context: "fork"
```

---

## CI/CD Scripts (v2.0)

Scripts for running Claude Code in headless mode.

### Available Scripts

| Script | Purpose |
|--------|---------|
| `scripts/ci/pr-review.sh` | Automated PR review |
| `scripts/ci/security-scan.sh` | Security scanning |
| `scripts/ci/test-gate.sh` | Coverage verification |
| `scripts/validate/prompt-check.sh` | Prompt validation |
| `scripts/validate/skill-lint.sh` | YAML frontmatter linting |

### Usage

```bash
# Run PR review
./scripts/ci/pr-review.sh --deep

# Security scan
./scripts/ci/security-scan.sh src/auth --ultrathink

# Test coverage gate
./scripts/ci/test-gate.sh --threshold=80
```

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `ANTHROPIC_API_KEY` | Required for CI scripts |
| `CLAUDE_MODEL` | Override model (default: sonnet) |
| `REVIEW_LEVEL` | quick, standard, deep |
| `BLOCK_ON_S1` | Whether S1 issues block (default: true) |

### GitHub Actions

Copy workflows to your repo:
```bash
cp -r .claude/scripts/.github/workflows/* .github/workflows/
```

---

## Autonomous Loop (v2.0)

Configuration for the `/loop` command and autonomous development.

### Loop Arguments

```
/loop [focus] [options]

Focus Areas:
  all        Full autonomous mode (default)
  security   Focus on security issues
  testing    Focus on test coverage
  features   Implement pending features

Options:
  --max-iterations=N   Maximum loop iterations (default: 50)
  --pause-on=S0|S1     Pause for user on severity level (default: S0)
  --modern             Force modern tech alternatives check
  --dry-run            Show what would be done without doing it
```

### Loop Behavior Configuration

Add to `settings.json`:

```json
{
  "loop": {
    "maxIterations": 50,
    "pauseOnSeverity": "S0",
    "autoCommit": true,
    "autoModernize": true,
    "coverageThreshold": 80,
    "newCodeCoverage": 90,
    "stateFile": "LOOP_STATE.md"
  }
}
```

### Quality Gate Thresholds

| Gate | Default | Override |
|------|---------|----------|
| Test coverage | 80% | `coverageThreshold` |
| New code coverage | 90% | `newCodeCoverage` |
| Max S1 issues | 0 | `maxS1Issues` |
| Max S2 issues | 5 | `maxS2Issues` |

### Work Queue Priority

Items are processed in this order:
1. **S0 Critical** - Security, crashes, data loss
2. **S1 High** - Major bugs, blockers
3. **Blocking dependencies** - Required for other work
4. **S2 Medium** - Important but not blocking
5. **Test coverage gaps** - Below threshold
6. **S3 Low** - Minor issues
7. **Enhancements** - Modernization, refactoring

### Dynamic Work Queue

New work discovered during the loop is automatically added:
- Bugs found while fixing other bugs
- Test gaps identified during coverage push
- Deprecated APIs found during review
- User requests mid-loop ("also add X")

**The loop continues until the queue is empty AND all gates pass.**

### Conda Environment Safety

The loop respects environment safety:
```json
{
  "loop": {
    "requireVirtualEnv": true,
    "blockBaseEnv": true
  }
}
```

If base conda environment is active, the loop pauses and requires you to create/activate a project environment.

### State Tracking

Loop progress is saved in `LOOP_STATE.md`:

```markdown
# Autonomous Loop State

## Current Iteration: 7
## Status: IN_PROGRESS

## Quality Gates
| Gate | Status | Issues |
|------|--------|--------|
| Tests | ✅ PASS | 0 |
| Coverage | ⚠️ WARN | 78% |
| Security | ✅ PASS | 0 |

## Work Queue
| Priority | Item | Status |
|----------|------|--------|
| S1 | Fix auth bypass | ✅ Done |
| S2 | Add validation | 🔄 In Progress |
```

---

## Project Files

### STATUS.md

```markdown
# Project Status

## Current Focus
[What you're working on]

## Recent Progress
- [x] Completed item
- [ ] In progress item

## Next Steps
1. Next task
2. Following task

## Blockers
- None currently

## Notes
[Important context]
```

### CHANGELOG.md

```markdown
# Changelog

## [Unreleased]

### Added
- New feature

### Changed
- Modified feature

### Fixed
- Bug fix

## [1.0.0] - 2024-01-15

### Added
- Initial release
```

### KNOWN_ISSUES.md

```markdown
# Known Issues

## Active Issues

### Issue Title
**Severity:** S2
**Description:** What's wrong
**Workaround:** How to work around it
**Tracking:** #123

## Resolved Issues

### Fixed Issue
**Resolved:** 2024-01-15
**Resolution:** How it was fixed
```

### PROJECT_MAP.md

Generated by `/map-project`. Contains:
- Project overview
- Tech stack
- Directory structure
- Entry points
- Key patterns
- Important files

---

## Environment Variables

### Setting Variables

**Windows (PowerShell):**
```powershell
[Environment]::SetEnvironmentVariable("VAR_NAME", "value", "User")
```

**macOS/Linux:**
```bash
echo 'export VAR_NAME="value"' >> ~/.zshrc
source ~/.zshrc
```

### Common Variables

| Variable | Purpose | Used By |
|----------|---------|---------|
| `GITHUB_TOKEN` | GitHub API access | github MCP |
| `DATABASE_URL` | Database connection | postgres MCP |
| `ANTHROPIC_API_KEY` | Claude API | CI/CD integration |

### Referencing in Config

```json
{
  "env": {
    "MY_VAR": "${MY_VAR}"
  }
}
```

---

## Cross-Platform Notes

### Hooks Compatibility

The default hooks use bash syntax. On Windows:
- Hooks work in Git Bash, WSL, or if bash is in PATH
- For native Windows, you may need to modify hook commands
- PowerShell alternatives can be used if needed

### Path Differences

| Platform | Home Directory | Example |
|----------|---------------|---------|
| Windows | `C:\Users\Name` | `C:\Users\Name\.claude\settings.json` |
| macOS | `/Users/Name` | `/Users/Name/.claude/settings.json` |
| Linux | `/home/name` | `/home/name/.claude/settings.json` |

### Shell Commands in Hooks

```json
// Bash (macOS/Linux, Git Bash on Windows)
"command": "[ -f file ] && echo 'exists'"

// PowerShell (Windows native)
"command": "if (Test-Path file) { Write-Host 'exists' }"
```

---

## Defaults

### Default Model Routing

| Task Type | Default Model |
|-----------|---------------|
| Simple/mechanical | Haiku |
| Standard development | Sonnet |
| Complex analysis | Opus |

### Default Permissions

- Read files: Allowed
- Write files: Allowed
- Execute npm/git: Allowed
- Force operations: Blocked

### Default Hooks

- Prettier on JS/TS edits
- Console.log warnings
- PROJECT_MAP.md reminder

---

## Overriding Defaults

### Per-Project Override

Create `.claude/settings.json` in project to override system defaults.

### Precedence Order

1. Per-project settings (highest)
2. System-wide settings
3. Built-in defaults (lowest)
