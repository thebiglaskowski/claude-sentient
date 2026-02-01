# Phase 1: Initialize

> **Purpose:** Load context, detect project type, prepare for work
> **Duration:** ~30 seconds
> **Triggers:** Start of /cs-loop or session start

---

## Overview

The init phase sets up everything needed for the autonomous loop. It detects what kind of project we're in, loads the appropriate profile, and retrieves relevant memory from previous sessions.

---

## Process

### 1. Detect Project Type

```
SCAN project root for profile indicators:
  - pyproject.toml, requirements.txt → Python
  - package.json, tsconfig.json → TypeScript
  - go.mod → Go
  - *.sh, *.ps1 → Shell
  - None match → General

LOAD matching profile from profiles/
```

### 2. Load Profile Configuration

```
FROM profile:
  - tools (lint, test, format commands)
  - thresholds (coverage, complexity)
  - patterns to apply
  - rules to load
  - conventions
```

### 3. Load Project State

```
READ .claude/state/loop.state.json if exists:
  - Previous work queue items
  - Incomplete tasks
  - Last checkpoint

IF no state file:
  CREATE fresh state
```

### 4. Emit Init Complete

```
STATE UPDATE:
  phase: "init"
  status: "complete"
  profile: detected_profile
  context_loaded: true
```

---

## Outputs

| Output | Description |
|--------|-------------|
| `profile` | Detected project profile |
| `tools` | Available tooling |
| `context` | Loaded memory and state |
| `ready` | Boolean, ready to proceed |

---

## Skip Conditions

This phase cannot be skipped. It must run at the start of every loop.

---

## Error Handling

| Error | Recovery |
|-------|----------|
| No profile matches | Use general profile |
| State file corrupted | Create fresh state |

---

## Example

```
[INIT] Detecting project type...
[INIT] Found: pyproject.toml, **/*.py
[INIT] Loading profile: python
[INIT] Tools: ruff, pytest, pyright
[INIT] Ready to proceed
```
