#!/usr/bin/env node
/**
 * PreCompact Hook - Backup state before context compaction
 *
 * Triggered before Claude compacts context.
 * Creates a backup of important state to preserve across compaction.
 */

const fs = require('fs');
const path = require('path');
const { loadJsonFile, saveJsonFile, logMessage, getStateFilePath, getProjectRoot, MAX_BACKUPS, pruneDirectory, MAX_COMPACT_FILE_HISTORY, MAX_COMPACT_DECISION_HISTORY } = require('./utils.cjs');

// State files to include in pre-compaction backup
const FILES_TO_BACKUP = [
    'session_start.json',
    'file_changes.json',
    'active_agents.json',
    'prompts.json',
    'current_task.json'
];

/**
 * Load state files into a backup bundle.
 * @param {string} stateDir - Path to state directory
 * @returns {{backedUp: string[], backupBundle: Object}} Files backed up and their data
 */
function collectStateFiles(stateDir) {
    const backedUp = [];
    const backupBundle = {};
    for (const file of FILES_TO_BACKUP) {
        const sourcePath = path.join(stateDir, file);
        const data = fs.existsSync(sourcePath) ? loadJsonFile(sourcePath, null) : null;
        if (data !== null) {
            backupBundle[file] = data;
            backedUp.push(file);
        }
    }
    return { backedUp, backupBundle };
}

/**
 * Write backup bundle to disk and prune old backups.
 * @param {string} backupDir - Path to backup directory
 * @param {string} timestamp - Formatted timestamp for filename
 * @param {string[]} backedUp - List of backed-up filenames
 * @param {Object} backupBundle - Bundle of state file data
 */
function writeBackupBundle(backupDir, timestamp, backedUp, backupBundle) {
    if (backedUp.length === 0) return;
    const backupFile = path.join(backupDir, `pre-compact-${timestamp}.json`);
    saveJsonFile(backupFile, { timestamp: new Date().toISOString(), files: backupBundle });
    pruneDirectory(backupDir, MAX_BACKUPS, 'pre-compact-');
}

/**
 * Extract active task from backup bundle.
 * @param {Object} backupBundle - Bundle of state file data
 * @returns {Object|null} Active task info or null
 */
function extractActiveTask(backupBundle) {
    const currentTask = backupBundle['current_task.json'];
    if (currentTask && currentTask.taskId) return currentTask;
    const sessionState = backupBundle['session_start.json'];
    return sessionState ? (sessionState.currentTask || sessionState.task || null) : null;
}

/**
 * Extract recent file changes from backup bundle.
 * @param {Object} backupBundle - Bundle of state file data
 * @returns {Array} Recent file change entries
 */
function extractFileChanges(backupBundle) {
    const fileChanges = backupBundle['file_changes.json'];
    if (Array.isArray(fileChanges)) {
        return fileChanges.slice(-MAX_COMPACT_FILE_HISTORY).map(f => ({
            file: f.file || f.path, action: f.action || f.type || 'modified'
        }));
    }
    if (fileChanges && typeof fileChanges === 'object') {
        return Object.keys(fileChanges).slice(-MAX_COMPACT_FILE_HISTORY).map(f => ({
            file: f, action: 'modified'
        }));
    }
    return [];
}

/**
 * Extract recent prompt decisions from backup bundle.
 * @param {Object} backupBundle - Bundle of state file data
 * @returns {Array} Recent decision entries
 */
function extractRecentDecisions(backupBundle) {
    const prompts = backupBundle['prompts.json'];
    if (!Array.isArray(prompts)) return [];
    return prompts.slice(-MAX_COMPACT_DECISION_HISTORY).map(p => ({
        topics: p.topics || [], timestamp: p.timestamp
    }));
}

/**
 * Build anchored iterative session summary for artifact trail preservation.
 * Structured format ensures the most important context survives compaction:
 * - sessionIntent: what task is being worked on
 * - filesModified: complete list of changed files this session
 * - decisionsMade: unique topic areas addressed
 * - currentState: profile + active task status
 * - nextSteps: what remains to be done
 * @param {Object} backupBundle - Bundle of state file data
 * @returns {Object} Structured session summary
 */
function buildSessionSummary(backupBundle) {
    const currentTask = backupBundle['current_task.json'];
    const session = backupBundle['session_start.json'];
    const fileChanges = backupBundle['file_changes.json'];
    const prompts = backupBundle['prompts.json'];

    // Session intent: task subject > session task > profile name
    const sessionIntent =
        (currentTask && (currentTask.subject || currentTask.description)) ||
        (session && (session.task || session.intent)) ||
        (session && session.profile ? `${session.profile} project session` : null) ||
        'Session in progress';

    // All unique files modified this session (not just recent MAX_COMPACT_FILE_HISTORY)
    let filesModified = [];
    if (Array.isArray(fileChanges)) {
        const seen = new Set();
        for (const f of fileChanges) {
            const name = f.file || f.path;
            if (name && !seen.has(name)) { seen.add(name); filesModified.push(name); }
        }
    } else if (fileChanges && typeof fileChanges === 'object') {
        filesModified = Object.keys(fileChanges);
    }

    // Unique decision topics from prompt history
    const topicSet = new Set();
    if (Array.isArray(prompts)) {
        for (const p of prompts) {
            if (Array.isArray(p.topics)) p.topics.forEach(t => topicSet.add(t));
        }
    }
    const decisionsMade = [...topicSet];

    // Current state: profile + task status
    const profile = session && session.profile ? session.profile : null;
    const taskStatus = currentTask && currentTask.taskId
        ? `Task ${currentTask.taskId}: ${currentTask.subject || 'in progress'}`
        : null;
    const currentState = [profile, taskStatus].filter(Boolean).join(' | ') || 'No active task';

    // Next steps: derive from active task or unresolved items
    const nextSteps = [];
    if (currentTask && currentTask.taskId) {
        nextSteps.push(`Complete task: ${currentTask.subject || currentTask.taskId}`);
    }
    if (currentTask && currentTask.startedAt) {
        nextSteps.push('Run VERIFY phase: lint, test, build');
    }

    return { sessionIntent, filesModified, decisionsMade, currentState, nextSteps };
}

function main() {
    const stateDir = path.join(getProjectRoot(), '.claude', 'state');
    const backupDir = path.join(stateDir, 'backups');
    if (!fs.existsSync(backupDir)) fs.mkdirSync(backupDir, { recursive: true });

    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const { backedUp, backupBundle } = collectStateFiles(stateDir);
    writeBackupBundle(backupDir, timestamp, backedUp, backupBundle);

    const summary = {
        timestamp: new Date().toISOString(),
        sessionSummary: buildSessionSummary(backupBundle),
        activeTask: extractActiveTask(backupBundle),
        recentDecisions: extractRecentDecisions(backupBundle),
        fileChanges: extractFileChanges(backupBundle),
        unresolved: []
    };
    saveJsonFile(path.join(stateDir, 'compact-context.json'), summary);

    logMessage(`PreCompact backup created: ${backedUp.length} files`);
    console.log(JSON.stringify({ backedUp, timestamp, backupCount: backedUp.length }));
}

main();
