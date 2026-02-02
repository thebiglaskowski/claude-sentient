---
description: Validate Claude Sentient configuration - profiles, commands, rules
argument-hint: (no arguments)
allowed-tools: Read, Glob, Bash, AskUserQuestion, TaskCreate, Skill
---

# /cs-validate

Validate that Claude Sentient is properly configured. Checks profiles, commands, rules, and governance files.

## Arguments

None.

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

**Output:**
```
PROFILES:
  python.yaml:     ✓ valid (lint, test, build)
  typescript.yaml: ✓ valid (lint, test, build)
  shell.yaml:      ✓ valid (lint)
  go.yaml:         ✓ valid (lint, test, build)
  general.yaml:    ✓ valid (auto-detect)
```

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

**Output:**
```
COMMANDS:
  cs-loop.md:     ✓ synced
  cs-plan.md:     ✓ synced
  cs-status.md:   ✓ synced
  cs-learn.md:    ✓ synced
  cs-validate.md: ✓ synced
```

### 3. Check Rules

Verify rule files exist:

**Location:** `rules/*.md`

**Output:**
```
RULES:
  Found 12 rule files
  Index: ✓ _index.md present
```

### 4. Check Governance Files

Verify governance files exist:

**Required files:**
- `STATUS.md`
- `CHANGELOG.md`
- `DECISIONS.md`
- `.claude/rules/learnings.md`

**Output:**
```
GOVERNANCE:
  STATUS.md:     ✓ exists
  CHANGELOG.md:  ✓ exists
  DECISIONS.md:  ✓ exists
  learnings.md:  ✓ exists
```

### 5. Check Memory

Verify `.claude/rules/` directory and settings:

**Output:**
```
MEMORY:
  .claude/rules/: ✓ exists
  learnings.md:   ✓ 3 decisions, 1 pattern
  settings.json:  ✓ hooks configured
```

## Full Output Example

```
=== Claude Sentient Validation ===

PROFILES:
  python.yaml:     ✓ valid (lint, test, type, build, format)
  typescript.yaml: ✓ valid (lint, test, type, build, format)
  shell.yaml:      ✓ valid (lint)
  go.yaml:         ✓ valid (lint, test, build, format)
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

## Auto-Fix with Skill Chaining

If validation finds issues, offer to fix them:

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
1. **Create tasks** for each issue using `TaskCreate`:
   - Missing profile → "Create {profile}.yaml from template"
   - Out of sync command → "Sync {command}.md to .claude/commands/"
   - Missing governance → "Create {file} from template"

2. **Chain to cs-loop**:
   ```
   Skill(skill="cs-loop", args="fix validation issues")
   ```

## Notes

- Primarily a read-only command — reports configuration issues
- Offers to auto-fix issues if found
- Use before `/cs-loop` to ensure configuration is correct
- Helps debug profile detection issues
- Validates the "plumbing" of Claude Sentient
