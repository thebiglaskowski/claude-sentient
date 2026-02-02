---
name: auto-update-checker
description: Check for updates to the prompts library
model: haiku
---

# Auto-Update Checker

Check for updates to the prompts library.

## Description

Use to check if the prompts library has updates available.
Triggers on: "check for updates", "update prompts", "is this up to date", "session start".

## How It Works

The prompts library is stored in a git repository. This skill checks if there are newer commits available.

## Check Process

### Step 1: Check Prompts Library Status

```bash
# Navigate to prompts library
cd C:\scripts\prompts

# Fetch latest without merging
git fetch origin main --quiet

# Compare local vs remote
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)

if [ "$LOCAL" = "$REMOTE" ]; then
  echo "✅ Prompts library is up to date"
else
  echo "⚠️ Updates available for prompts library"
  git log --oneline HEAD..origin/main
fi
```

### Step 2: Check Template Version

Compare project's `.claude/` folder against template:

```bash
# Get template version (if tracked)
TEMPLATE_VERSION=$(cat .claude/.version 2>/dev/null || echo "unknown")
LATEST_VERSION=$(cat C:\scripts\prompts\template\.claude\.version 2>/dev/null || echo "unknown")

echo "Project template: $TEMPLATE_VERSION"
echo "Latest template: $LATEST_VERSION"
```

### Step 3: Report

```markdown
## Update Check

### Prompts Library
**Status:** ⚠️ Updates Available
**Local:** abc1234
**Remote:** def5678

**New commits:**
- def5678 Add automatic .gitignore management
- 789abcd Add model routing optimization

**To update:**
```bash
cd C:\scripts\prompts && git pull
```

### Project Template
**Status:** ✅ Up to date
**Version:** 1.0.0

### Recommendations
- Pull latest prompts library for new features
- Re-run `/scout-skills` after updating to get new skills
```

## Update Process

If updates are available and user wants to update:

### Update Prompts Library
```bash
cd C:\scripts\prompts
git pull origin main
```

### Update Project Template
For existing projects, selectively update:

1. **Safe to update** (won't overwrite customizations):
   - `.claude/commands/` - Add new commands
   - `.claude/skills/` - Add new skills

2. **Review before updating**:
   - `.claude/CLAUDE.md` - May have project customizations
   - `.claude/settings.json` - May have custom hooks

```bash
# Copy new commands (won't overwrite existing)
cp -n C:\scripts\prompts\template\.claude\commands\* .claude\commands\

# Copy new skills (won't overwrite existing)
cp -n C:\scripts\prompts\template\.claude\skills\* .claude\skills\
```

## Version Tracking

### Template Version File
`.claude/.version`:
```
1.0.0
```

Update this when making significant template changes.

### Changelog Integration
Check CHANGELOG.md in prompts library for what's new:
```bash
head -50 C:\scripts\prompts\CHANGELOG.md
```

## Session Start Integration

Optionally check for updates at session start (non-blocking):

```json
{
  "SessionStart": [{
    "hooks": [{
      "type": "command",
      "command": "cd $PROMPTS_PATH && git fetch -q && [ $(git rev-parse HEAD) != $(git rev-parse origin/main) ] && echo '[INFO] Prompts library updates available - run update check'"
    }]
  }]
}
```

## Manual Check Command

User can ask:
- "Check for updates"
- "Is the prompts library up to date?"
- "Are there new prompts available?"

## Update Frequency

Recommended check frequency:
- **Automatic:** Once per session (lightweight fetch)
- **Manual:** When starting new features or hitting issues
- **After updates:** Re-run `/scout-skills` to get new skills
