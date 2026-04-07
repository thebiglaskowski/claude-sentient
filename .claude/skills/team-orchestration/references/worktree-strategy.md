# Worktree-First Team Strategy

## Overview

Each teammate gets an isolated git worktree instead of sharing the workspace. This eliminates file ownership conflicts entirely.

## How It Works

1. **Partition**: Tasks grouped into independent work streams (no shared files)
2. **Create worktrees**: `git worktree add -b team/{agent}-{task-id} .worktrees/team-{agent}`
3. **Spawn agents**: Each agent works in its own worktree directory
4. **Merge**: After all agents complete, merge branches sequentially

## Spawn Pattern

For each teammate:
1. `git worktree add -b team/{agent-name} .worktrees/team-{agent-name}`
2. Spawn agent with cwd = `.worktrees/team-{agent-name}`
3. Agent runs /cs-loop within its isolated workspace
4. On completion: run quality gates in the worktree
5. If gates pass: `git merge team/{agent-name} --no-ff`
6. Clean up: `git worktree remove .worktrees/team-{agent-name}`

## Fallback to Shared Workspace

Use shared workspace (original behavior) when:
- Tasks modify the same files (merge would conflict regardless)
- Single-file tasks where worktree overhead exceeds benefit
- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` is not set

## Conflict Resolution

If merge conflicts occur after worktree agents complete:
1. Show the conflict diff to the user
2. Offer: (a) manual resolution, (b) re-run conflicting agent with merged context, (c) abort and park
3. Never auto-resolve merge conflicts in team mode

## Merge Order

Merge agents that touch foundational files (types, interfaces, schemas) first, then dependents.

## Limits

- Maximum worktrees: 5 (matches /cs-batch limit)
- Worktree creation: ~200ms per worktree (negligible)
