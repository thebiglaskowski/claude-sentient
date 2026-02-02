"""
Snippet schema and validator for Claude Conductor snippets.

Snippets are indexed code templates:
- No frontmatter required
- Required sections: Description, When to Use, Code, Customization Points, Related Snippets
- Must have at least one code block
"""

from pathlib import Path
from typing import List, Set

from validators.base import BaseValidator, Severity, ValidationFinding, ValidationResult
from validators.frontmatter import parse_frontmatter
from validators.markdown import MarkdownValidator, extract_sections, normalize_section_name
from validators.code_blocks import CodeBlockValidator, extract_code_blocks


# Required sections for snippets (normalized)
REQUIRED_SNIPPET_SECTIONS = {
    "description",
    "when to use",
    "code",
}

# Recommended sections (warnings if missing)
RECOMMENDED_SNIPPET_SECTIONS = {
    "customization points",
    "related snippets",
}


class SnippetValidator(BaseValidator):
    """
    Validates snippet files against the snippet schema.

    Checks:
    - Required markdown sections present
    - Recommended sections present (warning if missing)
    - At least one code block present
    - Code block has valid syntax
    """

    def __init__(self):
        self.markdown_validator = MarkdownValidator(
            required_sections=REQUIRED_SNIPPET_SECTIONS,
        )
        self.code_validator = CodeBlockValidator(
            min_code_blocks=1,
            validate_syntax=True,
        )

    def validate(self, file_path: Path) -> ValidationResult:
        """Validate a snippet file."""
        findings: List[ValidationFinding] = []

        # Validate markdown structure
        md_result = self.markdown_validator.validate(file_path)
        findings.extend(md_result.findings)

        # Validate code blocks
        code_result = self.code_validator.validate(file_path)
        findings.extend(code_result.findings)

        # Additional snippet-specific validations
        try:
            content = file_path.read_text(encoding='utf-8')
            _, markdown_content, _ = parse_frontmatter(content)

            # Check for recommended sections
            sections = extract_sections(markdown_content)
            section_names = {normalize_section_name(title) for title in sections.keys()}

            for section in RECOMMENDED_SNIPPET_SECTIONS:
                normalized = normalize_section_name(section)
                if normalized not in section_names:
                    findings.append(self._create_finding(
                        Severity.S3_LOW,
                        "MISSING_RECOMMENDED_SECTION",
                        f"Recommended section '{section}' not found",
                        file_path,
                        suggestion=f"Consider adding a '## {section.title()}' section",
                    ))

            # Check code blocks have language specified
            code_blocks = extract_code_blocks(markdown_content)
            for lang, code, line_num in code_blocks:
                if not lang:
                    findings.append(self._create_finding(
                        Severity.S2_MEDIUM,
                        "CODE_BLOCK_NO_LANGUAGE",
                        "Code block has no language specified",
                        file_path,
                        line_number=line_num,
                        suggestion="Add language identifier: ```typescript, ```python, etc.",
                    ))

        except Exception as e:
            findings.append(self._create_finding(
                Severity.S2_MEDIUM,
                "VALIDATION_ERROR",
                f"Error during snippet-specific validation: {e}",
                file_path,
            ))

        # Combine metadata
        metadata = {
            **md_result.metadata,
            **code_result.metadata,
        }

        return self._create_result(findings, metadata)
