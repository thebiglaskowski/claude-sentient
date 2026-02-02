#!/usr/bin/env python3
"""
Definition of Done Verifier Hook (Stop)

STRICT ENFORCEMENT: This hook blocks loop exit until ALL quality gates pass.
No warnings, no exceptions - every threshold must be met.

Hook Type: Stop
Input: JSON with session context
Output: Verification result - PASS only when ALL gates pass
Exit Code: 0 = all pass, 1 = blocking failures exist
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional, Tuple

# =============================================================================
# THRESHOLDS - These are NON-NEGOTIABLE for loop exit
# =============================================================================

THRESHOLDS = {
    "coverage_overall": 80,      # Minimum overall test coverage %
    "coverage_new_code": 90,     # Minimum coverage for new/changed code %
    "lint_errors": 0,            # Maximum lint errors allowed
    "lint_warnings": 0,          # Maximum lint warnings allowed (strict mode)
    "type_errors": 0,            # Maximum type errors allowed
    "security_s0": 0,            # Maximum S0 (critical) vulnerabilities
    "security_s1": 0,            # Maximum S1 (high) vulnerabilities
    "tests_failing": 0,          # Maximum failing tests
    "tests_skipped_pct": 5,      # Maximum % of skipped tests
}

# =============================================================================
# FRAMEWORK DETECTION
# =============================================================================

def detect_project_type() -> dict:
    """Detect project type and available tools."""
    cwd = Path.cwd()
    project = {
        "type": "unknown",
        "test_framework": None,
        "test_command": None,
        "coverage_command": None,
        "lint_command": None,
        "type_check_command": None,
        "security_command": None,
    }

    # Node.js / JavaScript / TypeScript
    if (cwd / "package.json").exists():
        project["type"] = "node"
        pkg = json.loads((cwd / "package.json").read_text(encoding='utf-8'))
        scripts = pkg.get("scripts", {})
        deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}

        # Test framework detection
        if "jest" in deps or "jest" in scripts.get("test", ""):
            project["test_framework"] = "jest"
            project["test_command"] = "npm test -- --passWithNoTests"
            project["coverage_command"] = "npm test -- --coverage --passWithNoTests"
        elif "vitest" in deps:
            project["test_framework"] = "vitest"
            project["test_command"] = "npx vitest run"
            project["coverage_command"] = "npx vitest run --coverage"
        elif "mocha" in deps:
            project["test_framework"] = "mocha"
            project["test_command"] = "npm test"
            project["coverage_command"] = "npx nyc npm test"
        elif "test" in scripts:
            project["test_framework"] = "npm"
            project["test_command"] = "npm test"
            project["coverage_command"] = "npm test -- --coverage"

        # Lint detection
        if "eslint" in deps or (cwd / ".eslintrc.js").exists() or (cwd / ".eslintrc.json").exists():
            project["lint_command"] = "npx eslint . --max-warnings=0 --format=json"

        # Type check detection
        if "typescript" in deps or (cwd / "tsconfig.json").exists():
            project["type_check_command"] = "npx tsc --noEmit"

        # Security audit
        project["security_command"] = "npm audit --json"

    # Python
    elif (cwd / "pyproject.toml").exists() or (cwd / "setup.py").exists() or (cwd / "requirements.txt").exists():
        project["type"] = "python"

        # Test framework
        if (cwd / "pytest.ini").exists() or (cwd / "pyproject.toml").exists():
            project["test_framework"] = "pytest"
            project["test_command"] = "pytest"
            project["coverage_command"] = "pytest --cov=. --cov-report=json"

        # Lint detection
        if (cwd / "pyproject.toml").exists():
            project["lint_command"] = "ruff check . --output-format=json"

        # Type check
        project["type_check_command"] = "mypy . --ignore-missing-imports"

        # Security
        project["security_command"] = "pip-audit --format=json"

    # Go
    elif (cwd / "go.mod").exists():
        project["type"] = "go"
        project["test_framework"] = "go"
        project["test_command"] = "go test ./..."
        project["coverage_command"] = "go test -coverprofile=coverage.out ./... && go tool cover -func=coverage.out"
        project["lint_command"] = "golangci-lint run --out-format=json"
        project["security_command"] = "govulncheck ./..."

    # Rust
    elif (cwd / "Cargo.toml").exists():
        project["type"] = "rust"
        project["test_framework"] = "cargo"
        project["test_command"] = "cargo test"
        project["coverage_command"] = "cargo tarpaulin --out Json"
        project["lint_command"] = "cargo clippy --message-format=json"
        project["security_command"] = "cargo audit --json"

    return project


# =============================================================================
# QUALITY GATE CHECKS
# =============================================================================

def run_command(cmd: str, timeout: int = 120) -> Tuple[int, str, str]:
    """Run a command and return (exit_code, stdout, stderr)."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=Path.cwd()
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)


