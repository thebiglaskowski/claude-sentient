"""Claude Sentient SDK - Autonomous Development Orchestration Layer.

This SDK provides programmatic access to Claude Sentient's capabilities:
- Session persistence for resuming work across terminal closures
- SDK-based orchestration instead of text commands
- Production deployment support (CI/CD, webhooks, scheduled tasks)

Example:
    from claude_sentient import ClaudeSentient

    async def main():
        sentient = ClaudeSentient(cwd="./my-project")
        async for result in sentient.loop("Add user authentication"):
            print(f"Progress: {result.tasks_completed} tasks completed")
            if result.success:
                print(f"Done! Commit: {result.commit_hash}")
"""

from .orchestrator import ClaudeSentient, LoopResult
from .session import SessionManager, SessionState
from .profiles import ProfileLoader, Profile
from .gates import QualityGates, GateResult
from .hooks import HookManager
from .types import Task, TaskStatus, Phase, GateStatus

__version__ = "0.3.0"
__all__ = [
    "ClaudeSentient",
    "LoopResult",
    "SessionManager",
    "SessionState",
    "ProfileLoader",
    "Profile",
    "QualityGates",
    "GateResult",
    "HookManager",
    "Task",
    "TaskStatus",
    "Phase",
    "GateStatus",
]
