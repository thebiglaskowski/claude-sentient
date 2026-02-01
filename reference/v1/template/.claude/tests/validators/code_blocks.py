"""
Code block extraction and syntax validation for Claude Conductor components.

Provides:
- extract_code_blocks(): Extract fenced code blocks from markdown
- CodeBlockValidator: Validate code syntax in extracted blocks
"""

import ast
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from .base import BaseValidator, Severity, ValidationFinding, ValidationResult
from .frontmatter import parse_frontmatter


# Regex to match fenced code blocks with optional language
CODE_BLOCK_PATTERN = re.compile(
    r"```(\w*)\n(.*?)```",
    re.DOTALL
)

# SQL keywords for basic validation
SQL_KEYWORDS = {
    "select", "insert", "update", "delete", "create", "drop", "alter",
    "from", "where", "join", "on", "group", "order", "having", "limit",
    "table", "index", "view", "database", "schema", "begin", "commit",
}


def extract_code_blocks(content: str) -> List[Tuple[str, str, int]]:
    """
    Extract fenced code blocks from markdown content.

    Args:
        content: Markdown content

    Returns:
        List of tuples containing:
        - Language identifier (empty string if not specified)
        - Code content
        - Approximate line number where block starts
    """
    blocks = []

    for match in CODE_BLOCK_PATTERN.finditer(content):
        language = match.group(1).lower()
        code = match.group(2)
        line_num = content[:match.start()].count('\n') + 1
        blocks.append((language, code, line_num))

    return blocks


def validate_python_syntax(code: str) -> Optional[str]:
    """
    Validate Python code syntax.

    Args:
        code: Python code to validate

    Returns:
        Error message if invalid, None if valid
    """
    try:
        ast.parse(code)
        return None
    except SyntaxError as e:
        return f"Syntax error at line {e.lineno}: {e.msg}"
    except Exception as e:
        return f"Parse error: {str(e)}"


def validate_javascript_syntax(code: str) -> Optional[str]:
    """
    Basic JavaScript/TypeScript syntax validation.

    Checks:
    - Balanced braces, brackets, parentheses
    - Basic structure

    Note: This is not a full parser, just basic checks.

    Args:
        code: JavaScript/TypeScript code to validate

    Returns:
        Error message if invalid, None if valid
    """
    # Check balanced braces/brackets/parens
    stack = []
    pairs = {'{': '}', '[': ']', '(': ')'}
    in_string = False
    string_char = None
    prev_char = None

    for i, char in enumerate(code):
        # Handle strings (skip content inside strings)
        if char in ('"', "'", '`') and prev_char != '\\':
            if not in_string:
                in_string = True
                string_char = char
            elif char == string_char:
                in_string = False
                string_char = None
            prev_char = char
            continue

        prev_char = char

        if in_string:
            continue

        if char in pairs:
            stack.append(char)
        elif char in pairs.values():
            if not stack:
                return f"Unmatched closing '{char}' at position {i}"
            expected = pairs.get(stack.pop())
            if char != expected:
                return f"Mismatched bracket: expected '{expected}', got '{char}' at position {i}"

    if stack:
        unclosed = ', '.join(f"'{c}'" for c in stack)
        return f"Unclosed brackets: {unclosed}"

    return None


def validate_sql_syntax(code: str) -> Optional[str]:
    """
    Basic SQL syntax validation.

    Checks:
    - Contains recognizable SQL keywords
    - Basic structure

    Note: This is not a full SQL parser.

    Args:
        code: SQL code to validate

    Returns:
        Error message if invalid, None if valid
    """
    # Normalize and extract words
    words = set(re.findall(r'\b\w+\b', code.lower()))

    # Check if it contains any SQL keywords
    if not words.intersection(SQL_KEYWORDS):
        return "No recognizable SQL keywords found"

    return None


def validate_json_syntax(code: str) -> Optional[str]:
    """
    Validate JSON syntax.

    Args:
        code: JSON code to validate

    Returns:
        Error message if invalid, None if valid
    """
    import json
    try:
        json.loads(code)
        return None
    except json.JSONDecodeError as e:
        return f"JSON error at line {e.lineno}: {e.msg}"
    except Exception as e:
        return f"Parse error: {str(e)}"


def validate_yaml_syntax(code: str) -> Optional[str]:
    """
    Validate YAML syntax.

    Args:
        code: YAML code to validate

    Returns:
        Error message if invalid, None if valid
    """
    import yaml
    try:
        yaml.safe_load(code)
        return None
    except yaml.YAMLError as e:
        return f"YAML error: {str(e)}"
    except Exception as e:
        return f"Parse error: {str(e)}"


class CodeBlockValidator(BaseValidator):
    """
    Validates code blocks in markdown files.

    This validator:
    - Extracts all fenced code blocks
    - Validates syntax for supported languages
    - Reports findings by severity
    """

    # Map language identifiers to validators
    VALIDATORS = {
        'python': validate_python_syntax,
        'py': validate_python_syntax,
        'javascript': validate_javascript_syntax,
        'js': validate_javascript_syntax,
        'typescript': validate_javascript_syntax,
        'ts': validate_javascript_syntax,
        'tsx': validate_javascript_syntax,
        'jsx': validate_javascript_syntax,
        'sql': validate_sql_syntax,
        'json': validate_json_syntax,
        'yaml': validate_yaml_syntax,
        'yml': validate_yaml_syntax,
    }

    def __init__(
        self,
        required_languages: Optional[Set[str]] = None,
        validate_syntax: bool = True,
        min_code_blocks: int = 0,
    ):
        """
        Initialize the validator.

        Args:
            required_languages: Set of languages that must have at least one code block
            validate_syntax: Whether to validate code syntax (default: True)
            min_code_blocks: Minimum number of code blocks required (default: 0)
        """
        self.required_languages = required_languages or set()
        self.validate_syntax = validate_syntax
        self.min_code_blocks = min_code_blocks

    def validate(self, file_path: Path) -> ValidationResult:
        """Validate code blocks in a single file."""
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

        # Extract code blocks
        blocks = extract_code_blocks(content)

        # Check minimum code blocks
        if len(blocks) < self.min_code_blocks:
            findings.append(self._create_finding(
                Severity.S1_HIGH,
                "INSUFFICIENT_CODE_BLOCKS",
                f"Found {len(blocks)} code blocks, minimum required: {self.min_code_blocks}",
                file_path,
            ))

        # Check required languages
        found_languages = {lang for lang, _, _ in blocks if lang}
        for required in self.required_languages:
            if required.lower() not in found_languages:
                findings.append(self._create_finding(
                    Severity.S2_MEDIUM,
                    "MISSING_LANGUAGE_EXAMPLE",
                    f"No code block found for language: {required}",
                    file_path,
                    suggestion=f"Add a ```{required} code block",
                ))

        # Validate syntax
        if self.validate_syntax:
            for language, code, line_num in blocks:
                if language in self.VALIDATORS:
                    validator = self.VALIDATORS[language]
                    error = validator(code.strip())
                    if error:
                        findings.append(self._create_finding(
                            Severity.S2_MEDIUM,
                            "CODE_SYNTAX_ERROR",
                            f"Syntax error in {language} code block: {error}",
                            file_path,
                            line_number=line_num,
                        ))

        return self._create_result(
            findings,
            {
                "code_blocks": [
                    {"language": lang, "line": line, "length": len(code)}
                    for lang, code, line in blocks
                ],
                "languages_found": list(found_languages),
            }
        )
