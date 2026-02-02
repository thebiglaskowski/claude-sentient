"""
Tests for Claude Conductor command files.

Validates:
- YAML frontmatter structure (name, description, model)
- Command names start with 'cc:'
- Valid model values (sonnet, opus, haiku)
- Required XML-style sections present
"""

import pytest
from pathlib import Path

from validators.base import Severity
from schemas.command_schema import CommandValidator


class TestCommandStructure:
    """Test command file structure and content."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up validator for tests."""
        self.validator = CommandValidator()

    def test_command_is_valid(self, command_file: Path):
        """Test that a command file passes validation."""
        result = self.validator.validate(command_file)

        # Get blocking findings (S0 and S1)
        blocking = result.blocking_findings
        if blocking:
            # Format findings for error message
            msg_lines = [f"\nValidation failed for {command_file.name}:"]
            for f in blocking:
                msg_lines.append(f"  [{f.severity}] {f.code}: {f.message}")
                if f.suggestion:
                    msg_lines.append(f"    Suggestion: {f.suggestion}")

            pytest.fail("\n".join(msg_lines))

    def test_command_has_frontmatter(self, command_file: Path):
        """Test that command has YAML frontmatter."""
        result = self.validator.validate(command_file)

        frontmatter = result.metadata.get("frontmatter")
        assert frontmatter is not None, f"{command_file.name} is missing frontmatter"

    def test_command_name_format(self, command_file: Path):
        """Test that command name starts with 'cc:'."""
        result = self.validator.validate(command_file)

        frontmatter = result.metadata.get("frontmatter", {})
        name = frontmatter.get("name", "")

        assert name.startswith("cc:"), \
            f"{command_file.name}: name '{name}' should start with 'cc:'"

    def test_command_has_valid_model(self, command_file: Path):
        """Test that command has a valid model."""
        result = self.validator.validate(command_file)

        frontmatter = result.metadata.get("frontmatter", {})
        model = frontmatter.get("model")

        assert model in {"sonnet", "opus", "haiku"}, \
            f"{command_file.name}: invalid model '{model}'"

    def test_command_has_description(self, command_file: Path):
        """Test that command has a description."""
        result = self.validator.validate(command_file)

        frontmatter = result.metadata.get("frontmatter", {})
        description = frontmatter.get("description")

        assert description, f"{command_file.name} is missing description"


class TestCommandContent:
    """Test command content requirements."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up validator for tests."""
        self.validator = CommandValidator()

    def test_command_has_context_section(self, command_file: Path):
        """Test that command has a <context> section."""
        result = self.validator.validate(command_file)

        xml_tags = result.metadata.get("xml_tags", {})
        assert "context" in xml_tags, \
            f"{command_file.name} is missing <context> section"

    def test_command_has_role_section(self, command_file: Path):
        """Test that command has a <role> section."""
        result = self.validator.validate(command_file)

        xml_tags = result.metadata.get("xml_tags", {})
        assert "role" in xml_tags, \
            f"{command_file.name} is missing <role> section"

    def test_command_has_task_section(self, command_file: Path):
        """Test that command has a <task> section."""
        result = self.validator.validate(command_file)

        xml_tags = result.metadata.get("xml_tags", {})
        assert "task" in xml_tags, \
            f"{command_file.name} is missing <task> section"

    def test_command_has_instructions_section(self, command_file: Path):
        """Test that command has an <instructions> section."""
        result = self.validator.validate(command_file)

        xml_tags = result.metadata.get("xml_tags", {})
        assert "instructions" in xml_tags, \
            f"{command_file.name} is missing <instructions> section"

    def test_command_has_output_format_section(self, command_file: Path):
        """Test that command has an <output_format> section."""
        result = self.validator.validate(command_file)

        xml_tags = result.metadata.get("xml_tags", {})
        assert "output_format" in xml_tags, \
            f"{command_file.name} is missing <output_format> section"

    def test_command_has_rules_section(self, command_file: Path):
        """Test that command has a <rules> section."""
        result = self.validator.validate(command_file)

        xml_tags = result.metadata.get("xml_tags", {})
        assert "rules" in xml_tags, \
            f"{command_file.name} is missing <rules> section"


class TestCommandQuality:
    """Test command quality requirements."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up validator for tests."""
        self.validator = CommandValidator()

    def test_command_no_critical_issues(self, command_file: Path):
        """Test that command has no critical (S0) issues."""
        result = self.validator.validate(command_file)

        critical = result.critical_findings
        assert not critical, \
            f"{command_file.name} has critical issues: {[f.code for f in critical]}"

    def test_command_no_high_issues(self, command_file: Path):
        """Test that command has no high (S1) issues."""
        result = self.validator.validate(command_file)

        high = result.high_findings
        assert not high, \
            f"{command_file.name} has high-severity issues: {[f.code for f in high]}"
