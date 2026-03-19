#!/usr/bin/env node
/**
 * PreToolUse Hook - Skill usage tracker
 *
 * Triggered when the Skill tool is invoked.
 * Logs skill name + timestamp to .claude/state/skill-usage.json
 * for undertriggering detection via /cs-assess.
 */

const { parseHookInput, appendCapped, logMessage, MAX_SKILL_USAGE } = require('./utils.cjs');

function main() {
    let skillName = '';
    try {
        const parsed = parseHookInput();
        const toolInput = parsed.tool_input || {};
        skillName = toolInput.skill || '';
    } catch (e) {
        // No input available — allow through
    }

    if (!skillName) {
        console.log(JSON.stringify({ continue: true }));
        return;
    }

    appendCapped('skill-usage.json', {
        skill: skillName,
        timestamp: new Date().toISOString()
    }, MAX_SKILL_USAGE);

    logMessage(`Skill invoked: ${skillName}`);
    console.log(JSON.stringify({ continue: true }));
}

main();
