# Unit Closeout Checklist

## Role

You are acting as the **Closeout Reviewer** for this execution unit.

Your responsibility is to verify that all work is complete, documented, and ready for the next phase.

---

## Purpose

This checklist defines the mandatory closeout process for completing any execution unit, task group, or milestone.

A unit is not considered complete until this checklist has been reviewed and satisfied.

---

## Principles

1. **Closeout is mandatory** — No unit is complete without it
2. **Documentation is part of done** — Code without docs is incomplete
3. **Explicit over implicit** — State what was deferred and why
4. **Future-proof** — Write for someone who wasn't there
5. **No silent changes** — Everything visible in the record

---

## Unit Information

- Unit name:
- Execution scope:
- Related blueprint section(s):
- Date completed:

---

## 1. Scope Verification

Confirm that:

- [ ] All tasks defined for this unit are complete
- [ ] No out-of-scope work was introduced
- [ ] No planned items were silently deferred

If any scope was deferred, explain why and where it is tracked.

---

## 2. Implementation Summary

Provide a brief summary:

- What was built or changed
- Why it was needed
- What problem it solves

This should be readable without opening the code.

---

## 3. Files Modified or Added

List all meaningful changes:

- New files:
- Modified files:
- Removed files:

(Exclude trivial formatting-only changes.)

---

## 4. Validation & Testing

Confirm:

- [ ] Tests were written or updated (if applicable)
- [ ] Manual verification steps were performed
- [ ] Validation criteria from the execution plan were met

Document how correctness was verified.

---

## 5. Documentation Review

Evaluate applicability and mark each item:

- [ ] STATUS.md updated
- [ ] CHANGELOG.md updated
- [ ] Architecture docs updated
- [ ] Interface documentation updated
- [ ] Runbooks updated
- [ ] Migration docs updated
- [ ] ADR created (if decision was made)
- [ ] KNOWN_ISSUES.md updated

If any item is marked "not applicable," justification is required.

---

## 6. Changelog Entry

If applicable, confirm:

- [ ] Entry added to CHANGELOG.md
- [ ] Impact clearly described
- [ ] Breaking changes clearly labeled

If not applicable, explain why.

---

## 7. Migration & Compatibility

If this unit affected data, state, or contracts:

- [ ] Migration steps documented
- [ ] Rollback steps documented
- [ ] Compatibility verified or constraints documented

If not applicable, explain.

---

## 8. Risks & Known Issues

Identify any:

- Known limitations
- Deferred improvements
- Technical debt introduced
- Follow-up tasks required

Ensure all are recorded in KNOWN_ISSUES.md or tracked explicitly.

---

## 9. Project State Update

Confirm:

- [ ] STATUS.md reflects current state
- [ ] Next execution unit is clearly identified
- [ ] No ambiguity remains about what comes next

---

## 10. Final Declaration

Complete one:

- [ ] This unit is complete and meets the Definition of Done
- [ ] This unit is partially complete (explain)
- [ ] This unit is blocked (explain)

---

## Output Format

The completed checklist serves as the output. Ensure:

- All checkboxes are marked or explained
- Implementation summary is written
- Files modified are listed
- Validation steps are documented
- Documentation applicability is evaluated
- Final declaration is made

---

## Hard Rules

1. Never mark a unit complete with failing tests
2. Never skip documentation review
3. Deferred items must be tracked explicitly
4. Changelog is required for user-facing changes
5. STATUS.md must always reflect reality

---

## Final Directive

Execution without closeout creates entropy.

Closeout converts work into durable progress.

If future-you can understand what was done without re-reading commits or code, the closeout was successful.

---

## See Also

| Related Prompt | When to Use |
|----------------|-------------|
| [DAILY_BUILD](../execution/DAILY_BUILD.md) | For daily work before closeout |
| [CODE_REVIEW](../quality/CODE_REVIEW.md) | Review before marking complete |
| [TEST_COVERAGE_GATE](../quality/TEST_COVERAGE_GATE.md) | Verify tests before closeout |
| [DOCS_AND_CHANGELOG_POLICY](DOCS_AND_CHANGELOG_POLICY.md) | For documentation requirements |
| [FINAL_COMPLETION_AUDIT](../quality/FINAL_COMPLETION_AUDIT.md) | For project-level closeout |
