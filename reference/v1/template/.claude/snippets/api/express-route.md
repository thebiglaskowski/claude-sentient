# Snippet: express-route

## Description

Express.js route handler with proper error handling, validation, and TypeScript types.

## When to Use

- Creating new API endpoints
- REST resource operations
- Backend route handlers

## Code

```typescript
import { Router, Request, Response, NextFunction } from 'express';
import { z } from 'zod';
import { validateRequest } from '@/middleware/validate';
import { asyncHandler } from '@/middleware/async-handler';
import { NotFoundError } from '@/errors';

const router = Router();

// Validation schemas
const createSchema = z.object({
  body: z.object({
    name: z.string().min(1).max(100),
    email: z.string().email(),
  }),
});

const paramsSchema = z.object({
  params: z.object({
    id: z.string().uuid(),
  }),
});

const querySchema = z.object({
  query: z.object({
    page: z.coerce.number().int().positive().default(1),
    limit: z.coerce.number().int().min(1).max(100).default(20),
    sort: z.enum(['asc', 'desc']).default('desc'),
  }),
});

// GET /resources
router.get(
  '/',
  validateRequest(querySchema),
  asyncHandler(async (req: Request, res: Response) => {
    const { page, limit, sort } = req.query;

    const result = await resourceService.findAll({
      page: Number(page),
      limit: Number(limit),
      sort: sort as 'asc' | 'desc',
    });

    res.json({
      data: result.data,
      pagination: {
        page: result.page,
        limit: result.limit,
        total: result.total,
        totalPages: result.totalPages,
      },
    });
  })
);

// GET /resources/:id
router.get(
  '/:id',
  validateRequest(paramsSchema),
  asyncHandler(async (req: Request, res: Response) => {
    const { id } = req.params;

    const resource = await resourceService.findById(id);
    if (!resource) {
      throw new NotFoundError('Resource not found');
    }

    res.json({ data: resource });
  })
);

// POST /resources
router.post(
  '/',
  validateRequest(createSchema),
  asyncHandler(async (req: Request, res: Response) => {
    const resource = await resourceService.create(req.body);

    res.status(201).json({ data: resource });
  })
);

// PUT /resources/:id
router.put(
  '/:id',
  validateRequest(paramsSchema.merge(createSchema)),
  asyncHandler(async (req: Request, res: Response) => {
    const { id } = req.params;

    const resource = await resourceService.update(id, req.body);
    if (!resource) {
      throw new NotFoundError('Resource not found');
    }

    res.json({ data: resource });
  })
);

// DELETE /resources/:id
router.delete(
  '/:id',
  validateRequest(paramsSchema),
  asyncHandler(async (req: Request, res: Response) => {
    const { id } = req.params;

    await resourceService.delete(id);

    res.status(204).send();
  })
);

export default router;
```

### Async Handler Middleware

```typescript
// middleware/async-handler.ts
import { Request, Response, NextFunction, RequestHandler } from 'express';

export const asyncHandler = (
  fn: (req: Request, res: Response, next: NextFunction) => Promise<any>
): RequestHandler => {
  return (req, res, next) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
};
```

### Validation Middleware

```typescript
// middleware/validate.ts
import { Request, Response, NextFunction } from 'express';
import { AnyZodObject, ZodError } from 'zod';
import { ValidationError } from '@/errors';

export const validateRequest = (schema: AnyZodObject) => {
  return async (req: Request, res: Response, next: NextFunction) => {
    try {
      await schema.parseAsync({
        body: req.body,
        query: req.query,
        params: req.params,
      });
      next();
    } catch (error) {
      if (error instanceof ZodError) {
        next(new ValidationError(error.errors));
      } else {
        next(error);
      }
    }
  };
};
```

## Customization Points

- `resourceService` — Replace with your service
- `Resource` — Replace with your entity type
- Validation schemas — Adjust fields for your data
- Route path — Change `/resources` to your resource name

## Related Snippets

- [error-class](../utility/error-class.md) — Custom error classes
- [zod-schema](../validation/zod-schema.md) — Zod validation
- [jest-test](../testing/jest-test.md) — Test this route
