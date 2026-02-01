# Error Recovery Reference (v3.0)

Complete documentation of error classification, recovery strategies, and retry logic.

---

## Error Classification System

### Classification Categories

| Category | Description | Auto-Retry | Max Retries |
|----------|-------------|------------|-------------|
| `network` | Connection failures, timeouts | Yes | 3 |
| `rate_limit` | API rate limiting | Yes (with delay) | 3 |
| `timeout` | Operation timeout | Yes | 2 |
| `syntax` | Code/config syntax errors | No (fix needed) | 0 |
| `permission` | Access denied | No (user action) | 0 |
| `resource` | Resource exhaustion | Yes (with delay) | 2 |
| `validation` | Input validation failures | No (fix needed) | 0 |
| `external` | Third-party service errors | Yes | 2 |
| `unknown` | Unclassified errors | Log only | 1 |

---

## Classification Logic

### Pattern Matching

```python
ERROR_PATTERNS = {
    'network': [
        r'ECONNREFUSED',
        r'ENOTFOUND',
        r'ETIMEDOUT',
        r'ECONNRESET',
        r'network error',
        r'connection refused',
        r'DNS lookup failed',
        r'socket hang up'
    ],
    'rate_limit': [
        r'rate limit',
        r'too many requests',
        r'429',
        r'quota exceeded',
        r'throttl'
    ],
    'timeout': [
        r'timeout',
        r'timed out',
        r'deadline exceeded',
        r'ESOCKETTIMEDOUT'
    ],
    'syntax': [
        r'SyntaxError',
        r'ParseError',
        r'Unexpected token',
        r'Invalid syntax',
        r'YAML.*error',
        r'JSON.*parse'
    ],
    'permission': [
        r'EACCES',
        r'EPERM',
        r'permission denied',
        r'access denied',
        r'unauthorized',
        r'403',
        r'not authorized'
    ],
    'resource': [
        r'ENOMEM',
        r'ENOSPC',
        r'out of memory',
        r'disk full',
        r'no space left',
        r'resource exhausted'
    ],
    'validation': [
        r'ValidationError',
        r'Invalid.*value',
        r'required field',
        r'must be.*type'
    ],
    'external': [
        r'502',
        r'503',
        r'504',
        r'bad gateway',
        r'service unavailable',
        r'upstream.*error'
    ]
}
```

### Classification Function

```python
def classify_error(error_message: str, tool: str = None) -> str:
    """Classify error by pattern matching."""
    message = error_message.lower()

    for category, patterns in ERROR_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, message, re.IGNORECASE):
                return category

    return 'unknown'
```

---

## Retry Strategies

### Exponential Backoff (Network/External)

```
Attempt 1: Immediate
Attempt 2: Wait 2 seconds
Attempt 3: Wait 4 seconds
Attempt 4: Wait 8 seconds (if allowed)
```

```python
def calculate_backoff(attempt: int, base: float = 2.0) -> float:
    """Calculate exponential backoff delay."""
    return min(base ** attempt, 60)  # Cap at 60 seconds
```

### Rate Limit Handling

```
1. Check Retry-After header if present
2. Default: Wait 60 seconds
3. If no header and repeated failures: Double wait time
```

```python
def get_rate_limit_delay(headers: dict, attempt: int) -> float:
    """Get delay for rate limit retry."""
    if 'Retry-After' in headers:
        return float(headers['Retry-After'])

    # Default: 60s, doubled per attempt
    return min(60 * (2 ** (attempt - 1)), 300)  # Cap at 5 minutes
```

### Timeout Extension

```
Original timeout: T
Attempt 2: T * 1.5
Attempt 3: T * 2
```

---

## Recovery Actions by Category

### Network Errors

```
1. Log error with full context
2. Wait (exponential backoff)
3. Retry original operation
4. If max retries exceeded:
   - Add to work queue as S1 issue
   - Suggest user check network
   - Continue with other work
```

**User Message:**
```
[Recovery] Network error encountered. Retrying in {delay}s...
```

### Rate Limit Errors

