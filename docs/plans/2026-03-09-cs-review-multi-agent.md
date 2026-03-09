# Multi-Agent cs-review Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Upgrade `/cs-review` to spawn 5 specialist agents in parallel then synthesize findings, replacing the current single-agent sequential review.

**Architecture:** Fetch PR context → spawn Security, Performance, Logic, Tests, and Style agents in parallel via `Task` tool → each returns structured JSON findings → Synthesizer agent deduplicates, ranks by severity, and filters low-confidence findings → present ranked output → submit via GitHub API.

**Tech Stack:** Markdown command files, Claude Code `Task` tool (Agent spawning), `mcp__github__pull_request_read`, `mcp__github__pull_request_review_write`

---

### Task 1: Write failing tests for multi-agent cs-review

**Files:**
- Modify: `.claude/commands/__tests__/test-commands.js`

**Step 1: Add the failing test suite**

Add this suite before the final `summary()` call in `test-commands.js`:

```javascript
// ─────────────────────────────────────────────────────────────
suite('cs-review multi-agent', () => {
    const reviewPath = path.join(commandsDir, 'cs-review.md');

    test('cs-review has Task in allowed-tools', () => {
        if (fs.existsSync(reviewPath)) {
            const content = fs.readFileSync(reviewPath, 'utf8');
            const parsed = parseFrontmatter(content);
            assert.ok(parsed && parsed.frontmatter['allowed-tools'] &&
                parsed.frontmatter['allowed-tools'].includes('Task'),
                'cs-review allowed-tools must include Task for agent spawning');
        }
    });

    test('cs-review spawns specialist agents in parallel', () => {
        if (fs.existsSync(reviewPath)) {
            const content = fs.readFileSync(reviewPath, 'utf8');
            assert.ok(content.includes('Security Agent') || content.includes('security agent'),
                'cs-review should reference Security agent spawn');
            assert.ok(content.includes('Performance Agent') || content.includes('performance agent'),
                'cs-review should reference Performance agent spawn');
            assert.ok(content.includes('Logic Agent') || content.includes('logic agent'),
                'cs-review should reference Logic agent spawn');
        }
    });

    test('cs-review has synthesizer step', () => {
        if (fs.existsSync(reviewPath)) {
            const content = fs.readFileSync(reviewPath, 'utf8');
            assert.ok(content.includes('ynthesizer') || content.includes('synthesize'),
                'cs-review should have a synthesizer step to merge agent findings');
        }
    });

    test('cs-review defines severity levels', () => {
        if (fs.existsSync(reviewPath)) {
            const content = fs.readFileSync(reviewPath, 'utf8');
            assert.ok(content.includes('CRITICAL') || content.includes('severity'),
                'cs-review should define severity levels for findings');
        }
    });

    test('cs-review defines confidence threshold', () => {
        if (fs.existsSync(reviewPath)) {
            const content = fs.readFileSync(reviewPath, 'utf8');
            assert.ok(content.includes('confidence') || content.includes('false positive'),
                'cs-review should handle confidence filtering / false positives');
        }
    });
});
```

**Step 2: Run tests to confirm they fail**

```bash
bash --norc --noprofile -c "node .claude/commands/__tests__/test-commands.js" 2>/dev/null
```

Expected: 5 new tests FAIL (Task not in allowed-tools, no agent spawning text, no synthesizer, etc.)

**Step 3: Commit the failing tests**

```bash
git add .claude/commands/__tests__/test-commands.js
git commit -m "test: failing tests for cs-review multi-agent upgrade"
```

---

### Task 2: Rewrite cs-review.md with multi-agent architecture

**Files:**
- Modify: `.claude/commands/cs-review.md`

**Step 1: Read the current file**

Read `.claude/commands/cs-review.md` in full to understand current structure before editing.

**Step 2: Update frontmatter — add Task to allowed-tools**

Change the `allowed-tools` line to include `Task`:

```yaml
allowed-tools: Read, Glob, Grep, Task, AskUserQuestion, Skill, WebSearch, mcp__github__pull_request_read, mcp__github__pull_request_review_write, mcp__github__search_code
```

**Step 3: Replace steps section**

Replace the entire `<steps>` block with the new multi-agent workflow. The key structural changes:

