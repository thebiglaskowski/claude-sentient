#!/usr/bin/env node
/**
 * PostToolUse Hook — Unified observer for all post-tool events
 *
 * For Write/Edit: Tracks file changes, suggests lint
 * For Bash: Records gate exit codes, masks large output
 *
 * Merged from post-edit.cjs + gate-monitor.cjs to eliminate one
 * process spawn per PostToolUse event.
 */

const fs = require('fs');
const path = require('path');
const { parseHookInput, loadState, saveState, logMessage, getProjectRoot,
        MAX_FILE_CHANGES, MAX_LOGGED_COMMAND_LENGTH, MAX_GATE_HISTORY,
        MAX_GATE_LOG_TRUNCATE, MAX_OBSERVATION_SIZE, MAX_GATE_OUTPUTS,
        pruneDirectory } = require('./utils.cjs');

// --- Write/Edit tracking ---

const CODE_EXTENSIONS = {
    '.py': 'ruff check', '.ts': 'eslint', '.tsx': 'eslint',
    '.js': 'eslint', '.jsx': 'eslint', '.go': 'golangci-lint run',
    '.rs': 'cargo clippy', '.rb': 'rubocop', '.java': 'checkstyle', '.sh': 'shellcheck'
};

function trackFileChange(filePath, toolName) {
    let changes = loadState('file_changes.json', []);
    const changeEntry = { path: filePath, tool: toolName, timestamp: new Date().toISOString() };
    const existingIndex = changes.findIndex(c => c.path === filePath);
    if (existingIndex >= 0) {
        changes[existingIndex] = changeEntry;
    } else {
        changes.push(changeEntry);
    }
    if (changes.length > MAX_FILE_CHANGES) changes = changes.slice(-MAX_FILE_CHANGES);
    saveState('file_changes.json', changes);
    return changes;
}

function suggestLint(filePath) {
    const ext = path.extname(filePath).toLowerCase();
    const lintCmd = CODE_EXTENSIONS[ext];
    return lintCmd ? [`Consider running lint: ${lintCmd}`] : [];
}

function handleWriteEdit(parsed) {
    const filePath = parsed.tool_input?.file_path || parsed.tool_input?.path || '';
    const toolName = parsed.tool_name || 'unknown';

    if (parsed.tool_result?.success === false || !filePath) {
        console.log(JSON.stringify({ tracked: false }));
        return;
    }

    const changes = trackFileChange(filePath, toolName);
    const suggestions = suggestLint(filePath);
    logMessage(`${toolName} completed: ${filePath}`);

    console.log(JSON.stringify({
        tracked: true, path: filePath, totalChanges: changes.length,
        suggestions: suggestions.length > 0 ? suggestions : undefined
    }));
}

// --- Bash gate monitoring ---

const GATE_PATTERNS = [
    /\b(ruff|eslint|golangci-lint|clippy|checkstyle|rubocop|clang-tidy|shellcheck|cppcheck)\b/,
    /\b(pytest|vitest|jest|mocha|go\s+test|cargo\s+test|mvn\s+test|rspec|ctest)\b/,
    /\b(tsc|cargo\s+build|cmake\s+--build|mvn\s+compile|go\s+build|make)\b/,
    /\b(gofmt|clang-format|prettier|black|ruff\s+format)\b/,
    /\bnode\s+.*__tests__/
];

function maskLargeOutput(stdout, stateDir) {
    if (!stdout || stdout.length <= MAX_OBSERVATION_SIZE) return null;

    const outputDir = path.join(stateDir, 'gate-output');
    if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const outFile = path.join(outputDir, `gate-output-${timestamp}.txt`);
    fs.writeFileSync(outFile, stdout, 'utf8');
    pruneDirectory(outputDir, MAX_GATE_OUTPUTS, 'gate-output-');

    const lines = stdout.split('\n').length;
    const preview = stdout.substring(0, 200).replace(/\n/g, ' ');
    return { outputRef: outFile, lines, preview };
}

function handleBash(parsed) {
    const command = parsed.tool_input?.command || '';
    const exitCode = parsed.tool_result?.exit_code ?? parsed.tool_result?.exitCode ?? null;
    const duration = parsed.tool_result?.duration_ms ?? null;
    const stdout = parsed.tool_result?.stdout || '';

    // Early exit for non-gate commands
    if (!GATE_PATTERNS.some(p => p.test(command))) return;

    const history = loadState('gate_history.json', { entries: [] });
    const stateDir = path.join(getProjectRoot(), '.claude', 'state');

    const entry = {
        timestamp: new Date().toISOString(),
        command: command.substring(0, MAX_LOGGED_COMMAND_LENGTH),
        exitCode,
        duration,
        passed: exitCode === null ? null : exitCode === 0
    };

    const masked = maskLargeOutput(stdout, stateDir);
    if (masked) {
        entry.outputRef = masked.outputRef;
        entry.outputLines = masked.lines;
        entry.outputPreview = masked.preview;
    }

    history.entries.push(entry);
    if (history.entries.length > MAX_GATE_HISTORY) {
        history.entries = history.entries.slice(-MAX_GATE_HISTORY);
    }
    saveState('gate_history.json', history);

    if (exitCode !== null && exitCode !== 0) {
        logMessage(`Gate failed: ${command.substring(0, MAX_GATE_LOG_TRUNCATE)} (exit ${exitCode})`, 'WARNING');
    }
}

// --- Main dispatch ---

function main() {
    const parsed = parseHookInput();
    const toolName = parsed.tool_name || '';

    if (toolName === 'Write' || toolName === 'Edit') {
        handleWriteEdit(parsed);
    } else if (toolName === 'Bash') {
        handleBash(parsed);
    }
}

main();
