---
name: requirements-clarifier
description: Force clarifying questions before major work to reduce errors and rework
model: sonnet
version: 1.0.0
tags: [orchestration, planning, requirements]
---

# Requirements Clarifier

Before executing major work, systematically gather requirements through targeted questions.

## Description

This skill implements **Reverse Prompting** - instead of jumping into execution, the AI asks clarifying questions first. Research shows this reduces hallucinations by 40% and prevents costly rework.

Triggers on: "implement", "build", "create", "add feature", "new functionality", start of `/cc-plan`, `/cc-loop` with complex tasks

---

## When to Activate

### Always Clarify Before

| Task Type | Why |
|-----------|-----|
| New features | Requirements often ambiguous |
| Architectural changes | High impact, hard to reverse |
| Security implementations | Must understand threat model |
| Data migrations | Risk of data loss |
| API design | Affects all consumers |
| Complex bug fixes | Need to understand expected behavior |

### Skip Clarification For

- Simple typo fixes
- Explicit, detailed instructions already provided
- Follow-up work where context is established
- Emergency hotfixes (but note assumptions)

---

## Question Framework

### The 5 Essential Questions

Before major work, ask questions in these categories:

```markdown
## Before I Begin

I want to make sure I understand your requirements correctly. Please answer these questions:

### 1. Scope & Boundaries
- What exactly should be included?
- What should explicitly NOT be included?
- Are there related areas I should avoid touching?

### 2. Context & Constraints
- What existing patterns should I follow?
- Are there performance/security requirements?
- What's the timeline pressure (thorough vs. quick)?

### 3. Success Criteria
- How will we know this is complete?
- What does "working" look like?
- Are there specific test cases to satisfy?

### 4. Edge Cases
- What happens when [likely edge case]?
- Should I handle [error scenario]?
- What's the fallback behavior?

### 5. Dependencies & Integration
- What other systems/components does this touch?
- Who else needs to know about this change?
- Are there downstream consumers to consider?
```

---

## Examples

### Example 1: Feature Request

**User says:** "Add user authentication"

**Before (risky):**
```
I'll implement JWT-based authentication with login/logout endpoints...
[proceeds to build something that may not match expectations]
```

**After (with clarifier):**
```markdown
## Before I Implement Authentication

I want to build exactly what you need. A few questions:

### Scope
1. Which authentication methods? (email/password, OAuth, SSO, MFA?)
2. Should I include password reset and email verification?
3. Any admin/role-based access needed?

### Technical Constraints
4. Do you have a preferred JWT library or session approach?
5. Any existing user table I should integrate with?

### Security Requirements
6. What's the session timeout policy?
7. Should I implement rate limiting on auth endpoints?

Once you answer these, I'll create a detailed plan before writing any code.
```

### Example 2: Bug Fix

**User says:** "Fix the checkout bug"

**Before (risky):**
```
I see an error in checkout.js, let me fix it...
[fixes wrong bug or introduces new issues]
```

**After (with clarifier):**
```markdown
## Before I Fix the Checkout Bug

To fix this correctly, I need to understand:

1. **Symptoms**: What exactly happens? Error message? Wrong behavior?
2. **Reproduction**: What steps trigger this? Specific products/users?
3. **Expected**: What should happen instead?
4. **Scope**: Should I only fix this specific issue, or related issues too?
5. **Urgency**: Quick patch or proper fix with tests?

This helps me find the root cause rather than just treating symptoms.
```

---

## Integration with Loop

When `/cc-loop` receives a complex task:

```
Phase 0: CLARIFY (NEW)
├── Detect task complexity
├── Generate targeted questions
├── Wait for answers
├── Confirm understanding
└── Then proceed to Phase 1: ASSESS
```

---

## Question Templates by Task Type

### New Feature
```
1. What problem does this solve for users?
2. Are there existing features this should integrate with?
3. What's the MVP vs. nice-to-have?
4. Any designs/mockups to reference?
5. Who are the primary users of this feature?
```

### Refactoring
```
1. What's the main goal? (Performance? Readability? Testability?)
2. What should definitely NOT change?
3. Are there tests covering current behavior?
4. Is incremental refactoring OK or big-bang required?
5. Any deadline or can we take time to do it right?
```

### Bug Fix
```
1. What's the exact error/behavior observed?
2. Steps to reproduce?
3. When did this start happening?
4. What's the expected correct behavior?
5. Are there related bugs or just this one?
```

### Security Implementation
```
1. What's the threat model? (Who are we protecting against?)
2. What data needs protection?
3. Any compliance requirements? (SOC2, HIPAA, GDPR?)
4. Existing security infrastructure to integrate with?
5. What's the authentication/authorization model?
```

---

## Configuration

### Enable/Disable

In settings or conversation:
```
# Always clarify
"Always ask clarifying questions before major work"

# Skip this time
"Skip questions, here are the details: [comprehensive spec]"

# Disable
"Don't ask questions, just proceed"
```

### Sensitivity Levels

| Level | Behavior |
|-------|----------|
| `strict` | Always clarify, even simple tasks |
| `standard` | Clarify complex tasks (default) |
| `minimal` | Only clarify ambiguous requests |
| `off` | Never clarify, proceed immediately |

---

## Best Practices

### Do
- Ask 3-5 focused questions (not 20)
- Make questions specific to the task
- Offer reasonable defaults when asking
- Group related questions together
- Acknowledge when you have enough info

### Don't
- Ask obvious questions with clear answers
- Delay urgent work with excessive questions
- Ask the same questions repeatedly
- Require answers to proceed on simple tasks

---

## Output Format

When clarifying:

```markdown
## Quick Questions Before I Start

I'll implement [brief understanding]. To make sure I get it right:

1. **[Category]**: [Specific question]?
   - Default assumption: [what you'll do if no answer]

2. **[Category]**: [Specific question]?
   - Default assumption: [what you'll do if no answer]

3. **[Category]**: [Specific question]?
   - Default assumption: [what you'll do if no answer]

Feel free to answer any/all, or say "proceed with defaults" if my assumptions look good.
```
