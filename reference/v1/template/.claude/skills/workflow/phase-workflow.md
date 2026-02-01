---
name: phase-workflow
description: Detailed workflows for each project phase
model: sonnet
---

# Phase Workflow Guide

Detailed workflows for each project phase.

## Trigger

Use when:
- Starting a new project
- Transitioning between phases
- Unsure what to do next
- User asks about project workflow

## Phase Detection

```
┌─────────────────────────────────────────────────────────┐
│                    PROJECT PHASE?                        │
├─────────────────────────────────────────────────────────┤
│  No spec/blueprint exists?                               │
│  └─► PLANNING PHASE                                     │
│                                                          │
│  Spec exists, building features?                         │
│  └─► EXECUTION PHASE                                    │
│                                                          │
│  Features complete, verifying quality?                   │
│  └─► QUALITY PHASE                                      │
│                                                          │
│  Ready to ship?                                          │
│  └─► RELEASE PHASE                                      │
│                                                          │
│  Existing project needs assessment?                      │
│  └─► MAINTENANCE PHASE                                  │
└─────────────────────────────────────────────────────────┘
```

## Planning Phase

**Goal:** Turn ideas into executable plans.

**Workflow:**
1. `/plan` — Create detailed specification
2. `/audit-blueprint` — Validate plan completeness
3. `/adr` — Document key architectural decisions
4. Proceed to Execution when audit passes

**Exit Criteria:**
- Spec approved and complete
- All blockers identified
- Architecture decisions documented

## Execution Phase

**Goal:** Build what was planned.

**Workflow:**
1. `/daily` — Each session: review state, identify task, build
2. `/spike` — When blocked by unknowns
3. `/closeout` — After each milestone

**Exit Criteria:**
- All planned features implemented
- Tests passing
- Documentation updated

## Quality Phase

**Goal:** Verify everything works and is documented.

**Workflow:**
1. `/test` — Verify test coverage (must pass 80%+)
2. `/review` — Review all changes
3. `/secure` — Security audit (for user-facing features)
4. `/assess` — Final completion audit

**Exit Criteria:**
- Test coverage meets threshold
- No S0/S1 issues
- Documentation complete

## Release Phase

**Goal:** Ship with confidence.

**Workflow:**
1. `/release` — Pre-release checklist
2. Deploy to production
3. Monitor for issues

**Exit Criteria:**
- All checklist items green
- Stakeholders notified
- Rollback plan ready

## Maintenance Phase

**Goal:** Keep existing projects healthy.

**Workflow:**
- `/assess` — Full codebase audit
- `/debt` — Catalog technical debt
- `/refactor` — Safe code improvement
- `/fix` — Bug hunting
- `/postmortem` — Learn from incidents

**Exit Criteria:** Varies by task
