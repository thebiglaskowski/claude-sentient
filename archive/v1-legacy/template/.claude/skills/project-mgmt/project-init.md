---
name: project-init
description: Fully automated project setup for Claude Code
model: sonnet
---

# Project Initialization

Fully automated project setup for Claude Code.

## Description

Use when initializing a project, setting up Claude for a new codebase, or when user says "initialize".
Triggers on: "initialize", "init project", "setup project", "initialize this project", "set up claude", "get started".

## Trigger

Activates when:
- User says "initialize this project"
- User says "set up Claude for this project"
- User runs `claude --init` and asks for full setup
- User asks to "get started" on a new project

## What This Does

Runs the full project initialization sequence:

1. **Setup CLAUDE.md** — Create or improve project-specific CLAUDE.md
2. **Setup Gitignore** — Ensure .gitignore covers detected tech stack
3. **Scout Skills** — Find and install relevant skills from skills.sh
4. **Map Project** — Generate pre-computed project context
5. **Verify Setup** — Confirm everything is ready

## Process

### Step 1: Detect Tech Stack

```bash
# Check for project files
ls package.json pyproject.toml requirements.txt go.mod Cargo.toml 2>/dev/null
```

### Step 2: Setup Project CLAUDE.md

Create or improve the root-level CLAUDE.md (project-specific, separate from .claude/CLAUDE.md):

1. Check if `./CLAUDE.md` exists at project root
2. If **NO**: Analyze project and generate comprehensive CLAUDE.md
3. If **YES**: Analyze existing file, identify gaps, offer improvements

The CLAUDE.md should include:
- Project overview and purpose
- Tech stack (detected from project files)
- Architecture (from directory structure analysis)
- Development setup instructions
- Code standards (detected from linter configs, existing patterns)
- Testing approach
- Key files
- Common tasks
- Workflow integration with `.claude/`

See `/claude-md` command or `claude-md-manager` skill for full process.

```bash
# Check if root CLAUDE.md exists
test -f ./CLAUDE.md && echo "EXISTS - will analyze" || echo "MISSING - will create"
```

### Step 3: Setup Gitignore

Ensure .gitignore is comprehensive for detected technologies:

1. Read existing .gitignore (if any)
2. Detect all technologies (Node.js, Python, frameworks, etc.)
3. Add missing universal entries (.env, IDE files, OS files)
4. Add missing technology-specific entries (node_modules, __pycache__, etc.)
5. Preserve existing custom entries

```bash
# Check current .gitignore status
cat .gitignore 2>/dev/null || echo "No .gitignore found - will create"
```

Key entries to ensure are present:
- `.env*` — Never commit secrets
- `node_modules/` or equivalent dependency folders
- Build output (`dist/`, `build/`, `.next/`, etc.)
- IDE settings (`.idea/`, `.vscode/`)
- Coverage reports (`coverage/`)

### Step 4: Install Skills

Run the skill-scout process (via `/scout-skills`):
- Search skills.sh for matching technologies
- Auto-install high-confidence skills
- Recommend mid-tier skills

```bash
npx skills find "<technology>"
npx skills add "<owner/repo@skill>" --agent claude-code -y
```

### Step 5: Generate Project Map

Run the project-mapper process (via `/map-project`):
- Analyze directory structure
- Identify entry points
- Document patterns
- Create `.claude/context/PROJECT_MAP.md`

```bash
mkdir -p .claude/context
# Generate PROJECT_MAP.md
```

### Step 6: Verify Setup

Confirm:
- [ ] Root CLAUDE.md exists and is comprehensive
- [ ] .gitignore exists and covers tech stack
- [ ] Skills installed (check `.claude/skills/`)
- [ ] PROJECT_MAP.md exists and has content
- [ ] STATUS.md exists (create if not)

### Step 7: Report

```markdown
## Project Initialized

**Tech Stack Detected:** [list]

**CLAUDE.md:** [created/improved] with [X] sections
- Overview, Tech Stack, Architecture, Setup, Standards, Testing, Key Files, Tasks

**.gitignore:** [created/updated] with [X] entries

**Skills Installed:** [count]
- [skill 1]
- [skill 2]

**Project Map:** Generated (.claude/context/PROJECT_MAP.md)

**Next Steps:**
- Review CLAUDE.md and verify accuracy
- Review STATUS.md and update current focus
- Run /daily to start working
- Run /plan if starting a new feature
```

## When to Run

- **First time** using Claude on a project
- **After** adding the .claude template to a project
- **After** major technology changes (new framework, etc.)
- **Periodically** to refresh skills and context

## Idempotent

Safe to run multiple times:
- Improves CLAUDE.md (preserves custom sections, adds missing)
- Merges .gitignore entries (preserves existing, adds missing)
- Skips already-installed skills
- Regenerates PROJECT_MAP.md (updates to current state)
- Won't duplicate anything

## Full Command

To run manually:
```
Initialize this project
```

Or run components separately:
```
/claude-md
/gitignore
/scout-skills
/map-project
```
