#!/usr/bin/env node
/**
 * PostToolUse Hook for Bash - Monitor gate results
 *
 * Read-only observer that records exit codes, commands, and durations
 * to gate_history.json for quality gate tracking.
 * Decision: always allow (never blocks).
 */

const { parseHookInput, loadState, saveState, logMessage, MAX_LOGGED_COMMAND_LENGTH, MAX_GATE_HISTORY, MAX_GATE_LOG_TRUNCATE } = require('./utils.cjs');

// Parse hook input
const parsed = parseHookInput();
const command = parsed.tool_input?.command || '';
const exitCode = parsed.tool_result?.exit_code ?? parsed.tool_result?.exitCode ?? null;
const duration = parsed.tool_result?.duration_ms ?? null;

// Only record gate-relevant commands (lint, test, build, format)
const GATE_PATTERNS = [
    /\b(ruff|eslint|golangci-lint|clippy|checkstyle|rubocop|clang-tidy|shellcheck|cppcheck)\b/,
    /\b(pytest|vitest|jest|mocha|go\s+test|cargo\s+test|mvn\s+test|rspec|ctest)\b/,
    /\b(tsc|cargo\s+build|cmake\s+--build|mvn\s+compile|go\s+build|make)\b/,
    /\b(gofmt|clang-format|prettier|black|ruff\s+format)\b/,
    /\bnode\s+.*__tests__/
];

const isGateCommand = GATE_PATTERNS.some(p => p.test(command));

if (isGateCommand) {
    const history = loadState('gate_history.json', { entries: [] });

    history.entries.push({
        timestamp: new Date().toISOString(),
        command: command.substring(0, MAX_LOGGED_COMMAND_LENGTH),
        exitCode,
        duration,
        passed: exitCode === 0
    });

    // Cap history size
    if (history.entries.length > MAX_GATE_HISTORY) {
        history.entries = history.entries.slice(-MAX_GATE_HISTORY);
    }

    saveState('gate_history.json', history);

    if (exitCode !== 0) {
        logMessage(`Gate failed: ${command.substring(0, MAX_GATE_LOG_TRUNCATE)} (exit ${exitCode})`, 'WARNING');
    }
}

// Always allow — read-only observer
console.log(JSON.stringify({ decision: 'allow' }));
