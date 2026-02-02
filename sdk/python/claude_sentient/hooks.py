"""Custom hook definitions for Claude Sentient SDK."""

from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Any

from .datatypes import Phase
from .session import SessionManager

# Type alias for hook functions
HookFunction = Callable[
    [dict[str, Any], str, Any],
    Awaitable[dict[str, Any]]
]


@dataclass
class HookMatcher:
    """Matcher configuration for hooks."""

    matcher: str | None = None  # Regex pattern for tool names
    hooks: list[HookFunction] = field(default_factory=list)


class HookManager:
    """Manage custom hooks for the SDK."""

    def __init__(self, session_manager: SessionManager | None = None):
        self.session_manager = session_manager or SessionManager()
        self._custom_hooks: dict[str, list[HookMatcher]] = {
            "PreToolUse": [],
            "PostToolUse": [],
            "Stop": [],
        }

    def add_hook(
        self,
        event: str,
        hook: HookFunction,
        matcher: str | None = None,
    ) -> None:
        """Add a custom hook."""
        if event not in self._custom_hooks:
            self._custom_hooks[event] = []

        self._custom_hooks[event].append(HookMatcher(matcher=matcher, hooks=[hook]))

    def get_hooks(self) -> dict[str, list[HookMatcher]]:
        """Get all registered hooks."""
        return self._custom_hooks

    # Built-in hooks for session tracking

    async def track_file_changes(
        self,
        input_data: dict[str, Any],
        tool_use_id: str,
        context: Any,
    ) -> dict[str, Any]:
        """Track file changes for session state."""
        if input_data.get("hook_event_name") != "PostToolUse":
            return {}

        tool_name = input_data.get("tool_name")
        if tool_name not in ["Write", "Edit"]:
            return {}

        file_path = input_data.get("tool_input", {}).get("file_path")
        if file_path:
            self.session_manager.add_file_change(file_path)

        return {}

    async def track_commands(
        self,
        input_data: dict[str, Any],
        tool_use_id: str,
        context: Any,
    ) -> dict[str, Any]:
        """Track bash commands for session state."""
        if input_data.get("hook_event_name") != "PostToolUse":
            return {}

        if input_data.get("tool_name") != "Bash":
            return {}

        command = input_data.get("tool_input", {}).get("command", "")

        # Track git commits
        if "git commit" in command:
            # Extract commit hash from result if available
            result = input_data.get("result", "")
            if isinstance(result, str) and "commit" in result.lower():
                # Try to extract short hash from output
                import re
                match = re.search(r"\b([0-9a-f]{7,40})\b", result)
                if match:
                    self.session_manager.add_commit(match.group(1))

        return {}

    async def save_final_state(
        self,
        input_data: dict[str, Any],
        tool_use_id: str,
        context: Any,
    ) -> dict[str, Any]:
        """Save final session state on Stop."""
        if input_data.get("hook_event_name") != "Stop":
            return {}

        state = self.session_manager.load()
        if state:
            state.phase = "complete"
            self.session_manager.save(state)

        return {}

    async def update_phase(
        self,
        phase: Phase,
        input_data: dict[str, Any],
        tool_use_id: str,
        context: Any,
    ) -> dict[str, Any]:
        """Update session phase."""
        self.session_manager.update_phase(phase.value)
        return {}

    def create_default_hooks(self) -> dict[str, list[HookMatcher]]:
        """Create the default set of hooks for session tracking."""
        return {
            "PostToolUse": [
                HookMatcher(
                    matcher="Edit|Write",
                    hooks=[self.track_file_changes],
                ),
                HookMatcher(
                    matcher="Bash",
                    hooks=[self.track_commands],
                ),
            ],
            "Stop": [
                HookMatcher(
                    hooks=[self.save_final_state],
                ),
            ],
        }

    def merge_hooks(
        self,
        *hook_configs: dict[str, list[HookMatcher]],
    ) -> dict[str, list[HookMatcher]]:
        """Merge multiple hook configurations."""
        merged: dict[str, list[HookMatcher]] = {}

        for config in hook_configs:
            for event, matchers in config.items():
                if event not in merged:
                    merged[event] = []
                merged[event].extend(matchers)

        return merged
