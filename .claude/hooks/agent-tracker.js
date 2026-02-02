#!/usr/bin/env node
/**
 * SubagentStart Hook - Track subagent spawning
 *
 * Triggered when a subagent (Task tool) is started.
 * Tracks agent metadata for synthesis and cost allocation.
 */

const fs = require('fs');
const path = require('path');

const stateDir = path.join(process.cwd(), '.claude', 'state');
const agentsFile = path.join(stateDir, 'active_agents.json');

// Ensure state directory exists
if (!fs.existsSync(stateDir)) {
    fs.mkdirSync(stateDir, { recursive: true });
}

// Parse input from hook
let agentId = '';
let agentType = '';
let description = '';
let model = '';
let runInBackground = false;

try {
    const input = process.env.HOOK_INPUT;
    if (input) {
        const parsed = JSON.parse(input);
        agentId = parsed.agent_id || parsed.task_id || `agent-${Date.now()}`;
        agentType = parsed.tool_input?.subagent_type || 'general-purpose';
        description = parsed.tool_input?.description || '';
        model = parsed.tool_input?.model || 'sonnet';
        runInBackground = parsed.tool_input?.run_in_background || false;
    }
} catch (e) {
    // Try reading from stdin
    try {
        const stdin = fs.readFileSync(0, 'utf8');
        const parsed = JSON.parse(stdin);
        agentId = parsed.agent_id || parsed.task_id || `agent-${Date.now()}`;
        agentType = parsed.tool_input?.subagent_type || 'general-purpose';
        description = parsed.tool_input?.description || '';
        model = parsed.tool_input?.model || 'sonnet';
        runInBackground = parsed.tool_input?.run_in_background || false;
    } catch (e2) {
        agentId = `agent-${Date.now()}`;
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

// Track this agent
activeAgents[agentId] = {
    id: agentId,
    type: agentType,
    description,
    model,
    runInBackground,
    startTime: new Date().toISOString(),
    status: 'running'
};

fs.writeFileSync(agentsFile, JSON.stringify(activeAgents, null, 2));

// Log the agent start
const logFile = path.join(process.cwd(), '.claude', 'session.log');
const logEntry = `[cs] ${new Date().toISOString().slice(0, 19)} SubagentStart id=${agentId} type=${agentType} model=${model}\n`;
try {
    fs.appendFileSync(logFile, logEntry);
} catch (e) {
    // Ignore
}

// Output
const output = {
    tracked: true,
    agentId,
    agentType,
    model,
    activeCount: Object.keys(activeAgents).length
};

console.log(JSON.stringify(output));
