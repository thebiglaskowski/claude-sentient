---
name: error-classifier
description: Classifies errors by type, suggests recovery strategies, and routes to appropriate handlers
version: 3.0.0
triggers:
  - error
  - failed
  - exception
  - crash
  - timeout
model: haiku
tags: [orchestration, error-handling, recovery]
context: minimal
---

# Error Classifier

Automatically classifies errors by type and severity, suggests recovery strategies, and routes to appropriate handlers. Integrates with the error-recovery hook for automated retry logic.

---

## Error Classification Matrix

### By Type

| Type | Pattern | Severity | Recovery |
|------|---------|----------|----------|
| **Network** | ETIMEDOUT, ECONNRESET, ECONNREFUSED | Transient | Retry with backoff |
| **Rate Limit** | 429, quota exceeded, too many requests | Transient | Wait and retry |
| **Auth** | 401, 403, unauthorized, forbidden | Blocking | User intervention |
| **Not Found** | 404, ENOENT, module not found | Actionable | Fix path/install |
| **Validation** | 400, 422, invalid, malformed | Actionable | Fix input |
| **Type** | TypeError, type error, TS\d{4} | Code Issue | Fix code |
| **Syntax** | SyntaxError, parse error | Code Issue | Fix code (priority) |
| **Permission** | EACCES, EPERM, permission denied | Blocking | User intervention |
| **Resource** | ENOSPC, ENOMEM, out of memory | Blocking | User intervention |
| **Timeout** | timeout, deadline exceeded | Transient | Retry with longer timeout |
| **Conflict** | 409, lock, merge conflict | Actionable | Resolve conflict |
| **Server** | 500, 502, 503, internal error | Transient | Retry or escalate |

### By Severity

| Severity | Criteria | Action |
|----------|----------|--------|
| **S0 - Critical** | Blocks all progress, data at risk | Stop, alert user |
| **S1 - High** | Blocks current task | Add to queue as priority |
| **S2 - Medium** | Degrades functionality | Add to queue |
| **S3 - Low** | Minor issue, workaround exists | Log, continue |

---

## Classification Process

```
Error Received
    │
    ▼
┌─────────────────┐
│ Pattern Match   │ ──▶ Identify error type
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Assess Severity │ ──▶ S0/S1/S2/S3
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Check Retryable │ ──▶ Transient? Attempt retry?
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌───────┐ ┌───────────┐
│ Retry │ │ Route/Fix │
└───────┘ └───────────┘
```

---

## Recovery Strategies

### Transient Errors (Auto-Retry)
```
Network Errors:
├── Attempt 1: Wait 2s
├── Attempt 2: Wait 4s
├── Attempt 3: Wait 8s
└── Escalate after 3 failures

Rate Limits:
├── Read Retry-After header
├── Default: Wait 60s
├── Max 3 retries
└── Escalate if persistent

Timeouts:
├── Increase timeout 2x
├── Max 2 retries
└── Consider breaking into smaller ops
```

### Actionable Errors (Queue for Fix)
```
Module Not Found:
├── Identify missing package
├── Suggest: npm install <package>
├── Auto-add to work queue

Type Errors:
├── Extract file:line
├── Classify as S1
├── Add fix task to queue

Syntax Errors:
├── Extract file:line
├── Classify as S0
├── Add fix task to queue (priority)

Validation Errors:
├── Extract validation message
├── Identify invalid field
├── Suggest correction
```

### Blocking Errors (User Intervention)
```
Permission Denied:
├── Log clear message
├── Suggest: Check file permissions
├── Pause for user

Auth Failed:
├── Log clear message
├── Suggest: Check credentials
├── Pause for user

Out of Memory:
├── Log current memory usage
├── Suggest: Increase Node memory
├── Pause for user

Disk Full:
├── Log disk usage
├── Suggest: Free space
├── Pause for user
```

---

## Error Response Format

