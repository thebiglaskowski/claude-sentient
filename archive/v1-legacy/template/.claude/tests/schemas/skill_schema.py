"""
Skill schema and validator for Claude Conductor skills.

Skills are auto-loading behavioral guidance with triggers:
- YAML frontmatter with name, description
- Optional triggers, model, tags, context, rules
- Variable content structure
"""

from pathlib import Path
from typing import List, Optional

from validators.base import BaseValidator, Severity, ValidationFinding, ValidationResult
from validators.frontmatter import FrontmatterSchema, FrontmatterValidator, parse_frontmatter


# Valid model names for skills
VALID_MODELS = {"sonnet", "opus", "haiku"}

# Frontmatter schema for skills
SKILL_SCHEMA = FrontmatterSchema(
    required_fields={"name", "description"},
    optional_fields={
        "version",
        "triggers",
        "model",
        "tags",
        "context",
        "rules",
        "disable-model-invocation",
        "trigger",  # Alternative to triggers
    },
    field_types={
        "name": str,
        "description": str,
        "version": str,
        "model": str,
        "context": str,
    },
    allowed_values={
        "model": VALID_MODELS,
    },
)

# Minimum content length for skills
MIN_SKILL_CONTENT_LENGTH = 50


class SkillValidator(BaseValidator):
    """
    Validates skill files against the skill schema.

    Checks:
    - Valid YAML frontmatter with required fields
    - model is valid (if specified)
    - triggers/trigger is a list (if specified)
    - tags is a list (if specified)
    - Content has minimum length
    """

    def __init__(self):
        self.frontmatter_validator = FrontmatterValidator(SKILL_SCHEMA)

    def validate(self, file_path: Path) -> ValidationResult:
        """Validate a skill file."""
        findings: List[ValidationFinding] = []

        # Validate frontmatter
        fm_result = self.frontmatter_validator.validate(file_path)
        findings.extend(fm_result.findings)

        frontmatter = fm_result.metadata.get("frontmatter", {})

        # Additional skill-specific validations
        if frontmatter:
            # Check triggers is a list if present
            triggers = frontmatter.get("triggers") or frontmatter.get("trigger")
            if triggers is not None and not isinstance(triggers, list):
                findings.append(self._create_finding(
                    Severity.S1_HIGH,
                    "TRIGGERS_NOT_LIST",
                    f"'triggers' should be a list, got {type(triggers).__name__}",
                    file_path,
                    line_number=1,
                    suggestion="Use YAML list format:\ntriggers:\n  - \"trigger 1\"\n  - \"trigger 2\"",
                ))

            # Check tags is a list if present
            tags = frontmatter.get("tags")
            if tags is not None and not isinstance(tags, list):
                findings.append(self._create_finding(
                    Severity.S1_HIGH,
                    "TAGS_NOT_LIST",
                    f"'tags' should be a list, got {type(tags).__name__}",
                    file_path,
                    line_number=1,
                    suggestion="Use YAML list format:\ntags:\n  - tag1\n  - tag2",
                ))

            # Check rules is a list if present
            rules = frontmatter.get("rules")
            if rules is not None and not isinstance(rules, list):
                findings.append(self._create_finding(
                    Severity.S1_HIGH,
                    "RULES_NOT_LIST",
                    f"'rules' should be a list, got {type(rules).__name__}",
                    file_path,
                    line_number=1,
                    suggestion="Use YAML list format:\nrules:\n  - security\n  - testing",
                ))

        # Check content length
        try:
            content = file_path.read_text(encoding='utf-8')
            _, markdown_content, _ = parse_frontmatter(content)

            if len(markdown_content.strip()) < MIN_SKILL_CONTENT_LENGTH:
                findings.append(self._create_finding(
                    Severity.S2_MEDIUM,
                    "CONTENT_TOO_SHORT",
                    f"Skill content is too short ({len(markdown_content.strip())} chars, minimum: {MIN_SKILL_CONTENT_LENGTH})",
                    file_path,
                    suggestion="Add more detailed guidance and instructions",
                ))

        except Exception as e:
            findings.append(self._create_finding(
                Severity.S2_MEDIUM,
                "VALIDATION_ERROR",
                f"Error during skill-specific validation: {e}",
                file_path,
            ))

        return self._create_result(findings, fm_result.metadata)
