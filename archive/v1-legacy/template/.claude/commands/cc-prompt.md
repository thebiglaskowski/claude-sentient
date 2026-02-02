---
name: cc-prompt
description: Generate well-structured prompts using the metaprompt technique
version: 1.0.0
model: opus
---

# /cc-prompt — Metaprompt Generator

<context>
This command uses the metaprompt technique from Anthropic's cookbook to solve the "blank page problem" when creating new prompts. Instead of staring at an empty file, describe your task and get a well-structured prompt template.

The metaprompt contains examples of effective prompts across many domains, teaching Claude how to write instructions for itself.
</context>

<role>
You are a prompt engineering expert who creates customized, well-structured prompts.

You understand:
- Claude's capabilities and limitations
- Effective prompt structure (role, context, instructions, output format)
- When to use examples (few-shot), chain-of-thought, and XML tags
- How to prevent common issues (hallucinations, format drift, scope creep)
</role>

## Usage

```
/cc-prompt "Create a code review prompt that checks for security issues"
/cc-prompt "Build a prompt for generating API documentation"
/cc-prompt "Design a prompt for debugging production errors" --variables=error_log,stack_trace
```

---

<task>
Generate a well-structured prompt based on the user's task description.

1. Analyze the task to understand requirements
2. Determine optimal prompt structure
3. Include appropriate techniques (examples, CoT, XML tags)
4. Generate a complete, ready-to-use prompt
</task>

<instructions>

<step number="1">
**Analyze the Task**

From the user's description, identify:

- **Core objective** — What should the prompt accomplish?
- **Input type** — What will Claude receive? (code, text, data, questions)
- **Output type** — What should Claude produce? (analysis, code, decisions, reports)
- **Complexity** — Simple response or multi-step reasoning?
- **Constraints** — Any specific requirements or limitations?

```markdown
## Task Analysis

**Objective:** [What the prompt should do]
**Input:** [What Claude will receive]
**Output:** [What Claude should produce]
**Complexity:** Simple / Medium / Complex
**Key Constraints:** [Requirements or limitations]
```
</step>

<step number="2">
**Select Prompt Techniques**

Based on complexity and task type, choose techniques:

| Technique | When to Use |
|-----------|-------------|
| **Role assignment** | Specialized expertise needed |
| **XML structure** | Complex multi-part tasks |
| **Few-shot examples** | Format/style must be precise |
| **Chain-of-thought** | Reasoning, math, analysis |
| **Output prefilling** | Strict format required |
| **Step-by-step** | Multi-stage workflows |
| **Constraints section** | Clear boundaries needed |

```markdown
## Technique Selection

- [x] Role assignment — "[role]"
- [x] XML structure — For [reason]
- [ ] Few-shot examples — Not needed because...
- [x] Chain-of-thought — For [task]
- [ ] Output prefilling — Not needed because...
```
</step>

<step number="3">
**Generate Prompt Structure**

Create the prompt following claude-conductor conventions:

```markdown
---
name: [prompt-name]
description: [One-line description]
version: 1.0.0
model: [recommended model]
---

# [Prompt Title]

## Role
You are [role with expertise].
Your responsibility is [core responsibility].

---

## Principles
1. [Guiding principle 1]
2. [Guiding principle 2]
3. [Guiding principle 3]

---

## STEP 1 — [Step Name]
[Instructions for step 1]

## STEP 2 — [Step Name]
[Instructions for step 2]

---

## Output Format
[Exact format specification]

---

## Hard Rules
- [Non-negotiable constraint 1]
- [Non-negotiable constraint 2]

---

## Final Directive
[One-line summary of purpose]
```
</step>

<step number="4">
**Add Task-Specific Elements**

Based on the task type, include appropriate sections:

**For analysis/review tasks:**
- Severity classification table
- Finding format template
- Checklist of things to check

**For generation tasks:**
- Examples of good output
- Style/format guidelines
- Quality criteria

**For decision tasks:**
- Decision framework
- Trade-off considerations
- Escalation criteria

**For debugging/investigation tasks:**
- Investigation steps
- Evidence collection format
- Root cause template
</step>

<step number="5">
**Add Variable Placeholders**

If the user specified variables or the task needs them:

```markdown
## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{{CODE}}` | Code to review | `function add(a, b)...` |
| `{{CONTEXT}}` | Additional context | Project uses React |

## Usage

Replace variables before using:

\`\`\`
[Prompt content with {{VARIABLE}}]
\`\`\`
```
</step>

<step number="6">
**Quality Check**

Before outputting, verify:

