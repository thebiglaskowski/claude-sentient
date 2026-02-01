---
name: cc-adr
description: Document architectural decisions
model: sonnet
argument-hint: "[decision topic]"
---

# /adr - Architecture Decision Record

<context>
Architecture Decision Records (ADRs) capture significant technical decisions
and their context. They create a decision log that helps future team members
understand why the system is built the way it is.
</context>

<role>
You are a technical architect who:
- Captures decision context clearly
- Documents alternatives considered
- Explains rationale for decisions
- Notes consequences and tradeoffs
- Creates searchable decision history
</role>

## Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `$1` | Decision topic | `/adr use PostgreSQL` |

## Usage Examples

```
/adr                            # Interactive ADR creation
/adr use PostgreSQL             # Document DB choice
/adr adopt microservices        # Document architecture
/adr switch to TypeScript       # Document language choice
```

<task>
Create an Architecture Decision Record by:
1. Assigning ADR number
2. Documenting context
3. Listing options considered
4. Recording the decision
5. Noting consequences
</task>

<instructions>
<step number="1">
**Determine ADR number**: Check existing ADRs:
- Look in `docs/decisions/` or `docs/adr/`
- Assign next sequential number
- Use format: `ADR-001`, `ADR-002`, etc.
</step>

<step number="2">
**Document context**: Explain the situation:
- What problem or need prompted this decision?
- What constraints exist?
- What forces are at play?
</step>

<step number="3">
**List options considered**: Document alternatives:
- What options were evaluated?
- What are the pros/cons of each?
- Why were alternatives rejected?
</step>

<step number="4">
**Record the decision**: State clearly:
- What was decided?
- Why was this option chosen?
- What is the scope of the decision?
</step>

<step number="5">
**Note consequences**: Document outcomes:
- What are the positive outcomes?
- What are the negative outcomes or tradeoffs?
- What future considerations exist?
</step>
</instructions>

<output_format>
# ADR-[NNN]: [Title]

**Date:** [YYYY-MM-DD]
**Status:** [Proposed | Accepted | Deprecated | Superseded by ADR-XXX]
**Deciders:** [Names or roles]
**Technical Story:** [Optional: Link to issue/ticket]

---

## Context

[Describe the issue motivating this decision. Include any relevant background,
constraints, and forces at play. What problem are we trying to solve?]

---

## Decision Drivers

- [Driver 1: e.g., Need for high availability]
- [Driver 2: e.g., Team expertise]
- [Driver 3: e.g., Budget constraints]
- [Driver 4: e.g., Time to market]

---

## Considered Options

### Option 1: [Name]
[Brief description]

**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]
- [Con 2]

### Option 2: [Name]
[Brief description]

**Pros:**
- [Pro 1]

**Cons:**
- [Con 1]

### Option 3: [Name]
[Brief description]

---

## Decision

**We will use [Option X].**

[Explanation of why this option was chosen. Reference the decision drivers
and explain how this option best addresses them.]

---

## Consequences

### Positive
- [Positive consequence 1]
- [Positive consequence 2]

### Negative
- [Negative consequence 1]
- [Negative consequence 2]

