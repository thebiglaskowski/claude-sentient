#!/usr/bin/env node
/**
 * SessionStart Hook - Initialize session context
 *
 * Triggered when a Claude Code session begins.
 * Creates session state file and injects initial context.
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const stateDir = path.join(process.cwd(), '.claude', 'state');
const sessionFile = path.join(stateDir, 'session_start.json');

// Ensure state directory exists
if (!fs.existsSync(stateDir)) {
    fs.mkdirSync(stateDir, { recursive: true });
}

// Get git branch if available
let gitBranch = 'unknown';
try {
    gitBranch = execSync('git rev-parse --abbrev-ref HEAD', { encoding: 'utf8', stdio: ['pipe', 'pipe', 'pipe'] }).trim();
} catch (e) {
    // Not a git repo or git not available
}

// Get git status summary
let gitStatus = 'unknown';
try {
    const status = execSync('git status --porcelain', { encoding: 'utf8', stdio: ['pipe', 'pipe', 'pipe'] }).trim();
    gitStatus = status ? 'dirty' : 'clean';
} catch (e) {
    // Not a git repo
}

// Detect profile from files
function detectProfile() {
    const cwd = process.cwd();
    if (fs.existsSync(path.join(cwd, 'pyproject.toml')) || fs.existsSync(path.join(cwd, 'setup.py'))) {
        return 'python';
    }
    if (fs.existsSync(path.join(cwd, 'tsconfig.json'))) {
        return 'typescript';
    }
    if (fs.existsSync(path.join(cwd, 'go.mod'))) {
        return 'go';
    }
    if (fs.existsSync(path.join(cwd, 'Cargo.toml'))) {
        return 'rust';
    }
    if (fs.existsSync(path.join(cwd, 'package.json'))) {
        return 'javascript';
    }
    return 'general';
}

// Generate session ID
const sessionId = `session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

// Write session start info
const sessionInfo = {
    id: sessionId,
    timestamp: new Date().toISOString(),
    cwd: process.cwd(),
    gitBranch,
    gitStatus,
    profile: detectProfile(),
    platform: process.platform,
    nodeVersion: process.version
};

fs.writeFileSync(sessionFile, JSON.stringify(sessionInfo, null, 2));

// Also append to session log
const logFile = path.join(process.cwd(), '.claude', 'session.log');
const logEntry = `[cs] ${sessionInfo.timestamp.slice(0, 19)} SessionStart id=${sessionId} branch=${gitBranch} profile=${sessionInfo.profile}\n`;
fs.appendFileSync(logFile, logEntry);

// Output for hook system (optional context injection)
const output = {
    continue: true,
    context: {
        sessionId,
        profile: sessionInfo.profile,
        gitBranch,
        gitStatus
    }
};

console.log(JSON.stringify(output));
