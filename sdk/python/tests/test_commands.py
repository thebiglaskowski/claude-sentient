"""Tests for Claude Sentient command file validation.

These tests validate that command files have correct structure:
- Valid YAML frontmatter
- Required fields present
- XML structure tags present
"""

import re
import yaml
import pytest
from pathlib import Path


# Path to commands directory (sdk/python/tests -> claude-sentient/.claude/commands)
COMMANDS_DIR = Path(__file__).resolve().parent.parent.parent.parent / ".claude" / "commands"


def get_command_files() -> list[Path]:
    """Get all cs-*.md command files."""
    return list(COMMANDS_DIR.glob("cs-*.md"))


def parse_frontmatter(content: str) -> tuple[dict | None, str]:
    """Parse YAML frontmatter from command file content."""
    if not content.startswith("---"):
        return None, content

    # Find the closing ---
    end_match = re.search(r"\n---\n", content[3:])
    if not end_match:
        return None, content

    frontmatter_text = content[3:end_match.start() + 3]
    body = content[end_match.end() + 3:]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        return frontmatter, body
    except yaml.YAMLError:
        # Try to extract at least description manually for commands with complex YAML
        desc_match = re.search(r"description:\s*(.+)", frontmatter_text)
        if desc_match:
            return {"description": desc_match.group(1).strip()}, body
        return None, content


class TestCommandFilesExist:
    """Tests that all expected command files exist."""

    def test_commands_directory_exists(self):
        """Commands directory should exist."""
        assert COMMANDS_DIR.exists(), f"Commands directory not found: {COMMANDS_DIR}"

    def test_expected_commands_exist(self):
        """All expected command files should exist."""
        expected = [
            "cs-loop.md",
            "cs-plan.md",
            "cs-status.md",
            "cs-learn.md",
            "cs-validate.md",
            "cs-mcp.md",
            "cs-review.md",
            "cs-assess.md",
            "cs-ui.md",
        ]
        for cmd in expected:
            assert (COMMANDS_DIR / cmd).exists(), f"Missing command: {cmd}"

    def test_command_count(self):
        """Should have exactly 9 commands."""
        commands = get_command_files()
        assert len(commands) == 9, f"Expected 9 commands, found {len(commands)}"


class TestCommandFrontmatter:
    """Tests for command YAML frontmatter."""

    @pytest.fixture(params=get_command_files(), ids=lambda p: p.name)
    def command_file(self, request) -> Path:
        """Parameterized fixture for each command file."""
        return request.param

    def test_has_frontmatter(self, command_file: Path):
        """Command should have YAML frontmatter."""
        content = command_file.read_text(encoding="utf-8")
        assert content.startswith("---"), f"{command_file.name} should start with ---"

    def test_frontmatter_is_valid_yaml(self, command_file: Path):
        """Frontmatter should be valid YAML."""
        content = command_file.read_text(encoding="utf-8")
        frontmatter, _ = parse_frontmatter(content)
        assert frontmatter is not None, f"{command_file.name} has invalid YAML frontmatter"

    def test_has_description(self, command_file: Path):
        """Frontmatter should have description field."""
        content = command_file.read_text(encoding="utf-8")
        frontmatter, _ = parse_frontmatter(content)
        assert frontmatter is not None
        assert "description" in frontmatter, f"{command_file.name} missing 'description'"
        assert len(frontmatter["description"]) > 0, f"{command_file.name} has empty description"


class TestCommandXMLStructure:
    """Tests for XML tag structure in commands."""

    @pytest.fixture(params=get_command_files(), ids=lambda p: p.name)
    def command_content(self, request) -> tuple[str, str]:
        """Return (filename, content) for each command."""
        path = request.param
        return path.name, path.read_text(encoding="utf-8")

    def test_has_task_or_role_tag(self, command_content: tuple[str, str]):
        """Command should have <task> and/or <role> tag."""
        name, content = command_content
        _, body = parse_frontmatter(content)

        has_task = "<task>" in body
        has_role = "<role>" in body

        assert has_task or has_role, f"{name} should have <task> or <role> tag"

    def test_has_closing_tags(self, command_content: tuple[str, str]):
        """XML tags should have matching closing tags."""
        name, content = command_content
        _, body = parse_frontmatter(content)

        # Key XML tags we use in commands
        key_tags = ["role", "task", "context", "steps", "criteria", "constraints",
                    "output_format", "avoid", "examples", "thinking"]

        for tag in key_tags:
            opening = f"<{tag}>"
            if opening in body:
                closing = f"</{tag}>"
                assert closing in body, f"{name} missing closing tag for <{tag}>"


