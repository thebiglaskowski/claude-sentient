# Pagination Pattern

## Intent

Efficiently retrieve large datasets in manageable chunks, reducing memory usage and improving response times.

---

## When to Use

- Lists with more than 20-50 items
- Database queries returning large result sets
- API responses that could grow unbounded
- Infinite scroll or "load more" UI patterns

## When NOT to Use

- Small, bounded datasets
- Data that must be processed atomically
- Real-time streaming requirements

---

## Pagination Strategies

### 1. Offset-Based (Traditional)

```
GET /api/users?page=2&limit=20
GET /api/users?offset=20&limit=20
```

**Pros:** Simple, familiar, allows jumping to any page
**Cons:** Performance degrades on large offsets, inconsistent with concurrent writes

### 2. Cursor-Based (Recommended)

```
GET /api/users?cursor=eyJpZCI6MTAwfQ&limit=20
```

**Pros:** Consistent with concurrent writes, efficient at any position
**Cons:** Can't jump to arbitrary pages, cursor management

### 3. Keyset (Seek)

```
GET /api/users?after_id=100&limit=20
```

**Pros:** Very efficient, simple implementation
**Cons:** Requires sortable unique key, forward-only

---

## Implementation

### TypeScript (Cursor-Based)

```typescript
// Types
interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    hasNextPage: boolean;
    hasPreviousPage: boolean;
    startCursor: string | null;
    endCursor: string | null;
    totalCount?: number;
  };
}

interface PaginationParams {
  first?: number;
  after?: string;
  last?: number;
  before?: string;
}

// Cursor encoding/decoding
function encodeCursor(data: Record<string, unknown>): string {
  return Buffer.from(JSON.stringify(data)).toString('base64url');
}

function decodeCursor(cursor: string): Record<string, unknown> {
  return JSON.parse(Buffer.from(cursor, 'base64url').toString());
}

// Repository implementation
class UserRepository {
  async findPaginated(
    params: PaginationParams,
    filter?: UserFilter
  ): Promise<PaginatedResponse<User>> {
    const { first = 20, after, last, before } = params;
    const limit = first || last || 20;

    // Build query
    let query = this.db
      .select('*')
      .from('users')
      .where(this.buildFilter(filter));

    // Apply cursor
    if (after) {
      const { id, createdAt } = decodeCursor(after);
      query = query.where(
        (qb) => qb
          .where('created_at', '<', createdAt)
          .orWhere((inner) =>
            inner.where('created_at', '=', createdAt).where('id', '<', id)
          )
      );
    }

    // Fetch one extra to determine hasNextPage
    const rows = await query
      .orderBy('created_at', 'desc')
      .orderBy('id', 'desc')
      .limit(limit + 1);

    const hasNextPage = rows.length > limit;
    const data = hasNextPage ? rows.slice(0, -1) : rows;

    return {
      data: data.map(this.toDomain),
      pagination: {
        hasNextPage,
        hasPreviousPage: !!after,
        startCursor: data[0]
          ? encodeCursor({ id: data[0].id, createdAt: data[0].created_at })
          : null,
        endCursor: data[data.length - 1]
          ? encodeCursor({
              id: data[data.length - 1].id,
              createdAt: data[data.length - 1].created_at,
            })
          : null,
      },
    };
  }
}

// Controller
app.get('/api/users', async (req, res) => {
  const { first, after, filter } = req.query;

  const result = await userRepository.findPaginated(
    { first: parseInt(first) || 20, after },
    filter
  );

  res.json({
    data: result.data,
    pageInfo: result.pagination,
    links: {
      next: result.pagination.hasNextPage
        ? `/api/users?first=${first}&after=${result.pagination.endCursor}`
        : null,
    },
  });
});
```

### Python (FastAPI)

