# Repository Pattern

## Intent

Abstract data access logic behind a collection-like interface, decoupling business logic from persistence details.

---

## When to Use

- Multiple data sources (database, API, cache)
- Need to swap persistence layer
- Complex queries that should be reusable
- Unit testing requires data isolation
- Domain models differ from database schema

## When NOT to Use

- Simple CRUD with no business logic
- Single, unchanging data source
- Prototype or throwaway code
- ORM already provides sufficient abstraction

---

## Structure

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Business Logic │ ──▶ │   Repository    │ ──▶ │   Data Source   │
│    (Service)    │     │   (Interface)   │     │ (DB/API/Cache)  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                              │
                              ▼
                        ┌─────────────────┐
                        │   Repository    │
                        │ (Implementation)│
                        └─────────────────┘
```

---

## Implementation

### TypeScript

```typescript
// Interface
interface UserRepository {
  findById(id: string): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
  findAll(filter?: UserFilter): Promise<User[]>;
  save(user: User): Promise<User>;
  delete(id: string): Promise<void>;
}

// Implementation
class PostgresUserRepository implements UserRepository {
  constructor(private db: Database) {}

  async findById(id: string): Promise<User | null> {
    const row = await this.db.query(
      'SELECT * FROM users WHERE id = $1',
      [id]
    );
    return row ? this.toDomain(row) : null;
  }

  async findByEmail(email: string): Promise<User | null> {
    const row = await this.db.query(
      'SELECT * FROM users WHERE email = $1',
      [email]
    );
    return row ? this.toDomain(row) : null;
  }

  async findAll(filter?: UserFilter): Promise<User[]> {
    const { query, params } = this.buildQuery(filter);
    const rows = await this.db.query(query, params);
    return rows.map(this.toDomain);
  }

  async save(user: User): Promise<User> {
    const row = await this.db.query(
      `INSERT INTO users (id, email, name, created_at)
       VALUES ($1, $2, $3, $4)
       ON CONFLICT (id) DO UPDATE SET email = $2, name = $3
       RETURNING *`,
      [user.id, user.email, user.name, user.createdAt]
    );
    return this.toDomain(row);
  }

  async delete(id: string): Promise<void> {
    await this.db.query('DELETE FROM users WHERE id = $1', [id]);
  }

  private toDomain(row: UserRow): User {
    return new User({
      id: row.id,
      email: row.email,
      name: row.name,
      createdAt: row.created_at,
    });
  }

  private buildQuery(filter?: UserFilter): { query: string; params: any[] } {
    // Build dynamic query based on filter
  }
}

// Usage in service
class UserService {
  constructor(private userRepo: UserRepository) {}

  async getUser(id: string): Promise<User> {
    const user = await this.userRepo.findById(id);
    if (!user) throw new NotFoundError('User not found');
    return user;
  }
}
```

### Python

```python
from abc import ABC, abstractmethod
from typing import Optional, List

class UserRepository(ABC):
    @abstractmethod
    def find_by_id(self, id: str) -> Optional[User]:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def find_all(self, filter: Optional[UserFilter] = None) -> List[User]:
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def delete(self, id: str) -> None:
        pass


class PostgresUserRepository(UserRepository):
    def __init__(self, db: Database):
        self._db = db

    def find_by_id(self, id: str) -> Optional[User]:
        row = self._db.query_one(
            "SELECT * FROM users WHERE id = %s", (id,)
        )
        return self._to_domain(row) if row else None

    def save(self, user: User) -> User:
        row = self._db.query_one(
            """
            INSERT INTO users (id, email, name, created_at)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET email = %s, name = %s
            RETURNING *
            """,
            (user.id, user.email, user.name, user.created_at,
             user.email, user.name)
        )
        return self._to_domain(row)

    def _to_domain(self, row: dict) -> User:
        return User(
            id=row["id"],
            email=row["email"],
            name=row["name"],
            created_at=row["created_at"],
        )
```

### Go

```go
type UserRepository interface {
    FindByID(ctx context.Context, id string) (*User, error)
    FindByEmail(ctx context.Context, email string) (*User, error)
    FindAll(ctx context.Context, filter *UserFilter) ([]*User, error)
    Save(ctx context.Context, user *User) (*User, error)
    Delete(ctx context.Context, id string) error
}

type postgresUserRepository struct {
    db *sql.DB
}

func NewPostgresUserRepository(db *sql.DB) UserRepository {
    return &postgresUserRepository{db: db}
}

func (r *postgresUserRepository) FindByID(ctx context.Context, id string) (*User, error) {
    row := r.db.QueryRowContext(ctx,
        "SELECT id, email, name, created_at FROM users WHERE id = $1", id)

    var u User
    err := row.Scan(&u.ID, &u.Email, &u.Name, &u.CreatedAt)
    if err == sql.ErrNoRows {
        return nil, nil
    }
    if err != nil {
        return nil, fmt.Errorf("query user: %w", err)
    }
    return &u, nil
}
```

---

## Variations

### Generic Repository

```typescript
interface Repository<T, ID> {
  findById(id: ID): Promise<T | null>;
  findAll(): Promise<T[]>;
  save(entity: T): Promise<T>;
  delete(id: ID): Promise<void>;
}
```

### Specification Pattern

```typescript
interface Specification<T> {
  isSatisfiedBy(entity: T): boolean;
  toQuery(): QueryFragment;
}

interface UserRepository {
  findBySpec(spec: Specification<User>): Promise<User[]>;
}
```

### Unit of Work

```typescript
interface UnitOfWork {
  users: UserRepository;
  orders: OrderRepository;
  commit(): Promise<void>;
  rollback(): Promise<void>;
}
```

---

## Related Patterns

- **Service Layer** — Uses repositories for data access
- **Unit of Work** — Coordinates multiple repositories
- **Factory** — Creates repository instances
- **Adapter** — Repository adapts data source interface

---

## Anti-Patterns

- **Leaky abstraction** — Exposing ORM/query details
- **God repository** — Too many methods, split by aggregate
- **Anemic repository** — Just wrapping ORM without value
- **Business logic in repository** — Keep it in service layer
