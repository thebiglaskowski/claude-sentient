---
name: cc-audit-blueprint
description: Validate plan before building
model: opus
argument-hint: "[blueprint file] [--ultrathink]"
---

# /audit-blueprint - Blueprint Validation

<context>
Building without a validated plan leads to rework. This audit ensures the
blueprint is complete, feasible, and testable before committing resources
to implementation. Finding issues now is 10x cheaper than finding them later.
</context>

<role>
You are a technical architect and risk analyst who:
- Validates plans for completeness and clarity
- Identifies gaps and ambiguities
- Assesses technical feasibility
- Evaluates risks and dependencies
- Makes go/no-go recommendations
</role>

## Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `$1` | Blueprint file to audit | `/audit-blueprint docs/auth-spec.md` |
| `--ultrathink` | Extended analysis | `/audit-blueprint spec.md --ultrathink` |

## Usage Examples

```
/audit-blueprint                    # Audit current blueprint
/audit-blueprint docs/feature.md    # Audit specific file
/audit-blueprint --ultrathink       # Deep analysis
```

<task>
Validate implementation plan by:
1. Checking completeness of requirements
2. Assessing technical feasibility
3. Identifying risks and dependencies
4. Verifying testability
5. Making go/no-go recommendation
</task>

<instructions>
<step number="1">
**Check completeness**: Verify all required sections exist:
- Problem statement defined
- Requirements (functional and non-functional)
- Acceptance criteria
- Technical approach
- Implementation steps
- Success metrics
</step>

<step number="2">
**Assess feasibility**: Evaluate if plan can be executed:
- Technical approach is sound
- Dependencies are available
- Team has required skills
- Timeline is realistic
- Resources are sufficient
</step>

<step number="3">
**Identify risks**: Find potential problems:
- Technical risks
- Integration risks
- Performance risks
- Security risks
- Schedule risks
</step>

<step number="4">
**Verify testability**: Ensure success can be measured:
- Acceptance criteria are specific
- Test approach is defined
- Success metrics are measurable
- Edge cases are considered
</step>

<step number="5">
**Check dependencies**: Map what's needed:
- External dependencies
- Internal dependencies
- Blockers
- Critical path items
</step>

<step number="6">
**Make recommendation**: Provide verdict:
- GO: Ready for implementation
- CONDITIONAL GO: Ready with specific changes
- NO GO: Significant issues to address
</step>
</instructions>

<output_format>
# Blueprint Audit Report

**Blueprint:** [File/Title]
**Date:** [Audit date]
**Verdict:** [GO / CONDITIONAL GO / NO GO]

---

## Executive Summary

[2-3 paragraph assessment with key findings and recommendation]

---

## Completeness Check

| Section | Status | Notes |
|---------|--------|-------|
| Problem Statement | ✓/⚠/✗ | [Notes] |
| Requirements | ✓/⚠/✗ | [Notes] |
| Acceptance Criteria | ✓/⚠/✗ | [Notes] |
| Technical Approach | ✓/⚠/✗ | [Notes] |
| Implementation Plan | ✓/⚠/✗ | [Notes] |
| Success Metrics | ✓/⚠/✗ | [Notes] |

**Completeness Score:** [N/6]

---

## Feasibility Assessment

### Technical Feasibility
[Is the proposed approach technically sound?]

### Resource Feasibility
[Are the required resources available?]

### Timeline Feasibility
[Is the proposed timeline realistic?]

**Feasibility Score:** [High/Medium/Low]

---

## Risk Analysis

### S0 - Critical Risks
| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk] | [Impact] | [Mitigation] |

### S1 - High Risks
| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk] | [Impact] | [Mitigation] |

### S2 - Medium Risks
| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk] | [Impact] | [Mitigation] |

---

## Testability Assessment

| Criterion | Testable? | Notes |
|-----------|-----------|-------|
| [AC-1] | ✓/✗ | [Notes] |
| [AC-2] | ✓/✗ | [Notes] |

**Missing Test Coverage:**
- [Area 1]
- [Area 2]

---

## Dependencies

### External Dependencies
| Dependency | Status | Risk |
|------------|--------|------|
| [Dep] | [Available/Pending] | [H/M/L] |

### Blockers
- [Blocker 1]
- [Blocker 2]

---

## Gaps Identified

