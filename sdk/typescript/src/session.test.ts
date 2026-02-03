/**
 * Tests for session module.
 */

import { describe, it, expect, beforeEach, afterEach } from "vitest";
import * as fs from "fs";
import * as path from "path";
import * as os from "os";
import { SessionManager } from "./session.js";

describe("SessionManager", () => {
  let tempDir: string;
  let stateDir: string;

  beforeEach(() => {
    tempDir = fs.mkdtempSync(path.join(os.tmpdir(), "cs-test-"));
    stateDir = path.join(tempDir, ".claude", "state");
  });

  afterEach(() => {
    fs.rmSync(tempDir, { recursive: true, force: true });
  });

  describe("constructor", () => {
    it("should create state and history directories", () => {
      new SessionManager(stateDir);
      expect(fs.existsSync(stateDir)).toBe(true);
      expect(fs.existsSync(path.join(stateDir, "history"))).toBe(true);
    });
  });

  describe("create", () => {
    it("should create a new session state", () => {
      const manager = new SessionManager(stateDir);
      const state = manager.create("test-session", "typescript", "add feature");

      expect(state.sessionId).toBe("test-session");
      expect(state.profile).toBe("typescript");
      expect(state.task).toBe("add feature");
      expect(state.phase).toBe("init");
      expect(state.iteration).toBe(1);
      expect(state.tasks).toEqual([]);
      expect(state.commits).toEqual([]);
      expect(state.fileChanges).toEqual([]);
    });

    it("should persist the session to disk", () => {
      const manager = new SessionManager(stateDir);
      manager.create("test-session", "python", "fix bug");

      const sessionFile = path.join(stateDir, "session.json");
      expect(fs.existsSync(sessionFile)).toBe(true);

      const data = JSON.parse(fs.readFileSync(sessionFile, "utf-8"));
      expect(data.sessionId).toBe("test-session");
    });
  });

  describe("load", () => {
    it("should return null if no session exists", () => {
      const manager = new SessionManager(stateDir);
      expect(manager.load()).toBeNull();
    });

    it("should load an existing session", () => {
      const manager = new SessionManager(stateDir);
      manager.create("test-session", "go", "refactor");

      const loaded = manager.load();
      expect(loaded).not.toBeNull();
      expect(loaded?.sessionId).toBe("test-session");
      expect(loaded?.profile).toBe("go");
    });
  });

  describe("loadSessionId", () => {
    it("should return null if no session exists", () => {
      const manager = new SessionManager(stateDir);
      expect(manager.loadSessionId()).toBeNull();
    });

    it("should return session ID if session exists", () => {
      const manager = new SessionManager(stateDir);
      manager.create("my-session-123", "typescript", "test");

      expect(manager.loadSessionId()).toBe("my-session-123");
    });
  });

  describe("save", () => {
    it("should update lastUpdated timestamp", () => {
      const manager = new SessionManager(stateDir);
      const state = manager.create("test", "typescript", "task");
      const originalTimestamp = state.lastUpdated;

      // Small delay to ensure timestamp difference
      state.phase = "execute";
      manager.save(state);

      const loaded = manager.load();
      expect(loaded?.lastUpdated).not.toBe(originalTimestamp);
    });
  });

  describe("updatePhase", () => {
    it("should update the phase", () => {
      const manager = new SessionManager(stateDir);
      manager.create("test", "typescript", "task");

      manager.updatePhase("execute");

      const loaded = manager.load();
      expect(loaded?.phase).toBe("execute");
    });

    it("should not throw if no session exists", () => {
      const manager = new SessionManager(stateDir);
      expect(() => manager.updatePhase("execute")).not.toThrow();
    });
  });

  describe("incrementIteration", () => {
    it("should increment the iteration counter", () => {
      const manager = new SessionManager(stateDir);
      manager.create("test", "typescript", "task");

      manager.incrementIteration();

      const loaded = manager.load();
      expect(loaded?.iteration).toBe(2);
    });

    it("should increment multiple times", () => {
      const manager = new SessionManager(stateDir);
      manager.create("test", "typescript", "task");

      manager.incrementIteration();
      manager.incrementIteration();
      manager.incrementIteration();

      const loaded = manager.load();
      expect(loaded?.iteration).toBe(4);
    });
  });

  describe("addCommit", () => {
    it("should add a commit hash", () => {
      const manager = new SessionManager(stateDir);
      manager.create("test", "typescript", "task");

      manager.addCommit("abc1234");

      const loaded = manager.load();
      expect(loaded?.commits).toContain("abc1234");
    });

    it("should add multiple commits", () => {
      const manager = new SessionManager(stateDir);
      manager.create("test", "typescript", "task");

      manager.addCommit("abc1234");
      manager.addCommit("def5678");

      const loaded = manager.load();
      expect(loaded?.commits).toEqual(["abc1234", "def5678"]);
    });
  });

  describe("addFileChange", () => {
    it("should add a file change", () => {
      const manager = new SessionManager(stateDir);
      manager.create("test", "typescript", "task");

      manager.addFileChange("/src/app.ts");

      const loaded = manager.load();
      expect(loaded?.fileChanges).toContain("/src/app.ts");
    });

    it("should not add duplicate file changes", () => {
      const manager = new SessionManager(stateDir);
      manager.create("test", "typescript", "task");

      manager.addFileChange("/src/app.ts");
      manager.addFileChange("/src/app.ts");

      const loaded = manager.load();
      expect(loaded?.fileChanges).toEqual(["/src/app.ts"]);
    });
  });

  describe("updateGate", () => {
    it("should update a gate result", () => {
      const manager = new SessionManager(stateDir);
      manager.create("test", "typescript", "task");

      const gateResult = {
        name: "lint",
        status: "passed" as const,
        command: "eslint .",
        output: "All files passed",
        error: "",
        durationMs: 1500,
      };

      manager.updateGate("lint", gateResult);

      const loaded = manager.load();
      expect(loaded?.gates.lint).toEqual(gateResult);
    });
  });

  describe("clear", () => {
    it("should archive and remove current session", () => {
      const manager = new SessionManager(stateDir);
      manager.create("test-session", "typescript", "task");

      manager.clear();

      // Session file should be gone
      expect(manager.load()).toBeNull();

      // But archived
      const historyDir = path.join(stateDir, "history");
      const archives = fs.readdirSync(historyDir);
      expect(archives.length).toBe(1);
      expect(archives[0]).toBe("test-session.json");
    });

    it("should not throw if no session exists", () => {
      const manager = new SessionManager(stateDir);
      expect(() => manager.clear()).not.toThrow();
    });
  });

  describe("listHistory", () => {
    it("should return empty array if no history", () => {
      const manager = new SessionManager(stateDir);
      expect(manager.listHistory()).toEqual([]);
    });

    it("should list archived sessions", () => {
      const manager = new SessionManager(stateDir);

      // Create and archive a session
      manager.create("session-1", "typescript", "task 1");
      manager.clear();

      manager.create("session-2", "python", "task 2");
      manager.clear();

      const history = manager.listHistory();
      expect(history.length).toBe(2);
      expect(history.map((h) => h.sessionId)).toContain("session-1");
      expect(history.map((h) => h.sessionId)).toContain("session-2");
    });

    it("should sort by startedAt descending", () => {
      const manager = new SessionManager(stateDir);

      manager.create("old-session", "typescript", "old task");
      manager.clear();

      manager.create("new-session", "python", "new task");
      manager.clear();

      const history = manager.listHistory();
      expect(history[0].sessionId).toBe("new-session");
      expect(history[1].sessionId).toBe("old-session");
    });
  });
});
