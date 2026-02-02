# Plan: High-Value Native Tool Integrations

> **Created:** 2026-02-02
> **Status:** Completed
> **Estimated Scope:** Medium (updates to commands + new workflows)

---

## Overview

Three high-value native capabilities we're not using:
1. **GitHub PR Workflow** — Full PR lifecycle management
2. **Memory Search** — Query prior decisions, not just save them
3. **Skill Chaining** — Commands that invoke other commands

---

## Tasks

### 1. GitHub PR Workflow (High Priority)

**Current state:** We create PRs and add comments, but don't leverage the full API.

**New capabilities:**

| Tool | Use Case |
|------|----------|
| `mcp__github__get_pull_request` | Fetch PR details when working on PR-related tasks |
| `mcp__github__get_pull_request_files` | See what files changed in a PR (for reviews) |
| `mcp__github__get_pull_request_status` | Check if CI passed before suggesting merge |
| `mcp__github__get_pull_request_comments` | Load existing review comments |
| `mcp__github__get_pull_request_reviews` | See approval status |
| `mcp__github__create_pull_request_review` | Submit automated code review |
| `mcp__github__list_commits` | Understand recent changes |
| `mcp__github__search_code` | Find similar implementations across GitHub |
| `mcp__github__search_issues` | Find related issues automatically |

**Changes to `/cs-loop`:**

```markdown
## INIT Phase Additions

**GitHub context loading:**
- If task mentions PR number (e.g., "review PR #42", "fix PR feedback"):
  1. mcp__github__get_pull_request(owner, repo, pull_number)
  2. mcp__github__get_pull_request_files → list changed files
  3. mcp__github__get_pull_request_comments → load review feedback
  4. Report: [INIT] Loaded PR #42: {title} ({n} files, {m} comments)

- If task involves understanding recent changes:
  1. mcp__github__list_commits(owner, repo, sha=branch)
  2. Summarize: [INIT] Recent commits: {commit summaries}

## VERIFY Phase Additions

**PR status check before commit:**
- If working on a PR branch:
  1. mcp__github__get_pull_request_status
  2. If CI failing: [VERIFY] Warning: PR CI is failing
  3. If CI passing: [VERIFY] PR CI is green

## COMMIT Phase Additions

**Automated PR review (when reviewing PRs):**
- After analyzing changes:
  1. mcp__github__create_pull_request_review with:
     - event: "COMMENT" (or "APPROVE" / "REQUEST_CHANGES")
     - body: Summary of findings
     - comments: Line-specific feedback
  2. Report: [COMMIT] Submitted review on PR #{n}
```

**New command: `/cs-review`**

Create a dedicated PR review command:

```markdown
---
description: Review a pull request
argument-hint: <PR number or URL>
allowed-tools: Read, Glob, Grep, Task, mcp__github__get_pull_request, mcp__github__get_pull_request_files, mcp__github__get_pull_request_comments, mcp__github__get_pull_request_reviews, mcp__github__create_pull_request_review, mcp__github__search_code, AskUserQuestion
---

# /cs-review

Review a pull request with automated analysis.

## Workflow

1. **Load PR context**
   - Fetch PR details, files, existing reviews
   - Report: [REVIEW] PR #{n}: {title} by @{author}

2. **Analyze changes**
   - Read each changed file
   - Check for: security issues, performance, style, tests
   - Compare against similar code in repo

3. **Search for patterns** (optional)
   - mcp__github__search_code for similar implementations
   - Check if approach matches existing patterns

4. **Generate review**
   - Summarize findings
   - Add line-specific comments where needed
   - Ask user: "Submit as COMMENT, APPROVE, or REQUEST_CHANGES?"

5. **Submit review**
   - mcp__github__create_pull_request_review
   - Report: [REVIEW] Submitted: {event}
```

---

### 2. Memory Search Integration (High Priority)

**Current state:** We save decisions with `mcp__memory__create_entities` and `add_observations`, but never search them.

**New capabilities:**

| Tool | Use Case |
|------|----------|
| `mcp__memory__search_nodes` | Find relevant prior decisions by keyword |
| `mcp__memory__open_nodes` | Load specific named entities |

**Changes to `/cs-loop`:**

```markdown
## INIT Phase Additions

**Search memory for relevant context:**
- Extract keywords from task description
- mcp__memory__search_nodes(query="{keywords}")
- If matches found:
  1. mcp__memory__open_nodes(names=[...matching entities...])
  2. Inject prior decisions into context
  3. Report: [INIT] Found {n} relevant prior decisions

Example:
Task: "Add JWT authentication"
→ search_nodes("authentication JWT")
→ Found: "auth_decision_2026_01", "jwt_library_choice"
→ Load those entities for context
```

**Structured memory entities:**

Define a schema for what we store:

