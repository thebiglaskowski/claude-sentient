# Upgrade Guide

How to upgrade your project to newer template versions.

---

## Check Your Version

```bash
# Check current template version
cat .claude/.version

# Check latest version
cat C:\scripts\prompts\template\.claude\.version
```

---

## Upgrade Paths

### From Any Version to Latest

#### Step 1: Backup Current Configuration

```bash
# Backup your .claude folder
cp -r .claude .claude.backup
```

#### Step 2: Update Prompts Library

```bash
cd C:\scripts\prompts
git pull origin main
```

#### Step 3: Copy New Files (Safe - Won't Overwrite)

**Windows (PowerShell):**
```powershell
# Copy new commands (won't overwrite existing)
Copy-Item -Path "C:\scripts\prompts\template\.claude\commands\*" -Destination ".claude\commands\" -ErrorAction SilentlyContinue

# Copy new skills (won't overwrite existing)
Copy-Item -Path "C:\scripts\prompts\template\.claude\skills\*" -Destination ".claude\skills\" -ErrorAction SilentlyContinue

# Copy new documentation
Copy-Item -Path "C:\scripts\prompts\template\.claude\QUICK_REFERENCE.md" -Destination ".claude\" -Force
Copy-Item -Path "C:\scripts\prompts\template\.claude\CONFIGURATION.md" -Destination ".claude\" -Force
Copy-Item -Path "C:\scripts\prompts\template\.claude\UPGRADE_GUIDE.md" -Destination ".claude\" -Force
Copy-Item -Path "C:\scripts\prompts\template\.claude\MCP_SERVERS.md" -Destination ".claude\" -Force
```

**macOS/Linux:**
```bash
# Copy new commands (won't overwrite existing)
cp -n C:\scripts\prompts\template\.claude\commands\* .claude\commands\

# Copy new skills (won't overwrite existing)
cp -n C:\scripts\prompts\template\.claude\skills\* .claude\skills\

# Copy new documentation
cp C:\scripts\prompts\template\.claude\QUICK_REFERENCE.md .claude\
cp C:\scripts\prompts\template\.claude\CONFIGURATION.md .claude\
cp C:\scripts\prompts\template\.claude\UPGRADE_GUIDE.md .claude\
cp C:\scripts\prompts\template\.claude\MCP_SERVERS.md .claude\
```

#### Step 4: Review CLAUDE.md Changes

Your `CLAUDE.md` may have project-specific customizations. Compare:

```bash
# See differences
diff .claude/CLAUDE.md C:\scripts\prompts\template\.claude\CLAUDE.md
```

**Options:**
1. **Keep yours** - If heavily customized
2. **Use new** - Copy new version, re-add customizations
3. **Merge** - Manually combine changes

#### Step 5: Update Version File

```bash
cp C:\scripts\prompts\template\.claude\.version .claude\.version
```

#### Step 6: Verify

```bash
# Check new commands exist
ls .claude/commands/

# Check new skills exist
ls .claude/skills/

# Verify version
cat .claude/.version
```

---

## Version-Specific Upgrades

### Upgrading from 1.2.0 to 2.0.0

**Major Changes in v2.0:**
- YAML frontmatter for all skills
- Modular rules system
- Specialized agents
- Command arguments support
- Context fork (subagent isolation)
- Extended thinking ("ultrathink")
- CI/CD automation scripts

#### Step 1: Update Prompts Library

```bash
cd C:\scripts\prompts
git pull origin main
```

#### Step 2: Create New Directories

```bash
# Create new v2.0 directories
mkdir -p .claude/rules
mkdir -p .claude/agents
mkdir -p .claude/scripts/ci
mkdir -p .claude/scripts/validate
```

#### Step 3: Copy New Files

