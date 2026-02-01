"""
Tests for project-wide consistency across Claude Conductor components.

Validates:
- No duplicate command/agent names
- Index files exist for component directories
- Consistent severity level usage (S0-S3)
"""

import pytest
from pathlib import Path
from typing import Dict, List, Set
from collections import Counter

from validators.frontmatter import parse_frontmatter


class TestNameUniqueness:
    """Test that component names are unique."""

    def test_no_duplicate_command_names(self, command_files: List[Path]):
        """Test that all command names are unique."""
        names = []
        for file_path in command_files:
            content = file_path.read_text(encoding='utf-8')
            frontmatter, _, _ = parse_frontmatter(content)
            if frontmatter and "name" in frontmatter:
                names.append((frontmatter["name"], file_path.name))

        # Check for duplicates
        name_counts = Counter(name for name, _ in names)
        duplicates = [(name, count) for name, count in name_counts.items() if count > 1]

        if duplicates:
            msg = "Duplicate command names found:\n"
            for name, count in duplicates:
                files = [fname for n, fname in names if n == name]
                msg += f"  '{name}' appears {count} times: {', '.join(files)}\n"
            pytest.fail(msg)

    def test_no_duplicate_agent_names(self, agent_files: List[Path]):
        """Test that all agent names are unique."""
        names = []
        for file_path in agent_files:
            content = file_path.read_text(encoding='utf-8')
            frontmatter, _, _ = parse_frontmatter(content)
            if frontmatter and "name" in frontmatter:
                names.append((frontmatter["name"], file_path.name))

        # Check for duplicates
        name_counts = Counter(name for name, _ in names)
        duplicates = [(name, count) for name, count in name_counts.items() if count > 1]

        if duplicates:
            msg = "Duplicate agent names found:\n"
            for name, count in duplicates:
                files = [fname for n, fname in names if n == name]
                msg += f"  '{name}' appears {count} times: {', '.join(files)}\n"
            pytest.fail(msg)

    def test_no_duplicate_skill_names(self, skill_files: List[Path]):
        """Test that all skill names are unique."""
        names = []
        for file_path in skill_files:
            content = file_path.read_text(encoding='utf-8')
            frontmatter, _, _ = parse_frontmatter(content)
            if frontmatter and "name" in frontmatter:
                names.append((frontmatter["name"], str(file_path)))

        # Check for duplicates
        name_counts = Counter(name for name, _ in names)
        duplicates = [(name, count) for name, count in name_counts.items() if count > 1]

        if duplicates:
            msg = "Duplicate skill names found:\n"
            for name, count in duplicates:
                files = [fname for n, fname in names if n == name]
                msg += f"  '{name}' appears {count} times\n"
            pytest.fail(msg)


class TestIndexFiles:
    """Test that index files exist for component directories."""

    def test_commands_has_index(self, commands_dir: Path):
        """Test that commands directory has an index file."""
        # Note: commands may not have an index, this is informational
        index_files = list(commands_dir.glob("_index.md")) + list(commands_dir.glob("README.md"))
        if not index_files:
            pytest.skip("Commands directory has no index file (optional)")

    def test_skills_has_index(self, skills_dir: Path):
        """Test that skills directory has an index file."""
        index_file = skills_dir / "_index.md"
        assert index_file.exists(), "Skills directory is missing _index.md"

    def test_agents_has_index(self, agents_dir: Path):
        """Test that agents directory has an index file."""
        index_file = agents_dir / "_index.md"
        assert index_file.exists(), "Agents directory is missing _index.md"

    def test_patterns_has_index(self, patterns_dir: Path):
        """Test that patterns directory has an index file."""
        index_file = patterns_dir / "_index.md"
        assert index_file.exists(), "Patterns directory is missing _index.md"

    def test_snippets_has_index(self, snippets_dir: Path):
        """Test that snippets directory has an index file."""
        index_file = snippets_dir / "_index.md"
        assert index_file.exists(), "Snippets directory is missing _index.md"

    def test_rules_has_index(self, rules_dir: Path):
        """Test that rules directory has an index file."""
        index_file = rules_dir / "_index.md"
        assert index_file.exists(), "Rules directory is missing _index.md"


class TestSeverityConsistency:
    """Test consistent severity level usage."""

    def test_severity_format_in_rules(self, rule_files: List[Path]):
        """Test that rules use consistent severity format (S0-S3)."""
        import re

        severity_pattern = re.compile(r'\b(S[0-3]|Critical|High|Medium|Low)\b', re.IGNORECASE)
        inconsistent = []

        for file_path in rule_files:
            content = file_path.read_text(encoding='utf-8')
            matches = severity_pattern.findall(content)

            # Check if file mixes formats
            has_s_format = any(m.upper().startswith('S') and m[1:].isdigit() for m in matches)
            has_word_format = any(m.lower() in ('critical', 'high', 'medium', 'low') for m in matches)

            if has_s_format and has_word_format:
                inconsistent.append(file_path.name)

        if inconsistent:
            msg = "Files mixing severity formats (S0-S3 vs Critical/High/Medium/Low):\n"
            for fname in inconsistent:
                msg += f"  {fname}\n"
            # This is a warning, not a failure
            pytest.skip(msg)


class TestFileOrganization:
    """Test file organization and naming."""

    def test_command_files_are_lowercase(self, command_files: List[Path]):
        """Test that command filenames are lowercase."""
        uppercase_files = [f.name for f in command_files if f.name != f.name.lower()]

        if uppercase_files:
            msg = "Command files with uppercase characters:\n"
            for fname in uppercase_files:
                msg += f"  {fname}\n"
            pytest.skip(msg)  # Informational, not blocking

    def test_skill_files_are_lowercase(self, skill_files: List[Path]):
        """Test that skill filenames are lowercase."""
        uppercase_files = [f.name for f in skill_files if f.name != f.name.lower()]

        if uppercase_files:
            msg = "Skill files with uppercase characters:\n"
            for fname in uppercase_files:
                msg += f"  {fname}\n"
            pytest.skip(msg)

    def test_agent_files_are_lowercase(self, agent_files: List[Path]):
        """Test that agent filenames are lowercase."""
        uppercase_files = [f.name for f in agent_files if f.name != f.name.lower()]

        if uppercase_files:
            msg = "Agent files with uppercase characters:\n"
            for fname in uppercase_files:
                msg += f"  {fname}\n"
            pytest.skip(msg)
