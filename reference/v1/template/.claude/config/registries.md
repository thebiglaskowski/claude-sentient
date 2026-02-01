# Skill Registry Configuration

## Overview

This file defines the external registries used by `/cc-scout-skills` to discover and install skills, agents, commands, hooks, MCPs, and settings for projects.

---

## Active Registries

### 1. skills.sh

**URL:** https://skills.sh
**Type:** Multi-agent ecosystem
**Priority:** 2 (secondary)
**Status:** ✓ Active

| Resource Type | Available | Install Command |
|---------------|-----------|-----------------|
| Skills | ✓ 33,000+ | `npx skills add <owner/repo>` |
| Agents | Limited | `npx skills add <owner/repo>` |
| Commands | Limited | `npx skills add <owner/repo>` |
| Hooks | ✗ | — |
| MCPs | ✗ | — |
| Settings | ✗ | — |

**Strengths:**
- Massive skill library (33,000+)
- Multi-agent support (Cursor, Copilot, Claude, Gemini, etc.)
- Strong community contributions
- Well-known sources (vercel-labs, anthropic, google-labs-code)

**Search Command:**
```bash
npx skills find "<query>"
```

**Install Command:**
```bash
npx skills add "<owner/repo@skill>" --agent claude-code -y
```

**Trusted Sources:**
- `anthropic/*` — Official Anthropic skills
- `vercel-labs/*` — Vercel ecosystem
- `google-labs-code/*` — Google code tools
- `aws/*` — AWS patterns
- `stripe/*` — Stripe integration

---

### 2. aitmpl.com

**URL:** https://www.aitmpl.com
**Type:** Claude Code-specific templates
**Priority:** 1 (primary for Claude Code)
**Status:** ✓ Active

| Resource Type | Available | Install Command |
|---------------|-----------|-----------------|
| Skills | ✓ 200+ | `npx claude-code-templates install <template>` |
| Agents | ✓ 48+ | `npx claude-code-templates install <template>` |
| Commands | ✓ 21+ | `npx claude-code-templates install <template>` |
| Hooks | ✓ Yes | `npx claude-code-templates install <template>` |
| MCPs | ✓ Yes | `npx claude-code-templates install <template>` |
| Settings | ✓ Yes | `npx claude-code-templates install <template>` |

**Strengths:**
- Claude Code-specific (optimized for this platform)
- Complete configurations (not just skills)
- Company-specific stacks (AWS, Stripe, GitHub, Neon)
- Scientific computing skills (139+)
- Pre-configured hooks and MCPs

**Search Command:**
```bash
npx claude-code-templates list --type=<type>
npx claude-code-templates search "<query>"
```

**Install Command:**
```bash
npx claude-code-templates install <template-name>
```

**Notable Templates:**
- `aws-stack` — Complete AWS integration
- `stripe-integration` — Stripe payment patterns
- `security-auditor` — Security-focused agent
- `scientific-computing` — Research/science skills
- `neon-postgres` — Neon database patterns

---

## Registry Selection Logic

### Priority Rules

1. **Claude Code-specific sources preferred** — When a skill exists in both registries, prefer the Claude Code-specific version (aitmpl.com)

2. **Resource type routing:**
   | Resource | Primary Source | Fallback |
   |----------|---------------|----------|
   | Skills | aitmpl.com | skills.sh |
   | Agents | aitmpl.com | skills.sh |
   | Commands | aitmpl.com | skills.sh |
   | Hooks | aitmpl.com | — |
   | MCPs | aitmpl.com | — |
   | Settings | aitmpl.com | — |

3. **Technology-specific routing:**
   | Technology | Preferred Source |
   |------------|-----------------|
   | React/Next.js | skills.sh (vercel-labs) |
   | AWS | aitmpl.com (aws-stack) |
   | Stripe | aitmpl.com (stripe-integration) |
   | Scientific/Research | aitmpl.com |
   | General web | skills.sh |

### Scoring Algorithm

Each discovered resource is scored (0-100) based on:

| Factor | Weight | Description |
|--------|--------|-------------|
| Technology Match | 30% | Exact match = 30, partial = 15, related = 5 |
| Source Reputation | 25% | Verified/official = 25, trusted = 20, community = 10 |
| Specificity | 20% | Claude Code-specific = 20, multi-agent = 10 |
| Completeness | 15% | Includes agents+hooks+MCPs = 15, skills only = 5 |
| Recency | 10% | Updated <30 days = 10, <90 days = 7, <1 year = 3 |

**Scoring Tiers:**
- **Auto-install:** Score ≥ 80 (high confidence)
- **Recommend:** Score 50-79 (ask user)
- **Mention:** Score 30-49 (low confidence)
- **Skip:** Score < 30 (poor match)

---

## Adding New Registries

To add a new registry source:

1. **Add entry to this file** with:
   - URL and type
   - Priority level
   - Available resource types
   - Search and install commands
   - Trusted sources

2. **Update skill-scout.md** to include the new registry in search flow

3. **Test discovery** with common tech stacks

### Registry Template

```markdown
### [N]. [Registry Name]

**URL:** [url]
**Type:** [description]
**Priority:** [1-5, lower = higher priority]
**Status:** [✓ Active / ⚠ Beta / ✗ Disabled]

| Resource Type | Available | Install Command |
|---------------|-----------|-----------------|
| Skills | [✓/✗] [count] | [command] |
| Agents | [✓/✗] [count] | [command] |
| Commands | [✓/✗] [count] | [command] |
| Hooks | [✓/✗] | [command] |
| MCPs | [✓/✗] | [command] |
| Settings | [✓/✗] | [command] |

**Search Command:**
[command]

**Install Command:**
[command]

**Trusted Sources:**
- [source patterns]
```

---

## Future Registry Candidates

Potential registries to evaluate:

| Registry | URL | Notes |
|----------|-----|-------|
| GitHub Marketplace | github.com/marketplace | Claude Code actions |
| npm registry | npmjs.com | Claude Code packages |
| Awesome Claude | github.com/awesome-claude | Curated list |

---

## Configuration Options

### Environment Variables

```bash
# Disable specific registries
SCOUT_DISABLE_REGISTRIES="skills.sh"

# Set custom timeout for registry queries
SCOUT_REGISTRY_TIMEOUT=30000

# Enable verbose logging
SCOUT_VERBOSE=true
```

### Per-Project Configuration

Add to `.claude/settings.local.json`:

```json
{
  "scout": {
    "registries": {
      "skills.sh": { "enabled": true, "priority": 2 },
      "aitmpl.com": { "enabled": true, "priority": 1 }
    },
    "autoInstallThreshold": 80,
    "trustedSources": ["anthropic/*", "vercel-labs/*"]
  }
}
```
