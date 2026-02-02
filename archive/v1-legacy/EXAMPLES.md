# Prompt Examples

Real-world examples showing expected outputs from key prompts.

---

## Table of Contents

1. [Feature Spec Writer](#1-feature-spec-writer)
2. [Blueprint Auditor](#2-blueprint-auditor)
3. [Code Review](#3-code-review)
4. [Security Audit](#4-security-audit)
5. [Bug Hunt](#5-bug-hunt)
6. [Codebase Audit](#6-codebase-audit)
7. [Refactoring Engine](#7-refactoring-engine)
8. [Test Coverage Gate](#8-test-coverage-gate)
9. [Release Checklist](#9-release-checklist)
10. [Incident Postmortem](#10-incident-postmortem)
11. [Autonomous Loop](#11-autonomous-loop)
12. [Swarm Mode](#12-swarm-mode)
13. [Task Dependencies](#13-task-dependencies)

---

## 1. Feature Spec Writer

**Input:**
```
Create a spec for user authentication with OAuth support
```

**Output:**

```markdown
# Feature Specification: User Authentication with OAuth

## Overview
Implement user authentication supporting both email/password and OAuth providers (Google, GitHub).

## User Stories

### US-001: Email Registration
As a new user, I want to register with my email and password so that I can create an account.

**Acceptance Criteria:**
- [ ] Email validation (format and uniqueness)
- [ ] Password minimum 12 characters with complexity requirements
- [ ] Email verification link sent on registration
- [ ] Account created in "pending" state until verified

### US-002: OAuth Login
As a user, I want to log in with my Google or GitHub account so that I don't need to remember another password.

**Acceptance Criteria:**
- [ ] "Continue with Google" button on login page
- [ ] "Continue with GitHub" button on login page
- [ ] First OAuth login creates account automatically
- [ ] Subsequent logins link to existing account by email

### US-003: Session Management
As a logged-in user, I want my session to persist so that I don't have to log in repeatedly.

**Acceptance Criteria:**
- [ ] Session persists for 7 days with activity
- [ ] Session expires after 30 minutes of inactivity
- [ ] "Remember me" option extends session to 30 days
- [ ] Logout invalidates session immediately

## Technical Requirements

### Data Model
```
User {
  id: UUID
  email: string (unique)
  password_hash: string (nullable for OAuth-only)
  email_verified: boolean
  oauth_providers: OAuthLink[]
  created_at: timestamp
  updated_at: timestamp
}

OAuthLink {
  provider: enum (google, github)
  provider_id: string
  user_id: UUID
}

Session {
  id: UUID
  user_id: UUID
  expires_at: timestamp
  created_at: timestamp
}
```

### API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/register | Email registration |
| POST | /api/auth/login | Email login |
| POST | /api/auth/logout | End session |
| GET | /api/auth/oauth/google | Initiate Google OAuth |
| GET | /api/auth/oauth/github | Initiate GitHub OAuth |
| GET | /api/auth/oauth/callback | OAuth callback handler |
| POST | /api/auth/verify-email | Verify email token |

### Security Requirements
- Passwords hashed with bcrypt (cost 12)
- Sessions stored server-side (not JWT)
- CSRF protection on all forms
- Rate limiting: 5 failed logins per 15 minutes
- OAuth state parameter for CSRF protection

## Out of Scope
- Password reset (separate feature)
- Two-factor authentication (future enhancement)
- Social login with Facebook/Twitter

## Dependencies
- OAuth credentials for Google and GitHub
- Email service for verification emails
- Redis for session storage

## Estimation
- Backend: 3-4 days
- Frontend: 2-3 days
- Testing: 1-2 days
- **Total: 6-9 days**
```

---

## 2. Blueprint Auditor

**Input:**
```
Audit the authentication feature spec above
```

**Output:**

```markdown
# Blueprint Audit Report

## Summary
| Category | Status |
|----------|--------|
| Completeness | PASS |
| Feasibility | PASS |
| Security | WARN |
| Testability | PASS |
| Dependencies | PASS |

**Overall: APPROVED WITH RECOMMENDATIONS**

## Findings

### S1 — High Priority

#### AUDIT-001: Missing Rate Limiting Specification
**Location:** Security Requirements
**Issue:** Rate limiting specified as "5 failed logins per 15 minutes" but no specification for:
- What happens after limit reached (lockout duration?)
- Whether limit is per-IP, per-account, or both
- How to handle distributed attacks

**Recommendation:** Add explicit lockout policy:
```
- Account lockout: 15 minutes after 5 failures
- IP-based blocking: 1 hour after 20 failures across accounts
- CAPTCHA triggered after 3 failures
```

### S2 — Medium Priority

#### AUDIT-002: OAuth Token Storage Not Specified
**Location:** Technical Requirements > Data Model
**Issue:** OAuthLink stores provider_id but not access/refresh tokens. If we need to call provider APIs on behalf of user, we need these.

**Recommendation:** Clarify if OAuth is login-only or if we need API access. If API access needed:
```
OAuthLink {
  ...
  access_token: encrypted string
  refresh_token: encrypted string
  token_expires_at: timestamp
}
```

#### AUDIT-003: Session Invalidation on Password Change
**Location:** US-003 Session Management
**Issue:** No mention of invalidating sessions when user changes password.

**Recommendation:** Add acceptance criteria:
- [ ] All sessions invalidated when password changes
- [ ] Option to "log out all devices"

### S3 — Low Priority

#### AUDIT-004: Email Verification Expiry
**Location:** US-001 Email Registration
**Issue:** No expiry specified for email verification links.

**Recommendation:** Add: "Verification links expire after 24 hours"

## Checklist Verification

- [x] All user stories have acceptance criteria
- [x] Data model supports all features
- [x] API endpoints cover all operations
- [x] Security requirements documented
- [x] Dependencies identified
- [x] Estimation provided
- [ ] Error handling specified (MISSING)
- [ ] Monitoring/logging requirements (MISSING)

## Recommendations Before Implementation

1. **Required:** Address AUDIT-001 (rate limiting details)
2. **Required:** Add error response specifications
3. **Suggested:** Address AUDIT-002 if OAuth API access needed
4. **Suggested:** Add logging requirements for security events
```

---

## 3. Code Review

**Input:**
```javascript
// auth.js - Review this authentication code
async function login(email, password) {
  const user = await db.query(`SELECT * FROM users WHERE email = '${email}'`);
  if (!user) return { error: 'User not found' };

  if (user.password === password) {
    const token = Math.random().toString(36);
    return { token, user };
  }
  return { error: 'Invalid password' };
}
```

**Output:**

```markdown
# Code Review: auth.js

## Summary
Critical security vulnerabilities found. **Cannot approve.**

## Risk Level
**CRITICAL**

## Findings

### Blockers (Must Fix)

1. **[auth.js:2]** - Security
   - **Issue:** SQL Injection vulnerability. User input directly interpolated into query.
   - **Impact:** Attacker can extract entire database, bypass authentication, or delete data.
   - **Suggestion:** Use parameterized queries:
     ```javascript
     const user = await db.query('SELECT * FROM users WHERE email = $1', [email]);
     ```

2. **[auth.js:5]** - Security
   - **Issue:** Plain text password comparison. Passwords should never be stored or compared in plain text.
   - **Impact:** Database breach exposes all user passwords.
   - **Suggestion:** Use bcrypt:
     ```javascript
     const valid = await bcrypt.compare(password, user.password_hash);
     ```

3. **[auth.js:6]** - Security
   - **Issue:** Weak token generation using Math.random(). This is predictable and not cryptographically secure.
   - **Impact:** Attacker can predict tokens and hijack sessions.
   - **Suggestion:** Use crypto:
     ```javascript
     const token = crypto.randomBytes(32).toString('hex');
     ```

### Major Issues (Should Fix)

1. **[auth.js:3]** - Security
   - **Issue:** Different error messages for "user not found" vs "invalid password" enable user enumeration.
   - **Suggestion:** Use generic message: `{ error: 'Invalid credentials' }`

2. **[auth.js:7]** - Security
   - **Issue:** Returning full user object may expose sensitive fields (password hash, internal IDs).
   - **Suggestion:** Return only necessary fields:
     ```javascript
     return { token, user: { id: user.id, email: user.email } };
     ```

### Minor Issues

1. **[auth.js:1]** - Maintainability
   - **Issue:** No input validation before database query.
   - **Suggestion:** Validate email format before querying.

## Verdict
- [ ] Approved
- [ ] Approved with minor changes
- [x] **Changes requested**
- [ ] Needs discussion

## Checklist Verification
- [ ] Correctness verified — FAIL (security issues)
- [ ] Security considered — FAIL (multiple critical vulnerabilities)
- [ ] Tests adequate — NOT PROVIDED
- [ ] Documentation updated — NOT PROVIDED
```

---

## 4. Security Audit

**Input:**
```
Audit the user authentication module at src/auth/
```

**Output:**

```markdown
# Security Audit Report: Authentication Module

## Executive Summary
The authentication module contains **2 critical** and **3 high** severity vulnerabilities requiring immediate attention. The module should not be deployed until these issues are resolved.

## Scope
- `src/auth/login.ts`
- `src/auth/register.ts`
- `src/auth/session.ts`
- `src/middleware/auth.ts`

## Findings

### VULN-001: Timing Attack on Password Comparison

**Severity:** High

**Category:** A07 - Authentication Failures

**Location:** `src/auth/login.ts:45`

**Description:**
Password comparison uses string equality (`===`) which is vulnerable to timing attacks. The comparison short-circuits on first character mismatch, leaking information about password correctness.

**Evidence:**
```typescript
if (user.passwordHash === providedHash) {
  return createSession(user);
}
```

**Impact:**
Attacker can determine correct password characters by measuring response times.

**Remediation:**
Use constant-time comparison:
```typescript
import { timingSafeEqual } from 'crypto';
if (timingSafeEqual(Buffer.from(user.passwordHash), Buffer.from(providedHash))) {
  return createSession(user);
}
```

**Verification:**
Run timing analysis tool against login endpoint.

---

### VULN-002: Session Fixation

**Severity:** Critical

**Category:** A07 - Authentication Failures

**Location:** `src/auth/session.ts:23`

**Description:**
Session ID is not regenerated after successful login. An attacker who can set a victim's session ID (via XSS or URL parameter) can hijack the session after login.

**Evidence:**
```typescript
// Session ID preserved across login
async function login(sessionId, user) {
  await redis.set(`session:${sessionId}`, user.id);
}
```

**Impact:**
Complete account takeover.

**Remediation:**
Regenerate session ID on authentication:
```typescript
async function login(oldSessionId, user) {
  await redis.del(`session:${oldSessionId}`);
  const newSessionId = generateSecureId();
  await redis.set(`session:${newSessionId}`, user.id);
  return newSessionId;
}
```

---

### VULN-003: Missing CSRF Protection

**Severity:** High

**Category:** A01 - Broken Access Control

**Location:** `src/auth/login.ts`, `src/auth/register.ts`

**Description:**
Login and registration forms lack CSRF tokens. Attacker can create malicious page that submits forms on behalf of victim.

**Impact:**
- Login CSRF: Force victim to log into attacker's account
- Registration CSRF: Create accounts on victim's behalf

**Remediation:**
Implement CSRF tokens on all state-changing forms.

---

## Risk Summary

| Severity | Count |
|----------|-------|
| Critical | 2 |
| High | 3 |
| Medium | 1 |
| Low | 2 |

## Remediation Priority

1. **Immediate:** VULN-002 (Session Fixation)
2. **Immediate:** VULN-001 (Timing Attack)
3. **This Week:** VULN-003 (CSRF Protection)
```

---

## 5. Bug Hunt

**Input:**
```
Hunt for bugs in the payment processing module
```

**Output:**

```markdown
# Bug Hunt Report: Payment Processing Module

## Summary
Found **1 critical**, **2 major**, and **3 minor** bugs.

## Critical Bugs

### BUG-001: Race Condition in Balance Deduction

**Location:** `src/payments/charge.ts:67-82`

**Severity:** S0 - Critical

**Description:**
Balance check and deduction are not atomic. Two concurrent requests can both pass the balance check, resulting in negative balance.

**Reproduction:**
1. User has $100 balance
2. Simultaneously submit two $100 charges
3. Both pass `if (balance >= amount)` check
4. Both deduct, resulting in -$100 balance

**Evidence:**
```typescript
const balance = await getBalance(userId);
if (balance >= amount) {
  await deductBalance(userId, amount);  // Not atomic!
  await processPayment(amount);
}
```

**Impact:** Financial loss, negative balances, accounting discrepancies.

**Fix:**
```typescript
// Use database transaction with row locking
await db.transaction(async (tx) => {
  const balance = await tx.query(
    'SELECT balance FROM accounts WHERE user_id = $1 FOR UPDATE',
    [userId]
  );
  if (balance < amount) throw new InsufficientFundsError();
  await tx.query(
    'UPDATE accounts SET balance = balance - $1 WHERE user_id = $2',
    [amount, userId]
  );
});
```

---

## Major Bugs

### BUG-002: Floating Point Arithmetic for Currency

**Location:** `src/payments/calculate.ts:15`

**Severity:** S1 - High

**Evidence:**
```typescript
const total = subtotal + (subtotal * taxRate);  // 19.99 + 1.60 = 21.589999...
```

**Impact:** Rounding errors accumulate, financial discrepancies.

**Fix:** Use integer cents or decimal library:
```typescript
const totalCents = subtotalCents + Math.round(subtotalCents * taxRate);
```

### BUG-003: Unhandled Promise Rejection

**Location:** `src/payments/webhook.ts:34`

**Severity:** S1 - High

**Evidence:**
```typescript
app.post('/webhook', (req, res) => {
  processWebhook(req.body);  // No await, no catch
  res.send('OK');
});
```

**Impact:** Webhook failures are silent, payments not processed, no error visibility.

---

## Minor Bugs

### BUG-004: Hardcoded Timeout
**Location:** `src/payments/gateway.ts:12`
**Issue:** `timeout: 5000` hardcoded, should be configurable.

### BUG-005: Missing Null Check
**Location:** `src/payments/receipt.ts:28`
**Issue:** `user.email.toLowerCase()` crashes if email is null.

### BUG-006: Inconsistent Error Codes
**Location:** Multiple files
**Issue:** Some errors return `{ error: 'message' }`, others `{ code: 'ERROR_CODE' }`.

---

## Recommendations

1. **Immediate:** Fix BUG-001 before any production traffic
2. **This Sprint:** Fix BUG-002 and BUG-003
3. **Backlog:** Address minor bugs in next maintenance cycle
```

---

## 6. Codebase Audit

**Input:**
```
Full audit of the project codebase
```

**Output:**

```markdown
# Codebase Audit Report

## Executive Summary

| Category | Score | Status |
|----------|-------|--------|
| Code Quality | 72/100 | Needs Improvement |
| Test Coverage | 64% | Below Target (80%) |
| Security | 68/100 | Needs Improvement |
| Documentation | 45/100 | Poor |
| Dependencies | 85/100 | Good |

**Overall Health: 67/100 — NEEDS ATTENTION**

---

## Code Quality

### Strengths
- Consistent code style (ESLint enforced)
- TypeScript strict mode enabled
- Good separation of concerns in most modules

### Issues Found

| Severity | Count | Category |
|----------|-------|----------|
| S1 | 3 | Dead code |
| S2 | 12 | High complexity functions |
| S2 | 8 | Duplicate code |
| S3 | 24 | Missing type annotations |

### High Complexity Functions (Cyclomatic > 15)
1. `src/orders/validate.ts:processOrder` — CC: 23
2. `src/payments/route.ts:handlePayment` — CC: 18
3. `src/users/permissions.ts:checkAccess` — CC: 16

### Duplicate Code
- `src/api/users.ts:45-67` duplicates `src/api/admin.ts:23-45`
- Similar validation logic in 4 different files

---

## Test Coverage

```
Overall:        64.2%
src/api/:       78.3%
src/services/:  71.2%
src/utils/:     89.1%
src/payments/:  42.1% ← CRITICAL GAP
src/auth/:      51.3% ← SECURITY CRITICAL
```

### Untested Critical Paths
- Payment refund flow (0% coverage)
- Password reset flow (12% coverage)
- Admin user management (8% coverage)

---

## Security

### Vulnerabilities Found
| Severity | Count |
|----------|-------|
| Critical | 1 |
| High | 4 |
| Medium | 7 |

### Critical: SQL Injection
`src/search/query.ts:34` — User input in raw query

### High Severity
- Missing rate limiting on login
- Session tokens in URL parameters
- Sensitive data in error messages
- Missing CSRF on state-changing endpoints

---

## Documentation

### Missing Documentation
- No API documentation
- No architecture overview
- 67% of public functions lack JSDoc
- README outdated (references removed features)

---

## Recommendations

### Immediate (This Week)
1. Fix SQL injection vulnerability
2. Add rate limiting to authentication
3. Increase payment module test coverage

### Short-term (This Month)
1. Refactor high-complexity functions
2. Eliminate duplicate code
3. Add API documentation

### Long-term (This Quarter)
1. Achieve 80% test coverage
2. Complete JSDoc for all public APIs
3. Create architecture documentation
```

---

## 7. Refactoring Engine

**Input:**
```
Refactor the user validation function that has grown too complex
```

**Output:**

```markdown
# Refactoring Plan: User Validation

## Current State Analysis

**File:** `src/users/validate.ts`
**Function:** `validateUser()`
**Lines:** 187
**Cyclomatic Complexity:** 34
**Issues:**
- Multiple responsibilities
- Deep nesting (6 levels)
- Repeated validation patterns
- Hard to test individual rules

## Refactoring Strategy

**Approach:** Extract Method + Strategy Pattern

### Step 1: Extract Validation Rules

**Before:**
```typescript
function validateUser(user: User): ValidationResult {
  const errors = [];

  // Email validation (20 lines)
  if (!user.email) {
    errors.push({ field: 'email', message: 'Required' });
  } else if (!user.email.includes('@')) {
    errors.push({ field: 'email', message: 'Invalid format' });
  } else if (user.email.length > 255) {
    // ... more conditions
  }

  // Password validation (30 lines)
  // ... similar pattern

  // Name validation (15 lines)
  // ... similar pattern

  // 120 more lines...
}
```

**After:**
```typescript
// validators/email.ts
export const emailValidator: Validator<string> = {
  field: 'email',
  validate(value) {
    if (!value) return { valid: false, message: 'Required' };
    if (!value.includes('@')) return { valid: false, message: 'Invalid format' };
    if (value.length > 255) return { valid: false, message: 'Too long' };
    return { valid: true };
  }
};

// validators/password.ts
export const passwordValidator: Validator<string> = {
  field: 'password',
  validate(value) {
    if (!value) return { valid: false, message: 'Required' };
    if (value.length < 12) return { valid: false, message: 'Too short' };
    if (!/[A-Z]/.test(value)) return { valid: false, message: 'Needs uppercase' };
    return { valid: true };
  }
};

// validate.ts
const userValidators = [emailValidator, passwordValidator, nameValidator];

function validateUser(user: User): ValidationResult {
  const errors = userValidators
    .map(v => ({ field: v.field, ...v.validate(user[v.field]) }))
    .filter(r => !r.valid);

  return { valid: errors.length === 0, errors };
}
```

### Step 2: Execution Plan

| Step | Action | Risk | Verification |
|------|--------|------|--------------|
| 1 | Add tests for current behavior | None | Tests pass |
| 2 | Extract emailValidator | Low | Tests pass |
| 3 | Extract passwordValidator | Low | Tests pass |
| 4 | Extract remaining validators | Low | Tests pass |
| 5 | Refactor main function | Medium | Tests pass |
| 6 | Remove old code | Low | Tests pass |

### Step 3: Test Coverage

**Before Refactoring:**
```
validateUser(): 45% coverage
```

**Tests to Add:**
```typescript
describe('emailValidator', () => {
  it('should reject empty email');
  it('should reject invalid format');
  it('should reject too long');
  it('should accept valid email');
});

// Similar for each validator
```

**After Refactoring:**
```
emailValidator: 100%
passwordValidator: 100%
nameValidator: 100%
validateUser(): 100%
```

## Metrics Improvement

| Metric | Before | After |
|--------|--------|-------|
| Lines | 187 | 45 (main) + 20 (each validator) |
| Complexity | 34 | 4 (main), 5-8 (each validator) |
| Test coverage | 45% | 100% |
| Nesting depth | 6 | 2 |

## Risks & Mitigations

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Behavior change | Low | Comprehensive tests first |
| Missing edge case | Medium | Review all existing tests |
| Performance regression | Low | Benchmark before/after |
```

---

## 8. Test Coverage Gate

**Input:**
```
Check if the auth module is ready for release
```

**Output:**

```markdown
# Test Coverage Gate: Auth Module

## Coverage Summary

| Metric | Actual | Required | Status |
|--------|--------|----------|--------|
| Line Coverage | 76.3% | 80% | FAIL |
| Branch Coverage | 68.1% | 70% | FAIL |
| Function Coverage | 82.4% | 80% | PASS |
| New Code Coverage | 91.2% | 90% | PASS |

**Gate Status: FAIL**

---

## Uncovered Code

### Critical Gaps (Must Cover)

#### `src/auth/login.ts`
```
Lines 45-52: Error handling for database connection failure
Lines 78-85: Rate limiting enforcement
Lines 112-118: Account lockout logic
```

#### `src/auth/session.ts`
```
Lines 23-31: Session expiration check
Lines 67-72: Concurrent session handling
```

### Coverage by File

| File | Line % | Branch % | Status |
|------|--------|----------|--------|
| login.ts | 72.1% | 65.3% | FAIL |
| register.ts | 84.2% | 76.1% | PASS |
| session.ts | 68.9% | 58.2% | FAIL |
| middleware.ts | 91.3% | 88.7% | PASS |
| utils.ts | 95.2% | 92.1% | PASS |

---

## Missing Test Cases

### Must Add Before Release

1. **login.ts: Database failure handling**
   ```typescript
   it('should return 503 when database is unavailable', async () => {
     mockDb.connect.mockRejectedValue(new Error('Connection refused'));
     const res = await request(app).post('/login').send(credentials);
     expect(res.status).toBe(503);
   });
   ```

2. **login.ts: Rate limiting**
   ```typescript
   it('should block after 5 failed attempts', async () => {
     for (let i = 0; i < 5; i++) {
       await request(app).post('/login').send(wrongPassword);
     }
     const res = await request(app).post('/login').send(wrongPassword);
     expect(res.status).toBe(429);
   });
   ```

3. **session.ts: Expiration**
   ```typescript
   it('should reject expired session', async () => {
     const expiredSession = createSession({ expiresAt: Date.now() - 1000 });
     const res = await request(app)
       .get('/protected')
       .set('Authorization', `Bearer ${expiredSession.token}`);
     expect(res.status).toBe(401);
   });
   ```

---

## Recommendations

1. **Block Release:** Coverage below threshold
2. **Add 6 critical test cases** (estimated: 2 hours)
3. **Re-run gate** after tests added
4. **Consider:** Increase branch coverage threshold to 75%
```

---

## 9. Release Checklist

**Input:**
```
Prepare release v2.1.0 for production
```

**Output:**

```markdown
# Release Checklist: v2.1.0

## Pre-Release Verification

### Code Quality
- [x] All tests passing (127/127)
- [x] Coverage meets threshold (82.3% > 80%)
- [x] No lint errors
- [x] No TypeScript errors
- [x] Code review approved

### Security
- [x] Dependency audit clean (npm audit)
- [x] No high/critical vulnerabilities
- [x] Secrets scan passed (gitleaks)
- [ ] **BLOCKED:** Security review pending for OAuth changes

### Documentation
- [x] CHANGELOG.md updated
- [x] API documentation current
- [x] README reflects new features
- [ ] Migration guide for breaking changes

### Testing
- [x] Unit tests pass
- [x] Integration tests pass
- [x] E2E tests pass
- [ ] **PENDING:** Load testing (scheduled for tomorrow)
- [x] Staging environment validated

---

## Release Contents

### New Features
- OAuth login with Google and GitHub (#234)
- Session management improvements (#241)
- Rate limiting on authentication (#245)

### Bug Fixes
- Fixed race condition in balance deduction (#238)
- Fixed session fixation vulnerability (#242)

### Breaking Changes
- `POST /api/auth/login` response format changed
- Session cookie name changed from `sid` to `session_id`

---

## Deployment Steps

### 1. Pre-Deployment
```bash
# Create release branch
git checkout -b release/v2.1.0

# Update version
npm version 2.1.0

# Build production assets
npm run build:prod

# Run final verification
npm run verify:release
```

### 2. Database Migrations
```bash
# Backup database first!
pg_dump production > backup_pre_2.1.0.sql

# Run migrations
npm run migrate:prod
```

### 3. Deployment
```bash
# Deploy to production
./deploy.sh production v2.1.0

# Verify deployment
curl https://api.example.com/health
```

### 4. Post-Deployment
```bash
# Monitor error rates (15 minutes)
# Check key metrics dashboard
# Verify OAuth flows manually
```

---

## Rollback Plan

### Trigger Conditions
- Error rate > 1%
- P50 latency > 500ms
- Authentication success rate < 95%

### Rollback Steps
```bash
# Revert to previous version
./deploy.sh production v2.0.3

# Rollback database (if needed)
psql production < backup_pre_2.1.0.sql
```

---

## Sign-Off

| Role | Name | Status |
|------|------|--------|
| Engineering | | Approved |
| QA | | Approved |
| Security | | **PENDING** |
| Product | | Approved |

**Release Status: BLOCKED** — Awaiting security sign-off
```

---

## 10. Incident Postmortem

**Input:**
```
Postmortem for the payment processing outage on Jan 15
```

**Output:**

```markdown
# Incident Postmortem: Payment Processing Outage

**Date:** January 15, 2026
**Duration:** 2 hours 34 minutes (14:23 - 16:57 UTC)
**Severity:** SEV-1
**Author:** [Engineer Name]

---

## Executive Summary

Payment processing was completely unavailable for 2.5 hours due to a database connection pool exhaustion. The root cause was a missing database connection timeout combined with a slow third-party API. Approximately 12,000 transactions failed, with an estimated revenue impact of $180,000.

---

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 14:15 | Third-party fraud API begins responding slowly (>30s) |
| 14:20 | Database connection pool begins filling |
| 14:23 | **INCIDENT START:** First payment failures |
| 14:25 | Monitoring alert fires (error rate > 1%) |
| 14:31 | On-call engineer paged |
| 14:45 | Initial investigation: "Database healthy, queries fast" |
| 15:12 | Connection pool exhaustion identified |
| 15:30 | Attempted fix: Increase pool size (temporary relief) |
| 15:45 | Pool exhausted again |
| 16:15 | Root cause identified: Fraud API timeout holding connections |
| 16:30 | Fix deployed: Add 10s timeout to fraud API calls |
| 16:45 | Connection pool recovering |
| 16:57 | **INCIDENT END:** Error rate returns to normal |

---

## Root Cause Analysis

### The Chain of Events

1. **Trigger:** Third-party fraud detection API experienced degradation
2. **Amplification:** Our code waited indefinitely for API response
3. **Resource exhaustion:** Each waiting request held a database connection
4. **Cascade:** Connection pool (max 100) exhausted in ~8 minutes
5. **Outage:** New payment requests couldn't acquire connections

### Why Wasn't This Caught?

| Gap | Why It Existed |
|-----|----------------|
| No timeout on fraud API | "It's always been fast" assumption |
| No connection pool monitoring | Metrics existed but no alert |
| Slow initial diagnosis | Focused on DB, not external deps |

---

## Impact

### User Impact
- 12,347 failed payment attempts
- ~3,200 unique users affected
- Customer support received 89 tickets

### Business Impact
- Estimated $180,000 in lost transactions
- Unknown number of users who didn't retry
- Reputation impact (social media complaints)

### Technical Impact
- Payment service required restart
- Some transactions in inconsistent state (resolved manually)

---

## What Went Well

- Alert fired within 2 minutes of incident start
- On-call engineer responded within 6 minutes
- Customer support proactively messaged affected users
- No data loss or corruption

## What Went Poorly

- Took 1.5 hours to identify root cause
- Initial fix (increase pool) was wrong direction
- No runbook for connection pool issues
- Fraud API SLA not monitored

---

## Action Items

### Immediate (This Week)

| Action | Owner | Due |
|--------|-------|-----|
| Add timeout to all external API calls | Backend | Jan 17 |
| Alert on connection pool utilization > 80% | SRE | Jan 17 |
| Create runbook for connection exhaustion | Backend | Jan 19 |

### Short-term (This Month)

| Action | Owner | Due |
|--------|-------|-----|
| Circuit breaker for fraud API | Backend | Jan 31 |
| Load test with slow external dependencies | QA | Jan 31 |
| Review all external API call sites | Backend | Jan 31 |

### Long-term (This Quarter)

| Action | Owner | Due |
|--------|-------|-----|
| Implement async fraud checking | Architecture | Mar 31 |
| Add SLA monitoring for all third parties | SRE | Mar 31 |

---

## Lessons Learned

1. **Every external call needs a timeout.** No exceptions.
2. **Monitor resource pools, not just usage.** Pool exhaustion is different from high load.
3. **When stuck debugging, expand scope.** The problem might be outside your service.
```

---

## 11. Autonomous Loop

**Input:**
```
/loop "implement user authentication"
```

**Output (Iteration 1):**

```
[Context] Relevant paths: src/auth/, middleware/auth | Rules: @rules/security | Agents: security-analyst

Task Type: Feature Development (Security-Critical)
Loading rules: @rules/security, @rules/api-design, @rules/testing

## Phase 1: CONTEXTUALIZE
✓ Loaded existing auth files (none found)
✓ Loaded user model schema
✓ Loaded environment config

## Phase 2: ASSESS
Running /assess for codebase health...
- No existing auth implementation
- Test coverage: 78% (good baseline)
- No security vulnerabilities

Work Queue Created:
| Priority | Item | Status |
|----------|------|--------|
| S1 | Create login endpoint | Pending |
| S1 | Create logout endpoint | Pending |
| S1 | Add session management | Pending |
| S2 | Create auth middleware | Pending |
| S2 | Write auth tests | Pending |
| S3 | Update documentation | Pending |

## Phase 3: PLAN
Working on: [S1] Create login endpoint

Approach:
1. Create src/auth/login.ts
2. Add POST /api/auth/login route
3. Implement password verification
4. Create session on success

## Phase 4: BUILD
Creating src/auth/login.ts...
✓ Created login handler
✓ Added bcrypt password comparison
✓ Integrated session creation

Creating src/api/routes/auth.ts...
✓ Added /api/auth/login route
✓ Added input validation

## Phase 5: TEST
Running tests...
✓ 127 existing tests passing
✓ 5 new auth tests passing
Coverage: 76% → 79%

## Phase 6: QUALITY
Running quality gates...
| Gate | Status |
|------|--------|
| Pre-flight | ✓ PASS |
| Lint | ✓ PASS |
| Type | ✓ PASS |
| Unit Test | ✓ PASS |
| Security | ⚠ WARN (rate limiting missing) |
| Docs | ✓ PASS |

## Phase 7: EVALUATE
Check Definition of Done...
⚠ Security warning: Missing rate limiting
→ Adding to queue as S1

## Phase 8: RECOVER
Added to queue: [S1] Add rate limiting to login
Consecutive passes: 0
→ Continuing to iteration 2

---
Iteration 1 complete. Queue: 6 items remaining.
```

**Output (Final Iteration):**

```
## Iteration 5 - VERIFICATION

All quality gates passing for second consecutive iteration.

## Final Report

### Summary
- Total iterations: 5
- Issues fixed: 7
- Tests added: 24
- Coverage: 78% → 91%

### Quality Gates - ALL PASSING
✅ Pre-flight: Clean environment
✅ Lint: 0 errors
✅ Type: 0 errors
✅ Tests: 151 passing
✅ Integration: Pass
✅ Security: 0 vulnerabilities
✅ Performance: Acceptable
⏭️ Browser: N/A (backend only)
⏭️ Accessibility: N/A (backend only)
✅ Documentation: Complete
✅ Modern Tech: Current
✅ Definition of Done: Complete

### Files Created
- src/auth/login.ts
- src/auth/logout.ts
- src/auth/register.ts
- src/auth/session.ts
- src/middleware/auth.ts
- src/middleware/rateLimit.ts
- tests/auth/*.test.ts (6 files)

### Documentation Updated
- README.md (API section)
- CHANGELOG.md (v2.1.0)
- docs/api/auth.md (new)

### Recommendations (Not Blocking)
- Consider adding OAuth support (S3)
- Consider adding 2FA (S3)

---

✅ LOOP COMPLETE - All criteria met
```

---

## Using These Examples

### As Training Material
Show new team members what to expect from each prompt.

### As Quality Benchmarks
Compare your outputs against these examples for consistency.

### As Templates
Copy the structure when creating similar outputs.

### As Test Cases
Verify prompts produce outputs matching these patterns.

---

## 12. Swarm Mode

**Input:**
```
/cc-loop --swarm "Review the entire API layer for security and consistency"
```

**Output (Initialization):**

```
Task Type: Multi-File Review (Parallel-Safe)
Activating Swarm Mode with 3 workers

## Swarm Initialization

Decomposing task into independent work units...

### Task Pool Created
| ID | Task | Status | Claimed By |
|----|------|--------|------------|
| T001 | Review auth.ts | pending | — |
| T002 | Review users.ts | pending | — |
| T003 | Review orders.ts | pending | — |
| T004 | Review payments.ts | pending | — |
| T005 | Review webhooks.ts | pending | — |
| T006 | Synthesize findings | blocked | — |

### Dependencies
T006 (Synthesize) blocked by: T001, T002, T003, T004, T005

### Workers Spawned
- W1: Claiming T001 (auth.ts)
- W2: Claiming T002 (users.ts)
- W3: Claiming T003 (orders.ts)

Starting parallel execution...
```

**Output (Worker Progress):**

```
## Swarm Status Update

### Worker Activity
| Worker | Current Task | Status |
|--------|--------------|--------|
| W1 | T001 (auth.ts) | ✓ Complete |
| W2 | T002 (users.ts) | 🔄 In Progress |
| W3 | T003 (orders.ts) | ✓ Complete |

### Task Pool Status
| ID | Task | Status | Claimed By |
|----|------|--------|------------|
| T001 | Review auth.ts | ✓ complete | W1 |
| T002 | Review users.ts | 🔄 in_progress | W2 |
| T003 | Review orders.ts | ✓ complete | W3 |
| T004 | Review payments.ts | 🔄 in_progress | W1 |
| T005 | Review webhooks.ts | pending | — |
| T006 | Synthesize findings | blocked | — |

W1 completed T001, claimed T004
W3 completed T003, claimed T005

Progress: ████████░░░░░░░░ 40% (2/5 reviews complete)
```

**Output (Final Report):**

```
## Swarm Complete

All workers finished. Synthesizing results...

### Summary
- Workers: 3
- Tasks completed: 6
- Total time: 4m 23s
- Parallelization speedup: ~2.5x

### Findings by Severity

#### S1 — High
| Finding | File | Worker |
|---------|------|--------|
| SQL injection in search | users.ts:45 | W2 |
| Missing rate limiting | auth.ts:23 | W1 |

#### S2 — Medium
| Finding | File | Worker |
|---------|------|--------|
| Inconsistent error codes | orders.ts:89 | W3 |
| Missing input validation | payments.ts:34 | W1 |
| No request timeout | webhooks.ts:12 | W3 |

### Synthesized Recommendations
1. **Immediate:** Fix SQL injection in users.ts
2. **Immediate:** Add rate limiting to auth endpoints
3. **This Sprint:** Standardize error codes across API
4. **This Sprint:** Add input validation to all handlers

### Work Queue Created
| Priority | Item | From Finding |
|----------|------|--------------|
| S1 | Fix SQL injection | users.ts:45 |
| S1 | Add rate limiting | auth.ts:23 |
| S2 | Standardize errors | orders.ts:89 |
| S2 | Add validation | payments.ts:34 |
| S2 | Add timeouts | webhooks.ts:12 |

---

✅ SWARM COMPLETE - Ready for /cc-loop to process work queue
```

---

## 13. Task Dependencies

**Input:**
```
/cc-loop "Build user notification system"
```

**Output (With Dependencies):**

```
## Work Queue with Dependencies

Analyzing task structure...

### Dependency Graph
```
T001 (Design schema) ──┬──▶ T002 (Notification service) ──┬──▶ T005 (Integration tests)
                       │                                   │
                       └──▶ T003 (Email adapter) ──────────┤
                       │                                   │
                       └──▶ T004 (Push adapter) ───────────┘
```

### Task Status
| ID | Task | Status | Blocked By | Blocks |
|----|------|--------|------------|--------|
| T001 | Design notification schema | 🔄 in_progress | — | T002, T003, T004 |
| T002 | Implement notification service | blocked | T001 | T005 |
| T003 | Create email adapter | blocked | T001 | T005 |
| T004 | Create push adapter | blocked | T001 | T005 |
| T005 | Write integration tests | blocked | T002, T003, T004 | — |

### Pipeline Progress
Phase 1: Schema Design [████████████████████] 100%
Phase 2: Implementation [░░░░░░░░░░░░░░░░░░░░] 0% (waiting)
Phase 3: Integration [░░░░░░░░░░░░░░░░░░░░] 0% (blocked)

---

## Iteration 2

T001 (Schema) → COMPLETE

Auto-unblocking:
- T002: blocked → pending ✓
- T003: blocked → pending ✓
- T004: blocked → pending ✓

### Updated Status
| ID | Task | Status | Blocked By | Blocks |
|----|------|--------|------------|--------|
| T001 | Design notification schema | ✓ complete | — | — |
| T002 | Implement notification service | 🔄 in_progress | — | T005 |
| T003 | Create email adapter | pending | — | T005 |
| T004 | Create push adapter | pending | — | T005 |
| T005 | Write integration tests | blocked | T002, T003, T004 | — |

### Pipeline Progress
Phase 1: Schema Design [████████████████████] 100% ✓
Phase 2: Implementation [██████░░░░░░░░░░░░░░] 33%
Phase 3: Integration [░░░░░░░░░░░░░░░░░░░░] 0% (blocked)
```

---

## See Also

| Resource | Purpose |
|----------|---------|
| [CLAUDE.md](template/.claude/CLAUDE.md) | Command reference |
| [QUICK_REFERENCE.md](template/.claude/QUICK_REFERENCE.md) | One-page cheat sheet |
| [skills/_index.md](template/.claude/skills/_index.md) | Skill documentation |
| [SWARM_ARCHITECTURE.md](template/.claude/SWARM_ARCHITECTURE.md) | Swarm mode details |