1. **Steps 1–2** (Parse Input, Load PR Context) — keep identical
2. **Step 3** — replace "Analyze Changes" (single loop) with "Spawn Specialist Agents"
3. **Step 4** — replace "Search for Patterns" with "Synthesize Findings"
4. **Steps 5–7** — keep SAST, Generate Review, Ask for Review Type, Submit (renumbered)

**New Step 3 content:**

```markdown
### 3. Spawn Specialist Agents

Spawn all 5 agents IN PARALLEL using the Agent tool. Pass each agent:
- The PR title, description, and author
- The full diff text (all changed files with unified diff format)
- Their specific focus area and output format requirement

#### Agent Prompts

**Security Agent:**
```
You are a security code reviewer. Analyze this PR diff for security issues ONLY.
Focus: hardcoded secrets, SQL/command injection, XSS, auth bypass, insecure deserialization,
missing input validation, OWASP Top 10. Ignore style, performance, and test coverage.

Output ONLY valid JSON in this exact format:
{
  "agent": "security",
  "findings": [
    {
      "severity": "CRITICAL|HIGH|MEDIUM|LOW",
      "file": "path/to/file",
      "line": 42,
      "title": "Short title",
      "body": "Specific explanation with fix suggestion",
      "confidence": 0.0-1.0
    }
  ]
}

PR Diff:
{diff}
```

**Performance Agent:**
```
You are a performance code reviewer. Analyze this PR diff for performance issues ONLY.
Focus: N+1 queries, unnecessary loops inside loops, missing database indexes,
unbounded memory growth, blocking I/O in hot paths, missing caching opportunities.
Ignore style, security, and test coverage.

Output ONLY valid JSON:
{
  "agent": "performance",
  "findings": [...]
}

PR Diff:
{diff}
```

**Logic Agent:**
```
You are a logic and correctness code reviewer. Analyze this PR diff for logic errors ONLY.
Focus: null/undefined dereference, off-by-one errors, unchecked error returns,
race conditions, incorrect edge case handling, broken error propagation, type mismatches.
Ignore style, performance, and security.

Output ONLY valid JSON:
{
  "agent": "logic",
  "findings": [...]
}

PR Diff:
{diff}
```

**Tests Agent:**
```
You are a test coverage code reviewer. Analyze this PR diff for testing gaps ONLY.
Focus: new code paths without tests, missing edge case tests, assertions that
don't actually validate behavior, tests that would pass even if implementation broke.
Ignore implementation style and security.

Output ONLY valid JSON:
{
  "agent": "tests",
  "findings": [...]
}

PR Diff:
{diff}
```

**Style Agent:**
```
You are a code style and quality reviewer. Analyze this PR diff for style issues ONLY.
Focus: unclear naming, functions >50 lines, cyclomatic complexity >10, duplicated logic,
dead code, missing docstrings for public APIs, magic numbers without constants.
Ignore correctness, security, and performance.

Output ONLY valid JSON:
{
  "agent": "style",
  "findings": [...]
}

PR Diff:
{diff}
```

Collect all 5 JSON responses. If an agent fails to return valid JSON, treat it as empty findings.
```

**New Step 4 content:**

```markdown
### 4. Synthesize Findings

Pass all 5 agent JSON blobs to a Synthesizer agent:

```
You are a findings synthesizer for a code review system.

You have received findings from 5 specialist review agents. Your job:

1. DEDUPLICATE: If 2+ agents flagged the same file+line, keep the highest severity finding.
   Merge their body text into one comment.

2. RANK: Sort all findings by severity: CRITICAL → HIGH → MEDIUM → LOW

3. FILTER: Mark findings with confidence < 0.7 as "advisory" (show but note low confidence).
   If agents conflict on the same line (one flags, one clears), surface both perspectives.

4. OUTPUT: Return a single JSON object:
{
  "verdict": "APPROVE|COMMENT|REQUEST_CHANGES",
  "summary": "1-2 sentence overview",
  "findings": [
    {
      "severity": "HIGH",
      "file": "src/auth.ts",
      "line": 45,
      "title": "Hardcoded JWT secret",
      "body": "...",
      "advisory": false,
      "agents": ["security"]
    }
  ]
}