def check_coverage(project: dict) -> dict:
    """Check test coverage meets threshold."""
    result = {
        "gate": "coverage",
        "passed": False,
        "value": 0,
        "threshold": THRESHOLDS["coverage_overall"],
        "message": "",
        "blocking": True
    }

    if not project.get("coverage_command"):
        result["message"] = "No coverage tool detected"
        result["passed"] = True  # Skip if no tool
        result["blocking"] = False
        return result

    exit_code, stdout, stderr = run_command(project["coverage_command"])

    # Parse coverage from various formats
    coverage_pct = None

    # Jest/Vitest JSON output
    if project["test_framework"] in ["jest", "vitest"]:
        # Try to find coverage summary
        coverage_match = re.search(r'"lines"[^}]*"pct"\s*:\s*([\d.]+)', stdout + stderr)
        if coverage_match:
            coverage_pct = float(coverage_match.group(1))
        else:
            # Fallback: parse text output
            text_match = re.search(r'All files[^\d]+([\d.]+)\s*%', stdout + stderr)
            if text_match:
                coverage_pct = float(text_match.group(1))

    # Pytest coverage
    elif project["test_framework"] == "pytest":
        # JSON format
        coverage_file = Path.cwd() / "coverage.json"
        if coverage_file.exists():
            cov_data = json.loads(coverage_file.read_text(encoding='utf-8'))
            coverage_pct = cov_data.get("totals", {}).get("percent_covered", 0)
        else:
            # Text format fallback
            text_match = re.search(r'TOTAL\s+\d+\s+\d+\s+([\d.]+)%', stdout + stderr)
            if text_match:
                coverage_pct = float(text_match.group(1))

    # Go coverage
    elif project["test_framework"] == "go":
        text_match = re.search(r'total:\s+\(statements\)\s+([\d.]+)%', stdout + stderr)
        if text_match:
            coverage_pct = float(text_match.group(1))

    # Generic percentage finder
    if coverage_pct is None:
        pct_match = re.search(r'([\d.]+)\s*%\s*(coverage|covered)', stdout + stderr, re.IGNORECASE)
        if pct_match:
            coverage_pct = float(pct_match.group(1))

    if coverage_pct is not None:
        result["value"] = round(coverage_pct, 1)
        result["passed"] = coverage_pct >= THRESHOLDS["coverage_overall"]
        result["message"] = f"{coverage_pct:.1f}% (threshold: {THRESHOLDS['coverage_overall']}%)"
    else:
        result["message"] = "Could not parse coverage output"
        result["passed"] = False

    return result


