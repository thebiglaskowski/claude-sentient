---
name: pre-commit
description: Verification checklist before every git commit
model: haiku
---

# Pre-Commit Checklist

Verification before every commit.

## Description

Use before committing code changes. Verifies code quality, tests, and commit hygiene.
Triggers on: "commit", "git commit", "ready to commit", "before commit", "pre-commit check".

## Trigger

Activates when:
- About to create a git commit
- User asks "is this ready to commit?"
- User says "commit this" or "let's commit"

## Checklist

### Code Quality
- [ ] Code compiles/runs without errors
- [ ] No debug code left (`console.log`, `print`, `debugger`, etc.)
- [ ] No commented-out code blocks
- [ ] No hardcoded secrets or credentials
- [ ] No TODO comments for this change (complete or defer)

### Tests
- [ ] All tests pass
- [ ] New code has test coverage
- [ ] No skipped or disabled tests without documented reason

### Style
- [ ] Follows project conventions (check CLAUDE.md)
- [ ] Meaningful variable/function names
- [ ] No unnecessary complexity
- [ ] Formatting is consistent (run formatter if available)

### Documentation
- [ ] Public APIs documented
- [ ] Complex logic has explanatory comments
- [ ] README updated if user-facing changes

### Gitignore Check
- [ ] .gitignore exists in repository
- [ ] No `.env` files in staged changes
- [ ] No `node_modules/` or dependency folders staged
- [ ] No build artifacts (`dist/`, `.next/`, etc.) staged
- [ ] No IDE settings (`.idea/`, `.vscode/`) staged

### Commit Hygiene
- [ ] Changes are atomic (one logical change per commit)
- [ ] No unrelated changes included
- [ ] Commit message follows convention (see commit-style skill)

## Quick Verification Commands

```bash
# Run tests
npm test  # or pytest, go test, etc.

# Check for debug statements
grep -rn "console.log\|debugger" src/

# Check for secrets
grep -rn "password\|secret\|api_key" src/ --include="*.ts" --include="*.js"

# Run linter
npm run lint  # or equivalent

# Check gitignore coverage
git status --porcelain | grep -E "node_modules|\.env|dist/|\.next/"
# (should return nothing if .gitignore is working)

# Check for sensitive files in staged changes
git diff --cached --name-only | grep -E "\.env|\.pem|\.key|secrets"
# (should return nothing)
```

## If Any Item Fails

1. **Fix the issue** before committing
2. **If deferring**, create a follow-up task/issue
3. **Never commit** known broken code to main branch

## Auto-Checks (if hooks configured)

With hooks enabled, some checks run automatically:
- Prettier formats JS/TS files
- Console.log warnings appear

## Ready to Commit?

Only when ALL items pass. If unsure about any item, ask for clarification before committing.
