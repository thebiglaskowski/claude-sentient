# Plan: Integrate Underutilized Native Tools

> **Created:** 2026-02-01
> **Status:** Completed
> **Estimated Scope:** Medium (updates to commands + profiles)

---

## Overview

Claude Code has native tools we're not using. This plan adds them to Claude Sentient.

---

## Tasks

### 1. WebSearch Integration (High Priority)

**Where:** `/cs-loop` VERIFY phase

**What:** When quality gates fail, search for solutions before asking user.

**Changes:**
- `commands/cs-loop.md`: Add WebSearch step after gate failure
- Pattern: `WebSearch("python {error_message} fix 2026")`

**Example flow:**
```
[VERIFY] pytest failed: "AttributeError: module 'jwt' has no attribute 'encode'"
[VERIFY] Searching for solution...
[VERIFY] Found: PyJWT vs jwt package conflict. Uninstall jwt, keep PyJWT.
[VERIFY] Applying fix...
```

---

### 2. Structured AskUserQuestion (High Priority)

**Where:** `/cs-loop` decision points, `/cs-plan`

**What:** Replace free-text questions with structured options where applicable.

**Changes:**
- `commands/cs-loop.md`: Use structured questions for common decisions
- `commands/cs-plan.md`: Offer architecture choices with descriptions

**Common decision points to structure:**
| Decision | Options |
|----------|---------|
| Auth approach | JWT / Sessions / OAuth |
| Database | PostgreSQL / SQLite / MongoDB |
| Testing strategy | Unit only / Integration / E2E |
| Error handling | Exceptions / Result types / Status codes |

---

### 3. WebFetch for Dependencies (Medium Priority)

**Where:** `/cs-loop` INIT phase

**What:** When task involves updating/adding dependencies, fetch changelogs.

**Changes:**
- `commands/cs-loop.md`: Detect dependency-related tasks
- Fetch `CHANGELOG.md` or release notes from GitHub

**Trigger keywords:** "update", "upgrade", "migrate", "add dependency"

---

### 4. TaskStop for Timeouts (Medium Priority)

**Where:** `/cs-loop` EXECUTE phase

**What:** Add timeout handling for background tasks.

**Changes:**
- `commands/cs-loop.md`: Track background task IDs
- After N minutes, use `TaskStop` and report
- Add configurable timeout in profile

**Default timeouts:**
| Task Type | Timeout |
|-----------|---------|
| Tests | 10 min |
| Build | 5 min |
| Exploration | 3 min |

---

### 5. NotebookEdit Support (Medium Priority)

**Where:** Python profile

**What:** Add Jupyter notebook handling.

**Changes:**
- `profiles/python.yaml`: Add notebook detection
- Commands for notebook linting (`nbqa`)
- Commands for notebook testing (`nbval`)

**Detection:** `*.ipynb` files present

---

### 6. claude-code-guide Subagent (Low Priority)

**Where:** `/cs-loop` when stuck

**What:** Query Claude Code docs when uncertain about capabilities.

**Changes:**
- `commands/cs-loop.md`: Add fallback to claude-code-guide
- Trigger: Multiple failed attempts at same operation

---

### 7. TaskGet for Context (Low Priority)

**Where:** `/cs-loop` EXECUTE phase

**What:** Fetch full task details before starting work.

**Changes:**
- `commands/cs-loop.md`: Call `TaskGet` before each task
- Use description for better context

---

## Implementation Order

```
Day 1: Tasks 1-2 (High priority - WebSearch + AskUserQuestion)
Day 2: Tasks 3-4 (Medium priority - WebFetch + TaskStop)
Day 3: Tasks 5-7 (Remaining - Notebooks + subagents)
```

---

## Files to Modify

| File | Changes |
|------|---------|
| `commands/cs-loop.md` | WebSearch, AskUserQuestion, WebFetch, TaskStop, TaskGet |
| `commands/cs-plan.md` | Structured AskUserQuestion |
| `profiles/python.yaml` | NotebookEdit support |
| `CLAUDE.md` | Document new integrations |

---

## Success Criteria

- [x] Gate failures trigger WebSearch before asking user
- [x] Common decisions use structured options
- [x] Dependency updates fetch changelogs
- [x] Background tasks have timeouts
- [x] Notebooks work in Python projects
- [x] Documentation updated

---

## Resume Command

```
/cs-loop "Implement native tools integration per reference/PLAN-native-tools.md"
```

---
