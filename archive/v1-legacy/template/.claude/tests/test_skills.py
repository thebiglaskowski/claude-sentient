"""
Tests for Claude Conductor skill files.

Validates:
- YAML frontmatter structure (name, description)
- Optional fields are correct types (triggers, tags, model)
- Content has sufficient depth
"""

import pytest
from pathlib import Path

from validators.base import Severity
from schemas.skill_schema import SkillValidator


class TestSkillStructure:
    """Test skill file structure."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up validator for tests."""
        self.validator = SkillValidator()

    def test_skill_is_valid(self, skill_file: Path):
        """Test that a skill file passes validation."""
        result = self.validator.validate(skill_file)

        # Get blocking findings (S0 and S1)
        blocking = result.blocking_findings
        if blocking:
            msg_lines = [f"\nValidation failed for {skill_file}:"]
            for f in blocking:
                msg_lines.append(f"  [{f.severity}] {f.code}: {f.message}")
                if f.suggestion:
                    msg_lines.append(f"    Suggestion: {f.suggestion}")

            pytest.fail("\n".join(msg_lines))

    def test_skill_has_frontmatter(self, skill_file: Path):
        """Test that skill has YAML frontmatter."""
        result = self.validator.validate(skill_file)

        frontmatter = result.metadata.get("frontmatter")
        assert frontmatter is not None, f"{skill_file} is missing frontmatter"

    def test_skill_has_name(self, skill_file: Path):
        """Test that skill has a name."""
        result = self.validator.validate(skill_file)

        frontmatter = result.metadata.get("frontmatter", {})
        name = frontmatter.get("name")

        assert name, f"{skill_file} is missing name"

    def test_skill_has_description(self, skill_file: Path):
        """Test that skill has a description."""
        result = self.validator.validate(skill_file)

        frontmatter = result.metadata.get("frontmatter", {})
        description = frontmatter.get("description")

        assert description, f"{skill_file} is missing description"


class TestSkillContent:
    """Test skill content requirements."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up validator for tests."""
        self.validator = SkillValidator()

    def test_skill_has_sufficient_content(self, skill_file: Path):
        """Test that skill has sufficient content."""
        content = skill_file.read_text(encoding='utf-8')

        # Remove frontmatter from count
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                content = parts[2]

        # Skill content should be meaningful
        assert len(content.strip()) >= 50, \
            f"{skill_file} has insufficient content ({len(content.strip())} chars)"


class TestSkillQuality:
    """Test skill quality requirements."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up validator for tests."""
        self.validator = SkillValidator()

    def test_skill_no_critical_issues(self, skill_file: Path):
        """Test that skill has no critical (S0) issues."""
        result = self.validator.validate(skill_file)

        critical = result.critical_findings
        assert not critical, \
            f"{skill_file} has critical issues: {[f.code for f in critical]}"

    def test_skill_no_high_issues(self, skill_file: Path):
        """Test that skill has no high (S1) issues."""
        result = self.validator.validate(skill_file)

        high = result.high_findings
        assert not high, \
            f"{skill_file} has high-severity issues: {[f.code for f in high]}"

    def test_skill_model_is_valid(self, skill_file: Path):
        """Test that skill model is valid if specified."""
        result = self.validator.validate(skill_file)

        frontmatter = result.metadata.get("frontmatter", {})
        model = frontmatter.get("model")

        if model is not None:
            assert model in {"sonnet", "opus", "haiku"}, \
                f"{skill_file}: invalid model '{model}'"

    def test_skill_triggers_is_list(self, skill_file: Path):
        """Test that triggers is a list if specified."""
        result = self.validator.validate(skill_file)

        frontmatter = result.metadata.get("frontmatter", {})
        triggers = frontmatter.get("triggers") or frontmatter.get("trigger")

        if triggers is not None:
            assert isinstance(triggers, list), \
                f"{skill_file}: triggers should be a list, got {type(triggers).__name__}"
