# Claude Sentient Rules

This directory contains path-scoped rules that Claude Code loads automatically based on file context.

## How It Works

1. Files with `paths:` frontmatter load only when Claude works on matching files
2. Files without `paths:` frontmatter load every session (unconditional)
3. Claude reads these as project-specific instructions

## Frontmatter Format

```yaml
---
paths:
  - "**/auth/**"
  - "**/middleware/**"
---
```

## Files

### Conditional Rules (12 files — loaded by path matching)

| File | Triggers When Working On |
|------|-------------------------|
| `security.md` | auth, middleware, session, token, credential files |
| `testing.md` | test files, spec files, __tests__ directories |
| `api-design.md` | api, routes, controllers, endpoints |
| `database.md` | models, migrations, schema, SQL, prisma, db |
| `ui-ux-design.md` | components, pages, styles, CSS, TSX, Vue |
| `error-handling.md` | errors, exceptions, middleware, handlers |
| `performance.md` | cache, workers, queue, performance files |
| `logging.md` | log, logger, logging files |
| `terminal-ui.md` | cli, bin, shell scripts, PowerShell |
| `documentation.md` | markdown files, docs, README |
| `prompt-structure.md` | .claude/commands, command markdown files |
| `git-workflow.md` | .github, .gitignore, git config files |

### Unconditional Rules (3 files — always loaded)

| File | Purpose |
|------|---------|
| `anthropic-patterns.md` | Universal prompt patterns for all tasks |
| `code-quality.md` | Code quality standards for all source code |
| `learnings.md` | Team-shared decisions, patterns, and learnings |

### Other Files

| File | Purpose |
|------|---------|
| `README.md` | This file |

## Reference Copies

The canonical reference copies of all rules are in `rules/` (project root). The files here are the active, path-scoped versions.

## For Projects Using Claude Sentient

When Claude Sentient is installed, the installer copies rules with frontmatter to `.claude/rules/`. Use `/cs-learn` to add entries to `learnings.md`.
