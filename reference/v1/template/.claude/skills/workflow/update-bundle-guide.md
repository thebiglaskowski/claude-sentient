---
name: update-bundle-guide
description: Guidance for creating update bundles after implementation work
disable-model-invocation: true
---

# Update Bundle Guide

Guidance for creating update bundles after implementation work.

## Description

Use after completing features, bug fixes, or any work that changes behavior.
Triggers on: "update docs", "changelog", "STATUS.md", "document changes", "what to update", "finish feature".

## Trigger

Use when:
- Completing a feature or bug fix
- Finishing an execution unit
- User asks about documentation updates
- After any change to behavior, interfaces, or configuration

## Update Bundle Structure

After ANY work that changes behavior, interfaces, or configuration, produce:

```markdown
## Update Bundle

### STATUS.md
[Current project state - what's done, what's next]

### CHANGELOG.md
[What changed and why - user-facing description]

### Documentation
[Any docs that need updates, or "None"]

### KNOWN_ISSUES.md
[Any limitations discovered, or "None"]
```

## STATUS.md Format

```markdown
# Project Status

## Current State
[What phase: Planning / Execution / Quality / Release]

## Recently Completed
- [Item 1]
- [Item 2]

## In Progress
- [Current work]

## Next Up
- [Upcoming task]

## Blockers
- [Any blockers, or "None"]
```

## CHANGELOG.md Format

```markdown
## [Version] - YYYY-MM-DD

### Added
- [New features]

### Changed
- [Changes to existing features]

### Fixed
- [Bug fixes]

### Removed
- [Removed features]
```

## When to Skip

- Pure research/exploration (no code changes)
- Reading/understanding code
- Planning discussions (before implementation)