```
1. Log rate limit hit
2. Check for Retry-After header
3. Wait specified or default time
4. Retry operation
5. If repeated failures:
   - Pause all API operations
   - Alert user
   - Wait for reset period
```

**User Message:**
```
[Recovery] Rate limit reached. Waiting {delay}s before continuing...
```

### Syntax Errors

```
1. Extract error location (file:line)
2. Extract error description
3. Add to work queue as S0 (critical)
4. Do NOT retry (would fail again)
5. Continue to next task
```

**User Message:**
```
[Recovery] Syntax error detected in {file}:{line}
           Adding fix to work queue as S0 priority.
```

### Permission Errors

```
1. Log full error context
2. Identify required permission
3. Escalate to user immediately
4. Pause affected operations
5. Provide fix instructions
```

**User Message:**
```
[Recovery] Permission denied: {operation}
           Required: {permission}

           To fix:
           - {specific instructions}
```

### Resource Errors

```
1. Identify exhausted resource
2. If memory: Suggest GC or process restart
3. If disk: Suggest cleanup
4. Wait and retry (resource may free)
5. If persistent: Escalate to user
```

**User Message:**
```
[Recovery] Resource exhausted: {resource}
           Waiting for resources to free...
```

### Validation Errors

```
1. Extract validation failures
2. Identify invalid input source
3. Add to work queue as S1
4. Do NOT retry
5. Provide specific fix guidance
```

**User Message:**
```
[Recovery] Validation failed: {field} - {reason}
           Fix required before proceeding.
```

### External Service Errors

```
1. Log service and error
2. Check service status page (if known)
3. Retry with backoff
4. If max retries:
   - Mark operation as blocked
   - Continue with other work
   - Alert user to service issue
```

**User Message:**
```
[Recovery] External service error: {service}
           Status: {status}
           Retrying in {delay}s...
```

---

## Error State File

### Location
```
.claude/state/errors/classified.json
```

### Schema

```json
{
  "errors": [
    {
      "id": "err-uuid-001",
      "timestamp": "2026-01-29T10:30:00Z",
      "classification": "network",
      "tool": "WebFetch",
      "operation": "Fetch API documentation",
      "message": "ECONNREFUSED 127.0.0.1:3000",
      "context": {
        "url": "http://localhost:3000/api/docs",
        "method": "GET"
      },
      "retry": {
        "count": 2,
        "max": 3,
        "next_attempt": "2026-01-29T10:30:08Z",
        "strategy": "exponential_backoff"
      },
      "status": "pending_retry",
      "resolution": null
    }
  ],
  "summary": {
    "total": 5,
    "by_status": {
      "pending_retry": 1,
      "recovered": 3,
      "escalated": 1
    },
    "by_classification": {
      "network": 2,
      "syntax": 1,
      "rate_limit": 1,
      "permission": 1
    }
  }
}
```

---

## Hook Integration

### PostToolUseFailure Hook

**Trigger:** Any tool execution failure

**Input (stdin):**
```json
{
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test"
  },
  "error": "Command failed with exit code 1"
}
```

**Processing:**
```python
#!/usr/bin/env python3
import sys
import json

def handle_tool_failure():
    input_data = json.load(sys.stdin)

    tool = input_data.get('tool_name')
    error = input_data.get('error', '')

    # Classify error
    classification = classify_error(error, tool)

    # Get recovery strategy
    strategy = RECOVERY_STRATEGIES.get(classification)

    # Execute recovery
    if strategy['auto_retry']:
        result = attempt_retry(input_data, strategy)
        if result['success']:
            print(f"[Recovery] Recovered from {classification} error")
            return

    # If not auto-recoverable, add to queue
    add_to_work_queue({
        'priority': strategy['priority'],
        'title': f"Fix {classification} error in {tool}",
        'details': error
    })

    print(f"[Recovery] {classification} error added to work queue")
```

**Output (stdout):**
```
[Recovery] Classified as: network
[Recovery] Retry 1/3 in 2s...
[Recovery] Retry successful
```

---

## Recovery Decision Tree

