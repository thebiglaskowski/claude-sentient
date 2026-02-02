"""Type definitions for Claude Sentient SDK."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class Phase(str, Enum):
    """Loop phases."""

    INIT = "init"
    UNDERSTAND = "understand"
    PLAN = "plan"
    EXECUTE = "execute"
    VERIFY = "verify"
    COMMIT = "commit"
    EVALUATE = "evaluate"


class TaskStatus(str, Enum):
    """Task status values."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"


class GateStatus(str, Enum):
    """Quality gate status values."""

    PENDING = "pending"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


class HookType(str, Enum):
    """Hook execution types."""

    COMMAND = "command"  # Execute a shell command
    PROMPT = "prompt"  # Inject text into prompt
    AGENT = "agent"  # Spawn a subagent


class HookEvent(str, Enum):
    """Hook event types - all 11 Claude Code hook events."""

    SESSION_START = "SessionStart"
    SESSION_END = "SessionEnd"
    USER_PROMPT_SUBMIT = "UserPromptSubmit"
    PRE_TOOL_USE = "PreToolUse"
    POST_TOOL_USE = "PostToolUse"
    SUBAGENT_START = "SubagentStart"
    SUBAGENT_STOP = "SubagentStop"
    PRE_COMPACT = "PreCompact"
    STOP = "Stop"
    SETUP = "Setup"
    NOTIFICATION = "Notification"


class HookDecision(str, Enum):
    """Decision returned by PreToolUse hooks."""

    ALLOW = "allow"
    BLOCK = "block"


class ModelTier(str, Enum):
    """Model tiers for routing."""

    HAIKU = "haiku"
    SONNET = "sonnet"
    OPUS = "opus"


@dataclass
class Task:
    """A work item in the task queue."""

    id: str
    subject: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    blocked_by: list[str] = field(default_factory=list)
    blocks: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class GateResult:
    """Result of running a quality gate."""

    name: str
    status: GateStatus
    command: str
    output: str = ""
    error: str = ""
    duration_ms: float = 0.0


@dataclass
class ToolUseEvent:
    """Event data for tool use hooks."""

    tool_name: str
    tool_input: dict[str, Any]
    tool_use_id: str
    result: Any = None
    error: str | None = None


@dataclass
class HookContext:
    """Context passed to hook functions."""

    session_id: str
    phase: Phase
    iteration: int
    profile: str
    cwd: str
    tasks: list[Task]
    gates: dict[str, GateResult]


@dataclass
class SubagentInfo:
    """Information about a subagent."""

    id: str
    type: str  # Explore, Plan, general-purpose, Bash
    description: str
    model: str  # haiku, sonnet, opus
    run_in_background: bool = False
    start_time: str = field(default_factory=lambda: datetime.now().isoformat())
    end_time: str | None = None
    status: str = "running"  # running, completed, failed
    result_summary: str = ""


@dataclass
class CostTracking:
    """Cost tracking data."""

    total_usd: float = 0.0
    by_phase: dict[str, float] = field(default_factory=dict)
    by_model: dict[str, float] = field(default_factory=dict)
    budget_usd: float | None = None

    @property
    def over_budget(self) -> bool:
        """Check if cost exceeds budget."""
        if self.budget_usd is None:
            return False
        return self.total_usd > self.budget_usd

    @property
    def budget_remaining(self) -> float | None:
        """Get remaining budget if set."""
        if self.budget_usd is None:
            return None
        return max(0.0, self.budget_usd - self.total_usd)

    @property
    def budget_used_percent(self) -> float | None:
        """Get percentage of budget used."""
        if self.budget_usd is None or self.budget_usd == 0:
            return None
        return min(100.0, (self.total_usd / self.budget_usd) * 100)


@dataclass
class HookResult:
    """Result returned from a hook execution."""

    success: bool = True
    decision: HookDecision = HookDecision.ALLOW
    reason: str | None = None
    warnings: list[str] = field(default_factory=list)
    context: dict[str, Any] = field(default_factory=dict)
    system_message: str | None = None
