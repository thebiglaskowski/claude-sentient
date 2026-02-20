#!/usr/bin/env node
/**
 * UserPromptSubmit Hook - Enhanced context injection
 *
 * Triggered when user submits a prompt.
 * Injects relevant context based on prompt content.
 */

const { parseHookInput, appendCapped, logMessage, MAX_PROMPT_HISTORY } = require('./utils.cjs');

// Topic keyword maps for rule loading (module-level constant)
const TOPIC_KEYWORDS = {
    auth: ['auth', 'login', 'jwt', 'oauth', 'session', 'password', 'token', 'credential'],
    test: ['test', 'coverage', 'mock', 'spec', 'unittest', 'pytest', 'vitest', 'jest'],
    api: ['api', 'endpoint', 'rest', 'graphql', 'route', 'http', 'request', 'response'],
    database: ['database', 'query', 'sql', 'orm', 'migration', 'schema', 'table', 'model'],
    performance: ['performance', 'cache', 'optimize', 'speed', 'slow', 'fast', 'memory', 'latency'],
    ui: ['ui', 'component', 'css', 'style', 'layout', 'design', 'theme', 'color', 'responsive'],
    security: ['security', 'vulnerability', 'xss', 'injection', 'sanitize', 'encrypt', 'hash', 'secret'],
    codeQuality: ['lint', 'format', 'refactor', 'clean', 'organize', 'style', 'convention', 'typing'],
    errorHandling: ['error', 'bug', 'fix', 'exception', 'catch', 'throw', 'handle', 'crash'],
    documentation: ['doc', 'readme', 'comment', 'docstring', 'explain', 'document']
};

// File patterns for predictive context injection (module-level constant)
const FILE_PATTERNS = {
    auth: ['**/auth*', '**/middleware*', '**/session*', '**/login*', '**/passport*'],
    test: ['**/test*', '**/__tests__*', '**/*.test.*', '**/*.spec.*'],
    api: ['**/api*', '**/routes*', '**/controllers*', '**/endpoints*', '**/handlers*'],
    database: ['**/models*', '**/migrations*', '**/schema*', '**/queries*', '**/db*'],
    performance: ['**/cache*', '**/workers*', '**/queue*', '**/jobs*'],
    ui: ['**/components*', '**/views*', '**/pages*', '**/layouts*', '**/styles*'],
    security: ['**/auth*', '**/middleware*', '**/validators*', '**/sanitize*'],
    codeQuality: ['**/lint*', '**/config*', '**/.eslint*', '**/.prettier*'],
    errorHandling: ['**/errors*', '**/exceptions*', '**/middleware*', '**/handlers*'],
    documentation: ['**/docs*', '**/*.md', '**/README*']
};

/**
 * Detect topics from prompt text by matching against keyword maps.
 * @param {string} promptLower - Lowercased prompt text
 * @returns {string[]} Array of detected topic names
 */
function detectTopics(promptLower) {
    const topics = [];
    for (const [topic, words] of Object.entries(TOPIC_KEYWORDS)) {
        if (words.some(word => promptLower.includes(word))) {
            topics.push(topic);
        }
    }
    return topics;
}

/**
 * Build deduplicated file predictions from detected topics.
 * @param {string[]} topics - Detected topic names
 * @returns {string[]} Unique glob patterns for relevant files
 */
function buildFilePredictions(topics) {
    const predictions = [];
    for (const topic of topics) {
        if (FILE_PATTERNS[topic]) {
            predictions.push(...FILE_PATTERNS[topic]);
        }
    }
    return [...new Set(predictions)];
}

function main() {
    logMessage('Prompt received');

    let promptText = '';
    try {
        const parsed = parseHookInput();
        promptText = parsed.prompt || parsed.content || '';
    } catch (e) {
        // No input available
    }

    const detectedTopics = detectTopics(promptText.toLowerCase());
    const filePredictions = buildFilePredictions(detectedTopics);

    // Only persist prompt metadata when there is actual content
    if (promptText.length > 0) {
        appendCapped('prompts.json', {
            timestamp: new Date().toISOString(),
            topics: detectedTopics,
            length: promptText.length
        }, MAX_PROMPT_HISTORY);
    }

    console.log(JSON.stringify({
        continue: true,
        detectedTopics,
        filePredictions
    }));
}

main();
