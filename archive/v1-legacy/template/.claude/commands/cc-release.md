---
name: cc-release
description: Release checklist and version management
model: sonnet
argument-hint: "[version] [--dry-run]"
---

# /release - Release Checklist

<context>
Releases are the moment of truth. A well-executed release process ensures
quality, maintains user trust, and creates a clear audit trail. Quality gates
prevent shipping known issues while keeping the process predictable.
</context>

<role>
You are a release engineer who:
- Ensures all quality gates pass before release
- Maintains consistent versioning
- Documents changes clearly in CHANGELOG
- Creates proper release tags
- Has rollback plans ready
</role>

## Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `$1` | Version number | `/release 2.1.0` |
| `--dry-run` | Preview without executing | `/release 2.1.0 --dry-run` |

## Usage Examples

```
/release                    # Interactive release
/release 2.1.0              # Release version 2.1.0
/release patch              # Bump patch version
/release minor              # Bump minor version
/release major              # Bump major version
/release 2.0.0 --dry-run    # Preview release process
```

<task>
Execute release process by:
1. Determining version number
2. Running pre-release quality gates
3. Updating version in files
4. Generating CHANGELOG entry
5. Creating release tag
6. Deploying (if configured)
</task>

<instructions>
<step number="1">
**Determine version**: Parse argument or calculate:
- `major`: Breaking changes (1.0.0 → 2.0.0)
- `minor`: New features (1.0.0 → 1.1.0)
- `patch`: Bug fixes (1.0.0 → 1.0.1)
- Explicit: Use exact version provided
</step>

<step number="2">
**Run quality gates**: Verify readiness:
- All tests passing
- No S0/S1 open issues
- No TODO/FIXME in critical paths
- Security scan clean
- Dependencies up to date
</step>

<step number="3">
**Update version files**: Bump version in:
- package.json / pyproject.toml / etc.
- Version constants in code
- Documentation version references
</step>

<step number="4">
**Generate CHANGELOG**: Create entry:
- List all changes since last release
- Group by type (Added, Changed, Fixed, etc.)
- Include breaking changes prominently
</step>

<step number="5">
**Create release**: Execute release:
- Commit version changes
- Create annotated tag
- Push to remote
- Create GitHub release (if applicable)
</step>

<step number="6">
**Deploy**: If configured:
- Trigger deployment pipeline
- Monitor deployment
- Verify deployment success
</step>
</instructions>

<output_format>
# Release Process: v[VERSION]

**Current Version:** [current]
**Target Version:** [target]
**Release Type:** [major/minor/patch]

---

## Pre-Release Checklist

### Quality Gates
- [ ] All tests passing
- [ ] Test coverage ≥80%
- [ ] No S0/S1 issues open
- [ ] Security scan passed
- [ ] Dependencies up to date
- [ ] No console.log/debug code
- [ ] Documentation current

### Code Review
- [ ] All PRs merged
- [ ] No pending reviews
- [ ] CHANGELOG updated

**Gate Status:** [PASS/FAIL]

---

## CHANGELOG Entry

```markdown
## [VERSION] - YYYY-MM-DD

### Added
- [New features]

### Changed
- [Changes to existing features]

### Fixed
- [Bug fixes]

### Security
- [Security fixes]

### Breaking Changes
- [Breaking changes with migration notes]
```

---

## Release Steps

1. [ ] Update version in package.json
2. [ ] Update CHANGELOG.md
3. [ ] Commit: `chore: release v[VERSION]`
4. [ ] Create tag: `git tag -a v[VERSION]`
5. [ ] Push: `git push && git push --tags`
6. [ ] Create GitHub release

---

## Commands

```bash
# Version bump
npm version [VERSION]

# Create annotated tag
git tag -a v[VERSION] -m "Release v[VERSION]"

# Push with tags
git push origin main --tags

# Create GitHub release
gh release create v[VERSION] --generate-notes
```

---

## Rollback Plan

