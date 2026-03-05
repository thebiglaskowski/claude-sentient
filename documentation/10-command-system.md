---
feature: Command System
version: "1.0"
last_updated: 2026-03-04
dependencies: []
routes: []
status: draft
---

# Command System

> All `/cs-*` commands are Markdown files with YAML frontmatter and XML-structured instructions. Commands are invoked as slash commands in Claude Code and define Claude's role, task, steps, constraints, and output format.

## Command Files (15)

| Command | File | Purpose |
|---------|------|---------|
| `/cs-loop` | `cs-loop.md` | Autonomous work loop (7 phases) |
| `/cs-plan` | `cs-plan.md` | Plan before executing; EnterPlanMode |
| `/cs-status` | `cs-status.md` | Show tasks, git state, profile |
| `/cs-validate` | `cs-validate.md` | Validate Claude Sentient configuration |
| `/cs-learn` | `cs-learn.md` | Save decisions, patterns, learnings to memory |
| `/cs-mcp` | `cs-mcp.md` | Check, register, validate MCP servers |
| `/cs-review` | `cs-review.md` | Review a pull request |
| `/cs-assess` | `cs-assess.md` | Full codebase health audit |
| `/cs-init` | `cs-init.md` | Create/optimize nested CLAUDE.md architecture |
| `/cs-ui` | `cs-ui.md` | UI/UX audit for web projects |
| `/cs-team` | `cs-team.md` | Create and manage Agent Teams |
| `/cs-docs` | `cs-docs.md` | Generate and manage feature documentation |
| `/cs-deploy` | `cs-deploy.md` | Deployment readiness check |
| `/cs-sessions` | `cs-sessions.md` | Browse and resume previous sessions |
| `/cs-multi` | `cs-multi.md` | Configure multi-model routing per phase |

## Frontmatter Schema

Every command file starts with YAML frontmatter:

```yaml
---
description: What the command does (shown in /help listing)
argument-hint: <args>          # Placeholder shown in UI
allowed-tools: Tool1, Tool2    # Allowlist of tools Claude may use
---
```

### allowed-tools Constraints

Commands that chain to other commands via the `Skill` tool **must** include `Skill` in `allowed-tools`. Schema tests enforce this.

Common tool sets:

| Command Type | Typical allowed-tools |
|-------------|----------------------|
| Read-only audit | `Read, Glob, Grep, Bash, WebSearch` |
| Implementation | `Read, Write, Edit, Bash, Glob, Grep, Task, TaskCreate, TaskUpdate, TaskList, TaskGet` |
| Chaining commands | `+ Skill` |
| Planning | `+ EnterPlanMode, ExitPlanMode, AskUserQuestion` |

## XML Tag Structure

Commands use XML tags to structure instructions. Claude parses these as semantic sections:

| Tag | Purpose | Required? |
|-----|---------|-----------|
| `<role>` | Expert persona/specialization | Yes |
| `<task>` | Clear objective statement | Yes |
| `<context>` | Background info, tables, reference data | No |
| `<steps>` | Ordered procedure | Yes |
| `<thinking>` | Request explicit reasoning step | No |
| `<criteria>` | Success metrics | No |
| `<output_format>` | Response structure definition | No |
| `<constraints>` | Rules and limitations | No |
| `<avoid>` | Explicit anti-patterns (DON'Ts) | Recommended |
| `<examples>` | Sample inputs/outputs | No |

### Why XML Tags

- Separate WHAT from HOW in structured prompts
- Claude 4.x models parse XML tags as semantic boundaries
- Enable nested data without markdown ambiguity
- `<thinking>` blocks trigger explicit chain-of-thought

## Skill Chaining

Commands can invoke each other via the `Skill` tool. The chaining table:

| From | To | When |
|------|----|------|
| `/cs-plan` | `/cs-loop` | After plan approval, user chooses to execute |
| `/cs-status` | `/cs-loop` | When pending tasks exist, user chooses to continue |
| `/cs-validate` | `/cs-loop` | When issues found, user chooses to auto-fix |
| `/cs-loop` | `/cs-init` | When no CLAUDE.md detected during INIT |
| `/cs-init` | `/cs-loop` | After creating CLAUDE.md, user chooses to start |
| `/cs-loop` | `/cs-team` | When team eligibility detected, user approves |
| `/cs-team` | `/cs-loop` | When team completes, fallback to solo for remaining |
| `/cs-assess` | `/cs-loop` | When issues found, user chooses to fix |
| `/cs-review` | `/cs-loop` | When PR changes needed, user chooses to fix |
| `/cs-loop` | `/cs-docs` | At COMMIT, when changed files need doc sync check |
| `/cs-docs` | `/cs-loop` | After generating doc, user implements against spec |
| `/cs-ui` | `/cs-loop` | When UI issues found, user chooses to fix |
| `/cs-sessions` | `/cs-loop` | When user chooses to resume a previous session |

Standalone commands (never chain out): `/cs-learn`, `/cs-mcp`, `/cs-deploy`, `/cs-multi`

## Documentation Policy

Commands auto-update governance files based on change type:

| Change Type | STATUS.md | CHANGELOG.md | DECISIONS.md |
|-------------|-----------|--------------|--------------|
| Feature added | Auto | Confirm | Only if architectural |
| Bug fixed | Auto | Confirm | — |
| Refactoring | Auto | — | If significant |
| Breaking change | Auto | Confirm (required) | Required |
| Config change | Auto | — | — |

## Adding a New Command

1. Create `.claude/commands/cs-{name}.md` with frontmatter
2. Use XML tags (`<role>`, `<task>`, `<steps>`, `<avoid>`, etc.)
3. Add `<avoid>` section with command-specific anti-patterns
4. Update `cs-validate.md` required commands list
5. Update root `CLAUDE.md` commands table
6. Update `README.md`, `CHANGELOG.md`, `install.sh`, `install.ps1`
7. Run `node .claude/commands/__tests__/test-commands.js` to validate

## Business Rules

- **Command count consistency**: `install.sh`, `install.ps1`, and integration tests all assert the same number of commands. Adding a command requires updating all three.
- **Schema validation**: `test-commands.js` validates frontmatter presence, required XML tags, and skill chaining requirements.
- **argument-hint convention**: Use `<args>` for positional args, `[--flag]` for optional flags, `"quoted string"` for string args.
- **Skill in allowed-tools**: Any command that calls `Skill(...)` must list `Skill` in `allowed-tools`. Schema test fails otherwise.

## Edge Cases

- **No argument provided**: Commands with required args (like `/cs-loop "task"`) should prompt with `AskUserQuestion` if invoked without args.
- **Unknown argument**: Ignore unknown flags gracefully; don't error.
- **Chained command fails**: The originating command should surface the failure clearly rather than silently continuing.
