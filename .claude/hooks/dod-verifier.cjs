#!/usr/bin/env node
/**
 * Stop Hook - Definition of Done verification
 *
 * Triggered when Claude stops (task completion).
 * Verifies that quality gates passed and DoD is met.
 */

const path = require('path');
const { execSync } = require('child_process');
const { loadJsonFile, saveJsonFile, logMessage, getStateFilePath, GIT_EXEC_OPTIONS } = require('./utils.cjs');

// Extension-to-language mapping for change categorization
const EXT_TO_LANG = {
    '.py': 'python', '.ts': 'typescript', '.tsx': 'typescript',
    '.js': 'javascript', '.jsx': 'javascript', '.go': 'go'
};

/**
 * Categorize file changes by language.
 * @param {Array} fileChanges - Array of change entries with .path
 * @returns {Object} Map of language to array of file paths
 */
function categorizeChanges(fileChanges) {
    const byType = { python: [], typescript: [], javascript: [], go: [], other: [] };
    for (const change of fileChanges) {
        const ext = path.extname(change.path || '').toLowerCase();
        const lang = EXT_TO_LANG[ext] || 'other';
        byType[lang].push(change.path);
    }
    return byType;
}

/**
 * Get git working tree state.
 * @returns {{gitClean: boolean, uncommittedChanges: number}}
 */
function getGitState() {
    try {
        const status = execSync('git status --porcelain', GIT_EXEC_OPTIONS).trim();
        return { gitClean: !status, uncommittedChanges: status ? status.split('\n').length : 0 };
    } catch (e) {
        return { gitClean: false, uncommittedChanges: 0 };
    }
}

/**
 * Build recommendations based on session state.
 * @param {boolean} gitClean - Whether git working tree is clean
 * @param {Array} fileChanges - Array of tracked file changes
 * @param {Object} changesByType - Changes categorized by language
 * @returns {string[]} Array of recommendation strings
 */
function buildRecommendations(gitClean, fileChanges, changesByType) {
    const recs = [];
    if (!gitClean && fileChanges.length > 0) recs.push('Consider committing changes before ending session');
    if (changesByType.python.length > 0) recs.push('Run ruff check and pytest before finalizing');
    if (changesByType.typescript.length > 0 || changesByType.javascript.length > 0) {
        recs.push('Run eslint and tests before finalizing');
    }
    return recs;
}

function main() {
    logMessage('DoD verification started');

    const fileChanges = loadJsonFile(getStateFilePath('file_changes.json'), []);
    const changesByType = categorizeChanges(fileChanges);
    const { gitClean, uncommittedChanges } = getGitState();

    const verification = {
        timestamp: new Date().toISOString(),
        filesModified: fileChanges.length,
        changesByType: Object.fromEntries(
            Object.entries(changesByType).map(([k, v]) => [k, v.length])
        ),
        git: { clean: gitClean, uncommittedChanges },
        recommendations: buildRecommendations(gitClean, fileChanges, changesByType)
    };

    saveJsonFile(getStateFilePath('last_verification.json'), verification);
    console.log(JSON.stringify(verification));

    if (!gitClean && fileChanges.length > 0) process.exit(2);
}

main();
