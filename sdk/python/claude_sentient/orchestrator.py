"""Main orchestrator for Claude Sentient SDK.

This module integrates with the official Claude Agent SDK to provide
autonomous development capabilities.

See: https://platform.claude.com/docs/en/agent-sdk/overview
"""

import uuid
from collections.abc import AsyncIterator, Awaitable, Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

try:
    from claude_agent_sdk import (
        AssistantMessage,
        ClaudeAgentOptions,
        ClaudeSDKClient,
        ResultMessage,
        SystemMessage,
        TextBlock,
        ToolUseBlock,
        query,
    )
    from claude_agent_sdk.types import (
        AgentDefinition as SDKAgentDefinition,
    )
    from claude_agent_sdk.types import (
        PermissionResultAllow,
        PermissionResultDeny,
    )
    AGENT_SDK_AVAILABLE = True
except ImportError:
    AGENT_SDK_AVAILABLE = False
    # Define stubs for type hints when SDK not available
    SDKAgentDefinition = None
    PermissionResultAllow = None
    PermissionResultDeny = None

from .client import ClaudeSentientClient
from .datatypes import GateStatus
from .gates import QualityGates, create_gate_hooks
from .hooks import HookManager, HookMatcher
from .profiles import ProfileLoader
from .session import SessionManager, SessionState

# Type aliases for permission callbacks
# When Agent SDK is available, this is Union[PermissionResultAllow, PermissionResultDeny]
# When unavailable, falls back to Any for forward-compatible type hints
PermissionResult = PermissionResultAllow | PermissionResultDeny if AGENT_SDK_AVAILABLE else Any
CanUseTool = Callable[[str, dict[str, Any], Any], Awaitable[PermissionResult]]
HookCallback = Callable[[dict[str, Any], str | None, Any], Awaitable[dict[str, Any]]]


@dataclass
class LoopResult:
    """Result of a loop iteration."""

    success: bool
    session_id: str
    phase: str
    iteration: int
    tasks_completed: int
    tasks_remaining: int
    gates_passed: dict[str, bool]
    commit_hash: str | None
    duration_ms: float
    cost_usd: float
    message: str = ""


@dataclass
class AgentDefinition:
    """Definition for a subagent.

    See: https://platform.claude.com/docs/en/agent-sdk/subagents
    """

    description: str
    prompt: str
    tools: list[str] | None = None  # If None, inherits all tools
    model: Literal["sonnet", "opus", "haiku", "inherit"] | None = None


@dataclass
class SandboxConfig:
    """Configuration for sandbox mode.

    See: https://platform.claude.com/docs/en/agent-sdk/python#sandboxsettings
    """

    enabled: bool = False
    auto_allow_bash_if_sandboxed: bool = False
    excluded_commands: list[str] = field(default_factory=list)
    allow_unsandboxed_commands: bool = False


