---
name: dry-run-mode
description: Preview changes before applying them
model: sonnet
---

# Dry-Run Mode

Preview changes before applying them.

## Description

Shows what would happen without actually making changes. Essential for destructive or large-scale operations.
Triggers on: "dry run", "preview", "what would happen", "show me first", "don't actually", "simulate".

## When to Use Dry-Run

### Always Dry-Run First
- Refactoring operations
- Bulk file changes
- Delete operations
- Database migrations
- Regex replacements
- Configuration changes

### Skip Dry-Run (Safe Operations)
- Reading files
- Running tests
- Linting (read-only)
- Status checks

## Dry-Run Patterns

### File Changes
```markdown
## Dry-Run: Rename Component

**Operation:** Rename `Button` to `PrimaryButton`

**Files affected:** 12

| File | Change |
|------|--------|
| src/components/Button.tsx | Rename to PrimaryButton.tsx |
| src/components/index.ts | Update export |
| src/pages/Home.tsx | Update import (line 3) |
| src/pages/Login.tsx | Update import (line 5) |
| src/pages/Dashboard.tsx | Update import (line 2, 8) |
| ... | ... |

**Preview of changes:**

`src/pages/Home.tsx`:
```diff
- import { Button } from '@/components'
+ import { PrimaryButton } from '@/components'
...
- <Button onClick={handleClick}>Submit</Button>
+ <PrimaryButton onClick={handleClick}>Submit</PrimaryButton>
```

**Apply these changes?** [Yes / No / Modify]
```

### Command Execution
```markdown
## Dry-Run: npm Scripts

**Command:** `npm run clean`

**Script definition:**
```json
"clean": "rm -rf dist node_modules/.cache"
```

**Would delete:**
- dist/ (245 files, 12MB)
- node_modules/.cache/ (1,203 files, 89MB)

**Side effects:**
- Next build will be slower (cache cleared)
- dist/ will need rebuild

**Proceed?** [Yes / No]
```

### Git Operations
```markdown
## Dry-Run: Git Rebase

**Command:** `git rebase main`

**Current branch:** feature/auth
**Commits to rebase:** 5

**Potential conflicts:**
- src/config.ts (modified in both branches)
- package.json (dependency changes)

**Commit replay order:**
1. abc1234 - Add auth middleware
2. def5678 - Add login endpoint
3. ghi9012 - Add logout endpoint
4. jkl3456 - Add tests
5. mno7890 - Update docs

**Proceed?** [Yes / No / Abort]
```

### Database Operations
```markdown
## Dry-Run: Migration

**Migration:** add_user_roles

**Changes:**
```sql
-- UP
ALTER TABLE users ADD COLUMN role VARCHAR(50) DEFAULT 'user';
CREATE INDEX idx_users_role ON users(role);

-- DOWN
DROP INDEX idx_users_role;
ALTER TABLE users DROP COLUMN role;
```

**Impact:**
- Table: users
- Rows affected: ~10,000
- Estimated time: <1 second
- Downtime required: No (online DDL)

**Proceed?** [Yes / No / Review SQL]
```

## Implementation

### Trigger Phrases
When user says any of these, engage dry-run mode:
- "What would happen if..."
- "Preview the changes"
- "Dry run this"
- "Don't actually do it yet"
- "Show me first"
- "Simulate"

### Dry-Run Response Format

```markdown
## Dry-Run: [Operation Name]

### Summary
[One-line description of what would happen]

### Details
[Specific files/items affected]

### Preview
[Show actual diffs or changes]

### Risks
[Any potential issues]

### Reversibility
[How to undo if needed]

---
**Apply these changes?**
- ✅ Yes - Proceed with changes
- ❌ No - Cancel operation
- 📝 Modify - Adjust scope/parameters
```

## Commands with Built-in Dry-Run

### /refactor
```markdown
/refactor always shows preview:
1. Analyzes target code
2. Shows proposed changes
3. Waits for approval
4. Only then applies changes
```

### /migrate
```markdown
/migrate always shows preview:
1. Parses migration files
2. Shows SQL to execute
3. Estimates impact
4. Waits for approval
```

## Forcing Dry-Run

User can force dry-run for any operation:
```
"Dry run: delete all .log files"
"Preview: update all imports"
"Simulate: merge feature branch"
```

## Dry-Run Checklist

Before applying changes from dry-run:

- [ ] Reviewed all affected files
- [ ] Understood the scope of changes
- [ ] Verified no unintended side effects
- [ ] Confirmed reversibility plan
- [ ] Ready to proceed

## Recovery from Bad Changes

If changes were applied without dry-run and went wrong:

### Git-tracked Files
```bash
# Undo all uncommitted changes
git checkout -- .

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1
```

### Non-Git Files
```bash
# Check for backups
ls *.bak *~

# Restore from backup if available
```

## Best Practice

```markdown
## Safe Change Workflow

1. **Dry-run** - Preview changes
2. **Review** - Verify scope and impact
3. **Backup** - Ensure reversibility
4. **Apply** - Make changes
5. **Verify** - Confirm success
6. **Commit** - Save to git (atomic, reversible)
```
