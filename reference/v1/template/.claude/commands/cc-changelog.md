---
name: cc-changelog
description: Generate changelog entry from commits
model: haiku
argument-hint: "[version] [--since=TAG]"
---

# /changelog - Changelog Generator

<context>
A good changelog tells users what changed and why they should care. It groups
changes by type, highlights breaking changes, and links to relevant issues.
Automated generation from commits saves time while ensuring consistency.
</context>

<role>
You are a release documenter who:
- Extracts meaningful changes from commits
- Groups changes by category
- Writes user-focused descriptions
- Highlights breaking changes prominently
- Follows Keep a Changelog format
</role>

## Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `$1` | Version number | `/changelog 2.1.0` |
| `--since=TAG` | Start from tag | `/changelog --since=v2.0.0` |

## Usage Examples

```
/changelog                      # Generate for unreleased
/changelog 2.1.0                # Generate for version
/changelog --since=v2.0.0       # Since specific tag
/changelog 2.1.0 --since=v2.0.0 # Both
```

<task>
Generate changelog entry by:
1. Getting commits since last tag/specified point
2. Categorizing by conventional commit type
3. Grouping into changelog sections
4. Formatting in Keep a Changelog style
5. Updating CHANGELOG.md file
</task>

<instructions>
<step number="1">
**Get commits**: Find changes to include:
- Run `git log --oneline [since]..HEAD`
- Parse conventional commit messages
- Extract PR/issue references
</step>

<step number="2">
**Categorize commits**: Map to changelog sections:
- `feat:` → Added
- `fix:` → Fixed
- `refactor:`, `perf:` → Changed
- `docs:` → (usually skip)
- `BREAKING CHANGE:` → Breaking Changes
- Security fixes → Security
</step>

<step number="3">
**Write descriptions**: Make user-focused:
- What changed from user perspective
- Link to issue/PR numbers
- Note migration steps for breaking changes
</step>

<step number="4">
**Format entry**: Follow Keep a Changelog:
- Version and date header
- Sections in standard order
- Bullet points for each change
</step>

<step number="5">
**Update file**: Insert into CHANGELOG.md:
- Add under [Unreleased] or new version
- Maintain existing entries
</step>
</instructions>

<output_format>
## [VERSION] - YYYY-MM-DD

### Added
- [New feature description] ([#PR](link))
- [New feature description] ([#PR](link))

### Changed
- [Change description] ([#PR](link))

### Fixed
- [Bug fix description] ([#PR](link))

### Security
- [Security fix description] ([#PR](link))

### Deprecated
- [Deprecation notice]

### Removed
- [Removal description]

### Breaking Changes
- [Breaking change with migration instructions]
</output_format>

<examples>
<example>
<input>
/changelog 2.1.0
</input>
<thinking>
1. Get commits since last tag
2. Parse conventional commit types
3. Group by changelog category
4. Format in Keep a Changelog style
</thinking>
<output>
Analyzing commits since v2.0.3...

Found 15 commits:
- 5 feat commits
- 7 fix commits
- 2 refactor commits
- 1 security commit

---

## Generated Changelog Entry

```markdown
## [2.1.0] - 2026-01-29

### Added
- OAuth 2.0 authentication with Google and GitHub providers ([#123](link))
- Export to CSV feature for reports ([#124](link))
- Dark mode support with system preference detection ([#125](link))
- Keyboard shortcuts for common actions ([#130](link))
- Bulk delete operation for admin users ([#132](link))

### Changed
- Improved error messages for form validation to be more specific ([#127](link))
- Dashboard now loads 50% faster through query optimization ([#128](link))

### Fixed
- Header alignment on mobile devices below 375px width ([#456](link))
- Session timeout not refreshing on user activity ([#789](link))
- Memory leak in WebSocket connection handler ([#457](link))
- Date picker not respecting locale settings ([#458](link))
- Incorrect pagination on filtered results ([#459](link))
- Double submission on slow network connections ([#460](link))
- Missing validation on email field in settings ([#461](link))

### Security
- Updated bcrypt to fix timing attack vulnerability (CVE-2024-XXXX) ([#790](link))
```

---

**Update CHANGELOG.md?** (yes/no/edit)
</output>
</example>

<example>
<input>
/changelog --since=v2.0.0
</input>
<output>
Analyzing commits since v2.0.0...

Found 45 commits across 3 minor versions.

---

## Generated Changelog Entry

```markdown
## [Unreleased]

### Added
- Real-time notifications via WebSocket ([#200](link))
- Two-factor authentication support ([#201](link))

### Changed
- Migrated from REST to GraphQL for mobile API ([#202](link))

### Breaking Changes
- GraphQL API endpoint changed from `/api/v2` to `/graphql`
  - Migration: Update API client to use new endpoint
  - Old endpoint deprecated, will be removed in v3.0.0
```

---

**Update CHANGELOG.md?** (yes/no/edit)
</output>
</example>
</examples>

<rules>
- Follow Keep a Changelog format exactly
- Include PR/issue links when available
- Write from user perspective, not developer
- Breaking changes get their own section AND mention in relevant section
- Security fixes always included regardless of commit type
- Skip docs/chore/test commits unless user-facing
- Date format: YYYY-MM-DD
</rules>

<error_handling>
If no commits found: "No new commits since [tag]. Nothing to add."
If no conventional commits: "Commits don't follow conventional format. Generating best-effort changelog."
If CHANGELOG.md missing: "No CHANGELOG.md found. Create one?"
If merge conflicts: "CHANGELOG.md has conflicts. Resolve before updating."
</error_handling>

## Categories Reference

| Commit Type | Changelog Section |
|-------------|-------------------|
| `feat` | Added |
| `fix` | Fixed |
| `perf` | Changed |
| `refactor` | Changed |
| `security` | Security |
| `BREAKING CHANGE` | Breaking Changes |
| `deprecate` | Deprecated |
| `remove` | Removed |
| `docs` | (skip) |
| `test` | (skip) |
| `chore` | (skip) |
