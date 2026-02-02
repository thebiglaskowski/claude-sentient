---
name: cc-pr
description: Create pull request with auto-generated description
model: sonnet
argument-hint: "[--draft] [--base=BRANCH]"
---

# /pr - Create Pull Request

<context>
Pull requests are the gateway to merging code. A well-written PR description
helps reviewers understand changes quickly, reduces review cycles, and creates
valuable documentation for future reference.
</context>

<role>
You are a developer who creates clear, comprehensive pull requests that:
- Summarize changes concisely
- Explain the purpose and impact
- Include testing evidence
- Make reviewers' jobs easier
</role>

## Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `--draft` | Create as draft PR | `/pr --draft` |
| `--base=B` | Target branch | `/pr --base=develop` |

## Usage Examples

```
/pr                             # Create PR to default branch
/pr --draft                     # Create draft PR
/pr --base=develop              # PR to develop branch
```

<task>
Create a pull request by:
1. Analyzing commits since branch point
2. Summarizing changes meaningfully
3. Generating structured PR description
4. Creating PR with appropriate labels
5. Returning URL for review
</task>

<instructions>
<step number="1">
**Gather context**: Run these commands to understand the PR:
- `git log main..HEAD --oneline` — All commits to include
- `git diff main --stat` — Files changed summary
- `git branch --show-current` — Current branch name
</step>

<step number="2">
**Analyze changes**: Review each commit to understand:
- What type of change is this? (feat/fix/chore/etc.)
- What's the business impact?
- Are there breaking changes?
- What testing was done?
</step>

<step number="3">
**Generate title**: Create concise PR title:
- Format: `[TICKET-ID] Type: Brief description`
- Or: `Type: Brief description` if no ticket
- Max 72 characters
</step>

<step number="4">
**Write description**: Generate comprehensive PR body:
- Summary (1-3 bullets of key changes)
- Detailed changes list
- Testing checklist
- Screenshots if UI changes
- Breaking changes if any
</step>

<step number="5">
**Create PR**: Use `gh pr create` with generated content.
Add appropriate labels based on change type.
</step>
</instructions>

<output_format>
## Pull Request Preview

**Title:** [Generated title]
**Base:** [target branch]
**Head:** [current branch]

---

### Description Preview

## Summary
- [Key change 1]
- [Key change 2]

## Changes
- [Detailed change list]

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated

---

**Labels:** [suggested labels]

**Create this PR?** (yes/no/edit)
</output_format>

<examples>
<example>
<input>
Branch: feature/AUTH-123-add-oauth-login
Commits:
- Add Google OAuth provider
- Add OAuth callback handler
- Add login UI with OAuth button
- Add tests for OAuth flow
</input>
<thinking>
1. This is a feature branch for authentication
2. Multiple commits add OAuth functionality
3. Has tests - good!
4. Should mention security implications
5. Title should reference ticket
</thinking>
<output>
## Pull Request Preview

**Title:** [AUTH-123] feat: Add Google OAuth login
**Base:** main
**Head:** feature/AUTH-123-add-oauth-login

---

### Description Preview

## Summary
- Adds Google OAuth 2.0 authentication as login option
- Implements secure OAuth flow with PKCE
- Includes comprehensive test coverage

## Changes
- `src/auth/oauth.ts` - OAuth provider and token handling
- `src/auth/callback.ts` - OAuth callback with state verification
- `src/components/LoginButton.tsx` - OAuth login UI
- `src/auth/__tests__/oauth.test.ts` - Unit tests

## Testing
- [x] Unit tests added (15 new tests)
- [x] Integration tests pass
- [ ] Manual testing completed

## Screenshots
[Login button with OAuth option]

## Security Considerations
- Uses PKCE for enhanced security
- State parameter prevents CSRF
- Tokens stored in httpOnly cookies

## Checklist
- [x] Code follows style guidelines
- [x] Self-review completed
- [ ] Documentation updated

---

**Labels:** `feature`, `auth`, `needs-review`

**Create this PR?** (yes/no/edit)
</output>
</example>

<example>
<input>
Branch: fix/UI-456-header-alignment
Commits:
- Fix header alignment on mobile
</input>
<output>
## Pull Request Preview

**Title:** [UI-456] fix: Correct header alignment on mobile
**Base:** main
**Head:** fix/UI-456-header-alignment

---

### Description Preview

## Summary
- Fixes header misalignment issue on mobile viewports

## Changes
- `src/components/Header.css` - Adjusted flex properties for mobile

## Root Cause
Header used `justify-content: space-between` which caused uneven
spacing on viewports <768px. Changed to explicit gap with flex-wrap.

## Testing
- [x] Manual testing on iOS Safari
- [x] Manual testing on Android Chrome
- [x] Desktop browsers unaffected

## Screenshots
| Before | After |
|--------|-------|
| [misaligned] | [aligned] |

---

**Labels:** `bug`, `ui`, `mobile`

**Create this PR?** (yes/no/edit)
</output>
</example>
</examples>

<rules>
- Always include commit analysis in description
- Reference ticket numbers when available
- Warn if PR has >500 lines changed
- Suggest splitting large PRs
- Include screenshots for UI changes
- Mark breaking changes prominently
- Add appropriate labels automatically
</rules>

<error_handling>
If no commits to include: "No commits between main and current branch."
If uncommitted changes: "You have uncommitted changes. Commit or stash first."
If gh CLI not available: Provide PR description to copy manually
If branch not pushed: Push branch first, then create PR
</error_handling>

## PR Template

```markdown
## Summary
[1-3 bullet points of changes]

## Changes
- [Detailed change list]

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Screenshots (if UI)
[Before/after if applicable]

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
```
