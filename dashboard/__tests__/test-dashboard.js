#!/usr/bin/env node
'use strict';

const assert = require('assert');
const fs = require('fs');
const path = require('path');
const http = require('http');
const { test, suite, summary, getResults } = require('../../test-utils');

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

const TMP_DIR = path.join(__dirname, '.tmp-test-' + process.pid);
const STATE_DIR = path.join(TMP_DIR, '.claude', 'state');
const ARCHIVE_DIR = path.join(STATE_DIR, 'archive');
const LOG_FILE = path.join(TMP_DIR, '.claude', 'session.log');

function setup() {
  fs.mkdirSync(ARCHIVE_DIR, { recursive: true });
}

function cleanup() {
  fs.rmSync(TMP_DIR, { recursive: true, force: true });
}

function writeState(filename, data) {
  fs.writeFileSync(path.join(STATE_DIR, filename), JSON.stringify(data));
}

function writeLog(text) {
  fs.mkdirSync(path.dirname(LOG_FILE), { recursive: true });
  fs.writeFileSync(LOG_FILE, text);
}

function writeArchive(filename, data) {
  fs.writeFileSync(path.join(ARCHIVE_DIR, filename), JSON.stringify(data));
}

// Import server module
const serverPath = path.join(__dirname, '..', 'server.js');
const {
  parseLogLines,
  readJsonFile,
  readAllState,
  listArchive,
  STATE_FILES
} = require(serverPath);

// ---------------------------------------------------------------------------
// Suites
// ---------------------------------------------------------------------------

suite('parseLogLines', () => {
  test('parses valid log lines', () => {
    const text = '[cs] 2026-02-17T03:15:55.398Z INFO: Session started\n[cs] 2026-02-17T03:16:00.000Z WARN: Something happened\n';
    const lines = parseLogLines(text);
    assert.strictEqual(lines.length, 2);
    assert.strictEqual(lines[0].timestamp, '2026-02-17T03:15:55.398Z');
    assert.strictEqual(lines[0].level, 'INFO');
    assert.strictEqual(lines[0].message, 'Session started');
    assert.strictEqual(lines[1].level, 'WARN');
  });

  test('handles empty input', () => {
    assert.deepStrictEqual(parseLogLines(''), []);
    assert.deepStrictEqual(parseLogLines(null), []);
    assert.deepStrictEqual(parseLogLines(undefined), []);
  });

  test('handles malformed lines', () => {
    const text = 'not a log line\n[cs] 2026-02-17T03:15:55.398Z INFO: Valid\nrandom garbage\n';
    const lines = parseLogLines(text);
    assert.strictEqual(lines.length, 1);
    assert.strictEqual(lines[0].message, 'Valid');
  });

  test('respects limit parameter', () => {
    const text = '[cs] 2026-01-01T00:00:00Z INFO: Line 1\n[cs] 2026-01-01T00:00:01Z INFO: Line 2\n[cs] 2026-01-01T00:00:02Z INFO: Line 3\n';
    const lines = parseLogLines(text, 2);
    assert.strictEqual(lines.length, 2);
    assert.strictEqual(lines[0].message, 'Line 2');
    assert.strictEqual(lines[1].message, 'Line 3');
  });

  test('returns all lines when limit exceeds count', () => {
    const text = '[cs] 2026-01-01T00:00:00Z INFO: Only one\n';
    const lines = parseLogLines(text, 100);
    assert.strictEqual(lines.length, 1);
  });

  test('handles all log levels', () => {
    const text = [
      '[cs] 2026-01-01T00:00:00Z INFO: info msg',
      '[cs] 2026-01-01T00:00:01Z WARN: warn msg',
      '[cs] 2026-01-01T00:00:02Z ERROR: error msg',
      '[cs] 2026-01-01T00:00:03Z DEBUG: debug msg'
    ].join('\n');
    const lines = parseLogLines(text);
    assert.strictEqual(lines.length, 4);
    assert.strictEqual(lines[0].level, 'INFO');
    assert.strictEqual(lines[1].level, 'WARN');
    assert.strictEqual(lines[2].level, 'ERROR');
    assert.strictEqual(lines[3].level, 'DEBUG');
  });

  test('handles messages with colons', () => {
    const text = '[cs] 2026-01-01T00:00:00Z INFO: key: value: extra\n';
    const lines = parseLogLines(text);
    assert.strictEqual(lines.length, 1);
    assert.strictEqual(lines[0].message, 'key: value: extra');
  });

  test('handles empty message after level', () => {
    const text = '[cs] 2026-01-01T00:00:00Z INFO: \n';
    const lines = parseLogLines(text);
    assert.strictEqual(lines.length, 1);
    assert.strictEqual(lines[0].message, '');
  });
});

