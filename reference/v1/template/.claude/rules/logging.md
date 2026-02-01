# Logging Rules

## Core Principles

1. **Log for operators** — Someone debugging at 3 AM
2. **Structured over text** — JSON enables searching
3. **Context is king** — Include correlation IDs
4. **Protect privacy** — Never log secrets or PII
5. **Right level, right time** — Don't over-log or under-log

---

## Log Levels

| Level | When to Use | Examples |
|-------|-------------|----------|
| **ERROR** | Operation failed, needs attention | Database down, payment failed |
| **WARN** | Recoverable issue, potential problem | Retry succeeded, deprecated API |
| **INFO** | Business events, state changes | User login, order created |
| **DEBUG** | Development diagnostics | Function entry/exit, variable values |
| **TRACE** | Detailed debugging | Full request/response bodies |

### Level Guidelines

```javascript
// ERROR - Something broke, alert needed
logger.error('Payment processing failed', {
  error: err.message,
  orderId: order.id,
  provider: 'stripe'
});

// WARN - Something concerning, may need attention
logger.warn('API rate limit approaching', {
  currentRate: 95,
  limit: 100,
  window: '1m'
});

// INFO - Business event happened
logger.info('Order placed', {
  orderId: order.id,
  userId: user.id,
  total: order.total
});

// DEBUG - Development details
logger.debug('Cache miss', { key: cacheKey });
```

---

## Structured Logging

### Standard Format

```json
{
  "timestamp": "2026-01-29T10:30:00.000Z",
  "level": "info",
  "message": "Order created",
  "service": "order-service",
  "version": "2.1.0",
  "environment": "production",
  "requestId": "req_abc123",
  "traceId": "trace_xyz789",
  "userId": "user_123",
  "data": {
    "orderId": "order_456",
    "total": 9999,
    "itemCount": 3
  }
}
```

### Implementation

```javascript
// Configure structured logger
const logger = winston.createLogger({
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  defaultMeta: {
    service: 'order-service',
    version: process.env.VERSION,
    environment: process.env.NODE_ENV
  },
  transports: [
    new winston.transports.Console()
  ]
});

// Always include context
logger.info('Order created', {
  requestId: req.id,
  userId: user.id,
  orderId: order.id,
  total: order.total
});
```

---

## Context & Correlation

### Request Tracing

```javascript
// Middleware to add request context
app.use((req, res, next) => {
  req.id = req.headers['x-request-id'] || uuid();
  req.traceId = req.headers['x-trace-id'] || uuid();

  // Add to all logs in this request
  req.logger = logger.child({
    requestId: req.id,
    traceId: req.traceId,
    path: req.path,
    method: req.method
  });

  next();
});

// Use request logger throughout
app.post('/orders', async (req, res) => {
  req.logger.info('Creating order', { userId: req.user.id });
  // ...
  req.logger.info('Order created', { orderId: order.id });
});
```

### Async Context (Node.js)

```javascript
const { AsyncLocalStorage } = require('async_hooks');
const asyncLocalStorage = new AsyncLocalStorage();

// Middleware
app.use((req, res, next) => {
  const context = { requestId: uuid(), userId: req.user?.id };
  asyncLocalStorage.run(context, () => next());
});

// Anywhere in code
function getContext() {
  return asyncLocalStorage.getStore() || {};
}

logger.info('Processing', { ...getContext(), data });
```

---

## What to Log

### Always Log

```javascript
// Authentication events
logger.info('User login', { userId, method: 'oauth', provider: 'google' });
logger.warn('Failed login attempt', { email, reason: 'invalid_password' });

// Authorization failures
logger.warn('Access denied', { userId, resource, requiredRole });

// Business transactions
logger.info('Payment processed', { orderId, amount, provider });

// Errors with context
logger.error('Database query failed', {
  error: err.message,
  query: 'getUserById',
  userId,
  duration: 5000
});

// Performance anomalies
logger.warn('Slow query detected', { query, duration: 3500, threshold: 1000 });
```

### Never Log

```javascript
// NEVER log these
password, apiKey, token, secret, creditCard, ssn, sessionId

// Bad - exposes secrets
logger.info('User auth', { password: req.body.password }); // NEVER

// Bad - PII in logs
logger.info('User created', { email, ssn, creditCard }); // NEVER

// Good - redact sensitive data
logger.info('User created', { userId, email: mask(email) });
```

---

## Error Logging

### Good Error Logs

```javascript
// Include all debugging context
try {
  await processPayment(order);
} catch (error) {
  logger.error('Payment processing failed', {
    error: {
      message: error.message,
      code: error.code,
      stack: error.stack
    },
    context: {
      orderId: order.id,
      userId: user.id,
      amount: order.total,
      provider: 'stripe',
      attempt: retryCount
    },
    action: 'Retry scheduled in 5 minutes'
  });

  // Don't expose internals to user
  throw new UserFacingError('Payment failed. Please try again.');
}
```

### Error Sampling

```javascript
// For high-volume errors, sample to avoid log flood
const errorCounts = new Map();

function logSampledError(key, error, context) {
  const count = (errorCounts.get(key) || 0) + 1;
  errorCounts.set(key, count);

  // Log first occurrence, then every 100th
  if (count === 1 || count % 100 === 0) {
    logger.error(error.message, { ...context, occurrences: count });
  }
}
```

---

## Performance Logging

```javascript
// Request duration
app.use((req, res, next) => {
  const start = Date.now();

  res.on('finish', () => {
    const duration = Date.now() - start;
    const level = duration > 1000 ? 'warn' : 'info';

    logger[level]('Request completed', {
      method: req.method,
      path: req.path,
      status: res.statusCode,
      duration,
      requestId: req.id
    });
  });

  next();
});

// Database query timing
async function query(sql, params) {
  const start = Date.now();
  try {
    return await db.query(sql, params);
  } finally {
    const duration = Date.now() - start;
    if (duration > 100) {
      logger.warn('Slow query', { sql: sql.substring(0, 100), duration });
    }
  }
}
```

---

## Logging Checklist

### Configuration
- [ ] Structured JSON logging
- [ ] Log levels configurable per environment
- [ ] Correlation IDs in all logs
- [ ] Service name and version included

### Content
- [ ] No secrets in logs
- [ ] No raw PII in logs
- [ ] Errors include stack traces
- [ ] Business events logged at INFO
- [ ] Performance anomalies logged

### Operations
- [ ] Logs shipped to central system
- [ ] Log retention policy defined
- [ ] Alerts configured for ERROR level
- [ ] Log volume monitored
