"""
Negative test cases for validation edge cases.

Tests that validators correctly detect and report:
- Missing frontmatter
- Invalid code syntax
- Empty/minimal content
- Missing required fields
"""

import pytest
import tempfile
from pathlib import Path

from validators.frontmatter import FrontmatterValidator, FrontmatterSchema
from validators.markdown import MarkdownValidator
from validators.code_blocks import CodeBlockValidator, validate_python_syntax
from validators.base import Severity


class TestMissingFrontmatter:
    """Test detection of missing frontmatter."""

    def test_missing_frontmatter_detected(self):
        """Verify files without frontmatter are flagged as critical."""
        schema = FrontmatterSchema(
            required_fields={"name", "description"},
            optional_fields={"version"},
        )
        validator = FrontmatterValidator(schema, require_frontmatter=True)

        # Create a temporary file without frontmatter
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("# Just a Title\n\nSome content without frontmatter.\n")
            temp_path = Path(f.name)

        try:
            result = validator.validate(temp_path)

            # Should have findings
            assert not result.is_valid, "File without frontmatter should be invalid"
            assert len(result.findings) > 0, "Should have at least one finding"

            # Should be critical severity
            critical_findings = [f for f in result.findings if f.severity == Severity.S0_CRITICAL]
            assert len(critical_findings) > 0, "Missing frontmatter should be S0_CRITICAL"

            # Should have correct error code
            codes = [f.code for f in result.findings]
            assert "MISSING_FRONTMATTER" in codes, "Should have MISSING_FRONTMATTER code"
        finally:
            temp_path.unlink()

    def test_optional_frontmatter_allowed(self):
        """Verify files without frontmatter pass when frontmatter is optional."""
        schema = FrontmatterSchema(
            required_fields={"name"},
            optional_fields=set(),
        )
        validator = FrontmatterValidator(schema, require_frontmatter=False)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("# Just Content\n\nNo frontmatter here.\n")
            temp_path = Path(f.name)

        try:
            result = validator.validate(temp_path)
            # Should not have MISSING_FRONTMATTER error when not required
            codes = [f.code for f in result.findings]
            assert "MISSING_FRONTMATTER" not in codes
        finally:
            temp_path.unlink()


class TestMissingRequiredFields:
    """Test detection of missing required fields in frontmatter."""

    def test_missing_required_field_detected(self):
        """Verify missing required fields are flagged."""
        schema = FrontmatterSchema(
            required_fields={"name", "description", "model"},
            optional_fields={"version"},
        )
        validator = FrontmatterValidator(schema)

        # Create file with incomplete frontmatter (missing 'model')
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("""---
name: test-command
description: A test command
---

# Test Command

Some content.
""")
            temp_path = Path(f.name)

        try:
            result = validator.validate(temp_path)

            # Should have findings about missing field
            assert len(result.findings) > 0, "Should detect missing required field"

            # Find the missing field error (validator uses MISSING_REQUIRED_FIELD)
            missing_field_findings = [f for f in result.findings if "MISSING_REQUIRED_FIELD" in f.code]
            assert len(missing_field_findings) > 0, "Should have MISSING_REQUIRED_FIELD finding"

            # Check that 'model' is mentioned
            messages = " ".join(f.message for f in result.findings)
            assert "model" in messages.lower(), "Should mention the missing 'model' field"
        finally:
            temp_path.unlink()


class TestInvalidPythonSyntax:
    """Test detection of invalid Python syntax in code blocks."""

    def test_python_syntax_error_detected(self):
        """Verify Python syntax errors are caught."""
        # Test the direct validation function
        invalid_python = """
def broken_function(
    # Missing closing parenthesis and colon
    print("This won't parse")
"""
        error = validate_python_syntax(invalid_python)
        assert error is not None, "Should detect Python syntax error"
        assert "syntax" in error.lower() or "error" in error.lower()

    def test_valid_python_passes(self):
        """Verify valid Python passes validation."""
        valid_python = """
def working_function():
    print("This works")
    return True
"""
        error = validate_python_syntax(valid_python)
        assert error is None, f"Valid Python should pass, got: {error}"

    def test_code_block_validator_catches_python_errors(self):
        """Verify CodeBlockValidator catches Python syntax errors in files."""
        validator = CodeBlockValidator(min_code_blocks=1)

        # Create file with invalid Python code block
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("""# Test Snippet

## Code

```python
def broken(:
    print("syntax error"
```

## Description

This has broken Python.
""")
            temp_path = Path(f.name)

        try:
            result = validator.validate(temp_path)

            # Should have syntax error finding
            syntax_findings = [f for f in result.findings if "SYNTAX" in f.code]
            assert len(syntax_findings) > 0, "Should detect Python syntax error in code block"
        finally:
            temp_path.unlink()


