---
name: error-recovery
description: Handle failures with retries and smart recovery strategies
model: sonnet
---

# Error Recovery

Automatically handle failures with retries and smart recovery strategies.

## Description

Provides error handling patterns, auto-retry logic, and recovery suggestions.
Triggers on: "error", "failed", "retry", "fix this error", "something went wrong".

## Error Categories

### Transient Errors (Auto-Retry)
Errors that often resolve on retry:
- Network timeouts
- Rate limiting (429)
- Temporary file locks
- Git lock files
- npm registry hiccups

### Recoverable Errors (Suggest Fix)
Errors with known solutions:
- Missing dependencies
- Permission denied
- Port in use
- Merge conflicts
- Type errors

### Fatal Errors (Stop & Report)
Errors requiring human intervention:
- Authentication failures
- Corrupt data
- Missing required files
- Breaking changes

## Auto-Retry Strategy

### Retry Configuration
```markdown
| Error Type | Max Retries | Delay | Backoff |
|------------|-------------|-------|---------|
| Network timeout | 3 | 2s | Exponential |
| Rate limit | 3 | 5s | Exponential |
| File lock | 5 | 1s | Linear |
| Git lock | 3 | 2s | Linear |
```

### Retry Pattern
```bash
# Conceptual retry logic
attempt=1
max_attempts=3
while [ $attempt -le $max_attempts ]; do
  if command_succeeds; then
    break
  fi
  echo "Attempt $attempt failed, retrying in ${delay}s..."
  sleep $delay
  delay=$((delay * 2))  # Exponential backoff
  attempt=$((attempt + 1))
done
```

## Common Error Solutions

### npm/Node Errors

| Error | Solution |
|-------|----------|
| `ENOENT package.json` | Run from project root |
| `EACCES permission denied` | Fix npm permissions or use nvm |
| `ERESOLVE peer dependency` | `npm install --legacy-peer-deps` |
| `MODULE_NOT_FOUND` | `rm -rf node_modules && npm install` |
| `EADDRINUSE port in use` | Kill process on port or use different port |

### Git Errors

| Error | Solution |
|-------|----------|
| `fatal: not a git repository` | `git init` or cd to repo root |
| `index.lock exists` | `rm .git/index.lock` |
| `merge conflict` | Resolve conflicts, then `git add` |
| `divergent branches` | `git pull --rebase` or merge |
| `permission denied (publickey)` | Set up SSH keys |

### Python Errors

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError` | `pip install <module>` |
| `venv not found` | `python -m venv .venv` |
| `Permission denied` | Use `--user` flag or fix permissions |

### TypeScript Errors

| Error | Solution |
|-------|----------|
| `Cannot find module` | Check imports, run `npm install` |
| `Type X not assignable` | Fix type mismatch or add type assertion |
| `tsconfig.json not found` | `npx tsc --init` |

## Recovery Workflows

### Dependency Issues
```markdown
## Recovery: Dependency Issues

1. **Clear caches:**
   ```bash
   rm -rf node_modules
   rm package-lock.json  # or yarn.lock
   npm cache clean --force
   ```

2. **Reinstall:**
   ```bash
   npm install
   ```

3. **If still failing:**
   - Check Node version matches project requirements
   - Try `npm install --legacy-peer-deps`
   - Check for conflicting global packages
```

### Git State Issues
```markdown
## Recovery: Git State Issues

1. **Check status:**
   ```bash
   git status
   git stash list
   ```

2. **If uncommitted changes blocking:**
   ```bash
   git stash
   # do operation
   git stash pop
   ```

3. **If merge conflict:**
   ```bash
   # Edit conflicted files
   git add <resolved-files>
   git commit
   ```

4. **Nuclear option (careful!):**
   ```bash
   git fetch origin
   git reset --hard origin/main
   ```
```

### Build Failures
```markdown
## Recovery: Build Failures

1. **Clean build:**
   ```bash
   rm -rf dist .next build out
   npm run build
   ```

2. **Check for type errors:**
   ```bash
   npx tsc --noEmit
   ```

3. **Check environment:**
   - Required env vars set?
   - Correct Node version?
   - All dependencies installed?
```

## Error Reporting Format

When an error can't be auto-recovered:

```markdown
## Error Encountered

**Command:** `npm run build`
**Exit Code:** 1
**Error Type:** Build Failure

### Error Output
```
TypeError: Cannot read property 'map' of undefined
  at processItems (src/utils.ts:45:12)
```

### Analysis
- Null/undefined value being accessed
- Location: `src/utils.ts` line 45
- Likely cause: Missing null check

### Suggested Fixes
1. Add null check before `.map()`:
   ```typescript
   items?.map(...) || []
   ```

2. Validate input earlier in the function

3. Check where `processItems` is called from

### Recovery Steps
1. Fix the type error in `src/utils.ts`
2. Run `npm run build` again
3. If successful, run tests to verify
```

## Graceful Degradation

When optional features fail:

| Feature | Fallback |
|---------|----------|
| skills.sh unreachable | Skip skill install, use existing |
| Prettier not found | Skip auto-format, warn user |
| gh CLI missing | Use git-only workflow |
| Context7 unavailable | Use built-in knowledge |

## Prevention

### Pre-flight Checks
Before operations, verify:
- [ ] Required tools installed (dependency-checker)
- [ ] In correct directory
- [ ] Git state is clean (or changes are stashed)
- [ ] Required env vars set

### Safe Defaults
- Always use `--dry-run` first for destructive operations
- Create backups before major changes
- Commit frequently to enable easy rollback
