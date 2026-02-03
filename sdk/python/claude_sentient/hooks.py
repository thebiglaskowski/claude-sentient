"""Custom hook definitions for Claude Sentient SDK."""

import re
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .datatypes import (
    CostTracking,
    HookDecision,
    HookEvent,
    HookResult,
    HookType,
    Phase,
    SubagentInfo,
)
from .session import SessionManager

# Type alias for hook functions
HookFunction = Callable[
    [dict[str, Any], str, Any],
    Awaitable[HookResult]
]


@dataclass
class HookMatcher:
    """Matcher configuration for hooks."""

    matcher: str | None = None  # Regex pattern for tool names
    hooks: list[HookFunction] = field(default_factory=list)
    hook_type: HookType = HookType.COMMAND
    run_in_background: bool = False
    timeout: int = 5000  # milliseconds


@dataclass
class HookConfig:
    """Complete hook configuration."""

    event: HookEvent
    matchers: list[HookMatcher] = field(default_factory=list)
    enabled: bool = True


class HookManager:
    """Manage custom hooks for the SDK."""

    def __init__(self, session_manager: SessionManager | None = None):
        self.session_manager = session_manager or SessionManager()
        self._custom_hooks: dict[str, list[HookMatcher]] = {
            event.value: [] for event in HookEvent
        }
        self._active_agents: dict[str, SubagentInfo] = {}
        self._agent_history: list[SubagentInfo] = []
        self._cost_tracking: CostTracking = CostTracking()

    def add_hook(
        self,
        event: str | HookEvent,
        hook: HookFunction,
        matcher: str | None = None,
        hook_type: HookType = HookType.COMMAND,
        run_in_background: bool = False,
        timeout: int = 5000,
    ) -> None:
        """Add a custom hook."""
        event_str = event.value if isinstance(event, HookEvent) else event
        if event_str not in self._custom_hooks:
            self._custom_hooks[event_str] = []

        self._custom_hooks[event_str].append(
            HookMatcher(
                matcher=matcher,
                hooks=[hook],
                hook_type=hook_type,
                run_in_background=run_in_background,
                timeout=timeout,
            )
        )

    def get_hooks(self) -> dict[str, list[HookMatcher]]:
        """Get all registered hooks."""
        return self._custom_hooks

    def get_active_agents(self) -> dict[str, SubagentInfo]:
        """Get currently active subagents."""
        return self._active_agents

    def get_agent_history(self) -> list[SubagentInfo]:
        """Get completed subagent history."""
        return self._agent_history

    def get_cost_tracking(self) -> CostTracking:
        """Get cost tracking data."""
        return self._cost_tracking

    # --- Session lifecycle hooks ---

    async def on_session_start(
        self,
        input_data: dict[str, Any],
        tool_use_id: str,
        context: Any,
    ) -> HookResult:
        """Handle SessionStart event - initialize session context."""
        session_id = f"session-{int(datetime.now().timestamp())}"

        # Get profile and git info from context if available
        profile = input_data.get("profile", "auto-detect")
        git_branch = input_data.get("git_branch", "unknown")
        cwd = input_data.get("cwd", ".")

        # Initialize session state
        state = self.session_manager.load()
        if state is None:
            from .session import SessionState
            state = SessionState(
                session_id=session_id,
                cwd=cwd,
                profile=profile,
            )
        state.name = input_data.get("session_name")
        self.session_manager.save(state)

        return HookResult(
            success=True,
            context={
                "session_id": session_id,
                "profile": profile,
                "git_branch": git_branch,
            },
            system_message=f"Session started: {session_id}",
        )

    async def on_session_end(
        self,
        input_data: dict[str, Any],
        tool_use_id: str,
        context: Any,
    ) -> HookResult:
        """Handle SessionEnd event - archive session and cleanup."""
        state = self.session_manager.load()

        if state:
            # Calculate session duration
            start_time = datetime.fromisoformat(state.started_at)
            duration_min = (datetime.now() - start_time).total_seconds() / 60

            # Archive session
            archive_data = {
                "session_id": state.session_id,
                "duration_minutes": round(duration_min, 1),
                "files_changed": len(state.file_changes),
                "commits": len(state.commits),
                "tasks_completed": state.tasks_completed,
                "cost": self._cost_tracking.total_usd,
            }

            state.phase = "archived"
            self.session_manager.save(state)

            return HookResult(
                success=True,
                context=archive_data,
                system_message=f"Session archived after {duration_min:.1f} minutes",
            )

        return HookResult(success=True)

    async def on_pre_tool_use(
        self,
        input_data: dict[str, Any],
        tool_use_id: str,
        context: Any,
    ) -> HookResult:
        """Handle PreToolUse event - validate tool execution."""
        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})

        # Bash command validation
        if tool_name == "Bash":
            return await self._validate_bash_command(tool_input.get("command", ""))

        # File operation validation
        if tool_name in ("Write", "Edit"):
            return await self._validate_file_operation(tool_input.get("file_path", ""))

        return HookResult(success=True, decision=HookDecision.ALLOW)

    async def on_post_tool_use(
        self,
        input_data: dict[str, Any],
        tool_use_id: str,
        context: Any,
    ) -> HookResult:
        """Handle PostToolUse event - track changes and suggest actions."""
        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})
        result = input_data.get("result", {})

        suggestions = []

        # Track file changes
        if tool_name in ("Write", "Edit"):
            file_path = tool_input.get("file_path", "")
            if file_path:
                self.session_manager.add_file_change(file_path)

                # Suggest lint for code files
                ext_lint_map = {
                    ".py": "ruff check",
                    ".ts": "eslint",
                    ".tsx": "eslint",
                    ".js": "eslint",
                    ".go": "golangci-lint run",
                }
                ext = file_path.rsplit(".", 1)[-1] if "." in file_path else ""
                if f".{ext}" in ext_lint_map:
                    suggestions.append(f"Consider running: {ext_lint_map[f'.{ext}']}")

        # Track git commits
        if tool_name == "Bash" and "git commit" in tool_input.get("command", ""):
            result_str = str(result)
            match = re.search(r"\b([0-9a-f]{7,40})\b", result_str)
            if match:
                self.session_manager.add_commit(match.group(1))

        return HookResult(
            success=True,
            warnings=suggestions if suggestions else [],
        )

    async def on_subagent_start(
        self,
        input_data: dict[str, Any],
        tool_use_id: str,
        context: Any,
    ) -> HookResult:
        """Handle SubagentStart event - track agent spawning."""
        agent_id = input_data.get("agent_id", f"agent-{int(datetime.now().timestamp())}")
        agent_info = SubagentInfo(
            id=agent_id,
            type=input_data.get("subagent_type", "general-purpose"),
            description=input_data.get("description", ""),
            model=input_data.get("model", "sonnet"),
            run_in_background=input_data.get("run_in_background", False),
        )

        self._active_agents[agent_id] = agent_info

        return HookResult(
            success=True,
            context={
                "agent_id": agent_id,
                "agent_type": agent_info.type,
                "active_count": len(self._active_agents),
            },
        )

    async def on_subagent_stop(
        self,
        input_data: dict[str, Any],
        tool_use_id: str,
        context: Any,
    ) -> HookResult:
        """Handle SubagentStop event - synthesize agent results."""
        agent_id = input_data.get("agent_id", "")
        success = input_data.get("success", True)
        result_summary = input_data.get("result_summary", "")

        agent_info = self._active_agents.pop(agent_id, None)

        if agent_info:
            # Update agent info
            agent_info.end_time = datetime.now().isoformat()
            agent_info.status = "completed" if success else "failed"
            agent_info.result_summary = result_summary[:500]  # Truncate

            # Calculate duration
            start = datetime.fromisoformat(agent_info.start_time)
            duration_sec = (datetime.now() - start).total_seconds()

            # Add to history
            self._agent_history.append(agent_info)
            # Keep only last 50
            if len(self._agent_history) > 50:
                self._agent_history = self._agent_history[-50:]

            return HookResult(
                success=True,
                context={
                    "agent_id": agent_id,
                    "type": agent_info.type,
                    "success": success,
                    "duration_seconds": round(duration_sec, 1),
                    "remaining_agents": len(self._active_agents),
                },
            )

        return HookResult(success=True)

    async def on_pre_compact(
        self,
        input_data: dict[str, Any],
        tool_use_id: str,
        context: Any,
    ) -> HookResult:
        """Handle PreCompact event - backup state before compaction."""
        state = self.session_manager.load()

        if state:
            # Create backup
            backup = {
                "timestamp": datetime.now().isoformat(),
                "session_id": state.session_id,
                "phase": state.phase,
                "iteration": state.iteration,
                "files_changed": state.file_changes,
                "active_agents": [a.id for a in self._active_agents.values()],
                "cost": self._cost_tracking.total_usd,
            }

            # Store backup in session state
            if not hasattr(state, "backups"):
                state.backups = []
            state.backups = (state.backups or [])[-9:]  # Keep last 10
            state.backups.append(backup)
            self.session_manager.save(state)

            return HookResult(
                success=True,
                context={"backup_created": True},
                system_message="State backed up before compaction",
            )

        return HookResult(success=True)

    async def on_stop(
        self,
        input_data: dict[str, Any],
        tool_use_id: str,
        context: Any,
    ) -> HookResult:
        """Handle Stop event - verify DoD and save state."""
        state = self.session_manager.load()

        if state:
            state.phase = "complete"
            self.session_manager.save(state)

            # Build verification summary
            verification = {
                "files_modified": len(state.file_changes),
                "commits": len(state.commits),
                "tasks_completed": state.tasks_completed,
                "cost_usd": self._cost_tracking.total_usd,
            }

            recommendations = []
            if state.file_changes and not state.commits:
                recommendations.append("Consider committing changes")

            return HookResult(
                success=True,
                context=verification,
                warnings=recommendations,
            )

        return HookResult(success=True)

    # --- Private validation methods ---

    async def _validate_bash_command(self, command: str) -> HookResult:
        """Validate a bash command for dangerous patterns."""
        dangerous_patterns = [
            # Destructive file operations
            (r"rm\s+-rf\s+[\/~]", "Recursive delete from root or home"),
            (r"rm\s+-rf\s+\*", "Recursive delete all files"),
            (r"rm\s+-rf\s+\.", "Recursive delete current directory"),
            # Disk operations
            (r">\s*\/dev\/sd", "Direct write to disk device"),
            (r"mkfs", "Filesystem creation"),
            (r"dd\s+if=.*of=\/dev", "Direct disk write with dd"),
            # Permission changes
            (r"chmod\s+-R\s+777\s+\/", "Recursive chmod 777 from root"),
            (r"chown\s+-R\s+.*\s+\/", "Recursive chown from root"),
            # System modification
            (r":\(\)\{\s*:\|:&\s*\};:", "Fork bomb"),
            (r">\s*\/dev\/null\s*2>&1\s*&\s*disown", "Background process hiding"),
            # Network attacks
            (r"nc\s+-l.*-e\s+\/bin", "Netcat reverse shell"),
            # History manipulation
            (r"history\s+-c", "Clear command history"),
            (r"shred.*\.bash_history", "Shred bash history"),
        ]

        for pattern, reason in dangerous_patterns:
            if re.search(pattern, command):
                return HookResult(
                    success=True,
                    decision=HookDecision.BLOCK,
                    reason=f"BLOCKED: {reason}",
                )

        # Check for warnings
        warning_patterns = [
            (r"sudo\s+", "Using sudo"),
            (r"curl.*\|\s*sh", "Piping curl to shell"),
            (r"wget.*\|\s*sh", "Piping wget to shell"),
            (r"npm\s+install\s+-g", "Global npm install"),
            (r"pip\s+install\s+--user", "User pip install"),
        ]

        warnings = []
        for pattern, reason in warning_patterns:
            if re.search(pattern, command):
                warnings.append(reason)

        return HookResult(
            success=True,
            decision=HookDecision.ALLOW,
            warnings=warnings,
        )

    async def _validate_file_operation(self, file_path: str) -> HookResult:
        """Validate a file operation for protected paths."""
        # Normalize path for comparison (handle Windows backslashes)
        normalized = file_path.replace("\\", "/")

        protected_patterns = [
            # System files (anchored)
            r"^/etc/",
            r"^/usr/",
            r"^/bin/",
            r"^/sbin/",
            r"^C:/Windows/",
            r"^C:/Program Files",
            # User sensitive files (can appear anywhere in path)
            r"(^|/)\.ssh/",
            r"(^|/)\.gnupg/",
            r"(^|/)\.aws/credentials$",
            r"(^|/)\.env\.production$",
            # Git internals
            r"(^|/)\.git/objects/",
            r"(^|/)\.git/refs/",
            r"(^|/)\.git/HEAD$",
        ]

        for pattern in protected_patterns:
            if re.search(pattern, normalized, re.IGNORECASE):
                return HookResult(
                    success=True,
                    decision=HookDecision.BLOCK,
                    reason=f"BLOCKED: Cannot modify protected path: {file_path}",
                )

        # Check for sensitive files (warn but allow)
        sensitive_patterns = [
            r"(^|/)\.env$",
            r"(^|/)\.env\.local$",
            r"secrets?\.",
            r"credentials?\.",
            r"password",
            r"api[_-]?key",
            r"\.pem$",
            r"\.key$",
            r"id_rsa",
            r"id_ed25519",
        ]

        warnings = []
        for pattern in sensitive_patterns:
            if re.search(pattern, file_path, re.IGNORECASE):
                warnings.append("Modifying sensitive file")
                break

        return HookResult(
            success=True,
            decision=HookDecision.ALLOW,
            warnings=warnings,
        )

    # --- Cost tracking methods ---

    def add_cost(
        self,
        amount_usd: float,
        phase: str | None = None,
        model: str | None = None,
    ) -> None:
        """Add cost to tracking."""
        self._cost_tracking.total_usd += amount_usd

        if phase:
            self._cost_tracking.by_phase[phase] = (
                self._cost_tracking.by_phase.get(phase, 0.0) + amount_usd
            )

        if model:
            self._cost_tracking.by_model[model] = (
                self._cost_tracking.by_model.get(model, 0.0) + amount_usd
            )

    def set_budget(self, budget_usd: float) -> None:
        """Set the cost budget."""
        self._cost_tracking.budget_usd = budget_usd

    # --- Built-in hooks for backward compatibility ---

    async def track_file_changes(
        self,
        input_data: dict[str, Any],
        tool_use_id: str,
        context: Any,
    ) -> HookResult:
        """Track file changes for session state (backward compatible)."""
        if input_data.get("hook_event_name") != "PostToolUse":
            return HookResult()

        tool_name = input_data.get("tool_name")
        if tool_name not in ["Write", "Edit"]:
            return HookResult()

        file_path = input_data.get("tool_input", {}).get("file_path")
        if file_path:
            self.session_manager.add_file_change(file_path)

        return HookResult()

    async def track_commands(
        self,
        input_data: dict[str, Any],
        tool_use_id: str,
        context: Any,
    ) -> HookResult:
        """Track bash commands for session state (backward compatible)."""
        if input_data.get("hook_event_name") != "PostToolUse":
            return HookResult()

        if input_data.get("tool_name") != "Bash":
            return HookResult()

        command = input_data.get("tool_input", {}).get("command", "")

        # Track git commits
        if "git commit" in command:
            result = input_data.get("result", "")
            if isinstance(result, str) and "commit" in result.lower():
                match = re.search(r"\b([0-9a-f]{7,40})\b", result)
                if match:
                    self.session_manager.add_commit(match.group(1))

        return HookResult()

    async def save_final_state(
        self,
        input_data: dict[str, Any],
        tool_use_id: str,
        context: Any,
    ) -> HookResult:
        """Save final session state on Stop (backward compatible)."""
        return await self.on_stop(input_data, tool_use_id, context)

    async def update_phase(
        self,
        phase: Phase,
        input_data: dict[str, Any],
        tool_use_id: str,
        context: Any,
    ) -> HookResult:
        """Update session phase."""
        self.session_manager.update_phase(phase.value)
        return HookResult()

    def create_default_hooks(self) -> dict[str, list[HookMatcher]]:
        """Create the default set of hooks for session tracking."""
        return {
            HookEvent.SESSION_START.value: [
                HookMatcher(hooks=[self.on_session_start]),
            ],
            HookEvent.SESSION_END.value: [
                HookMatcher(hooks=[self.on_session_end]),
            ],
            HookEvent.USER_PROMPT_SUBMIT.value: [],
            HookEvent.PRE_TOOL_USE.value: [
                HookMatcher(
                    matcher="Bash",
                    hooks=[self.on_pre_tool_use],
                ),
                HookMatcher(
                    matcher="Write|Edit",
                    hooks=[self.on_pre_tool_use],
                ),
            ],
            HookEvent.POST_TOOL_USE.value: [
                HookMatcher(
                    matcher="Edit|Write",
                    hooks=[self.on_post_tool_use],
                ),
                HookMatcher(
                    matcher="Bash",
                    hooks=[self.on_post_tool_use],
                ),
            ],
            HookEvent.SUBAGENT_START.value: [
                HookMatcher(hooks=[self.on_subagent_start]),
            ],
            HookEvent.SUBAGENT_STOP.value: [
                HookMatcher(hooks=[self.on_subagent_stop]),
            ],
            HookEvent.PRE_COMPACT.value: [
                HookMatcher(hooks=[self.on_pre_compact]),
            ],
            HookEvent.STOP.value: [
                HookMatcher(hooks=[self.on_stop]),
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


class BudgetExceededError(Exception):
    """Raised when the cost budget is exceeded."""

    def __init__(self, budget: float, actual: float):
        self.budget = budget
        self.actual = actual
        super().__init__(
            f"Budget exceeded: ${actual:.2f} spent, budget was ${budget:.2f}"
        )
