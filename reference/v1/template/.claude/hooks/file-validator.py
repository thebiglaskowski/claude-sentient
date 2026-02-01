#!/usr/bin/env python3
"""
File Validator Hook (PreToolUse)

Validates file operations before execution to prevent accidents.
Checks for protected files, dangerous patterns, and size limits.

Hook Type: PreToolUse (matcher: tool in ["Write", "Edit", "NotebookEdit"])
Input: JSON with tool and file path
Output: Exit 0 to allow, exit 1 to block with message
"""

import json
import os
import re
import sys
from pathlib import Path

# Files that should never be modified
PROTECTED_FILES = [
    ".git/config",
    ".git/HEAD",
    ".git/index",
    ".gitignore",  # Warn but allow
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "Cargo.lock",
    "poetry.lock",
    "Gemfile.lock",
    ".env",
    ".env.local",
    ".env.production",
    "*.pem",
    "*.key",
    "*.p12",
    "id_rsa",
    "id_ed25519"
]

# Patterns that require extra caution
CAUTION_PATTERNS = [
    r".*\.lock$",
    r".*\.min\.js$",
    r".*\.min\.css$",
    r"node_modules/.*",
    r"\.git/.*",
    r"vendor/.*",
    r"dist/.*",
    r"build/.*",
    r"__pycache__/.*",
    r"\.pyc$"
]

# Files that should trigger warnings but not blocks
WARN_FILES = [
    "README.md",
    "CHANGELOG.md",
    "LICENSE",
    "package.json",
    "tsconfig.json",
    "pyproject.toml",
    "Cargo.toml"
]

# Maximum file size to write (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024


def is_protected(file_path: str) -> tuple[bool, str]:
    """Check if file is protected from modification."""
    path = Path(file_path)
    name = path.name

    for protected in PROTECTED_FILES:
        if protected.startswith("*"):
            # Glob pattern
            if path.match(protected):
                return True, f"Protected pattern: {protected}"
        elif name == protected or str(path).endswith(protected):
            return True, f"Protected file: {protected}"

    return False, ""


def matches_caution_pattern(file_path: str) -> tuple[bool, str]:
    """Check if file matches a caution pattern."""
    for pattern in CAUTION_PATTERNS:
        if re.match(pattern, file_path):
            return True, f"Caution pattern: {pattern}"
    return False, ""


def is_warn_file(file_path: str) -> tuple[bool, str]:
    """Check if file should trigger a warning."""
    path = Path(file_path)
    name = path.name

    for warn in WARN_FILES:
        if name == warn:
            return True, f"Important file: {warn}"

    return False, ""


def check_content_safety(content: str) -> tuple[bool, str]:
    """Check if content appears safe to write."""
    # Check for potential secrets
    secret_patterns = [
        r"(api[_-]?key|apikey)\s*[=:]\s*['\"][^'\"]+['\"]",
        r"(secret|password|passwd|pwd)\s*[=:]\s*['\"][^'\"]+['\"]",
        r"(access[_-]?token|auth[_-]?token)\s*[=:]\s*['\"][^'\"]+['\"]",
        r"-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----",
        r"sk-[a-zA-Z0-9]{48}",  # OpenAI API key pattern
        r"ghp_[a-zA-Z0-9]{36}",  # GitHub token pattern
    ]

    for pattern in secret_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return False, "Potential secret detected in content"

    # Check file size
    if len(content) > MAX_FILE_SIZE:
        return False, f"Content exceeds maximum size ({len(content)} > {MAX_FILE_SIZE})"

    return True, ""


def validate_file_operation(data: dict) -> tuple[bool, str, str]:
    """
    Validate a file operation.
    Returns: (allowed, severity, message)
    severity: "block", "warn", "info"
    """
    tool = data.get("tool", "")
    tool_input = data.get("tool_input", {})

    # Get file path based on tool
    file_path = tool_input.get("file_path", "")
    if not file_path:
        file_path = tool_input.get("path", "")
    if not file_path:
        file_path = tool_input.get("notebook_path", "")

    if not file_path:
        return True, "info", "No file path to validate"

    # Check protected files
    protected, reason = is_protected(file_path)
    if protected:
        # Allow .gitignore with warning
        if ".gitignore" in file_path:
            return True, "warn", f"Modifying {reason} - ensure intentional"
        return False, "block", f"Blocked: {reason}"

    # Check caution patterns
    caution, reason = matches_caution_pattern(file_path)
    if caution:
        return False, "block", f"Blocked: {reason} - likely generated/external file"

    # Check warn files
    warn, reason = is_warn_file(file_path)
    if warn:
        return True, "warn", f"Modifying {reason} - verify changes"

    # Check content if available (for Write tool)
    if tool == "Write":
        content = tool_input.get("content", "")
        if content:
            safe, reason = check_content_safety(content)
            if not safe:
                return False, "block", f"Blocked: {reason}"

    return True, "info", "Validation passed"


def main():
    """Main hook entry point."""
    try:
        input_data = sys.stdin.read()

        if not input_data.strip():
            sys.exit(0)  # Allow if no input

        data = json.loads(input_data)

        # Validate the operation
        allowed, severity, message = validate_file_operation(data)

        if severity == "block":
            print(f"[File Validator] ✗ {message}", file=sys.stderr)
            sys.exit(1)  # Block the operation

        if severity == "warn":
            print(f"[File Validator] ⚠ {message}", file=sys.stderr)

        sys.exit(0)  # Allow the operation

    except json.JSONDecodeError:
        sys.exit(0)  # Allow on parse error
    except Exception as e:
        print(f"[File Validator Error] {e}", file=sys.stderr)
        sys.exit(0)  # Allow on error (fail open)


if __name__ == "__main__":
    main()
