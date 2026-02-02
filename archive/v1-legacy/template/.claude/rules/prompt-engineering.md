# Prompt Engineering Rules

## Core Principles

1. **Clarity over cleverness** — Simple, direct instructions
2. **Structure aids understanding** — Use XML tags, sections
3. **Examples teach better than rules** — Show, don't just tell
4. **Give thinking space** — Let AI reason step-by-step
5. **Iterate and test** — Prompts need refinement

---

## Anthropic's Official Techniques

### Priority Order (Most to Least Impact)

1. **Be clear and direct** — Explicit instructions
2. **Use examples (few-shot)** — Show desired output
3. **Let Claude think (CoT)** — Step-by-step reasoning
4. **Use XML tags** — Structure data and instructions
5. **Give Claude a role** — System prompts for persona
6. **Prefill response** — Guide output format
7. **Chain complex prompts** — Break into steps

---

## Prompt Structure

### Basic Template

```xml
<context>
[Background information Claude needs]
</context>

<task>
[Clear description of what to do]
</task>

<format>
[Expected output structure]
</format>

<rules>
- [Constraint 1]
- [Constraint 2]
</rules>
```

### With Examples (Few-Shot)

```xml
<task>
Classify customer feedback as positive, negative, or neutral.
</task>

<examples>
<example>
<input>The product arrived quickly and works great!</input>
<output>positive</output>
</example>

<example>
<input>It's okay, nothing special.</input>
<output>neutral</output>
</example>

<example>
<input>Broken on arrival. Want refund.</input>
<output>negative</output>
</example>
</examples>

<input>
{{USER_FEEDBACK}}
</input>
```

---

## Chain of Thought

### When to Use

- Complex reasoning tasks
- Multi-step problems
- Math and logic
- Code generation

### Implementation

```xml
<task>
Analyze this code for security vulnerabilities.
</task>

<instructions>
Think through this step by step:
1. First, identify all user inputs
2. Then, trace how each input flows through the code
3. Check if inputs are validated/sanitized
4. Look for common vulnerability patterns
5. Finally, provide your findings
</instructions>

<code>
{{CODE}}
</code>
```

---

## Role Assignment

### System Prompt Pattern

```
You are a senior software engineer with 15 years of experience
in security-focused development. You specialize in identifying
vulnerabilities and writing secure code.

Your approach:
- Always assume inputs are malicious
- Follow OWASP guidelines
- Explain risks in business terms
- Provide actionable fixes

When reviewing code, you think like an attacker first,
then like a defender.
```

---

## Output Control

### Format Specification

```xml
<format>
Respond in this exact JSON format:
{
  "summary": "one sentence summary",
  "severity": "critical|high|medium|low",
  "findings": [
    {
      "issue": "description",
      "location": "file:line",
      "fix": "how to fix"
    }
  ]
}
</format>
```

### Prefilling Response

Start Claude's response to guide format:

```
Assistant: Here is my analysis:
```

---

## Prompt Chaining

### When to Use

- Complex multi-step tasks
- When one step's output feeds another
- To maintain accuracy across steps
- When context would be too long

### Pattern

```
Step 1: Extract requirements → Output: List
Step 2: Analyze each requirement → Output: Analysis
Step 3: Generate implementation → Output: Code
Step 4: Review and refine → Output: Final
```

---

## Reducing Hallucinations

### Techniques

1. **Allow uncertainty**
```
If you're not sure, say "I'm not certain" rather than guessing.
```

2. **Cite sources**
```
Only use information from the provided documents.
Quote the relevant section when making claims.
```

3. **Verify before answering**
```
Before answering, verify that:
1. The information is in the provided context
2. You're not making assumptions
3. Your answer directly addresses the question
```

---

## Common Anti-Patterns

### Avoid These

```
❌ Vague instructions
"Make it better"

✅ Specific instructions
"Reduce function length to under 20 lines by extracting
helper functions. Maintain the same behavior."
```

```
❌ Overloaded prompts
"Analyze, optimize, document, test, and deploy this code"

✅ Focused prompts
"Analyze this code for performance issues. List each issue
with its location and suggested fix."
```

```
❌ No examples
"Format the output correctly"

✅ With examples
"Format like this example:
- **Issue**: Description
- **Location**: file.js:42
- **Fix**: How to fix it"
```

---

## Prompt Optimization Checklist

### Before Using
- [ ] Task is clearly defined
- [ ] Context provided is sufficient
- [ ] Output format is specified
- [ ] Examples included (if complex)
- [ ] Constraints are explicit

### Testing
- [ ] Test with edge cases
- [ ] Verify output format consistency
- [ ] Check for hallucinations
- [ ] Measure against success criteria
- [ ] Iterate based on failures

---

## Resources

### Official Anthropic
- [Prompt Engineering Docs](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)
- [Interactive Tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial)

### Community
- [DAIR.AI Prompt Engineering Guide](https://www.promptingguide.ai/)
- [Learn Prompting](https://learnprompting.org/)