**Windows (PowerShell):**
```powershell
# Copy rules
Copy-Item -Path "C:\scripts\prompts\template\.claude\rules\*" -Destination ".claude\rules\" -Force

# Copy agents
Copy-Item -Path "C:\scripts\prompts\template\.claude\agents\*" -Destination ".claude\agents\" -Force

# Copy scripts
Copy-Item -Path "C:\scripts\prompts\template\.claude\scripts\*" -Destination ".claude\scripts\" -Recurse -Force

# Copy new skills (4 new in v2.0)
Copy-Item -Path "C:\scripts\prompts\template\.claude\skills\argument-parser.md" -Destination ".claude\skills\"
Copy-Item -Path "C:\scripts\prompts\template\.claude\skills\subagent-research.md" -Destination ".claude\skills\"
Copy-Item -Path "C:\scripts\prompts\template\.claude\skills\parallel-exploration.md" -Destination ".claude\skills\"
Copy-Item -Path "C:\scripts\prompts\template\.claude\skills\extended-thinking.md" -Destination ".claude\skills\"

# Update documentation
Copy-Item -Path "C:\scripts\prompts\template\.claude\QUICK_REFERENCE.md" -Destination ".claude\" -Force
Copy-Item -Path "C:\scripts\prompts\template\.claude\CONFIGURATION.md" -Destination ".claude\" -Force
Copy-Item -Path "C:\scripts\prompts\template\.claude\UPGRADE_GUIDE.md" -Destination ".claude\" -Force
```

**macOS/Linux:**
```bash
# Copy rules
cp -r ~/scripts/prompts/template/.claude/rules/* .claude/rules/

# Copy agents
cp -r ~/scripts/prompts/template/.claude/agents/* .claude/agents/

# Copy scripts
cp -r ~/scripts/prompts/template/.claude/scripts/* .claude/scripts/

# Copy new skills
cp ~/scripts/prompts/template/.claude/skills/argument-parser.md .claude/skills/
cp ~/scripts/prompts/template/.claude/skills/subagent-research.md .claude/skills/
cp ~/scripts/prompts/template/.claude/skills/parallel-exploration.md .claude/skills/
cp ~/scripts/prompts/template/.claude/skills/extended-thinking.md .claude/skills/

# Update documentation
cp ~/scripts/prompts/template/.claude/QUICK_REFERENCE.md .claude/
cp ~/scripts/prompts/template/.claude/CONFIGURATION.md .claude/
cp ~/scripts/prompts/template/.claude/UPGRADE_GUIDE.md .claude/
```

#### Step 4: Update Existing Skills (Optional)

Your existing skills will continue to work, but to enable v2.0 features, add YAML frontmatter.

**Option A: Auto-generate frontmatter (Recommended)**

Use the new frontmatter-generator skill:
```
add frontmatter
```

This scans all skills and generates frontmatter for those missing it.

**Option B: Manual frontmatter**

Add this structure to each skill (use minimal official format):

```markdown
---
name: skill-name
description: What it does in one line
model: sonnet
---

# Existing Skill Content...
```

**Official frontmatter fields:**
- `name` - Skill identifier (kebab-case)
- `description` - One-line description
- `model` - haiku, sonnet, or opus
- `argument-hint` - Hint for arguments (e.g., `"<path>"`)
- `disable-model-invocation` - true for reference-only skills
- `context` - fork for isolated subagent execution

> **Important:** Use hyphens, not underscores (e.g., `disable-model-invocation` not `disable_model_invocation`).

**Option C: Copy from template (will overwrite)**
```bash
cp C:\scripts\prompts\template\.claude\skills\*.md .claude\skills\
```

**Note:** Skills downloaded from skills.sh after upgrading will automatically get frontmatter generated by the updated skill-scout.

#### Step 5: Update CLAUDE.md

Add these sections to your project's CLAUDE.md:

```markdown
## Modular Rules

Load topic-specific guidance with `@rules/[name]`:

| Rule | Purpose |
|------|---------|
| `@rules/security` | OWASP, authentication, secrets |
| `@rules/testing` | Coverage, TDD, mocks |
| `@rules/git-workflow` | Commits, branches, PRs |

---

## Specialized Agents

Spawn focused agents for specific tasks:

| Agent | Model | Use Case |
|-------|-------|----------|
| `code-reviewer` | sonnet | Code review tasks |
| `security-analyst` | opus | Security audits |
| `test-engineer` | sonnet | Test writing/analysis |
```

#### Step 6: Setup GitHub Actions (Optional)

To enable automated code review and security scanning:

**Copy workflows:**
```bash
mkdir -p .github/workflows
cp /path/to/prompts/template/.github/workflows/*.yml .github/workflows/
```

**Add repository secret:**
1. Go to repository → Settings → Secrets → Actions
2. Click "New repository secret"
3. Name: `ANTHROPIC_API_KEY`
4. Value: Your API key
5. Click "Add secret"

See `.claude/SETUP.md` for detailed instructions.

#### Step 7: Update Version

```bash
echo "2.0.0" > .claude/.version
```

#### Step 7: Verify Installation

```bash
# Check new directories exist
ls .claude/rules/
ls .claude/agents/
ls .claude/scripts/

# Check version
cat .claude/.version
```

