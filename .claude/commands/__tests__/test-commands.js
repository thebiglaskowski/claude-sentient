#!/usr/bin/env node
/**
 * Validation tests for Claude Sentient command files.
 *
 * Validates all cs-*.md command files for:
 * - Valid YAML frontmatter
 * - Required fields (description)
 * - Non-empty content
 * - Proper file naming
 *
 * Run: node .claude/commands/__tests__/test-commands.js
 */

const assert = require('assert');
const fs = require('fs');
const path = require('path');

// Test infrastructure
let passed = 0;
let failed = 0;
const failures = [];

function test(name, fn) {
    try {
        fn();
        passed++;
        process.stdout.write(`  \x1b[32m✓\x1b[0m ${name}\n`);
    } catch (e) {
        failed++;
        failures.push({ name, error: e.message });
        process.stdout.write(`  \x1b[31m✗\x1b[0m ${name}\n    ${e.message}\n`);
    }
}

function suite(name, fn) {
    process.stdout.write(`\n\x1b[1m${name}\x1b[0m\n`);
    fn();
}

/**
 * Parse YAML frontmatter from a markdown file.
 * Returns { frontmatter, content } or null if no frontmatter.
 */
function parseFrontmatter(text) {
    const match = text.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
    if (!match) return null;

    const yamlText = match[1];
    const content = match[2];

    // Simple YAML key-value parser (handles: key: value)
    const frontmatter = {};
    for (const line of yamlText.split('\n')) {
        const kvMatch = line.match(/^(\w[\w-]*)\s*:\s*(.+)$/);
        if (kvMatch) {
            frontmatter[kvMatch[1]] = kvMatch[2].trim();
        }
    }

    return { frontmatter, content };
}

// Find command files
const commandsDir = path.resolve(__dirname, '..');
const commandFiles = fs.readdirSync(commandsDir)
    .filter(f => f.startsWith('cs-') && f.endsWith('.md'))
    .sort();

// ─────────────────────────────────────────────────────────────
suite('Command file inventory', () => {
    test('at least 10 command files exist', () => {
        assert.ok(commandFiles.length >= 10,
            `Expected >= 10 command files, found ${commandFiles.length}`);
    });

    test('all commands use cs- prefix', () => {
        for (const file of commandFiles) {
            assert.ok(file.startsWith('cs-'), `${file} should start with cs-`);
        }
    });
});

// ─────────────────────────────────────────────────────────────
suite('Command file structure', () => {
    for (const file of commandFiles) {
        const filePath = path.join(commandsDir, file);
        const content = fs.readFileSync(filePath, 'utf8');
        const commandName = file.replace('.md', '');

        test(`${commandName}: has YAML frontmatter`, () => {
            const parsed = parseFrontmatter(content);
            assert.ok(parsed !== null,
                `${file} is missing YAML frontmatter (--- ... ---)`);
        });

        test(`${commandName}: has description field`, () => {
            const parsed = parseFrontmatter(content);
            if (parsed) {
                assert.ok(parsed.frontmatter.description,
                    `${file} is missing 'description' in frontmatter`);
            }
        });

        test(`${commandName}: has non-empty content`, () => {
            const parsed = parseFrontmatter(content);
            if (parsed) {
                assert.ok(parsed.content.trim().length > 50,
                    `${file} content is too short (${parsed.content.trim().length} chars)`);
            }
        });

        test(`${commandName}: content size is reasonable`, () => {
            assert.ok(content.length < 50000,
                `${file} is too large (${content.length} chars, max 50000)`);
            assert.ok(content.length > 100,
                `${file} is too small (${content.length} chars, min 100)`);
        });
    }
});

// ─────────────────────────────────────────────────────────────
suite('Command CLAUDE.md', () => {
    test('CLAUDE.md exists in commands directory', () => {
        const claudeMd = path.join(commandsDir, 'CLAUDE.md');
        assert.ok(fs.existsSync(claudeMd), 'commands/CLAUDE.md should exist');
    });

    test('CLAUDE.md references all command files', () => {
        const claudeMd = fs.readFileSync(
            path.join(commandsDir, 'CLAUDE.md'), 'utf8'
        );
        for (const file of commandFiles) {
            const cmdName = '/' + file.replace('.md', '');
            assert.ok(claudeMd.includes(cmdName) || claudeMd.includes(file),
                `CLAUDE.md should reference ${cmdName}`);
        }
    });
});

