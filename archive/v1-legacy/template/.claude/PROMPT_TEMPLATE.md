# Prompt Engineering Template

This template enforces best practices from Anthropic's official prompt engineering guidelines.

---

## Template Structure

Use this structure for all new prompts (commands, skills, rules):

```markdown
---
name: prompt-name
description: One-line description of what this does
version: 1.0.0
model: haiku|sonnet|opus
triggers:
  - "trigger phrase one"
  - "trigger phrase two"
tags: [category1, category2]
---

<context>
Background information Claude needs to understand the task.
Include relevant domain knowledge, constraints, and assumptions.
</context>

<role>
You are a [specific expert role] with expertise in [relevant domains].
Your approach emphasizes [key principles].
</role>

<task>
Clear description of what needs to be accomplished.
Be explicit about the goal and expected outcome.
</task>

<instructions>
<step number="1">
First action to take with specific details.
</step>

<step number="2">
Second action with clear expectations.
</step>

<step number="3">
Continue until task is complete.
</step>
</instructions>

<output_format>
Specify exactly how the output should be structured.

Example:
```
## Summary
[One paragraph overview]

## Findings
| Item | Severity | Details |
|------|----------|---------|
| ... | ... | ... |

## Recommendations
1. [First recommendation]
2. [Second recommendation]
```
</output_format>

<examples>
<example>
<input>
Example input or scenario
</input>
<thinking>
Step-by-step reasoning (optional, for complex tasks)
</thinking>
<output>
Expected output for this input
</output>
</example>

<example>
<input>
Another example with different conditions
</input>
<output>
Expected output showing variation
</output>
</example>
</examples>

<rules>
- Hard constraint that must never be violated
- Another non-negotiable requirement
- Safety or quality guardrail
</rules>

<error_handling>
If [error condition], then [recovery action].
If [ambiguity], then [clarification approach].
If [edge case], then [handling strategy].
</error_handling>
```

---

## Best Practices Checklist

Before finalizing any prompt, verify:

### Clarity (Most Important)
- [ ] Task is explicitly stated, not implied
- [ ] Success criteria are measurable
- [ ] Ambiguous terms are defined
- [ ] Scope boundaries are clear

### Structure
- [ ] Uses XML tags for distinct sections
- [ ] Instructions are numbered steps
- [ ] Output format is specified
- [ ] Role is defined (if helpful)

### Examples (High Impact)
- [ ] At least 2 examples for complex tasks
- [ ] Examples show input AND output
- [ ] Edge cases demonstrated
- [ ] Wrong approaches shown (optional)

### Reasoning
- [ ] Complex tasks include "think step by step"
- [ ] Chain of thought for multi-step logic
- [ ] Verification steps for critical decisions

### Error Handling
- [ ] Unclear input → ask for clarification
- [ ] Ambiguous requirements → show options
- [ ] Failures → graceful degradation

---

## XML Tag Reference

### Structural Tags

| Tag | Purpose | When to Use |
|-----|---------|-------------|
| `<context>` | Background information | Always |
| `<role>` | Expert persona | When expertise matters |
| `<task>` | Main objective | Always |
| `<instructions>` | Step-by-step process | Multi-step tasks |
| `<step>` | Individual instruction | Inside instructions |
| `<output_format>` | Expected structure | When format matters |
| `<examples>` | Input/output pairs | Complex or ambiguous tasks |
| `<rules>` | Hard constraints | Safety/quality critical |

### Content Tags

| Tag | Purpose | When to Use |
|-----|---------|-------------|
| `<input>` | Example input | Inside examples |
| `<output>` | Example output | Inside examples |
| `<thinking>` | Reasoning process | Chain of thought |
| `<error_handling>` | Recovery strategies | Production prompts |

### Data Tags

| Tag | Purpose | When to Use |
|-----|---------|-------------|
| `<code>` | Code blocks | Code review/generation |
| `<document>` | Long text input | Document analysis |
| `<data>` | Structured data | Data processing |

