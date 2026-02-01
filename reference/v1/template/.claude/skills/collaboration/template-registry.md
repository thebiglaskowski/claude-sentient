---
name: template-registry
description: Browse and manually install resources from community registries
version: "2.0.0"
model: haiku
triggers:
  - "browse templates"
  - "list registries"
  - "manual install"
  - "registry search"
tags: ["collaboration", "discovery", "manual"]
---

# Template Registry Browser

Manually browse and install resources from community registries.

## Relationship to /cc-scout-skills

| Feature | /cc-scout-skills | template-registry |
|---------|------------------|-------------------|
| **Purpose** | Automated discovery | Manual browsing |
| **Tech detection** | Automatic | Manual |
| **Scoring** | Automatic ranking | User judgment |
| **Best for** | Project setup | Exploring options |
| **Automation** | High | Low |

**Use `/cc-scout-skills`** for automated project setup with intelligent recommendations.
**Use this skill** for manual exploration when you want to browse what's available.

---

## Available Registries

### 1. aitmpl.com (Claude Code Templates)

**Priority:** 1 (Primary for Claude Code)
**Focus:** Claude Code-specific complete configurations
**URL:** https://www.aitmpl.com

| Resource Type | Count | Available |
|---------------|-------|-----------|
| Skills | 200+ | Yes |
| Agents | 48+ | Yes |
| Commands | 21+ | Yes |
| Hooks | Yes | Yes |
| MCPs | Yes | Yes |
| Settings | Yes | Yes |

**Commands:**
```bash
# List all resources
npx claude-code-templates list

# List by type
npx claude-code-templates list --type=skills
npx claude-code-templates list --type=agents
npx claude-code-templates list --type=commands

# Search
npx claude-code-templates search "<query>"

# Install
npx claude-code-templates install <template-name>
```

**Notable Templates:**
- `aws-stack` — Complete AWS integration with MCP
- `stripe-integration` — Stripe payments with webhook handling
- `security-auditor` — Security analysis agent
- `scientific-computing` — 139+ research/science skills
- `neon-postgres` — PostgreSQL with Neon MCP

---

### 2. skills.sh (Open Agent Skills)

**Priority:** 2 (Secondary, multi-agent)
**Focus:** Broad ecosystem for multiple AI agents
**URL:** https://skills.sh

| Resource Type | Count | Available |
|---------------|-------|-----------|
| Skills | 33,000+ | Yes |
| Agents | Limited | Yes |
| Commands | Limited | Yes |
| Hooks | No | — |
| MCPs | No | — |
| Settings | No | — |

**Commands:**
```bash
# Search for skills
npx skills find "<query>"

# Get skill details
npx skills info "<owner/repo>"

# Install skill
npx skills add "<owner/repo>" --agent claude-code -y

# List installed
npx skills list --installed
```

**Trusted Sources:**
- `anthropic/*` — Official Anthropic skills
- `vercel-labs/*` — Vercel/Next.js ecosystem
- `google-labs-code/*` — Google code tools
- `aws/*` — AWS patterns
- `stripe/*` — Stripe integration
- `prisma/*` — Prisma ORM

---

## Manual Discovery Workflow

### Step 1: Identify What You Need

Determine the resource type:
- **Skill** — Behavioral guidance for specific technology
- **Agent** — Specialized expert for complex tasks
- **Command** — Slash command for quick actions
- **Hook** — Automated triggers (pre-commit, etc.)
- **MCP** — External tool integration

### Step 2: Search Both Registries

```bash
# Search aitmpl.com first (Claude Code-specific)
npx claude-code-templates search "react"

# Then search skills.sh (broader coverage)
npx skills find "react"
```

### Step 3: Compare Results

| Factor | aitmpl.com | skills.sh |
|--------|------------|-----------|
| Claude Code-specific | Yes | No |
| Includes agents/hooks/MCPs | Often | Rarely |
| Volume | 200+ | 33,000+ |
| Quality assurance | Curated | Community |

### Step 4: Install Chosen Resource

```bash
# From aitmpl.com (RECOMMENDED for Claude Code)
npx claude-code-templates install <template>

# From skills.sh
npx skills add "<owner/repo>" --agent claude-code -y
```

### Step 5: Post-Install (MANUAL)

After installation, you must:
- [ ] Add any required API keys to `.env`
- [ ] Restart Claude Code if MCPs were installed
- [ ] Review and customize the installed resource
- [ ] Add frontmatter if missing (see skill-scout.md)

---

## Registry Comparison

| Feature | aitmpl.com | skills.sh |
|---------|------------|-----------|
| **Focus** | Claude Code | Multi-agent |
| **Skills** | 200+ | 33,000+ |
| **Agents** | 48+ | Limited |
| **Commands** | 21+ | Limited |
| **Hooks** | Yes | No |
| **MCPs** | Yes | No |
| **Settings** | Yes | No |
| **Quality** | Curated | Community |
| **Best for** | Complete stacks | Specific skills |

**Recommendation:**
- Use **aitmpl.com** for Claude Code-specific complete configurations
- Use **skills.sh** for specific technology skills not in aitmpl.com
- Use **both** via `/cc-scout-skills` for automatic best-of-both selection

---

## Technology-Specific Recommendations

| Technology | Preferred Source | Why |
|------------|-----------------|-----|
| React/Next.js | skills.sh (vercel-labs) | Official Vercel skills |
| AWS | aitmpl.com | Complete stack with MCP |
| Stripe | aitmpl.com | Full integration + MCP |
| PostgreSQL | aitmpl.com | Database MCP included |
| Python/Django | skills.sh | Larger skill library |
| Scientific/Research | aitmpl.com | 139+ specialized skills |
| General web | skills.sh | Volume advantage |

---

## Creating Shareable Resources

### Publish to skills.sh

1. Create `.claude/` structure in GitHub repo
2. Add skills as markdown files
3. Register at skills.sh
4. Others install with `npx skills add your/repo`

### Publish to aitmpl.com

1. Create complete Claude Code configuration
2. Submit to aitmpl.com for review
3. Include agents, hooks, MCPs for full stack
4. Others install with `npx claude-code-templates install your-template`

---

## See Also

- `/cc-scout-skills` — Automated multi-registry discovery
- `.claude/config/registries.md` — Registry configuration
- `.claude/skills/project-mgmt/skill-scout.md` — Scout skill details
