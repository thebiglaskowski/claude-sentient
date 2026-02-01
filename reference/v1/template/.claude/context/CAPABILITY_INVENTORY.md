# Capability Inventory

**A complete inventory of all tools, commands, agents, skills, patterns, snippets, and hooks available to the autonomous development system.**

This file should be loaded at session start to ensure full awareness of capabilities.

---

## Quick Reference

| Category | Count | Purpose |
|----------|-------|---------|
| Commands | 37 | Invoke specific workflows (`/cc-*`) |
| Agents | 15 | Specialized expert analysis |
| Skills | 58 | Auto-loading behaviors |
| Rules | 13 | Topic-specific standards |
| Patterns | 15+ | Reusable architecture patterns (`@patterns/*`) |
| Snippets | 9 | Indexed code templates (`snippet:*`) |
| Hooks | 12 | Lifecycle automation |
| MCP Servers | Variable | External integrations (check `.mcp.json` and `.claude/settings.json`) |

---

## Commands

All commands use the `cc-` namespace to avoid conflicts with other tools.

### Planning Commands
| Command | Purpose | Use When |
|---------|---------|----------|
| `/cc-plan` | Create feature specification | Starting new feature |
| `/cc-audit-blueprint` | Validate plan before building | Plan complete, need review |
| `/cc-spike` | Technical research | Unknown territory |
| `/cc-analyze` | Brownfield codebase analysis | Existing project |

### Execution Commands
| Command | Purpose | Use When |
|---------|---------|----------|
| `/cc-daily` | Continue development work | Ongoing work |
| `/cc-loop` | Autonomous work loop | Need sustained execution |
| `/cc-scaffold` | Generate project structure | New project/module |
| `/cc-revert` | Smart git revert | Need to undo work |

### Quality Commands
| Command | Purpose | Use When |
|---------|---------|----------|
| `/cc-review` | Code review | Before merge |
| `/cc-test` | Test coverage gate | Coverage gaps |
| `/cc-secure` | Security audit | Security concerns |
| `/cc-assess` | Full codebase audit | Periodic review |

### Performance Commands
| Command | Purpose | Use When |
|---------|---------|----------|
| `/cc-perf` | Performance audit | Speed issues |
| `/cc-deps` | Dependency audit | Update dependencies |
| `/cc-debt` | Track technical debt | Debt accumulating |

### Refactoring Commands
| Command | Purpose | Use When |
|---------|---------|----------|
| `/cc-refactor` | Safe refactoring | Code smells |
| `/cc-fix` | Bug hunting | Bugs reported |

### UI/UX Commands
| Command | Purpose | Use When |
|---------|---------|----------|
| `/cc-ui` | UI/UX audit | Web interface issues |
| `/cc-terminal` | Terminal UI audit | CLI polish needed |
| `/cc-seo` | SEO audit | SEO improvements |
| `/cc-sync` | Frontend-backend sync | Integration issues |

### Operations Commands
| Command | Purpose | Use When |
|---------|---------|----------|
| `/cc-release` | Release checklist | Shipping |
| `/cc-postmortem` | Incident analysis | After incident |
| `/cc-migrate` | Migration planning | Schema/API changes |
| `/cc-closeout` | Complete milestone | Finishing phase |

### Git Commands
| Command | Purpose | Use When |
|---------|---------|----------|
| `/cc-commit` | Create commit | Changes ready |
| `/cc-pr` | Create pull request | Feature complete |
| `/cc-standup` | Generate standup | Daily sync |
| `/cc-retro` | Sprint retrospective | End of sprint |
| `/cc-changelog` | Update changelog | Version bump |

### Documentation Commands
| Command | Purpose | Use When |
|---------|---------|----------|
| `/cc-adr` | Document decisions | Architecture decision |
| `/cc-onboard` | Create onboarding docs | New team member |
| `/cc-docs` | Generate documentation | Docs outdated |
| `/cc-claude-md` | Create project CLAUDE.md | New project |
| `/cc-gitignore` | Update .gitignore | Tech stack changes |
| `/cc-map-project` | Generate project map | Need overview |
| `/cc-scout-skills` | Install skills | New project setup |

---

## Pattern Library

Reusable architecture patterns loaded with `@patterns/[name]`:

