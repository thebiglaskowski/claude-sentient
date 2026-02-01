#!/usr/bin/env python3
"""
Schema validation tool for Claude Conductor 2.0

Validates all components against their JSON schemas.

Usage:
    python validate.py                    # Validate all
    python validate.py --schema skill     # Validate only skills
    python validate.py path/to/file.yaml  # Validate specific file
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
    from jsonschema import Draft202012Validator, ValidationError
    from jsonschema.exceptions import SchemaError
except ImportError:
    print("Missing dependencies. Install with:")
    print("  pip install pyyaml jsonschema")
    sys.exit(1)


# Schema type to file patterns mapping
SCHEMA_PATTERNS = {
    "skill": "skills/**/*.skill.yaml",
    "command": "commands/**/*.cmd.yaml",
    "gate": "gates/**/*.gate.json",
    "phase": "phases/*.md",
    "event": "events/**/*.events.yaml",
}

# Schema file paths
SCHEMA_FILES = {
    "skill": "schemas/skill.schema.json",
    "command": "schemas/command.schema.json",
    "gate": "schemas/gate.schema.json",
    "phase": "schemas/phase.schema.json",
    "event": "schemas/event.schema.json",
}


def load_schema(schema_type: str) -> dict[str, Any]:
    """Load a JSON schema by type."""
    schema_path = Path(SCHEMA_FILES[schema_type])
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema not found: {schema_path}")

    with open(schema_path) as f:
        return json.load(f)


def load_file(file_path: Path) -> dict[str, Any]:
    """Load a YAML or JSON file."""
    with open(file_path) as f:
        if file_path.suffix in [".yaml", ".yml"]:
            return yaml.safe_load(f)
        elif file_path.suffix == ".json":
            return json.load(f)
        elif file_path.suffix == ".md":
            # Extract YAML frontmatter from Markdown
            content = f.read()
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    return yaml.safe_load(parts[1])
            return {}
        else:
            raise ValueError(f"Unknown file type: {file_path.suffix}")


def determine_schema_type(file_path: Path) -> str | None:
    """Determine schema type from file path."""
    path_str = str(file_path)

    if ".skill.yaml" in path_str:
        return "skill"
    elif ".cmd.yaml" in path_str:
        return "command"
    elif ".gate.json" in path_str:
        return "gate"
    elif "phases/" in path_str and path_str.endswith(".md"):
        return "phase"
    elif ".events.yaml" in path_str:
        return "event"

    return None


def validate_file(file_path: Path, schema: dict[str, Any]) -> list[str]:
    """Validate a single file. Returns list of errors."""
    errors = []

    try:
        content = load_file(file_path)
        if not content:
            return [f"{file_path}: Empty or invalid content"]

        validator = Draft202012Validator(schema)
        for error in validator.iter_errors(content):
            path = " -> ".join(str(p) for p in error.absolute_path)
            errors.append(f"{file_path}: {error.message}" + (f" at {path}" if path else ""))

    except yaml.YAMLError as e:
        errors.append(f"{file_path}: YAML parse error: {e}")
    except json.JSONDecodeError as e:
        errors.append(f"{file_path}: JSON parse error: {e}")
    except Exception as e:
        errors.append(f"{file_path}: {str(e)}")

    return errors


def validate_schema_type(schema_type: str) -> tuple[int, int]:
    """Validate all files of a schema type. Returns (passed, failed)."""
    pattern = SCHEMA_PATTERNS.get(schema_type)
    if not pattern:
        print(f"Unknown schema type: {schema_type}")
        return 0, 1

    try:
        schema = load_schema(schema_type)
    except FileNotFoundError as e:
        print(f"❌ {e}")
        return 0, 1

    passed = 0
    failed = 0

    for file_path in Path(".").glob(pattern):
        errors = validate_file(file_path, schema)
        if errors:
            failed += 1
            for error in errors:
                print(f"❌ {error}")
        else:
            passed += 1
            print(f"✅ {file_path}")

    return passed, failed


def validate_all() -> tuple[int, int]:
    """Validate all components. Returns (passed, failed)."""
    total_passed = 0
    total_failed = 0

    for schema_type in SCHEMA_PATTERNS:
        print(f"\n=== Validating {schema_type}s ===")
        passed, failed = validate_schema_type(schema_type)
        total_passed += passed
        total_failed += failed

    return total_passed, total_failed


def main():
    parser = argparse.ArgumentParser(description="Validate Claude Conductor components")
    parser.add_argument("file", nargs="?", help="Specific file to validate")
    parser.add_argument("--schema", "-s", choices=list(SCHEMA_PATTERNS.keys()),
                        help="Validate only this schema type")
    args = parser.parse_args()

    if args.file:
        # Validate specific file
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            sys.exit(1)

        schema_type = determine_schema_type(file_path)
        if not schema_type:
            print(f"❌ Cannot determine schema type for: {file_path}")
            sys.exit(1)

        schema = load_schema(schema_type)
        errors = validate_file(file_path, schema)

        if errors:
            for error in errors:
                print(f"❌ {error}")
            sys.exit(1)
        else:
            print(f"✅ {file_path}")
            sys.exit(0)

    elif args.schema:
        # Validate specific schema type
        passed, failed = validate_schema_type(args.schema)
        print(f"\n{passed} passed, {failed} failed")
        sys.exit(1 if failed > 0 else 0)

    else:
        # Validate all
        passed, failed = validate_all()
        print(f"\n{'='*40}")
        print(f"Total: {passed} passed, {failed} failed")
        sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()
