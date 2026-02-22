---
name: team-orchestration
description: Agent Teams workflow for the EXECUTE phase. Covers team eligibility evaluation, agent matching, teammate spawning, progress monitoring, and result collection.
user-invocable: false
---

# Team Orchestration Skill

Reference material for Agent Teams mode in `/cs-loop` EXECUTE phase.

## Team Eligibility Check

Evaluate three signals after task creation in PLAN phase:

| Signal | Check | Threshold |
|--------|-------|-----------|
| Scope | Count tasks with no `blockedBy` dependencies | >= 3 independent tasks |
| Independence | Compare directory paths of independent tasks | No overlapping file scopes |
| Complexity | Estimate total work across all tasks | > simple feature or bug fix |

All three must be true AND `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` must be enabled. If env var not set, skip silently and use standard mode.

## Agent Matching

1. Read `agents/*.yaml` files (or use `.claude/agents/*.md` native agents)
2. Match each work stream to the best-fit agent based on `expertise` arrays
3. Use the agent's `spawn_prompt`, `rules_to_load`, and `file_scope_hints`
4. Fall back to generic role prompts if no matching agent exists

## Teammate Spawning

Create an Agent Team with agent-specific configuration:

```
Teammate "{agent-name}":
- Prompt: {spawn_prompt from agent definition}
- Scope: {file_scope_hints, or directory/package they own}
- Tasks: {specific task IDs and descriptions}
- Rules: {rules_to_load from agent}
- Quality gates: {lint command}, {test command}
- Rule: Only modify files in your scope
```

Require plan approval before teammates make changes.

## Progress Monitoring

After spawning, switch to coordination-only mode:

1. Track progress via shared task list
2. Redirect teammates that drift from scope
3. Unblock teammates that report issues
4. Synthesize results as tasks complete

## Result Collection

When all teammate tasks complete:

1. Send shutdown requests to all teammates
2. Wait for shutdown confirmations
3. Review combined changes across all streams
4. Report: `[EXECUTE] Team complete: {completed}/{total} tasks`
5. Proceed to VERIFY with all changes

## Key Lessons

- Carefully partition file ownership to avoid edit conflicts on shared files
- If a teammate modifies a file, re-read before editing ("File modified since read" errors)
- Send shutdown_request and wait for shutdown_approved before TeamDelete
- TeamDelete fails if any members are still active
