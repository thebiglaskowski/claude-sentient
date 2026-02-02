/**
 * Custom hook definitions for Claude Sentient SDK.
 */

import type { HookFunction, HookMatcher, HookContext, Phase } from "./types";
import { SessionManager } from "./session";

export class HookManager {
  private sessionManager: SessionManager;
  private customHooks: Map<string, HookMatcher[]> = new Map([
    ["PreToolUse", []],
    ["PostToolUse", []],
    ["Stop", []],
  ]);

  constructor(sessionManager?: SessionManager) {
    this.sessionManager = sessionManager ?? new SessionManager();
  }

  /** Add a custom hook */
  addHook(event: string, hook: HookFunction, matcher?: string): void {
    if (!this.customHooks.has(event)) {
      this.customHooks.set(event, []);
    }

    this.customHooks.get(event)!.push({
      matcher,
      hooks: [hook],
    });
  }

  /** Get all registered hooks */
  getHooks(): Map<string, HookMatcher[]> {
    return this.customHooks;
  }

  // Built-in hooks for session tracking

  /** Track file changes for session state */
  async trackFileChanges(
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

    const toolInput = inputData.tool_input as Record<string, unknown>;
    const filePath = toolInput?.file_path as string;
    if (filePath) {
      this.sessionManager.addFileChange(filePath);
    }

    return {};
  }

  /** Track bash commands for session state */
  async trackCommands(
    inputData: Record<string, unknown>,
    _toolUseId: string,
    _context: HookContext
  ): Promise<Record<string, unknown>> {
    if (inputData.hook_event_name !== "PostToolUse") {
      return {};
    }

    if (inputData.tool_name !== "Bash") {
      return {};
    }

    const toolInput = inputData.tool_input as Record<string, unknown>;
    const command = (toolInput?.command as string) ?? "";

    // Track git commits
    if (command.includes("git commit")) {
      const result = inputData.result as string;
      if (typeof result === "string" && result.toLowerCase().includes("commit")) {
        // Try to extract short hash from output
        const match = result.match(/\b([0-9a-f]{7,40})\b/);
        if (match) {
          this.sessionManager.addCommit(match[1]);
        }
      }
    }

    return {};
  }

  /** Save final session state on Stop */
  async saveFinalState(
    inputData: Record<string, unknown>,
    _toolUseId: string,
    _context: HookContext
  ): Promise<Record<string, unknown>> {
    if (inputData.hook_event_name !== "Stop") {
      return {};
    }

    const state = this.sessionManager.load();
    if (state) {
      state.phase = "complete";
      this.sessionManager.save(state);
    }

    return {};
  }

  /** Update session phase */
  async updatePhase(
    phase: Phase,
    _inputData: Record<string, unknown>,
    _toolUseId: string,
    _context: HookContext
  ): Promise<Record<string, unknown>> {
    this.sessionManager.updatePhase(phase);
    return {};
  }

  /** Create the default set of hooks for session tracking */
  createDefaultHooks(): Map<string, HookMatcher[]> {
    return new Map([
      [
        "PostToolUse",
        [
          {
            matcher: "Edit|Write",
            hooks: [this.trackFileChanges.bind(this)],
          },
          {
            matcher: "Bash",
            hooks: [this.trackCommands.bind(this)],
          },
        ],
      ],
      [
        "Stop",
        [
          {
            hooks: [this.saveFinalState.bind(this)],
          },
        ],
      ],
    ]);
  }

  /** Merge multiple hook configurations */
  mergeHooks(...hookConfigs: Map<string, HookMatcher[]>[]): Map<string, HookMatcher[]> {
    const merged = new Map<string, HookMatcher[]>();

    for (const config of hookConfigs) {
      for (const [event, matchers] of config) {
        if (!merged.has(event)) {
          merged.set(event, []);
        }
        merged.get(event)!.push(...matchers);
      }
    }

    return merged;
  }
}

export type { HookFunction, HookMatcher };
