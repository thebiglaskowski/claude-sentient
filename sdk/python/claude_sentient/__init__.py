"""Claude Sentient SDK - Autonomous Development Orchestration Layer.

This SDK provides programmatic access to Claude Sentient's capabilities:
- Session persistence for resuming work across terminal closures
- SDK-based orchestration instead of text commands
- Production deployment support (CI/CD, webhooks, scheduled tasks)
- Integration with official Claude Agent SDK for full autonomous capabilities
- Vision analysis for UI/UX testing and error debugging
- Model routing for cost-optimized inference

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

from .datatypes import (
    CostTracking,
    GateStatus,
    HookDecision,
    HookEvent,
    HookResult,
    HookType,
    ModelTier,
    Phase,
    SubagentInfo,
    Task,
    TaskStatus,
)
from .gates import GateResult, QualityGates
from .hooks import BudgetExceededError, HookConfig, HookManager, HookMatcher
from .orchestrator import (
    AGENT_SDK_AVAILABLE,
    AgentDefinition,
    ClaudeSentient,
    ClaudeSentientClient,
    LoopResult,
    SandboxConfig,
)
from .profiles import ModelConfig, Profile, ProfileLoader, ThinkingConfig
from .session import (
    SessionManager,
    SessionState,
    TASK_TIMEOUTS,
    generate_session_name,
    get_task_timeout,
)
from .vision import (
    ScreenshotResult,
    VisualDiff,
    VisionAnalyzer,
    analyze_responsive_layout,
    analyze_screenshot,
    capture_error_screenshot,
    visual_diff,
)

__version__ = "0.4.0"
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
    "generate_session_name",
    "get_task_timeout",
    "TASK_TIMEOUTS",
    # Profiles
    "ProfileLoader",
    "Profile",
    "ModelConfig",
    "ThinkingConfig",
    # Quality gates
    "QualityGates",
    "GateResult",
    # Hooks
    "HookManager",
    "HookMatcher",
    "HookConfig",
    "BudgetExceededError",
    # Vision
    "VisionAnalyzer",
    "ScreenshotResult",
    "VisualDiff",
    "analyze_screenshot",
    "capture_error_screenshot",
    "visual_diff",
    "analyze_responsive_layout",
    # Types / Enums
    "Task",
    "TaskStatus",
    "Phase",
    "GateStatus",
    "HookType",
    "HookEvent",
    "HookDecision",
    "HookResult",
    "ModelTier",
    "SubagentInfo",
    "CostTracking",
]
