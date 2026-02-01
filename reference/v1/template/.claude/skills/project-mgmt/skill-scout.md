---
name: skill-scout
description: Find and install the best skills, agents, commands, hooks, and MCPs from multiple registries
version: "2.0.0"
model: sonnet
triggers:
  - "install skills"
  - "find skills"
  - "scout skills"
  - "project setup"
  - "init project"
  - "skills.sh"
  - "aitmpl"
tags: ["project-mgmt", "discovery", "multi-registry"]
---

# Skill Scout v2.0

Automatically discover and install the best resources from multiple registries for your project.

## Description

Multi-registry skill discovery system that searches skills.sh, aitmpl.com, and future sources to find the optimal skills, agents, commands, hooks, MCPs, and settings for your tech stack.

## Trigger

This skill activates when:
- User runs `/cc-scout-skills` command
- User asks to "find skills" or "install skills"
- Project is initialized with `claude --init` (if hook configured)
- User mentions "skills.sh" or "aitmpl"

---

## Supported Registries

| Registry | Focus | Resources | Priority |
|----------|-------|-----------|----------|
| **aitmpl.com** | Claude Code-specific | Skills, Agents, Commands, Hooks, MCPs, Settings | 1 (primary) |
| **skills.sh** | Multi-agent ecosystem | Skills (33,000+), some Agents | 2 (secondary) |

See `.claude/config/registries.md` for full registry configuration.

---

## Behavior

### Phase 1: Detect Tech Stack

Read project files to identify technologies:

```
package.json       → Node.js, frameworks, libraries
requirements.txt   → Python packages
pyproject.toml     → Modern Python
go.mod             → Go modules
Cargo.toml         → Rust crates
Gemfile            → Ruby gems
pom.xml            → Java/Maven
composer.json      → PHP
Dockerfile         → Container tech
.github/workflows/ → CI/CD
terraform/         → Infrastructure
.env, config/      → Services (AWS, Stripe, etc.)
```

### Phase 2: Query All Registries

Search each enabled registry in parallel:

**aitmpl.com (Primary):**
```bash
# List available by type
npx claude-code-templates list --type=skills
npx claude-code-templates list --type=agents
npx claude-code-templates list --type=commands

# Search by technology
npx claude-code-templates search "<technology>"
```

**skills.sh (Secondary):**
```bash
# Search by technology
npx skills find "<technology>"

# Get details
npx skills info "<owner/repo>"
```

### Phase 3: Score and Rank Results

Each discovered resource is scored (0-100):

| Factor | Weight | Scoring |
|--------|--------|---------|
| **Technology Match** | 30% | Exact=30, Partial=15, Related=5 |
| **Source Reputation** | 25% | Official=25, Trusted=20, Community=10 |
| **Specificity** | 20% | Claude Code-specific=20, Multi-agent=10 |
| **Completeness** | 15% | Full stack (agents+hooks+MCPs)=15, Skills only=5 |
| **Recency** | 10% | <30 days=10, <90 days=7, <1 year=3 |

**Score Tiers:**
- **Auto-install** (≥80): High confidence, install without asking
- **Recommend** (50-79): Good match, ask user to confirm
- **Mention** (30-49): Available but low confidence
- **Skip** (<30): Poor match, don't show

### Phase 4: Deduplicate Across Registries

When the same technology appears in multiple registries:

