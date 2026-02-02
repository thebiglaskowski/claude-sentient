"""
Pytest configuration and shared fixtures for Claude Conductor component tests.

Provides:
- Path fixtures for component directories
- Registry fixtures for cross-reference validation
- Parameterized test helpers
"""

import sys
from pathlib import Path
from typing import Dict, List

import pytest


# Add validators and schemas to path
TEST_DIR = Path(__file__).parent
sys.path.insert(0, str(TEST_DIR))

# Base path to .claude directory
CLAUDE_DIR = TEST_DIR.parent

# Component directories
COMMANDS_DIR = CLAUDE_DIR / "commands"
SKILLS_DIR = CLAUDE_DIR / "skills"
AGENTS_DIR = CLAUDE_DIR / "agents"
PATTERNS_DIR = CLAUDE_DIR / "patterns"
SNIPPETS_DIR = CLAUDE_DIR / "snippets"
RULES_DIR = CLAUDE_DIR / "rules"


def get_component_files(directory: Path, recursive: bool = False) -> List[Path]:
    """
    Get all markdown files in a component directory.

    Excludes:
    - Files starting with underscore (e.g., _index.md)
    - README files

    Args:
        directory: Directory to search
        recursive: Whether to search subdirectories

    Returns:
        List of Path objects for component files
    """
    if not directory.exists():
        return []

    pattern = "**/*.md" if recursive else "*.md"
    files = []
    for f in directory.glob(pattern):
        if f.is_file() and not f.name.startswith("_") and f.name.lower() != "readme.md":
            files.append(f)
    return sorted(files)


# ============================================================================
# Path Fixtures
# ============================================================================

@pytest.fixture
def claude_dir() -> Path:
    """Return the path to the .claude directory."""
    return CLAUDE_DIR


@pytest.fixture
def commands_dir() -> Path:
    """Return the path to the commands directory."""
    return COMMANDS_DIR


@pytest.fixture
def skills_dir() -> Path:
    """Return the path to the skills directory."""
    return SKILLS_DIR


@pytest.fixture
def agents_dir() -> Path:
    """Return the path to the agents directory."""
    return AGENTS_DIR


@pytest.fixture
def patterns_dir() -> Path:
    """Return the path to the patterns directory."""
    return PATTERNS_DIR


@pytest.fixture
def snippets_dir() -> Path:
    """Return the path to the snippets directory."""
    return SNIPPETS_DIR


@pytest.fixture
def rules_dir() -> Path:
    """Return the path to the rules directory."""
    return RULES_DIR


# ============================================================================
# File Collection Fixtures
# ============================================================================

@pytest.fixture
def command_files() -> List[Path]:
    """Return list of all command files."""
    return get_component_files(COMMANDS_DIR)


@pytest.fixture
def skill_files() -> List[Path]:
    """Return list of all skill files (including subdirectories)."""
    return get_component_files(SKILLS_DIR, recursive=True)


@pytest.fixture
def agent_files() -> List[Path]:
    """Return list of all agent files."""
    return get_component_files(AGENTS_DIR)


@pytest.fixture
def pattern_files() -> List[Path]:
    """Return list of all pattern files (including subdirectories)."""
    return get_component_files(PATTERNS_DIR, recursive=True)


@pytest.fixture
def snippet_files() -> List[Path]:
    """Return list of all snippet files (including subdirectories)."""
    return get_component_files(SNIPPETS_DIR, recursive=True)


@pytest.fixture
def rule_files() -> List[Path]:
    """Return list of all rule files."""
    return get_component_files(RULES_DIR)


# ============================================================================
# Validator Fixtures
# ============================================================================

@pytest.fixture
def cross_reference_registry():
    """Return a CrossReferenceRegistry for validation."""
    from validators.cross_reference import CrossReferenceRegistry
    return CrossReferenceRegistry(CLAUDE_DIR)


# ============================================================================
# Parameterization Helpers
# ============================================================================

def pytest_generate_tests(metafunc):
    """
    Generate test parameters for component file tests.

    This allows tests to be parameterized with all files of a given type.
    """
    if "command_file" in metafunc.fixturenames:
        files = get_component_files(COMMANDS_DIR)
        metafunc.parametrize("command_file", files, ids=[f.stem for f in files])

    if "skill_file" in metafunc.fixturenames:
        files = get_component_files(SKILLS_DIR, recursive=True)
        # Use relative path as ID for skills (they're in subdirectories)
        ids = [str(f.relative_to(SKILLS_DIR)).replace("\\", "/") for f in files]
        metafunc.parametrize("skill_file", files, ids=ids)

    if "agent_file" in metafunc.fixturenames:
        files = get_component_files(AGENTS_DIR)
        metafunc.parametrize("agent_file", files, ids=[f.stem for f in files])

    if "pattern_file" in metafunc.fixturenames:
        files = get_component_files(PATTERNS_DIR, recursive=True)
        ids = [str(f.relative_to(PATTERNS_DIR)).replace("\\", "/") for f in files]
        metafunc.parametrize("pattern_file", files, ids=ids)

    if "snippet_file" in metafunc.fixturenames:
        files = get_component_files(SNIPPETS_DIR, recursive=True)
        ids = [str(f.relative_to(SNIPPETS_DIR)).replace("\\", "/") for f in files]
        metafunc.parametrize("snippet_file", files, ids=ids)

    if "rule_file" in metafunc.fixturenames:
        files = get_component_files(RULES_DIR)
        metafunc.parametrize("rule_file", files, ids=[f.stem for f in files])


# ============================================================================
# Summary Helpers
# ============================================================================

def summarize_findings(findings: List) -> Dict[str, int]:
    """
    Summarize validation findings by severity.

    Args:
        findings: List of ValidationFinding objects

    Returns:
        Dictionary with severity counts
    """
    summary = {"S0": 0, "S1": 0, "S2": 0, "S3": 0}
    for finding in findings:
        severity = str(finding.severity)
        if severity in summary:
            summary[severity] += 1
    return summary


def format_findings(findings: List) -> str:
    """
    Format findings for test output.

    Args:
        findings: List of ValidationFinding objects

    Returns:
        Formatted string of findings
    """
    if not findings:
        return "No findings"

    lines = []
    for f in findings:
        location = f"{f.file_path.name}"
        if f.line_number:
            location += f":{f.line_number}"
        lines.append(f"[{f.severity}] {f.code}: {f.message}")
        if f.suggestion:
            lines.append(f"    Suggestion: {f.suggestion}")
    return "\n".join(lines)
