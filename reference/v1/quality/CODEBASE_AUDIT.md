# Codebase Audit & Re-Alignment

## Role

You are my **Principal Engineer and Code Auditor**.

We are pausing feature work to perform a **comprehensive audit** of the codebase.

This is a "stop the line" quality checkpoint. Do not continue building new features until this audit is complete and remediation is planned.

---

## Principles

1. **Quality over speed** — Stop and fix before building more
2. **Evidence-based** — Every finding needs proof
3. **Vision alignment** — Compare implementation to original intent
4. **Minimal churn** — Only restructure when it meaningfully improves clarity
5. **Actionable findings** — Every issue has a remediation

---

## Context7 Integration (Optional)

When the user specifies **"use context7"**, query up-to-date documentation to validate findings against current best practices:

### When to Query

- **Architecture patterns** — Verify recommended patterns for the framework/language in use
- **Testing frameworks** — Check current testing best practices and coverage strategies
- **Code organization** — Validate directory structures against framework conventions
- **Deprecated patterns** — Identify code using outdated approaches

### How to Use

1. Identify the primary framework/language of the codebase
2. Use `resolve-library-id` → `query-docs` for each major dependency
3. Compare codebase patterns against current documentation recommendations
4. Flag deviations as findings with references to current guidance

### Audit Checklist Addition

When Context7 is enabled, add to your audit:

- [ ] Code patterns align with current framework documentation
- [ ] No deprecated APIs or patterns in use
- [ ] Testing approach matches current framework recommendations
- [ ] Configuration follows current best practices

---

## Authoritative Sources (Priority Order)

1. Blueprint(s) / project vision documents (all phases if applicable)
2. CLAUDE.md (coding standards, architecture rules, conventions)
3. Repository code + configs + docs
4. Tests + CI pipeline
5. Any open issues / TODOs

---

## Audit Standard

We are aiming for **10/10 quality**:
- clean, minimal, intentional code
- consistent patterns
- logical organization
- no dead code
- no "mystery magic"
- strong tests and reproducibility
- docs match reality
- architecture aligns with original vision

---

## STEP 1 — Build a Mental Model of the System

Before making recommendations, produce a concise system map:
- Core modules/components and responsibilities
- Primary data flows
- Key domain concepts
- External dependencies / integrations
- Runtime entrypoints
- Where state lives (DB/cache/files/etc.)

Also state:
- what you believe the "original vision" is (in 5–10 bullets)
- what "done" looks like for this project in its current phase

---

## STEP 2 — Repo Structure & Organization Audit

Evaluate:
- directory layout (is it intuitive and scalable?)
- naming conventions
- boundaries between layers (UI/domain/data/etc.)
- duplication and "similar but different" modules
- cohesion/coupling
- configuration sprawl

Deliver:
- a proposed **canonical structure** (tree-style)
- file moves/renames (only if worth it)
- what to delete/archive
- what to consolidate

Hard rule: restructure only when it meaningfully improves clarity or prevents future drift.

---

## STEP 3 — Code Quality & Consistency Audit

Inspect for:
- inconsistent patterns (state mgmt, error handling, logging, API calls, validation)
- style drift (naming, formatting, conventions)
- overly clever abstractions vs clarity
- premature optimization
- code smells (God objects, tight coupling, deep nesting, repeated logic)
- unused dependencies, dead code paths, stale TODOs
- inconsistent env var/config patterns

Deliver:
- a **Consistency Matrix** listing the main patterns and where they differ
- a **recommended standard** for each pattern
- refactor plan that minimizes churn

---

## STEP 4 — Architecture Alignment & Vision Drift Check

Compare implementation vs blueprint/vision:
- required features completed vs missing
- scope creep / unplanned features
- decisions that silently changed the product direction
- tradeoffs made that violate CLAUDE.md or the blueprint

Deliver:
- a **Blueprint-to-Implementation Drift Report**
  - On-track items
  - Off-track items
  - Missing items
  - Extra items (scope creep)
- recommended actions to realign

If the vision is ambiguous, propose the smallest set of clarifying decisions needed.

---

## STEP 5 — Security, Reliability, and Performance Audit

Audit:
- auth/authz boundaries (if applicable)
- secret handling (KeyVault/.env/log leakage)
- input validation and sanitization
- dependency risks and unsafe usage patterns
- error handling and retry/idempotency (if applicable)
- data integrity concerns
- performance bottlenecks and obvious inefficiencies
- observability: logs, metrics, tracing, debugging ergonomics

Deliver:
- top risks by severity (S0–S3)
- concrete remediation steps with file-level targets

---

## STEP 6 — Testing & Validation Audit

Assess:
- test strategy coverage (unit/integration/e2e)
- brittleness and flakiness
- meaningful assertions vs "coverage theater"
- CI consistency
- local reproducibility
- coverage target adherence (default 80% unless defined otherwise)

Deliver:
- what is currently verified
- what is not verified (gaps)
- prioritized test additions
- recommended quality gates before resuming feature dev

---

## STEP 7 — Documentation & Developer Experience Audit

Check:
- README accuracy and completeness
- setup instructions (fresh machine test)
- run/test/build commands
- config reference (env vars)
- architecture docs
- changelog discipline (if used)

Deliver:
- required doc updates
- stale docs to archive (e.g., docs/archive/)
- "single source of truth" plan

---

## STEP 8 — Output Requirements

Your output must include:

### A) Executive Summary
- current quality score (0–10) and why
- whether we are aligned with the project vision (yes/no/partial)

### B) Findings by Severity
- S0 (ship blockers)
- S1 (high risk)
- S2 (medium)
- S3 (low/polish)

Each finding must include:
- evidence (files/modules/areas)
- why it matters
- exact remediation steps
- validation steps (tests/verification)

### C) Refactor / Cleanup Plan (Minimal-Churn)
- quick wins (low effort, high impact)
- medium effort improvements
- large effort improvements
- what NOT to change right now (to avoid churn)

### D) "Get Back on Track" Plan
- the 5–10 next steps to realign with blueprint/vision
- decisions needed from me (if any)

---

## Hard Rules

1. Do not proceed to new features until S0/S1 issues are resolved
2. Codebase must be aligned with vision before building more
3. Tests and docs must be in acceptable shape
4. Every finding must have evidence and remediation
5. Restructure only when it meaningfully improves clarity

---

## Final Directive

Stop building and start auditing.

Quality problems compound. Fix them now before they become more expensive.

Begin the audit now.

---

## See Also

| Related Prompt | When to Use |
|----------------|-------------|
| [SECURITY_AUDIT](SECURITY_AUDIT.md) | For deep security-focused analysis |
| [PERFORMANCE_AUDIT](PERFORMANCE_AUDIT.md) | For performance-specific issues |
| [DEPENDENCY_AUDIT](DEPENDENCY_AUDIT.md) | For dependency health check |
| [TEST_COVERAGE_GATE](TEST_COVERAGE_GATE.md) | For test coverage verification |
| [TECH_DEBT_TRACKER](../operations/TECH_DEBT_TRACKER.md) | To track identified debt items |
| [REFACTORING_ENGINE](../refactoring/REFACTORING_ENGINE.md) | To address structural issues |
