---
name: self-critique
description: After generating code, identify potential issues and fix them before presenting
model: sonnet
version: 1.0.0
tags: [quality, verification, code-generation]
---

# Self-Critique

After generating code or solutions, systematically identify potential issues and fix them before presenting the final result.

## Description

This skill implements the **Verification Loop** - after generating output, the AI critiques its own work, identifies flaws, and fixes them. This catches errors that slip past single-pass generation.

The pattern: Generate → Critique → Fix → Present

Triggers on: code generation, solution proposals, implementation tasks

---

## When to Apply

### Always Self-Critique

| Output Type | Why |
|-------------|-----|
| New code | Bugs, edge cases, security issues |
| Bug fixes | May introduce new bugs |
| Refactoring | Behavior changes, regressions |
| API designs | Breaking changes, usability issues |
| Configuration | Security, correctness |
| Scripts | Destructive operations, edge cases |

### Skip Self-Critique For

- Simple lookups/queries
- Explanations (no code)
- When user says "quick draft" or "rough idea"

---

## The Self-Critique Process

### Step 1: Generate Initial Solution

```python
# Initial implementation
def process_payment(user_id, amount):
    user = get_user(user_id)
    if user.balance >= amount:
        user.balance -= amount
        return {"success": True}
    return {"success": False}
```

### Step 2: Critique (Ask These Questions)

```markdown
## Self-Critique Checklist

### Correctness
- [ ] Does it handle null/undefined inputs?
- [ ] Are there off-by-one errors?
- [ ] Does it handle empty collections?
- [ ] Are comparisons correct (>, >=, ==)?

### Edge Cases
- [ ] What if input is 0? Negative?
- [ ] What if collection is empty?
- [ ] What if string is empty/whitespace?
- [ ] What about concurrent access?

### Security
- [ ] Input validation present?
- [ ] SQL injection possible?
- [ ] XSS possible?
- [ ] Sensitive data exposed in logs/errors?

### Error Handling
- [ ] What exceptions can be thrown?
- [ ] Are they caught appropriately?
- [ ] Are error messages helpful?
- [ ] Is there proper cleanup on failure?

### Performance
- [ ] Any N+1 queries?
- [ ] Unbounded loops/recursion?
- [ ] Memory leaks possible?
- [ ] Missing indexes for queries?

### Maintainability
- [ ] Are names clear and descriptive?
- [ ] Is complexity reasonable?
- [ ] Would a new developer understand this?
- [ ] Are magic numbers extracted?
```

### Step 3: Identify Issues

```markdown
## Issues Found

1. **No input validation** - user_id could be None/invalid
2. **Race condition** - balance check and deduction not atomic
3. **No error handling** - get_user could throw
4. **Missing logging** - no audit trail for payments
5. **Floating point** - using float for money is dangerous
```

### Step 4: Fix and Present

```python
# Revised implementation with fixes

from decimal import Decimal
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)

class PaymentError(Exception):
    """Base exception for payment errors."""
    pass

class InsufficientFundsError(PaymentError):
    """Raised when user has insufficient balance."""
    pass

def process_payment(user_id: str, amount: Decimal) -> dict:
    """
    Process a payment by deducting from user balance.

    Args:
        user_id: The user's unique identifier
        amount: Payment amount (must be positive)

    Returns:
        dict with 'success' and 'transaction_id'

    Raises:
        PaymentError: If payment cannot be processed
        InsufficientFundsError: If balance is too low
    """
    # Input validation
    if not user_id:
        raise PaymentError("user_id is required")
    if not isinstance(amount, Decimal) or amount <= 0:
        raise PaymentError("amount must be a positive Decimal")

    try:
        # Atomic balance update with row locking
        with db.transaction():
            user = get_user_for_update(user_id)  # SELECT FOR UPDATE

            if user is None:
                raise PaymentError(f"User not found: {user_id}")

            if user.balance < amount:
                logger.warning(
                    "Insufficient funds",
                    extra={"user_id": user_id, "amount": str(amount)}
                )
                raise InsufficientFundsError("Insufficient balance")

            user.balance -= amount
            transaction_id = create_transaction_record(user_id, amount)

            logger.info(
                "Payment processed",
                extra={
                    "user_id": user_id,
                    "amount": str(amount),
                    "transaction_id": transaction_id
                }
            )

            return {
                "success": True,
                "transaction_id": transaction_id
            }

    except PaymentError:
        raise
    except Exception as e:
        logger.exception("Unexpected error processing payment")
        raise PaymentError("Payment processing failed") from e
```

---

## Output Format

When presenting code after self-critique:

```markdown
## Implementation

[Code here]

## Self-Critique Applied

I reviewed this code for potential issues. Here's what I found and fixed:

| Issue | Severity | Fix Applied |
|-------|----------|-------------|
| No input validation | High | Added type and value checks |
| Race condition | Critical | Added transaction with row locking |
| No error handling | Medium | Added try/except with specific errors |
| Missing logging | Low | Added structured logging |
| Float for money | High | Changed to Decimal |

## Remaining Considerations

- [ ] May want to add retry logic for transient DB failures
- [ ] Consider adding idempotency key for duplicate prevention
```

---

## Critique Templates

### For Functions

```markdown
### Reviewing: [function_name]

**Purpose check:** Does it do what the name suggests?
**Input check:** All parameters validated?
**Output check:** Return type consistent? All paths return?
**Error check:** What can fail? Is it handled?
**Edge cases:** Empty input? Null? Negative? Very large?
```

### For API Endpoints

```markdown
### Reviewing: [endpoint]

**Auth check:** Is authentication required? Applied?
**Input check:** All body/query params validated?
**Output check:** Response format consistent?
**Error responses:** Are error codes correct?
**Rate limiting:** Should there be limits?
**Logging:** Are requests/errors logged?
```

### For Database Queries

```markdown
### Reviewing: [query/migration]

**Injection check:** Using parameterized queries?
**Performance check:** Will it use indexes? EXPLAIN?
**Nullability check:** Handling NULL correctly?
**Transaction check:** Needs to be atomic?
**Rollback check:** Can this be reversed?
```

### For Scripts

```markdown
### Reviewing: [script]

**Destructive check:** Does it delete/modify data?
**Idempotent check:** Safe to run twice?
**Error check:** What if something fails midway?
**Permissions check:** Does it need elevated privileges?
**Confirmation check:** Should it prompt before destructive ops?
```

---

## Integration with Loop

The self-critique happens in the BUILD phase:

```
Phase 4: BUILD
├── Generate initial solution
├── Run self-critique checklist
├── Identify issues (aim for 3+)
├── Fix identified issues
├── Document what was fixed
└── Present final solution
```

---

## Configuration

### Critique Depth Levels

| Level | Checks | Use When |
|-------|--------|----------|
| `quick` | Correctness, obvious errors | Simple changes, time pressure |
| `standard` | + Edge cases, error handling | Normal development |
| `thorough` | + Security, performance, maintainability | Critical code |
| `paranoid` | + All security vectors, abuse cases | Auth, payments, PII |

### Enable/Disable

```
# Enable thorough critique
"Review this code thoroughly before presenting"

# Skip critique
"Give me a quick draft, I'll review it myself"

# Specific focus
"Critique this specifically for security issues"
```

---

## Best Practices

### Do
- Always find at least 3 potential issues (they exist)
- Fix issues before presenting (don't just list them)
- Document what was fixed (builds trust)
- Be specific about remaining considerations

### Don't
- Skip critique for "simple" code (bugs hide there)
- Only look for one type of issue
- Present unfixed code with a list of problems
- Over-engineer fixes beyond the scope
