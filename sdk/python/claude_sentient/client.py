"""Continuous conversation client for Claude Sentient SDK.

Wraps ClaudeSDKClient for multi-turn conversations where Claude
remembers previous context.

See: https://platform.claude.com/docs/en/agent-sdk/python#claudesdkclient
"""

from typing import TYPE_CHECKING, Any

try:
    from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient

    AGENT_SDK_AVAILABLE = True
except ImportError:
    AGENT_SDK_AVAILABLE = False

if TYPE_CHECKING:
    from .orchestrator import ClaudeSentient


class ClaudeSentientClient:
    """Continuous conversation client wrapping ClaudeSDKClient.

    Provides a context manager interface for multi-turn conversations
    where Claude remembers previous context.

    See: https://platform.claude.com/docs/en/agent-sdk/python#claudesdkclient
    """

    def __init__(self, sentient: "ClaudeSentient"):
        """Initialize the client wrapper.

        Args:
            sentient: Parent ClaudeSentient instance with configuration
        """
        self.sentient = sentient
        self._client: Any = None

    async def __aenter__(self) -> "ClaudeSentientClient":
        """Enter the context manager and connect."""
        all_hooks = self.sentient.build_merged_hooks()
        sdk_agents = self.sentient.build_sdk_agents()
        sandbox_config = self.sentient.build_sandbox_config()

        options = ClaudeAgentOptions(
            allowed_tools=self.sentient.DEFAULT_TOOLS,
            agents=sdk_agents if sdk_agents else None,
            permission_mode=self.sentient.permission_mode,
            cwd=str(self.sentient.cwd),
            setting_sources=self.sentient.setting_sources,
            can_use_tool=self.sentient.can_use_tool,
            hooks=all_hooks if all_hooks else None,
            enable_file_checkpointing=self.sentient.enable_file_checkpointing,
            max_budget_usd=self.sentient.max_budget_usd,
            model=self.sentient.model,
            sandbox=sandbox_config,
        )

        self._client = ClaudeSDKClient(options)
        await self._client.connect()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit the context manager and disconnect."""
        if self._client:
            await self._client.disconnect()
            self._client = None

    async def query(self, prompt: str) -> None:
        """Send a query to Claude.

        Args:
            prompt: The message to send
        """
        if not self._client:
            raise RuntimeError("Client not connected. Use 'async with' context manager.")
        await self._client.query(prompt)

    async def receive_response(self):
        """Receive messages until result.

        Yields:
            Messages from Claude
        """
        if not self._client:
            raise RuntimeError("Client not connected. Use 'async with' context manager.")
        async for message in self._client.receive_response():
            yield message

    async def receive_messages(self):
        """Receive all messages.

        Yields:
            All messages from Claude
        """
        if not self._client:
            raise RuntimeError("Client not connected. Use 'async with' context manager.")
        async for message in self._client.receive_messages():
            yield message

    async def interrupt(self) -> None:
        """Interrupt the current operation."""
        if self._client:
            await self._client.interrupt()

    async def rewind_files(self, user_message_uuid: str) -> None:
        """Rewind files to state at a specific user message.

        Requires enable_file_checkpointing=True in ClaudeSentient.

        Args:
            user_message_uuid: UUID of the user message to rewind to
        """
        if not self._client:
            raise RuntimeError("Client not connected. Use 'async with' context manager.")
        await self._client.rewind_files(user_message_uuid)
