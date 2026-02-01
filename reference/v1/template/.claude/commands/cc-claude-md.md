---
name: cc-claude-md
description: Create or improve project CLAUDE.md
model: sonnet
argument-hint: "[--refresh]"
---

# /claude-md - CLAUDE.md Manager

<context>
A project-specific CLAUDE.md provides Claude with context about your codebase,
conventions, and patterns. This enables more accurate, contextual assistance
by teaching Claude how your project works. Better context = better code.
</context>

<role>
You are a project documentation specialist who:
- Analyzes codebases comprehensively
- Extracts patterns and conventions
- Creates clear, actionable guidance
- Writes for AI consumption
- Maintains living documentation
</role>

## Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `--refresh` | Update existing CLAUDE.md | `/claude-md --refresh` |

## Usage Examples

```
/claude-md                      # Create new CLAUDE.md
/claude-md --refresh            # Update existing
/claude-md --minimal            # Create minimal version
```

<task>
Create or update CLAUDE.md by:
1. Analyzing project structure
2. Detecting technologies and patterns
3. Extracting conventions
4. Generating project-specific guidance
5. Writing CLAUDE.md file
</task>

<instructions>
<step number="1">
**Analyze project**: Scan codebase for:
- Package files (package.json, requirements.txt, etc.)
- Configuration files
- Directory structure
- Existing documentation
- Source code patterns
</step>

<step number="2">
**Detect technology stack**: Identify:
- Languages and versions
- Frameworks and libraries
- Build tools
- Testing frameworks
- Database/infrastructure
</step>

<step number="3">
**Extract conventions**: Find patterns for:
- File and folder naming
- Code style and formatting
- Import organization
- Error handling patterns
- Component patterns
</step>

<step number="4">
**Identify key files**: Document:
- Entry points
- Configuration files
- Core business logic
- Shared utilities
- Types/schemas
</step>

<step number="5">
**Generate CLAUDE.md**: Create file with:
- Project overview
- Tech stack summary
- Key directories and files
- Conventions to follow
- Common patterns
- Project-specific commands
</step>
</instructions>

<output_format>
# [Project Name]

## Overview
[One-paragraph description of what this project does]

---

## Tech Stack

| Category | Technology |
|----------|------------|
| Language | [e.g., TypeScript 5.x] |
| Framework | [e.g., Next.js 14] |
| Database | [e.g., PostgreSQL + Prisma] |
| Testing | [e.g., Jest + RTL] |
| Styling | [e.g., Tailwind CSS] |

---

## Directory Structure

```
[project]/
├── src/              # [Purpose]
│   ├── [dir]/        # [Purpose]
│   └── [dir]/        # [Purpose]
├── tests/            # [Purpose]
└── [config files]
```

---

## Key Files

| File | Purpose |
|------|---------|
| [path] | [What it does] |

---

## Conventions

### Naming
- Files: [Convention]
- Components: [Convention]
- Functions: [Convention]

### Code Style
- [Key convention 1]
- [Key convention 2]

### Imports
```typescript
// Order
[Example import order]
```

---

## Common Patterns

### [Pattern Name]
```typescript
// Example
[Code example]
```

---

## Commands

| Command | Purpose |
|---------|---------|
| `npm run dev` | [Description] |
| `npm test` | [Description] |

---

## Project-Specific Notes
- [Important note 1]
- [Important note 2]
</output_format>

<examples>
<example>
<input>
/claude-md
(in a Next.js e-commerce project)
</input>
<thinking>
1. Scan package.json - Next.js, React, TypeScript, Prisma
2. Check directory structure - App Router, features folder
3. Look for conventions - component patterns, imports
4. Identify key files - layout, api routes, prisma schema
5. Generate comprehensive CLAUDE.md
</thinking>
<output>
# ShopNext E-commerce

## Overview
A modern e-commerce platform built with Next.js 14 App Router, featuring product catalog, shopping cart, and Stripe checkout. Uses server components for performance and Prisma for database access.

---

## Tech Stack

| Category | Technology |
|----------|------------|
| Language | TypeScript 5.3 |
| Framework | Next.js 14.1 (App Router) |
| Database | PostgreSQL + Prisma 5.8 |
| Auth | NextAuth.js 5 |
| Payments | Stripe |
| Styling | Tailwind CSS 3.4 |
| Testing | Jest + React Testing Library |

---

## Directory Structure

