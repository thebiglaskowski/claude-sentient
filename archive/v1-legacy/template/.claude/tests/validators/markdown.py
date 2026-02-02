"""
Markdown section extraction and validation for Claude Conductor components.

Provides:
- extract_sections(): Extract markdown sections from content
- MarkdownValidator: Validate markdown structure against requirements
"""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from .base import BaseValidator, Severity, ValidationFinding, ValidationResult
from .frontmatter import parse_frontmatter


# Regex to match markdown headings
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)

# Regex to match XML-style tags used in commands
XML_TAG_PATTERN = re.compile(r"<(\w+)>(.*?)</\1>", re.DOTALL)


def extract_sections(
    content: str,
    min_heading_level: int = 1,
    max_heading_level: int = 6,
) -> Dict[str, Tuple[str, int, str]]:
    """
    Extract markdown sections from content.

    Args:
        content: Markdown content (without frontmatter)
        min_heading_level: Minimum heading level to extract (1-6)
        max_heading_level: Maximum heading level to extract (1-6)

    Returns:
        Dictionary mapping section titles to tuples of:
        - Normalized section name (lowercase, no special chars)
        - Line number where section starts
        - Section content (text until next heading)
    """
    sections = {}
    lines = content.split('\n')

    current_section = None
    current_content_lines = []
    current_line_num = 1

    for i, line in enumerate(lines, 1):
        match = HEADING_PATTERN.match(line)
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()

            if min_heading_level <= level <= max_heading_level:
                # Save previous section if exists
                if current_section:
                    sections[current_section] = (
                        normalize_section_name(current_section),
                        current_line_num,
                        '\n'.join(current_content_lines).strip(),
                    )

                current_section = title
                current_content_lines = []
                current_line_num = i
            else:
                if current_section:
                    current_content_lines.append(line)
        else:
            if current_section:
                current_content_lines.append(line)

    # Save last section
    if current_section:
        sections[current_section] = (
            normalize_section_name(current_section),
            current_line_num,
            '\n'.join(current_content_lines).strip(),
        )

    return sections


def extract_xml_sections(content: str) -> Dict[str, Tuple[int, str]]:
    """
    Extract XML-style tag sections from content (used in commands).

    Args:
        content: Markdown content that may contain XML tags

    Returns:
        Dictionary mapping tag names to tuples of:
        - Line number where tag starts (approximate)
        - Tag content
    """
    sections = {}

    for match in XML_TAG_PATTERN.finditer(content):
        tag_name = match.group(1)
        tag_content = match.group(2).strip()

        # Approximate line number by counting newlines before match
        line_num = content[:match.start()].count('\n') + 1

        sections[tag_name] = (line_num, tag_content)

    return sections


def normalize_section_name(name: str) -> str:
    """
    Normalize a section name for comparison.

    - Converts to lowercase
    - Removes special characters
    - Strips whitespace
    - Replaces multiple spaces with single space
    """
    # Remove markdown formatting
    name = re.sub(r'\*\*|__|\*|_|`', '', name)
    # Remove special characters except spaces and hyphens
    name = re.sub(r'[^\w\s-]', '', name)
    # Normalize whitespace
    name = ' '.join(name.lower().split())
    return name


class MarkdownValidator(BaseValidator):
    """
    Validates markdown structure in files.

    This validator checks:
    - Required sections are present
    - Section ordering (optional)
    - Minimum content length
    - XML-style tags (for commands)
    """

    def __init__(
        self,
        required_sections: Optional[Set[str]] = None,
        required_xml_tags: Optional[Set[str]] = None,
        min_content_length: int = 0,
        check_section_order: bool = False,
        section_order: Optional[List[str]] = None,
    ):
        """
        Initialize the validator.

        Args:
            required_sections: Set of required markdown section names
            required_xml_tags: Set of required XML-style tags
            min_content_length: Minimum length of content after frontmatter
            check_section_order: Whether to validate section ordering
            section_order: Expected order of sections (if check_section_order is True)
        """
        self.required_sections = {normalize_section_name(s) for s in (required_sections or set())}
        self.required_xml_tags = required_xml_tags or set()
        self.min_content_length = min_content_length
        self.check_section_order = check_section_order
        self.section_order = [normalize_section_name(s) for s in (section_order or [])]

    def validate(self, file_path: Path) -> ValidationResult:
        """Validate a single file's markdown structure."""
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

        # Parse frontmatter to get content only
        _, markdown_content, content_start = parse_frontmatter(content)

        # Check minimum content length
        if len(markdown_content.strip()) < self.min_content_length:
            findings.append(self._create_finding(
                Severity.S1_HIGH,
                "CONTENT_TOO_SHORT",
                f"Content is too short ({len(markdown_content.strip())} chars, minimum: {self.min_content_length})",
                file_path,
                line_number=content_start,
            ))

        # Extract and validate markdown sections
        sections = extract_sections(markdown_content)
        section_names = {normalized for _, (normalized, _, _) in sections.items()}

        # Check required sections (partial match - section must contain the required term)
        for required in self.required_sections:
            # Check if any section name contains the required term
            has_section = any(required in name for name in section_names)
            if not has_section:
                findings.append(self._create_finding(
                    Severity.S1_HIGH,
                    "MISSING_SECTION",
                    f"Missing required section: {required}",
                    file_path,
                    suggestion=f"Add a section with heading containing '{required}'",
                ))

        # Extract and validate XML tags
        xml_sections = extract_xml_sections(markdown_content)
        xml_tag_names = set(xml_sections.keys())

        # Check required XML tags
        for required in self.required_xml_tags:
            if required not in xml_tag_names:
                findings.append(self._create_finding(
                    Severity.S1_HIGH,
                    "MISSING_XML_TAG",
                    f"Missing required XML tag: <{required}>",
                    file_path,
                    suggestion=f"Add a <{required}>...</{required}> block",
                ))

        # Check section order if requested
        if self.check_section_order and self.section_order:
            found_sections = []
            for title, (normalized, line_num, _) in sorted(sections.items(), key=lambda x: x[1][1]):
                if normalized in self.section_order:
                    found_sections.append((normalized, line_num))

            # Check if found sections are in correct order
            expected_order = [s for s in self.section_order if s in [f[0] for f in found_sections]]
            actual_order = [f[0] for f in found_sections]

            if actual_order != expected_order:
                findings.append(self._create_finding(
                    Severity.S2_MEDIUM,
                    "SECTION_ORDER",
                    f"Sections are out of order",
                    file_path,
                    suggestion=f"Expected order: {', '.join(expected_order)}",
                ))

        return self._create_result(
            findings,
            {
                "sections": {title: content for title, (_, _, content) in sections.items()},
                "xml_tags": {tag: content for tag, (_, content) in xml_sections.items()},
            }
        )
