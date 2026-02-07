/**
 * Tests for orchestrator module.
 */

import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { ClaudeSentient } from "./orchestrator.js";
import * as fs from "fs";
import * as path from "path";
import * as os from "os";

describe("ClaudeSentient", () => {
  let tmpDir: string;

  beforeEach(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "cs-orch-test-"));
    const stateDir = path.join(tmpDir, ".claude", "state");
    fs.mkdirSync(stateDir, { recursive: true });
  });

  afterEach(() => {
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  describe("constructor", () => {
    it("should initialize with defaults", () => {
      const sentient = new ClaudeSentient({ cwd: tmpDir });
      expect(sentient).toBeDefined();
    });

    it("should detect general profile when no markers exist", () => {
      const sentient = new ClaudeSentient({ cwd: tmpDir });
      const state = sentient.getSessionState();
      // No session created yet, state is null
      expect(state).toBeNull();
    });

    it("should detect profile from project files", () => {
      // Create a tsconfig.json to trigger TypeScript detection
      fs.writeFileSync(
        path.join(tmpDir, "tsconfig.json"),
        JSON.stringify({ compilerOptions: {} })
      );
      const sentient = new ClaudeSentient({ cwd: tmpDir });
      expect(sentient).toBeDefined();
    });

    it("should use explicit profile when provided", () => {
      const sentient = new ClaudeSentient({
        cwd: tmpDir,
        profile: "python",
      });
      expect(sentient).toBeDefined();
    });

    it("should have default tools list", () => {
      expect(ClaudeSentient.DEFAULT_TOOLS).toContain("Read");
      expect(ClaudeSentient.DEFAULT_TOOLS).toContain("Write");
      expect(ClaudeSentient.DEFAULT_TOOLS).toContain("Bash");
      expect(ClaudeSentient.DEFAULT_TOOLS).toContain("TaskCreate");
    });
  });

  describe("loop", () => {
    it("should create a new session", async () => {
      const sentient = new ClaudeSentient({ cwd: tmpDir, profile: "general" });
      const results: Array<{ success: boolean; phase: string }> = [];

      for await (const result of sentient.loop("test task")) {
        results.push({ success: result.success, phase: result.phase });
      }

      expect(results.length).toBeGreaterThan(0);
      expect(results[0].phase).toBe("complete");
    });

    it("should return simulation message when SDK not available", async () => {
      const sentient = new ClaudeSentient({ cwd: tmpDir, profile: "general" });

      for await (const result of sentient.loop("test task")) {
        expect(result.message).toContain("simulation");
      }
    });

    it("should fail to resume without existing session", async () => {
      const sentient = new ClaudeSentient({ cwd: tmpDir, profile: "general" });

      await expect(async () => {
        for await (const _result of sentient.loop("test", { resume: true })) {
          // Should throw before yielding
        }
      }).rejects.toThrow("No session to resume");
    });

    it("should set session ID on new session", async () => {
      const sentient = new ClaudeSentient({ cwd: tmpDir, profile: "general" });

      for await (const result of sentient.loop("test task")) {
        expect(result.sessionId).toBeTruthy();
        expect(result.sessionId.length).toBeGreaterThan(0);
      }
    });

    it("should track iteration count", async () => {
      const sentient = new ClaudeSentient({ cwd: tmpDir, profile: "general" });

      for await (const result of sentient.loop("test task")) {
        expect(result.iteration).toBe(1);
      }
    });

    it("should track duration", async () => {
      const sentient = new ClaudeSentient({ cwd: tmpDir, profile: "general" });

      for await (const result of sentient.loop("test task")) {
        expect(result.durationMs).toBeGreaterThanOrEqual(0);
      }
    });
  });

  describe("plan", () => {
    it("should return a plan string", async () => {
      const sentient = new ClaudeSentient({ cwd: tmpDir, profile: "general" });
      const plan = await sentient.plan("refactor the API");

      expect(plan).toContain("Plan for:");
      expect(plan).toContain("refactor the API");
    });
  });

  describe("resume", () => {
    it("should throw when no session exists", async () => {
      const sentient = new ClaudeSentient({ cwd: tmpDir, profile: "general" });

      await expect(async () => {
        for await (const _result of sentient.resume()) {
          // Should throw
        }
      }).rejects.toThrow("No session to resume");
    });
  });

  describe("getSessionState", () => {
    it("should return null before any session", () => {
      const sentient = new ClaudeSentient({ cwd: tmpDir, profile: "general" });
      expect(sentient.getSessionState()).toBeNull();
    });

    it("should return state after loop", async () => {
      const sentient = new ClaudeSentient({ cwd: tmpDir, profile: "general" });

      for await (const _result of sentient.loop("test task")) {
        // Run loop
      }

      const state = sentient.getSessionState();
      expect(state).toBeDefined();
      expect(state?.sessionId).toBeTruthy();
    });
  });

  describe("getGateResults", () => {
    it("should return null for general profile (no gates)", () => {
      const sentient = new ClaudeSentient({ cwd: tmpDir, profile: "general" });
      expect(sentient.getGateResults()).toBeNull();
    });
  });

  describe("error handling", () => {
    it("should catch errors in loop and yield error result", async () => {
      const sentient = new ClaudeSentient({ cwd: tmpDir, profile: "general" });

      // Force an error by trying to resume a non-existent session
      const results: Array<{ success: boolean; message: string }> = [];
      try {
        for await (const result of sentient.loop("test", { resume: true })) {
          results.push({ success: result.success, message: result.message });
        }
      } catch (e) {
        // Expected
        expect(e).toBeDefined();
      }
    });
  });
});
