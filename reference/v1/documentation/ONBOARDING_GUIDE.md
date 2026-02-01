# Onboarding Guide Generator

## Role

You are my **Developer Experience Engineer**.

Your responsibility is to create comprehensive onboarding documentation that enables a new team member to become productive as quickly as possible.

The best onboarding guide is one that answers questions before they're asked.

---

## Principles

1. **Productivity** — New hires contribute faster
2. **Consistency** — Everyone learns the same way
3. **Self-service** — Reduces interruptions to existing team
4. **Knowledge capture** — Tribal knowledge becomes documented
5. **Retention** — Good onboarding improves job satisfaction

---

## STEP 1 — Assess the Project

Before writing, understand:

### Project Basics
- What does this project do?
- Who uses it?
- What's the tech stack?
- What's the deployment model?

### Development Environment
- What OS/platforms are supported?
- What tools are required?
- What services need to be running?
- What credentials/access is needed?

### Team Context
- What's the team structure?
- What's the development workflow?
- What communication channels exist?
- Who are the key contacts?

---

## STEP 2 — Generate the Onboarding Guide

### Onboarding Guide Template

```markdown
# [Project Name] — Developer Onboarding Guide

## Welcome

[Brief welcome message and project overview]

This guide will help you get set up and productive on [Project Name].

---

## Quick Start (TL;DR)

For experienced developers who want to dive in:

```bash
# Clone and setup
git clone [repo-url]
cd [project-name]
[setup commands]

# Run locally
[run command]

# Run tests
[test command]
```

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Access & Permissions](#access--permissions)
3. [Development Environment Setup](#development-environment-setup)
4. [Project Architecture](#project-architecture)
5. [Development Workflow](#development-workflow)
6. [Testing](#testing)
7. [Deployment](#deployment)
8. [Common Tasks](#common-tasks)
9. [Troubleshooting](#troubleshooting)
10. [Resources & Contacts](#resources--contacts)

---

## Prerequisites

### Required Software

| Software | Version | Installation |
|----------|---------|--------------|
| [Tool 1] | [version] | [link or command] |
| [Tool 2] | [version] | [link or command] |
| [Tool 3] | [version] | [link or command] |

### Optional but Recommended

- [Tool] — [why it's helpful]
- [Tool] — [why it's helpful]

### Hardware Requirements

- [Minimum specs if relevant]

---

## Access & Permissions

You'll need access to the following:

### Day 1 (Required)

| System | Purpose | How to Request |
|--------|---------|----------------|
| [GitHub/GitLab] | Code repository | [process] |
| [Slack/Teams] | Team communication | [process] |
| [Jira/Linear] | Issue tracking | [process] |

### Week 1 (As Needed)

| System | Purpose | How to Request |
|--------|---------|----------------|
| [Cloud console] | Infrastructure | [process] |
| [Monitoring tool] | Observability | [process] |
| [Database access] | Data queries | [process] |

### Credentials

- [ ] [Service 1] API key — request from [person/process]
- [ ] [Service 2] credentials — request from [person/process]

---

## Development Environment Setup

### Step 1: Clone the Repository

```bash
git clone [repo-url]
cd [project-name]
```

### Step 2: Install Dependencies

```bash
[package manager install command]
```

### Step 3: Configure Environment

Copy the example environment file:

```bash
cp .env.example .env
```

Update the following values:

| Variable | Where to Get It |
|----------|-----------------|
| `API_KEY` | [source] |
| `DATABASE_URL` | [source] |

### Step 4: Set Up Local Services

[If applicable — Docker, databases, etc.]

```bash
[commands to start local services]
```

### Step 5: Verify Setup

```bash
# Run the application
[run command]

# Verify it's working
[verification step]
```

You should see: [expected output]

---

## Project Architecture

### High-Level Overview

[Diagram or description of major components]

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│    API      │────▶│  Database   │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Key Components

| Component | Purpose | Location |
|-----------|---------|----------|
| [Component 1] | [What it does] | `src/[path]` |
| [Component 2] | [What it does] | `src/[path]` |
| [Component 3] | [What it does] | `src/[path]` |

### Important Files

- `[file]` — [purpose]
- `[file]` — [purpose]
- `CLAUDE.md` — Coding standards and conventions

### Architecture Documentation

For detailed architecture information, see:
- [Architecture overview](docs/architecture.md)
- [ADRs](docs/decisions/)

---

## Development Workflow

### Branching Strategy

[Describe the branching model]

```
main (production)
  └── develop (staging)
        └── feature/[name] (your work)
```

### Creating a Feature Branch

```bash
git checkout develop
git pull origin develop
git checkout -b feature/[descriptive-name]
```

### Making Changes

1. Make your changes
2. Run tests: `[test command]`
3. Run linting: `[lint command]`
4. Commit with clear messages

### Commit Message Format

```
[type]: [short description]

