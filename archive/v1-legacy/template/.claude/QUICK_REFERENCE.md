# Quick Reference Card

One-page cheat sheet for Claude Conductor v4.3.

---

## Commands

All commands use the `cc-` namespace to avoid conflicts.

### Planning
| Command | Purpose | Args |
|---------|---------|------|
| `/cc-plan` | Create feature specification | `[feature name]` |
| `/cc-audit-blueprint` | Validate plan before building | `[file] [--ultrathink]` |
| `/cc-adr` | Document architectural decision | `[decision topic]` |
| `/cc-spike` | Technical research | `[topic] [--timebox=Nh]` |
| `/cc-analyze` | Brownfield codebase analysis | `[--conventions] [--architecture]` |

### Development
| Command | Purpose | Args |
|---------|---------|------|
| `/cc-daily` | Continue development work | `[focus area]` |
| `/cc-fix` | Find and fix bugs | `[bug description]` |
| `/cc-refactor` | Safe code refactoring | `[target] [--type=T] [--dry-run]` |
| `/cc-migrate` | Migration planning | `[target version]` |
| `/cc-loop` | Autonomous work loop | `[task] [--max-iterations=N] [--swarm] [--workers=N]` |
| `/cc-revert` | Smart git revert | `[commit/feature] [--preview]` |

### Quality
| Command | Purpose | Args |
|---------|---------|------|
| `/cc-review` | Code review | `[path] [--deep] [--security]` |
| `/cc-test` | Test coverage gate | `[path] [--coverage=N]` |
| `/cc-secure` | Security audit (Opus) | `[scope] [--ultrathink]` |
| `/cc-assess` | Full codebase audit (Opus) | `[scope] [--ultrathink]` |
| `/cc-perf` | Performance audit | `[scope] [--web] [--api] [--db]` |
| `/cc-deps` | Dependency audit | `[--security] [--outdated]` |

### UI/UX & Frontend
| Command | Purpose | Args |
|---------|---------|------|
| `/cc-ui` | UI/UX audit | `[component] [--accessibility]` |
| `/cc-terminal` | Terminal UI audit | `[command] [--demo]` |
| `/cc-seo` | SEO audit | `[page] [--technical]` |
| `/cc-sync` | Frontend-backend sync check | `[feature]` |

### Operations
| Command | Purpose | Args |
|---------|---------|------|
| `/cc-release` | Release checklist | `[version] [--dry-run]` |
| `/cc-debt` | Technical debt tracker | `[category] [--severity=N]` |
| `/cc-postmortem` | Incident analysis | `[incident]` |
| `/cc-closeout` | Complete milestone | `[milestone]` |

### Git & Workflow
| Command | Purpose | Args |
|---------|---------|------|
| `/cc-commit` | Create well-formatted commit | — |
| `/cc-pr` | Create pull request | — |
| `/cc-standup` | Generate standup summary | — |
| `/cc-retro` | Run sprint retrospective | — |
| `/cc-changelog` | Update changelog | — |

### Documentation & Setup
| Command | Purpose | Args |
|---------|---------|------|
| `/cc-onboard` | Create onboarding docs | `[role]` |
| `/cc-docs` | Generate documentation | — |
| `/cc-scaffold` | Generate project structure | — |
| `/cc-scout-skills` | Multi-registry resource discovery | `[--registry=X] [--type=Y] [--auto]` |
| `/cc-map-project` | Generate project context | `[--refresh]` |
| `/cc-gitignore` | Update .gitignore | `[technology]` |
| `/cc-claude-md` | Create/improve CLAUDE.md | `[--refresh]` |

---

## Patterns

Load architecture patterns with `@patterns/[name]`:

| Pattern | Category | Use When |
|---------|----------|----------|
| `@patterns/repository` | Architecture | Data access layer |
| `@patterns/service-layer` | Architecture | Business logic |
| `@patterns/retry-with-backoff` | Resilience | Transient failures |
| `@patterns/circuit-breaker` | Resilience | Cascade prevention |
| `@patterns/error-boundary` | Error Handling | Contain failures |
| `@patterns/pagination` | API | Large datasets |
| `@patterns/strategy` | Behavioral | Swap algorithms |
| `@patterns/feature-flag` | Operations | Gradual rollout |

---

## Snippets

