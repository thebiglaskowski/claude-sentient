---
name: snippet-library
description: Reusable code patterns and boilerplate
disable-model-invocation: true
---

# Code Snippet Library

Reusable code patterns and boilerplate.

## Description

Library of commonly used code snippets for quick insertion.
Triggers on: "snippet", "boilerplate", "template code", "give me the code for", "standard pattern".

## Snippet Categories

### API Snippets

#### Express Route Handler
```typescript
// snippet:express-route
import { Request, Response, NextFunction } from 'express'

export const handlerName = async (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  try {
    // Implementation
    res.json({ success: true, data: {} })
  } catch (error) {
    next(error)
  }
}
```

#### Express Router Setup
```typescript
// snippet:express-router
import { Router } from 'express'
import { authenticate } from '../middleware/auth'

const router = Router()

router.get('/', authenticate, getAll)
router.get('/:id', authenticate, getById)
router.post('/', authenticate, create)
router.put('/:id', authenticate, update)
router.delete('/:id', authenticate, remove)

export default router
```

#### API Error Class
```typescript
// snippet:api-error
export class ApiError extends Error {
  constructor(
    public statusCode: number,
    public message: string,
    public code?: string
  ) {
    super(message)
    this.name = 'ApiError'
  }

  static badRequest(message: string) {
    return new ApiError(400, message, 'BAD_REQUEST')
  }

  static unauthorized(message = 'Unauthorized') {
    return new ApiError(401, message, 'UNAUTHORIZED')
  }

  static notFound(message = 'Not found') {
    return new ApiError(404, message, 'NOT_FOUND')
  }
}
```

### React Snippets

#### Functional Component
```tsx
// snippet:react-component
import { FC } from 'react'

interface Props {
  // props
}

export const ComponentName: FC<Props> = ({ }) => {
  return (
    <div>
      {/* content */}
    </div>
  )
}
```

#### Custom Hook
```tsx
// snippet:react-hook
import { useState, useEffect } from 'react'

export function useHookName(param: ParamType) {
  const [state, setState] = useState<StateType>(initialValue)

  useEffect(() => {
    // effect
    return () => {
      // cleanup
    }
  }, [param])

  return { state }
}
```

#### Context Provider
```tsx
// snippet:react-context
import { createContext, useContext, useState, ReactNode } from 'react'

interface ContextType {
  value: string
  setValue: (value: string) => void
}

const Context = createContext<ContextType | undefined>(undefined)

export function Provider({ children }: { children: ReactNode }) {
  const [value, setValue] = useState('')

  return (
    <Context.Provider value={{ value, setValue }}>
      {children}
    </Context.Provider>
  )
}

export function useContextName() {
  const context = useContext(Context)
  if (!context) {
    throw new Error('useContextName must be used within Provider')
  }
  return context
}
```

### Testing Snippets

#### Jest Test Suite
```typescript
// snippet:jest-suite
describe('ModuleName', () => {
  beforeEach(() => {
    // setup
  })

  afterEach(() => {
    // cleanup
  })

  describe('functionName', () => {
    it('should handle normal case', () => {
      // arrange
      // act
      // assert
    })

    it('should handle edge case', () => {
      // test
    })

    it('should throw on invalid input', () => {
      expect(() => functionName(invalid)).toThrow()
    })
  })
})
```

#### Mock Setup
```typescript
// snippet:jest-mock
jest.mock('../services/api', () => ({
  fetchData: jest.fn(),
}))

import { fetchData } from '../services/api'

const mockFetchData = fetchData as jest.MockedFunction<typeof fetchData>

beforeEach(() => {
  mockFetchData.mockClear()
})

it('should call api', async () => {
  mockFetchData.mockResolvedValue({ data: 'test' })

  // test

  expect(mockFetchData).toHaveBeenCalledWith(expectedArgs)
})
```

### Database Snippets

