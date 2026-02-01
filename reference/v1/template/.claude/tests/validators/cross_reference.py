"""
Cross-reference validation for Claude Conductor components.

Validates that references between components are valid:
- @rules/[name] references
- @patterns/[name] references
- snippet:[name] references
- Agent references
"""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from .base import BaseValidator, Severity, ValidationFinding, ValidationResult


# Patterns for detecting cross-references
RULES_REF_PATTERN = re.compile(r"@rules/(\w[\w-]*)", re.IGNORECASE)
PATTERNS_REF_PATTERN = re.compile(r"@patterns/(\w[\w-]*)", re.IGNORECASE)
SNIPPET_REF_PATTERN = re.compile(r"snippet:(\w[\w-]*)", re.IGNORECASE)
# Pattern for agent references - look for agent names with known suffixes
AGENT_SUFFIXES = r"analyst|engineer|expert|writer|reviewer|specialist|optimizer|designer"
AGENT_REF_PATTERN = re.compile(
    rf"(?:spawn|use)\s+(\w[\w-]*-(?:{AGENT_SUFFIXES}))\b",
    re.IGNORECASE
)


class CrossReferenceRegistry:
    """
    Registry of valid cross-reference targets.

    Scans component directories to build a registry of valid references.
    """

    def __init__(self, base_path: Path):
        """
        Initialize the registry.

        Args:
            base_path: Base path to the .claude directory
        """
        self.base_path = base_path
        self._rules: Set[str] = set()
        self._patterns: Set[str] = set()
        self._snippets: Set[str] = set()
        self._agents: Set[str] = set()
        self._loaded = False

    def _load(self) -> None:
        """Lazy-load all valid references from the filesystem."""
        if self._loaded:
            return

        # Load rules
        rules_dir = self.base_path / "rules"
        if rules_dir.exists():
            for f in rules_dir.glob("*.md"):
                if not f.name.startswith("_"):
                    self._rules.add(f.stem.lower())

        # Load patterns (may be in subdirectories)
        patterns_dir = self.base_path / "patterns"
        if patterns_dir.exists():
            for f in patterns_dir.rglob("*.md"):
                if not f.name.startswith("_"):
                    self._patterns.add(f.stem.lower())

        # Load snippets (may be in subdirectories)
        snippets_dir = self.base_path / "snippets"
        if snippets_dir.exists():
            for f in snippets_dir.rglob("*.md"):
                if not f.name.startswith("_"):
                    self._snippets.add(f.stem.lower())

        # Load agents
        agents_dir = self.base_path / "agents"
        if agents_dir.exists():
            for f in agents_dir.glob("*.md"):
                if not f.name.startswith("_"):
                    self._agents.add(f.stem.lower())

        self._loaded = True

    @property
    def rules(self) -> Set[str]:
        """Get all valid rule names."""
        self._load()
        return self._rules

    @property
    def patterns(self) -> Set[str]:
        """Get all valid pattern names."""
        self._load()
        return self._patterns

    @property
    def snippets(self) -> Set[str]:
        """Get all valid snippet names."""
        self._load()
        return self._snippets

    @property
    def agents(self) -> Set[str]:
        """Get all valid agent names."""
        self._load()
        return self._agents


def extract_references(content: str) -> Dict[str, List[Tuple[str, int]]]:
    """
    Extract all cross-references from content.

    Args:
        content: File content to scan

    Returns:
        Dictionary mapping reference type to list of (name, line_number) tuples
    """
    references = {
        "rules": [],
        "patterns": [],
        "snippets": [],
        "agents": [],
    }

    # Track if we're inside a code block
    in_code_block = False
    lines = content.split('\n')

    for i, line in enumerate(lines, 1):
        # Track code blocks (skip references inside code)
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue

        if in_code_block:
            continue

        # Find rules references
        for match in RULES_REF_PATTERN.finditer(line):
            references["rules"].append((match.group(1).lower(), i))

        # Find patterns references
        for match in PATTERNS_REF_PATTERN.finditer(line):
            references["patterns"].append((match.group(1).lower(), i))

        # Find snippet references (but not in comment-style definitions)
        # Skip lines that look like snippet definitions (e.g., "// snippet:name")
        if not line.strip().startswith('//') and not line.strip().startswith('#'):
            for match in SNIPPET_REF_PATTERN.finditer(line):
                references["snippets"].append((match.group(1).lower(), i))

        # Find agent references
        for match in AGENT_REF_PATTERN.finditer(line):
            references["agents"].append((match.group(1).lower(), i))

    return references


class CrossReferenceValidator(BaseValidator):
    """
    Validates cross-references in markdown files.

    Checks that all references to:
    - @rules/[name]
    - @patterns/[name]
    - snippet:[name]
    - agents

    resolve to existing components.
    """

    def __init__(self, registry: CrossReferenceRegistry):
        """
        Initialize the validator.

        Args:
            registry: CrossReferenceRegistry with valid reference targets
        """
        self.registry = registry

    def validate(self, file_path: Path) -> ValidationResult:
        """Validate cross-references in a single file."""
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

        references = extract_references(content)

        # Validate rules references
        for name, line_num in references["rules"]:
            if name not in self.registry.rules:
                findings.append(self._create_finding(
                    Severity.S1_HIGH,
                    "INVALID_RULES_REF",
                    f"Reference to non-existent rule: @rules/{name}",
                    file_path,
                    line_number=line_num,
                    suggestion=f"Valid rules: {', '.join(sorted(self.registry.rules)[:10])}...",
                ))

        # Validate patterns references
        for name, line_num in references["patterns"]:
            if name not in self.registry.patterns:
                findings.append(self._create_finding(
                    Severity.S1_HIGH,
                    "INVALID_PATTERNS_REF",
                    f"Reference to non-existent pattern: @patterns/{name}",
                    file_path,
                    line_number=line_num,
                    suggestion=f"Valid patterns: {', '.join(sorted(self.registry.patterns)[:10])}...",
                ))

        # Validate snippet references
        for name, line_num in references["snippets"]:
            if name not in self.registry.snippets:
                findings.append(self._create_finding(
                    Severity.S1_HIGH,
                    "INVALID_SNIPPET_REF",
                    f"Reference to non-existent snippet: snippet:{name}",
                    file_path,
                    line_number=line_num,
                    suggestion=f"Valid snippets: {', '.join(sorted(self.registry.snippets)[:10])}...",
                ))

        # Validate agent references
        for name, line_num in references["agents"]:
            if name not in self.registry.agents:
                findings.append(self._create_finding(
                    Severity.S2_MEDIUM,
                    "INVALID_AGENT_REF",
                    f"Reference to non-existent agent: {name}",
                    file_path,
                    line_number=line_num,
                    suggestion=f"Valid agents: {', '.join(sorted(self.registry.agents)[:10])}...",
                ))

        return self._create_result(
            findings,
            {"references": references}
        )


def validate_all_cross_references(base_path: Path) -> Dict[Path, ValidationResult]:
    """
    Validate cross-references across all components.

    Args:
        base_path: Base path to the .claude directory

    Returns:
        Dictionary mapping file paths to validation results
    """
    registry = CrossReferenceRegistry(base_path)
    validator = CrossReferenceValidator(registry)

    results = {}

    # Validate all markdown files in component directories
    component_dirs = ["commands", "skills", "agents", "patterns", "snippets", "rules"]
    for dir_name in component_dirs:
        dir_path = base_path / dir_name
        if dir_path.exists():
            for file_path in dir_path.rglob("*.md"):
                if not file_path.name.startswith("_"):
                    results[file_path] = validator.validate(file_path)

    return results
