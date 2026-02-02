---
name: brownfield-analyzer
description: Auto-detect existing project patterns, conventions, and architecture
disable-model-invocation: false
trigger-phrases:
  - "analyze this codebase"
  - "detect project patterns"
  - "understand this project"
  - "brownfield analysis"
  - "existing project"
  - "what patterns does this use"
rules:
  - code-quality
---

# Brownfield Analyzer

Automatically analyze existing codebases to detect patterns, conventions, and architecture before making changes.

---

## Purpose

When working with existing projects, understanding established patterns is critical:
- Avoid introducing inconsistent code styles
- Respect existing architectural decisions
- Identify tech stack and dependencies
- Document implicit conventions
- Find areas needing attention

---

## Activation

This skill activates when:
1. `/cc-claude-md` is run on existing project
2. User asks to "understand this project"
3. First significant code change in unfamiliar codebase
4. Project initialization detects existing code

---

## Analysis Process

### Phase 1: Tech Stack Detection

```
Scan for indicators:
├── package.json → Node.js ecosystem
│   ├── dependencies → Runtime tech
│   ├── devDependencies → Build/test tools
│   └── scripts → Available commands
├── requirements.txt / pyproject.toml → Python
├── go.mod → Go
├── Cargo.toml → Rust
├── pom.xml / build.gradle → Java
├── Gemfile → Ruby
└── .tool-versions / .nvmrc → Version managers
```

**Extract:**
- Primary language(s)
- Framework(s) in use
- Package manager
- Build system
- Test framework
- Linter/formatter

### Phase 2: Architecture Pattern Detection

```
Analyze structure:
├── src/
│   ├── controllers/ → MVC pattern
│   ├── services/ → Service layer
│   ├── repositories/ → Repository pattern
│   ├── models/ / entities/ → Domain models
│   ├── routes/ / api/ → API layer
│   ├── components/ → Component-based (React/Vue)
│   ├── hooks/ → Custom hooks (React)
│   ├── stores/ / state/ → State management
│   └── utils/ / helpers/ → Utilities
```

**Identify:**
- Architectural pattern (MVC, Clean, Hexagonal, etc.)
- Layer organization
- Module boundaries
- Dependency direction

### Phase 3: Convention Detection

**Naming conventions:**
```
Files: kebab-case, PascalCase, snake_case
Variables: camelCase, snake_case
Constants: UPPER_SNAKE_CASE
Components: PascalCase
```

**Code style indicators:**
- Semicolons (yes/no)
- Quote style (single/double)
- Indentation (tabs/spaces, width)
- Trailing commas
- Import ordering

**Configuration files:**
- `.eslintrc` / `eslint.config.js`
- `.prettierrc`
- `tsconfig.json`
- `.editorconfig`

### Phase 4: Testing Patterns

```
Detect test setup:
├── __tests__/ → Jest default
├── tests/ → General test folder
├── *.test.ts → Co-located tests
├── *.spec.ts → Spec naming
├── cypress/ / e2e/ → E2E tests
└── fixtures/ / mocks/ → Test utilities
```

**Identify:**
- Test framework
- Test file location
- Naming convention
- Coverage configuration
- Mock patterns

### Phase 5: Documentation Patterns

```
Check for:
├── README.md → Project documentation
├── docs/ → Documentation folder
├── CHANGELOG.md → Version history
├── CONTRIBUTING.md → Contribution guide
├── ADRs / decisions/ → Architecture decisions
└── API docs → OpenAPI/Swagger
```

### Phase 6: CI/CD & DevOps

```
Detect:
├── .github/workflows/ → GitHub Actions
├── .gitlab-ci.yml → GitLab CI
├── Jenkinsfile → Jenkins
├── Dockerfile → Containerization
├── docker-compose.yml → Local dev
├── k8s/ / kubernetes/ → Kubernetes
└── terraform/ / infra/ → IaC
```

---

## Output: Project Profile

Generate a structured analysis:

```markdown
## Project Profile

### Tech Stack
- **Language:** TypeScript 5.3
- **Runtime:** Node.js 20
- **Framework:** Express.js 4.18
- **Database:** PostgreSQL (via Prisma)
- **Cache:** Redis
- **Queue:** Bull

### Architecture
- **Pattern:** Layered (Controller → Service → Repository)
- **API Style:** REST
- **Auth:** JWT with refresh tokens

### Conventions
| Aspect | Convention | Source |
|--------|------------|--------|
| File naming | kebab-case | Observed |
| Variables | camelCase | ESLint config |
| Indentation | 2 spaces | .editorconfig |
| Quotes | Single | Prettier |
| Semicolons | No | Prettier |
| Imports | Grouped, sorted | ESLint |

### Testing
- **Framework:** Jest + Supertest
- **Location:** `__tests__/` folder
- **Coverage:** 80% threshold
- **E2E:** Playwright

### Patterns Observed
1. **Repository pattern** — All DB access via repositories
2. **DTO validation** — Zod schemas for request validation
3. **Error hierarchy** — Custom error classes in `src/errors/`
4. **Middleware chain** — Auth → Validate → Handle

### Quality Tools
- ESLint + Prettier (pre-commit hook)
- TypeScript strict mode
- Husky + lint-staged

### Potential Issues
- [ ] No CHANGELOG.md
- [ ] Missing API documentation
- [ ] Some tests skipped (.skip)
- [ ] TODO comments: 12 found
```

---

## Integration with Workflow

### Before Making Changes

1. Run brownfield analysis if project unfamiliar
2. Load detected conventions into context
3. Follow established patterns
4. Flag deviations for discussion

### Updating CLAUDE.md

Analysis results feed into project CLAUDE.md:

```markdown
## Project Conventions (Auto-Detected)

Based on brownfield analysis of existing codebase:

### Must Follow
- Use kebab-case for file names
- Place tests in `__tests__/` folder
- Use Zod for request validation
- Follow repository pattern for data access

### Architecture
- Controllers handle HTTP, delegate to services
- Services contain business logic
- Repositories handle data access
- No direct DB calls from controllers
```

---

## Commands

### Manual Analysis

```
/cc-analyze                    # Run full brownfield analysis
/cc-analyze --conventions      # Just coding conventions
/cc-analyze --architecture     # Just architecture patterns
/cc-analyze --dependencies     # Just tech stack
```

### Integration Points

- `/cc-claude-md` — Uses analysis for project CLAUDE.md
- `/cc-review` — Checks against detected conventions
- `/cc-scaffold` — Follows detected patterns

---

## Anti-Patterns to Detect

Flag these for attention:

| Anti-Pattern | Indicator | Severity |
|--------------|-----------|----------|
| God class | Class > 500 lines | Medium |
| Circular deps | Import cycles | High |
| Mixed patterns | MVC + Clean architecture | Medium |
| No tests | Missing test folder | High |
| Hardcoded secrets | .env patterns in code | Critical |
| Console.log | Debug statements | Low |
| TODO debt | Excessive TODO comments | Low |

---

## Confidence Levels

Analysis confidence varies:

| Confidence | Meaning | Action |
|------------|---------|--------|
| **High** | Config file explicitly states | Follow strictly |
| **Medium** | Consistent pattern observed | Follow, note assumption |
| **Low** | Inconsistent or unclear | Ask before assuming |

Example:
```
- Indentation: 2 spaces (HIGH - .editorconfig)
- Import order: grouped (MEDIUM - 80% consistent)
- Error handling: unclear (LOW - mixed patterns)
```

---

## Caching

Store analysis in `.claude/context/PROJECT_PROFILE.md`:
- Regenerate on major changes
- Reference for all operations
- Update when patterns evolve
