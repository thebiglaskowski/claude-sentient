# CLAUDE.md — Dashboard

> **Component:** Claude Sentient Web Dashboard
> **Type:** Zero-dependency Node.js web server + single-file frontend
> **Port:** 3777 (configurable via `CS_DASHBOARD_PORT`)

---

## What Is This?

A real-time dashboard that visualizes data captured by Claude Sentient's hooks. It reads the JSON state files in `.claude/state/` and streams updates to the browser via Server-Sent Events.

---

## Running

```bash
node dashboard/server.cjs                          # Default port 3777
CS_DASHBOARD_PORT=4000 node dashboard/server.cjs   # Custom port
```

Open `http://localhost:3777` in a browser. The dashboard auto-connects via SSE and updates in real time as Claude Code works.

---

## Testing

```bash
node dashboard/__tests__/test-dashboard.js
```

Tests use the project's shared `test-utils.js` pattern. They cover log parsing, state reading, archive listing, HTTP routes, SSE behavior, and frontend structure.

---

## Architecture

### Files

| File | Purpose |
|------|---------|
| `server.cjs` | HTTP server, SSE broadcast, file watcher, state reader |
| `index.html` | Single-file frontend (HTML + CSS + JS, no build step) |
| `__tests__/test-dashboard.js` | Test suite |
| `CLAUDE.md` | This file |

### Server Routes

| Route | Method | Response |
|-------|--------|----------|
| `/` | GET | Serves `index.html` |
| `/api/state` | GET | All state files merged into one JSON object |
| `/api/log?tail=N` | GET | Last N parsed lines from `session.log` (default 100) |
| `/api/archive` | GET | Session summaries from `state/archive/` |
| `/events` | GET | SSE stream |

### SSE Events

| Event | Payload | When |
|-------|---------|------|
| `full_state` | Complete state object | On client connect |
| `state_update` | `{ key, data }` | When any state JSON changes |
| `log_append` | Array of log entries | When `session.log` grows |

### State Files Read

| File | Dashboard Panel |
|------|----------------|
| `session_start.json` | Session (timer, branch, profile) |
| `active_agents.json` | Active Agents (live duration, model badges) |
| `agent_history.json` | Agent History (success/fail, duration) |
| `file_changes.json` | File Activity (tool badges, relative time) |
| `team-state.json` | Team Status (teammates, task counts) |
| `prompts.json` | Prompt Activity (topic distribution bar) |
| `last_verification.json` | (Data available but not in a dedicated panel) |
| `session.log` | Event Timeline (color-coded by level) |
| `archive/*.json` | Session History (past sessions) |

---

## Frontend Design

The dashboard is a single HTML file with embedded CSS and JS. No framework, no build step.

**Design language:** Dark theme, terminal-inspired with amber accent (`#f0b429`). JetBrains Mono font with scanline overlay for atmosphere.

**Layout:** CSS Grid — 3 columns on wide screens, 2 on medium, 1 on mobile.

**8 panels:** Session, Active Agents, Agent History, File Activity, Team Status, Event Timeline, Prompt Activity, Session History.

**Live elements:**
- Session duration timer updates every second
- Active agent duration counters update every second
- SSE pushes state changes in real time (100ms debounce)
- Pulsing cyan dots for running agents
- Green/red dots for success/fail status

**JS architecture:**
- Global `state` object as single source of truth
- `applyUpdate(key, data)` updates state and re-renders only the affected panel
- `EventSource('/events')` for real-time updates
- Archive and log fetched once on page load, then updated via SSE

---

## Key Design Decisions

1. **Zero dependencies** — Only uses Node.js built-in `http`, `fs`, `path` modules
2. **Single HTML file** — No build step, no framework, no bundler
3. **SSE over WebSocket** — Simpler, auto-reconnect, one-way data flow (server to browser)
4. **Read-only** — Dashboard never writes to state files (hooks own that)
5. **Debounced file watching** — 100ms debounce per filename prevents event storms
6. **Incremental log reading** — Tracks file size, reads only new bytes
7. **Graceful degradation** — Missing/corrupt state files return `null`, not errors
8. **Testable exports** — Pure functions exported when `require.main !== module`

---

## Conventions

- State file key names use underscores: `session_start`, `active_agents`, `team_state`
- Log format: `[cs] TIMESTAMP LEVEL: MESSAGE`
- All timestamps are ISO 8601
- The server resolves `.claude/state/` relative to `process.cwd()` (same pattern as hooks)
