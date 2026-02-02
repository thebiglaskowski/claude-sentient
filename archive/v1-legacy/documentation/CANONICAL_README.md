# Canonical README Template

## Role

You are creating or updating a **project README file**.

This template defines the standard structure for README files. Replace bracketed content with actual values.

---

## Principles

1. **Accuracy over aspiration** — Document what exists, not what's planned
2. **User-first** — Write for someone seeing this project for the first time
3. **Executable examples** — Commands must be copy-paste ready
4. **Current state** — Remove references to features that don't exist

---

## Template

> Replace all bracketed `[content]` with actual values.

---

# [Project Name]

[Short, accurate, one-paragraph description of what the project does.]
[No marketing language. No future promises.]
[Describe the system as it exists today.]

---

## Status

Current project state:
- [ ] In development
- [ ] Production-ready
- [ ] Experimental
- [ ] Deprecated

[Brief note on maturity and intended usage.]

---

## Overview

[Explain:]
- [what problem this solves]
- [who it is for]
- [what it is not]
- [high-level behavior]

[This section should align exactly with the blueprint and implementation.]

---

## Architecture (High-Level)

[Brief explanation of:]
- [major components]
- [how they interact]
- [external dependencies]

[Link to detailed docs:]
- `docs/architecture.md`
- ADRs (if applicable)

[Avoid low-level implementation detail here.]

---

## Features

[List implemented features only.]

- Feature 1 — [brief description]
- Feature 2 — [brief description]
- Feature 3 — [brief description]

[No roadmap here. Do not list future work.]

---

## Getting Started

### Prerequisites

- [Runtime requirement 1]
- [Runtime requirement 2]
- [Tool requirement]

### Installation

```bash
# Clone the repository
git clone [repo-url]
cd [project-name]

# Install dependencies
[package manager install command]
```

### Configuration

[Environment variables:]

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `VAR_NAME` | Yes/No | `value` | [What it does] |

[Config files:]
- `config/[file]` — [purpose]

---

## Usage

[Concrete examples:]

### [Use Case 1]

```bash
[command or code example]
```

Expected output:
```
[expected result]
```

### [Use Case 2]

```bash
[command or code example]
```

[This must match reality exactly.]

---

## Testing

[How to run tests:]

```bash
# Run all tests
[test command]

# Run with coverage
[coverage command]
```

[Coverage requirements:] [X]% minimum

[Expected results:] All tests should pass.

---

## Project Structure

```
[project-name]/
├── src/              # [Source code]
├── tests/            # [Test files]
├── docs/             # [Documentation]
├── config/           # [Configuration]
└── [other dirs]      # [Purpose]
```

---

## Development

### Setup

```bash
# Development setup steps
[commands]
```

### Code Standards

- [Reference to CLAUDE.md or coding standards]
- [Linting/formatting commands]

### Contributing

[How to contribute, if applicable]

---

## Deployment

[Brief deployment instructions or link to deployment docs]

```bash
# Build for production
[build command]

# Deploy
[deploy command]
```

---

## Troubleshooting

### Common Issues

**Issue:** [Problem description]
**Solution:** [How to fix]

**Issue:** [Problem description]
**Solution:** [How to fix]

[Link to KNOWN_ISSUES.md if it exists]

---

## Documentation

- [Architecture](docs/architecture.md)
- [API Reference](docs/api.md)
- [Runbooks](docs/runbooks/)
- [Decision Records](docs/decisions/)

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

---

## License

[License type and brief note]

---

## Maintainers

- [Name/Team] — [Contact/Role]

---

## Hard Rules

1. README must accurately describe the current system
2. All commands must be tested and working
3. Do not document features that don't exist
4. Remove references to deprecated functionality
5. Status section must reflect reality

---

## Final Directive

The README is often the first thing users see.

Make it accurate, make it useful, make it trustworthy.

---

## See Also

| Related Prompt | When to Use |
|----------------|-------------|
| [DOCS_AND_CHANGELOG_POLICY](DOCS_AND_CHANGELOG_POLICY.md) | For documentation standards |
| [ONBOARDING_GUIDE](ONBOARDING_GUIDE.md) | For detailed developer onboarding |
| [UNIT_CLOSEOUT_CHECKLIST](UNIT_CLOSEOUT_CHECKLIST.md) | README updates part of closeout |
| [RELEASE_CHECKLIST](../operations/RELEASE_CHECKLIST.md) | Verify README before release |
