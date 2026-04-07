# Best Practice Enhancements Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrate 13 enhancement opportunities identified from comparing Claude Sentient with shanraisshan/claude-code-best-practice into the project — covering notification hooks, batch/loop integration, CLAUDE.local.md, agent memory, commit strategies, worktree-first teams, MCP recommendations, browser verification, cross-model workflows, progressive skill disclosure, native command documentation, bare flag optimization, and skill config.

**Architecture:** Each enhancement is an independent task modifying existing commands, hooks, skills, agents, or documentation. No new external dependencies. All changes follow the existing XML command structure, CJS hook pattern, and YAML agent frontmatter conventions. Tests are added to existing test suites using the shared `test-utils.js` infrastructure.

**Tech Stack:** Node.js (CJS hooks), Markdown (commands/skills/docs), YAML frontmatter (agents), JSON (schemas/settings), Bash/PowerShell (installers)

---

## File Structure

### New Files
| File | Responsibility |
|------|---------------|
| `.claude/hooks/notification.cjs` | Optional audio/visual notifications for hook lifecycle events |
| `.claude/hooks/__tests__/test-notification.js` | Tests for notification hook |
| `.claude/commands/cs-batch.md` | Fan-out tasks to parallel worktree agents |
| `.claude/commands/cs-schedule.md` | Recurring autonomous work via native /schedule |
| `templates/CLAUDE.local.md` | Template for personal preferences (gitignored) |
| `.claude/skills/team-orchestration/references/worktree-strategy.md` | Worktree-first team mode reference |
| `.claude/skills/quality-gates/references/commit-strategies.md` | Per-file, per-task, atomic commit strategies |
| `.claude/skills/profile-detection/references/cross-model.md` | Claude + Codex cross-model workflow reference |
| `documentation/16-native-tips.md` | Documentation for /btw, /branch, /voice, /loop, /batch, --bare |

### Modified Files
| File | What Changes |
|------|-------------|
| `templates/settings.json` | Add Notification hook entry |
| `install.sh` | Copy notification hook, create CLAUDE.local.md template |
| `install.ps1` | Mirror install.sh changes |
| `.claude/agents/architect.md` | Add `memory:` frontmatter section |
| `.claude/agents/backend.md` | Add `memory:` frontmatter section |
| `.claude/agents/frontend.md` | Add `memory:` frontmatter section |
| `.claude/agents/database.md` | Add `memory:` frontmatter section |
| `.claude/agents/security.md` | Add `memory:` frontmatter section |
| `.claude/agents/tester.md` | Add `memory:` frontmatter section |
| `.claude/agents/devops.md` | Add `memory:` frontmatter section |
| `.claude/agents/docs.md` | Add `memory:` frontmatter section |
| `.claude/agents/build-resolver.md` | Add `memory:` frontmatter section |
| `.claude/commands/cs-loop.md` | Add commit strategy selection to COMMIT phase, add /btw note to EXECUTE |
| `.claude/commands/cs-mcp.md` | Add DeepWiki, Excalidraw, Playwright to known servers reference |
| `.claude/commands/cs-team.md` | Add worktree-first default strategy |
| `.claude/skills/team-orchestration/SKILL.md` | Add worktree-per-teammate section |
| `.claude/skills/profile-detection/SKILL.md` | Add CLAUDE.local.md detection, cross-model workflow reference |
| `.claude/skills/quality-gates/SKILL.md` | Add commit strategy and browser verification references |
| `CLAUDE.md` | Add cs-batch, cs-schedule to commands table; add Native Tips reference; bump version |
| `.claude/hooks/utils.cjs` | Add `getNotificationConfig()` utility |
| `CHANGELOG.md` | Add v1.6.0 entry |
| `STATUS.md` | Update component counts |

---

## Task 1: Notification Hook System

**Why this matters:** When `/cs-loop` runs autonomously for minutes, users need feedback on completions, gate failures, and errors. The best-practice repo implements audio notifications for all 25 hook events — we add a lighter, configurable version.

**Files:**
- Create: `.claude/hooks/notification.cjs`
- Create: `.claude/hooks/__tests__/test-notification.js`
- Modify: `templates/settings.json`
- Modify: `.claude/hooks/utils.cjs`
- Modify: `install.sh` (copy section summary line)
- Modify: `install.ps1` (mirror)

- [ ] **Step 1: Write failing tests for notification hook**

Create `.claude/hooks/__tests__/test-notification.js`:

