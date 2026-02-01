# Testing Rules

## Core Principles

1. **Test first** — Write tests before or alongside code, never after
2. **Test behavior, not implementation** — Tests survive refactoring
3. **Fast feedback** — Unit tests in milliseconds, suites in seconds
4. **Deterministic** — Same input = same result, no flaky tests
5. **Isolated** — Tests don't depend on each other or external state

---

## Testing Pyramid

```
        /\
       /  \      E2E (few, slow, high confidence)
      /----\
     /      \    Integration (some, medium speed)
    /--------\
   /          \  Unit (many, fast, low cost)
  /____________\
```

### Distribution Guidelines
| Type | Coverage | Speed | Count |
|------|----------|-------|-------|
| Unit | 70-80% | <10ms each | Many |
| Integration | 15-20% | <1s each | Some |
| E2E | 5-10% | <30s each | Few |

---

## Coverage Standards

### Minimum Thresholds
```
Overall: 80%
New code: 90%
Critical paths: 100%
```

### What to Cover
- All public APIs
- All error paths
- All edge cases
- All business logic
- All security controls

### What Not to Cover
- Generated code
- Third-party code
- Simple getters/setters
- Framework boilerplate
- Configuration files

---

## Naming Conventions

### Test File Names
```
# Unit tests
[module].test.ts
[module].spec.ts

# Integration tests
[feature].integration.test.ts

# E2E tests
[flow].e2e.test.ts
```

### Test Case Names
```javascript
// Pattern: should_[expected]_when_[condition]
it('should_return_user_when_valid_id_provided')
it('should_throw_error_when_user_not_found')
it('should_hash_password_when_creating_user')

// Alternative: [unit]_[scenario]_[expected]
it('getUser_validId_returnsUser')
it('getUser_invalidId_throwsNotFoundError')
```

### Describe Blocks
```javascript
describe('UserService', () => {
  describe('createUser', () => {
    it('should create user with valid data')
    it('should hash password before saving')
    it('should throw when email exists')
  })
})
```

---

## Test Structure (AAA Pattern)

```javascript
it('should calculate total with tax', () => {
  // Arrange - Set up test data and conditions
  const cart = new Cart();
  cart.addItem({ price: 100, quantity: 2 });
  const taxRate = 0.1;

  // Act - Execute the code under test
  const total = cart.calculateTotal(taxRate);

  // Assert - Verify the results
  expect(total).toBe(220);
});
```

---

## Mocking Guidelines

### When to Mock
- External services (APIs, databases)
- Time-dependent operations
- Random number generation
- File system operations
- Network requests

### When NOT to Mock
- The code under test
- Simple value objects
- Pure functions
- Internal collaborators (usually)

### Mock Patterns
```javascript
// Stub - Returns canned data
jest.spyOn(userRepo, 'findById').mockResolvedValue(mockUser);

// Spy - Tracks calls without changing behavior
const spy = jest.spyOn(logger, 'info');
expect(spy).toHaveBeenCalledWith('User created');

// Fake - Working implementation for testing
const fakeDb = new InMemoryDatabase();

// Mock - Full replacement with assertions
const mockEmail = jest.fn().mockResolvedValue({ sent: true });
```

---

## Test Data Management

### Factories over Fixtures
```javascript
// Good - Factory function
const createUser = (overrides = {}) => ({
  id: faker.datatype.uuid(),
  email: faker.internet.email(),
  name: faker.name.fullName(),
  ...overrides
});

// Use in tests
const user = createUser({ email: 'specific@test.com' });
```

### Test Data Rules
- Generate unique data per test
- Use meaningful values that document intent
- Clean up after integration tests
- Never use production data
- Reset state between tests

---

## Async Testing

```javascript
// Promises
it('should fetch user', async () => {
  const user = await userService.getUser(1);
  expect(user.name).toBe('John');
});

// Error assertions
it('should throw on invalid id', async () => {
  await expect(userService.getUser(-1))
    .rejects.toThrow('Invalid ID');
});

// Timeouts
it('should complete within limit', async () => {
  const result = await Promise.race([
    slowOperation(),
    timeout(1000)
  ]);
  expect(result).toBeDefined();
}, 5000);
```

---

## Anti-Patterns

### Avoid These
```javascript
// Testing implementation details
expect(component.state.isLoading).toBe(true); // Bad

// Multiple assertions testing different things
it('should work', () => {
  expect(createUser()).toBeDefined();
  expect(deleteUser()).toBe(true);
  expect(listUsers()).toHaveLength(0);
}); // Bad - three tests in one

// Non-deterministic tests
it('should generate unique id', () => {
  expect(generateId()).not.toBe(generateId()); // Flaky
});

// Shared mutable state
let user; // Defined outside tests - dangerous
beforeEach(() => { user = createUser(); });

// Sleeping instead of waiting
await new Promise(r => setTimeout(r, 1000)); // Bad
await waitFor(() => expect(elem).toBeVisible()); // Good
```

---

## Test Quality Checklist

Before merging tests:

- [ ] Tests have descriptive names
- [ ] Each test verifies one behavior
- [ ] Tests are independent and isolated
- [ ] No hardcoded sleep/delays
- [ ] Mocks are minimal and justified
- [ ] Edge cases are covered
- [ ] Error paths are tested
- [ ] Test data is meaningful
- [ ] No console.log or debug code
- [ ] Tests run fast (<10s for unit suite)

---

## TDD Workflow

1. **Red** — Write a failing test for the next feature
2. **Green** — Write minimum code to pass the test
3. **Refactor** — Improve code while tests pass

```bash
# Typical cycle
1. Write test → npm test → FAIL (red)
2. Implement → npm test → PASS (green)
3. Refactor → npm test → PASS (still green)
4. Repeat
```
