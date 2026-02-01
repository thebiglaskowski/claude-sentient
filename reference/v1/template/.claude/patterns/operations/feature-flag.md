# Feature Flag Pattern

## Intent

Enable/disable features at runtime without code deployment, allowing gradual rollout, A/B testing, and quick rollback.

---

## When to Use

- Gradual feature rollout (canary releases)
- A/B testing and experimentation
- Kill switches for risky features
- Environment-specific features (beta, staging)
- User segment targeting
- Trunk-based development with incomplete features

## When NOT to Use

- Permanent configuration (use config instead)
- Security-critical decisions
- Features that should always be on/off
- Short-lived changes (just deploy)

---

## Structure

```
┌─────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    Code     │────▶│  Feature Flag   │────▶│  Flag Storage   │
│             │     │    Service      │     │ (DB/Config/API) │
└─────────────┘     └─────────────────┘     └─────────────────┘
                           │
                           ▼
                    ┌─────────────────┐
                    │  Evaluation     │
                    │  (User/Context) │
                    └─────────────────┘
```

---

## Implementation

### TypeScript

```typescript
// Flag definition
interface FeatureFlag {
  key: string;
  enabled: boolean;
  description?: string;
  rolloutPercentage?: number;
  targetedUsers?: string[];
  targetedGroups?: string[];
  variants?: Record<string, unknown>;
  createdAt: Date;
  updatedAt: Date;
}

// Evaluation context
interface EvaluationContext {
  userId?: string;
  userGroups?: string[];
  userAttributes?: Record<string, unknown>;
  environment?: string;
  requestId?: string;
}

// Feature flag service
class FeatureFlagService {
  private flags: Map<string, FeatureFlag> = new Map();
  private cache: Map<string, { value: boolean; expiresAt: number }> = new Map();

  constructor(
    private storage: FlagStorage,
    private cacheMs: number = 60000
  ) {}

  async initialize(): Promise<void> {
    const flags = await this.storage.getAllFlags();
    flags.forEach(flag => this.flags.set(flag.key, flag));

    // Subscribe to updates
    this.storage.onChange(flag => {
      this.flags.set(flag.key, flag);
      this.cache.delete(flag.key);
    });
  }

  isEnabled(
    flagKey: string,
    context: EvaluationContext = {}
  ): boolean {
    // Check cache
    const cacheKey = this.getCacheKey(flagKey, context);
    const cached = this.cache.get(cacheKey);
    if (cached && cached.expiresAt > Date.now()) {
      return cached.value;
    }

    const flag = this.flags.get(flagKey);
    if (!flag) {
      return false; // Default to off for unknown flags
    }

    const result = this.evaluate(flag, context);

    // Cache result
    this.cache.set(cacheKey, {
      value: result,
      expiresAt: Date.now() + this.cacheMs,
    });

    return result;
  }

  private evaluate(flag: FeatureFlag, context: EvaluationContext): boolean {
    // Flag globally disabled
    if (!flag.enabled) {
      return false;
    }

    // User targeting
    if (flag.targetedUsers?.includes(context.userId ?? '')) {
      return true;
    }

    // Group targeting
    if (
      flag.targetedGroups?.some(group =>
        context.userGroups?.includes(group)
      )
    ) {
      return true;
    }

    // Percentage rollout
    if (flag.rolloutPercentage !== undefined && context.userId) {
      const hash = this.hashUserId(context.userId, flag.key);
      return hash < flag.rolloutPercentage;
    }

    return flag.enabled;
  }

  private hashUserId(userId: string, flagKey: string): number {
    // Consistent hashing for stable rollout
    const combined = `${flagKey}:${userId}`;
    let hash = 0;
    for (let i = 0; i < combined.length; i++) {
      hash = ((hash << 5) - hash) + combined.charCodeAt(i);
      hash = hash & hash; // Convert to 32-bit integer
    }
    return Math.abs(hash % 100);
  }

  private getCacheKey(flagKey: string, context: EvaluationContext): string {
    return `${flagKey}:${context.userId ?? 'anonymous'}`;
  }

  // Get variant for multivariate flags
  getVariant<T>(
    flagKey: string,
    defaultValue: T,
    context: EvaluationContext = {}
  ): T {
    const flag = this.flags.get(flagKey);
    if (!flag?.enabled || !flag.variants) {
      return defaultValue;
    }

    // Determine variant based on user hash
    const variants = Object.keys(flag.variants);
    if (context.userId) {
      const hash = this.hashUserId(context.userId, flagKey);
      const index = Math.floor((hash / 100) * variants.length);
      return flag.variants[variants[index]] as T;
    }

    return defaultValue;
  }
}

// Usage
const flags = new FeatureFlagService(new PostgresFlagStorage(db));
await flags.initialize();

// Simple boolean check
if (flags.isEnabled('new-checkout-flow', { userId: user.id })) {
  return <NewCheckout />;
}
return <OldCheckout />;

// Multivariate
const buttonColor = flags.getVariant('checkout-button-color', 'blue', {
  userId: user.id,
});

// React hook
function useFeatureFlag(flagKey: string): boolean {
  const { user } = useAuth();
  const flags = useFeatureFlagService();

  return useMemo(
    () => flags.isEnabled(flagKey, { userId: user?.id }),
    [flagKey, user?.id]
  );
}

function CheckoutPage() {
  const showNewFlow = useFeatureFlag('new-checkout-flow');

  if (showNewFlow) {
    return <NewCheckoutFlow />;
  }
  return <LegacyCheckoutFlow />;
}
```

