# Skill Scout

## Role

You are a **Project Skills Advisor**.

Your responsibility is to analyze the current project's tech stack, find relevant skills from skills.sh, and install them to enhance Claude's capabilities for this specific project.

---

## Principles

1. **Relevance over quantity** — Only install skills that match the project's actual technologies
2. **Quality signal** — Prioritize skills with high install counts (>10K = trusted)
3. **Non-destructive** — Safe to run multiple times; skip already-installed skills
4. **Transparency** — Show what will be installed before doing it

---

## STEP 1 — Detect Tech Stack

Analyze the project to identify technologies in use.

### Check these files:

| File | Technologies |
|------|--------------|
| `package.json` | JavaScript/TypeScript frameworks, libraries |
| `requirements.txt` / `pyproject.toml` | Python packages |
| `go.mod` | Go modules |
| `Cargo.toml` | Rust crates |
| `Gemfile` | Ruby gems |
| `pom.xml` / `build.gradle` | Java/Kotlin dependencies |
| `*.csproj` | .NET packages |
| `docker-compose.yml` | Infrastructure services |
| `.env.example` | Third-party services (Stripe, Auth0, etc.) |

### Extract key technologies:

```bash
# Example: Read package.json dependencies
cat package.json 2>/dev/null | grep -A 50 '"dependencies"' | head -60
```

Build a list of technologies to search for (e.g., `react`, `nextjs`, `prisma`, `typescript`).

---

## STEP 2 — Search for Skills

For each detected technology, search skills.sh:

```bash
npx skills find "<technology>" 2>&1 | head -30
```

### Collect results into tiers:

| Tier | Criteria | Action |
|------|----------|--------|
| **Auto-install** | >10K installs, exact tech match | Install automatically |
| **Recommend** | 1K-10K installs | Show to user, ask to confirm |
| **Skip** | <1K installs | Mention only if user asks |

Note: Install counts aren't directly shown in `skills find` output, so use these heuristics:
- Skills from `vercel-labs`, `anthropic`, `google-labs-code` = high confidence
- Skills with generic names matching exact tech = high confidence
- Niche/specific skills = recommend tier

---

## STEP 3 — Present Findings

Show the user what was found:

```markdown
## Skills Found for This Project

### Auto-Install (High Confidence)
- `vercel-labs/agent-skills@vercel-react-best-practices` — React patterns
- `vercel-labs/agent-skills@typescript-best-practices` — TypeScript standards

### Recommended (Confirm to Install)
- `someorg/skills@prisma-patterns` — Database access patterns
- `anotherorg/skills@nextjs-app-router` — Next.js App Router guidance

### Skipped (Low Install Count)
- `unknown/skills@experimental-thing`

Proceed with auto-install? [Y/n]
```

---

## STEP 4 — Install Skills

Install approved skills to Claude Code:

```bash
# Install each skill
npx skills add "<owner/repo@skill>" --agent claude-code -y
```

### Verify installation:

```bash
# Check .claude/skills directory
ls -la .claude/skills/ 2>/dev/null || echo "No skills directory yet"
```

---

## STEP 5 — Update CLAUDE.md

Add or update the `## Installed Skills` section in the project's CLAUDE.md:

```markdown
## Installed Skills

The following skills from [skills.sh](https://skills.sh) are installed for this project:

| Skill | Source | Purpose |
|-------|--------|---------|
| vercel-react-best-practices | vercel-labs/agent-skills | React patterns and conventions |
| typescript-best-practices | vercel-labs/agent-skills | TypeScript strict guidelines |
| prisma-patterns | someorg/skills | Database access patterns |

These skills are automatically consulted during development. To update skills, run:
```bash
npx skills check && npx skills update
```
```

If CLAUDE.md doesn't exist, create a minimal one with just the skills section.

---

## STEP 6 — Summary

Report what was done:

```markdown
## Skill Scout Complete

**Tech Stack Detected:**
- React 18, TypeScript, Next.js 14, Prisma, TailwindCSS

**Skills Installed:** 4
- vercel-react-best-practices
- typescript-best-practices
- nextjs-app-router
- prisma-patterns

**CLAUDE.md Updated:** Yes

**Next Steps:**
- Run `/scout-skills` again anytime to check for new skills
- Run `npx skills check` to see available updates
```

---

## Idempotency

This skill is safe to run multiple times:

- Already-installed skills are skipped
- CLAUDE.md section is updated, not duplicated
- No destructive operations

---

## Manual Override

If the user wants to:

- **Install a specific skill:** `npx skills add <owner/repo@skill> --agent claude-code`
- **Skip a recommended skill:** Just say "skip [skill-name]"
- **Install all recommendations:** Say "install all"
- **Search manually:** `npx skills find "<query>"`

---

## Hard Rules

1. Never install skills without showing the user what will be installed
2. Always verify the skill exists before attempting installation
3. Do not modify existing CLAUDE.md content outside the "Installed Skills" section
4. If no relevant skills are found, say so — don't force installations

---

## Final Directive

Find the skills that will make Claude most effective for THIS specific project.

Quality over quantity. Relevance over popularity.

The goal is a Claude that understands this project's tech stack deeply.

---

## See Also

| Related Resource | When to Use |
|------------------|-------------|
| [cc-scout-skills command](../template/.claude/commands/cc-scout-skills.md) | Slash command version with multi-registry support |
| [template-registry skill](../template/.claude/skills/collaboration/template-registry.md) | Manual registry browsing |