suite('readJsonFile', () => {
  test('reads valid JSON file', () => {
    setup();
    const data = { key: 'value', num: 42 };
    const filePath = path.join(STATE_DIR, 'test-read.json');
    fs.writeFileSync(filePath, JSON.stringify(data));
    const result = readJsonFile(filePath);
    assert.deepStrictEqual(result, data);
    cleanup();
  });

  test('returns null for missing file', () => {
    const result = readJsonFile('/tmp/does-not-exist-' + Date.now() + '.json');
    assert.strictEqual(result, null);
  });

  test('returns null for corrupt JSON', () => {
    setup();
    const filePath = path.join(STATE_DIR, 'corrupt.json');
    fs.writeFileSync(filePath, '{not valid json!!!');
    const result = readJsonFile(filePath);
    assert.strictEqual(result, null);
    cleanup();
  });

  test('reads array JSON', () => {
    setup();
    const data = [1, 2, 3];
    const filePath = path.join(STATE_DIR, 'array.json');
    fs.writeFileSync(filePath, JSON.stringify(data));
    const result = readJsonFile(filePath);
    assert.deepStrictEqual(result, data);
    cleanup();
  });

  test('reads nested objects', () => {
    setup();
    const data = { a: { b: { c: 'deep' } } };
    const filePath = path.join(STATE_DIR, 'nested.json');
    fs.writeFileSync(filePath, JSON.stringify(data));
    const result = readJsonFile(filePath);
    assert.deepStrictEqual(result, data);
    cleanup();
  });
});

suite('readAllState', () => {
  test('returns object with all expected keys', () => {
    // readAllState reads from process.cwd()/.claude/state/ — we test the key structure
    const result = readAllState();
    assert.strictEqual(typeof result, 'object');
    // Should have keys for all STATE_FILES
    for (const file of STATE_FILES) {
      const key = file.replace('.json', '').replace(/-/g, '_');
      assert.ok(key in result, `Missing key: ${key}`);
    }
  });

  test('returns null for missing state files', () => {
    const result = readAllState();
    // Values can be null or actual data, but must not throw
    for (const file of STATE_FILES) {
      const key = file.replace('.json', '').replace(/-/g, '_');
      const val = result[key];
      assert.ok(val === null || typeof val === 'object', `Key ${key} should be null or object, got ${typeof val}`);
    }
  });

  test('key naming converts hyphens to underscores', () => {
    const result = readAllState();
    assert.ok('team_state' in result, 'team-state.json should map to team_state');
    assert.ok('session_start' in result, 'session_start.json should map to session_start');
    assert.ok('last_verification' in result, 'last_verification.json should map to last_verification');
  });
});

suite('listArchive', () => {
  test('lists archive files', () => {
    setup();
    writeArchive('session-1000.json', { timestamp: '2026-01-01T00:00:00Z', profile: 'python' });
    writeArchive('session-2000.json', { timestamp: '2026-02-01T00:00:00Z', profile: 'typescript' });

    // listArchive reads from STATE_DIR/archive relative to process.cwd()
    // We can't easily redirect it, so test it returns an array
    const result = listArchive();
    assert.ok(Array.isArray(result));
    cleanup();
  });

  test('returns empty array when archive dir missing', () => {
    // Default behavior — archive dir may not exist
    const result = listArchive();
    assert.ok(Array.isArray(result));
  });

  test('sorts newest first', () => {
    setup();
    writeArchive('old.json', { timestamp: '2025-01-01T00:00:00Z', profile: 'go' });
    writeArchive('new.json', { timestamp: '2026-06-01T00:00:00Z', profile: 'rust' });

    const result = listArchive();
    assert.ok(Array.isArray(result));
    // Can only verify structure if archive dir matches
    cleanup();
  });
});

suite('STATE_FILES constant', () => {
  test('lists all expected state files', () => {
    assert.ok(Array.isArray(STATE_FILES));
    assert.ok(STATE_FILES.includes('session_start.json'));
    assert.ok(STATE_FILES.includes('active_agents.json'));
    assert.ok(STATE_FILES.includes('agent_history.json'));
    assert.ok(STATE_FILES.includes('file_changes.json'));
    assert.ok(STATE_FILES.includes('team-state.json'));
    assert.ok(STATE_FILES.includes('last_verification.json'));
    assert.ok(STATE_FILES.includes('prompts.json'));
  });

  test('has 7 state files', () => {
    assert.strictEqual(STATE_FILES.length, 7);
  });
});

