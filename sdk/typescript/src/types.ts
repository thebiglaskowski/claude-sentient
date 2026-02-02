/**
 * Type definitions for Claude Sentient SDK.
 */

/** Loop phases */
export type Phase =
  | "init"
  | "understand"
  | "plan"
  | "execute"
  | "verify"
  | "commit"
  | "evaluate"
  | "complete"
  | "error";

/** Task status values */
export type TaskStatus = "pending" | "in_progress" | "completed" | "blocked";

/** Quality gate status values */
export type GateStatus = "pending" | "passed" | "failed" | "skipped";

/** A work item in the task queue */
export interface Task {
  id: string;
  subject: string;
  description: string;
  status: TaskStatus;
  blockedBy: string[];
  blocks: string[];
  createdAt: string;
  completedAt?: string;
  metadata: Record<string, unknown>;
}

/** Result of running a quality gate */
export interface GateResult {
  name: string;
  status: GateStatus;
  command: string;
  output: string;
  error: string;
  durationMs: number;
}

/** Result of a loop iteration */
export interface LoopResult {
  success: boolean;
  sessionId: string;
  phase: Phase;
  iteration: number;
  tasksCompleted: number;
  tasksRemaining: number;
  gatesPassed: Record<string, boolean>;
  commitHash?: string;
  durationMs: number;
  costUsd: number;
  message: string;
}

/** Event data for tool use hooks */
export interface ToolUseEvent {
  toolName: string;
  toolInput: Record<string, unknown>;
  toolUseId: string;
  result?: unknown;
  error?: string;
}

/** Context passed to hook functions */
export interface HookContext {
  sessionId: string;
  phase: Phase;
  iteration: number;
  profile: string;
  cwd: string;
  tasks: Task[];
  gates: Record<string, GateResult>;
}

/** Hook function signature */
export type HookFunction = (
  inputData: Record<string, unknown>,
  toolUseId: string,
  context: HookContext
) => Promise<Record<string, unknown>>;

/** Hook matcher configuration */
export interface HookMatcher {
  matcher?: string; // Regex pattern for tool names
  hooks: HookFunction[];
}

/** Configuration for a quality gate */
export interface GateConfig {
  command: string;
  blocking: boolean;
  timeout: number; // seconds
}

/** Project profile configuration */
export interface Profile {
  name: string;
  detectFiles: string[];
  detectExtensions: string[];
  gates: Record<string, GateConfig>;
  conventions: Record<string, unknown>;
  tools: string[];
}

/** Persistent session state */
export interface SessionState {
  sessionId: string;
  startedAt: string;
  lastUpdated: string;
  phase: Phase;
  iteration: number;
  profile: string;
  task: string;
  tasks: Task[];
  gates: Record<string, GateResult>;
  commits: string[];
  fileChanges: string[];
  metadata: Record<string, unknown>;
}

/** Agent definition for subagents */
export interface AgentDefinition {
  description: string;
  prompt: string;
  tools: string[];
  model: "haiku" | "sonnet" | "opus";
}

/** Options for ClaudeSentient constructor */
export interface ClaudeSentientOptions {
  cwd?: string;
  profile?: string;
  permissionMode?: string;
  profilesDir?: string;
}

/** Options for the loop method */
export interface LoopOptions {
  resume?: boolean;
  maxIterations?: number;
}
