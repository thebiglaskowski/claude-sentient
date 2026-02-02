"""
Base validation classes for Claude Conductor component validation.

Provides:
- Severity enum for classifying findings
- ValidationFinding dataclass for individual issues
- ValidationResult dataclass for validation outcomes
- BaseValidator abstract class for all validators
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class Severity(Enum):
    """
    Severity levels for validation findings.

    Aligned with Claude Conductor severity conventions:
    - S0: Critical - Blocker, prevents component from working
    - S1: High - Major issue, should be fixed before use
    - S2: Medium - Degraded but functional
    - S3: Low - Minor issue, polish
    """
    S0_CRITICAL = "S0"
    S1_HIGH = "S1"
    S2_MEDIUM = "S2"
    S3_LOW = "S3"

    def __str__(self) -> str:
        return self.value


@dataclass
class ValidationFinding:
    """
    Represents a single validation issue found during validation.

    Attributes:
        severity: The severity level of the finding
        code: A unique code identifying the type of issue (e.g., "MISSING_FRONTMATTER")
        message: Human-readable description of the issue
        file_path: Path to the file with the issue
        line_number: Optional line number where the issue occurs
        suggestion: Optional suggestion for how to fix the issue
    """
    severity: Severity
    code: str
    message: str
    file_path: Path
    line_number: Optional[int] = None
    suggestion: Optional[str] = None

    def __str__(self) -> str:
        location = f"{self.file_path}"
        if self.line_number:
            location += f":{self.line_number}"
        return f"[{self.severity}] {self.code}: {self.message} ({location})"

    def to_dict(self) -> Dict[str, Any]:
        """Convert finding to dictionary for JSON serialization."""
        return {
            "severity": str(self.severity),
            "code": self.code,
            "message": self.message,
            "file_path": str(self.file_path),
            "line_number": self.line_number,
            "suggestion": self.suggestion,
        }


@dataclass
class ValidationResult:
    """
    Result of validating a single file or component.

    Attributes:
        is_valid: True if no S0/S1 findings, False otherwise
        findings: List of all validation findings
        metadata: Additional data extracted during validation (e.g., parsed frontmatter)
    """
    is_valid: bool
    findings: List[ValidationFinding] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def critical_findings(self) -> List[ValidationFinding]:
        """Return only S0 (critical) findings."""
        return [f for f in self.findings if f.severity == Severity.S0_CRITICAL]

    @property
    def high_findings(self) -> List[ValidationFinding]:
        """Return only S1 (high) findings."""
        return [f for f in self.findings if f.severity == Severity.S1_HIGH]

    @property
    def blocking_findings(self) -> List[ValidationFinding]:
        """Return S0 and S1 findings that should block approval."""
        return [f for f in self.findings
                if f.severity in (Severity.S0_CRITICAL, Severity.S1_HIGH)]

    def has_severity(self, severity: Severity) -> bool:
        """Check if any finding has the given severity."""
        return any(f.severity == severity for f in self.findings)

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary for JSON serialization."""
        return {
            "is_valid": self.is_valid,
            "findings": [f.to_dict() for f in self.findings],
            "metadata": self.metadata,
        }


class BaseValidator(ABC):
    """
    Abstract base class for all component validators.

    Subclasses must implement the validate() method to check a single file.
    The validate_all() method is provided to validate multiple files.
    """

    @abstractmethod
    def validate(self, file_path: Path) -> ValidationResult:
        """
        Validate a single file.

        Args:
            file_path: Path to the file to validate

        Returns:
            ValidationResult with findings and metadata
        """
        pass

    def validate_all(self, directory: Path, pattern: str = "*.md") -> Dict[Path, ValidationResult]:
        """
        Validate all matching files in a directory.

        Args:
            directory: Directory to search for files
            pattern: Glob pattern for matching files (default: "*.md")

        Returns:
            Dictionary mapping file paths to their validation results
        """
        results = {}
        for file_path in directory.rglob(pattern):
            if file_path.is_file():
                results[file_path] = self.validate(file_path)
        return results

    def _create_finding(
        self,
        severity: Severity,
        code: str,
        message: str,
        file_path: Path,
        line_number: Optional[int] = None,
        suggestion: Optional[str] = None,
    ) -> ValidationFinding:
        """Helper method to create a ValidationFinding."""
        return ValidationFinding(
            severity=severity,
            code=code,
            message=message,
            file_path=file_path,
            line_number=line_number,
            suggestion=suggestion,
        )

    def _create_result(
        self,
        findings: List[ValidationFinding],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ValidationResult:
        """
        Helper method to create a ValidationResult.

        The is_valid flag is automatically set based on whether there are
        any S0 or S1 severity findings.
        """
        is_valid = not any(
            f.severity in (Severity.S0_CRITICAL, Severity.S1_HIGH)
            for f in findings
        )
        return ValidationResult(
            is_valid=is_valid,
            findings=findings,
            metadata=metadata or {},
        )
