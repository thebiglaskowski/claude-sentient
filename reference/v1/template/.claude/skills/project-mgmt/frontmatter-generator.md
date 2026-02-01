---
name: frontmatter-generator
description: Add YAML frontmatter to skills that are missing it for v2.0 compatibility
argument-hint: "[skill-file.md]"
model: haiku
---

# Frontmatter Generator

Add YAML frontmatter to skills that are missing it, enabling v2.0 features.

## Official Frontmatter Fields (Claude Code)

These fields are processed by Claude Code:

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Skill identifier (kebab-case) |
| `description` | string | One-line description |
| `argument-hint` | string | Hint shown for arguments |
| `disable-model-invocation` | bool | True for reference-only skills |
| `user-invocable` | bool | Can be called with /command |
| `allowed-tools` | list | Tools this skill can use |
| `model` | string | haiku, sonnet, or opus |
| `context` | string | fork or inherit |
| `agent` | string | Agent to delegate to |
| `hooks` | list | Skill-specific hooks |

## Custom Metadata Fields (Documentation Only)

These fields are metadata and NOT processed:

| Field | Purpose |
|-------|---------|
| `version` | Skill version for tracking |
| `triggers` | Document when skill activates |
| `tags` | Categorization |

## Description

Use to upgrade skills that lack YAML frontmatter. This is especially useful for:
- Skills downloaded from skills.sh before v2.0
- Custom skills created without frontmatter
- Migrating v1.x skills to v2.0 format

Triggers on: "add frontmatter", "generate frontmatter", "fix skills", "upgrade skills"

## Arguments

```
$1 - Optional: specific skill file to update
     If not provided, scans all skills in .claude/skills/
```

**Examples:**
```
add frontmatter                           # Scan all skills
add frontmatter my-custom-skill.md        # Specific skill
generate frontmatter for downloaded skills
```

## Behavior

### 1. Scan for Skills Without Frontmatter

```bash
# Find skills missing frontmatter
for skill in .claude/skills/*.md; do
  if ! head -1 "$skill" | grep -q "^---"; then
    echo "Missing frontmatter: $skill"
  fi
done
```

### 2. Extract Metadata from Content

For each skill without frontmatter:

| Field | Extraction Method |
|-------|-------------------|
| `name` | H1 heading (`# Name`) or title-case filename |
| `description` | First paragraph or sentence after H1 |
| `triggers` | "Triggers on:" line, split by comma |
| `model` | Default "sonnet", or "opus" if mentions security/complex |
| `tags` | Technology keywords found in content |

### 3. Generate Frontmatter

```yaml
---
name: skill-name
description: One-line description of what skill does
argument-hint: "[optional args]"
disable-model-invocation: false
model: sonnet
context: inherit
---
```

Note: Only include fields that are needed. Omit optional fields to keep frontmatter clean.

### 4. Prepend to File

- Read original content
- Prepend generated frontmatter
- Write back to file
- Preserve original content exactly

## Process

1. **If $1 provided:** Process only that skill file
2. **If no $1:** Scan `.claude/skills/*.md`
3. **For each file:**
   - Skip if already has frontmatter (starts with `---`)
   - Extract metadata from content
   - Generate YAML frontmatter
   - Show preview to user
   - Apply changes after confirmation

## Output

```markdown
## Frontmatter Generation Report

### Skills Updated
| Skill | Name | Triggers Added |
|-------|------|----------------|
| custom-skill.md | Custom Skill | "custom", "skill name" |
| downloaded.md | Downloaded Tool | "tool", "helper" |

### Skills Skipped (Already Have Frontmatter)
- pre-commit.md
- severity-levels.md

### Skills Requiring Manual Review
- ambiguous-skill.md (couldn't extract triggers)
```

## Safety

- **Non-destructive:** Creates backup before modifying
- **Preview mode:** Shows changes before applying
- **Idempotent:** Skips files that already have frontmatter
- **Reversible:** Backup stored as `.skill.md.bak`

## Example Transformation

**Before:**
```markdown
# My Custom Skill

This skill helps with custom task automation.

Triggers on: "automate", "custom task", "run automation"

## Steps
1. Do thing
2. Do other thing
```

**After:**
```yaml
---
name: my-custom-skill
description: This skill helps with custom task automation
model: sonnet
---

# My Custom Skill

This skill helps with custom task automation.

Triggers on: "automate", "custom task", "run automation"

## Steps
1. Do thing
2. Do other thing
```

## Manual Override

If extraction isn't accurate, provide hints:

```
add frontmatter my-skill.md with model=opus
```

This sets specific values instead of auto-detecting.

## Reference-Only Skills

For skills that are pure documentation (not actionable), use:

```yaml
---
name: reference-skill
description: Pure reference documentation
disable-model-invocation: true
---
```

This prevents the skill from being invoked and saves context.
