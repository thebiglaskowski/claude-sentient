# API Design Rules

## Core Principles

1. **Consistency** — Same patterns everywhere
2. **Predictability** — Clients can guess behavior
3. **Backward compatibility** — Don't break existing clients
4. **Self-documenting** — Clear names and structures
5. **Stateless** — No server-side session state

---

## REST URL Design

### Resource Naming
```
# Use nouns, not verbs
GET /users          (not /getUsers)
POST /orders        (not /createOrder)
DELETE /users/123   (not /deleteUser/123)

# Use plural nouns
GET /users          (not /user)
GET /orders         (not /order)

# Use lowercase with hyphens
GET /user-profiles  (not /userProfiles or /user_profiles)

# Nest for relationships
GET /users/123/orders
GET /orders/456/items
```

### HTTP Methods
| Method | Use Case | Idempotent |
|--------|----------|------------|
| GET | Retrieve resource(s) | Yes |
| POST | Create new resource | No |
| PUT | Replace entire resource | Yes |
| PATCH | Update partial resource | Yes |
| DELETE | Remove resource | Yes |

### URL Examples
```
# Collection operations
GET    /api/v1/users           # List users
POST   /api/v1/users           # Create user

# Instance operations
GET    /api/v1/users/123       # Get user
PUT    /api/v1/users/123       # Replace user
PATCH  /api/v1/users/123       # Update user
DELETE /api/v1/users/123       # Delete user

# Nested resources
GET    /api/v1/users/123/orders
POST   /api/v1/users/123/orders

# Actions (when REST verbs don't fit)
POST   /api/v1/users/123/actions/deactivate
POST   /api/v1/orders/456/actions/cancel
```

---

## Request/Response Formats

### Standard Response Envelope
```json
{
  "data": { ... },
  "meta": {
    "timestamp": "2024-01-15T10:00:00Z",
    "requestId": "req_abc123"
  }
}
```

### Collection Response
```json
{
  "data": [
    { "id": "1", "name": "Item 1" },
    { "id": "2", "name": "Item 2" }
  ],
  "meta": {
    "total": 100,
    "page": 1,
    "perPage": 20,
    "totalPages": 5
  },
  "links": {
    "self": "/api/v1/items?page=1",
    "next": "/api/v1/items?page=2",
    "last": "/api/v1/items?page=5"
  }
}
```

### Error Response
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": [
      {
        "field": "email",
        "code": "INVALID_FORMAT",
        "message": "Email must be a valid email address"
      }
    ]
  },
  "meta": {
    "timestamp": "2024-01-15T10:00:00Z",
    "requestId": "req_abc123"
  }
}
```

---

## HTTP Status Codes

### Success Codes
| Code | Meaning | Use Case |
|------|---------|----------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |

### Client Error Codes
| Code | Meaning | Use Case |
|------|---------|----------|
| 400 | Bad Request | Invalid syntax/parameters |
| 401 | Unauthorized | Missing/invalid authentication |
| 403 | Forbidden | Valid auth, insufficient permission |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | State conflict (duplicate, etc.) |
| 422 | Unprocessable | Valid syntax, semantic error |
| 429 | Too Many Requests | Rate limit exceeded |

### Server Error Codes
| Code | Meaning | Use Case |
|------|---------|----------|
| 500 | Internal Error | Unexpected server error |
| 502 | Bad Gateway | Upstream service error |
| 503 | Service Unavailable | Temporary overload/maintenance |

---

## Versioning

### URL Versioning (Recommended)
```
/api/v1/users
/api/v2/users
```

### Header Versioning (Alternative)
```
Accept: application/vnd.myapp.v1+json
```

### Versioning Rules
- Never break backward compatibility in same version
- Deprecate before removing
- Support N-1 version minimum
- Document migration path

---

## Pagination

### Offset Pagination
```
GET /users?page=2&perPage=20
GET /users?offset=40&limit=20
```

### Cursor Pagination (Recommended for large sets)
```
GET /users?cursor=eyJpZCI6MTIzfQ&limit=20

Response:
{
  "data": [...],
  "cursors": {
    "next": "eyJpZCI6MTQzfQ",
    "previous": "eyJpZCI6MTAzfQ"
  }
}
```

---

## Filtering & Sorting

### Query Parameters
```
# Filtering
GET /users?status=active
GET /users?status=active,pending
GET /users?createdAt[gte]=2024-01-01
GET /users?search=john

# Sorting
GET /users?sort=name        # ascending
GET /users?sort=-createdAt  # descending
GET /users?sort=name,-createdAt  # multiple

# Field selection
GET /users?fields=id,name,email
```

---

## Rate Limiting

### Headers
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1705315200
```

### 429 Response
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests",
    "retryAfter": 60
  }
}
```

---

## Idempotency

### For Non-Idempotent Operations
```
# Client sends idempotency key
POST /orders
Idempotency-Key: unique-request-id-123

# Server checks key, returns cached response if duplicate
```

---

## Anti-Patterns

### Avoid These
```
# Verbs in URLs
GET /getUser/123
POST /createOrder

# Inconsistent naming
GET /users/123
GET /order/456  # Should be /orders/456

# Nested too deep
GET /users/123/orders/456/items/789/reviews

# Returning 200 for errors
HTTP 200 OK
{ "success": false, "error": "Not found" }

# Exposing internal IDs
{ "id": 12345 }  # Better: UUID or encoded ID
```

---

## API Checklist

Before releasing:
- [ ] URLs follow REST conventions
- [ ] HTTP methods used correctly
- [ ] Status codes are appropriate
- [ ] Error responses are structured
- [ ] Pagination implemented
- [ ] Rate limiting in place
- [ ] Versioning strategy defined
- [ ] Authentication documented
- [ ] OpenAPI spec generated
- [ ] Examples for all endpoints