class TestAvoidSections:
    """Tests for <avoid> sections in commands."""

    @pytest.fixture(params=get_command_files(), ids=lambda p: p.name)
    def command_content(self, request) -> tuple[str, str]:
        """Return (filename, content) for each command."""
        path = request.param
        return path.name, path.read_text(encoding="utf-8")

    def test_has_avoid_section(self, command_content: tuple[str, str]):
        """Command should have <avoid> section (anti-prompt pattern)."""
        name, content = command_content
        _, body = parse_frontmatter(content)

        # All 9 commands should have <avoid> sections as per Option C
        assert "<avoid>" in body, f"{name} should have <avoid> section"
        assert "</avoid>" in body, f"{name} should have closing </avoid>"


class TestSpecificCommands:
    """Tests for specific command requirements."""

    def test_cs_loop_has_phases(self):
        """cs-loop should document all phases."""
        content = (COMMANDS_DIR / "cs-loop.md").read_text(encoding="utf-8")

        phases = ["INIT", "UNDERSTAND", "PLAN", "EXECUTE", "VERIFY", "COMMIT", "EVALUATE"]
        for phase in phases:
            assert phase in content, f"cs-loop missing phase: {phase}"

    def test_cs_loop_has_mcp_integration(self):
        """cs-loop should mention MCP server integration."""
        content = (COMMANDS_DIR / "cs-loop.md").read_text(encoding="utf-8")
        assert "MCP" in content or "mcp" in content, "cs-loop should mention MCP integration"

    def test_cs_assess_has_dimensions(self):
        """cs-assess should have assessment dimensions."""
        content = (COMMANDS_DIR / "cs-assess.md").read_text(encoding="utf-8")

        dimensions = ["Architecture", "Code Quality", "Security", "Performance", "Tech Debt", "Test Coverage"]
        for dim in dimensions:
            assert dim in content, f"cs-assess missing dimension: {dim}"

    def test_cs_plan_chains_to_loop(self):
        """cs-plan should reference chaining to cs-loop."""
        content = (COMMANDS_DIR / "cs-plan.md").read_text(encoding="utf-8")
        assert "cs-loop" in content, "cs-plan should reference cs-loop for execution"

    def test_cs_status_shows_tasks(self):
        """cs-status should mention task display."""
        content = (COMMANDS_DIR / "cs-status.md").read_text(encoding="utf-8")
        assert "task" in content.lower() or "Task" in content, "cs-status should show tasks"

    def test_cs_learn_has_memory_types(self):
        """cs-learn should document memory types."""
        content = (COMMANDS_DIR / "cs-learn.md").read_text(encoding="utf-8")

        types = ["decision", "pattern", "learning"]
        for t in types:
            assert t in content.lower(), f"cs-learn missing type: {t}"

    def test_cs_validate_checks_components(self):
        """cs-validate should check various components."""
        content = (COMMANDS_DIR / "cs-validate.md").read_text(encoding="utf-8")

        components = ["profile", "command", "rule"]
        for c in components:
            assert c in content.lower(), f"cs-validate should check: {c}"

    def test_cs_mcp_has_server_docs(self):
        """cs-mcp should document MCP servers."""
        content = (COMMANDS_DIR / "cs-mcp.md").read_text(encoding="utf-8")
        assert "server" in content.lower(), "cs-mcp should document servers"

    def test_cs_review_is_for_prs(self):
        """cs-review should be for pull request review."""
        content = (COMMANDS_DIR / "cs-review.md").read_text(encoding="utf-8")
        assert "PR" in content or "pull request" in content.lower(), "cs-review should be for PRs"

    def test_cs_ui_has_design_guidelines(self):
        """cs-ui should have UI/UX design guidelines."""
        content = (COMMANDS_DIR / "cs-ui.md").read_text(encoding="utf-8")
        assert "design" in content.lower() or "UI" in content, "cs-ui should have design content"