1. **Prefer Claude Code-specific** — aitmpl.com over skills.sh for same tech
2. **Prefer complete stacks** — Templates with agents+hooks over skills only
3. **Prefer official sources** — anthropic/*, vercel-labs/* rank higher
4. **Show alternatives** — Note when good options exist in both

### Phase 5: Present Recommendations

Organize by resource type and confidence:

```markdown
## Recommended Resources

### Skills (Auto-install: Score ≥80)
| Skill | Source | Score | Technology |
|-------|--------|-------|------------|
| react-patterns | aitmpl.com | 92 | React |
| nextjs-app-router | skills.sh/vercel-labs | 88 | Next.js |

### Skills (Recommended: Score 50-79)
| Skill | Source | Score | Technology |
|-------|--------|-------|------------|
| tailwind-patterns | skills.sh | 72 | Tailwind |

### Agents
| Agent | Source | Score | Purpose |
|-------|--------|-------|---------|
| security-auditor | aitmpl.com | 85 | Security analysis |

### Hooks & MCPs
| Resource | Type | Source | Purpose |
|----------|------|--------|---------|
| pre-commit-lint | Hook | aitmpl.com | Auto-linting |
| postgres-mcp | MCP | aitmpl.com | Database tools |
```

### Phase 6: Install Selected

Install from appropriate registry:

**From aitmpl.com:**
```bash
npx claude-code-templates install <template-name>
```

**From skills.sh:**
```bash
npx skills add "<owner/repo@skill>" --agent claude-code -y
```

### Phase 7: Post-Install Processing

Ensure all installed resources are v2.0 compatible:

1. **Check for frontmatter** — Add if missing
2. **Validate structure** — Ensure required fields present
3. **Update project CLAUDE.md** — Add to Installed Resources section
4. **Record source** — Tag with registry origin for updates

---

## Resource Type Routing

| Resource | Primary Source | Fallback | Notes |
|----------|---------------|----------|-------|
| Skills | aitmpl.com | skills.sh | skills.sh has volume |
| Agents | aitmpl.com | skills.sh | aitmpl.com has more |
| Commands | aitmpl.com | — | aitmpl.com only |
| Hooks | aitmpl.com | — | aitmpl.com only |
| MCPs | aitmpl.com | — | aitmpl.com only |
| Settings | aitmpl.com | — | aitmpl.com only |

---

## Technology-Specific Routing

Some technologies have preferred sources:

| Technology | Preferred Source | Why |
|------------|-----------------|-----|
| React/Next.js | skills.sh (vercel-labs) | Official Vercel skills |
| AWS | aitmpl.com (aws-stack) | Complete stack with MCPs |
| Stripe | aitmpl.com | Full integration template |
| PostgreSQL/Neon | aitmpl.com | Database MCP included |
| Scientific/Research | aitmpl.com | 139+ specialized skills |
| General web dev | skills.sh | Largest skill library |

---

## Trusted Sources

### skills.sh Trusted Sources
- `anthropic/*` — Official Anthropic
- `vercel-labs/*` — Vercel ecosystem
- `google-labs-code/*` — Google tools
- `aws/*` — AWS patterns
- `stripe/*` — Stripe integration
- `prisma/*` — Prisma ORM

### aitmpl.com Trusted Templates
- `aws-stack` — Complete AWS integration
- `stripe-integration` — Payment processing
- `security-auditor` — Security agent
- `scientific-computing` — Research tools
- `neon-postgres` — Database patterns

---

## Commands Reference

### Search Commands

```bash
# aitmpl.com
npx claude-code-templates list                    # List all
npx claude-code-templates list --type=skills      # List skills
npx claude-code-templates list --type=agents      # List agents
npx claude-code-templates search "react"          # Search

# skills.sh
npx skills find "react"                           # Search
npx skills info "vercel-labs/react"               # Details
npx skills list --installed                       # Show installed
```

### Install Commands

```bash
# aitmpl.com
npx claude-code-templates install aws-stack
npx claude-code-templates install security-auditor

# skills.sh
npx skills add "vercel-labs/react" --agent claude-code -y
npx skills add "anthropic/claude-patterns" --agent claude-code -y
```

---

## Post-Install Frontmatter Generation

If downloaded skill lacks YAML frontmatter, generate it:

```yaml
---
name: "[Extracted from H1 or filename]"
description: "[First paragraph]"
version: "1.0.0"
triggers:
  - "[from 'Triggers on:' line]"
model: "sonnet"
tags: ["external", "[source-registry]", "[technology]"]
source:
  registry: "[skills.sh|aitmpl.com]"
  identifier: "[owner/repo or template-name]"
  installed: "[ISO date]"
---
```

---

## Idempotency

Safe to run multiple times:
- Skips already-installed resources
- Updates (not duplicates) recommendations
- Preserves user customizations
- No destructive operations

---

## Configuration

### Environment Variables

```bash
SCOUT_DISABLE_REGISTRIES="skills.sh"  # Disable specific registries
SCOUT_REGISTRY_TIMEOUT=30000          # Query timeout (ms)
SCOUT_AUTO_INSTALL_THRESHOLD=80       # Auto-install score threshold
SCOUT_VERBOSE=true                    # Enable verbose output
```

### Per-Project Settings

In `.claude/settings.local.json`:

```json
{
  "scout": {
    "registries": {
      "aitmpl.com": { "enabled": true, "priority": 1 },
      "skills.sh": { "enabled": true, "priority": 2 }
    },
    "autoInstallThreshold": 80,
    "recommendThreshold": 50,
    "trustedSources": ["anthropic/*", "vercel-labs/*"]
  }
}
```

---

## Example Output

```
# Skill Scout Report

**Project:** my-nextjs-app
**Technologies Detected:** 8
**Registries Searched:** 2

---

## Detected Tech Stack

- **Languages:** TypeScript, JavaScript
- **Frameworks:** Next.js 14, React 18, Tailwind CSS
- **Database:** PostgreSQL (Neon)
- **Services:** Stripe, AWS S3
- **DevOps:** Docker, GitHub Actions

---

## Recommended Resources

### Auto-Install (Score ≥80)

| Resource | Type | Source | Score | Technology |
|----------|------|--------|-------|------------|
| nextjs-app-router | Skill | skills.sh/vercel-labs | 92 | Next.js |
| react-patterns | Skill | aitmpl.com | 88 | React |
| stripe-integration | Stack | aitmpl.com | 95 | Stripe |
| neon-postgres | Stack | aitmpl.com | 90 | PostgreSQL |

### Recommended (Score 50-79)

| Resource | Type | Source | Score | Technology |
|----------|------|--------|-------|------------|
| tailwind-patterns | Skill | skills.sh | 72 | Tailwind |
| typescript-strict | Skill | skills.sh | 68 | TypeScript |
| docker-node | Skill | skills.sh | 65 | Docker |

### Available Agents

| Agent | Source | Score | Purpose |
|-------|--------|-------|---------|
| security-auditor | aitmpl.com | 85 | Security analysis |
| code-reviewer | aitmpl.com | 80 | Code review |

### Available Hooks & MCPs

| Resource | Type | Source | Purpose |
|----------|------|--------|---------|
| stripe-mcp | MCP | aitmpl.com | Stripe API tools |
| neon-mcp | MCP | aitmpl.com | Database tools |
| pre-commit-lint | Hook | aitmpl.com | Auto-linting |

---

## Installation

**Install all auto-install resources?** (yes/no/select)

> yes

### Installation Results

- ✓ nextjs-app-router installed from skills.sh
- ✓ react-patterns installed from aitmpl.com
- ✓ stripe-integration installed from aitmpl.com
- ✓ neon-postgres installed from aitmpl.com

### Project CLAUDE.md Updated

Added to `## Installed Resources` section.

---

## Next Steps

1. Configure Stripe API key in `.env`
2. Set up Neon database connection
3. Review security-auditor agent for first audit
```

---

## See Also

- `.claude/config/registries.md` — Registry configuration
- `.claude/skills/collaboration/template-registry.md` — Manual registry browsing
- `/cc-analyze` — Brownfield codebase analysis
