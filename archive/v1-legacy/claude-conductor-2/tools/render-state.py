#!/usr/bin/env python3
"""
State rendering tool for Claude Conductor 2.0

Converts JSON state to human-readable Markdown.

Usage:
    python render-state.py                           # Render current state
    python render-state.py .claude/state/loop.state.json  # Render specific file
    python render-state.py --watch                   # Watch and auto-render
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

try:
    from jsonschema import validate
except ImportError:
    validate = None  # Optional


def load_state(state_path: Path) -> dict:
    """Load JSON state file."""
    with open(state_path) as f:
        return json.load(f)


def format_status_icon(status: str) -> str:
    """Convert status to icon."""
    icons = {
        "pending": "⏳",
        "running": "🔄",
        "in-progress": "🔄",
        "passed": "✅",
        "done": "✅",
        "complete": "✅",
        "failed": "❌",
        "skipped": "⏭️",
        "blocked": "🚫",
        "cancelled": "🚫",
    }
    return icons.get(status, "❓")


def format_priority(priority: str) -> str:
    """Format priority with color hint."""
    colors = {
        "S0": "🔴",
        "S1": "🟠",
        "S2": "🟡",
        "S3": "🟢",
    }
    return f"{colors.get(priority, '')} {priority}"


def format_context_bar(budget_used: float) -> str:
    """Create visual context budget bar."""
    filled = int(budget_used * 20)
    empty = 20 - filled
    return f"[{'█' * filled}{'░' * empty}] {int(budget_used * 100)}%"


def render_state(state: dict) -> str:
    """Convert state dict to Markdown."""
    lines = []

    # Header
    lines.append("# Loop State\n")
    session_id = state.get("sessionId", "unknown")[:8] if state.get("sessionId") else "none"
    started = state.get("startedAt", "unknown")
    iteration = state.get("iteration", 0)
    lines.append(f"**Session:** {session_id} | **Started:** {started} | **Iteration:** {iteration}\n")

    # Classification
    if state.get("classification"):
        c = state["classification"]
        lines.append("## Classification\n")
        lines.append("| Property | Value |")
        lines.append("|----------|-------|")
        lines.append(f"| Type | {c.get('type', 'unknown')} |")
        lines.append(f"| Complexity | {c.get('complexity', 'unknown')} |")
        lines.append(f"| Subagents | {c.get('subagentCount', 0)} |")
        lines.append(f"| Mode | {c.get('orchestrationMode', 'standard')} |")
        lines.append("")

    # Work Queue
    queue = state.get("workQueue", [])
    if queue:
        lines.append("## Work Queue\n")
        lines.append("| ID | Priority | Title | Status | Blocked By |")
        lines.append("|----|----------|-------|--------|------------|")
        for item in queue:
            blocked = ", ".join(item.get("blockedBy", [])) or "—"
            status_icon = format_status_icon(item.get("status", "pending"))
            status = item.get("status", "pending").replace("-", " ").title()
            lines.append(
                f"| {item['id']} | {format_priority(item['priority'])} | "
                f"{item['title']} | {status_icon} {status} | {blocked} |"
            )
        lines.append("")

    # Quality Gates
    gates = state.get("gates", {})
    if gates:
        lines.append("## Quality Gates\n")
        lines.append("| Gate | Status | Value | Threshold |")
        lines.append("|------|--------|-------|-----------|")
        for name, gate in gates.items():
            status = gate.get("status", "pending")
            icon = format_status_icon(status)
            value = gate.get("value", "—")
            threshold = gate.get("threshold", "—")
            if isinstance(value, float):
                value = f"{value:.0%}" if value <= 1 else f"{value:.1f}"
            if isinstance(threshold, float):
                threshold = f"{threshold:.0%}" if threshold <= 1 else f"{threshold:.1f}"
            lines.append(f"| {name} | {icon} {status.title()} | {value} | {threshold} |")
        lines.append("")

    # Context Budget
    context = state.get("context", {})
    if context:
        lines.append("## Context Budget\n")
        lines.append("```")
        budget = context.get("budgetUsed", 0)
        level = context.get("level", "green")
        lines.append(f"{format_context_bar(budget)} ({level.title()})")
        if context.get("compactionReady"):
            lines.append("Compaction: Ready")
        lines.append("```")
        lines.append("")

    # Metrics
    metrics = state.get("metrics", {})
    if metrics:
        lines.append("## Metrics\n")
        for key, value in metrics.items():
            # Convert camelCase to readable
            readable = "".join(" " + c if c.isupper() else c for c in key).strip().title()
            lines.append(f"- {readable}: {value}")
        lines.append("")

    # Recent History
    history = state.get("history", [])
    if history:
        lines.append("## Recent History\n")
        lines.append("| Iteration | Phase | Action | Result |")
        lines.append("|-----------|-------|--------|--------|")
        for entry in history[-10:]:  # Last 10 entries
            lines.append(
                f"| {entry.get('iteration', '—')} | {entry.get('phase', '—')} | "
                f"{entry.get('action', '—')} | {entry.get('result', '—')} |"
            )
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Render loop state as Markdown")
    parser.add_argument("file", nargs="?", default=".claude/state/loop.state.json",
                        help="State file to render")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    parser.add_argument("--watch", "-w", action="store_true",
                        help="Watch file and auto-render on change")
    args = parser.parse_args()

    state_path = Path(args.file)

    if not state_path.exists():
        print(f"State file not found: {state_path}")
        print("Using default empty state...")
        state = {"version": "2.0", "iteration": 0, "phase": "classify"}
    else:
        state = load_state(state_path)

    markdown = render_state(state)

    if args.output:
        Path(args.output).write_text(markdown)
        print(f"Rendered to {args.output}")
    else:
        print(markdown)


if __name__ == "__main__":
    main()
