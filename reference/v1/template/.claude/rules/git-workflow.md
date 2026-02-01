# Git Workflow Rules

## Core Principles

1. **Atomic commits** — One logical change per commit
2. **Clean history** — Squash WIP, keep meaningful commits
3. **Protected main** — Never commit directly to main
4. **Review required** — All changes through PRs
5. **Fast-forward merges** — Keep linear history when possible

---

## Branch Naming

### Conventions
```
feature/[ticket]-[short-description]
bugfix/[ticket]-[short-description]
hotfix/[ticket]-[short-description]
release/v[major].[minor].[patch]
chore/[description]
docs/[description]
refactor/[description]
```

### Examples
```
feature/AUTH-123-add-oauth-login
bugfix/UI-456-fix-header-alignment
hotfix/SEC-789-patch-xss-vulnerability
release/v2.1.0
chore/update-dependencies
docs/add-api-documentation
refactor/extract-user-service
```

---

## Commit Messages

### Format
```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Types
| Type | When to Use |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code change that neither fixes bug nor adds feature |
| `perf` | Performance improvement |
| `test` | Adding or updating tests |
| `chore` | Build process, dependencies, tooling |
| `revert` | Reverting previous commit |

### Rules
- Subject line: 50 chars max, imperative mood
- Body: 72 chars per line, explain what and why
- Reference issues in footer

### Examples
```
feat(auth): add OAuth 2.0 login with Google

Implements Google OAuth flow with PKCE for security.
Includes refresh token handling and session management.

Closes #123

---

fix(api): handle null response from user service

The user service returns null when user is not found.
Previously this caused a TypeError in the caller.

Fixes #456
```

---

## Pull Request Standards

### PR Title
```
[TICKET-123] Short description of change
```

### PR Description Template
```markdown
## Summary
Brief description of what this PR does.

## Changes
- Change 1
- Change 2

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Screenshots (if UI change)
[Before/After images]

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings
```

### PR Size Guidelines
| Size | Lines Changed | Review Time |
|------|---------------|-------------|
| XS | < 50 | Minutes |
| S | 50-200 | 30 minutes |
| M | 200-500 | 1-2 hours |
| L | 500-1000 | Half day |
| XL | > 1000 | Split it |

---

## Branch Protection Rules

### Main Branch
```
- Require pull request reviews (min 1)
- Require status checks to pass
- Require branches to be up to date
- Require signed commits (recommended)
- Include administrators
- Allow force pushes: NEVER
- Allow deletions: NEVER
```

### Release Branches
```
- Require pull request reviews (min 2)
- Require status checks to pass
- Restrict who can push
```

---

## Merge Strategies

### When to Use Each
| Strategy | Use Case |
|----------|----------|
| Squash merge | Feature branches, clean history |
| Merge commit | Release branches, preserve context |
| Rebase | Personal branches, linear history |

### Squash Merge (Default)
```bash
# Creates single commit from PR
git checkout main
git merge --squash feature/xyz
git commit -m "feat: implement xyz"
```

### Rebase Before Merge
```bash
# Keep up with main
git fetch origin
git rebase origin/main
git push --force-with-lease
```

---

## Common Workflows

### Feature Development
```bash
# 1. Create branch
git checkout main
git pull
git checkout -b feature/AUTH-123-add-login

# 2. Make changes with commits
git add .
git commit -m "feat(auth): add login form"

# 3. Keep updated with main
git fetch origin
git rebase origin/main

# 4. Push and create PR
git push -u origin feature/AUTH-123-add-login
gh pr create --fill
```

### Hotfix
```bash
# 1. Branch from main
git checkout main
git pull
git checkout -b hotfix/SEC-789-fix-xss

# 2. Fix and test
git add .
git commit -m "fix(security): sanitize user input"

# 3. PR with expedited review
git push -u origin hotfix/SEC-789-fix-xss
gh pr create --label "hotfix" --label "priority:critical"
```

### Release
```bash
# 1. Create release branch
git checkout main
git pull
git checkout -b release/v2.1.0

# 2. Version bump and changelog
npm version minor
git add .
git commit -m "chore: bump version to 2.1.0"

# 3. Create PR and tag after merge
gh pr create --fill
# After merge:
git tag -a v2.1.0 -m "Release v2.1.0"
git push origin v2.1.0
```

---

## Git Hygiene

### Do Regularly
- Pull and rebase frequently
- Delete merged branches
- Review stale branches monthly
- Sign commits (GPG)

### Never Do
- Force push to shared branches
- Commit directly to main
- Commit secrets or credentials
- Create commits > 1000 lines
- Leave WIP commits in PRs

---

## Checklist

Before pushing:
- [ ] Branch follows naming convention
- [ ] Commits are atomic and well-messaged
- [ ] Rebased on latest main
- [ ] No merge conflicts
- [ ] Tests pass locally
- [ ] No debug code or console.logs
- [ ] No secrets in commits
