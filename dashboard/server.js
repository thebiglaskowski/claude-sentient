#!/usr/bin/env node
'use strict';

const http = require('http');
const fs = require('fs');
const path = require('path');

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------

const PORT = parseInt(process.env.CS_DASHBOARD_PORT || '3777', 10);
const STATE_DIR = path.join(process.cwd(), '.claude', 'state');
const LOG_FILE = path.join(process.cwd(), '.claude', 'session.log');
const ARCHIVE_DIR = path.join(STATE_DIR, 'archive');
const DEBOUNCE_MS = 100;

const STATE_FILES = [
  'session_start.json',
  'active_agents.json',
  'agent_history.json',
  'file_changes.json',
  'team-state.json',
  'last_verification.json',
  'prompts.json'
];

// ---------------------------------------------------------------------------
// State reading
// ---------------------------------------------------------------------------

function readJsonFile(filePath) {
  try {
    const raw = fs.readFileSync(filePath, 'utf8');
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

function readAllState() {
  const state = {};
  for (const file of STATE_FILES) {
    const key = file.replace('.json', '').replace(/-/g, '_');
    state[key] = readJsonFile(path.join(STATE_DIR, file));
  }
  return state;
}

// ---------------------------------------------------------------------------
// Log parsing
// ---------------------------------------------------------------------------

/**
 * Parses [cs] log lines into structured objects.
 * Format: [cs] TIMESTAMP LEVEL: MESSAGE
 */
function parseLogLines(text, limit) {
  if (!text || typeof text !== 'string') return [];
  const lines = text.split('\n').filter(l => l.trim());
  const parsed = [];
  for (const line of lines) {
    const match = line.match(/^\[cs\]\s+(\S+)\s+(\w+):\s*(.*)$/);
    if (match) {
      parsed.push({ timestamp: match[1], level: match[2], message: match[3] });
    }
  }
  if (typeof limit === 'number' && limit > 0) {
    return parsed.slice(-limit);
  }
  return parsed;
}

// ---------------------------------------------------------------------------
// Archive listing
// ---------------------------------------------------------------------------

function listArchive() {
  try {
    const files = fs.readdirSync(ARCHIVE_DIR).filter(f => f.endsWith('.json'));
    const entries = [];
    for (const file of files) {
      const data = readJsonFile(path.join(ARCHIVE_DIR, file));
      if (data) {
        entries.push({ filename: file, ...data });
      }
    }
    // Sort newest first by timestamp
    entries.sort((a, b) => {
      const ta = a.timestamp || '';
      const tb = b.timestamp || '';
      return tb.localeCompare(ta);
    });
    return entries;
  } catch {
    return [];
  }
}

// ---------------------------------------------------------------------------
// SSE management
// ---------------------------------------------------------------------------

const clients = new Set();

function broadcast(eventName, data) {
  const payload = `event: ${eventName}\ndata: ${JSON.stringify(data)}\n\n`;
  for (const res of clients) {
    try {
      res.write(payload);
    } catch {
      clients.delete(res);
    }
  }
}

// ---------------------------------------------------------------------------
// File watcher
// ---------------------------------------------------------------------------

let watchers = [];

function setupFileWatcher() {
  const debounceTimers = {};

  // Watch state directory for JSON changes
  try {
    const stateWatcher = fs.watch(STATE_DIR, (eventType, filename) => {
      if (!filename || !filename.endsWith('.json')) return;
      clearTimeout(debounceTimers[filename]);
      debounceTimers[filename] = setTimeout(() => {
        const key = filename.replace('.json', '').replace(/-/g, '_');
        const data = readJsonFile(path.join(STATE_DIR, filename));
        if (data !== null) {
          broadcast('state_update', { key, data });
        }
      }, DEBOUNCE_MS);
    });
    watchers.push(stateWatcher);
  } catch {
    // State dir may not exist yet
  }

  // Watch session.log incrementally
  let logSize = 0;
  try {
    const stat = fs.statSync(LOG_FILE);
    logSize = stat.size;
  } catch {
    // File may not exist
  }

  try {
    const logWatcher = fs.watch(path.dirname(LOG_FILE), (eventType, filename) => {
      if (filename !== 'session.log') return;
      clearTimeout(debounceTimers['session.log']);
      debounceTimers['session.log'] = setTimeout(() => {
        try {
          const stat = fs.statSync(LOG_FILE);
          if (stat.size > logSize) {
            const fd = fs.openSync(LOG_FILE, 'r');
            const buf = Buffer.alloc(stat.size - logSize);
            fs.readSync(fd, buf, 0, buf.length, logSize);
            fs.closeSync(fd);
            logSize = stat.size;
            const newLines = parseLogLines(buf.toString('utf8'));
            if (newLines.length > 0) {
              broadcast('log_append', newLines);
            }
          } else if (stat.size < logSize) {
            // Log was truncated/rotated — reset
            logSize = stat.size;
          }
        } catch {
          // Ignore read errors
        }
      }, DEBOUNCE_MS);
    });
    watchers.push(logWatcher);
  } catch {
    // Log dir may not exist
  }
}

function closeWatchers() {
  for (const w of watchers) {
    try { w.close(); } catch { /* ignore */ }
  }
  watchers = [];
}

// ---------------------------------------------------------------------------
// HTTP server
// ---------------------------------------------------------------------------

function serveHTML(res) {
  const htmlPath = path.join(__dirname, 'index.html');
  try {
    const html = fs.readFileSync(htmlPath, 'utf8');
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(html);
  } catch {
    res.writeHead(500, { 'Content-Type': 'text/plain' });
    res.end('Could not read index.html');
  }
}

function handleRequest(req, res) {
  const url = new URL(req.url, `http://${req.headers.host}`);
  const pathname = url.pathname;

  // CORS headers for local dev
  res.setHeader('Access-Control-Allow-Origin', '*');

  if (pathname === '/' || pathname === '/index.html') {
    return serveHTML(res);
  }

  if (pathname === '/api/state') {
    const state = readAllState();
    res.writeHead(200, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify(state));
  }

  if (pathname === '/api/log') {
    const tail = parseInt(url.searchParams.get('tail') || '100', 10);
    let text = '';
    try {
      text = fs.readFileSync(LOG_FILE, 'utf8');
    } catch {
      // No log file yet
    }
    const lines = parseLogLines(text, tail);
    res.writeHead(200, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify(lines));
  }

  if (pathname === '/api/archive') {
    const entries = listArchive();
    res.writeHead(200, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify(entries));
  }

  if (pathname === '/events') {
    res.writeHead(200, {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive'
    });
    res.write('\n');

    // Send initial full state
    const state = readAllState();
    res.write(`event: full_state\ndata: ${JSON.stringify(state)}\n\n`);

    clients.add(res);
    req.on('close', () => clients.delete(res));
    return;
  }

  res.writeHead(404, { 'Content-Type': 'text/plain' });
  res.end('Not Found');
}

const server = http.createServer(handleRequest);

function startServer(port) {
  port = port || PORT;
  return new Promise((resolve, reject) => {
    server.on('error', (err) => {
      if (err.code === 'EADDRINUSE') {
        const msg = `Port ${port} is already in use. Set CS_DASHBOARD_PORT to use a different port.`;
        console.error(msg);
        reject(new Error(msg));
      } else {
        reject(err);
      }
    });
    server.listen(port, () => {
      console.log(`Claude Sentient Dashboard: http://localhost:${port}`);
      setupFileWatcher();
      resolve(server);
    });
  });
}

function stopServer() {
  return new Promise((resolve) => {
    closeWatchers();
    for (const res of clients) {
      try { res.end(); } catch { /* ignore */ }
    }
    clients.clear();
    server.close(() => resolve());
  });
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

if (require.main === module) {
  startServer().catch(() => process.exit(1));
}

// ---------------------------------------------------------------------------
// Exports for testing
// ---------------------------------------------------------------------------

module.exports = {
  readAllState,
  readJsonFile,
  parseLogLines,
  listArchive,
  startServer,
  stopServer,
  broadcast,
  clients,
  STATE_FILES
};
