# Strategy Pattern

## Intent

Define a family of interchangeable algorithms, encapsulating each one and making them interchangeable at runtime.

---

## When to Use

- Multiple algorithms for the same task
- Need to switch algorithms at runtime
- Algorithm selection based on context/configuration
- Avoid complex conditionals selecting behavior
- Different validation/processing rules per context

## When NOT to Use

- Only one algorithm exists
- Algorithms rarely change
- Simple if/else is clearer
- Overhead outweighs benefit

---

## Structure

```
┌─────────────┐     ┌─────────────────┐
│   Context   │────▶│    Strategy     │ (interface)
└─────────────┘     └─────────────────┘
                           ▲
           ┌───────────────┼───────────────┐
           │               │               │
    ┌──────┴──────┐ ┌──────┴──────┐ ┌──────┴──────┐
    │ ConcreteA   │ │ ConcreteB   │ │ ConcreteC   │
    └─────────────┘ └─────────────┘ └─────────────┘
```

---

## Implementation

### TypeScript

```typescript
// Strategy interface
interface PaymentStrategy {
  pay(amount: number): Promise<PaymentResult>;
  validate(details: PaymentDetails): ValidationResult;
  readonly name: string;
}

// Concrete strategies
class CreditCardStrategy implements PaymentStrategy {
  readonly name = 'credit_card';

  async pay(amount: number): Promise<PaymentResult> {
    // Process credit card payment
    const response = await stripe.charges.create({
      amount: Math.round(amount * 100),
      currency: 'usd',
      source: this.token,
    });
    return { success: true, transactionId: response.id };
  }

  validate(details: PaymentDetails): ValidationResult {
    if (!details.cardNumber || !this.isValidCard(details.cardNumber)) {
      return { valid: false, error: 'Invalid card number' };
    }
    return { valid: true };
  }

  private isValidCard(number: string): boolean {
    // Luhn algorithm
    return luhnCheck(number);
  }
}

class PayPalStrategy implements PaymentStrategy {
  readonly name = 'paypal';

  async pay(amount: number): Promise<PaymentResult> {
    const order = await paypal.orders.create({
      purchase_units: [{ amount: { value: amount.toString() } }],
    });
    return { success: true, transactionId: order.id };
  }

  validate(details: PaymentDetails): ValidationResult {
    if (!details.email || !isValidEmail(details.email)) {
      return { valid: false, error: 'Invalid PayPal email' };
    }
    return { valid: true };
  }
}

class CryptoStrategy implements PaymentStrategy {
  readonly name = 'crypto';

  async pay(amount: number): Promise<PaymentResult> {
    const charge = await coinbase.charges.create({
      pricing_type: 'fixed_price',
      local_price: { amount: amount.toString(), currency: 'USD' },
    });
    return { success: true, transactionId: charge.id };
  }

  validate(details: PaymentDetails): ValidationResult {
    if (!details.walletAddress) {
      return { valid: false, error: 'Wallet address required' };
    }
    return { valid: true };
  }
}

// Context
class PaymentProcessor {
  private strategy: PaymentStrategy;

  constructor(strategy: PaymentStrategy) {
    this.strategy = strategy;
  }

  setStrategy(strategy: PaymentStrategy): void {
    this.strategy = strategy;
  }

  async processPayment(
    amount: number,
    details: PaymentDetails
  ): Promise<PaymentResult> {
    const validation = this.strategy.validate(details);
    if (!validation.valid) {
      throw new ValidationError(validation.error);
    }

    logger.info(`Processing ${this.strategy.name} payment`, { amount });
    return this.strategy.pay(amount);
  }
}

// Strategy factory
class PaymentStrategyFactory {
  private strategies = new Map<string, PaymentStrategy>();

  register(strategy: PaymentStrategy): void {
    this.strategies.set(strategy.name, strategy);
  }

  get(name: string): PaymentStrategy {
    const strategy = this.strategies.get(name);
    if (!strategy) {
      throw new Error(`Unknown payment strategy: ${name}`);
    }
    return strategy;
  }
}

// Usage
const factory = new PaymentStrategyFactory();
factory.register(new CreditCardStrategy());
factory.register(new PayPalStrategy());
factory.register(new CryptoStrategy());

const processor = new PaymentProcessor(factory.get('credit_card'));
await processor.processPayment(99.99, { cardNumber: '4111...' });

// Switch strategy at runtime
processor.setStrategy(factory.get('paypal'));
await processor.processPayment(49.99, { email: 'user@example.com' });
```

### Python

