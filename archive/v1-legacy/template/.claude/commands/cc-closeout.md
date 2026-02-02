---
name: cc-closeout
description: Complete milestone and document learnings
model: sonnet
argument-hint: "[milestone name]"
---

# /closeout - Milestone Completion

<context>
Milestones aren't complete until they're documented and learnings captured.
Proper closeout prevents knowledge loss, ensures clean handoffs, and builds
institutional memory. What we don't document, we repeat.
</context>

<role>
You are a project completion specialist who:
- Ensures all work is truly done
- Captures learnings systematically
- Updates all relevant artifacts
- Creates clean handoff documentation
- Identifies follow-up work
</role>

## Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `$1` | Milestone name | `/closeout v2.0 release` |

## Usage Examples

```
/closeout                       # Close current milestone
/closeout v2.0 release          # Close specific release
/closeout Q4 features           # Close quarterly work
/closeout auth-epic             # Close feature epic
/closeout sprint-23             # Close sprint
```

<task>
Complete a milestone with full documentation by:
1. Verifying all deliverables are complete
2. Capturing learnings (what worked, what didn't)
3. Updating CHANGELOG and documentation
4. Archiving related issues and PRs
5. Identifying follow-up work
</task>

<instructions>
<step number="1">
**Verify completion**: Check all deliverables:
- All planned features implemented
- All tests passing
- Documentation updated
- No critical bugs outstanding
- Acceptance criteria met
</step>

<step number="2">
**Capture learnings**: Document retrospective insights:
- What went well?
- What didn't go well?
- What surprised us?
- What would we do differently?
- Key decisions and their outcomes
</step>

<step number="3">
**Update artifacts**: Ensure all records current:
- CHANGELOG.md with all changes
- Documentation reflects new features
- STATUS.md updated to next phase
- ADRs for key decisions made
</step>

<step number="4">
**Archive work items**: Close out tracking:
- Close completed issues
- Merge or close stale PRs
- Tag release in git
- Archive completed project boards
</step>

<step number="5">
**Identify follow-up**: Capture future work:
- Deferred items
- Technical debt introduced
- Discovered improvements
- Next milestone planning
</step>
</instructions>

<output_format>
# Milestone Closeout: [Name]

**Completed:** [Date]
**Duration:** [Actual vs planned]
**Team:** [Contributors]

---

## Completion Verification

### Deliverables
| Deliverable | Status | Notes |
|-------------|--------|-------|
| [Item] | ✓ Complete / ⚠ Partial / ✗ Incomplete | [Notes] |

### Quality Gates
- [ ] All tests passing
- [ ] Documentation updated
- [ ] No S0/S1 bugs
- [ ] Performance targets met
- [ ] Security review passed

---

## What We Delivered

### Features
- [Feature 1]: [Brief description and impact]
- [Feature 2]: [Brief description and impact]

### Improvements
- [Improvement 1]
- [Improvement 2]

### Bug Fixes
- [Fix 1]
- [Fix 2]

---

## Learnings

### What Went Well ✓
- [Positive 1]
- [Positive 2]

### What Didn't Go Well ✗
- [Challenge 1]: [What we learned]
- [Challenge 2]: [What we learned]

### Surprises
- [Unexpected finding or outcome]

### Key Decisions
| Decision | Context | Outcome |
|----------|---------|---------|
| [Decision] | [Why made] | [How it worked out] |

---

## Metrics

| Metric | Target | Actual |
|--------|--------|--------|
| Timeline | [Planned] | [Actual] |
| Scope | [Planned items] | [Delivered items] |
| Quality | [Target] | [Achieved] |

---

## Follow-Up Work

### Deferred Items
| Item | Reason | Priority |
|------|--------|----------|
| [Item] | [Why deferred] | [When to revisit] |

### Technical Debt Created
- [Debt 1]: [Impact and remediation plan]

### Future Improvements
- [Improvement opportunity discovered]

---

## Artifacts Updated
- [ ] CHANGELOG.md
- [ ] STATUS.md
- [ ] README.md (if needed)
- [ ] Documentation
- [ ] Git tag created

---

## Acknowledgments
[Team members and their contributions]
</output_format>

<examples>
<example>
<input>
/closeout v2.0 release
</input>
<thinking>
1. Major release - thorough verification needed
2. Multiple features shipped - document each
3. Likely had challenges - capture learnings
4. Update all release artifacts
5. Plan v2.1 work
</thinking>
<output>
# Milestone Closeout: v2.0 Release

**Completed:** 2026-01-29
**Duration:** 8 weeks (planned: 6 weeks)
**Team:** Alex, Sam, Jordan, Taylor

---

## Completion Verification

### Deliverables
| Deliverable | Status | Notes |
|-------------|--------|-------|
| OAuth Integration | ✓ Complete | Google + GitHub providers |
| New Dashboard | ✓ Complete | Real-time updates working |
| API v2 | ✓ Complete | Full backward compatibility |
| Mobile Responsive | ⚠ Partial | Tablet optimization deferred |
| Performance Targets | ✓ Complete | LCP < 2s achieved |

### Quality Gates
- [x] All tests passing (487 tests)
- [x] Documentation updated
- [x] No S0/S1 bugs outstanding
- [x] Performance targets met (LCP 1.8s)
- [x] Security review passed

---

## What We Delivered

### Features
- **OAuth 2.0 Authentication**: Users can now sign in with Google or GitHub. Reduced signup friction by 40%.
- **Real-time Dashboard**: Live updates via WebSocket. No more manual refresh needed.
- **API v2**: New endpoints with better pagination, filtering, and error messages.

### Improvements
- 50% faster page loads through code splitting
- Reduced bundle size from 450KB to 280KB
- New onboarding flow with 3-step wizard

### Bug Fixes
- Fixed session timeout not warning users
- Fixed data export failing for large datasets
- Fixed timezone issues in date picker

---

## Learnings

### What Went Well ✓
- **Early API design review** caught breaking changes before implementation
- **Feature flags** let us ship incrementally with confidence
- **Pair programming** on OAuth reduced security bugs to zero
- **Weekly demos** kept stakeholders informed and caught UX issues early

### What Didn't Go Well ✗
- **Underestimated OAuth complexity**: Token refresh edge cases took 2 extra weeks. Next time, prototype auth flows in week 1.
- **Late design changes**: Dashboard redesign mid-sprint caused rework. Lock designs before sprint starts.
- **Test flakiness**: CI failures from flaky tests wasted 10+ hours. Need dedicated test stability sprint.

### Surprises
- Users loved the keyboard shortcuts we added as a bonus feature
- Performance was better than expected after bundle optimization
- The API v1 to v2 migration tool was used by 80% of clients (expected 30%)

### Key Decisions
| Decision | Context | Outcome |
|----------|---------|---------|
| Use PKCE for OAuth | Security requirement | Good - prevented token theft vectors |
| WebSocket over polling | Real-time requirements | Good - 90% less server load |
| Defer mobile tablet | Timeline pressure | OK - only 8% of users on tablet |

---

## Metrics

| Metric | Target | Actual |
|--------|--------|--------|
| Timeline | 6 weeks | 8 weeks |
| Scope | 12 features | 11 features (1 deferred) |
| Test Coverage | 80% | 84% |
| Bug Escape Rate | < 5 | 2 |
| User Satisfaction | 4.0/5 | 4.3/5 |

---

## Follow-Up Work

### Deferred Items
| Item | Reason | Priority |
|------|--------|----------|
| Tablet optimization | Timeline | v2.1 (P2) |
| Apple Sign-In | Scope creep | v2.2 (P3) |
| Offline mode | Technical complexity | v3.0 (P2) |

### Technical Debt Created
- **WebSocket reconnection**: Current implementation doesn't handle network changes well. Needs retry logic with exponential backoff.
- **OAuth token storage**: Using localStorage, should migrate to httpOnly cookies.

### Future Improvements
- Add analytics dashboard based on new API v2 capabilities
- Consider GraphQL for mobile app (reduce over-fetching)
- Explore server components for faster initial loads

---

## Artifacts Updated
- [x] CHANGELOG.md - v2.0.0 entry added
- [x] STATUS.md - Updated to "v2.0 released, planning v2.1"
- [x] README.md - Updated features list
- [x] API Documentation - v2 endpoints documented
- [x] Git tag created: v2.0.0

---

## Acknowledgments
- **Alex**: OAuth implementation lead, WebSocket architecture
- **Sam**: Dashboard UI, performance optimization
- **Jordan**: API v2 design, migration tooling
- **Taylor**: Testing strategy, bug fixes
- **Design team**: Dashboard redesign, onboarding flow
</output>
</example>

<example>
<input>
/closeout sprint-23
</input>
<output>
# Milestone Closeout: Sprint 23

**Completed:** 2026-01-29
**Duration:** 2 weeks (as planned)
**Team:** Core team (5 engineers)

---

## Completion Verification

### Sprint Goals
| Goal | Status | Notes |
|------|--------|-------|
| Complete user settings redesign | ✓ Complete | Shipped to 100% of users |
| Fix critical search bug | ✓ Complete | P99 latency now < 200ms |
| Start API rate limiting | ⚠ Partial | Design complete, implementation WIP |

### Velocity
- **Planned:** 34 points
- **Completed:** 31 points (91%)
- **Carried over:** 3 points (rate limiting)

---

## What We Delivered

### Features
- User settings page redesign with better organization
- Search performance fix (was timing out for complex queries)

### Bug Fixes
- Fixed email notification preferences not saving
- Fixed avatar upload failing for PNG files

---

## Learnings

### What Went Well ✓
- Settings redesign was scoped well
- Search fix root cause found quickly with new logging

### What Didn't Go Well ✗
- Rate limiting was underestimated - needs dedicated sprint focus

---

## Follow-Up Work

### Carried to Sprint 24
- API rate limiting implementation (3 points)

### New Items Discovered
- Need to add rate limit headers to API responses
- Settings page could use keyboard navigation

---

## Artifacts Updated
- [x] Sprint board archived
- [x] STATUS.md updated for Sprint 24
</output>
</example>
</examples>

<rules>
- Don't close out incomplete milestones without explicit decision
- Always capture both successes and failures
- Be specific about learnings, not generic platitudes
- Update CHANGELOG before marking complete
- Create follow-up tickets for deferred work
- Tag releases in git before closing
</rules>

<error_handling>
If milestone not specified: "Which milestone are you closing out?"
If incomplete items found: "The following items are incomplete: [list]. Close anyway?"
If no git tag exists: "No release tag found. Create tag v[X.Y.Z] before closing?"
If CHANGELOG missing entry: "CHANGELOG.md needs update for this milestone. Add entry?"
</error_handling>
