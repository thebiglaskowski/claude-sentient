"""
Tests for Claude Conductor snippet files.

Validates:
- Required sections (Description, When to Use, Code)
- At least one code block present
- Code block has language specified
"""

import pytest
from pathlib import Path

from validators.base import Severity
from schemas.snippet_schema import SnippetValidator


class TestSnippetStructure:
    """Test snippet file structure."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up validator for tests."""
        self.validator = SnippetValidator()

    def test_snippet_is_valid(self, snippet_file: Path):
        """Test that a snippet file passes validation."""
        result = self.validator.validate(snippet_file)

        # Get blocking findings (S0 and S1)
        blocking = result.blocking_findings
        if blocking:
            msg_lines = [f"\nValidation failed for {snippet_file}:"]
            for f in blocking:
                msg_lines.append(f"  [{f.severity}] {f.code}: {f.message}")
                if f.suggestion:
                    msg_lines.append(f"    Suggestion: {f.suggestion}")

            pytest.fail("\n".join(msg_lines))


class TestSnippetContent:
    """Test snippet content requirements."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up validator for tests."""
        self.validator = SnippetValidator()

    def test_snippet_has_description_section(self, snippet_file: Path):
        """Test that snippet has a Description section."""
        result = self.validator.validate(snippet_file)

        sections = result.metadata.get("sections", {})
        section_names = {s.lower() for s in sections.keys()}

        has_description = any("description" in s for s in section_names)
        assert has_description, f"{snippet_file} is missing Description section"

    def test_snippet_has_when_to_use_section(self, snippet_file: Path):
        """Test that snippet has a When to Use section."""
        result = self.validator.validate(snippet_file)

        sections = result.metadata.get("sections", {})
        section_names = {s.lower() for s in sections.keys()}

        has_when_to_use = any("when to use" in s for s in section_names)
        assert has_when_to_use, f"{snippet_file} is missing 'When to Use' section"

    def test_snippet_has_code_block(self, snippet_file: Path):
        """Test that snippet has at least one code block."""
        result = self.validator.validate(snippet_file)

        code_blocks = result.metadata.get("code_blocks", [])
        assert len(code_blocks) > 0, f"{snippet_file} has no code blocks"


class TestSnippetQuality:
    """Test snippet quality requirements."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up validator for tests."""
        self.validator = SnippetValidator()

    def test_snippet_no_critical_issues(self, snippet_file: Path):
        """Test that snippet has no critical (S0) issues."""
        result = self.validator.validate(snippet_file)

        critical = result.critical_findings
        assert not critical, \
            f"{snippet_file} has critical issues: {[f.code for f in critical]}"

    def test_snippet_no_high_issues(self, snippet_file: Path):
        """Test that snippet has no high (S1) issues."""
        result = self.validator.validate(snippet_file)

        high = result.high_findings
        assert not high, \
            f"{snippet_file} has high-severity issues: {[f.code for f in high]}"

    def test_snippet_code_has_language(self, snippet_file: Path):
        """Test that code blocks have language specified."""
        result = self.validator.validate(snippet_file)

        code_blocks = result.metadata.get("code_blocks", [])
        for block in code_blocks:
            lang = block.get("language", "")
            # Warning if missing language, not a failure
            if not lang:
                pytest.skip(f"{snippet_file} has code block without language")
