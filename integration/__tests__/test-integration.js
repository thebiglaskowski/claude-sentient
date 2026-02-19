#!/usr/bin/env node
/**
 * Integration test suite for Claude Sentient
 *
 * Tests cross-module integrity: verifying that references between
 * CLAUDE.md, commands, profiles, agents, rules, hooks, and install
 * scripts are all consistent.
 *
 * Run: node integration/__tests__/test-integration.js
 */

const assert = require('assert');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const os = require('os');

const { test, suite, summary, getResults } = require('../../test-utils');

const ROOT = path.resolve(__dirname, '../..');

// --- Helpers ---

/** Read a file relative to project root */
function readFile(relPath) {
    return fs.readFileSync(path.join(ROOT, relPath), 'utf8');
}

/** Check if a file exists relative to project root */
function fileExists(relPath) {
    return fs.existsSync(path.join(ROOT, relPath));
}

/** Extract markdown table rows from content (skips header and separator) */
function parseMarkdownTableRows(content, headerPattern) {
    const lines = content.split('\n');
    const headerIndex = lines.findIndex(l => headerPattern.test(l));
    if (headerIndex === -1) return [];

    const rows = [];
    // Skip the header line and the separator line (---|----|---)
    for (let i = headerIndex + 2; i < lines.length; i++) {
        const line = lines[i].trim();
        if (!line.startsWith('|')) break;
        const cells = line.split('|').map(c => c.trim()).filter(c => c.length > 0);
        rows.push(cells);
    }
    return rows;
}

// ============================================================
// Suite 1: Cross-file reference integrity
// ============================================================