def check_tests(project: dict) -> dict:
    """Check all tests pass."""
    result = {
        "gate": "tests",
        "passed": False,
        "value": {"passed": 0, "failed": 0, "skipped": 0},
        "threshold": f"{THRESHOLDS['tests_failing']} failures",
        "message": "",
        "blocking": True
    }

    if not project.get("test_command"):
        result["message"] = "No test framework detected"
        result["passed"] = True
        result["blocking"] = False
        return result

    exit_code, stdout, stderr = run_command(project["test_command"])
    output = stdout + stderr

    # Parse test results
    passed = failed = skipped = 0

    # Jest/Vitest
    if project["test_framework"] in ["jest", "vitest"]:
        match = re.search(r'Tests:\s+(\d+)\s+passed', output)
        if match:
            passed = int(match.group(1))
        match = re.search(r'(\d+)\s+failed', output)
        if match:
            failed = int(match.group(1))
        match = re.search(r'(\d+)\s+skipped', output)
        if match:
            skipped = int(match.group(1))

    # Pytest
    elif project["test_framework"] == "pytest":
        match = re.search(r'(\d+)\s+passed', output)
        if match:
            passed = int(match.group(1))
        match = re.search(r'(\d+)\s+failed', output)
        if match:
            failed = int(match.group(1))
        match = re.search(r'(\d+)\s+skipped', output)
        if match:
            skipped = int(match.group(1))

    # Go
    elif project["test_framework"] == "go":
        passed = output.count("--- PASS:")
        failed = output.count("--- FAIL:")
        skipped = output.count("--- SKIP:")

    result["value"] = {"passed": passed, "failed": failed, "skipped": skipped}
    result["passed"] = (failed <= THRESHOLDS["tests_failing"]) and (exit_code == 0 or failed == 0)

    total = passed + failed + skipped
    if total > 0:
        result["message"] = f"{passed} passed, {failed} failed, {skipped} skipped"
    else:
        result["message"] = "No tests found or could not parse output"
        result["passed"] = exit_code == 0  # Trust exit code if can't parse

    return result


def check_lint(project: dict) -> dict:
    """Check linting passes with zero errors/warnings."""
    result = {
        "gate": "lint",
        "passed": False,
        "value": {"errors": 0, "warnings": 0},
        "threshold": f"{THRESHOLDS['lint_errors']} errors, {THRESHOLDS['lint_warnings']} warnings",
        "message": "",
        "blocking": True
    }

    if not project.get("lint_command"):
        result["message"] = "No linter detected"
        result["passed"] = True
        result["blocking"] = False
        return result

    exit_code, stdout, stderr = run_command(project["lint_command"])
    output = stdout + stderr

    errors = warnings = 0

    # Try JSON parsing first
    try:
        if stdout.strip().startswith('[') or stdout.strip().startswith('{'):
            lint_data = json.loads(stdout)
            if isinstance(lint_data, list):
                for item in lint_data:
                    if isinstance(item, dict):
                        errors += item.get("errorCount", 0)
                        warnings += item.get("warningCount", 0)
    except json.JSONDecodeError:
        pass

    # Fallback: count error/warning keywords
    if errors == 0 and warnings == 0:
        errors = len(re.findall(r'\berror\b', output, re.IGNORECASE))
        warnings = len(re.findall(r'\bwarning\b', output, re.IGNORECASE))

    result["value"] = {"errors": errors, "warnings": warnings}
    result["passed"] = (errors <= THRESHOLDS["lint_errors"]) and (warnings <= THRESHOLDS["lint_warnings"])
    result["message"] = f"{errors} errors, {warnings} warnings"

    # If exit code is 0 and we couldn't parse, trust it
    if exit_code == 0 and errors == 0 and warnings == 0:
        result["passed"] = True
        result["message"] = "Clean"

    return result


def check_types(project: dict) -> dict:
    """Check type checking passes."""
    result = {
        "gate": "types",
        "passed": False,
        "value": 0,
        "threshold": f"{THRESHOLDS['type_errors']} errors",
        "message": "",
        "blocking": True
    }

    if not project.get("type_check_command"):
        result["message"] = "No type checker detected"
        result["passed"] = True
        result["blocking"] = False
        return result

    exit_code, stdout, stderr = run_command(project["type_check_command"])
    output = stdout + stderr

    # Count errors
    error_count = len(re.findall(r'error\s+TS\d+:', output))  # TypeScript
    error_count += len(re.findall(r'error:', output, re.IGNORECASE))  # Generic

    # Remove double counting
    error_count = max(error_count, output.count('\n') if exit_code != 0 else 0)

    result["value"] = error_count
    result["passed"] = (error_count <= THRESHOLDS["type_errors"]) or (exit_code == 0)
    result["message"] = f"{error_count} errors" if error_count > 0 else "Clean"

    return result