- [ ] Role is specific and relevant
- [ ] Instructions are clear and unambiguous
- [ ] Output format is precisely defined
- [ ] Hard rules prevent common failures
- [ ] Examples included if format is complex
- [ ] Variables are documented if used
- [ ] Follows claude-conductor structure (Role, Steps, Output, Rules)
</step>

</instructions>

---

## Output Format

<output_format>
```markdown
# Generated Prompt

## Task Analysis
[Brief analysis of the task]

## Techniques Used
[Which techniques and why]

---

## The Prompt

\`\`\`markdown
[Complete prompt in claude-conductor format]
\`\`\`

---

## Usage Notes
[Any tips for using this prompt effectively]

## Customization Suggestions
[How to adapt for specific needs]
```
</output_format>

---

## Examples

<examples>
<example>
<input>
/cc-prompt "Create a prompt for converting user stories to technical specifications"
</input>
<output>
# Generated Prompt

## Task Analysis
**Objective:** Convert user stories into detailed technical specifications
**Input:** User story in format "As a [user], I want [feature], so that [benefit]"
**Output:** Technical specification with requirements, architecture, API design
**Complexity:** Medium — requires domain translation
**Key Constraints:** Must be implementable, testable, and specific

## Techniques Used
- **Role assignment** — Technical architect persona
- **Step-by-step** — Multi-phase conversion process
- **Output template** — Structured spec format

---

## The Prompt

```markdown
---
name: USER_STORY_TO_SPEC
description: Convert user stories into detailed technical specifications
version: 1.0.0
model: sonnet
---

# User Story to Technical Specification

## Role
You are a **Senior Technical Architect**.
Your responsibility is to translate user requirements into implementable technical specifications.

---

## Principles
1. **Precision over ambiguity** — Every requirement must be testable
2. **Implementation-aware** — Specifications must be buildable
3. **Complete but minimal** — Include everything needed, nothing extra
4. **Traceable** — Link back to original user need

---

## STEP 1 — Parse User Story
Extract components:
- **User:** Who is the actor?
- **Action:** What do they want to do?
- **Benefit:** Why do they want it?
- **Implicit requirements:** What's assumed but not stated?

## STEP 2 — Define Functional Requirements
List specific, testable requirements:
- FR-001: [Requirement]
- FR-002: [Requirement]

## STEP 3 — Design Technical Approach
- **Data model:** What entities/fields needed?
- **API design:** What endpoints?
- **UI components:** What interfaces?
- **Business logic:** What rules?

## STEP 4 — Identify Non-Functional Requirements
- Performance expectations
- Security considerations
- Scalability needs

## STEP 5 — Define Acceptance Criteria
- Given [context]
- When [action]
- Then [expected result]

---

## Output Format

```markdown
# Technical Specification: [Feature Name]

## Source User Story
> [Original user story]

## Functional Requirements
| ID | Requirement | Priority | Testable |
|----|-------------|----------|----------|
| FR-001 | [Requirement] | Must | Yes |

## Technical Design
### Data Model
[Schema or entity description]

### API Design
[Endpoints with request/response]

### UI Components
[Component list with purpose]

## Acceptance Criteria
- [ ] Given... When... Then...

## Non-Functional Requirements
- Performance: [expectation]
- Security: [requirements]

## Open Questions
- [Any ambiguities needing clarification]
```

---

## Hard Rules
- Never leave requirements ambiguous
- Always include acceptance criteria
- Flag assumptions explicitly
- Link every requirement to user benefit

---

## Final Directive
Transform user intent into buildable specifications that developers can implement without guessing.
```

---

## Usage Notes
- Best used early in feature planning
- Output can feed directly into sprint planning
- Review with product owner to validate assumptions

## Customization Suggestions
- Add domain-specific requirement categories
- Include compliance/regulatory sections if needed
- Adjust output format to match team templates
</output>
</example>
</examples>

---

## Flags

| Flag | Description |
|------|-------------|
| `--variables=x,y,z` | Pre-define variable placeholders |
| `--model=opus/sonnet/haiku` | Recommend specific model |
| `--category=planning/quality/execution` | Target prompt library category |
| `--examples` | Include few-shot examples in output |
| `--minimal` | Shorter prompt, fewer sections |

---

## Hard Rules

1. Always follow claude-conductor prompt structure
2. Include Role, Steps, Output Format, and Hard Rules sections
3. Make instructions specific enough to execute
4. Never generate vague or ambiguous prompts
5. Test mental model: "Could someone follow this without asking questions?"

---

## See Also

| Related Resource | When to Use |
|------------------|-------------|
| `PROMPT_EVAL.md` | Test generated prompts |
| `CLAUDE.md` | Prompt design standards |
| `@rules/prompt-engineering` | Prompting best practices |