```
Error Occurs
    │
    ▼
Classify Error
    │
    ├─── network ──────► Retry with backoff ──► Success? ──► Continue
    │                                              │
    │                                              └─► Add to queue
    │
    ├─── rate_limit ───► Wait for reset ──────► Retry ──► Continue
    │
    ├─── timeout ──────► Extend timeout ──────► Retry ──► Continue
    │
    ├─── syntax ───────► Add to queue (S0) ───► Continue other work
    │
    ├─── permission ───► Escalate to user ────► Pause
    │
    ├─── resource ─────► Wait and retry ──────► Escalate if fails
    │
    ├─── validation ───► Add to queue (S1) ───► Continue other work
    │
    ├─── external ─────► Retry with backoff ──► Mark blocked if fails
    │
    └─── unknown ──────► Log and continue ────► Alert if repeated
```

---

## Loop Integration

### Error During BUILD Phase

```
1. error-recovery.py classifies error
2. If auto-recoverable:
   - Attempt recovery
   - If success: Continue BUILD
   - If fail: Add to queue
3. If not recoverable:
   - Add to queue with appropriate severity
   - Continue to next item
4. Phase completes when:
   - All items processed OR
   - Unrecoverable error with empty queue
```

### Error During TEST Phase

```
1. Test failure is NOT an error (expected behavior)
2. Actual errors (syntax, permission):
   - Classify and handle
   - Add fix to queue
   - Re-run tests after fix
```

### Error During QUALITY Phase

```
1. Gate failure adds item to queue
2. Infrastructure error (tool not found):
   - Escalate to user
   - Skip gate with warning
```

---

## User Escalation

### When to Escalate

- Permission errors (always)
- Max retries exceeded for critical operation
- User input required
- Resource errors not auto-resolvable
- Unknown errors repeated 3+ times

### Escalation Format

```
╭─────────────────────────────────────────────────────────╮
│  User Action Required                                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Error: Permission denied accessing ./secure/config.json │
│                                                          │
│  Classification: permission                              │
│  Attempts: 1 (no retry - user action needed)            │
│                                                          │
│  To resolve:                                             │
│  1. Check file permissions: ls -la ./secure/            │
│  2. Grant read access: chmod +r ./secure/config.json    │
│  3. Say "continue" to retry                             │
│                                                          │
│  Or say "skip" to continue without this operation       │
│                                                          │
╰─────────────────────────────────────────────────────────╯
```

---

## Metrics & Monitoring

### Tracked Metrics

| Metric | Description |
|--------|-------------|
| `error_total` | Total errors encountered |
| `error_by_class` | Count per classification |
| `recovery_success` | Successful auto-recoveries |
| `recovery_failure` | Failed recovery attempts |
| `escalation_count` | User escalations |
| `mean_retry_count` | Average retries before success |

### Session Summary

```
Error Recovery Summary
━━━━━━━━━━━━━━━━━━━━━

Total Errors: 8

By Classification:
  network:     3 (all recovered)
  rate_limit:  1 (recovered)
  syntax:      2 (fixed via queue)
  permission:  1 (user resolved)
  unknown:     1 (logged)

Recovery Rate: 87.5%
Escalations: 1
```

---

## Best Practices

### For Hook Authors

1. Always output classification for transparency
2. Include retry count in messages
3. Provide actionable fix suggestions
4. Log full context for debugging
5. Respect max retry limits

### For Loop Integration

1. Don't halt loop for recoverable errors
2. Prioritize S0 fixes over new work
3. Verify fixes before continuing
4. Track error patterns across iterations

### For Users

1. Check permissions before starting long operations
2. Ensure network connectivity for external operations
3. Review escalation messages promptly
4. Use `--dry-run` to catch errors early

---

## See Also

| Document | Purpose |
|----------|---------|
| [HOOKS_REFERENCE](HOOKS_REFERENCE.md) | Hook implementation details |
| [STATE_FILES](STATE_FILES.md) | State file schemas |
| [LOOP_WORKFLOW](LOOP_WORKFLOW.md) | Loop execution flow |
