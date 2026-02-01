# Database Rules

## Core Principles

1. **Data integrity first** — Constraints prevent bugs
2. **Normalize, then denormalize** — Start clean, optimize later
3. **Index strategically** — Every index has a cost
4. **Migrations are code** — Version controlled, reversible
5. **Backups are mandatory** — Test restores regularly

---

## Schema Design

### Naming Conventions

```sql
-- Tables: plural, snake_case
CREATE TABLE users (...);
CREATE TABLE order_items (...);

-- Columns: snake_case
user_id, created_at, is_active

-- Primary keys: id or table_id
id SERIAL PRIMARY KEY
-- or
user_id UUID PRIMARY KEY

-- Foreign keys: referenced_table_id
user_id INTEGER REFERENCES users(id)

-- Indexes: idx_table_columns
CREATE INDEX idx_orders_user_id ON orders(user_id);
```

### Data Types

| Use Case | Type | Not |
|----------|------|-----|
| IDs | `UUID` or `BIGINT` | `INT` (runs out) |
| Money | `DECIMAL(19,4)` | `FLOAT` (precision loss) |
| Timestamps | `TIMESTAMPTZ` | `TIMESTAMP` (no timezone) |
| Status | `ENUM` or lookup table | `VARCHAR` |
| Large text | `TEXT` | `VARCHAR(MAX)` |
| Boolean | `BOOLEAN` | `INT` (0/1) |

### Required Columns

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  -- ... your columns ...
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  deleted_at TIMESTAMPTZ -- for soft deletes
);
```

---

## Constraints

### Always Use

```sql
-- Primary key
PRIMARY KEY (id)

-- Foreign keys with cascade rules
FOREIGN KEY (user_id) REFERENCES users(id)
  ON DELETE CASCADE  -- or RESTRICT, SET NULL
  ON UPDATE CASCADE

-- Not null for required fields
email VARCHAR(255) NOT NULL

-- Unique constraints
UNIQUE (email)

-- Check constraints for validation
CHECK (price >= 0)
CHECK (status IN ('pending', 'active', 'completed'))
```

### Constraint Examples

```sql
CREATE TABLE orders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  status VARCHAR(20) NOT NULL DEFAULT 'pending'
    CHECK (status IN ('pending', 'paid', 'shipped', 'delivered', 'cancelled')),
  total_cents INTEGER NOT NULL CHECK (total_cents >= 0),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

---

## Indexing Strategy

### When to Index

| Scenario | Index Type |
|----------|------------|
| Foreign keys | B-tree (default) |
| Unique lookups | Unique B-tree |
| Text search | GIN with tsvector |
| JSON queries | GIN |
| Range queries | B-tree |
| Geospatial | GiST or SP-GiST |

### Index Examples

```sql
-- Single column
CREATE INDEX idx_users_email ON users(email);

-- Composite (order matters!)
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- Partial (filtered)
CREATE INDEX idx_active_users ON users(email) WHERE deleted_at IS NULL;

-- Covering (includes all queried columns)
CREATE INDEX idx_orders_user_covering ON orders(user_id)
  INCLUDE (status, total_cents);
```

### Index Anti-Patterns

```sql
-- Too many indexes (slows writes)
-- Index on low-cardinality columns
CREATE INDEX idx_users_active ON users(is_active); -- Bad: only true/false

-- Index not matching query patterns
-- Query: WHERE user_id = ? AND status = ?
CREATE INDEX idx_orders_status ON orders(status); -- Missing user_id
```

---

## Migrations

### Safe Migration Practices

```sql
-- 1. Add columns as nullable first
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- 2. Backfill data (in batches for large tables)
UPDATE users SET phone = 'unknown' WHERE phone IS NULL;

-- 3. Add NOT NULL constraint after backfill
ALTER TABLE users ALTER COLUMN phone SET NOT NULL;

-- 4. Add index CONCURRENTLY (no lock)
CREATE INDEX CONCURRENTLY idx_users_phone ON users(phone);
```

### Dangerous Operations

```sql
-- DANGEROUS: Locks table
ALTER TABLE large_table ADD COLUMN x NOT NULL DEFAULT 'value';

-- SAFE: Add nullable, backfill, then constrain
ALTER TABLE large_table ADD COLUMN x VARCHAR(50);
-- Backfill in batches
ALTER TABLE large_table ALTER COLUMN x SET NOT NULL;
```

### Migration Checklist

- [ ] Can be rolled back
- [ ] Won't lock tables for long
- [ ] Backfill runs in batches
- [ ] Tested on copy of production data
- [ ] Index creation is CONCURRENT

---

## Query Patterns

### Good Patterns

```sql
-- Pagination with cursor (better for large datasets)
SELECT * FROM orders
WHERE created_at < '2026-01-29'
ORDER BY created_at DESC
LIMIT 20;

-- Batch operations
UPDATE users SET synced = true
WHERE id IN (SELECT id FROM users WHERE synced = false LIMIT 1000);

-- Upsert
INSERT INTO users (email, name)
VALUES ('user@example.com', 'User')
ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name;
```

### Anti-Patterns

```sql
-- SELECT * (over-fetching)
SELECT * FROM users; -- Select specific columns

-- No LIMIT (dangerous)
SELECT id FROM large_table; -- Add LIMIT

-- OR on different columns (hard to index)
WHERE user_id = 1 OR email = 'x'; -- Use UNION instead

-- Functions on indexed columns
WHERE LOWER(email) = 'x'; -- Create functional index
```

---

## Database Checklist

### Schema
- [ ] All tables have primary keys
- [ ] Foreign keys have constraints
- [ ] Appropriate data types used
- [ ] Timestamps on all tables
- [ ] Enums or lookup tables for fixed values

### Performance
- [ ] Indexes on all foreign keys
- [ ] Indexes match query patterns
- [ ] No N+1 queries
- [ ] Large queries use pagination
- [ ] EXPLAIN shows index usage

### Safety
- [ ] Migrations are reversible
- [ ] Backups run daily
- [ ] Restore tested monthly
- [ ] Sensitive data encrypted
- [ ] Audit logging for PII access
