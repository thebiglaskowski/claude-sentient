#!/usr/bin/env python3
"""
Bash Auto-Approve Hook (PermissionRequest / PreToolUse)

Automatically approves safe, read-only bash commands to reduce permission prompts.
Returns exit code 0 to approve, exit code 1 to require manual approval.

Hook Type: PreToolUse (matcher: tool == "Bash")
"""

import json
import re
import sys

# Safe command patterns that can be auto-approved
# These are read-only or have no side effects
SAFE_PATTERNS = [
    # Read-only file operations
    r"^ls(\s|$)",
    r"^cat\s",
    r"^head\s",
    r"^tail\s",
    r"^less\s",
    r"^more\s",
    r"^wc\s",
    r"^diff\s",
    r"^file\s",
    r"^stat\s",
    r"^du\s",
    r"^df\s",
    r"^pwd$",
    r"^which\s",
    r"^whereis\s",
    r"^type\s",
    r"^realpath\s",
    r"^dirname\s",
    r"^basename\s",

    # Git read operations
    r"^git\s+status",
    r"^git\s+log",
    r"^git\s+diff",
    r"^git\s+show",
    r"^git\s+branch(\s+-[alr]|\s*$)",
    r"^git\s+remote\s+-v",
    r"^git\s+config\s+--get",
    r"^git\s+rev-parse",
    r"^git\s+describe",
    r"^git\s+ls-files",
    r"^git\s+ls-tree",
    r"^git\s+blame",
    r"^git\s+shortlog",
    r"^git\s+stash\s+list",

    # Package info (not install)
    r"^npm\s+list",
    r"^npm\s+ls",
    r"^npm\s+outdated",
    r"^npm\s+audit(\s+--json)?",
    r"^npm\s+view",
    r"^npm\s+info",
    r"^npm\s+search",
    r"^npm\s+config\s+get",
    r"^yarn\s+list",
    r"^yarn\s+info",
    r"^yarn\s+why",
    r"^pip\s+list",
    r"^pip\s+show",
    r"^pip\s+freeze",
    r"^pip\s+check",
    r"^pipenv\s+graph",
    r"^poetry\s+show",
    r"^cargo\s+tree",
    r"^go\s+list",
    r"^go\s+mod\s+graph",

    # Tests (read-only verification)
    r"^npm\s+test",
    r"^npm\s+run\s+test",
    r"^yarn\s+test",
    r"^pytest",
    r"^jest",
    r"^mocha",
    r"^vitest",
    r"^cargo\s+test",
    r"^go\s+test",
    r"^mix\s+test",
    r"^rspec",
    r"^phpunit",

    # Linting (read-only checks)
    r"^npm\s+run\s+lint",
    r"^npm\s+run\s+format",
    r"^npx\s+eslint",
    r"^npx\s+prettier\s+--check",
    r"^yarn\s+lint",
    r"^pylint",
    r"^flake8",
    r"^black\s+--check",
    r"^ruff\s+check",
    r"^mypy",
    r"^cargo\s+clippy",
    r"^cargo\s+fmt\s+--check",
    r"^golint",
    r"^go\s+vet",
    r"^gofmt\s+-l",
    r"^rubocop",
    r"^shellcheck",

    # Type checking
    r"^npx\s+tsc\s+--noEmit",
    r"^yarn\s+tsc\s+--noEmit",
    r"^tsc\s+--noEmit",
    r"^mypy",
    r"^pyright",

    # Build verification (no write)
    r"^npm\s+run\s+build\s+--dry-run",
    r"^cargo\s+check",

    # Environment info
    r"^node\s+--version",
    r"^npm\s+--version",
    r"^python\s+--version",
    r"^python3\s+--version",
    r"^go\s+version",
    r"^cargo\s+--version",
    r"^rustc\s+--version",
    r"^ruby\s+--version",
    r"^php\s+--version",
    r"^java\s+--version",
    r"^dotnet\s+--version",
    r"^echo\s+\$",
    r"^printenv",
    r"^env$",

    # Process info
    r"^ps\s",
    r"^top\s+-bn1",
    r"^pgrep",
    r"^lsof",
]

# Dangerous patterns that should NEVER be auto-approved
DANGEROUS_PATTERNS = [
    r"rm\s+-rf\s+/",
    r"rm\s+-rf\s+\*",
    r"rm\s+-rf\s+\.",
    r"sudo\s",
    r"chmod\s+777",
    r">\s*/dev/",
    r"mkfs",
    r"dd\s+if=",
    r":\s*\(\)\s*\{",  # Fork bomb
    r"git\s+push\s+--force",
    r"git\s+push\s+-f\s",
    r"git\s+reset\s+--hard",
    r"git\s+clean\s+-fd",
    r"npm\s+publish",
    r"pip\s+install\s+--user",
    r"curl\s+.*\|\s*(ba)?sh",
    r"wget\s+.*\|\s*(ba)?sh",
    r"eval\s+",
]


def is_safe_command(command: str) -> bool:
    """Check if a command is safe to auto-approve."""
    command = command.strip()

    # First check for dangerous patterns
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return False

    # Then check for safe patterns
    for pattern in SAFE_PATTERNS:
        if re.match(pattern, command, re.IGNORECASE):
            return True

    return False


def main():
    """Main hook entry point."""
    try:
        # Read input from stdin
        input_data = sys.stdin.read()

        if not input_data.strip():
            sys.exit(1)  # Require approval if no input

        data = json.loads(input_data)

        # Get the bash command
        command = ""
        if "tool_input" in data and "command" in data["tool_input"]:
            command = data["tool_input"]["command"]

        if not command:
            sys.exit(1)  # Require approval if no command

        # Check if command is safe
        if is_safe_command(command):
            # Auto-approve
            sys.exit(0)
        else:
            # Require manual approval
            sys.exit(1)

    except json.JSONDecodeError:
        sys.exit(1)  # Require approval on parse error
    except Exception as e:
        print(f"[Auto-Approve Error] {e}", file=sys.stderr)
        sys.exit(1)  # Require approval on any error


if __name__ == "__main__":
    main()