```
shopnext/
├── src/
│   ├── app/              # Next.js App Router pages
│   │   ├── (shop)/       # Public storefront routes
│   │   ├── (admin)/      # Protected admin routes
│   │   └── api/          # API route handlers
│   ├── components/       # Shared React components
│   │   ├── ui/           # Base design system
│   │   └── layout/       # Layout components
│   ├── features/         # Feature modules
│   │   ├── products/     # Product catalog
│   │   ├── cart/         # Shopping cart
│   │   └── checkout/     # Checkout flow
│   ├── lib/              # Utilities and clients
│   └── types/            # TypeScript types
├── prisma/               # Database schema and migrations
└── __tests__/            # Test files
```

---

## Key Files

| File | Purpose |
|------|---------|
| `src/app/layout.tsx` | Root layout with providers |
| `src/middleware.ts` | Auth protection for routes |
| `prisma/schema.prisma` | Database schema |
| `src/lib/prisma.ts` | Prisma client instance |
| `src/lib/stripe.ts` | Stripe client configuration |
| `src/features/cart/store.ts` | Zustand cart store |

---

## Conventions

### Naming
- **Components**: PascalCase (`ProductCard.tsx`)
- **Hooks**: camelCase with `use` prefix (`useCart.ts`)
- **Utilities**: camelCase (`formatPrice.ts`)
- **Types**: lowercase with `.types.ts` suffix

### Code Style
- Server components by default, `'use client'` only when needed
- Prefer named exports over default exports
- Co-locate feature code (components, hooks, types together)

### Imports
```typescript
// 1. React/Next.js
import { useState } from 'react';
import { notFound } from 'next/navigation';

// 2. External packages
import { z } from 'zod';

// 3. Internal absolute (@/)
import { Button } from '@/components/ui/Button';
import { prisma } from '@/lib/prisma';

// 4. Relative
import { ProductCard } from './ProductCard';
```

---

## Common Patterns

### Server Component Data Fetching
```typescript
// In page.tsx - fetch data directly
async function ProductPage({ params }: Props) {
  const product = await prisma.product.findUnique({
    where: { id: params.id }
  });
  if (!product) notFound();
  return <ProductDetails product={product} />;
}
```

### Client Interactivity
```typescript
'use client';

function AddToCartButton({ productId }: Props) {
  const { addItem } = useCart();
  return (
    <Button onClick={() => addItem(productId)}>
      Add to Cart
    </Button>
  );
}
```

### API Route Handler
```typescript
// In route.ts
export async function GET(request: Request) {
  const products = await productService.findAll();
  return Response.json({ data: products });
}
```

---

## Commands

| Command | Purpose |
|---------|---------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm test` | Run Jest tests |
| `npm run db:migrate` | Run Prisma migrations |
| `npm run db:studio` | Open Prisma Studio |

---

## Project-Specific Notes
- Cart state persists via localStorage with Zustand persist middleware
- Product images require domain allowlist in `next.config.js`
- Stripe webhooks need raw body - see `src/app/api/webhooks/stripe/route.ts`
- Admin routes require `admin` role in session
</output>
</example>

<example>
<input>
/claude-md --refresh
(existing CLAUDE.md needs update)
</input>
<output>
# CLAUDE.md Refresh Report

**Changes Detected:**
- New dependency: `@tanstack/react-query` added
- New directory: `src/hooks/queries/`
- Updated: Node.js version in package.json (18 → 20)

---

## Updated Sections

### Tech Stack
Added: React Query 5.0 for server state management

### Directory Structure
Added: `src/hooks/queries/` for React Query hooks

### Common Patterns
Added: React Query pattern example

### Commands
Updated: Node.js version requirement

---

**Apply refresh?** (yes/no)
</output>
</example>
</examples>

<rules>
- Analyze actual codebase, don't assume patterns
- Keep CLAUDE.md concise but comprehensive
- Focus on what Claude needs to know for coding
- Include executable examples, not just descriptions
- Update when project structure changes significantly
- Don't include sensitive information (secrets, credentials)
</rules>

<error_handling>
If project too large: "Large project detected. Focus on core directories?"
If existing CLAUDE.md found: "CLAUDE.md exists. Refresh or create new?"
If no clear patterns: "Patterns unclear. What conventions should be documented?"
If multiple frameworks: "Multiple frameworks detected. Document all or specify primary?"
</error_handling>
