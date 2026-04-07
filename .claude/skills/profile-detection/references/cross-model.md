# Cross-Model Workflow (Claude + Codex)

## Overview

Use Claude Code for planning and implementation, and OpenAI Codex CLI for independent QA review. Different model families catch different blind spots.

## Workflow

### Phase 1: Plan (Claude Code)
Use `/cs-plan` to create implementation plan, export to PLAN.md.

### Phase 2: QA Review (Codex CLI)
```
codex "Review PLAN.md against the codebase. Check for: missing edge cases, security gaps, architectural misalignment, over-engineering. Be critical."
```

### Phase 3: Implement (Claude Code)
```
/cs-loop "implement PLAN.md, addressing QA feedback"
```

### Phase 4: Verify (Codex CLI)
```
codex "Review changes in this branch against PLAN.md. Verify: all plan items implemented, no regressions, tests cover edge cases."
```

## When to Use

- High-stakes changes (auth, payments, data migrations)
- Architecture decisions affecting many files
- When you want a second opinion from a different model family

## Setup

Requires OpenAI Codex CLI installed separately. Codex instructions can be placed in `.codex/instructions.md` (Claude Sentient installer creates this).

## Limitations

- Adds latency (two model round-trips per phase)
- Codex may not have access to all MCP servers
- Best for review/verification, not real-time collaboration
