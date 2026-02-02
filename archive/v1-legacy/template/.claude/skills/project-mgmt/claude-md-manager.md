---
name: claude-md-manager
description: Create or improve project CLAUDE.md files based on project analysis
context: fork
model: sonnet
---

# Skill: CLAUDE.md Manager

## Description

Intelligently create or improve root-level CLAUDE.md files based on project analysis. Ensures every project has comprehensive, accurate documentation that integrates with the prompts library workflow.

---

## Triggers

Activate this skill when:
- User says "create claude.md", "generate claude.md", "init claude.md"
- User says "improve claude.md", "update claude.md", "fix claude.md"
- User runs `/claude-md` command
- Project initialization and no root CLAUDE.md exists
- User asks about project documentation setup

---

## Analysis Process

### 1. Tech Stack Detection

**Package Managers & Languages:**
```
package.json          → Node.js (check engines for version)
package-lock.json     → npm
yarn.lock             → Yarn
pnpm-lock.yaml        → pnpm
requirements.txt      → Python
pyproject.toml        → Python (modern)
Pipfile               → Python (pipenv)
Cargo.toml            → Rust
go.mod                → Go
*.csproj              → .NET/C#
*.fsproj              → F#
build.gradle          → Java/Kotlin (Gradle)
pom.xml               → Java (Maven)
Gemfile               → Ruby
composer.json         → PHP
mix.exs               → Elixir
pubspec.yaml          → Dart/Flutter
```

**Frameworks (from dependencies):**
```
react                 → React
next                  → Next.js
vue                   → Vue.js
nuxt                  → Nuxt
angular               → Angular
svelte                → Svelte
express               → Express.js
fastify               → Fastify
nestjs                → NestJS
django                → Django
flask                 → Flask
fastapi               → FastAPI
rails                 → Ruby on Rails
laravel               → Laravel
gin                   → Gin (Go)
echo                  → Echo (Go)
actix                 → Actix (Rust)
axum                  → Axum (Rust)
```

**Databases (from dependencies or config):**
```
prisma                → Prisma ORM
sequelize             → Sequelize
typeorm               → TypeORM
mongoose              → MongoDB
pg / postgres         → PostgreSQL
mysql                 → MySQL
sqlite                → SQLite
redis                 → Redis
```

**Testing (from dependencies or config):**
```
jest                  → Jest
vitest                → Vitest
mocha                 → Mocha
pytest                → Pytest
unittest              → Python unittest
rspec                 → RSpec
phpunit               → PHPUnit
go test               → Go testing
cargo test            → Rust testing
```

### 2. Architecture Detection

**Directory Patterns:**
```
src/                  → Source code
lib/                  → Library code
app/                  → Application code (Rails, Next.js)
pages/                → Page components (Next.js, Nuxt)
components/           → UI components
controllers/          → MVC controllers
services/             → Service layer
models/               → Data models
entities/             → Domain entities
repositories/         → Data access
middleware/           → Middleware
routes/               → Route definitions
api/                  → API endpoints
utils/ or helpers/    → Utility functions
config/               → Configuration
tests/ or __tests__/  → Test files
spec/                 → Test specs (Ruby)
```

**Config Files:**
```
.eslintrc*            → ESLint config
.prettierrc*          → Prettier config
tsconfig.json         → TypeScript config
jest.config.*         → Jest config
vite.config.*         → Vite config
webpack.config.*      → Webpack config
docker-compose.yml    → Docker services
Dockerfile            → Container build
.env.example          → Environment template
```

### 3. Code Pattern Detection

**Analyze sample files for:**
- Naming conventions (check 5-10 files)
- Import ordering patterns
- Error handling approach
- Logging usage
- Comment style
- Type usage (TypeScript, type hints)

### 4. Existing Documentation

**Check for:**
- README.md content
- docs/ folder
- CONTRIBUTING.md
- API documentation
- Inline code comments

---

## CLAUDE.md Quality Checklist

### Required Sections (Must Have)

```
□ Overview — Clear project description
□ Tech Stack — Accurate, versioned
□ Architecture — Directory structure explained
□ Development Setup — Complete, working instructions
□ Code Standards — Naming, formatting documented
□ Testing — How to run, coverage expectations
□ Key Files — Important files listed
□ Common Tasks — Commands documented
□ Workflow Integration — References .claude/
```

### Quality Criteria

**Overview:**
- [ ] Describes what the project does
- [ ] Identifies target users/audience
- [ ] 1-3 sentences max

**Tech Stack:**
- [ ] Lists all major technologies
- [ ] Includes versions where relevant
- [ ] Explains purpose of key dependencies

**Architecture:**
- [ ] Shows directory structure
- [ ] Explains purpose of each major folder
- [ ] Documents key patterns used

**Development Setup:**
- [ ] Lists prerequisites with versions
- [ ] Step-by-step installation
- [ ] Environment variable documentation
- [ ] Instructions actually work

**Code Standards:**
- [ ] Naming conventions for all types
- [ ] Formatting rules documented
- [ ] Import ordering specified
- [ ] Error handling approach documented

