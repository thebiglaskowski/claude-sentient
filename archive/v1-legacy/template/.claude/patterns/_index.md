# Pattern Library Index

Reusable architectural and design patterns surfaced contextually during implementation.

---

## Quick Reference

| Pattern | Category | Use When |
|---------|----------|----------|
| `@patterns/repository` | Architecture | Data access layer needed |
| `@patterns/service-layer` | Architecture | Business logic organization |
| `@patterns/factory` | Creational | Object creation complexity |
| `@patterns/singleton` | Creational | Single instance required |
| `@patterns/adapter` | Structural | Interface compatibility |
| `@patterns/decorator` | Structural | Add behavior dynamically |
| `@patterns/observer` | Behavioral | Event-driven updates |
| `@patterns/strategy` | Behavioral | Interchangeable algorithms |
| `@patterns/error-boundary` | Error Handling | Graceful error recovery |
| `@patterns/retry-with-backoff` | Resilience | Transient failure handling |
| `@patterns/circuit-breaker` | Resilience | Prevent cascade failures |
| `@patterns/pagination` | API | Large dataset retrieval |
| `@patterns/cqrs` | Architecture | Read/write separation |
| `@patterns/event-sourcing` | Architecture | Audit trail, replay |
| `@patterns/feature-flag` | Operations | Gradual rollout |

---

## Loading Patterns

Load a pattern with `@patterns/[name]`:

```
@patterns/repository
@patterns/retry-with-backoff
```

Or ask Claude to surface relevant patterns:

```
"What patterns apply to this task?"
"Show me the repository pattern"
```

---

## Categories

### Architecture Patterns
High-level structural patterns for system organization.

| Pattern | Purpose | Complexity |
|---------|---------|------------|
| [repository](architecture/repository.md) | Abstract data access | Medium |
| [service-layer](architecture/service-layer.md) | Organize business logic | Medium |
| [cqrs](architecture/cqrs.md) | Separate reads/writes | High |
| [event-sourcing](architecture/event-sourcing.md) | Event-based state | High |
| [clean-architecture](architecture/clean-architecture.md) | Dependency inversion | High |

### Creational Patterns
Object creation mechanisms.

| Pattern | Purpose | Complexity |
|---------|---------|------------|
| [factory](creational/factory.md) | Encapsulate creation | Low |
| [singleton](creational/singleton.md) | Single instance | Low |
| [builder](creational/builder.md) | Complex construction | Medium |

### Structural Patterns
Object composition and relationships.

| Pattern | Purpose | Complexity |
|---------|---------|------------|
| [adapter](structural/adapter.md) | Interface translation | Low |
| [decorator](structural/decorator.md) | Add behavior | Medium |
| [facade](structural/facade.md) | Simplify interface | Low |
| [composite](structural/composite.md) | Tree structures | Medium |

### Behavioral Patterns
Object interaction and responsibility.

| Pattern | Purpose | Complexity |
|---------|---------|------------|
| [observer](behavioral/observer.md) | Event subscription | Medium |
| [strategy](behavioral/strategy.md) | Swap algorithms | Low |
| [command](behavioral/command.md) | Encapsulate actions | Medium |
| [state-machine](behavioral/state-machine.md) | State transitions | Medium |

### Resilience Patterns
Fault tolerance and recovery.

| Pattern | Purpose | Complexity |
|---------|---------|------------|
| [retry-with-backoff](resilience/retry-with-backoff.md) | Handle transient failures | Low |
| [circuit-breaker](resilience/circuit-breaker.md) | Prevent cascades | Medium |
| [bulkhead](resilience/bulkhead.md) | Isolate failures | Medium |
| [timeout](resilience/timeout.md) | Bound wait time | Low |

### Error Handling Patterns
Graceful error management.

| Pattern | Purpose | Complexity |
|---------|---------|------------|
| [error-boundary](error-handling/error-boundary.md) | Contain failures | Low |
| [result-type](error-handling/result-type.md) | Explicit errors | Medium |
| [global-handler](error-handling/global-handler.md) | Centralized handling | Low |

### API Patterns
REST and API design.

| Pattern | Purpose | Complexity |
|---------|---------|------------|
| [pagination](api/pagination.md) | Large datasets | Low |
| [rate-limiting](api/rate-limiting.md) | Throttle requests | Medium |
| [versioning](api/versioning.md) | API evolution | Low |
| [hateoas](api/hateoas.md) | Discoverable APIs | High |

### Testing Patterns
Test organization and mocking.

| Pattern | Purpose | Complexity |
|---------|---------|------------|
| [arrange-act-assert](testing/arrange-act-assert.md) | Test structure | Low |
| [test-doubles](testing/test-doubles.md) | Mocks, stubs, fakes | Medium |
| [fixture-factory](testing/fixture-factory.md) | Test data creation | Medium |

### Operations Patterns
Deployment and feature management.

| Pattern | Purpose | Complexity |
|---------|---------|------------|
| [feature-flag](operations/feature-flag.md) | Toggle features | Low |
| [blue-green](operations/blue-green.md) | Zero-downtime deploy | Medium |
| [canary](operations/canary.md) | Gradual rollout | Medium |

---

## Pattern Structure

Each pattern file includes:

1. **Intent** — What problem it solves
2. **When to Use** — Specific scenarios
3. **When NOT to Use** — Anti-patterns
4. **Structure** — Components and relationships
5. **Implementation** — Code examples (multiple languages)
6. **Variations** — Common modifications
7. **Related Patterns** — Cross-references

---

## Adding New Patterns

1. Create file in appropriate category folder
2. Follow the standard structure
3. Include examples in relevant languages
4. Add to this index
5. Cross-reference related patterns

---

## Auto-Surfacing

Patterns are automatically surfaced when:

- Task matches pattern use case
- Code review identifies pattern opportunity
- Architecture discussion occurs
- Refactoring targets structural issues

The meta-cognition skill consults this library during the ASSESS phase.