class ClaudeSentient:
    """SDK wrapper for Claude Sentient autonomous development loop.

    This class provides programmatic access to Claude Sentient's capabilities,
    enabling session persistence, SDK-based orchestration, and production deployment.

    Integrates with the official Claude Agent SDK for full autonomous capabilities.
    See: https://platform.claude.com/docs/en/agent-sdk/overview

    Example:
        sentient = ClaudeSentient(cwd="./my-project")

        # Run the autonomous loop
        async for result in sentient.loop("Add user authentication"):
            print(f"Phase: {result.phase}, Tasks: {result.tasks_completed}")
            if result.success:
                print(f"Done! Commit: {result.commit_hash}")

        # Or plan without executing
        plan = await sentient.plan("Refactor the API layer")
        print(plan)

        # Resume a previous session
        async for result in sentient.resume():
            print(f"Resumed: {result.phase}")

        # Use continuous conversation mode
        async with sentient.client() as client:
            await client.query("Analyze this codebase")
            async for msg in client.receive_response():
                print(msg)
    """

    DEFAULT_TOOLS = [
        "Read", "Write", "Edit", "Bash", "Glob", "Grep",
        "Task", "TaskCreate", "TaskUpdate", "TaskList", "TaskGet",
        "EnterPlanMode", "ExitPlanMode", "AskUserQuestion",
        "WebSearch", "WebFetch", "NotebookEdit", "Skill",
    ]

    def __init__(
        self,
        cwd: str | Path = ".",
        profile: str | None = None,
        permission_mode: Literal["default", "acceptEdits", "plan", "bypassPermissions"] = "acceptEdits",
        profiles_dir: str | Path | None = None,
        setting_sources: list[Literal["user", "project", "local"]] | None = None,
        can_use_tool: CanUseTool | None = None,
        hooks: dict[str, list[HookMatcher]] | None = None,
        sandbox: SandboxConfig | None = None,
        enable_file_checkpointing: bool = False,
        max_budget_usd: float | None = None,
        model: str | None = None,
    ):
        """Initialize Claude Sentient.

        Args:
            cwd: Working directory for the project
            profile: Profile name (auto-detected if not provided)
            permission_mode: Permission mode for Claude Agent SDK
                - "default": Standard permission behavior
                - "acceptEdits": Auto-accept file edits (recommended)
                - "plan": Planning mode - no execution
                - "bypassPermissions": Bypass all checks (use with caution)
            profiles_dir: Directory containing profile YAML files
            setting_sources: Which filesystem settings to load
                - "user": Global user settings (~/.claude/settings.json)
                - "project": Project settings (.claude/settings.json)
                - "local": Local settings (.claude/settings.local.json)
                If None (default), no filesystem settings are loaded.
                Must include "project" to load CLAUDE.md files.
            can_use_tool: Callback for custom tool permission handling.
                Receives (tool_name, input_data, context) and returns
                PermissionResultAllow or PermissionResultDeny.
            hooks: Hook configurations for intercepting events.
                Keys: "PreToolUse", "PostToolUse", "UserPromptSubmit", etc.
            sandbox: Sandbox configuration for command execution.
            enable_file_checkpointing: Enable file change tracking for rewinding.
            max_budget_usd: Maximum budget in USD for the session.
            model: Claude model to use (e.g., "claude-sonnet-4-20250514").
        """
        self.cwd = Path(cwd).resolve()
        self.permission_mode = permission_mode
        self.setting_sources = setting_sources
        self.can_use_tool = can_use_tool
        self.custom_hooks = hooks
        self.sandbox = sandbox
        self.enable_file_checkpointing = enable_file_checkpointing
        self.max_budget_usd = max_budget_usd
        self.model = model

        # Initialize managers
        self.session_manager = SessionManager(self.cwd / ".claude/state")
        self.profile_loader = ProfileLoader(profiles_dir)
        self.hook_manager = HookManager(self.session_manager)

        # Detect or load profile
        self.profile_name = profile or self.profile_loader.detect(self.cwd)
        self.profile = self.profile_loader.load(self.profile_name)

        # Initialize quality gates
        if self.profile:
            self.gates = QualityGates(profile=self.profile)
        else:
            self.gates = None

        self.session_id: str | None = None
        self._client: Any = None  # ClaudeSDKClient instance when using client mode
        self._total_cost_usd: float = 0.0

    async def loop(
        self,
        task: str,
        resume: bool = False,
        max_iterations: int = 10,
    ) -> AsyncIterator[LoopResult]:
        """Execute autonomous development loop.

        Args:
            task: The task description to execute
            resume: Whether to resume a previous session
            max_iterations: Maximum loop iterations before stopping

        Yields:
            LoopResult for each phase/iteration
        """
        # Handle resume
        if resume:
            existing_state = self.session_manager.load()
            if existing_state:
                self.session_id = existing_state.session_id
            else:
                raise ValueError("No session to resume")
        else:
            # Create new session
            self.session_id = str(uuid.uuid4())[:8]
            self.session_manager.create(
                session_id=self.session_id,
                profile=self.profile_name,
                task=task,
            )

        try:
            if AGENT_SDK_AVAILABLE:
                # Use the official Claude Agent SDK
                async for result in self._run_with_agent_sdk(task, max_iterations):
                    yield result
            else:
                # Fallback to simulation mode
                yield await self._run_simulation(task, max_iterations)

        except Exception as e:
            yield self._make_error_result(str(e))

    def build_sdk_agents(self) -> dict[str, dict[str, Any]]:
        """Build SDK-compatible agent definitions.

        Returns:
            Dictionary of agent configurations for Claude Agent SDK
        """
        agents = self._define_agents()
        sdk_agents = {}

        if SDKAgentDefinition is not None:
            for name, agent in agents.items():
                sdk_agents[name] = {
                    "description": agent.description,
                    "prompt": agent.prompt,
                    "tools": agent.tools,
                    "model": agent.model,
                }

        return sdk_agents

    def build_sandbox_config(self) -> dict[str, Any] | None:
        """Build sandbox configuration dictionary.

        Returns:
            Sandbox configuration dict or None if not configured
        """
        if not self.sandbox:
            return None

        return {
            "enabled": self.sandbox.enabled,
            "autoAllowBashIfSandboxed": self.sandbox.auto_allow_bash_if_sandboxed,
            "excludedCommands": self.sandbox.excluded_commands,
            "allowUnsandboxedCommands": self.sandbox.allow_unsandboxed_commands,
        }

    def build_merged_hooks(self) -> dict[str, list[Any]] | None:
        """Merge custom hooks with quality gate hooks.

        Returns:
            Merged hook configuration or None
        """
        all_hooks = self._create_hooks()

        if self.custom_hooks:
            for event, matchers in self.custom_hooks.items():
                if event in all_hooks:
                    all_hooks[event].extend(matchers)
                else:
                    all_hooks[event] = matchers

        return all_hooks if all_hooks else None

    def _build_sdk_options(
        self,
        task: str,
        max_iterations: int,
    ) -> "ClaudeAgentOptions":
        """Build Claude Agent SDK options.

        Args:
            task: The task description
            max_iterations: Maximum loop iterations

        Returns:
            Configured ClaudeAgentOptions instance
        """
        system_prompt = self._build_system_prompt(task)
        sdk_agents = self.build_sdk_agents()
        all_hooks = self.build_merged_hooks()
        sandbox_config = self.build_sandbox_config()

        return ClaudeAgentOptions(
            allowed_tools=self.DEFAULT_TOOLS,
            agents=sdk_agents if sdk_agents else None,
            permission_mode=self.permission_mode,
            cwd=str(self.cwd),
            system_prompt={
                "type": "preset",
                "preset": "claude_code",
                "append": system_prompt,
            },
            setting_sources=self.setting_sources,
            can_use_tool=self.can_use_tool,
            hooks=all_hooks,
            enable_file_checkpointing=self.enable_file_checkpointing,
            max_budget_usd=self.max_budget_usd,
            model=self.model,
            sandbox=sandbox_config,
            max_turns=max_iterations,
        )

    def _process_system_message(self, message: Any) -> None:
        """Process a SystemMessage to extract session info."""
        if message.subtype == "init":
            session_id = getattr(message, "session_id", None)
            if session_id:
                self.session_id = session_id

    def _process_assistant_message(
        self,
        message: Any,
        current_phase: str,
        tasks_completed: int,
    ) -> tuple[str, int]:
        """Process an AssistantMessage to extract phase and task updates."""
        for block in message.content:
            if isinstance(block, TextBlock):
                current_phase = self._extract_phase(block.text, current_phase)
            elif isinstance(block, ToolUseBlock) and block.name in ("TaskCreate", "TaskUpdate"):
                tasks_completed += 1
        return current_phase, tasks_completed

    def _process_result_message(
        self,
        message: Any,
        current_phase: str,
        total_cost_usd: float,
    ) -> tuple[str, float]:
        """Process a ResultMessage to extract cost and final status."""
        if message.total_cost_usd:
            total_cost_usd = message.total_cost_usd
        if message.subtype == "success":
            current_phase = "done"
        elif message.subtype == "error":
            current_phase = "error"
        return current_phase, total_cost_usd

    def _process_message(
        self,
        message: Any,
        current_phase: str,
        tasks_completed: int,
        total_cost_usd: float,
    ) -> tuple[str, int, float]:
        """Process a single message from the SDK stream.

        Args:
            message: SDK message object
            current_phase: Current phase name
            tasks_completed: Running count of completed tasks
            total_cost_usd: Running total cost

        Returns:
            Tuple of (updated_phase, tasks_completed, total_cost_usd)
        """
        if isinstance(message, SystemMessage):
            self._process_system_message(message)
        elif isinstance(message, AssistantMessage):
            current_phase, tasks_completed = self._process_assistant_message(
                message, current_phase, tasks_completed
            )
        elif isinstance(message, ResultMessage):
            current_phase, total_cost_usd = self._process_result_message(
                message, current_phase, total_cost_usd
            )
        return current_phase, tasks_completed, total_cost_usd

    def _make_error_result(
        self,
        error: str,
        iteration: int = 0,
        tasks_completed: int = 0,
        cost_usd: float = 0.0,
        duration_ms: float = 0.0,
    ) -> LoopResult:
        """Create a LoopResult for error conditions."""
        return LoopResult(
            success=False,
            session_id=self.session_id or "",
            phase="error",
            iteration=iteration,
            tasks_completed=tasks_completed,
            tasks_remaining=0,
            gates_passed={},
            commit_hash=None,
            duration_ms=duration_ms,
            cost_usd=cost_usd,
            message=error,
        )

    async def _run_with_agent_sdk(
        self,
        task: str,
        max_iterations: int,
    ) -> AsyncIterator[LoopResult]:
        """Run the loop using the official Claude Agent SDK.

        Uses ClaudeAgentOptions with full feature support including:
        - Custom hooks for quality gates and state tracking
        - canUseTool callback for permission handling
        - Subagent definitions for parallel work
        - Session management with cost tracking
        - File checkpointing for rollback

        See: https://platform.claude.com/docs/en/agent-sdk/python
        """
        import time
        start_time = time.time()
        iteration = 0
        tasks_completed = 0
        total_cost_usd = 0.0
        commit_hash = None
        current_phase = "init"
        gates_passed: dict[str, bool] = {}

        options = self._build_sdk_options(task, max_iterations)

        try:
            async for message in query(prompt=task, options=options):
                iteration += 1

                # Process message and update state
                current_phase, tasks_completed, total_cost_usd = self._process_message(
                    message, current_phase, tasks_completed, total_cost_usd
                )

                # Update session state
                self.session_manager.update_phase(current_phase)

                duration_ms = (time.time() - start_time) * 1000

                yield LoopResult(
                    success=current_phase == "done",
                    session_id=self.session_id or "",
                    phase=current_phase,
                    iteration=iteration,
                    tasks_completed=tasks_completed,
                    tasks_remaining=0,
                    gates_passed=gates_passed,
                    commit_hash=commit_hash,
                    duration_ms=duration_ms,
                    cost_usd=total_cost_usd,
                    message=self._extract_message(message),
                )

                if current_phase in ("done", "error") or iteration >= max_iterations:
                    break

            self._total_cost_usd = total_cost_usd

        except Exception as e:
            yield self._make_error_result(
                error=f"Error: {e}",
                iteration=iteration,
                tasks_completed=tasks_completed,
                cost_usd=total_cost_usd,
                duration_ms=(time.time() - start_time) * 1000,
            )

    # Valid phase transitions for the autonomous loop
    # Each phase maps to the phases it can transition to
    VALID_PHASE_TRANSITIONS: dict[str, list[str]] = {
        "init": ["understand"],
        "understand": ["plan"],
        "plan": ["execute"],
        "execute": ["verify", "execute"],  # Can loop within execute
        "verify": ["commit", "execute"],   # Can retry execute on failure
        "commit": ["evaluate"],
        "evaluate": ["done", "execute"],   # Can loop back for more work
        "done": [],
        "error": [],
    }

    def _validate_phase_transition(self, from_phase: str, to_phase: str) -> bool:
        """Validate that a phase transition is allowed.

        Args:
            from_phase: Current phase
            to_phase: Target phase

        Returns:
            True if transition is valid, False otherwise
        """
        valid_targets = self.VALID_PHASE_TRANSITIONS.get(from_phase, [])
        return to_phase in valid_targets

    def _extract_phase(self, content: str, current_phase: str) -> str:
        """Extract phase from message content with transition validation.

        Phases progress through: init → understand → plan → execute → verify → commit → evaluate → done
        Some phases can loop (execute, verify) or branch (evaluate can go to done or execute).
        """
        phase_markers = {
            "[INIT]": "init",
            "[UNDERSTAND]": "understand",
            "[PLAN]": "plan",
            "[EXECUTE]": "execute",
            "[VERIFY]": "verify",
            "[COMMIT]": "commit",
            "[DONE]": "done",
            "[EVALUATE]": "evaluate",
        }
        for marker, phase in phase_markers.items():
            if marker in content:
                # Validate transition (log warning but don't block)
                if not self._validate_phase_transition(current_phase, phase):
                    # Invalid transition - this is a warning, not an error
                    # The loop may skip phases or transition unexpectedly
                    pass
                return phase
        return current_phase

    def _extract_message(self, message: Any) -> str:
        """Extract readable message from SDK message."""
        if isinstance(message, AssistantMessage):
            parts = []
            for block in message.content:
                if isinstance(block, TextBlock):
                    parts.append(block.text)
            return "\n".join(parts)
        elif isinstance(message, ResultMessage):
            return message.result or ""
        elif hasattr(message, "content"):
            return str(message.content)
        return ""

    def _build_system_prompt(self, task: str) -> str:
        """Build the system prompt appendix with profile context."""
        profile_info = f"Profile: {self.profile_name}"
        if self.profile:
            gates_info = ", ".join(self.profile.gates.keys())
            profile_info += f"\nGates: {gates_info}"

        return f"""
## Claude Sentient Context

{profile_info}

Execute the autonomous development loop for this task using these phases:
1. [INIT] - Load context and detect profile
2. [UNDERSTAND] - Classify request, assess scope
3. [PLAN] - Create tasks with dependencies using TaskCreate
4. [EXECUTE] - Work through tasks, update status
5. [VERIFY] - Run quality gates (lint, test, build)
6. [COMMIT] - Create checkpoint commit
7. [EVALUATE] - Check if done, loop if needed

Mark phase transitions with [PHASE_NAME] tags.
"""

    async def _run_simulation(
        self,
        task: str,
        max_iterations: int,
    ) -> LoopResult:
        """Fallback simulation when Claude Agent SDK is not installed.

        This provides a demonstration of the expected interface.
        Install claude-agent-sdk for full functionality.
        """
        import time
        start_time = time.time()

        # Update phase
        self.session_manager.update_phase("execute")

        # Run quality gates if available
        gates_passed = {}
        if self.gates:
            results = self.gates.run_all_blocking(str(self.cwd))
            gates_passed = {
                name: result.status == GateStatus.PASSED
                for name, result in results.items()
            }

        duration_ms = (time.time() - start_time) * 1000

        return LoopResult(
            success=True,
            session_id=self.session_id or "",
            phase="complete",
            iteration=1,
            tasks_completed=0,
            tasks_remaining=0,
            gates_passed=gates_passed,
            commit_hash=None,
            duration_ms=duration_ms,
            cost_usd=0.0,
            message="Simulation mode. Install claude-agent-sdk (`pip install claude-agent-sdk`) for full functionality.",
        )

    async def plan(self, task: str) -> str:
        """Plan a task without executing (plan mode).

        Uses Claude Agent SDK's "plan" permission mode which prevents
        tool execution while allowing Claude to analyze and plan.

        See: https://platform.claude.com/docs/en/agent-sdk/permissions#plan-mode-plan

        Args:
            task: The task description to plan

        Returns:
            The generated plan as a string
        """
        if not AGENT_SDK_AVAILABLE:
            return f"Plan for: {task}\n\nNote: Install claude-agent-sdk (`pip install claude-agent-sdk`) for full planning functionality."

        # Use Claude Agent SDK in plan-only mode
        plan_parts = []
        options = ClaudeAgentOptions(
            allowed_tools=["Read", "Glob", "Grep", "Task", "AskUserQuestion"],
            permission_mode="plan",
            cwd=str(self.cwd),
            setting_sources=self.setting_sources,
            system_prompt={
                "type": "preset",
                "preset": "claude_code",
                "append": f"""## Planning Mode

Profile: {self.profile_name}

Task to plan: {task}

Create a structured plan with:
1. Task summary
2. Approach
3. Files to change
4. Dependencies
5. Risks
6. Quality gates

Do NOT make any changes. Only analyze and plan.
Use AskUserQuestion if you need clarification on the approach.""",
            },
            model=self.model,
        )

        async for message in query(prompt=f"Plan: {task}", options=options):
            plan_parts.append(self._extract_message(message))

        return "\n".join(filter(None, plan_parts)) if plan_parts else f"Plan created for: {task}"

    async def resume(self) -> AsyncIterator[LoopResult]:
        """Resume the last session.

        Yields:
            LoopResult for each phase/iteration
        """
        session_id = self.session_manager.load_session_id()
        if not session_id:
            raise ValueError("No session to resume")

        state = self.session_manager.load()
        if not state:
            raise ValueError("Session state not found")

        async for result in self.loop(
            task=state.task,
            resume=True,
        ):
            yield result

    def get_session_state(self) -> SessionState | None:
        """Get the current session state."""
        return self.session_manager.load()

    def get_gate_results(self) -> dict[str, dict[str, Any]]:
        """Get quality gate results."""
        if not self.gates:
            return {}
        return self.gates.get_summary()

    def get_total_cost(self) -> float:
        """Get total cost in USD for all operations in this instance."""
        return self._total_cost_usd

    def client(self) -> "ClaudeSentientClient":
        """Create a continuous conversation client.

        Use this for multi-turn conversations where Claude remembers context.
        The client maintains a session across multiple query() calls.

        See: https://platform.claude.com/docs/en/agent-sdk/python#claudesdkclient

        Example:
            async with sentient.client() as client:
                await client.query("What files are in this project?")
                async for msg in client.receive_response():
                    print(msg)

                # Follow-up in same conversation
                await client.query("Which one handles authentication?")
                async for msg in client.receive_response():
                    print(msg)

        Returns:
            ClaudeSentientClient context manager
        """
        if not AGENT_SDK_AVAILABLE:
            raise RuntimeError(
                "ClaudeSDKClient requires claude-agent-sdk. "
                "Install with: pip install claude-agent-sdk"
            )
        return ClaudeSentientClient(self)

    def _create_hooks(self) -> dict[str, list[HookMatcher]]:
        """Create hooks for quality gates and state tracking."""
        # Get default session tracking hooks
        session_hooks = self.hook_manager.create_default_hooks()

        # Get gate hooks if profile is available
        if self.profile:
            gate_hooks = create_gate_hooks(self.profile)
            return self.hook_manager.merge_hooks(session_hooks, gate_hooks)

        return session_hooks

    def _define_agents(self) -> dict[str, AgentDefinition]:
        """Define subagents for specialized tasks.

        These agents are used by the Task tool for parallel or specialized work.
        See: https://platform.claude.com/docs/en/agent-sdk/subagents
        """
        return {
            "explore": AgentDefinition(
                description="Fast codebase exploration and file search",
                prompt="Search and analyze code patterns. Use Glob to find files, Grep to search content, Read to examine files.",
                tools=["Read", "Glob", "Grep"],
                model="haiku",
            ),
            "test-runner": AgentDefinition(
                description="Run and analyze test suites",
                prompt="Execute test suites and report results. Identify failing tests and their causes.",
                tools=["Bash", "Read"],
                model="sonnet",
            ),
            "lint-fixer": AgentDefinition(
                description="Fix linting and formatting issues",
                prompt="Analyze lint errors and fix them. Run linter, read errors, apply fixes.",
                tools=["Read", "Edit", "Bash"],
                model="sonnet",
            ),
            "reviewer": AgentDefinition(
                description="Code review and quality analysis",
                prompt="Review code for quality, security, and best practices. Provide specific feedback with file:line references.",
                tools=["Read", "Glob", "Grep"],
                model="sonnet",
            ),
        }


