# Agent Role Definitions

Reference for matching work streams to agent roles during team orchestration.

## Available Agents

| Agent | Description | Expertise Areas |
|-------|-------------|----------------|
| **architect** | Design patterns, code quality, dependency management | Architecture reviews, refactoring, complexity reduction |
| **backend** | API design, database operations, server-side performance | API endpoints, database queries, auth, caching |
| **frontend** | UI components, accessibility, responsive design | Components, design systems, WCAG compliance |
| **database** | Schema design, migrations, query optimization | Schema changes, ORM patterns, migration scripts |
| **tester** | Test coverage, edge cases, quality assurance | Unit tests, integration tests, coverage gaps |
| **security** | Vulnerability analysis, security hardening | OWASP Top 10, auth patterns, secrets management |
| **devops** | CI/CD pipelines, containerization, deployment | Pipelines, Dockerfiles, infrastructure as code |
| **docs** | Technical writing, API docs, changelog management | READMEs, API references, changelogs |
| **build-resolver** | Build failures, dependency issues, pipeline problems | CI failures, dependency conflicts, compilation errors |

## Matching Algorithm

1. Extract task keywords and file paths
2. Match against each agent's `expertise` array
3. Score by keyword overlap count
4. Break ties by preferring more specialized agents over general ones

## Known Roles Fast-Path

The `agent-tracker.cjs` hook has a `KNOWN_ROLES` set for these built-in roles: `implementer`, `reviewer`, `researcher`, `tester`, `architect`, `general-purpose`. These skip YAML file scanning for faster tracking.

## Custom Agents

Projects can define custom agents in `.claude/agents/*.md`. Custom agents can have project-specific expertise arrays and spawn prompts.
