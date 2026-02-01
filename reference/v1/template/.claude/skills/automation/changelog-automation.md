---
name: changelog-automation
description: Auto-generate CHANGELOG entries from git commits
model: sonnet
---

# Changelog Automation

Auto-generate CHANGELOG entries from git commits.

## Description

Automatically creates and updates CHANGELOG.md based on commit history.
Triggers on: "update changelog", "generate changelog", "what changed", "release notes".

## Changelog Format

Following [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- New feature X for doing Y

### Changed
- Updated Z to improve performance

### Fixed
- Bug in authentication flow (#123)

### Removed
- Deprecated API endpoint /old

## [1.2.0] - 2024-01-15

### Added
- User profile pages
- Export to CSV functionality
```

## Categories

Map commit prefixes to changelog sections:

| Commit Prefix | Changelog Section |
|---------------|-------------------|
| `feat:`, `add:` | Added |
| `change:`, `update:`, `refactor:` | Changed |
| `fix:`, `bugfix:` | Fixed |
| `remove:`, `delete:` | Removed |
| `deprecate:` | Deprecated |
| `security:` | Security |
| `perf:` | Changed (performance) |
| `docs:` | (skip or Documentation) |
| `test:`, `chore:` | (skip) |

## Generation Process

### Step 1: Get Commits Since Last Release

```bash
# Find last version tag
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")

# Get commits since last tag (or all commits)
if [ -n "$LAST_TAG" ]; then
  git log $LAST_TAG..HEAD --oneline --no-merges
else
  git log --oneline --no-merges
fi
```

### Step 2: Parse and Categorize

For each commit:
1. Extract prefix (feat:, fix:, etc.)
2. Extract description
3. Extract PR/issue numbers if present
4. Map to changelog category

### Step 3: Generate Entry

```markdown
## [Unreleased]

### Added
- User authentication system (#45)
- Password reset flow (#48)

### Fixed
- Login timeout issue (#52)
- Session handling on mobile (#53)

### Changed
- Improved error messages
```

### Step 4: Update CHANGELOG.md

Insert new entries under `[Unreleased]` section, preserving existing content.

## Commands

### Generate Unreleased Changes
```
"Generate changelog for unreleased changes"
```

Output: Updates `[Unreleased]` section with new commits.

### Create Release Entry
```
"Create changelog entry for version 1.3.0"
```

Output: Moves `[Unreleased]` to `[1.3.0] - DATE` and creates new empty `[Unreleased]`.

### Full Regeneration
```
"Regenerate full changelog from git history"
```

Output: Rebuilds entire CHANGELOG from tags and commits.

## Smart Features

### Issue/PR Links
Automatically link to issues:
```markdown
- Add user profiles ([#45](https://github.com/user/repo/issues/45))
```

### Breaking Changes
Commits with `BREAKING:` or `!` get special callout:
```markdown
### ⚠️ Breaking Changes
- API v1 endpoints removed - migrate to v2
```

### Contributors
Optionally include contributors:
```markdown
### Contributors
- @username1
- @username2
```

## Integration

### Pre-Release Hook
Before release, verify changelog is updated:
```markdown
Pre-release check:
- [ ] CHANGELOG.md has entries in [Unreleased]
- [ ] All significant changes documented
- [ ] Breaking changes called out
```

### Commit Hook (Optional)
Remind to update changelog for significant commits:
```bash
# If commit is feat: or fix:, remind about changelog
if echo "$COMMIT_MSG" | grep -qE "^(feat|fix):"; then
  echo "Remember to update CHANGELOG.md"
fi
```

## Example Workflow

```markdown
## Changelog Generation

**Last release:** v1.2.0 (2024-01-01)
**Commits since:** 15

### Categorized Changes

**Added (5 commits):**
- feat: Add user dashboard
- feat: Add export functionality
- feat: Add dark mode support
- add: New API endpoint /users/me
- feat: Add notification preferences

**Fixed (3 commits):**
- fix: Login redirect loop
- fix: Memory leak in websocket handler
- bugfix: Timezone display issue

**Changed (2 commits):**
- refactor: Simplify auth middleware
- perf: Optimize database queries

**Skipped (5 commits):**
- docs: Update README
- test: Add integration tests
- chore: Update dependencies
- style: Format code
- ci: Fix build pipeline

### Generated Entry

```markdown
## [Unreleased]

### Added
- User dashboard with activity overview
- Export functionality (CSV, JSON)
- Dark mode support
- New API endpoint `/users/me`
- Notification preferences

### Fixed
- Login redirect loop on expired sessions
- Memory leak in websocket handler
- Timezone display issue in date pickers

### Changed
- Simplified auth middleware
- Optimized database queries for better performance
```

**Apply to CHANGELOG.md?** [Yes / No / Edit]
```

## Configuration

In project settings:
```json
{
  "changelog": {
    "skipPrefixes": ["docs:", "test:", "chore:", "style:", "ci:"],
    "includeLinks": true,
    "includeContributors": false,
    "dateFormat": "YYYY-MM-DD"
  }
}
```
