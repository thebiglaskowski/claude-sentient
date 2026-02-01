# Snippet: jest-test

## Description

Jest test suite with TypeScript, proper mocking, and arrange-act-assert pattern.

## When to Use

- Writing unit tests
- Testing services/utilities
- Testing React components
- Integration tests

## Code

### Service Test

```typescript
import { describe, it, expect, beforeEach, jest } from '@jest/globals';
import { UserService } from './user.service';
import { UserRepository } from './user.repository';
import { PasswordHasher } from './password-hasher';
import { EmailService } from './email.service';

// Mock dependencies
jest.mock('./user.repository');
jest.mock('./password-hasher');
jest.mock('./email.service');

describe('UserService', () => {
  let service: UserService;
  let userRepo: jest.Mocked<UserRepository>;
  let hasher: jest.Mocked<PasswordHasher>;
  let emailService: jest.Mocked<EmailService>;

  beforeEach(() => {
    // Reset mocks
    jest.clearAllMocks();

    // Create mock instances
    userRepo = new UserRepository() as jest.Mocked<UserRepository>;
    hasher = new PasswordHasher() as jest.Mocked<PasswordHasher>;
    emailService = new EmailService() as jest.Mocked<EmailService>;

    // Create service with mocks
    service = new UserService(userRepo, hasher, emailService);
  });

  describe('createUser', () => {
    const validInput = {
      email: 'test@example.com',
      password: 'password123',
      name: 'Test User',
    };

    it('should create user with hashed password', async () => {
      // Arrange
      hasher.hash.mockResolvedValue('hashed_password');
      userRepo.findByEmail.mockResolvedValue(null);
      userRepo.save.mockResolvedValue({
        id: 'user-123',
        ...validInput,
        password: 'hashed_password',
        createdAt: new Date(),
      });

      // Act
      const result = await service.createUser(validInput);

      // Assert
      expect(result.id).toBe('user-123');
      expect(hasher.hash).toHaveBeenCalledWith('password123');
      expect(userRepo.save).toHaveBeenCalledWith(
        expect.objectContaining({
          email: validInput.email,
          password: 'hashed_password',
        })
      );
    });

    it('should send welcome email after creation', async () => {
      // Arrange
      hasher.hash.mockResolvedValue('hashed');
      userRepo.findByEmail.mockResolvedValue(null);
      userRepo.save.mockResolvedValue({
        id: 'user-123',
        email: validInput.email,
        name: validInput.name,
      });

      // Act
      await service.createUser(validInput);

      // Assert
      expect(emailService.sendWelcome).toHaveBeenCalledWith({
        to: validInput.email,
        name: validInput.name,
      });
    });

    it('should throw when email already exists', async () => {
      // Arrange
      userRepo.findByEmail.mockResolvedValue({ id: 'existing' });

      // Act & Assert
      await expect(service.createUser(validInput)).rejects.toThrow(
        'Email already exists'
      );
      expect(userRepo.save).not.toHaveBeenCalled();
    });

    it.each([
      ['empty email', { ...validInput, email: '' }, 'Email is required'],
      ['invalid email', { ...validInput, email: 'invalid' }, 'Invalid email'],
      ['short password', { ...validInput, password: '123' }, 'Password too short'],
    ])('should reject %s', async (_, input, expectedError) => {
      // Act & Assert
      await expect(service.createUser(input)).rejects.toThrow(expectedError);
    });
  });

  describe('findById', () => {
    it('should return user when found', async () => {
      // Arrange
      const user = { id: 'user-123', email: 'test@example.com' };
      userRepo.findById.mockResolvedValue(user);

      // Act
      const result = await service.findById('user-123');

      // Assert
      expect(result).toEqual(user);
    });

    it('should return null when not found', async () => {
      // Arrange
      userRepo.findById.mockResolvedValue(null);

      // Act
      const result = await service.findById('nonexistent');

      // Assert
      expect(result).toBeNull();
    });
  });
});
```

### React Component Test

```tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { UserProfile } from './UserProfile';
import { fetchUser, updateUser } from '@/api/users';

// Mock API
jest.mock('@/api/users');
const mockFetchUser = fetchUser as jest.MockedFunction<typeof fetchUser>;
const mockUpdateUser = updateUser as jest.MockedFunction<typeof updateUser>;

// Test wrapper
function createWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  });
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}

describe('UserProfile', () => {
  const mockUser = {
    id: 'user-123',
    name: 'John Doe',
    email: 'john@example.com',
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should render loading state initially', () => {
    // Arrange
    mockFetchUser.mockReturnValue(new Promise(() => {})); // Never resolves

    // Act
    render(<UserProfile userId="user-123" />, { wrapper: createWrapper() });

    // Assert
    expect(screen.getByRole('status')).toBeInTheDocument();
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  it('should render user data when loaded', async () => {
    // Arrange
    mockFetchUser.mockResolvedValue(mockUser);

    // Act
    render(<UserProfile userId="user-123" />, { wrapper: createWrapper() });

    // Assert
    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument();
    });
    expect(screen.getByText('john@example.com')).toBeInTheDocument();
  });

  it('should render error state on failure', async () => {
    // Arrange
    mockFetchUser.mockRejectedValue(new Error('Failed to fetch'));

    // Act
    render(<UserProfile userId="user-123" />, { wrapper: createWrapper() });

    // Assert
    await waitFor(() => {
      expect(screen.getByRole('alert')).toBeInTheDocument();
    });
    expect(screen.getByText(/failed to fetch/i)).toBeInTheDocument();
  });

  it('should update user name on form submit', async () => {
    // Arrange
    const user = userEvent.setup();
    mockFetchUser.mockResolvedValue(mockUser);
    mockUpdateUser.mockResolvedValue({ ...mockUser, name: 'Jane Doe' });

    render(<UserProfile userId="user-123" />, { wrapper: createWrapper() });
    await waitFor(() => screen.getByText('John Doe'));

    // Act
    await user.click(screen.getByRole('button', { name: /edit/i }));
    await user.clear(screen.getByLabelText(/name/i));
    await user.type(screen.getByLabelText(/name/i), 'Jane Doe');
    await user.click(screen.getByRole('button', { name: /save/i }));

    // Assert
    await waitFor(() => {
      expect(mockUpdateUser).toHaveBeenCalledWith('user-123', {
        name: 'Jane Doe',
      });
    });
  });

  it('should be accessible', async () => {
    // Arrange
    mockFetchUser.mockResolvedValue(mockUser);

    // Act
    const { container } = render(<UserProfile userId="user-123" />, {
      wrapper: createWrapper(),
    });
    await waitFor(() => screen.getByText('John Doe'));

    // Assert
    expect(container).toBeAccessible();
  });
});
```

### API Route Test

```typescript
import request from 'supertest';
import { app } from './app';
import { db } from './db';

describe('POST /api/users', () => {
  beforeEach(async () => {
    await db.user.deleteMany();
  });

  afterAll(async () => {
    await db.$disconnect();
  });

  it('should create a user and return 201', async () => {
    // Arrange
    const input = {
      email: 'test@example.com',
      password: 'password123',
      name: 'Test User',
    };

    // Act
    const response = await request(app)
      .post('/api/users')
      .send(input)
      .expect('Content-Type', /json/);

    // Assert
    expect(response.status).toBe(201);
    expect(response.body.data).toMatchObject({
      email: input.email,
      name: input.name,
    });
    expect(response.body.data.password).toBeUndefined();
  });

  it('should return 400 for invalid email', async () => {
    // Arrange
    const input = { email: 'invalid', password: 'password123' };

    // Act
    const response = await request(app).post('/api/users').send(input);

    // Assert
    expect(response.status).toBe(400);
    expect(response.body.error).toContain('email');
  });

  it('should return 409 for duplicate email', async () => {
    // Arrange
    const input = { email: 'test@example.com', password: 'password123' };
    await db.user.create({ data: input });

    // Act
    const response = await request(app).post('/api/users').send(input);

    // Assert
    expect(response.status).toBe(409);
  });
});
```

## Customization Points

- Service/component name — Replace with your target
- Mock setup — Adjust for your dependencies
- Test cases — Add your specific scenarios
- Assertions — Match your expected behavior

## Related Snippets

- [express-route](../api/express-route.md) — Route to test
- [react-component](../react/react-component.md) — Component to test
- [error-class](../utility/error-class.md) — Error assertions
