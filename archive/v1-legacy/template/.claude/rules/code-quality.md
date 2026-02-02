# Code Quality Rules

## Core Principles

1. **Readability over cleverness** — Code is read more than written
2. **Consistency** — Follow established patterns in codebase
3. **Simplicity** — Prefer simple solutions to complex ones
4. **DRY with judgment** — Avoid premature abstraction
5. **Fail fast** — Validate early, fail with clear messages

---

## Complexity Limits

### Function Complexity
| Metric | Limit | Action |
|--------|-------|--------|
| Lines of code | 50 | Extract helper functions |
| Cyclomatic complexity | 10 | Simplify conditionals |
| Nesting depth | 3 | Use early returns |
| Parameters | 4 | Use options object |

### File Complexity
| Metric | Limit | Action |
|--------|-------|--------|
| Lines of code | 400 | Split into modules |
| Exports | 10 | Create submodules |
| Dependencies | 15 | Review necessity |

---

## Naming Conventions

### Variables
```javascript
// Booleans - is/has/can/should prefix
const isActive = true;
const hasPermission = true;
const canEdit = true;
const shouldRefresh = false;

// Arrays - plural nouns
const users = [];
const selectedItems = [];

// Objects/instances - singular nouns
const user = {};
const config = {};

// Functions - verb + noun
function getUser() {}
function calculateTotal() {}
function validateEmail() {}
function handleClick() {}
```

### Constants
```javascript
// UPPER_SNAKE_CASE for true constants
const MAX_RETRIES = 3;
const API_BASE_URL = 'https://api.example.com';
const DEFAULT_TIMEOUT_MS = 5000;
```

### Classes/Types
```javascript
// PascalCase
class UserService {}
interface PaymentRequest {}
type ResponseStatus = 'success' | 'error';
```

### Files
```
# Components
UserProfile.tsx
PaymentForm.tsx

# Utilities
stringUtils.ts
dateHelpers.ts

# Constants
config.ts
constants.ts

# Tests
UserProfile.test.tsx
stringUtils.test.ts
```

---

## Code Smells

### Long Methods
```javascript
// Bad - too many responsibilities
function processOrder(order) {
  // 100 lines of validation
  // 50 lines of calculation
  // 30 lines of notification
  // 20 lines of logging
}

// Good - single responsibility
function processOrder(order) {
  validateOrder(order);
  const total = calculateTotal(order);
  await saveOrder(order, total);
  notifyCustomer(order);
}
```

### Deep Nesting
```javascript
// Bad - pyramid of doom
if (user) {
  if (user.isActive) {
    if (user.hasPermission) {
      if (order.isValid) {
        // finally do something
      }
    }
  }
}

// Good - early returns
if (!user) return;
if (!user.isActive) return;
if (!user.hasPermission) return;
if (!order.isValid) return;
// do something
```

### Magic Numbers
```javascript
// Bad
if (retries > 3) throw new Error();
setTimeout(callback, 86400000);

// Good
const MAX_RETRIES = 3;
const ONE_DAY_MS = 24 * 60 * 60 * 1000;

if (retries > MAX_RETRIES) throw new Error();
setTimeout(callback, ONE_DAY_MS);
```

### Boolean Parameters
```javascript
// Bad - unclear at call site
createUser(userData, true, false);

// Good - explicit options
createUser(userData, {
  sendWelcomeEmail: true,
  skipValidation: false
});
```

---

## Dependency Management

### Guidelines
- Pin exact versions in production
- Update dependencies regularly (weekly/monthly)
- Audit for vulnerabilities on every build
- Remove unused dependencies
- Prefer well-maintained packages

### Selection Criteria
Before adding a dependency, check:
- [ ] Downloads/week > 10,000
- [ ] Last update < 6 months
- [ ] Open issues triaged
- [ ] License compatible
- [ ] Bundle size acceptable
- [ ] No known vulnerabilities

### Bundling Impact
```
# Check before adding
npx bundlephobia <package-name>

# Guidelines
- Core web bundle < 250KB
- Per-page lazy loaded < 100KB
- Avoid packages > 50KB for small features
```

---

## Error Handling

### Validation Pattern
```javascript
function createUser(data) {
  // Validate at boundaries
  if (!data) throw new ValidationError('Data required');
  if (!data.email) throw new ValidationError('Email required');
  if (!isValidEmail(data.email)) throw new ValidationError('Invalid email');

  // Business logic after validation
  return userRepository.create(data);
}
```

### Try-Catch Guidelines
```javascript
// Bad - catch everything
try {
  doSomething();
} catch (e) {
  console.log('Error');
}

// Good - specific handling
try {
  await saveUser(user);
} catch (error) {
  if (error instanceof ValidationError) {
    return { success: false, errors: error.fields };
  }
  if (error instanceof DatabaseError) {
    logger.error('Database error saving user', { error, user });
    throw new ServiceError('Unable to save user');
  }
  throw error; // Re-throw unexpected errors
}
```

---

## Performance Guidelines

### Avoid These
```javascript
// N+1 queries
for (const user of users) {
  const orders = await getOrders(user.id); // Query per user
}

// Synchronous file operations
const data = fs.readFileSync(path); // Blocks event loop

// Memory leaks
const cache = {}; // Unbounded growth
```

### Prefer These
```javascript
// Batch queries
const orders = await getOrdersForUsers(userIds);

// Async operations
const data = await fs.promises.readFile(path);

// Bounded caches
const cache = new LRUCache({ max: 1000 });
```

---

## Code Review Checklist

Before approving:
- [ ] Names are clear and consistent
- [ ] No functions > 50 lines
- [ ] No nesting > 3 levels
- [ ] No magic numbers
- [ ] Errors handled appropriately
- [ ] No console.log or debug code
- [ ] No commented-out code
- [ ] Tests cover new functionality
- [ ] No obvious performance issues
- [ ] Dependencies justified