Verdict rules:
- CRITICAL or HIGH findings → REQUEST_CHANGES
- MEDIUM findings only → COMMENT
- LOW/advisory only → APPROVE with notes

Agent findings:
{all_five_json_blobs}
```

Parse the synthesizer output and proceed to display.
```

**Step 4: Update output_format section**

Update the `<output_format>` section to reflect ranked multi-agent findings:

```markdown
## Review Format

```markdown
## Summary
{synthesizer 1-2 sentence overview}

## Findings by Severity

### CRITICAL
- **[file:line]** Title — explanation (agents: security, logic)

### HIGH
- **[file:line]** Title — explanation (agents: security)

### MEDIUM
- **[file:line]** Title — explanation (agents: performance)

### Advisory (low confidence)
- **[file:line]** Title — explanation *(confidence: 0.6)*

## Verdict
{APPROVE / REQUEST_CHANGES / COMMENT reason}
```

**Step 5: Run failing tests — should now pass**

```bash
bash --norc --noprofile -c "node .claude/commands/__tests__/test-commands.js" 2>/dev/null
```

Expected: all tests pass including the 5 new ones.

**Step 6: Commit**

```bash
git add .claude/commands/cs-review.md
git commit -m "feat: upgrade cs-review to multi-agent parallel review with synthesizer"
```

---

### Task 3: Update CHANGELOG.md and STATUS.md

**Files:**
- Modify: `CHANGELOG.md`
- Modify: `STATUS.md`

**Step 1: Read current CHANGELOG.md top section**

Read `CHANGELOG.md` (first 50 lines) to see current version and format.

**Step 2: Add v1.5.9 entry to CHANGELOG.md**

Add at the top of the changelog entries (after the header):

```markdown
## [1.5.9] — 2026-03-09

### Added
- `/cs-review` now spawns 5 specialist agents in parallel (Security, Performance, Logic, Tests, Style)
- Synthesizer agent deduplicates cross-agent findings, ranks by severity, filters false positives
- Confidence scoring: findings < 0.7 confidence surfaced as advisory-only
- Severity-ranked output: CRITICAL → HIGH → MEDIUM → LOW
```

**Step 3: Update version in STATUS.md**

Change `Version: 1.5.8` → `Version: 1.5.9` and update `Last Updated` date.

**Step 4: Commit**

```bash
git add CHANGELOG.md STATUS.md
git commit -m "docs: bump to v1.5.9, update changelog for multi-agent cs-review"
```

---

### Task 4: Update CLAUDE.md version and regenerate checksums

**Files:**
- Modify: `CLAUDE.md`
- Run: `generate-checksums.sh`

**Step 1: Update version in CLAUDE.md**

Change the version line in CLAUDE.md from `1.5.8` → `1.5.9`.

**Step 2: Read generate-checksums.sh to understand what it does**

Read `generate-checksums.sh` before running it.

**Step 3: Run checksum generation**

```bash
bash --norc --noprofile -c "bash generate-checksums.sh"
```

Expected: checksums file updated without errors.

**Step 4: Run full test suite to confirm nothing broke**

```bash
bash --norc --noprofile -c "node .claude/commands/__tests__/test-commands.js" 2>/dev/null
bash --norc --noprofile -c "node integration/__tests__/test-integration.js" 2>/dev/null
```

Expected: all tests pass.

**Step 5: Commit and push**

```bash
git add CLAUDE.md checksums.sha256  # or whatever the checksum file is named
git commit -m "chore: update checksums and version for v1.5.9"
git push
```

---

## Verification Checklist

- [ ] All 5 new test suite tests pass
- [ ] Full command test suite passes (81+ tests)
- [ ] Integration tests pass (69 tests)
- [ ] `cs-review.md` has `Task` in `allowed-tools`
- [ ] `cs-review.md` references all 5 agent types by name
- [ ] `cs-review.md` has synthesizer step with deduplication/ranking/confidence rules
- [ ] CHANGELOG has v1.5.9 entry
- [ ] STATUS.md shows v1.5.9
- [ ] CLAUDE.md shows v1.5.9
- [ ] Checksums regenerated
- [ ] Changes pushed to remote
