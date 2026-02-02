# Claude Sentient Issues Found During Testing

## Test Project
- **Location:** `C:\scripts\cs-test-project`
- **Type:** TypeScript monorepo (React + Express)
- **Profile:** TypeScript

---

## Issues Found in Claude Sentient

### 1. Profile Detection Doesn't Handle Monorepos
**File:** `.claude/hooks/session-start.js:38-57`

**Problem:** The `detectProfile()` function only checks for config files at the root level. In monorepos, `tsconfig.json` and `package.json` are often in subdirectories (packages/).

**Current behavior:**
```javascript
if (fs.existsSync(path.join(cwd, 'tsconfig.json'))) {
    return 'typescript';
}
```

**Workaround:** Added root-level `tsconfig.json` with project references.

**Suggested fix:** Search recursively or check common monorepo patterns:
```javascript
function detectProfile() {
    const cwd = process.cwd();

    // Check root first
    if (fs.existsSync(path.join(cwd, 'tsconfig.json'))) return 'typescript';

    // Check packages/* for monorepos
    const packagesDir = path.join(cwd, 'packages');
    if (fs.existsSync(packagesDir)) {
        const packages = fs.readdirSync(packagesDir);
        for (const pkg of packages) {
            if (fs.existsSync(path.join(packagesDir, pkg, 'tsconfig.json'))) {
                return 'typescript';
            }
        }
    }
    // ... rest of detection
}
```

---

### 2. PowerShell Installer Parsing Issue (FIXED)
**File:** `install.ps1:90-96`

**Problem:** Parentheses in double-quoted strings caused parsing errors in some PowerShell environments.

**Fix applied:** Changed to single-quoted strings.

---

### 3. Context Injector Keywords Missing Common Terms (FIXED)
**File:** `.claude/hooks/context-injector.js:40-48`

**Problem:** Keywords like "lint", "refactor", "error", "bug" weren't detected.

**Fix applied:** Added `codeQuality`, `errorHandling`, and `documentation` topic categories.

---

### 4. Git Branch Detection Fails for Fresh Repos
**File:** `.claude/hooks/session-start.js:22-27`

**Problem:** For new repos with no commits, `git rev-parse --abbrev-ref HEAD` fails and returns "unknown".

**Observed:** Test project showed `"gitBranch":"unknown"` after `git init` but before commits.

**Suggested fix:** Check if HEAD exists first:
```javascript
try {
    execSync('git rev-parse HEAD', { stdio: ['pipe', 'pipe', 'pipe'] });
    gitBranch = execSync('git rev-parse --abbrev-ref HEAD', { encoding: 'utf8', stdio: ['pipe', 'pipe', 'pipe'] }).trim();
} catch (e) {
    gitBranch = 'no-commits';
}
```

---

### 5. TypeScript SDK Not Tested Yet
**File:** `sdk/typescript/`

**Status:** The TypeScript SDK exists but hasn't been tested with the new test project.

**TODO:** Run the SDK against the test project to validate:
- Profile detection
- Hook integration
- Quality gate execution
- Session persistence

---

## Test Project Validation

### Hooks Tested ✅
| Hook | Status | Notes |
|------|--------|-------|
| session-start.js | ✅ Working | Detects TypeScript profile |
| bash-validator.js | ✅ Working | Blocks dangerous commands |
| file-validator.js | ✅ Working | Blocks protected paths |
| context-injector.js | ✅ Working | Detects expanded keywords |
| post-edit.js | ✅ Working | Tracks file changes |

### Quality Gates Tested
| Gate | Tool | Status |
|------|------|--------|
| Lint | ESLint | ✅ 3 warnings found |
| Type | TypeScript | ✅ Works (errors found in tests) |
| Test | Vitest | ⚠️ Needs jest-dom types |

---

## Recommendations

1. **Improve monorepo detection** in session-start.js
2. **Add more robust git detection** for new/empty repos
3. **Test TypeScript SDK** with the new test project
4. **Add E2E tests** for the hook system
5. **Consider adding npm/pnpm workspace detection** to profile detection

---

## Next Steps

1. Fix the monorepo detection issue
2. Run `/cs-assess` on the TypeScript test project
3. Test the TypeScript SDK integration
4. Run `/cs-loop` to see if it can fix the test project issues