// ─────────────────────────────────────────────────────────────
suite('cs-loop AUTO-FIX section', () => {
    test('cs-loop has AUTO-FIX sub-loop in VERIFY', () => {
        const loopPath = path.join(commandsDir, 'cs-loop.md');
        if (fs.existsSync(loopPath)) {
            const content = fs.readFileSync(loopPath, 'utf8');
            assert.ok(content.includes('AUTO-FIX'),
                'cs-loop should have AUTO-FIX section in VERIFY phase');
        }
    });

    test('cs-loop AUTO-FIX references fix_command', () => {
        const loopPath = path.join(commandsDir, 'cs-loop.md');
        if (fs.existsSync(loopPath)) {
            const content = fs.readFileSync(loopPath, 'utf8');
            assert.ok(content.includes('fix_command'),
                'cs-loop AUTO-FIX should reference fix_command from profiles');
        }
    });

    test('cs-loop AUTO-FIX has max 3 attempts limit', () => {
        const loopPath = path.join(commandsDir, 'cs-loop.md');
        if (fs.existsSync(loopPath)) {
            const content = fs.readFileSync(loopPath, 'utf8');
            assert.ok(content.includes('3 attempts') || content.includes('{n}/3'),
                'cs-loop AUTO-FIX should limit to 3 attempts');
        }
    });
});

// ─────────────────────────────────────────────────────────────
suite('cs-assess --map mode', () => {
    test('cs-assess mentions --map mode', () => {
        const assessPath = path.join(commandsDir, 'cs-assess.md');
        if (fs.existsSync(assessPath)) {
            const content = fs.readFileSync(assessPath, 'utf8');
            assert.ok(content.includes('--map'), 'cs-assess should document --map mode');
        }
    });
});

// ─────────────────────────────────────────────────────────────
suite('Collective intelligence features', () => {
    test('cs-learn has --scope argument documented', () => {
        const learnPath = path.join(commandsDir, 'cs-learn.md');
        if (fs.existsSync(learnPath)) {
            const content = fs.readFileSync(learnPath, 'utf8');
            assert.ok(content.includes('--scope'),
                'cs-learn should document --scope flag');
        }
    });

    test('cs-learn documents global/org/project scopes', () => {
        const learnPath = path.join(commandsDir, 'cs-learn.md');
        if (fs.existsSync(learnPath)) {
            const content = fs.readFileSync(learnPath, 'utf8');
            assert.ok(content.includes('global') && content.includes('org'),
                'cs-learn should document global and org scopes');
        }
    });

    test('cs-loop has cross-project memory search in INIT', () => {
        const loopPath = path.join(commandsDir, 'cs-loop.md');
        if (fs.existsSync(loopPath)) {
            const content = fs.readFileSync(loopPath, 'utf8');
            assert.ok(content.includes('scope:global') || content.includes('cross-project'),
                'cs-loop should have cross-project memory search');
        }
    });

    test('cs-init has dynamic profile generation', () => {
        const initPath = path.join(commandsDir, 'cs-init.md');
        if (fs.existsSync(initPath)) {
            const content = fs.readFileSync(initPath, 'utf8');
            assert.ok(content.includes('Dynamic profile generation') || content.includes('custom profile'),
                'cs-init should have dynamic profile generation');
        }
    });
});

// ─────────────────────────────────────────────────────────────
suite('cs-deploy command', () => {
    test('cs-deploy.md exists', () => {
        const deployPath = path.join(commandsDir, 'cs-deploy.md');
        assert.ok(fs.existsSync(deployPath), 'cs-deploy.md should exist');
    });

    test('cs-deploy has YAML frontmatter', () => {
        const deployPath = path.join(commandsDir, 'cs-deploy.md');
        if (fs.existsSync(deployPath)) {
            const content = fs.readFileSync(deployPath, 'utf8');
            const parsed = parseFrontmatter(content);
            assert.ok(parsed !== null, 'cs-deploy should have YAML frontmatter');
        }
    });
});

