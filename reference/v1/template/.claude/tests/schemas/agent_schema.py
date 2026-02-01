"""
Agent schema and validator for Claude Conductor agents.

Agents are specialized expert definitions:
- YAML frontmatter with name, description, tools, disallowedTools, model
- Structured content with expertise, process, output format, checklist
"""

from pathlib import Path
from typing import List, Optional, Set

from validators.base import BaseValidator, Severity, ValidationFinding, ValidationResult
from validators.frontmatter import FrontmatterSchema, FrontmatterValidator, parse_frontmatter
from validators.markdown import MarkdownValidator, normalize_section_name


# Valid model names for agents
VALID_MODELS = {"sonnet", "opus", "haiku"}

# Valid tool names
VALID_TOOLS = {
    "Read", "Write", "Edit", "Grep", "Glob", "Bash",
    "WebFetch", "WebSearch", "Task", "NotebookEdit",
}

# Frontmatter schema for agents
AGENT_SCHEMA = FrontmatterSchema(
    required_fields={"name", "description", "tools", "model"},
    optional_fields={"disallowedTools"},
    field_types={
        "name": str,
        "description": str,
        "model": str,
    },
    allowed_values={
        "model": VALID_MODELS,
    },
)

# Required markdown sections for agents (normalized)
# Note: These use partial matching - section names must CONTAIN these terms
REQUIRED_AGENT_SECTIONS = {
    "expertise",
    "process",
}


class AgentValidator(BaseValidator):
    """
    Validates agent files against the agent schema.

    Checks:
    - Valid YAML frontmatter with required fields
    - tools is a list of valid tool names
    - disallowedTools is a list of valid tool names
    - model is valid (sonnet, opus, haiku)
    - Required markdown sections present
    """

    def __init__(self):
        self.frontmatter_validator = FrontmatterValidator(AGENT_SCHEMA)
        self.markdown_validator = MarkdownValidator(
            required_sections=REQUIRED_AGENT_SECTIONS,
        )

    def validate(self, file_path: Path) -> ValidationResult:
        """Validate an agent file."""
        findings: List[ValidationFinding] = []

        # Validate frontmatter
        fm_result = self.frontmatter_validator.validate(file_path)
        findings.extend(fm_result.findings)

        frontmatter = fm_result.metadata.get("frontmatter", {})

        # Additional agent-specific validations
        if frontmatter:
            # Validate tools field
            tools = frontmatter.get("tools")
            if tools is not None:
                if isinstance(tools, str):
                    # Handle comma-separated string format
                    tool_list = [t.strip() for t in tools.split(",")]
                elif isinstance(tools, list):
                    tool_list = tools
                else:
                    tool_list = []
                    findings.append(self._create_finding(
                        Severity.S1_HIGH,
                        "TOOLS_INVALID_TYPE",
                        f"'tools' should be a list or comma-separated string, got {type(tools).__name__}",
                        file_path,
                        line_number=1,
                    ))

                # Check each tool is valid
                for tool in tool_list:
                    if tool and tool not in VALID_TOOLS:
                        findings.append(self._create_finding(
                            Severity.S2_MEDIUM,
                            "UNKNOWN_TOOL",
                            f"Unknown tool: {tool}",
                            file_path,
                            line_number=1,
                            suggestion=f"Valid tools: {', '.join(sorted(VALID_TOOLS))}",
                        ))

            # Validate disallowedTools field
            disallowed = frontmatter.get("disallowedTools")
            if disallowed is not None:
                if isinstance(disallowed, str):
                    # Handle comma-separated string format
                    disallowed_list = [t.strip() for t in disallowed.split(",")]
                elif isinstance(disallowed, list):
                    disallowed_list = disallowed
                else:
                    disallowed_list = []
                    findings.append(self._create_finding(
                        Severity.S1_HIGH,
                        "DISALLOWED_TOOLS_INVALID_TYPE",
                        f"'disallowedTools' should be a list or comma-separated string, got {type(disallowed).__name__}",
                        file_path,
                        line_number=1,
                    ))

                # Check each disallowed tool is valid
                for tool in disallowed_list:
                    if tool and tool not in VALID_TOOLS:
                        findings.append(self._create_finding(
                            Severity.S2_MEDIUM,
                            "UNKNOWN_DISALLOWED_TOOL",
                            f"Unknown disallowed tool: {tool}",
                            file_path,
                            line_number=1,
                            suggestion=f"Valid tools: {', '.join(sorted(VALID_TOOLS))}",
                        ))

        # Validate markdown structure
        md_result = self.markdown_validator.validate(file_path)
        findings.extend(md_result.findings)

        # Combine metadata
        metadata = {
            **fm_result.metadata,
            **md_result.metadata,
        }

        return self._create_result(findings, metadata)
