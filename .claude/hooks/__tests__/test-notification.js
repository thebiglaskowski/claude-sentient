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

const { buildDesktopCommand, resolveEvent, notify, TITLES, getBody } = require('../notification.cjs');

suite('buildDesktopCommand', () => {
    test('returns platform-appropriate array', () => {
        const cmd = buildDesktopCommand('Test Title', 'Test Body');
        const platform = process.platform;
        if (platform === 'linux') {
            assert.ok(Array.isArray(cmd), 'should return an array');
            assert.strictEqual(cmd[0], 'notify-send');
            assert.strictEqual(cmd[1], 'Test Title');
            assert.strictEqual(cmd[2], 'Test Body');
        } else if (platform === 'darwin') {
            assert.ok(Array.isArray(cmd), 'should return an array');
            assert.strictEqual(cmd[0], 'osascript');
        } else if (platform === 'win32') {
            assert.strictEqual(cmd, null, 'win32 should return null');
        }
    });

    test('returns null on win32', () => {
        // buildDesktopCommand uses process.platform which we cannot mock easily,
        // but we can verify the function handles the unsupported case
        const cmd = buildDesktopCommand('Title', 'Body');
        if (process.platform === 'win32') {
            assert.strictEqual(cmd, null);
        } else {
            assert.ok(Array.isArray(cmd), 'non-win32 should return array');
        }
    });

    test('includes title and body in command array', () => {
        const cmd = buildDesktopCommand("it's a test", "don't panic");
        if (process.platform === 'linux') {
            assert.strictEqual(cmd[1], "it's a test", 'title preserved as array element');
            assert.strictEqual(cmd[2], "don't panic", 'body preserved as array element');
        }
        // execFileSync with array args does not need shell escaping
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

    test('handles null input without crashing', () => {
        const result = resolveEvent(null, null);
        assert.strictEqual(result, 'unknown');
    });

    test('handles undefined input without crashing', () => {
        const result = resolveEvent(undefined, undefined);
        assert.strictEqual(result, 'unknown');
    });

    test('handles empty string hookEvent', () => {
        const result = resolveEvent('', {});
        assert.strictEqual(result, 'unknown');
    });
});

suite('TITLES and getBody', () => {
    test('TITLES has entries for known events', () => {
        assert.strictEqual(TITLES['Stop'], 'Claude Sentient: Done');
        assert.strictEqual(TITLES['gate-failure'], 'Claude Sentient: Gate Failed');
        assert.strictEqual(TITLES['task-completed'], 'Claude Sentient: Task Complete');
        assert.strictEqual(TITLES['session-end'], 'Claude Sentient: Session Ended');
    });

    test('getBody returns human-readable message for Stop', () => {
        assert.strictEqual(getBody('Stop', {}), 'Work loop completed.');
    });

    test('getBody returns human-readable message for session-end', () => {
        assert.strictEqual(getBody('session-end', {}), 'Session has ended.');
    });

    test('getBody returns human-readable message for task-completed', () => {
        assert.strictEqual(getBody('task-completed', {}), 'A task was marked complete.');
    });

    test('getBody includes exit code for gate-failure', () => {
        assert.strictEqual(getBody('gate-failure', { exit_code: 1 }), 'Gate failed (exit 1)');
    });

    test('getBody uses ? for gate-failure with no exit code', () => {
        assert.strictEqual(getBody('gate-failure', {}), 'Gate failed (exit ?)');
    });

    test('getBody falls back to event name for unknown events', () => {
        assert.strictEqual(getBody('SomeEvent', {}), 'SomeEvent');
    });
});

suite('notify', () => {
    test('bell type writes bell character to stdout', () => {
        let written = '';
        const origWrite = process.stdout.write;
        process.stdout.write = (str) => { written += str; return true; };
        try {
            notify({ type: 'bell' }, 'Stop', {});
            assert.strictEqual(written, '\x07');
        } finally {
            process.stdout.write = origWrite;
        }
    });

    test('defaults to bell when type is not set', () => {
        let written = '';
        const origWrite = process.stdout.write;
        process.stdout.write = (str) => { written += str; return true; };
        try {
            notify({}, 'Stop', {});
            assert.strictEqual(written, '\x07');
        } finally {
            process.stdout.write = origWrite;
        }
    });

    test('desktop type does not crash on unsupported platform', () => {
        // On win32 buildDesktopCommand returns null, so notify should just return
        assert.doesNotThrow(() => {
            notify({ type: 'desktop' }, 'Stop', {});
        });
    });

    test('command type with missing command does not crash', () => {
        assert.doesNotThrow(() => {
            notify({ type: 'command' }, 'Stop', {});
        });
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