def check_security(project: dict) -> dict:
    """Check security vulnerabilities."""
    result = {
        "gate": "security",
        "passed": False,
        "value": {"s0": 0, "s1": 0, "s2": 0},
        "threshold": f"{THRESHOLDS['security_s0']} critical, {THRESHOLDS['security_s1']} high",
        "message": "",
        "blocking": True
    }

    if not project.get("security_command"):
        result["message"] = "No security scanner detected"
        result["passed"] = True
        result["blocking"] = False
        return result

    exit_code, stdout, stderr = run_command(project["security_command"])
    output = stdout + stderr

    s0 = s1 = s2 = 0

    # npm audit
    try:
        if "npm" in project.get("security_command", ""):
            audit_data = json.loads(stdout) if stdout.strip().startswith('{') else {}
            vulns = audit_data.get("metadata", {}).get("vulnerabilities", {})
            s0 = vulns.get("critical", 0)
            s1 = vulns.get("high", 0)
            s2 = vulns.get("moderate", 0) + vulns.get("low", 0)
    except json.JSONDecodeError:
        # Fallback: keyword search
        s0 = len(re.findall(r'\bcritical\b', output, re.IGNORECASE))
        s1 = len(re.findall(r'\bhigh\b', output, re.IGNORECASE))

    result["value"] = {"s0": s0, "s1": s1, "s2": s2}
    result["passed"] = (s0 <= THRESHOLDS["security_s0"]) and (s1 <= THRESHOLDS["security_s1"])
    result["message"] = f"{s0} critical, {s1} high, {s2} moderate"

    if s0 == 0 and s1 == 0 and exit_code == 0:
        result["passed"] = True
        result["message"] = "No critical/high vulnerabilities"

    return result


def check_documentation() -> dict:
    """Check documentation completeness."""
    result = {
        "gate": "documentation",
        "passed": False,
        "value": {"readme": False, "changelog": False},
        "threshold": "README and CHANGELOG exist and updated",
        "message": "",
        "blocking": True
    }

    cwd = Path.cwd()

    readme_exists = (cwd / "README.md").exists()
    changelog_exists = (cwd / "CHANGELOG.md").exists()

    # Check CHANGELOG has recent entry
    changelog_updated = False
    if changelog_exists:
        content = (cwd / "CHANGELOG.md").read_text(encoding='utf-8')
        changelog_updated = "[Unreleased]" in content or "## [" in content

    result["value"] = {
        "readme": readme_exists,
        "changelog": changelog_exists and changelog_updated
    }

    issues = []
    if not readme_exists:
        issues.append("README.md missing")
    if not changelog_exists:
        issues.append("CHANGELOG.md missing")
    elif not changelog_updated:
        issues.append("CHANGELOG.md needs update")

    result["passed"] = readme_exists and changelog_updated
    result["message"] = ", ".join(issues) if issues else "Documentation complete"

    return result


