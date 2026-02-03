"""Tests for Claude Sentient SDK hooks module."""

from pathlib import Path

import pytest

from claude_sentient.datatypes import HookDecision, HookResult, Phase
from claude_sentient.hooks import HookManager, HookMatcher
from claude_sentient.session import SessionManager


def is_allow_result(result) -> bool:
    """Check if result is an allow HookResult (equivalent to empty dict in old API)."""
    if isinstance(result, HookResult):
        return result.success and result.decision == HookDecision.ALLOW
    return result == {}


class TestHookMatcher:
    """Tests for HookMatcher dataclass."""

    def test_hook_matcher_creation(self):
        """HookMatcher should be created with default values."""
        matcher = HookMatcher()
        assert matcher.matcher is None
        assert matcher.hooks == []

    def test_hook_matcher_with_pattern(self):
        """HookMatcher should accept a pattern string."""
        async def dummy_hook(input_data, tool_use_id, context):
            return {}

        matcher = HookMatcher(matcher="Write|Edit", hooks=[dummy_hook])
        assert matcher.matcher == "Write|Edit"
        assert len(matcher.hooks) == 1

    def test_hook_matcher_with_multiple_hooks(self):
        """HookMatcher should accept multiple hooks."""
        async def hook1(input_data, tool_use_id, context):
            return {}

        async def hook2(input_data, tool_use_id, context):
            return {}

        matcher = HookMatcher(matcher="Bash", hooks=[hook1, hook2])
        assert len(matcher.hooks) == 2


class TestHookManager:
    """Tests for HookManager class."""

    def test_init_creates_default_events(self):
        """HookManager should initialize with default event types."""
        manager = HookManager()
        hooks = manager.get_hooks()

        assert "PreToolUse" in hooks
        assert "PostToolUse" in hooks
        assert "Stop" in hooks

    def test_init_with_session_manager(self, temp_dir: Path):
        """HookManager should accept a session manager."""
        session_mgr = SessionManager(state_dir=temp_dir)
        manager = HookManager(session_manager=session_mgr)

        assert manager.session_manager is session_mgr

    def test_init_creates_session_manager_if_not_provided(self):
        """HookManager should create its own session manager if not provided."""
        manager = HookManager()
        assert manager.session_manager is not None

    def test_add_hook_to_existing_event(self):
        """add_hook should add a hook to an existing event."""
        manager = HookManager()

        async def my_hook(input_data, tool_use_id, context):
            return {"test": True}

        manager.add_hook("PreToolUse", my_hook)
        hooks = manager.get_hooks()

        assert len(hooks["PreToolUse"]) == 1
        assert hooks["PreToolUse"][0].hooks[0] is my_hook

    def test_add_hook_with_matcher(self):
        """add_hook should accept a matcher pattern."""
        manager = HookManager()

        async def my_hook(input_data, tool_use_id, context):
            return {}

        manager.add_hook("PostToolUse", my_hook, matcher="Write")
        hooks = manager.get_hooks()

        assert hooks["PostToolUse"][0].matcher == "Write"

    def test_add_hook_to_new_event(self):
        """add_hook should create a new event if it doesn't exist."""
        manager = HookManager()

        async def my_hook(input_data, tool_use_id, context):
            return {}

        manager.add_hook("CustomEvent", my_hook)
        hooks = manager.get_hooks()

        assert "CustomEvent" in hooks
        assert len(hooks["CustomEvent"]) == 1

    def test_add_multiple_hooks_to_same_event(self):
        """Multiple hooks can be added to the same event."""
        manager = HookManager()

        async def hook1(input_data, tool_use_id, context):
            return {}

        async def hook2(input_data, tool_use_id, context):
            return {}

        manager.add_hook("PreToolUse", hook1)
        manager.add_hook("PreToolUse", hook2)
        hooks = manager.get_hooks()

        assert len(hooks["PreToolUse"]) == 2

    def test_get_hooks_returns_copy(self):
        """get_hooks should return the actual hooks dict."""
        manager = HookManager()
        hooks1 = manager.get_hooks()
        hooks2 = manager.get_hooks()

        # Both should reference the same internal dict
        assert hooks1 is hooks2


