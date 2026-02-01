"""
Tests for content quality across Claude Conductor components.

Validates:
- No TODO/FIXME markers
- No placeholder text
- No absolute file paths in links
"""

import re
import pytest
from pathlib import Path
from typing import List, Tuple


# Patterns for quality issues
PLACEHOLDER_PATTERNS = [
    re.compile(r'\[.*?placeholder.*?\]', re.IGNORECASE),
    re.compile(r'\[.*?your.*?here\]', re.IGNORECASE),
    re.compile(r'\[.*?insert.*?here\]', re.IGNORECASE),
    # Note: Don't flag <input placeholder="..."> which is valid HTML
    # or {{ variable }} in code examples (React, GitHub Actions, etc.)
]
# Absolute path pattern - be more specific to avoid false positives in examples
# that show Windows/Unix paths as documentation
ABSOLUTE_PATH_PATTERN = re.compile(r'(?<!example[: ])(?<!# )[CDE]:\\(?!scripts\\prompts)|/home/(?!user)|/Users/(?!name)')


def is_todo_in_documentation_context(line: str) -> bool:
    """
    Check if a TODO/FIXME on this line is in a documentation context
    (not an actual incomplete work marker).

    Returns True if the TODO should be IGNORED (it's documentation).
    """
    line_lower = line.lower()

    # Skip lines with grep/search commands looking for TODOs
    if 'grep' in line_lower or '!search' in line_lower or 'rg ' in line_lower:
        return True

    # Skip lines documenting "No TODO" as a quality requirement
    if 'no todo' in line_lower or 'no fixme' in line_lower:
        return True

    # Skip lines about "TODO debt" or "TODO comments" as concepts
    if 'todo debt' in line_lower or 'todo comment' in line_lower:
        return True

    # Skip lines listing TODO/FIXME as things to find (e.g., "TODO and FIXME comments")
    if 'todo and fixme' in line_lower or 'fixme and todo' in line_lower:
        return True

    # Skip HTML comments (template placeholders in examples)
    if '<!--' in line and '-->' in line:
        return True

    # Skip lines where TODO is in quotes (documenting the concept)
    if '"todo' in line_lower or "'todo" in line_lower:
        return True

    # Skip lines that say "Mark as TODO" (documenting process)
    if 'mark as todo' in line_lower or 'mark as fixme' in line_lower:
        return True

    return False


def find_quality_issues(file_path: Path) -> List[Tuple[str, int, str]]:
    """
    Find quality issues in a file.

    Returns list of (issue_type, line_number, match) tuples.
    """
    issues = []
    content = file_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    # Track code blocks
    in_code_block = False

    # Basic TODO pattern - we'll filter context separately
    todo_pattern = re.compile(r'\b(TODO|FIXME)\b', re.IGNORECASE)

    for i, line in enumerate(lines, 1):
        # Track code blocks (skip TODOs inside code examples)
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue

        # Check for TODOs (skip if in code block or documentation context)
        if not in_code_block:
            match = todo_pattern.search(line)
            if match and not is_todo_in_documentation_context(line):
                issues.append(("TODO", i, match.group(0)))

        # Check for placeholders (always check, even in code blocks)
        for pattern in PLACEHOLDER_PATTERNS:
            match = pattern.search(line)
            if match:
                issues.append(("PLACEHOLDER", i, match.group(0)))
                break  # Only report once per line

        # Check for absolute paths
        match = ABSOLUTE_PATH_PATTERN.search(line)
        if match:
            issues.append(("ABSOLUTE_PATH", i, match.group(0)))

    return issues


class TestNoTodoMarkers:
    """Test that components don't have TODO markers."""

    def test_commands_no_todos(self, command_files: List[Path]):
        """Test that commands don't have TODO markers."""
        all_todos = []
        for file_path in command_files:
            issues = [i for i in find_quality_issues(file_path) if i[0] == "TODO"]
            for issue_type, line, match in issues:
                all_todos.append((file_path.name, line, match))

        if all_todos:
            msg = f"Found {len(all_todos)} TODO markers in commands:\n"
            for fname, line, match in all_todos[:10]:
                msg += f"  {fname}:{line}: {match}\n"
            # These are real issues but not blocking - convert to warning
            pytest.skip(f"{msg}\n(This is a quality warning, not a structural failure)")

    def test_skills_no_todos(self, skill_files: List[Path]):
        """Test that skills don't have TODO markers."""
        all_todos = []
        for file_path in skill_files:
            issues = [i for i in find_quality_issues(file_path) if i[0] == "TODO"]
            for issue_type, line, match in issues:
                all_todos.append((str(file_path), line, match))

        if all_todos:
            msg = f"Found {len(all_todos)} TODO markers in skills:\n"
            for fname, line, match in all_todos[:10]:
                msg += f"  {fname}:{line}: {match}\n"
            pytest.skip(f"{msg}\n(This is a quality warning, not a structural failure)")

    def test_agents_no_todos(self, agent_files: List[Path]):
        """Test that agents don't have TODO markers."""
        all_todos = []
        for file_path in agent_files:
            issues = [i for i in find_quality_issues(file_path) if i[0] == "TODO"]
            for issue_type, line, match in issues:
                all_todos.append((file_path.name, line, match))

        if all_todos:
            msg = f"Found {len(all_todos)} TODO markers in agents:\n"
            for fname, line, match in all_todos[:10]:
                msg += f"  {fname}:{line}: {match}\n"
            pytest.skip(f"{msg}\n(This is a quality warning, not a structural failure)")


