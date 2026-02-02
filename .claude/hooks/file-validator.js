#!/usr/bin/env node
/**
 * PreToolUse Hook for Write/Edit - Validate file operations
 *
 * Triggered before Write or Edit tool execution.
 * Validates file paths and prevents dangerous overwrites.
 */

const fs = require('fs');
const path = require('path');

// Protected paths that should never be modified
const PROTECTED_PATHS = [
    // System files
    /^\/etc\//,
    /^\/usr\//,
    /^\/bin\//,
    /^\/sbin\//,
    /^C:\\Windows\\/i,
    /^C:\\Program Files/i,

    // User sensitive files
    /\.ssh\/.*$/,
    /\.gnupg\/.*$/,
    /\.aws\/credentials$/,
    /\.env\.production$/,

    // Git internals
    /\.git\/objects\//,
    /\.git\/refs\//,
    /\.git\/HEAD$/
];

// Files that need confirmation (warn but allow)
const SENSITIVE_FILES = [
    /\.env$/,
    /\.env\.local$/,
    /secrets?\./i,
    /credentials?\./i,
    /password/i,
    /api[_-]?key/i,
    /\.pem$/,
    /\.key$/,
    /id_rsa/,
    /id_ed25519/
];

// Parse input from hook
let filePath = '';
let toolName = '';
try {
    const input = process.env.HOOK_INPUT;
    if (input) {
        const parsed = JSON.parse(input);
        filePath = parsed.tool_input?.file_path || parsed.tool_input?.path || '';
        toolName = parsed.tool_name || 'unknown';
    }
} catch (e) {
    // Try reading from stdin
    try {
        const stdin = fs.readFileSync(0, 'utf8');
        const parsed = JSON.parse(stdin);
        filePath = parsed.tool_input?.file_path || parsed.tool_input?.path || '';
        toolName = parsed.tool_name || 'unknown';
    } catch (e2) {
        // No input
    }
}

// Normalize path for comparison
const normalizedPath = path.normalize(filePath).replace(/\\/g, '/');

// Check protected paths
for (const pattern of PROTECTED_PATHS) {
    if (pattern.test(normalizedPath) || pattern.test(filePath)) {
        const output = {
            decision: 'block',
            reason: `BLOCKED: Cannot modify protected path`,
            path: filePath
        };
        console.log(JSON.stringify(output));

        // Log the blocked operation
        const logFile = path.join(process.cwd(), '.claude', 'session.log');
        const logEntry = `[cs] ${new Date().toISOString().slice(0, 19)} BLOCKED ${toolName} on protected path: ${filePath}\n`;
        try {
            fs.appendFileSync(logFile, logEntry);
        } catch (e) {
            // Ignore
        }

        process.exit(0);
    }
}

// Check sensitive files (warn but allow)
const warnings = [];
for (const pattern of SENSITIVE_FILES) {
    if (pattern.test(normalizedPath) || pattern.test(path.basename(filePath))) {
        warnings.push('Modifying sensitive file');
        break;
    }
}

// Check if file exists (for overwrites)
if (fs.existsSync(filePath)) {
    const stats = fs.statSync(filePath);
    if (stats.size > 100000) { // > 100KB
        warnings.push('Large file modification');
    }
}

// Log warnings if any
if (warnings.length > 0) {
    const logFile = path.join(process.cwd(), '.claude', 'session.log');
    const logEntry = `[cs] ${new Date().toISOString().slice(0, 19)} WARNING ${toolName}: ${warnings.join(', ')} - ${filePath}\n`;
    try {
        fs.appendFileSync(logFile, logEntry);
    } catch (e) {
        // Ignore
    }
}

// Allow the operation
const output = {
    decision: 'allow',
    warnings: warnings.length > 0 ? warnings : undefined,
    path: filePath
};

console.log(JSON.stringify(output));
