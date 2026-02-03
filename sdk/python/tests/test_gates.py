"""Tests for Claude Sentient SDK quality gates."""

import subprocess
from unittest.mock import MagicMock, patch

import pytest

from claude_sentient.datatypes import GateStatus
from claude_sentient.gates import QualityGates, create_gate_hooks
from claude_sentient.profiles import GateConfig, Profile


@pytest.fixture
def python_profile() -> Profile:
    """Create a Python profile with standard gates."""
    return Profile(
        name="python",
        gates={
            "lint": GateConfig(command="ruff check .", timeout=60, blocking=True),
            "test": GateConfig(command="pytest", timeout=300, blocking=True),
            "type": GateConfig(command="pyright", timeout=120, blocking=False),
        },
    )


@pytest.fixture
def empty_profile() -> Profile:
    """Create a profile with no gates."""
    return Profile(name="empty")


class TestQualityGates:
    """Tests for QualityGates class."""

    def test_init(self, python_profile: Profile):
        """QualityGates should initialize with profile."""
        gates = QualityGates(profile=python_profile)
        assert gates.profile.name == "python"
        assert gates.results == {}

    def test_run_gate_skipped_if_not_configured(self, empty_profile: Profile):
        """run_gate should skip if gate not in profile."""
        gates = QualityGates(profile=empty_profile)
        result = gates.run_gate("lint")

        assert result.status == GateStatus.SKIPPED
        assert "not configured" in result.output

    @patch("subprocess.run")
    def test_run_gate_passed(self, mock_run: MagicMock, python_profile: Profile):
        """run_gate should return PASSED when command succeeds."""
        # For lint gates, empty output is required for pass (no warnings)
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="",
            stderr="",
        )

        gates = QualityGates(profile=python_profile)
        result = gates.run_gate("lint")

        assert result.status == GateStatus.PASSED
        assert result.command == "ruff check ."
        assert result.output == ""
        assert result.name == "lint"
        assert result.duration_ms >= 0

    @patch("subprocess.run")
    def test_run_gate_failed(self, mock_run: MagicMock, python_profile: Profile):
        """run_gate should return FAILED when command fails."""
        mock_run.return_value = MagicMock(
            returncode=1,
            stdout="",
            stderr="Found 3 errors",
        )

        gates = QualityGates(profile=python_profile)
        result = gates.run_gate("lint")

        assert result.status == GateStatus.FAILED
        assert result.error == "Found 3 errors"

    @patch("subprocess.run")
    def test_lint_fails_with_warnings(self, mock_run: MagicMock, python_profile: Profile):
        """Lint gate should fail if there's any output, even with return code 0.

        This ensures warnings are treated as failures, not ignored.
        Prevents dismissing lint warnings as 'pre-existing' or 'non-blocking'.
        """
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="src/file.py:1: I001 Import block is unsorted",
            stderr="",
        )

        gates = QualityGates(profile=python_profile)
        result = gates.run_gate("lint")

        # Should FAIL because there's output (a warning), even though return code is 0
        assert result.status == GateStatus.FAILED
        assert "unsorted" in result.output

    @patch("subprocess.run")
    def test_non_lint_gate_passes_with_output(self, mock_run: MagicMock, python_profile: Profile):
        """Non-lint gates should pass if return code is 0, regardless of output.

        Only the lint gate has the strict 'no output' requirement.
        """
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="123 tests passed in 5.2s",
            stderr="",
        )

        gates = QualityGates(profile=python_profile)
        result = gates.run_gate("test")

        # Should PASS because return code is 0 (test output is informational)
        assert result.status == GateStatus.PASSED
        assert "tests passed" in result.output

    @patch("subprocess.run")
    def test_run_gate_timeout(self, mock_run: MagicMock, python_profile: Profile):
        """run_gate should handle timeout."""
        mock_run.side_effect = subprocess.TimeoutExpired("ruff", 60)

        gates = QualityGates(profile=python_profile)
        result = gates.run_gate("lint")

        assert result.status == GateStatus.FAILED
        assert "Timeout" in result.error

    @patch("subprocess.run")
    def test_run_gate_exception(self, mock_run: MagicMock, python_profile: Profile):
        """run_gate should handle unexpected exceptions."""
        mock_run.side_effect = OSError("Command not found")

        gates = QualityGates(profile=python_profile)
        result = gates.run_gate("lint")

        assert result.status == GateStatus.FAILED
        assert "Command not found" in result.error

    @patch("subprocess.run")
    def test_results_are_stored(self, mock_run: MagicMock, python_profile: Profile):
        """run_gate should store results."""
        # Empty stdout for lint (strict), non-empty OK for test
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout="", stderr=""),  # lint
            MagicMock(returncode=0, stdout="OK", stderr=""),  # test
        ]

        gates = QualityGates(profile=python_profile)
        gates.run_gate("lint")
        gates.run_gate("test")

        assert "lint" in gates.results
        assert "test" in gates.results

    @patch("subprocess.run")
    def test_run_all_blocking(self, mock_run: MagicMock, python_profile: Profile):
        """run_all_blocking should run only blocking gates."""
        # Empty stdout for lint (strict), non-empty OK for test
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout="", stderr=""),  # lint
            MagicMock(returncode=0, stdout="OK", stderr=""),  # test
        ]

        gates = QualityGates(profile=python_profile)
        results = gates.run_all_blocking()

        # lint and test are blocking, type is not
        assert "lint" in results
        assert "test" in results
        assert "type" not in results

    @patch("subprocess.run")
    def test_all_blocking_passed_true(self, mock_run: MagicMock, python_profile: Profile):
        """all_blocking_passed should return True when all pass."""
        # Empty stdout for lint (strict), non-empty OK for test
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout="", stderr=""),  # lint
            MagicMock(returncode=0, stdout="OK", stderr=""),  # test
        ]

        gates = QualityGates(profile=python_profile)
        gates.run_all_blocking()

        assert gates.all_blocking_passed() is True

    @patch("subprocess.run")
    def test_all_blocking_passed_false(self, mock_run: MagicMock, python_profile: Profile):
        """all_blocking_passed should return False when any fail."""
        # Lint passes (empty output), test fails
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout="", stderr=""),  # lint passes
            MagicMock(returncode=1, stdout="", stderr="Test failed"),  # test fails
        ]

        gates = QualityGates(profile=python_profile)
        gates.run_all_blocking()

        assert gates.all_blocking_passed() is False

    @patch("subprocess.run")
    def test_get_failed_gates(self, mock_run: MagicMock, python_profile: Profile):
        """get_failed_gates should return list of failures."""
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout="", stderr=""),  # lint passes (empty output)
            MagicMock(returncode=1, stdout="", stderr="Failed"),  # test fails
        ]

        gates = QualityGates(profile=python_profile)
        gates.run_gate("lint")
        gates.run_gate("test")

        failed = gates.get_failed_gates()
        assert len(failed) == 1
        assert failed[0].name == "test"

    @patch("subprocess.run")
    def test_get_summary(self, mock_run: MagicMock, python_profile: Profile):
        """get_summary should return gate statistics."""
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout="", stderr=""),  # lint passes (empty output)
            MagicMock(returncode=1, stdout="", stderr="Failed"),  # test fails
        ]

        gates = QualityGates(profile=python_profile)
        gates.run_gate("lint")
        gates.run_gate("test")

        summary = gates.get_summary()
        assert summary["total"] == 2
        assert summary["passed"] == 1
        assert summary["failed"] == 1
        assert summary["all_blocking_passed"] is False
        assert summary["gates"]["lint"] == "passed"
        assert summary["gates"]["test"] == "failed"


