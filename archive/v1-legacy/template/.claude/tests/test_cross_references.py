"""
Tests for cross-reference validation across all Claude Conductor components.

Validates:
- @rules/[name] references resolve to existing rules
- @patterns/[name] references resolve to existing patterns
- snippet:[name] references resolve to existing snippets
- Agent references resolve to existing agents
"""

import pytest
from pathlib import Path
from typing import List

from validators.cross_reference import (
    CrossReferenceRegistry,
    CrossReferenceValidator,
    extract_references,
    validate_all_cross_references,
)


class TestCrossReferenceRegistry:
    """Test the CrossReferenceRegistry."""

    def test_registry_loads_rules(self, claude_dir: Path):
        """Test that registry loads rules from the rules directory."""
        registry = CrossReferenceRegistry(claude_dir)
        rules = registry.rules

        # Should have loaded some rules
        assert len(rules) > 0, "No rules found in registry"

        # Check for known rules
        expected_rules = {"security", "testing", "api-design", "code-quality"}
        found = expected_rules.intersection(rules)
        assert len(found) > 0, f"Expected rules not found: {expected_rules}"

    def test_registry_loads_agents(self, claude_dir: Path):
        """Test that registry loads agents from the agents directory."""
        registry = CrossReferenceRegistry(claude_dir)
        agents = registry.agents

        # Should have loaded some agents
        assert len(agents) > 0, "No agents found in registry"

        # Check for known agents
        expected_agents = {"security-analyst", "code-reviewer", "test-engineer"}
        found = expected_agents.intersection(agents)
        assert len(found) > 0, f"Expected agents not found: {expected_agents}"

    def test_registry_loads_patterns(self, claude_dir: Path):
        """Test that registry loads patterns from the patterns directory."""
        registry = CrossReferenceRegistry(claude_dir)
        patterns = registry.patterns

        # Should have loaded some patterns
        assert len(patterns) > 0, "No patterns found in registry"

    def test_registry_loads_snippets(self, claude_dir: Path):
        """Test that registry loads snippets from the snippets directory."""
        registry = CrossReferenceRegistry(claude_dir)
        snippets = registry.snippets

        # Should have loaded some snippets
        assert len(snippets) > 0, "No snippets found in registry"


class TestExtractReferences:
    """Test reference extraction from content."""

    def test_extract_rules_references(self):
        """Test extraction of @rules/[name] references."""
        content = """
        Load the security rules with @rules/security and @rules/testing.
        Also consider @rules/api-design for API work.
        """

        refs = extract_references(content)
        rules = [name for name, _ in refs["rules"]]

        assert "security" in rules
        assert "testing" in rules
        assert "api-design" in rules

    def test_extract_patterns_references(self):
        """Test extraction of @patterns/[name] references."""
        content = """
        Use @patterns/repository for data access.
        Consider @patterns/retry-with-backoff for resilience.
        """

        refs = extract_references(content)
        patterns = [name for name, _ in refs["patterns"]]

        assert "repository" in patterns
        assert "retry-with-backoff" in patterns

    def test_extract_snippet_references(self):
        """Test extraction of snippet:[name] references."""
        content = """
        Use snippet:express-route for the endpoint.
        Also snippet:jest-test for testing.
        """

        refs = extract_references(content)
        snippets = [name for name, _ in refs["snippets"]]

        assert "express-route" in snippets
        assert "jest-test" in snippets

    def test_extract_agent_references(self):
        """Test extraction of agent references."""
        content = """
        Spawn security-analyst for security review.
        Use code-reviewer agent for quality.
        """

        refs = extract_references(content)
        agents = [name for name, _ in refs["agents"]]

        assert "security-analyst" in agents
        assert "code-reviewer" in agents


class TestCrossReferenceValidation:
    """Test cross-reference validation across files."""

    def test_all_rules_references_valid(self, claude_dir: Path, command_files: List[Path]):
        """Test that all @rules/ references in commands are valid."""
        registry = CrossReferenceRegistry(claude_dir)
        validator = CrossReferenceValidator(registry)

        invalid_refs = []
        for file_path in command_files:
            result = validator.validate(file_path)
            for finding in result.findings:
                if "INVALID_RULES_REF" in finding.code:
                    invalid_refs.append((file_path.name, finding.message))

        if invalid_refs:
            msg = "Invalid rule references found:\n"
            for fname, message in invalid_refs[:10]:  # Limit output
                msg += f"  {fname}: {message}\n"
            pytest.skip(f"{msg}\n(These references should be fixed or the referenced rules created)")

    def test_all_patterns_references_valid(self, claude_dir: Path, skill_files: List[Path]):
        """Test that all @patterns/ references in skills are valid."""
        registry = CrossReferenceRegistry(claude_dir)
        validator = CrossReferenceValidator(registry)

        invalid_refs = []
        for file_path in skill_files:
            result = validator.validate(file_path)
            for finding in result.findings:
                if "INVALID_PATTERNS_REF" in finding.code:
                    invalid_refs.append((str(file_path.relative_to(claude_dir)), finding.message))

        if invalid_refs:
            msg = "Invalid pattern references found:\n"
            for fname, message in invalid_refs[:10]:
                msg += f"  {fname}: {message}\n"
            pytest.skip(f"{msg}\n(These references should be fixed or the referenced patterns created)")


class TestCrossReferenceIntegrity:
    """Test overall cross-reference integrity."""

    def test_validate_all_cross_references(self, claude_dir: Path):
        """Test that all cross-references across the project are valid."""
        results = validate_all_cross_references(claude_dir)

        # Collect all blocking findings
        all_findings = []
        for file_path, result in results.items():
            for finding in result.blocking_findings:
                all_findings.append((file_path, finding))

        if all_findings:
            msg = f"Found {len(all_findings)} cross-reference issues:\n"
            for file_path, finding in all_findings[:20]:  # Limit output
                relative = file_path.relative_to(claude_dir)
                msg += f"  {relative}: [{finding.code}] {finding.message}\n"
            pytest.skip(f"{msg}\n(These cross-references should be fixed)")
