# Agents Index

## Overview

Agents are specialized subagent definitions that can be spawned for focused tasks. Each agent has:
- Specific expertise area
- Recommended model
- Context isolation (fork)
- Defined output format

---

## Available Agents (15 Total)

| Agent | Model | Expertise | Use Case |
|-------|-------|-----------|----------|
| `code-reviewer` | sonnet | Quality, patterns, tests | Code review tasks |
| `security-analyst` | opus | OWASP, STRIDE, vulns | Security audits |
| `test-engineer` | sonnet | Coverage, mocks, TDD | Test writing/analysis |
| `documentation-writer` | sonnet | README, API docs | Documentation tasks |
| `researcher` | sonnet | Tech research, spikes | Investigation tasks |
| `ui-ux-expert` | sonnet | Modern UI, accessibility | Web interface design |
| `terminal-ui-expert` | sonnet | CLI polish, spinners, colors | Terminal app UX |
| `seo-expert` | sonnet | Meta tags, structured data | Search optimization |
| `database-expert` | sonnet | Schema, queries, migrations | Database optimization |
| `devops-engineer` | sonnet | CI/CD, Docker, K8s | Infrastructure tasks |
| `accessibility-expert` | sonnet | WCAG, ARIA, screen readers | A11y compliance |
| `performance-optimizer` | sonnet | Profiling, caching, Core Web Vitals | Performance tuning |
| `api-designer` | sonnet | REST/GraphQL, OpenAPI | API design review |
| `migration-specialist` | sonnet | DB migrations, version upgrades | Migration planning |
| `prompt-engineer` | sonnet | AI prompts, best practices | Prompt optimization |

---

## How to Use Agents

### Spawning an Agent

```
Spawn code-reviewer agent to review the auth module
```

or

```
Use security-analyst to audit src/api
```

### In Commands

Commands can specify agents:
```markdown
## Agent
Use: `code-reviewer`
Model: sonnet
Context: fork
```

### Automatic Agent Selection

Based on task type, agents are selected automatically:
- "Review this code" → `code-reviewer`
- "Check for vulnerabilities" → `security-analyst`
- "Write tests for" → `test-engineer`
- "Document this" → `documentation-writer`
- "Research how to" → `researcher`
- "Design the UI" → `ui-ux-expert`
- "Make CLI output pretty" → `terminal-ui-expert`
- "Optimize for search engines" → `seo-expert`
- "Optimize database" → `database-expert`
- "Set up CI/CD" → `devops-engineer`
- "Check accessibility" → `accessibility-expert`

---

## Agent Capabilities

### What Agents Can Do

- Read files extensively
- Analyze code patterns
- Search the codebase
- Generate structured reports
- Make recommendations

### What Agents Return

Each agent returns a focused summary:
```markdown
## Agent Report: [Agent Name]

### Findings
[Structured findings]

### Recommendations
[Actionable recommendations]

### Severity/Priority
[If applicable]
```

---

## Context Isolation

Agents work in isolated contexts:

```
Main Conversation
       │
       ├── Agent spawned ──────┐
       │                       │ (isolated context)
       │                       │ (reads many files)
       │                       │ (generates report)
       │<── Summary returned ──┘
       │
       ▼ (continues with summary only)
```

This keeps the main conversation clean while allowing deep exploration.

---

## Creating Custom Agents

Create new agents in `.claude/agents/`:

```markdown
---
name: agent-name
description: What this agent does in one line
tools: Read, Grep, Glob, Bash
disallowedTools: Write, Edit
model: sonnet
---

# Agent: [Name]

## Expertise
[What this agent specializes in]

## Process
[How the agent approaches tasks]

## Output Format
[What the agent returns]
```

### Valid Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Agent identifier (kebab-case) |
| `description` | Yes | One-line description |
| `tools` | No | Comma-separated allowed tools |
| `disallowedTools` | No | Tools agent cannot use |
| `model` | No | `haiku`, `sonnet`, or `opus` |
| `permissionMode` | No | Permission handling mode |
| `skills` | No | Skills available to agent |
| `hooks` | No | Agent-specific hooks |

---

## Model Selection by Agent

| Task Complexity | Recommended |
|-----------------|-------------|
| Simple search/lookup | haiku |
| Code analysis | sonnet |
| Security/Architecture | opus |

Agents default to their recommended model but can be overridden:
```
Spawn code-reviewer with opus for deep review
```
