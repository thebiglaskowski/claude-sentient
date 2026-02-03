/**
 * Tests for gates module.
 */

import { describe, it, expect, beforeEach } from "vitest";
import { QualityGates, createGateHooks } from "./gates.js";
import type { Profile, HookContext, GateConfig } from "./types.js";

describe("QualityGates", () => {
  const mockProfile: Profile = {
    name: "test",
    detectFiles: [],
    detectExtensions: [],
    gates: {
      lint: { command: "echo lint-ok", blocking: true, timeout: 10 },
      test: { command: "echo test-ok", blocking: true, timeout: 10 },
      type: { command: "echo type-ok", blocking: false, timeout: 10 },
      failing: { command: "exit 1", blocking: true, timeout: 10 },
    },
    conventions: {},
    tools: [],
  };

  describe("constructor", () => {
    it("should initialize with empty results", () => {
      const gates = new QualityGates(mockProfile);
      expect(gates.results.size).toBe(0);
    });
  });

  describe("runGate", () => {
    it("should run a passing gate", () => {
      const gates = new QualityGates(mockProfile);
      const result = gates.runGate("lint");

      expect(result.name).toBe("lint");
      expect(result.status).toBe("passed");
      expect(result.command).toBe("echo lint-ok");
      expect(result.output).toContain("lint-ok");
      expect(result.durationMs).toBeGreaterThanOrEqual(0);
    });

    it("should run a failing gate", () => {
      const gates = new QualityGates(mockProfile);
      const result = gates.runGate("failing");

      expect(result.name).toBe("failing");
      expect(result.status).toBe("failed");
    });

    it("should skip unconfigured gates", () => {
      const gates = new QualityGates(mockProfile);
      const result = gates.runGate("unknown-gate");

      expect(result.status).toBe("skipped");
      expect(result.output).toContain("not configured");
    });

    it("should store results", () => {
      const gates = new QualityGates(mockProfile);
      gates.runGate("lint");

      expect(gates.results.has("lint")).toBe(true);
    });
  });

  describe("runGateAsync", () => {
    it("should run a passing gate asynchronously", async () => {
      const gates = new QualityGates(mockProfile);
      const result = await gates.runGateAsync("lint");

      expect(result.status).toBe("passed");
    });

    it("should run a failing gate asynchronously", async () => {
      const gates = new QualityGates(mockProfile);
      const result = await gates.runGateAsync("failing");

      expect(result.status).toBe("failed");
    });

    it("should skip unconfigured gates", async () => {
      const gates = new QualityGates(mockProfile);
      const result = await gates.runGateAsync("unknown-gate");

      expect(result.status).toBe("skipped");
    });
  });

  describe("runAllBlocking", () => {
    it("should run all blocking gates", () => {
      const gates = new QualityGates({
        ...mockProfile,
        gates: {
          lint: { command: "echo lint", blocking: true, timeout: 10 },
          test: { command: "echo test", blocking: true, timeout: 10 },
          type: { command: "echo type", blocking: false, timeout: 10 },
        },
      });

      const results = gates.runAllBlocking();

      expect(results.has("lint")).toBe(true);
      expect(results.has("test")).toBe(true);
      expect(results.has("type")).toBe(false); // Non-blocking
    });
  });

  describe("runAllBlockingAsync", () => {
    it("should run all blocking gates in parallel", async () => {
      const gates = new QualityGates({
        ...mockProfile,
        gates: {
          lint: { command: "echo lint", blocking: true, timeout: 10 },
          test: { command: "echo test", blocking: true, timeout: 10 },
        },
      });

      const results = await gates.runAllBlockingAsync();

      expect(results.size).toBe(2);
      expect(results.get("lint")?.status).toBe("passed");
      expect(results.get("test")?.status).toBe("passed");
    });
  });

  describe("allBlockingPassed", () => {
    it("should return true when all blocking gates pass", () => {
      const gates = new QualityGates({
        ...mockProfile,
        gates: {
          lint: { command: "echo ok", blocking: true, timeout: 10 },
          test: { command: "echo ok", blocking: true, timeout: 10 },
        },
      });

      gates.runAllBlocking();
      expect(gates.allBlockingPassed()).toBe(true);
    });

    it("should return false when a blocking gate fails", () => {
      const gates = new QualityGates({
        ...mockProfile,
        gates: {
          lint: { command: "echo ok", blocking: true, timeout: 10 },
          test: { command: "exit 1", blocking: true, timeout: 10 },
        },
      });

      gates.runAllBlocking();
      expect(gates.allBlockingPassed()).toBe(false);
    });

    it("should return true if non-blocking gates fail", () => {
      const gates = new QualityGates({
        ...mockProfile,
        gates: {
          lint: { command: "echo ok", blocking: true, timeout: 10 },
          type: { command: "exit 1", blocking: false, timeout: 10 },
        },
      });

      gates.runGate("lint");
      gates.runGate("type");
      expect(gates.allBlockingPassed()).toBe(true);
    });

    it("should return true when no blocking gates defined", () => {
      const gates = new QualityGates({
        ...mockProfile,
        gates: {},
      });

      expect(gates.allBlockingPassed()).toBe(true);
    });
  });

  describe("getFailedGates", () => {
    it("should return list of failed gates", () => {
      const gates = new QualityGates({
        ...mockProfile,
        gates: {
          lint: { command: "echo ok", blocking: true, timeout: 10 },
          test: { command: "exit 1", blocking: true, timeout: 10 },
        },
      });

      gates.runAllBlocking();
      const failed = gates.getFailedGates();

      expect(failed.length).toBe(1);
      expect(failed[0].name).toBe("test");
    });

    it("should return empty array when all pass", () => {
      const gates = new QualityGates({
        ...mockProfile,
        gates: {
          lint: { command: "echo ok", blocking: true, timeout: 10 },
        },
      });

      gates.runAllBlocking();
      expect(gates.getFailedGates()).toEqual([]);
    });
  });

  describe("getSummary", () => {
    it("should return correct summary", () => {
      const gates = new QualityGates({
        ...mockProfile,
        gates: {
          lint: { command: "echo ok", blocking: true, timeout: 10 },
          test: { command: "exit 1", blocking: true, timeout: 10 },
          type: { command: "echo ok", blocking: false, timeout: 10 },
        },
      });

      gates.runGate("lint");
      gates.runGate("test");
      gates.runGate("type");
      // Note: runGate("unknown") returns skipped but doesn't store in results
      // since it's not in the profile's gates

      const summary = gates.getSummary();

      expect(summary.total).toBe(3);
      expect(summary.passed).toBe(2);
      expect(summary.failed).toBe(1);
      expect(summary.skipped).toBe(0);
      expect(summary.allBlockingPassed).toBe(false);
      expect(summary.gates.lint).toBe("passed");
      expect(summary.gates.test).toBe("failed");
    });
  });

  describe("lintHook", () => {
    const mockContext: HookContext = {
      sessionId: "test",
      phase: "execute",
      iteration: 1,
      profile: "test",
      cwd: ".",
      tasks: [],
      gates: {},
    };

    it("should ignore non-PostToolUse events", async () => {
      const gates = new QualityGates(mockProfile);
      const result = await gates.lintHook(
        { hook_event_name: "PreToolUse", tool_name: "Write" },
        "tool-123",
        mockContext
      );

      expect(result).toEqual({});
    });

    it("should ignore non-file tools", async () => {
      const gates = new QualityGates(mockProfile);
      const result = await gates.lintHook(
        { hook_event_name: "PostToolUse", tool_name: "Bash" },
        "tool-123",
        mockContext
      );

      expect(result).toEqual({});
    });
  });

  describe("testHook", () => {
    const mockContext: HookContext = {
      sessionId: "test",
      phase: "execute",
      iteration: 1,
      profile: "test",
      cwd: ".",
      tasks: [],
      gates: {},
    };

    it("should ignore non-PreToolUse events", async () => {
      const gates = new QualityGates(mockProfile);
      const result = await gates.testHook(
        { hook_event_name: "PostToolUse", tool_name: "Bash" },
        "tool-123",
        mockContext
      );

      expect(result).toEqual({});
    });

    it("should ignore non-Bash tools", async () => {
      const gates = new QualityGates(mockProfile);
      const result = await gates.testHook(
        { hook_event_name: "PreToolUse", tool_name: "Write" },
        "tool-123",
        mockContext
      );

      expect(result).toEqual({});
    });

    it("should ignore non-git-commit commands", async () => {
      const gates = new QualityGates(mockProfile);
      const result = await gates.testHook(
        {
          hook_event_name: "PreToolUse",
          tool_name: "Bash",
          tool_input: { command: "npm test" },
        },
        "tool-123",
        mockContext
      );

      expect(result).toEqual({});
    });
  });
});

describe("createGateHooks", () => {
  it("should create hooks structure", () => {
    const profile: Profile = {
      name: "test",
      detectFiles: [],
      detectExtensions: [],
      gates: {
        lint: { command: "echo ok", blocking: true, timeout: 10 },
      },
      conventions: {},
      tools: [],
    };

    const hooks = createGateHooks(profile);

    expect(hooks.PostToolUse).toBeDefined();
    expect(hooks.PostToolUse[0].matcher).toBe("Write|Edit");
    expect(hooks.PostToolUse[0].hooks.length).toBe(1);

    expect(hooks.PreToolUse).toBeDefined();
    expect(hooks.PreToolUse[0].matcher).toBe("Bash");
    expect(hooks.PreToolUse[0].hooks.length).toBe(1);
  });
});
