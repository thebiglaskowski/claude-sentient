"""
Pattern schema and validator for Claude Conductor patterns.

Patterns are reusable architecture patterns:
- No frontmatter required
- Required sections: Intent, When to Use, When NOT to Use, Structure, Implementation,
  Variations, Related Patterns, Anti-Patterns
- Should include code examples in multiple languages
"""

from pathlib import Path
from typing import List, Set

from validators.base import BaseValidator, Severity, ValidationFinding, ValidationResult
from validators.frontmatter import parse_frontmatter
from validators.markdown import MarkdownValidator, extract_sections, normalize_section_name
from validators.code_blocks import CodeBlockValidator, extract_code_blocks


# Required sections for patterns (normalized)
# Note: "when not to use" moved to recommended since not all patterns need it
REQUIRED_PATTERN_SECTIONS = {
    "intent",
    "when to use",
}

# Recommended sections (warnings if missing)
RECOMMENDED_PATTERN_SECTIONS = {
    "when not to use",
    "implementation",
    "related patterns",
    "anti-patterns",
}

# Recommended languages for code examples
RECOMMENDED_LANGUAGES = {"typescript", "python", "go"}


class PatternValidator(BaseValidator):
    """
    Validates pattern files against the pattern schema.

    Checks:
    - Required markdown sections present
    - Recommended sections present (warning if missing)
    - Code examples present
    - Code examples include multiple languages (recommended)
    """

    def __init__(self):
        self.markdown_validator = MarkdownValidator(
            required_sections=REQUIRED_PATTERN_SECTIONS,
        )
        self.code_validator = CodeBlockValidator(
            min_code_blocks=1,
        )

    def validate(self, file_path: Path) -> ValidationResult:
        """Validate a pattern file."""
        findings: List[ValidationFinding] = []

        # Validate markdown structure
        md_result = self.markdown_validator.validate(file_path)
        findings.extend(md_result.findings)

        # Validate code blocks
        code_result = self.code_validator.validate(file_path)
        findings.extend(code_result.findings)

        # Additional pattern-specific validations
        try:
            content = file_path.read_text(encoding='utf-8')
            _, markdown_content, _ = parse_frontmatter(content)

            # Check for recommended sections
            sections = extract_sections(markdown_content)
            section_names = {normalize_section_name(title) for title in sections.keys()}

            for section in RECOMMENDED_PATTERN_SECTIONS:
                normalized = normalize_section_name(section)
                if normalized not in section_names:
                    findings.append(self._create_finding(
                        Severity.S3_LOW,
                        "MISSING_RECOMMENDED_SECTION",
                        f"Recommended section '{section}' not found",
                        file_path,
                        suggestion=f"Consider adding a '## {section.title()}' section",
                    ))

            # Check for language diversity in code examples
            code_blocks = extract_code_blocks(markdown_content)
            found_languages = {lang.lower() for lang, _, _ in code_blocks if lang}

            # Map common language aliases
            language_map = {
                "ts": "typescript",
                "tsx": "typescript",
                "js": "javascript",
                "jsx": "javascript",
                "py": "python",
            }
            normalized_languages = {language_map.get(lang, lang) for lang in found_languages}

            # Check for at least 2 different languages
            if len(normalized_languages) < 2:
                findings.append(self._create_finding(
                    Severity.S3_LOW,
                    "LIMITED_LANGUAGE_EXAMPLES",
                    f"Pattern only has examples in {len(normalized_languages)} language(s)",
                    file_path,
                    suggestion="Consider adding examples in TypeScript, Python, and Go",
                ))

            # Check for recommended languages
            missing_recommended = RECOMMENDED_LANGUAGES - normalized_languages - {"javascript"}  # JS can substitute for TS
            if "typescript" in normalized_languages or "javascript" in normalized_languages:
                missing_recommended.discard("typescript")

            if missing_recommended:
                findings.append(self._create_finding(
                    Severity.S3_LOW,
                    "MISSING_RECOMMENDED_LANGUAGES",
                    f"Missing examples for recommended languages: {', '.join(missing_recommended)}",
                    file_path,
                ))

        except Exception as e:
            findings.append(self._create_finding(
                Severity.S2_MEDIUM,
                "VALIDATION_ERROR",
                f"Error during pattern-specific validation: {e}",
                file_path,
            ))

        # Combine metadata
        metadata = {
            **md_result.metadata,
            **code_result.metadata,
        }

        return self._create_result(findings, metadata)
