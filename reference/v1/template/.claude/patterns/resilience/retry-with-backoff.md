# Retry with Backoff Pattern

## Intent

Automatically retry failed operations with increasing delays, handling transient failures without overwhelming the target system.

---

## When to Use

- Network requests that may fail temporarily
- Database connections during high load
- External API calls with rate limits
- Distributed system communication
- Any operation with transient failure modes

## When NOT to Use

- Permanent failures (400 Bad Request, validation errors)
- Non-idempotent operations without safeguards
- User-facing operations requiring immediate feedback
- When failure indicates a bug, not transient issue

---

## Structure

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│ Attempt │ ──▶ │  Fail?  │ ──▶ │  Wait   │ ──┐
└─────────┘     └─────────┘     └─────────┘   │
     ▲               │                         │
     │               ▼                         │
     │          ┌─────────┐                    │
     └──────────│ Retry?  │◀───────────────────┘
                └─────────┘
                     │
                     ▼
                ┌─────────┐
                │  Fail   │
                └─────────┘
```

---

## Implementation

### TypeScript

```typescript
interface RetryConfig {
  maxAttempts: number;
  initialDelayMs: number;
  maxDelayMs: number;
  backoffMultiplier: number;
  retryableErrors?: (error: Error) => boolean;
  onRetry?: (attempt: number, error: Error, delayMs: number) => void;
}

const defaultConfig: RetryConfig = {
  maxAttempts: 3,
  initialDelayMs: 1000,
  maxDelayMs: 30000,
  backoffMultiplier: 2,
};

async function withRetry<T>(
  operation: () => Promise<T>,
  config: Partial<RetryConfig> = {}
): Promise<T> {
  const {
    maxAttempts,
    initialDelayMs,
    maxDelayMs,
    backoffMultiplier,
    retryableErrors,
    onRetry,
  } = { ...defaultConfig, ...config };

  let lastError: Error;
  let delayMs = initialDelayMs;

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await operation();
    } catch (error) {
      lastError = error as Error;

      // Check if error is retryable
      if (retryableErrors && !retryableErrors(lastError)) {
        throw lastError;
      }

      // Last attempt, don't retry
      if (attempt === maxAttempts) {
        break;
      }

      // Add jitter to prevent thundering herd
      const jitter = Math.random() * 0.3 * delayMs;
      const actualDelay = Math.min(delayMs + jitter, maxDelayMs);

      onRetry?.(attempt, lastError, actualDelay);

      await sleep(actualDelay);
      delayMs = Math.min(delayMs * backoffMultiplier, maxDelayMs);
    }
  }

  throw new RetryExhaustedError(
    `Operation failed after ${maxAttempts} attempts`,
    lastError!
  );
}

function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Usage
const data = await withRetry(
  () => fetchFromApi('/users'),
  {
    maxAttempts: 5,
    initialDelayMs: 500,
    retryableErrors: (err) => err instanceof NetworkError,
    onRetry: (attempt, err, delay) => {
      logger.warn(`Retry ${attempt} after ${delay}ms: ${err.message}`);
    },
  }
);
```

### Python

```python
import asyncio
import random
from functools import wraps
from typing import Callable, TypeVar, Optional, Type
from dataclasses import dataclass

T = TypeVar('T')

@dataclass
class RetryConfig:
    max_attempts: int = 3
    initial_delay: float = 1.0
    max_delay: float = 30.0
    backoff_multiplier: float = 2.0
    retryable_exceptions: tuple = (Exception,)
    on_retry: Optional[Callable[[int, Exception, float], None]] = None

async def with_retry(
    operation: Callable[[], T],
    config: Optional[RetryConfig] = None
) -> T:
    cfg = config or RetryConfig()
    delay = cfg.initial_delay
    last_error: Optional[Exception] = None

    for attempt in range(1, cfg.max_attempts + 1):
        try:
            if asyncio.iscoroutinefunction(operation):
                return await operation()
            return operation()
        except cfg.retryable_exceptions as e:
            last_error = e

            if attempt == cfg.max_attempts:
                break

            # Add jitter
            jitter = random.uniform(0, 0.3 * delay)
            actual_delay = min(delay + jitter, cfg.max_delay)

            if cfg.on_retry:
                cfg.on_retry(attempt, e, actual_delay)

            await asyncio.sleep(actual_delay)
            delay = min(delay * cfg.backoff_multiplier, cfg.max_delay)

    raise RetryExhaustedError(
        f"Operation failed after {cfg.max_attempts} attempts"
    ) from last_error


