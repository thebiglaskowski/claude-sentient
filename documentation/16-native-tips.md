# Native Claude Code Tips for Claude Sentient Users

> Power features from Claude Code that compose well with Claude Sentient commands.

## /btw - Side Queries Without Interrupting

During a `/cs-loop` session, use `/btw` to ask a question without breaking the agent's flow:

```
/btw what does the handleAuth middleware do?
```

The agent continues its current task after answering.

## /branch - Fork a Session

Fork the current session to explore an alternative approach:

```
/branch
```

Creates a copy of the current conversation. Resume the original with `/cs-sessions --resume`.

## /voice - Voice Coding

Activate voice input. Works with all Claude Sentient commands:
- "cs-loop implement user authentication"
- "cs-status"

Tips: speak command names clearly ("cs dash loop"), spell out variable names if needed.

## /loop - Recurring Monitoring

Run a command on a recurring interval:

```
/loop 5m /cs-status
/loop 10m /cs-assess --security
```

## /batch - Massive Fan-Out

Fan work to hundreds of worktree agents. Use `/cs-batch` for Claude Sentient's quality-gated variant, or native `/batch` for maximum speed.

## --bare Flag

10x faster startup by skipping settings and MCP discovery:

```
claude --bare -p "quick question about this file"
```

Not recommended for `/cs-loop` (needs MCP servers and settings).

## --add-dir - Multi-Repo Access

Give Claude access to files in another repository:

```
claude --add-dir ../shared-lib --add-dir ../design-system
```

## Combining with Claude Sentient

| Native Feature | Claude Sentient Combo | Use Case |
|---------------|----------------------|----------|
| `/btw` | During `/cs-loop` | Side queries without breaking flow |
| `/branch` | Before risky `/cs-loop` task | Safe exploration |
| `/voice` | Any `/cs-*` command | Hands-free development |
| `/loop` | `/loop 5m /cs-status` | Monitoring |
| `--add-dir` | `/cs-loop` on multi-repo features | Cross-repo work |
| `--bare` | Quick lookups | Speed over features |