// ─────────────────────────────────────────────────────────────
suite('Native memory integration', () => {
    test('cs-learn documents --scope personal', () => {
        const learnPath = path.join(commandsDir, 'cs-learn.md');
        if (fs.existsSync(learnPath)) {
            const content = fs.readFileSync(learnPath, 'utf8');
            assert.ok(content.includes('personal'),
                'cs-learn should document --scope personal');
        }
    });

    test('cs-init mentions @rules/ imports', () => {
        const initPath = path.join(commandsDir, 'cs-init.md');
        if (fs.existsSync(initPath)) {
            const content = fs.readFileSync(initPath, 'utf8');
            assert.ok(content.includes('@rules/'),
                'cs-init should mention @rules/ imports for nested CLAUDE.md');
        }
    });

    test('cs-loop notes path-scoped rules', () => {
        const loopPath = path.join(commandsDir, 'cs-loop.md');
        if (fs.existsSync(loopPath)) {
            const content = fs.readFileSync(loopPath, 'utf8');
            assert.ok(content.includes('paths:') || content.includes('path-scoped') || content.includes('frontmatter'),
                'cs-loop should note that rules load via path matching');
        }
    });
});

// ─────────────────────────────────────────────────────────────
suite('Path-scoped rules validation', () => {
    const rulesDir = path.resolve(__dirname, '../../rules');

    // Rules that should have paths: frontmatter
    const conditionalRules = [
        'security.md', 'testing.md', 'api-design.md', 'database.md',
        'ui-ux-design.md', 'error-handling.md', 'performance.md',
        'logging.md', 'terminal-ui.md', 'documentation.md',
        'prompt-structure.md', 'git-workflow.md'
    ];

    // Rules that should NOT have paths: frontmatter
    const unconditionalRules = ['anthropic-patterns.md', 'code-quality.md'];

    // Skip files that aren't rule content
    const skipFiles = ['README.md', 'learnings.md'];

    test('conditional rule files exist in .claude/rules/', () => {
        for (const file of conditionalRules) {
            const filePath = path.join(rulesDir, file);
            assert.ok(fs.existsSync(filePath),
                `.claude/rules/${file} should exist`);
        }
    });

    for (const file of conditionalRules) {
        test(`${file}: has paths: frontmatter`, () => {
            const filePath = path.join(rulesDir, file);
            if (fs.existsSync(filePath)) {
                const content = fs.readFileSync(filePath, 'utf8');
                const parsed = parseFrontmatter(content);
                assert.ok(parsed !== null,
                    `${file} should have frontmatter`);
                // Check raw YAML for paths: key
                const yamlMatch = content.match(/^---\n([\s\S]*?)\n---/);
                assert.ok(yamlMatch && yamlMatch[1].includes('paths:'),
                    `${file} frontmatter should contain paths: key`);
            }
        });
    }

    for (const file of unconditionalRules) {
        test(`${file}: does NOT have paths: frontmatter`, () => {
            const filePath = path.join(rulesDir, file);
            if (fs.existsSync(filePath)) {
                const content = fs.readFileSync(filePath, 'utf8');
                const hasFrontmatter = content.startsWith('---\n');
                if (hasFrontmatter) {
                    const yamlMatch = content.match(/^---\n([\s\S]*?)\n---/);
                    if (yamlMatch) {
                        assert.ok(!yamlMatch[1].includes('paths:'),
                            `${file} should NOT have paths: in frontmatter (unconditional rule)`);
                    }
                }
                // No frontmatter at all is also fine for unconditional rules
            }
        });
    }

    test('unconditional rule files exist in .claude/rules/', () => {
        for (const file of unconditionalRules) {
            const filePath = path.join(rulesDir, file);
            assert.ok(fs.existsSync(filePath),
                `.claude/rules/${file} should exist`);
        }
    });
});

// ─────────────────────────────────────────────────────────────
// Report
process.stdout.write('\n─────────────────────────────────────\n');
process.stdout.write(`\x1b[1mResults:\x1b[0m ${passed} passed, ${failed} failed\n`);

if (failures.length > 0) {
    process.stdout.write('\n\x1b[31mFailures:\x1b[0m\n');
    for (const f of failures) {
        process.stdout.write(`  - ${f.name}: ${f.error}\n`);
    }
}

process.exit(failed > 0 ? 1 : 0);
