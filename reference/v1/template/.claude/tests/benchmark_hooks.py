#!/usr/bin/env python3
"""
Performance Benchmarking for v3.0 Hook System

Measures execution time, memory usage, and throughput for all hooks.
Run with: python benchmark_hooks.py

Output: Detailed benchmark report with recommendations.
"""

import json
import os
import subprocess
import sys
import tempfile
import shutil
import statistics
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse


@dataclass
class BenchmarkResult:
    """Results from benchmarking a single hook."""
    hook_name: str
    runs: int = 0
    success_count: int = 0
    failure_count: int = 0
    durations_ms: List[float] = field(default_factory=list)
    min_ms: float = 0
    max_ms: float = 0
    mean_ms: float = 0
    median_ms: float = 0
    std_dev_ms: float = 0
    p95_ms: float = 0
    p99_ms: float = 0
    errors: List[str] = field(default_factory=list)

    def calculate_stats(self):
        """Calculate statistics from durations."""
        if not self.durations_ms:
            return

        self.min_ms = min(self.durations_ms)
        self.max_ms = max(self.durations_ms)
        self.mean_ms = statistics.mean(self.durations_ms)
        self.median_ms = statistics.median(self.durations_ms)

        if len(self.durations_ms) > 1:
            self.std_dev_ms = statistics.stdev(self.durations_ms)

        sorted_durations = sorted(self.durations_ms)
        p95_idx = int(len(sorted_durations) * 0.95)
        p99_idx = int(len(sorted_durations) * 0.99)
        self.p95_ms = sorted_durations[min(p95_idx, len(sorted_durations) - 1)]
        self.p99_ms = sorted_durations[min(p99_idx, len(sorted_durations) - 1)]


@dataclass
class BenchmarkConfig:
    """Configuration for benchmark run."""
    runs_per_hook: int = 10
    warmup_runs: int = 2
    timeout_seconds: int = 30
    parallel_runs: int = 1
    include_shell_hooks: bool = True
    include_python_hooks: bool = True
    verbose: bool = False