### Architecture Patterns
| Pattern | Purpose | Use When |
|---------|---------|----------|
| `@patterns/repository` | Data access abstraction | Database operations |
| `@patterns/service-layer` | Business logic organization | Complex domain logic |
| `@patterns/cqrs` | Command-Query separation | Read/write optimization |
| `@patterns/clean-architecture` | Dependency inversion | Large applications |

### Resilience Patterns
| Pattern | Purpose | Use When |
|---------|---------|----------|
| `@patterns/retry-with-backoff` | Handle transient failures | External API calls |
| `@patterns/circuit-breaker` | Prevent cascade failures | Service dependencies |
| `@patterns/bulkhead` | Isolate failures | Critical services |

### Error Handling Patterns
| Pattern | Purpose | Use When |
|---------|---------|----------|
| `@patterns/error-boundary` | Contain failures | React/Vue/Node apps |
| `@patterns/result-type` | Explicit error handling | Functional style |

### API Patterns
| Pattern | Purpose | Use When |
|---------|---------|----------|
| `@patterns/pagination` | Large dataset handling | List endpoints |
| `@patterns/rate-limiting` | Protect resources | Public APIs |

### Behavioral Patterns
| Pattern | Purpose | Use When |
|---------|---------|----------|
| `@patterns/strategy` | Interchangeable algorithms | Multiple approaches |
| `@patterns/observer` | Event notification | Decoupled updates |
| `@patterns/state-machine` | State management | Complex workflows |

### Testing Patterns
| Pattern | Purpose | Use When |
|---------|---------|----------|
| `@patterns/arrange-act-assert` | Test structure | Unit/integration tests |
| `@patterns/test-doubles` | Mocking strategy | Isolated testing |

### Operations Patterns
| Pattern | Purpose | Use When |
|---------|---------|----------|
| `@patterns/feature-flag` | Gradual rollout | New features |
| `@patterns/blue-green` | Zero-downtime deploy | Production releases |

---

## Snippet Registry

Indexed code templates requested with `snippet:[name]`:

### API Snippets
| Snippet | Language | Use When |
|---------|----------|----------|
| `snippet:express-route` | TypeScript | Express endpoints |
| `snippet:fastapi-endpoint` | Python | FastAPI routes |
| `snippet:go-handler` | Go | Go HTTP handlers |

### React Snippets
| Snippet | Language | Use When |
|---------|----------|----------|
| `snippet:react-component` | TypeScript | React components |
| `snippet:react-hook` | TypeScript | Custom hooks |
| `snippet:react-context` | TypeScript | Context providers |

### Testing Snippets
| Snippet | Language | Use When |
|---------|----------|----------|
| `snippet:jest-test` | TypeScript | Jest tests |
| `snippet:pytest-test` | Python | Pytest tests |
| `snippet:go-test` | Go | Go tests |

### Database Snippets
| Snippet | Language | Use When |
|---------|----------|----------|
| `snippet:prisma-model` | Prisma | Database models |
| `snippet:migration` | SQL | Schema migrations |

### DevOps Snippets
| Snippet | Language | Use When |
|---------|----------|----------|
| `snippet:dockerfile` | Docker | Container builds |
| `snippet:github-action` | YAML | CI/CD workflows |

### Utility Snippets
| Snippet | Language | Use When |
|---------|----------|----------|
| `snippet:error-class` | TypeScript | Custom errors |
| `snippet:logger` | TypeScript | Logging setup |
| `snippet:config` | TypeScript | Configuration |

---

## Agents

### Code Quality Agents
| Agent | Model | Specialty | Spawn When |
|-------|-------|-----------|------------|
| `code-reviewer` | sonnet | Code review, patterns | PR review, code smells |
| `test-engineer` | sonnet | Tests, coverage | Coverage < 80%, test gaps |
| `performance-optimizer` | sonnet | Speed, efficiency | Slow code, optimization |

### Security Agents
| Agent | Model | Specialty | Spawn When |
|-------|-------|-----------|------------|
| `security-analyst` | opus | Vulnerabilities, auth | Security audit, auth work |

### Frontend Agents
| Agent | Model | Specialty | Spawn When |
|-------|-------|-----------|------------|
| `ui-ux-expert` | sonnet | Web design, UX | UI issues, design work |
| `terminal-ui-expert` | sonnet | CLI polish | Terminal app polish |
| `accessibility-expert` | sonnet | WCAG, a11y | Accessibility audit |
| `seo-expert` | sonnet | Search optimization | SEO work |

