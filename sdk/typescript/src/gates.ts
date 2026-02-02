/**
 * Quality gate execution for Claude Sentient SDK.
 */

import { execSync, spawn } from "child_process";
import type { Profile, GateResult, GateStatus, HookContext, GateConfig } from "./types.js";

export class QualityGates {
  private profile: Profile;
  public results: Map<string, GateResult> = new Map();

  constructor(profile: Profile) {
    this.profile = profile;
  }

  /** Run a single quality gate synchronously */
  runGate(gateName: string, cwd: string = "."): GateResult {
    if (!(gateName in this.profile.gates)) {
      return {
        name: gateName,
        status: "skipped",
        command: "",
        output: "Gate not configured for this profile",
        error: "",
        durationMs: 0,
      };
    }

    const gateConfig = this.profile.gates[gateName];
    const startTime = Date.now();

    try {
      const output = execSync(gateConfig.command, {
        cwd,
        timeout: gateConfig.timeout * 1000,
        encoding: "utf-8",
        stdio: ["pipe", "pipe", "pipe"],
      });

      const result: GateResult = {
        name: gateName,
        status: "passed",
        command: gateConfig.command,
        output: output,
        error: "",
        durationMs: Date.now() - startTime,
      };

      this.results.set(gateName, result);
      return result;
    } catch (error: unknown) {
      const execError = error as {
        status?: number;
        stdout?: string;
        stderr?: string;
        message?: string;
      };

      const result: GateResult = {
        name: gateName,
        status: "failed",
        command: gateConfig.command,
        output: execError.stdout ?? "",
        error: execError.stderr ?? execError.message ?? "Unknown error",
        durationMs: Date.now() - startTime,
      };

      this.results.set(gateName, result);
      return result;
    }
  }

  /** Run a single quality gate asynchronously */
  async runGateAsync(gateName: string, cwd: string = "."): Promise<GateResult> {
    return new Promise((resolve) => {
      if (!(gateName in this.profile.gates)) {
        resolve({
          name: gateName,
          status: "skipped",
          command: "",
          output: "Gate not configured for this profile",
          error: "",
          durationMs: 0,
        });
        return;
      }

      const gateConfig = this.profile.gates[gateName];
      const startTime = Date.now();

      const child = spawn(gateConfig.command, {
        cwd,
        shell: true,
        timeout: gateConfig.timeout * 1000,
      });

      let stdout = "";
      let stderr = "";

      child.stdout?.on("data", (data) => {
        stdout += data.toString();
      });

      child.stderr?.on("data", (data) => {
        stderr += data.toString();
      });

      child.on("close", (code) => {
        const result: GateResult = {
          name: gateName,
          status: code === 0 ? "passed" : "failed",
          command: gateConfig.command,
          output: stdout,
          error: stderr,
          durationMs: Date.now() - startTime,
        };

        this.results.set(gateName, result);
        resolve(result);
      });

      child.on("error", (error) => {
        const result: GateResult = {
          name: gateName,
          status: "failed",
          command: gateConfig.command,
          output: stdout,
          error: error.message,
          durationMs: Date.now() - startTime,
        };

        this.results.set(gateName, result);
        resolve(result);
      });
    });
  }

  /** Run all blocking gates */
  runAllBlocking(cwd: string = "."): Map<string, GateResult> {
    const gateEntries = Object.entries(this.profile.gates) as [string, GateConfig][];
    for (const [gateName, gateConfig] of gateEntries) {
      if (gateConfig.blocking) {
        this.runGate(gateName, cwd);
      }
    }
    return new Map(
      [...this.results].filter(([name]) => this.profile.gates[name]?.blocking)
    );
  }

  /** Run all blocking gates asynchronously (in parallel) */
  async runAllBlockingAsync(cwd: string = "."): Promise<Map<string, GateResult>> {
    const gateEntries = Object.entries(this.profile.gates) as [string, GateConfig][];
    const blockingGates = gateEntries
      .filter(([, config]) => config.blocking)
      .map(([name]) => name);

    await Promise.all(blockingGates.map((gate) => this.runGateAsync(gate, cwd)));

    return new Map(
      [...this.results].filter(([name]) => blockingGates.includes(name))
    );
  }

  /** Check if all blocking gates passed */
  allBlockingPassed(): boolean {
    const gateEntries = Object.entries(this.profile.gates) as [string, GateConfig][];
    for (const [gateName, gateConfig] of gateEntries) {
      if (gateConfig.blocking) {
        const result = this.results.get(gateName);
        if (!result || result.status !== "passed") {
          return false;
        }
      }
    }
    return true;
  }

  /** Get list of failed gates */
  getFailedGates(): GateResult[] {
    return [...this.results.values()].filter((r) => r.status === "failed");
  }

  /** Get a summary of gate results */
  getSummary(): {
    total: number;
    passed: number;
    failed: number;
    skipped: number;
    allBlockingPassed: boolean;
    gates: Record<string, GateStatus>;
  } {
    const results = [...this.results.values()];
    return {
      total: results.length,
      passed: results.filter((r) => r.status === "passed").length,
      failed: results.filter((r) => r.status === "failed").length,
      skipped: results.filter((r) => r.status === "skipped").length,
      allBlockingPassed: this.allBlockingPassed(),
      gates: Object.fromEntries(
        [...this.results].map(([name, result]) => [name, result.status])
      ),
    };
  }

  // Hook methods for SDK integration

  /** Run lint after file changes (PostToolUse hook) */
  async lintHook(
    inputData: Record<string, unknown>,
    _toolUseId: string,
    _context: HookContext
  ): Promise<Record<string, unknown>> {
    if (inputData.hook_event_name !== "PostToolUse") {
      return {};
    }

    const toolName = inputData.tool_name as string;
    if (!["Write", "Edit"].includes(toolName)) {
      return {};
    }

    const cwd = (inputData.cwd as string) ?? ".";
    const result = await this.runGateAsync("lint", cwd);

    if (result.status === "failed") {
      return {
        systemMessage: `Lint failed:\n${result.error || result.output}`,
      };
    }

    return {};
  }

  /** Run tests before commit (PreToolUse hook) */
  async testHook(
    inputData: Record<string, unknown>,
    _toolUseId: string,
    _context: HookContext
  ): Promise<Record<string, unknown>> {
    if (inputData.hook_event_name !== "PreToolUse") {
      return {};
    }

    if (inputData.tool_name !== "Bash") {
      return {};
    }

    const toolInput = inputData.tool_input as Record<string, unknown>;
    const command = (toolInput?.command as string) ?? "";
    if (!command.includes("git commit")) {
      return {};
    }

    const cwd = (inputData.cwd as string) ?? ".";
    const result = await this.runGateAsync("test", cwd);

    if (result.status === "failed") {
      return {
        hookSpecificOutput: {
          hookEventName: "PreToolUse",
          permissionDecision: "deny",
          permissionDecisionReason: `Tests failed:\n${result.error || result.output}`,
        },
      };
    }

    return {};
  }
}

/** Create hook configuration for quality gates */
export function createGateHooks(
  profile: Profile
): Record<string, Array<{ matcher: string; hooks: Function[] }>> {
  const gates = new QualityGates(profile);

  return {
    PostToolUse: [
      {
        matcher: "Write|Edit",
        hooks: [gates.lintHook.bind(gates)],
      },
    ],
    PreToolUse: [
      {
        matcher: "Bash",
        hooks: [gates.testHook.bind(gates)],
      },
    ],
  };
}

export type { GateResult };