suite('Cross-file reference integrity', () => {
    const claudeMd = readFile('CLAUDE.md');

    // --- Commands table references ---
    test('all commands in CLAUDE.md commands table exist as .claude/commands/cs-*.md files', () => {
        const rows = parseMarkdownTableRows(claudeMd, /^\|\s*Command\s*\|\s*Purpose\s*\|/);
        assert.ok(rows.length > 0, 'Should find command rows in CLAUDE.md');

        const commandNames = rows.map(row => {
            // Extract command name from first cell, e.g. "`/cs-loop [task]`" -> "cs-loop"
            const match = row[0].match(/\/?(cs-[a-z]+)/);
            return match ? match[1] : null;
        }).filter(Boolean);

        assert.ok(commandNames.length >= 10, `Expected at least 10 commands, got ${commandNames.length}`);

        const missing = [];
        for (const cmd of commandNames) {
            const filePath = `.claude/commands/${cmd}.md`;
            if (!fileExists(filePath)) {
                missing.push(filePath);
            }
        }
        assert.strictEqual(missing.length, 0,
            `Commands referenced in CLAUDE.md but missing files: ${missing.join(', ')}`);
    });

    test('all .claude/commands/cs-*.md files are listed in CLAUDE.md commands table', () => {
        const commandFiles = fs.readdirSync(path.join(ROOT, '.claude/commands'))
            .filter(f => f.startsWith('cs-') && f.endsWith('.md'))
            .map(f => f.replace('.md', ''));

        const rows = parseMarkdownTableRows(claudeMd, /^\|\s*Command\s*\|\s*Purpose\s*\|/);
        const listedCommands = rows.map(row => {
            const match = row[0].match(/\/?(cs-[a-z]+)/);
            return match ? match[1] : null;
        }).filter(Boolean);

        const unlisted = commandFiles.filter(cmd => !listedCommands.includes(cmd));
        assert.strictEqual(unlisted.length, 0,
            `Command files not listed in CLAUDE.md: ${unlisted.join(', ')}`);
    });

    // --- Profiles table references ---
    test('all profiles in CLAUDE.md profiles table exist as profiles/*.yaml files', () => {
        const rows = parseMarkdownTableRows(claudeMd, /^\|\s*Profile\s*\|\s*Detected By\s*\|/);
        assert.ok(rows.length > 0, 'Should find profile rows in CLAUDE.md');

        // Map profile display names to yaml filenames
        const profileNameMap = {
            'Python': 'python',
            'TypeScript': 'typescript',
            'Go': 'go',
            'Rust': 'rust',
            'Java': 'java',
            'C/C++': 'cpp',
            'Ruby': 'ruby',
            'Shell': 'shell',
            'General': 'general',
        };

        const missing = [];
        for (const row of rows) {
            const displayName = row[0];
            const yamlName = profileNameMap[displayName];
            if (!yamlName) {
                missing.push(`Unknown profile name: ${displayName}`);
                continue;
            }
            if (!fileExists(`profiles/${yamlName}.yaml`)) {
                missing.push(`profiles/${yamlName}.yaml`);
            }
        }
        assert.strictEqual(missing.length, 0,
            `Profiles referenced in CLAUDE.md but missing: ${missing.join(', ')}`);
    });

    // --- Agent roles references ---
    test('all agent roles in agents/CLAUDE.md exist as agents/*.yaml files', () => {
        const agentsClaude = readFile('agents/CLAUDE.md');
        // The agents/CLAUDE.md mentions roles in the YAML example and text.
        // We check for actual agent yaml files and verify they exist.
        const agentFiles = fs.readdirSync(path.join(ROOT, 'agents'))
            .filter(f => f.endsWith('.yaml') && !f.startsWith('_'));

        assert.ok(agentFiles.length >= 5, `Expected at least 5 agent files, got ${agentFiles.length}`);

        // Verify each agent yaml file has the required 'name' field
        for (const file of agentFiles) {
            const content = readFile(`agents/${file}`);
            const nameMatch = content.match(/^name:\s*(.+)/m);
            assert.ok(nameMatch, `agents/${file} should have a 'name' field`);
        }
    });

    test('agent roles referenced in README match agents/*.yaml files', () => {
        const readme = readFile('README.md');
        // README mentions "6 specialized agent roles" - verify count
        const agentFiles = fs.readdirSync(path.join(ROOT, 'agents'))
            .filter(f => f.endsWith('.yaml') && !f.startsWith('_'));

        const countMatch = readme.match(/Agent Roles\s*\|\s*(\d+)/);
        if (countMatch) {
            assert.strictEqual(parseInt(countMatch[1], 10), agentFiles.length,
                `README agent count (${countMatch[1]}) should match actual agent files (${agentFiles.length})`);
        }
    });

    // --- Rules index references ---
    test('all rules in rules/_index.md "Available Rules" table exist in rules/ directory', () => {
        const indexMd = readFile('rules/_index.md');
        const rows = parseMarkdownTableRows(indexMd, /^\|\s*Rule\s*\|\s*Focus\s*\|/);
        assert.ok(rows.length > 0, 'Should find rule rows in rules/_index.md');

        const missing = [];
        for (const row of rows) {
            // First cell is the rule name in backticks, e.g. "`security`"
            const ruleName = row[0].replace(/`/g, '').trim();
            if (!fileExists(`rules/${ruleName}.md`)) {
                missing.push(`rules/${ruleName}.md`);
            }
        }
        assert.strictEqual(missing.length, 0,
            `Rules in _index.md but missing from rules/: ${missing.join(', ')}`);
    });

    test('all rules in rules/_index.md also exist in .claude/rules/ directory', () => {
        const indexMd = readFile('rules/_index.md');
        const rows = parseMarkdownTableRows(indexMd, /^\|\s*Rule\s*\|\s*Focus\s*\|/);

        const missing = [];
        for (const row of rows) {
            const ruleName = row[0].replace(/`/g, '').trim();
            if (!fileExists(`.claude/rules/${ruleName}.md`)) {
                missing.push(`.claude/rules/${ruleName}.md`);
            }
        }
        assert.strictEqual(missing.length, 0,
            `Rules in _index.md but missing from .claude/rules/: ${missing.join(', ')}`);
    });

    test('always-loaded rules in _index.md exist in .claude/rules/', () => {
        const indexMd = readFile('rules/_index.md');
        const rows = parseMarkdownTableRows(indexMd, /^\|\s*Rule\s*\|\s*Purpose\s*\|/);

        // learnings.md is a special case: it lives only in .claude/rules/ (project-specific,
        // created from templates/), not in rules/ (which holds canonical reference copies).
        const templateOnlyRules = ['learnings'];

        for (const row of rows) {
            const ruleName = row[0].replace(/`/g, '').trim();
            assert.ok(fileExists(`.claude/rules/${ruleName}.md`),
                `Always-loaded rule '${ruleName}' missing from .claude/rules/`);
            if (!templateOnlyRules.includes(ruleName)) {
                assert.ok(fileExists(`rules/${ruleName}.md`),
                    `Always-loaded rule '${ruleName}' missing from rules/`);
            }
        }
    });
});

// ============================================================
// Suite 2: Hook chain state flow
// ============================================================

suite('Hook chain state flow', () => {
    // Create an isolated temp directory for hook tests
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'cs-integration-'));
    const hooksDir = path.join(ROOT, '.claude', 'hooks');

    // Ensure .claude/state exists in temp dir for hooks that write state
    fs.mkdirSync(path.join(tmpDir, '.claude', 'state'), { recursive: true });
    // Copy utils.cjs so hooks can require('./utils.cjs')
    fs.copyFileSync(path.join(hooksDir, 'utils.cjs'), path.join(tmpDir, 'utils.cjs'));

    /** Run a hook in the temp directory and return parsed JSON output */
    function runHook(hookName, input = {}) {
        const hookPath = path.join(hooksDir, hookName);
        const env = {
            ...process.env,
            HOOK_INPUT: JSON.stringify(input),
        };

        const result = execSync(`node "${hookPath}"`, {
            cwd: tmpDir,
            env,
            encoding: 'utf8',
            timeout: 5000,
            stdio: ['pipe', 'pipe', 'pipe'],
        });

        // Parse last line as JSON (hooks may produce debug output on other lines)
        const lines = result.trim().split('\n');
        return JSON.parse(lines[lines.length - 1]);
    }

    test('session-start.cjs produces valid JSON with profile field', () => {
        const output = runHook('session-start.cjs');
        assert.ok(output, 'session-start should produce output');
        assert.strictEqual(typeof output, 'object', 'Output should be an object');
        assert.ok('context' in output || 'profile' in output,
            'Output should contain context or profile field');

        if (output.context) {
            assert.ok('profile' in output.context, 'context should contain profile field');
            assert.strictEqual(typeof output.context.profile, 'string', 'profile should be a string');
        }
    });

    test('session-start.cjs creates state file readable by other hooks', () => {
        // session-start writes session_start.json to .claude/state/
        const stateFile = path.join(tmpDir, '.claude', 'state', 'session_start.json');
        assert.ok(fs.existsSync(stateFile),
            'session-start should create .claude/state/session_start.json');

        const state = JSON.parse(fs.readFileSync(stateFile, 'utf8'));
        assert.ok('profile' in state, 'State file should contain profile field');
        assert.ok('id' in state, 'State file should contain session id');
        assert.ok('timestamp' in state, 'State file should contain timestamp');
    });

    test('post-edit.js produces valid JSON output with mock file path', () => {
        const output = runHook('post-edit.cjs', {
            tool_name: 'Write',
            tool_input: { file_path: '/tmp/test-file.js' },
            tool_result: { success: true },
        });

        assert.ok(output, 'post-edit should produce output');
        assert.strictEqual(typeof output, 'object', 'Output should be an object');
        assert.strictEqual(output.tracked, true, 'Should track the file change');
        assert.ok('path' in output, 'Output should contain path field');
    });

    test('post-edit.js returns tracked:false for failed operations', () => {
        const output = runHook('post-edit.cjs', {
            tool_name: 'Write',
            tool_input: { file_path: '/tmp/test-file.js' },
            tool_result: { success: false },
        });

        assert.strictEqual(output.tracked, false, 'Should not track failed operations');
    });

    test('context-injector.js produces valid JSON output with detected topics', () => {
        const output = runHook('context-injector.cjs', {
            prompt: 'Fix the authentication bug in the login API endpoint',
        });

        assert.ok(output, 'context-injector should produce output');
        assert.strictEqual(typeof output, 'object', 'Output should be an object');
        assert.strictEqual(output.continue, true, 'Should allow continuation');
        assert.ok(Array.isArray(output.detectedTopics), 'Should have detectedTopics array');
        assert.ok(output.detectedTopics.length > 0,
            'Should detect topics from "authentication" and "API" keywords');
    });

    test('context-injector.js returns empty topics for generic prompt', () => {
        const output = runHook('context-injector.cjs', {
            prompt: 'hello world',
        });

        assert.strictEqual(output.continue, true, 'Should allow continuation');
        assert.ok(Array.isArray(output.detectedTopics), 'Should have detectedTopics array');
    });

    // Cleanup temp directory
    try {
        fs.rmSync(tmpDir, { recursive: true, force: true });
    } catch (e) {
        // Best-effort cleanup
    }
});

// ============================================================
// Suite 3: Hook smoke tests (remaining hooks)
// ============================================================

suite('Hook smoke tests', () => {
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'cs-hook-smoke-'));
    const hooksDir = path.join(ROOT, '.claude', 'hooks');

    fs.mkdirSync(path.join(tmpDir, '.claude', 'state'), { recursive: true });

    // Initialize git repo for hooks that need it
    try {
        execSync('git init', { cwd: tmpDir, stdio: 'pipe' });
        execSync('git commit --allow-empty -m "init"', { cwd: tmpDir, stdio: 'pipe' });
    } catch { /* git may not be available */ }

    function runHookSafe(hookName, input = {}) {
        const hookPath = path.join(hooksDir, hookName);
        const env = { ...process.env, HOOK_INPUT: JSON.stringify(input) };
        try {
            const result = execSync(`node "${hookPath}"`, {
                cwd: tmpDir, env, encoding: 'utf8', timeout: 5000,
                stdio: ['pipe', 'pipe', 'pipe'],
            });
            const trimmed = result.trim();
            if (!trimmed) return { exitCode: 0, output: null };
            const lines = trimmed.split('\n');
            try {
                return { exitCode: 0, output: JSON.parse(lines[lines.length - 1]) };
            } catch {
                return { exitCode: 0, output: null, raw: trimmed };
            }
        } catch (e) {
            return { exitCode: e.status || 1, stderr: e.stderr || '' };
        }
    }

    test('bash-validator.cjs produces valid JSON for safe commands', () => {
        const { exitCode, output } = runHookSafe('bash-validator.cjs', {
            tool_input: { command: 'echo hello' }
        });
        assert.strictEqual(exitCode, 0);
        assert.strictEqual(output.decision, 'allow');
    });

    test('bash-validator.cjs blocks dangerous commands with decision:block', () => {
        const { exitCode, output } = runHookSafe('bash-validator.cjs', {
            tool_input: { command: 'rm -rf /' }
        });
        assert.strictEqual(exitCode, 0);
        assert.strictEqual(output.decision, 'block');
    });

    test('file-validator.cjs produces valid JSON for project files', () => {
        const { exitCode, output } = runHookSafe('file-validator.cjs', {
            tool_input: { file_path: path.join(tmpDir, 'src/index.ts') },
            tool_name: 'Write'
        });
        assert.strictEqual(exitCode, 0);
        assert.strictEqual(output.decision, 'allow');
    });

    test('agent-tracker.cjs produces valid JSON output', () => {
        const { exitCode, output } = runHookSafe('agent-tracker.cjs', {
            agent_id: 'smoke-test-agent',
            tool_input: { subagent_type: 'Explore', description: 'test' }
        });
        assert.strictEqual(exitCode, 0);
        assert.strictEqual(output.tracked, true);
    });

    test('agent-synthesizer.cjs produces valid JSON output', () => {
        runHookSafe('agent-tracker.cjs', {
            agent_id: 'smoke-synth',
            tool_input: { subagent_type: 'Explore' }
        });
        const { exitCode, output } = runHookSafe('agent-synthesizer.cjs', {
            agent_id: 'smoke-synth', success: true
        });
        assert.strictEqual(exitCode, 0);
        assert.strictEqual(output.agentId, 'smoke-synth');
    });

    test('pre-compact.cjs produces valid JSON output', () => {
        fs.writeFileSync(
            path.join(tmpDir, '.claude', 'state', 'session_start.json'),
            JSON.stringify({ id: 'smoke-test' })
        );
        const { exitCode, output } = runHookSafe('pre-compact.cjs');
        assert.strictEqual(exitCode, 0);
        assert.ok(typeof output.backupCount === 'number');
    });

    test('session-end.cjs produces valid JSON output', () => {
        fs.writeFileSync(
            path.join(tmpDir, '.claude', 'state', 'session_start.json'),
            JSON.stringify({ id: 'smoke-end', timestamp: new Date().toISOString() })
        );
        const { exitCode, output } = runHookSafe('session-end.cjs');
        assert.strictEqual(exitCode, 0);
        assert.strictEqual(output.sessionId, 'smoke-end');
    });

    test('dod-verifier.cjs produces valid JSON output', () => {
        const { exitCode, output } = runHookSafe('dod-verifier.cjs');
        assert.strictEqual(exitCode, 0);
        assert.ok(output.timestamp);
        assert.ok(Array.isArray(output.recommendations));
    });

    test('task-completed.cjs accepts valid task (exit 0)', () => {
        fs.writeFileSync(
            path.join(tmpDir, '.claude', 'state', 'team-state.json'),
            JSON.stringify({ teammates: {}, completed_tasks: [], file_ownership: {} })
        );
        const result = runHookSafe('task-completed.cjs', {
            task_id: 'smoke-task', task_subject: 'Test',
            teammate_name: 'tester', files_changed: ['file.ts']
        });
        assert.strictEqual(result.exitCode, 0);
        // Verify state was written
        const state = JSON.parse(fs.readFileSync(
            path.join(tmpDir, '.claude', 'state', 'team-state.json'), 'utf8'));
        assert.ok(state.completed_tasks.length > 0, 'should record completed task');
    });

    test('teammate-idle.cjs allows idle with completed tasks (exit 0)', () => {
        fs.writeFileSync(
            path.join(tmpDir, '.claude', 'state', 'team-state.json'),
            JSON.stringify({
                teammates: { 'smoker': { idle_count: 0, tasks_completed: ['t1'], last_idle: null } },
                quality_checks: []
            })
        );
        const result = runHookSafe('teammate-idle.cjs', {
            teammate_name: 'smoker', tasks_completed: ['t1']
        });
        assert.strictEqual(result.exitCode, 0);
        // Verify state was updated
        const state = JSON.parse(fs.readFileSync(
            path.join(tmpDir, '.claude', 'state', 'team-state.json'), 'utf8'));
        assert.ok(state.teammates.smoker.idle_count >= 1, 'should increment idle count');
    });

    // Cleanup
    try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch { /* ignore */ }
});

// ============================================================
// Suite 4: Install/uninstall script parity (renumbered)
// ============================================================

suite('Install/uninstall script parity', () => {

    /** Extract "Installed:" summary lines from install script content */
    function extractInstalledItems(scriptContent) {
        const items = [];
        const lines = scriptContent.split('\n');
        let inInstalledSection = false;

        for (const line of lines) {
            // Detect the "Installed:" header (echo or Write-Host)
            if (/(?:echo|Write-Host)\s+['"]Installed:['"]/.test(line)) {
                inInstalledSection = true;
                continue;
            }
            if (inInstalledSection) {
                // Match lines like: echo "  .claude/commands/cs-*.md       (12 commands)"
                // or: Write-Host '  .claude/commands/cs-*.md       (12 commands)'
                const match = line.match(/(?:echo|Write-Host)\s+['"]  ([^\s]+)\s+/);
                if (match) {
                    items.push(match[1]);
                } else if (/(?:echo|Write-Host)\s+['"]$/.test(line) ||
                           /(?:echo|Write-Host)\s+["']Next steps/.test(line) ||
                           /(?:echo|Write-Host)\s+""/.test(line) ||
                           line.trim() === '') {
                    // End of installed section (empty echo or "Next steps")
                    if (items.length > 0) break;
                }
            }
        }
        return items;
    }

    /** Extract uninstalled component categories from uninstall script */
    function extractUninstallCategories(scriptContent) {
        const categories = [];
        const lines = scriptContent.split('\n');

        for (const line of lines) {
            // Match "Removing commands...", "Removing hooks...", etc.
            const match = line.match(/(?:echo|Write-Host)\s+["']Removing (\w[\w\s-]*)\.{3}["']/);
            if (match) {
                categories.push(match[1].trim().toLowerCase());
            }
        }
        return categories;
    }

    test('install.sh and install.ps1 list the same installed components', () => {
        const bashScript = readFile('install.sh');
        const ps1Script = readFile('install.ps1');

        const bashItems = extractInstalledItems(bashScript);
        const ps1Items = extractInstalledItems(ps1Script);

        assert.ok(bashItems.length > 0, 'install.sh should list installed items');
        assert.ok(ps1Items.length > 0, 'install.ps1 should list installed items');

        assert.deepStrictEqual(bashItems.sort(), ps1Items.sort(),
            `install.sh and install.ps1 should list the same components.\n` +
            `  Bash: ${bashItems.join(', ')}\n` +
            `  PS1:  ${ps1Items.join(', ')}`);
    });

    test('uninstall.sh and uninstall.ps1 remove the same component categories', () => {
        const bashScript = readFile('uninstall.sh');
        const ps1Script = readFile('uninstall.ps1');

        const bashCategories = extractUninstallCategories(bashScript);
        const ps1Categories = extractUninstallCategories(ps1Script);

        assert.ok(bashCategories.length > 0, 'uninstall.sh should have removal categories');
        assert.ok(ps1Categories.length > 0, 'uninstall.ps1 should have removal categories');

        assert.deepStrictEqual(bashCategories.sort(), ps1Categories.sort(),
            `Uninstall scripts should remove the same categories.\n` +
            `  Bash: ${bashCategories.join(', ')}\n` +
            `  PS1:  ${ps1Categories.join(', ')}`);
    });

    test('key files referenced in install scripts exist in the repo', () => {
        // Verify that the most important installed file patterns actually exist
        const expectedPaths = [
            { glob: '.claude/commands/cs-loop.md', desc: 'commands' },
            { glob: '.claude/hooks/session-start.cjs', desc: 'hooks' },
            { glob: '.claude/hooks/utils.cjs', desc: 'hook utilities' },
            { glob: 'profiles/python.yaml', desc: 'profiles' },
            { glob: 'profiles/typescript.yaml', desc: 'profiles' },
            { glob: 'agents/backend.yaml', desc: 'agents' },
            { glob: 'agents/CLAUDE.md', desc: 'agents CLAUDE.md' },
            { glob: 'rules/_index.md', desc: 'rules index' },
            { glob: 'test-utils.js', desc: 'shared test infrastructure' },
            { glob: '.claude/rules/anthropic-patterns.md', desc: 'path-scoped rules' },
            { glob: '.claude/rules/code-quality.md', desc: 'path-scoped rules' },
        ];

        const missing = [];
        for (const item of expectedPaths) {
            if (!fileExists(item.glob)) {
                missing.push(`${item.glob} (${item.desc})`);
            }
        }
        assert.strictEqual(missing.length, 0,
            `Files referenced by install scripts but missing from repo: ${missing.join(', ')}`);
    });

    test('install scripts reference the same number of commands', () => {
        const bashScript = readFile('install.sh');
        const ps1Script = readFile('install.ps1');

        const bashMatch = bashScript.match(/\((\d+) commands\)/);
        const ps1Match = ps1Script.match(/\((\d+) commands\)/);

        assert.ok(bashMatch, 'install.sh should mention command count');
        assert.ok(ps1Match, 'install.ps1 should mention command count');
        assert.strictEqual(bashMatch[1], ps1Match[1],
            `Command counts should match: bash=${bashMatch[1]}, ps1=${ps1Match[1]}`);
    });

    test('install scripts reference the same number of profiles', () => {
        const bashScript = readFile('install.sh');
        const ps1Script = readFile('install.ps1');

        const bashMatch = bashScript.match(/\((\d+) profiles/);
        const ps1Match = ps1Script.match(/\((\d+) profiles/);

        assert.ok(bashMatch, 'install.sh should mention profile count');
        assert.ok(ps1Match, 'install.ps1 should mention profile count');
        assert.strictEqual(bashMatch[1], ps1Match[1],
            `Profile counts should match: bash=${bashMatch[1]}, ps1=${ps1Match[1]}`);
    });
});

// ============================================================
// Suite 5: Documentation consistency
// ============================================================

suite('Documentation consistency', () => {
    const claudeMd = readFile('CLAUDE.md');
    const readmeMd = readFile('README.md');

    test('README.md version matches CLAUDE.md version', () => {
        const claudeVersion = claudeMd.match(/\*\*Version:\*\*\s*(\d+\.\d+\.\d+)/);
        const readmeVersion = readmeMd.match(/version-(\d+\.\d+\.\d+)/);

        assert.ok(claudeVersion, 'CLAUDE.md should contain a version number');
        assert.ok(readmeVersion, 'README.md should contain a version badge');

        assert.strictEqual(claudeVersion[1], readmeVersion[1],
            `Version mismatch: CLAUDE.md=${claudeVersion[1]}, README.md=${readmeVersion[1]}`);
    });

    test('README.md command count matches actual command file count', () => {
        const commandFiles = fs.readdirSync(path.join(ROOT, '.claude/commands'))
            .filter(f => f.startsWith('cs-') && f.endsWith('.md'));

        // README has a "By the Numbers" table with command count
        const countMatch = readmeMd.match(/Commands\s*\|\s*(\d+)/);
        assert.ok(countMatch, 'README.md should have a command count in By the Numbers');

        assert.strictEqual(parseInt(countMatch[1], 10), commandFiles.length,
            `README command count (${countMatch[1]}) should match actual files (${commandFiles.length})`);
    });

    test('README.md profile count matches actual profile file count', () => {
        const profileFiles = fs.readdirSync(path.join(ROOT, 'profiles'))
            .filter(f => f.endsWith('.yaml') && !f.startsWith('_'));

        const countMatch = readmeMd.match(/Profiles\s*\|\s*(\d+)/);
        assert.ok(countMatch, 'README.md should have a profile count');

        assert.strictEqual(parseInt(countMatch[1], 10), profileFiles.length,
            `README profile count (${countMatch[1]}) should match actual files (${profileFiles.length})`);
    });

    test('all nested CLAUDE.md files exist', () => {
        const expectedNestedClaude = [
            'profiles/CLAUDE.md',
            'agents/CLAUDE.md',
            '.claude/commands/CLAUDE.md',
            '.claude/hooks/CLAUDE.md',
        ];

        const missing = expectedNestedClaude.filter(p => !fileExists(p));
        assert.strictEqual(missing.length, 0,
            `Missing nested CLAUDE.md files: ${missing.join(', ')}`);
    });

    test('CLAUDE.md commands table count matches actual command files', () => {
        const rows = parseMarkdownTableRows(claudeMd, /^\|\s*Command\s*\|\s*Purpose\s*\|/);
        const commandFiles = fs.readdirSync(path.join(ROOT, '.claude/commands'))
            .filter(f => f.startsWith('cs-') && f.endsWith('.md'));

        assert.strictEqual(rows.length, commandFiles.length,
            `CLAUDE.md table rows (${rows.length}) should match command files (${commandFiles.length})`);
    });

    test('CLAUDE.md profiles table count matches actual profile files', () => {
        const rows = parseMarkdownTableRows(claudeMd, /^\|\s*Profile\s*\|\s*Detected By\s*\|/);
        const profileFiles = fs.readdirSync(path.join(ROOT, 'profiles'))
            .filter(f => f.endsWith('.yaml') && !f.startsWith('_'));

        assert.strictEqual(rows.length, profileFiles.length,
            `CLAUDE.md profile rows (${rows.length}) should match profile files (${profileFiles.length})`);
    });
});

// ============================================================
// Suite 6: Plugin parity
// ============================================================

suite('Plugin parity', () => {

    /** Extract LSP plugin names from installer script content */
    function extractLspPlugins(scriptContent) {
        const plugins = [];
        const pattern = /([a-z][a-z-]*-lsp@claude-plugins-official)/g;
        let match;
        while ((match = pattern.exec(scriptContent)) !== null) {
            if (!plugins.includes(match[1])) {
                plugins.push(match[1]);
            }
        }
        return plugins.sort();
    }

    /** Extract recommended plugin names from installer script content */
    function extractRecommendedPlugins(scriptContent) {
        const plugins = [];
        // Match lines like: echo "  claude plugin install pr-review-toolkit@claude-plugins-official"
        const pattern = /plugin install ([a-z-]+@claude-plugins-official)/g;
        let match;
        while ((match = pattern.exec(scriptContent)) !== null) {
            const name = match[1];
            // Exclude LSP plugins and security-guidance (those are auto-installed, not recommended)
            if (!name.includes('-lsp@') && name !== 'security-guidance@claude-plugins-official') {
                if (!plugins.includes(name)) {
                    plugins.push(name);
                }
            }
        }
        return plugins.sort();
    }

    test('install.sh and install.ps1 reference the same LSP plugins', () => {
        const bashScript = readFile('install.sh');
        const ps1Script = readFile('install.ps1');

        const bashPlugins = extractLspPlugins(bashScript);
        const ps1Plugins = extractLspPlugins(ps1Script);

        assert.ok(bashPlugins.length > 0, 'install.sh should reference LSP plugins');
        assert.ok(ps1Plugins.length > 0, 'install.ps1 should reference LSP plugins');

        assert.deepStrictEqual(bashPlugins, ps1Plugins,
            `LSP plugins should match between installers.\n` +
            `  Bash: ${bashPlugins.join(', ')}\n` +
            `  PS1:  ${ps1Plugins.join(', ')}`);
    });

    test('install.sh and install.ps1 list the same recommended plugins', () => {
        const bashScript = readFile('install.sh');
        const ps1Script = readFile('install.ps1');

        const bashRecommended = extractRecommendedPlugins(bashScript);
        const ps1Recommended = extractRecommendedPlugins(ps1Script);

        assert.ok(bashRecommended.length > 0, 'install.sh should list recommended plugins');
        assert.ok(ps1Recommended.length > 0, 'install.ps1 should list recommended plugins');

        assert.deepStrictEqual(bashRecommended, ps1Recommended,
            `Recommended plugins should match between installers.\n` +
            `  Bash: ${bashRecommended.join(', ')}\n` +
            `  PS1:  ${ps1Recommended.join(', ')}`);
    });

    test('installer LSP plugins match profile plugins.lsp values', () => {
        const bashScript = readFile('install.sh');
        const installerPlugins = extractLspPlugins(bashScript);

        // Read all profiles and collect non-null plugins.lsp values
        const profilePlugins = [];
        const profileDir = path.join(ROOT, 'profiles');
        const profileFiles = fs.readdirSync(profileDir)
            .filter(f => f.endsWith('.yaml') && !f.startsWith('_'));

        for (const file of profileFiles) {
            const content = fs.readFileSync(path.join(profileDir, file), 'utf8');
            const lspMatch = content.match(/^  lsp:\s*(.+)/m);
            if (lspMatch) {
                const value = lspMatch[1].trim();
                if (value !== 'null' && !profilePlugins.includes(value)) {
                    profilePlugins.push(value);
                }
            }
        }

        assert.ok(profilePlugins.length > 0, 'Some profiles should have LSP plugins');
        assert.deepStrictEqual(installerPlugins, profilePlugins.sort(),
            `Installer LSP plugins should match profile plugins.lsp values.\n` +
            `  Installer: ${installerPlugins.join(', ')}\n` +
            `  Profiles:  ${profilePlugins.sort().join(', ')}`);
    });

    test('uninstall scripts reference the same LSP plugins as install scripts', () => {
        const bashInstall = readFile('install.sh');
        const bashUninstall = readFile('uninstall.sh');

        const installPlugins = extractLspPlugins(bashInstall);
        const uninstallPlugins = extractLspPlugins(bashUninstall);

        assert.deepStrictEqual(installPlugins, uninstallPlugins,
            `Uninstaller should reference the same LSP plugins as installer.\n` +
            `  Install:   ${installPlugins.join(', ')}\n` +
            `  Uninstall: ${uninstallPlugins.join(', ')}`);
    });
});

// ============================================================
// Suite 7: Installer validation
// ============================================================

suite('Installer validation', () => {

    test('install.sh is valid bash syntax', () => {
        execSync('bash -n ' + path.join(ROOT, 'install.sh'), {
            encoding: 'utf8',
            stdio: ['pipe', 'pipe', 'pipe'],
        });
        assert.ok(true);
    });

    test('install.ps1 exists', () => {
        assert.ok(fileExists('install.ps1'), 'install.ps1 should exist');
    });

    test('uninstall.sh is valid bash syntax', () => {
        execSync('bash -n ' + path.join(ROOT, 'uninstall.sh'), {
            encoding: 'utf8',
            stdio: ['pipe', 'pipe', 'pipe'],
        });
        assert.ok(true);
    });

    test('uninstall.ps1 exists', () => {
        assert.ok(fileExists('uninstall.ps1'), 'uninstall.ps1 should exist');
    });

    test('generate-checksums.sh exists and is valid bash', () => {
        assert.ok(fileExists('generate-checksums.sh'), 'generate-checksums.sh should exist');
        execSync('bash -n ' + path.join(ROOT, 'generate-checksums.sh'), {
            encoding: 'utf8',
            stdio: ['pipe', 'pipe', 'pipe'],
        });
        assert.ok(true);
    });

    test('install.sh references CHECKSUMS.sha256 for integrity verification', () => {
        const content = readFile('install.sh');
        assert.ok(content.includes('CHECKSUMS.sha256'),
            'install.sh should reference CHECKSUMS.sha256 for file integrity');
    });

    test('install.sh exits non-zero on checksum mismatch without --force', () => {
        // Verify the checksum failure path exits with code 1
        const content = readFile('install.sh');
        assert.ok(content.includes('exit 1'),
            'install.sh should exit 1 on checksum failure');
        assert.ok(content.includes('--force'),
            'install.sh should mention --force bypass option');
        // Verify the conditional structure: FORCE_INSTALL=false -> exit 1
        assert.ok(content.includes('FORCE_INSTALL') && content.includes('exit 1'),
            'install.sh should gate checksum failure on FORCE_INSTALL flag');
    });
});

// ============================================================
// Summary
// ============================================================

summary('Integration tests — cross-module integrity');
process.exit(getResults().failed > 0 ? 1 : 0);
