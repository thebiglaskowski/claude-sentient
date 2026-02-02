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
    """Persist and restore session state.

    Uses a dirty flag pattern to batch writes:
    - Modifications mark the state as dirty
    - Call flush() to persist or use auto_flush=True for immediate writes
    - Context manager ensures flush on exit
    """

    def __init__(self, state_dir: str | Path = ".claude/state", auto_flush: bool = False):
        """Initialize session manager.

        Args:
            state_dir: Directory for session state files
            auto_flush: If True, write to disk on every change (legacy behavior)
                       If False, batch writes until flush() is called
        """
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.state_file = self.state_dir / "session.json"
        self.history_dir = self.state_dir / "history"
        self.history_dir.mkdir(exist_ok=True)

        self.auto_flush = auto_flush
        self._cached_state: SessionState | None = None
        self._dirty = False

    def __enter__(self) -> "SessionManager":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit - flush pending changes."""
        self.flush()

    def flush(self) -> None:
        """Write cached state to disk if dirty."""
        if self._dirty and self._cached_state is not None:
            self._write_state(self._cached_state)
            self._dirty = False

    def _write_state(self, state: SessionState) -> None:
        """Internal method to write state to disk."""
        state.last_updated = datetime.now().isoformat()
        self.state_file.write_text(json.dumps(asdict(state), indent=2))

    def _mark_dirty(self) -> None:
        """Mark state as modified."""
        self._dirty = True
        if self.auto_flush:
            self.flush()

    def save(self, state: SessionState) -> None:
        """Save session state.

        With auto_flush=True (default in legacy mode), writes immediately.
        With auto_flush=False, caches and marks dirty for later flush.
        """
        self._cached_state = state
        self._mark_dirty()

    def load(self) -> SessionState | None:
        """Load current session state.

        Returns cached state if available, otherwise reads from disk.
        """
        # Return cached state if we have it
        if self._cached_state is not None:
            return self._cached_state

        if not self.state_file.exists():
            return None
        try:
            data = json.loads(self.state_file.read_text())
            self._cached_state = SessionState(**data)
            return self._cached_state
        except (json.JSONDecodeError, TypeError):
            return None

    def load_session_id(self) -> str | None:
        """Load just the session ID for resume."""
        state = self.load()
        return state.session_id if state else None

    def clear(self) -> None:
        """Clear current session (archive to history first)."""
        # Flush any pending changes first
        self.flush()

        if self.state_file.exists():
            # Archive to history
            state = self.load()
            if state:
                archive_file = (
                    self.history_dir / f"{state.session_id}.json"
                )
                archive_file.write_text(self.state_file.read_text())
            self.state_file.unlink()

        # Clear cache
        self._cached_state = None
        self._dirty = False

    def create(
        self,
        session_id: str,
        profile: str,
        task: str,
    ) -> SessionState:
        """Create a new session state.

        Note: Always writes immediately to establish the session file.
        """
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
        self._cached_state = state
        # Always write immediately on create to establish session
        self._write_state(state)
        return state

    def update_phase(self, phase: str) -> None:
        """Update the current phase."""
        state = self.load()
        if state:
            state.phase = phase
            self._mark_dirty()

    def increment_iteration(self) -> None:
        """Increment the iteration counter."""
        state = self.load()
        if state:
            state.iteration += 1
            self._mark_dirty()

    def add_commit(self, commit_hash: str) -> None:
        """Record a commit."""
        state = self.load()
        if state:
            state.commits.append(commit_hash)
            self._mark_dirty()

    def add_file_change(self, file_path: str) -> None:
        """Record a file change."""
        state = self.load()
        if state:
            if file_path not in state.file_changes:
                state.file_changes.append(file_path)
                self._mark_dirty()

    def update_gate(self, gate_name: str, result: dict[str, Any]) -> None:
        """Update a gate result."""
        state = self.load()
        if state:
            state.gates[gate_name] = result
            self._mark_dirty()

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
