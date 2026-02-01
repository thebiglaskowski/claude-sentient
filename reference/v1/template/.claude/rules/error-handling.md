# Error Handling Rules

## Core Principles

1. **Fail fast** — Detect and report errors early
2. **Fail loud** — Make errors visible, don't swallow
3. **Fail safe** — Graceful degradation when possible
4. **Provide context** — Include what, where, why
5. **Enable recovery** — Tell users how to fix

---

## Error Hierarchy

### Standard Error Types
```
Error (base)
├── ValidationError      # Invalid input data
├── AuthenticationError  # Who are you?
├── AuthorizationError   # Not permitted
├── NotFoundError        # Resource doesn't exist
├── ConflictError        # State conflict
├── RateLimitError       # Too many requests
├── ServiceError         # Internal failure
└── ExternalError        # Third-party failure
```

### Implementation
```typescript
class AppError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number,
    public details?: unknown
  ) {
    super(message);
    this.name = this.constructor.name;
    Error.captureStackTrace(this, this.constructor);
  }
}

class ValidationError extends AppError {
  constructor(message: string, details?: unknown) {
    super(message, 'VALIDATION_ERROR', 400, details);
  }
}

class NotFoundError extends AppError {
  constructor(resource: string, id: string) {
    super(`${resource} not found: ${id}`, 'NOT_FOUND', 404);
  }
}
```

---

## Error Messages

### For Users
```
# Bad - technical jargon
"ECONNREFUSED 127.0.0.1:5432"
"TypeError: Cannot read property 'name' of undefined"

# Good - actionable messages
"Unable to save your changes. Please try again."
"Your session has expired. Please log in again."
"This email is already registered. Try logging in instead."
```

### For Developers
```javascript
// Include context for debugging
logger.error('Failed to process payment', {
  error: err.message,
  stack: err.stack,
  userId: user.id,
  orderId: order.id,
  amount: order.total,
  paymentProvider: 'stripe',
  requestId: req.id
});
```

---

## Error Response Format

### Structured Response
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Please fix the following errors",
    "details": [
      {
        "field": "email",
        "code": "INVALID_FORMAT",
        "message": "Please enter a valid email address"
      },
      {
        "field": "password",
        "code": "TOO_SHORT",
        "message": "Password must be at least 8 characters"
      }
    ],
    "documentation": "https://api.example.com/docs/errors#VALIDATION_ERROR"
  }
}
```

### Error Codes
```
# Format: CATEGORY_SPECIFIC_ERROR
VALIDATION_REQUIRED_FIELD
VALIDATION_INVALID_FORMAT
VALIDATION_OUT_OF_RANGE

AUTH_INVALID_CREDENTIALS
AUTH_TOKEN_EXPIRED
AUTH_INSUFFICIENT_PERMISSION

RESOURCE_NOT_FOUND
RESOURCE_ALREADY_EXISTS
RESOURCE_STATE_CONFLICT

RATE_LIMIT_EXCEEDED
SERVICE_UNAVAILABLE
EXTERNAL_SERVICE_ERROR
```

---

## Try-Catch Patterns

### Specific Catching
```javascript
// Good - handle known errors specifically
try {
  const user = await userService.create(data);
  return user;
} catch (error) {
  if (error instanceof ValidationError) {
    return res.status(400).json({ error: error.toJSON() });
  }
  if (error instanceof ConflictError) {
    return res.status(409).json({ error: error.toJSON() });
  }
  // Re-throw unexpected errors for global handler
  throw error;
}
```

### Global Error Handler
```javascript
// Express global error handler
app.use((err, req, res, next) => {
  // Log full error for debugging
  logger.error('Unhandled error', {
    error: err.message,
    stack: err.stack,
    path: req.path,
    method: req.method,
    requestId: req.id
  });

  // Return safe error to client
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: err.toJSON()
    });
  }

  // Generic error for unknown issues
  res.status(500).json({
    error: {
      code: 'INTERNAL_ERROR',
      message: 'An unexpected error occurred',
      requestId: req.id
    }
  });
});
```

---

## Logging Strategy

### What to Log
```
ALWAYS log:
- All errors (with context)
- Security events (auth failures, permission denials)
- Business events (orders, payments)
- Performance anomalies

NEVER log:
- Passwords or secrets
- Personal data (PII) unless required
- Full request/response bodies in production
- Stack traces to users
```

### Log Levels
| Level | When to Use |
|-------|-------------|
| ERROR | Operation failed, needs attention |
| WARN | Recoverable issue, potential problem |
| INFO | Business events, state changes |
| DEBUG | Development diagnostics |

### Structured Logging
```javascript
// Good - structured, searchable
logger.error('Payment failed', {
  level: 'error',
  service: 'payment',
  event: 'payment_failed',
  userId: '123',
  orderId: '456',
  amount: 9999,
  currency: 'USD',
  provider: 'stripe',
  errorCode: 'card_declined',
  requestId: 'req_abc123'
});
```

---

## Recovery Strategies

### Retry with Backoff
```javascript
async function withRetry(fn, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxRetries) throw error;
      if (!isRetryable(error)) throw error;

      const delay = Math.pow(2, attempt) * 1000;
      await sleep(delay);
    }
  }
}

function isRetryable(error) {
  return (
    error.code === 'ETIMEDOUT' ||
    error.code === 'ECONNRESET' ||
    error.statusCode === 503 ||
    error.statusCode === 429
  );
}
```

### Circuit Breaker
```javascript
class CircuitBreaker {
  constructor(threshold = 5, resetTimeout = 30000) {
    this.failures = 0;
    this.threshold = threshold;
    this.resetTimeout = resetTimeout;
    this.state = 'CLOSED';
  }

  async execute(fn) {
    if (this.state === 'OPEN') {
      throw new Error('Circuit breaker is open');
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  onSuccess() {
    this.failures = 0;
    this.state = 'CLOSED';
  }

  onFailure() {
    this.failures++;
    if (this.failures >= this.threshold) {
      this.state = 'OPEN';
      setTimeout(() => {
        this.state = 'HALF_OPEN';
      }, this.resetTimeout);
    }
  }
}
```

---

## Anti-Patterns

### Avoid These
```javascript
// Swallowing errors
try {
  doSomething();
} catch (e) {
  // Silent failure - BAD
}

// Generic catch-all
try {
  doSomething();
} catch (e) {
  console.log('Error'); // No context - BAD
}

// Exposing internals
res.status(500).json({
  error: error.stack // Security risk - BAD
});

// Wrong status codes
res.status(200).json({
  success: false,
  error: 'Not found' // Should be 404 - BAD
});
```

---

## Checklist

Before deploying:
- [ ] All errors have appropriate types
- [ ] User messages are friendly and actionable
- [ ] Developer logs include context
- [ ] No sensitive data in error messages
- [ ] Global error handler catches all
- [ ] Retry logic for transient failures
- [ ] Circuit breakers for external services
- [ ] Error monitoring/alerting in place
