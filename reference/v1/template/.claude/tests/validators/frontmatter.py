"""
YAML frontmatter parsing and validation for Claude Conductor components.

Provides:
- parse_frontmatter(): Extract YAML frontmatter from markdown files
- FrontmatterValidator: Validate frontmatter against a schema
"""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import yaml

from .base import BaseValidator, Severity, ValidationFinding, ValidationResult


# Regex to match YAML frontmatter block at start of file
FRONTMATTER_PATTERN = re.compile(
    r"^---\s*\n(.*?)\n---\s*\n",
    re.DOTALL
)


def parse_frontmatter(content: str) -> Tuple[Optional[Dict[str, Any]], str, int]:
    """
    Parse YAML frontmatter from markdown content.

    Args:
        content: The full markdown file content

    Returns:
        Tuple of:
        - Parsed frontmatter dict (or None if no frontmatter)
        - Remaining content after frontmatter
        - Line number where content starts (for error reporting)
    """
    match = FRONTMATTER_PATTERN.match(content)
    if not match:
        return None, content, 1

    frontmatter_text = match.group(1)
    remaining_content = content[match.end():]

    # Count lines in frontmatter to get content start line
    content_start_line = frontmatter_text.count('\n') + 3  # +3 for --- lines

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if frontmatter is None:
            frontmatter = {}
        return frontmatter, remaining_content, content_start_line
    except yaml.YAMLError:
        return None, content, 1


class FrontmatterSchema:
    """
    Schema definition for validating frontmatter fields.

    Attributes:
        required_fields: Set of field names that must be present
        optional_fields: Set of field names that are allowed but not required
        field_types: Dict mapping field names to expected types
        field_validators: Dict mapping field names to custom validation functions
    """

    def __init__(
        self,
        required_fields: Optional[Set[str]] = None,
        optional_fields: Optional[Set[str]] = None,
        field_types: Optional[Dict[str, type]] = None,
        field_validators: Optional[Dict[str, callable]] = None,
        allowed_values: Optional[Dict[str, Set[str]]] = None,
    ):
        self.required_fields = required_fields or set()
        self.optional_fields = optional_fields or set()
        self.field_types = field_types or {}
        self.field_validators = field_validators or {}
        self.allowed_values = allowed_values or {}

    @property
    def all_known_fields(self) -> Set[str]:
        """Return all fields defined in the schema."""
        return self.required_fields | self.optional_fields


class FrontmatterValidator(BaseValidator):
    """
    Validates YAML frontmatter in markdown files against a schema.

    This validator checks:
    - Presence of frontmatter block
    - Required fields are present
    - Field types match expectations
    - Field values are within allowed values
    - No unknown fields (optional, warning only)
    """

    def __init__(self, schema: FrontmatterSchema, require_frontmatter: bool = True):
        """
        Initialize the validator with a schema.

        Args:
            schema: FrontmatterSchema defining validation rules
            require_frontmatter: Whether frontmatter is required (default: True)
        """
        self.schema = schema
        self.require_frontmatter = require_frontmatter

    def validate(self, file_path: Path) -> ValidationResult:
        """Validate a single file's frontmatter."""
        findings: List[ValidationFinding] = []

        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            findings.append(self._create_finding(
                Severity.S0_CRITICAL,
                "FILE_READ_ERROR",
                f"Failed to read file: {e}",
                file_path,
            ))
            return self._create_result(findings)

        frontmatter, _, content_start = parse_frontmatter(content)

        # Check if frontmatter exists
        if frontmatter is None:
            if self.require_frontmatter:
                findings.append(self._create_finding(
                    Severity.S0_CRITICAL,
                    "MISSING_FRONTMATTER",
                    "File is missing YAML frontmatter block",
                    file_path,
                    line_number=1,
                    suggestion="Add frontmatter block at the start of the file:\n---\nname: ...\ndescription: ...\n---",
                ))
            return self._create_result(findings, {"frontmatter": None})

        # Check required fields
        for field in self.schema.required_fields:
            if field not in frontmatter:
                findings.append(self._create_finding(
                    Severity.S0_CRITICAL,
                    "MISSING_REQUIRED_FIELD",
                    f"Missing required frontmatter field: {field}",
                    file_path,
                    line_number=1,
                    suggestion=f"Add '{field}' to the frontmatter block",
                ))
            elif frontmatter[field] is None or frontmatter[field] == "":
                findings.append(self._create_finding(
                    Severity.S1_HIGH,
                    "EMPTY_REQUIRED_FIELD",
                    f"Required field '{field}' is empty",
                    file_path,
                    line_number=1,
                    suggestion=f"Provide a value for '{field}'",
                ))

        # Check field types
        for field, expected_type in self.schema.field_types.items():
            if field in frontmatter and frontmatter[field] is not None:
                value = frontmatter[field]
                if not isinstance(value, expected_type):
                    findings.append(self._create_finding(
                        Severity.S1_HIGH,
                        "INVALID_FIELD_TYPE",
                        f"Field '{field}' has type {type(value).__name__}, expected {expected_type.__name__}",
                        file_path,
                        line_number=1,
                        suggestion=f"Change '{field}' to be a {expected_type.__name__}",
                    ))

        # Check allowed values
        for field, allowed in self.schema.allowed_values.items():
            if field in frontmatter and frontmatter[field] is not None:
                value = frontmatter[field]
                if value not in allowed:
                    findings.append(self._create_finding(
                        Severity.S1_HIGH,
                        "INVALID_FIELD_VALUE",
                        f"Field '{field}' has invalid value '{value}'",
                        file_path,
                        line_number=1,
                        suggestion=f"Valid values for '{field}': {', '.join(sorted(allowed))}",
                    ))

        # Check custom validators
        for field, validator in self.schema.field_validators.items():
            if field in frontmatter and frontmatter[field] is not None:
                value = frontmatter[field]
                try:
                    error_msg = validator(value)
                    if error_msg:
                        findings.append(self._create_finding(
                            Severity.S1_HIGH,
                            "FIELD_VALIDATION_FAILED",
                            f"Field '{field}' validation failed: {error_msg}",
                            file_path,
                            line_number=1,
                        ))
                except Exception as e:
                    findings.append(self._create_finding(
                        Severity.S2_MEDIUM,
                        "VALIDATOR_ERROR",
                        f"Error running validator for '{field}': {e}",
                        file_path,
                    ))

        # Check for unknown fields (warning only)
        known_fields = self.schema.all_known_fields
        if known_fields:  # Only check if schema defines known fields
            for field in frontmatter:
                if field not in known_fields:
                    findings.append(self._create_finding(
                        Severity.S3_LOW,
                        "UNKNOWN_FIELD",
                        f"Unknown frontmatter field: {field}",
                        file_path,
                        line_number=1,
                        suggestion=f"Known fields: {', '.join(sorted(known_fields))}",
                    ))

        return self._create_result(findings, {"frontmatter": frontmatter})
