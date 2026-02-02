---
description: Review a pull request with automated analysis
argument-hint: <PR number or URL>
allowed-tools: Read, Glob, Grep, Task, AskUserQuestion, mcp__github__get_pull_request, mcp__github__get_pull_request_files, mcp__github__get_pull_request_comments, mcp__github__get_pull_request_reviews, mcp__github__create_pull_request_review, mcp__github__search_code
---

# /cs-review

Review a pull request with automated analysis. Fetches PR context, analyzes changes, and submits a review.

## Arguments

- `pr`: PR number (e.g., `42`) or full URL (e.g., `https://github.com/owner/repo/pull/42`)

## Workflow

### 1. Parse Input

Extract owner, repo, and PR number from argument:
- `42` → use current repo, PR #42
- `owner/repo#42` → use specified repo
- `https://github.com/owner/repo/pull/42` → parse URL

### 2. Load PR Context

```
Step 1: mcp__github__get_pull_request(owner, repo, pull_number)
  → Get title, description, author, base/head branches

Step 2: mcp__github__get_pull_request_files(owner, repo, pull_number)
  → List all changed files with additions/deletions

Step 3: mcp__github__get_pull_request_comments(owner, repo, pull_number)
  → Load existing review comments

Step 4: mcp__github__get_pull_request_reviews(owner, repo, pull_number)
  → Check current approval status

Report: [REVIEW] PR #{n}: {title} by @{author}
        {files_changed} files changed (+{additions}/-{deletions})
        Status: {approved/changes_requested/pending}
```

### 3. Analyze Changes

For each changed file:
1. Read the file content
2. Check for common issues:

| Category | What to Check |
|----------|---------------|
| Security | Hardcoded secrets, SQL injection, XSS, auth bypass |
| Performance | N+1 queries, unnecessary loops, missing indexes |
| Style | Naming conventions, code organization, comments |
| Tests | Test coverage for new code, edge cases |
| Types | Type safety, any usage, null handling |
| Logic | Edge cases, error handling, race conditions |

### 4. Search for Patterns (Optional)

For unfamiliar patterns, search GitHub:
```
mcp__github__search_code(q="{pattern} language:{lang}")
→ Compare PR approach against common implementations
→ Note if PR deviates from standard patterns
```

### 5. Generate Review

Compile findings into a review:

```markdown
## Summary
{1-2 sentence overview of the changes}

## Findings

### Security
- [ ] No hardcoded secrets found
- [ ] Input validation present

### Code Quality
- {specific feedback}

### Suggestions
- {optional improvements}

## Verdict
{APPROVE / REQUEST_CHANGES / COMMENT reason}
```

### 6. Ask for Review Type

```
AskUserQuestion:
  question: "How should I submit this review?"
  header: "Review"
  options:
    - label: "Comment only"
      description: "Leave feedback without approval status"
    - label: "Approve"
      description: "Approve the PR with comments"
    - label: "Request changes"
      description: "Block merge until issues addressed"
    - label: "Don't submit"
      description: "Show review but don't post it"
```

### 7. Submit Review

```
mcp__github__create_pull_request_review(
  owner, repo, pull_number,
  event: "COMMENT" | "APPROVE" | "REQUEST_CHANGES",
  body: {review summary},
  comments: [
    { path: "file.ts", line: 42, body: "Consider using..." },
    ...
  ]
)

Report: [REVIEW] Submitted {event} review on PR #{n}
```

## Example

```
User: /cs-review 42

[REVIEW] Loading PR #42...
[REVIEW] PR #42: Add user authentication by @developer
         5 files changed (+342/-12)
         Status: pending review

[REVIEW] Analyzing changes...
  src/auth/jwt.ts: New file, JWT utilities
  src/middleware/auth.ts: Modified, added token verification
  src/routes/login.ts: Modified, issues JWT on login
  tests/auth.test.ts: New file, 12 test cases
  package.json: Added jsonwebtoken dependency

[REVIEW] Findings:

## Summary
Adds JWT-based authentication with login endpoint and middleware.

## Security
✓ No hardcoded secrets
✓ Token expiration set (1h)
⚠ Consider adding refresh token rotation

## Code Quality
✓ Good test coverage (12 cases)
✓ Error handling present
- Line 45: Consider extracting magic number to constant

## Suggestions
- Add rate limiting to login endpoint
- Document token format in README

---

How should I submit this review?
> [Comment only] [Approve] [Request changes] [Don't submit]

User: Approve

[REVIEW] Submitted APPROVE review on PR #42
```

## Line-Specific Comments

When adding line-specific feedback, format as:
```
comments: [
  {
    path: "src/auth/jwt.ts",
    line: 45,
    body: "Consider extracting `3600` to a named constant like `TOKEN_EXPIRY_SECONDS`"
  }
]
```

## Notes

- This command is read-heavy — it reads files but doesn't modify them
- Reviews are submitted via GitHub API, visible to all PR participants
- Use "Comment only" for feedback without blocking merge
- For large PRs, focus on critical files first
