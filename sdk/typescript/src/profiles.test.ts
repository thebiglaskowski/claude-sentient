/**
 * Tests for profiles module.
 */

import { describe, it, expect, beforeEach, afterEach } from "vitest";
import * as fs from "fs";
import * as path from "path";
import * as os from "os";
import { ProfileLoader } from "./profiles.js";

describe("ProfileLoader", () => {
  let tempDir: string;

  beforeEach(() => {
    tempDir = fs.mkdtempSync(path.join(os.tmpdir(), "cs-profile-test-"));
  });

  afterEach(() => {
    fs.rmSync(tempDir, { recursive: true, force: true });
  });

  describe("load", () => {
    it("should load python profile", () => {
      const loader = new ProfileLoader();
      const profile = loader.load("python");

      expect(profile).not.toBeNull();
      expect(profile?.name).toBe("python");
      expect(profile?.detectFiles).toContain("pyproject.toml");
      expect(profile?.detectExtensions).toContain(".py");
      expect(profile?.gates.lint.command).toBe("ruff check .");
    });

    it("should load typescript profile", () => {
      const loader = new ProfileLoader();
      const profile = loader.load("typescript");

      expect(profile).not.toBeNull();
      expect(profile?.name).toBe("typescript");
      expect(profile?.detectFiles).toContain("tsconfig.json");
      expect(profile?.detectExtensions).toContain(".ts");
    });

    it("should load go profile", () => {
      const loader = new ProfileLoader();
      const profile = loader.load("go");

      expect(profile).not.toBeNull();
      expect(profile?.name).toBe("go");
      expect(profile?.detectFiles).toContain("go.mod");
      expect(profile?.gates.test.command).toBe("go test ./...");
    });

    it("should load rust profile", () => {
      const loader = new ProfileLoader();
      const profile = loader.load("rust");

      expect(profile).not.toBeNull();
      expect(profile?.name).toBe("rust");
      expect(profile?.detectFiles).toContain("Cargo.toml");
    });

    it("should load general profile", () => {
      const loader = new ProfileLoader();
      const profile = loader.load("general");

      expect(profile).not.toBeNull();
      expect(profile?.name).toBe("general");
      expect(profile?.detectFiles).toEqual([]);
    });

    it("should return null for unknown profile", () => {
      const loader = new ProfileLoader();
      const profile = loader.load("unknown-profile");

      expect(profile).toBeNull();
    });

    it("should cache loaded profiles", () => {
      const loader = new ProfileLoader();

      const profile1 = loader.load("python");
      const profile2 = loader.load("python");

      expect(profile1).toBe(profile2); // Same reference
    });
  });

  describe("detect", () => {
    it("should detect python from pyproject.toml", () => {
      fs.writeFileSync(path.join(tempDir, "pyproject.toml"), "[project]");
      const loader = new ProfileLoader();

      expect(loader.detect(tempDir)).toBe("python");
    });

    it("should detect python from setup.py", () => {
      fs.writeFileSync(path.join(tempDir, "setup.py"), "from setuptools import setup");
      const loader = new ProfileLoader();

      expect(loader.detect(tempDir)).toBe("python");
    });

    it("should detect typescript from tsconfig.json", () => {
      fs.writeFileSync(path.join(tempDir, "tsconfig.json"), "{}");
      const loader = new ProfileLoader();

      expect(loader.detect(tempDir)).toBe("typescript");
    });

    it("should detect go from go.mod", () => {
      fs.writeFileSync(path.join(tempDir, "go.mod"), "module example.com/mymodule");
      const loader = new ProfileLoader();

      expect(loader.detect(tempDir)).toBe("go");
    });

    it("should detect rust from Cargo.toml", () => {
      fs.writeFileSync(path.join(tempDir, "Cargo.toml"), "[package]");
      const loader = new ProfileLoader();

      expect(loader.detect(tempDir)).toBe("rust");
    });

    it("should detect python from .py files", () => {
      fs.writeFileSync(path.join(tempDir, "main.py"), "print('hello')");
      const loader = new ProfileLoader();

      expect(loader.detect(tempDir)).toBe("python");
    });

    it("should detect typescript from .ts files", () => {
      fs.writeFileSync(path.join(tempDir, "app.ts"), "const x: number = 1");
      const loader = new ProfileLoader();

      // Python is checked first, but we have no .py files
      // TypeScript is checked second
      expect(loader.detect(tempDir)).toBe("typescript");
    });

    it("should fall back to general if no indicators found", () => {
      const loader = new ProfileLoader();
      expect(loader.detect(tempDir)).toBe("general");
    });

    it("should prioritize config files over extensions", () => {
      // Both Python and TypeScript indicators
      fs.writeFileSync(path.join(tempDir, "pyproject.toml"), "[project]");
      fs.writeFileSync(path.join(tempDir, "app.ts"), "const x = 1");

      const loader = new ProfileLoader();
      // Python has higher priority
      expect(loader.detect(tempDir)).toBe("python");
    });
  });

  describe("getGateCommand", () => {
    it("should return the gate command", () => {
      const loader = new ProfileLoader();
      const command = loader.getGateCommand("python", "lint");

      expect(command).toBe("ruff check .");
    });

    it("should return null for unknown gate", () => {
      const loader = new ProfileLoader();
      const command = loader.getGateCommand("python", "unknown-gate");

      expect(command).toBeNull();
    });

    it("should return null for unknown profile", () => {
      const loader = new ProfileLoader();
      const command = loader.getGateCommand("unknown-profile", "lint");

      expect(command).toBeNull();
    });
  });

  describe("isGateBlocking", () => {
    it("should return true for blocking gates", () => {
      const loader = new ProfileLoader();
      expect(loader.isGateBlocking("python", "lint")).toBe(true);
      expect(loader.isGateBlocking("python", "test")).toBe(true);
    });

    it("should return false for non-blocking gates", () => {
      const loader = new ProfileLoader();
      expect(loader.isGateBlocking("python", "type")).toBe(false);
    });

    it("should default to true for unknown gates", () => {
      const loader = new ProfileLoader();
      expect(loader.isGateBlocking("python", "unknown")).toBe(true);
    });
  });
});
