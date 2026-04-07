#!/usr/bin/env node
/**
 * Tests for notification.cjs hook
 *
 * Run: node .claude/hooks/__tests__/test-notification.js
 */

const assert = require('assert');
const fs = require('fs');
const path = require('path');
const os = require('os');

// Shared test infrastructure
const { test, suite, summary, getResults } = require('../../../test-utils');

suite('notification.cjs — module loading', () => {
    test('module loads without error', () => {
        const mod = require('../notification.cjs');
        assert.ok(mod);
        assert.strictEqual(typeof mod.buildDesktopCommand, 'function');
        assert.strictEqual(typeof mod.resolveEvent, 'function');
        assert.strictEqual(typeof mod.notify, 'function');
    });
});

const { buildDesktopCommand, resolveEvent, notify } = require('../notification.cjs');

suite('buildDesktopCommand', () => {
    test('returns platform-appropriate string', () => {
        const cmd = buildDesktopCommand('Test Title', 'Test Body');
        const platform = os.platform();
        if (platform === 'linux') {
            assert.ok(cmd.includes('notify-send'), 'Linux should use notify-send');
        } else if (platform === 'darwin') {
            assert.ok(cmd.includes('osascript'), 'macOS should use osascript');
        } else if (platform === 'win32') {
            assert.ok(cmd.includes('powershell'), 'Windows should use powershell');
        }
        // On any platform, the command should be a non-empty string
        assert.strictEqual(typeof cmd, 'string');
        assert.ok(cmd.length > 0);
    });

    test('escapes single quotes in title and body', () => {
        const cmd = buildDesktopCommand("it's a test", "don't panic");
        assert.ok(cmd, 'command should not be null');
        // The raw unescaped single quotes should not appear as-is in a way
        // that would break the shell command
        assert.ok(!cmd.includes("it's a test"), 'title single quote should be escaped');
        assert.ok(!cmd.includes("don't panic"), 'body single quote should be escaped');
    });
});

suite('resolveEvent', () => {
    test('maps PostToolUse with non-zero exit_code to gate-failure', () => {
        const result = resolveEvent('PostToolUse', { exit_code: 1 });
        assert.strictEqual(result, 'gate-failure');
    });

    test('maps PostToolUse with exit_code 0 to PostToolUse', () => {
        const result = resolveEvent('PostToolUse', { exit_code: 0 });
        assert.strictEqual(result, 'PostToolUse');
    });

    test('maps TaskCompleted to task-completed', () => {
        const result = resolveEvent('TaskCompleted', {});
        assert.strictEqual(result, 'task-completed');
    });

    test('maps SessionEnd to session-end', () => {
        const result = resolveEvent('SessionEnd', {});
        assert.strictEqual(result, 'session-end');
    });

    test('passes Stop through unchanged', () => {
        const result = resolveEvent('Stop', {});
        assert.strictEqual(result, 'Stop');
    });

    test('passes unknown events through unchanged', () => {
        const result = resolveEvent('SomeRandomEvent', {});
        assert.strictEqual(result, 'SomeRandomEvent');
    });
});

suite('getNotificationConfig', () => {
    const { getNotificationConfig } = require('../utils.cjs');

    test('returns null for nonexistent path', () => {
        const result = getNotificationConfig('/tmp/nonexistent-project-' + Date.now());
        assert.strictEqual(result, null);
    });

    test('returns null when config exists but disabled', () => {
        const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'cs-notif-test-'));
        const stateDir = path.join(tmpDir, '.claude', 'state');
        fs.mkdirSync(stateDir, { recursive: true });
        fs.writeFileSync(
            path.join(stateDir, 'notification-config.json'),
            JSON.stringify({ enabled: false, type: 'bell' })
        );
        const result = getNotificationConfig(tmpDir);
        assert.strictEqual(result, null);
        // Cleanup
        fs.rmSync(tmpDir, { recursive: true, force: true });
    });

    test('returns config when enabled', () => {
        const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'cs-notif-test-'));
        const stateDir = path.join(tmpDir, '.claude', 'state');
        fs.mkdirSync(stateDir, { recursive: true });
        const config = { enabled: true, type: 'bell', events: { Stop: true } };
        fs.writeFileSync(
            path.join(stateDir, 'notification-config.json'),
            JSON.stringify(config)
        );
        const result = getNotificationConfig(tmpDir);
        assert.ok(result);
        assert.strictEqual(result.enabled, true);
        assert.strictEqual(result.type, 'bell');
        assert.strictEqual(result.events.Stop, true);
        // Cleanup
        fs.rmSync(tmpDir, { recursive: true, force: true });
    });
});

summary();
process.exit(getResults().failed > 0 ? 1 : 0);
