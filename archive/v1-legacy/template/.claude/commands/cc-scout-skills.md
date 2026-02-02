---
name: cc-scout-skills
description: Discover and install the best skills, agents, and resources from multiple registries
version: "2.0.0"
model: sonnet
---

# /cc-scout-skills — Multi-Registry Resource Discovery

<context>
This command searches multiple registries (skills.sh, aitmpl.com, and future sources) to find
and install the best skills, agents, commands, hooks, MCPs, and settings for your project.
It uses intelligent scoring to recommend the highest quality resources for your tech stack.
</context>

<role>
You are a resource discovery agent who:
- Detects project technology stack automatically
- Queries multiple registries in parallel
- Scores and ranks discovered resources
- Recommends the best options for each technology
- Handles installation from the appropriate registry
- Ensures post-install compatibility
</role>

## Usage

```
/cc-scout-skills                    # Full discovery and recommendations
/cc-scout-skills --registry=aitmpl  # Search specific registry only
/cc-scout-skills --type=agents      # Search for specific resource type
/cc-scout-skills --auto             # Auto-install all high-confidence matches
```

---

## Automation vs Manual Steps

### AUTOMATED (No User Intervention Required)

| Step | What Happens |
|------|--------------|
| Tech stack detection | Reads package.json, requirements.txt, etc. automatically |
| Registry querying | Searches all enabled registries in parallel |
| Scoring & ranking | Calculates relevance scores (0-100) for each resource |
| Deduplication | Identifies duplicates across registries, keeps best |
| Categorization | Groups by resource type (skills, agents, hooks, etc.) |
| Post-install processing | Adds frontmatter if missing, updates CLAUDE.md |

### REQUIRES USER CONFIRMATION

| Step | What Happens |
|------|--------------|
| Auto-install resources (≥80 score) | Asks "Install all auto-install resources?" |
| Recommended resources (50-79 score) | Presents list, asks which to install |
| Alternative selection | When duplicates exist, asks which source to use |
| Configuration after install | Prompts for API keys, env vars needed |

### FULLY MANUAL (User Must Do)

| Step | What User Does |
|------|----------------|
| Configure API keys | Add Stripe, AWS, etc. keys to `.env` |
| Database connections | Set up connection strings |
| MCP server activation | May need to restart Claude Code |
| Custom configuration | Modify installed resources for project needs |

---

<task>
Discover and install optimal resources by:
1. Detecting project technologies (AUTOMATED)
2. Querying all registries (AUTOMATED)
3. Scoring and ranking results (AUTOMATED)
4. Presenting recommendations (AUTOMATED)
5. Installing selected resources (REQUIRES CONFIRMATION)
6. Post-processing installations (AUTOMATED)
7. Guiding post-install configuration (MANUAL STEPS LISTED)
</task>

<instructions>

<step number="1">
**Detect Tech Stack (AUTOMATED)**

Read project files to identify technologies:

| File | Technologies |
|------|--------------|
| `package.json` | Node.js, frameworks (React, Next.js, Express), libraries |
| `requirements.txt` / `pyproject.toml` | Python packages |
| `go.mod` | Go modules |
| `Cargo.toml` | Rust crates |
| `Gemfile` | Ruby gems |
| `pom.xml` / `build.gradle` | Java dependencies |
| `composer.json` | PHP packages |
| `Dockerfile` | Container technologies |
| `.github/workflows/` | CI/CD tools |
| `terraform/` / `*.tf` | Infrastructure as code |
| `.env` / `config/` | Services (AWS, Stripe, database) |

Output: List of detected technologies with versions.
</step>

<step number="2">
**Query Registries (AUTOMATED)**

Search each enabled registry in parallel:

**aitmpl.com (Priority 1 - Claude Code-specific):**
```bash
npx claude-code-templates list --type=skills
npx claude-code-templates list --type=agents
npx claude-code-templates list --type=commands
npx claude-code-templates search "<technology>"
```

**skills.sh (Priority 2 - Multi-agent ecosystem):**
```bash
npx skills find "<technology>"
npx skills info "<owner/repo>"
```

Collect all results with metadata (source, type, description, popularity).
</step>

<step number="3">
**Score and Rank (AUTOMATED)**

Apply scoring algorithm (0-100 points):

| Factor | Weight | Scoring Criteria |
|--------|--------|------------------|
| Technology Match | 30% | Exact match=30, Partial=15, Related=5 |
| Source Reputation | 25% | Official/verified=25, Trusted=20, Community=10 |
| Specificity | 20% | Claude Code-specific=20, Multi-agent=10 |
| Completeness | 15% | Full stack (agents+hooks+MCPs)=15, Skills only=5 |
| Recency | 10% | Updated <30 days=10, <90 days=7, <1 year=3 |

**Classification:**
- **Auto-install** (≥80): High confidence
- **Recommend** (50-79): Good match, ask user
- **Mention** (30-49): Available but low confidence
- **Skip** (<30): Don't show
</step>

