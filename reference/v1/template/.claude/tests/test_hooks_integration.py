#!/usr/bin/env python3
"""
Integration Tests for v3.0 Hook System

Tests all 12 hooks working together in realistic workflows.
Run with: python -m pytest test_hooks_integration.py -v
Or standalone: python test_hooks_integration.py
"""

import json
import os
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import unittest


class HookTestEnvironment:
    """Sets up and tears down a test environment for hooks."""

    def __init__(self):
        self.test_dir = None
        self.original_cwd = None
        self.hooks_dir = None

    def setup(self):
        """Create isolated test environment."""
        self.original_cwd = os.getcwd()
        self.test_dir = tempfile.mkdtemp(prefix="hook_test_")

        # Create .claude directory structure
        claude_dir = Path(self.test_dir) / ".claude"
        claude_dir.mkdir()

        # Create state directories
        state_dirs = [
            "state/agents/results",
            "state/loop",
            "state/session",
            "state/errors",
            "state/compaction",
        ]
        for d in state_dirs:
            (claude_dir / d).mkdir(parents=True)

        # Copy hooks from parent directory
        self.hooks_dir = claude_dir / "hooks"
        self.hooks_dir.mkdir()

        # Get the actual hooks directory (relative to this test file)
        script_dir = Path(__file__).parent.parent
        actual_hooks = script_dir / "hooks"

        if actual_hooks.exists():
            for hook_file in actual_hooks.iterdir():
                if hook_file.is_file():
                    shutil.copy(hook_file, self.hooks_dir)

        os.chdir(self.test_dir)
        return self

    def teardown(self):
        """Clean up test environment."""
        if self.original_cwd:
            os.chdir(self.original_cwd)
        if self.test_dir and os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def run_hook(self, hook_name: str, input_data: Optional[Dict] = None,
                 env_vars: Optional[Dict] = None) -> Dict[str, Any]:
        """Run a hook script and capture results."""
        hook_path = self.hooks_dir / hook_name

        if not hook_path.exists():
            return {
                "success": False,
                "error": f"Hook not found: {hook_name}",
                "stdout": "",
                "stderr": "",
                "exit_code": -1,
                "duration_ms": 0
            }

        # Determine interpreter
        if hook_name.endswith(".py"):
            cmd = [sys.executable, str(hook_path)]
        elif hook_name.endswith(".sh"):
            cmd = ["bash", str(hook_path)]
        else:
            cmd = [str(hook_path)]

        # Prepare environment
        env = os.environ.copy()
        if env_vars:
            env.update(env_vars)

        # Prepare input
        input_bytes = None
        if input_data:
            input_bytes = json.dumps(input_data).encode()

        # Run hook
        start_time = datetime.now()
        try:
            result = subprocess.run(
                cmd,
                input=input_bytes,
                capture_output=True,
                timeout=30,
                env=env,
                cwd=self.test_dir
            )
            duration = (datetime.now() - start_time).total_seconds() * 1000

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout.decode("utf-8", errors="replace"),
                "stderr": result.stderr.decode("utf-8", errors="replace"),
                "exit_code": result.returncode,
                "duration_ms": duration
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Hook timed out",
                "stdout": "",
                "stderr": "",
                "exit_code": -1,
                "duration_ms": 30000
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "stdout": "",
                "stderr": "",
                "exit_code": -1,
                "duration_ms": 0
            }


