---
name: Project Hygiene
description: Enforce documentation, changelog, and closeout discipline whenever implementing or modifying project work. Always produce an Update Bundle (STATUS.md, CHANGELOG.md, docs/runbooks/migrations, known issues) and justify any non-applicable items.
---

## Rules

- Treat documentation and changelog updates as part of Definition of Done.
- At the end of any implementation response that changes behavior, interfaces, configuration, ops, or dependencies, include an **Update Bundle** section.
- The Update Bundle must propose exact edits (bullet diffs or full entry text) for:
  - STATUS.md
  - CHANGELOG.md (if triggered)
  - impacted docs/runbooks/migrations
  - KNOWN_ISSUES.md (if any)
- If any item is "not applicable," explicitly justify why.

## Update Bundle Format

```markdown
## Update Bundle

### STATUS.md
[Exact changes or "No update needed — reason"]

### CHANGELOG.md
[Entry text or "Not applicable — internal refactor with no behavior change"]

### Documentation
[List of docs to update with changes, or "No updates needed — reason"]

### KNOWN_ISSUES.md
[New issues to add, or "None"]
```

## Trigger Conditions

Always include an Update Bundle when you:

- Add a new feature
- Fix a user-facing bug
- Change an API or interface
- Modify configuration options
- Change deployment or operational behavior
- Add or remove dependencies
- Complete an execution unit

## Quality Standards

- STATUS.md must always reflect current reality
- CHANGELOG.md entries must be user-focused (what changed, not how)
- Documentation must match implementation
- Known issues must be tracked, not hidden

---

## Final Directive

Documentation is a deliverable, not an afterthought. Every change ships with its Update Bundle.
