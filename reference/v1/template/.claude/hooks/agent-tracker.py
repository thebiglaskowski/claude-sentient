#!/usr/bin/env python3
"""
Agent Tracker Hook (SubagentStart)

Tracks parallel agent execution for coordination and synthesis.
Maintains agent registry in LOOP_STATE.md or temporary state file.

Hook Type: SubagentStart
Input: JSON with agent details (id, type, task, model)
Output: Registration confirmation, coordination hints
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

STATE_FILE = ".claude/state/active_agents.json"


def ensure_state_dir():
    """Ensure state directory exists."""
    state_dir = Path(".claude/state")
    state_dir.mkdir(parents=True, exist_ok=True)
    return state_dir


def load_agent_state() -> dict:
    """Load current agent state."""
    state_path = Path(STATE_FILE)
    if state_path.exists():
        try:
            return json.loads(state_path.read_text(encoding='utf-8'))
        except json.JSONDecodeError:
            return {"agents": {}, "started": None}
    return {"agents": {}, "started": None}


def save_agent_state(state: dict):
    """Save agent state to file."""
    ensure_state_dir()
    Path(STATE_FILE).write_text(json.dumps(state, indent=2), encoding='utf-8')


def register_agent(agent_data: dict) -> dict:
    """Register a new agent and return coordination info."""
    state = load_agent_state()

    agent_id = agent_data.get("agent_id", f"agent_{len(state['agents'])}")
    agent_type = agent_data.get("subagent_type", "general")
    task = agent_data.get("prompt", "")[:100]
    model = agent_data.get("model", "sonnet")

    # Initialize session if first agent
    if not state["started"]:
        state["started"] = datetime.now().isoformat()

    # Register agent
    state["agents"][agent_id] = {
        "type": agent_type,
        "task": task,
        "model": model,
        "started": datetime.now().isoformat(),
        "status": "running"
    }

    save_agent_state(state)

    # Count active agents by type
    type_counts = {}
    for aid, info in state["agents"].items():
        if info.get("status") == "running":
            atype = info.get("type", "unknown")
            type_counts[atype] = type_counts.get(atype, 0) + 1

    return {
        "agent_id": agent_id,
        "total_active": sum(type_counts.values()),
        "by_type": type_counts,
        "parallel_hint": get_parallel_hint(type_counts, agent_type)
    }


def get_parallel_hint(type_counts: dict, current_type: str) -> str:
    """Provide coordination hints for parallel execution."""
    total = sum(type_counts.values())

    if total > 5:
        return "High parallelism - consider batching results"

    if type_counts.get(current_type, 0) > 1:
        return f"Multiple {current_type} agents active - ensure non-overlapping scope"

    if total > 2:
        return "Moderate parallelism - synthesizer will merge results"

    return "Single agent tracking - proceed normally"


def main():
    """Main hook entry point."""
    try:
        input_data = sys.stdin.read()

        if not input_data.strip():
            sys.exit(0)

        data = json.loads(input_data)

        # Register the agent
        result = register_agent(data)

        # Output tracking info
        print(f"[Agent Tracker] Registered {result['agent_id']}", file=sys.stderr)
        print(f"  Active agents: {result['total_active']}", file=sys.stderr)
        if result['parallel_hint']:
            print(f"  Hint: {result['parallel_hint']}", file=sys.stderr)

        # Output machine-readable result
        print(json.dumps(result))
        sys.exit(0)

    except json.JSONDecodeError:
        sys.exit(0)
    except Exception as e:
        print(f"[Agent Tracker Error] {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
