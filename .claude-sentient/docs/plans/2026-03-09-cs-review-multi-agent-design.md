# Design: Multi-Agent Parallel Code Review for /cs-review

**Date:** 2026-03-09
**Version target:** v1.5.9
**Status:** Approved

## Problem

The existing `/cs-review` command uses a single agent to review all changed files sequentially. A single agent must split attention across security, performance, logic, tests, and style — leading to shallower findings than a focused specialist.

Anthropic's Code Review system (described at claude.com/blog/code-review) demonstrated that parallel specialist agents produce substantially better recall: 54% of PRs receive substantive feedback vs. 16% previously.

## Solution

Upgrade `/cs-review` to spawn 5 specialist agents in parallel, then run a synthesizer to deduplicate, rank, and filter findings before presenting the final review.

## Architecture

```
PR context (mcp__github__pull_request_read)
    │
    ├─► Security Agent  ──────────────────┐
    ├─► Performance Agent ────────────────┤
    ├─► Logic Agent ──────────────────────┤── Synthesizer Agent ──► Ranked findings ──► GitHub API
    ├─► Tests Agent ──────────────────────┤
    └─► Style Agent ──────────────────────┘
```

## Agent Focus Areas

| Agent | Reviews for | Explicitly ignores |
|-------|-------------|-------------------|
| Security | Secrets, injection, auth bypass, OWASP Top 10 | Style, coverage |
| Performance | N+1, loops, missing indexes, memory leaks | Naming, security |
| Logic | Null handling, edge cases, error propagation, race conditions | Style, performance |
| Tests | Coverage gaps, assertion quality, missing edge cases | Implementation |
| Style | Naming, cyclomatic complexity >10, duplication, dead code | Correctness |

## Structured Output Format

Each agent returns JSON:

```json
{
  "agent": "security",
  "findings": [
    {
      "severity": "HIGH",
      "file": "src/auth/jwt.ts",
      "line": 45,
      "title": "Hardcoded JWT secret",
      "body": "Secret committed in plaintext. Use process.env.JWT_SECRET.",
      "confidence": 0.95
    }
  ]
}
```

Severity levels: `CRITICAL` > `HIGH` > `MEDIUM` > `LOW`

## Synthesizer Rules

1. Same `file+line` flagged by 2+ agents → keep highest severity, merge bodies into one comment
2. `confidence < 0.7` → downgrade to advisory (shown but not blocking verdict)
3. Conflicting assessments (one agent flags, another clears same line) → surface for human judgment with both perspectives

## Files Changed

| File | Change |
|------|--------|
| `.claude/commands/cs-review.md` | Replace "Analyze Changes" with parallel agent spawns + synthesizer step; add `Task` to `allowed-tools` |
| `.claude/commands/__tests__/test-commands.js` | Assert `Task` in allowed-tools, synthesizer step present in command |
| `CHANGELOG.md` | v1.5.9 entry |
| `STATUS.md` | Version bump |

## Out of Scope

- GitHub Actions auto-trigger workflow (follow-up)
- Analytics/cost tracking dashboard (follow-up)
- Size-adaptive mode (always multi-agent per decision)
