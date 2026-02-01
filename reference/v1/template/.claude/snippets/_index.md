# Snippet Registry

Indexed, searchable code snippets for rapid development.

---

## Quick Search

| Snippet | Language | Category | Description |
|---------|----------|----------|-------------|
| `snippet:express-route` | TypeScript | API | Express route handler |
| `snippet:fastapi-endpoint` | Python | API | FastAPI endpoint |
| `snippet:go-handler` | Go | API | HTTP handler |
| `snippet:react-component` | TypeScript | React | Functional component |
| `snippet:react-hook` | TypeScript | React | Custom hook |
| `snippet:react-context` | TypeScript | React | Context provider |
| `snippet:prisma-model` | Prisma | Database | Model definition |
| `snippet:sql-migration` | SQL | Database | Migration template |
| `snippet:jest-test` | TypeScript | Testing | Jest test suite |
| `snippet:pytest-test` | Python | Testing | Pytest test |
| `snippet:go-test` | Go | Testing | Go test |
| `snippet:dockerfile` | Docker | DevOps | Multi-stage Dockerfile |
| `snippet:github-action` | YAML | DevOps | CI workflow |
| `snippet:error-class` | TypeScript | Error | Custom error class |
| `snippet:logger` | TypeScript | Utility | Structured logger |
| `snippet:env-config` | TypeScript | Config | Environment config |
| `snippet:zod-schema` | TypeScript | Validation | Zod schema |
| `snippet:pydantic-model` | Python | Validation | Pydantic model |

---

## Usage

### Request a Snippet

```
"Give me snippet:express-route"
"Use snippet:react-component for the user profile"
"Apply snippet:dockerfile to this project"
```

### Search Snippets

```
"What snippets do you have for React?"
"Show me API snippets"
"List all TypeScript snippets"
```

### Customize on Use

```
"Use snippet:express-route but with authentication middleware"
"Apply snippet:react-component with TypeScript generics"
```

---

## Categories

### API Snippets
Backend route handlers and endpoints.

| Snippet | File | Framework |
|---------|------|-----------|
| [express-route](api/express-route.md) | Express handler | Express.js |
| [fastapi-endpoint](api/fastapi-endpoint.md) | FastAPI route | FastAPI |
| [go-handler](api/go-handler.md) | HTTP handler | Go stdlib |
| [nest-controller](api/nest-controller.md) | NestJS controller | NestJS |

### React Snippets
React components and hooks.

| Snippet | File | Use Case |
|---------|------|----------|
| [react-component](react/react-component.md) | Functional component | UI components |
| [react-hook](react/react-hook.md) | Custom hook | Reusable logic |
| [react-context](react/react-context.md) | Context provider | State management |
| [react-form](react/react-form.md) | Form with validation | User input |

### Database Snippets
Models, migrations, and queries.

| Snippet | File | ORM/DB |
|---------|------|--------|
| [prisma-model](database/prisma-model.md) | Prisma schema | Prisma |
| [sql-migration](database/sql-migration.md) | Migration file | Raw SQL |
| [typeorm-entity](database/typeorm-entity.md) | TypeORM entity | TypeORM |
| [sqlalchemy-model](database/sqlalchemy-model.md) | SQLAlchemy model | SQLAlchemy |

### Testing Snippets
Test templates and utilities.

| Snippet | File | Framework |
|---------|------|-----------|
| [jest-test](testing/jest-test.md) | Jest test suite | Jest |
| [pytest-test](testing/pytest-test.md) | Pytest test | pytest |
| [go-test](testing/go-test.md) | Go test | testing |
| [vitest-test](testing/vitest-test.md) | Vitest test | Vitest |

### DevOps Snippets
CI/CD and containerization.

| Snippet | File | Platform |
|---------|------|----------|
| [dockerfile](devops/dockerfile.md) | Multi-stage build | Docker |
| [github-action](devops/github-action.md) | CI workflow | GitHub Actions |
| [docker-compose](devops/docker-compose.md) | Compose file | Docker Compose |

### Utility Snippets
Common utilities and helpers.

| Snippet | File | Purpose |
|---------|------|---------|
| [error-class](utility/error-class.md) | Custom errors | Error handling |
| [logger](utility/logger.md) | Structured logger | Logging |
| [env-config](utility/env-config.md) | Env configuration | Config |
| [retry-helper](utility/retry-helper.md) | Retry with backoff | Resilience |

### Validation Snippets
Schema and input validation.

| Snippet | File | Library |
|---------|------|---------|
| [zod-schema](validation/zod-schema.md) | Zod schema | Zod |
| [pydantic-model](validation/pydantic-model.md) | Pydantic model | Pydantic |
| [joi-schema](validation/joi-schema.md) | Joi schema | Joi |

---

## Snippet Structure

Each snippet file contains:

1. **Description** — What it does
2. **When to Use** — Appropriate scenarios
3. **Code** — The actual snippet
4. **Customization Points** — What to modify
5. **Related Snippets** — Cross-references

---

## Adding New Snippets

1. Create file in appropriate category folder
2. Follow the standard structure
3. Add to this index
4. Test the snippet works

### Template

```markdown
# Snippet: [name]

## Description
[What this snippet does]

## When to Use
- [Scenario 1]
- [Scenario 2]

## Code

\`\`\`[language]
[snippet code]
\`\`\`

## Customization Points
- `[placeholder]` — [what to replace]

## Related Snippets
- [related-snippet-1]
- [related-snippet-2]
```

---

## Auto-Surfacing

Snippets are automatically suggested when:

- Creating new files matching snippet types
- Implementing common patterns
- Setting up new projects
- Explicit snippet requests

The meta-cognition skill checks this registry during implementation.
