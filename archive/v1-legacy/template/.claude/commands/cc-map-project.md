---
name: cc-map-project
description: Generate project context map for faster onboarding
model: sonnet
argument-hint: "[--refresh]"
---

# /map-project - Project Context Mapper

<context>
Understanding a codebase quickly is essential for effective development. A
project context map provides a bird's-eye view of the architecture, key files,
patterns, and conventions. This accelerates onboarding and helps Claude
provide more accurate, contextual assistance.
</context>

<role>
You are a codebase analyst who:
- Maps project structure comprehensively
- Identifies architectural patterns
- Documents key files and their purposes
- Extracts conventions and standards
- Creates navigable reference documentation
</role>

## Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `--refresh` | Regenerate existing map | `/map-project --refresh` |

## Usage Examples

```
/map-project                    # Generate project map
/map-project --refresh          # Refresh existing map
```

<task>
Generate comprehensive project context by:
1. Scanning the codebase structure
2. Identifying architecture patterns
3. Mapping key files and entry points
4. Documenting conventions
5. Creating PROJECT_MAP.md
</task>

<instructions>
<step number="1">
**Scan codebase**: Analyze project structure:
- Directory layout and organization
- Source file distribution
- Configuration files present
- Build and deployment setup
</step>

<step number="2">
**Identify architecture**: Determine patterns used:
- Monolith, microservices, or monorepo
- MVC, layered, clean architecture
- Frontend framework patterns
- Backend framework patterns
- Data flow architecture
</step>

<step number="3">
**Map key files**: Document important files:
- Entry points (main, index, app)
- Configuration files
- Route definitions
- Schema definitions
- Core business logic
- Utilities and helpers
</step>

<step number="4">
**Extract conventions**: Document patterns:
- File naming conventions
- Directory organization patterns
- Code style patterns
- Import/export patterns
- Error handling patterns
</step>

<step number="5">
**Generate map**: Create PROJECT_MAP.md:
- Structured reference document
- Searchable and navigable
- Include examples
- Note deviations from conventions
</step>
</instructions>

<output_format>
# Project Map: [Project Name]

**Generated:** [Date]
**Tech Stack:** [Primary technologies]
**Architecture:** [Pattern name]

---

## Quick Navigation

| Area | Location | Purpose |
|------|----------|---------|
| Entry Point | [path] | [description] |
| Routes | [path] | [description] |
| Components | [path] | [description] |
| API | [path] | [description] |
| Database | [path] | [description] |
| Tests | [path] | [description] |
| Config | [path] | [description] |

---

## Directory Structure

```
[project root]
├── src/                    # [Description]
│   ├── [dir]/              # [Description]
│   └── [dir]/              # [Description]
├── tests/                  # [Description]
├── docs/                   # [Description]
└── [config files]          # [Description]
```

---

## Architecture Overview

### Pattern: [Architecture Name]
[Description of architecture with diagram if helpful]

### Data Flow
```
[Flow diagram using ASCII]
```

### Key Boundaries
- [Boundary 1]: [What it separates]
- [Boundary 2]: [What it separates]

---

## Key Files Reference

### Entry Points
| File | Purpose | Notes |
|------|---------|-------|
| [file] | [what it does] | [important notes] |

### Configuration
| File | Purpose | Notes |
|------|---------|-------|
| [file] | [what it configures] | [important notes] |

### Core Business Logic
| File | Purpose | Notes |
|------|---------|-------|
| [file] | [domain/feature] | [important notes] |

---

## Conventions

### File Naming
- Components: `PascalCase.tsx`
- Utilities: `camelCase.ts`
- Tests: `[name].test.ts`
- Styles: `[name].module.css`

### Directory Patterns
- Feature-based: `/features/[feature]/`
- Layer-based: `/services/`, `/repositories/`

### Import Conventions
```typescript
// Example of standard import order
[external imports]
[internal absolute imports]
[relative imports]
```

### Code Patterns
[Examples of common patterns used in the codebase]

---

## Technology Stack

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| [tech] | [version] | [use case] |

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| [tech] | [version] | [use case] |

