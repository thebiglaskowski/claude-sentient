# Snippet: error-class

## Description

Custom error classes with proper inheritance, error codes, and HTTP status mapping.

## When to Use

- Creating application-specific errors
- API error handling
- Domain error modeling
- Error serialization

## Code

### TypeScript Error Hierarchy

```typescript
// Base application error
export class AppError extends Error {
  public readonly code: string;
  public readonly statusCode: number;
  public readonly isOperational: boolean;
  public readonly context?: Record<string, unknown>;

  constructor(
    message: string,
    options: {
      code?: string;
      statusCode?: number;
      isOperational?: boolean;
      context?: Record<string, unknown>;
      cause?: Error;
    } = {}
  ) {
    super(message, { cause: options.cause });

    this.name = this.constructor.name;
    this.code = options.code ?? 'INTERNAL_ERROR';
    this.statusCode = options.statusCode ?? 500;
    this.isOperational = options.isOperational ?? true;
    this.context = options.context;

    // Maintains proper stack trace
    Error.captureStackTrace(this, this.constructor);
  }

  toJSON() {
    return {
      name: this.name,
      message: this.message,
      code: this.code,
      ...(this.context && { context: this.context }),
    };
  }
}

// HTTP errors
export class NotFoundError extends AppError {
  constructor(resource: string, id?: string) {
    super(id ? `${resource} with id '${id}' not found` : `${resource} not found`, {
      code: 'NOT_FOUND',
      statusCode: 404,
      context: { resource, id },
    });
  }
}

export class BadRequestError extends AppError {
  constructor(message: string, context?: Record<string, unknown>) {
    super(message, {
      code: 'BAD_REQUEST',
      statusCode: 400,
      context,
    });
  }
}

export class UnauthorizedError extends AppError {
  constructor(message = 'Authentication required') {
    super(message, {
      code: 'UNAUTHORIZED',
      statusCode: 401,
    });
  }
}

export class ForbiddenError extends AppError {
  constructor(message = 'Access denied') {
    super(message, {
      code: 'FORBIDDEN',
      statusCode: 403,
    });
  }
}

export class ConflictError extends AppError {
  constructor(message: string, context?: Record<string, unknown>) {
    super(message, {
      code: 'CONFLICT',
      statusCode: 409,
      context,
    });
  }
}

export class ValidationError extends AppError {
  public readonly errors: ValidationErrorItem[];

  constructor(errors: ValidationErrorItem[]) {
    super('Validation failed', {
      code: 'VALIDATION_ERROR',
      statusCode: 400,
      context: { errors },
    });
    this.errors = errors;
  }

  toJSON() {
    return {
      ...super.toJSON(),
      errors: this.errors,
    };
  }
}

interface ValidationErrorItem {
  field: string;
  message: string;
  code?: string;
}

// Domain errors
export class DomainError extends AppError {
  constructor(message: string, code: string) {
    super(message, {
      code,
      statusCode: 422,
      isOperational: true,
    });
  }
}

export class InsufficientFundsError extends DomainError {
  constructor(available: number, required: number) {
    super(
      `Insufficient funds: ${available} available, ${required} required`,
      'INSUFFICIENT_FUNDS'
    );
  }
}

export class DuplicateEmailError extends DomainError {
  constructor(email: string) {
    super(`Email '${email}' is already registered`, 'DUPLICATE_EMAIL');
  }
}

// External service errors
export class ExternalServiceError extends AppError {
  constructor(
    service: string,
    message: string,
    cause?: Error
  ) {
    super(`${service} error: ${message}`, {
      code: 'EXTERNAL_SERVICE_ERROR',
      statusCode: 502,
      isOperational: true,
      context: { service },
      cause,
    });
  }
}

// Type guards
export function isAppError(error: unknown): error is AppError {
  return error instanceof AppError;
}

export function isOperationalError(error: unknown): boolean {
  return isAppError(error) && error.isOperational;
}
```

### Express Error Handler

```typescript
import { Request, Response, NextFunction } from 'express';
import { AppError, isAppError, isOperationalError } from './errors';
import { logger } from './logger';

export function errorHandler(
  error: Error,
  req: Request,
  res: Response,
  next: NextFunction
) {
  // Log error
  logger.error('Request error', {
    error: {
      name: error.name,
      message: error.message,
      stack: error.stack,
    },
    request: {
      method: req.method,
      path: req.path,
      body: req.body,
    },
  });

  // Handle known operational errors
  if (isAppError(error)) {
    return res.status(error.statusCode).json({
      error: error.toJSON(),
    });
  }

  // Unknown errors - don't leak details
  return res.status(500).json({
    error: {
      name: 'InternalError',
      message: 'An unexpected error occurred',
      code: 'INTERNAL_ERROR',
    },
  });
}

// Not found handler
export function notFoundHandler(req: Request, res: Response) {
  res.status(404).json({
    error: {
      name: 'NotFoundError',
      message: `Route ${req.method} ${req.path} not found`,
      code: 'ROUTE_NOT_FOUND',
    },
  });
}
```

### Python Error Classes

```python
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List

class AppError(Exception):
    """Base application error"""

    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_ERROR",
        status_code: int = 500,
        is_operational: bool = True,
        context: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.is_operational = is_operational
        self.context = context or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.__class__.__name__,
            "message": self.message,
            "code": self.code,
            **({"context": self.context} if self.context else {}),
        }


class NotFoundError(AppError):
    def __init__(self, resource: str, id: Optional[str] = None):
        message = f"{resource} with id '{id}' not found" if id else f"{resource} not found"
        super().__init__(
            message,
            code="NOT_FOUND",
            status_code=404,
            context={"resource": resource, "id": id},
        )


class ValidationError(AppError):
    def __init__(self, errors: List[Dict[str, str]]):
        super().__init__(
            "Validation failed",
            code="VALIDATION_ERROR",
            status_code=400,
            context={"errors": errors},
        )
        self.errors = errors


class UnauthorizedError(AppError):
    def __init__(self, message: str = "Authentication required"):
        super().__init__(message, code="UNAUTHORIZED", status_code=401)


class ForbiddenError(AppError):
    def __init__(self, message: str = "Access denied"):
        super().__init__(message, code="FORBIDDEN", status_code=403)
```

## Customization Points

- Error types — Add domain-specific errors
- Status codes — Adjust for your API conventions
- Context fields — Add relevant debugging info
- Serialization — Modify `toJSON` for your format

## Related Snippets

- [express-route](../api/express-route.md) — Use errors in routes
- [logger](logger.md) — Log errors
- [jest-test](../testing/jest-test.md) — Test error cases
