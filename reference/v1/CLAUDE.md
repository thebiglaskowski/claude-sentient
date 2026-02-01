# CLAUDE.md — Prompts Library Guidelines

## Purpose

This folder contains reusable prompts for software project work. Each prompt is designed to be:

- **Generic** — Works on any project (except tool-specific)
- **Self-contained** — Includes all instructions needed
- **Structured** — Step-by-step with clear outputs
- **Quality-focused** — Emphasizes correctness over speed

---

## Folder Organization

```
claude-conductor/
├── planning/           # Before building: blueprints, specs
├── execution/          # During building: implementation, research
├── quality/            # Verification: reviews, audits, testing
├── documentation/      # Docs: policies, templates, guides
├── operations/         # Post-build: releases, incidents, debt
├── refactoring/        # Code improvement
├── skills/             # Claude Code automatic behaviors
├── tool-specific/      # Tool-specific (e.g., Notion)
├── template/           # Project template reference files
├── archive/            # Deprecated prompts (per deprecation policy)
├── assets/             # Images, logos, and other assets
└── .claude/            # Claude Code configuration
```

---

## Prompt Design Standards

### File Naming

- Use `UPPERCASE_SNAKE_CASE.md`
- Name should describe the action (e.g., `CODE_REVIEW.md`, not `reviewer.md`)
- Skills use `lowercase-kebab.md`

### Structure

Every prompt should include:

1. **Role** — Who the AI is acting as
2. **Principles** — Guiding rules
3. **Steps** — Numbered, sequential process (STEP 1, STEP 2, etc.)
4. **Output Format** — What to produce
5. **Hard Rules** — Non-negotiable constraints
6. **Final Directive** — Summary of purpose

Note: Documentation files (policies, checklists, templates) may use a lighter structure appropriate to their reference nature.

### Example Structure

```markdown
# [Prompt Name]

## Role
You are my **[Role Title]**.
Your responsibility is to [core responsibility].

---

## Principles
1. [Principle 1]
2. [Principle 2]

---

## STEP 1 — [Step Name]
[Instructions]

## STEP 2 — [Step Name]
[Instructions]

---

## Output Format
[What the output should look like]

---

## Hard Rules
- [Rule 1]
- [Rule 2]

---

## Final Directive
[One-line summary of purpose]
```


---

## Usage Patterns

### Pattern 1: Direct System Prompt

Use the prompt as a system prompt for a conversation:

```
System: [Paste prompt content]
User: Here's my project...
```

### Pattern 2: Task Instruction

Reference the prompt when assigning work:

```
Follow the CODE_REVIEW prompt to review this PR...
```

### Pattern 3: Claude Code Skill

Skills in `skills/` are designed for Claude Code's skill system:

```yaml
# .claude/skills/project-hygiene.md
[Skill content]
```

### Pattern 4: Chained Prompts

Use multiple prompts in sequence:

1. FEATURE_SPEC_WRITER → Create spec
2. BLUEPRINT_AUDITOR → Validate plan
3. PROJECT_EXECUTION → Build it
4. CODE_REVIEW → Review changes
5. TEST_COVERAGE_GATE → Verify tests
6. RELEASE_CHECKLIST → Ship it

---

## Severity Levels

All quality prompts use consistent severity levels:

| Level | Meaning | Action |
|-------|---------|--------|
| **S0 / Critical** | Blocker, security, data loss | Fix immediately |
| **S1 / High** | Major functionality broken | Fix before proceeding |
| **S2 / Medium** | Degraded but functional | Fix soon |
| **S3 / Low** | Minor, polish | Fix when convenient |

---

## Common Output Artifacts

### Update Bundle

Many prompts produce an "Update Bundle" with:

- STATUS.md updates
- CHANGELOG.md entry
- Documentation updates
- KNOWN_ISSUES.md entries

### Traceability Matrix

Audit prompts produce traceability matrices:

| Requirement | Implementation | Validation | Documentation |
|-------------|----------------|------------|---------------|
| [Req] | [Evidence] | [Test] | [Doc] |

### Findings Report

Quality prompts produce findings by severity:

```markdown
### S0 — Critical
[Finding with evidence, impact, remediation]

### S1 — High
[Finding with evidence, impact, remediation]
```

---

## Key Principles Across All Prompts

### 1. Evidence-Based

Never assume. Always verify. Require proof.

### 2. Smallest Safe Change

Prefer minimal changes over large rewrites.

### 3. Test First

Don't change code without tests to verify behavior.

### 4. Documentation is Required

Changes aren't complete until documented.

### 5. Reversibility

Every action should be reversible where possible.

### 6. No Guessing

When uncertain, stop and ask. Don't proceed with assumptions.

---

## Integration with Project Work

### With CLAUDE.md (Project-Level)

Project CLAUDE.md files define project-specific standards. These prompts are generic — project CLAUDE.md takes precedence for:

- Coding standards
- Naming conventions
- Architecture patterns
- Technology choices

### With Blueprints

Blueprints define WHAT to build. These prompts define HOW to work:

- Blueprint: "Build a user authentication system"
- Prompt: "Here's how to execute that work safely"

### With Status Tracking

Execution prompts expect these files to exist:

- `STATUS.md` — Current project state
- `CHANGELOG.md` — Version history
- `KNOWN_ISSUES.md` — Known limitations

---

## Adding New Prompts

### Checklist

- [ ] Placed in correct category folder
- [ ] Follows naming convention
- [ ] Includes all required sections (Role, Steps, Output, Rules)
- [ ] Tested on real work
- [ ] Added to README.md index
- [ ] Generic (no project-specific content)

### Categories

| If the prompt is for... | Put it in... |
|-------------------------|--------------|
| Before building starts | `planning/` |
| Active development | `execution/` |
| Checking quality | `quality/` |
| Creating docs | `documentation/` |
| After release | `operations/` |
| Improving code | `refactoring/` |
| Automatic behavior | `skills/` |
| Specific tool | `tool-specific/[tool]/` |

---

## Maintenance

### Review Cadence

- **Quarterly**: Review all prompts for relevance
- **After use**: Update based on real-world feedback
- **On failure**: If a prompt leads to bad outcomes, fix it

### Deprecation

When retiring a prompt:

1. Move to `archive/` folder
2. Add deprecation notice at top
3. Update README.md
4. Note replacement (if any)

---

## Philosophy

These prompts encode hard-won lessons about software quality:

- **Planning prevents rework** — Audit before building
- **Small steps are safer** — Incremental over big-bang
- **Tests enable change** — Can't refactor without tests
- **Documentation is memory** — What's not written is forgotten
- **Debt compounds** — Track and pay it down
- **Incidents teach** — Learn from every failure

Use these prompts to build software that works, is maintainable, and improves over time.
