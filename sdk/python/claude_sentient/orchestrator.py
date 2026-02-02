"""Main orchestrator for Claude Sentient SDK."""

import subprocess
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, AsyncIterator

from .gates import QualityGates, create_gate_hooks
from .hooks import HookManager, HookMatcher
from .profiles import ProfileLoader, Profile
from .session import SessionManager, SessionState
from .types import Phase, GateStatus


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
    """Definition for a subagent."""

    description: str
    prompt: str
    tools: list[str] = field(default_factory=list)
    model: str = "sonnet"


class ClaudeSentient:
    """SDK wrapper for Claude Sentient autonomous development loop.

    This class provides programmatic access to Claude Sentient's capabilities,
    enabling session persistence, SDK-based orchestration, and production deployment.

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
    """

    DEFAULT_TOOLS = [
        "Read", "Write", "Edit", "Bash", "Glob", "Grep",
        "Task", "TaskCreate", "TaskUpdate", "TaskList",
        "EnterPlanMode", "ExitPlanMode",
    ]

    def __init__(
        self,
        cwd: str | Path = ".",
        profile: str | None = None,
        permission_mode: str = "acceptEdits",
        profiles_dir: str | Path | None = None,
    ):
        """Initialize Claude Sentient.

        Args:
            cwd: Working directory for the project
            profile: Profile name (auto-detected if not provided)
            permission_mode: Permission mode for Claude Agent SDK
            profiles_dir: Directory containing profile YAML files
        """
        self.cwd = Path(cwd).resolve()
        self.permission_mode = permission_mode

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
            # Note: In a real implementation, this would use the Claude Agent SDK
            # For now, we provide a simulation that shows the expected interface
            yield await self._simulate_loop(task, max_iterations)

        except Exception as e:
            yield LoopResult(
                success=False,
                session_id=self.session_id,
                phase="error",
                iteration=0,
                tasks_completed=0,
                tasks_remaining=0,
                gates_passed={},
                commit_hash=None,
                duration_ms=0,
                cost_usd=0,
                message=str(e),
            )

    async def _simulate_loop(
        self,
        task: str,
        max_iterations: int,
    ) -> LoopResult:
        """Simulate the loop for SDK interface demonstration.

        In a real implementation, this would call the Claude Agent SDK.
        This simulation shows the expected return values and structure.
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
            message="SDK simulation complete. Install claude-agent-sdk for full functionality.",
        )

    async def plan(self, task: str) -> str:
        """Plan a task without executing (plan mode).

        Args:
            task: The task description to plan

        Returns:
            The generated plan as a string
        """
        # In a real implementation, this would use the Claude Agent SDK
        # with permission_mode="plan"
        return f"Plan for: {task}\n\nNote: Install claude-agent-sdk for full planning functionality."

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

    def _build_loop_prompt(self, task: str) -> str:
        """Build the /cs-loop system prompt with profile context."""
        profile_info = f"Profile: {self.profile_name}"
        if self.profile:
            gates_info = ", ".join(self.profile.gates.keys())
            profile_info += f"\nGates: {gates_info}"

        return f"""
Execute the Claude Sentient autonomous development loop for this task:

Task: {task}

{profile_info}

Follow the /cs-loop phases:
1. INIT - Load context and detect profile
2. UNDERSTAND - Classify request, assess scope
3. PLAN - Create tasks with dependencies
4. EXECUTE - Work through tasks
5. VERIFY - Run quality gates
6. COMMIT - Create checkpoint commit
7. EVALUATE - Check if done, loop if needed
"""

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
        """Define subagents for specialized tasks."""
        return {
            "explore": AgentDefinition(
                description="Fast codebase exploration",
                prompt="Search and analyze code patterns",
                tools=["Read", "Glob", "Grep"],
                model="haiku",
            ),
            "test-runner": AgentDefinition(
                description="Run and analyze tests",
                prompt="Execute test suites and report results",
                tools=["Bash", "Read"],
                model="sonnet",
            ),
            "lint-fixer": AgentDefinition(
                description="Fix linting issues",
                prompt="Analyze lint errors and fix them",
                tools=["Read", "Edit", "Bash"],
                model="sonnet",
            ),
        }


# CLI entry point
async def main():
    """CLI entry point for the SDK."""
    import argparse
    import asyncio

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