### Infrastructure
| Technology | Purpose |
|------------|---------|
| [tech] | [use case] |

---

## Common Tasks

### How to add a new [component/feature/endpoint]
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Where to find [common thing]
- [Thing]: [Location]

---

## Gotchas & Notes

- [Non-obvious behavior or pattern]
- [Historical decision that might confuse]
- [Area that needs refactoring]
</output_format>

<examples>
<example>
<input>
/map-project
(in a Next.js e-commerce project)
</input>
<thinking>
1. Scan directory structure for Next.js patterns
2. Identify app router vs pages router
3. Map API routes and data fetching
4. Document component organization
5. Note state management approach
</thinking>
<output>
# Project Map: ShopNext E-commerce

**Generated:** 2026-01-29
**Tech Stack:** Next.js 14, TypeScript, PostgreSQL, Prisma, Stripe
**Architecture:** Feature-based with App Router

---

## Quick Navigation

| Area | Location | Purpose |
|------|----------|---------|
| Entry Point | `src/app/layout.tsx` | Root layout with providers |
| Routes | `src/app/` | App router pages |
| Components | `src/components/` | Shared UI components |
| Features | `src/features/` | Feature-specific code |
| API | `src/app/api/` | API route handlers |
| Database | `prisma/schema.prisma` | Database schema |
| Tests | `__tests__/` | Test files |
| Config | Root `.config` files | Build/lint config |

---

## Directory Structure

```
shopnext/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── (shop)/             # Public shop routes
│   │   │   ├── page.tsx        # Homepage
│   │   │   ├── products/       # Product pages
│   │   │   └── cart/           # Cart page
│   │   ├── (admin)/            # Admin routes (protected)
│   │   │   └── dashboard/      # Admin dashboard
│   │   ├── api/                # API routes
│   │   │   ├── products/       # Product CRUD
│   │   │   ├── orders/         # Order management
│   │   │   └── webhooks/       # Stripe webhooks
│   │   ├── layout.tsx          # Root layout
│   │   └── globals.css         # Global styles
│   ├── components/             # Shared components
│   │   ├── ui/                 # Base UI (Button, Input, etc.)
│   │   └── layout/             # Layout components
│   ├── features/               # Feature modules
│   │   ├── products/           # Product feature
│   │   ├── cart/               # Cart feature
│   │   ├── checkout/           # Checkout feature
│   │   └── auth/               # Authentication
│   ├── lib/                    # Utilities
│   │   ├── prisma.ts           # Prisma client
│   │   ├── stripe.ts           # Stripe client
│   │   └── utils.ts            # General utilities
│   └── types/                  # TypeScript types
├── prisma/
│   ├── schema.prisma           # Database schema
│   └── migrations/             # Migration history
├── __tests__/                  # Test files
├── public/                     # Static assets
└── [config files]
```

---

## Architecture Overview

### Pattern: Feature-Based Architecture with App Router
Each feature (`products`, `cart`, `checkout`) is self-contained with:
- Components specific to the feature
- Hooks for feature logic
- API calls/server actions
- Types for the feature

### Data Flow
```
User Action
    │
    ▼
Page/Component (src/app or src/features)
    │
    ▼
Server Action or API Route (src/app/api)
    │
    ▼
Service Layer (src/features/[feature]/services)
    │
    ▼
Prisma Client (src/lib/prisma.ts)
    │
    ▼
PostgreSQL Database
```

### Key Boundaries
- **Client/Server**: Server components by default, `'use client'` for interactivity
- **Feature isolation**: Features don't import from each other directly
- **API boundary**: All mutations through API routes or server actions

---

## Key Files Reference

### Entry Points
| File | Purpose | Notes |
|------|---------|-------|
| `src/app/layout.tsx` | Root layout | Wraps with AuthProvider, CartProvider |
| `src/app/page.tsx` | Homepage | Server component, fetches featured products |
| `src/middleware.ts` | Auth middleware | Protects `/admin/*` routes |

### Configuration
| File | Purpose | Notes |
|------|---------|-------|
| `prisma/schema.prisma` | DB schema | Source of truth for data models |
| `next.config.js` | Next.js config | Image domains, redirects |
| `.env.local` | Environment vars | Never commit, use `.env.example` |

