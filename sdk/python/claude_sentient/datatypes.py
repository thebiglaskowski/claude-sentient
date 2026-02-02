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
