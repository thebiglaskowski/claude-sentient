---
feature: Context Injection
version: "1.0"
last_updated: 2026-03-04
dependencies:
  - "02-session-lifecycle.md"
routes: []
status: draft
---

# Context Injection

> context-injector.cjs runs synchronously on every ContextRequest event, enriching Claude's context with topic-relevant file suggestions and monitoring for context degradation.

## Hook Overview

| Hook | Event | Sync | Purpose |
|------|-------|------|---------|
| `context-injector.cjs` | ContextRequest | sync | Topic detection, file suggestions, degradation monitoring |

## Topic Detection

The hook maps prompt keywords to 10 topic categories:

| Topic | Keywords |
|-------|---------|
| `auth` | login, auth, jwt, oauth, session, password, token |
| `test` | test, spec, coverage, mock, assert, fixture |
| `api` | api, endpoint, route, rest, graphql, handler |
| `database` | database, query, schema, migration, orm, sql |
| `performance` | performance, optimize, cache, slow, memory, profiling |
| `ui` | ui, component, css, style, tailwind, design |
| `security` | security, vulnerability, xss, injection, csrf |
| `codeQuality` | refactor, lint, complexity, smell, clean |
| `errorHandling` | error, exception, catch, try, throw |
| `documentation` | docs, readme, changelog, docstring |

Detection is case-insensitive. Multiple topics can match a single prompt.

## File Pattern Suggestions

For each detected topic, the hook suggests glob patterns for relevant files:

| Topic | File Patterns |
|-------|--------------|
| `auth` | `**/auth/**`, `**/middleware/**`, `**/session*` |
| `test` | `**/__tests__/**`, `**/*.test.*`, `**/*.spec.*` |
| `api` | `**/routes/**`, `**/controllers/**`, `**/handlers/**` |
| `database` | `**/models/**`, `**/migrations/**`, `**/schemas/**` |
| `performance` | `**/cache/**`, `**/utils/**`, `**/lib/**` |
| `ui` | `**/components/**`, `**/pages/**`, `**/styles/**` |
| `security` | `**/middleware/**`, `**/auth/**`, `**/validators/**` |
| `codeQuality` | `**/utils/**`, `**/helpers/**`, `**/lib/**` |
| `errorHandling` | `**/errors/**`, `**/exceptions/**`, `**/middleware/**` |
| `documentation` | `**/*.md`, `**/docs/**` |

## Context Output Format

The hook outputs context (not a permission decision — this is a ContextRequest hook):

```json
{
  "context": "Detected topics: auth, security. Suggested files: **/auth/**, **/middleware/**",
  "contextWarning": "optional degradation warning"
}
```

## Context Degradation Monitoring

The hook tracks prompt count in `prompts.json` and warns when approaching degradation thresholds:

| Threshold | Constant | Severity | Effect |
|-----------|---------|---------|--------|
| Early warning | `CONTEXT_DEGRADATION_EARLY = 15` | `medium` | contextWarning added to output |
| High warning | `CONTEXT_DEGRADATION_THRESHOLD = 20` | `high` | contextWarning added, suggests compaction |

**Important implementation detail**: The hook appends the current prompt to `prompts.json` BEFORE calling `checkContextDegradation()`. So when seeding N entries and triggering the hook, `promptCount` is `N+1`. Assert `>= threshold`, not `=== N`.

### context_degradation.json Shape

```json
{
  "promptCount": 16,
  "severity": "medium",
  "detectedAt": "2026-03-04T00:00:00.000Z",
  "suggestion": "Consider running /cs-loop compact to preserve context"
}
```

## prompts.json

Append-only log of prompt entries used for degradation tracking. Not capped (grows per session). Located at `.claude/state/prompts.json`.

## State Files Written

| File | Purpose |
|------|---------|
| `.claude/state/prompts.json` | Prompt count tracking (append) |
| `.claude/state/context_degradation.json` | Degradation severity and metadata |

## Business Rules

- **Sync required**: context-injector must complete before Claude's response — never mark as `async: true`
- **Always exits 0**: Even if topic detection finds nothing, the hook exits without error
- **contextWarning passthrough**: Written to output only when degradation threshold is met — no noise below thresholds
- **Multi-topic support**: A prompt matching auth + security topics gets file suggestions from both
