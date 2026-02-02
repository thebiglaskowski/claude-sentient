#!/usr/bin/env python3
"""
Error Recovery Hook (PostToolUseFailure)

Classifies errors and suggests recovery strategies.
Implements retry logic with exponential backoff for transient errors.

Hook Type: PostToolUseFailure
Input: JSON with error details
Output: Recovery suggestion or retry instruction
"""

import json
import re
import sys
import time
from dataclasses import dataclass
from typing import Optional

@dataclass
class RecoveryStrategy:
    action: str  # "retry", "suggest", "queue", "escalate"
    message: str
    max_retries: int = 0
    delay: float = 0
    backoff: str = "linear"  # "linear" or "exponential"
    command: Optional[str] = None


# Error patterns and their recovery strategies
RECOVERY_STRATEGIES = {
    # Network errors - retry with backoff
    r"ETIMEDOUT|ECONNRESET|ECONNREFUSED|ENOTFOUND|EHOSTUNREACH": RecoveryStrategy(
        action="retry",
        message="Network error detected. Retrying with backoff...",
        max_retries=3,
        delay=2.0,
        backoff="exponential"
    ),

    # Rate limiting
    r"429|rate.?limit|too many requests|quota exceeded": RecoveryStrategy(
        action="retry",
        message="Rate limited. Waiting before retry...",
        max_retries=3,
        delay=5.0,
        backoff="exponential"
    ),

    # File/resource locks
    r"EBUSY|lock|index\.lock|resource busy|locked": RecoveryStrategy(
        action="retry",
        message="Resource locked. Waiting for release...",
        max_retries=5,
        delay=1.0,
        backoff="linear"
    ),

    # Git lock specifically
    r"\.git/index\.lock": RecoveryStrategy(
        action="suggest",
        message="Git index is locked. Try: rm -f .git/index.lock",
        command="rm -f .git/index.lock"
    ),

    # Missing module/package
    r"MODULE_NOT_FOUND|Cannot find module|No module named|ImportError": RecoveryStrategy(
        action="suggest",
        message="Missing dependency detected. Run package install.",
        command="npm install"  # or pip install, etc.
    ),

    # TypeScript/Type errors
    r"TypeError|type.?error|TS\d{4}": RecoveryStrategy(
        action="queue",
        message="Type error detected. Adding to work queue as S1."
    ),

    # Syntax errors
    r"SyntaxError|Unexpected token|Parse error": RecoveryStrategy(
        action="queue",
        message="Syntax error detected. Adding to work queue as S0."
    ),

    # Permission errors
    r"EACCES|EPERM|permission denied|access denied": RecoveryStrategy(
        action="escalate",
        message="Permission denied. User intervention may be required."
    ),

    # Disk space
    r"ENOSPC|No space left|disk full": RecoveryStrategy(
        action="escalate",
        message="Disk space exhausted. User intervention required."
    ),

    # Memory errors
    r"ENOMEM|out of memory|heap out of memory|JavaScript heap": RecoveryStrategy(
        action="escalate",
        message="Memory exhausted. Consider increasing Node memory or breaking task into smaller pieces."
    ),

    # Test failures
    r"Test failed|FAIL|AssertionError|expect.*received": RecoveryStrategy(
        action="queue",
        message="Test failure detected. Adding fix to work queue."
    ),

    # Lint errors
    r"lint|eslint|prettier|formatting": RecoveryStrategy(
        action="suggest",
        message="Linting errors. Try: npm run lint:fix or npx prettier --write",
        command="npm run lint:fix"
    ),

    # Build failures
    r"Build failed|Compilation failed|webpack|vite|rollup": RecoveryStrategy(
        action="queue",
        message="Build failure detected. Adding to work queue."
    ),

    # Authentication errors
    r"401|Unauthorized|authentication|not authenticated": RecoveryStrategy(
        action="escalate",
        message="Authentication required. User must provide credentials."
    ),

    # API/Service errors
    r"503|502|Service unavailable|Bad gateway": RecoveryStrategy(
        action="retry",
        message="Service temporarily unavailable. Retrying...",
        max_retries=3,
        delay=10.0,
        backoff="exponential"
    ),

    # Timeout
    r"timeout|timed? ?out|deadline exceeded": RecoveryStrategy(
        action="retry",
        message="Operation timed out. Retrying with longer timeout...",
        max_retries=2,
        delay=5.0,
        backoff="linear"
    ),
}


