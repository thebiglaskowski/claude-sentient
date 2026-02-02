---
name: undo-history
description: Track changes and enable easy rollback
model: sonnet
---

# Undo/History Tracking

Track changes and enable easy rollback.

## Description

Maintains history of changes made during session for easy undo/rollback.
Triggers on: "undo", "revert", "rollback", "go back", "what did we change", "history".

## What Gets Tracked

### File Changes
- Files created
- Files modified (with before/after)
- Files deleted (content preserved)
- Files renamed/moved

### Git Operations
- Commits made
- Branches created
- Merges performed

### Configuration Changes
- Settings modified
- Dependencies added/removed
- Environment changes

## History Structure

```markdown
## Session History

### Change #5 (latest) - 10:45 AM
**Action:** Edit file
**File:** src/utils/auth.ts
**Lines:** 45-52
**Before:**
```typescript
function validateToken(token) {
  return token.length > 0
}
```
**After:**
```typescript
function validateToken(token: string): boolean {
  if (!token) return false
  return verifyJWT(token)
}
```
**Undo:** `git checkout HEAD -- src/utils/auth.ts`

---

### Change #4 - 10:42 AM
**Action:** Create file
**File:** src/utils/jwt.ts
**Undo:** `rm src/utils/jwt.ts`

---

### Change #3 - 10:40 AM
**Action:** Git commit
**Message:** "Add JWT validation"
**SHA:** abc1234
**Undo:** `git reset --soft HEAD~1`

---

### Change #2 - 10:35 AM
**Action:** Install dependency
**Package:** jsonwebtoken@9.0.0
**Undo:** `npm uninstall jsonwebtoken`

---

### Change #1 - 10:30 AM
**Action:** Edit file
**File:** package.json
**Undo:** `git checkout HEAD -- package.json`
```

## Undo Commands

### Undo Last Change
```
"Undo the last change"
```
Reverts the most recent tracked change.

### Undo Specific Change
```
"Undo change #3"
```
Reverts a specific change by number.

### Undo All Session Changes
```
"Undo everything from this session"
```
Reverts all changes made in current session.

### Preview Undo
```
"What would undo do?"
```
Shows what would be reverted without doing it.

## Undo Strategies

### File Edits
```bash
# If file is git-tracked and not committed
git checkout HEAD -- <file>

# If committed
git show HEAD~1:<file> > <file>

# If not in git, use saved backup
cp .claude/history/backups/<file>.bak <file>
```

### File Creation
```bash
# Simply delete the file
rm <file>

# If committed, need to remove from git too
git rm <file>
git commit -m "Revert: remove <file>"
```

### File Deletion
```bash
# Restore from git
git checkout HEAD~1 -- <file>

# Or from backup
cp .claude/history/backups/<file>.bak <file>
```

### Git Commits
```bash
# Undo last commit, keep changes
git reset --soft HEAD~1

# Undo last commit, discard changes
git reset --hard HEAD~1

# Undo specific commit (creates new commit)
git revert <sha>
```

### Dependency Changes
```bash
# Undo npm install
npm uninstall <package>

# Undo npm uninstall
npm install <package>@<version>
```

## Backup System

### Automatic Backups
Before modifying any file, save backup:
```
.claude/history/backups/
├── src_utils_auth.ts.1705312345.bak
├── src_utils_auth.ts.1705312400.bak
└── package.json.1705312300.bak
```

### Backup Retention
- Keep last 10 versions per file
- Keep all backups from current session
- Clean up old backups weekly

### Backup Naming
```
{path_with_underscores}.{timestamp}.bak
```

## History Commands

### Show History
```
"Show change history"
"What have we changed?"
```

### Show File History
```
"Show history for src/utils/auth.ts"
```

### Compare Versions
```
"Compare current auth.ts with version from 10:30"
```

## Smart Undo

### Dependency Analysis
Before undoing, check for dependencies:
```markdown
⚠️ Warning: Undoing change #3 may break:
- Change #4 depends on jwt.ts created in #3
- Change #5 imports from jwt.ts

Options:
1. Undo #3, #4, and #5 together
2. Undo only #3 (may cause errors)
3. Cancel
```

### Conflict Detection
```markdown
⚠️ Warning: File has been modified since change #2

Current content differs from expected state.
Manual merge may be required.

Options:
1. Force revert (lose current changes)
2. Show diff and merge manually
3. Cancel
```

## Integration

### Session Start
Initialize history tracking:
```bash
mkdir -p .claude/history/backups
echo "# Session started $(date)" > .claude/history/session.log
```

### Before Each Change
1. Log the intended change
2. Backup affected files
3. Proceed with change
4. Log completion

### Session End
```markdown
## Session Summary

**Changes made:** 12
**Files modified:** 5
**Commits created:** 2
**Undo available:** Yes

History saved to .claude/history/
```

## Gitignore

Add to .gitignore:
```
.claude/history/
```

## Limitations

### Cannot Undo
- External system changes
- Database modifications (unless scripted)
- Deployed changes
- Third-party API calls

### Partial Undo
Some changes may require manual intervention:
- Complex refactors across multiple files
- Changes with external dependencies
- Merged git branches
