---
feature: Rules System
version: "1.0"
last_updated: 2026-03-04
dependencies: []
routes: []
status: draft
---

# Rules System

> Topic-specific standards that auto-load into Claude's context based on task keywords. Rules provide domain guidance (security patterns, testing conventions, API design) without polluting every session with everything at once.

## Rule Locations

Rules exist in two locations with different loading mechanisms:

| Location | Purpose | Loading Mechanism |
|----------|---------|------------------|
| `rules/*.md` | Canonical reference copies | Keyword-based loading during cs-loop INIT |
| `.claude/rules/*.md` | Active runtime copies with `paths:` frontmatter | Auto-loaded by Claude Code when working on matching files |

Both directories stay in sync. The `rules/` directory is the source of truth.

## Available Rules (15 files)

| Rule | Focus |
|------|-------|
| `_index.md` | Keyword-to-rule mapping table (this file) |
| `anthropic-patterns` | Universal Claude prompt patterns for all interactions |
| `code-quality` | Complexity limits, naming, code smells |
| `learnings` | Team decisions, patterns, captured learnings |
| `security` | OWASP Top 10, auth, secrets management, input validation |
| `testing` | Coverage standards, mocks, TDD, test naming |
| `api-design` | REST conventions, response formats, versioning |
| `database` | Schema design, indexes, migrations, query optimization |
| `performance` | Caching strategies, optimization, Web Vitals |
| `documentation` | README standards, changelog format, comment quality |
| `git-workflow` | Commit conventions, branching, PR process |
| `error-handling` | Error types, propagation, logging on failure |
| `logging` | Structured logging, levels, context fields |
| `ui-ux-design` | Spacing, typography, accessibility (WCAG), color |
| `terminal-ui` | Spinners, colors, progress bars, CLI aesthetics |
| `prompt-structure` | XML tags, command templates, `<avoid>` sections |

## Always-Loaded Rules (3)

These load every session regardless of task keywords:

| Rule | Why Always |
|------|-----------|
| `anthropic-patterns` | Universal Claude interaction patterns |
| `code-quality` | Applied to all source code changes |
| `learnings` | Team decisions that override defaults |

## Keyword Auto-Loading

During `/cs-loop` INIT, rules load based on task keywords (two-step process):

**Step 1 — Keyword matching:**

| Keywords | Rules Loaded |
|----------|-------------|
| `auth`, `login`, `password`, `jwt`, `oauth` | `security`, `api-design` |
| `test`, `spec`, `coverage`, `mock` | `testing` |
| `api`, `endpoint`, `route`, `rest` | `api-design`, `error-handling` |
| `database`, `query`, `schema`, `migration` | `database` |
| `performance`, `optimize`, `cache`, `slow` | `performance` |
| `ui`, `component`, `css`, `style` | `ui-ux-design` |
| `react`, `vue`, `svelte`, `angular`, `next`, `nuxt` | `ui-ux-design` |
| `frontend`, `web`, `responsive`, `tailwind` | `ui-ux-design` |
| `cli`, `terminal`, `command` | `terminal-ui` |
| `docs`, `readme`, `changelog` | `documentation` |
| `refactor`, `cleanup`, `quality` | `code-quality` |
| `git`, `commit`, `branch`, `pr` | `git-workflow` |
| `log`, `debug`, `trace` | `logging` |
| `error`, `exception`, `catch` | `error-handling` |
| `prompt`, `command`, `xml`, `template` | `prompt-structure` |

**Step 2 — Semantic pass:**
After keyword matching, cs-loop briefly reviews `rules/_index.md` to identify additional rules not captured by string matching but semantically relevant (e.g., error-handling rules for a debugging task where no keyword triggered).

## Path-Scoped Rules

Rules in `.claude/rules/` include `paths:` frontmatter for automatic loading:

```markdown
---
paths:
  - "**/*.ts"
  - "**/*.tsx"
---
# TypeScript-specific rules...
```

Claude Code auto-loads these rules when you open a file matching the glob — no manual invocation needed.

## Rule File Format

```markdown
---
paths:
  - "glob/pattern/**"
---
# Rule Name

> One-line description

## Section
Content...
```

The `paths:` frontmatter is optional — rules without it are only loaded via keyword matching.

## Manual Loading

Rules auto-load during `/cs-loop`. For ad-hoc loading:

```
Load @rules/security for this review
```

Or in a command's allowed-tools context using the `@` reference syntax.

## Business Rules

- **learnings.md special case**: Lives only in `.claude/rules/` (project-specific). NOT in `rules/` (reference copies). Integration tests know about this exception.
- **Stale reference removal**: Rule files must not contain links to non-existent paths. All `reference/v1/template/` footers were removed in v1.3.x.
- **Two-step loading**: Both keyword AND semantic pass run during INIT. The semantic pass catches domain-relevant rules missed by string matching.
- **No duplication**: Rules in `.claude/rules/` mirror `rules/` content. Don't maintain separate versions; keep in sync.

## Edge Cases

- **No keywords match**: Only the 3 always-loaded rules apply. Adequate for simple tasks.
- **Multiple keyword hits**: All matching rules load. Overlap is intentional — `api-design` + `error-handling` complement each other.
- **Path-scoped + keyword**: Both can load the same rule; Claude Code deduplicates.
- **Conflicting guidance**: `learnings.md` overrides rule files — it captures project-specific decisions that supersede general rules.
