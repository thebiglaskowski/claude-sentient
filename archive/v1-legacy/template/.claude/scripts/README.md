# Claude Code CI/CD Scripts

Scripts for running Claude Code in headless mode for CI/CD pipelines.

## Overview

These scripts enable automated code review, security scanning, and quality gates using Claude Code in CI/CD environments.

---

## Scripts

### CI Scripts (`ci/`)

| Script | Purpose |
|--------|---------|
| `pr-review.sh` | Automated PR code review |
| `security-scan.sh` | Security vulnerability scanning |
| `test-gate.sh` | Test coverage gate checking |

### Validation Scripts (`validate/`)

| Script | Purpose |
|--------|---------|
| `prompt-check.sh` | Validate prompt structure |
| `skill-lint.sh` | Lint YAML frontmatter in skills |

---

## Requirements

- Claude Code CLI installed (`npm install -g @anthropic/claude-code`)
- `ANTHROPIC_API_KEY` environment variable set
- Git repository with proper access

---

## Usage

### PR Review

```bash
# In CI pipeline
./scripts/ci/pr-review.sh

# With options
./scripts/ci/pr-review.sh --deep --security
```

### Security Scan

```bash
# Full security scan
./scripts/ci/security-scan.sh

# Scope to specific path
./scripts/ci/security-scan.sh src/auth
```

### Test Gate

```bash
# Check coverage meets threshold
./scripts/ci/test-gate.sh

# Custom threshold
./scripts/ci/test-gate.sh --threshold=90
```

---

## GitHub Actions Integration

### Quick Setup

1. Copy workflows to your repository:
   ```bash
   mkdir -p .github/workflows
   cp /path/to/prompts/template/.github/workflows/*.yml .github/workflows/
   ```

2. Add `ANTHROPIC_API_KEY` secret to your repository:
   - Go to repository → Settings → Secrets → Actions
   - Click "New repository secret"
   - Name: `ANTHROPIC_API_KEY`
   - Value: Your Anthropic API key

> **Detailed instructions:** See `.claude/SETUP.md` for complete setup guide.

### Available Workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `claude-review.yml` | PR open/sync | Automated code review |
| `security-scan.yml` | Push to main, PRs, manual | Security vulnerability scanning |

---

## Configuration

### Environment Variables

```bash
ANTHROPIC_API_KEY=sk-ant-...      # Required: API key
CLAUDE_MODEL=sonnet               # Optional: Model (default: sonnet)
CLAUDE_MAX_TOKENS=4000            # Optional: Max tokens
REVIEW_LEVEL=standard             # Optional: quick|standard|deep
```

### CI-specific Settings

Create `.claude/ci-config.json`:

```json
{
  "review": {
    "level": "standard",
    "blockOnS0": true,
    "blockOnS1": true
  },
  "security": {
    "scanPaths": ["src/auth", "src/api"],
    "ignorePaths": ["tests/"]
  },
  "coverage": {
    "threshold": 80,
    "failOnDecrease": true
  }
}
```

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success, no blocking issues |
| 1 | Blocking issues found (S0/S1) |
| 2 | Configuration error |
| 3 | API error |

---

## Cost Management

### Token Limits

Set `CLAUDE_MAX_TOKENS` to limit per-run costs:
- Quick review: 2000 tokens
- Standard review: 4000 tokens
- Deep review: 8000 tokens

### Selective Triggers

Only run expensive scans when needed:
```yaml
# Only security scan on auth changes
paths:
  - 'src/auth/**'
  - 'src/api/**'
```

---

## Troubleshooting

### API Key Issues
```
Error: ANTHROPIC_API_KEY not set
```
Set the environment variable or add to CI secrets.

### Rate Limiting
```
Error: Rate limit exceeded
```
Add delay between runs or reduce token usage.

### Timeout
```
Error: Request timed out
```
Increase timeout or scope the review to smaller areas.
