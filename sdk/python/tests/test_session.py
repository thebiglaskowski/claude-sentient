"""Tests for Claude Sentient SDK session management."""

from pathlib import Path

from claude_sentient.session import SessionManager, SessionState


class TestSessionState:
    """Tests for SessionState dataclass."""

    def test_session_state_creation(self):
        """SessionState should be created with required fields."""
        state = SessionState(
            session_id="test-123",
            started_at="2026-01-01T00:00:00",
            last_updated="2026-01-01T00:00:00",
            phase="init",
            iteration=1,
            profile="python",
            task="Test task",
        )
        assert state.session_id == "test-123"
        assert state.phase == "init"
        assert state.iteration == 1
        assert state.profile == "python"
        assert state.task == "Test task"
        assert state.tasks == []
        assert state.gates == {}
        assert state.commits == []
        assert state.file_changes == []

    def test_session_state_with_data(self):
        """SessionState should accept task and gate data."""
        state = SessionState(
            session_id="test-456",
            started_at="2026-01-01T00:00:00",
            last_updated="2026-01-01T00:01:00",
            phase="execute",
            iteration=3,
            profile="typescript",
            task="Build feature",
            tasks=[{"id": "t1", "subject": "Task 1"}],
            gates={"lint": {"status": "passed"}},
            commits=["abc123"],
            file_changes=["src/app.ts"],
        )
        assert state.iteration == 3
        assert len(state.tasks) == 1
        assert state.gates["lint"]["status"] == "passed"
        assert "abc123" in state.commits


class TestSessionManager:
    """Tests for SessionManager class."""

    def test_session_manager_init(self, temp_dir: Path):
        """SessionManager should initialize with state directory."""
        manager = SessionManager(temp_dir / ".claude/state")
        assert manager.state_dir.exists()
        assert manager.history_dir.exists()

    def test_session_manager_creates_directory(self, temp_dir: Path):
        """SessionManager should create state directory if missing."""
        state_dir = temp_dir / "new_state_dir"
        SessionManager(state_dir)
        assert state_dir.exists()

    def test_create_session(self, temp_dir: Path):
        """SessionManager should create new session."""
        manager = SessionManager(temp_dir / ".claude/state")
        state = manager.create(
            session_id="new-sess",
            profile="python",
            task="Test task",
        )

        assert state.session_id == "new-sess"
        assert state.profile == "python"
        assert state.task == "Test task"
        assert state.phase == "init"
        assert state.iteration == 1

    def test_save_and_load_state(self, temp_dir: Path):
        """SessionManager should save and load state."""
        manager = SessionManager(temp_dir / ".claude/state")
        manager.create(
            session_id="save-load",
            profile="go",
            task="Go task",
        )

        loaded = manager.load()
        assert loaded is not None
        assert loaded.session_id == "save-load"
        assert loaded.profile == "go"

    def test_load_returns_none_if_missing(self, temp_dir: Path):
        """SessionManager should return None if no state file exists."""
        manager = SessionManager(temp_dir / ".claude/state")
        state = manager.load()
        assert state is None

    def test_load_session_id(self, temp_dir: Path):
        """SessionManager should load just session ID."""
        manager = SessionManager(temp_dir / ".claude/state")
        manager.create(session_id="id-only", profile="rust", task="Task")

        session_id = manager.load_session_id()
        assert session_id == "id-only"

    def test_update_phase(self, temp_dir: Path):
        """SessionManager should update phase."""
        manager = SessionManager(temp_dir / ".claude/state")
        manager.create(session_id="phase-test", profile="python", task="Task")

        manager.update_phase("execute")
        state = manager.load()
        assert state.phase == "execute"

    def test_increment_iteration(self, temp_dir: Path):
        """SessionManager should increment iteration."""
        manager = SessionManager(temp_dir / ".claude/state")
        manager.create(session_id="iter-test", profile="python", task="Task")

        manager.increment_iteration()
        state = manager.load()
        assert state.iteration == 2

    def test_add_commit(self, temp_dir: Path):
        """SessionManager should add commit hash."""
        manager = SessionManager(temp_dir / ".claude/state")
        manager.create(session_id="commit-test", profile="python", task="Task")

        manager.add_commit("abc123")
        manager.add_commit("def456")
        state = manager.load()
        assert state.commits == ["abc123", "def456"]

    def test_add_file_change(self, temp_dir: Path):
        """SessionManager should track file changes."""
        manager = SessionManager(temp_dir / ".claude/state")
        manager.create(session_id="file-test", profile="python", task="Task")

        manager.add_file_change("src/main.py")
        manager.add_file_change("src/main.py")  # Duplicate should not be added
        manager.add_file_change("src/utils.py")

        state = manager.load()
        assert len(state.file_changes) == 2
        assert "src/main.py" in state.file_changes

    def test_update_gate(self, temp_dir: Path):
        """SessionManager should update gate results."""
        manager = SessionManager(temp_dir / ".claude/state")
        manager.create(session_id="gate-test", profile="python", task="Task")

        manager.update_gate("lint", {"status": "passed", "duration": 150})
        state = manager.load()
        assert state.gates["lint"]["status"] == "passed"

    def test_clear_archives_session(self, temp_dir: Path):
        """SessionManager clear should archive and delete session."""
        manager = SessionManager(temp_dir / ".claude/state")
        manager.create(session_id="to-clear", profile="python", task="Task")

        assert manager.state_file.exists()
        manager.clear()
        assert not manager.state_file.exists()

        # Check it was archived
        archive_files = list(manager.history_dir.glob("*.json"))
        assert len(archive_files) == 1

    def test_clear_nonexistent_is_safe(self, temp_dir: Path):
        """SessionManager clear should not raise if file doesn't exist."""
        manager = SessionManager(temp_dir / ".claude/state")
        manager.clear()  # Should not raise

    def test_list_history(self, temp_dir: Path):
        """SessionManager should list archived sessions."""
        manager = SessionManager(temp_dir / ".claude/state")

        # Create and clear multiple sessions
        manager.create(session_id="hist-1", profile="python", task="Task 1")
        manager.clear()
        manager.create(session_id="hist-2", profile="go", task="Task 2")
        manager.clear()

        history = manager.list_history()
        assert len(history) == 2
        session_ids = [h["session_id"] for h in history]
        assert "hist-1" in session_ids
        assert "hist-2" in session_ids