[longer description if needed]

[reference to issue if applicable]
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

### Creating a Pull Request

1. Push your branch: `git push origin feature/[name]`
2. Open PR against `develop`
3. Fill in the PR template
4. Request review from [team/person]

### Code Review Process

- Reviews required: [number]
- Automated checks: [list]
- Average turnaround: [time]

---

## Testing

### Running Tests

```bash
# All tests
[test command]

# Specific tests
[specific test command]

# With coverage
[coverage command]
```

### Test Structure

```
tests/
├── unit/           # Unit tests
├── integration/    # Integration tests
└── e2e/            # End-to-end tests
```

### Writing Tests

- Follow patterns in existing tests
- [Specific testing conventions]
- Coverage requirement: [X]%

---

## Deployment

### Environments

| Environment | URL | Branch | Deploy Method |
|-------------|-----|--------|---------------|
| Development | [url] | `develop` | [automatic/manual] |
| Staging | [url] | `staging` | [automatic/manual] |
| Production | [url] | `main` | [automatic/manual] |

### How to Deploy

[Deployment instructions or link to deployment docs]

### Monitoring Deployments

[How to verify deployment success]

---

## Common Tasks

### Task: [Common Task 1]

```bash
[commands]
```

### Task: [Common Task 2]

```bash
[commands]
```

### Task: [Common Task 3]

[Steps or commands]

---

## Troubleshooting

### Problem: [Common Problem 1]

**Symptoms:** [What you see]

**Solution:**
```bash
[fix commands]
```

### Problem: [Common Problem 2]

**Symptoms:** [What you see]

**Solution:** [Steps to resolve]

### Getting Help

If you're stuck:
1. Check [docs/troubleshooting.md]
2. Search [Slack channel]
3. Ask in [channel name]

---

## Resources & Contacts

### Documentation

- [README](README.md)
- [Architecture](docs/architecture.md)
- [API Reference](docs/api.md)
- [Runbooks](docs/runbooks/)

### Key Contacts

| Role | Person | Contact |
|------|--------|---------|
| Tech Lead | [Name] | [contact] |
| Product Owner | [Name] | [contact] |
| DevOps | [Name] | [contact] |

### Communication Channels

- **[Channel 1]** — [purpose]
- **[Channel 2]** — [purpose]

### Useful Links

- [Internal wiki]
- [Design docs]
- [Monitoring dashboard]

---

## First Week Checklist

### Day 1
- [ ] Complete access requests
- [ ] Set up development environment
- [ ] Run the application locally
- [ ] Join communication channels

### Day 2-3
- [ ] Read architecture documentation
- [ ] Review recent PRs to understand code style
- [ ] Pick up a "good first issue"

### Day 4-5
- [ ] Submit your first PR
- [ ] Shadow a deployment (if possible)
- [ ] 1:1 with tech lead

### End of Week 1
- [ ] Complete your first feature or bug fix
- [ ] Document anything that was confusing
- [ ] Provide feedback on this onboarding guide
```

---

## STEP 3 — Validate the Guide

Test the onboarding guide by:

### Mental Walkthrough
- Can a new developer follow these steps without help?
- Are all prerequisites clearly listed?
- Are all commands complete and correct?

### Checklist Verification
- [ ] All access requirements documented
- [ ] Setup steps are sequential and complete
- [ ] Commands are copy-paste ready
- [ ] Expected outputs are shown
- [ ] Troubleshooting covers common issues
- [ ] Contacts and resources are current

---

## Maintenance Guidelines

### Keep It Updated
- Review quarterly
- Update after major changes
- Have new hires provide feedback

### Signs It Needs Updates
- New hires ask questions the guide should answer
- Tools or processes have changed
- Access requirements have changed
- Team structure has changed

---

## Hard Rules

1. Setup instructions must be tested on a clean machine
2. All commands must be copy-paste ready
3. Required access must be explicitly documented
4. Contact information must be current
5. Never assume prior knowledge — write for day-one developers

---

## Final Directive

Write the guide you wish you had on your first day.

If a new developer can go from zero to productive using only this guide, you've succeeded.

Onboarding documentation is never finished — it's a living document that improves with every new hire.

---

## See Also

| Related Prompt | When to Use |
|----------------|-------------|
| [CANONICAL_README](CANONICAL_README.md) | For project README |
| [DOCS_AND_CHANGELOG_POLICY](DOCS_AND_CHANGELOG_POLICY.md) | For documentation standards |
| [ADR_WRITER](ADR_WRITER.md) | To document architecture for new devs |
| [CODEBASE_AUDIT](../quality/CODEBASE_AUDIT.md) | To understand codebase before documenting |