Request code with `snippet:[name]`:

| Snippet | Language | Category |
|---------|----------|----------|
| `snippet:express-route` | TypeScript | API |
| `snippet:react-component` | TypeScript | React |
| `snippet:jest-test` | TypeScript | Testing |
| `snippet:dockerfile` | Docker | DevOps |
| `snippet:error-class` | TypeScript | Utility |

---

## Rules

Load topic-specific guidance with `@rules/[name]`:

| Rule | What It Covers |
|------|----------------|
| `@rules/security` | OWASP Top 10, auth, secrets, input validation |
| `@rules/testing` | Coverage standards, TDD, mocking, naming |
| `@rules/git-workflow` | Commits, branches, PRs, merge strategies |
| `@rules/documentation` | README, changelog, comments, ADRs |
| `@rules/code-quality` | Complexity limits, naming, dependencies |
| `@rules/api-design` | REST, status codes, versioning, pagination |
| `@rules/error-handling` | Error hierarchy, logging, recovery |
| `@rules/ui-ux-design` | Spacing, typography, accessibility |
| `@rules/terminal-ui` | Progress, colors, tables, error messages |

---

## Agents

Spawn specialized agents for focused tasks:

| Agent | Model | Expertise |
|-------|-------|-----------|
| `code-reviewer` | Sonnet | Quality, patterns, test coverage |
| `security-analyst` | Opus | OWASP, STRIDE, vulnerabilities |
| `test-engineer` | Sonnet | Coverage, mocks, TDD |
| `documentation-writer` | Sonnet | README, API docs, guides |
| `researcher` | Sonnet | Tech research, evaluations |
| `ui-ux-expert` | Sonnet | Modern UI, accessibility |
| `terminal-ui-expert` | Sonnet | CLI polish, spinners, colors |
| `seo-expert` | Sonnet | Meta tags, structured data |

**Usage:** "Spawn code-reviewer agent to review the auth module"

---

## Severity Levels

| Level | Meaning | Action |
|-------|---------|--------|
| **S0** | Critical — Blocker, security, data loss | Fix immediately |
| **S1** | High — Major functionality broken | Fix before proceeding |
| **S2** | Medium — Degraded but functional | Fix soon |
| **S3** | Low — Minor, polish | Fix when convenient |

---

## Model Routing

| Task Type | Model | Why |
|-----------|-------|-----|
| Simple queries, formatting | Haiku | Fast, cheap |
| Code review, implementation | Sonnet | Balanced |
| Security, architecture, planning | Opus | Deep reasoning |

---

## Quick Workflows

### New Feature
```
/cc-plan user authentication    # Create spec
/cc-audit-blueprint             # Validate plan
/cc-daily                       # Start building
/cc-review                      # Self-review
/cc-test                        # Verify coverage
/cc-release patch               # Ship it
```

### Bug Fix
```
/cc-fix login timeout           # Investigate and fix
/cc-test src/auth               # Verify fix
/cc-review                      # Self-review
```

### Security Audit
```
/cc-secure --ultrathink         # Deep security analysis
/cc-deps --security             # Check dependencies
```

### UI Polish
```
/cc-ui --accessibility          # Check accessibility
/cc-seo                         # Check SEO
/cc-perf --web                  # Check web performance
```

### Brownfield Project
```
/cc-analyze                     # Detect existing patterns
/cc-claude-md                   # Generate project CLAUDE.md
```

### Smart Revert
```
/cc-revert abc123 --preview     # Preview revert
/cc-revert feature-auth         # Revert entire feature
/cc-revert "last 2 hours"       # Revert time window
```

### Swarm Mode (v4.1)
```
/cc-loop --swarm "review API"   # Parallel workers
/cc-loop --swarm --workers=5    # Custom worker count
```

---

## Swarm Orchestration (v4.1)

### When to Use Swarm Mode
| Scenario | Mode | Why |
|----------|------|-----|
| Many independent reviews | `--swarm` | Parallel execution |
| Sequential pipeline | Standard | Dependencies matter |
| >5 independent tasks | `--swarm` | Maximum parallelism |
| Files share concerns | Standard | Avoid conflicts |

### Task Dependencies
```markdown
| ID | Task | Blocked By | Blocks |
| T001 | Design schema | — | T002, T003 |
| T002 | Build service | T001 | T004 |
| T003 | Build adapter | T001 | T004 |
| T004 | Tests | T002, T003 | — |
```
When T001 completes → T002, T003 auto-unblock.

