---
name: file-watcher
description: Monitor files for changes and trigger appropriate actions
model: sonnet
---

# Smart File Watching

React to file changes automatically.

## Description

Monitor files for changes and trigger appropriate actions automatically.
Triggers on: "watch files", "auto-run", "on change", "file changed", "live reload".

## Watch Configurations

### Default Watchers

| File Pattern | Action | Description |
|--------------|--------|-------------|
| `*.test.ts` | Run test | Re-run test when test file changes |
| `src/**/*.ts` | Type check | Run tsc on source changes |
| `package.json` | Notify | Alert about dependency changes |
| `.env*` | Warn | Security reminder for env changes |
| `*.md` | Lint | Check markdown formatting |
| `schema.prisma` | Generate | Run prisma generate |

### Watch Configuration File

`.claude/watch.json`:
```json
{
  "watchers": [
    {
      "name": "tests",
      "pattern": "**/*.test.{ts,tsx}",
      "action": "npm test -- --findRelatedTests ${file}",
      "debounce": 500
    },
    {
      "name": "typecheck",
      "pattern": "src/**/*.{ts,tsx}",
      "action": "npx tsc --noEmit",
      "debounce": 1000
    },
    {
      "name": "lint",
      "pattern": "src/**/*.{ts,tsx,js,jsx}",
      "action": "npx eslint ${file} --fix",
      "debounce": 300
    },
    {
      "name": "prisma",
      "pattern": "prisma/schema.prisma",
      "action": "npx prisma generate",
      "debounce": 1000
    },
    {
      "name": "env-warning",
      "pattern": ".env*",
      "action": "echo '⚠️ Environment file changed - verify not committing secrets'",
      "debounce": 0
    }
  ]
}
```

## Watcher Actions

### Run Tests
```markdown
## Auto-Test on Change

**Trigger:** `src/utils/auth.ts` modified
**Action:** Run related tests

```bash
npm test -- --findRelatedTests src/utils/auth.ts
```

**Result:**
✅ auth.test.ts: 5 passed
✅ login.test.ts: 3 passed
```

### Type Check
```markdown
## Auto-TypeCheck

**Trigger:** TypeScript file modified
**Action:** Run compiler check

```bash
npx tsc --noEmit
```

**Result:**
✅ No type errors
```

### Format
```markdown
## Auto-Format

**Trigger:** Source file saved
**Action:** Run Prettier

```bash
npx prettier --write src/utils/auth.ts
```

**Result:**
✅ Formatted
```

### Custom Actions
```markdown
## Custom Watcher

**Trigger:** Schema file changed
**Action:** Regenerate types

```bash
npx prisma generate
npx prisma-json-types-generator
```

**Result:**
✅ Types regenerated
```

## Smart Detection

### Related File Detection
When a file changes, identify related files:

```markdown
**File changed:** src/services/userService.ts

**Related files detected:**
- src/services/userService.test.ts (test)
- src/controllers/userController.ts (imports this)
- src/routes/users.ts (uses controller)
- src/types/user.ts (shared types)

**Auto-actions:**
1. Run userService.test.ts
2. Type-check dependent files
```

### Change Impact Analysis
```markdown
**Change:** Modified `src/lib/db.ts`

**Impact Analysis:**
- 🔴 High impact: Core database module
- 📁 15 files depend on this
- 🧪 42 tests may be affected

**Recommended actions:**
1. Run full test suite (not just related)
2. Manual review of dependent files
```

## Notification Modes

### Inline (Default)
Show results in terminal:
```
[watch] src/utils/auth.ts changed
[watch] Running tests...
[watch] ✅ 8 tests passed
```

### Toast Notifications
Desktop notifications for background watching:
```
🧪 Tests Passed
8 tests passed in 1.2s
```

### Quiet Mode
Only notify on failures:
```
[watch] ❌ 2 tests failed
```

## Debouncing

Prevent action spam during rapid edits:

```json
{
  "debounce": 500  // Wait 500ms after last change
}
```

```
File saved → wait 500ms → no more changes → run action
```

## Watch Modes

### Development Mode
All watchers active:
```
"Start watching for development"
```

### Test Mode
Only test-related watchers:
```
"Watch tests only"
```

### CI Mode
Strict mode, fail on any issue:
```
"Watch with CI strictness"
```

## Integration with Claude

### Proactive Suggestions
When file changes detected:

```markdown
I noticed you modified `src/auth/login.ts`.

**Auto-ran:**
- ✅ Type check passed
- ✅ Related tests passed (3/3)

**Suggestions:**
- The function `validateCredentials` might need a test for empty password
- Consider updating the API documentation
```

### Change Summary
At end of session:
```markdown
## File Changes This Session

**Modified:** 8 files
**Tests run:** 24 (all passed)
**Type errors fixed:** 2
**Auto-formatted:** 8 files

**Files without test coverage:**
- src/utils/newHelper.ts (new file)
```

## Performance

### Ignore Patterns
Don't watch generated/dependency files:
```json
{
  "ignore": [
    "node_modules/**",
    "dist/**",
    ".git/**",
    "coverage/**",
    "*.log"
  ]
}
```

### Resource Limits
```json
{
  "maxWatchers": 1000,
  "cpuThrottle": true,
  "batchChanges": true
}
```

## Commands

### Start Watching
```
"Start file watchers"
"Watch for changes"
```

### Stop Watching
```
"Stop watching"
"Pause watchers"
```

### Status
```
"Show watcher status"
"What's being watched?"
```

### Add Watcher
```
"Watch *.graphql files and regenerate types"
"Add watcher for schema changes"
```

## Platform Support

### macOS/Linux
Uses native FSEvents/inotify.

### Windows
Uses ReadDirectoryChangesW or polling fallback.

### WSL
Special handling for Windows/WSL file system boundary.
