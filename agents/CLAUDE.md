# Agents — Claude Sentient

> Context for working on agent definition YAML files.

## Agent Definition System

Specialized agents are defined in `agents/*.yaml` and loaded by `/cs-team` during team creation. Each agent provides role-specific expertise, spawn prompts, and quality gate requirements.

---

## YAML Structure

Every agent definition must have these fields:

```yaml
name: security
description: "Security specialist for vulnerability analysis"
version: "1.2.0"
role: reviewer
expertise:
  - OWASP Top 10
  - Authentication patterns
  - Input validation
spawn_prompt: |
  You are a security specialist. Your focus areas include:
  - OWASP Top 10 vulnerability detection
  - Authentication and authorization review
  ...
rules_to_load:
  - security
  - api-design
quality_gates:
  - lint
  - test
file_scope_hints:
  - "**/*auth*"
  - "**/*token*"
```

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Unique identifier (kebab-case, matches filename) |
| `description` | string | One-line description (10+ chars) |
| `version` | string | Semver version |
| `role` | enum | `implementer`, `reviewer`, `researcher`, `tester`, or `architect` |
| `expertise` | array | Areas of expertise (3+ items) |
| `spawn_prompt` | string | Detailed initialization prompt (50+ chars) |
| `quality_gates` | array | Gates to run: `lint`, `test`, `build` |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `rules_to_load` | array | Rule files from `rules/` to inject into context |
| `file_scope_hints` | array | Glob patterns for files this agent works with |

---

## How Agents Are Used

1. `/cs-team` reads all `agents/*.yaml` during team design
2. Agent `expertise` is matched against work stream requirements
3. Matched agents' `spawn_prompt` initializes teammates
4. Agent `rules_to_load` are injected into teammate context
5. Agent `quality_gates` are enforced via hooks

If no matching agent YAML exists for a work stream, `/cs-team` falls back to generic role-based prompts.

---

## Adding a Custom Agent

1. Create `agents/{name}.yaml` with all required fields
2. Ensure `rules_to_load` references exist in `rules/` directory
3. Use specific `file_scope_hints` to avoid overlap with other agents
4. Run `node agents/__tests__/test-agents.js` to validate
5. The agent becomes available to `/cs-team` automatically

---

## Schema

Agent definitions are validated against `schemas/agent.schema.json`.
