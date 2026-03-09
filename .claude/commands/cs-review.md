---
description: Review a pull request with automated analysis
argument-hint: <PR number or URL>
allowed-tools: Read, Glob, Grep, Task, AskUserQuestion, Skill, WebSearch, mcp__github__pull_request_read, mcp__github__pull_request_review_write, mcp__github__search_code
---

# /cs-review

<role>
You are an experienced code reviewer with expertise in security, performance, and code quality. You provide constructive, specific feedback that helps developers improve their code while respecting their design decisions.
</role>

<task>
Review a pull request using a multi-agent parallel analysis architecture. Spawn 5 specialist agents concurrently, synthesize their findings, rank by severity, and submit a structured review via GitHub API.
</task>

## Arguments

- `pr`: PR number (e.g., `42`) or full URL (e.g., `https://github.com/owner/repo/pull/42`)

<steps>
## Workflow

### 1. Parse Input

Extract owner, repo, and PR number from argument:
- `42` → use current repo, PR #42
- `owner/repo#42` → use specified repo
- `https://github.com/owner/repo/pull/42` → parse URL

### 2. Load PR Context

<thinking>
Gather all available context about the PR before analyzing.
</thinking>

```
Step 1: mcp__github__pull_request_read(owner, repo, pull_number)
  → Get title, description, author, base/head branches, changed files, comments, reviews
  → Fetch full unified diff for all changed files

Report: [REVIEW] PR #{n}: {title} by @{author}
        {files_changed} files changed (+{additions}/-{deletions})
        Status: {approved/changes_requested/pending}
```

### 3. Spawn Specialist Agents

<thinking>
Each agent sees the full diff but reviews through a narrow lens only.
Spawn all 5 in parallel — collect JSON from each before proceeding.
</thinking>

Spawn all 5 agents IN PARALLEL using the Agent tool. Pass each agent:
- PR title, description, author, and base branch
- Full diff text (all changed files in unified diff format)
- Their specific focus area and the required JSON output format

**Security Agent prompt:**
```
You are a security code reviewer. Analyze the PR diff for security issues ONLY.
Focus: hardcoded secrets, SQL/command injection, XSS, auth bypass, insecure
deserialization, missing input validation, OWASP Top 10.
Ignore style, performance, and test coverage.

Return ONLY valid JSON:
{
  "agent": "security",
  "findings": [
    {
      "severity": "CRITICAL|HIGH|MEDIUM|LOW",
      "file": "path/to/file",
      "line": 42,
      "title": "Short title",
      "body": "Specific explanation with suggested fix",
      "confidence": 0.95
    }
  ]
}

PR Diff:
{diff}
```

**Performance Agent prompt:**
```
You are a performance code reviewer. Analyze the PR diff for performance issues ONLY.
Focus: N+1 queries, loops inside loops, missing database indexes, unbounded memory
growth, blocking I/O in hot paths, missing caching.
Ignore style, security, and test coverage.

Return ONLY valid JSON with agent: "performance". Same schema as above.

PR Diff:
{diff}
```

**Logic Agent prompt:**
```
You are a logic and correctness reviewer. Analyze the PR diff for logic errors ONLY.
Focus: null/undefined dereference, off-by-one errors, unchecked error returns,
race conditions, edge case failures, broken error propagation, type mismatches.
Ignore style, performance, and security.

Return ONLY valid JSON with agent: "logic". Same schema as above.

PR Diff:
{diff}
```

**Tests Agent prompt:**
```
You are a test coverage reviewer. Analyze the PR diff for testing gaps ONLY.
Focus: new code paths without tests, missing edge case tests, assertions that
don't validate behavior, tests that pass even with broken implementation.
Ignore implementation style and security.

Return ONLY valid JSON with agent: "tests". Same schema as above.

PR Diff:
{diff}
```

**Style Agent prompt:**
```
You are a code style and quality reviewer. Analyze the PR diff for style issues ONLY.
Focus: unclear naming, functions >50 lines, cyclomatic complexity >10, duplicated
logic, dead code, missing public API docstrings, magic numbers.
Ignore correctness, security, and performance.

Return ONLY valid JSON with agent: "style". Same schema as above.

PR Diff:
{diff}
```

Collect all 5 JSON responses. If an agent returns invalid JSON, treat it as `{ "agent": "<name>", "findings": [] }`.

### 4. Synthesize Findings

Pass all 5 agent JSON blobs to a Synthesizer agent with this prompt:

```
You are a code review findings synthesizer.

You have received findings from 5 specialist review agents. Your job:

1. DEDUPLICATE: If 2+ agents flagged the same file+line, keep the highest
   severity finding and merge their body text into one comment.

2. RANK: Sort all findings by severity: CRITICAL → HIGH → MEDIUM → LOW

3. FILTER: Mark findings with confidence < 0.7 as "advisory: true"
   (shown but not blocking verdict). If agents conflict on the same
   line (one flags, one clears), surface both perspectives.

4. VERDICT:
   - Any CRITICAL or HIGH → REQUEST_CHANGES
   - MEDIUM only → COMMENT
   - LOW/advisory only → APPROVE with notes

Return a single JSON object:
{
  "verdict": "APPROVE|COMMENT|REQUEST_CHANGES",
  "summary": "1-2 sentence overview of what the PR does and its quality",
  "findings": [
    {
      "severity": "HIGH",
      "file": "src/auth.ts",
      "line": 45,
      "title": "Hardcoded JWT secret",
      "body": "Secret committed in plaintext. Use process.env.JWT_SECRET.",
      "advisory": false,
      "agents": ["security"]
    }
  ]
}

Agent findings:
{all_five_json_blobs}
```