class TestEmptyContent:
    """Test detection of empty or minimal content."""

    def test_empty_content_flagged(self):
        """Verify files with minimal content are flagged."""
        validator = MarkdownValidator(
            required_sections=[],
            min_content_length=50,  # Require at least 50 chars
        )

        # Create file with very little content
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("""---
name: empty
---

# Title

Short.
""")
            temp_path = Path(f.name)

        try:
            result = validator.validate(temp_path)

            # Should have content length finding
            short_findings = [f for f in result.findings if "SHORT" in f.code or "LENGTH" in f.code]
            assert len(short_findings) > 0, "Should flag content that's too short"
        finally:
            temp_path.unlink()

    def test_adequate_content_passes(self):
        """Verify files with adequate content pass."""
        validator = MarkdownValidator(
            required_sections=[],
            min_content_length=50,
        )

        # Create file with sufficient content
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("""---
name: adequate
---

# Title

This is a file with adequate content that should pass the minimum
content length validation. It has multiple sentences and provides
enough text to meet the threshold.
""")
            temp_path = Path(f.name)

        try:
            result = validator.validate(temp_path)

            # Should not have content length finding
            short_findings = [f for f in result.findings if "SHORT" in f.code or "LENGTH" in f.code]
            assert len(short_findings) == 0, f"Adequate content should pass, got: {short_findings}"
        finally:
            temp_path.unlink()


class TestMissingSections:
    """Test detection of missing required sections."""

    def test_missing_section_detected(self):
        """Verify missing required sections are flagged."""
        validator = MarkdownValidator(
            required_sections=["Description", "Usage", "Examples"],
            min_content_length=10,
        )

        # Create file missing 'Examples' section
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("""---
name: incomplete
---

# Title

## Description

This describes the thing.

## Usage

How to use it.

No examples section here!
""")
            temp_path = Path(f.name)

        try:
            result = validator.validate(temp_path)

            # Should have missing section finding
            section_findings = [f for f in result.findings if "SECTION" in f.code]
            assert len(section_findings) > 0, "Should detect missing required section"

            # Should mention 'examples'
            messages = " ".join(f.message.lower() for f in result.findings)
            assert "example" in messages, "Should mention the missing 'Examples' section"
        finally:
            temp_path.unlink()


class TestInvalidFieldValues:
    """Test detection of invalid field values."""

    def test_invalid_model_value_detected(self):
        """Verify invalid model values are flagged."""
        # The field_validator should return an error message when validation fails,
        # or None/empty string when valid
        def validate_model(v):
            if v not in ["sonnet", "opus", "haiku"]:
                return f"Invalid model: {v}. Must be one of: sonnet, opus, haiku"
            return None

        schema = FrontmatterSchema(
            required_fields={"name", "model"},
            optional_fields=set(),
            field_validators={
                "model": validate_model,
            },
        )
        validator = FrontmatterValidator(schema)

        # Create file with invalid model value
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("""---
name: test
model: invalid-model-name
---

# Content
""")
            temp_path = Path(f.name)

        try:
            result = validator.validate(temp_path)

            # Should have field validation failed finding (uses FIELD_VALIDATION_FAILED code)
            invalid_findings = [f for f in result.findings if "VALIDATION_FAILED" in f.code]
            assert len(invalid_findings) > 0, "Should detect invalid model value"
        finally:
            temp_path.unlink()


class TestFileReadErrors:
    """Test handling of file read errors."""

    def test_nonexistent_file_handled(self):
        """Verify non-existent files are handled gracefully."""
        schema = FrontmatterSchema(required_fields={"name"}, optional_fields=set())
        validator = FrontmatterValidator(schema)

        fake_path = Path("/nonexistent/path/to/file.md")
        result = validator.validate(fake_path)

        # Should have file read error
        assert not result.is_valid
        error_findings = [f for f in result.findings if "ERROR" in f.code or "READ" in f.code]
        assert len(error_findings) > 0, "Should report file read error"
        assert error_findings[0].severity == Severity.S0_CRITICAL


class TestValidationResultHelpers:
    """Test ValidationResult helper methods."""

    def test_blocking_findings_filter(self):
        """Verify blocking_findings filters correctly."""
        from validators.base import ValidationFinding, ValidationResult

        findings = [
            ValidationFinding(Severity.S0_CRITICAL, "CRIT", "Critical", Path("test.md")),
            ValidationFinding(Severity.S1_HIGH, "HIGH", "High", Path("test.md")),
            ValidationFinding(Severity.S2_MEDIUM, "MED", "Medium", Path("test.md")),
            ValidationFinding(Severity.S3_LOW, "LOW", "Low", Path("test.md")),
        ]

        result = ValidationResult(is_valid=False, findings=findings, metadata={})

        # S0 and S1 are blocking
        blocking = result.blocking_findings
        assert len(blocking) == 2
        assert all(f.severity in [Severity.S0_CRITICAL, Severity.S1_HIGH] for f in blocking)

    def test_finding_str_representation(self):
        """Verify ValidationFinding __str__ works correctly."""
        from validators.base import ValidationFinding

        finding = ValidationFinding(
            severity=Severity.S1_HIGH,
            code="TEST_CODE",
            message="Test message",
            file_path=Path("test/file.md"),
            line_number=42,
        )

        str_repr = str(finding)
        assert "S1" in str_repr or "HIGH" in str_repr
        assert "TEST_CODE" in str_repr
        assert "Test message" in str_repr
        assert "42" in str_repr

    def test_finding_to_dict(self):
        """Verify ValidationFinding to_dict works correctly."""
        from validators.base import ValidationFinding

        finding = ValidationFinding(
            severity=Severity.S2_MEDIUM,
            code="DICT_TEST",
            message="Dictionary test",
            file_path=Path("dict/test.md"),
            line_number=10,
            suggestion="Fix it",
        )

        d = finding.to_dict()
        assert d["code"] == "DICT_TEST"
        assert d["message"] == "Dictionary test"
        assert d["line_number"] == 10
        assert d["suggestion"] == "Fix it"