### Neutral
- [Neutral consequence: something that changes but isn't clearly good or bad]

---

## Compliance

[How will we ensure this decision is followed?]

- [Enforcement mechanism 1]
- [Enforcement mechanism 2]

---

## Notes

[Any additional notes, links to resources, or follow-up items]

---

## Related Decisions

- [ADR-XXX: Related decision]
- [ADR-YYY: Related decision]
</output_format>

<examples>
<example>
<input>
/adr use PostgreSQL for primary database
</input>
<thinking>
1. Database choice is a significant architectural decision
2. Need to compare against alternatives (MySQL, MongoDB, etc.)
3. Consider team expertise, performance, features
4. Document tradeoffs clearly
</thinking>
<output>
# ADR-003: Use PostgreSQL for Primary Database

**Date:** 2026-01-29
**Status:** Accepted
**Deciders:** Engineering Team
**Technical Story:** PROJ-123 - Database Selection

---

## Context

We are building a new e-commerce platform and need to select a primary
database. The system will handle product catalog, user accounts, orders,
and inventory management. We expect to scale to 1M+ users within 2 years.

Key requirements:
- ACID compliance for financial transactions
- Complex querying for reporting
- JSON support for flexible product attributes
- Strong ecosystem and tooling

---

## Decision Drivers

- Need ACID transactions for order processing
- Team has strong SQL experience
- Complex reporting requirements
- Need JSON support for product attributes
- Long-term maintainability and support
- Cost considerations (open source preferred)

---

## Considered Options

### Option 1: PostgreSQL
Open-source relational database with advanced features.

**Pros:**
- Full ACID compliance
- Excellent JSON/JSONB support
- Advanced indexing (GIN, GiST, BRIN)
- Strong community and documentation
- Team familiarity
- Free and open source

**Cons:**
- Horizontal scaling requires additional tooling
- Write-heavy workloads need tuning

### Option 2: MySQL
Popular open-source relational database.

**Pros:**
- Widely used, large community
- Good performance for read-heavy workloads
- Team has some experience

**Cons:**
- JSON support less mature than PostgreSQL
- Fewer advanced indexing options
- Less feature-rich for complex queries

### Option 3: MongoDB
Document database with flexible schema.

**Pros:**
- Flexible schema for product attributes
- Built-in horizontal scaling
- Good for rapid prototyping

**Cons:**
- No ACID transactions across documents (until recent versions)
- Team has limited NoSQL experience
- Complex reporting requires aggregation pipelines
- Not ideal for relational data patterns

---

## Decision

**We will use PostgreSQL 15+ as our primary database.**

PostgreSQL best addresses our decision drivers:
1. Full ACID compliance for order/payment processing
2. Superior JSON/JSONB support for flexible product attributes
3. Team's strong SQL experience reduces learning curve
4. Advanced features (CTEs, window functions, full-text search) support
   complex reporting requirements
5. Open source with excellent long-term support

---

## Consequences

### Positive
- Reliable transaction handling for financial operations
- Flexible product attribute storage with JSONB
- Rich querying capabilities for analytics
- Strong tooling ecosystem (pgAdmin, pg_dump, etc.)
- No licensing costs

### Negative
- Will need to implement connection pooling (PgBouncer)
- May need read replicas for heavy reporting workloads
- Team needs training on PostgreSQL-specific features

### Neutral
- Will use Prisma ORM for application access
- Migrations managed through Prisma Migrate

---

## Compliance

- All new services must use PostgreSQL unless explicitly approved
- Database changes require migration scripts
- Production access limited to DBA team

---

## Notes

- Consider TimescaleDB extension if time-series data grows significantly
- Evaluate Citus for horizontal scaling if needed in future
- Set up pg_stat_statements for query performance monitoring

---

## Related Decisions

- ADR-001: Use Prisma as ORM
- ADR-005: Implement read replicas for reporting (future)
</output>
</example>

<example>
<input>
/adr adopt TypeScript
</input>
<output>
# ADR-007: Adopt TypeScript for All New Code

**Date:** 2026-01-29
**Status:** Accepted
**Deciders:** Frontend Team, Backend Team
**Technical Story:** INFRA-456 - Type Safety Initiative

---

## Context

Our JavaScript codebase has grown to 150K+ lines across frontend and backend.
We're experiencing increasing bugs related to type mismatches, especially
at API boundaries. Onboarding new developers takes longer than expected due
to lack of type documentation.

---

## Decision Drivers

- Reduce runtime type errors
- Improve developer productivity with IDE support
- Better documentation through types
- Easier refactoring of large codebase
- Industry trend toward typed JavaScript

---

## Considered Options

### Option 1: TypeScript
Typed superset of JavaScript.

**Pros:**
- Gradual adoption possible
- Excellent IDE support
- Large ecosystem
- Can coexist with JavaScript

**Cons:**
- Build step required
- Learning curve for team
- Some library types incomplete

### Option 2: Flow
Facebook's type system for JavaScript.

**Pros:**
- Gradual adoption
- Good for React codebases

**Cons:**
- Declining community support
- Fewer library definitions
- Tooling less mature

### Option 3: JSDoc with TypeScript checking
Type annotations in comments.

**Pros:**
- No build step
- Gradual adoption

**Cons:**
- Less expressive than TypeScript
- Verbose for complex types
- IDE support varies

---

## Decision

**We will adopt TypeScript for all new code and gradually migrate existing code.**

---

## Consequences

### Positive
- Catch type errors at compile time
- Better IDE autocompletion and refactoring
- Self-documenting code through types
- Easier onboarding with type hints

### Negative
- Initial productivity dip during learning
- Build configuration complexity
- Need to maintain type definitions

---

## Compliance

- All new files must be `.ts` or `.tsx`
- Existing files migrated when modified substantially
- `strict` mode enabled for new code
- No `any` types without justification comment

---

## Related Decisions

- ADR-008: TypeScript configuration standards
</output>
</example>
</examples>

<rules>
- Every significant technical decision should have an ADR
- ADRs are immutable once accepted (create new ADR to supersede)
- Keep ADRs concise but complete
- Include rejected alternatives and why
- Update status when decisions change
- Store in version control with code
</rules>

<error_handling>
If decision unclear: Ask clarifying questions about context and constraints
If no alternatives considered: Research and present at least 2 alternatives
If consequences unknown: Note as "requires evaluation" with timeline
If superseding existing ADR: Reference the old ADR and explain what changed
</error_handling>

## ADR Status Lifecycle

```
Proposed → Accepted → [Deprecated | Superseded]
    ↓
 Rejected
```

- **Proposed**: Under discussion
- **Accepted**: Approved and in effect
- **Deprecated**: No longer recommended
- **Superseded**: Replaced by newer ADR
- **Rejected**: Considered but not adopted
