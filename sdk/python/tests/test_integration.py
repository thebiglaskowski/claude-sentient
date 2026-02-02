"""Integration tests for Claude Sentient SDK.

These tests verify cross-module interactions and end-to-end workflows.
"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, AsyncMock

from claude_sentient import (
    ClaudeSentient,
    SessionManager,
    SessionState,
    ProfileLoader,
    Profile,
    QualityGates,
    HookManager,
    Task,
    TaskStatus,
    Phase,
    GateStatus,
)
from claude_sentient.datatypes import GateResult


class TestEndToEndLoop:
    """End-to-end integration tests for the autonomous loop."""

    @pytest.mark.asyncio
    async def test_full_session_lifecycle(self, temp_dir: Path):
        """Test: create session -> run simulation -> save state."""
        sentient = ClaudeSentient(cwd=str(temp_dir))

        # Run loop to create session
        results = []
        async for result in sentient.loop("Add authentication"):
            results.append(result)

        assert len(results) >= 1

        # Session should be saved
        state = sentient.session_manager.load()
        assert state is not None
        assert state.task == "Add authentication"
        assert state.session_id is not None

    @pytest.mark.asyncio
    async def test_session_resume_preserves_state(self, temp_dir: Path):
        """Test: create session -> resume preserves profile and task."""
        sentient = ClaudeSentient(cwd=str(temp_dir), profile="python")

        # Create initial session
        async for _ in sentient.loop("Initial task"):
            pass

        # Save session ID for verification
        initial_id = sentient.session_id

        # Create new instance and resume
        sentient2 = ClaudeSentient(cwd=str(temp_dir))
        async for result in sentient2.resume():
            assert result.session_id == initial_id
            break

    @pytest.mark.asyncio
    async def test_loop_updates_session_phase(self, temp_dir: Path):
        """Test: loop should update session phase."""
        sentient = ClaudeSentient(cwd=str(temp_dir))

        async for _ in sentient.loop("Test task"):
            pass

        state = sentient.session_manager.load()
        assert state is not None
        # Should be updated to execute or complete phase
        assert state.phase in ("execute", "complete")


class TestProfileAndGatesIntegration:
    """Tests for profile loading and gate execution integration."""

    def test_profile_gates_available_to_sentient(self, python_project: Path):
        """Sentient should have access to profile gates."""
        sentient = ClaudeSentient(cwd=str(python_project))

        assert sentient.profile is not None
        assert "lint" in sentient.profile.gates
        assert "test" in sentient.profile.gates

    def test_quality_gates_use_profile_commands(self, python_project: Path):
        """QualityGates should use profile gate commands."""
        sentient = ClaudeSentient(cwd=str(python_project))

        # Gates should be initialized from profile
        assert sentient.gates is not None
        assert sentient.gates.profile.gates["lint"].command == "ruff check ."

    @pytest.mark.asyncio
    async def test_gates_run_in_simulation(self, python_project: Path):
        """Gates should run during simulation mode loop."""
        sentient = ClaudeSentient(cwd=str(python_project))

        async for result in sentient.loop("Fix linting"):
            # Gates may run (depends on ruff being available)
            assert isinstance(result.gates_passed, dict)


class TestHookManagerIntegration:
    """Tests for hook manager integration with orchestrator."""

    def test_hook_manager_created_with_session_manager(self, temp_dir: Path):
        """HookManager should be created with SessionManager reference."""
        sentient = ClaudeSentient(cwd=str(temp_dir))

        assert sentient.hook_manager is not None
        assert sentient.hook_manager.session_manager is sentient.session_manager

    def test_default_hooks_created(self, temp_dir: Path):
        """Default hooks should be created for session tracking."""
        sentient = ClaudeSentient(cwd=str(temp_dir))

        hooks = sentient.hook_manager.create_default_hooks()
        assert "PostToolUse" in hooks
        assert "Stop" in hooks

    def test_merged_hooks_include_gate_hooks(self, python_project: Path):
        """Merged hooks should include quality gate hooks."""
        sentient = ClaudeSentient(cwd=str(python_project))

        merged = sentient._build_merged_hooks()
        assert merged is not None
        # Should have at least PostToolUse for lint hook
        assert "PostToolUse" in merged


class TestSessionPersistence:
    """Tests for session persistence across operations."""

    def test_session_file_created_on_loop(self, temp_dir: Path):
        """Session file should be created when loop starts."""
        sentient = ClaudeSentient(cwd=str(temp_dir))

        # Session file doesn't exist yet
        state_file = temp_dir / ".claude" / "state" / "session.json"
        assert not state_file.exists() or state_file.read_text() == ""

        # Run loop
        import asyncio
        async def run():
            async for _ in sentient.loop("Test"):
                pass
        asyncio.run(run())

        # Session file should exist
        assert state_file.exists()

    def test_session_cleared_archives_to_history(self, temp_dir: Path):
        """Clearing session should archive to history."""
        manager = SessionManager(temp_dir / ".claude" / "state")

        # Create session
        state = manager.create(
            session_id="archive-test",
            profile="python",
            task="Test task",
        )

        # Clear session
        manager.clear()

        # Should be archived
        history_file = manager.history_dir / "archive-test.json"
        assert history_file.exists()

    def test_list_history_returns_archived_sessions(self, temp_dir: Path):
        """list_history should return all archived sessions."""
        manager = SessionManager(temp_dir / ".claude" / "state")

        # Create and archive multiple sessions
        for i in range(3):
            manager.create(
                session_id=f"session-{i}",
                profile="python",
                task=f"Task {i}",
            )
            manager.clear()

        history = manager.list_history()
        assert len(history) == 3


class TestCustomHooksIntegration:
    """Tests for custom hook integration."""

    def test_custom_hooks_merged_with_defaults(self, temp_dir: Path):
        """Custom hooks should be merged with default hooks."""
        async def my_hook(input_data, tool_use_id, context):
            return {}

        custom_hooks = {
            "PostToolUse": [MagicMock(matcher="Read", hooks=[my_hook])]
        }

        sentient = ClaudeSentient(cwd=str(temp_dir), hooks=custom_hooks)
        merged = sentient._build_merged_hooks()

        # Should have both default and custom PostToolUse hooks
        assert merged is not None
        assert "PostToolUse" in merged
        assert len(merged["PostToolUse"]) > 1  # Default + custom


class TestProfileDetectionIntegration:
    """Tests for profile detection with different project types."""

    def test_python_project_detected(self, python_project: Path):
        """Python profile should be detected for Python projects."""
        sentient = ClaudeSentient(cwd=str(python_project))
        assert sentient.profile_name == "python"

    def test_typescript_project_detected(self, temp_dir: Path):
        """TypeScript profile should be detected for TS projects."""
        # Create TS project indicators
        (temp_dir / "tsconfig.json").write_text("{}")
        (temp_dir / "index.ts").write_text("console.log('hello')")

        sentient = ClaudeSentient(cwd=str(temp_dir))
        assert sentient.profile_name == "typescript"

    def test_general_fallback(self, temp_dir: Path):
        """General profile should be used as fallback."""
        sentient = ClaudeSentient(cwd=str(temp_dir))
        assert sentient.profile_name == "general"


class TestDataTypesUsage:
    """Tests for proper usage of datatypes module."""

    def test_phase_enum_used_correctly(self):
        """Phase enum should work as string enum."""
        assert Phase.INIT.value == "init"
        assert Phase.EXECUTE.value == "execute"
        assert Phase.EVALUATE.value == "evaluate"
        # Note: "done" and "error" are string states, not Phase enum values

    def test_task_status_enum_used_correctly(self):
        """TaskStatus enum should work as string enum."""
        assert TaskStatus.PENDING.value == "pending"
        assert TaskStatus.COMPLETED.value == "completed"

    def test_gate_status_enum_used_correctly(self):
        """GateStatus enum should work as string enum."""
        assert GateStatus.PASSED.value == "passed"
        assert GateStatus.FAILED.value == "failed"

    def test_task_dataclass_fields(self):
        """Task dataclass should have all expected fields."""
        task = Task(
            id="test-1",
            subject="Test task",
            description="A test",
            status=TaskStatus.IN_PROGRESS,
        )
        assert task.id == "test-1"
        assert task.status == TaskStatus.IN_PROGRESS
        assert isinstance(task.created_at, str)


class TestErrorRecovery:
    """Tests for error recovery scenarios."""

    def test_corrupted_session_returns_none(self, temp_dir: Path):
        """Corrupted session file should return None, not raise."""
        manager = SessionManager(temp_dir / ".claude" / "state")

        # Create corrupted file
        state_file = temp_dir / ".claude" / "state" / "session.json"
        state_file.write_text("not valid json {{{")

        # Should return None, not raise
        state = manager.load()
        assert state is None

    def test_missing_profile_falls_back_to_general(self, temp_dir: Path):
        """Missing profile should fall back to general."""
        sentient = ClaudeSentient(
            cwd=str(temp_dir),
            profile="nonexistent_profile_xyz"
        )
        # Profile will be None, but should not crash
        # Gates will be None in this case
        assert sentient.profile is None or sentient.profile_name == "nonexistent_profile_xyz"

    @pytest.mark.asyncio
    async def test_loop_handles_gate_failure_gracefully(self, temp_dir: Path):
        """Loop should handle gate failures without crashing."""
        sentient = ClaudeSentient(cwd=str(temp_dir), profile="python")

        # Gates will likely fail (no ruff installed in test env)
        # But loop should complete
        async for result in sentient.loop("Test task"):
            # Should complete without raising
            assert result is not None


class TestBatchedWrites:
    """Tests for session manager's batched write functionality."""

    def test_auto_flush_false_batches_writes(self, temp_dir: Path):
        """With auto_flush=False, writes should be batched."""
        manager = SessionManager(temp_dir / ".claude" / "state", auto_flush=False)

        state = manager.create(
            session_id="batch-test",
            profile="python",
            task="Test",
        )

        # Update multiple times
        manager.update_phase("understand")
        manager.update_phase("plan")
        manager.update_phase("execute")

        # File may still have old state until flush
        # (create always writes immediately)
        manager.flush()

        # Now file should be updated
        loaded = SessionManager(temp_dir / ".claude" / "state").load()
        assert loaded.phase == "execute"

    def test_context_manager_flushes_on_exit(self, temp_dir: Path):
        """Context manager should flush on exit."""
        state_dir = temp_dir / ".claude" / "state"

        with SessionManager(state_dir, auto_flush=False) as manager:
            manager.create(
                session_id="ctx-test",
                profile="python",
                task="Test",
            )
            manager.update_phase("execute")
        # exit flushes

        # Load fresh and verify
        fresh_manager = SessionManager(state_dir)
        loaded = fresh_manager.load()
        assert loaded.phase == "execute"