---

## Few-Shot Example Patterns

### Classification Task
```xml
<examples>
<example>
<input>The application crashes when clicking submit</input>
<output>
Severity: S0 (Critical)
Category: Functionality
Reason: Complete feature failure blocking user workflow
</output>
</example>

<example>
<input>The button color doesn't match the design</input>
<output>
Severity: S3 (Low)
Category: Visual Polish
Reason: Cosmetic issue with no functional impact
</output>
</example>

<example>
<input>API response is slow under heavy load</input>
<output>
Severity: S2 (Medium)
Category: Performance
Reason: Degraded experience but functional
</output>
</example>
</examples>
```

### Generation Task
```xml
<examples>
<example>
<input>Function: calculateTotal(items, taxRate)</input>
<output>
/**
 * Calculates the total price including tax.
 *
 * @param items - Array of items with price and quantity
 * @param taxRate - Tax rate as decimal (e.g., 0.1 for 10%)
 * @returns Total price in cents
 * @throws {InvalidTaxRateError} If tax rate is negative
 *
 * @example
 * calculateTotal([{price: 100, qty: 2}], 0.1) // Returns 220
 */
</output>
</example>
</examples>
```

### Analysis Task
```xml
<examples>
<example>
<input>
const query = `SELECT * FROM users WHERE id = ${userId}`;
</input>
<thinking>
1. This is a SQL query construction
2. User input (userId) is directly interpolated
3. No sanitization or parameterization
4. This is a SQL injection vulnerability
</thinking>
<output>
**S0 - Critical Security Issue**

SQL Injection vulnerability detected.

Location: String interpolation in SQL query
Risk: Full database compromise
Fix: Use parameterized queries

```javascript
// Before (vulnerable)
const query = `SELECT * FROM users WHERE id = ${userId}`;

// After (safe)
const query = 'SELECT * FROM users WHERE id = $1';
const result = await db.query(query, [userId]);
```
</output>
</example>
</examples>
```

---

## Chain of Thought Patterns

### For Analysis Tasks
```xml
<instructions>
Before providing your analysis, think through:

<step number="1">
What is the primary purpose of this code/document/system?
</step>

<step number="2">
What patterns or anti-patterns are present?
</step>

<step number="3">
What could go wrong? What are the edge cases?
</step>

<step number="4">
What would improve this? Prioritize by impact.
</step>

Then provide your structured analysis.
</instructions>
```

### For Decision Tasks
```xml
<instructions>
When making this decision:

<step number="1">
List all available options.
</step>

<step number="2">
For each option, identify:
- Pros (benefits, advantages)
- Cons (costs, risks, downsides)
- Trade-offs (what you gain vs. lose)
</step>

<step number="3">
Consider the specific context and constraints.
</step>

<step number="4">
Make a recommendation with clear reasoning.
</step>
</instructions>
```

### For Verification Tasks
```xml
<instructions>
Before confirming completion:

<step number="1">
Re-read the original requirements.
</step>

<step number="2">
Check each requirement against the implementation.
</step>

<step number="3">
Identify any gaps or assumptions made.
</step>

<step number="4">
Verify edge cases are handled.
</step>

<step number="5">
Confirm with explicit pass/fail for each criterion.
</step>
</instructions>
```

---

## Anti-Patterns to Avoid

### Vague Instructions
```xml
<!-- BAD -->
<task>Review the code and make it better.</task>

<!-- GOOD -->
<task>
Review the code for:
1. Security vulnerabilities (OWASP Top 10)
2. Performance issues (N+1 queries, memory leaks)
3. Code quality (complexity, naming, duplication)

For each issue found, provide:
- Severity (S0-S3)
- Location (file:line)
- Description of the problem
- Recommended fix with code example
</task>
```