# CLI entry point
async def main():
    """CLI entry point for the SDK."""
    import argparse

    parser = argparse.ArgumentParser(description="Claude Sentient SDK")
    parser.add_argument("command", choices=["loop", "plan", "resume", "status"])
    parser.add_argument("task", nargs="?", default="")
    parser.add_argument("--cwd", default=".", help="Working directory")
    parser.add_argument("--profile", help="Profile name")

    args = parser.parse_args()

    sentient = ClaudeSentient(cwd=args.cwd, profile=args.profile)

    if args.command == "loop":
        if not args.task:
            print("Error: task is required for loop command")
            return
        async for result in sentient.loop(args.task):
            print(f"[{result.phase}] Tasks: {result.tasks_completed}, Gates: {result.gates_passed}")
            if result.success:
                print(f"Done! Commit: {result.commit_hash}")
            else:
                print(f"Error: {result.message}")

    elif args.command == "plan":
        if not args.task:
            print("Error: task is required for plan command")
            return
        plan = await sentient.plan(args.task)
        print(plan)

    elif args.command == "resume":
        try:
            async for result in sentient.resume():
                print(f"[{result.phase}] Resumed session {result.session_id}")
        except ValueError as e:
            print(f"Error: {e}")

    elif args.command == "status":
        state = sentient.get_session_state()
        if state:
            print(f"Session: {state.session_id}")
            print(f"Phase: {state.phase}")
            print(f"Task: {state.task}")
            print(f"Iteration: {state.iteration}")
        else:
            print("No active session")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