class TestCreateGateHooks:
    """Tests for create_gate_hooks function."""

    def test_returns_hook_config(self, python_profile: Profile):
        """create_gate_hooks should return hook configuration."""
        hooks = create_gate_hooks(python_profile)

        assert "PostToolUse" in hooks
        assert "PreToolUse" in hooks

    def test_post_tool_use_has_lint_hook(self, python_profile: Profile):
        """PostToolUse should have lint hook for Write/Edit."""
        hooks = create_gate_hooks(python_profile)

        post_hooks = hooks["PostToolUse"]
        assert len(post_hooks) > 0
        assert post_hooks[0]["matcher"] == "Write|Edit"

    def test_pre_tool_use_has_test_hook(self, python_profile: Profile):
        """PreToolUse should have test hook for Bash (git commit)."""
        hooks = create_gate_hooks(python_profile)

        pre_hooks = hooks["PreToolUse"]
        assert len(pre_hooks) > 0
        assert pre_hooks[0]["matcher"] == "Bash"


@pytest.mark.asyncio
class TestAsyncGates:
    """Async tests for QualityGates."""

    @patch("subprocess.run")
    async def test_run_gate_async(self, mock_run: MagicMock, python_profile: Profile):
        """run_gate_async should work asynchronously."""
        # Lint requires empty output to pass
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

        gates = QualityGates(profile=python_profile)
        result = await gates.run_gate_async("lint")

        assert result.status == GateStatus.PASSED

    @patch("subprocess.run")
    async def test_run_all_blocking_async(self, mock_run: MagicMock, python_profile: Profile):
        """run_all_blocking_async should run gates in parallel."""
        # Empty output for all gates (lint needs it, doesn't hurt test)
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

        gates = QualityGates(profile=python_profile)
        results = await gates.run_all_blocking_async()

        assert "lint" in results
        assert "test" in results
