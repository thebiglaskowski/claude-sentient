# Commands Index

Searchable index of all `/cc-*` commands organized by category.

All commands use the `cc-` namespace to avoid conflicts with other tools.

---

## Quick Search

| Need to... | Use Command | Category |
|------------|-------------|----------|
| Plan a feature | `/cc-plan` | Planning |
| Validate a plan | `/cc-audit-blueprint` | Planning |
| Research a topic | `/cc-spike` | Planning |
| Continue work | `/cc-daily` | Execution |
| Run autonomous loop | `/cc-loop` | Execution |
| Analyze codebase | `/cc-analyze` | Execution |
| Review code | `/cc-review` | Quality |
| Run tests | `/cc-test` | Quality |
| Security audit | `/cc-secure` | Quality |
| Full assessment | `/cc-assess` | Quality |
| Fix bugs | `/cc-fix` | Quality |
| Refactor code | `/cc-refactor` | Quality |
| Performance audit | `/cc-perf` | Quality |
| Check dependencies | `/cc-deps` | Quality |
| Track debt | `/cc-debt` | Quality |
| UI/UX audit | `/cc-ui` | Frontend |
| Terminal UI audit | `/cc-terminal` | Frontend |
| SEO audit | `/cc-seo` | Frontend |
| Frontend-backend sync | `/cc-sync` | Frontend |
| Create commit | `/cc-commit` | Git |
| Create PR | `/cc-pr` | Git |
| Revert changes | `/cc-revert` | Git |
| Release checklist | `/cc-release` | Operations |
| Incident analysis | `/cc-postmortem` | Operations |
| Migration planning | `/cc-migrate` | Operations |
| Complete milestone | `/cc-closeout` | Operations |
| Update changelog | `/cc-changelog` | Documentation |
| Document decision | `/cc-adr` | Documentation |
| Generate docs | `/cc-docs` | Documentation |
| Onboarding guide | `/cc-onboard` | Documentation |
| Standup summary | `/cc-standup` | Team |
| Sprint retro | `/cc-retro` | Team |
| Scaffold project | `/cc-scaffold` | Setup |
| Install skills | `/cc-scout-skills` | Setup |
| Map project | `/cc-map-project` | Setup |
| Update gitignore | `/cc-gitignore` | Setup |
| Create CLAUDE.md | `/cc-claude-md` | Setup |
| Generate prompts | `/cc-prompt` | Setup |

---

## By Category

### Planning
| Command | Purpose |
|---------|---------|
| `/cc-plan` | Create feature specification |
| `/cc-audit-blueprint` | Validate plan before building |
| `/cc-spike` | Technical research and investigation |

### Execution
| Command | Purpose |
|---------|---------|
| `/cc-daily` | Continue development work |
| `/cc-loop` | Autonomous work loop until complete |
| `/cc-analyze` | Brownfield codebase analysis |

### Quality
| Command | Purpose |
|---------|---------|
| `/cc-review` | Code review |
| `/cc-test` | Test coverage gate |
| `/cc-secure` | Security audit |
| `/cc-assess` | Full codebase audit |
| `/cc-fix` | Bug hunting and fixing |
| `/cc-refactor` | Safe refactoring |
| `/cc-perf` | Performance audit |
| `/cc-deps` | Dependency audit |
| `/cc-debt` | Technical debt tracking |

### Frontend
| Command | Purpose |
|---------|---------|
| `/cc-ui` | UI/UX audit |
| `/cc-terminal` | Terminal UI audit |
| `/cc-seo` | SEO audit |
| `/cc-sync` | Frontend-backend sync check |

### Git & Version Control
| Command | Purpose |
|---------|---------|
| `/cc-commit` | Create well-formatted commit |
| `/cc-pr` | Create pull request |
| `/cc-revert` | Smart git revert |

### Operations
| Command | Purpose |
|---------|---------|
| `/cc-release` | Release checklist |
| `/cc-postmortem` | Incident analysis |
| `/cc-migrate` | Migration planning |
| `/cc-closeout` | Complete milestone |

### Documentation
| Command | Purpose |
|---------|---------|
| `/cc-changelog` | Update changelog |
| `/cc-adr` | Document architecture decisions |
| `/cc-docs` | Generate/update documentation |
| `/cc-onboard` | Create onboarding guide |

### Team
| Command | Purpose |
|---------|---------|
| `/cc-standup` | Generate standup summary |
| `/cc-retro` | Run sprint retrospective |

### Setup
| Command | Purpose |
|---------|---------|
| `/cc-scaffold` | Generate project structure |
| `/cc-scout-skills` | Install skills from registries |
| `/cc-map-project` | Generate project context map |
| `/cc-gitignore` | Update .gitignore for tech stack |
| `/cc-claude-md` | Create/improve project CLAUDE.md |
| `/cc-prompt` | Generate well-structured prompts |

---

## Command Structure

All commands follow this structure:

```yaml
---
name: cc-[command]
description: [What it does]
model: [sonnet|opus|haiku]
argument-hint: [Optional argument description]
---
```

### Content Sections
- `<context>` - Background and purpose
- `<role>` - AI persona for the task
- `<task>` - Main objective
- `<instructions>` - Step-by-step process
- `<output_format>` - Expected output structure
- `<examples>` - Usage examples
- `<rules>` - Constraints and guidelines
- `<error_handling>` - How to handle edge cases

---

## Usage

```bash
# Run a command
/cc-review

# Run with arguments
/cc-spike "WebSocket authentication"

# Chain commands
/cc-plan → /cc-audit-blueprint → /cc-daily → /cc-review
```

---

## Model Selection

| Model | Commands | Use For |
|-------|----------|---------|
| `opus` | secure, assess | Deep analysis, security-critical |
| `sonnet` | Most commands | General development work |
| `haiku` | Quick checks | Fast, lightweight tasks |
