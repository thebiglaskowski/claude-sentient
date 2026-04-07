#!/usr/bin/env node
/**
 * Notification hook for Claude Sentient
 *
 * Provides audio/visual feedback for lifecycle events (gate failures,
 * task completions, session end, stop). Configured via
 * .claude/state/notification-config.json.
 *
 * Three notification types:
 *   - bell: Terminal bell character (\x07)
 *   - desktop: OS-native notification (notify-send, osascript, PowerShell)
 *   - command: Custom command with {title} and {body} placeholders
 */

const { execFileSync } = require('child_process');
const { getNotificationConfig, parseHookInput, logMessage } = require('./utils.cjs');

/**
 * Resolve the hook event name to a notification event.
 * Maps Claude Code hook events to user-facing notification event names.
 * @param {string} hookEvent - Raw HOOK_EVENT value
 * @param {Object} input - Parsed HOOK_INPUT
 * @returns {string} Resolved event name
 */
function resolveEvent(hookEvent, input) {
    if (!hookEvent) return 'unknown';
    if (hookEvent === 'PostToolUse') {
        const exitCode = input && input.exit_code;
        if (exitCode !== null && exitCode !== undefined && exitCode !== 0) {
            return 'gate-failure';
        }
        return 'PostToolUse';
    }
    if (hookEvent === 'TaskCompleted') return 'task-completed';
    if (hookEvent === 'SessionEnd') return 'session-end';
    return hookEvent;
}

/**
 * Human-readable title for each notification event.
 */
const TITLES = {
    'Stop': 'Claude Sentient: Done',
    'gate-failure': 'Claude Sentient: Gate Failed',
    'task-completed': 'Claude Sentient: Task Complete',
    'session-end': 'Claude Sentient: Session Ended'
};

/**
 * Human-readable body for each notification event.
 * @param {string} event - Resolved event name
 * @param {Object} input - Parsed hook input (used for exit code in gate-failure)
 * @returns {string}
 */
function getBody(event, input) {
    if (event === 'gate-failure') {
        const exitCode = input && input.exit_code;
        return 'Gate failed (exit ' + (exitCode || '?') + ')';
    }
    const bodies = {
        'Stop': 'Work loop completed.',
        'task-completed': 'A task was marked complete.',
        'session-end': 'Session has ended.'
    };
    return bodies[event] || event;
}

/**
 * Build the platform-appropriate desktop notification command as an
 * array suitable for execFileSync(parts[0], parts.slice(1)).
 * @param {string} title - Notification title
 * @param {string} body - Notification body
 * @returns {string[]|null} Command array, or null if unsupported
 */
function buildDesktopCommand(title, body) {
    const platform = process.platform;

    if (platform === 'linux') {
        return ['notify-send', title, body];
    }
    if (platform === 'darwin') {
        return ['osascript', '-e', 'display notification "' + body.replace(/"/g, '\\"') + '" with title "' + title.replace(/"/g, '\\"') + '"'];
    }
    // win32: no reliable built-in; return null to fall back to bell
    return null;
}

/**
 * Send a notification based on the configured type.
 * @param {Object} config - Notification config
 * @param {string} event - Resolved event name
 * @param {Object} input - Parsed hook input (for context like exit codes)
 */
function notify(config, event, input) {
    const title = TITLES[event] || 'Claude Sentient';
    const body = getBody(event, input);
    const type = config.type || 'bell';

    if (type === 'bell') {
        process.stdout.write('\x07');
        return;
    }

    if (type === 'desktop') {
        const cmd = buildDesktopCommand(title, body);
        if (cmd) {
            try {
                execFileSync(cmd[0], cmd.slice(1), { stdio: 'ignore', timeout: 2000 });
            } catch (_) {
                // Desktop notification failed silently
            }
        }
        return;
    }

    if (type === 'command' && config.command) {
        const parts = config.command
            .replace(/\{title\}/g, title)
            .replace(/\{body\}/g, body)
            .split(/\s+/)
            .filter(Boolean);
        if (parts.length > 0) {
            try {
                execFileSync(parts[0], parts.slice(1), { stdio: 'ignore', timeout: 2000 });
            } catch (_) {
                // Custom command failed silently
            }
        }
        return;
    }
}

// Main execution
if (require.main === module) {
    try {
        const config = getNotificationConfig();
        if (!config) process.exit(0);

        const hookEvent = process.env.HOOK_EVENT || '';
        const input = parseHookInput() || {};

        const event = resolveEvent(hookEvent, input);

        // Check if this event is in the allowlist
        if (config.events && !config.events[event]) {
            process.exit(0);
        }

        notify(config, event, input);
    } catch (e) {
        logMessage('Notification hook error: ' + e.message, 'WARNING');
    }
    process.exit(0);
}

module.exports = { buildDesktopCommand, resolveEvent, notify, TITLES, getBody };
