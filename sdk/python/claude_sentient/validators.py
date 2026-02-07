"""JSON Schema validation for Claude Sentient SDK.

Validates profile YAML files and session state against the project's
JSON Schema definitions in schemas/.
"""

import json
import sys
from pathlib import Path
from typing import Any

# Schema directory relative to the SDK package
_SCHEMAS_DIR = Path(__file__).parent.parent.parent.parent / "schemas"


def _load_schema(schema_name: str) -> dict[str, Any] | None:
    """Load a JSON schema file by name.

    Args:
        schema_name: Schema filename (e.g., 'state.schema.json')

    Returns:
        Parsed schema dict, or None if not found.
    """
    schema_path = _SCHEMAS_DIR / schema_name
    if not schema_path.exists():
        return None
    try:
        return json.loads(schema_path.read_text())
    except (json.JSONDecodeError, OSError) as e:
        print(f"Warning: Failed to load schema {schema_name}: {e}", file=sys.stderr)
        return None


def validate_state(data: dict[str, Any]) -> list[str]:
    """Validate session state data against state.schema.json.

    Args:
        data: State dictionary to validate.

    Returns:
        List of validation error messages. Empty list means valid.
    """
    try:
        import jsonschema
    except ImportError:
        return []  # Skip validation if jsonschema not installed

    schema = _load_schema("state.schema.json")
    if not schema:
        return []

    errors = []
    validator = jsonschema.Draft202012Validator(schema)
    for error in validator.iter_errors(data):
        path = ".".join(str(p) for p in error.absolute_path) or "(root)"
        errors.append(f"{path}: {error.message}")
    return errors


def validate_profile_yaml(data: dict[str, Any]) -> list[str]:
    """Validate profile YAML data against expected structure.

    Checks required fields, types, and gate configurations
    without requiring full JSON Schema (profiles use YAML not JSON).

    Args:
        data: Parsed YAML profile data.

    Returns:
        List of validation error messages. Empty list means valid.
    """
    errors = []

    if not isinstance(data, dict):
        return ["Profile data must be a dictionary"]

    # Check name field
    if "name" not in data:
        errors.append("Missing required field: name")
    elif not isinstance(data["name"], str):
        errors.append("Field 'name' must be a string")

    # Validate gates structure
    gates = data.get("gates", {})
    if not isinstance(gates, dict):
        errors.append("Field 'gates' must be a dictionary")
    else:
        for gate_name, gate_config in gates.items():
            if isinstance(gate_config, dict):
                if "command" not in gate_config:
                    errors.append(f"Gate '{gate_name}' missing 'command' field")
                if "blocking" in gate_config and not isinstance(gate_config["blocking"], bool):
                    errors.append(f"Gate '{gate_name}' field 'blocking' must be boolean")
                if "timeout" in gate_config and not isinstance(gate_config["timeout"], (int, float)):
                    errors.append(f"Gate '{gate_name}' field 'timeout' must be a number")
            elif not isinstance(gate_config, str):
                errors.append(f"Gate '{gate_name}' must be a dict or string")

    # Validate models structure
    models = data.get("models", {})
    if models and not isinstance(models, dict):
        errors.append("Field 'models' must be a dictionary")
    elif isinstance(models, dict):
        valid_tiers = {"opus", "sonnet", "haiku"}
        for key in ("default", "planning", "exploration", "security"):
            if key in models and models[key] not in valid_tiers:
                errors.append(f"Model '{key}' must be one of: {', '.join(valid_tiers)}")

    # Validate thinking structure
    thinking = data.get("thinking", {})
    if thinking and not isinstance(thinking, dict):
        errors.append("Field 'thinking' must be a dictionary")
    elif isinstance(thinking, dict):
        max_tokens = thinking.get("max_tokens", thinking.get("maxTokens"))
        if max_tokens is not None and not isinstance(max_tokens, int):
            errors.append("Thinking 'max_tokens' must be an integer")
        extended_for = thinking.get("extended_for", thinking.get("extendedFor"))
        if extended_for is not None and not isinstance(extended_for, list):
            errors.append("Thinking 'extended_for' must be a list")

    return errors
