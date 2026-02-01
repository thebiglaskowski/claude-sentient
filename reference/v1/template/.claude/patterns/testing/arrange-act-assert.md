# Arrange-Act-Assert Pattern

## Intent

Structure tests in three clear phases: setup (Arrange), execution (Act), and verification (Assert), making tests readable and maintainable.

---

## When to Use

- All unit tests
- Integration tests
- Any automated test requiring clarity
- Code review of test files

## Structure

```
┌─────────────────────────────────────┐
│              TEST                    │
├─────────────────────────────────────┤
│  ARRANGE                            │
│  - Set up test data                 │
│  - Create mocks/stubs               │
│  - Initialize system under test     │
├─────────────────────────────────────┤
│  ACT                                │
│  - Execute the behavior             │
│  - Usually ONE action               │
├─────────────────────────────────────┤
│  ASSERT                             │
│  - Verify expected outcomes         │
│  - Check state changes              │
│  - Verify interactions              │
└─────────────────────────────────────┘
```

---

## Implementation

### TypeScript (Jest/Vitest)

```typescript
describe('UserService', () => {
  describe('createUser', () => {
    it('should create a user with hashed password', async () => {
      // Arrange
      const userRepo = mock<UserRepository>();
      const hasher = mock<PasswordHasher>();
      const service = new UserService(userRepo, hasher);

      const input = {
        email: 'test@example.com',
        password: 'plaintext123',
        name: 'Test User',
      };

      hasher.hash.mockResolvedValue('hashed_password_xyz');
      userRepo.save.mockResolvedValue({
        id: 'user-123',
        ...input,
        password: 'hashed_password_xyz',
        createdAt: new Date(),
      });

      // Act
      const result = await service.createUser(input);

      // Assert
      expect(result.id).toBe('user-123');
      expect(result.email).toBe(input.email);
      expect(hasher.hash).toHaveBeenCalledWith('plaintext123');
      expect(userRepo.save).toHaveBeenCalledWith(
        expect.objectContaining({
          email: input.email,
          password: 'hashed_password_xyz',
        })
      );
    });

    it('should throw when email already exists', async () => {
      // Arrange
      const userRepo = mock<UserRepository>();
      const service = new UserService(userRepo, mock<PasswordHasher>());

      userRepo.findByEmail.mockResolvedValue({
        id: 'existing-user',
        email: 'test@example.com',
      });

      // Act & Assert
      await expect(
        service.createUser({ email: 'test@example.com', password: 'pass' })
      ).rejects.toThrow(DuplicateEmailError);

      expect(userRepo.save).not.toHaveBeenCalled();
    });
  });
});

// Helper for complex arrange
function createTestContext() {
  const userRepo = mock<UserRepository>();
  const hasher = mock<PasswordHasher>();
  const emailService = mock<EmailService>();
  const service = new UserService(userRepo, hasher, emailService);

  return { userRepo, hasher, emailService, service };
}

describe('with helper', () => {
  it('should send welcome email after creation', async () => {
    // Arrange
    const { service, userRepo, emailService } = createTestContext();
    userRepo.save.mockResolvedValue(createTestUser());

    // Act
    await service.createUser(validUserInput());

    // Assert
    expect(emailService.sendWelcome).toHaveBeenCalled();
  });
});
```

### Python (pytest)

```python
import pytest
from unittest.mock import Mock, AsyncMock

class TestUserService:
    """Tests for UserService.create_user"""

    @pytest.fixture
    def user_repo(self):
        return Mock(spec=UserRepository)

    @pytest.fixture
    def password_hasher(self):
        return Mock(spec=PasswordHasher)

    @pytest.fixture
    def service(self, user_repo, password_hasher):
        return UserService(user_repo, password_hasher)

    async def test_creates_user_with_hashed_password(
        self, service, user_repo, password_hasher
    ):
        # Arrange
        input_data = {
            "email": "test@example.com",
            "password": "plaintext123",
            "name": "Test User",
        }
        password_hasher.hash.return_value = "hashed_xyz"
        user_repo.save = AsyncMock(return_value=User(
            id="user-123",
            email=input_data["email"],
            password="hashed_xyz",
        ))

        # Act
        result = await service.create_user(input_data)

        # Assert
        assert result.id == "user-123"
        assert result.email == input_data["email"]
        password_hasher.hash.assert_called_once_with("plaintext123")
        user_repo.save.assert_called_once()

    async def test_raises_when_email_exists(self, service, user_repo):
        # Arrange
        user_repo.find_by_email = AsyncMock(return_value=User(id="existing"))

        # Act & Assert
        with pytest.raises(DuplicateEmailError):
            await service.create_user({"email": "test@example.com"})

        user_repo.save.assert_not_called()


# Parametrized tests maintain AAA structure
@pytest.mark.parametrize("input_email,expected_error", [
    ("", "Email is required"),
    ("invalid", "Invalid email format"),
    ("a" * 256 + "@test.com", "Email too long"),
])
def test_validates_email_format(service, input_email, expected_error):
    # Arrange
    input_data = {"email": input_email, "password": "valid123"}

    # Act & Assert
    with pytest.raises(ValidationError) as exc:
        service.create_user(input_data)

    assert expected_error in str(exc.value)
```

