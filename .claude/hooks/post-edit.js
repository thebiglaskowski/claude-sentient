#!/usr/bin/env node
/**
 * PostToolUse Hook for Write/Edit - Track changes and suggest lint
 *
 * Triggered after Write or Edit tool execution.
 * Tracks file changes and suggests running lint for code files.
 */

const fs = require('fs');
const path = require('path');

const stateDir = path.join(process.cwd(), '.claude', 'state');
const changesFile = path.join(stateDir, 'file_changes.json');

// Ensure state directory exists
if (!fs.existsSync(stateDir)) {
    fs.mkdirSync(stateDir, { recursive: true });
}

// Parse input from hook
let filePath = '';
let toolName = '';
let success = true;
try {
    const input = process.env.HOOK_INPUT;
    if (input) {
        const parsed = JSON.parse(input);
        filePath = parsed.tool_input?.file_path || parsed.tool_input?.path || '';
        toolName = parsed.tool_name || 'unknown';
        success = parsed.tool_result?.success !== false;
    }
} catch (e) {
    // Try reading from stdin
    try {
        const stdin = fs.readFileSync(0, 'utf8');
        const parsed = JSON.parse(stdin);
        filePath = parsed.tool_input?.file_path || parsed.tool_input?.path || '';
        toolName = parsed.tool_name || 'unknown';
        success = parsed.tool_result?.success !== false;
    } catch (e2) {
        // No input
    }
}

// Only track successful operations
if (!success || !filePath) {
    console.log(JSON.stringify({ tracked: false }));
    process.exit(0);
}

// Track file change
let changes = [];
if (fs.existsSync(changesFile)) {
    try {
        changes = JSON.parse(fs.readFileSync(changesFile, 'utf8'));
    } catch (e) {
        changes = [];
    }
}

// Add to changes if not already tracked
const changeEntry = {
    path: filePath,
    tool: toolName,
    timestamp: new Date().toISOString()
};

// Check if already in list (update timestamp)
const existingIndex = changes.findIndex(c => c.path === filePath);
if (existingIndex >= 0) {
    changes[existingIndex] = changeEntry;
} else {
    changes.push(changeEntry);
}

// Keep only last 100 changes
if (changes.length > 100) {
    changes = changes.slice(-100);
}

fs.writeFileSync(changesFile, JSON.stringify(changes, null, 2));

// Determine file type for lint suggestion
const ext = path.extname(filePath).toLowerCase();
const codeExtensions = {
    '.py': 'ruff check',
    '.ts': 'eslint',
    '.tsx': 'eslint',
    '.js': 'eslint',
    '.jsx': 'eslint',
    '.go': 'golangci-lint run',
    '.rs': 'cargo clippy',
    '.rb': 'rubocop',
    '.java': 'checkstyle',
    '.sh': 'shellcheck'
};

const suggestions = [];
if (codeExtensions[ext]) {
    suggestions.push(`Consider running lint: ${codeExtensions[ext]}`);
}

// Log the change
const logFile = path.join(process.cwd(), '.claude', 'session.log');
const logEntry = `[cs] ${new Date().toISOString().slice(0, 19)} ${toolName} completed: ${filePath}\n`;
try {
    fs.appendFileSync(logFile, logEntry);
} catch (e) {
    // Ignore
}

// Output
const output = {
    tracked: true,
    path: filePath,
    totalChanges: changes.length,
    suggestions: suggestions.length > 0 ? suggestions : undefined
};

console.log(JSON.stringify(output));
