---
name: docs-generator
description: Auto-generate documentation from code analysis
model: sonnet
---

# Documentation Generator

Auto-generate documentation from code.

## Description

Analyzes code and generates documentation including API docs, component docs, and README sections.
Triggers on: "generate docs", "document this", "create documentation", "API docs", "update docs".

## Documentation Types

### 1. API Documentation
For REST APIs, generate endpoint documentation:

```markdown
## API Reference

### Authentication

#### POST /auth/login
Authenticate a user and receive access token.

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string | Yes | User's email address |
| password | string | Yes | User's password |

**Response:** `200 OK`
```json
{
  "token": "eyJhbG...",
  "expiresIn": 3600,
  "user": { "id": "123", "email": "user@example.com" }
}
```

**Errors:**
| Code | Description |
|------|-------------|
| 401 | Invalid credentials |
| 429 | Too many attempts |
```

### 2. Component Documentation
For React/Vue components:

```markdown
## Button Component

A reusable button component with multiple variants.

### Props
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| variant | 'primary' \| 'secondary' | 'primary' | Button style variant |
| size | 'sm' \| 'md' \| 'lg' | 'md' | Button size |
| disabled | boolean | false | Disable the button |
| onClick | () => void | - | Click handler |

### Usage
```tsx
<Button variant="primary" size="lg" onClick={handleClick}>
  Submit
</Button>
```

### Examples
[Visual examples or Storybook link]
```

### 3. Function/Module Documentation
```markdown
## Utils Module

### `formatDate(date, format)`
Formats a date according to the specified format string.

**Parameters:**
- `date` (Date | string | number) - The date to format
- `format` (string) - Format string (e.g., 'YYYY-MM-DD')

**Returns:** `string` - Formatted date string

**Example:**
```typescript
formatDate(new Date(), 'YYYY-MM-DD') // '2024-01-15'
formatDate('2024-01-15', 'MMM D, YYYY') // 'Jan 15, 2024'
```

**Throws:** `InvalidDateError` if date is invalid
```

### 4. Database Schema Documentation
```markdown
## Database Schema

### Users Table
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User's email |
| password_hash | VARCHAR(255) | NOT NULL | Bcrypt hash |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |

### Relationships
- Users → Posts (1:N)
- Users → Comments (1:N)
- Users ↔ Roles (N:M via user_roles)
```

## Generation Process

### Step 1: Analyze Code Structure

```bash
# Find documentable files
find src -name "*.ts" -o -name "*.tsx" | head -50

# Identify patterns
grep -r "export function\|export const\|export class" src/
grep -r "@route\|@api\|router\." src/
```

### Step 2: Extract Information

For each file/module:
1. Parse exports (functions, classes, components)
2. Extract JSDoc/TSDoc comments
3. Infer types from TypeScript
4. Identify patterns (API routes, React components, etc.)

### Step 3: Generate Documentation

Based on file type:
- `routes/*.ts` → API documentation
- `components/*.tsx` → Component documentation
- `utils/*.ts` → Function documentation
- `models/*.ts` → Schema documentation

### Step 4: Output

Create or update:
- `docs/api/` - API reference
- `docs/components/` - Component library
- `README.md` - Overview sections

## Smart Features

### Type Inference
Extract types from TypeScript:
```typescript
// From this:
function getUser(id: string): Promise<User | null>

// Generate:
// **Parameters:** id (string) - ...
// **Returns:** Promise<User | null>
```

### Example Extraction
Pull examples from tests:
```typescript
// From test file:
it('should format date correctly', () => {
  expect(formatDate(new Date('2024-01-15'), 'YYYY-MM-DD')).toBe('2024-01-15')
})

// Generate example in docs
```

### Change Detection
Only regenerate docs for changed files:
```bash
git diff --name-only HEAD~1 | grep -E "\.(ts|tsx)$"
```

## Output Formats

### Markdown (Default)
Standard markdown files for GitHub/GitLab.

### OpenAPI/Swagger
For API documentation:
```yaml
openapi: 3.0.0
paths:
  /auth/login:
    post:
      summary: Authenticate user
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/LoginRequest'
```

### TypeDoc/JSDoc
Generate from existing doc comments.

## Integration

### Pre-Commit
Verify docs are updated with code:
```markdown
- [ ] New exports have documentation
- [ ] Changed APIs have updated docs
- [ ] README reflects current state
```

### CI/CD
Auto-generate and publish docs on release:
```yaml
- name: Generate Docs
  run: claude-docs generate

- name: Publish to GitHub Pages
  run: gh-pages -d docs
```

## Commands

### Generate All Docs
```
"Generate documentation for the entire project"
```

### Document Specific File
```
"Document src/utils/date.ts"
```

### Update README
```
"Update README with current API endpoints"
```

### Generate API Spec
```
"Generate OpenAPI spec from routes"
```

## Configuration

```json
{
  "docs": {
    "output": "docs/",
    "format": "markdown",
    "includePrivate": false,
    "includeExamples": true,
    "apiStyle": "openapi"
  }
}
```
