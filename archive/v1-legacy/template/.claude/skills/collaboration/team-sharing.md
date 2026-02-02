---
name: team-sharing
description: Share prompts, skills, and patterns across team
model: sonnet
---

# Team Sharing

Share prompts, skills, and patterns across team.

## Description

Collaborate on prompts, skills, and patterns with team members.
Triggers on: "share with team", "team prompts", "sync prompts", "collaborate", "team setup".

## Sharing Architecture

```
Team Repository (git)
├── prompts/              # Shared prompts
├── skills/               # Shared skills
├── patterns/             # Shared patterns
├── snippets/             # Shared snippets
└── config/               # Shared configuration
    ├── hooks.json
    └── settings.json

Project Repository
└── .claude/
    ├── CLAUDE.md         # Project-specific
    ├── commands/         # Inherited + project-specific
    ├── skills/           # Inherited + project-specific
    └── local/            # Not shared (gitignored)
```

## Setup Team Sharing

### 1. Create Team Repository
```bash
# Create team prompts repo
mkdir team-prompts && cd team-prompts
git init

# Structure
mkdir -p prompts skills patterns snippets config
touch README.md

# Initial commit
git add . && git commit -m "Initialize team prompts"
git remote add origin git@github.com:team/prompts.git
git push -u origin main
```

### 2. Configure in Projects
In project's `.claude/team.json`:
```json
{
  "team": {
    "repository": "git@github.com:team/prompts.git",
    "branch": "main",
    "syncOnStart": true,
    "localOverrides": true
  }
}
```

### 3. Sync Team Resources
```bash
# Pull team resources
claude-team sync

# Or manually
git clone git@github.com:team/prompts.git .claude/team
```

## Sharing Workflows

### Share a Skill
```markdown
## Share Skill with Team

**Skill:** custom-review.md
**From:** project-a/.claude/skills/

**Steps:**
1. Copy to team repo
2. Generalize project-specific parts
3. Add documentation
4. Create PR

```bash
cp .claude/skills/custom-review.md ../team-prompts/skills/
cd ../team-prompts
git add skills/custom-review.md
git commit -m "Add custom review skill from project-a"
git push
```

**Notify team:** Post in #engineering about new skill
```

### Share a Pattern
```markdown
## Share Pattern with Team

**Pattern:** API pagination
**Source:** project-b

**Process:**
1. Extract pattern to generic form
2. Remove project-specific code
3. Add to patterns library
4. Document usage

**PR:** team/prompts#45 - Add pagination pattern
```

## Team Configuration

### Shared Settings
`config/settings.json`:
```json
{
  "team": "Engineering",
  "conventions": {
    "commitStyle": "conventional",
    "branchNaming": "feature/TICKET-description",
    "prTemplate": true
  },
  "quality": {
    "minCoverage": 80,
    "requiredReviewers": 1,
    "blockOnS0S1": true
  },
  "models": {
    "default": "sonnet",
    "review": "opus",
    "simple": "haiku"
  }
}
```

### Shared Hooks
`config/hooks.json`:
```json
{
  "PreCommit": [
    {
      "name": "team-lint",
      "command": "npm run lint"
    }
  ],
  "PrePush": [
    {
      "name": "team-test",
      "command": "npm test"
    }
  ]
}
```

## Inheritance Model

### Precedence Order
1. **Project-specific** (highest priority)
2. **Team shared**
3. **Global defaults** (lowest priority)

### Example
```markdown
**Skill lookup:** `code-review`

1. Check: .claude/skills/code-review.md (project)
   → Not found
2. Check: .claude/team/skills/code-review.md (team)
   → Found! Use this
3. (Fallback): Built-in code review

**Result:** Team skill used
```

### Override Team Settings
In project `.claude/CLAUDE.md`:
```markdown
## Team Overrides

This project uses different conventions:
- Coverage threshold: 90% (team default: 80%)
- Commit style: angular (team default: conventional)
```

## Collaboration Features

### Skill Suggestions
```markdown
## Team Skill Recommendations

Based on your project (Next.js + Prisma):

**From team library:**
- ✅ nextjs-patterns (installed)
- 📥 prisma-migrations (recommended)
- 📥 api-testing (recommended)

**From teammates:**
- @alice shared `form-validation` skill
- @bob shared `error-boundary` pattern

[Install recommended] [Browse all]
```

### Activity Feed
```markdown
## Team Activity

**Recent updates to team-prompts:**

- 2h ago: @alice added `form-validation` skill
- 1d ago: @bob updated `api-error-handling` pattern
- 2d ago: @carol fixed typo in `code-review` prompt
- 3d ago: @dave added `testing-fixtures` snippets

**Your contributions:**
- 5 skills shared
- 3 patterns contributed
- Last contribution: 1 week ago
```

### Request Skills
```markdown
## Skill Requests

**Open requests:**
- [ ] GraphQL subscription pattern (3 👍)
- [ ] Stripe integration skill (2 👍)
- [ ] Docker multi-stage build (1 👍)

**Request new skill:**
"Request a skill for [description]"
```

## Sync Commands

### Full Sync
```
"Sync with team"
"Update team resources"
```
Pulls latest from team repo.

### Push Local Changes
```
"Share my changes with team"
"Push to team repo"
```
Creates PR with local changes.

### Check for Updates
```
"Are there team updates?"
"What's new from team?"
```

## Conflict Resolution

### Skill Conflict
```markdown
## Conflict Detected

**Skill:** code-review.md

**Team version:**
- Updated: 2 days ago by @alice
- Changes: Added security checks

**Local version:**
- Updated: Today by you
- Changes: Added performance checks

**Options:**
1. Keep local (ignore team update)
2. Use team version (lose local changes)
3. Merge both (recommended)
4. View diff
```

### Merge Strategy
```markdown
## Merge Skills

Combining local and team versions:

**From team:**
+ Security checks section
+ OWASP reference

**From local:**
+ Performance checks section
+ Bundle size check

**Merged result:** [Preview]

[Apply merge] [Edit manually] [Cancel]
```

## Access Control

### Roles
| Role | Permissions |
|------|-------------|
| Admin | Full access, manage members |
| Contributor | Add/edit resources |
| Viewer | Read-only access |

### Approval Workflow
```markdown
## PR: Add new-skill.md

**Author:** @developer
**Reviewers:** @lead, @senior

**Checks:**
- [ ] Follows team conventions
- [ ] Documented properly
- [ ] Tested in at least one project
- [ ] No sensitive information

**Status:** Awaiting review
```

## Best Practices

### When to Share
- Pattern used in 2+ projects
- Skill that's generally applicable
- Snippets that save significant time
- Configurations that enforce standards

### When NOT to Share
- Project-specific code
- Experimental/unstable patterns
- Personal preferences
- Sensitive/proprietary logic

### Contribution Guidelines
```markdown
## Contributing to Team Prompts

1. **Test locally first** - Use in your project
2. **Generalize** - Remove project-specific parts
3. **Document** - Add clear usage instructions
4. **PR** - Submit for team review
5. **Notify** - Post in #engineering
```