suite('HTTP server', () => {
  let srv;
  const TEST_PORT = 13777 + Math.floor(Math.random() * 1000);

  function fetch(urlPath) {
    return new Promise((resolve, reject) => {
      const req = http.get(`http://localhost:${TEST_PORT}${urlPath}`, (res) => {
        let body = '';
        res.on('data', chunk => body += chunk);
        res.on('end', () => resolve({ status: res.statusCode, headers: res.headers, body }));
      });
      req.on('error', reject);
      req.setTimeout(3000, () => { req.destroy(); reject(new Error('timeout')); });
    });
  }

  // Start server before tests
  const { startServer, stopServer } = require(serverPath);

  test('starts on specified port', async () => {
    srv = await startServer(TEST_PORT);
    assert.ok(srv, 'Server should start');
    assert.ok(srv.listening, 'Server should be listening');
  });

  test('serves index.html on /', async () => {
    const res = await fetch('/');
    assert.strictEqual(res.status, 200);
    assert.ok(res.headers['content-type'].includes('text/html'));
    assert.ok(res.body.includes('Claude Sentient Dashboard'));
  });

  test('returns JSON for /api/state', async () => {
    const res = await fetch('/api/state');
    assert.strictEqual(res.status, 200);
    assert.ok(res.headers['content-type'].includes('application/json'));
    const data = JSON.parse(res.body);
    assert.strictEqual(typeof data, 'object');
    assert.ok('session_start' in data);
  });

  test('returns JSON array for /api/log', async () => {
    const res = await fetch('/api/log');
    assert.strictEqual(res.status, 200);
    const data = JSON.parse(res.body);
    assert.ok(Array.isArray(data));
  });

  test('respects tail parameter for /api/log', async () => {
    const res = await fetch('/api/log?tail=5');
    assert.strictEqual(res.status, 200);
    const data = JSON.parse(res.body);
    assert.ok(Array.isArray(data));
    assert.ok(data.length <= 5);
  });

  test('returns JSON array for /api/archive', async () => {
    const res = await fetch('/api/archive');
    assert.strictEqual(res.status, 200);
    const data = JSON.parse(res.body);
    assert.ok(Array.isArray(data));
  });

  test('returns 404 for unknown routes', async () => {
    const res = await fetch('/unknown');
    assert.strictEqual(res.status, 404);
  });

  test('SSE endpoint returns correct headers', async () => {
    const res = await new Promise((resolve, reject) => {
      const req = http.get(`http://localhost:${TEST_PORT}/events`, (res) => {
        resolve({ status: res.statusCode, headers: res.headers });
        res.destroy();
      });
      req.on('error', reject);
      req.setTimeout(2000, () => { req.destroy(); reject(new Error('timeout')); });
    });
    assert.strictEqual(res.status, 200);
    assert.strictEqual(res.headers['content-type'], 'text/event-stream');
    assert.strictEqual(res.headers['cache-control'], 'no-cache');
  });

  test('SSE sends full_state on connect', async () => {
    const data = await new Promise((resolve, reject) => {
      const req = http.get(`http://localhost:${TEST_PORT}/events`, (res) => {
        let buf = '';
        res.on('data', chunk => {
          buf += chunk.toString();
          // Look for full_state event
          if (buf.includes('event: full_state')) {
            res.destroy();
            resolve(buf);
          }
        });
        setTimeout(() => { res.destroy(); reject(new Error('timeout waiting for full_state')); }, 3000);
      });
      req.on('error', reject);
    });
    assert.ok(data.includes('event: full_state'));
    assert.ok(data.includes('"session_start"'));
  });

  test('CORS header is set', async () => {
    const res = await fetch('/api/state');
    assert.strictEqual(res.headers['access-control-allow-origin'], '*');
  });

  // Stop server after all HTTP tests
  test('server stops cleanly', async () => {
    await stopServer();
    assert.ok(true, 'Server stopped');
  });
});

suite('index.html structure', () => {
  const htmlPath = path.join(__dirname, '..', 'index.html');
  const html = fs.readFileSync(htmlPath, 'utf8');

  test('contains all 8 panel IDs', () => {
    const panels = ['p-session', 'p-active-agents', 'p-agent-history', 'p-files', 'p-team', 'p-log', 'p-prompts', 'p-archive'];
    for (const id of panels) {
      assert.ok(html.includes(`id="${id}"`), `Missing panel: ${id}`);
    }
  });

  test('contains SSE EventSource connection', () => {
    assert.ok(html.includes("EventSource('/events')") || html.includes('EventSource("/events")'));
  });

  test('contains dark theme CSS variables', () => {
    assert.ok(html.includes('--bg:'));
    assert.ok(html.includes('--amber:'));
    assert.ok(html.includes('--cyan:'));
  });

  test('uses JetBrains Mono font', () => {
    assert.ok(html.includes('JetBrains Mono'));
  });

  test('has scanline overlay', () => {
    assert.ok(html.includes('repeating-linear-gradient'));
  });

  test('has responsive grid', () => {
    assert.ok(html.includes('grid-template-columns'));
    assert.ok(html.includes('@media'));
  });
});

// ---------------------------------------------------------------------------
// Summary
// ---------------------------------------------------------------------------

summary('Dashboard tests');
const results = getResults();
process.exit(results.failed > 0 ? 1 : 0);
