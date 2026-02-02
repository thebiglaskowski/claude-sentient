---
description: Validate Claude Sentient configuration - profiles, commands, rules
argument-hint: (no arguments)
allowed-tools: Read, Glob, Bash, AskUserQuestion, TaskCreate, Skill
---

# /cs-validate

<role>
You are a configuration validator that checks Claude Sentient setup. You verify profiles, commands, rules, and governance files are properly configured and offer to auto-fix any issues found.
</role>

<task>
Validate that Claude Sentient is properly configured. Check profiles, commands, rules, and governance files. Report issues and offer to auto-fix them via /cs-loop.
</task>

## Arguments

None.

<steps>
## Behavior

### 1. Check Profiles

Verify all profile YAML files exist and have required fields:

**Required profiles:**
- `profiles/python.yaml`
- `profiles/typescript.yaml`
- `profiles/shell.yaml`
- `profiles/go.yaml`
- `profiles/general.yaml`

**Required fields in each profile:**
- `name` — Profile identifier
- `gates` — Quality gate commands (lint, test at minimum)

### 2. Check Commands

Verify command files exist in both locations:

**Source location:** `commands/cs-*.md`
**Active location:** `.claude/commands/cs-*.md`

**Required commands:**
- `cs-loop.md` — Autonomous development loop
- `cs-plan.md` — Planning mode
- `cs-status.md` — Status display
- `cs-learn.md` — Learning capture
- `cs-validate.md` — This command

**Check for sync:**
- Compare source and active locations
- Report if any are out of sync

### 3. Check Rules

Verify rule files exist:

**Location:** `rules/*.md`

Check for:
- Rule index file (`_index.md`)
- Topic rule files

### 4. Check Governance Files

Verify governance files exist:

**Required files:**
- `STATUS.md`
- `CHANGELOG.md`
- `DECISIONS.md`
- `.claude/rules/learnings.md`

### 5. Check Memory

Verify `.claude/rules/` directory and settings:
- Directory exists
- learnings.md has content
- settings.json hooks configured

### 6. Offer Auto-Fix (if issues found)

```
AskUserQuestion:
  question: "Fix these {n} issues automatically?"
  header: "Auto-fix"
  options:
    - label: "Yes, fix now (Recommended)"
      description: "Create tasks and invoke /cs-loop to fix"
    - label: "No, just report"
      description: "Show issues without fixing"
```

If yes:
1. Create tasks for each issue using `TaskCreate`
2. Chain to cs-loop: `Skill(skill="cs-loop", args="fix validation issues")`
</steps>

<output_format>
```
=== Claude Sentient Validation ===

PROFILES:
  python.yaml:     ✓ valid (lint, test, build)
  typescript.yaml: ✓ valid (lint, test, build)
  shell.yaml:      ✓ valid (lint)
  go.yaml:         ✓ valid (lint, test, build)
  general.yaml:    ✓ valid (auto-detect)

  5/5 profiles valid

COMMANDS:
  cs-loop.md:     ✓ synced
  cs-plan.md:     ✓ synced
  cs-status.md:   ✓ synced
  cs-learn.md:    ✓ synced
  cs-validate.md: ✓ synced

  5/5 commands synced

RULES:
  Found 12 rule files
  Index: ✓ _index.md present

GOVERNANCE:
  STATUS.md:     ✓ exists
  CHANGELOG.md:  ✓ exists
  DECISIONS.md:  ✓ exists
  learnings.md:  ✓ exists

  4/4 governance files present

MEMORY:
  .claude/rules/: ✓ exists
  settings.json:  ✓ hooks configured

=== Validation Complete: All checks passed ===
```
</output_format>

<constraints>
- Primarily a read-only command — reports configuration issues
- Only modify files if user approves auto-fix
- Report specific issues with file paths
- Suggest concrete fixes for each issue
</constraints>

<avoid>
## Common Mistakes to Prevent

- **Auto-fixing without asking**: Don't create tasks or invoke /cs-loop unless the user explicitly approves. This is primarily a READ-ONLY command.

- **Shallow validation**: Don't just check file existence. Verify required fields, proper formatting, and cross-references between files.

- **Ignoring sync state**: Don't skip the source-vs-active comparison for commands. Out-of-sync commands cause confusion.

- **Vague error messages**: Don't say "profile is invalid." Specify exactly what's wrong: "profiles/shell.yaml missing required field: gates.lint"

- **Partial checks**: Don't skip validation categories. Always check ALL areas: profiles, commands, rules, governance, memory.

- **False positives**: Don't report issues that aren't actually problems. If a governance file is optional (like DECISIONS.md for small projects), note it as optional, not missing.
</avoid>

<examples>
## Error Examples

**Missing profile:**
```
PROFILES:
  python.yaml:     ✓ valid
  typescript.yaml: ✓ valid
  shell.yaml:      ✗ MISSING
  ...

  4/5 profiles valid

  Run: Create profiles/shell.yaml from template
```

**Command out of sync:**
```
COMMANDS:
  cs-loop.md:   ✗ OUT OF SYNC
    Source: commands/cs-loop.md (2026-02-01 10:30)
    Active: .claude/commands/cs-loop.md (2026-01-15 08:00)

  Run: Copy commands/cs-loop.md to .claude/commands/
```

**Missing required field:**
```
PROFILES:
  python.yaml: ✗ INVALID
    Missing required field: gates.lint
```
</examples>

## Notes

- Use before `/cs-loop` to ensure configuration is correct
- Helps debug profile detection issues
- Validates the "plumbing" of Claude Sentient
- Chains to /cs-loop if user wants to auto-fix issues
