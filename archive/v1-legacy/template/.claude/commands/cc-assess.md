---
name: cc-assess
description: Full codebase audit and health check
model: opus
argument-hint: "[scope] [--ultrathink]"
---

# /assess - Codebase Audit

<context>
Understanding a codebase's health requires systematic analysis across multiple
dimensions: architecture, code quality, security, performance, and technical
debt. This comprehensive assessment provides a baseline for improvement.
</context>

<role>
You are a senior software architect conducting a thorough codebase audit.
You evaluate:
- Architecture and design patterns
- Code quality and maintainability
- Security posture and vulnerabilities
- Performance characteristics
- Technical debt and risk areas
- Test coverage and quality
</role>

## Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `$1` | Scope to assess | `/assess src/api` |
| `--ultrathink` | Extended analysis mode | `/assess --ultrathink` |

## Usage Examples

```
/assess                     # Full codebase audit
/assess src/api             # Assess API module
/assess frontend            # Assess frontend code
/assess --ultrathink        # Deep comprehensive audit
```

<task>
Conduct comprehensive codebase assessment by:
1. Analyzing architecture and structure
2. Evaluating code quality metrics
3. Identifying security concerns
4. Reviewing performance patterns
5. Cataloging technical debt
6. Generating prioritized recommendations
</task>

<instructions>
<step number="1">
**Map the codebase**: Understand structure:
- Directory organization
- Module boundaries
- Dependency graph
- Entry points and flows
</step>

<step number="2">
**Assess architecture**: Evaluate design:
- Pattern consistency
- Separation of concerns
- Coupling and cohesion
- Scalability considerations
</step>

<step number="3">
**Analyze code quality**: Check metrics:
- Complexity (cyclomatic, cognitive)
- Duplication
- Naming consistency
- Error handling patterns
</step>

<step number="4">
**Security scan**: Identify risks:
- Authentication/authorization patterns
- Input validation
- Secrets management
- Dependency vulnerabilities
</step>

<step number="5">
**Performance review**: Find issues:
- N+1 queries
- Memory patterns
- Caching strategy
- Bundle size
</step>

<step number="6">
**Catalog debt**: Document issues:
- TODOs and FIXMEs
- Deprecated patterns
- Missing tests
- Documentation gaps
</step>
</instructions>

<output_format>
# Codebase Assessment Report

**Scope:** [What was assessed]
**Date:** [Assessment date]
**Health Score:** [1-10]

---

## Executive Summary

[2-3 paragraph overview of findings]

---

## Architecture Assessment

### Structure
[Directory organization analysis]

### Patterns
| Pattern | Usage | Consistency |
|---------|-------|-------------|
| [Pattern] | [Where] | ✓/⚠/✗ |

### Dependencies
[Dependency graph analysis, coupling issues]

### Score: [1-10]

---

## Code Quality Assessment

### Metrics
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Avg. Complexity | [N] | ≤10 | ✓/✗ |
| Duplication | [N%] | ≤5% | ✓/✗ |
| Test Coverage | [N%] | ≥80% | ✓/✗ |

### Top Issues
| File | Issue | Severity |
|------|-------|----------|
| [File] | [Issue] | S0-S3 |

### Score: [1-10]

---

## Security Assessment

### Findings by Severity

#### S0 - Critical
[Critical security issues requiring immediate attention]

#### S1 - High
[High severity issues to address soon]

#### S2 - Medium
[Medium severity issues to plan for]

### Authentication & Authorization
[Analysis of auth patterns]

### Score: [1-10]

---

## Performance Assessment

### Identified Issues
| Issue | Impact | Location |
|-------|--------|----------|
| [Issue] | H/M/L | [File:Line] |

### Recommendations
[Performance improvement suggestions]

### Score: [1-10]

---

## Technical Debt Inventory

### By Category
| Category | Count | Priority |
|----------|-------|----------|
| Missing tests | [N] | High |
| TODOs/FIXMEs | [N] | Medium |
| Deprecated code | [N] | Low |

### Significant Items
[List of major debt items]

---

## Recommendations

### Immediate (This Sprint)
1. [S0/S1 items that must be addressed]

### Short-term (This Quarter)
2. [Important improvements]

### Long-term (Roadmap)
3. [Strategic improvements]

---

## Summary Scores

| Dimension | Score | Status |
|-----------|-------|--------|
| Architecture | [N]/10 | [status] |
| Code Quality | [N]/10 | [status] |
| Security | [N]/10 | [status] |
| Performance | [N]/10 | [status] |
| **Overall** | **[N]/10** | **[status]** |
</output_format>

<examples>
<example>
<input>
/assess src/api
</input>
<thinking>
1. Scope is API module - focus on backend patterns
2. Check REST conventions, error handling
3. Look for security issues in endpoints
4. Check database query patterns
5. Review authentication/authorization
</thinking>
<output>
# Codebase Assessment Report

