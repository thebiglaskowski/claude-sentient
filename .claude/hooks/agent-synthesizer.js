#!/usr/bin/env node
/**
 * SubagentStop Hook - Synthesize subagent results
 *
 * Triggered when a subagent completes.
 * Synthesizes results and updates cost tracking.
 */

const fs = require('fs');
const path = require('path');

const stateDir = path.join(process.cwd(), '.claude', 'state');
const agentsFile = path.join(stateDir, 'active_agents.json');
const historyFile = path.join(stateDir, 'agent_history.json');

// Ensure state directory exists
if (!fs.existsSync(stateDir)) {
    fs.mkdirSync(stateDir, { recursive: true });
}

// Parse input from hook
let agentId = '';
let success = true;
let resultSummary = '';

try {
    const input = process.env.HOOK_INPUT;
    if (input) {
        const parsed = JSON.parse(input);
        agentId = parsed.agent_id || parsed.task_id || '';
        success = parsed.success !== false;
        resultSummary = parsed.result_summary || parsed.output?.substring(0, 500) || '';
    }
} catch (e) {
    // Try reading from stdin
    try {
        const stdin = fs.readFileSync(0, 'utf8');
        const parsed = JSON.parse(stdin);
        agentId = parsed.agent_id || parsed.task_id || '';
        success = parsed.success !== false;
        resultSummary = parsed.result_summary || parsed.output?.substring(0, 500) || '';
    } catch (e2) {
        // No input
    }
}

// Load active agents
let activeAgents = {};
if (fs.existsSync(agentsFile)) {
    try {
        activeAgents = JSON.parse(fs.readFileSync(agentsFile, 'utf8'));
    } catch (e) {
        activeAgents = {};
    }
}

// Get agent info
const agentInfo = activeAgents[agentId] || {
    id: agentId,
    type: 'unknown',
    startTime: new Date().toISOString()
};

// Calculate duration
const startTime = new Date(agentInfo.startTime);
const endTime = new Date();
const durationMs = endTime - startTime;
const durationSec = Math.round(durationMs / 1000);

// Create history entry
const historyEntry = {
    ...agentInfo,
    endTime: endTime.toISOString(),
    durationSeconds: durationSec,
    success,
    resultSummary: resultSummary.substring(0, 500)
};

// Load and update history
let history = [];
if (fs.existsSync(historyFile)) {
    try {
        history = JSON.parse(fs.readFileSync(historyFile, 'utf8'));
    } catch (e) {
        history = [];
    }
}
history.push(historyEntry);

// Keep only last 50 entries
if (history.length > 50) {
    history = history.slice(-50);
}
fs.writeFileSync(historyFile, JSON.stringify(history, null, 2));

// Remove from active agents
if (activeAgents[agentId]) {
    delete activeAgents[agentId];
    fs.writeFileSync(agentsFile, JSON.stringify(activeAgents, null, 2));
}

// Log the agent completion
const logFile = path.join(process.cwd(), '.claude', 'session.log');
const status = success ? 'completed' : 'failed';
const logEntry = `[cs] ${endTime.toISOString().slice(0, 19)} SubagentStop id=${agentId} status=${status} duration=${durationSec}s\n`;
try {
    fs.appendFileSync(logFile, logEntry);
} catch (e) {
    // Ignore
}

// Output synthesis
const output = {
    agentId,
    type: agentInfo.type,
    success,
    durationSeconds: durationSec,
    remainingAgents: Object.keys(activeAgents).length
};

console.log(JSON.stringify(output));
