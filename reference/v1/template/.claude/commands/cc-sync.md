---
name: cc-sync
description: Verify frontend-backend synchronization
model: sonnet
argument-hint: "[feature or module]"
---

# /sync - Frontend-Backend Sync Check

<context>
Full-stack applications break when frontend and backend get out of sync.
Type mismatches, missing API calls, and outdated response handling cause
runtime errors and frustrated users. Regular sync checks catch these issues
before they hit production.
</context>

<role>
You are a full-stack integration specialist who:
- Maps API endpoints to frontend calls
- Compares type definitions across boundaries
- Identifies missing integrations
- Spots validation mismatches
- Ensures error handling coverage
</role>

## Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `$1` | Feature or module to check | `/sync user-api` |

## Usage Examples

```
/sync                           # Check entire project
/sync auth                      # Check auth module sync
/sync user-api                  # Check user API sync
/sync recent                    # Check recent changes only
```

<task>
Verify frontend-backend synchronization by:
1. Scanning backend for API endpoints
2. Scanning frontend for API calls
3. Comparing types and contracts
4. Identifying mismatches and gaps
5. Generating sync report
</task>

<instructions>
<step number="1">
**Scan backend**: Find API definitions:
- Route handlers and endpoints
- Request/response schemas
- Validation rules
- Error response formats
- New or changed endpoints
</step>

<step number="2">
**Scan frontend**: Find API integrations:
- API client calls (fetch, axios, etc.)
- TypeScript types for responses
- Form validation matching backend
- Error handling for API responses
- React Query/SWR hooks
</step>

<step number="3">
**Compare contracts**: Match definitions:
- Endpoint URL matching
- HTTP method alignment
- Request body shape
- Response type shape
- Query parameter handling
</step>

<step number="4">
**Check validation**: Match rules:
- Required vs optional fields
- Field constraints (length, format)
- Business rule validation
- Error message consistency
</step>

<step number="5">
**Verify error handling**: Complete coverage:
- 400 (validation) handling
- 401/403 (auth) handling
- 404 (not found) handling
- 500 (server error) handling
- Network error handling
</step>
</instructions>

<output_format>
# Frontend-Backend Sync Report

**Scope:** [Module or feature]
**Date:** [Date]
**Sync Status:** [Synced / Partially Synced / Out of Sync]

---

## Summary

| Category | Status | Issues |
|----------|--------|--------|
| Endpoints | [N synced / M total] | [count] |
| Types | [N synced / M total] | [count] |
| Validation | [N synced / M total] | [count] |
| Error Handling | [N synced / M total] | [count] |

---

## Synced (OK)

| Backend | Frontend | Status |
|---------|----------|--------|
| `GET /api/users` | `useUsers()` | ✓ |
| `POST /api/orders` | `createOrder()` | ✓ |

---

## Missing Frontend Integration

