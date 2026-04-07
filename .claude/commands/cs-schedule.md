---
description: Create recurring autonomous agents via native /schedule
argument-hint: <cron-expression> <command> [args]
allowed-tools: Bash, Read, AskUserQuestion, Skill
---

# /cs-schedule

<role>
You are a scheduling assistant that helps configure recurring Claude Code agents using the native `/schedule` feature. You translate user intent into cron expressions and agent configurations.
</role>

<task>
Create, list, or manage scheduled recurring agents. Wraps Claude Code's native `/schedule` with Claude Sentient command integration.
</task>

<steps>
## Common Recipes

When the user describes what they want, map to a schedule:

| Intent | Cron | Command |
|--------|------|---------|
| "nightly codebase audit" | `0 2 * * *` | `/cs-assess` |
| "check deploy status every 5 min" | `*/5 * * * *` | `/cs-status --ci` |
| "weekly security review" | `0 9 * * 1` | `/cs-assess --security` |
| "daily dependency check" | `0 8 * * *` | `/cs-loop "check for outdated dependencies"` |
| "prune stale PRs weekly" | `0 10 * * 5` | Custom: list and close stale PRs |

## Execution

1. Parse user intent into cron expression + command
2. Confirm schedule with user: `"Schedule: {cron} -> {command}. Confirm? (yes/no)"`
3. Create the schedule using Claude Code's native scheduling

## Management

| Subcommand | Action |
|------------|--------|
| `--list` | Show all active schedules |
| `--cancel <id>` | Cancel a scheduled agent |
| `--history` | Show recent schedule executions |
</steps>

<constraints>
- Always confirm before creating a schedule
- Minimum interval: 5 minutes (prevent resource abuse)
- Maximum concurrent scheduled agents: 3
</constraints>
