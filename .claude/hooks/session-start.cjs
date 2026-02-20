#!/usr/bin/env node
/**
 * SessionStart Hook - Initialize session context
 *
 * Triggered when a Claude Code session begins.
 * Creates session state file and injects initial context.
 *
 * NOTE: Commands (cs-loop, cs-status, cs-team, cs-ui, cs-init) depend on
 * the `profile` field in .claude/state/session_start.json written by this hook.
 * If you change the profile detection logic, update the commands accordingly.
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { ensureStateDir, saveState, logMessage, GIT_EXEC_OPTIONS, getProjectRoot, MIN_SHELL_FILES, SESSION_ID_SUFFIX_LEN } = require('./utils.cjs');

// Root-level profile detection by marker files (all 9 profiles)
function detectRootProfile(cwd) {
    if (fs.existsSync(path.join(cwd, 'pyproject.toml')) || fs.existsSync(path.join(cwd, 'setup.py')) || fs.existsSync(path.join(cwd, 'requirements.txt'))) {
        return 'python';
    }
    if (fs.existsSync(path.join(cwd, 'tsconfig.json'))) return 'typescript';
    if (fs.existsSync(path.join(cwd, 'go.mod'))) return 'go';
    if (fs.existsSync(path.join(cwd, 'Cargo.toml'))) return 'rust';
    if (fs.existsSync(path.join(cwd, 'pom.xml')) || fs.existsSync(path.join(cwd, 'build.gradle'))) {
        return 'java';
    }
    if (fs.existsSync(path.join(cwd, 'CMakeLists.txt')) || fs.existsSync(path.join(cwd, 'Makefile'))) {
        return 'cpp';
    }
    if (fs.existsSync(path.join(cwd, 'Gemfile'))) return 'ruby';
    return null;
}

// Check a single monorepo subdirectory for profile markers
function detectSubdirProfile(subdirPath) {
    if (!fs.statSync(subdirPath).isDirectory()) return null;
    if (fs.existsSync(path.join(subdirPath, 'tsconfig.json'))) return 'typescript';
    if (fs.existsSync(path.join(subdirPath, 'pyproject.toml'))) return 'python';
    return null;
}

// Search monorepo directories for nested profiles
function detectMonorepoProfile(cwd) {
    const monorepoLocations = ['packages', 'apps', 'src'];
    // Early exit: if none of the monorepo dirs exist, skip scanning entirely
    if (!monorepoLocations.some(dir => fs.existsSync(path.join(cwd, dir)))) return null;
    for (const dir of monorepoLocations) {
        const dirPath = path.join(cwd, dir);
        if (!fs.existsSync(dirPath) || !fs.statSync(dirPath).isDirectory()) continue;

        try {
            for (const subdir of fs.readdirSync(dirPath)) {
                const result = detectSubdirProfile(path.join(dirPath, subdir));
                if (result) return result;
            }
        } catch (e) {
            // Ignore read errors on individual directories
        }
    }
    return null;
}

// Fallback: check package.json for TypeScript dependency
function detectFromPackageJson(cwd) {
    const pkgPath = path.join(cwd, 'package.json');
    if (!fs.existsSync(pkgPath)) return null;

    try {
        const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));
        if (pkg.devDependencies?.typescript || pkg.dependencies?.typescript) {
            return 'typescript';
        }
    } catch (e) {
        // Ignore parse errors
    }
    return 'general';
}

// Detect shell profile by scanning for shell scripts
function detectShellProfile(cwd) {
    try {
        const files = fs.readdirSync(cwd);
        const shellFiles = files.filter(f => f.endsWith('.sh') || f.endsWith('.ps1'));
        if (shellFiles.length >= MIN_SHELL_FILES) return 'shell';
    } catch (e) {
        // Ignore read errors
    }
    return null;
}

// Detect profile from files (supports monorepos)
function detectProfile() {
    const cwd = process.cwd();
    return detectRootProfile(cwd)
        || detectMonorepoProfile(cwd)
        || detectFromPackageJson(cwd)
        || detectShellProfile(cwd)
        || 'general';
}

/**
 * Get git branch name and working tree status.
 * @returns {{gitBranch: string, gitStatus: string}}
 */
function getGitInfo() {
    try {
        const gitBranch = execSync('git rev-parse --abbrev-ref HEAD', GIT_EXEC_OPTIONS).trim();
        const status = execSync('git status --porcelain', GIT_EXEC_OPTIONS).trim();
        return { gitBranch, gitStatus: status ? 'dirty' : 'clean' };
    } catch (e) {
        try {
            execSync('git rev-parse --git-dir', GIT_EXEC_OPTIONS);
            return { gitBranch: 'no-commits', gitStatus: 'unknown' };
        } catch (_) {
            return { gitBranch: 'not-a-repo', gitStatus: 'unknown' };
        }
    }
}

function main() {
    ensureStateDir();
    const { gitBranch, gitStatus } = getGitInfo();
    const sessionId = `session-${Date.now()}-${Math.random().toString(36).slice(2, 2 + SESSION_ID_SUFFIX_LEN)}`;

    const profile = detectProfile();

    const sessionInfo = {
        id: sessionId, timestamp: new Date().toISOString(),
        cwd: process.cwd(), project_root: getProjectRoot(),
        gitBranch, gitStatus, profile,
        platform: process.platform, nodeVersion: process.version
    };

    saveState('session_start.json', sessionInfo);
    logMessage(`SessionStart id=${sessionId} branch=${gitBranch} profile=${profile}`);
    console.log(JSON.stringify({
        continue: true,
        context: { sessionId, profile, gitBranch, gitStatus }
    }));
}

main();