```javascript
#!/usr/bin/env node
const assert = require('assert');
const { test, suite, summary, getResults } = require('../../../test-utils');
const path = require('path');
const fs = require('fs');

suite('notification hook');

test('module loads without error', () => {
    const hookPath = path.join(__dirname, '..', 'notification.cjs');
    const mod = require(hookPath);
    assert.ok(mod);
});

test('buildDesktopCommand returns string for linux', () => {
    const { buildDesktopCommand } = require(path.join(__dirname, '..', 'notification.cjs'));
    if (process.platform === 'linux') {
        const cmd = buildDesktopCommand('Test Title', 'Test Body');
        assert.ok(cmd.includes('notify-send'));
    }
});

test('buildDesktopCommand returns string for darwin', () => {
    const { buildDesktopCommand } = require(path.join(__dirname, '..', 'notification.cjs'));
    if (process.platform === 'darwin') {
        const cmd = buildDesktopCommand('Test Title', 'Test Body');
        assert.ok(cmd.includes('osascript'));
    }
});

test('buildDesktopCommand escapes single quotes in title', () => {
    const { buildDesktopCommand } = require(path.join(__dirname, '..', 'notification.cjs'));
    const cmd = buildDesktopCommand("It's done", 'Body');
    assert.ok(cmd); // Should not throw
    assert.ok(!cmd.includes("It's done")); // Quotes should be escaped
});

test('resolveEvent maps PostToolUse with non-zero exit to gate-failure', () => {
    const { resolveEvent } = require(path.join(__dirname, '..', 'notification.cjs'));
    const result = resolveEvent('PostToolUse', { exit_code: 1 });
    assert.strictEqual(result, 'gate-failure');
});

test('resolveEvent maps PostToolUse with exit 0 to PostToolUse', () => {
    const { resolveEvent } = require(path.join(__dirname, '..', 'notification.cjs'));
    const result = resolveEvent('PostToolUse', { exit_code: 0 });
    assert.strictEqual(result, 'PostToolUse');
});

test('resolveEvent maps TaskCompleted to task-completed', () => {
    const { resolveEvent } = require(path.join(__dirname, '..', 'notification.cjs'));
    assert.strictEqual(resolveEvent('TaskCompleted', {}), 'task-completed');
});

test('resolveEvent maps SessionEnd to session-end', () => {
    const { resolveEvent } = require(path.join(__dirname, '..', 'notification.cjs'));
    assert.strictEqual(resolveEvent('SessionEnd', {}), 'session-end');
});

test('resolveEvent passes Stop through unchanged', () => {
    const { resolveEvent } = require(path.join(__dirname, '..', 'notification.cjs'));
    assert.strictEqual(resolveEvent('Stop', {}), 'Stop');
});

test('resolveEvent passes unknown events through', () => {
    const { resolveEvent } = require(path.join(__dirname, '..', 'notification.cjs'));
    assert.strictEqual(resolveEvent('SubagentStart', {}), 'SubagentStart');
});

test('getNotificationConfig returns null for nonexistent path', () => {
    const { getNotificationConfig } = require(path.join(__dirname, '..', 'utils.cjs'));
    const config = getNotificationConfig('/nonexistent/path/that/does/not/exist');
    assert.strictEqual(config, null);
});

test('getNotificationConfig returns null when disabled', () => {
    const { getNotificationConfig } = require(path.join(__dirname, '..', 'utils.cjs'));
    const tmpDir = fs.mkdtempSync(path.join(require('os').tmpdir(), 'cs-notify-'));
    const stateDir = path.join(tmpDir, '.claude', 'state');
    fs.mkdirSync(stateDir, { recursive: true });
    fs.writeFileSync(path.join(stateDir, 'notification-config.json'), JSON.stringify({
        enabled: false,
        type: 'bell',
        events: { Stop: true }
    }));
    const config = getNotificationConfig(tmpDir);
    assert.strictEqual(config, null);
    fs.rmSync(tmpDir, { recursive: true, force: true });
});

test('getNotificationConfig returns config when enabled', () => {
    const { getNotificationConfig } = require(path.join(__dirname, '..', 'utils.cjs'));
    const tmpDir = fs.mkdtempSync(path.join(require('os').tmpdir(), 'cs-notify-'));
    const stateDir = path.join(tmpDir, '.claude', 'state');
    fs.mkdirSync(stateDir, { recursive: true });
    const expected = { enabled: true, type: 'bell', events: { Stop: true } };
    fs.writeFileSync(path.join(stateDir, 'notification-config.json'), JSON.stringify(expected));
    const config = getNotificationConfig(tmpDir);
    assert.deepStrictEqual(config, expected);
    fs.rmSync(tmpDir, { recursive: true, force: true });
});

summary();
const results = getResults();
process.exit(results.failed > 0 ? 1 : 0);
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `bash --norc --noprofile -c "node .claude/hooks/__tests__/test-notification.js" 2>/dev/null`
Expected: FAIL — module not found

- [ ] **Step 3: Add getNotificationConfig to utils.cjs**

In `.claude/hooks/utils.cjs`, add before the `module.exports` line:

```javascript
/**
 * Load notification configuration from state directory.
 * @param {string} [projectRoot] - Optional project root override
 * @returns {object|null} Config object or null if not configured/disabled
 */
function getNotificationConfig(projectRoot) {
    try {
        const root = projectRoot || getProjectRoot();
        const configPath = path.join(root, '.claude', 'state', 'notification-config.json');
        if (!fs.existsSync(configPath)) return null;
        const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
        if (!config || !config.enabled) return null;
        return config;
    } catch (_) {
        return null;
    }
}
```

Add `getNotificationConfig` to the `module.exports` object.

- [ ] **Step 4: Implement the notification hook**

Create `.claude/hooks/notification.cjs`:

```javascript
#!/usr/bin/env node
/**
 * Notification Hook - Optional audio/visual feedback for Claude Sentient lifecycle events
 *
 * Configuration: .claude/state/notification-config.json
 * {
 *   "enabled": true,
 *   "type": "bell" | "desktop" | "command",
 *   "command": "custom-command {title} {body}",  // only for type: command
 *   "events": { "Stop": true, "gate-failure": true, "task-completed": true, "session-end": true }
 * }
 */

const path = require('path');
const { getNotificationConfig, parseHookInput, getProjectRoot } = require('./utils.cjs');

const EVENT = process.env.HOOK_EVENT || '';

/**
 * Build a desktop notification command for the current platform.
 * @param {string} title - Notification title
 * @param {string} body - Notification body
 * @returns {string|null} Shell command or null if unsupported
 */