def check_work_queue() -> dict:
    """Check that work queue is empty (all tasks completed)."""
    result = {
        "gate": "work_queue",
        "passed": False,
        "value": {"pending": 0, "in_progress": 0, "blocked": 0},
        "threshold": "0 pending, 0 in_progress, 0 blocked tasks",
        "message": "",
        "blocking": True
    }

    cwd = Path.cwd()

    # Check LOOP_STATE.md for pending work
    loop_state = cwd / "LOOP_STATE.md"
    status_file = cwd / "STATUS.md"
    known_issues = cwd / "KNOWN_ISSUES.md"

    pending = in_progress = blocked = 0
    issues = []

    # Parse LOOP_STATE.md
    if loop_state.exists():
        content = loop_state.read_text(encoding='utf-8')
        # Count pending items (⏳ or "Pending")
        pending += len(re.findall(r'⏳|Pending|\[ \]', content))
        # Count in-progress items (🔄 or "In Progress")
        in_progress += len(re.findall(r'🔄|In Progress|\[-\]', content))
        # Count blocked items
        blocked += len(re.findall(r'blocked|Blocked|BLOCKED', content, re.IGNORECASE))

    # Parse STATUS.md for TODO/FIXME/pending work
    if status_file.exists():
        content = status_file.read_text(encoding='utf-8')
        # Check for explicit pending work markers
        pending += len(re.findall(r'TODO|FIXME|\[ \]|pending|remaining', content, re.IGNORECASE))

    # Check KNOWN_ISSUES.md for unresolved blockers
    if known_issues.exists():
        content = known_issues.read_text(encoding='utf-8')
        # Count S0/S1 issues that aren't marked resolved
        s0_s1 = len(re.findall(r'\[S[01]\](?!.*resolved|fixed|closed)', content, re.IGNORECASE))
        if s0_s1 > 0:
            blocked += s0_s1
            issues.append(f"{s0_s1} unresolved S0/S1 issues")

    result["value"] = {
        "pending": pending,
        "in_progress": in_progress,
        "blocked": blocked
    }

    # Work queue must be empty
    total_incomplete = pending + in_progress + blocked
    result["passed"] = total_incomplete == 0

    if pending > 0:
        issues.append(f"{pending} pending tasks")
    if in_progress > 0:
        issues.append(f"{in_progress} in-progress tasks")
    if blocked > 0:
        issues.append(f"{blocked} blocked tasks")

    result["message"] = ", ".join(issues) if issues else "Work queue empty"

    return result


def check_known_issues() -> dict:
    """Check that no critical/high issues remain unresolved."""
    result = {
        "gate": "known_issues",
        "passed": False,
        "value": {"s0": 0, "s1": 0, "s2": 0},
        "threshold": "0 S0, 0 S1 unresolved issues",
        "message": "",
        "blocking": True
    }

    cwd = Path.cwd()
    known_issues = cwd / "KNOWN_ISSUES.md"

    s0 = s1 = s2 = 0

    if known_issues.exists():
        content = known_issues.read_text(encoding='utf-8')

        # Count unresolved issues by severity
        # Look for [S0], [S1], [S2] NOT followed by resolved/fixed/closed
        lines = content.split('\n')
        for line in lines:
            line_lower = line.lower()
            if '[s0]' in line_lower and not any(x in line_lower for x in ['resolved', 'fixed', 'closed', '✓', '✅']):
                s0 += 1
            elif '[s1]' in line_lower and not any(x in line_lower for x in ['resolved', 'fixed', 'closed', '✓', '✅']):
                s1 += 1
            elif '[s2]' in line_lower and not any(x in line_lower for x in ['resolved', 'fixed', 'closed', '✓', '✅']):
                s2 += 1

    result["value"] = {"s0": s0, "s1": s1, "s2": s2}
    result["passed"] = (s0 == 0) and (s1 == 0)  # S2 allowed but tracked

    issues = []
    if s0 > 0:
        issues.append(f"{s0} critical (S0) issues")
    if s1 > 0:
        issues.append(f"{s1} high (S1) issues")
    if s2 > 0:
        issues.append(f"{s2} medium (S2) issues (non-blocking)")

    result["message"] = ", ".join(issues) if issues else "No critical/high issues"

    return result


def check_git_state() -> dict:
    """Check git state is clean and ready for completion."""
    result = {
        "gate": "git_state",
        "passed": False,
        "value": {"uncommitted": 0, "untracked": 0},
        "threshold": "All changes committed",
        "message": "",
        "blocking": True
    }

    # Run git status
    exit_code, stdout, stderr = run_command("git status --porcelain")

    if exit_code != 0:
        result["message"] = "Not a git repository or git error"
        result["passed"] = True  # Skip if not a git repo
        result["blocking"] = False
        return result

    lines = [l for l in stdout.strip().split('\n') if l.strip()]

    uncommitted = sum(1 for l in lines if l.startswith((' M', 'M ', 'MM', 'A ', 'D ', 'R ', 'C ')))
    untracked = sum(1 for l in lines if l.startswith('??'))

    result["value"] = {"uncommitted": uncommitted, "untracked": untracked}

    # All work should be committed
    result["passed"] = (uncommitted == 0)  # Untracked files OK

    issues = []
    if uncommitted > 0:
        issues.append(f"{uncommitted} uncommitted changes")
    if untracked > 0:
        issues.append(f"{untracked} untracked files (non-blocking)")

    result["message"] = ", ".join(issues) if issues else "Git state clean"

    return result


