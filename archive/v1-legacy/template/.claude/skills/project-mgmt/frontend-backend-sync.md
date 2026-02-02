---
name: frontend-backend-sync
description: Ensure frontend and backend changes stay synchronized in fullstack projects
model: sonnet
---

# Frontend-Backend Sync

Automatically ensure frontend and backend changes are properly connected in fullstack applications.

## Trigger

This skill activates when:
- Working on fullstack projects (frontend + backend)
- Adding/modifying API endpoints
- Creating/updating data models
- Implementing new features that span both layers
- Words like "API", "endpoint", "frontend", "backend", "fullstack"

---

## The Problem

Common sync issues in fullstack development:

1. **Backend endpoint created, frontend never calls it**
2. **API response shape changed, frontend breaks**
3. **New field added to model, not displayed in UI**
4. **Frontend expects data that backend doesn't provide**
5. **Types/interfaces out of sync**
6. **Error handling mismatch**

---

## Automatic Checks

### When Backend Changes Are Made

After any backend modification, verify:

```
□ API Endpoint Changes
  □ Is there a corresponding frontend API call?
  □ Does the frontend handle the response shape?
  □ Are error cases handled in the UI?
  □ Are types/interfaces updated on frontend?

□ Data Model Changes
  □ Is the new/changed field used in frontend?
  □ Are form inputs updated if needed?
  □ Are display components updated?
  □ Are validation rules synced?

□ Authentication/Authorization Changes
  □ Does frontend handle new auth requirements?
  □ Are protected routes updated?
  □ Are error states (401, 403) handled in UI?
```

### When Frontend Changes Are Made

After any frontend modification, verify:

```
□ New UI Component
  □ Does it need backend data?
  □ Is the API endpoint available?
  □ Are loading/error states handled?

□ Form Changes
  □ Does backend accept the new fields?
  □ Is validation consistent?
  □ Are error messages from backend displayed?

□ New Feature
  □ Is the backend support complete?
  □ Are all required endpoints available?
  □ Is the data flow complete end-to-end?
```

---

## Sync Verification Process

### 1. Identify the Change Scope

```markdown
## Change Analysis

**What changed:** [Description]
**Layer:** Backend / Frontend / Both
**Type:** New feature / Bug fix / Enhancement

### Affected Areas

Backend:
- [ ] API endpoints: [list]
- [ ] Data models: [list]
- [ ] Business logic: [list]

Frontend:
- [ ] Components: [list]
- [ ] API calls: [list]
- [ ] State management: [list]
```

### 2. Trace the Data Flow

```
[Database] → [Backend Model] → [API Endpoint] → [Frontend API Call] → [State] → [Component]
     ↓              ↓                ↓                  ↓              ↓           ↓
  Schema?      Validation?      Response shape?     Error handling?  Types?    Display?
```

### 3. Generate Sync Report

```markdown
## Frontend-Backend Sync Report

### Changes Made
- Backend: Added `GET /api/users/:id/preferences`
- Backend: Added `preferences` field to User model

### Sync Status

| Backend | Frontend | Status |
|---------|----------|--------|
| GET /api/users/:id/preferences | ❌ No API call | MISSING |
| User.preferences field | ❌ Not in UserType | MISSING |
| PreferencesSchema validation | ❌ No form validation | MISSING |

### Required Frontend Updates

1. **Add API call**
   ```typescript
   // src/api/users.ts
   export const getUserPreferences = (id: string) =>
     api.get(`/users/${id}/preferences`);
   ```

2. **Update types**
   ```typescript
   // src/types/user.ts
   interface User {
     // ... existing fields
     preferences: UserPreferences;
   }
   ```

3. **Add UI component**
   ```typescript
   // src/components/UserPreferences.tsx
   // Component to display/edit preferences
   ```
```

---

## Type Synchronization

### Shared Types (Recommended)

```typescript
// shared/types/user.ts (used by both)
export interface User {
  id: string;
  email: string;
  name: string;
  preferences: UserPreferences;
}

export interface UserPreferences {
  theme: 'light' | 'dark';
  notifications: boolean;
}

// Backend: import { User } from '@shared/types/user'
// Frontend: import { User } from '@shared/types/user'
```

### API Contract Generation

```typescript
// Using tools like:
// - tRPC (type-safe API)
// - OpenAPI/Swagger → TypeScript
// - GraphQL codegen

// Example: tRPC
// Backend defines, frontend gets types automatically
const appRouter = router({
  getUser: publicProcedure
    .input(z.string())
    .query(({ input }) => getUserById(input)),
});

// Frontend - fully typed
const { data } = trpc.getUser.useQuery(userId);
```

---

## Common Patterns to Check

### REST API Sync

```typescript
// Backend endpoint
app.get('/api/products/:id', async (req, res) => {
  const product = await getProduct(req.params.id);
  res.json({
    id: product.id,
    name: product.name,
    price: product.price,
    // ⚠️ New field added - is frontend updated?
    inventory: product.inventory,
  });
});

// Frontend must match
interface Product {
  id: string;
  name: string;
  price: number;
  inventory: number; // ← Must add this
}

const ProductCard = ({ product }: { product: Product }) => (
  <div>
    <h2>{product.name}</h2>
    <p>${product.price}</p>
    <p>In stock: {product.inventory}</p> {/* ← Must display */}
  </div>
);
```

### Error Handling Sync

```typescript
// Backend throws specific errors
throw new ValidationError('Email already exists', { field: 'email' });

// Frontend must handle
try {
  await api.createUser(data);
} catch (error) {
  if (error.code === 'VALIDATION_ERROR') {
    setFieldError(error.details.field, error.message);
  }
}
```

### Form Validation Sync

```typescript
// Backend validation (Zod)
const createUserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  name: z.string().min(2).max(50),
});

// Frontend validation should match
const schema = yup.object({
  email: yup.string().email().required(),
  password: yup.string().min(8).required(),
  name: yup.string().min(2).max(50).required(),
});
```

---

## Enforcement

### Before Completing Any Task

Ask these questions:

1. **"Does this change affect both frontend and backend?"**
   - If yes, have both sides been updated?

2. **"Is there a UI for this backend feature?"**
   - If no, should there be?

3. **"Does the frontend expect this backend behavior?"**
   - If no, update frontend or document why not.

4. **"Are the types synchronized?"**
   - If not, update shared types or both sides.

5. **"Is error handling complete end-to-end?"**
   - Backend errors → Frontend display → User feedback

### Sync Checklist

Before marking a fullstack feature complete:

```
□ All new endpoints have corresponding frontend calls
□ All new fields are displayed/used in UI
□ Types match between frontend and backend
□ Validation rules are consistent
□ Error handling is complete
□ Loading states exist for async operations
□ Empty/null states are handled
□ Feature works end-to-end (tested)
```

---

## Integration with Other Skills

This skill works with:

- **pre-commit** — Verify sync before committing
- **test-first** — Write integration tests spanning both layers
- **code-reviewer** — Check for sync issues in reviews
- **ui-ux-expert** — Ensure UI reflects all backend capabilities