function buildDesktopCommand(title, body) {
    const safeTitle = title.replace(/'/g, "'\\''");
    const safeBody = body.replace(/'/g, "'\\''");
    if (process.platform === 'linux') {
        return "notify-send '" + safeTitle + "' '" + safeBody + "' 2>/dev/null || true";
    }
    if (process.platform === 'darwin') {
        return 'osascript -e \'display notification "' + safeBody.replace(/"/g, '\\"') + '" with title "' + safeTitle.replace(/"/g, '\\"') + '"\' 2>/dev/null || true';
    }
    if (process.platform === 'win32') {
        return 'powershell -Command "Add-Type -AssemblyName System.Windows.Forms; $n=New-Object System.Windows.Forms.NotifyIcon; $n.Icon=[System.Drawing.SystemIcons]::Information; $n.Visible=$true; $n.ShowBalloonTip(3000,\'' + safeTitle + '\',\'' + safeBody + '\',[System.Windows.Forms.ToolTipIcon]::Info)" 2>nul || exit /b 0';
    }
    return null;
}

/**
 * Resolve the effective event name from the raw HOOK_EVENT + input context.
 * @param {string} event - Raw HOOK_EVENT
 * @param {object} input - Parsed HOOK_INPUT
 * @returns {string} Effective event name
 */
function resolveEvent(event, input) {
    if (event === 'PostToolUse' && input && input.exit_code && input.exit_code !== 0) {
        return 'gate-failure';
    }
    if (event === 'TaskCompleted') return 'task-completed';
    if (event === 'SessionEnd') return 'session-end';
    return event;
}

/**
 * Send a notification based on config type.
 * @param {object} config - Notification configuration
 * @param {string} title - Notification title
 * @param {string} body - Notification body
 */
function notify(config, title, body) {
    const { execFileSync } = require('child_process');
    switch (config.type) {
        case 'bell':
            process.stdout.write('\x07');
            break;
        case 'desktop': {
            const cmd = buildDesktopCommand(title, body);
            if (cmd) {
                try {
                    // Use shell: true since we need platform-specific shell syntax
                    require('child_process').execSync(cmd, { timeout: 3000, stdio: 'ignore' });
                } catch (_) {}
            }
            break;
        }
        case 'command':
            if (config.command) {
                const parts = config.command.replace('{title}', title).replace('{body}', body).split(' ');
                try {
                    execFileSync(parts[0], parts.slice(1), { timeout: 3000, stdio: 'ignore' });
                } catch (_) {}
            }
            break;
        default:
            process.stdout.write('\x07');
    }
}

function main() {
    const config = getNotificationConfig();
    if (!config) process.exit(0);

    let input = {};
    try { input = parseHookInput(); } catch (_) {}

    const effectiveEvent = resolveEvent(EVENT, input);

    if (!config.events || !config.events[effectiveEvent]) {
        process.exit(0);
    }

    const titles = {
        'Stop': 'Claude Sentient: Done',
        'gate-failure': 'Claude Sentient: Gate Failed',
        'task-completed': 'Claude Sentient: Task Complete',
        'session-end': 'Claude Sentient: Session Ended'
    };
    const bodies = {
        'Stop': 'Work loop completed.',
        'gate-failure': 'Gate failed (exit ' + (input.exit_code || '?') + ')',
        'task-completed': 'A task was marked complete.',
        'session-end': 'Session has ended.'
    };

    notify(config, titles[effectiveEvent] || 'Claude Sentient: ' + effectiveEvent, bodies[effectiveEvent] || effectiveEvent);
}

main();

module.exports = { buildDesktopCommand, resolveEvent, notify };
```

- [ ] **Step 5: Add notification hook to settings template**

In `templates/settings.json`, add a `"Notification"` entry to the hooks object:

```json
"Notification": [
    {
        "hooks": [
            {
                "type": "command",
                "command": "node .claude/hooks/notification.cjs",
                "timeout": 3000,
                "async": true
            }
        ]
    }
]
```

- [ ] **Step 6: Update install.sh summary line**

In `install.sh`, after `echo "  Installed hook scripts + tests"`, add:

```bash
echo "  Includes notification hook (configure via notification-config.json)"
```

Mirror in `install.ps1`.

- [ ] **Step 7: Run tests to verify they pass**

Run: `bash --norc --noprofile -c "node .claude/hooks/__tests__/test-notification.js" 2>/dev/null`
Expected: All tests PASS

- [ ] **Step 8: Commit**

Write to `/tmp/commit-msg.txt`: `feat: add optional notification hook for lifecycle events`

```bash
git add .claude/hooks/notification.cjs .claude/hooks/__tests__/test-notification.js .claude/hooks/utils.cjs templates/settings.json install.sh install.ps1
git commit -F /tmp/commit-msg.txt
```

---

## Task 2: /cs-batch and /cs-schedule Commands

**Why this matters:** Boris Cherny calls `/loop` and `/schedule` "the most powerful features" of Claude Code. `/cs-batch` fans out plan tasks to parallel worktree agents. `/cs-schedule` wraps native `/schedule` for recurring autonomous work like nightly audits.

**Files:**
- Create: `.claude/commands/cs-batch.md`
- Create: `.claude/commands/cs-schedule.md`
- Modify: `CLAUDE.md` (commands table)
- Modify: `.claude/commands/CLAUDE.md` (command inventory)

- [ ] **Step 1: Create /cs-batch command**

Create `.claude/commands/cs-batch.md`:

```markdown
---
description: Fan out plan tasks to parallel worktree agents
argument-hint: [plan-file | task-description]
allowed-tools: Read, Bash, Glob, Grep, Task, TaskCreate, TaskUpdate, TaskList, TaskGet, EnterWorktree, ExitWorktree, AskUserQuestion, Skill
---

# /cs-batch

<role>
You are a parallel work orchestrator. You decompose tasks into independent work streams and fan them out to isolated worktree agents for maximum throughput.
</role>

<task>
Take a plan (from /cs-plan output or a task description) and distribute independent tasks across parallel git worktree agents. Each agent works in isolation on its own branch, then results are merged back.
</task>

<steps>
## Phase 1: Load or Create Plan

1. If argument is a file path, read it as a plan document
2. If argument is a task description, run `Skill(skill="cs-plan", args="<task>")` first
3. Extract independent task groups (tasks with no `blockedBy` dependencies between groups)

## Phase 2: Partition into Work Streams

1. Group tasks by file scope independence (no overlapping files)
2. Each group becomes a work stream
3. Report: `[BATCH] {n} work streams identified from {total} tasks`

## Phase 3: Fan Out

For each work stream:
1. Create a worktree branch: `git worktree add -b batch/{stream-id} .worktrees/batch-{stream-id}`
2. Use `EnterWorktree` to enter the isolated workspace
3. Spawn a subagent with the stream's task list and `/cs-loop` instructions
4. The subagent works autonomously through its tasks with quality gates

## Phase 4: Collect Results

1. Wait for all worktree agents to complete
2. For each completed stream:
   - Review changes via `git diff main...batch/{stream-id}`
   - Run quality gates on the combined result
   - If gates pass, merge: `git merge batch/{stream-id} --no-ff`
3. Clean up worktrees: `git worktree remove .worktrees/batch-{stream-id}`

## Phase 5: Report

```
[BATCH] Complete:
  Streams: {n} dispatched, {passed} merged, {failed} need attention
  Commits: {total} across all streams
  Files: {files} modified
```
</steps>

<constraints>
- Maximum 5 concurrent worktree agents (prevent resource exhaustion)
- Each agent must pass quality gates independently before merge
- Merge conflicts trigger `AskUserQuestion` for resolution strategy
- If any stream fails gates after 2 retries, park it and continue others
</constraints>

<avoid>
- Don't batch tasks that have cross-dependencies — those must be sequential
- Don't create worktrees for single-file tasks — overhead isn't worth it
- Don't merge without running gates on the combined result
</avoid>
```

- [ ] **Step 2: Create /cs-schedule command**

Create `.claude/commands/cs-schedule.md`:

```markdown
---
description: Create recurring autonomous agents via native /schedule
argument-hint: <cron-expression> <command> [args]
allowed-tools: Bash, Read, AskUserQuestion, Skill
---

# /cs-schedule

<role>
You are a scheduling assistant that helps configure recurring Claude Code agents using the native `/schedule` feature. You translate user intent into cron expressions and agent configurations.
</role>

<task>
Create, list, or manage scheduled recurring agents. Wraps Claude Code's native `/schedule` with Claude Sentient command integration.
</task>

<steps>
## Common Recipes

When the user describes what they want, map to a schedule:

| Intent | Cron | Command |
|--------|------|---------|
| "nightly codebase audit" | `0 2 * * *` | `/cs-assess` |
| "check deploy status every 5 min" | `*/5 * * * *` | `/cs-status --ci` |
| "weekly security review" | `0 9 * * 1` | `/cs-assess --security` |
| "daily dependency check" | `0 8 * * *` | `/cs-loop "check for outdated dependencies"` |
| "prune stale PRs weekly" | `0 10 * * 5` | Custom: list and close stale PRs |

## Execution

1. Parse user intent into cron expression + command
2. Confirm schedule with user: `"Schedule: {cron} -> {command}. Confirm? (yes/no)"`
3. Create the schedule using Claude Code's native scheduling

## Management

| Subcommand | Action |
|------------|--------|
| `--list` | Show all active schedules |
| `--cancel <id>` | Cancel a scheduled agent |
| `--history` | Show recent schedule executions |
</steps>

<constraints>
- Always confirm before creating a schedule
- Minimum interval: 5 minutes (prevent resource abuse)
- Maximum concurrent scheduled agents: 3
</constraints>
```

- [ ] **Step 3: Update CLAUDE.md commands table**

In `CLAUDE.md`, add two rows to the commands table (after `/cs-log`):

```markdown
| `/cs-batch [plan]` | Fan out tasks to parallel worktree agents |
| `/cs-schedule <cron> <cmd>` | Create recurring autonomous agents |
```

Also add to Quick Start section:

```markdown
/cs-batch "migrate all API endpoints to v2"  # Parallel worktree fan-out
/cs-schedule "0 2 * * *" /cs-assess           # Nightly codebase audit
```

- [ ] **Step 4: Update .claude/commands/CLAUDE.md command inventory**

Add cs-batch and cs-schedule entries to the command inventory table.

- [ ] **Step 5: Run command tests**

Run: `bash --norc --noprofile -c "node .claude/commands/__tests__/test-commands.js" 2>/dev/null`
Expected: PASS (may need test count update if schema validates command count)

- [ ] **Step 6: Commit**

```bash
git add .claude/commands/cs-batch.md .claude/commands/cs-schedule.md CLAUDE.md .claude/commands/CLAUDE.md
git commit -m "feat: add /cs-batch and /cs-schedule commands for parallel fan-out and recurring agents"
```

---

## Task 3: CLAUDE.local.md Template and Installer Support

**Why this matters:** `CLAUDE.local.md` is gitignored and holds personal preferences. The best-practice repo emphasizes this as essential. Our installer should scaffold it.

**Files:**
- Create: `templates/CLAUDE.local.md`
- Modify: `install.sh` (after memory initialization, around line 162)
- Modify: `install.ps1` (mirror)
- Modify: `.claude/skills/profile-detection/SKILL.md`

- [ ] **Step 1: Create CLAUDE.local.md template**

Create `templates/CLAUDE.local.md`:

```markdown
# CLAUDE.local.md - Personal Preferences

> This file is gitignored. Use it for preferences that should not be shared with the team.
> It loads automatically alongside the project CLAUDE.md (ancestor loading).

## My Preferences

<!-- Uncomment and customize any section below -->

<!-- ## Coding Style
- I prefer [descriptive variable names / short names]
- I like [tabs / 2-space / 4-space] indentation
- I prefer [single quotes / double quotes] in [JS/TS/Python]
-->

<!-- ## Communication
- I prefer [concise / detailed] explanations
- I [do / don't] want educational comments in code
- I prefer [minimal / verbose] commit messages
-->

<!-- ## Model Preferences
- Default model: [sonnet / opus / haiku]
- Use opus for: [security reviews / complex architecture]
- Use haiku for: [quick lookups / formatting]
-->

<!-- ## Tools
- My terminal: [iTerm2 / Windows Terminal / Alacritty / other]
- My editor: [VS Code / Neovim / JetBrains / other]
- Notifications: [bell / desktop / none]
-->

<!-- ## Commit Strategy
- Default: [atomic / per-file / per-task]
-->

<!-- ## Project-Specific
- My focus area: [frontend / backend / infra / full-stack]
-->
```

- [ ] **Step 2: Add CLAUDE.local.md creation to install.sh**

In `install.sh`, after the "Initializing memory..." section (around line 162), add:

```bash
echo "Creating CLAUDE.local.md template..."
if [ ! -f "CLAUDE.local.md" ]; then
    cp "$TEMP_DIR"/templates/CLAUDE.local.md ./CLAUDE.local.md
    echo "  Created CLAUDE.local.md (gitignored - personal preferences)"
else
    echo "  Preserved existing CLAUDE.local.md"
fi
```

Mirror in `install.ps1`.

- [ ] **Step 3: Verify .gitignore already covers CLAUDE.local.md**

`.gitignore` line 9 already contains `CLAUDE.local.md`. No change needed.

- [ ] **Step 4: Add CLAUDE.local.md detection to profile-detection skill**

In `.claude/skills/profile-detection/SKILL.md`, add a bullet to the "Governance Files" section (around line 54):

```markdown
- Check for `CLAUDE.local.md` in project root. If missing and first session, note: `[INIT] Tip: Create CLAUDE.local.md for personal preferences (gitignored). Template: templates/CLAUDE.local.md`
```

- [ ] **Step 5: Run integration tests**

Run: `bash --norc --noprofile -c "node integration/__tests__/test-integration.js" 2>/dev/null`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add templates/CLAUDE.local.md install.sh install.ps1 .claude/skills/profile-detection/SKILL.md
git commit -m "feat: add CLAUDE.local.md template and installer scaffolding"
```

---

## Task 4: Agent Memory Frontmatter

**Why this matters:** The `memory:` field in agent definitions enables persistent agent knowledge across sessions. Architects remember past decisions, security agents remember past vulnerabilities. This is an under-documented feature the best-practice repo highlights.

**Files:**
- Modify: All 9 files in `.claude/agents/*.md`

- [ ] **Step 1: Add memory to architect agent**

In `.claude/agents/architect.md`, add after line 20 (`  - quality-gates`), before the closing `---`:

```yaml
memory:
  - scope: project
    description: "Architecture decisions, module boundaries, dependency choices, and technical debt priorities"
  - scope: user
    description: "User's architecture preferences, preferred patterns, and design philosophy"
```

- [ ] **Step 2: Add memory to backend agent**

In `.claude/agents/backend.md`, add after `skills:` section:

```yaml
memory:
  - scope: project
    description: "API conventions, database patterns, auth strategies, and performance baselines"
```

- [ ] **Step 3: Add memory to frontend agent**

In `.claude/agents/frontend.md`, add after `skills:` section:

```yaml
memory:
  - scope: project
    description: "Component patterns, design system tokens, accessibility findings, and responsive breakpoints"
```

- [ ] **Step 4: Add memory to database agent**

In `.claude/agents/database.md`, add after `skills:` section:

```yaml
memory:
  - scope: project
    description: "Schema evolution history, index strategies, migration patterns, and query performance baselines"
```

- [ ] **Step 5: Add memory to security agent**

In `.claude/agents/security.md`, add after `skills:` section:

```yaml
memory:
  - scope: project
    description: "Past vulnerability findings, remediation patterns, auth flow decisions, and threat model updates"
  - scope: user
    description: "Security posture preferences, compliance requirements, and risk tolerance"
```

- [ ] **Step 6: Add memory to tester agent**

In `.claude/agents/tester.md`, add after `skills:` section:

```yaml
memory:
  - scope: project
    description: "Flaky test patterns, coverage gaps, test infrastructure quirks, and edge case catalogs"
```

- [ ] **Step 7: Add memory to devops agent**

In `.claude/agents/devops.md`, add after `skills:` section:

```yaml
memory:
  - scope: project
    description: "CI/CD pipeline configurations, deployment targets, infrastructure decisions, and incident history"
```

- [ ] **Step 8: Add memory to docs agent**

In `.claude/agents/docs.md`, add after `skills:` section:

```yaml
memory:
  - scope: project
    description: "Documentation standards, API doc conventions, changelog format, and terminology glossary"
```

- [ ] **Step 9: Add memory to build-resolver agent**

In `.claude/agents/build-resolver.md`, add after `skills:` section:

```yaml
memory:
  - scope: project
    description: "Build system quirks, dependency conflict resolutions, CI environment specifics, and past build fix patterns"
```

- [ ] **Step 10: Run agent tests**

Run: `bash --norc --noprofile -c "node agents/__tests__/test-agents.js" 2>/dev/null`
Expected: All 108 tests PASS

- [ ] **Step 11: Commit**

```bash
git add .claude/agents/*.md
git commit -m "feat: add memory frontmatter to all 9 agent definitions for persistent cross-session knowledge"
```

---

## Task 5: Commit Strategy Selection

**Why this matters:** The best-practice repo recommends per-file commits for cleaner `git blame`. Currently `/cs-loop` always does atomic commits. Offering a choice lets users pick the right strategy.

**Files:**
- Create: `.claude/skills/quality-gates/references/commit-strategies.md`
- Modify: `.claude/commands/cs-loop.md` (COMMIT phase)
- Modify: `.claude/skills/quality-gates/SKILL.md`

- [ ] **Step 1: Create commit strategies reference**

Create `.claude/skills/quality-gates/references/commit-strategies.md`:

```markdown
# Commit Strategies

## Strategies

| Strategy | Behavior | Best For |
|----------|----------|----------|
| `atomic` | One commit per checkpoint (all changed files) | Fast iteration, feature branches |
| `per-file` | Separate commit per modified file | Clean git blame, easy per-file revert |
| `per-task` | One commit per completed task | Task-level traceability |

## Atomic (default)
```
git add <all-changed-files>
git commit -m "feat: implement feature X"
```

## Per-File
```
# For each modified file:
git add src/auth.ts
git commit -m "feat(auth): add token validation"
git add src/middleware.ts
git commit -m "feat(middleware): integrate auth check"
```

Rules for per-file commits:
- Each commit must pass lint independently
- Commit message scopes match the file's module/directory
- If files are tightly coupled (changing one without the other breaks build), commit them together

## Per-Task
```
# After each TaskUpdate(status: completed):
git add <files-modified-for-this-task>
git commit -m "feat: complete task - <task subject>"
```

## Configuration

Set via (checked in order):
1. `/cs-loop --commit-strategy per-file` (argument)
2. `.claude/state/session_start.json` field `commitStrategy`
3. `CLAUDE.local.md` personal default
4. Default: `atomic`
```

- [ ] **Step 2: Add commit strategy dispatch to cs-loop COMMIT phase**

In `.claude/commands/cs-loop.md`, add to the beginning of the COMMIT phase (section 6):

```markdown
**Determine commit strategy** (check in order):
1. If `--commit-strategy <strategy>` was passed as argument, use it
2. If `.claude/state/session_start.json` has `commitStrategy`, use it
3. If `CLAUDE.local.md` specifies a preference, use it
4. Default: `atomic`

| Strategy | Behavior |
|----------|----------|
| `atomic` | Stage all changes, single commit |
| `per-file` | Separate commit per modified file (each must pass lint) |
| `per-task` | One commit per completed task |

See `quality-gates/references/commit-strategies.md` for detailed rules.
```

- [ ] **Step 3: Add reference pointer to quality-gates skill**

In `.claude/skills/quality-gates/SKILL.md`, add before the Gotchas section:

```markdown
## Commit Strategies

See `references/commit-strategies.md` for per-file and per-task commit strategies.
Default is `atomic` (single checkpoint commit). Override via `--commit-strategy` argument or `CLAUDE.local.md`.
```

- [ ] **Step 4: Run command tests**

Run: `bash --norc --noprofile -c "node .claude/commands/__tests__/test-commands.js" 2>/dev/null`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/quality-gates/references/commit-strategies.md .claude/commands/cs-loop.md .claude/skills/quality-gates/SKILL.md
git commit -m "feat: add configurable commit strategies (atomic, per-file, per-task)"
```

---

## Task 6: Worktree-First Team Mode

**Why this matters:** Boris's #1 productivity tip is parallel worktrees. Worktree-per-teammate eliminates file ownership conflicts entirely.

**Files:**
- Create: `.claude/skills/team-orchestration/references/worktree-strategy.md`
- Modify: `.claude/skills/team-orchestration/SKILL.md` (lines 29-42)
- Modify: `.claude/commands/cs-team.md`

- [ ] **Step 1: Create worktree strategy reference**

Create `.claude/skills/team-orchestration/references/worktree-strategy.md`:

```markdown
# Worktree-First Team Strategy

## Overview

Each teammate gets an isolated git worktree instead of sharing the workspace. This eliminates file ownership conflicts entirely.

## How It Works

1. **Partition**: Tasks grouped into independent work streams (no shared files)
2. **Create worktrees**: `git worktree add -b team/{agent}-{task-id} .worktrees/team-{agent}`
3. **Spawn agents**: Each agent works in its own worktree directory
4. **Merge**: After all agents complete, merge branches sequentially

## Spawn Pattern

For each teammate:
1. `git worktree add -b team/{agent-name} .worktrees/team-{agent-name}`
2. Spawn agent with cwd = `.worktrees/team-{agent-name}`
3. Agent runs /cs-loop within its isolated workspace
4. On completion: run quality gates in the worktree
5. If gates pass: `git merge team/{agent-name} --no-ff`
6. Clean up: `git worktree remove .worktrees/team-{agent-name}`

## Fallback to Shared Workspace

Use shared workspace (original behavior) when:
- Tasks modify the same files (merge would conflict regardless)
- Single-file tasks where worktree overhead exceeds benefit
- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` is not set

## Conflict Resolution

If merge conflicts occur after worktree agents complete:
1. Show the conflict diff to the user
2. Offer: (a) manual resolution, (b) re-run conflicting agent with merged context, (c) abort and park
3. Never auto-resolve merge conflicts in team mode

## Merge Order

Merge agents that touch foundational files (types, interfaces, schemas) first, then dependents.

## Limits

- Maximum worktrees: 5 (matches /cs-batch limit)
- Worktree creation: ~200ms per worktree (negligible)
```

- [ ] **Step 2: Update team-orchestration SKILL.md**

In `.claude/skills/team-orchestration/SKILL.md`, replace the "Teammate Spawning" section (lines 29-42) with:

```markdown
## Teammate Spawning

**Default strategy: worktree-per-teammate** (eliminates file ownership conflicts).

1. Partition tasks into independent work streams (no overlapping files)
2. For each stream, create an isolated worktree:
   - Branch: `team/{agent-name}-{stream-id}`
   - Path: `.worktrees/team-{agent-name}`
3. Spawn teammate agent in the worktree directory
4. Agent receives: task list, quality gates, file scope, rules
5. On completion: run gates in worktree, merge if passing

**Fallback**: If tasks share files or worktrees unavailable, fall back to shared workspace with file ownership tracking (original behavior).

See `references/worktree-strategy.md` for full details, conflict resolution, and merge order.
```

Also add to the Gotchas section:

```markdown
- Worktree cleanup: Always `git worktree remove` after merge, even on failure - leaked worktrees consume disk
- Merge order matters: Merge agents that touch foundational files (types, interfaces) first
```

- [ ] **Step 3: Update cs-team command**

In `.claude/commands/cs-team.md`, add a section on worktree isolation to the execution flow:

```markdown
### Worktree Isolation (default)

When spawning teammates, prefer worktree-per-teammate:
1. `git worktree add -b team/{agent} .worktrees/team-{agent}`
2. Spawn agent in the worktree directory
3. Merge results back after gates pass

This eliminates file ownership conflicts. Fall back to shared workspace only when tasks must modify the same files.
```

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/team-orchestration/references/worktree-strategy.md .claude/skills/team-orchestration/SKILL.md .claude/commands/cs-team.md
git commit -m "feat: worktree-first team mode as default strategy for agent teams"
```

---

## Task 7: MCP Server Recommendations Update

**Why this matters:** DeepWiki, Excalidraw, and Playwright are recommended by the best-practice community. Updating `/cs-mcp` with these improves discoverability.

**Files:**
- Modify: `.claude/commands/cs-mcp.md` (Known Servers Reference table and /cs-loop Integration table)

- [ ] **Step 1: Add new servers to cs-mcp**

In `.claude/commands/cs-mcp.md`, add to the "Known Servers Reference" table:

```markdown
| deepwiki | `@anthropic-ai/deepwiki-mcp` | - | Wiki-style docs for any GitHub repo |
| excalidraw | `@anthropic-ai/excalidraw-mcp` | - | Generate architecture diagrams |
| playwright | Plugin (official) | - | Browser automation (recommended over puppeteer) |
```

Add to the `/cs-loop Integration` table:

```markdown
| **deepwiki** | INIT | Fetch repo documentation for unfamiliar dependencies |
| **excalidraw** | COMMIT | Generate architecture diagrams for /cs-docs |
| **playwright** | VERIFY | Screenshot web apps after UI changes (preferred over puppeteer) |
```

Add a "Recommended Setup" section to `<context>`:

```markdown
## Recommended Setup

Most projects need 4-5 MCP servers. Don't install 15 - each adds startup overhead.

**Essential**: context7 (library docs), github (PRs/issues)
**Recommended**: playwright or puppeteer (web projects), deepwiki (open source exploration)
**Optional**: excalidraw (diagrams), memory (session persistence), filesystem (file access)
```

- [ ] **Step 2: Commit**

```bash
git add .claude/commands/cs-mcp.md
git commit -m "feat: add DeepWiki, Excalidraw, Playwright to MCP server recommendations"
```

---

## Task 8: Browser Verification Enhancement

**Why this matters:** Boris says giving Claude "a way to verify its output" is essential for frontend work. VERIFY phase should actively use Playwright/puppeteer for visual checks.

**Files:**
- Modify: `.claude/commands/cs-loop.md` (VERIFY phase)
- Modify: `.claude/skills/quality-gates/SKILL.md`

- [ ] **Step 1: Add browser verification to VERIFY phase**

In `.claude/commands/cs-loop.md`, add to the VERIFY phase (section 5), after the BUILD gate row in the table:

```markdown
**Browser verification** (web projects only, advisory):
1. Detect if Playwright or puppeteer MCP is connected
2. If connected AND profile is web (TypeScript Web or Python Web):
   - Navigate to `localhost:{port}` (detect from dev server or default 3000/5173/8000)
   - Take screenshot
   - Compare against task intent: "Does this screenshot match what was requested?"
   - If visual regression detected, report and offer to fix
3. If no browser MCP: `[VERIFY] No browser MCP - skipping visual verification. Tip: /cs-mcp --fix`
```

- [ ] **Step 2: Add browser gate to quality-gates skill**

In `.claude/skills/quality-gates/SKILL.md`, add after the GIT gate section:

```markdown
## Advisory: Browser Verification (web projects)

**Trigger**: Web project profile AND Playwright/puppeteer MCP connected
**Action**: Navigate to dev server, take screenshot, validate against task intent
**Blocking**: No (advisory only)
**Gotcha**: Dev server must be running. If not, attempt `npm run dev` or equivalent in background, wait 5s, then screenshot.
```

- [ ] **Step 3: Commit**

```bash
git add .claude/commands/cs-loop.md .claude/skills/quality-gates/SKILL.md
git commit -m "feat: add browser verification advisory gate for web projects"
```

---

## Task 9: Cross-Model Workflow Reference

**Why this matters:** Independent verification from a different model family catches blind spots. We add this as a reference doc.

**Files:**
- Create: `.claude/skills/profile-detection/references/cross-model.md`
- Modify: `.claude/skills/profile-detection/SKILL.md`

- [ ] **Step 1: Create cross-model workflow reference**

Create `.claude/skills/profile-detection/references/cross-model.md`:

```markdown
# Cross-Model Workflow (Claude + Codex)

## Overview

Use Claude Code for planning and implementation, and OpenAI Codex CLI for independent QA review. Different model families catch different blind spots.

## Workflow

### Phase 1: Plan (Claude Code)
Use `/cs-plan` to create implementation plan, export to PLAN.md.

### Phase 2: QA Review (Codex CLI)
```
codex "Review PLAN.md against the codebase. Check for: missing edge cases, security gaps, architectural misalignment, over-engineering. Be critical."
```

### Phase 3: Implement (Claude Code)
```
/cs-loop "implement PLAN.md, addressing QA feedback"
```

### Phase 4: Verify (Codex CLI)
```
codex "Review changes in this branch against PLAN.md. Verify: all plan items implemented, no regressions, tests cover edge cases."
```

## When to Use

- High-stakes changes (auth, payments, data migrations)
- Architecture decisions affecting many files
- When you want a second opinion from a different model family

## Setup

Requires OpenAI Codex CLI installed separately. Codex instructions can be placed in `.codex/instructions.md` (Claude Sentient installer creates this).

## Limitations

- Adds latency (two model round-trips per phase)
- Codex may not have access to all MCP servers
- Best for review/verification, not real-time collaboration
```

- [ ] **Step 2: Add pointer in profile-detection skill**

In `.claude/skills/profile-detection/SKILL.md`, add a bullet near the end:

```markdown
- **Cross-model workflow**: For high-stakes changes, consider Claude + Codex QA review. See `references/cross-model.md`
```

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/profile-detection/references/cross-model.md .claude/skills/profile-detection/SKILL.md
git commit -m "docs: add cross-model workflow reference (Claude + Codex QA review)"
```

---

## Task 10: Progressive Skill Disclosure (Worked Examples)

**Why this matters:** Thariq recommends skills as folders with subdirectories for progressive disclosure. We add `examples/` to all 3 skills.

**Files:**
- Create: `.claude/skills/quality-gates/examples/gate-failure-fix.md`
- Create: `.claude/skills/team-orchestration/examples/team-spawn.md`
- Create: `.claude/skills/profile-detection/examples/python-conda-init.md`

- [ ] **Step 1: Create quality-gates worked example**

Create `.claude/skills/quality-gates/examples/gate-failure-fix.md`:

```markdown
# Example: Fixing a Lint Gate Failure

## Scenario
Running `/cs-loop "add input validation"` hits a lint failure in VERIFY.

## Gate Output
```
$ ruff check src/
src/forms/signup.py:45:1: I001 Import block is un-sorted or un-formatted
src/forms/signup.py:78:5: E712 Comparison to True should be 'if cond:' not 'if cond == True:'
Found 2 errors.
```

## Auto-Fix Attempt 1
```
ruff check src/ --fix
```
Result: I001 fixed. E712 requires manual fix.

## Manual Fix (Attempt 2)
Read `src/forms/signup.py:78`, change `if is_valid == True:` to `if is_valid:`

## Re-Verify
```
ruff check src/
```
Result: 0 errors. Gate passes.

## Key Lesson
- `ruff --fix` handles import sorting but not all style issues
- Read the specific error before attempting manual fix
- Never suppress with `# noqa`
```

- [ ] **Step 2: Create team-orchestration worked example**

Create `.claude/skills/team-orchestration/examples/team-spawn.md`:

```markdown
# Example: Spawning a 3-Agent Team

## Scenario
Task: "Refactor auth - new JWT middleware, update DB schema, add login form"

## Eligibility Check
- 3 independent tasks: middleware (backend), schema (database), form (frontend)
- Non-overlapping scopes: src/middleware/, migrations/, src/components/
- Complexity: moderate
- CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS: set

## Work Stream Partition

| Stream | Agent | Files | Branch |
|--------|-------|-------|--------|
| 1 | backend | src/middleware/auth.ts, src/routes/login.ts | team/backend-auth |
| 2 | database | migrations/003-jwt.sql, src/models/session.ts | team/database-jwt |
| 3 | frontend | src/components/LoginForm.tsx, src/hooks/useAuth.ts | team/frontend-login |

## Merge Order
1. Database first (schema is foundational)
2. Backend second (depends on schema)
3. Frontend last (depends on API)

## Result
3 clean branches, each passing gates, merged in dependency order.
```

- [ ] **Step 3: Create profile-detection worked example**

Create `.claude/skills/profile-detection/examples/python-conda-init.md`:

```markdown
# Example: Python Conda Environment Detection

## Scenario
Project has `environment.yml` with `name: ml-pipeline` and `pyproject.toml`.

## Detection Flow
1. session-start.cjs detects `pyproject.toml` -> profile: `python`
2. profile-detection skill checks for Python environment:
   - `environment.yml` found -> extract `name: ml-pipeline`
   - Set prefix: `conda run -n ml-pipeline --no-capture-output`
3. All gate commands prepended with conda prefix

## Report
```
[INIT] Profile: python, Tools: ruff, pytest
[INIT] Environment: conda (ml-pipeline)
[INIT] Rules loaded: code-quality, testing
```

## Gotcha
If `conda run` fails with "environment not found", the env may need creation:
```
conda env create -f environment.yml
```
```

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/quality-gates/examples/ .claude/skills/team-orchestration/examples/ .claude/skills/profile-detection/examples/
git commit -m "docs: add worked examples to all 3 skills for progressive disclosure"
```

---

## Task 11: Native Command Documentation

**Why this matters:** `/btw`, `/branch`, `/voice`, `--bare`, `--add-dir` are powerful native features undocumented in Claude Sentient.

**Files:**
- Create: `documentation/16-native-tips.md`
- Modify: `CLAUDE.md` (Reference table)

- [ ] **Step 1: Create native tips documentation**

Create `documentation/16-native-tips.md`:

```markdown
# Native Claude Code Tips for Claude Sentient Users

> Power features from Claude Code that compose well with Claude Sentient commands.

## /btw - Side Queries Without Interrupting

During a `/cs-loop` session, use `/btw` to ask a question without breaking the agent's flow:

```
/btw what does the handleAuth middleware do?
```

The agent continues its current task after answering.

## /branch - Fork a Session

Fork the current session to explore an alternative approach:

```
/branch
```

Creates a copy of the current conversation. Resume the original with `/cs-sessions --resume`.

## /voice - Voice Coding

Activate voice input. Works with all Claude Sentient commands:
- "cs-loop implement user authentication"
- "cs-status"

Tips: speak command names clearly ("cs dash loop"), spell out variable names if needed.

## /loop - Recurring Monitoring

Run a command on a recurring interval:

```
/loop 5m /cs-status
/loop 10m /cs-assess --security
```

## /batch - Massive Fan-Out

Fan work to hundreds of worktree agents. Use `/cs-batch` for Claude Sentient's quality-gated variant, or native `/batch` for maximum speed.

## --bare Flag

10x faster startup by skipping settings and MCP discovery:

```
claude --bare -p "quick question about this file"
```

Not recommended for `/cs-loop` (needs MCP servers and settings).

## --add-dir - Multi-Repo Access

Give Claude access to files in another repository:

```
claude --add-dir ../shared-lib --add-dir ../design-system
```

## Combining with Claude Sentient

| Native Feature | Claude Sentient Combo | Use Case |
|---------------|----------------------|----------|
| `/btw` | During `/cs-loop` | Side queries without breaking flow |
| `/branch` | Before risky `/cs-loop` task | Safe exploration |
| `/voice` | Any `/cs-*` command | Hands-free development |
| `/loop` | `/loop 5m /cs-status` | Monitoring |
| `--add-dir` | `/cs-loop` on multi-repo features | Cross-repo work |
| `--bare` | Quick lookups | Speed over features |
```

- [ ] **Step 2: Add Native Tips reference to CLAUDE.md**

In `CLAUDE.md`, add to the Reference table:

```markdown
| Native tips | `documentation/16-native-tips.md` |
```

- [ ] **Step 3: Commit**

```bash
git add documentation/16-native-tips.md CLAUDE.md
git commit -m "docs: add native Claude Code tips documentation"
```

---

## Task 12: --bare Flag Optimization Guidance

**Why this matters:** Clarifies when --bare is and isn't appropriate for subagent performance.

**Files:**
- Modify: `.claude/skills/team-orchestration/SKILL.md`
- Modify: `.claude/commands/cs-loop.md` (EXECUTE phase)

- [ ] **Step 1: Add --bare guidance to team-orchestration skill**

In `.claude/skills/team-orchestration/SKILL.md`, add to the "Teammate Spawning" section:

```markdown
**Performance note**: Do NOT use `--bare` for teammate agents - they need full MCP and settings context for quality gates. `--bare` is only appropriate for quick lookup subagents (e.g., "what does function X do?") spawned during EXECUTE.
```

- [ ] **Step 2: Add --bare guidance to cs-loop EXECUTE phase**

In `.claude/commands/cs-loop.md`, add to the EXECUTE Standard Mode section:

```markdown
**Quick lookup subagents**: When spawning a subagent for a focused question (not a full task), use `model: "haiku"` for speed. The `--bare` flag applies to CLI invocations, not to the Task tool.
```

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/team-orchestration/SKILL.md .claude/commands/cs-loop.md
git commit -m "docs: add --bare flag guidance for subagent performance"
```

---

## Task 13: Commit Strategy Wiring in cs-loop COMMIT Phase

**Why this matters:** Task 5 added the reference doc and config. This task wires the detailed step-by-step procedure into the COMMIT phase.

**Files:**
- Modify: `.claude/commands/cs-loop.md` (COMMIT phase - replace existing steps)

- [ ] **Step 1: Rewrite COMMIT phase with strategy dispatch**

In `.claude/commands/cs-loop.md`, replace the existing COMMIT phase (section 6) numbered steps with:

```markdown
**Strategy: atomic** (default)
1. Stage all changes: `git add <files>`
2. Create commit with conventional message (`feat:`, `fix:`, etc.)

**Strategy: per-file**
1. For each modified file (ordered by dependency - foundational types first):
   a. Stage single file: `git add <file>`
   b. Run linter on that file (must pass independently)
   c. Commit: `git commit -m "feat(<scope>): <what changed>"`
   d. If lint fails, stage the fix too and commit together
2. Tightly coupled files (changing one breaks the other) get committed together

**Strategy: per-task**
1. After each `TaskUpdate(status: completed)` in EXECUTE (not here):
   a. Stage files for that task: `git add <task-files>`
   b. Commit: `git commit -m "feat: <task subject>"`
2. In COMMIT phase, only handle remaining unstaged changes

**Post-commit (all strategies):**
3. Doc sync check: if changed files match a feature in `documentation/`, update if needed
4. Auto-update STATUS.md and CHANGELOG.md for `feat:`/`fix:` commits
5. MCP: github (link commits, create PRs), memory (persist session state)
6. Auto-capture non-obvious learnings via `/cs-learn`
7. CI monitoring: check PR status, auto-fix if lint/test failure (max 2 attempts)

Report: `[COMMIT] Created checkpoint: {hash} (strategy: {strategy})`
```

- [ ] **Step 2: Run command tests**

Run: `bash --norc --noprofile -c "node .claude/commands/__tests__/test-commands.js" 2>/dev/null`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add .claude/commands/cs-loop.md
git commit -m "feat: implement commit strategy dispatch in cs-loop COMMIT phase"
```

---

## Task 14: Version Bump and Final Documentation Sync

**Why this matters:** All enhancements need version bump, CHANGELOG, and STATUS.md updates. Integration tests enforce consistency.

**Files:**
- Modify: `CLAUDE.md` (version 1.5.9 -> 1.6.0)
- Modify: `CHANGELOG.md`
- Modify: `STATUS.md`
- Modify: All `profiles/*.yaml` and `agents/*.yaml` (if versioned)
- Modify: `README.md` (badge)

- [ ] **Step 1: Bump version in CLAUDE.md**

Change `**Version:** 1.5.9` to `**Version:** 1.6.0`.

- [ ] **Step 2: Update CHANGELOG.md**

Add to top:

```markdown
## v1.6.0 - Best Practice Enhancements

### Added
- Notification hook (notification.cjs): Optional audio/visual lifecycle notifications
- /cs-batch: Fan-out tasks to parallel worktree agents with quality gates
- /cs-schedule: Create recurring autonomous agents via native /schedule
- CLAUDE.local.md template: Installer scaffolds personal preferences (gitignored)
- Agent memory: All 9 agents have memory: frontmatter for persistent knowledge
- Commit strategies: atomic (default), per-file, per-task
- Worktree-first team mode: Default strategy for /cs-team
- MCP recommendations: Added DeepWiki, Excalidraw, Playwright
- Browser verification: Advisory gate in VERIFY for web projects
- Cross-model workflow: Claude + Codex QA review reference
- Worked examples: Progressive disclosure for all 3 skills
- Native tips doc: /btw, /branch, /voice, /loop, /batch, --bare, --add-dir

### Changed
- /cs-loop COMMIT phase supports commit strategy selection
- Team orchestration defaults to worktree-per-teammate
- Profile detection suggests CLAUDE.local.md creation

### Source
Enhancements from comparing with shanraisshan/claude-code-best-practice (32K+ stars).
```

- [ ] **Step 3: Update STATUS.md component counts**

Update command count: 17 -> 19 (cs-batch, cs-schedule).
Update hook count: 16 -> 17 (notification.cjs).

- [ ] **Step 4: Bump version across profiles and agents**

Find-and-replace `1.5.9` -> `1.6.0` in:
- `profiles/*.yaml`
- `README.md` badge

- [ ] **Step 5: Run all 6 test suites**

```bash
bash --norc --noprofile -c "node profiles/__tests__/test-profiles.js" 2>/dev/null
bash --norc --noprofile -c "node .claude/hooks/__tests__/test-hooks.js" 2>/dev/null
bash --norc --noprofile -c "node .claude/commands/__tests__/test-commands.js" 2>/dev/null
bash --norc --noprofile -c "node agents/__tests__/test-agents.js" 2>/dev/null
bash --norc --noprofile -c "node schemas/__tests__/test-schemas.js" 2>/dev/null
bash --norc --noprofile -c "node integration/__tests__/test-integration.js" 2>/dev/null
```

Expected: All PASS. Update test expectations if counts changed.

- [ ] **Step 6: Regenerate checksums**

```bash
bash generate-checksums.sh
```

- [ ] **Step 7: Commit**

Write commit message to `/tmp/commit-msg.txt`:
```
chore: bump to v1.6.0, update changelog and docs for best-practice enhancements
```

```bash
git add CLAUDE.md CHANGELOG.md STATUS.md README.md profiles/ CHECKSUMS.sha256
git commit -F /tmp/commit-msg.txt
```

---

## Self-Review Checklist

### Spec Coverage
- [x] Task 1: Notification hooks
- [x] Task 2: /cs-batch + /cs-schedule
- [x] Task 3: CLAUDE.local.md
- [x] Task 4: Agent memory frontmatter
- [x] Task 5: Commit strategies reference
- [x] Task 6: Worktree-first teams
- [x] Task 7: MCP recommendations
- [x] Task 8: Browser verification
- [x] Task 9: Cross-model workflow
- [x] Task 10: Progressive skill disclosure (examples)
- [x] Task 11: Native tips documentation
- [x] Task 12: --bare optimization guidance
- [x] Task 13: Commit strategy wiring in COMMIT phase
- [x] Task 14: Version bump + final sync

### Placeholder Scan
- No TBD/TODO items in any task
- All file paths are exact
- All test commands are runnable
- Code blocks contain complete implementations

### Type/Name Consistency
- `getNotificationConfig()` consistent in utils.cjs and notification.cjs
- `notification-config.json` path consistent throughout
- Commit strategy names (`atomic`, `per-file`, `per-task`) consistent across cs-loop.md, commit-strategies.md, SKILL.md
- Worktree branch naming (`team/{agent}`) consistent across team skill, worktree reference, cs-team
- Version `1.6.0` used consistently in all bump locations
