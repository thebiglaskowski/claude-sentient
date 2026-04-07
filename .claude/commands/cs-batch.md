---
description: Fan out plan tasks to parallel worktree agents
argument-hint: [plan-file | task-description]
allowed-tools: Read, Bash, Glob, Grep, Task, TaskCreate, TaskUpdate, TaskList, TaskGet, EnterWorktree, ExitWorktree, AskUserQuestion, Skill
---

# /cs-batch

<role>
You are a parallel work orchestrator. You decompose tasks into independent work streams and fan them out to isolated worktree agents for maximum throughput.
</role>

<task>
Take a plan (from /cs-plan output or a task description) and distribute independent tasks across parallel git worktree agents. Each agent works in isolation on its own branch, then results are merged back.
</task>

<steps>
## Phase 1: Load or Create Plan

1. If argument is a file path, read it as a plan document
2. If argument is a task description, run `Skill(skill="cs-plan", args="<task>")` first
3. Extract independent task groups (tasks with no `blockedBy` dependencies between groups)

## Phase 2: Partition into Work Streams

1. Group tasks by file scope independence (no overlapping files)
2. Each group becomes a work stream
3. Report: `[BATCH] {n} work streams identified from {total} tasks`

## Phase 3: Fan Out

For each work stream:
1. Create a worktree branch: `git worktree add -b batch/{stream-id} .worktrees/batch-{stream-id}`
2. Use `EnterWorktree` to enter the isolated workspace
3. Spawn a subagent with the stream's task list and `/cs-loop` instructions
4. The subagent works autonomously through its tasks with quality gates

## Phase 4: Collect Results

1. Wait for all worktree agents to complete
2. For each completed stream:
   - Review changes via `git diff main...batch/{stream-id}`
   - Run quality gates on the combined result
   - If gates pass, merge: `git merge batch/{stream-id} --no-ff`
3. Clean up worktrees: `git worktree remove .worktrees/batch-{stream-id}`

## Phase 5: Report

```
[BATCH] Complete:
  Streams: {n} dispatched, {passed} merged, {failed} need attention
  Commits: {total} across all streams
  Files: {files} modified
```
</steps>

<constraints>
- Maximum 5 concurrent worktree agents (prevent resource exhaustion)
- Each agent must pass quality gates independently before merge
- Merge conflicts trigger `AskUserQuestion` for resolution strategy
- If any stream fails gates after 2 retries, park it and continue others
</constraints>

<avoid>
- Don't batch tasks that have cross-dependencies — those must be sequential
- Don't create worktrees for single-file tasks — overhead isn't worth it
- Don't merge without running gates on the combined result
</avoid>