### Missing Output Format
```xml
<!-- BAD -->
<task>Analyze the database schema.</task>

<!-- GOOD -->
<task>Analyze the database schema.</task>

<output_format>
## Schema Analysis

### Tables Reviewed
| Table | Columns | Indexes | Issues |
|-------|---------|---------|--------|

### Findings by Severity
#### S0 - Critical
[Finding with details]

#### S1 - High
[Finding with details]

### Recommendations
1. [Prioritized recommendation]
</output_format>
```

### No Examples for Ambiguous Tasks
```xml
<!-- BAD -->
<task>Classify the issues by priority.</task>

<!-- GOOD -->
<task>Classify the issues by priority.</task>

<examples>
<example>
<input>Users can't log in</input>
<output>P0 - Critical: Blocks all user access</output>
</example>
<example>
<input>Typo in footer</input>
<output>P3 - Low: Cosmetic, no user impact</output>
</example>
</examples>
```

---

## Validation Checklist

Run through this before deploying any prompt:

### Structure
- [ ] Has YAML frontmatter with required fields
- [ ] Uses XML tags for major sections
- [ ] Instructions are numbered steps
- [ ] Output format is explicit

### Content
- [ ] Task is unambiguous
- [ ] Role is appropriate (if used)
- [ ] Examples cover common cases
- [ ] Edge cases addressed
- [ ] Error handling defined

### Quality
- [ ] Tested with real inputs
- [ ] Output format verified
- [ ] No hallucination triggers
- [ ] Appropriate model selected
- [ ] Token efficient (not overly verbose)

---

## Converting Existing Prompts

When upgrading old prompts to this template:

1. **Extract the task** → Put in `<task>` tags
2. **Identify steps** → Convert to numbered `<step>` tags
3. **Find implicit rules** → Make explicit in `<rules>`
4. **Add examples** → At least 2 input/output pairs
5. **Define output** → Create `<output_format>` section
6. **Add frontmatter** → Name, description, triggers, model

### Before
```markdown
# Code Review

Review the code for bugs and issues.
Check for security problems.
Make sure tests are adequate.
Report findings.
```

### After
```markdown
---
name: code-review
description: Comprehensive code review with severity-rated findings
model: sonnet
triggers: ["review", "code review", "check this code"]
---

<role>
You are a senior software engineer conducting a thorough code review.
You prioritize security, correctness, and maintainability.
</role>

<task>
Review the provided code for issues in these categories:
1. Security vulnerabilities
2. Bugs and logic errors
3. Performance problems
4. Code quality issues
5. Test coverage gaps
</task>

<instructions>
<step number="1">
Read through all the code to understand its purpose and flow.
</step>

<step number="2">
Check for security issues (injection, auth, secrets, etc.)
</step>

<step number="3">
Look for bugs, edge cases, and error handling gaps.
</step>

<step number="4">
Identify performance concerns and optimization opportunities.
</step>

<step number="5">
Assess code quality (naming, complexity, duplication).
</step>

<step number="6">
Review test coverage and test quality.
</step>
</instructions>

<output_format>
## Code Review Summary

**Files Reviewed:** [count]
**Issues Found:** [count by severity]

### S0 - Critical
[Issue with location, description, and fix]

### S1 - High
[Issue with location, description, and fix]

### S2 - Medium
[Issue with location, description, and fix]

### S3 - Low
[Issue with location, description, and fix]

### Positive Observations
[What's done well]

### Recommendations
[Prioritized action items]
</output_format>

<examples>
<example>
<input>
const query = `SELECT * FROM users WHERE id = ${userId}`;
</input>
<output>
### S0 - Critical

**SQL Injection Vulnerability**
- Location: line 1
- Description: User input directly interpolated into SQL query
- Impact: Full database compromise possible
- Fix: Use parameterized queries
```javascript
const query = 'SELECT * FROM users WHERE id = $1';
await db.query(query, [userId]);
```
</output>
</example>
</examples>

<rules>
- Never approve code with S0 issues
- Always provide fix suggestions, not just problems
- Be specific about locations (file:line)
- Prioritize security over style issues
</rules>
```