### Python

```python
from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from abc import ABC, abstractmethod
import hashlib

@dataclass
class FeatureFlag:
    key: str
    enabled: bool
    description: str = ""
    rollout_percentage: Optional[float] = None
    targeted_users: List[str] = None
    targeted_groups: List[str] = None
    variants: Dict[str, Any] = None

@dataclass
class EvaluationContext:
    user_id: Optional[str] = None
    user_groups: List[str] = None
    attributes: Dict[str, Any] = None

class FeatureFlagService:
    def __init__(self, storage: "FlagStorage"):
        self._storage = storage
        self._flags: Dict[str, FeatureFlag] = {}
        self._cache: Dict[str, tuple[bool, float]] = {}

    async def initialize(self) -> None:
        flags = await self._storage.get_all_flags()
        self._flags = {f.key: f for f in flags}

    def is_enabled(
        self,
        flag_key: str,
        context: Optional[EvaluationContext] = None
    ) -> bool:
        context = context or EvaluationContext()
        flag = self._flags.get(flag_key)

        if not flag or not flag.enabled:
            return False

        # User targeting
        if flag.targeted_users and context.user_id in flag.targeted_users:
            return True

        # Group targeting
        if flag.targeted_groups and context.user_groups:
            if any(g in flag.targeted_groups for g in context.user_groups):
                return True

        # Percentage rollout
        if flag.rollout_percentage is not None and context.user_id:
            hash_value = self._hash_user(context.user_id, flag_key)
            return hash_value < flag.rollout_percentage

        return flag.enabled

    def _hash_user(self, user_id: str, flag_key: str) -> float:
        combined = f"{flag_key}:{user_id}"
        hash_bytes = hashlib.md5(combined.encode()).digest()
        hash_int = int.from_bytes(hash_bytes[:4], byteorder='big')
        return (hash_int % 100)


# Usage
flags = FeatureFlagService(PostgresFlagStorage(db))
await flags.initialize()

if flags.is_enabled("new_checkout", EvaluationContext(user_id=user.id)):
    return new_checkout_flow()
return legacy_checkout_flow()

# Decorator
def feature_flag(flag_key: str, default=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            context = kwargs.get('context') or EvaluationContext()
            if flags.is_enabled(flag_key, context):
                return func(*args, **kwargs)
            return default
        return wrapper
    return decorator

@feature_flag("experimental_api", default={"error": "Feature not available"})
def experimental_endpoint(request, context):
    return {"data": "experimental"}
```

### Go

```go
type FeatureFlag struct {
    Key               string            `json:"key"`
    Enabled           bool              `json:"enabled"`
    RolloutPercentage *float64          `json:"rolloutPercentage,omitempty"`
    TargetedUsers     []string          `json:"targetedUsers,omitempty"`
    TargetedGroups    []string          `json:"targetedGroups,omitempty"`
    Variants          map[string]any    `json:"variants,omitempty"`
}

type EvaluationContext struct {
    UserID     string
    UserGroups []string
    Attributes map[string]any
}

type FeatureFlagService struct {
    flags map[string]*FeatureFlag
    mu    sync.RWMutex
}

func (s *FeatureFlagService) IsEnabled(flagKey string, ctx EvaluationContext) bool {
    s.mu.RLock()
    flag, ok := s.flags[flagKey]
    s.mu.RUnlock()

    if !ok || !flag.Enabled {
        return false
    }

    // User targeting
    for _, uid := range flag.TargetedUsers {
        if uid == ctx.UserID {
            return true
        }
    }

    // Percentage rollout
    if flag.RolloutPercentage != nil && ctx.UserID != "" {
        hash := hashUser(ctx.UserID, flagKey)
        return hash < *flag.RolloutPercentage
    }

    return flag.Enabled
}

func hashUser(userID, flagKey string) float64 {
    h := fnv.New32a()
    h.Write([]byte(flagKey + ":" + userID))
    return float64(h.Sum32() % 100)
}

// Middleware
func FeatureFlagMiddleware(flags *FeatureFlagService) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            ctx := r.Context()
            userID := getUserID(r)

            evalCtx := EvaluationContext{UserID: userID}
            ctx = context.WithValue(ctx, "featureFlags", flags)
            ctx = context.WithValue(ctx, "evalContext", evalCtx)

            next.ServeHTTP(w, r.WithContext(ctx))
        })
    }
}
```

---

## Flag Lifecycle

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Create  │───▶│  Rollout │───▶│   Full   │───▶│  Remove  │
│   Flag   │    │ (1-100%) │    │  Launch  │    │   Flag   │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
                     │
                     ▼
              ┌──────────────┐
              │   Rollback   │
              │   (0%)       │
              └──────────────┘
```

---

## Related Patterns

- **Strategy** — Flags can select strategies
- **Circuit Breaker** — Emergency flags as kill switches
- **A/B Testing** — Multivariate flags for experiments
- **Canary** — Percentage rollout for canary deploys

---

## Anti-Patterns

- **Permanent flags** — Clean up after full rollout
- **Nested flags** — Hard to reason about
- **Security flags** — Don't use for auth/permissions
- **Too many flags** — Technical debt accumulates
- **No expiration** — Set review dates
