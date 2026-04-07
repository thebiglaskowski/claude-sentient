---
feature: Agent Roles
version: "1.0"
last_updated: 2026-03-04
dependencies:
  - "06-agent-teams.md"
routes: []
status: draft
---

# Agent Roles

> Specialized agent definitions for parallel Agent Teams work. Agents have domain expertise, file scope hints, and quality gate requirements. Two complementary formats: YAML configs for metadata and expertise matching, native .md files for Claude Code invocation.

## Dual Agent System

| Format | Location | Purpose |
|--------|----------|---------|
| **YAML configs** | `agents/*.yaml` | Schema-validated metadata — tested by `test-agents.js`, used by `/cs-team` for expertise matching and team design |
| **Native agents** | `.claude/agents/*.md` | Claude Code-native format with frontmatter — directly invocable via `Task(subagent_type="agent-name")` |

The YAML files are the **source of truth** for agent metadata. The `.md` files are the **runtime format** Claude Code uses directly.

## Available Agents (9)

| Agent | Role | Expertise Focus |
|-------|------|----------------|
| `frontend` | implementer | UI components, accessibility, responsive design |
| `backend` | implementer | API design, database operations, server-side performance |
| `database` | implementer | Schema design, migrations, query optimization |
| `devops` | implementer | CI/CD pipelines, containerization, deployment |
| `security` | reviewer | Vulnerability analysis, OWASP Top 10, auth patterns |
| `architect` | architect | Design patterns, code quality, dependency management |
| `docs` | researcher | Technical writing, API docs, changelog management |
| `tester` | tester | Test coverage, edge cases, quality assurance |
| `build-resolver` | implementer | Build failures, dependency issues, CI problems |

## YAML Config Format (`agents/*.yaml`)

### Required Fields

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `name` | string | kebab-case, matches filename | Unique identifier |
| `description` | string | 10+ chars | One-line description |
| `version` | string | semver | e.g. `"1.0"` |
| `role` | enum | implementer\|reviewer\|researcher\|tester\|architect | Agent's primary role |
| `expertise` | array | 3+ items | Areas of domain expertise for matching |
| `spawn_prompt` | string | 50+ chars | Detailed initialization prompt for the agent |
| `quality_gates` | array | lint\|test\|build | Gates the agent must run before completing a task |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `rules_to_load` | array | Rule files from `rules/` to inject at startup |
| `file_scope_hints` | array | Glob patterns for files this agent primarily works with |

### Example YAML

```yaml
name: frontend
description: "Frontend specialist for UI components, accessibility, and responsive design"
version: "1.0"
role: implementer
expertise:
  - React components and hooks
  - CSS and responsive design
  - Accessibility (WCAG 2.1)
  - TypeScript for frontend
  - Testing with React Testing Library
  - Performance optimization
  - Design systems and component libraries
spawn_prompt: |
  You are a frontend specialist. Focus on:
  - Building accessible, responsive UI components
  - Writing clean TypeScript/React code
  - Following WCAG 2.1 accessibility guidelines
  - Optimizing for Core Web Vitals
rules_to_load:
  - ui-ux-design
  - code-quality
quality_gates:
  - lint
  - test
  - build
file_scope_hints:
  - "**/*.tsx"
  - "**/*.jsx"
  - "**/*.vue"
  - "**/*.svelte"
  - "**/*.css"
  - "**/*.scss"
  - "**/components/**"
  - "**/pages/**"
  - "**/views/**"
```

## Native Agent Format (`.claude/agents/*.md`)

### Frontmatter Fields

| Field | Type | Values | Description |
|-------|------|--------|-------------|
| `name` | string | kebab-case | Unique identifier |
| `description` | string | — | When to invoke this agent |
| `model` | enum | `haiku`, `sonnet`, `opus`, `inherit` | Model for this agent |
| `permissionMode` | enum | `default`, `acceptEdits`, `plan`, `dontAsk` | Edit permission level |
| `tools` | array | — | Allowlist of permitted tools |
| `skills` | array | — | Skills preloaded at startup (e.g., `quality-gates`) |
| `maxTurns` | number | optional | Maximum agentic iterations |
| `memory` | enum | `user`, `project`, `local` | optional |
| `isolation` | string | `"worktree"` | Git worktree isolation (optional) |

### Example Native Agent

```markdown
---
name: backend
description: "Backend specialist for API design, database operations, and server-side performance"
model: sonnet
permissionMode: acceptEdits
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
  - TaskCreate
  - TaskUpdate
  - TaskList
  - TaskGet
skills:
  - quality-gates
---

You are a backend specialist. Your focus areas include:
[spawn_prompt content from YAML]

## Rules
Apply rules from: api-design, error-handling, database

## Quality Gates
Run before completing any task: lint, test, build

## File Scope
Focus on files matching: controllers, routes, services, models
```

## How Agents Are Used

### By `/cs-team`

1. Reads `agents/*.yaml` to build expertise inventory
2. Matches agent expertise arrays against task requirements
3. Selects 2-5 agents with complementary, non-overlapping scopes
4. Spawns agents via `Task(subagent_type="agent-name")`
5. Assigns tasks based on `file_scope_hints` to prevent edit conflicts

### By Quality Gate Hooks

- `teammate-idle.cjs` (TeammateIdle): checks if agent ran required quality gates before going idle
- `task-completed.cjs` (TaskCompleted): validates gates passed before accepting task completion
- Agent's `quality_gates` from YAML determines which gates are enforced

### Known Roles Fast-Path

`agent-tracker.cjs` maintains a `KNOWN_ROLES` set for SubagentStart performance:

```
implementer, reviewer, researcher, tester, architect, general-purpose
```

For these, the hook skips YAML scanning and assigns the role directly. Unknown agent types trigger a full `agents/*.yaml` scan.

## Business Rules

- **File partition required**: When parallelizing, partition `file_scope_hints` carefully. Two agents editing the same file causes "file modified since read" errors requiring re-reads.
- **Schema validation**: Run `node agents/__tests__/test-agents.js` to validate. Enforces required fields, minimum expertise count, spawn_prompt length.
- **Version consistency**: All agent YAMLs must use the same version as the project. Schema tests enforce this.
- **Role enum constraint**: `role` must be one of the 5 valid values — no freeform strings.
- **Quality gates at completion**: Agents must run their declared `quality_gates` before any task is marked complete. Hooks enforce this.
- **Agent availability**: Any `.claude/agents/*.md` file is immediately available via `Task(subagent_type="name")` — no registration required.

## Edge Cases

- **No matching agent**: `/cs-team` falls back to generic role prompts if no agent YAML matches a required expertise.
- **Agent without YAML**: A `.claude/agents/*.md` file without a corresponding `agents/*.yaml` is invocable but not included in `/cs-team` expertise matching.
- **YAML without .md**: Agent is used for expertise matching by `/cs-team` but cannot be directly invoked via `Task()`. `/cs-team` will generate a prompt from the YAML `spawn_prompt`.
- **file_scope_hints overlap**: If two agents have overlapping globs, the team lead must explicitly partition work in task descriptions to avoid conflicts.
- **maxTurns exceeded**: Agent stops and reports partial completion. Team lead detects via task remaining in_progress state.
