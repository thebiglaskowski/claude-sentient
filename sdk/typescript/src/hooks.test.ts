/**
 * Tests for hooks module.
 */

import { describe, it, expect, beforeEach, afterEach } from "vitest";
import * as fs from "fs";
import * as path from "path";
import * as os from "os";
import { HookManager } from "./hooks.js";
import { SessionManager } from "./session.js";
import type { HookContext } from "./types.js";

describe("HookManager", () => {
  let tempDir: string;
  let stateDir: string;
  let sessionManager: SessionManager;

  beforeEach(() => {
    tempDir = fs.mkdtempSync(path.join(os.tmpdir(), "cs-hook-test-"));
    stateDir = path.join(tempDir, ".claude", "state");
    sessionManager = new SessionManager(stateDir);
  });

  afterEach(() => {
    fs.rmSync(tempDir, { recursive: true, force: true });
  });

  const mockContext: HookContext = {
    sessionId: "test",
    phase: "execute",
    iteration: 1,
    profile: "typescript",
    cwd: ".",
    tasks: [],
    gates: {},
  };

  describe("constructor", () => {
    it("should initialize with default events", () => {
      const manager = new HookManager(sessionManager);
      const hooks = manager.getHooks();

      expect(hooks.has("PreToolUse")).toBe(true);
      expect(hooks.has("PostToolUse")).toBe(true);
      expect(hooks.has("Stop")).toBe(true);
    });

    it("should create a session manager if not provided", () => {
      const manager = new HookManager();
      expect(manager.getHooks()).toBeDefined();
    });
  });

  describe("addHook", () => {
    it("should add a hook to existing event", () => {
      const manager = new HookManager(sessionManager);
      const hook = async () => ({ added: true });

      manager.addHook("PostToolUse", hook);

      const hooks = manager.getHooks();
      expect(hooks.get("PostToolUse")?.length).toBeGreaterThan(0);
    });

    it("should add a hook with matcher", () => {
      const manager = new HookManager(sessionManager);
      const hook = async () => ({});

      manager.addHook("PostToolUse", hook, "Write|Edit");

      const hooks = manager.getHooks();
      const lastMatcher = hooks.get("PostToolUse")!.at(-1);
      expect(lastMatcher?.matcher).toBe("Write|Edit");
    });

    it("should create new event if it doesn't exist", () => {
      const manager = new HookManager(sessionManager);
      const hook = async () => ({});

      manager.addHook("CustomEvent", hook);

      expect(manager.getHooks().has("CustomEvent")).toBe(true);
    });
  });

  describe("trackFileChanges", () => {
    it("should ignore non-PostToolUse events", async () => {
      sessionManager.create("test", "typescript", "task");
      const manager = new HookManager(sessionManager);

      await manager.trackFileChanges(
        { hook_event_name: "PreToolUse", tool_name: "Write" },
        "tool-123",
        mockContext
      );

      const state = sessionManager.load();
      expect(state?.fileChanges).toEqual([]);
    });

    it("should ignore non-file tools", async () => {
      sessionManager.create("test", "typescript", "task");
      const manager = new HookManager(sessionManager);

      await manager.trackFileChanges(
        { hook_event_name: "PostToolUse", tool_name: "Bash" },
        "tool-123",
        mockContext
      );

      const state = sessionManager.load();
      expect(state?.fileChanges).toEqual([]);
    });

    it("should track Write tool file changes", async () => {
      sessionManager.create("test", "typescript", "task");
      const manager = new HookManager(sessionManager);

      await manager.trackFileChanges(
        {
          hook_event_name: "PostToolUse",
          tool_name: "Write",
          tool_input: { file_path: "/src/app.ts" },
        },
        "tool-123",
        mockContext
      );

      const state = sessionManager.load();
      expect(state?.fileChanges).toContain("/src/app.ts");
    });

    it("should track Edit tool file changes", async () => {
      sessionManager.create("test", "typescript", "task");
      const manager = new HookManager(sessionManager);

      await manager.trackFileChanges(
        {
          hook_event_name: "PostToolUse",
          tool_name: "Edit",
          tool_input: { file_path: "/src/utils.ts" },
        },
        "tool-123",
        mockContext
      );

      const state = sessionManager.load();
      expect(state?.fileChanges).toContain("/src/utils.ts");
    });
  });

  describe("trackCommands", () => {
    it("should ignore non-PostToolUse events", async () => {
      sessionManager.create("test", "typescript", "task");
      const manager = new HookManager(sessionManager);

      await manager.trackCommands(
        { hook_event_name: "PreToolUse", tool_name: "Bash" },
        "tool-123",
        mockContext
      );

      const state = sessionManager.load();
      expect(state?.commits).toEqual([]);
    });

    it("should ignore non-Bash tools", async () => {
      sessionManager.create("test", "typescript", "task");
      const manager = new HookManager(sessionManager);

      await manager.trackCommands(
        { hook_event_name: "PostToolUse", tool_name: "Write" },
        "tool-123",
        mockContext
      );

      const state = sessionManager.load();
      expect(state?.commits).toEqual([]);
    });

    it("should track git commit hashes", async () => {
      sessionManager.create("test", "typescript", "task");
      const manager = new HookManager(sessionManager);

      await manager.trackCommands(
        {
          hook_event_name: "PostToolUse",
          tool_name: "Bash",
          tool_input: { command: "git commit -m 'test'" },
          result: "[main abc1234] test commit",
        },
        "tool-123",
        mockContext
      );

      const state = sessionManager.load();
      expect(state?.commits).toContain("abc1234");
    });

    it("should handle missing hash in commit output", async () => {
      sessionManager.create("test", "typescript", "task");
      const manager = new HookManager(sessionManager);

      await manager.trackCommands(
        {
          hook_event_name: "PostToolUse",
          tool_name: "Bash",
          tool_input: { command: "git commit -m 'test'" },
          result: "No changes to commit",
        },
        "tool-123",
        mockContext
      );

      const state = sessionManager.load();
      expect(state?.commits).toEqual([]);
    });
  });

  describe("saveFinalState", () => {
    it("should ignore non-Stop events", async () => {
      sessionManager.create("test", "typescript", "task");
      const manager = new HookManager(sessionManager);

      await manager.saveFinalState(
        { hook_event_name: "PostToolUse" },
        "tool-123",
        mockContext
      );

      const state = sessionManager.load();
      expect(state?.phase).toBe("init");
    });

    it("should update phase to complete on Stop", async () => {
      sessionManager.create("test", "typescript", "task");
      const manager = new HookManager(sessionManager);

      await manager.saveFinalState(
        { hook_event_name: "Stop" },
        "tool-123",
        mockContext
      );

      const state = sessionManager.load();
      expect(state?.phase).toBe("complete");
    });

    it("should handle missing session gracefully", async () => {
      const manager = new HookManager(sessionManager);

      // Should not throw
      await expect(
        manager.saveFinalState(
          { hook_event_name: "Stop" },
          "tool-123",
          mockContext
        )
      ).resolves.toEqual({});
    });
  });

  describe("updatePhase", () => {
    it("should update session phase", async () => {
      sessionManager.create("test", "typescript", "task");
      const manager = new HookManager(sessionManager);

      await manager.updatePhase("execute", {}, "tool-123", mockContext);

      const state = sessionManager.load();
      expect(state?.phase).toBe("execute");
    });
  });

  describe("createDefaultHooks", () => {
    it("should create default hooks structure", () => {
      const manager = new HookManager(sessionManager);
      const hooks = manager.createDefaultHooks();

      expect(hooks.has("PostToolUse")).toBe(true);
      expect(hooks.has("Stop")).toBe(true);

      // PostToolUse should have matchers for files and bash
      const postToolUse = hooks.get("PostToolUse")!;
      expect(postToolUse.length).toBe(2);
      expect(postToolUse[0].matcher).toBe("Edit|Write");
      expect(postToolUse[1].matcher).toBe("Bash");
    });
  });

  describe("mergeHooks", () => {
    it("should merge empty configs", () => {
      const manager = new HookManager(sessionManager);
      const merged = manager.mergeHooks(new Map(), new Map());

      expect(merged.size).toBe(0);
    });

    it("should merge single config", () => {
      const manager = new HookManager(sessionManager);
      const config = new Map([
        ["PostToolUse", [{ hooks: [async () => ({})] }]],
      ]);

      const merged = manager.mergeHooks(config);

      expect(merged.has("PostToolUse")).toBe(true);
    });

    it("should merge multiple configs", () => {
      const manager = new HookManager(sessionManager);
      const config1 = new Map([
        ["PostToolUse", [{ hooks: [async () => ({ a: 1 })] }]],
      ]);
      const config2 = new Map([
        ["PostToolUse", [{ hooks: [async () => ({ b: 2 })] }]],
      ]);

      const merged = manager.mergeHooks(config1, config2);

      expect(merged.get("PostToolUse")?.length).toBe(2);
    });

    it("should merge different events", () => {
      const manager = new HookManager(sessionManager);
      const config1 = new Map([
        ["PostToolUse", [{ hooks: [async () => ({})] }]],
      ]);
      const config2 = new Map([["Stop", [{ hooks: [async () => ({})] }]]]);

      const merged = manager.mergeHooks(config1, config2);

      expect(merged.has("PostToolUse")).toBe(true);
      expect(merged.has("Stop")).toBe(true);
    });
  });
});
