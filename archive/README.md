# Archive

This directory contains historical code that is no longer actively used.

## Contents

### v1-legacy/

Original Claude Sentient V1 implementation. This was replaced by the V2 architecture that uses native Claude Code tools instead of custom implementations.

**Why archived:** V1 used custom Python implementations for:
- Session management
- Task queues
- Quality gates
- Profile detection

V2 instead leverages Claude Code's native tools (`TaskCreate`, `TaskUpdate`, `EnterPlanMode`, etc.) and the official Claude Agent SDK, making the custom implementations unnecessary.

**Status:** Historical reference only. Do not use for new development.