#### New Features to Try

1. **Command arguments:**
   ```
   /review src/api --deep --security
   /test src/utils --coverage=90
   ```

2. **Load rules:**
   ```
   Review this code with @rules/security
   ```

3. **Spawn agents:**
   ```
   Spawn security-analyst to audit src/auth
   ```

4. **Extended thinking:**
   ```
   /secure --ultrathink
   ```

5. **Context fork:**
   ```
   Research in background: How does caching work here?
   ```

---

### Upgrading from 1.0.0 to 1.2.0

**New files to add:**

Commands:
- `gitignore.md`
- `map-project.md`
- `scout-skills.md`

Skills (20 new):
- `auto-update-checker.md`
- `changelog-automation.md`
- `ci-cd-integration.md`
- `compound-commands.md`
- `cross-project-patterns.md`
- `dependency-checker.md`
- `dependency-tracker.md`
- `docs-generator.md`
- `dry-run-mode.md`
- `error-recovery.md`
- `file-watcher.md`
- `gitignore-manager.md`
- `health-dashboard.md`
- `metrics-logger.md`
- `project-init.md`
- `project-templates.md`
- `prompt-testing.md`
- `session-memory.md`
- `smart-context.md`
- `snippet-library.md`
- `team-sharing.md`
- `undo-history.md`

Documentation:
- `QUICK_REFERENCE.md`
- `CONFIGURATION.md`
- `UPGRADE_GUIDE.md`
- Updated `MCP_SERVERS.md`

**CLAUDE.md changes:**
- Skills reorganized into categories
- New skills table added
- Project initialization section updated

### Upgrading from 1.1.0 to 1.2.0

**New files to add:**

Skills (10 new):
- `changelog-automation.md`
- `ci-cd-integration.md`
- `compound-commands.md`
- `cross-project-patterns.md`
- `dependency-tracker.md`
- `docs-generator.md`
- `file-watcher.md`
- `health-dashboard.md`
- `prompt-testing.md`
- `snippet-library.md`
- `team-sharing.md`
- `undo-history.md`

Documentation:
- `QUICK_REFERENCE.md`
- `CONFIGURATION.md`
- `UPGRADE_GUIDE.md`

---

## Handling Customizations

### Commands You've Modified

If you've customized commands:

1. **Backup your version:**
   ```bash
   cp .claude/commands/daily.md .claude/commands/daily.md.custom
   ```

2. **Compare with new:**
   ```bash
   diff .claude/commands/daily.md.custom C:\scripts\prompts\template\.claude\commands\daily.md
   ```

3. **Merge changes** as needed

### Skills You've Added

Custom skills you created are safe - they won't be overwritten.

### Settings You've Configured

Your `settings.json` customizations are preserved. New features may require additions:

```json
{
  "mcpServers": {
    // Your existing servers
  },
  "hooks": {
    // May want to add new hooks
  }
}
```

---

## Fresh Install (Alternative)

If you prefer a clean slate:

#### Step 1: Backup Critical Files

```bash
# Save your customizations
cp .claude/CLAUDE.md ./CLAUDE.md.backup
cp .claude/settings.json ./settings.json.backup
cp -r .claude/context ./context.backup
```

#### Step 2: Remove Old Template

```bash
rm -rf .claude
```

#### Step 3: Install Fresh

```bash
# Use install script
cd C:\scripts\prompts
./install.sh /path/to/your/project
```

#### Step 4: Restore Customizations

```bash
# Merge your customizations back
# Review and copy relevant parts from backups
```

#### Step 5: Re-initialize

In Claude Code:
```
initialize this project
```

---

## Rollback

If upgrade causes issues:

```bash
# Restore from backup
rm -rf .claude
mv .claude.backup .claude
```

---

## Checking What's New

### View Changelog

```bash
cat C:\scripts\prompts\CHANGELOG.md
```

### Compare Versions

```bash
cd C:\scripts\prompts
git log --oneline -20
```

### See Changed Files

```bash
cd C:\scripts\prompts
git diff v1.1.0..v1.2.0 --name-only
```

---

## Automated Upgrade (Future)

A future version may include an upgrade command:

```
/upgrade-template
```

For now, follow the manual steps above.

---

## Getting Help

If you encounter issues during upgrade:

1. Check `TROUBLESHOOTING.md`
2. Compare with fresh template
3. Review the CHANGELOG for breaking changes
4. Restore from backup if needed
