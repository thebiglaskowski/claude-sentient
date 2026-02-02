/**
 * Claude Sentient SDK - Autonomous Development Orchestration Layer
 *
 * This SDK provides programmatic access to Claude Sentient's capabilities:
 * - Session persistence for resuming work across terminal closures
 * - SDK-based orchestration instead of text commands
 * - Production deployment support (CI/CD, webhooks, scheduled tasks)
 *
 * @example
 * ```typescript
 * import { ClaudeSentient } from "@claude-sentient/sdk";
 *
 * async function main() {
 *   const sentient = new ClaudeSentient({ cwd: "./my-project" });
 *
 *   for await (const result of sentient.loop("Add user authentication")) {
 *     console.log(`Phase: ${result.phase}`);
 *     console.log(`Tasks completed: ${result.tasksCompleted}`);
 *
 *     if (result.success) {
 *       console.log(`Done! Commit: ${result.commitHash}`);
 *     }
 *   }
 * }
 * ```
 *
 * @packageDocumentation
 */

export { ClaudeSentient } from "./orchestrator";
export type {
  LoopResult,
  ClaudeSentientOptions,
  LoopOptions,
} from "./orchestrator";

export { SessionManager } from "./session";
export type { SessionState } from "./session";

export { ProfileLoader } from "./profiles";
export type { Profile, GateConfig } from "./profiles";

export { QualityGates, createGateHooks } from "./gates";
export type { GateResult } from "./gates";

export { HookManager } from "./hooks";
export type { HookFunction, HookMatcher } from "./hooks";

export type {
  Phase,
  TaskStatus,
  GateStatus,
  Task,
  ToolUseEvent,
  HookContext,
  AgentDefinition,
} from "./types";

/** SDK version */
export const VERSION = "0.3.0";