class TestHookManagerBuiltInHooks:
    """Tests for HookManager built-in hooks."""

    @pytest.mark.asyncio
    async def test_track_file_changes_ignores_non_post_tool_use(self, temp_dir: Path):
        """track_file_changes should ignore non-PostToolUse events."""
        session_mgr = SessionManager(state_dir=temp_dir)
        manager = HookManager(session_manager=session_mgr)

        input_data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Write",
            "tool_input": {"file_path": "/test/file.py"},
        }

        result = await manager.track_file_changes(input_data, "tool-123", None)
        assert is_allow_result(result)

    @pytest.mark.asyncio
    async def test_track_file_changes_ignores_non_file_tools(self, temp_dir: Path):
        """track_file_changes should ignore non-Write/Edit tools."""
        session_mgr = SessionManager(state_dir=temp_dir)
        manager = HookManager(session_manager=session_mgr)

        input_data = {
            "hook_event_name": "PostToolUse",
            "tool_name": "Bash",
            "tool_input": {"command": "ls"},
        }

        result = await manager.track_file_changes(input_data, "tool-123", None)
        assert is_allow_result(result)

    @pytest.mark.asyncio
    async def test_track_file_changes_tracks_write(self, temp_dir: Path):
        """track_file_changes should track Write tool usage."""
        session_mgr = SessionManager(state_dir=temp_dir)
        session_mgr.create(session_id="test", profile="python", task="test task")
        manager = HookManager(session_manager=session_mgr)

        input_data = {
            "hook_event_name": "PostToolUse",
            "tool_name": "Write",
            "tool_input": {"file_path": "/test/file.py"},
        }

        result = await manager.track_file_changes(input_data, "tool-123", None)
        assert is_allow_result(result)

        # Verify file was tracked
        state = session_mgr.load()
        assert "/test/file.py" in state.file_changes

    @pytest.mark.asyncio
    async def test_track_file_changes_tracks_edit(self, temp_dir: Path):
        """track_file_changes should track Edit tool usage."""
        session_mgr = SessionManager(state_dir=temp_dir)
        session_mgr.create(session_id="test", profile="python", task="test task")
        manager = HookManager(session_manager=session_mgr)

        input_data = {
            "hook_event_name": "PostToolUse",
            "tool_name": "Edit",
            "tool_input": {"file_path": "/test/edited.py"},
        }

        result = await manager.track_file_changes(input_data, "tool-123", None)
        assert is_allow_result(result)

        state = session_mgr.load()
        assert "/test/edited.py" in state.file_changes

    @pytest.mark.asyncio
    async def test_track_commands_ignores_non_post_tool_use(self, temp_dir: Path):
        """track_commands should ignore non-PostToolUse events."""
        session_mgr = SessionManager(state_dir=temp_dir)
        manager = HookManager(session_manager=session_mgr)

        input_data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Bash",
            "tool_input": {"command": "git commit -m 'test'"},
        }

        result = await manager.track_commands(input_data, "tool-123", None)
        assert is_allow_result(result)

    @pytest.mark.asyncio
    async def test_track_commands_ignores_non_bash(self, temp_dir: Path):
        """track_commands should ignore non-Bash tools."""
        session_mgr = SessionManager(state_dir=temp_dir)
        manager = HookManager(session_manager=session_mgr)

        input_data = {
            "hook_event_name": "PostToolUse",
            "tool_name": "Write",
            "tool_input": {"file_path": "/test.py"},
        }

        result = await manager.track_commands(input_data, "tool-123", None)
        assert is_allow_result(result)

    @pytest.mark.asyncio
    async def test_track_commands_tracks_git_commit(self, temp_dir: Path):
        """track_commands should track git commit hashes."""
        session_mgr = SessionManager(state_dir=temp_dir)
        session_mgr.create(session_id="test", profile="python", task="test task")
        manager = HookManager(session_manager=session_mgr)

        input_data = {
            "hook_event_name": "PostToolUse",
            "tool_name": "Bash",
            "tool_input": {"command": "git commit -m 'test'"},
            "result": "[main abc1234] test commit",
        }

        result = await manager.track_commands(input_data, "tool-123", None)
        assert is_allow_result(result)

        state = session_mgr.load()
        assert "abc1234" in state.commits

    @pytest.mark.asyncio
    async def test_track_commands_handles_missing_hash(self, temp_dir: Path):
        """track_commands should handle commit output without hash."""
        session_mgr = SessionManager(state_dir=temp_dir)
        session_mgr.create(session_id="test", profile="python", task="test task")
        manager = HookManager(session_manager=session_mgr)

        input_data = {
            "hook_event_name": "PostToolUse",
            "tool_name": "Bash",
            "tool_input": {"command": "git commit -m 'test'"},
            "result": "No changes to commit",
        }

        result = await manager.track_commands(input_data, "tool-123", None)
        assert is_allow_result(result)

        state = session_mgr.load()
        assert len(state.commits) == 0

    @pytest.mark.asyncio
    async def test_save_final_state_ignores_non_stop(self, temp_dir: Path):
        """save_final_state should ignore non-Stop events."""
        session_mgr = SessionManager(state_dir=temp_dir)
        manager = HookManager(session_manager=session_mgr)

        input_data = {"hook_event_name": "PostToolUse"}

        result = await manager.save_final_state(input_data, "tool-123", None)
        assert is_allow_result(result)

    @pytest.mark.asyncio
    async def test_save_final_state_updates_phase(self, temp_dir: Path):
        """save_final_state should set phase to complete."""
        session_mgr = SessionManager(state_dir=temp_dir)
        session_mgr.create(session_id="test", profile="python", task="test task")
        manager = HookManager(session_manager=session_mgr)

        input_data = {"hook_event_name": "Stop"}

        result = await manager.save_final_state(input_data, "tool-123", None)
        assert is_allow_result(result)

        state = session_mgr.load()
        assert state.phase == "complete"

    @pytest.mark.asyncio
    async def test_save_final_state_handles_no_session(self, temp_dir: Path):
        """save_final_state should handle missing session gracefully."""
        session_mgr = SessionManager(state_dir=temp_dir)
        manager = HookManager(session_manager=session_mgr)

        input_data = {"hook_event_name": "Stop"}

        # Should not raise even with no session
        result = await manager.save_final_state(input_data, "tool-123", None)
        assert is_allow_result(result)

    @pytest.mark.asyncio
    async def test_update_phase(self, temp_dir: Path):
        """update_phase should update session phase."""
        session_mgr = SessionManager(state_dir=temp_dir)
        session_mgr.create(session_id="test", profile="python", task="test task")
        manager = HookManager(session_manager=session_mgr)

        result = await manager.update_phase(Phase.EXECUTE, {}, "tool-123", None)
        assert is_allow_result(result)

        state = session_mgr.load()
        assert state.phase == "execute"


