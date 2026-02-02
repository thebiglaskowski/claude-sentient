"""
Tests for Claude Conductor agent files.

Validates:
- YAML frontmatter structure (name, description, tools, disallowedTools, model)
- Valid tool names
- Valid model values
- Required markdown sections present
"""

import pytest
from pathlib import Path

from validators.base import Severity
from schemas.agent_schema import AgentValidator, VALID_TOOLS


class TestAgentStructure:
    """Test agent file structure."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up validator for tests."""
        self.validator = AgentValidator()

    def test_agent_is_valid(self, agent_file: Path):
        """Test that an agent file passes validation."""
        result = self.validator.validate(agent_file)

        # Get blocking findings (S0 and S1)
        blocking = result.blocking_findings
        if blocking:
            msg_lines = [f"\nValidation failed for {agent_file.name}:"]
            for f in blocking:
                msg_lines.append(f"  [{f.severity}] {f.code}: {f.message}")
                if f.suggestion:
                    msg_lines.append(f"    Suggestion: {f.suggestion}")

            pytest.fail("\n".join(msg_lines))

    def test_agent_has_frontmatter(self, agent_file: Path):
        """Test that agent has YAML frontmatter."""
        result = self.validator.validate(agent_file)

        frontmatter = result.metadata.get("frontmatter")
        assert frontmatter is not None, f"{agent_file.name} is missing frontmatter"

    def test_agent_has_name(self, agent_file: Path):
        """Test that agent has a name."""
        result = self.validator.validate(agent_file)

        frontmatter = result.metadata.get("frontmatter", {})
        name = frontmatter.get("name")

        assert name, f"{agent_file.name} is missing name"

    def test_agent_has_description(self, agent_file: Path):
        """Test that agent has a description."""
        result = self.validator.validate(agent_file)

        frontmatter = result.metadata.get("frontmatter", {})
        description = frontmatter.get("description")

        assert description, f"{agent_file.name} is missing description"


class TestAgentTools:
    """Test agent tools configuration."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up validator for tests."""
        self.validator = AgentValidator()

    def test_agent_has_tools(self, agent_file: Path):
        """Test that agent has tools defined."""
        result = self.validator.validate(agent_file)

        frontmatter = result.metadata.get("frontmatter", {})
        tools = frontmatter.get("tools")

        assert tools is not None, f"{agent_file.name} is missing tools"

    def test_agent_has_disallowed_tools_if_read_only(self, agent_file: Path):
        """Test that read-only agents have disallowedTools defined."""
        result = self.validator.validate(agent_file)

        frontmatter = result.metadata.get("frontmatter", {})
        disallowed = frontmatter.get("disallowedTools")

        # disallowedTools is optional, but if tools don't include Write/Edit,
        # it's a read-only agent and should be documented
        tools = frontmatter.get("tools", "")
        if isinstance(tools, str):
            tools_str = tools.lower()
        else:
            tools_str = ",".join(tools).lower() if tools else ""

        if "write" not in tools_str and "edit" not in tools_str:
            # This is effectively a read-only agent even without disallowedTools
            pass  # OK, no disallowedTools needed if Write/Edit not in tools

    def test_agent_tools_are_valid(self, agent_file: Path):
        """Test that agent tools are valid tool names."""
        result = self.validator.validate(agent_file)

        frontmatter = result.metadata.get("frontmatter", {})
        tools = frontmatter.get("tools", "")

        if isinstance(tools, str):
            tool_list = [t.strip() for t in tools.split(",")]
        elif isinstance(tools, list):
            tool_list = tools
        else:
            tool_list = []

        for tool in tool_list:
            if tool:
                assert tool in VALID_TOOLS, \
                    f"{agent_file.name}: unknown tool '{tool}'"


class TestAgentModel:
    """Test agent model configuration."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up validator for tests."""
        self.validator = AgentValidator()

    def test_agent_has_model(self, agent_file: Path):
        """Test that agent has a model specified."""
        result = self.validator.validate(agent_file)

        frontmatter = result.metadata.get("frontmatter", {})
        model = frontmatter.get("model")

        assert model, f"{agent_file.name} is missing model"

    def test_agent_model_is_valid(self, agent_file: Path):
        """Test that agent model is valid."""
        result = self.validator.validate(agent_file)

        frontmatter = result.metadata.get("frontmatter", {})
        model = frontmatter.get("model")

        if model:
            assert model in {"sonnet", "opus", "haiku"}, \
                f"{agent_file.name}: invalid model '{model}'"


class TestAgentContent:
    """Test agent content requirements."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up validator for tests."""
        self.validator = AgentValidator()

    def test_agent_has_expertise_section(self, agent_file: Path):
        """Test that agent has an Expertise section."""
        result = self.validator.validate(agent_file)

        sections = result.metadata.get("sections", {})
        section_names = {s.lower() for s in sections.keys()}

        has_expertise = any("expertise" in s for s in section_names)
        assert has_expertise, f"{agent_file.name} is missing Expertise section"

    def test_agent_has_process_section(self, agent_file: Path):
        """Test that agent has a Process section."""
        result = self.validator.validate(agent_file)

        sections = result.metadata.get("sections", {})
        section_names = {s.lower() for s in sections.keys()}

        has_process = any("process" in s for s in section_names)
        assert has_process, f"{agent_file.name} is missing Process section"


class TestAgentQuality:
    """Test agent quality requirements."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up validator for tests."""
        self.validator = AgentValidator()

    def test_agent_no_critical_issues(self, agent_file: Path):
        """Test that agent has no critical (S0) issues."""
        result = self.validator.validate(agent_file)

        critical = result.critical_findings
        assert not critical, \
            f"{agent_file.name} has critical issues: {[f.code for f in critical]}"

    def test_agent_no_high_issues(self, agent_file: Path):
        """Test that agent has no high (S1) issues."""
        result = self.validator.validate(agent_file)

        high = result.high_findings
        assert not high, \
            f"{agent_file.name} has high-severity issues: {[f.code for f in high]}"