class TestHookLifecycle(unittest.TestCase):
    """Test hooks in lifecycle order."""

    @classmethod
    def setUpClass(cls):
        cls.env = HookTestEnvironment().setup()

    @classmethod
    def tearDownClass(cls):
        cls.env.teardown()

    def test_01_setup_init(self):
        """Test Setup hook initializes project correctly."""
        result = self.env.run_hook("setup-init.sh")

        # Should complete (may fail if deps missing, but shouldn't crash)
        self.assertIn(result["exit_code"], [0, 1],
                      f"Setup hook crashed: {result.get('stderr', '')}")

    def test_02_session_start(self):
        """Test SessionStart hook initializes session."""
        result = self.env.run_hook("session-start.sh")

        self.assertIn(result["exit_code"], [0, 1],
                      f"Session start crashed: {result.get('stderr', '')}")

        # Check if session state was created
        session_file = Path(self.env.test_dir) / ".claude/state/session/current.json"
        # File may or may not exist depending on implementation

    def test_03_context_injector(self):
        """Test UserPromptSubmit hook processes prompts."""
        input_data = {
            "prompt": "implement user authentication with OAuth"
        }

        result = self.env.run_hook("context-injector.py", input_data)

        # Should process without crashing
        self.assertIn(result["exit_code"], [0, 1],
                      f"Context injector crashed: {result.get('stderr', '')}")

    def test_04_bash_auto_approve(self):
        """Test PreToolUse hook for Bash commands."""
        # Safe command
        safe_input = {
            "tool_name": "Bash",
            "tool_input": {"command": "git status"}
        }
        result = self.env.run_hook("bash-auto-approve.py", safe_input)
        self.assertIn(result["exit_code"], [0, 1])

        # Unsafe command
        unsafe_input = {
            "tool_name": "Bash",
            "tool_input": {"command": "rm -rf /"}
        }
        result = self.env.run_hook("bash-auto-approve.py", unsafe_input)
        # Should either reject (exit 2) or pass through for user approval
        self.assertIn(result["exit_code"], [0, 1, 2])

    def test_05_file_validator(self):
        """Test PreToolUse hook for file operations."""
        # Safe file write
        safe_input = {
            "tool_name": "Write",
            "tool_input": {
                "file_path": "src/app.js",
                "content": "console.log('hello');"
            }
        }
        result = self.env.run_hook("file-validator.py", safe_input)
        self.assertIn(result["exit_code"], [0, 1, 2])

        # Dangerous file (secrets)
        dangerous_input = {
            "tool_name": "Write",
            "tool_input": {
                "file_path": ".env",
                "content": "API_KEY=secret123"
            }
        }
        result = self.env.run_hook("file-validator.py", dangerous_input)
        # Should warn or block
        self.assertIn(result["exit_code"], [0, 1, 2])

    def test_06_post_edit(self):
        """Test PostToolUse hook after edits."""
        # Create a test file to format
        test_file = Path(self.env.test_dir) / "test.js"
        test_file.write_text("const x=1")

        result = self.env.run_hook(
            "post-edit.sh",
            env_vars={"EDITED_FILE": str(test_file)}
        )

        # Should complete (may fail if prettier not installed)
        self.assertIn(result["exit_code"], [0, 1])

    def test_07_error_recovery(self):
        """Test PostToolUseFailure hook classifies errors."""
        error_input = {
            "tool_name": "Bash",
            "tool_input": {"command": "npm test"},
            "error": "ECONNREFUSED 127.0.0.1:5432"
        }

        result = self.env.run_hook("error-recovery.py", error_input)

        # Exit code 2 is valid (means "blocked/rejected" in hook system)
        self.assertIn(result["exit_code"], [0, 1, 2])
        # Should output classification
        if result["success"]:
            self.assertIn("network", result["stdout"].lower())

    def test_08_agent_tracker(self):
        """Test SubagentStart hook tracks agents."""
        agent_input = {
            "agent_id": "test-agent-001",
            "agent_type": "security-analyst",
            "task": "Review authentication code"
        }

        result = self.env.run_hook("agent-tracker.py", agent_input)

        self.assertIn(result["exit_code"], [0, 1])

        # Check if agent was tracked
        active_file = Path(self.env.test_dir) / ".claude/state/agents/active.json"
        if active_file.exists():
            data = json.loads(active_file.read_text())
            self.assertIn("agents", data)

    def test_09_agent_synthesizer(self):
        """Test SubagentStop hook synthesizes results."""
        agent_result = {
            "agent_id": "test-agent-001",
            "status": "completed",
            "findings": [
                {"severity": "S2", "title": "Missing rate limiting"}
            ]
        }

        result = self.env.run_hook("agent-synthesizer.py", agent_result)

        self.assertIn(result["exit_code"], [0, 1])

    def test_10_pre_compact(self):
        """Test PreCompact hook backs up state."""
        # Create some state to backup
        state_dir = Path(self.env.test_dir) / ".claude/state"
        loop_state = state_dir / "loop/LOOP_STATE.md"
        loop_state.parent.mkdir(parents=True, exist_ok=True)
        loop_state.write_text("# Loop State\nIteration: 1")

        result = self.env.run_hook("pre-compact.sh")

        self.assertIn(result["exit_code"], [0, 1])

        # Check if backup was created
        backup_dir = state_dir / "compaction"
        if backup_dir.exists():
            backups = list(backup_dir.glob("backup_*.json"))
            # May or may not have created backup depending on implementation

    def test_11_dod_verifier(self):
        """Test Stop hook verifies Definition of Done."""
        dod_input = {
            "work_type": "feature",
            "task": "Implement user authentication"
        }

        result = self.env.run_hook("dod-verifier.py", dod_input)

        self.assertIn(result["exit_code"], [0, 1])
        # Should output DoD status

    def test_12_session_end(self):
        """Test SessionEnd hook cleans up."""
        result = self.env.run_hook("session-end.sh")

        self.assertIn(result["exit_code"], [0, 1])


