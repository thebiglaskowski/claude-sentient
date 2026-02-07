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
