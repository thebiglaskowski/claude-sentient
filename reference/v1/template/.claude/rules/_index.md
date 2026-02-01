# Rules Index

## Overview

Rules provide modular, topic-specific guidance that can be loaded on-demand using `@rules/[name]` syntax. Unlike skills (which trigger automatically), rules are explicit references for deep context on a topic.

---

## Available Rules

| Rule | Purpose | Load With |
|------|---------|-----------|
| `security` | OWASP, authentication, secrets | `@rules/security` |
| `testing` | Coverage, naming, mocks, TDD | `@rules/testing` |
| `git-workflow` | Commits, branches, PRs | `@rules/git-workflow` |
| `documentation` | README, comments, changelog | `@rules/documentation` |
| `code-quality` | Complexity, naming, deps | `@rules/code-quality` |
| `api-design` | REST, errors, versioning | `@rules/api-design` |
| `error-handling` | Hierarchy, logging, recovery | `@rules/error-handling` |
| `ui-ux-design` | Spacing, typography, accessibility | `@rules/ui-ux-design` |
| `terminal-ui` | Spinners, colors, progress bars | `@rules/terminal-ui` |
| `performance` | Optimization, caching, Web Vitals | `@rules/performance` |
| `database` | Schema design, indexing, migrations | `@rules/database` |
| `logging` | Structured logs, levels, context | `@rules/logging` |
| `prompt-engineering` | AI prompts, techniques, patterns | `@rules/prompt-engineering` |

---

## How to Use Rules

### In Commands
```markdown
When performing security audits, load `@rules/security` for detailed guidance.
```

### In Skills
```markdown
---
rules:
  - security
  - testing
---
```

### In Conversation
```
User: Review this auth code with security rules
Claude: [Loads @rules/security, applies comprehensive security checks]
```

---

## Rule vs Skill

| Aspect | Rule | Skill |
|--------|------|-------|
| Activation | Explicit (`@rules/name`) | Automatic (trigger phrases) |
| Purpose | Reference documentation | Behavioral guidance |
| Scope | Topic-specific standards | Task-specific actions |
| Loading | On-demand | Auto-detected |

---

## Creating New Rules

1. Create `rules/[topic].md`
2. Include clear sections with standards
3. Add to this index
4. Reference in relevant skills/commands

### Rule Template
```markdown
# [Topic] Rules

## Core Principles
[3-5 guiding principles]

## Standards
[Specific requirements with examples]

## Anti-Patterns
[What NOT to do]

## Checklist
[Quick verification list]
```