### Core Business Logic
| File | Purpose | Notes |
|------|---------|-------|
| `src/features/checkout/services/checkout.ts` | Checkout flow | Stripe integration here |
| `src/features/cart/hooks/useCart.ts` | Cart state | Uses Zustand store |
| `src/app/api/webhooks/stripe/route.ts` | Payment webhooks | Handles payment events |

---

## Conventions

### File Naming
- Components: `ProductCard.tsx` (PascalCase)
- Hooks: `useCart.ts` (camelCase with `use` prefix)
- Utilities: `formatPrice.ts` (camelCase)
- Types: `product.types.ts` (lowercase with `.types` suffix)
- Tests: `ProductCard.test.tsx` (matching component name)

### Directory Patterns
```
src/features/[feature]/
├── components/     # Feature-specific components
├── hooks/          # Feature hooks
├── services/       # API/data services
├── types/          # Feature types
└── index.ts        # Public exports
```

### Import Conventions
```typescript
// 1. External packages
import { useState } from 'react';
import { z } from 'zod';

// 2. Internal absolute imports (using @/ alias)
import { Button } from '@/components/ui/Button';
import { prisma } from '@/lib/prisma';

// 3. Relative imports
import { ProductCard } from './ProductCard';
```

### Code Patterns
```typescript
// Server Component (default)
async function ProductPage({ params }: { params: { id: string } }) {
  const product = await getProduct(params.id);
  return <ProductDetails product={product} />;
}

// Client Component (when needed)
'use client';
function AddToCartButton({ productId }: Props) {
  const { addItem } = useCart();
  return <Button onClick={() => addItem(productId)}>Add to Cart</Button>;
}
```

---

## Technology Stack

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| Next.js | 14.1.0 | Framework |
| React | 18.2.0 | UI library |
| TypeScript | 5.3.0 | Type safety |
| Tailwind CSS | 3.4.0 | Styling |
| Zustand | 4.5.0 | Client state |

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| Next.js API Routes | - | API endpoints |
| Prisma | 5.8.0 | ORM |
| PostgreSQL | 15 | Database |
| Stripe | 14.0.0 | Payments |

### Infrastructure
| Technology | Purpose |
|------------|---------|
| Vercel | Hosting & deployment |
| Supabase | PostgreSQL hosting |
| Stripe | Payment processing |

---

## Common Tasks

### How to add a new product field
1. Update `prisma/schema.prisma` with new field
2. Run `npx prisma migrate dev`
3. Update `src/features/products/types/product.types.ts`
4. Update affected components

### How to add a new API endpoint
1. Create route in `src/app/api/[resource]/route.ts`
2. Add service function in `src/features/[feature]/services/`
3. Add types in `src/features/[feature]/types/`

### Where to find common things
- **Auth logic**: `src/features/auth/`
- **Stripe setup**: `src/lib/stripe.ts`
- **Database queries**: `src/features/[feature]/services/`
- **Shared UI**: `src/components/ui/`

---

## Gotchas & Notes

- **Cart persists via localStorage** - See `src/features/cart/store.ts` for hydration handling
- **Images use next/image** - All product images must be in `next.config.js` domains
- **API routes are Edge-ready** - Avoid Node.js-only APIs in route handlers
- **Webhook verification** - Stripe webhooks require raw body, see `route.ts` for setup
</output>
</example>
</examples>

<rules>
- Scan actual codebase structure, don't assume
- Document patterns as they are, not as they should be
- Note inconsistencies or areas needing cleanup
- Include version numbers for key dependencies
- Keep the map updated when major changes occur
- Make navigation tables genuinely useful
</rules>

<error_handling>
If codebase too large: "This is a large codebase. Focus on specific area?"
If structure unclear: "Unconventional structure detected. Document as-is with notes."
If existing map found: "PROJECT_MAP.md exists. Refresh or create parallel map?"
If permission issues: "Cannot access some directories. Proceed with accessible areas?"
</error_handling>

## Output Location

Creates `.claude/context/PROJECT_MAP.md` for Claude to reference during work.