```markdown
## Memory Entity Types

| Type | Name Pattern | Observations |
|------|--------------|--------------|
| Decision | `decision_{topic}_{date}` | choice, rationale, alternatives |
| Pattern | `pattern_{name}` | description, example, when_to_use |
| Blocker | `blocker_{id}` | description, status, resolution |
| Session | `session_{date}_{task}` | summary, commits, follow_ups |
```

**Changes to `/cs-learn`:**

```markdown
## Save with searchable structure

When saving a decision:
1. Create entity: `decision_{topic}_{date}`
2. Add observations:
   - "type: decision"
   - "topic: {topic}"
   - "choice: {what was chosen}"
   - "rationale: {why}"
3. Create relations to related entities
```

---

### 3. Skill Chaining (Medium Priority)

**Current state:** Commands are standalone. User must manually invoke each.

**New capability:** Commands can invoke other commands via `Skill` tool.

**Use cases:**

| Scenario | Chain |
|----------|-------|
| Plan then execute | `/cs-plan` → (on approval) → `/cs-loop` |
| Status then loop | `/cs-status` → (if tasks pending) → `/cs-loop` |
| Validate then fix | `/cs-validate` → (if issues) → `/cs-loop "fix validation issues"` |

**Changes to `/cs-plan`:**

```markdown
## After Approval

When user approves the plan:

1. Create tasks from plan using TaskCreate
2. Ask: "Execute this plan now?"
3. If yes:
   - Skill(skill="cs-loop", args="{original task}")
   - The loop will pick up the created tasks
4. If no:
   - Report: [PLAN] Tasks created. Run /cs-loop when ready.
```

**Changes to `/cs-status`:**

```markdown
## After Status Report

If there are pending tasks:
1. Ask: "Continue working on these tasks?"
2. If yes:
   - Skill(skill="cs-loop")
   - Loop resumes from pending tasks
```

**Changes to `/cs-validate`:**

```markdown
## After Validation

If validation finds issues:
1. Create tasks for each issue
2. Ask: "Fix these issues automatically?"
3. If yes:
   - Skill(skill="cs-loop", args="fix validation issues")
```

---

### 4. GitHub Code Search (Medium Priority)

**Current state:** Not used at all.

**New capability:** Search GitHub for patterns, examples, implementations.

**Use cases:**

| Scenario | Search |
|----------|--------|
| "How do others implement X?" | Search public repos for patterns |
| "Is there a library for Y?" | Search for existing solutions |
| "What's the standard approach?" | Find best practices |

**Changes to `/cs-loop`:**

```markdown
## UNDERSTAND Phase Additions

**Search for reference implementations:**
- If task involves implementing a standard pattern:
  1. mcp__github__search_code(q="{pattern} language:{lang}")
  2. Review top results for patterns
  3. Report: [UNDERSTAND] Found {n} reference implementations

Example:
Task: "Add rate limiting to the API"
→ search_code("rate limit middleware language:typescript")
→ Found: express-rate-limit patterns, custom implementations
→ Summarize approaches found
```

**Note:** Use sparingly to avoid rate limits. Only for genuinely unfamiliar patterns.

---

## Implementation Order

```
Phase 1: Memory Search (most immediately useful)
  - Add search_nodes to INIT
  - Add open_nodes for loading context
  - Update /cs-learn for structured storage

Phase 2: GitHub PR Workflow
  - Add PR context loading to INIT
  - Add PR status check to VERIFY
  - Create /cs-review command

Phase 3: Skill Chaining
  - Update /cs-plan with auto-execute option
  - Update /cs-status with resume option
  - Update /cs-validate with auto-fix option

Phase 4: GitHub Code Search
  - Add to UNDERSTAND phase
  - Use for pattern discovery
```

---

## Files to Modify

| File | Changes |
|------|---------|
| `commands/cs-loop.md` | Memory search, PR workflow, code search |
| `commands/cs-plan.md` | Skill chaining to cs-loop |
| `commands/cs-status.md` | Skill chaining to cs-loop |
| `commands/cs-validate.md` | Skill chaining to cs-loop |
| `commands/cs-learn.md` | Structured memory storage |
| `commands/cs-review.md` | **New command** for PR review |
| `CLAUDE.md` | Document new integrations |

---

## Success Criteria

- [x] Memory search finds relevant prior decisions in INIT
- [x] PR context loads automatically for PR-related tasks
- [x] /cs-review command works end-to-end
- [x] /cs-plan can auto-invoke /cs-loop after approval
- [x] GitHub code search finds reference implementations
- [x] Documentation updated

---

## New allowed-tools

Add to relevant commands:

```
mcp__github__get_pull_request
mcp__github__get_pull_request_files
mcp__github__get_pull_request_status
mcp__github__get_pull_request_comments
mcp__github__get_pull_request_reviews
mcp__github__create_pull_request_review
mcp__github__list_commits
mcp__github__search_code
mcp__github__search_issues
mcp__memory__search_nodes
mcp__memory__open_nodes
Skill
```

---

## Resume Command

```
/cs-loop "Implement high-value native integrations per reference/PLAN-high-value-native.md"
```

---
