"""Tests for Claude Sentient SDK orchestrator."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, AsyncMock

from claude_sentient.orchestrator import ClaudeSentient, LoopResult, AgentDefinition, SandboxConfig
from claude_sentient.session import SessionState
from claude_sentient.datatypes import GateStatus


class TestLoopResult:
    """Tests for LoopResult dataclass."""

    def test_loop_result_creation(self):
        """LoopResult should be created with all required fields."""
        result = LoopResult(
            success=True,
            session_id="sess-123",
            phase="complete",
            iteration=1,
            tasks_completed=5,
            tasks_remaining=0,
            gates_passed={"lint": True, "test": True},
            commit_hash="abc123",
            duration_ms=1500.5,
            cost_usd=0.02,
        )
        assert result.success is True
        assert result.session_id == "sess-123"
        assert result.phase == "complete"
        assert result.tasks_completed == 5
        assert result.commit_hash == "abc123"

    def test_loop_result_with_message(self):
        """LoopResult should accept optional message."""
        result = LoopResult(
            success=False,
            session_id="sess-456",
            phase="error",
            iteration=1,
            tasks_completed=0,
            tasks_remaining=3,
            gates_passed={},
            commit_hash=None,
            duration_ms=100.0,
            cost_usd=0.0,
            message="Something went wrong",
        )
        assert result.success is False
        assert result.message == "Something went wrong"


class TestClaudeSentient:
    """Tests for ClaudeSentient class."""

    def test_init_with_cwd(self, temp_dir: Path):
        """ClaudeSentient should initialize with cwd."""
        sentient = ClaudeSentient(cwd=str(temp_dir))
        assert sentient.cwd == temp_dir

    def test_init_creates_state_dir(self, temp_dir: Path):
        """ClaudeSentient should create .claude/state directory."""
        sentient = ClaudeSentient(cwd=str(temp_dir))
        state_dir = temp_dir / ".claude" / "state"
        assert state_dir.exists()

    def test_init_detects_profile(self, python_project: Path):
        """ClaudeSentient should detect Python profile."""
        sentient = ClaudeSentient(cwd=str(python_project))
        assert sentient.profile_name == "python"

    def test_init_loads_profile(self, python_project: Path):
        """ClaudeSentient should load profile with gates."""
        sentient = ClaudeSentient(cwd=str(python_project))
        assert sentient.profile is not None
        assert sentient.profile.name == "python"

    def test_init_with_explicit_profile(self, temp_dir: Path):
        """ClaudeSentient should accept explicit profile."""
        sentient = ClaudeSentient(cwd=str(temp_dir), profile="typescript")
        assert sentient.profile_name == "typescript"

    def test_session_manager_initialized(self, temp_dir: Path):
        """ClaudeSentient should initialize session manager."""
        sentient = ClaudeSentient(cwd=str(temp_dir))
        assert sentient.session_manager is not None

    def test_gates_initialized(self, python_project: Path):
        """ClaudeSentient should initialize quality gates."""
        sentient = ClaudeSentient(cwd=str(python_project))
        assert sentient.gates is not None

    def test_get_session_state_none(self, temp_dir: Path):
        """get_session_state should return None when no session."""
        sentient = ClaudeSentient(cwd=str(temp_dir))
        state = sentient.get_session_state()
        assert state is None

    def test_get_gate_results_empty(self, temp_dir: Path):
        """get_gate_results should return empty dict initially."""
        sentient = ClaudeSentient(cwd=str(temp_dir))
        results = sentient.get_gate_results()
        # May be empty if no profile or no gates run
        assert isinstance(results, dict)


class TestClaudeSentientLoop:
    """Tests for ClaudeSentient loop method."""

    @pytest.mark.asyncio
    async def test_loop_yields_results(self, temp_dir: Path):
        """loop should yield LoopResult objects."""
        sentient = ClaudeSentient(cwd=str(temp_dir))

        results = []
        async for result in sentient.loop("test task"):
            results.append(result)

        assert len(results) >= 1
        assert isinstance(results[0], LoopResult)

    @pytest.mark.asyncio
    async def test_loop_creates_session(self, temp_dir: Path):
        """loop should create a new session."""
        sentient = ClaudeSentient(cwd=str(temp_dir))

        async for result in sentient.loop("test task"):
            assert result.session_id is not None
            assert len(result.session_id) > 0

    @pytest.mark.asyncio
    async def test_loop_simulation_completes(self, temp_dir: Path):
        """loop should complete in simulation mode."""
        sentient = ClaudeSentient(cwd=str(temp_dir))

        final_result = None
        async for result in sentient.loop("test task"):
            final_result = result

        assert final_result is not None
        assert final_result.phase == "complete"
        assert final_result.success is True


class TestClaudeSentientPlan:
    """Tests for ClaudeSentient plan method."""

    @pytest.mark.asyncio
    async def test_plan_returns_string(self, temp_dir: Path):
        """plan should return a plan string."""
        sentient = ClaudeSentient(cwd=str(temp_dir))
        plan = await sentient.plan("test task")

        assert isinstance(plan, str)
        assert "test task" in plan

    @pytest.mark.asyncio
    async def test_plan_mentions_sdk(self, temp_dir: Path):
        """plan should mention SDK requirement."""
        sentient = ClaudeSentient(cwd=str(temp_dir))
        plan = await sentient.plan("build feature")

        assert "claude-agent-sdk" in plan.lower() or "sdk" in plan.lower()


class TestClaudeSentientResume:
    """Tests for ClaudeSentient resume method."""

    @pytest.mark.asyncio
    async def test_resume_raises_if_no_session(self, temp_dir: Path):
        """resume should raise ValueError if no active session."""
        sentient = ClaudeSentient(cwd=str(temp_dir))

        with pytest.raises(ValueError, match="No session"):
            async for _ in sentient.resume():
                pass

    @pytest.mark.asyncio
    async def test_resume_continues_session(self, temp_dir: Path):
        """resume should continue from saved state."""
        sentient = ClaudeSentient(cwd=str(temp_dir))

        # Create a session first
        sentient.session_manager.create(
            session_id="resume-test",
            profile="python",
            task="Original task",
        )

        results = []
        async for result in sentient.resume():
            results.append(result)

        assert len(results) >= 1
        assert results[0].session_id == "resume-test"


class TestClaudeSentientAgents:
    """Tests for ClaudeSentient agent definitions."""

    def test_define_agents(self, temp_dir: Path):
        """_define_agents should return agent definitions."""
        sentient = ClaudeSentient(cwd=str(temp_dir))
        agents = sentient._define_agents()

        assert "explore" in agents
        assert "test-runner" in agents
        assert "lint-fixer" in agents

    def test_agent_has_required_fields(self, temp_dir: Path):
        """Agent definitions should have required fields."""
        sentient = ClaudeSentient(cwd=str(temp_dir))
        agents = sentient._define_agents()

        explore = agents["explore"]
        assert explore.description
        assert explore.prompt
        assert explore.tools
        assert explore.model


class TestClaudeSentientPrompts:
    """Tests for ClaudeSentient prompt building."""

    def test_build_system_prompt(self, temp_dir: Path):
        """_build_system_prompt should include profile info."""
        sentient = ClaudeSentient(cwd=str(temp_dir))
        prompt = sentient._build_system_prompt("Add authentication")

        assert "Profile:" in prompt
        assert "[INIT]" in prompt  # Phase marker

    def test_build_system_prompt_includes_gates(self, python_project: Path):
        """_build_system_prompt should include gate info."""
        sentient = ClaudeSentient(cwd=str(python_project))
        prompt = sentient._build_system_prompt("Fix bug")

        assert "Gates:" in prompt


class TestClaudeSentientNewFeatures:
    """Tests for new SDK features."""

    def test_get_total_cost_starts_at_zero(self, temp_dir: Path):
        """get_total_cost should return 0 initially."""
        sentient = ClaudeSentient(cwd=str(temp_dir))
        assert sentient.get_total_cost() == 0.0

    def test_init_with_permission_mode(self, temp_dir: Path):
        """ClaudeSentient should accept permission_mode."""
        sentient = ClaudeSentient(cwd=str(temp_dir), permission_mode="bypassPermissions")
        assert sentient.permission_mode == "bypassPermissions"

    def test_init_with_setting_sources(self, temp_dir: Path):
        """ClaudeSentient should accept setting_sources."""
        sentient = ClaudeSentient(cwd=str(temp_dir), setting_sources=["user", "project"])
        assert sentient.setting_sources == ["user", "project"]

    def test_init_with_max_budget(self, temp_dir: Path):
        """ClaudeSentient should accept max_budget_usd."""
        sentient = ClaudeSentient(cwd=str(temp_dir), max_budget_usd=10.0)
        assert sentient.max_budget_usd == 10.0

    def test_init_with_model(self, temp_dir: Path):
        """ClaudeSentient should accept model override."""
        sentient = ClaudeSentient(cwd=str(temp_dir), model="claude-sonnet-4-20250514")
        assert sentient.model == "claude-sonnet-4-20250514"

    def test_init_with_sandbox_config(self, temp_dir: Path):
        """ClaudeSentient should accept sandbox configuration."""
        from claude_sentient import SandboxConfig

        sandbox = SandboxConfig(enabled=True, auto_allow_bash_if_sandboxed=True)
        sentient = ClaudeSentient(cwd=str(temp_dir), sandbox=sandbox)

        assert sentient.sandbox is not None
        assert sentient.sandbox.enabled is True
        assert sentient.sandbox.auto_allow_bash_if_sandboxed is True

    def test_init_with_file_checkpointing(self, temp_dir: Path):
        """ClaudeSentient should accept enable_file_checkpointing."""
        sentient = ClaudeSentient(cwd=str(temp_dir), enable_file_checkpointing=True)
        assert sentient.enable_file_checkpointing is True

    def test_client_method_raises_without_sdk(self, temp_dir: Path):
        """client() should raise if SDK not available."""
        from claude_sentient.orchestrator import AGENT_SDK_AVAILABLE

        sentient = ClaudeSentient(cwd=str(temp_dir))

        if not AGENT_SDK_AVAILABLE:
            import pytest
            with pytest.raises(RuntimeError, match="requires claude-agent-sdk"):
                sentient.client()

    def test_define_agents_includes_reviewer(self, temp_dir: Path):
        """_define_agents should include reviewer agent."""
        sentient = ClaudeSentient(cwd=str(temp_dir))
        agents = sentient._define_agents()

        assert "reviewer" in agents
        assert "Code review" in agents["reviewer"].description


class TestPhaseValidation:
    """Tests for phase transition validation."""

    def test_valid_transitions_defined(self, temp_dir: Path):
        """ClaudeSentient should have VALID_PHASE_TRANSITIONS."""
        assert hasattr(ClaudeSentient, 'VALID_PHASE_TRANSITIONS')
        transitions = ClaudeSentient.VALID_PHASE_TRANSITIONS
        assert "init" in transitions
        assert "understand" in transitions["init"]

    def test_validate_phase_transition_valid(self, temp_dir: Path):
        """_validate_phase_transition should return True for valid transitions."""
        sentient = ClaudeSentient(cwd=str(temp_dir))
        assert sentient._validate_phase_transition("init", "understand") is True
        assert sentient._validate_phase_transition("plan", "execute") is True
        assert sentient._validate_phase_transition("execute", "verify") is True

    def test_validate_phase_transition_invalid(self, temp_dir: Path):
        """_validate_phase_transition should return False for invalid transitions."""
        sentient = ClaudeSentient(cwd=str(temp_dir))
        assert sentient._validate_phase_transition("init", "execute") is False
        assert sentient._validate_phase_transition("done", "init") is False
        assert sentient._validate_phase_transition("commit", "plan") is False

    def test_validate_phase_transition_loops(self, temp_dir: Path):
        """_validate_phase_transition should allow valid loops."""
        sentient = ClaudeSentient(cwd=str(temp_dir))
        # Execute can loop back to itself
        assert sentient._validate_phase_transition("execute", "execute") is True
        # Verify can retry execute
        assert sentient._validate_phase_transition("verify", "execute") is True
        # Evaluate can loop back to execute
        assert sentient._validate_phase_transition("evaluate", "execute") is True

    def test_extract_phase_with_marker(self, temp_dir: Path):
        """_extract_phase should extract phase from marker."""
        sentient = ClaudeSentient(cwd=str(temp_dir))
        content = "Starting work...\n[EXECUTE] Working on tasks..."
        phase = sentient._extract_phase(content, "plan")
        assert phase == "execute"

    def test_extract_phase_no_marker(self, temp_dir: Path):
        """_extract_phase should return current phase when no marker."""
        sentient = ClaudeSentient(cwd=str(temp_dir))
        content = "Just some text without any phase marker"
        phase = sentient._extract_phase(content, "verify")
        assert phase == "verify"

    def test_extract_phase_multiple_markers(self, temp_dir: Path):
        """_extract_phase should return first marker found."""
        sentient = ClaudeSentient(cwd=str(temp_dir))
        content = "[INIT] Starting...\n[UNDERSTAND] Analyzing..."
        phase = sentient._extract_phase(content, "init")
        # Returns first marker found in iteration order
        assert phase in ("init", "understand")


class TestMessageProcessing:
    """Tests for message processing helpers."""

    def test_process_system_message_with_session_id(self, temp_dir: Path):
        """_process_system_message should extract session_id."""
        sentient = ClaudeSentient(cwd=str(temp_dir))
        mock_msg = MagicMock()
        mock_msg.subtype = "init"
        mock_msg.session_id = "test-session-123"

        sentient._process_system_message(mock_msg)
        assert sentient.session_id == "test-session-123"

    def test_process_system_message_without_session_id(self, temp_dir: Path):
        """_process_system_message should handle missing session_id."""
        sentient = ClaudeSentient(cwd=str(temp_dir))
        mock_msg = MagicMock()
        mock_msg.subtype = "init"
        delattr(mock_msg, 'session_id')

        sentient._process_system_message(mock_msg)
        # Should not raise

    def test_process_result_message_success(self, temp_dir: Path):
        """_process_result_message should set phase to done on success."""
        sentient = ClaudeSentient(cwd=str(temp_dir))
        mock_msg = MagicMock()
        mock_msg.total_cost_usd = 0.05
        mock_msg.subtype = "success"

        phase, cost = sentient._process_result_message(mock_msg, "verify", 0.0)
        assert phase == "done"
        assert cost == 0.05

    def test_process_result_message_error(self, temp_dir: Path):
        """_process_result_message should set phase to error on failure."""
        sentient = ClaudeSentient(cwd=str(temp_dir))
        mock_msg = MagicMock()
        mock_msg.total_cost_usd = 0.02
        mock_msg.subtype = "error"

        phase, cost = sentient._process_result_message(mock_msg, "execute", 0.0)
        assert phase == "error"
        assert cost == 0.02


class TestSDKOptionsBuilding:
    """Tests for SDK options building methods."""

    def test_build_sdk_agents(self, temp_dir: Path):
        """_build_sdk_agents should return dict with agent configs."""
        sentient = ClaudeSentient(cwd=str(temp_dir))
        agents = sentient._build_sdk_agents()

        # When SDK not available, may be empty
        # But structure should be dict
        assert isinstance(agents, dict)

    def test_build_sandbox_config_none(self, temp_dir: Path):
        """_build_sandbox_config should return None when not configured."""
        sentient = ClaudeSentient(cwd=str(temp_dir))
        config = sentient._build_sandbox_config()
        assert config is None

    def test_build_sandbox_config_enabled(self, temp_dir: Path):
        """_build_sandbox_config should return config when sandbox set."""
        sandbox = SandboxConfig(enabled=True, auto_allow_bash_if_sandboxed=True)
        sentient = ClaudeSentient(cwd=str(temp_dir), sandbox=sandbox)
        config = sentient._build_sandbox_config()

        assert config is not None
        assert config["enabled"] is True
        assert config["autoAllowBashIfSandboxed"] is True

    def test_build_merged_hooks(self, python_project: Path):
        """_build_merged_hooks should merge gate and custom hooks."""
        sentient = ClaudeSentient(cwd=str(python_project))
        hooks = sentient._build_merged_hooks()

        # Should have at least session hooks
        assert hooks is not None
        assert isinstance(hooks, dict)


class TestLoopErrorHandling:
    """Tests for loop error handling."""

    @pytest.mark.asyncio
    async def test_loop_handles_exception(self, temp_dir: Path):
        """loop should yield error result on exception."""
        sentient = ClaudeSentient(cwd=str(temp_dir))

        # Mock to raise exception
        with patch.object(sentient, '_run_simulation', side_effect=Exception("Test error")):
            results = []
            async for result in sentient.loop("task"):
                results.append(result)

            assert len(results) == 1
            assert results[0].success is False
            assert results[0].phase == "error"
            assert "Test error" in results[0].message

    @pytest.mark.asyncio
    async def test_loop_resume_false_creates_new_session(self, temp_dir: Path):
        """loop with resume=False should create new session."""
        sentient = ClaudeSentient(cwd=str(temp_dir))

        # Create existing session
        sentient.session_manager.create(
            session_id="old-session",
            profile="python",
            task="old task",
        )

        # Run loop without resume - should create new session
        async for result in sentient.loop("new task", resume=False):
            assert result.session_id != "old-session"
            break

    @pytest.mark.asyncio
    async def test_loop_resume_true_uses_existing(self, temp_dir: Path):
        """loop with resume=True should use existing session."""
        sentient = ClaudeSentient(cwd=str(temp_dir))

        # Create existing session
        sentient.session_manager.create(
            session_id="existing-session",
            profile="python",
            task="existing task",
        )

        # Run loop with resume - should use existing
        async for result in sentient.loop("task", resume=True):
            assert result.session_id == "existing-session"
            break

    @pytest.mark.asyncio
    async def test_loop_resume_true_no_session_raises(self, temp_dir: Path):
        """loop with resume=True and no session should raise."""
        sentient = ClaudeSentient(cwd=str(temp_dir))

        with pytest.raises(ValueError, match="No session"):
            async for _ in sentient.loop("task", resume=True):
                pass


class TestQualityGatesIntegration:
    """Tests for quality gates integration."""

    def test_gates_initialized_with_profile(self, python_project: Path):
        """gates should be initialized when profile has gates."""
        sentient = ClaudeSentient(cwd=str(python_project))
        assert sentient.gates is not None

    def test_gates_none_without_profile(self, temp_dir: Path):
        """gates should be None when no profile found."""
        # Use a profile that doesn't exist
        sentient = ClaudeSentient(cwd=str(temp_dir), profile="nonexistent")
        assert sentient.gates is None

    def test_get_gate_results_structure(self, python_project: Path):
        """get_gate_results should return proper structure."""
        sentient = ClaudeSentient(cwd=str(python_project))
        results = sentient.get_gate_results()

        assert isinstance(results, dict)
        # Initially empty or has structure keys
        if results:
            assert "total" in results or len(results) == 0


class TestAgentDefinitionDataclass:
    """Tests for AgentDefinition dataclass."""

    def test_agent_definition_creation(self):
        """AgentDefinition should be created with required fields."""
        agent = AgentDefinition(
            description="Test agent",
            prompt="Do something",
        )
        assert agent.description == "Test agent"
        assert agent.prompt == "Do something"
        assert agent.tools is None
        assert agent.model is None

    def test_agent_definition_with_tools(self):
        """AgentDefinition should accept tools list."""
        agent = AgentDefinition(
            description="File explorer",
            prompt="Search files",
            tools=["Read", "Glob", "Grep"],
            model="haiku",
        )
        assert agent.tools == ["Read", "Glob", "Grep"]
        assert agent.model == "haiku"


class TestSandboxConfigDataclass:
    """Tests for SandboxConfig dataclass."""

    def test_sandbox_config_defaults(self):
        """SandboxConfig should have sensible defaults."""
        config = SandboxConfig()
        assert config.enabled is False
        assert config.auto_allow_bash_if_sandboxed is False
        assert config.excluded_commands == []
        assert config.allow_unsandboxed_commands is False

    def test_sandbox_config_custom_values(self):
        """SandboxConfig should accept custom values."""
        config = SandboxConfig(
            enabled=True,
            auto_allow_bash_if_sandboxed=True,
            excluded_commands=["rm -rf"],
            allow_unsandboxed_commands=True,
        )
        assert config.enabled is True
        assert config.auto_allow_bash_if_sandboxed is True
        assert "rm -rf" in config.excluded_commands


class TestCostTracking:
    """Tests for cost tracking functionality."""

    def test_total_cost_initially_zero(self, temp_dir: Path):
        """_total_cost_usd should start at zero."""
        sentient = ClaudeSentient(cwd=str(temp_dir))
        assert sentient._total_cost_usd == 0.0

    def test_get_total_cost_returns_tracked(self, temp_dir: Path):
        """get_total_cost should return tracked cost."""
        sentient = ClaudeSentient(cwd=str(temp_dir))
        sentient._total_cost_usd = 1.50
        assert sentient.get_total_cost() == 1.50
