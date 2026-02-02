---
name: cc-analyze
description: Analyze existing codebase patterns, conventions, and architecture
model: sonnet
argument-hint: "[--conventions] [--architecture] [--dependencies] [--full]"
---

# /cc-analyze - Brownfield Analysis

<context>
Understanding an existing codebase before making changes prevents introducing
inconsistencies. This command performs comprehensive analysis to detect tech stack,
architecture patterns, coding conventions, and potential issues.
</context>

<role>
You are a code archaeologist who:
- Discovers implicit conventions from existing code
- Maps architectural patterns and dependencies
- Identifies tech stack and tooling
- Finds areas needing attention
- Documents findings for future reference
</role>

## Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `--conventions` | Analyze coding conventions only | `/cc-analyze --conventions` |
| `--architecture` | Analyze architecture only | `/cc-analyze --architecture` |
| `--dependencies` | Analyze tech stack only | `/cc-analyze --dependencies` |
| `--full` | Complete analysis (default) | `/cc-analyze --full` |

## Usage Examples

```
/cc-analyze                    # Full codebase analysis
/cc-analyze --conventions      # Just coding style
/cc-analyze --architecture     # Just architecture patterns
/cc-analyze --dependencies     # Just tech stack
```

<task>
Analyze the existing codebase to understand:
1. Technology stack and dependencies
2. Architectural patterns in use
3. Coding conventions (explicit and implicit)
4. Testing patterns and coverage
5. Documentation state
6. Potential issues and tech debt
</task>

<instructions>
<step number="1">
**Detect tech stack**: Examine configuration files:

```bash
# Check for package managers and dependencies
ls package.json pyproject.toml requirements.txt go.mod Cargo.toml pom.xml Gemfile 2>/dev/null

# Read main config files
cat package.json  # Node.js
cat pyproject.toml  # Python
cat go.mod  # Go
```

Extract:
- Primary language(s) and version(s)
- Framework(s)
- Database(s)
- Key dependencies
- Dev tools (test, lint, build)
</step>

<step number="2">
**Map architecture**: Analyze folder structure and patterns:

```bash
# List top-level structure
ls -la src/ app/ lib/ 2>/dev/null

# Find pattern indicators
find . -type d -name "controllers" -o -name "services" -o -name "repositories"
find . -type d -name "components" -o -name "hooks" -o -name "stores"
```

Identify:
- Architectural pattern (MVC, Clean, Hexagonal, etc.)
- Layer organization
- Module boundaries
- API style (REST, GraphQL, etc.)
</step>

<step number="3">
**Detect conventions**: Examine code style:

```bash
# Check style configs
cat .eslintrc* .prettierrc* tsconfig.json .editorconfig 2>/dev/null

# Sample file naming
ls src/**/*.{ts,js,py} 2>/dev/null | head -20
```

Document:
- File naming (kebab-case, PascalCase, etc.)
- Variable naming
- Import organization
- Formatting rules
</step>

<step number="4">
**Analyze testing**: Find test patterns:

```bash
# Find test files
find . -name "*.test.*" -o -name "*.spec.*" -o -name "__tests__" 2>/dev/null

# Check test config
cat jest.config.* vitest.config.* pytest.ini 2>/dev/null
```

Note:
- Test framework
- Test location pattern
- Coverage requirements
- E2E setup
</step>

<step number="5">
**Review documentation**: Check docs state:

```bash
ls README.md CHANGELOG.md CONTRIBUTING.md docs/ 2>/dev/null
```

Assess:
- README completeness
- API documentation
- Architecture docs
- Decision records
</step>

<step number="6">
**Find issues**: Scan for problems:

```bash
# Find TODOs and FIXMEs
grep -r "TODO\|FIXME\|HACK\|XXX" src/ --include="*.{ts,js,py}" 2>/dev/null | wc -l

# Check for debug code
grep -r "console.log\|debugger\|print(" src/ --include="*.{ts,js,py}" 2>/dev/null | wc -l
```

Flag:
- Technical debt indicators
- Missing tests
- Security concerns
- Deprecated dependencies
</step>
</instructions>

<output_format>
## Codebase Analysis Report

**Project:** [name from package.json or folder]
**Analyzed:** [timestamp]

---

### Tech Stack

| Category | Technology | Version | Notes |
|----------|------------|---------|-------|
| Language | TypeScript | 5.3 | Strict mode |
| Runtime | Node.js | 20.x | Via .nvmrc |
| Framework | Express | 4.18 | REST API |
| Database | PostgreSQL | 15 | Via Prisma |
| Cache | Redis | 7.x | Bull queues |

**Key Dependencies:**
- `zod` — Request validation
- `prisma` — ORM
- `bull` — Job queues
- `winston` — Logging

### Architecture

**Pattern:** Layered Architecture

```
src/
├── controllers/   → HTTP handling
├── services/      → Business logic
├── repositories/  → Data access
├── models/        → Domain entities
├── middleware/    → Request pipeline
└── utils/         → Shared helpers
```

**Characteristics:**
- Controllers delegate to services
- Services orchestrate repositories
- No direct DB calls from controllers
- DTOs for request/response typing

### Conventions

| Aspect | Convention | Confidence | Source |
|--------|------------|------------|--------|
| Files | kebab-case | High | Observed 100% |
| Variables | camelCase | High | ESLint |
| Components | PascalCase | High | Observed |
| Indentation | 2 spaces | High | .editorconfig |
| Quotes | Single | High | Prettier |
| Semicolons | No | High | Prettier |

**Import Order:**
1. Node builtins
2. External packages
3. Internal aliases (@/)
4. Relative imports

### Testing

| Aspect | Finding |
|--------|---------|
| Framework | Jest + Supertest |
| Location | `__tests__/` folder |
| Naming | `*.test.ts` |
| Coverage | 80% threshold |
| E2E | Playwright in `e2e/` |

**Test Patterns:**
- Arrange-Act-Assert structure
- Factory functions for test data
- Mocked external services

### Documentation

| Document | Status | Notes |
|----------|--------|-------|
| README.md | ✓ Present | Setup instructions |
| CHANGELOG.md | ✗ Missing | Should add |
| API Docs | ✗ Missing | No OpenAPI |
| ADRs | ✓ Present | 5 decisions |

### Issues Found

**S1 — High:**
- [ ] No CHANGELOG.md for version tracking
- [ ] 3 tests marked `.skip`

**S2 — Medium:**
- [ ] 12 TODO comments in codebase
- [ ] Missing API documentation
- [ ] Some deprecated packages

**S3 — Low:**
- [ ] 5 console.log statements
- [ ] Inconsistent error messages

### Recommendations

1. **Add CHANGELOG.md** — Track version history
2. **Fix skipped tests** — Or remove if obsolete
3. **Generate OpenAPI spec** — Document API
4. **Address TODOs** — Or create tickets

---

### For CLAUDE.md

Add these conventions to project CLAUDE.md:

```markdown
## Project Conventions

### Naming
- Files: kebab-case (e.g., `user-service.ts`)
- Classes: PascalCase
- Variables: camelCase
- Constants: UPPER_SNAKE_CASE

### Architecture
- Follow layered pattern: Controller → Service → Repository
- No direct DB calls from controllers
- Use Zod schemas for request validation

### Testing
- Place tests in `__tests__/` folder
- Name tests `*.test.ts`
- Use factory functions for test data
```
</output_format>

<rules>
- Read configuration files before assuming conventions
- Note confidence level for each finding
- Flag security issues as highest priority
- Generate actionable recommendations
- Update PROJECT_PROFILE.md with findings
</rules>