### Plan Approval Triggers
- Schema/database changes
- Breaking API changes
- Security configuration changes
- Core dependency updates

---

## Project Files

| File | Purpose | Update When |
|------|---------|-------------|
| `STATUS.md` | Current state | Every session |
| `CHANGELOG.md` | Version history | Every release |
| `KNOWN_ISSUES.md` | Tracked limitations | As discovered |
| `.claude/context/PROJECT_MAP.md` | Project structure | Major changes |
| `.claude/context/PROJECT_PROFILE.md` | Brownfield analysis | After /cc-analyze |

---

## MCP Servers

External integrations via Model Context Protocol.

### Configuration Locations
| Location | Scope |
|----------|-------|
| `~/.claude/settings.json` | System-wide |
| `.mcp.json` | Project root (common) |
| `.claude/settings.json` | Project-specific |

### Common Servers
| Server | Purpose | Tools Prefix |
|--------|---------|--------------|
| `context7` | Library docs | `mcp__context7__*` |
| `memory` | Persistence | `mcp__memory__*` |
| `github` | GitHub API | `mcp__github__*` |
| `postgres` | Database | `mcp__postgres__*` |

**Tip:** Check `.mcp.json` in project root for project-specific servers.

---

## Plugins

Extend Claude Code with additional capabilities.

### Installation

```bash
claude plugin marketplace add <repo>
claude plugin install <plugin-name>
claude plugin list
```

### Supermemory (Persistent Memory)

```bash
# Set API key (Windows PowerShell)
[Environment]::SetEnvironmentVariable("SUPERMEMORY_CC_API_KEY", "sm_...", "User")

# Set API key (macOS/Linux)
echo 'export SUPERMEMORY_CC_API_KEY="sm_..."' >> ~/.zshrc

# Install
claude plugin marketplace add supermemoryai/claude-supermemory
claude plugin install claude-supermemory

# Index codebase (inside Claude Code)
/claude-supermemory:index
```

| Feature | What It Does |
|---------|--------------|
| Context Injection | Loads memories on session start |
| Auto Capture | Saves conversations automatically |
| Super Search | Search past work and sessions |

---

## Skill Registries (v4.3)

Multi-registry discovery system for skills, agents, commands, hooks, and MCPs.

### Available Registries

| Registry | Focus | Resources | Priority |
|----------|-------|-----------|----------|
| **aitmpl.com** | Claude Code-specific | Skills, Agents, Commands, Hooks, MCPs | 1 (primary) |
| **skills.sh** | Multi-agent ecosystem | 33,000+ skills | 2 (secondary) |

### Automation Levels

| What | Automation |
|------|------------|
| Tech detection | AUTOMATED |
| Registry querying | AUTOMATED |
| Scoring & ranking | AUTOMATED |
| Deduplication | AUTOMATED |
| Install (≥80 score) | REQUIRES CONFIRMATION |
| Install (50-79 score) | USER SELECTS |
| API key configuration | MANUAL |
| MCP activation | MANUAL (restart required) |

### Quick Commands

```bash
# Automated discovery
/cc-scout-skills                    # Full discovery
/cc-scout-skills --auto             # Auto-install high-confidence

# Manual registry commands
npx claude-code-templates search "react"        # aitmpl.com
npx skills find "react"                         # skills.sh

# Install from specific registry
npx claude-code-templates install aws-stack     # aitmpl.com
npx skills add "vercel-labs/react" --agent claude-code -y  # skills.sh
```

### Scoring Algorithm

| Factor | Weight |
|--------|--------|
| Technology match | 30% |
| Source reputation | 25% |
| Specificity (Claude-specific) | 20% |
| Completeness (agents+hooks) | 15% |
| Recency | 10% |

**Configuration:** `.claude/config/registries.md`

---

## Getting Help

```
/help                        # General help
```

Documentation:
- `SETUP.md` — Initial setup guide
- `CONFIGURATION.md` — All settings
- `TROUBLESHOOTING.md` — Common issues
- `MCP_SERVERS.md` — MCP setup
- `patterns/_index.md` — Pattern library
- `snippets/_index.md` — Snippet registry
