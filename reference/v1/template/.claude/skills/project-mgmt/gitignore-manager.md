---
name: gitignore-manager
description: Ensure .gitignore is comprehensive for the project's tech stack
model: haiku
---

# Gitignore Manager

Automatically ensures .gitignore is comprehensive for the project's tech stack.

## Description

Use when initializing projects, before commits, or when adding new technologies.
Triggers on: "update gitignore", "check gitignore", "fix gitignore", "initialize", "before commit", "add .gitignore".

## When This Activates

- During project initialization
- When new dependencies/technologies are added
- Before first commit on a new project
- When user asks about gitignore

## Process

### Step 1: Detect Technologies

Check for these indicators and map to gitignore needs:

| File/Pattern | Technology | Ignore Entries |
|--------------|------------|----------------|
| `package.json` | Node.js | `node_modules/`, `.npm`, `*.log` |
| `package-lock.json` | npm | (covered above) |
| `yarn.lock` | Yarn | `.yarn/`, `.pnp.*` |
| `pnpm-lock.yaml` | pnpm | `.pnpm-store/` |
| `requirements.txt` | Python | `__pycache__/`, `*.pyc`, `.venv/`, `venv/` |
| `pyproject.toml` | Python | `*.egg-info/`, `.eggs/`, `dist/`, `build/` |
| `Pipfile` | Pipenv | `.venv/` |
| `go.mod` | Go | `vendor/` (optional) |
| `Cargo.toml` | Rust | `target/`, `Cargo.lock` (if library) |
| `*.csproj` | .NET | `bin/`, `obj/`, `*.user` |
| `pom.xml` | Java/Maven | `target/` |
| `build.gradle` | Java/Gradle | `build/`, `.gradle/` |
| `Gemfile` | Ruby | `.bundle/`, `vendor/bundle/` |
| `composer.json` | PHP | `vendor/` |
| `mix.exs` | Elixir | `_build/`, `deps/` |
| `pubspec.yaml` | Dart/Flutter | `.dart_tool/`, `build/` |

### Step 2: Check for Frameworks

| Indicator | Framework | Additional Ignores |
|-----------|-----------|-------------------|
| `next.config.*` | Next.js | `.next/`, `out/` |
| `nuxt.config.*` | Nuxt | `.nuxt/`, `.output/` |
| `vite.config.*` | Vite | `dist/` |
| `angular.json` | Angular | `.angular/` |
| `svelte.config.*` | SvelteKit | `.svelte-kit/` |
| `astro.config.*` | Astro | `dist/` |
| `remix.config.*` | Remix | `.cache/`, `build/`, `public/build/` |
| `gatsby-config.*` | Gatsby | `.cache/`, `public/` |
| `docker-compose.*` | Docker | (none specific) |
| `serverless.yml` | Serverless | `.serverless/` |
| `terraform/` | Terraform | `.terraform/`, `*.tfstate*` |

### Step 3: Universal Entries (Always Include)

```gitignore
# Environment and secrets
.env
.env.local
.env.*.local
*.pem
*.key
secrets/
.secrets

# IDE and editors
.idea/
.vscode/
*.swp
*.swo
*~
.project
.classpath
.settings/

# OS files
.DS_Store
Thumbs.db
desktop.ini

# Logs
*.log
logs/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Testing and coverage
coverage/
.nyc_output/
*.lcov
.coverage
htmlcov/

# Build artifacts (generic)
dist/
build/
out/
*.min.js
*.min.css

# Temporary files
tmp/
temp/
*.tmp
*.temp
*.bak

# Claude Code context (optional - may want to track)
# .claude/context/

# Claude Code metrics (local only)
.claude/metrics/
```

### Step 4: Merge Strategy

When updating .gitignore:

1. **Read existing** .gitignore if present
2. **Preserve** all existing entries (user may have custom rules)
3. **Add missing** entries based on detected tech stack
4. **Group** entries by category with comments
5. **Sort** within each category
6. **Remove duplicates**

### Step 5: Implementation

```bash
# Check if .gitignore exists
if [ -f .gitignore ]; then
    echo "Existing .gitignore found - will merge"
else
    echo "Creating new .gitignore"
fi
```

Generate or update .gitignore with detected patterns.

## Output Format

When updating .gitignore, report:

```markdown
## .gitignore Updated

**Technologies Detected:**
- Node.js (package.json)
- TypeScript (tsconfig.json)
- Next.js (next.config.js)

**Entries Added:**
- `node_modules/`
- `.next/`
- `.env.local`
- [X more entries]

**Already Present:**
- `.env`
- `dist/`

**Review:** Check .gitignore for any project-specific additions needed.
```

## Hard Rules

1. **Never remove** existing entries
2. **Always include** environment/secrets patterns
3. **Preserve comments** in existing .gitignore
4. **Add category headers** for clarity
5. **Check before commit** if .gitignore is missing critical entries

## Pre-Commit Check

Before any commit, verify:
- [ ] `.env` files are ignored
- [ ] `node_modules/` or equivalent is ignored
- [ ] No secrets in staged files
- [ ] Build artifacts are ignored

If .gitignore is missing critical entries, warn before committing.

## Context7 Integration

When uncertain about a technology's ignore patterns:
```
Use context7 to look up gitignore patterns for [technology]
```

## Quick Reference: Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing `.env` | Add `.env*` patterns |
| Committing `node_modules` | Add `node_modules/` |
| Committing build output | Add `dist/`, `build/`, etc. |
| Committing IDE settings | Add `.idea/`, `.vscode/` |
| Missing lock files | Usually SHOULD be committed |
| Committing coverage | Add `coverage/` |
