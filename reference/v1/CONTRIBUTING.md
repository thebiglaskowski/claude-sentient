# Contributing Guide

How to contribute to the Prompts Library.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Types of Contributions](#types-of-contributions)
3. [Adding New Prompts](#adding-new-prompts)
4. [Adding New Skills](#adding-new-skills)
5. [Adding New Commands](#adding-new-commands)
6. [Documentation](#documentation)
7. [Pull Request Process](#pull-request-process)
8. [Style Guide](#style-guide)

---

## Getting Started

### Prerequisites

- Git installed
- Understanding of Claude Code
- Familiarity with Markdown

### Setup

```bash
# Clone the repository
git clone git@github.com:your-org/prompts.git
cd prompts

# Create a branch for your changes
git checkout -b feature/my-contribution
```

---

## Types of Contributions

| Type | Location | Description |
|------|----------|-------------|
| **Prompts** | `prompts/[category]/` | Full prompt files |
| **Skills** | `template/.claude/skills/` | Auto-loading behaviors |
| **Commands** | `template/.claude/commands/` | Slash commands |
| **Documentation** | Various | Guides, references |
| **Bug Fixes** | Various | Fix existing issues |
| **Improvements** | Various | Enhance existing items |

---

## Adding New Prompts

### Step 1: Choose Category

| Category | For |
|----------|-----|
| `planning/` | Pre-implementation work |
| `execution/` | Active development |
| `quality/` | Testing, review, auditing |
| `documentation/` | Docs standards |
| `operations/` | Release, maintenance |
| `refactoring/` | Code improvement |

### Step 2: Create File

```bash
# Use UPPERCASE_SNAKE_CASE
touch prompts/quality/MY_NEW_PROMPT.md
```

### Step 3: Follow Template

```markdown
# Prompt Name

## Role

You are my **[Role Title]**.
Your responsibility is to [core responsibility].

---

## Principles

1. [Principle 1]
2. [Principle 2]
3. [Principle 3]

---

## STEP 1 — [Step Name]

[Instructions for step 1]

## STEP 2 — [Step Name]

[Instructions for step 2]

## STEP 3 — [Step Name]

[Instructions for step 3]

---

## Output Format

[What the output should look like]

---

## Hard Rules

- [Non-negotiable rule 1]
- [Non-negotiable rule 2]

---

## Final Directive

[One-line summary of purpose]
```

### Step 4: Add to README

Edit `README.md` to include your prompt in the appropriate table.

### Step 5: Test

Use the prompt in a real scenario to verify it works as intended.

---

## Adding New Skills

### Step 1: Create Skill File

```bash
# Use lowercase-kebab-case
touch template/.claude/skills/my-new-skill.md
```

### Step 2: Follow Template

```markdown
# Skill Name

Brief description of what this skill does.

## Description

Use when [context]. Triggers on: "keyword1", "keyword2", "keyword3".

## Trigger

Activates when:
- User mentions [trigger condition 1]
- User is about to [trigger condition 2]
- Context includes [trigger condition 3]

## Guidance

[Detailed guidance content]

### Section 1

[Content]

### Section 2

[Content]

## Examples

[Example usage]

## Related

- Related skill 1
- Related skill 2
```

### Step 3: Add to CLAUDE.md

Edit `template/.claude/CLAUDE.md` to include in skills table.

### Step 4: Test Triggers

Verify skill auto-loads when trigger words are used.

---

## Adding New Commands

### Step 1: Create Command File

```bash
# Use lowercase-kebab-case
touch template/.claude/commands/my-command.md
```

### Step 2: Follow Template

```markdown
# /my-command - Brief Description

## Model Recommendation
**Use: [Haiku|Sonnet|Opus]** — [Reason for model choice]

Load and execute: `C:\scripts\prompts\[category]/[PROMPT].md`

## Quick Start

[Brief description of what this does]

**Input needed:**
- [Required input 1]
- [Required input 2]

**Output:**
- [Output 1]
- [Output 2]

**Use when:**
- [Use case 1]
- [Use case 2]
```

### Step 3: Add to CLAUDE.md

Edit `template/.claude/CLAUDE.md` command reference table.

### Step 4: Add to Quick Reference

Edit `template/.claude/QUICK_REFERENCE.md`.

---

## Documentation

### Types of Documentation

| Document | Purpose | Location |
|----------|---------|----------|
| README.md | Main overview | Root |
| CHANGELOG.md | Version history | Root |
| CONTRIBUTING.md | This guide | Root |
| MCP_SERVERS.md | MCP setup | Template |
| CONFIGURATION.md | Config reference | Template |
| QUICK_REFERENCE.md | Cheat sheet | Template |
| TROUBLESHOOTING.md | Problem solving | Template |
| UPGRADE_GUIDE.md | Version migration | Template |
| EXAMPLES.md | Usage examples | Template |

### Documentation Style

- Use clear headings
- Include code examples
- Add tables for reference data
- Keep paragraphs short
- Use bullet points for lists

---

## Pull Request Process

### Step 1: Make Changes

```bash
# Create feature branch
git checkout -b feature/my-contribution

# Make your changes
# ...

# Commit with conventional format
git commit -m "feat: add new skill for X"
```

### Commit Message Format

```
type: description

[optional body]

[optional footer]
```

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance

### Step 2: Update Documentation

- Update README.md if adding prompt/skill/command
- Update CHANGELOG.md with your changes
- Update QUICK_REFERENCE.md if adding command

### Step 3: Test

- Test your prompt/skill/command works
- Verify documentation is accurate
- Check no existing functionality broke

### Step 4: Create PR

```bash
git push -u origin feature/my-contribution
```

Then create PR with:
- Clear title
- Description of changes
- Any testing done
- Screenshots if applicable

### Step 5: Review

- Address reviewer feedback
- Make requested changes
- Get approval

---

## Style Guide

### File Naming

| Type | Convention | Example |
|------|------------|---------|
| Prompts | UPPERCASE_SNAKE_CASE | `CODE_REVIEW.md` |
| Skills | lowercase-kebab-case | `pre-commit.md` |
| Commands | lowercase-kebab-case | `daily.md` |
| Docs | UPPERCASE or Title Case | `README.md`, `CHANGELOG.md` |

### Markdown Style

- Use ATX headings (`#`, `##`, `###`)
- Use fenced code blocks with language
- Use tables for structured data
- Use horizontal rules (`---`) to separate sections
- One sentence per line (for better diffs)

### Content Style

- Be concise but complete
- Use active voice
- Include examples
- Avoid jargon without explanation
- Test instructions before documenting

### Severity Levels

Always use standard severity levels:
- **S0** - Critical/Blocker
- **S1** - High/Major
- **S2** - Medium
- **S3** - Low/Minor

### Model Recommendations

Always include for commands:
- **Haiku** - Simple, mechanical tasks
- **Sonnet** - Standard development work
- **Opus** - Complex analysis, decisions

---

## Quality Checklist

Before submitting:

- [ ] File follows naming convention
- [ ] Content follows template structure
- [ ] Tested in real usage scenario
- [ ] Documentation updated (README, etc.)
- [ ] CHANGELOG.md entry added
- [ ] No sensitive information included
- [ ] Spell-check passed
- [ ] Links work correctly

---

## Questions?

If you're unsure about something:

1. Check existing prompts/skills for patterns
2. Review the style guide above
3. Ask in your PR description
4. Start a discussion issue

---

## Recognition

Contributors will be recognized in:
- CHANGELOG.md (for significant contributions)
- Git commit history

Thank you for contributing!
