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
    /\.git\/hooks\//,

    // Container and package manager credentials
    /\.kube[/\\]config$/,           // Kubernetes cluster credentials
    /\.docker[/\\]config\.json$/,   // Docker registry credentials
    /\.cargo[/\\]credentials$/,      // Rust crates.io token

    // Shell config files (persistent code execution)
    /[/\\]\.bashrc$/,               // persistent shell code execution
    /[/\\]\.zshrc$/,
    /[/\\]\.bash_profile$/,
    /[/\\]\.profile$/,
    /[/\\]\.gitconfig$/,            // can redirect git hook execution
    /[/\\]\.aws[/\\]config$/,       // AWS role/credential_process config
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

/**
 * Resolve the real path of a file, following symlinks.
 * @param {string} filePath - Path to resolve
 * @returns {string} Resolved path, or original path if resolution fails
 */
function resolveRealPath(filePath) {
    try { return fs.realpathSync(filePath); } catch (_) { return filePath; }
}

/**
 * Block a file operation with a reason and exit.
 * @param {string} toolName - Name of the tool being blocked
 * @param {string} reason - Reason for blocking
 * @param {string} filePath - Path being blocked
 */
function blockPath(toolName, reason, filePath) {
    console.log(JSON.stringify({ decision: 'block', reason: `BLOCKED: ${reason}`, path: filePath }));
    logMessage(`BLOCKED ${toolName}: ${reason} - ${filePath}`, 'BLOCKED');
    process.exit(0);
}

function main() {
    // Parse input from hook
    const parsed = parseHookInput();
    const filePath = parsed.tool_input?.file_path || parsed.tool_input?.path || '';
    const toolName = parsed.tool_name || 'unknown';

    // Validate path for null bytes, control chars, excessive length
    const pathError = validateFilePath(filePath);
    if (pathError) {
        blockPath(toolName, pathError, filePath);
    }

    // Resolve to absolute path and check for symlinks
    let resolvedPath = filePath;
    const fileExists = fs.existsSync(filePath);
    if (fileExists) {
        const realPath = resolveRealPath(filePath);
        if (realPath !== path.resolve(filePath)) resolvedPath = realPath;
    } else {
        const parentDir = path.dirname(filePath);
        if (fs.existsSync(parentDir)) {
            resolvedPath = path.join(resolveRealPath(parentDir), path.basename(filePath));
        }
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
        blockPath(toolName, 'Cannot modify global Claude Code settings', filePath);
    }

    // Block writes to global Claude Code commands and rules (cross-project poisoning vector)
    if (absolutePath.startsWith(path.join(claudeHome, 'commands') + path.sep) ||
        absolutePath.startsWith(path.join(claudeHome, 'rules') + path.sep)) {
        blockPath(toolName, 'Cannot modify global Claude Code commands or rules', filePath);
    }

    if (!absolutePath.startsWith(path.resolve(projectRoot) + path.sep) &&
        !absolutePath.startsWith(os.tmpdir() + path.sep) &&
        !absolutePath.startsWith(claudeHome + path.sep)) {
        blockPath(toolName, 'Cannot modify files outside project root', filePath);
    }

    // Protect hook scripts from self-modification
    const hookDir = path.join(projectRoot, '.claude', 'hooks');
    if (resolvedPath.startsWith(hookDir + path.sep) && resolvedPath.endsWith('.cjs')) {
        blockPath(toolName, 'Cannot modify active hook scripts. Edit hooks outside a running session or restart after changes', filePath);
    }

    // Check protected paths
    for (const pattern of PROTECTED_PATHS) {
        if (pattern.test(normalizedPath) || pattern.test(filePath)) {
            blockPath(toolName, 'Cannot modify protected path', filePath);
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

    // Check if file exists (for overwrites) — reuse earlier existsSync result
    if (fileExists) {
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
}

main();