### Go

```go
func TestUserService_CreateUser(t *testing.T) {
    t.Run("creates user with hashed password", func(t *testing.T) {
        // Arrange
        repo := &mockUserRepo{}
        hasher := &mockPasswordHasher{
            hashResult: "hashed_xyz",
        }
        service := NewUserService(repo, hasher)

        input := CreateUserInput{
            Email:    "test@example.com",
            Password: "plaintext123",
            Name:     "Test User",
        }

        repo.saveResult = &User{
            ID:    "user-123",
            Email: input.Email,
        }

        // Act
        result, err := service.CreateUser(context.Background(), input)

        // Assert
        require.NoError(t, err)
        assert.Equal(t, "user-123", result.ID)
        assert.Equal(t, input.Email, result.Email)
        assert.Equal(t, "plaintext123", hasher.lastHashInput)
        assert.NotNil(t, repo.lastSavedUser)
        assert.Equal(t, "hashed_xyz", repo.lastSavedUser.Password)
    })

    t.Run("returns error when email exists", func(t *testing.T) {
        // Arrange
        repo := &mockUserRepo{
            findByEmailResult: &User{ID: "existing"},
        }
        service := NewUserService(repo, &mockPasswordHasher{})

        // Act
        _, err := service.CreateUser(context.Background(), CreateUserInput{
            Email: "test@example.com",
        })

        // Assert
        assert.ErrorIs(t, err, ErrDuplicateEmail)
        assert.Nil(t, repo.lastSavedUser, "should not save")
    })
}

// Table-driven tests with AAA
func TestUserService_ValidateEmail(t *testing.T) {
    tests := []struct {
        name          string
        email         string
        expectedError string
    }{
        {"empty email", "", "email is required"},
        {"invalid format", "invalid", "invalid email format"},
        {"too long", strings.Repeat("a", 256) + "@test.com", "email too long"},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            // Arrange
            service := NewUserService(nil, nil)

            // Act
            err := service.ValidateEmail(tt.email)

            // Assert
            require.Error(t, err)
            assert.Contains(t, err.Error(), tt.expectedError)
        })
    }
}
```

---

## Guidelines

### One Act Per Test

```typescript
// Good - single action
it('should add item to cart', () => {
  const cart = new Cart();
  const item = createItem();

  cart.addItem(item);  // Single action

  expect(cart.items).toContain(item);
});

// Bad - multiple actions
it('should handle cart operations', () => {
  const cart = new Cart();

  cart.addItem(item1);
  cart.addItem(item2);
  cart.removeItem(item1);  // Multiple actions = multiple tests

  expect(cart.items).toEqual([item2]);
});
```

### Descriptive Names

```typescript
// Good - describes behavior
it('should throw ValidationError when email format is invalid')
it('should return empty array when no users match filter')
it('should send notification email after successful order')

// Bad - vague
it('should work correctly')
it('handles edge case')
it('test user creation')
```

### Isolated Tests

```typescript
// Good - each test is independent
beforeEach(() => {
  database.clear();  // Fresh state
});

// Bad - tests depend on order
it('creates user', () => { /* creates user-1 */ });
it('finds user', () => { /* assumes user-1 exists */ });
```

---

## Related Patterns

- **Test Doubles** — Mocks, stubs, fakes for Arrange
- **Fixture Factory** — Reusable test data setup
- **Given-When-Then** — BDD variant of AAA
- **Builder** — Complex test object construction

---

## Anti-Patterns

- **Multiple Acts** — Split into separate tests
- **Assert-Act-Assert** — Testing behavior during arrange
- **No assertions** — Every test needs verification
- **Arrange in loop** — Use parametrized tests instead