# =============================================================================
# MAIN VERIFICATION
# =============================================================================

def run_all_gates() -> dict:
    """Run all quality gates and return comprehensive result."""
    project = detect_project_type()

    gates = [
        # Code Quality Gates
        check_tests(project),
        check_coverage(project),
        check_lint(project),
        check_types(project),
        check_security(project),
        # Work Completion Gates
        check_work_queue(),
        check_known_issues(),
        check_documentation(),
        check_git_state(),
    ]

    all_passed = all(g["passed"] for g in gates if g["blocking"])
    blocking_failures = [g for g in gates if g["blocking"] and not g["passed"]]

    return {
        "project_type": project["type"],
        "test_framework": project["test_framework"],
        "all_passed": all_passed,
        "gates": gates,
        "blocking_failures": len(blocking_failures),
        "thresholds": THRESHOLDS,
        "verdict": "PASS" if all_passed else "FAIL - LOOP MUST CONTINUE"
    }


def format_output(result: dict) -> str:
    """Format result for display."""
    lines = [
        "=" * 60,
        "  DEFINITION OF DONE VERIFICATION",
        "=" * 60,
        f"  Project Type: {result['project_type']}",
        f"  Test Framework: {result['test_framework'] or 'none detected'}",
        "",
        "  QUALITY GATES:",
        "-" * 60,
    ]

    for gate in result["gates"]:
        status = "PASS" if gate["passed"] else "FAIL"
        icon = "  [PASS]" if gate["passed"] else "X [FAIL]"
        blocking = " (BLOCKING)" if gate["blocking"] and not gate["passed"] else ""
        lines.append(f"  {icon} {gate['gate'].upper()}: {gate['message']}{blocking}")

    lines.extend([
        "-" * 60,
        "",
        f"  VERDICT: {result['verdict']}",
    ])

    if not result["all_passed"]:
        lines.extend([
            "",
            "  The loop CANNOT exit until all blocking gates pass.",
            "  Blocking failures: " + str(result["blocking_failures"]),
            "",
            "  Required thresholds (ALL must be met):",
            "",
            "  CODE QUALITY:",
            f"    - Test coverage: >= {THRESHOLDS['coverage_overall']}%",
            f"    - Lint errors: {THRESHOLDS['lint_errors']}",
            f"    - Lint warnings: {THRESHOLDS['lint_warnings']}",
            f"    - Type errors: {THRESHOLDS['type_errors']}",
            f"    - Security S0/S1: {THRESHOLDS['security_s0']}/{THRESHOLDS['security_s1']}",
            f"    - All tests passing: required",
            "",
            "  WORK COMPLETION:",
            "    - Work queue: empty (0 pending/in-progress)",
            "    - Known issues: 0 S0, 0 S1 unresolved",
            "    - Documentation: README + CHANGELOG present",
            "    - Git state: all changes committed",
        ])

    lines.append("=" * 60)

    return "\n".join(lines)


def main():
    """Main hook entry point."""
    try:
        # Read input (may be empty)
        input_data = sys.stdin.read() if not sys.stdin.isatty() else ""

        # Run all quality gates
        result = run_all_gates()

        # Output human-readable report
        print(format_output(result), file=sys.stderr)

        # Output machine-readable JSON
        print(json.dumps(result))

        # EXIT CODE DETERMINES IF LOOP CAN EXIT
        # 0 = all pass, loop may exit
        # 1 = failures exist, loop MUST continue
        if result["all_passed"]:
            sys.exit(0)
        else:
            sys.exit(1)

    except Exception as e:
        print(f"[DoD Verifier Error] {e}", file=sys.stderr)
        # On error, fail safe - don't let loop exit
        sys.exit(1)


if __name__ == "__main__":
    main()