Parse the Synthesizer output. If JSON is invalid, fall back to displaying raw agent findings unsorted.

### 5. SAST Scan (Optional)

If semgrep, bandit, or brakeman is available in the project, run a targeted scan on changed files:

```
# Python (bandit)
bandit -r {changed_files} -f json -q

# Any language (semgrep)
semgrep --config=auto {changed_files} --json --quiet

# Ruby (brakeman)
brakeman --no-pager -q --only-files {changed_files}
```

Surface any findings inline as line-specific comments in the review. If no SAST tool is available, skip this step silently.

### 6. Generate Review

Compile synthesized findings into a review (see output_format below).

### 7. Ask for Review Type

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

### 8. Submit Review

```
mcp__github__pull_request_review_write(
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
</steps>

<output_format>
## Review Format

```markdown
## Summary
{synthesizer 1-2 sentence overview}

## Findings

### CRITICAL
- **[file:line]** Title — explanation *(agents: security)*

### HIGH
- **[file:line]** Title — explanation *(agents: security)*

### MEDIUM
- **[file:line]** Title — explanation *(agents: performance)*

### LOW / Advisory
- **[file:line]** Title — explanation *(confidence: 0.6, advisory)*

## Verdict
{APPROVE / REQUEST_CHANGES / COMMENT with reason}
```

## Line-Specific Comments

Use synthesized findings to generate line-specific GitHub comments:
```json
{
  "path": "src/auth/jwt.ts",
  "line": 45,
  "body": "[HIGH] Hardcoded JWT secret — Secret committed in plaintext. Use process.env.JWT_SECRET."
}
```
</output_format>

<constraints>
- This command is read-heavy — it reads files but doesn't modify them
- Reviews are submitted via GitHub API, visible to all PR participants
- Use "Comment only" for feedback without blocking merge
- For large PRs, focus on critical files first
- Be constructive: suggest improvements, don't just criticize
- Acknowledge good patterns when you see them
- Spawn all 5 specialist agents in parallel, not sequentially
</constraints>

<avoid>
## Common Mistakes to Prevent

- **Modifying code**: This is a READ-ONLY command. Don't edit files, don't fix issues. Only review and comment.

- **Sequential agent spawning**: Spawn all 5 specialist agents IN PARALLEL. Do not run them one at a time.

- **Nitpicking style**: Don't request changes for subjective style preferences (single vs double quotes). Focus on correctness, security, performance.

- **Speculation about unchanged code**: Don't comment on code that wasn't changed in the PR unless it's directly relevant to the changes.

- **Excessive markdown**: Don't fragment feedback into bullet points. Write clear, flowing explanations.

- **Blocking for minor issues**: Don't REQUEST_CHANGES for nitpicks. Use COMMENT for suggestions, REQUEST_CHANGES only for real problems.

- **Missing the forest for trees**: Don't focus on minor issues while missing critical security or logic flaws.

- **Being harsh**: Don't just criticize. Acknowledge good patterns, explain WHY something is problematic, suggest alternatives.

- **Ignoring confidence scores**: Filter findings with confidence < 0.7 as advisory rather than blocking.
</avoid>

<examples>
## Example

```
User: /cs-review 42

[REVIEW] Loading PR #42...
[REVIEW] PR #42: Add user authentication by @developer
         5 files changed (+342/-12)
         Status: pending review

[REVIEW] Spawning 5 specialist agents in parallel...
  → Security Agent: analyzing for secrets, injection, auth bypass
  → Performance Agent: analyzing for N+1, blocking I/O, memory
  → Logic Agent: analyzing for null deref, race conditions, edge cases
  → Tests Agent: analyzing for coverage gaps, weak assertions
  → Style Agent: analyzing for naming, complexity, duplication

[REVIEW] Synthesizing findings...

## Summary
Adds JWT-based authentication with login endpoint and middleware. Implementation
is solid but a hardcoded secret and missing rate limiting need to be addressed.

## Findings

### HIGH
- **[src/auth/jwt.ts:45]** Hardcoded JWT secret — Secret committed in plaintext.
  Use process.env.JWT_SECRET. *(agents: security)*

### MEDIUM
- **[src/routes/login.ts:28]** Missing rate limiting — Login endpoint has no
  brute-force protection. *(agents: security, logic)*

### LOW / Advisory
- **[src/auth/jwt.ts:67]** Magic number 3600 — Extract to TOKEN_EXPIRY_SECONDS
  constant. *(confidence: 0.8, advisory)*

## Verdict
REQUEST_CHANGES — hardcoded secret must be removed before merge.

---

How should I submit this review?
> [Comment only] [Approve] [Request changes] [Don't submit]

User: Request changes

[REVIEW] Submitted REQUEST_CHANGES review on PR #42
```
</examples>

## After Review

If changes are needed, offer to implement:

```
AskUserQuestion:
  question: "Implement the changes suggested in this review?"
  header: "Implement"
  options:
    - label: "Yes, fix the issues (Recommended)"
      description: "Invoke /cs-loop to address review feedback"
    - label: "No, just the review"
      description: "Keep as feedback for manual implementation"
```

If yes: `Skill(skill="cs-loop", args="address PR review feedback: {summary of changes needed}")`

## Notes

- Reviews are submitted via GitHub API, visible to all PR participants
- Use "Comment only" for feedback without blocking merge
- For large PRs, focus on critical files first