```python
from abc import ABC, abstractmethod
from typing import Dict, Type
from dataclasses import dataclass

@dataclass
class PaymentResult:
    success: bool
    transaction_id: str

@dataclass
class ValidationResult:
    valid: bool
    error: str = ""

class PaymentStrategy(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    async def pay(self, amount: float) -> PaymentResult:
        pass

    @abstractmethod
    def validate(self, details: dict) -> ValidationResult:
        pass


class CreditCardStrategy(PaymentStrategy):
    @property
    def name(self) -> str:
        return "credit_card"

    async def pay(self, amount: float) -> PaymentResult:
        response = await stripe.Charge.create(
            amount=int(amount * 100),
            currency="usd",
        )
        return PaymentResult(success=True, transaction_id=response.id)

    def validate(self, details: dict) -> ValidationResult:
        if not details.get("card_number"):
            return ValidationResult(valid=False, error="Card number required")
        return ValidationResult(valid=True)


class PayPalStrategy(PaymentStrategy):
    @property
    def name(self) -> str:
        return "paypal"

    async def pay(self, amount: float) -> PaymentResult:
        order = await paypal.Order.create(amount=amount)
        return PaymentResult(success=True, transaction_id=order.id)

    def validate(self, details: dict) -> ValidationResult:
        if not details.get("email"):
            return ValidationResult(valid=False, error="Email required")
        return ValidationResult(valid=True)


class PaymentProcessor:
    def __init__(self, strategy: PaymentStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: PaymentStrategy) -> None:
        self._strategy = strategy

    async def process(self, amount: float, details: dict) -> PaymentResult:
        validation = self._strategy.validate(details)
        if not validation.valid:
            raise ValidationError(validation.error)
        return await self._strategy.pay(amount)


# Strategy registry
class StrategyRegistry:
    _strategies: Dict[str, Type[PaymentStrategy]] = {}

    @classmethod
    def register(cls, strategy_class: Type[PaymentStrategy]) -> Type[PaymentStrategy]:
        instance = strategy_class()
        cls._strategies[instance.name] = strategy_class
        return strategy_class

    @classmethod
    def get(cls, name: str) -> PaymentStrategy:
        if name not in cls._strategies:
            raise ValueError(f"Unknown strategy: {name}")
        return cls._strategies[name]()


# Usage with decorator registration
@StrategyRegistry.register
class BankTransferStrategy(PaymentStrategy):
    @property
    def name(self) -> str:
        return "bank_transfer"
    # ...
```

### Go

```go
// Strategy interface
type PaymentStrategy interface {
    Name() string
    Pay(ctx context.Context, amount float64) (*PaymentResult, error)
    Validate(details PaymentDetails) error
}

// Concrete strategies
type CreditCardStrategy struct {
    client *stripe.Client
}

func (s *CreditCardStrategy) Name() string {
    return "credit_card"
}

func (s *CreditCardStrategy) Pay(ctx context.Context, amount float64) (*PaymentResult, error) {
    charge, err := s.client.Charges.Create(&stripe.ChargeParams{
        Amount:   stripe.Int64(int64(amount * 100)),
        Currency: stripe.String("usd"),
    })
    if err != nil {
        return nil, fmt.Errorf("stripe charge failed: %w", err)
    }
    return &PaymentResult{
        Success:       true,
        TransactionID: charge.ID,
    }, nil
}

func (s *CreditCardStrategy) Validate(details PaymentDetails) error {
    if details.CardNumber == "" {
        return errors.New("card number required")
    }
    if !luhnCheck(details.CardNumber) {
        return errors.New("invalid card number")
    }
    return nil
}

// Context
type PaymentProcessor struct {
    strategy PaymentStrategy
}

func NewPaymentProcessor(strategy PaymentStrategy) *PaymentProcessor {
    return &PaymentProcessor{strategy: strategy}
}

func (p *PaymentProcessor) SetStrategy(strategy PaymentStrategy) {
    p.strategy = strategy
}

func (p *PaymentProcessor) Process(
    ctx context.Context,
    amount float64,
    details PaymentDetails,
) (*PaymentResult, error) {
    if err := p.strategy.Validate(details); err != nil {
        return nil, fmt.Errorf("validation failed: %w", err)
    }
    return p.strategy.Pay(ctx, amount)
}

// Strategy registry
type StrategyRegistry struct {
    strategies map[string]PaymentStrategy
}

func NewStrategyRegistry() *StrategyRegistry {
    return &StrategyRegistry{
        strategies: make(map[string]PaymentStrategy),
    }
}

func (r *StrategyRegistry) Register(strategy PaymentStrategy) {
    r.strategies[strategy.Name()] = strategy
}

func (r *StrategyRegistry) Get(name string) (PaymentStrategy, error) {
    strategy, ok := r.strategies[name]
    if !ok {
        return nil, fmt.Errorf("unknown strategy: %s", name)
    }
    return strategy, nil
}
```

---

## Variations

### Function-Based Strategy

```typescript
type SortStrategy<T> = (items: T[]) => T[];

const strategies: Record<string, SortStrategy<User>> = {
  byName: (users) => [...users].sort((a, b) => a.name.localeCompare(b.name)),
  byDate: (users) => [...users].sort((a, b) => b.createdAt - a.createdAt),
  byScore: (users) => [...users].sort((a, b) => b.score - a.score),
};

function sortUsers(users: User[], strategyName: string): User[] {
  const strategy = strategies[strategyName] ?? strategies.byDate;
  return strategy(users);
}
```

### Configuration-Driven Strategy

```typescript
interface StrategyConfig {
  type: string;
  options: Record<string, unknown>;
}

class StrategyFactory {
  create(config: StrategyConfig): Strategy {
    switch (config.type) {
      case 'credit_card':
        return new CreditCardStrategy(config.options);
      case 'paypal':
        return new PayPalStrategy(config.options);
      default:
        throw new Error(`Unknown strategy: ${config.type}`);
    }
  }
}

// Load from config
const config = loadConfig();
const strategy = factory.create(config.payment);
```

---

## Related Patterns

- **Factory** — Creates strategy instances
- **State** — Similar structure, different intent (state transitions)
- **Template Method** — Fixed algorithm with variable steps
- **Decorator** — Can wrap strategies for additional behavior

---

## Anti-Patterns

- **Too many strategies** — May indicate need for different abstraction
- **Strategy knows context** — Keep strategies independent
- **Hardcoded strategy selection** — Use factory or configuration
- **Stateful strategies** — Prefer stateless for thread safety