#### Prisma Model
```prisma
// snippet:prisma-model
model ModelName {
  id        String   @id @default(cuid())
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  // fields
  name      String
  email     String   @unique

  // relations
  posts     Post[]

  @@map("table_name")
}
```

#### Prisma Query
```typescript
// snippet:prisma-query
const result = await prisma.modelName.findMany({
  where: {
    field: value,
  },
  include: {
    relation: true,
  },
  orderBy: {
    createdAt: 'desc',
  },
  take: 10,
  skip: 0,
})
```

### Utility Snippets

#### Async Handler
```typescript
// snippet:async-handler
export const asyncHandler = <T>(
  fn: (req: Request, res: Response, next: NextFunction) => Promise<T>
) => {
  return (req: Request, res: Response, next: NextFunction) => {
    Promise.resolve(fn(req, res, next)).catch(next)
  }
}
```

#### Retry Logic
```typescript
// snippet:retry
async function retry<T>(
  fn: () => Promise<T>,
  maxAttempts = 3,
  delay = 1000
): Promise<T> {
  let lastError: Error

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn()
    } catch (error) {
      lastError = error as Error
      if (attempt < maxAttempts) {
        await new Promise(resolve => setTimeout(resolve, delay * attempt))
      }
    }
  }

  throw lastError!
}
```

#### Debounce
```typescript
// snippet:debounce
function debounce<T extends (...args: any[]) => any>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timeoutId: NodeJS.Timeout

  return (...args: Parameters<T>) => {
    clearTimeout(timeoutId)
    timeoutId = setTimeout(() => fn(...args), delay)
  }
}
```

## Snippet Usage

### Insert Snippet
```
"Give me the express route handler snippet"
"Insert react component boilerplate"
"Add jest test suite template"
```

### Customize on Insert
```markdown
**Inserting:** snippet:react-component

**Customizations:**
- Component name: `UserProfile`
- Props: `{ userId: string, onUpdate: () => void }`

**Generated:**
```tsx
interface Props {
  userId: string
  onUpdate: () => void
}

export const UserProfile: FC<Props> = ({ userId, onUpdate }) => {
  return (
    <div>
      {/* content */}
    </div>
  )
}
```
```

### List Available Snippets
```
"What snippets do you have?"
"List API snippets"
"Show testing templates"
```

## Custom Snippets

### Add Project Snippet
Save to `.claude/snippets/`:

```markdown
# snippet:project-service

```typescript
import { prisma } from '../lib/db'
import { ApiError } from '../utils/errors'

export class ${ServiceName}Service {
  async getAll() {
    return prisma.${modelName}.findMany()
  }

  async getById(id: string) {
    const item = await prisma.${modelName}.findUnique({ where: { id } })
    if (!item) throw ApiError.notFound()
    return item
  }

  async create(data: Create${ModelName}Input) {
    return prisma.${modelName}.create({ data })
  }

  async update(id: string, data: Update${ModelName}Input) {
    return prisma.${modelName}.update({ where: { id }, data })
  }

  async delete(id: string) {
    return prisma.${modelName}.delete({ where: { id } })
  }
}
```
```

### Snippet Variables
| Variable | Description |
|----------|-------------|
| `${Name}` | PascalCase name |
| `${name}` | camelCase name |
| `${NAME}` | UPPER_CASE name |
| `${date}` | Current date |
| `${author}` | Git user name |

## Snippet Library Structure

```
.claude/snippets/
├── api/
│   ├── route-handler.md
│   ├── middleware.md
│   └── error-handling.md
├── react/
│   ├── component.md
│   ├── hook.md
│   └── context.md
├── testing/
│   ├── jest-suite.md
│   └── mock-setup.md
└── utils/
    ├── async.md
    └── helpers.md
```

## Integration

### VS Code Snippets
Export to VS Code format:
```json
{
  "React Component": {
    "prefix": "rfc",
    "body": ["..."],
    "description": "React functional component"
  }
}
```

### IntelliJ Live Templates
Export to IntelliJ format for team sharing.
