#!/usr/bin/env node
/**
 * PreToolUse Hook for Write/Edit - Validate file operations
 *
 * Triggered before Write or Edit tool execution.
 * Validates file paths and prevents dangerous overwrites.
 */

const fs = require('fs');
const os = require('os');
const path = require('path');
const { parseHookInput, logMessage, getProjectRoot, validateFilePath, LARGE_FILE_THRESHOLD } = require('./utils.cjs');

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

    // Git internals, config, and hooks (can contain credentials or enable code execution)
    /\.git\/objects\//,
    /\.git\/refs\//,
    /\.git\/HEAD$/,
    /\.git\/config$/,
    /\.git\/hooks\//
];

// Files that need confirmation (warn but allow)
const SENSITIVE_FILES = [
    /\.env$/,
    /\.env\.local$/,
    /\.env\.staging$/,
    /\.env\.development$/,
    /\.env\.test$/,
    /secrets?\./i,
    /credentials?\./i,
    /password/i,
    /api[_-]?key/i,
    /\.pem$/,
    /\.key$/,
    /id_rsa/,
    /id_ed25519/,
    /\.netrc$/,
    /\.npmrc$/
];

// Parse input from hook
const parsed = parseHookInput();
const filePath = parsed.tool_input?.file_path || parsed.tool_input?.path || '';
const toolName = parsed.tool_name || 'unknown';

// Validate path for null bytes, control chars, excessive length
const pathError = validateFilePath(filePath);
if (pathError) {
    console.log(JSON.stringify({ decision: 'block', reason: `BLOCKED: ${pathError}`, path: filePath }));
    logMessage(`BLOCKED ${toolName}: ${pathError} - ${filePath}`, 'BLOCKED');
    process.exit(0);
}

// Resolve to absolute path and check for symlinks
let resolvedPath = filePath;
try {
    // Resolve symlinks to prevent traversal attacks
    if (fs.existsSync(filePath)) {
        const realPath = fs.realpathSync(filePath);
        if (realPath !== path.resolve(filePath)) {
            // File is a symlink — use resolved path for validation
            resolvedPath = realPath;
        }
    } else {
        // For new files, resolve the parent directory
        const parentDir = path.dirname(filePath);
        if (fs.existsSync(parentDir)) {
            const realParent = fs.realpathSync(parentDir);
            resolvedPath = path.join(realParent, path.basename(filePath));
        }
    }
} catch (e) {
    // If resolution fails, use original path
}

// Normalize path for comparison
const normalizedPath = path.normalize(resolvedPath).replace(/\\/g, '/');

// Ensure path stays within project root
const projectRoot = getProjectRoot();
const absolutePath = path.resolve(resolvedPath);
// Block writes to global Claude Code settings (even though ~/.claude is allowed for state)
const claudeHome = path.join(os.homedir(), '.claude');
const globalSettingsProtected = [
    path.join(claudeHome, 'settings.json'),
    path.join(claudeHome, 'settings.local.json')
];
if (globalSettingsProtected.some(p => absolutePath === p)) {
    const output = { decision: 'block', reason: 'BLOCKED: Cannot modify global Claude Code settings', path: filePath };
    console.log(JSON.stringify(output));
    logMessage(`BLOCKED ${toolName} on global settings: ${filePath}`, 'BLOCKED');
    process.exit(0);
}

if (!absolutePath.startsWith(path.resolve(projectRoot) + path.sep) &&
    !absolutePath.startsWith(os.tmpdir() + path.sep) &&
    !absolutePath.startsWith(claudeHome + path.sep)) {
    const output = {
        decision: 'block',
        reason: 'BLOCKED: Cannot modify files outside project root',
        path: filePath
    };
    console.log(JSON.stringify(output));
    logMessage(`BLOCKED ${toolName} outside project root: ${filePath}`, 'BLOCKED');
    process.exit(0);
}

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
        logMessage(`BLOCKED ${toolName} on protected path: ${filePath}`, 'BLOCKED');

        process.exit(0);
    }
}

// Warn on writes to ~/.claude/projects/ (auto-memory persistence vector)
const claudeProjects = path.join(claudeHome, 'projects');
if (absolutePath.startsWith(claudeProjects + path.sep)) {
    logMessage(`WARNING ${toolName}: Writing to auto-memory directory: ${filePath}`, 'WARNING');
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
    if (stats.size > LARGE_FILE_THRESHOLD) {
        warnings.push('Large file modification');
    }
}

// Log warnings if any
if (warnings.length > 0) {
    logMessage(`${toolName}: ${warnings.join(', ')} - ${filePath}`, 'WARNING');
}

// Allow the operation
const output = {
    decision: 'allow',
    warnings: warnings.length > 0 ? warnings : undefined,
    path: filePath
};

console.log(JSON.stringify(output));
