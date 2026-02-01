# Claude Code Project Template

This folder contains a complete `.claude/` configuration for autonomous development with Claude Code.

## Quick Setup

### 1. Copy to Your Project

```bash
# Copy the entire .claude folder to your project root
cp -r template/.claude /path/to/your/project/
```

### 2. Initialize

In your project directory with Claude Code:
```
initialize this project
```

Or manually:
```
/claude-md
/gitignore
/scout-skills
/map-project
```

### 3. Start Working

```
/daily           # Continue development
/loop "task"     # Autonomous work loop
/plan "feature"  # Plan a feature
```

---

## What's Included

### Component Counts (v3.0)

| Component | Count | Location |
|-----------|-------|----------|
| Commands | 35 | `.claude/commands/` |
| Skills | 56 | `.claude/skills/[category]/` |
| Rules | 13 | `.claude/rules/` |
| Agents | 15 | `.claude/agents/` |
| Hooks | 12 | `.claude/hooks/` |

### Directory Structure

```
.claude/
├── CLAUDE.md              # Main configuration and command reference
├── settings.json          # Permissions, hooks, MCP servers
├── _system.md             # Platform architecture documentation
│
├── commands/              # 35 slash commands
│   ├── daily.md           # /daily - continue work
│   ├── loop.md            # /loop - autonomous execution
│   ├── review.md          # /review - code review
│   └── ...
│
├── skills/                # 56 auto-loading skills
│   ├── orchestration/     # Core loop, task management
│   ├── quality/           # DoD, severity levels
│   ├── workflow/          # Pre-commit, pre-merge
│   ├── optimization/      # Context, memory, errors
│   └── ...
│
├── rules/                 # 13 topic-specific standards
│   ├── security.md        # OWASP, auth, secrets
│   ├── testing.md         # Coverage, TDD, mocks
│   ├── api-design.md      # REST, errors, versioning
│   └── ...
│
├── agents/                # 15 specialized experts
│   ├── security-analyst.md
│   ├── code-reviewer.md
│   └── ...
│
├── hooks/                 # 12 lifecycle hooks
│   ├── context-injector.py    # Load relevant context
│   ├── error-recovery.py      # Handle failures
│   ├── agent-tracker.py       # Track parallel agents
│   └── ...
│
└── context/               # Session state
    ├── PROJECT_MAP.md     # Generated project structure
    └── SESSION_HISTORY.md # Cross-session memory
```

---

## Key Features

### Autonomous Loop (v3.0)

The `/loop` command runs 8 phases and 12 quality gates:

```
Phases: CONTEXTUALIZE → ASSESS → PLAN → BUILD → TEST → QUALITY → EVALUATE → RECOVER

Gates: PRE-FLIGHT → LINT → TYPE → UNIT → INTEGRATION → SECURITY →
       PERFORMANCE → BROWSER → ACCESSIBILITY → DOCS → MODERN → DoD
```

### Hook Integration

Hooks automate common workflows:

| Hook | Trigger | Action |
|------|---------|--------|
| `context-injector.py` | User prompt | Load relevant files/rules |
| `bash-auto-approve.py` | Bash command | Auto-approve safe commands |
| `error-recovery.py` | Tool failure | Classify and recover |
| `agent-tracker.py` | Agent spawn | Track parallel execution |
| `dod-verifier.py` | Stop | Verify completion criteria |

### Parallel Agents

Run multiple experts simultaneously:

```
"Run full audit with security-analyst, code-reviewer, test-engineer"
→ Spawns all three agents in parallel
→ agent-synthesizer.py merges results
→ Creates unified work queue
```

---

## Customization

### Add Project-Specific Rules

Create `.claude/rules/my-project.md`:
```markdown
# My Project Rules

## Framework Specifics
- Use Next.js App Router
- Prefer Server Components
- Use Tailwind for styling

## Naming Conventions
...
```

### Add Custom Commands

Create `.claude/commands/my-command.md`:
```markdown
---
name: my-command
description: What it does
---

# My Command

[Instructions for the command]
```

### Configure Hooks

Edit `.claude/settings.json` to add/modify hooks.

---

## Requirements

- Python 3.8+ (for hooks)
- Bash (for shell hooks)
- Node.js (optional, for MCP servers)

---

## Documentation

| Resource | Description |
|----------|-------------|
| `CLAUDE.md` | Main reference and commands |
| `_system.md` | Platform architecture |
| `QUICK_REFERENCE.md` | One-page cheat sheet |
| `CONFIGURATION.md` | Detailed configuration |
| `TROUBLESHOOTING.md` | Common issues |
| `skills/_index.md` | Searchable skill directory |
| `agents/_index.md` | Agent capabilities |
| `rules/_index.md` | Rule descriptions |

---

## Version

**Claude Code on Steroids v3.0**

- 8-phase autonomous loop
- 12 quality gates
- 12 lifecycle hooks
- 15 specialized agents
- 56 auto-loading skills