### Backend Agents
| Agent | Model | Specialty | Spawn When |
|-------|-------|-----------|------------|
| `api-designer` | sonnet | REST, GraphQL | API design |
| `database-expert` | sonnet | Schema, queries | DB optimization |
| `devops-engineer` | sonnet | CI/CD, infra | Pipeline issues |

### Research Agents
| Agent | Model | Specialty | Spawn When |
|-------|-------|-----------|------------|
| `researcher` | sonnet | Investigation | Unknown problem |
| `documentation-writer` | sonnet | Docs, guides | Docs needed |
| `migration-specialist` | sonnet | Migrations | Breaking changes |
| `prompt-engineer` | sonnet | AI prompts | Prompt optimization |

---

## Skills (Key Orchestration)

| Skill | Purpose | Triggers |
|-------|---------|----------|
| `task-orchestrator` | Classify task, load context | Session start |
| `autonomous-loop` | Iterate until complete | `/cc-loop`, "keep working" |
| `meta-cognition` | Self-aware decisions | "reassess", "what tools" |
| `definition-of-done` | Completion criteria | Work completion |
| `queue-manager` | Manage work queue | Task management |
| `smart-context-v3` | Load relevant context | Context needed |
| `error-classifier` | Classify errors | Error occurs |
| `parallel-agents` | Coordinate agents | Multiple agents |
| `browser-verification` | Verify UI changes | UI work |
| `session-memory` | Cross-session memory | Session start |
| `context-budget-monitor` | Prevent context bloat | Heavy operations |
| `parallel-task-decomposer` | Break into parallel units | Complex tasks |
| `decision-logger` | Capture decisions | Choices made |
| `commit-checkpoint` | Create verified commits | Feature complete |
| `brownfield-analyzer` | Detect existing patterns | Existing codebase |

---

## Rules

| Rule | Topic | Load When |
|------|-------|-----------|
| `@rules/security` | OWASP, auth, secrets | Security work |
| `@rules/testing` | TDD, coverage, mocks | Test work |
| `@rules/git-workflow` | Commits, PRs | Git operations |
| `@rules/documentation` | Docs standards | Doc work |
| `@rules/code-quality` | Complexity, naming | Code review |
| `@rules/api-design` | REST, versioning | API work |
| `@rules/error-handling` | Errors, recovery | Error handling |
| `@rules/ui-ux-design` | Web UI standards | UI work |
| `@rules/terminal-ui` | CLI standards | CLI work |
| `@rules/performance` | Optimization | Perf work |
| `@rules/database` | Schema, queries | DB work |
| `@rules/logging` | Log standards | Logging |
| `@rules/prompt-engineering` | AI prompts | Prompt work |

---

## Hooks

| Hook | Event | Purpose |
|------|-------|---------|
| `setup-init` | Setup | One-time project init |
| `session-start` | SessionStart | Load session state |
| `context-injector` | UserPromptSubmit | Inject relevant context |
| `bash-auto-approve` | PreToolUse (Bash) | Auto-approve safe commands |
| `file-validator` | PreToolUse (Write/Edit) | Validate file changes |
| `post-edit` | PostToolUse (Edit/Write) | Format and lint |
| `error-recovery` | PostToolUseFailure | Classify and recover |
| `agent-tracker` | SubagentStart | Track parallel agents |
| `agent-synthesizer` | SubagentStop | Merge agent results |
| `pre-compact` | PreCompact | Backup before compaction |
| `dod-verifier` | Stop | Verify Definition of Done |
| `session-end` | SessionEnd | Save metrics, cleanup |

---

## MCP Servers

MCP (Model Context Protocol) servers extend Claude Code with external tools and services. Available servers vary by project and user configuration.

### Discovering Available MCP Servers

MCP servers are configured in multiple locations (checked in order):

| Location | Scope | Priority |
|----------|-------|----------|
| `~/.claude/settings.json` | System-wide (all projects) | Lower |
| `.claude/settings.json` | Project-specific | Higher |
| `.mcp.json` | Project root (alternative) | Higher |

**Important:** The `.mcp.json` file may live in the **project root**, not inside `.claude/`. Always check both locations.

### How to Check Available MCP Servers

At session start, check what MCP tools are available:

1. **Look for configuration files:**
   ```
   Check: .mcp.json (project root)
   Check: .claude/settings.json (mcpServers key)
   ```

