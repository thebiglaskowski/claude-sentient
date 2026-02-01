# Error Boundary Pattern

## Intent

Contain failures within defined boundaries, preventing errors from cascading and enabling graceful degradation.

---

## When to Use

- Component-based UI frameworks (React, Vue)
- Microservice boundaries
- Plugin/extension systems
- Third-party integrations
- Any subsystem that should fail independently

## When NOT to Use

- Errors that should propagate (validation, auth)
- Critical path operations requiring immediate failure
- Simple scripts without recovery needs

---

## Structure

```
┌──────────────────────────────────────────────┐
│              Error Boundary                   │
│  ┌─────────────────────────────────────────┐ │
│  │         Protected Component              │ │
│  │  ┌──────────┐  ┌──────────┐            │ │
│  │  │ Child A  │  │ Child B  │  ← Error!  │ │
│  │  └──────────┘  └──────────┘            │ │
│  └─────────────────────────────────────────┘ │
│                      │                        │
│                      ▼                        │
│              ┌──────────────┐                │
│              │ Fallback UI  │                │
│              └──────────────┘                │
└──────────────────────────────────────────────┘
```

---

## Implementation

### React (TypeScript)

```tsx
import React, { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode | ((error: Error, reset: () => void) => ReactNode);
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
  resetKeys?: unknown[];
}

interface State {
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error: Error): Partial<State> {
    return { error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    this.setState({ errorInfo });
    this.props.onError?.(error, errorInfo);

    // Log to error tracking service
    logErrorToService(error, errorInfo);
  }

  componentDidUpdate(prevProps: Props): void {
    // Reset on key change (e.g., route change)
    if (
      this.state.error &&
      this.props.resetKeys?.some(
        (key, i) => key !== prevProps.resetKeys?.[i]
      )
    ) {
      this.reset();
    }
  }

  reset = (): void => {
    this.setState({ error: null, errorInfo: null });
  };

  render(): ReactNode {
    const { error } = this.state;
    const { children, fallback } = this.props;

    if (error) {
      if (typeof fallback === 'function') {
        return fallback(error, this.reset);
      }
      return fallback ?? <DefaultErrorFallback error={error} reset={this.reset} />;
    }

    return children;
  }
}

// Default fallback component
function DefaultErrorFallback({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  return (
    <div role="alert" className="error-boundary-fallback">
      <h2>Something went wrong</h2>
      <pre>{error.message}</pre>
      <button onClick={reset}>Try again</button>
    </div>
  );
}

// Usage
function App() {
  return (
    <ErrorBoundary
      fallback={(error, reset) => (
        <ErrorPage error={error} onRetry={reset} />
      )}
      onError={(error) => analytics.track('error', { message: error.message })}
      resetKeys={[location.pathname]}
    >
      <Router>
        <Routes />
      </Router>
    </ErrorBoundary>
  );
}

// Granular boundaries
function Dashboard() {
  return (
    <div>
      <ErrorBoundary fallback={<WidgetError />}>
        <AnalyticsWidget />
      </ErrorBoundary>
      <ErrorBoundary fallback={<WidgetError />}>
        <RecentOrdersWidget />
      </ErrorBoundary>
    </div>
  );
}
```

### React Hooks (with react-error-boundary)

```tsx
import { ErrorBoundary, useErrorBoundary } from 'react-error-boundary';

function ErrorFallback({ error, resetErrorBoundary }) {
  return (
    <div role="alert">
      <p>Something went wrong:</p>
      <pre>{error.message}</pre>
      <button onClick={resetErrorBoundary}>Try again</button>
    </div>
  );
}

// Component that can trigger boundary
function DataLoader({ id }) {
  const { showBoundary } = useErrorBoundary();

  useEffect(() => {
    fetchData(id).catch(showBoundary);
  }, [id, showBoundary]);

  return <Data />;
}
```

### Vue 3

