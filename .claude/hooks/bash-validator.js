#!/usr/bin/env node
/**
 * PreToolUse Hook for Bash - Validate dangerous commands
 *
 * Triggered before Bash tool execution.
 * Blocks dangerous commands that could harm the system.
 */

const fs = require('fs');
const path = require('path');

// Dangerous command patterns
const DANGEROUS_PATTERNS = [
    // Destructive file operations
    { pattern: /rm\s+-rf\s+[\/~]/, reason: 'Recursive delete from root or home' },
    { pattern: /rm\s+-rf\s+\*/, reason: 'Recursive delete all files' },
    { pattern: /rm\s+-rf\s+\./, reason: 'Recursive delete current directory' },

    // Disk operations
    { pattern: />\s*\/dev\/sd/, reason: 'Direct write to disk device' },
    { pattern: /mkfs/, reason: 'Filesystem creation' },
    { pattern: /dd\s+if=.*of=\/dev/, reason: 'Direct disk write with dd' },

    // Permission changes
    { pattern: /chmod\s+-R\s+777\s+\//, reason: 'Recursive chmod 777 from root' },
    { pattern: /chown\s+-R\s+.*\s+\//, reason: 'Recursive chown from root' },

    // System modification
    { pattern: /:(){ :|:& };:/, reason: 'Fork bomb' },
    { pattern: />\s*\/dev\/null\s*2>&1\s*&\s*disown/, reason: 'Background process hiding' },

    // Network attacks
    { pattern: /nc\s+-l.*-e\s+\/bin/, reason: 'Netcat reverse shell' },

    // History manipulation
    { pattern: /history\s+-c/, reason: 'Clear command history' },
    { pattern: /shred.*\.bash_history/, reason: 'Shred bash history' }
];

// Warning patterns (allow but log)
const WARNING_PATTERNS = [
    { pattern: /sudo\s+/, reason: 'Using sudo' },
    { pattern: /curl.*\|\s*sh/, reason: 'Piping curl to shell' },
    { pattern: /wget.*\|\s*sh/, reason: 'Piping wget to shell' },
    { pattern: /npm\s+install\s+-g/, reason: 'Global npm install' },
    { pattern: /pip\s+install\s+--user/, reason: 'User pip install' }
];

// Parse input from hook
let command = '';
try {
    const input = process.env.HOOK_INPUT;
    if (input) {
        const parsed = JSON.parse(input);
        command = parsed.tool_input?.command || parsed.command || '';
    }
} catch (e) {
    // Try reading from stdin as fallback
    try {
        const stdin = fs.readFileSync(0, 'utf8');
        const parsed = JSON.parse(stdin);
        command = parsed.tool_input?.command || parsed.command || '';
    } catch (e2) {
        // No input
    }
}

// Check for dangerous patterns
for (const { pattern, reason } of DANGEROUS_PATTERNS) {
    if (pattern.test(command)) {
        const output = {
            decision: 'block',
            reason: `BLOCKED: ${reason}`,
            pattern: pattern.toString(),
            command: command.substring(0, 100)
        };
        console.log(JSON.stringify(output));

        // Log the blocked command
        const logFile = path.join(process.cwd(), '.claude', 'session.log');
        const logEntry = `[cs] ${new Date().toISOString().slice(0, 19)} BLOCKED dangerous command: ${reason}\n`;
        try {
            fs.appendFileSync(logFile, logEntry);
        } catch (e) {
            // Ignore log errors
        }

        process.exit(0);
    }
}

// Check for warning patterns
const warnings = [];
for (const { pattern, reason } of WARNING_PATTERNS) {
    if (pattern.test(command)) {
        warnings.push(reason);
    }
}

// Log warnings if any
if (warnings.length > 0) {
    const logFile = path.join(process.cwd(), '.claude', 'session.log');
    const logEntry = `[cs] ${new Date().toISOString().slice(0, 19)} WARNING: ${warnings.join(', ')}\n`;
    try {
        fs.appendFileSync(logFile, logEntry);
    } catch (e) {
        // Ignore log errors
    }
}

// Allow the command
const output = {
    decision: 'allow',
    warnings: warnings.length > 0 ? warnings : undefined
};

console.log(JSON.stringify(output));
