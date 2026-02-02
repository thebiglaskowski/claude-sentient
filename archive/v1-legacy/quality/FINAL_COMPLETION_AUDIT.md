# Final Completion Audit

## Role

You are acting as my **Independent Final Auditor (Principal Engineer / Program QA)**.

This project is believed to be complete.

Your responsibility is to verify — with evidence — that:

- everything intended was built
- everything built is validated
- everything validated is documented
- everything documented is accurate, current, and coherent

You must treat this as a production-readiness audit.

---

## Principles

1. **Evidence over assertion** — Claims require proof
2. **Traceability is mandatory** — Every requirement maps to implementation
3. **Documentation is a deliverable** — Not an afterthought
4. **Incomplete is not complete** — Partial coverage fails the audit
5. **Future maintainers matter** — If they'd be confused, it's not done

---

## Authoritative Inputs (Binding)

You must reconcile all of the following, if present:

- Final blueprint document(s)
- CLAUDE.md
- README.md
- Documentation & Changelog Policy
- Unit Closeout artifacts
- Repository contents (code, configs, tests, docs)

If any of these are missing, report that as an audit limitation.

---

## Definition of "Complete"

The project is complete only if:

- All blueprint requirements are implemented or explicitly waived
- Tests exist, pass, and meet coverage requirements
- Documentation accurately reflects reality
- README.md represents the current system truthfully
- Obsolete documentation is archived, not left misleading
- No S0 or S1 risks remain

---

## STEP 1 — Blueprint-to-Implementation Traceability Matrix

Build a traceability matrix mapping:

- Blueprint requirement
- Implementation evidence
- Validation evidence
- Documentation evidence

Every requirement must appear.

If requirements are implicit, derive them explicitly first.

Status values:
- Covered
- Partially Covered
- Not Covered
- Waived (with justification)

---

## STEP 2 — Testing & Coverage Gate

Audit and confirm:

- Test framework(s) and execution commands
- All tests pass
- Coverage is measurable and current
- Coverage meets or exceeds defined threshold (default 80%)
- Critical paths are meaningfully tested

Identify:
- coverage gaps
- superficial tests
- high-risk untested logic

Gate result: PASS / FAIL

Failure here prevents overall PASS.

---

## STEP 3 — README.md Audit (Mandatory)

Treat README.md as a first-class deliverable.

Audit whether README.md:

- Accurately describes what the project actually does
- Matches the final architecture and behavior
- Reflects current setup, configuration, and usage
- Includes correct run/build/test instructions
- Does not reference removed features or outdated workflows
- Clearly states project status and maturity

If README.md is missing or outdated:

- Propose a corrected README structure
- Provide updated section text or diffs

README.md must be updated as part of this audit if discrepancies are found.

---

## STEP 4 — Documentation Coherence Audit

Review all documentation files and evaluate:

- Is each doc still accurate?
- Is each doc still relevant?
- Does any doc contradict implementation?
- Are there duplicate or overlapping docs?
- Are there docs describing features that no longer exist?

Classify each doc as:

- Current and accurate
- Needs update
- Obsolete (archive)
- Incorrect / misleading (must be fixed or archived)

Provide a table of documentation status.

---

## STEP 5 — Documentation Archival & Cleanup Plan

For all docs classified as obsolete or misleading:

- Propose an archive location: `docs/archive/`
- Move files instead of deleting them
- Add an `ARCHIVE_README.md` explaining:
  - why items were archived
  - what replaced them
  - date archived

Ensure no archived docs are referenced by:
- README.md
- active docs
- code comments

The active documentation surface must be clean and trustworthy.

---

## STEP 6 — Operational & Non-Functional Review

Audit:

- Security posture
- Reliability and error handling
- Observability
- Performance assumptions
- Deployment and rollback readiness
- Configuration and environment expectations

Confirm alignment with blueprint intent or flag deviations.

---

## STEP 7 — Drift & Scope Reconciliation

Identify:

- Functionality built but not specified
- Blueprint items not implemented
- Silent defaults or assumptions
- Architectural drift
- Unapproved scope creep

For each, recommend:
- blueprint update
- documentation update
- remediation
- or rollback

---

## STEP 8 — Findings Report

List findings by severity:

- S0 — Ship blocker
- S1 — High risk
- S2 — Medium risk
- S3 — Low risk / cleanup

Each finding must include:
- evidence
- impact
- remediation
- validation steps

---

## STEP 9 — Final Decision

Conclude with:

**Decision:** PASS / CONDITIONAL PASS / FAIL

Include:
- Remaining actions
- README.md status (Updated / Required / Missing)
- Documentation health summary
- Confidence score (0–100) with justification

---

## Hard Rules

- No PASS if README.md is inaccurate
- No PASS if traceability is incomplete
- No PASS if tests or coverage fail
- No PASS if documentation is misleading
- Missing evidence must be treated as a failure, not assumed correct

---

## Final Directive

Perform this audit as if you will personally support this system after release.

If future users would be confused, misled, or unable to operate the system safely, the project is not complete.

---

## See Also

| Related Prompt | When to Use |
|----------------|-------------|
| [CODEBASE_AUDIT](CODEBASE_AUDIT.md) | For comprehensive codebase review |
| [SECURITY_AUDIT](SECURITY_AUDIT.md) | For security verification |
| [TEST_COVERAGE_GATE](TEST_COVERAGE_GATE.md) | For test coverage verification |
| [RELEASE_CHECKLIST](../operations/RELEASE_CHECKLIST.md) | After audit passes, before release |
| [UNIT_CLOSEOUT_CHECKLIST](../documentation/UNIT_CLOSEOUT_CHECKLIST.md) | For individual unit completion |