```python
from typing import Generic, TypeVar, Optional, List
from pydantic import BaseModel
from base64 import urlsafe_b64encode, urlsafe_b64decode
import json

T = TypeVar('T')

class PageInfo(BaseModel):
    has_next_page: bool
    has_previous_page: bool
    start_cursor: Optional[str]
    end_cursor: Optional[str]
    total_count: Optional[int] = None

class PaginatedResponse(BaseModel, Generic[T]):
    data: List[T]
    page_info: PageInfo

def encode_cursor(data: dict) -> str:
    return urlsafe_b64encode(json.dumps(data).encode()).decode()

def decode_cursor(cursor: str) -> dict:
    return json.loads(urlsafe_b64decode(cursor.encode()).decode())

class UserRepository:
    async def find_paginated(
        self,
        first: int = 20,
        after: Optional[str] = None,
        filter: Optional[UserFilter] = None,
    ) -> PaginatedResponse[User]:
        query = select(User)

        if filter:
            query = self._apply_filter(query, filter)

        if after:
            cursor_data = decode_cursor(after)
            query = query.where(
                or_(
                    User.created_at < cursor_data["created_at"],
                    and_(
                        User.created_at == cursor_data["created_at"],
                        User.id < cursor_data["id"]
                    )
                )
            )

        query = query.order_by(User.created_at.desc(), User.id.desc())
        query = query.limit(first + 1)

        rows = await self.db.fetch_all(query)

        has_next = len(rows) > first
        data = rows[:first] if has_next else rows

        return PaginatedResponse(
            data=data,
            page_info=PageInfo(
                has_next_page=has_next,
                has_previous_page=after is not None,
                start_cursor=encode_cursor({
                    "id": data[0].id,
                    "created_at": data[0].created_at.isoformat()
                }) if data else None,
                end_cursor=encode_cursor({
                    "id": data[-1].id,
                    "created_at": data[-1].created_at.isoformat()
                }) if data else None,
            )
        )

# FastAPI endpoint
@router.get("/users", response_model=PaginatedResponse[UserResponse])
async def list_users(
    first: int = Query(20, ge=1, le=100),
    after: Optional[str] = None,
    repo: UserRepository = Depends(),
):
    return await repo.find_paginated(first=first, after=after)
```

### Go

```go
type PageInfo struct {
    HasNextPage     bool    `json:"hasNextPage"`
    HasPreviousPage bool    `json:"hasPreviousPage"`
    StartCursor     *string `json:"startCursor,omitempty"`
    EndCursor       *string `json:"endCursor,omitempty"`
    TotalCount      *int    `json:"totalCount,omitempty"`
}

type PaginatedResponse[T any] struct {
    Data     []T      `json:"data"`
    PageInfo PageInfo `json:"pageInfo"`
}

type Cursor struct {
    ID        string    `json:"id"`
    CreatedAt time.Time `json:"createdAt"`
}

func EncodeCursor(c Cursor) string {
    data, _ := json.Marshal(c)
    return base64.URLEncoding.EncodeToString(data)
}

func DecodeCursor(s string) (Cursor, error) {
    data, err := base64.URLEncoding.DecodeString(s)
    if err != nil {
        return Cursor{}, err
    }
    var c Cursor
    err = json.Unmarshal(data, &c)
    return c, err
}

func (r *UserRepository) FindPaginated(
    ctx context.Context,
    first int,
    after *string,
) (*PaginatedResponse[User], error) {
    query := `
        SELECT * FROM users
        WHERE ($1::timestamp IS NULL OR created_at < $1
               OR (created_at = $1 AND id < $2))
        ORDER BY created_at DESC, id DESC
        LIMIT $3
    `

    var cursorTime *time.Time
    var cursorID *string
    if after != nil {
        cursor, _ := DecodeCursor(*after)
        cursorTime = &cursor.CreatedAt
        cursorID = &cursor.ID
    }

    rows, err := r.db.QueryContext(ctx, query, cursorTime, cursorID, first+1)
    if err != nil {
        return nil, err
    }
    defer rows.Close()

    var users []User
    for rows.Next() {
        var u User
        if err := rows.Scan(&u.ID, &u.Email, &u.CreatedAt); err != nil {
            return nil, err
        }
        users = append(users, u)
    }

    hasNext := len(users) > first
    if hasNext {
        users = users[:first]
    }

    var startCursor, endCursor *string
    if len(users) > 0 {
        sc := EncodeCursor(Cursor{ID: users[0].ID, CreatedAt: users[0].CreatedAt})
        ec := EncodeCursor(Cursor{ID: users[len(users)-1].ID, CreatedAt: users[len(users)-1].CreatedAt})
        startCursor = &sc
        endCursor = &ec
    }

    return &PaginatedResponse[User]{
        Data: users,
        PageInfo: PageInfo{
            HasNextPage:     hasNext,
            HasPreviousPage: after != nil,
            StartCursor:     startCursor,
            EndCursor:       endCursor,
        },
    }, nil
}
```

---

## Response Formats

### REST (JSON:API style)

```json
{
  "data": [...],
  "meta": {
    "totalCount": 1000,
    "pageSize": 20
  },
  "links": {
    "self": "/api/users?page=2",
    "first": "/api/users?page=1",
    "prev": "/api/users?page=1",
    "next": "/api/users?page=3",
    "last": "/api/users?page=50"
  }
}
```

### GraphQL (Relay Connection)

```graphql
type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int
}

type UserEdge {
  node: User!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}
```

---

## Related Patterns

- **Caching** — Cache paginated results
- **Rate Limiting** — Prevent abuse of pagination
- **Filtering** — Combine with pagination
- **Sorting** — Affect cursor behavior

---

## Anti-Patterns

- **Large offsets** — Use cursor instead for deep pagination
- **Unbounded page size** — Always enforce max limit
- **No total count option** — Can be expensive, make optional
- **Inconsistent ordering** — Must have stable sort for cursors
