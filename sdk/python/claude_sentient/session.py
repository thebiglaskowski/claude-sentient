"""Session persistence for Claude Sentient SDK."""

import json
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class SessionState:
    """Persistent session state."""

    session_id: str
    started_at: str
    last_updated: str
    phase: str  # init, understand, plan, execute, verify, commit, evaluate
    iteration: int
    profile: str
    task: str  # The original task/prompt
    tasks: list[dict[str, Any]] = field(default_factory=list)
    gates: dict[str, dict[str, Any]] = field(default_factory=dict)
    commits: list[str] = field(default_factory=list)
    file_changes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class SessionManager:
    """Persist and restore session state."""

    def __init__(self, state_dir: str | Path = ".claude/state"):
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.state_file = self.state_dir / "session.json"
        self.history_dir = self.state_dir / "history"
        self.history_dir.mkdir(exist_ok=True)

    def save(self, state: SessionState) -> None:
        """Save current session state."""
        state.last_updated = datetime.now().isoformat()
        self.state_file.write_text(json.dumps(asdict(state), indent=2))

    def load(self) -> SessionState | None:
        """Load current session state."""
        if not self.state_file.exists():
            return None
        try:
            data = json.loads(self.state_file.read_text())
            return SessionState(**data)
        except (json.JSONDecodeError, TypeError):
            return None

    def load_session_id(self) -> str | None:
        """Load just the session ID for resume."""
        state = self.load()
        return state.session_id if state else None

    def clear(self) -> None:
        """Clear current session (archive to history first)."""
        if self.state_file.exists():
            # Archive to history
            state = self.load()
            if state:
                archive_file = (
                    self.history_dir / f"{state.session_id}.json"
                )
                archive_file.write_text(self.state_file.read_text())
            self.state_file.unlink()

    def create(
        self,
        session_id: str,
        profile: str,
        task: str,
    ) -> SessionState:
        """Create a new session state."""
        now = datetime.now().isoformat()
        state = SessionState(
            session_id=session_id,
            started_at=now,
            last_updated=now,
            phase="init",
            iteration=1,
            profile=profile,
            task=task,
        )
        self.save(state)
        return state

    def update_phase(self, phase: str) -> None:
        """Update the current phase."""
        state = self.load()
        if state:
            state.phase = phase
            self.save(state)

    def increment_iteration(self) -> None:
        """Increment the iteration counter."""
        state = self.load()
        if state:
            state.iteration += 1
            self.save(state)

    def add_commit(self, commit_hash: str) -> None:
        """Record a commit."""
        state = self.load()
        if state:
            state.commits.append(commit_hash)
            self.save(state)

    def add_file_change(self, file_path: str) -> None:
        """Record a file change."""
        state = self.load()
        if state:
            if file_path not in state.file_changes:
                state.file_changes.append(file_path)
                self.save(state)

    def update_gate(self, gate_name: str, result: dict[str, Any]) -> None:
        """Update a gate result."""
        state = self.load()
        if state:
            state.gates[gate_name] = result
            self.save(state)

    def list_history(self) -> list[dict[str, Any]]:
        """List archived sessions."""
        sessions = []
        for file in self.history_dir.glob("*.json"):
            try:
                data = json.loads(file.read_text())
                sessions.append({
                    "session_id": data.get("session_id"),
                    "task": data.get("task"),
                    "started_at": data.get("started_at"),
                    "last_updated": data.get("last_updated"),
                    "profile": data.get("profile"),
                })
            except (json.JSONDecodeError, KeyError):
                continue
        return sorted(sessions, key=lambda x: x.get("started_at", ""), reverse=True)