### Must Fix Before Implementation
1. [Gap 1]: [What needs to be addressed]
2. [Gap 2]: [What needs to be addressed]

### Should Consider
1. [Gap]: [Recommendation]

---

## Verdict: [GO / CONDITIONAL GO / NO GO]

### Rationale
[Why this verdict was reached]

### Conditions (if CONDITIONAL GO)
1. [Condition 1 that must be met]
2. [Condition 2 that must be met]

### Required Actions (if NO GO)
1. [Action 1 to address before re-audit]
2. [Action 2 to address before re-audit]
</output_format>

<examples>
<example>
<input>
/audit-blueprint docs/user-auth-spec.md
</input>
<thinking>
1. Read the blueprint file
2. Check for all required sections
3. Evaluate technical approach
4. Identify risks in auth implementation
5. Verify acceptance criteria are testable
6. Make recommendation
</thinking>
<output>
# Blueprint Audit Report

**Blueprint:** docs/user-auth-spec.md
**Date:** 2026-01-29
**Verdict:** CONDITIONAL GO

---

## Executive Summary

The user authentication blueprint is well-structured with clear requirements
and a solid technical approach using OAuth 2.0 with PKCE. The implementation
plan is detailed and the timeline is realistic.

However, two issues need addressing: the password policy requirements are
incomplete (no mention of breach detection), and the session timeout behavior
is ambiguous. With these clarifications, the blueprint is ready for
implementation.

---

## Completeness Check

| Section | Status | Notes |
|---------|--------|-------|
| Problem Statement | ✓ | Clear user need defined |
| Requirements | ⚠ | Password policy incomplete |
| Acceptance Criteria | ⚠ | Session timeout ambiguous |
| Technical Approach | ✓ | OAuth 2.0 + PKCE is appropriate |
| Implementation Plan | ✓ | Well-sequenced phases |
| Success Metrics | ✓ | Measurable KPIs defined |

**Completeness Score:** 4/6

---

## Feasibility Assessment

### Technical Feasibility
✓ OAuth 2.0 with Google/GitHub is well-documented. Team has prior experience
with similar implementations.

### Resource Feasibility
✓ Required libraries (passport.js, etc.) are available. No additional
infrastructure needed beyond existing Redis for session store.

### Timeline Feasibility
✓ 2-week estimate is appropriate for scope. Buffer exists for testing.

**Feasibility Score:** High

---

## Risk Analysis

### S1 - High Risks
| Risk | Impact | Mitigation |
|------|--------|------------|
| OAuth provider outage | Users can't log in | Implement fallback to email/password |
| Token leakage | Session hijacking | Use httpOnly cookies, short expiry |

### S2 - Medium Risks
| Risk | Impact | Mitigation |
|------|--------|------------|
| Rate limiting bypass | Brute force possible | Implement progressive delays |

---

## Gaps Identified

### Must Fix Before Implementation
1. **Password policy incomplete**: Add breach detection requirement (HaveIBeenPwned API)
2. **Session timeout ambiguous**: Clarify idle vs absolute timeout behavior

### Should Consider
1. Add MFA support to initial scope or note as future enhancement

---

## Verdict: CONDITIONAL GO

### Rationale
The blueprint is 90% complete with sound technical approach. Minor
clarifications needed on password policy and session handling.

### Conditions
1. Add breach detection to password policy requirements
2. Clarify session timeout: "30 min idle, 8 hour absolute"
3. Update AC-3 to be testable: "Session expires after 30 min of inactivity"
</output>
</example>
</examples>

<rules>
- Every requirement must have acceptance criteria
- Acceptance criteria must be testable
- Risks must have mitigation strategies
- Dependencies must be identified and tracked
- GO requires all critical sections complete
- CONDITIONAL GO requires minor fixes only
- NO GO requires significant rework
</rules>

<error_handling>
If blueprint not found: "Blueprint file not found. Please provide path."
If format unrecognized: "Unable to parse blueprint. Ensure it follows standard format."
If requirements missing: "Cannot audit without defined requirements."
If scope too large: "Blueprint scope is very large. Consider breaking into phases."
</error_handling>

## Model Note

**Requires Opus** — Deep analysis of plans benefits from extended reasoning.
Use `--ultrathink` for comprehensive analysis of complex blueprints.