class HookBenchmark:
    """Benchmark runner for hooks."""

    # Standard test inputs for each hook type
    HOOK_INPUTS = {
        "context-injector.py": {"prompt": "implement user authentication"},
        "bash-auto-approve.py": {
            "tool_name": "Bash",
            "tool_input": {"command": "git status"}
        },
        "file-validator.py": {
            "tool_name": "Write",
            "tool_input": {"file_path": "src/test.js", "content": "const x = 1;"}
        },
        "error-recovery.py": {
            "tool_name": "Bash",
            "tool_input": {"command": "npm test"},
            "error": "ECONNREFUSED 127.0.0.1:5432"
        },
        "agent-tracker.py": {
            "agent_id": "bench-agent-001",
            "agent_type": "security-analyst",
            "task": "Benchmark test task"
        },
        "agent-synthesizer.py": {
            "agent_id": "bench-agent-001",
            "status": "completed",
            "findings": [{"severity": "S2", "title": "Test finding"}]
        },
        "dod-verifier.py": {
            "work_type": "feature",
            "task": "Benchmark test task"
        },
    }

    # Performance thresholds (in milliseconds)
    THRESHOLDS = {
        "excellent": 50,    # < 50ms
        "good": 100,        # < 100ms
        "acceptable": 250,  # < 250ms
        "slow": 500,        # < 500ms
        # > 500ms is "very slow"
    }

    def __init__(self, config: BenchmarkConfig):
        self.config = config
        self.test_dir = None
        self.hooks_dir = None
        self.results: Dict[str, BenchmarkResult] = {}

    def setup(self):
        """Create benchmark environment."""
        self.test_dir = tempfile.mkdtemp(prefix="hook_bench_")

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

        # Copy hooks
        self.hooks_dir = claude_dir / "hooks"
        self.hooks_dir.mkdir()

        script_dir = Path(__file__).parent.parent
        actual_hooks = script_dir / "hooks"

        if actual_hooks.exists():
            for hook_file in actual_hooks.iterdir():
                if hook_file.is_file():
                    shutil.copy(hook_file, self.hooks_dir)

        return self

    def teardown(self):
        """Clean up benchmark environment."""
        if self.test_dir and os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def get_hooks(self) -> List[Path]:
        """Get list of hooks to benchmark."""
        hooks = []

        if not self.hooks_dir or not self.hooks_dir.exists():
            return hooks

        for hook_file in sorted(self.hooks_dir.iterdir()):
            if not hook_file.is_file():
                continue

            if hook_file.suffix == ".py" and self.config.include_python_hooks:
                hooks.append(hook_file)
            elif hook_file.suffix == ".sh" and self.config.include_shell_hooks:
                hooks.append(hook_file)

        return hooks

    def run_hook_once(self, hook_path: Path, input_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Run a hook once and measure execution time."""
        # Determine interpreter
        if hook_path.suffix == ".py":
            cmd = [sys.executable, str(hook_path)]
        elif hook_path.suffix == ".sh":
            cmd = ["bash", str(hook_path)]
        else:
            cmd = [str(hook_path)]

        # Prepare input
        input_bytes = None
        if input_data:
            input_bytes = json.dumps(input_data).encode()

        # Run and time
        start_time = time.perf_counter()
        try:
            result = subprocess.run(
                cmd,
                input=input_bytes,
                capture_output=True,
                timeout=self.config.timeout_seconds,
                cwd=self.test_dir
            )
            duration_ms = (time.perf_counter() - start_time) * 1000

            return {
                "success": result.returncode in [0, 1],  # 0=approve, 1=pass-through
                "duration_ms": duration_ms,
                "exit_code": result.returncode,
                "error": None if result.returncode in [0, 1] else result.stderr.decode("utf-8", errors="replace")
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "duration_ms": self.config.timeout_seconds * 1000,
                "exit_code": -1,
                "error": "Timeout"
            }
        except Exception as e:
            return {
                "success": False,
                "duration_ms": (time.perf_counter() - start_time) * 1000,
                "exit_code": -1,
                "error": str(e)
            }

    def benchmark_hook(self, hook_path: Path) -> BenchmarkResult:
        """Benchmark a single hook with multiple runs."""
        hook_name = hook_path.name
        result = BenchmarkResult(hook_name=hook_name)

        # Get input data for this hook
        input_data = self.HOOK_INPUTS.get(hook_name)

        # Warmup runs (not counted)
        for _ in range(self.config.warmup_runs):
            self.run_hook_once(hook_path, input_data)

        # Actual benchmark runs
        for i in range(self.config.runs_per_hook):
            run_result = self.run_hook_once(hook_path, input_data)
            result.runs += 1

            if run_result["success"]:
                result.success_count += 1
                result.durations_ms.append(run_result["duration_ms"])
            else:
                result.failure_count += 1
                if run_result["error"]:
                    result.errors.append(run_result["error"][:100])

            if self.config.verbose:
                status = "OK" if run_result["success"] else "FAIL"
                print(f"  Run {i+1}/{self.config.runs_per_hook}: {run_result['duration_ms']:.2f}ms [{status}]")

        result.calculate_stats()
        return result

    def run_benchmarks(self) -> Dict[str, BenchmarkResult]:
        """Run benchmarks for all hooks."""
        hooks = self.get_hooks()

        if not hooks:
            print("No hooks found to benchmark!")
            return {}

        print(f"\nBenchmarking {len(hooks)} hooks...")
        print(f"  Runs per hook: {self.config.runs_per_hook}")
        print(f"  Warmup runs: {self.config.warmup_runs}")
        print()

        for hook_path in hooks:
            print(f"Benchmarking {hook_path.name}...")
            result = self.benchmark_hook(hook_path)
            self.results[hook_path.name] = result

            if result.durations_ms:
                print(f"  Mean: {result.mean_ms:.2f}ms | "
                      f"Median: {result.median_ms:.2f}ms | "
                      f"P95: {result.p95_ms:.2f}ms | "
                      f"Success: {result.success_count}/{result.runs}")
            else:
                print(f"  All runs failed!")

        return self.results

    def get_performance_rating(self, duration_ms: float) -> str:
        """Get performance rating for a duration."""
        if duration_ms < self.THRESHOLDS["excellent"]:
            return "EXCELLENT"
        elif duration_ms < self.THRESHOLDS["good"]:
            return "GOOD"
        elif duration_ms < self.THRESHOLDS["acceptable"]:
            return "ACCEPTABLE"
        elif duration_ms < self.THRESHOLDS["slow"]:
            return "SLOW"
        else:
            return "VERY SLOW"

    def generate_report(self) -> str:
        """Generate benchmark report."""
        lines = []
        lines.append("=" * 70)
        lines.append("HOOK PERFORMANCE BENCHMARK REPORT")
        lines.append(f"Generated: {datetime.now().isoformat()}")
        lines.append("=" * 70)
        lines.append("")

        # Configuration
        lines.append("CONFIGURATION")
        lines.append("-" * 40)
        lines.append(f"  Runs per hook: {self.config.runs_per_hook}")
        lines.append(f"  Warmup runs: {self.config.warmup_runs}")
        lines.append(f"  Timeout: {self.config.timeout_seconds}s")
        lines.append("")

        # Summary table
        lines.append("RESULTS SUMMARY")
        lines.append("-" * 70)
        lines.append(f"{'Hook':<30} {'Mean':>8} {'P95':>8} {'P99':>8} {'Rating':<12}")
        lines.append("-" * 70)

        sorted_results = sorted(
            self.results.items(),
            key=lambda x: x[1].mean_ms if x[1].durations_ms else float('inf')
        )

        for hook_name, result in sorted_results:
            if result.durations_ms:
                rating = self.get_performance_rating(result.mean_ms)
                lines.append(
                    f"{hook_name:<30} {result.mean_ms:>7.1f}ms {result.p95_ms:>7.1f}ms "
                    f"{result.p99_ms:>7.1f}ms {rating:<12}"
                )
            else:
                lines.append(f"{hook_name:<30} {'FAILED':>8} {'-':>8} {'-':>8} {'N/A':<12}")

        lines.append("-" * 70)
        lines.append("")

        # Detailed results
        lines.append("DETAILED RESULTS")
        lines.append("-" * 70)

        for hook_name, result in sorted_results:
            lines.append(f"\n{hook_name}")
            lines.append("  " + "-" * 40)

            if result.durations_ms:
                lines.append(f"  Runs:       {result.runs}")
                lines.append(f"  Success:    {result.success_count} ({result.success_count/result.runs*100:.0f}%)")
                lines.append(f"  Min:        {result.min_ms:.2f}ms")
                lines.append(f"  Max:        {result.max_ms:.2f}ms")
                lines.append(f"  Mean:       {result.mean_ms:.2f}ms")
                lines.append(f"  Median:     {result.median_ms:.2f}ms")
                lines.append(f"  Std Dev:    {result.std_dev_ms:.2f}ms")
                lines.append(f"  P95:        {result.p95_ms:.2f}ms")
                lines.append(f"  P99:        {result.p99_ms:.2f}ms")
                lines.append(f"  Rating:     {self.get_performance_rating(result.mean_ms)}")
            else:
                lines.append(f"  Status:     ALL RUNS FAILED")
                lines.append(f"  Failures:   {result.failure_count}")

            if result.errors:
                lines.append(f"  Errors:")
                for err in result.errors[:3]:  # Show first 3 errors
                    lines.append(f"    - {err}")

        lines.append("")

        # Performance thresholds
        lines.append("PERFORMANCE THRESHOLDS")
        lines.append("-" * 40)
        lines.append(f"  EXCELLENT:   < {self.THRESHOLDS['excellent']}ms")
        lines.append(f"  GOOD:        < {self.THRESHOLDS['good']}ms")
        lines.append(f"  ACCEPTABLE:  < {self.THRESHOLDS['acceptable']}ms")
        lines.append(f"  SLOW:        < {self.THRESHOLDS['slow']}ms")
        lines.append(f"  VERY SLOW:   >= {self.THRESHOLDS['slow']}ms")
        lines.append("")

        # Recommendations
        lines.append("RECOMMENDATIONS")
        lines.append("-" * 40)

        slow_hooks = [
            (name, result) for name, result in self.results.items()
            if result.durations_ms and result.mean_ms >= self.THRESHOLDS["acceptable"]
        ]

        if slow_hooks:
            lines.append("  Hooks needing optimization:")
            for name, result in slow_hooks:
                lines.append(f"    - {name}: {result.mean_ms:.0f}ms mean")
        else:
            lines.append("  All hooks performing within acceptable thresholds.")

        failed_hooks = [
            name for name, result in self.results.items()
            if result.failure_count > result.success_count
        ]

        if failed_hooks:
            lines.append("")
            lines.append("  Hooks with reliability issues:")
            for name in failed_hooks:
                lines.append(f"    - {name}")

        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def export_json(self, filepath: str):
        """Export results as JSON."""
        data = {
            "generated": datetime.now().isoformat(),
            "config": {
                "runs_per_hook": self.config.runs_per_hook,
                "warmup_runs": self.config.warmup_runs,
                "timeout_seconds": self.config.timeout_seconds,
            },
            "thresholds": self.THRESHOLDS,
            "results": {}
        }

        for hook_name, result in self.results.items():
            data["results"][hook_name] = {
                "runs": result.runs,
                "success_count": result.success_count,
                "failure_count": result.failure_count,
                "min_ms": result.min_ms,
                "max_ms": result.max_ms,
                "mean_ms": result.mean_ms,
                "median_ms": result.median_ms,
                "std_dev_ms": result.std_dev_ms,
                "p95_ms": result.p95_ms,
                "p99_ms": result.p99_ms,
                "rating": self.get_performance_rating(result.mean_ms) if result.durations_ms else "FAILED"
            }

        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Benchmark hook performance")
    parser.add_argument("-n", "--runs", type=int, default=10,
                        help="Number of benchmark runs per hook (default: 10)")
    parser.add_argument("-w", "--warmup", type=int, default=2,
                        help="Number of warmup runs (default: 2)")
    parser.add_argument("-t", "--timeout", type=int, default=30,
                        help="Timeout in seconds (default: 30)")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Show individual run results")
    parser.add_argument("-o", "--output", type=str,
                        help="Output JSON file path")
    parser.add_argument("--python-only", action="store_true",
                        help="Only benchmark Python hooks")
    parser.add_argument("--shell-only", action="store_true",
                        help="Only benchmark shell hooks")

    args = parser.parse_args()

    config = BenchmarkConfig(
        runs_per_hook=args.runs,
        warmup_runs=args.warmup,
        timeout_seconds=args.timeout,
        verbose=args.verbose,
        include_python_hooks=not args.shell_only,
        include_shell_hooks=not args.python_only,
    )

    benchmark = HookBenchmark(config)

    try:
        benchmark.setup()
        benchmark.run_benchmarks()

        # Print report
        report = benchmark.generate_report()
        print("\n" + report)

        # Export JSON if requested
        if args.output:
            benchmark.export_json(args.output)
            print(f"\nResults exported to: {args.output}")

    finally:
        benchmark.teardown()


if __name__ == "__main__":
    main()
