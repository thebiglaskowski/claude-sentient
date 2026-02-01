"""
Command schema and validator for Claude Conductor commands.

Commands are slash-command workflows that follow a specific structure:
- YAML frontmatter with name, description, model
- Structured content with context, role, task, instructions, output_format
"""

from pathlib import Path
from typing import List, Optional

from validators.base import BaseValidator, Severity, ValidationFinding, ValidationResult
from validators.frontmatter import FrontmatterSchema, FrontmatterValidator, parse_frontmatter
from validators.markdown import MarkdownValidator, extract_xml_sections


# Valid model names for commands
VALID_MODELS = {"sonnet", "opus", "haiku"}

# Frontmatter schema for commands
COMMAND_SCHEMA = FrontmatterSchema(
    required_fields={"name", "description", "model"},
    optional_fields={"argument-hint"},
    field_types={
        "name": str,
        "description": str,
        "model": str,
        "argument-hint": str,
    },
    allowed_values={
        "model": VALID_MODELS,
    },
    field_validators={
        "name": lambda v: None if v.startswith("cc:") else "Command name must start with 'cc:'",
    },
)

# Required XML-style tags in commands
REQUIRED_XML_TAGS = {"context", "role", "task", "instructions", "output_format", "rules"}

# Optional but recommended tags
RECOMMENDED_XML_TAGS = {"examples", "error_handling"}


class CommandValidator(BaseValidator):
    """
    Validates command files against the command schema.

    Checks:
    - Valid YAML frontmatter with required fields
    - name starts with 'cc:'
    - model is valid (sonnet, opus, haiku)
    - Required XML-style sections present
    - Recommended sections present (warning if missing)
    """

    def __init__(self):
        self.frontmatter_validator = FrontmatterValidator(COMMAND_SCHEMA)
        self.markdown_validator = MarkdownValidator(
            required_xml_tags=REQUIRED_XML_TAGS,
        )

    def validate(self, file_path: Path) -> ValidationResult:
        """Validate a command file."""
        findings: List[ValidationFinding] = []

        # Validate frontmatter
        fm_result = self.frontmatter_validator.validate(file_path)
        findings.extend(fm_result.findings)

        # Validate markdown structure
        md_result = self.markdown_validator.validate(file_path)
        findings.extend(md_result.findings)

        # Additional command-specific validations
        try:
            content = file_path.read_text(encoding='utf-8')
            _, markdown_content, _ = parse_frontmatter(content)
            xml_sections = extract_xml_sections(markdown_content)

            # Check for recommended tags (warnings only)
            for tag in RECOMMENDED_XML_TAGS:
                if tag not in xml_sections:
                    findings.append(self._create_finding(
                        Severity.S3_LOW,
                        "MISSING_RECOMMENDED_TAG",
                        f"Recommended tag <{tag}> not found",
                        file_path,
                        suggestion=f"Consider adding a <{tag}>...</{tag}> section",
                    ))

            # Check instructions has numbered steps
            if "instructions" in xml_sections:
                _, instructions_content = xml_sections["instructions"]
                if "<step" not in instructions_content.lower():
                    findings.append(self._create_finding(
                        Severity.S3_LOW,
                        "INSTRUCTIONS_NO_STEPS",
                        "Instructions section doesn't use numbered <step> tags",
                        file_path,
                        suggestion="Use <step number=\"1\">...</step> format for instructions",
                    ))

            # Check examples has example blocks
            if "examples" in xml_sections:
                _, examples_content = xml_sections["examples"]
                if "<example>" not in examples_content.lower():
                    findings.append(self._create_finding(
                        Severity.S3_LOW,
                        "EXAMPLES_NO_BLOCKS",
                        "Examples section doesn't use <example> blocks",
                        file_path,
                        suggestion="Use <example>...</example> format for examples",
                    ))

        except Exception as e:
            findings.append(self._create_finding(
                Severity.S2_MEDIUM,
                "VALIDATION_ERROR",
                f"Error during command-specific validation: {e}",
                file_path,
            ))

        # Combine metadata
        metadata = {
            **fm_result.metadata,
            **md_result.metadata,
        }

        return self._create_result(findings, metadata)
