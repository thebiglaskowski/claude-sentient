# Documentation Rules

## Core Principles

1. **Documentation is code** — Versioned, reviewed, maintained
2. **Single source of truth** — One place for each piece of info
3. **Audience-first** — Write for the reader, not the writer
4. **Keep it current** — Outdated docs are worse than none
5. **Examples over explanations** — Show, don't just tell

---

## Documentation Types

### README.md (Required)
Every project root must have:
```markdown
# Project Name

One-line description.

## Quick Start
[How to get running in <5 minutes]

## Installation
[Step-by-step setup]

## Usage
[Basic examples]

## Contributing
[How to contribute]

## License
[License type]
```

### CHANGELOG.md (Required)
```markdown
# Changelog

## [Unreleased]
### Added
### Changed
### Fixed
### Removed

## [1.0.0] - 2024-01-15
### Added
- Initial release
```

### ADRs (Architecture Decision Records)
```markdown
# ADR-001: Use PostgreSQL for primary database

## Status
Accepted

## Context
[Why this decision was needed]

## Decision
[What was decided]

## Consequences
[Positive and negative outcomes]
```

---

## Code Comments

### When to Comment
- **Why** something is done (not what)
- Complex algorithms
- Workarounds with ticket references
- Public API documentation
- Performance critical sections

### When NOT to Comment
- Obvious code
- Commented-out code (delete it)
- Redundant information
- Version history (use git)

### Comment Examples
```javascript
// Good - explains WHY
// Using WeakMap to prevent memory leaks with DOM references
const cache = new WeakMap();

// Bad - explains WHAT (obvious from code)
// Increment counter by 1
counter++;

// Good - documents workaround
// HACK: Safari doesn't support ResizeObserver in iframes
// See: https://bugs.webkit.org/show_bug.cgi?id=123456
// TODO: Remove when Safari 17 is minimum supported

// Bad - commented out code
// function oldImplementation() { ... }
```

---

## API Documentation

### REST Endpoints
```markdown
## Create User

`POST /api/users`

Creates a new user account.

### Request
```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "password": "secure123"
}
```

### Response
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "John Doe",
  "createdAt": "2024-01-15T10:00:00Z"
}
```

### Errors
| Status | Code | Description |
|--------|------|-------------|
| 400 | INVALID_EMAIL | Email format invalid |
| 409 | EMAIL_EXISTS | Email already registered |
```

### Function Documentation
```typescript
/**
 * Calculates the total price including tax and discounts.
 *
 * @param items - Array of cart items with price and quantity
 * @param taxRate - Tax rate as decimal (e.g., 0.1 for 10%)
 * @param discountCode - Optional discount code to apply
 * @returns Total price in cents
 * @throws {InvalidTaxRateError} If tax rate is negative
 *
 * @example
 * const total = calculateTotal(
 *   [{ price: 1000, quantity: 2 }],
 *   0.1,
 *   'SAVE10'
 * );
 * // Returns 1980 (2000 + 200 tax - 10% discount)
 */
function calculateTotal(
  items: CartItem[],
  taxRate: number,
  discountCode?: string
): number
```

---

## Changelog Standards

### Keep a Changelog Format
```markdown
## [1.2.0] - 2024-01-15

### Added
- New OAuth login with Google (#123)
- Export to CSV functionality

### Changed
- Improved error messages for validation
- Updated dependencies to latest versions

### Fixed
- Header alignment on mobile (#456)
- Memory leak in WebSocket handler

### Deprecated
- Legacy authentication endpoint (use OAuth)

### Removed
- Support for IE11

### Security
- Fixed XSS vulnerability in user bio (#789)
```

### Versioning (SemVer)
```
MAJOR.MINOR.PATCH

MAJOR: Breaking changes
MINOR: New features (backward compatible)
PATCH: Bug fixes (backward compatible)
```

---

## Writing Style

### Be Direct
```markdown
# Bad
It should be noted that the system might occasionally experience issues.

# Good
The system may fail under high load.
```

### Use Active Voice
```markdown
# Bad
The configuration file should be edited by the user.

# Good
Edit the configuration file.
```

### Use Present Tense
```markdown
# Bad
The function will return an error.

# Good
The function returns an error.
```

### Be Specific
```markdown
# Bad
The timeout is configurable.

# Good
Set timeout with `--timeout=30s` (default: 10s, max: 5m).
```

---

## Formatting Standards

### Headings
```markdown
# Page Title (H1) - One per page
## Major Section (H2)
### Subsection (H3)
#### Minor Section (H4) - Avoid if possible
```

### Code Blocks
```markdown
```javascript
// Always specify language
const x = 1;
```
```

### Lists
```markdown
Use bullets for unordered:
- Item one
- Item two

Use numbers for ordered:
1. First step
2. Second step
```

### Tables
```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data     | Data     | Data     |
```

---

## Documentation Checklist

Before merging:
- [ ] README updated if user-facing changes
- [ ] CHANGELOG entry added
- [ ] API docs updated for endpoint changes
- [ ] Code comments explain complex logic
- [ ] No typos or grammar errors
- [ ] Links are valid
- [ ] Examples are tested and work
- [ ] Screenshots updated if UI changed
