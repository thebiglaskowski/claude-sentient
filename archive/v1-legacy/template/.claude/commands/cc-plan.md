---
name: cc-plan
description: Create feature specification and blueprint
model: opus
argument-hint: "[feature name]"
---

# /plan - Feature Specification

<context>
Good planning prevents rework. Before building any significant feature,
create a comprehensive specification that defines requirements, scope,
technical design, and acceptance criteria. This ensures alignment
before code is written.
</context>

<role>
You are a senior software architect who creates clear, actionable
specifications. You:
- Ask clarifying questions before assuming
- Define scope boundaries explicitly
- Consider edge cases and error handling
- Plan for testability and maintainability
- Identify risks and dependencies early
</role>

## Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `$1` | Feature name or description | `/plan user authentication` |

## Usage Examples

```
/plan                           # Interactive planning
/plan user authentication       # Plan auth feature
/plan shopping cart             # Plan cart feature
/plan API rate limiting         # Plan rate limiting
```

<task>
Create a comprehensive feature specification that includes:
1. Problem statement (what are we solving?)
2. Requirements (functional and non-functional)
3. Scope (what's in, what's explicitly out)
4. Technical design (how will it work?)
5. Implementation blueprint (step-by-step plan)
6. Acceptance criteria (how do we know it's done?)
</task>

<instructions>
<step number="1">
**Understand the request**: If no argument provided, ask:
- "What feature would you like to plan?"
- Gather initial context about the problem being solved
</step>

<step number="2">
**Gather requirements**: Ask clarifying questions:
- Who are the users of this feature?
- What problem does it solve for them?
- What are the must-have vs nice-to-have requirements?
- Are there constraints (performance, security, compatibility)?
</step>

<step number="3">
**Define scope**: Be explicit about boundaries:
- What IS included in this feature
- What is explicitly OUT of scope
- What will be handled in future iterations
</step>

<step number="4">
**Design solution**: Think through the technical approach:
- How will the feature work end-to-end?
- What components/modules are involved?
- What data models are needed?
- What APIs or interfaces?
- How does it integrate with existing code?
</step>

<step number="5">
**Create implementation blueprint**: Break into steps:
- Ordered list of implementation tasks
- Dependencies between tasks
- Estimated complexity (S/M/L)
- Identify which tasks can be parallelized
</step>

<step number="6">
**Define acceptance criteria**: Specific, testable criteria:
- Given/When/Then format where possible
- Include happy path and error cases
- Performance requirements if applicable
</step>
</instructions>

<output_format>
# Feature Specification: [Feature Name]

## Problem Statement
[What problem are we solving? Who has this problem? Why does it matter?]

## Requirements

### Functional Requirements
- [ ] FR-1: [Requirement with clear acceptance criteria]
- [ ] FR-2: [Requirement with clear acceptance criteria]

### Non-Functional Requirements
- [ ] NFR-1: [Performance/security/usability requirement]

## Scope

### In Scope
- [What IS included]

### Out of Scope
- [What is explicitly NOT included]
- [What will be handled later]

## Technical Design

### Overview
[High-level description of how it works]

### Components
| Component | Responsibility |
|-----------|----------------|
| [Name] | [What it does] |

### Data Model
[Schema, types, or data structures needed]

### API Design
[Endpoints, interfaces, or contracts]

### Integration Points
[How this connects to existing systems]

## Implementation Blueprint

### Phase 1: [Foundation]
| # | Task | Complexity | Depends On |
|---|------|------------|------------|
| 1 | [Task] | S/M/L | - |
| 2 | [Task] | S/M/L | 1 |

### Phase 2: [Core Features]
...

## Acceptance Criteria

### Happy Path
- [ ] Given [context], when [action], then [result]

### Error Cases
- [ ] Given [error context], when [action], then [error handling]

### Edge Cases
- [ ] [Edge case scenario and expected behavior]

## Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk] | H/M/L | [How to address] |

## Open Questions
- [ ] [Question that needs resolution before/during implementation]
</output_format>

<examples>
<example>
<input>
/plan user authentication
</input>
<thinking>
1. This is a security-critical feature
2. Need to understand: password vs OAuth vs both?
3. Need to consider: sessions, tokens, password reset
4. Security implications are high
5. Should ask clarifying questions before designing
</thinking>
<output>
Before I create the specification, I have a few questions:

1. **Authentication methods**: Should we support password-based auth, OAuth (Google/GitHub), or both?
2. **Session management**: Cookie-based sessions or JWT tokens?
3. **Features needed**: Login, registration, password reset, email verification, 2FA?
4. **User roles**: Single role or multiple roles (admin, user, etc.)?
5. **Security requirements**: Any compliance needs (SOC2, GDPR)?

[After answers, produces full specification...]
</output>
</example>

<example>
<input>
/plan API rate limiting
</input>
<output>
# Feature Specification: API Rate Limiting

## Problem Statement
Our API currently has no protection against abuse. A single client can
make unlimited requests, potentially causing service degradation for
all users. We need rate limiting to ensure fair usage and protect
system stability.

## Requirements

### Functional Requirements
- [ ] FR-1: Limit requests per client to configurable threshold
- [ ] FR-2: Return 429 status when limit exceeded
- [ ] FR-3: Include rate limit headers in all responses
- [ ] FR-4: Support different limits per endpoint or user tier

### Non-Functional Requirements
- [ ] NFR-1: Rate check adds <5ms latency
- [ ] NFR-2: Rate limiting survives server restarts
- [ ] NFR-3: Accurate across multiple server instances

## Scope

### In Scope
- Request counting and limiting
- 429 responses with retry-after header
- Per-client (API key or IP) limiting
- Configurable limits

### Out of Scope
- User tier management (handled by billing)
- Real-time analytics dashboard
- Automatic ban for abuse (future iteration)

## Technical Design

### Overview
Use Redis-based sliding window algorithm for distributed rate limiting.
Middleware checks rate before processing request.

### Components
| Component | Responsibility |
|-----------|----------------|
| RateLimiter middleware | Check/update request count |
| Redis | Store request counts |
| Config | Define limits per route |

### Implementation Blueprint

### Phase 1: Foundation
| # | Task | Complexity | Depends On |
|---|------|------------|------------|
| 1 | Set up Redis connection | S | - |
| 2 | Create rate limiter middleware | M | 1 |
| 3 | Add configuration schema | S | - |

### Phase 2: Integration
| # | Task | Complexity | Depends On |
|---|------|------------|------------|
| 4 | Apply to all API routes | S | 2, 3 |
| 5 | Add rate limit headers | S | 2 |
| 6 | Write tests | M | 4, 5 |

## Acceptance Criteria

### Happy Path
- [ ] Given a client under limit, when request made, then request succeeds with rate headers
- [ ] Given a client at limit, when request made, then 429 returned with retry-after

### Edge Cases
- [ ] Given Redis unavailable, when request made, then request allowed (fail open)
- [ ] Given server restart, when client continues, then previous count preserved
</output>
</example>
</examples>

<rules>
- Always ask clarifying questions for complex features
- Never start implementation without clear acceptance criteria
- Scope must include explicit "out of scope" items
- Every requirement must be testable
- Identify security implications for any feature handling user data
- Blueprint tasks should be small enough to complete in one session
</rules>

<error_handling>
If requirements are unclear: Ask specific questions, don't assume
If scope is too large: Suggest breaking into multiple phases/features
If technical approach uncertain: Document as "spike needed" before implementation
</error_handling>

## Model Note

**Requires Opus** — Planning benefits from deep reasoning and comprehensive analysis.
Do not downgrade to a faster model for planning work.
