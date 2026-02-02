"""Tests for Claude Sentient SDK types."""

import pytest
from claude_sentient.types import (
    Phase,
    TaskStatus,
    GateStatus,
    Task,
    GateResult,
    ToolUseEvent,
    HookContext,
)


class TestPhaseEnum:
    """Tests for Phase enum."""

    def test_phase_values(self):
        """Phase enum should have expected values."""
        assert Phase.INIT.value == "init"
        assert Phase.UNDERSTAND.value == "understand"
        assert Phase.PLAN.value == "plan"
        assert Phase.EXECUTE.value == "execute"
        assert Phase.VERIFY.value == "verify"
        assert Phase.COMMIT.value == "commit"
        assert Phase.EVALUATE.value == "evaluate"

    def test_phase_count(self):
        """Phase enum should have 7 phases."""
        assert len(Phase) == 7

    def test_phase_is_string_enum(self):
        """Phase should be a string enum for JSON serialization."""
        assert isinstance(Phase.INIT, str)
        assert Phase.INIT == "init"


class TestTaskStatusEnum:
    """Tests for TaskStatus enum."""

    def test_task_status_values(self):
        """TaskStatus enum should have expected values."""
        assert TaskStatus.PENDING.value == "pending"
        assert TaskStatus.IN_PROGRESS.value == "in_progress"
        assert TaskStatus.COMPLETED.value == "completed"
        assert TaskStatus.BLOCKED.value == "blocked"

    def test_task_status_count(self):
        """TaskStatus enum should have 4 statuses."""
        assert len(TaskStatus) == 4


class TestGateStatusEnum:
    """Tests for GateStatus enum."""

    def test_gate_status_values(self):
        """GateStatus enum should have expected values."""
        assert GateStatus.PENDING.value == "pending"
        assert GateStatus.PASSED.value == "passed"
        assert GateStatus.FAILED.value == "failed"
        assert GateStatus.SKIPPED.value == "skipped"

    def test_gate_status_count(self):
        """GateStatus enum should have 4 statuses."""
        assert len(GateStatus) == 4


class TestTaskDataclass:
    """Tests for Task dataclass."""

    def test_task_creation(self):
        """Task should be created with required fields."""
        task = Task(
            id="task-1",
            subject="Test task",
            description="A test task",
        )
        assert task.id == "task-1"
        assert task.subject == "Test task"
        assert task.description == "A test task"
        assert task.status == TaskStatus.PENDING
        assert task.blocked_by == []
        assert task.blocks == []

    def test_task_with_status(self):
        """Task should accept custom status."""
        task = Task(
            id="task-2",
            subject="In progress task",
            description="Working on it",
            status=TaskStatus.IN_PROGRESS,
        )
        assert task.status == TaskStatus.IN_PROGRESS

    def test_task_with_dependencies(self):
        """Task should track blocked_by dependencies."""
        task = Task(
            id="task-3",
            subject="Blocked task",
            description="Waiting for others",
            status=TaskStatus.BLOCKED,
            blocked_by=["task-1", "task-2"],
        )
        assert task.blocked_by == ["task-1", "task-2"]

    def test_task_has_created_at(self):
        """Task should have created_at timestamp."""
        task = Task(id="t1", subject="Test", description="Desc")
        assert task.created_at is not None
        assert isinstance(task.created_at, str)


class TestGateResultDataclass:
    """Tests for GateResult dataclass."""

    def test_gate_result_passed(self):
        """GateResult should track passed gates."""
        result = GateResult(
            name="lint",
            status=GateStatus.PASSED,
            command="ruff check .",
            output="All checks passed!",
            duration_ms=150.5,
        )
        assert result.name == "lint"
        assert result.status == GateStatus.PASSED
        assert result.command == "ruff check ."
        assert result.output == "All checks passed!"
        assert result.error == ""
        assert result.duration_ms == 150.5

    def test_gate_result_failed(self):
        """GateResult should track failed gates with error."""
        result = GateResult(
            name="test",
            status=GateStatus.FAILED,
            command="pytest",
            output="",
            error="2 tests failed",
            duration_ms=5000.0,
        )
        assert result.status == GateStatus.FAILED
        assert result.error == "2 tests failed"

    def test_gate_result_skipped(self):
        """GateResult should track skipped gates."""
        result = GateResult(
            name="build",
            status=GateStatus.SKIPPED,
            command="",
            output="Gate not configured",
        )
        assert result.status == GateStatus.SKIPPED


class TestToolUseEventDataclass:
    """Tests for ToolUseEvent dataclass."""

    def test_tool_use_event_creation(self):
        """ToolUseEvent should capture tool invocation details."""
        event = ToolUseEvent(
            tool_name="Read",
            tool_input={"file_path": "/tmp/test.py"},
            tool_use_id="tu-123",
        )
        assert event.tool_use_id == "tu-123"
        assert event.tool_name == "Read"
        assert event.tool_input == {"file_path": "/tmp/test.py"}
        assert event.result is None
        assert event.error is None

    def test_tool_use_event_with_result(self):
        """ToolUseEvent should store result."""
        event = ToolUseEvent(
            tool_name="Bash",
            tool_input={"command": "echo hello"},
            tool_use_id="tu-456",
            result="hello\n",
        )
        assert event.result == "hello\n"


class TestHookContextDataclass:
    """Tests for HookContext dataclass."""

    def test_hook_context_creation(self):
        """HookContext should hold context for hooks."""
        context = HookContext(
            session_id="sess-123",
            phase=Phase.EXECUTE,
            iteration=2,
            profile="python",
            cwd="/projects/myapp",
            tasks=[],
            gates={},
        )
        assert context.session_id == "sess-123"
        assert context.phase == Phase.EXECUTE
        assert context.iteration == 2
        assert context.profile == "python"
        assert context.cwd == "/projects/myapp"
        assert context.tasks == []
        assert context.gates == {}