<step number="4">
**Deduplicate (AUTOMATED)**

When same technology appears in multiple registries:

1. **Prefer Claude Code-specific** — aitmpl.com over skills.sh
2. **Prefer complete stacks** — Templates with agents+hooks+MCPs
3. **Prefer official sources** — anthropic/*, vercel-labs/*
4. **Note alternatives** — Show when good options exist in both
</step>

<step number="5">
**Present Recommendations (AUTOMATED)**

Generate structured report:

```markdown
# Skill Scout Report

**Project:** [name]
**Technologies Detected:** [count]
**Registries Searched:** [count]

---

## Auto-Install Resources (Score ≥80)

| Resource | Type | Source | Score | Technology |
|----------|------|--------|-------|------------|
| [name] | [skill/agent/hook] | [registry] | [score] | [tech] |

## Recommended Resources (Score 50-79)

| Resource | Type | Source | Score | Technology |
|----------|------|--------|-------|------------|
| [name] | [skill/agent/hook] | [registry] | [score] | [tech] |

## Available Agents

| Agent | Source | Purpose |
|-------|--------|---------|

## Available Hooks & MCPs

| Resource | Type | Source | Purpose |
|----------|------|--------|---------|
```
</step>

<step number="6">
**Install Resources (REQUIRES CONFIRMATION)**

Ask user what to install:

```
Install all auto-install resources? (yes/no/select)
```

Based on response:
- **yes**: Install all ≥80 score resources
- **no**: Skip to recommended list
- **select**: Show numbered list for selection

Install from appropriate registry:

```bash
# From aitmpl.com
npx claude-code-templates install <template-name>

# From skills.sh
npx skills add "<owner/repo>" --agent claude-code -y
```
</step>

<step number="7">
**Post-Install Processing (AUTOMATED)**

For each installed resource:

1. **Check frontmatter** — Add YAML frontmatter if missing
2. **Validate structure** — Ensure required fields present
3. **Tag source** — Add registry origin for future updates
4. **Update CLAUDE.md** — Add to `## Installed Resources` section

Frontmatter template for external resources:
```yaml
---
name: "[from H1 or filename]"
description: "[first paragraph]"
version: "1.0.0"
tags: ["external", "[registry]", "[technology]"]
source:
  registry: "[skills.sh|aitmpl.com]"
  identifier: "[owner/repo or template-name]"
  installed: "[ISO date]"
---
```
</step>

<step number="8">
**Guide Configuration (MANUAL STEPS)**

List required manual configuration:

```markdown
## Manual Configuration Required

### API Keys & Secrets
- [ ] Add `STRIPE_SECRET_KEY` to `.env`
- [ ] Add `AWS_ACCESS_KEY_ID` to `.env`

### Database Setup
- [ ] Configure `DATABASE_URL` in `.env`
- [ ] Run database migrations if needed

### MCP Activation
- [ ] Restart Claude Code to activate new MCPs
- [ ] Verify MCP connection with `/mcp status`

### Custom Configuration
- [ ] Review installed agents for project-specific settings
- [ ] Adjust hook triggers if needed
```
</step>

</instructions>

---

## Output Format

<output_format>
```markdown
# Skill Scout Report

**Project:** [project-name]
**Technologies Detected:** [N]
**Registries Searched:** skills.sh, aitmpl.com

---

## Detected Tech Stack

### Languages
- [Language] [version] (from [source file])

### Frameworks
- [Framework] [version]

### Databases
- [Database] (from [config source])

### Services
- [Service] (detected from [source])

### DevOps
- [Tool]

---

## Recommended Resources

### Auto-Install (Score ≥80) — WILL INSTALL AUTOMATICALLY IF CONFIRMED

| Resource | Type | Source | Score | Technology |
|----------|------|--------|-------|------------|
| [name] | [type] | [source] | [score] | [tech] |

### Recommended (Score 50-79) — REQUIRES SELECTION

| Resource | Type | Source | Score | Technology |
|----------|------|--------|-------|------------|
| [name] | [type] | [source] | [score] | [tech] |

### Available Agents

| Agent | Source | Score | Purpose |
|-------|--------|-------|---------|
| [name] | [source] | [score] | [description] |

### Available Hooks & MCPs

| Resource | Type | Source | Purpose |
|----------|------|--------|---------|
| [name] | [hook/mcp] | [source] | [description] |

---

## Installation

**Install all auto-install resources?** (yes/no/select)

> [user response]

### Installation Results

- ✓ [resource] installed from [source]
- ✗ [resource] failed: [reason]

---

## Manual Configuration Required

After installation, complete these steps manually:

### API Keys & Secrets
- [ ] [Key name] — Add to `.env`

### Database Setup
- [ ] [Configuration step]

### MCP Activation
- [ ] Restart Claude Code to activate MCPs

### Verification
- [ ] Run `/cc-test` to verify installations
```
</output_format>

---

## Examples

<examples>
<example>
<input>
/cc-scout-skills
(in a Next.js + Stripe + PostgreSQL project)
</input>
<output>
# Skill Scout Report

**Project:** ecommerce-app
**Technologies Detected:** 12
**Registries Searched:** skills.sh, aitmpl.com

---

## Detected Tech Stack

### Languages
- TypeScript 5.3 (from tsconfig.json)
- JavaScript (from package.json)

### Frameworks
- Next.js 14.1.0
- React 18.2.0
- Tailwind CSS 3.4.0

### Databases
- PostgreSQL (from DATABASE_URL in .env)
- Prisma ORM 5.8.0

### Services
- Stripe (from STRIPE_SECRET_KEY in .env)
- AWS S3 (from aws-sdk in package.json)

### DevOps
- Docker (from Dockerfile)
- GitHub Actions (from .github/workflows/)

---

## Recommended Resources

### Auto-Install (Score ≥80)

| Resource | Type | Source | Score | Technology |
|----------|------|--------|-------|------------|
| stripe-integration | Stack | aitmpl.com | 95 | Stripe |
| nextjs-app-router | Skill | skills.sh/vercel-labs | 92 | Next.js |
| neon-postgres | Stack | aitmpl.com | 90 | PostgreSQL |
| react-patterns | Skill | aitmpl.com | 88 | React |

### Recommended (Score 50-79)

| Resource | Type | Source | Score | Technology |
|----------|------|--------|-------|------------|
| tailwind-patterns | Skill | skills.sh | 72 | Tailwind |
| typescript-strict | Skill | skills.sh | 68 | TypeScript |
| prisma-patterns | Skill | skills.sh | 65 | Prisma |
| docker-node | Skill | skills.sh | 62 | Docker |

### Available Agents

| Agent | Source | Score | Purpose |
|-------|--------|-------|---------|
| security-auditor | aitmpl.com | 85 | Security vulnerability analysis |
| code-reviewer | aitmpl.com | 80 | Automated code review |

### Available Hooks & MCPs

| Resource | Type | Source | Purpose |
|----------|------|--------|---------|
| stripe-mcp | MCP | aitmpl.com | Stripe API tools |
| postgres-mcp | MCP | aitmpl.com | Database query tools |
| pre-commit-lint | Hook | aitmpl.com | Auto-linting on commit |

---

## Installation

**Install all auto-install resources?** (yes/no/select)

> yes

### Installation Results

- ✓ stripe-integration installed from aitmpl.com
- ✓ nextjs-app-router installed from skills.sh
- ✓ neon-postgres installed from aitmpl.com
- ✓ react-patterns installed from aitmpl.com

### Project CLAUDE.md Updated

Added 4 resources to `## Installed Resources` section.

---

## Manual Configuration Required

### API Keys & Secrets (YOU MUST DO THIS)
- [ ] Verify `STRIPE_SECRET_KEY` is set in `.env`
- [ ] Verify `STRIPE_WEBHOOK_SECRET` is set in `.env`
- [ ] Verify `DATABASE_URL` points to your PostgreSQL instance

### MCP Activation (YOU MUST DO THIS)
- [ ] Restart Claude Code to activate stripe-mcp and postgres-mcp
- [ ] Verify MCPs loaded: Check for tools in `/mcp` output

### Verification
- [ ] Run `/cc-test` to verify skill installations
- [ ] Test Stripe webhook with `stripe trigger payment_intent.succeeded`

---

## Next Steps

1. **Install recommended skills?** Say "install tailwind-patterns, typescript-strict"
2. **Add agents?** Say "install security-auditor agent"
3. **Run security audit?** Say "spawn security-auditor to audit the codebase"
</output>
</example>
</examples>

---

## Registry Configuration

See `.claude/config/registries.md` for:
- Full registry details
- Scoring algorithm configuration
- Trusted sources list
- Adding new registries

---

## Flags

| Flag | Description |
|------|-------------|
| `--registry=<name>` | Search only specified registry (aitmpl, skills.sh) |
| `--type=<type>` | Search for specific type (skills, agents, commands, hooks, mcps) |
| `--auto` | Auto-install all ≥80 score without prompting |
| `--dry-run` | Show what would be installed without installing |
| `--verbose` | Show detailed scoring breakdown |
| `--refresh` | Re-query registries even if cached |

---

## Error Handling

| Error | Recovery |
|-------|----------|
| Registry unreachable | Skip registry, continue with others, warn user |
| Install fails | Log error, continue with other installs, report at end |
| Frontmatter generation fails | Install anyway, mark for manual review |
| CLAUDE.md update fails | Log error, provide manual instructions |

---

## See Also

| Related Resource | When to Use |
|------------------|-------------|
| `.claude/config/registries.md` | Registry configuration and scoring weights |
| [skill-scout.md](../../../../skills/skill-scout.md) | Core skill this command invokes |
| `.claude/skills/collaboration/template-registry.md` | Manual browsing of registries |
| `/cc-analyze` | Brownfield codebase analysis before skill discovery |
