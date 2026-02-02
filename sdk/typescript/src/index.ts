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

export { ClaudeSentient } from "./orchestrator.js";
export type {
  LoopResult,
  ClaudeSentientOptions,
  LoopOptions,
} from "./orchestrator.js";

export { SessionManager } from "./session.js";
export type { SessionState } from "./session.js";

export { ProfileLoader } from "./profiles.js";
export type { Profile, GateConfig } from "./profiles.js";

export { QualityGates, createGateHooks } from "./gates.js";
export type { GateResult } from "./gates.js";

export { HookManager } from "./hooks.js";
export type { HookFunction, HookMatcher } from "./hooks.js";

export type {
  Phase,
  TaskStatus,
  GateStatus,
  Task,
  ToolUseEvent,
  HookContext,
  AgentDefinition,
} from "./types.js";

/** SDK version */
export const VERSION = "0.3.0";
