---
name: modern-tech-checker
description: Identify outdated patterns and suggest modern alternatives
argument-hint: "<technology or area>"
model: sonnet
---

# Modern Tech Checker

Identify outdated technologies, patterns, and dependencies. Suggest modern alternatives.

## Description

Continuously strive to use the most modern, well-supported technologies. This skill scans the codebase for outdated patterns and suggests upgrades.

Triggers on: "modernize", "update tech", "modern alternatives", "latest patterns"

## Arguments

```
$1 - Optional: specific area to check (deps, patterns, apis, all)
     Default: all

--aggressive    Suggest bleeding-edge alternatives
--conservative  Only suggest stable, widely-adopted alternatives
--report-only   Generate report without making changes
```

## Modernization Categories

### 1. Deprecated Dependencies

Check for packages that are:
- No longer maintained
- Have security vulnerabilities
- Have better modern alternatives

```
Common Replacements:
┌────────────────────┬────────────────────┬─────────────────┐
│ Outdated           │ Modern             │ Why Switch      │
├────────────────────┼────────────────────┼─────────────────┤
│ moment.js          │ date-fns, dayjs    │ Size, tree-shake│
│ request            │ fetch, axios, got  │ Deprecated      │
│ lodash (full)      │ lodash-es, native  │ Bundle size     │
│ enzyme             │ @testing-library   │ React recommend │
│ tslint             │ eslint             │ Deprecated      │
│ node-sass          │ sass (dart-sass)   │ Deprecated      │
│ create-react-app   │ vite, next.js      │ Performance     │
│ webpack (basic)    │ vite, esbuild      │ Speed           │
│ express-validator  │ zod, yup           │ TypeScript      │
│ passport (simple)  │ lucia, auth.js     │ Modern patterns │
│ mongoose           │ prisma, drizzle    │ Type safety     │
│ redux (vanilla)    │ zustand, jotai     │ Simplicity      │
│ styled-components  │ tailwind, vanilla  │ Performance     │
└────────────────────┴────────────────────┴─────────────────┘
```

### 2. Outdated Language Patterns

```javascript
// ❌ Outdated Patterns          // ✅ Modern Alternatives

// Callbacks
fs.readFile(path, (err, data) => {  →  const data = await fs.promises.readFile(path);
  if (err) throw err;
  // use data
});

// var keyword
var x = 1;                          →  const x = 1; // or let if mutable

// Function declarations for arrows
function handler(e) { }             →  const handler = (e) => { }

// String concatenation
"Hello " + name                     →  `Hello ${name}`

// Object.assign
Object.assign({}, obj, { a: 1 })    →  { ...obj, a: 1 }

// Array methods
arr.filter(x => x).length > 0       →  arr.some(Boolean)

// Promises without async/await
promise.then(x => {                 →  const x = await promise;
  return process(x);                    return process(x);
}).catch(err => {                   // with try/catch
  handleError(err);
});

// CommonJS in modern projects
const x = require('x');             →  import x from 'x';
module.exports = y;                 →  export default y;
```

### 3. API Evolution

```typescript
// Check if using deprecated APIs

// Node.js
url.parse()                         →  new URL()
new Buffer()                        →  Buffer.from()
fs.exists()                         →  fs.access() or fs.stat()
path.join(__dirname, x)             →  import.meta.url + fileURLToPath

// React
componentDidMount                   →  useEffect
this.state                          →  useState
React.createClass                   →  function/class components
ReactDOM.render                     →  createRoot().render()

// Browser
document.write                      →  DOM manipulation
XMLHttpRequest                      →  fetch
.bind(this)                         →  arrow functions
```

### 4. Configuration Modernization

```yaml
# Outdated configs to update:

# .babelrc → babel.config.js (or remove if using modern bundler)
# tslint.json → .eslintrc with @typescript-eslint
# .prettierrc (old) → prettier.config.js
# webpack.config.js → vite.config.ts
# jest.config.js → vitest.config.ts
```

## Check Process

### Step 1: Dependency Audit
```bash
# Check for outdated packages
npm outdated
# or
pip list --outdated
# or
conda list --outdated

# Check for vulnerabilities
npm audit
# or
pip-audit
# or
safety check
```

### Step 2: Pattern Scan
```
Scan codebase for:
- var usage
- Callback patterns
- CommonJS in ESM projects
- Deprecated API calls
- Old React patterns (class components, lifecycle methods)
```

### Step 3: Context7 Verification
```
For each potential modernization:
1. Query context7 for current best practices
2. Verify the suggested alternative is actually recommended
3. Check for migration guides
4. Note any breaking changes
```

### Step 4: Impact Assessment
```
For each suggestion:
- Breaking change? (major version bump)
- Migration effort (low/medium/high)
- Risk level (safe/moderate/risky)
- Benefits (performance, DX, security, bundle size)
```

## Output Report

```markdown
# Modernization Report

## Summary
- Outdated dependencies: 5
- Deprecated patterns: 12
- Deprecated APIs: 3
- Estimated effort: Medium

## Critical Updates (Do Now)
| Item | Current | Recommended | Breaking | Effort |
|------|---------|-------------|----------|--------|
| node-sass | 7.0.0 | sass 1.x | Yes | Low |
| @types/node | 14 | 20 | No | Low |

## Recommended Updates
| Item | Current | Recommended | Why |
|------|---------|-------------|-----|
| moment | 2.29 | date-fns 3.x | Bundle size -90% |
| lodash | 4.17 | lodash-es | Tree-shaking |

## Pattern Modernization
| File | Line | Current | Modern |
|------|------|---------|--------|
| utils.js | 45 | var | const |
| api.js | 23 | callback | async/await |
| App.jsx | 12 | class | function |

## Migration Guides
- [moment → date-fns](https://date-fns.org/docs/moment)
- [class → hooks](https://react.dev/reference/react)

## Deferred (Review Later)
- Webpack → Vite (major undertaking, schedule separately)
```

## Integration with Autonomous Loop

When running in autonomous loop:

1. **Check tech on each iteration**
2. **Prioritize:**
   - Security vulnerabilities (immediate)
   - Deprecated with no support (high)
   - Performance improvements (medium)
   - Nice-to-have modernization (low)
3. **Auto-fix low-risk items** (var → const, etc.)
4. **Queue high-risk items** for user review

## Using Context7

```
For each technology question:

1. "use context7 to check [library] latest best practices"
2. "use context7 to find [library] migration guide"
3. "use context7 for [library] vs [alternative] comparison"

Example queries:
- "React Query v5 patterns"
- "Prisma vs Mongoose 2024"
- "Vite migration from Webpack"
- "Next.js App Router patterns"
```

## Safety Rules

1. **Never auto-upgrade major versions** without review
2. **Always check for breaking changes** before suggesting
3. **Prefer stable releases** over bleeding edge
4. **Consider team familiarity** with new tech
5. **One major migration at a time** to limit risk
