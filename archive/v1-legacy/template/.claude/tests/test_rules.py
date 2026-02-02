"""
Tests for Claude Conductor rule files.

Validates:
- Required sections (Core Principles)
- Sufficient content depth
- No frontmatter (rules don't use frontmatter)
"""

import pytest
from pathlib import Path

from validators.base import Severity
from schemas.rule_schema import RuleValidator


class TestRuleStructure:
    """Test rule file structure."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up validator for tests."""
        self.validator = RuleValidator()

    def test_rule_is_valid(self, rule_file: Path):
        """Test that a rule file passes validation."""
        result = self.validator.validate(rule_file)

        # Get blocking findings (S0 and S1)
        blocking = result.blocking_findings
        if blocking:
            msg_lines = [f"\nValidation failed for {rule_file.name}:"]
            for f in blocking:
                msg_lines.append(f"  [{f.severity}] {f.code}: {f.message}")
                if f.suggestion:
                    msg_lines.append(f"    Suggestion: {f.suggestion}")

            pytest.fail("\n".join(msg_lines))


class TestRuleContent:
    """Test rule content requirements."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up validator for tests."""
        self.validator = RuleValidator()

    def test_rule_has_core_principles(self, rule_file: Path):
        """Test that rule has a Core Principles section."""
        result = self.validator.validate(rule_file)

        sections = result.metadata.get("sections", {})
        section_names = {s.lower() for s in sections.keys()}

        has_principles = any("core principles" in s or "principles" in s for s in section_names)
        assert has_principles, f"{rule_file.name} is missing Core Principles section"

    def test_rule_has_sufficient_content(self, rule_file: Path):
        """Test that rule has sufficient content."""
        content = rule_file.read_text(encoding='utf-8')

        # Rules should be comprehensive
        assert len(content.strip()) >= 500, \
            f"{rule_file.name} has insufficient content ({len(content.strip())} chars)"


class TestRuleQuality:
    """Test rule quality requirements."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up validator for tests."""
        self.validator = RuleValidator()

    def test_rule_no_critical_issues(self, rule_file: Path):
        """Test that rule has no critical (S0) issues."""
        result = self.validator.validate(rule_file)

        critical = result.critical_findings
        assert not critical, \
            f"{rule_file.name} has critical issues: {[f.code for f in critical]}"

    def test_rule_no_high_issues(self, rule_file: Path):
        """Test that rule has no high (S1) issues."""
        result = self.validator.validate(rule_file)

        high = result.high_findings
        assert not high, \
            f"{rule_file.name} has high-severity issues: {[f.code for f in high]}"

    def test_rule_has_multiple_sections(self, rule_file: Path):
        """Test that rule has multiple sections (comprehensive coverage)."""
        result = self.validator.validate(rule_file)

        sections = result.metadata.get("sections", {})
        # Rules should be comprehensive with multiple sections
        assert len(sections) >= 3, \
            f"{rule_file.name} has only {len(sections)} sections (should be comprehensive)"