def classify_error(error_message: str) -> Optional[RecoveryStrategy]:
    """Classify error and return recovery strategy."""
    error_lower = error_message.lower()

    for pattern, strategy in RECOVERY_STRATEGIES.items():
        if re.search(pattern, error_message, re.IGNORECASE):
            return strategy

    return None


def get_retry_count_key(tool: str, error_pattern: str) -> str:
    """Generate a key for tracking retry counts."""
    return f"{tool}:{error_pattern}"


def format_recovery_message(strategy: RecoveryStrategy, attempt: int = 0) -> str:
    """Format recovery message for output."""
    lines = [f"[Recovery] {strategy.message}"]

    if strategy.action == "retry" and strategy.max_retries > 0:
        lines.append(f"  Attempt {attempt + 1}/{strategy.max_retries}")
        if strategy.delay > 0:
            delay = strategy.delay * (2 ** attempt if strategy.backoff == "exponential" else 1)
            lines.append(f"  Waiting {delay:.1f}s before retry...")

    if strategy.command:
        lines.append(f"  Suggested command: {strategy.command}")

    if strategy.action == "queue":
        lines.append("  Issue will be added to work queue for resolution.")

    if strategy.action == "escalate":
        lines.append("  This requires user intervention.")

    return "\n".join(lines)


def main():
    """Main hook entry point."""
    try:
        # Read input from stdin
        input_data = sys.stdin.read()

        if not input_data.strip():
            sys.exit(0)

        data = json.loads(input_data)

        # Extract error information
        error_message = ""
        tool = data.get("tool", "unknown")

        if "error" in data:
            if isinstance(data["error"], str):
                error_message = data["error"]
            elif isinstance(data["error"], dict):
                error_message = data["error"].get("message", str(data["error"]))
        elif "tool_result" in data:
            error_message = str(data["tool_result"])

        if not error_message:
            sys.exit(0)

        # Classify and get recovery strategy
        strategy = classify_error(error_message)

        if strategy:
            # Get retry attempt from environment or context
            attempt = int(data.get("retry_attempt", 0))

            message = format_recovery_message(strategy, attempt)
            print(message, file=sys.stderr)

            # If this is a retry action and we have attempts left
            if strategy.action == "retry" and attempt < strategy.max_retries:
                delay = strategy.delay * (2 ** attempt if strategy.backoff == "exponential" else 1)

                # Output retry instruction as JSON
                retry_instruction = {
                    "action": "retry",
                    "delay": delay,
                    "attempt": attempt + 1,
                    "max_retries": strategy.max_retries
                }
                print(json.dumps(retry_instruction))
                sys.exit(2)  # Special exit code for "retry requested"

            # If action is suggest and we have a command
            if strategy.action == "suggest" and strategy.command:
                suggestion = {
                    "action": "suggest",
                    "command": strategy.command
                }
                print(json.dumps(suggestion))
                sys.exit(0)

            # If action is queue
            if strategy.action == "queue":
                queue_item = {
                    "action": "queue",
                    "severity": "S1" if "syntax" in error_message.lower() else "S2",
                    "description": f"Fix: {error_message[:100]}"
                }
                print(json.dumps(queue_item))
                sys.exit(0)

            # If action is escalate
            if strategy.action == "escalate":
                escalation = {
                    "action": "escalate",
                    "message": strategy.message,
                    "error": error_message[:200]
                }
                print(json.dumps(escalation))
                sys.exit(1)  # Indicate user intervention needed

        sys.exit(0)

    except json.JSONDecodeError:
        sys.exit(0)
    except Exception as e:
        print(f"[Recovery Hook Error] {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