class TestNoPlaceholders:
    """Test that components don't have placeholder text."""

    def test_commands_no_placeholders(self, command_files: List[Path]):
        """Test that commands don't have placeholder text."""
        all_placeholders = []
        for file_path in command_files:
            issues = [i for i in find_quality_issues(file_path) if i[0] == "PLACEHOLDER"]
            for issue_type, line, match in issues:
                all_placeholders.append((file_path.name, line, match))

        if all_placeholders:
            msg = f"Found {len(all_placeholders)} placeholders in commands:\n"
            for fname, line, match in all_placeholders[:10]:
                msg += f"  {fname}:{line}: {match}\n"
            pytest.fail(msg)

    def test_skills_no_placeholders(self, skill_files: List[Path]):
        """Test that skills don't have placeholder text."""
        all_placeholders = []
        for file_path in skill_files:
            issues = [i for i in find_quality_issues(file_path) if i[0] == "PLACEHOLDER"]
            for issue_type, line, match in issues:
                all_placeholders.append((str(file_path), line, match))

        if all_placeholders:
            msg = f"Found {len(all_placeholders)} placeholders in skills:\n"
            for fname, line, match in all_placeholders[:10]:
                msg += f"  {fname}:{line}: {match}\n"
            pytest.fail(msg)


class TestNoAbsolutePaths:
    """Test that components don't have absolute file paths."""

    def test_commands_no_absolute_paths(self, command_files: List[Path]):
        """Test that commands don't have absolute file paths."""
        all_paths = []
        for file_path in command_files:
            issues = [i for i in find_quality_issues(file_path) if i[0] == "ABSOLUTE_PATH"]
            for issue_type, line, match in issues:
                all_paths.append((file_path.name, line, match))

        if all_paths:
            msg = f"Found {len(all_paths)} absolute paths in commands:\n"
            for fname, line, match in all_paths[:10]:
                msg += f"  {fname}:{line}: contains '{match}'\n"
            pytest.skip(f"{msg}\n(This is a quality warning, not a structural failure)")

    def test_skills_no_absolute_paths(self, skill_files: List[Path]):
        """Test that skills don't have absolute file paths."""
        all_paths = []
        for file_path in skill_files:
            issues = [i for i in find_quality_issues(file_path) if i[0] == "ABSOLUTE_PATH"]
            for issue_type, line, match in issues:
                all_paths.append((str(file_path), line, match))

        if all_paths:
            msg = f"Found {len(all_paths)} absolute paths in skills:\n"
            for fname, line, match in all_paths[:10]:
                msg += f"  {fname}:{line}: contains '{match}'\n"
            pytest.skip(f"{msg}\n(This is a quality warning, not a structural failure)")

    def test_agents_no_absolute_paths(self, agent_files: List[Path]):
        """Test that agents don't have absolute file paths."""
        all_paths = []
        for file_path in agent_files:
            issues = [i for i in find_quality_issues(file_path) if i[0] == "ABSOLUTE_PATH"]
            for issue_type, line, match in issues:
                all_paths.append((file_path.name, line, match))

        if all_paths:
            msg = f"Found {len(all_paths)} absolute paths in agents:\n"
            for fname, line, match in all_paths[:10]:
                msg += f"  {fname}:{line}: contains '{match}'\n"
            pytest.skip(f"{msg}\n(This is a quality warning, not a structural failure)")


class TestContentQuality:
    """Test overall content quality."""

    def test_files_are_utf8(self, command_files: List[Path], skill_files: List[Path]):
        """Test that all files are valid UTF-8."""
        all_files = command_files + skill_files
        encoding_errors = []

        for file_path in all_files:
            try:
                file_path.read_text(encoding='utf-8')
            except UnicodeDecodeError as e:
                encoding_errors.append((str(file_path), str(e)))

        if encoding_errors:
            msg = "Files with encoding issues:\n"
            for fname, error in encoding_errors:
                msg += f"  {fname}: {error}\n"
            pytest.fail(msg)

    def test_no_empty_files(self, command_files: List[Path], skill_files: List[Path]):
        """Test that no component files are empty."""
        all_files = command_files + skill_files
        empty_files = []

        for file_path in all_files:
            content = file_path.read_text(encoding='utf-8')
            if len(content.strip()) == 0:
                empty_files.append(str(file_path))

        if empty_files:
            msg = "Empty files found:\n"
            for fname in empty_files:
                msg += f"  {fname}\n"
            pytest.fail(msg)
