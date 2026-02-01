"""
Rule schema and validator for Claude Conductor rules.

Rules are topic-specific standards:
- No frontmatter required
- Required sections: Core Principles, specific content sections
- Should have Anti-Patterns and Checklist sections
"""

from pathlib import Path
from typing import List, Set

from validators.base import BaseValidator, Severity, ValidationFinding, ValidationResult
from validators.frontmatter import parse_frontmatter
from validators.markdown import MarkdownValidator, extract_sections, normalize_section_name


# Required sections for rules (normalized)
REQUIRED_RULE_SECTIONS = {
    "core principles",
}

# Recommended sections (warnings if missing)
RECOMMENDED_RULE_SECTIONS = {
    "anti-patterns",
    "checklist",
}

# Minimum content length for rules
MIN_RULE_CONTENT_LENGTH = 500


class RuleValidator(BaseValidator):
    """
    Validates rule files against the rule schema.

    Checks:
    - Required markdown sections present
    - Recommended sections present (warning if missing)
    - Sufficient content depth
    - No frontmatter (rules don't use frontmatter)
    """

    def __init__(self):
        self.markdown_validator = MarkdownValidator(
            required_sections=REQUIRED_RULE_SECTIONS,
            min_content_length=MIN_RULE_CONTENT_LENGTH,
        )

    def validate(self, file_path: Path) -> ValidationResult:
        """Validate a rule file."""
        findings: List[ValidationFinding] = []

        # Validate markdown structure
        md_result = self.markdown_validator.validate(file_path)
        findings.extend(md_result.findings)

        # Additional rule-specific validations
        try:
            content = file_path.read_text(encoding='utf-8')
            frontmatter, markdown_content, _ = parse_frontmatter(content)

            # Rules should not have frontmatter
            if frontmatter:
                findings.append(self._create_finding(
                    Severity.S3_LOW,
                    "UNEXPECTED_FRONTMATTER",
                    "Rule files typically don't use frontmatter",
                    file_path,
                    line_number=1,
                    suggestion="Remove the frontmatter block if not needed",
                ))

            # Check for recommended sections
            sections = extract_sections(markdown_content)
            section_names = {normalize_section_name(title) for title in sections.keys()}

            for section in RECOMMENDED_RULE_SECTIONS:
                normalized = normalize_section_name(section)
                # Check if any section contains the key words
                has_section = any(normalized in s for s in section_names)
                if not has_section:
                    findings.append(self._create_finding(
                        Severity.S3_LOW,
                        "MISSING_RECOMMENDED_SECTION",
                        f"Recommended section '{section}' not found",
                        file_path,
                        suggestion=f"Consider adding a '## {section.title()}' section",
                    ))

            # Check for multiple H2 sections (rules should be comprehensive)
            h2_count = sum(1 for title in sections.keys()
                          if sections[title][0] in section_names)
            if h2_count < 3:
                findings.append(self._create_finding(
                    Severity.S3_LOW,
                    "FEW_SECTIONS",
                    f"Rule has only {h2_count} main sections",
                    file_path,
                    suggestion="Rules should have multiple sections covering different aspects",
                ))

        except Exception as e:
            findings.append(self._create_finding(
                Severity.S2_MEDIUM,
                "VALIDATION_ERROR",
                f"Error during rule-specific validation: {e}",
                file_path,
            ))

        return self._create_result(findings, md_result.metadata)