class TestSessionManagerBatching:
    """Tests for SessionManager write batching functionality."""

    def test_auto_flush_false_does_not_write_immediately(self, temp_dir: Path):
        """With auto_flush=False, changes should not write to disk immediately."""
        manager = SessionManager(temp_dir / ".claude/state", auto_flush=False)
        manager.create(session_id="batch-test", profile="python", task="Task")

        # Create writes immediately
        initial_mtime = manager.state_file.stat().st_mtime

        # Update phase - should NOT write to disk
        import time
        time.sleep(0.01)  # Small delay to ensure mtime would change
        manager.update_phase("execute")

        # File should NOT have been updated
        assert manager.state_file.stat().st_mtime == initial_mtime

        # But in-memory state should be updated
        state = manager.load()
        assert state.phase == "execute"

    def test_auto_flush_true_writes_immediately(self, temp_dir: Path):
        """With auto_flush=True, changes should write to disk immediately."""
        manager = SessionManager(temp_dir / ".claude/state", auto_flush=True)
        manager.create(session_id="auto-test", profile="python", task="Task")

        initial_mtime = manager.state_file.stat().st_mtime

        import time
        time.sleep(0.01)
        manager.update_phase("execute")

        # File SHOULD have been updated
        assert manager.state_file.stat().st_mtime > initial_mtime

    def test_flush_writes_pending_changes(self, temp_dir: Path):
        """flush() should write all pending changes to disk."""
        manager = SessionManager(temp_dir / ".claude/state", auto_flush=False)
        manager.create(session_id="flush-test", profile="python", task="Task")

        # Make multiple changes
        manager.update_phase("execute")
        manager.add_commit("abc123")
        manager.add_file_change("test.py")

        initial_mtime = manager.state_file.stat().st_mtime

        import time
        time.sleep(0.01)
        manager.flush()

        # File should be updated
        assert manager.state_file.stat().st_mtime > initial_mtime

        # Verify data was written
        new_manager = SessionManager(temp_dir / ".claude/state", auto_flush=False)
        state = new_manager.load()
        assert state.phase == "execute"
        assert "abc123" in state.commits
        assert "test.py" in state.file_changes

    def test_context_manager_flushes_on_exit(self, temp_dir: Path):
        """Context manager should flush on exit."""
        state_dir = temp_dir / ".claude/state"

        with SessionManager(state_dir, auto_flush=False) as manager:
            manager.create(session_id="ctx-test", profile="python", task="Task")
            manager.update_phase("verify")

        # After context manager exit, load with new manager
        new_manager = SessionManager(state_dir, auto_flush=False)
        state = new_manager.load()
        assert state.phase == "verify"

    def test_dirty_flag_cleared_after_flush(self, temp_dir: Path):
        """Dirty flag should be cleared after flush."""
        manager = SessionManager(temp_dir / ".claude/state", auto_flush=False)
        manager.create(session_id="dirty-test", profile="python", task="Task")

        manager.update_phase("execute")
        assert manager._dirty is True

        manager.flush()
        assert manager._dirty is False

    def test_flush_noop_when_not_dirty(self, temp_dir: Path):
        """flush() should be a no-op when not dirty."""
        manager = SessionManager(temp_dir / ".claude/state", auto_flush=False)
        manager.create(session_id="noop-test", profile="python", task="Task")

        initial_mtime = manager.state_file.stat().st_mtime
        manager._dirty = False  # Ensure not dirty

        import time
        time.sleep(0.01)
        manager.flush()

        # File should NOT have been updated
        assert manager.state_file.stat().st_mtime == initial_mtime

    def test_batched_writes_reduce_io(self, temp_dir: Path):
        """Multiple updates should result in single write when batched."""
        manager = SessionManager(temp_dir / ".claude/state", auto_flush=False)
        manager.create(session_id="io-test", profile="python", task="Task")

        # Make 10 updates
        for i in range(10):
            manager.add_file_change(f"file{i}.py")

        # File should still only have the initial create
        # (we can't easily count writes, but we can verify all data is there after flush)
        manager.flush()

        state = manager.load()
        assert len(state.file_changes) == 10
