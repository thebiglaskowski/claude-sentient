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

const { execSync } = require('child_process');
const os = require('os');
const { getNotificationConfig, logMessage } = require('./utils.cjs');

/**
 * Resolve the hook event name to a notification event.
 * Maps Claude Code hook events to user-facing notification event names.
 * @param {string} hookEvent - Raw HOOK_EVENT value
 * @param {Object} input - Parsed HOOK_INPUT
 * @returns {string} Resolved event name
 */
function resolveEvent(hookEvent, input) {
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
 * Build the platform-appropriate desktop notification command.
 * @param {string} title - Notification title
 * @param {string} body - Notification body
 * @returns {string|null} Shell command string, or null if unsupported
 */
function buildDesktopCommand(title, body) {
    const platform = os.platform();
    // Escape single quotes for shell safety
    const safeTitle = title.replace(/'/g, "'\\''");
    const safeBody = body.replace(/'/g, "'\\''");

    if (platform === 'linux') {
        return "notify-send '" + safeTitle + "' '" + safeBody + "'";
    }
    if (platform === 'darwin') {
        return "osascript -e 'display notification \"" + safeBody.replace(/"/g, '\\"') + "\" with title \"" + safeTitle.replace(/"/g, '\\"') + "\"'";
    }
    if (platform === 'win32') {
        return 'powershell -Command "New-BurntToastNotification -Text \'' + safeTitle + '\', \'' + safeBody + '\'"';
    }
    return null;
}

/**
 * Send a notification based on the configured type.
 * @param {Object} config - Notification config
 * @param {string} event - Resolved event name
 */
function notify(config, event) {
    const title = 'Claude Sentient';
    const body = event;
    const type = config.type || 'bell';

    if (type === 'bell') {
        process.stdout.write('\x07');
        return;
    }

    if (type === 'desktop') {
        const cmd = buildDesktopCommand(title, body);
        if (cmd) {
            try {
                execSync(cmd, { stdio: 'ignore', timeout: 2000 });
            } catch (_) {
                // Desktop notification failed silently
            }
        }
        return;
    }

    if (type === 'command' && config.command) {
        const userCmd = config.command
            .replace(/\{title\}/g, title)
            .replace(/\{body\}/g, body);
        try {
            execSync(userCmd, { stdio: 'ignore', timeout: 2000 });
        } catch (_) {
            // Custom command failed silently
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
        let input = {};
        try {
            input = JSON.parse(process.env.HOOK_INPUT || '{}');
        } catch (_) {}

        const event = resolveEvent(hookEvent, input);

        // Check if this event is in the allowlist
        if (config.events && !config.events[event]) {
            process.exit(0);
        }

        notify(config, event);
    } catch (e) {
        logMessage('Notification hook error: ' + e.message, 'WARNING');
    }
    process.exit(0);
}

module.exports = { buildDesktopCommand, resolveEvent, notify };