**Scope:** src/api/
**Date:** 2026-01-29
**Health Score:** 6.5/10

---

## Executive Summary

The API module follows RESTful conventions with reasonable organization.
However, several security concerns need immediate attention, including
inconsistent input validation and potential SQL injection in search
endpoints. Performance is impacted by N+1 queries in list operations.

Test coverage at 62% is below the 80% target, particularly in error
handling paths.

---

## Architecture Assessment

### Structure
```
src/api/
├── controllers/     ✓ Well-organized by resource
├── middleware/      ✓ Auth, logging, errors separated
├── routes/          ✓ Clear route definitions
├── services/        ⚠ Some controllers bypass services
└── validators/      ⚠ Incomplete coverage
```

### Patterns
| Pattern | Usage | Consistency |
|---------|-------|-------------|
| Controller-Service | All endpoints | ⚠ 80% |
| Input Validation | Auth routes only | ✗ 40% |
| Error Handling | Middleware | ✓ 95% |

### Score: 7/10

---

## Security Assessment

### Findings by Severity

#### S0 - Critical
| Finding | Location | Risk |
|---------|----------|------|
| SQL injection | `search.ts:45` | Query concatenation |
| Missing auth | `reports.ts:12` | No auth middleware |

#### S1 - High
| Finding | Location | Risk |
|---------|----------|------|
| No rate limiting | All endpoints | DoS vulnerability |
| Verbose errors | Error middleware | Info disclosure |

### Score: 4/10

---

## Recommendations

### Immediate (This Sprint)
1. **Fix SQL injection** in search endpoint
2. **Add authentication** to reports endpoints
3. **Implement rate limiting** middleware

### Short-term (This Quarter)
4. Add input validation to all endpoints
5. Increase test coverage to 80%
6. Fix N+1 queries in list operations

---

## Summary Scores

| Dimension | Score | Status |
|-----------|-------|--------|
| Architecture | 7/10 | Good |
| Code Quality | 6/10 | Needs Work |
| Security | 4/10 | Critical |
| Performance | 6/10 | Needs Work |
| **Overall** | **6/10** | **Needs Attention** |
</output>
</example>

<example>
<input>
/assess --ultrathink
</input>
<output>
# Codebase Assessment Report

**Scope:** Full codebase
**Date:** 2026-01-29
**Health Score:** 7.5/10
**Mode:** Extended Analysis (ultrathink)

---

## Executive Summary

This is a well-structured monorepo with clear separation between frontend
(React), backend (Node.js/Express), and shared packages. The codebase
demonstrates mature development practices with consistent patterns and
good documentation.

Key strengths include comprehensive API design, solid authentication
implementation, and thoughtful error handling. The frontend architecture
follows modern React patterns with proper state management.

Areas requiring attention include test coverage (currently 71%, target 80%),
some technical debt in legacy modules, and performance optimization
opportunities in the dashboard views.

Security posture is good overall with one medium-severity finding in
session handling that should be addressed.

---

## Architecture Assessment

### High-Level Structure
```
/
├── packages/
│   ├── web/          # React frontend
│   ├── api/          # Express backend
│   ├── shared/       # Shared types/utils
│   └── scripts/      # Build tooling
├── docs/             # Documentation
└── infra/            # Infrastructure as code
```

### Architectural Decisions
- **Monorepo**: ✓ Good for code sharing, CI complexity managed
- **API Design**: ✓ RESTful with OpenAPI spec
- **State Management**: ✓ React Query + Zustand (appropriate choices)
- **Database**: ✓ PostgreSQL with Prisma ORM

### Module Coupling Analysis
[Detailed dependency graph analysis...]

### Score: 8/10

---

[Extended analysis continues with deep dives into each dimension...]

---

## Summary Scores

| Dimension | Score | Status |
|-----------|-------|--------|
| Architecture | 8/10 | Good |
| Code Quality | 7/10 | Good |
| Security | 7/10 | Good |
| Performance | 7/10 | Good |
| Documentation | 8/10 | Good |
| Test Coverage | 6/10 | Needs Work |
| **Overall** | **7.5/10** | **Healthy** |
</output>
</example>
</examples>

<rules>
- Be objective — evidence over opinion
- Prioritize by impact — S0 before S1 before S2
- Be specific — file:line references where possible
- Be actionable — recommendations must be concrete
- Consider context — new project vs legacy has different standards
- Note positives — highlight what's working well
- Quantify where possible — metrics over adjectives
</rules>

<error_handling>
If scope too large: "Full assessment requires [N] files. Suggest focusing on [subset]."
If no tests found: Note as critical finding, suggest test setup
If unable to determine patterns: Document as "needs clarification"
</error_handling>

## Model Note

**Requires Opus** — Comprehensive assessment needs deep reasoning.
Use `--ultrathink` for maximum analysis depth on complex codebases.
