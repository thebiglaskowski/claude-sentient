#!/usr/bin/env python3
"""
Agent Synthesizer Hook (SubagentStop)

Merges results from completed agents into unified findings.
Updates agent registry and prepares synthesis summary.

Hook Type: SubagentStop
Input: JSON with agent result details
Output: Synthesis summary, updated state
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

STATE_FILE = ".claude/state/active_agents.json"
RESULTS_FILE = ".claude/state/agent_results.json"


def load_state(filepath: str) -> dict:
    """Load state from file."""
    path = Path(filepath)
    if path.exists():
        try:
            return json.loads(path.read_text(encoding='utf-8'))
        except json.JSONDecodeError:
            return {}
    return {}


def save_state(filepath: str, state: dict):
    """Save state to file."""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    Path(filepath).write_text(json.dumps(state, indent=2), encoding='utf-8')


def extract_findings(result: str) -> dict:
    """Extract structured findings from agent result."""
    findings = {
        "issues": [],
        "recommendations": [],
        "changes": [],
        "severity_counts": {"S0": 0, "S1": 0, "S2": 0, "S3": 0}
    }

    if not result:
        return findings

    lines = result.split('\n')
    current_section = None

    for line in lines:
        line_lower = line.lower().strip()

        # Detect severity markers
        for sev in ["s0", "s1", "s2", "s3"]:
            if sev in line_lower or f"severity: {sev}" in line_lower:
                findings["severity_counts"][sev.upper()] += 1

        # Detect section headers
        if "issue" in line_lower or "finding" in line_lower or "problem" in line_lower:
            current_section = "issues"
        elif "recommend" in line_lower or "suggest" in line_lower:
            current_section = "recommendations"
        elif "change" in line_lower or "modif" in line_lower or "update" in line_lower:
            current_section = "changes"

        # Collect bullet points
        if line.strip().startswith(('-', '*', '•', '✓', '✗')):
            content = line.strip().lstrip('-*•✓✗ ').strip()
            if content and current_section and current_section in findings:
                findings[current_section].append(content[:200])

    return findings


def complete_agent(agent_data: dict) -> dict:
    """Mark agent complete and record results."""
    agent_state = load_state(STATE_FILE)
    results_state = load_state(RESULTS_FILE)

    if "results" not in results_state:
        results_state["results"] = []

    agent_id = agent_data.get("agent_id", "unknown")
    result = agent_data.get("result", "")

    # Update agent status
    if agent_id in agent_state.get("agents", {}):
        agent_state["agents"][agent_id]["status"] = "completed"
        agent_state["agents"][agent_id]["completed"] = datetime.now().isoformat()

    # Extract and store findings
    findings = extract_findings(result)
    findings["agent_id"] = agent_id
    findings["agent_type"] = agent_state.get("agents", {}).get(agent_id, {}).get("type", "unknown")
    findings["timestamp"] = datetime.now().isoformat()

    results_state["results"].append(findings)

    # Save states
    save_state(STATE_FILE, agent_state)
    save_state(RESULTS_FILE, results_state)

    # Check if all agents complete
    active_count = sum(
        1 for a in agent_state.get("agents", {}).values()
        if a.get("status") == "running"
    )

    # Generate synthesis if all complete
    synthesis = None
    if active_count == 0 and results_state["results"]:
        synthesis = synthesize_results(results_state["results"])

    return {
        "agent_id": agent_id,
        "findings": findings,
        "active_remaining": active_count,
        "synthesis": synthesis
    }


def synthesize_results(results: list) -> dict:
    """Synthesize all agent results into unified summary."""
    synthesis = {
        "total_agents": len(results),
        "severity_totals": {"S0": 0, "S1": 0, "S2": 0, "S3": 0},
        "all_issues": [],
        "all_recommendations": [],
        "by_agent_type": {}
    }

    for result in results:
        agent_type = result.get("agent_type", "unknown")

        # Aggregate severity counts
        for sev, count in result.get("severity_counts", {}).items():
            synthesis["severity_totals"][sev] += count

        # Collect issues and recommendations
        synthesis["all_issues"].extend(result.get("issues", [])[:10])
        synthesis["all_recommendations"].extend(result.get("recommendations", [])[:5])

        # Group by agent type
        if agent_type not in synthesis["by_agent_type"]:
            synthesis["by_agent_type"][agent_type] = {"count": 0, "findings": 0}
        synthesis["by_agent_type"][agent_type]["count"] += 1
        synthesis["by_agent_type"][agent_type]["findings"] += len(result.get("issues", []))

    # Deduplicate
    synthesis["all_issues"] = list(set(synthesis["all_issues"]))[:20]
    synthesis["all_recommendations"] = list(set(synthesis["all_recommendations"]))[:10]

    return synthesis


def format_synthesis_message(result: dict) -> str:
    """Format synthesis summary for output."""
    lines = [f"[Synthesizer] Agent {result['agent_id']} completed"]

    findings = result.get("findings", {})
    sev = findings.get("severity_counts", {})
    issue_count = len(findings.get("issues", []))

    lines.append(f"  Findings: {issue_count} issues (S0:{sev.get('S0',0)} S1:{sev.get('S1',0)} S2:{sev.get('S2',0)} S3:{sev.get('S3',0)})")
    lines.append(f"  Remaining agents: {result.get('active_remaining', 0)}")

    if result.get("synthesis"):
        syn = result["synthesis"]
        lines.append("")
        lines.append("  === All Agents Complete - Synthesis ===")
        lines.append(f"  Total agents: {syn['total_agents']}")
        sev_totals = syn["severity_totals"]
        lines.append(f"  Combined: S0:{sev_totals['S0']} S1:{sev_totals['S1']} S2:{sev_totals['S2']} S3:{sev_totals['S3']}")
        lines.append(f"  Unique issues: {len(syn['all_issues'])}")
        lines.append(f"  Recommendations: {len(syn['all_recommendations'])}")

    return "\n".join(lines)


def main():
    """Main hook entry point."""
    try:
        input_data = sys.stdin.read()

        if not input_data.strip():
            sys.exit(0)

        data = json.loads(input_data)

        # Complete the agent and synthesize
        result = complete_agent(data)

        # Output synthesis info
        message = format_synthesis_message(result)
        print(message, file=sys.stderr)

        # Output machine-readable result
        print(json.dumps(result))
        sys.exit(0)

    except json.JSONDecodeError:
        sys.exit(0)
    except Exception as e:
        print(f"[Synthesizer Error] {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