### [Endpoint]
**Backend:** `[Method] [URL]`
**Problem:** No corresponding API call in frontend
**Impact:** [What users can't do]
**Fix:**
```typescript
// Add to src/lib/api/[module].ts
export async function [functionName]() {
  return api.[method]('[url]');
}
```

---

## Missing Backend Endpoint

### [Feature]
**Frontend calls:** `[Method] [URL]`
**Problem:** Endpoint does not exist
**Impact:** [What breaks]
**Fix:** Create endpoint or update frontend to correct URL

---

## Type Mismatches

### [Type Name]
**Backend returns:**
```typescript
{
  id: string;
  createdAt: Date;
  preferences: { theme: string };  // NEW FIELD
}
```

**Frontend expects:**
```typescript
{
  id: string;
  createdAt: string;  // Type mismatch
  // Missing: preferences
}
```

**Fix:** Update frontend type definition

---

## Validation Mismatches

### [Field/Form]
| Rule | Backend | Frontend |
|------|---------|----------|
| email format | ✓ Required | ✗ Optional |
| password min | 12 chars | 8 chars |

---

## Action Items

1. [Priority 1]
2. [Priority 2]
3. [Priority 3]
</output_format>

<examples>
<example>
<input>
/sync auth
</input>
<thinking>
1. Find auth-related backend endpoints
2. Find auth-related frontend API calls
3. Compare login/register/logout flows
4. Check session/token handling
5. Verify error handling for 401s
</thinking>
<output>
# Frontend-Backend Sync Report

**Scope:** Authentication module
**Date:** 2026-01-29
**Sync Status:** Partially Synced (3 issues)

---

## Summary

| Category | Status | Issues |
|----------|--------|--------|
| Endpoints | 5/6 synced | 1 |
| Types | 3/4 synced | 1 |
| Validation | 4/6 synced | 2 |
| Error Handling | 3/4 synced | 1 |

---

## Synced (OK)

| Backend | Frontend | Status |
|---------|----------|--------|
| `POST /api/auth/login` | `useLogin()` | ✓ |
| `POST /api/auth/register` | `useRegister()` | ✓ |
| `POST /api/auth/logout` | `useLogout()` | ✓ |
| `GET /api/auth/me` | `useCurrentUser()` | ✓ |
| `POST /api/auth/refresh` | auto-refresh interceptor | ✓ |

---

## Missing Frontend Integration

### Password Reset Flow
**Backend:** `POST /api/auth/forgot-password`
**Problem:** Endpoint exists but no frontend implementation
**Impact:** Users cannot reset forgotten passwords
**Fix:**
```typescript
// Add to src/features/auth/api.ts
export async function requestPasswordReset(email: string) {
  return api.post('/api/auth/forgot-password', { email });
}

// Add to src/features/auth/hooks.ts
export function usePasswordReset() {
  return useMutation({
    mutationFn: requestPasswordReset,
    onSuccess: () => toast.success('Check your email'),
  });
}
```

---

## Type Mismatches

### User Type
**Backend returns:**
```typescript
// From GET /api/auth/me
{
  id: string;
  email: string;
  name: string;
  role: 'user' | 'admin';
  emailVerified: boolean;  // NEW
  createdAt: string;
  preferences: {           // NEW
    theme: 'light' | 'dark';
    notifications: boolean;
  };
}
```

**Frontend expects:**
```typescript
// In src/features/auth/types.ts
interface User {
  id: string;
  email: string;
  name: string;
  role: 'user' | 'admin';
  createdAt: string;
  // Missing: emailVerified, preferences
}
```

**Fix:**
```typescript
interface User {
  id: string;
  email: string;
  name: string;
  role: 'user' | 'admin';
  emailVerified: boolean;
  createdAt: string;
  preferences: UserPreferences;
}

interface UserPreferences {
  theme: 'light' | 'dark';
  notifications: boolean;
}
```

---

## Validation Mismatches

### Registration Form
| Rule | Backend | Frontend |
|------|---------|----------|
| email | Required, valid format | ✓ Matches |
| password min | 12 characters | 8 characters ✗ |
| password pattern | 1 uppercase, 1 number, 1 special | Not enforced ✗ |
| name | Optional, max 100 | ✓ Matches |

**Fix:** Update frontend validation schema:
```typescript
const registerSchema = z.object({
  email: z.string().email(),
  password: z
    .string()
    .min(12, 'Password must be at least 12 characters')
    .regex(/[A-Z]/, 'Must contain uppercase')
    .regex(/[0-9]/, 'Must contain number')
    .regex(/[!@#$%]/, 'Must contain special character'),
  name: z.string().max(100).optional(),
});
```

---

## Error Handling Gap

### Missing 401 Handler on Protected Routes
**Problem:** API calls to protected endpoints don't handle 401 consistently
**Impact:** Users see generic error instead of redirect to login
**Fix:**
```typescript
// In API interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear user state
      authStore.logout();
      // Redirect to login
      router.push('/login?expired=true');
    }
    return Promise.reject(error);
  }
);
```

---

## Action Items

1. **Implement password reset flow** (P1) - Missing feature
2. **Update User type** (P1) - Causes TypeScript errors
3. **Fix registration validation** (P2) - Security risk
4. **Add 401 interceptor** (P2) - UX improvement
</output>
</example>

<example>
<input>
/sync recent
</input>
<output>
# Recent Changes Sync Report

**Scope:** Changes in last 7 days
**Date:** 2026-01-29
**Status:** 2 sync issues found

---

## Recent Backend Changes

| Commit | Change | Synced? |
|--------|--------|---------|
| `a1b2c3d` | Added `preferences` to User | ✗ Frontend missing |
| `d4e5f6g` | New `POST /api/notifications/subscribe` | ✗ No frontend |
| `h7i8j9k` | Updated validation on orders | ✓ Frontend updated |

---

## Action Required

### 1. User Preferences Field
Frontend needs to handle new `preferences` field.
See type mismatch details above.

### 2. Push Notification Subscribe
New endpoint needs frontend integration:
```typescript
export function useSubscribePush() {
  return useMutation({
    mutationFn: (subscription: PushSubscription) =>
      api.post('/api/notifications/subscribe', subscription),
  });
}
```

---

## No Issues

- Order validation changes already synced
- Cart API unchanged
- Product API unchanged
</output>
</example>
</examples>

<rules>
- Scan both directions (backend→frontend and frontend→backend)
- Compare actual types, not just endpoint existence
- Include validation rules in comparison
- Check error handling coverage
- Provide ready-to-use code fixes
- Flag security-sensitive mismatches (auth, validation)
</rules>

<error_handling>
If no backend found: "No API endpoints found. Specify backend directory."
If no frontend found: "No frontend API calls found. Specify frontend directory."
If monorepo: "Monorepo detected. Which packages to compare?"
If types not found: "No type definitions found. Comparing raw shapes."
</error_handling>
