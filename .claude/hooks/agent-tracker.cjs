#!/usr/bin/env node
/**
 * SubagentStart Hook - Track subagent spawning
 *
 * Triggered when a subagent (Task tool) is started.
 * Tracks agent metadata for synthesis and cost allocation.
 */

const fs = require('fs');
const path = require('path');
const { parseHookInput, loadState, saveState, logMessage, MAX_ACTIVE_AGENTS } = require('./utils.cjs');

// Parse input from hook
const parsed = parseHookInput();
const agentId = parsed.agent_id || parsed.task_id || `agent-${Date.now()}`;
const agentType = parsed.tool_input?.subagent_type || 'general-purpose';
const description = parsed.tool_input?.description || '';
const model = parsed.tool_input?.model || 'sonnet';
const runInBackground = parsed.tool_input?.run_in_background || false;

// Load active agents
const activeAgents = loadState('active_agents.json', {});

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

// Detect if agent matches a known agent definition from agents/*.yaml
let agentRole = null;
let rulesLoaded = [];
let expertise = [];

try {
    const agentsDir = path.resolve(__dirname, '..', '..', 'agents');
    if (!fs.existsSync(agentsDir)) throw new Error('no agents dir');

    const agentFiles = fs.readdirSync(agentsDir).filter(f => f.endsWith('.yaml'));
    const searchText = (description + ' ' + agentType).toLowerCase();

    for (const file of agentFiles) {
        const roleName = file.replace('.yaml', '');
        if (!searchText.includes(roleName)) continue;

        agentRole = roleName;
        const content = fs.readFileSync(path.join(agentsDir, file), 'utf8');
        let currentSection = null;

        for (const line of content.split('\n')) {
            if (/^[a-z]/.test(line)) {
                currentSection = line.startsWith('rules_to_load:') ? 'rules'
                    : line.startsWith('expertise:') ? 'expertise' : null;
                continue;
            }
            const match = line.match(/^\s+-\s+(.+)/);
            if (!match) continue;
            if (currentSection === 'rules') rulesLoaded.push(match[1].trim());
            if (currentSection === 'expertise') expertise.push(match[1].trim());
        }
        break;
    }
} catch {
    // Agent definition detection is best-effort
}

// Add agent role info to tracked data
if (agentRole) {
    activeAgents[agentId].agentRole = agentRole;
    activeAgents[agentId].rulesLoaded = rulesLoaded;
    activeAgents[agentId].expertise = expertise;
}

// Prune oldest agents if exceeding cap
const agentKeys = Object.keys(activeAgents);
if (agentKeys.length > MAX_ACTIVE_AGENTS) {
    const sorted = agentKeys.sort((a, b) => {
        const ta = activeAgents[a].startTime || '';
        const tb = activeAgents[b].startTime || '';
        return ta.localeCompare(tb);
    });
    for (let i = 0; i < sorted.length - MAX_ACTIVE_AGENTS; i++) {
        delete activeAgents[sorted[i]];
    }
}

saveState('active_agents.json', activeAgents);

// Log the agent start
logMessage(`SubagentStart id=${agentId} type=${agentType} model=${model}${agentRole ? ` role=${agentRole}` : ''}`);

// Output
const output = {
    tracked: true,
    agentId,
    agentType,
    model,
    activeCount: Object.keys(activeAgents).length
};

if (agentRole) {
    output.agentRole = agentRole;
    output.rulesLoaded = rulesLoaded;
    output.expertise = expertise;
}

console.log(JSON.stringify(output));
