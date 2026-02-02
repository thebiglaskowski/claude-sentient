"""Claude Sentient SDK - Autonomous Development Orchestration Layer.

This SDK provides programmatic access to Claude Sentient's capabilities:
- Session persistence for resuming work across terminal closures
- SDK-based orchestration instead of text commands
- Production deployment support (CI/CD, webhooks, scheduled tasks)
- Integration with official Claude Agent SDK for full autonomous capabilities

See: https://platform.claude.com/docs/en/agent-sdk/overview

Example:
    from claude_sentient import ClaudeSentient

    async def main():
        sentient = ClaudeSentient(cwd="./my-project")
        async for result in sentient.loop("Add user authentication"):
            print(f"Progress: {result.tasks_completed} tasks completed")
            if result.success:
                print(f"Done! Commit: {result.commit_hash}")

        # Or use continuous conversation mode
        async with sentient.client() as client:
            await client.query("What's in this project?")
            async for msg in client.receive_response():
                print(msg)
"""

from .datatypes import GateStatus, Phase, Task, TaskStatus
from .gates import GateResult, QualityGates
from .hooks import HookManager
from .orchestrator import (
    AGENT_SDK_AVAILABLE,
    AgentDefinition,
    ClaudeSentient,
    ClaudeSentientClient,
    LoopResult,
    SandboxConfig,
)
from .profiles import Profile, ProfileLoader
from .session import SessionManager, SessionState

__version__ = "0.3.0"
__all__ = [
    # Main classes
    "ClaudeSentient",
    "ClaudeSentientClient",
    "LoopResult",
    "AgentDefinition",
    "SandboxConfig",
    "AGENT_SDK_AVAILABLE",
    # Session management
    "SessionManager",
    "SessionState",
    # Profiles
    "ProfileLoader",
    "Profile",
    # Quality gates
    "QualityGates",
    "GateResult",
    # Hooks
    "HookManager",
    # Types
    "Task",
    "TaskStatus",
    "Phase",
    "GateStatus",
]