```vue
<script setup lang="ts">
import { ref, onErrorCaptured } from 'vue';

const error = ref<Error | null>(null);
const errorInfo = ref<string>('');

onErrorCaptured((err, instance, info) => {
  error.value = err;
  errorInfo.value = info;

  // Log error
  logErrorToService(err, info);

  // Prevent propagation
  return false;
});

function reset() {
  error.value = null;
  errorInfo.value = '';
}
</script>

<template>
  <div v-if="error" class="error-boundary">
    <h2>Something went wrong</h2>
    <pre>{{ error.message }}</pre>
    <button @click="reset">Try again</button>
  </div>
  <slot v-else />
</template>
```

### Node.js / Backend

```typescript
// Domain-based error boundary
import { createDomain } from 'domain';

function withErrorBoundary<T>(
  operation: () => Promise<T>,
  options: {
    onError?: (error: Error) => void;
    fallback?: T;
  } = {}
): Promise<T> {
  return new Promise((resolve, reject) => {
    const d = createDomain();

    d.on('error', (error) => {
      options.onError?.(error);
      if (options.fallback !== undefined) {
        resolve(options.fallback);
      } else {
        reject(error);
      }
    });

    d.run(async () => {
      try {
        const result = await operation();
        resolve(result);
      } catch (error) {
        d.emit('error', error);
      }
    });
  });
}

// Express middleware boundary
function errorBoundary(
  handler: RequestHandler
): RequestHandler {
  return async (req, res, next) => {
    try {
      await handler(req, res, next);
    } catch (error) {
      // Log but don't crash
      logger.error('Request handler error', { error, path: req.path });

      // Send graceful response
      res.status(500).json({
        error: 'Internal server error',
        requestId: req.id,
      });
    }
  };
}

// Usage
app.get('/api/users', errorBoundary(async (req, res) => {
  const users = await userService.getAll();
  res.json(users);
}));
```

### Go

```go
// Panic recovery boundary
func withRecovery[T any](
    operation func() (T, error),
    onPanic func(recovered any),
) (result T, err error) {
    defer func() {
        if r := recover(); r != nil {
            if onPanic != nil {
                onPanic(r)
            }
            err = fmt.Errorf("panic recovered: %v", r)
        }
    }()

    return operation()
}

// HTTP middleware
func RecoveryMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        defer func() {
            if err := recover(); err != nil {
                log.Printf("Panic recovered: %v\n%s", err, debug.Stack())

                w.Header().Set("Content-Type", "application/json")
                w.WriteHeader(http.StatusInternalServerError)
                json.NewEncoder(w).Encode(map[string]string{
                    "error": "Internal server error",
                })
            }
        }()

        next.ServeHTTP(w, r)
    })
}
```

---

## Variations

### Retry Boundary

```tsx
function RetryBoundary({ children, maxRetries = 3 }) {
  const [retryCount, setRetryCount] = useState(0);

  if (retryCount >= maxRetries) {
    return <MaxRetriesExceeded />;
  }

  return (
    <ErrorBoundary
      onReset={() => setRetryCount(c => c + 1)}
      fallback={({ resetErrorBoundary }) => (
        <RetryPrompt onRetry={resetErrorBoundary} attempt={retryCount + 1} />
      )}
    >
      {children}
    </ErrorBoundary>
  );
}
```

### Suspense + Error Boundary

```tsx
function AsyncBoundary({ children }) {
  return (
    <ErrorBoundary fallback={<ErrorFallback />}>
      <Suspense fallback={<Loading />}>
        {children}
      </Suspense>
    </ErrorBoundary>
  );
}
```

---

## Related Patterns

- **Circuit Breaker** — Boundary for external calls
- **Bulkhead** — Isolate failure domains
- **Retry** — Recovery within boundary
- **Fallback** — Graceful degradation

---

## Anti-Patterns

- **Swallowing errors** — Always log, even if recovering
- **Too broad** — Boundaries should be granular
- **No user feedback** — Always show something went wrong
- **Catching everything** — Some errors should propagate