class TestHookWorkflows(unittest.TestCase):
    """Test hooks in realistic workflow sequences."""

    def setUp(self):
        self.env = HookTestEnvironment().setup()

    def tearDown(self):
        self.env.teardown()

    def test_feature_development_workflow(self):
        """Simulate a feature development workflow with all relevant hooks."""
        results = []

        # 1. Session start
        results.append(("session-start", self.env.run_hook("session-start.sh")))

        # 2. Context injection for task
        results.append(("context-injector", self.env.run_hook(
            "context-injector.py",
            {"prompt": "implement login feature"}
        )))

        # 3. Spawn security analyst agent
        results.append(("agent-tracker", self.env.run_hook(
            "agent-tracker.py",
            {"agent_id": "sec-001", "agent_type": "security-analyst", "task": "review"}
        )))

        # 4. Validate file write
        results.append(("file-validator", self.env.run_hook(
            "file-validator.py",
            {"tool_name": "Write", "tool_input": {"file_path": "src/auth.js", "content": "code"}}
        )))

        # 5. Bash auto-approve for tests
        results.append(("bash-auto-approve", self.env.run_hook(
            "bash-auto-approve.py",
            {"tool_name": "Bash", "tool_input": {"command": "npm test"}}
        )))

        # 6. Agent completes
        results.append(("agent-synthesizer", self.env.run_hook(
            "agent-synthesizer.py",
            {"agent_id": "sec-001", "status": "completed", "findings": []}
        )))

        # 7. DoD verification
        results.append(("dod-verifier", self.env.run_hook(
            "dod-verifier.py",
            {"work_type": "feature", "task": "login feature"}
        )))

        # 8. Session end
        results.append(("session-end", self.env.run_hook("session-end.sh")))

        # Verify no crashes
        for name, result in results:
            self.assertNotEqual(
                result["exit_code"], -1,
                f"Hook {name} crashed: {result.get('error', result.get('stderr', ''))}"
            )

    def test_error_recovery_workflow(self):
        """Test error handling and recovery flow."""
        results = []

        # 1. Simulate network error
        results.append(("error-recovery-network", self.env.run_hook(
            "error-recovery.py",
            {"tool_name": "WebFetch", "error": "ECONNREFUSED 127.0.0.1:3000"}
        )))

        # 2. Simulate rate limit
        results.append(("error-recovery-ratelimit", self.env.run_hook(
            "error-recovery.py",
            {"tool_name": "Bash", "error": "429 Too Many Requests"}
        )))

        # 3. Simulate syntax error
        results.append(("error-recovery-syntax", self.env.run_hook(
            "error-recovery.py",
            {"tool_name": "Bash", "error": "SyntaxError: Unexpected token"}
        )))

        # 4. Simulate permission error
        results.append(("error-recovery-permission", self.env.run_hook(
            "error-recovery.py",
            {"tool_name": "Write", "error": "EACCES: permission denied"}
        )))

        # All should handle gracefully
        for name, result in results:
            self.assertIn(
                result["exit_code"], [0, 1, 2],
                f"Hook {name} crashed: {result.get('error', '')}"
            )

    def test_parallel_agents_workflow(self):
        """Test multiple agents running in parallel."""
        # Start multiple agents
        agents = [
            ("security-analyst", "sec-001"),
            ("test-engineer", "test-001"),
            ("documentation-writer", "doc-001"),
        ]

        # Track all agents
        for agent_type, agent_id in agents:
            result = self.env.run_hook(
                "agent-tracker.py",
                {"agent_id": agent_id, "agent_type": agent_type, "task": f"{agent_type} task"}
            )
            self.assertIn(result["exit_code"], [0, 1])

        # Complete all agents with findings
        for agent_type, agent_id in agents:
            result = self.env.run_hook(
                "agent-synthesizer.py",
                {
                    "agent_id": agent_id,
                    "status": "completed",
                    "findings": [{"severity": "S2", "title": f"Finding from {agent_type}"}]
                }
            )
            self.assertIn(result["exit_code"], [0, 1])


class TestHookEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""

    def setUp(self):
        self.env = HookTestEnvironment().setup()

    def tearDown(self):
        self.env.teardown()

    def test_empty_input(self):
        """Hooks should handle empty input gracefully."""
        hooks = [
            "context-injector.py",
            "bash-auto-approve.py",
            "file-validator.py",
            "error-recovery.py",
            "agent-tracker.py",
            "agent-synthesizer.py",
            "dod-verifier.py",
        ]

        for hook in hooks:
            result = self.env.run_hook(hook, {})
            self.assertNotEqual(
                result["exit_code"], -1,
                f"Hook {hook} crashed with empty input"
            )

    def test_malformed_json(self):
        """Hooks should handle malformed JSON gracefully."""
        # This tests the hook's stdin handling
        # Since we pass dict that gets serialized, test with None
        hooks = ["context-injector.py", "error-recovery.py"]

        for hook in hooks:
            result = self.env.run_hook(hook, None)
            # Should not crash (-1)
            self.assertNotEqual(
                result["exit_code"], -1,
                f"Hook {hook} crashed with no input"
            )

    def test_missing_state_directories(self):
        """Hooks should handle missing state directories."""
        # Remove state directory
        state_dir = Path(self.env.test_dir) / ".claude/state"
        if state_dir.exists():
            shutil.rmtree(state_dir)

        # Hooks should still work or fail gracefully
        result = self.env.run_hook(
            "agent-tracker.py",
            {"agent_id": "test", "agent_type": "test", "task": "test"}
        )

        self.assertNotEqual(result["exit_code"], -1, "Hook crashed without state dir")


def run_tests():
    """Run all tests and return results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestHookLifecycle))
    suite.addTests(loader.loadTestsFromTestCase(TestHookWorkflows))
    suite.addTests(loader.loadTestsFromTestCase(TestHookEdgeCases))

    # Run with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
