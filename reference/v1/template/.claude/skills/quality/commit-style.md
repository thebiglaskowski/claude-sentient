---
name: commit-style
description: Consistent git commit message formatting standards
disable-model-invocation: true
---

# Commit Style

Consistent git commit message formatting.

## Description

Use when creating git commits, writing commit messages, or reviewing commit history.
Triggers on: "commit", "git commit", "commit message", "push changes", "save changes".

## Trigger

Activates when:
- Creating git commits
- User asks about commit message format
- Reviewing commits for consistency

## Format

```
<type>: <subject>

[optional body]

[optional footer]
```

## Types

| Type | When to Use |
|------|-------------|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `docs` | Documentation only changes |
| `style` | Formatting, no code change |
| `refactor` | Code change that neither fixes nor adds |
| `test` | Adding or updating tests |
| `chore` | Maintenance, dependencies, config |
| `perf` | Performance improvement |

## Rules

1. **Subject line:** Imperative mood ("add" not "added"), no period, max 50 chars
2. **Body:** Wrap at 72 chars, explain what AND why (not how)
3. **Footer:** Reference issues with `Fixes #123` or `Relates to #456`

## Examples

**Good:**
```
feat: add user authentication flow

Implements JWT-based auth with refresh tokens.
Session timeout set to 24 hours.

Fixes #42
```

```
fix: prevent crash on empty input

Added null check before processing user data.
The API can return null for optional fields.
```

**Bad:**
```
updated stuff          # Vague
Fixed the bug.        # Has period, past tense
feat: Add new feature for user authentication that allows... # Too long
```

## Co-Author

When Claude helps write code, commits should include:
```
Co-Authored-By: Claude <noreply@anthropic.com>
```
