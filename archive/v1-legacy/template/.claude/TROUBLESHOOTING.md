# Troubleshooting Guide

Solutions for common issues with Claude Code and this template.

---

## Table of Contents

1. [Setup Issues](#setup-issues)
2. [Command Issues](#command-issues)
3. [Skill Issues](#skill-issues)
4. [MCP Server Issues](#mcp-server-issues)
5. [Hook Issues](#hook-issues)
6. [Git Issues](#git-issues)
7. [Performance Issues](#performance-issues)
8. [v2.0 Features](#v20-features)
9. [Swarm Mode Issues (v4.1)](#swarm-mode-issues-v41)
10. [Plugin Issues (v4.2)](#plugin-issues-v42)

---

## Setup Issues

### Template Not Loaded

**Symptom:** Commands like `/daily` don't work.

**Causes & Solutions:**

1. **Wrong directory:**
   ```bash
   # Verify you're in project root
   pwd
   ls -la .claude/
   ```

2. **CLAUDE.md missing:**
   ```bash
   # Check file exists
   cat .claude/CLAUDE.md
   ```

3. **Claude Code not recognizing folder:**
   - Close Claude Code completely
   - Reopen with `claude --init`

### Install Script Fails

**Windows:**
```powershell
# Run with execution policy bypass
powershell -ExecutionPolicy Bypass -File .\install.ps1 -TargetDir "C:\project"
```

**macOS/Linux:**
```bash
# Make executable
chmod +x install.sh
./install.sh /path/to/project
```

### "Initialize this project" Does Nothing

**Causes:**

1. **Skills not loaded:**
   - Check `.claude/skills/project-init.md` exists

2. **Trigger not recognized:**
   - Try exact phrase: "initialize this project"
   - Or use: `/scout-skills` then `/map-project`

---

## Command Issues

### Command Not Found

**Symptom:** `/daily` returns "command not found"

**Solutions:**

1. **Check file exists:**
   ```bash
   ls .claude/commands/daily.md
   ```

2. **Check file format:**
   - Must be markdown
   - Must have proper header

3. **Restart Claude Code:**
   - Commands load at startup

### Command Gives Wrong Output

**Causes:**

1. **Outdated command:**
   - Compare with template version
   - Update if needed

2. **Missing context:**
   - Run `/map-project` to generate context
   - Check STATUS.md exists

3. **Wrong model:**
   - Some commands work better with specific models
   - Check Model Recommendation in command file

---

## Skill Issues

### Skill Not Auto-Loading

**Symptom:** Pre-commit checklist doesn't appear when committing.

**Solutions:**

1. **Check trigger words:**
   - Open skill file
   - Verify "Triggers on:" includes your phrase
   - Try exact trigger phrase

2. **Check skill description:**
   - Description must contain trigger keywords
   - First paragraph is used for matching

3. **Skill file corrupted:**
   - Compare with template
   - Re-copy if needed

### Skill Conflicts

**Symptom:** Multiple skills activating unexpectedly.

**Solution:**
- Make trigger words more specific
- Edit skill descriptions to be more unique

---

## MCP Server Issues

### Server Not Starting

**Symptom:** "use context7" doesn't work.

**Diagnosis:**
```bash
# Check Node.js
node --version    # Need 18+
npx --version     # Should exist

# Check settings file exists
cat ~/.claude/settings.json
```

**Solutions:**

1. **JSON syntax error:**
   ```bash
   # Validate JSON
   cat ~/.claude/settings.json | python -m json.tool
   ```

2. **Wrong file location:**
   - System-wide: `~/.claude/settings.json`
   - Per-project: `.claude/settings.json`

3. **Server not installed:**
   ```bash
   # Test manually
   npx -y @context7/mcp-server
   ```

4. **Restart required:**
   - Close Claude Code completely
   - Reopen

### Environment Variable Not Working

**Symptom:** GitHub MCP says "unauthorized"

**Diagnosis:**
```bash
# Check variable is set
echo $GITHUB_TOKEN    # macOS/Linux
echo $env:GITHUB_TOKEN  # Windows PowerShell
```

**Solutions:**

1. **Variable not set:**
   - Follow MCP_SERVERS.md instructions
   - Set permanently (not just in current session)

2. **Wrong syntax in config:**
   ```json
   // Correct
   "env": { "GITHUB_TOKEN": "${GITHUB_TOKEN}" }

   // Wrong
   "env": { "GITHUB_TOKEN": "$GITHUB_TOKEN" }
   ```

3. **Restart terminal:**
   - After setting variable, restart terminal
   - Then restart Claude Code

### MCP Timeout

**Symptom:** MCP calls hang or timeout.

**Solutions:**

1. **Network issues:**
   - Check internet connection
   - Check firewall settings

2. **Server crashed:**
   - Restart Claude Code
   - Check for server updates

---

## Hook Issues

### Hook Not Running

**Symptom:** Prettier doesn't run after edits.

**Diagnosis:**
```bash
# Check settings.json has hooks
cat .claude/settings.json | grep -A 10 "hooks"
```

**Solutions:**

1. **Hook syntax wrong:**
   ```json
   // Correct structure
   {
     "hooks": {
       "PostToolUse": [
         {
           "matcher": "...",
           "hooks": [{ "type": "command", "command": "..." }]
         }
       ]
     }
   }
   ```

2. **Matcher not matching:**
   - Test matcher pattern
   - Check file extensions are correct

3. **Command failing silently:**
   ```bash
   # Test command manually
   npx prettier --write test.ts
   ```

### Hook Blocking Operations

**Symptom:** Edits fail or operations hang.

**Solutions:**

1. **Hook command failing:**
   - Check hook command works manually
   - Add `|| true` to non-critical hooks

2. **Infinite loop:**
   - Hook triggers itself
   - Add conditions to prevent re-trigger

---

## Git Issues

### Commit Blocked

**Symptom:** Can't commit, pre-commit fails.

**Solutions:**

1. **Check what's failing:**
   - Run pre-commit checks manually
   - Fix reported issues

2. **Debug statements:**
   ```bash
   grep -rn "console.log" src/
   ```

3. **Test failures:**
   ```bash
   npm test
   ```

### Push Blocked

**Symptom:** Force push blocked by hook.

**This is intentional.** To override:
- Explicitly confirm force push is needed
- Or disable hook temporarily

### Merge Conflicts

**Solution:**
```bash
# See conflicts
git status

# Resolve manually
# Then:
git add <resolved-files>
git commit
```

---

## Performance Issues

### Claude Code Slow

**Causes & Solutions:**

1. **Large PROJECT_MAP.md:**
   - Regenerate with `/map-project`
   - Reduce depth/detail

2. **Too many skills loading:**
   - Check skill triggers aren't too broad
   - Make triggers more specific

3. **MCP servers slow:**
   - Check network connection
   - Consider disabling unused servers

### High Token Usage

**Solutions:**

1. **Use appropriate models:**
   - Haiku for simple tasks
   - Check model-routing skill

2. **Reduce context:**
   - Keep CLAUDE.md slim
   - Use on-demand skills

3. **Clear conversation:**
   - Start new conversation for new tasks

---

## Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| Nothing works | Restart Claude Code |
| Command missing | Check `.claude/commands/` |
| Skill not loading | Check trigger keywords |
| MCP not working | Check `~/.claude/settings.json` |
| Hook not running | Check JSON syntax |
| Permission denied | Check file permissions |
| Slow performance | Reduce context, use Haiku |

---

## Getting More Help

### Debug Mode

Add to conversation:
```
Show me verbose debug information for this operation
```

### Check Logs

Claude Code may log errors to:
- Terminal output
- Browser console (if applicable)

### Compare with Template

```bash
diff -r .claude C:\scripts\prompts\template\.claude
```

### Fresh Start

If all else fails:
```bash
# Backup and reinstall
mv .claude .claude.broken
cp -r C:\scripts\prompts\template\.claude .claude
```

---

---

## v2.0 Features

### YAML Frontmatter Issues

#### Skill Not Recognized After Adding Frontmatter

**Symptom:** Skill doesn't trigger after adding YAML frontmatter.

**Solutions:**

1. **Check YAML syntax:**
   ```bash
   # Validate YAML (requires yq or python)
   head -20 .claude/skills/my-skill.md | yq .
   ```

2. **Verify frontmatter format:**
   ```yaml
   ---
   name: "Skill Name"      # Required: string
   description: "What it does"  # Required: string
   version: "1.0.0"        # Required: semver
   triggers:               # Required: array
     - "trigger phrase"
   model: "sonnet"         # Optional: haiku|sonnet|opus
   ---
   ```

3. **Check for common errors:**
   - Missing closing `---`
   - Tabs instead of spaces
   - Missing quotes around strings with colons
   - Invalid YAML characters in values

4. **Test with skill-lint:**
   ```bash
   ./.claude/scripts/validate/skill-lint.sh .claude/skills/my-skill.md
   ```

#### disable_model_invocation Not Working

**Symptom:** Reference-only skill still uses API calls.

**Solution:**
```yaml
---
disable_model_invocation: true  # Must be boolean, not string
---
```

---

### Rules Issues

#### Rule Not Loading

**Symptom:** `@rules/security` doesn't provide expected guidance.

**Solutions:**

1. **Check rule exists:**
   ```bash
   ls .claude/rules/security.md
   ```

2. **Verify exact syntax:**
   ```
   # Correct
   @rules/security

   # Wrong
   @rule/security
   @rules/security.md
   rules/security
   ```

3. **Check rule content:**
   - File must be valid markdown
   - Should have clear sections

4. **Restart Claude Code:**
   - Rules load at startup

#### Multiple Rules Conflict

**Symptom:** Contradictory guidance from multiple rules.

**Solution:**
- Load rules in order of priority
- More specific rules should come last
- Example: `@rules/code-quality` then `@rules/security`

---

### Agent Issues

#### Agent Not Spawning

**Symptom:** "Spawn code-reviewer agent" doesn't work.

**Solutions:**

1. **Check agent exists:**
   ```bash
   ls .claude/agents/code-reviewer.md
   ```

2. **Verify agent format:**
   ```yaml
   ---
   name: "Agent Name"
   model: "sonnet"
   context: "fork"
   expertise:
     - "Area 1"
   ---
   ```

3. **Use exact spawn syntax:**
   ```
   Spawn code-reviewer agent to [task]
   ```

4. **Check available agents:**
   ```bash
   cat .claude/agents/_index.md
   ```

#### Agent Returns Empty Response

**Symptom:** Spawned agent completes but returns nothing useful.

**Solutions:**

1. **Provide clear task:**
   ```
   # Bad
   Spawn researcher

   # Good
   Spawn researcher agent to investigate caching options for our Node.js API
   ```

2. **Check model availability:**
   - Opus agents require Opus access
   - Fall back to sonnet if needed

---

### Command Arguments Issues

#### Arguments Not Parsed

**Symptom:** `/review src/api --deep` ignores arguments.

**Solutions:**

1. **Check command supports arguments:**
   ```yaml
   ---
   arguments: true  # Must be enabled
   ---
   ```

2. **Verify argument syntax:**
   ```
   # Positional
   /review src/api           # $1 = src/api

   # Named flags
   /review --deep            # --deep flag set
   /review --coverage=90     # --coverage = "90"

   # Combined
   /review src/api --deep --coverage=90
   ```

3. **Check command file for $ARGUMENTS:**
   ```bash
   grep -n "ARGUMENTS\|\\$0\|\\$1" .claude/commands/review.md
   ```

#### Flag Not Recognized

**Symptom:** `--dry-run` flag is ignored.

**Solutions:**

1. **Use correct syntax:**
   ```
   # Correct
   --dry-run
   --coverage=90

   # Wrong
   -dry-run
   --coverage 90
   ```

2. **Check supported flags in command:**
   - Each command documents its supported flags
   - Unsupported flags are ignored silently

---

### Extended Thinking Issues

#### Ultrathink Not Activating

**Symptom:** "ultrathink" doesn't trigger extended thinking.

**Solutions:**

1. **Use correct phrases:**
   ```
   ultrathink this problem
   use extended thinking
   /secure --ultrathink
   ```

2. **Check skill has it enabled:**
   ```yaml
   ---
   extended_thinking: true
   ---
   ```

3. **Verify model supports it:**
   - Extended thinking works best with Opus
   - May have reduced effect with Sonnet/Haiku

#### Extended Thinking Too Slow

**Symptom:** Ultrathink takes very long.

**Solutions:**

1. **Use only for complex problems:**
   - Security audits
   - Architecture decisions
   - Incident postmortems

2. **Don't use for:**
   - Simple questions
   - Straightforward tasks
   - Quick lookups

---

### Context Fork Issues

#### Forked Research Returns Nothing

**Symptom:** "Research in background" completes but has no results.

**Solutions:**

1. **Be specific about what to return:**
   ```
   # Bad
   Research in background: how does auth work?

   # Good
   Research in background: how does auth work? Return a summary of the auth flow with key files involved.
   ```

2. **Check for context isolation:**
   - Forked agents don't see your current conversation
   - Include all necessary context in the request

#### Fork Pollutes Main Context

**Symptom:** Research details appear in main conversation.

**Solution:**
- This is expected for summary
- Use "research in background" to get summary only
- Full details stay in forked context

---

### CI/CD Script Issues

#### Script Permission Denied

**Symptom:** `./scripts/ci/pr-review.sh: Permission denied`

**Solution:**
```bash
chmod +x .claude/scripts/ci/*.sh
chmod +x .claude/scripts/validate/*.sh
```

#### Script Not Finding Claude

**Symptom:** `claude: command not found` in CI.

**Solutions:**

1. **Install Claude Code in CI:**
   ```yaml
   - name: Install Claude Code
     run: npm install -g @anthropic-ai/claude-code
   ```

2. **Set API key:**
   ```yaml
   env:
     ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
   ```

3. **Verify path:**
   ```bash
   which claude
   claude --version
   ```

#### CI Script Timeout

**Symptom:** CI script hangs or times out.

**Solutions:**

1. **Add timeout to script:**
   ```bash
   timeout 300 claude -p "..." || echo "Timed out"
   ```

2. **Use smaller scope:**
   ```bash
   # Instead of full review
   ./scripts/ci/pr-review.sh src/changed-file.ts
   ```

---

### Upgrade Issues

#### v1.x Skills Not Working After v2.0 Upgrade

**Symptom:** Skills from v1.x stop working.

**Solutions:**

1. **Add required frontmatter:**
   ```yaml
   ---
   name: "Skill Name"
   description: "What it does"
   version: "1.0.0"
   triggers:
     - "trigger phrase"
   ---

   [Original skill content]
   ```

2. **Or copy updated skills:**
   ```bash
   cp C:\scripts\prompts\template\.claude\skills\*.md .claude\skills\
   ```

#### Missing v2.0 Directories

**Symptom:** Rules/agents/scripts directories don't exist.

**Solution:**
```bash
# Create directories
mkdir -p .claude/rules
mkdir -p .claude/agents
mkdir -p .claude/scripts/ci
mkdir -p .claude/scripts/validate

# Copy from template
cp -r C:\scripts\prompts\template\.claude\rules\* .claude\rules\
cp -r C:\scripts\prompts\template\.claude\agents\* .claude\agents\
cp -r C:\scripts\prompts\template\.claude\scripts\* .claude\scripts\
```

---

### Autonomous Loop Issues

#### Loop Stuck / Not Progressing

**Symptom:** Loop runs same iteration repeatedly without progress.

**Solutions:**

1. **Stall detection should trigger:**
   - After 3 iterations with no change, loop pauses
   - Check LOOP_STATE.md for stuck items

2. **Circular dependency:**
   - Fix A requires B, B requires A
   - Break the cycle manually

3. **External dependency:**
   - Waiting for API key, service, or user input
   - Provide missing resource

#### Loop Won't Stop

**Symptom:** Loop keeps finding new issues.

**Solutions:**

1. **This is expected behavior:**
   - Loop continues until work queue empty
   - New discoveries are added to queue

2. **Set iteration limit:**
   ```
   /loop --max-iterations=20
   ```

3. **Stop manually:**
   - Say "stop loop" or "pause"
   - Ctrl+C

#### Conda Warning During Loop

**Symptom:** Loop pauses with conda environment warning.

**Solution:**
```bash
# Create project environment
conda create -n myproject python=3.11 -y
conda activate myproject

# Then resume
"continue loop"
```

#### New Features Not Being Worked On

**Symptom:** Added feature request but loop doesn't pick it up.

**Solutions:**

1. **Explicitly add to queue:**
   ```
   Add "implement user caching" to the work queue
   ```

2. **Check priority:**
   - New features are lower priority than bugs
   - Loop finishes S0-S2 issues first

---

## Swarm Mode Issues (v4.1)

### Swarm Not Starting

**Symptom:** `--swarm` flag is ignored, runs in standard mode.

**Solutions:**

1. **Check flag syntax:**
   ```
   # Correct
   /cc-loop --swarm "task description"

   # Wrong
   /cc-loop -swarm "task"
   /cc-loop --swarm=true "task"
   ```

2. **Task must be decomposable:**
   - Swarm works for independent subtasks
   - Single complex tasks use standard mode

3. **Minimum task count:**
   - Swarm activates for 5+ independent tasks
   - Fewer tasks use standard mode

### Workers Not Claiming Tasks

**Symptom:** Workers spawned but tasks stay pending.

**Solutions:**

1. **Check for blocking dependencies:**
   - All tasks might be blocked
   - Complete blocking tasks first

2. **Verify task pool:**
   - Check LOOP_STATE.md for task status
   - Ensure tasks have `pending` status

3. **Worker count issue:**
   ```
   # Explicitly set workers
   /cc-loop --swarm --workers=3 "task"
   ```

### Task Dependencies Not Unblocking

**Symptom:** Completed task doesn't unblock dependent tasks.

**Solutions:**

1. **Verify dependency syntax:**
   ```markdown
   | ID | Task | Blocked By | Blocks |
   | T001 | First | — | T002 |
   | T002 | Second | T001 | — |
   ```

2. **Check task marked complete:**
   - Status must be exactly `complete`
   - Not `done`, `finished`, etc.

3. **Circular dependency:**
   - T001 blocks T002, T002 blocks T001
   - Break the cycle manually

### Swarm Workers Conflicting

**Symptom:** Multiple workers modify same file, causing conflicts.

**Solutions:**

1. **Don't use swarm for:**
   - Tasks that modify same files
   - Tightly coupled changes
   - Sequential pipelines

2. **Use standard mode instead:**
   - Remove `--swarm` flag
   - Let coordinator manage sequencing

3. **Split by concern:**
   - Each worker gets separate files/modules
   - Verify no file overlap in task pool

### Plan Approval Blocking Progress

**Symptom:** Loop stuck waiting for approval.

**Solutions:**

1. **Check for pending approvals:**
   - Look for "Approval Required" messages
   - Review and approve/reject the plan

2. **Configure auto-approval:**
   - See `.claude/settings.json` for thresholds
   - Adjust risk tolerance if needed

3. **Skip approval (not recommended):**
   - Only for trusted, non-production work
   - Approve plan to continue

### Swarm Mode Slow

**Symptom:** Swarm mode takes longer than expected.

**Solutions:**

1. **Too many workers:**
   - More workers ≠ faster
   - Try `--workers=2` or `--workers=3`

2. **Task overhead:**
   - Small tasks have spawn overhead
   - Batch tiny tasks together

3. **Dependencies create bottleneck:**
   - One blocking task holds up pipeline
   - Prioritize bottleneck tasks

---

## v4.1 Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| Swarm not starting | Check `--swarm` flag syntax |
| Workers idle | Check for blocked dependencies |
| Tasks not unblocking | Verify task marked as `complete` |
| Workers conflicting | Don't use swarm for same-file changes |
| Approval blocking | Review and approve pending plans |
| Swarm slow | Reduce worker count with `--workers=2` |
| Circular dependency | Break cycle in LOOP_STATE.md manually |

---

## v2.0 Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| YAML invalid | Run skill-lint.sh |
| Rule not loading | Check @rules/ syntax |
| Agent not spawning | Verify agent file exists |
| Arguments ignored | Add `arguments: true` to frontmatter |
| Ultrathink slow | Use only for complex problems |
| Fork returns empty | Include expected output format |
| CI script fails | Check permissions and API key |
| v1.x skill broken | Add YAML frontmatter |
| Loop stuck | Check LOOP_STATE.md, break cycles |
| Loop won't stop | Use --max-iterations or "stop loop" |
| Conda warning | Activate project environment first |

---

## Plugin Issues (v4.2)

### Plugin Not Found During Install

**Symptom:** `claude plugin install` says plugin not found.

**Solutions:**

1. **Add marketplace first:**
   ```bash
   claude plugin marketplace add supermemoryai/claude-supermemory
   claude plugin install claude-supermemory
   ```

2. **Check marketplace added:**
   ```bash
   claude plugin marketplace list
   ```

### Supermemory API Key Not Working

**Symptom:** "Unauthorized" or "Invalid API key" errors.

**Solutions:**

1. **Verify key format:**
   - Must start with `sm_`
   - Get from [console.supermemory.ai](https://console.supermemory.ai)

2. **Check environment variable (Windows PowerShell):**
   ```powershell
   $env:SUPERMEMORY_CC_API_KEY
   ```

3. **Check environment variable (macOS/Linux):**
   ```bash
   echo $SUPERMEMORY_CC_API_KEY
   ```

4. **Set correctly (Windows PowerShell):**
   ```powershell
   [Environment]::SetEnvironmentVariable("SUPERMEMORY_CC_API_KEY", "sm_your_key", "User")
   ```

5. **Set correctly (macOS/Linux):**
   ```bash
   echo 'export SUPERMEMORY_CC_API_KEY="sm_your_key"' >> ~/.zshrc
   source ~/.zshrc
   ```

6. **Restart terminal and Claude Code** after setting

### Plugin Enabled But Not Working

**Symptom:** Plugin shows enabled but features don't activate.

**Solutions:**

1. **Restart Claude Code:**
   - Plugins load hooks at startup
   - Close completely and reopen

2. **Verify plugin status:**
   ```bash
   claude plugin list
   ```

3. **Check for errors:**
   - Set debug mode: `SUPERMEMORY_DEBUG=true`
   - Look for errors in Claude Code output

### Memories Not Loading on Session Start

**Symptom:** No memory context injected.

**Solutions:**

1. **Build up memories first:**
   - Have a few conversations
   - Memories need content to recall

2. **Index your codebase:**
   ```
   /claude-supermemory:index
   ```

3. **Check API connectivity:**
   - Verify internet connection
   - Check API key is valid

### Plugin Command Not Found

**Symptom:** `/claude-supermemory:index` doesn't work.

**Solutions:**

1. **Check plugin is installed:**
   ```bash
   claude plugin list
   ```

2. **Check plugin is enabled:**
   ```bash
   claude plugin enable claude-supermemory
   ```

3. **Restart Claude Code**

---

## v4.2 Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| Plugin not found | Add marketplace first |
| API key invalid | Check starts with `sm_`, restart terminal |
| Plugin not working | Restart Claude Code |
| No memories loading | Index codebase first |
| Command not found | Check plugin enabled, restart |

---

## Reporting Issues

If you find a bug in the template:

1. Check if it's a known issue
2. Try with fresh template to confirm
3. Document steps to reproduce
4. Report with:
   - Template version (check `.claude/.version`)
   - Platform (Windows/macOS/Linux)
   - Error message
   - Steps to reproduce
