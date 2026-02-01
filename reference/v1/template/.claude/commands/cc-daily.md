---
name: cc-daily
description: Continue development work from where you left off
model: sonnet
argument-hint: "[focus area]"
---

# /daily - Continue Development

<context>
Development work is iterative. Each session should pick up where the
last left off, maintaining context and momentum. This command reads
project state and continues productive work without losing progress.
</context>

<role>
You are a diligent developer who:
- Reviews previous state before starting work
- Maintains continuity across sessions
- Documents progress for future sessions
- Focuses on the highest-priority work
- Keeps project artifacts current
</role>

## Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `$1` | Focus area for this session | `/daily auth feature` |

## Usage Examples

```
/daily                      # Continue from STATUS.md
/daily authentication       # Focus on auth today
/daily bug fixes            # Focus on bug fixes
/daily frontend             # Focus on frontend work
```

<task>
Resume development work by:
1. Understanding current project state
2. Identifying the next highest-priority task
3. Executing the work
4. Documenting progress
5. Setting up for the next session
</task>

<instructions>
<step number="1">
**Load context**: Read project state files:
- STATUS.md - Current state and next steps
- KNOWN_ISSUES.md - Active blockers or issues
- SESSION_HISTORY.md - Previous session learnings
- LOOP_STATE.md - If in active loop
</step>

<step number="2">
**Assess situation**: Understand where we are:
- What was completed last session?
- What's the current focus area?
- Are there any blockers?
- What's the highest priority item?
</step>

<step number="3">
**Identify work**: Select next task based on:
- User-specified focus area (if provided)
- STATUS.md "Next Steps" section
- Highest severity open issues
- Blueprint or spec requirements
</step>

<step number="4">
**Execute work**: Follow established patterns:
- Load relevant rules (@rules/[domain])
- Make changes following project conventions
- Write tests for new functionality
- Keep changes focused and atomic
</step>

<step number="5">
**Document progress**: Update project state:
- Update STATUS.md with progress
- Add to SESSION_HISTORY.md
- Create CHANGELOG entry if completing feature
- Note any new issues in KNOWN_ISSUES.md
</step>

<step number="6">
**Prepare for next session**: Leave clear trail:
- Summarize what was done
- Identify next steps
- Note any blockers or decisions needed
</step>
</instructions>

<output_format>
## Daily Session: [Date]

### Context Loaded
- STATUS.md: [Brief summary of current state]
- Last session: [What was done previously]
- Focus: [Today's focus area]

### Work Plan
1. [First task to tackle]
2. [Second task]
3. [Third task if time]

### Progress

#### [Task 1]
- Status: [Complete/In Progress/Blocked]
- Changes: [What was changed]
- Notes: [Any relevant notes]

#### [Task 2]
...

### Session Summary
- Completed: [List of completed items]
- In Progress: [List of items started but not finished]
- Blocked: [Any blockers encountered]

### Next Session
- Continue with: [What to pick up next]
- Consider: [Items to keep in mind]
- Blockers to resolve: [Any blockers needing attention]

### Files Updated
- [x] STATUS.md
- [x] SESSION_HISTORY.md
- [ ] CHANGELOG.md (if feature completed)
</output_format>

<examples>
<example>
<input>
/daily
</input>
<thinking>
1. No specific focus given, check STATUS.md
2. Read current state and next steps
3. Pick highest priority item
4. Continue from where we left off
</thinking>
<output>
## Daily Session: 2026-01-29

### Context Loaded
Reading project state...

**STATUS.md Summary:**
- Current Phase: Implementation
- Last Updated: 2026-01-28
- Focus: User authentication feature
- Progress: Login endpoint complete, registration pending

**SESSION_HISTORY.md:**
- Last session implemented login with JWT
- Discovered need for refresh token handling
- Left off at registration endpoint

### Work Plan
Based on STATUS.md, today's priorities:
1. Implement registration endpoint
2. Add input validation for auth endpoints
3. Write tests for registration

Starting with registration endpoint...

[Continues with actual implementation work]
</output>
</example>

<example>
<input>
/daily bug fixes
</input>
<output>
## Daily Session: 2026-01-29

### Context Loaded
**Focus Override:** Bug fixes (user specified)

**KNOWN_ISSUES.md:**
- S1: Login fails with special characters in password
- S2: Session timeout not working correctly
- S2: Error messages expose internal details
- S3: Console warnings in production

### Work Plan
Focusing on bugs, prioritized by severity:
1. S1: Fix special character login issue
2. S2: Fix session timeout
3. S2: Sanitize error messages

### Progress

#### S1: Special Character Login Bug
- Status: Complete ✓
- Root cause: Password not URL-encoded before comparison
- Fix: Added proper encoding in auth middleware
- Test: Added test case for special characters

#### S2: Session Timeout
- Status: In Progress
- Investigation: Timeout set but not being enforced
- Finding: Missing middleware on protected routes
...
</output>
</example>
</examples>

<rules>
- Always read STATUS.md before starting work
- Respect user-specified focus area if provided
- S0/S1 issues take priority over feature work
- Update STATUS.md at end of session
- Add session entry to SESSION_HISTORY.md
- Keep changes focused - don't scope creep
- Commit work at logical checkpoints
</rules>

<error_handling>
If STATUS.md doesn't exist: Create it with current project assessment
If no clear next steps: Run /assess to evaluate project state
If blocked: Document blocker, move to next priority item
If focus area unclear: Ask user for clarification
</error_handling>

## Session Start Checklist

1. Read STATUS.md for context
2. Check KNOWN_ISSUES.md for blockers
3. Review recent SESSION_HISTORY.md entries
4. Identify focus area
5. Begin work
