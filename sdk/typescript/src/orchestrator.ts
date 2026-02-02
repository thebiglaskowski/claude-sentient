/**
 * Main orchestrator for Claude Sentient SDK.
 */

import * as path from "path";
import { v4 as uuidv4 } from "uuid";
import type {
  LoopResult,
  LoopOptions,
  ClaudeSentientOptions,
  SessionState,
} from "./types.js";
import { SessionManager } from "./session.js";
import { ProfileLoader, Profile } from "./profiles.js";
import { QualityGates } from "./gates.js";
// Note: HookManager import reserved for future Claude Agent SDK integration
// import { HookManager } from "./hooks.js";

/**
 * SDK wrapper for Claude Sentient autonomous development loop.
 *
 * This class provides programmatic access to Claude Sentient's capabilities,
 * enabling session persistence, SDK-based orchestration, and production deployment.
 *
 * @example
 * ```typescript
 * const sentient = new ClaudeSentient({ cwd: "./my-project" });
 *
 * // Run the autonomous loop
 * for await (const result of sentient.loop("Add user authentication")) {
 *   console.log(`Phase: ${result.phase}, Tasks: ${result.tasksCompleted}`);
 *   if (result.success) {
 *     console.log(`Done! Commit: ${result.commitHash}`);
 *   }
 * }
 *
 * // Or plan without executing
 * const plan = await sentient.plan("Refactor the API layer");
 * console.log(plan);
 *
 * // Resume a previous session
 * for await (const result of sentient.resume()) {
 *   console.log(`Resumed: ${result.phase}`);
 * }
 * ```
 */
export class ClaudeSentient {
  private cwd: string;
  private sessionManager: SessionManager;
  private profileLoader: ProfileLoader;
  private profileName: string;
  private profile: Profile | null;
  private gates: QualityGates | null;
  private sessionId: string | null = null;
  // Note: HookManager reserved for future Claude Agent SDK integration

  static readonly DEFAULT_TOOLS = [
    "Read",
    "Write",
    "Edit",
    "Bash",
    "Glob",
    "Grep",
    "Task",
    "TaskCreate",
    "TaskUpdate",
    "TaskList",
    "EnterPlanMode",
    "ExitPlanMode",
  ];

  constructor(options: ClaudeSentientOptions = {}) {
    this.cwd = path.resolve(options.cwd ?? ".");
    // Note: permissionMode reserved for future Claude Agent SDK integration

    // Initialize managers
    this.sessionManager = new SessionManager(
      path.join(this.cwd, ".claude/state")
    );
    this.profileLoader = new ProfileLoader(options.profilesDir);

    // Detect or load profile
    this.profileName = options.profile ?? this.profileLoader.detect(this.cwd);
    this.profile = this.profileLoader.load(this.profileName);

    // Initialize quality gates
    this.gates = this.profile ? new QualityGates(this.profile) : null;
  }

  /**
   * Execute autonomous development loop.
   *
   * @param task - The task description to execute
   * @param options - Loop options (resume, maxIterations)
   * @yields LoopResult for each phase/iteration
   */
  async *loop(
    task: string,
    options: LoopOptions = {}
  ): AsyncGenerator<LoopResult> {
    const { resume = false, maxIterations = 10 } = options;

    // Handle resume
    if (resume) {
      const existingState = this.sessionManager.load();
      if (existingState) {
        this.sessionId = existingState.sessionId;
      } else {
        throw new Error("No session to resume");
      }
    } else {
      // Create new session
      this.sessionId = uuidv4().substring(0, 8);
      this.sessionManager.create(this.sessionId, this.profileName, task);
    }

    try {
      // Note: In a real implementation, this would use the Claude Agent SDK
      // For now, we provide a simulation that shows the expected interface
      yield await this.simulateLoop(task, maxIterations);
    } catch (error) {
      yield {
        success: false,
        sessionId: this.sessionId,
        phase: "error",
        iteration: 0,
        tasksCompleted: 0,
        tasksRemaining: 0,
        gatesPassed: {},
        durationMs: 0,
        costUsd: 0,
        message: error instanceof Error ? error.message : "Unknown error",
      };
    }
  }

  /**
   * Simulate the loop for SDK interface demonstration.
   * In a real implementation, this would call the Claude Agent SDK.
   */
  private async simulateLoop(
    _task: string,
    _maxIterations: number
  ): Promise<LoopResult> {
    const startTime = Date.now();

    // Update phase
    this.sessionManager.updatePhase("execute");

    // Run quality gates if available
    const gatesPassed: Record<string, boolean> = {};
    if (this.gates) {
      const results = await this.gates.runAllBlockingAsync(this.cwd);
      for (const [name, result] of results) {
        gatesPassed[name] = result.status === "passed";
      }
    }

    const durationMs = Date.now() - startTime;

    return {
      success: true,
      sessionId: this.sessionId ?? "",
      phase: "complete",
      iteration: 1,
      tasksCompleted: 0,
      tasksRemaining: 0,
      gatesPassed,
      durationMs,
      costUsd: 0.0,
      message:
        "SDK simulation complete. Install @anthropic-ai/claude-agent-sdk for full functionality.",
    };
  }

  /**
   * Plan a task without executing (plan mode).
   *
   * @param task - The task description to plan
   * @returns The generated plan as a string
   */
  async plan(task: string): Promise<string> {
    // In a real implementation, this would use the Claude Agent SDK
    // with permissionMode="plan"
    return `Plan for: ${task}\n\nNote: Install @anthropic-ai/claude-agent-sdk for full planning functionality.`;
  }

  /**
   * Resume the last session.
   *
   * @yields LoopResult for each phase/iteration
   */
  async *resume(): AsyncGenerator<LoopResult> {
    const sessionId = this.sessionManager.loadSessionId();
    if (!sessionId) {
      throw new Error("No session to resume");
    }

    const state = this.sessionManager.load();
    if (!state) {
      throw new Error("Session state not found");
    }

    yield* this.loop(state.task, { resume: true });
  }

  /** Get the current session state */
  getSessionState(): SessionState | null {
    return this.sessionManager.load();
  }

  /** Get quality gate results */
  getGateResults(): {
    total: number;
    passed: number;
    failed: number;
    skipped: number;
    allBlockingPassed: boolean;
    gates: Record<string, string>;
  } | null {
    return this.gates?.getSummary() ?? null;
  }

  // Note: The following methods are reserved for future Claude Agent SDK integration:
  // - buildLoopPrompt(task: string): Build system prompt with profile context
  // - createHooks(): Create hooks for quality gates and state tracking
  // - defineAgents(): Define subagents for specialized tasks (explore, test-runner, lint-fixer)
  // These will be implemented when @anthropic-ai/claude-agent-sdk is available.
}

export type { LoopResult, ClaudeSentientOptions, LoopOptions };
