# Example Workflows

Real-world examples of using this template effectively.

---

## Table of Contents

1. [Starting a New Project](#starting-a-new-project)
2. [Daily Development](#daily-development)
3. [Feature Development](#feature-development)
4. [Bug Fixing](#bug-fixing)
5. [Code Review](#code-review)
6. [Release Process](#release-process)
7. [Maintenance & Debt](#maintenance--debt)
8. [Using MCP Servers](#using-mcp-servers)

---

## Starting a New Project

### Scenario
You're starting a new React/Node.js project.

### Steps

**1. Install template (in regular terminal):**
```bash
cd ~/projects/my-new-app
C:\scripts\prompts\install.sh .
```

**2. Start Claude Code:**
```bash
claude --init
```

**3. Initialize (in Claude Code conversation):**
```
initialize this project
```

**Claude will:**
- Detect React, Node.js, TypeScript
- Create comprehensive .gitignore
- Install relevant skills from skills.sh
- Generate PROJECT_MAP.md
- Create STATUS.md

**4. Plan your first feature:**
```
/plan

I want to add user authentication with:
- Email/password login
- JWT tokens
- Password reset via email
```

**5. Review the plan:**
```
/audit-blueprint
```

**6. Start building:**
```
/daily
```

---

## Daily Development

### Scenario
Continuing work on an existing project.

### Morning Startup

**1. Open project:**
```bash
cd ~/projects/my-app
claude
```

**2. Check status:**
```
What were we working on? Check STATUS.md
```

**3. Continue work:**
```
/daily
```

### During Development

**Working on code:**
```
Implement the password reset endpoint following our auth patterns
```

**Need to research something:**
```
/spike

How should we handle email queuing for password resets?
Time-box: 30 minutes
```

**Stuck on a bug:**
```
/fix

The password reset token expires immediately instead of after 1 hour
```

### End of Day

**Commit your work:**
```
Ready to commit these changes
```

(Pre-commit skill auto-loads, runs checklist)

**Update status:**
```
Update STATUS.md with today's progress
```

---

## Feature Development

### Scenario
Building a complete user profile feature.

### Phase 1: Planning

```
/plan

Feature: User Profile Page
- Display user info (name, email, avatar)
- Allow editing profile
- Upload profile picture
- Change password
```

**Review plan:**
```
/audit-blueprint
```

**Document the decision:**
```
/adr

We chose to store avatars in S3 instead of the database because...
```

### Phase 2: Implementation

**Start the feature:**
```
/start-feature user-profile

or manually:
git checkout -b feature/user-profile
```

**Daily work:**
```
/daily

Implement the profile display component
```

**Check progress:**
```
Show me the project health dashboard
```

### Phase 3: Quality

**Review code:**
```
/review
```

**Check tests:**
```
/test
```

**Security check:**
```
/secure

Focus on the file upload functionality
```

### Phase 4: Completion

**Finish the feature:**
```
/finish-feature

or manually:
/test
/review
Update CHANGELOG
/closeout
```

**Create PR:**
```
Create a pull request for user-profile feature
```

---

## Bug Fixing

### Scenario
Users report login fails on mobile devices.

### Step 1: Investigate

```
/fix

Bug: Login fails on mobile devices
Reported by: 3 users in the last day
Error: "Invalid token" in logs
```

### Step 2: Find Root Cause

**Claude investigates:**
- Checks auth code
- Reviews token generation
- Looks at mobile-specific code paths

**Research if needed:**
```
/spike

How do JWT tokens behave differently on mobile browsers?
use context7
```

### Step 3: Fix

```
Apply the fix we discussed for the mobile token issue
```

### Step 4: Verify

```
/test

Focus on authentication tests
```

### Step 5: Deploy

```
/quick-fix

Commit and push this bug fix
```

---

## Code Review

### Scenario
Reviewing a teammate's PR.

### Quick Review

```
/review

PR #123: Add payment processing
Focus on security and error handling
```

### Thorough Review

```
/full-review

PR #123: Add payment processing

This is a critical feature, do a comprehensive review including:
- Security audit
- Test coverage
- Performance implications
```

### Using Context7

```
/review

use context7 to verify Stripe API usage is current

PR #123: Add Stripe payment integration
```

---

## Release Process

### Scenario
Preparing version 2.0.0 release.

### Step 1: Preparation

```
/release-prep 2.0.0

or manually:
```

**Run full test suite:**
```
/test
```

**Security audit:**
```
/secure
```

**Check dependencies:**
```
Check for outdated or vulnerable dependencies
```

### Step 2: Documentation

**Update changelog:**
```
Generate changelog for version 2.0.0
```

**Review:**
```
Review the generated CHANGELOG entries
```

### Step 3: Release Checklist

```
/release

Version: 2.0.0
Environment: Production
```

**Checklist covers:**
- All tests passing
- Security audit clean
- Documentation updated
- CHANGELOG complete
- Version numbers updated
- Rollback plan ready

### Step 4: Deploy

```
All checks passed, create the release tag
```

---

## Maintenance & Debt

### Scenario
Monthly maintenance window.

### Full Assessment

```
/maintenance

or manually:
```

**Codebase audit:**
```
/assess
```

**Tech debt inventory:**
```
/debt
```

**Security scan:**
```
/secure
```

**Dependency check:**
```
Check all dependencies for updates and vulnerabilities
```

### Review Results

```
Show me the project health dashboard
```

### Plan Improvements

```
/plan

Address the top 3 tech debt items:
1. Refactor auth middleware
2. Add missing tests for utils
3. Update deprecated API calls
```

### Execute

```
/daily

Start with the auth middleware refactor
```

---

## Using MCP Servers

### Context7 for Documentation

**Research current best practices:**
```
use context7 to look up React Query v5 patterns

I want to implement data fetching with caching
```

**Verify API isn't deprecated:**
```
/review

use context7 to check if any APIs we're using are deprecated
```

### GitHub for Issues

**Create issue from code:**
```
Create a GitHub issue for this TODO:
// TODO: Implement rate limiting for API

In repository my-org/my-app
```

**Check PR status:**
```
What's the status of PR #45?
```

### Memory for Persistence

**Save decision:**
```
Remember that we decided to use PostgreSQL for this project
with connection pooling via PgBouncer
```

**Recall later:**
```
What database setup did we decide on?
```

---

## Complete Day Example

### 9:00 AM - Start

```
Good morning! Let's continue on the payment feature.
What's our current status?
```

### 9:30 AM - Development

```
/daily

Implement the checkout flow we planned yesterday
```

### 11:00 AM - Research

```
/spike

use context7

Best practices for handling Stripe webhooks with retries
Time-box: 45 minutes
```

### 12:00 PM - Lunch Break

```
Update STATUS.md with morning progress
```

### 1:00 PM - Continue

```
/daily

Implement the webhook handler based on our research
```

### 3:00 PM - Testing

```
/test

Focus on the new payment code
```

### 4:00 PM - Review

```
/review

Self-review before creating PR
```

### 4:30 PM - Commit

```
Ready to commit the payment feature
```

### 5:00 PM - Wrap Up

```
/closeout

Update STATUS.md and prepare for tomorrow
```

---

## v2.0 Features

### Using Command Arguments

**Review with options:**
```
/review src/api --deep --security

Reviews src/api with deep analysis and security focus
```

**Test with coverage threshold:**
```
/test src/utils --coverage=90

Runs tests for src/utils requiring 90% coverage
```

**Refactor with dry-run:**
```
/refactor src/legacy/oldCode.ts --type=extract --dry-run

Shows what would change without applying
```

**Security with severity filter:**
```
/secure src/auth --severity=S0 --ultrathink

Deep security audit looking only for critical issues
```

---

### Using Modular Rules

**Load security rules for review:**
```
Review this authentication code with @rules/security

I want to make sure we follow OWASP guidelines
```

**Apply testing standards:**
```
Help me write tests for userService.ts following @rules/testing
```

**Check API design:**
```
Review our REST API endpoints with @rules/api-design
```

---

### Using Specialized Agents

**Spawn code reviewer:**
```
Spawn code-reviewer agent to review the entire auth module

Look for patterns, test coverage, and code quality issues
```

**Security analysis:**
```
Use security-analyst to audit src/api for vulnerabilities

Focus on injection risks and authentication
```

**Research with isolated context:**
```
Spawn researcher agent to evaluate these caching options:
1. Redis
2. Memcached
3. Node-cache

Compare performance, setup complexity, and cost
```

---

### Extended Thinking (Ultrathink)

**Deep security audit:**
```
/secure --ultrathink

Perform a thorough security analysis of the entire application
```

**Complex architecture decision:**
```
Ultrathink this: Should we migrate from REST to GraphQL?

Consider:
- Team experience
- Client needs
- Migration effort
- Performance implications
```

**Incident analysis:**
```
/postmortem --ultrathink

Analyze the payment processing outage from last week
```

---

### Context Fork (Background Research)

**Research without context pollution:**
```
Research in background: How does the authentication system work in this codebase?

I need a summary, not all the details in my main context
```

**Parallel investigations:**
```
In parallel, research:
1. How pagination is implemented
2. How caching works
3. How errors are handled

Compare approaches and give me a summary
```

**Spike with isolation:**
```
Fork investigation: What would it take to add WebSocket support?

Explore the codebase and give me an estimate
```

---

### CI/CD Integration

**Run PR review in CI:**
```bash
./scripts/ci/pr-review.sh --deep
```

**Security scan in pipeline:**
```bash
./scripts/ci/security-scan.sh src/api --severity=S0
```

**Coverage gate:**
```bash
./scripts/ci/test-gate.sh --threshold=80 --strict
```

---

---

## Autonomous Development Loop

### Basic Usage

**Start exhaustive loop:**
```
/loop

Work until every quality gate passes
```

**Focus on specific area:**
```
/loop security          # Fix all security issues first
/loop testing           # Push for test coverage
/loop features          # Implement pending features
```

**With limits:**
```
/loop --max-iterations=20
/loop --pause-on=S1     # Pause for S1+ issues
```

### Full Session Example

```
User: /loop

Claude: Starting autonomous development loop...

## Iteration 1 - Assessment
Running /assess...
- Codebase health: 65/100
- Test coverage: 58%
- Security issues: 2 S1, 3 S2
- Tech debt items: 12
- Outdated deps: 5

Creating work queue...

## Iteration 2 - S1 Security Fixes
- Fixed: SQL injection in user search
- Fixed: Missing CSRF protection on forms
- Tests added: 4

## Iteration 3 - Coverage Push
- Added unit tests for AuthService
- Added integration tests for API
- Coverage: 58% → 72%

## Iteration 4 - Modernization
- Replaced moment.js with date-fns
- Updated deprecated APIs
- Bundle size: -45KB

[Checkpoint] Need direction:
Found multiple approaches for caching:
1. Redis (scalable, separate service)
2. In-memory (simple, single instance)
3. Hybrid (memory + Redis fallback)

Which approach should I use?

User: Use Redis for production scalability

Claude: Continuing with Redis caching...

## Iteration 5 - Redis Caching
- Implemented Redis cache layer
- Added cache invalidation
- Tests added: 6

## Iteration 6 - S2 Issues
- Fixed: Input validation gaps
- Fixed: Error message leakage
- Fixed: Rate limiting edge case

## Iteration 7 - Final Quality Gates
All checks passing:
✅ Tests: 127 passing
✅ Coverage: 89%
✅ Security: 0 issues
✅ Code Quality: A
✅ Documentation: Complete

## Loop Complete! 🎉
- Total iterations: 7
- Issues resolved: 18
- Tests added: 31
- Time elapsed: 35 minutes
```

### When It Pauses

The loop pauses for user input when:

```
[Checkpoint] Direction needed:

The auth module could be refactored two ways:
1. Keep current pattern, add middleware
2. Full rewrite with new auth library

Option 1 is faster, Option 2 is cleaner.
Which do you prefer?
```

### Conda Environment Awareness

The loop respects environment safety:

```
## Environment Check
⚠️ Base conda environment detected!

Before installing packages, I need you to:
1. Create project environment: conda create -n myproject python=3.11
2. Activate it: conda activate myproject

Or if environment.yml exists:
   conda env create -f environment.yml

Waiting for environment confirmation...
```

---

## Tips for Success

1. **Start with `/daily`** - Establishes context quickly
2. **Use compound commands** - `/ship`, `/quick-fix` save time
3. **Check health regularly** - Catch issues early
4. **Leverage Context7** - Get current documentation
5. **Update STATUS.md** - Future you will thank you
6. **Use appropriate models** - Haiku for simple, Opus for complex
7. **Use command arguments** - `/review src/api --deep` is more focused
8. **Spawn agents for deep work** - Keep main context clean
9. **Use ultrathink for complex decisions** - Worth the extra time
10. **Load rules when needed** - `@rules/security` for security reviews