class TestHookManagerDefaultHooks:
    """Tests for HookManager default hooks creation."""

    def test_create_default_hooks_structure(self, temp_dir: Path):
        """create_default_hooks should return proper structure."""
        session_mgr = SessionManager(state_dir=temp_dir)
        manager = HookManager(session_manager=session_mgr)

        hooks = manager.create_default_hooks()

        assert "PostToolUse" in hooks
        assert "Stop" in hooks
        assert len(hooks["PostToolUse"]) == 2  # file changes + commands
        assert len(hooks["Stop"]) == 1  # save final state

    def test_create_default_hooks_matchers(self, temp_dir: Path):
        """create_default_hooks should have correct matchers."""
        session_mgr = SessionManager(state_dir=temp_dir)
        manager = HookManager(session_manager=session_mgr)

        hooks = manager.create_default_hooks()

        post_matchers = [h.matcher for h in hooks["PostToolUse"]]
        assert "Edit|Write" in post_matchers
        assert "Bash" in post_matchers


class TestHookManagerMergeHooks:
    """Tests for HookManager merge_hooks method."""

    def test_merge_empty_configs(self, temp_dir: Path):
        """merge_hooks should handle empty configs."""
        manager = HookManager()
        result = manager.merge_hooks({}, {})
        assert result == {}

    def test_merge_single_config(self, temp_dir: Path):
        """merge_hooks should handle single config."""
        manager = HookManager()

        async def my_hook(input_data, tool_use_id, context):
            return {}

        config = {
            "PreToolUse": [HookMatcher(matcher="Bash", hooks=[my_hook])]
        }

        result = manager.merge_hooks(config)
        assert "PreToolUse" in result
        assert len(result["PreToolUse"]) == 1

    def test_merge_multiple_configs(self, temp_dir: Path):
        """merge_hooks should merge multiple configs."""
        manager = HookManager()

        async def hook1(input_data, tool_use_id, context):
            return {}

        async def hook2(input_data, tool_use_id, context):
            return {}

        config1 = {
            "PreToolUse": [HookMatcher(matcher="Bash", hooks=[hook1])]
        }
        config2 = {
            "PreToolUse": [HookMatcher(matcher="Write", hooks=[hook2])]
        }

        result = manager.merge_hooks(config1, config2)
        assert len(result["PreToolUse"]) == 2

    def test_merge_different_events(self, temp_dir: Path):
        """merge_hooks should handle different events."""
        manager = HookManager()

        async def hook1(input_data, tool_use_id, context):
            return {}

        async def hook2(input_data, tool_use_id, context):
            return {}

        config1 = {
            "PreToolUse": [HookMatcher(hooks=[hook1])]
        }
        config2 = {
            "PostToolUse": [HookMatcher(hooks=[hook2])]
        }

        result = manager.merge_hooks(config1, config2)
        assert "PreToolUse" in result
        assert "PostToolUse" in result
        assert len(result["PreToolUse"]) == 1
        assert len(result["PostToolUse"]) == 1

    def test_merge_preserves_order(self, temp_dir: Path):
        """merge_hooks should preserve insertion order."""
        manager = HookManager()

        async def hook1(input_data, tool_use_id, context):
            return {"order": 1}

        async def hook2(input_data, tool_use_id, context):
            return {"order": 2}

        async def hook3(input_data, tool_use_id, context):
            return {"order": 3}

        config1 = {"PreToolUse": [HookMatcher(hooks=[hook1])]}
        config2 = {"PreToolUse": [HookMatcher(hooks=[hook2])]}
        config3 = {"PreToolUse": [HookMatcher(hooks=[hook3])]}

        result = manager.merge_hooks(config1, config2, config3)
        hooks = [m.hooks[0] for m in result["PreToolUse"]]
        assert hooks == [hook1, hook2, hook3]
