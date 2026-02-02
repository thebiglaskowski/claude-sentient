# Performance Rules

## Core Principles

1. **Measure first** — Profile before optimizing
2. **Optimize the right thing** — Focus on bottlenecks
3. **Trade-offs are real** — Understand what you sacrifice
4. **Cache strategically** — Right data, right duration
5. **User perception matters** — Perceived speed ≠ actual speed

---

## Web Performance (Core Web Vitals)

### Targets

| Metric | Good | Needs Work | Poor |
|--------|------|------------|------|
| LCP (Largest Contentful Paint) | ≤2.5s | ≤4s | >4s |
| FID (First Input Delay) | ≤100ms | ≤300ms | >300ms |
| CLS (Cumulative Layout Shift) | ≤0.1 | ≤0.25 | >0.25 |
| TTFB (Time to First Byte) | ≤800ms | ≤1.8s | >1.8s |

### Optimization Strategies

```javascript
// Lazy load images
<img loading="lazy" src="image.jpg" alt="..." />

// Preload critical resources
<link rel="preload" href="critical.css" as="style" />
<link rel="preload" href="hero.jpg" as="image" />

// Defer non-critical JavaScript
<script defer src="analytics.js"></script>
```

---

## API Performance

### Response Time Targets

| Endpoint Type | Target | Max Acceptable |
|---------------|--------|----------------|
| Health check | <10ms | <50ms |
| Simple CRUD | <100ms | <500ms |
| List with pagination | <200ms | <1s |
| Complex aggregation | <500ms | <2s |
| Report generation | <2s | <10s |

### Optimization Patterns

```javascript
// Pagination - never return unlimited results
app.get('/users', async (req, res) => {
  const { page = 1, limit = 20 } = req.query;
  const users = await User.findAll({
    limit: Math.min(limit, 100), // Cap at 100
    offset: (page - 1) * limit,
  });
});

// Field selection - return only needed fields
const user = await User.findOne({
  attributes: ['id', 'name', 'email'], // Not SELECT *
  where: { id }
});

// Parallel requests when possible
const [users, orders, stats] = await Promise.all([
  getUsers(),
  getOrders(),
  getStats()
]);
```

---

## Database Performance

### Query Optimization

```sql
-- Use EXPLAIN to analyze queries
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 123;

-- Index foreign keys
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- Composite indexes for common queries
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- Avoid SELECT *
SELECT id, name, email FROM users WHERE active = true;
```

### N+1 Prevention

```javascript
// Bad: N+1 queries
const users = await User.findAll();
for (const user of users) {
  user.orders = await Order.findAll({ where: { userId: user.id } });
}

// Good: Eager loading
const users = await User.findAll({
  include: [{ model: Order }]
});

// Good: Batch loading
const userIds = users.map(u => u.id);
const orders = await Order.findAll({
  where: { userId: { [Op.in]: userIds } }
});
```

---

## Caching Strategy

### Cache Hierarchy

```
Request → CDN → Application Cache → Database Cache → Database
         (1)          (2)                (3)           (4)

1. CDN: Static assets, API responses (public)
2. Application: Redis/Memcached for computed data
3. Database: Query cache, connection pool
4. Database: Actual queries (last resort)
```

### Cache Patterns

```javascript
// Cache-aside pattern
async function getUser(id) {
  const cached = await redis.get(`user:${id}`);
  if (cached) return JSON.parse(cached);

  const user = await db.users.findOne({ where: { id } });
  await redis.setex(`user:${id}`, 3600, JSON.stringify(user));
  return user;
}

// Cache invalidation
async function updateUser(id, data) {
  await db.users.update(data, { where: { id } });
  await redis.del(`user:${id}`); // Invalidate cache
}
```

### TTL Guidelines

| Data Type | TTL | Reason |
|-----------|-----|--------|
| Static content | 1 year | Versioned URLs |
| User session | 30 min | Security |
| API response | 1-5 min | Freshness |
| Computed stats | 15-60 min | Expensive to compute |
| User profile | 1 hour | Rarely changes |

---

## Frontend Performance

### Bundle Optimization

```javascript
// Code splitting
const Dashboard = lazy(() => import('./Dashboard'));

// Dynamic imports
const loadChart = async () => {
  const { Chart } = await import('chart.js');
  return Chart;
};

// Tree shaking - import only what you need
import { debounce } from 'lodash-es'; // Not import _ from 'lodash'
```

### Image Optimization

```html
<!-- Responsive images -->
<img
  srcset="image-320.jpg 320w, image-640.jpg 640w, image-1280.jpg 1280w"
  sizes="(max-width: 320px) 280px, (max-width: 640px) 600px, 1200px"
  src="image-1280.jpg"
  alt="..."
  loading="lazy"
/>

<!-- Modern formats -->
<picture>
  <source srcset="image.avif" type="image/avif" />
  <source srcset="image.webp" type="image/webp" />
  <img src="image.jpg" alt="..." />
</picture>
```

---

## Performance Anti-Patterns

### Avoid These

```javascript
// Synchronous operations in hot path
const data = fs.readFileSync(path); // Use async

// Unbounded memory growth
const cache = {}; // Use LRU cache with limit

// Blocking the event loop
while (processing) { /* ... */ } // Use async/workers

// Over-fetching
SELECT * FROM large_table; // Select specific columns

// No pagination
const ALL_USERS = await User.findAll(); // Add limit
```

---

## Performance Checklist

### Before Deploying
- [ ] Core Web Vitals in "Good" range
- [ ] No API response >2s
- [ ] No N+1 queries
- [ ] Bundle size <250KB (gzipped)
- [ ] Images optimized and lazy loaded
- [ ] Caching strategy implemented
- [ ] Database queries have indexes
- [ ] Connection pooling configured
