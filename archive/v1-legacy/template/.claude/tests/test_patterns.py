"""
Tests for Claude Conductor pattern files.

Validates:
- Required sections (Intent, When to Use, When NOT to Use)
- Code examples present
- Multiple language examples (recommended)
"""

import pytest
from pathlib import Path

from validators.base import Severity
from schemas.pattern_schema import PatternValidator


class TestPatternStructure:
    """Test pattern file structure."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up validator for tests."""
        self.validator = PatternValidator()

    def test_pattern_is_valid(self, pattern_file: Path):
        """Test that a pattern file passes validation."""
        result = self.validator.validate(pattern_file)

        # Get blocking findings (S0 and S1)
        blocking = result.blocking_findings
        if blocking:
            msg_lines = [f"\nValidation failed for {pattern_file}:"]
            for f in blocking:
                msg_lines.append(f"  [{f.severity}] {f.code}: {f.message}")
                if f.suggestion:
                    msg_lines.append(f"    Suggestion: {f.suggestion}")

            pytest.fail("\n".join(msg_lines))


class TestPatternContent:
    """Test pattern content requirements."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up validator for tests."""
        self.validator = PatternValidator()

    def test_pattern_has_intent_section(self, pattern_file: Path):
        """Test that pattern has an Intent section."""
        result = self.validator.validate(pattern_file)

        sections = result.metadata.get("sections", {})
        section_names = {s.lower() for s in sections.keys()}

        has_intent = any("intent" in s for s in section_names)
        assert has_intent, f"{pattern_file} is missing Intent section"

    def test_pattern_has_when_to_use_section(self, pattern_file: Path):
        """Test that pattern has a When to Use section."""
        result = self.validator.validate(pattern_file)

        sections = result.metadata.get("sections", {})
        section_names = {s.lower() for s in sections.keys()}

        has_when_to_use = any("when to use" in s for s in section_names)
        assert has_when_to_use, f"{pattern_file} is missing 'When to Use' section"

    def test_pattern_has_code_examples(self, pattern_file: Path):
        """Test that pattern has code examples."""
        result = self.validator.validate(pattern_file)

        code_blocks = result.metadata.get("code_blocks", [])
        assert len(code_blocks) > 0, f"{pattern_file} has no code examples"


class TestPatternQuality:
    """Test pattern quality requirements."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up validator for tests."""
        self.validator = PatternValidator()

    def test_pattern_no_critical_issues(self, pattern_file: Path):
        """Test that pattern has no critical (S0) issues."""
        result = self.validator.validate(pattern_file)

        critical = result.critical_findings
        assert not critical, \
            f"{pattern_file} has critical issues: {[f.code for f in critical]}"

    def test_pattern_no_high_issues(self, pattern_file: Path):
        """Test that pattern has no high (S1) issues."""
        result = self.validator.validate(pattern_file)

        high = result.high_findings
        assert not high, \
            f"{pattern_file} has high-severity issues: {[f.code for f in high]}"

    def test_pattern_has_multiple_languages(self, pattern_file: Path):
        """Test that pattern has examples in multiple languages (warning only)."""
        result = self.validator.validate(pattern_file)

        languages = result.metadata.get("languages_found", [])
        # This is informational, not a failure
        if len(languages) < 2:
            pytest.skip(f"{pattern_file} only has {len(languages)} language(s)")