2. **Available tools appear with prefix:** `mcp__[server-name]__[tool]`

3. **Common server detection:**
   - If `mcp__context7__*` tools exist → Context7 available
   - If `mcp__memory__*` tools exist → Memory server available
   - If `mcp__github__*` tools exist → GitHub server available
   - If `mcp__postgres__*` or `mcp__sqlite__*` tools exist → Database access available

### Common MCP Servers

| Server | Purpose | Tools Provided | Use When |
|--------|---------|----------------|----------|
| `context7` | Documentation lookup | `resolve-library-id`, `query-docs` | Need current library docs |
| `memory` | Persistent storage | `store`, `retrieve`, `search` | Cross-session memory |
| `github` | GitHub API | Issues, PRs, repos | GitHub operations |
| `postgres` | PostgreSQL queries | `query`, `schema` | Database work |
| `sqlite` | SQLite queries | `query`, `schema` | Local database |
| `filesystem` | Extended file access | `read`, `write`, `list` | Files outside project |
| `puppeteer` | Browser automation | Screenshots, scraping | Web testing |

### Project-Specific MCP Servers

Projects may have custom MCP servers configured. When starting work on a project:

1. **Check for `.mcp.json` in project root** — This file often contains project-specific servers (databases, custom APIs)
2. **Check `.claude/settings.json`** — May contain project-specific overrides
3. **Note available tools** — Any `mcp__*` tools in your toolkit indicate active servers

### Using MCP Servers

```
# Context7 - Get up-to-date docs
"Use context7 to look up React hooks documentation"

# Memory - Store/retrieve information
"Remember that this project uses PostgreSQL 15"

# Database - Query directly
"Show me the users table schema"
"Query recent orders"
```

### Decision Matrix for MCP

| Situation | Check For | Use |
|-----------|-----------|-----|
| Need current library docs | `context7` | `mcp__context7__query-docs` |
| Need to remember something | `memory` | `mcp__memory__store` |
| GitHub operations | `github` | `mcp__github__*` |
| Database queries | `postgres`/`sqlite` | `mcp__[db]__query` |
| Project-specific tools | Check `.mcp.json` | Project's custom servers |

---

## Decision Matrix

### Situation → Best Tool

| Situation | Primary Tool | Patterns/Snippets | Backup |
|-----------|--------------|-------------------|--------|
| New project | `/cc-scaffold` → `/cc-claude-md` | — | `/cc-map-project` |
| Existing project | `/cc-analyze` | — | `/cc-map-project` |
| Need to understand code | `/cc-assess` | — | `researcher` agent |
| Feature work, clear plan | `/cc-loop` | Surface relevant patterns | `/cc-daily` |
| Feature work, unclear | `/cc-plan` → `/cc-audit-blueprint` | — | `/cc-spike` |
| Tests failing | Focus on tests | `@patterns/arrange-act-assert` | `test-engineer` agent |
| Coverage < 80% | `test-engineer` agent | `snippet:jest-test` | `/cc-test` |
| Security vulnerability | `security-analyst` agent | — | `/cc-secure` |
| Performance issue | `performance-optimizer` | `@patterns/retry-with-backoff` | `/cc-perf` |
| UI looks wrong | `ui-ux-expert` | `snippet:react-component` | `/cc-ui` |
| CLI needs polish | `terminal-ui-expert` | — | `/cc-terminal` |
| DB slow | `database-expert` | `@patterns/repository` | `@rules/database` |
| API work | `api-designer` | `@patterns/pagination`, `snippet:express-route` | `/cc-sync` |
| Docs missing | `documentation-writer` | — | `/cc-docs` |
| Ready to ship | `/cc-release` → `/cc-changelog` | — | `/cc-commit` → `/cc-pr` |
| Need to undo work | `/cc-revert` | — | Manual git revert |
| Incident happened | `/cc-postmortem` | — | Document in ADR |
| Stuck, no progress | Reassess with `meta-cognition` | Check capability inventory | Spawn `researcher` |

---

## Usage

This inventory should be:
1. **Loaded at session start** via `session-start` hook
2. **Referenced by `meta-cognition`** skill for decisions
3. **Consulted when stuck** to find alternative approaches
4. **Updated** when new capabilities are added

The system should ALWAYS be aware of this inventory and actively use it for intelligent decision-making.
