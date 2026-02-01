#!/usr/bin/env python3
"""
Context Injector Hook (UserPromptSubmit)

Analyzes each user prompt and injects relevant context dynamically.
Outputs context suggestions as a system message.

Hook Type: UserPromptSubmit
Input: JSON with conversation_history and user prompt
Output: System message with context suggestions (to stderr)
"""

import json
import re
import sys
import os
from pathlib import Path

# Keyword to context mapping
# Keys are regex patterns, values are lists of paths/rules to suggest
CONTEXT_MAP = {
    # Security-related
    r"(auth|login|session|password|token|jwt|oauth|permission|role|access)": {
        "paths": ["src/auth/", "middleware/auth", "lib/auth"],
        "rules": ["@rules/security"],
        "agents": ["security-analyst"]
    },

    # API-related
    r"(api|endpoint|route|rest|graphql|controller|handler)": {
        "paths": ["src/api/", "routes/", "controllers/", "openapi.yaml", "swagger.json"],
        "rules": ["@rules/api-design", "@rules/error-handling"],
        "agents": ["code-reviewer"]
    },

    # Database-related
    r"(database|db|query|schema|migration|model|prisma|sequelize|mongoose|sql)": {
        "paths": ["prisma/", "src/db/", "models/", "migrations/", "schema.prisma"],
        "rules": ["@rules/database"],
        "agents": ["database-expert"]
    },

    # Testing-related
    r"(test|coverage|jest|pytest|spec|mock|fixture)": {
        "paths": ["__tests__/", "tests/", "test/", "*.test.*", "*.spec.*", "jest.config", "pytest.ini"],
        "rules": ["@rules/testing"],
        "agents": ["test-engineer"]
    },

    # Security audit
    r"(security|vuln|vulnerability|cve|exploit|xss|injection|csrf)": {
        "paths": ["src/auth/", "src/api/", "middleware/"],
        "rules": ["@rules/security"],
        "agents": ["security-analyst"]
    },

    # UI/Frontend
    r"(ui|component|page|form|button|modal|dialog|layout|style|css|tailwind)": {
        "paths": ["src/components/", "src/pages/", "src/ui/", "styles/"],
        "rules": ["@rules/ui-ux-design"],
        "agents": ["ui-ux-expert", "accessibility-expert"]
    },

    # Performance
    r"(perf|performance|slow|optimize|cache|lazy|bundle|speed)": {
        "paths": ["src/", "webpack.config", "vite.config", "next.config"],
        "rules": ["@rules/performance"],
        "agents": []
    },

    # Documentation
    r"(doc|readme|changelog|comment|explain|guide)": {
        "paths": ["README.md", "docs/", "CHANGELOG.md"],
        "rules": ["@rules/documentation"],
        "agents": ["documentation-writer"]
    },

    # Error handling
    r"(error|exception|catch|throw|fail|crash|bug|fix)": {
        "paths": ["src/", "lib/"],
        "rules": ["@rules/error-handling", "@rules/logging"],
        "agents": []
    },

    # DevOps/CI
    r"(ci|cd|deploy|docker|kubernetes|k8s|pipeline|github.?action|workflow)": {
        "paths": [".github/", "Dockerfile", "docker-compose", ".gitlab-ci", "Jenkinsfile"],
        "rules": [],
        "agents": ["devops-engineer"]
    },

    # Terminal/CLI
    r"(cli|terminal|command|console|argv|flag|spinner|progress)": {
        "paths": ["src/cli/", "bin/", "commands/"],
        "rules": ["@rules/terminal-ui"],
        "agents": ["terminal-ui-expert"]
    }
}


def analyze_prompt(prompt: str) -> dict:
    """Analyze prompt and return context suggestions."""
    prompt_lower = prompt.lower()

    suggestions = {
        "paths": set(),
        "rules": set(),
        "agents": set()
    }

    for pattern, context in CONTEXT_MAP.items():
        if re.search(pattern, prompt_lower):
            suggestions["paths"].update(context.get("paths", []))
            suggestions["rules"].update(context.get("rules", []))
            suggestions["agents"].update(context.get("agents", []))

    return {
        "paths": sorted(suggestions["paths"]),
        "rules": sorted(suggestions["rules"]),
        "agents": sorted(suggestions["agents"])
    }


def find_existing_paths(suggested_paths: list) -> list:
    """Filter suggested paths to only those that exist."""
    cwd = Path.cwd()
    existing = []

    for path_pattern in suggested_paths:
        # Handle glob patterns
        if "*" in path_pattern:
            matches = list(cwd.glob(path_pattern))
            existing.extend([str(m.relative_to(cwd)) for m in matches[:5]])  # Limit to 5
        else:
            path = cwd / path_pattern
            if path.exists():
                existing.append(path_pattern)

    return existing[:10]  # Limit total suggestions


def format_context_message(suggestions: dict, existing_paths: list) -> str:
    """Format context suggestions as a system message."""
    parts = []

    if existing_paths:
        parts.append(f"Relevant paths: {', '.join(existing_paths)}")

    if suggestions["rules"]:
        parts.append(f"Recommended rules: {', '.join(suggestions['rules'])}")

    if suggestions["agents"]:
        parts.append(f"Consider agents: {', '.join(suggestions['agents'])}")

    if parts:
        return "[Context] " + " | ".join(parts)

    return ""


def main():
    """Main hook entry point."""
    try:
        # Read input from stdin
        input_data = sys.stdin.read()

        if not input_data.strip():
            sys.exit(0)

        data = json.loads(input_data)

        # Get the user's prompt
        prompt = ""
        if "user_prompt" in data:
            prompt = data["user_prompt"]
        elif "tool_input" in data and "prompt" in data["tool_input"]:
            prompt = data["tool_input"]["prompt"]

        if not prompt:
            sys.exit(0)

        # Analyze and suggest context
        suggestions = analyze_prompt(prompt)

        if any(suggestions.values()):
            existing_paths = find_existing_paths(suggestions["paths"])
            message = format_context_message(suggestions, existing_paths)

            if message:
                print(message, file=sys.stderr)

        sys.exit(0)

    except json.JSONDecodeError:
        # Not valid JSON, skip
        sys.exit(0)
    except Exception as e:
        print(f"[Context Hook Error] {e}", file=sys.stderr)
        sys.exit(0)  # Don't fail the operation


if __name__ == "__main__":
    main()