### Standard Error Report
```markdown
## Error Detected

**Type:** Network Error (ETIMEDOUT)
**Severity:** S2 - Medium (transient)
**Location:** src/api/client.ts:42

### Details
```
Error: connect ETIMEDOUT 192.168.1.1:443
    at TCPConnectWrap.afterConnect [as oncomplete]
```

### Classification
- Retryable: Yes
- Attempts: 1/3
- Backoff: 2s → 4s → 8s

### Recovery Strategy
Automatic retry with exponential backoff.
Will escalate after 3 failed attempts.

### Action
⏳ Retrying in 2 seconds...
```

### Actionable Error Report
```markdown
## Error Detected

**Type:** Module Not Found
**Severity:** S1 - High (blocking)
**Location:** src/index.ts:5

### Details
```
Error: Cannot find module 'lodash'
```

### Classification
- Retryable: No
- Recoverable: Yes (install dependency)

### Recovery Strategy
Install missing dependency.

### Suggested Command
```bash
npm install lodash
```

### Action
Adding to work queue as S1 priority.
```

---

## Integration with Hooks

### Error Recovery Hook (PostToolUseFailure)
```python
# error-recovery.py processes errors automatically
# This skill provides classification logic

Input: Error from failed tool
Output: Recovery action (retry, queue, escalate)
```

### Workflow
```
Tool Fails → error-recovery.py hook triggers
          → Classifies error using this skill's logic
          → Returns recovery action
          → Loop continues or pauses based on action
```

---

## Queue Integration

### Adding to Work Queue
```
Error classified as actionable:
1. Extract error details
2. Create work queue item:
   - Subject: "Fix: [error type] in [file]"
   - Description: Error details + suggested fix
   - Severity: Based on classification
   - Priority: S0/S1 at top of queue
3. Continue with next queue item
```

### Queue Item Format
```json
{
  "subject": "Fix: SyntaxError in src/api/users.ts",
  "description": "Unexpected token at line 42. Missing closing bracket.",
  "severity": "S0",
  "source": "error-classifier",
  "metadata": {
    "errorType": "SyntaxError",
    "file": "src/api/users.ts",
    "line": 42,
    "originalError": "Unexpected token '}'"
  }
}
```

---

## Common Error Patterns

### JavaScript/TypeScript
```
SyntaxError: Unexpected token     → Missing bracket/paren
TypeError: Cannot read property   → Null check needed
ReferenceError: X is not defined → Import missing
RangeError: Maximum call stack   → Infinite recursion
```

### Node.js
```
ENOENT: no such file or directory → Path incorrect
EACCES: permission denied         → File permissions
EADDRINUSE: address already in use → Port conflict
EMFILE: too many open files       → Resource leak
```

### Git
```
.git/index.lock exists            → Remove lock file
merge conflict                    → Resolve conflicts
cannot lock ref                   → Stale locks
```

### Database
```
Connection refused                → DB not running
Deadlock detected                → Retry transaction
Unique constraint violated       → Duplicate data
```

---

## Severity Guidelines

### S0 - Critical (Immediate)
- Syntax errors (code won't run)
- Security vulnerabilities discovered
- Data corruption risk
- Build completely broken

### S1 - High (Priority)
- Type errors blocking compilation
- Test failures
- Missing dependencies
- Auth/permission issues

### S2 - Medium (Soon)
- Linting errors
- Deprecation warnings
- Performance issues
- Minor functionality broken

### S3 - Low (When Convenient)
- Style issues
- Documentation gaps
- Minor warnings
- Optimization opportunities

---

## Configuration

```json
{
  "errorClassifier": {
    "autoRetry": {
      "enabled": true,
      "maxAttempts": 3,
      "backoff": "exponential",
      "baseDelay": 2000
    },
    "queueOnError": {
      "enabled": true,
      "minSeverity": "S2"
    },
    "escalateOn": ["auth", "permission", "resource"]
  }
}
```