**Testing:**
- [ ] Test framework identified
- [ ] How to run tests
- [ ] Coverage requirements stated
- [ ] Test file location/naming

**Key Files:**
- [ ] Entry points identified
- [ ] Config files listed
- [ ] Generated files marked

**Common Tasks:**
- [ ] All frequent commands listed
- [ ] Commands are accurate
- [ ] Covers dev, test, build, deploy

**Workflow Integration:**
- [ ] References .claude/ folder
- [ ] Mentions state files
- [ ] Lists key commands

---

## Improvement Strategies

### When Improving Existing CLAUDE.md

**1. Gap Analysis:**
- Compare against required sections checklist
- Identify missing sections
- Note incomplete sections

**2. Accuracy Check:**
- Compare tech stack to actual dependencies
- Verify commands actually work
- Check if architecture matches reality

**3. Staleness Detection:**
- Look for outdated versions
- Check for deprecated dependencies
- Verify file paths still exist

**4. Enhancement Opportunities:**
- Add missing context
- Improve unclear sections
- Add workflow integration if missing

### Preservation Rules

When improving, ALWAYS preserve:
- Custom sections user added
- Project-specific notes
- Unique conventions
- Historical context

Never remove content unless:
- It's demonstrably incorrect
- User explicitly approves removal

---

## Output Formats

### New CLAUDE.md Report

```
╔══════════════════════════════════════════════════════════════╗
║  CLAUDE.md Created for [Project Name]                        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Tech Stack Detected:                                        ║
║  • Node.js 20 (from package.json engines)                    ║
║  • TypeScript 5.3 (from devDependencies)                     ║
║  • React 18.2 (from dependencies)                            ║
║  • PostgreSQL (from prisma schema)                           ║
║  • Jest (from devDependencies)                               ║
║                                                              ║
║  Architecture Pattern: Component-based with services         ║
║                                                              ║
║  Sections Generated:                                         ║
║  ✓ Overview                                                  ║
║  ✓ Tech Stack                                                ║
║  ✓ Architecture                                              ║
║  ✓ Development Setup                                         ║
║  ✓ Code Standards (detected from .eslintrc, .prettierrc)    ║
║  ✓ Testing                                                   ║
║  ✓ Key Files                                                 ║
║  ✓ Common Tasks (from package.json scripts)                  ║
║  ✓ Workflow Integration                                      ║
║                                                              ║
║  Review Required:                                            ║
║  ⚠ Overview — Verify description accuracy                    ║
║  ⚠ Setup — Test installation steps                           ║
║  ⚠ Standards — Confirm conventions match team practice       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Improvement Report

```
╔══════════════════════════════════════════════════════════════╗
║  CLAUDE.md Analysis for [Project Name]                       ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Current State: 6/9 required sections                        ║
║                                                              ║
║  Missing Sections:                                           ║
║  ✗ Testing — No testing documentation                        ║
║  ✗ Key Files — Important files not listed                    ║
║  ✗ Workflow Integration — No .claude/ reference              ║
║                                                              ║
║  Improvements Needed:                                        ║
║  △ Tech Stack — Missing TypeScript version                   ║
║  △ Architecture — Outdated folder structure                  ║
║  △ Setup — Missing environment variables                     ║
║                                                              ║
║  Accurate Sections:                                          ║
║  ✓ Overview                                                  ║
║  ✓ Code Standards                                            ║
║  ✓ Common Tasks                                              ║
║                                                              ║
║  Recommended Actions:                                        ║
║  1. Add Testing section with Jest configuration              ║
║  2. Add Key Files section                                    ║
║  3. Add Workflow Integration section                         ║
║  4. Update Tech Stack with TypeScript 5.3                    ║
║  5. Update Architecture to match current structure           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

Apply improvements? [Y/n]
```

---

## Integration with Project Init

When `/scout-skills` or "initialize this project" runs:

1. Check if root CLAUDE.md exists
2. If NO: Offer to create one
3. If YES: Offer to analyze and improve
4. Respect user choice (don't force)

---

## Hard Rules

1. **Never overwrite without consent** — Always show changes first
2. **Preserve user content** — Custom sections are sacred
3. **Accuracy over assumptions** — Mark uncertain sections for review
4. **Detect, don't invent** — Base content on actual project analysis
5. **Keep it current** — CLAUDE.md should reflect actual project state
6. **Integration required** — Always include workflow integration section

---

## Examples

### Minimal Detection (Unknown Project)

If analysis finds limited information:

```markdown
# [folder-name]

## Overview

<!-- TODO: Add project description -->

## Tech Stack

Unable to detect tech stack automatically. Please document:
- Primary language
- Framework (if any)
- Database (if any)
- Testing framework

## Development Setup

<!-- TODO: Add setup instructions -->

## Workflow Integration

This project uses the prompts library. See `.claude/` for commands and skills.
```

### Rich Detection (Well-Configured Project)

Full CLAUDE.md with all sections populated from detected information.