# Decorator version
def retry(
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    retryable_exceptions: tuple = (Exception,)
):
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await with_retry(
                lambda: func(*args, **kwargs),
                RetryConfig(
                    max_attempts=max_attempts,
                    initial_delay=initial_delay,
                    retryable_exceptions=retryable_exceptions,
                )
            )
        return wrapper
    return decorator


# Usage
@retry(max_attempts=5, retryable_exceptions=(NetworkError, TimeoutError))
async def fetch_user(user_id: str) -> User:
    return await api.get(f"/users/{user_id}")
```

### Go

```go
type RetryConfig struct {
    MaxAttempts       int
    InitialDelay      time.Duration
    MaxDelay          time.Duration
    BackoffMultiplier float64
    IsRetryable       func(error) bool
    OnRetry           func(attempt int, err error, delay time.Duration)
}

func DefaultRetryConfig() RetryConfig {
    return RetryConfig{
        MaxAttempts:       3,
        InitialDelay:      time.Second,
        MaxDelay:          30 * time.Second,
        BackoffMultiplier: 2.0,
        IsRetryable:       func(error) bool { return true },
    }
}

func WithRetry[T any](
    ctx context.Context,
    operation func() (T, error),
    config RetryConfig,
) (T, error) {
    var zero T
    var lastErr error
    delay := config.InitialDelay

    for attempt := 1; attempt <= config.MaxAttempts; attempt++ {
        result, err := operation()
        if err == nil {
            return result, nil
        }

        lastErr = err

        if !config.IsRetryable(err) {
            return zero, err
        }

        if attempt == config.MaxAttempts {
            break
        }

        // Add jitter
        jitter := time.Duration(rand.Float64() * 0.3 * float64(delay))
        actualDelay := delay + jitter
        if actualDelay > config.MaxDelay {
            actualDelay = config.MaxDelay
        }

        if config.OnRetry != nil {
            config.OnRetry(attempt, err, actualDelay)
        }

        select {
        case <-ctx.Done():
            return zero, ctx.Err()
        case <-time.After(actualDelay):
        }

        delay = time.Duration(float64(delay) * config.BackoffMultiplier)
        if delay > config.MaxDelay {
            delay = config.MaxDelay
        }
    }

    return zero, fmt.Errorf("operation failed after %d attempts: %w",
        config.MaxAttempts, lastErr)
}
```

---

## Variations

### Exponential Backoff

```
Delay = InitialDelay * (Multiplier ^ Attempt)
Example: 1s, 2s, 4s, 8s, 16s...
```

### Linear Backoff

```
Delay = InitialDelay * Attempt
Example: 1s, 2s, 3s, 4s, 5s...
```

### Decorrelated Jitter

```typescript
// Better distribution than simple jitter
const nextDelay = Math.min(
  maxDelay,
  Math.random() * (previousDelay * 3 - initialDelay) + initialDelay
);
```

### Circuit Breaker Integration

```typescript
async function withRetryAndCircuitBreaker<T>(
  operation: () => Promise<T>,
  circuitBreaker: CircuitBreaker,
  retryConfig: RetryConfig
): Promise<T> {
  return circuitBreaker.execute(() =>
    withRetry(operation, retryConfig)
  );
}
```

---

## Related Patterns

- **Circuit Breaker** — Stop retrying when system is unhealthy
- **Timeout** — Bound individual attempt duration
- **Bulkhead** — Isolate retry pools
- **Idempotency Key** — Safe retries for non-idempotent operations

---

## Anti-Patterns

- **No jitter** — Causes thundering herd problem
- **Retrying non-retryable errors** — Wastes resources
- **Infinite retries** — Always have a max
- **Same delay** — Use backoff to give system recovery time
- **Retrying non-idempotent operations** — Data corruption risk
