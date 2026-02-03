/**
 * Tests for types module.
 *
 * These tests verify that the type definitions are correct
 * by creating objects that conform to the interfaces.
 */

import { describe, it, expect } from "vitest";
import type {
  Phase,
  TaskStatus,
  GateStatus,
  Task,
  GateResult,
  LoopResult,
  ToolUseEvent,
  HookContext,
  HookMatcher,
  GateConfig,
  Profile,
  SessionState,
  AgentDefinition,
  ClaudeSentientOptions,
  LoopOptions,
} from "./types.js";

describe("Type Definitions", () => {
  describe("Phase", () => {
    it("should accept valid phase values", () => {
      const phases: Phase[] = [
        "init",
        "understand",
        "plan",
        "execute",
        "verify",
        "commit",
        "evaluate",
        "complete",
        "error",
      ];
      expect(phases).toHaveLength(9);
    });
  });

  describe("TaskStatus", () => {
    it("should accept valid task status values", () => {
      const statuses: TaskStatus[] = [
        "pending",
        "in_progress",
        "completed",
        "blocked",
      ];
      expect(statuses).toHaveLength(4);
    });
  });

  describe("GateStatus", () => {
    it("should accept valid gate status values", () => {
      const statuses: GateStatus[] = ["pending", "passed", "failed", "skipped"];
      expect(statuses).toHaveLength(4);
    });
  });

  describe("Task", () => {
    it("should create a valid task object", () => {
      const task: Task = {
        id: "task-123",
        subject: "Add feature",
        description: "Implement user authentication",
        status: "pending",
        blockedBy: [],
        blocks: ["task-456"],
        createdAt: new Date().toISOString(),
        metadata: { priority: "high" },
      };

      expect(task.id).toBe("task-123");
      expect(task.status).toBe("pending");
      expect(task.blocks).toContain("task-456");
    });

    it("should allow optional completedAt", () => {
      const task: Task = {
        id: "task-123",
        subject: "Done task",
        description: "Completed work",
        status: "completed",
        blockedBy: [],
        blocks: [],
        createdAt: new Date().toISOString(),
        completedAt: new Date().toISOString(),
        metadata: {},
      };

      expect(task.completedAt).toBeDefined();
    });
  });

  describe("GateResult", () => {
    it("should create a valid gate result", () => {
      const result: GateResult = {
        name: "lint",
        status: "passed",
        command: "eslint .",
        output: "No errors found",
        error: "",
        durationMs: 1234,
      };

      expect(result.name).toBe("lint");
      expect(result.status).toBe("passed");
      expect(result.durationMs).toBe(1234);
    });
  });

  describe("LoopResult", () => {
    it("should create a valid loop result", () => {
      const result: LoopResult = {
        success: true,
        sessionId: "session-123",
        phase: "complete",
        iteration: 3,
        tasksCompleted: 5,
        tasksRemaining: 0,
        gatesPassed: { lint: true, test: true },
        commitHash: "abc1234",
        durationMs: 60000,
        costUsd: 0.42,
        message: "All tasks completed successfully",
      };

      expect(result.success).toBe(true);
      expect(result.gatesPassed.lint).toBe(true);
    });
  });

  describe("ToolUseEvent", () => {
    it("should create a valid tool use event", () => {
      const event: ToolUseEvent = {
        toolName: "Write",
        toolInput: { file_path: "/src/app.ts", content: "code" },
        toolUseId: "tool-123",
        result: { success: true },
      };

      expect(event.toolName).toBe("Write");
      expect(event.result).toEqual({ success: true });
    });
  });

  describe("HookContext", () => {
    it("should create a valid hook context", () => {
      const context: HookContext = {
        sessionId: "session-123",
        phase: "execute",
        iteration: 2,
        profile: "typescript",
        cwd: "/project",
        tasks: [],
        gates: {},
      };

      expect(context.phase).toBe("execute");
      expect(context.profile).toBe("typescript");
    });
  });

  describe("HookMatcher", () => {
    it("should create a valid hook matcher", () => {
      const matcher: HookMatcher = {
        matcher: "Write|Edit",
        hooks: [
          async (input, toolUseId, context) => {
            return { tracked: true };
          },
        ],
      };

      expect(matcher.matcher).toBe("Write|Edit");
      expect(matcher.hooks).toHaveLength(1);
    });
  });

  describe("GateConfig", () => {
    it("should create a valid gate config", () => {
      const config: GateConfig = {
        command: "npm test",
        blocking: true,
        timeout: 300,
      };

      expect(config.command).toBe("npm test");
      expect(config.blocking).toBe(true);
    });
  });

  describe("Profile", () => {
    it("should create a valid profile", () => {
      const profile: Profile = {
        name: "typescript",
        detectFiles: ["tsconfig.json"],
        detectExtensions: [".ts", ".tsx"],
        gates: {
          lint: { command: "eslint .", blocking: true, timeout: 120 },
          test: { command: "vitest run", blocking: true, timeout: 300 },
        },
        conventions: { style: "functional" },
        tools: ["eslint", "vitest"],
      };

      expect(profile.name).toBe("typescript");
      expect(profile.gates.lint.blocking).toBe(true);
    });
  });

  describe("SessionState", () => {
    it("should create a valid session state", () => {
      const state: SessionState = {
        sessionId: "session-123",
        startedAt: new Date().toISOString(),
        lastUpdated: new Date().toISOString(),
        phase: "init",
        iteration: 1,
        profile: "typescript",
        task: "Add feature",
        tasks: [],
        gates: {},
        commits: [],
        fileChanges: [],
        metadata: {},
      };

      expect(state.sessionId).toBe("session-123");
      expect(state.phase).toBe("init");
    });
  });

  describe("AgentDefinition", () => {
    it("should create a valid agent definition", () => {
      const agent: AgentDefinition = {
        description: "Code explorer",
        prompt: "Explore the codebase",
        tools: ["Glob", "Grep", "Read"],
        model: "haiku",
      };

      expect(agent.model).toBe("haiku");
      expect(agent.tools).toContain("Grep");
    });
  });

  describe("ClaudeSentientOptions", () => {
    it("should create valid options with all fields", () => {
      const options: ClaudeSentientOptions = {
        cwd: "/project",
        profile: "typescript",
        permissionMode: "auto",
        profilesDir: "/profiles",
      };

      expect(options.cwd).toBe("/project");
    });

    it("should allow empty options", () => {
      const options: ClaudeSentientOptions = {};
      expect(options).toEqual({});
    });
  });

  describe("LoopOptions", () => {
    it("should create valid loop options", () => {
      const options: LoopOptions = {
        resume: true,
        maxIterations: 10,
      };

      expect(options.resume).toBe(true);
      expect(options.maxIterations).toBe(10);
    });
  });
});
