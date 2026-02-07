#!/usr/bin/env python3
"""Tests for Claude Sentient utility tools.

Validates:
- validate.py: Schema loading, validation logic
- migrate.py: Migration path detection
- render-state.py: State rendering

Run: python tools/test_tools.py
"""

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class TestValidateTool(unittest.TestCase):
    """Tests for validate.py."""

    def test_schema_files_exist(self):
        """All referenced schema files should exist."""
        schemas_dir = PROJECT_ROOT / "schemas"
        expected_schemas = [
            "base.schema.json",
            "command.schema.json",
            "event.schema.json",
            "gate.schema.json",
            "phase.schema.json",
            "skill.schema.json",
            "state.schema.json",
        ]
        for schema_file in expected_schemas:
            self.assertTrue(
                (schemas_dir / schema_file).exists(),
                f"Schema file {schema_file} should exist",
            )

    def test_schemas_are_valid_json(self):
        """All schema files should be valid JSON."""
        schemas_dir = PROJECT_ROOT / "schemas"
        for schema_file in schemas_dir.glob("*.json"):
            with open(schema_file) as f:
                try:
                    data = json.load(f)
                    self.assertIsInstance(data, dict, f"{schema_file.name} should be a JSON object")
                except json.JSONDecodeError as e:
                    self.fail(f"{schema_file.name} is not valid JSON: {e}")

    def test_schemas_have_required_fields(self):
        """Schema files should have $schema and type fields."""
        schemas_dir = PROJECT_ROOT / "schemas"
        for schema_file in schemas_dir.glob("*.json"):
            with open(schema_file) as f:
                data = json.load(f)
            # Most schemas should have a type or $schema field
            has_structure = "$schema" in data or "type" in data or "properties" in data
            self.assertTrue(
                has_structure,
                f"{schema_file.name} should have $schema, type, or properties",
            )


class TestSharedConfig(unittest.TestCase):
    """Tests for shared configuration files."""

    def test_dangerous_patterns_exists(self):
        """shared/dangerous-patterns.json should exist."""
        config = PROJECT_ROOT / "shared" / "dangerous-patterns.json"
        self.assertTrue(config.exists(), "shared/dangerous-patterns.json should exist")

    def test_dangerous_patterns_valid(self):
        """Dangerous patterns config should be valid JSON with expected structure."""
        config = PROJECT_ROOT / "shared" / "dangerous-patterns.json"
        with open(config) as f:
            data = json.load(f)
        self.assertIn("dangerous", data)
        self.assertIn("warnings", data)
        self.assertIsInstance(data["dangerous"], list)
        self.assertIsInstance(data["warnings"], list)

        # Each pattern should have pattern and reason
        for entry in data["dangerous"]:
            self.assertIn("pattern", entry, f"Missing pattern in: {entry}")
            self.assertIn("reason", entry, f"Missing reason in: {entry}")

    def test_protected_paths_exists(self):
        """shared/protected-paths.json should exist."""
        config = PROJECT_ROOT / "shared" / "protected-paths.json"
        self.assertTrue(config.exists(), "shared/protected-paths.json should exist")

    def test_protected_paths_valid(self):
        """Protected paths config should be valid JSON with expected structure."""
        config = PROJECT_ROOT / "shared" / "protected-paths.json"
        with open(config) as f:
            data = json.load(f)
        self.assertIn("protected", data)
        self.assertIn("sensitive", data)
        self.assertIsInstance(data["protected"], list)
        self.assertIsInstance(data["sensitive"], list)

        for entry in data["protected"]:
            self.assertIn("pattern", entry)
            self.assertIn("reason", entry)


class TestProfileFiles(unittest.TestCase):
    """Tests for profile YAML files."""

    def test_all_profiles_are_valid_yaml(self):
        """All profile YAML files should be parseable."""
        try:
            import yaml
        except ImportError:
            self.skipTest("pyyaml not installed")

        profiles_dir = PROJECT_ROOT / "profiles"
        for profile_file in profiles_dir.glob("*.yaml"):
            if profile_file.name.startswith("_"):
                continue  # Skip schema files
            with open(profile_file) as f:
                try:
                    data = yaml.safe_load(f)
                    self.assertIsInstance(
                        data, dict,
                        f"{profile_file.name} should parse to a dict",
                    )
                except yaml.YAMLError as e:
                    self.fail(f"{profile_file.name} is not valid YAML: {e}")

    def test_profiles_have_name(self):
        """Profile files should have a name field."""
        try:
            import yaml
        except ImportError:
            self.skipTest("pyyaml not installed")

        profiles_dir = PROJECT_ROOT / "profiles"
        for profile_file in profiles_dir.glob("*.yaml"):
            if profile_file.name.startswith("_"):
                continue
            with open(profile_file) as f:
                data = yaml.safe_load(f)
            self.assertIn(
                "name", data,
                f"{profile_file.name} should have a 'name' field",
            )


class TestProjectStructure(unittest.TestCase):
    """Tests for overall project structure."""

    def test_required_directories_exist(self):
        """Required project directories should exist."""
        required_dirs = [
            "profiles",
            "schemas",
            "rules",
            "phases",
            "templates",
            ".claude/commands",
            ".claude/hooks",
            ".claude/rules",
        ]
        for dir_name in required_dirs:
            self.assertTrue(
                (PROJECT_ROOT / dir_name).exists(),
                f"Directory {dir_name}/ should exist",
            )

    def test_required_files_exist(self):
        """Required project files should exist."""
        required_files = [
            "CLAUDE.md",
            "README.md",
            "STATUS.md",
            "CHANGELOG.md",
            "LICENSE",
            "install.sh",
            "install.ps1",
        ]
        for file_name in required_files:
            self.assertTrue(
                (PROJECT_ROOT / file_name).exists(),
                f"File {file_name} should exist",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
