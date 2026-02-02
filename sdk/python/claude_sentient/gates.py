"""Quality gate execution for Claude Sentient SDK."""

import asyncio
import shlex
import subprocess
import sys
import time
from dataclasses import dataclass, field
from typing import Any

from .datatypes import GateResult, GateStatus
from .profiles import Profile


def _parse_command(command: str) -> list[str]:
    """Parse a command string into a list for subprocess.

    Uses shlex.split for POSIX parsing. On Windows, uses cmd.exe /c
    for proper command execution without shell=True security risks.

    Args:
        command: Command string to parse

    Returns:
        List of command arguments for subprocess
    """
    if sys.platform == "win32":
        # Windows: Use cmd.exe /c to execute command string safely
        # This avoids shell=True while still supporting shell features
        return ["cmd", "/c", command]
    try:
        return shlex.split(command)
    except ValueError:
        # Malformed command string, split on whitespace as fallback
        # This is safer than shell=True
        return command.split()


@dataclass
class QualityGates:
    """Run quality gates as SDK hooks."""

    profile: Profile
    results: dict[str, GateResult] = field(default_factory=dict)

    def run_gate(self, gate_name: str, cwd: str = ".") -> GateResult:
        """Run a single quality gate synchronously."""
        if gate_name not in self.profile.gates:
            return GateResult(
                name=gate_name,
                status=GateStatus.SKIPPED,
                command="",
                output="Gate not configured for this profile",
            )

        gate_config = self.profile.gates[gate_name]
        start_time = time.time()

        try:
            # Parse command to avoid shell=True (security)
            parsed_cmd = _parse_command(gate_config.command)

            result = subprocess.run(
                parsed_cmd,
                shell=False,
                capture_output=True,
                text=True,
                cwd=cwd,
                timeout=gate_config.timeout,
            )

            duration_ms = (time.time() - start_time) * 1000
            status = GateStatus.PASSED if result.returncode == 0 else GateStatus.FAILED

            gate_result = GateResult(
                name=gate_name,
                status=status,
                command=gate_config.command,
                output=result.stdout,
                error=result.stderr,
                duration_ms=duration_ms,
            )

        except subprocess.TimeoutExpired:
            gate_result = GateResult(
                name=gate_name,
                status=GateStatus.FAILED,
                command=gate_config.command,
                error=f"Timeout after {gate_config.timeout} seconds",
                duration_ms=gate_config.timeout * 1000,
            )

        except Exception as e:
            gate_result = GateResult(
                name=gate_name,
                status=GateStatus.FAILED,
                command=gate_config.command,
                error=str(e),
                duration_ms=(time.time() - start_time) * 1000,
            )

        self.results[gate_name] = gate_result
        return gate_result

    async def run_gate_async(self, gate_name: str, cwd: str = ".") -> GateResult:
        """Run a single quality gate asynchronously."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.run_gate, gate_name, cwd)

    def run_all_blocking(self, cwd: str = ".") -> dict[str, GateResult]:
        """Run all blocking gates."""
        for gate_name, gate_config in self.profile.gates.items():
            if gate_config.blocking:
                self.run_gate(gate_name, cwd)
        return {k: v for k, v in self.results.items() if self.profile.gates[k].blocking}

    async def run_all_blocking_async(self, cwd: str = ".") -> dict[str, GateResult]:
        """Run all blocking gates asynchronously (in parallel)."""
        blocking_gates = [
            name for name, config in self.profile.gates.items() if config.blocking
        ]

        tasks = [self.run_gate_async(gate, cwd) for gate in blocking_gates]
        await asyncio.gather(*tasks)

        return {k: v for k, v in self.results.items() if k in blocking_gates}

    def all_blocking_passed(self) -> bool:
        """Check if all blocking gates passed."""
        for gate_name, gate_config in self.profile.gates.items():
            if gate_config.blocking:
                result = self.results.get(gate_name)
                if not result or result.status != GateStatus.PASSED:
                    return False
        return True

    def get_failed_gates(self) -> list[GateResult]:
        """Get list of failed gates."""
        return [r for r in self.results.values() if r.status == GateStatus.FAILED]

    def get_summary(self) -> dict[str, Any]:
        """Get a summary of gate results."""
        return {
            "total": len(self.results),
            "passed": sum(1 for r in self.results.values() if r.status == GateStatus.PASSED),
            "failed": sum(1 for r in self.results.values() if r.status == GateStatus.FAILED),
            "skipped": sum(1 for r in self.results.values() if r.status == GateStatus.SKIPPED),
            "all_blocking_passed": self.all_blocking_passed(),
            "gates": {name: result.status.value for name, result in self.results.items()},
        }

    # Hook methods for SDK integration
    async def lint_hook(
        self,
        input_data: dict[str, Any],
        tool_use_id: str,
        context: Any,
    ) -> dict[str, Any]:
        """Run lint after file changes (PostToolUse hook)."""
        if input_data.get("hook_event_name") != "PostToolUse":
            return {}

        if input_data.get("tool_name") not in ["Write", "Edit"]:
            return {}

        cwd = input_data.get("cwd", ".")
        result = await self.run_gate_async("lint", cwd)

        if result.status == GateStatus.FAILED:
            return {
                "systemMessage": f"Lint failed:\n{result.error or result.output}"
            }

        return {}

    async def test_hook(
        self,
        input_data: dict[str, Any],
        tool_use_id: str,
        context: Any,
    ) -> dict[str, Any]:
        """Run tests before commit (PreToolUse hook)."""
        if input_data.get("hook_event_name") != "PreToolUse":
            return {}

        if input_data.get("tool_name") != "Bash":
            return {}

        command = input_data.get("tool_input", {}).get("command", "")
        if "git commit" not in command:
            return {}

        cwd = input_data.get("cwd", ".")
        result = await self.run_gate_async("test", cwd)

        if result.status == GateStatus.FAILED:
            return {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": f"Tests failed:\n{result.error or result.output}",
                }
            }

        return {}


def create_gate_hooks(profile: Profile) -> dict[str, list[dict[str, Any]]]:
    """Create hook configuration for quality gates."""
    gates = QualityGates(profile=profile)

    return {
        "PostToolUse": [
            {
                "matcher": "Write|Edit",
                "hooks": [gates.lint_hook],
            }
        ],
        "PreToolUse": [
            {
                "matcher": "Bash",
                "hooks": [gates.test_hook],
            }
        ],
    }