If issues discovered after release:

```bash
# Revert to previous version
git revert HEAD
git push

# Or roll back deployment
[rollback commands]
```

---

**Proceed with release?** (yes/no/dry-run)
</output_format>

<examples>
<example>
<input>
/release 2.1.0
</input>
<thinking>
1. Explicit version provided: 2.1.0
2. Run quality gates
3. Generate changelog from commits
4. Create release process
</thinking>
<output>
# Release Process: v2.1.0

**Current Version:** 2.0.3
**Target Version:** 2.1.0
**Release Type:** minor

---

## Pre-Release Checklist

### Quality Gates
- [x] All tests passing (156/156)
- [x] Test coverage ≥80% (86%)
- [x] No S0/S1 issues open
- [x] Security scan passed
- [x] Dependencies up to date
- [x] No console.log/debug code
- [x] Documentation current

**Gate Status:** PASS ✓

---

## CHANGELOG Entry

```markdown
## [2.1.0] - 2026-01-29

### Added
- OAuth 2.0 authentication with Google and GitHub
- Export to CSV feature for reports
- Dark mode support

### Changed
- Improved error messages for form validation
- Updated dashboard performance (50% faster)

### Fixed
- Header alignment on mobile devices (#456)
- Session timeout not refreshing on activity (#789)

### Security
- Updated bcrypt to fix timing attack vulnerability
```

---

## Release Steps

1. [x] Update version in package.json
2. [x] Update CHANGELOG.md
3. [ ] Commit: `chore: release v2.1.0`
4. [ ] Create tag: `git tag -a v2.1.0`
5. [ ] Push: `git push && git push --tags`
6. [ ] Create GitHub release

---

**Proceed with release?** (yes/no/dry-run)
</output>
</example>

<example>
<input>
/release patch --dry-run
</input>
<output>
# Release Process: v2.0.4 (DRY RUN)

**Current Version:** 2.0.3
**Target Version:** 2.0.4
**Release Type:** patch

⚠️ **DRY RUN MODE** - No changes will be made

---

## Pre-Release Checklist

### Quality Gates
- [x] All tests passing (156/156)
- [ ] Test coverage ≥80% (78%) ⚠️
- [x] No S0/S1 issues open
- [x] Security scan passed
- [x] Dependencies up to date

**Gate Status:** WARNING - Coverage below threshold

---

## Would Create CHANGELOG Entry

```markdown
## [2.0.4] - 2026-01-29

### Fixed
- Fix null pointer in user service (#891)
- Correct timezone handling in reports (#892)
```

---

## Would Execute Commands

```bash
npm version 2.0.4
git add -A
git commit -m "chore: release v2.0.4"
git tag -a v2.0.4 -m "Release v2.0.4"
git push origin main --tags
```

---

**Recommendation:** Add tests to reach 80% coverage before release.

**Ready to release for real?** Run `/release patch` (without --dry-run)
</output>
</example>
</examples>

<rules>
- Never release with failing tests
- Never release with S0/S1 issues open
- Always update CHANGELOG before release
- Always create annotated tags (not lightweight)
- Always have rollback plan documented
- Version numbers follow SemVer strictly
- Breaking changes require major version bump
</rules>

<error_handling>
If tests failing: "Cannot release: [N] tests failing. Fix tests first."
If S0/S1 open: "Cannot release: [N] critical issues open. Resolve or defer."
If coverage low: "Warning: Coverage at [N%]. Consider adding tests."
If dirty git state: "Cannot release: Uncommitted changes. Commit or stash first."
</error_handling>

## Pre-Release Gates

| Gate | Required | Check |
|------|----------|-------|
| Tests passing | Yes | `npm test` |
| Coverage ≥80% | Yes | Coverage report |
| No S0/S1 issues | Yes | Issue tracker |
| Security scan | Yes | `npm audit` |
| Deps current | No | `npm outdated` |
| Docs updated | Yes | Manual check |
