---
name: ci-cd-integration
description: Use prompts in automated pipelines for consistent quality gates
disable-model-invocation: true
---

# CI/CD Integration

Use prompts in automated pipelines for consistent quality gates.

## Description

Integrate prompts into CI/CD workflows for automated code review, testing, and release validation.
Triggers on: "CI", "CD", "pipeline", "automation", "GitHub Actions", "continuous integration".

## Use Cases

### 1. Automated PR Review
Run `/review` on every pull request.

### 2. Pre-Merge Validation
Run `/test` and pre-merge checklist before allowing merge.

### 3. Release Gating
Run `/release` checklist before deployment.

### 4. Security Scanning
Run `/secure` on PRs touching sensitive areas.

### 5. Documentation Checks
Verify docs are updated with code changes.

## GitHub Actions Examples

### PR Review Workflow
```yaml
# .github/workflows/claude-review.yml
name: Claude Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Get changed files
        id: changed
        run: |
          echo "files=$(git diff --name-only origin/main...HEAD | tr '\n' ' ')" >> $GITHUB_OUTPUT

      - name: Claude Review
        uses: anthropics/claude-code-action@v1  # Hypothetical action
        with:
          prompt: |
            Review these changes following the CODE_REVIEW prompt:
            Files changed: ${{ steps.changed.outputs.files }}

            Focus on:
            - Security issues (S0, S1)
            - Logic errors
            - Test coverage
          api-key: ${{ secrets.ANTHROPIC_API_KEY }}

      - name: Post Review Comment
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: process.env.REVIEW_OUTPUT
            })
```

### Test Coverage Gate
```yaml
# .github/workflows/test-gate.yml
name: Test Coverage Gate

on:
  pull_request:
    branches: [main]

jobs:
  coverage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Tests
        run: npm test -- --coverage --json --outputFile=coverage.json

      - name: Coverage Analysis
        uses: anthropics/claude-code-action@v1
        with:
          prompt: |
            Analyze test coverage following TEST_COVERAGE_GATE prompt.
            Coverage report: coverage.json

            Requirements:
            - Overall coverage >= 80%
            - New code coverage >= 90%
            - No untested critical paths
          files: coverage.json

      - name: Fail if Below Threshold
        if: env.COVERAGE_PASS != 'true'
        run: exit 1
```

### Security Check
```yaml
# .github/workflows/security-scan.yml
name: Security Scan

on:
  pull_request:
    paths:
      - 'src/auth/**'
      - 'src/api/**'
      - '**/*secret*'
      - '**/*auth*'

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Security Analysis
        uses: anthropics/claude-code-action@v1
        with:
          prompt: |
            Security audit following SECURITY_AUDIT prompt.
            Focus on: OWASP Top 10, authentication, data handling.
            Flag any S0 or S1 issues as blocking.
```

### Release Validation
```yaml
# .github/workflows/release-gate.yml
name: Release Gate

on:
  push:
    tags:
      - 'v*'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Release Checklist
        uses: anthropics/claude-code-action@v1
        with:
          prompt: |
            Run RELEASE_CHECKLIST for version ${{ github.ref_name }}

            Verify:
            - All tests pass
            - CHANGELOG updated
            - No S0/S1 issues
            - Documentation current

      - name: Gate Release
        if: env.RELEASE_READY != 'true'
        run: |
          echo "Release blocked - checklist not satisfied"
          exit 1
```

## GitLab CI Examples

```yaml
# .gitlab-ci.yml
stages:
  - review
  - test
  - security
  - release

claude-review:
  stage: review
  script:
    - claude-code-cli review --prompt "CODE_REVIEW" --files "$CI_MERGE_REQUEST_DIFF"
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"

claude-security:
  stage: security
  script:
    - claude-code-cli audit --prompt "SECURITY_AUDIT"
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
```

## Local CI Simulation

Test CI checks locally before pushing:

```bash
#!/bin/bash
# scripts/pre-push-check.sh

echo "=== Pre-Push Validation ==="

# Run review
echo "Running code review..."
# claude --prompt "Quick review of staged changes"

# Run tests
echo "Running tests..."
npm test

# Run security check
echo "Running security scan..."
# claude --prompt "Quick security check"

# Check coverage
echo "Checking coverage..."
npm test -- --coverage

echo "=== All checks passed ==="
```

## Integration Patterns

### Pattern 1: Comment Bot
Post review findings as PR comments.

```yaml
- name: Post Findings
  uses: actions/github-script@v7
  with:
    script: |
      const findings = JSON.parse(process.env.FINDINGS);

      for (const finding of findings) {
        await github.rest.pulls.createReviewComment({
          owner: context.repo.owner,
          repo: context.repo.repo,
          pull_number: context.issue.number,
          body: finding.message,
          path: finding.file,
          line: finding.line
        });
      }
```

### Pattern 2: Status Check
Block merge based on findings.

```yaml
- name: Set Status
  uses: actions/github-script@v7
  with:
    script: |
      const state = process.env.HAS_BLOCKERS === 'true' ? 'failure' : 'success';
      await github.rest.repos.createCommitStatus({
        owner: context.repo.owner,
        repo: context.repo.repo,
        sha: context.sha,
        state: state,
        context: 'Claude Review',
        description: process.env.STATUS_MESSAGE
      });
```

### Pattern 3: Auto-Fix
Automatically fix simple issues.

```yaml
- name: Auto-Fix
  if: env.AUTO_FIXABLE == 'true'
  run: |
    # Apply suggested fixes
    npm run lint:fix
    git add .
    git commit -m "Auto-fix: linting issues"
    git push
```

## Configuration

### Required Secrets
```
ANTHROPIC_API_KEY    - API key for Claude
GITHUB_TOKEN         - Auto-provided by Actions
```

### Environment Variables
```yaml
env:
  REVIEW_LEVEL: standard     # quick | standard | thorough
  SECURITY_LEVEL: strict     # permissive | standard | strict
  COVERAGE_THRESHOLD: 80     # Minimum coverage %
  BLOCK_ON_S0: true         # Block PRs with S0 issues
  BLOCK_ON_S1: true         # Block PRs with S1 issues
```

## Cost Management

### Token Budgets
```yaml
env:
  MAX_TOKENS_REVIEW: 4000    # Limit review output
  MAX_TOKENS_SECURITY: 8000  # Security needs more
  MAX_FILES_PER_RUN: 50      # Don't review huge PRs in one go
```

### Smart Triggers
Only run expensive checks when needed:
```yaml
# Only security scan auth changes
paths:
  - 'src/auth/**'
  - '**/security/**'

# Only review code changes
paths-ignore:
  - '**.md'
  - 'docs/**'
```

## Monitoring

Track CI integration effectiveness:
- Issues caught in CI vs production
- False positive rate
- Time added to pipeline
- Developer satisfaction

## Fallback Behavior

If Claude API unavailable:
```yaml
- name: Claude Review
  id: review
  continue-on-error: true
  ...

- name: Fallback
  if: steps.review.outcome == 'failure'
  run: |
    echo "⚠️ Claude review unavailable"
    echo "Please review manually"
    # Don't block the pipeline
```
