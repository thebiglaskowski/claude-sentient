/**
 * Session persistence for Claude Sentient SDK.
 */

import * as fs from "fs";
import * as path from "path";
import type { SessionState, Phase, Task, GateResult } from "./types";

export class SessionManager {
  private stateDir: string;
  private stateFile: string;
  private historyDir: string;

  constructor(stateDir: string = ".claude/state") {
    this.stateDir = stateDir;
    this.stateFile = path.join(stateDir, "session.json");
    this.historyDir = path.join(stateDir, "history");

    // Ensure directories exist
    fs.mkdirSync(this.stateDir, { recursive: true });
    fs.mkdirSync(this.historyDir, { recursive: true });
  }

  /** Save current session state */
  save(state: SessionState): void {
    state.lastUpdated = new Date().toISOString();
    fs.writeFileSync(this.stateFile, JSON.stringify(state, null, 2));
  }

  /** Load current session state */
  load(): SessionState | null {
    if (!fs.existsSync(this.stateFile)) {
      return null;
    }
    try {
      const data = fs.readFileSync(this.stateFile, "utf-8");
      return JSON.parse(data) as SessionState;
    } catch {
      return null;
    }
  }

  /** Load just the session ID for resume */
  loadSessionId(): string | null {
    const state = this.load();
    return state?.sessionId ?? null;
  }

  /** Clear current session (archive to history first) */
  clear(): void {
    if (fs.existsSync(this.stateFile)) {
      const state = this.load();
      if (state) {
        const archiveFile = path.join(
          this.historyDir,
          `${state.sessionId}.json`
        );
        fs.copyFileSync(this.stateFile, archiveFile);
      }
      fs.unlinkSync(this.stateFile);
    }
  }

  /** Create a new session state */
  create(sessionId: string, profile: string, task: string): SessionState {
    const now = new Date().toISOString();
    const state: SessionState = {
      sessionId,
      startedAt: now,
      lastUpdated: now,
      phase: "init",
      iteration: 1,
      profile,
      task,
      tasks: [],
      gates: {},
      commits: [],
      fileChanges: [],
      metadata: {},
    };
    this.save(state);
    return state;
  }

  /** Update the current phase */
  updatePhase(phase: Phase): void {
    const state = this.load();
    if (state) {
      state.phase = phase;
      this.save(state);
    }
  }

  /** Increment the iteration counter */
  incrementIteration(): void {
    const state = this.load();
    if (state) {
      state.iteration += 1;
      this.save(state);
    }
  }

  /** Record a commit */
  addCommit(commitHash: string): void {
    const state = this.load();
    if (state) {
      state.commits.push(commitHash);
      this.save(state);
    }
  }

  /** Record a file change */
  addFileChange(filePath: string): void {
    const state = this.load();
    if (state && !state.fileChanges.includes(filePath)) {
      state.fileChanges.push(filePath);
      this.save(state);
    }
  }

  /** Update a gate result */
  updateGate(gateName: string, result: GateResult): void {
    const state = this.load();
    if (state) {
      state.gates[gateName] = result;
      this.save(state);
    }
  }

  /** List archived sessions */
  listHistory(): Array<{
    sessionId: string;
    task: string;
    startedAt: string;
    lastUpdated: string;
    profile: string;
  }> {
    const sessions: Array<{
      sessionId: string;
      task: string;
      startedAt: string;
      lastUpdated: string;
      profile: string;
    }> = [];

    if (!fs.existsSync(this.historyDir)) {
      return sessions;
    }

    const files = fs.readdirSync(this.historyDir);
    for (const file of files) {
      if (!file.endsWith(".json")) continue;
      try {
        const data = fs.readFileSync(
          path.join(this.historyDir, file),
          "utf-8"
        );
        const state = JSON.parse(data) as SessionState;
        sessions.push({
          sessionId: state.sessionId,
          task: state.task,
          startedAt: state.startedAt,
          lastUpdated: state.lastUpdated,
          profile: state.profile,
        });
      } catch {
        continue;
      }
    }

    return sessions.sort(
      (a, b) =>
        new Date(b.startedAt).getTime() - new Date(a.startedAt).getTime()
    );
  }
}

export type { SessionState };
