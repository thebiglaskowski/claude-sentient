"""Session persistence for Claude Sentient SDK."""

import json
import os
import re
import sys
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class SessionState:
    """Persistent session state."""

    session_id: str
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())
    phase: str = "init"  # init, understand, plan, execute, verify, commit, evaluate, complete, archived
    iteration: int = 1
    profile: str = "general"
    task: str = ""  # The original task/prompt
    cwd: str = ""  # Working directory

    # Session naming and forking
    name: str | None = None  # Human-readable session name
    parent_session_id: str | None = None  # For forks
    forked_at: str | None = None  # When this session was forked

    # Task tracking
    tasks: list[dict[str, Any]] = field(default_factory=list)
    tasks_completed: int = 0

    # Quality gates
    gates: dict[str, dict[str, Any]] = field(default_factory=dict)

    # Git tracking
    commits: list[str] = field(default_factory=list)
    file_changes: list[str] = field(default_factory=list)

    # Cost tracking
    cost_usd: float = 0.0
    cost_by_phase: dict[str, float] = field(default_factory=dict)
    cost_by_model: dict[str, float] = field(default_factory=dict)
    budget_usd: float | None = None

    # State backups (for PreCompact)
    backups: list[dict[str, Any]] = field(default_factory=list)

    # Metadata
    metadata: dict[str, Any] = field(default_factory=dict)


# Task timeout configuration (milliseconds)
TASK_TIMEOUTS = {
    "tests": 600000,       # 10 min
    "build": 300000,       # 5 min
    "exploration": 180000,  # 3 min
    "lint": 120000,        # 2 min
    "default": 120000,     # 2 min
}


def get_task_timeout(task_type: str) -> int:
    """Get the timeout for a task type in milliseconds."""
    return TASK_TIMEOUTS.get(task_type, TASK_TIMEOUTS["default"])


def generate_session_name(task: str, command: str = "loop") -> str:
    """Generate a human-readable session name from task and command.

    Format: {command}-{YYYYMMDD}-{task-slug}

    Examples:
        - loop-20240201-add-auth → from "/cs-loop add user authentication"
        - plan-refactor-api → from "/cs-plan refactor the API layer"
        - review-pr-42 → from "/cs-review 42"
        - assess-20240201 → from "/cs-assess"
    """
    date_str = datetime.now().strftime("%Y%m%d")

    # Extract slug from task (first 3-4 significant words)
    words = re.sub(r"[^\w\s-]", "", task.lower()).split()
    # Filter out common words
    stopwords = {"the", "a", "an", "to", "for", "in", "on", "with", "and", "or", "is", "it"}
    significant_words = [w for w in words if w not in stopwords][:4]
    slug = "-".join(significant_words) if significant_words else "task"

    # Handle special commands
    if command == "review":
        # Extract PR number if present
        pr_match = re.search(r"\b(\d+)\b", task)
        if pr_match:
            return f"review-pr-{pr_match.group(1)}"
        return f"review-{date_str}"
    elif command == "assess":
        return f"assess-{date_str}"
    elif command == "plan":
        return f"plan-{slug}"

    return f"{command}-{date_str}-{slug}"


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
        self._set_secure_permissions(self.state_dir)
        self.state_file = self.state_dir / "session.json"
        self.history_dir = self.state_dir / "history"
        self.history_dir.mkdir(exist_ok=True)
        self._set_secure_permissions(self.history_dir)
        self.forks_dir = self.state_dir / "forks"
        self.forks_dir.mkdir(exist_ok=True)
        self._set_secure_permissions(self.forks_dir)

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

    def _set_secure_permissions(self, path: Path) -> None:
        """Set secure permissions on file or directory (owner-only access).

        On Unix: chmod 0700 for directories, 0600 for files.
        On Windows: Relies on NTFS ACLs (no chmod equivalent).
        """
        if sys.platform != "win32":
            mode = 0o700 if path.is_dir() else 0o600
            os.chmod(path, mode)

    def _write_state(self, state: SessionState) -> None:
        """Internal method to write state to disk."""
        state.last_updated = datetime.now().isoformat()
        self.state_file.write_text(json.dumps(asdict(state), indent=2))
        self._set_secure_permissions(self.state_file)

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

    def load_by_name(self, name: str) -> SessionState | None:
        """Load a session by its name from history or forks."""
        # Check current session first
        state = self.load()
        if state and state.name == name:
            return state

        # Check forks
        for fork_file in self.forks_dir.glob("*.json"):
            try:
                data = json.loads(fork_file.read_text())
                if data.get("name") == name:
                    return SessionState(**data)
            except (json.JSONDecodeError, TypeError):
                continue

        # Check history
        for hist_file in self.history_dir.glob("*.json"):
            try:
                data = json.loads(hist_file.read_text())
                if data.get("name") == name:
                    return SessionState(**data)
            except (json.JSONDecodeError, TypeError):
                continue

        return None

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
        session_id: str | None = None,
        profile: str = "general",
        task: str = "",
        name: str | None = None,
        command: str = "loop",
        cwd: str = "",
    ) -> SessionState:
        """Create a new session state.

        Args:
            session_id: Unique session ID (auto-generated if not provided)
            profile: Project profile name
            task: The original task/prompt
            name: Human-readable session name (auto-generated if not provided)
            command: Command that started the session (for name generation)
            cwd: Working directory

        Note: Always writes immediately to establish the session file.
        """
        if session_id is None:
            session_id = f"session-{int(datetime.now().timestamp())}-{uuid.uuid4().hex[:8]}"

        if name is None:
            name = generate_session_name(task, command)

        now = datetime.now().isoformat()
        state = SessionState(
            session_id=session_id,
            started_at=now,
            last_updated=now,
            phase="init",
            iteration=1,
            profile=profile,
            task=task,
            name=name,
            cwd=cwd,
        )
        self._cached_state = state
        # Always write immediately on create to establish session
        self._write_state(state)
        return state

    def fork(self, fork_name: str | None = None) -> "SessionManager":
        """Create a fork of the current session for experimentation.

        Args:
            fork_name: Name for the fork (auto-generated if not provided)

        Returns:
            New SessionManager instance for the forked session
        """
        state = self.load()
        if not state:
            raise ValueError("No session to fork")

        # Generate fork name
        if fork_name is None:
            fork_name = f"{state.name or state.session_id}-fork-{uuid.uuid4().hex[:4]}"

        # Create fork session ID
        fork_session_id = f"fork-{int(datetime.now().timestamp())}-{uuid.uuid4().hex[:8]}"

        # Create fork state
        now = datetime.now().isoformat()
        fork_state = SessionState(
            session_id=fork_session_id,
            started_at=now,
            last_updated=now,
            phase=state.phase,
            iteration=state.iteration,
            profile=state.profile,
            task=state.task,
            name=fork_name,
            parent_session_id=state.session_id,
            forked_at=now,
            cwd=state.cwd,
            tasks=list(state.tasks),  # Copy tasks
            tasks_completed=state.tasks_completed,
            gates=dict(state.gates),  # Copy gates
            commits=list(state.commits),  # Copy commits
            file_changes=list(state.file_changes),  # Copy file changes
            cost_usd=state.cost_usd,
            cost_by_phase=dict(state.cost_by_phase),
            cost_by_model=dict(state.cost_by_model),
            budget_usd=state.budget_usd,
            metadata=dict(state.metadata),
        )

        # Save fork to forks directory
        fork_file = self.forks_dir / f"{fork_session_id}.json"
        fork_file.write_text(json.dumps(asdict(fork_state), indent=2))

        # Create new SessionManager for fork
        fork_manager = SessionManager(
            state_dir=self.forks_dir / fork_session_id,
            auto_flush=self.auto_flush,
        )
        fork_manager._cached_state = fork_state
        fork_manager._write_state(fork_state)

        return fork_manager

    def merge_fork(self, fork_manager: "SessionManager") -> None:
        """Merge a successful fork back into this session.

        Args:
            fork_manager: The forked session manager to merge from
        """
        state = self.load()
        fork_state = fork_manager.load()

        if not state or not fork_state:
            raise ValueError("Cannot merge: missing session state")

        if fork_state.parent_session_id != state.session_id:
            raise ValueError("Cannot merge: fork is not a child of this session")

        # Merge changes from fork
        # Take the more progressed phase
        state.phase = fork_state.phase
        state.iteration = max(state.iteration, fork_state.iteration)
        state.tasks_completed = fork_state.tasks_completed

        # Merge file changes (union)
        for file_path in fork_state.file_changes:
            if file_path not in state.file_changes:
                state.file_changes.append(file_path)

        # Merge commits (append new ones)
        for commit in fork_state.commits:
            if commit not in state.commits:
                state.commits.append(commit)

        # Merge gates (take fork's results)
        state.gates.update(fork_state.gates)

        # Update costs
        state.cost_usd = fork_state.cost_usd
        state.cost_by_phase = fork_state.cost_by_phase
        state.cost_by_model = fork_state.cost_by_model

        self._mark_dirty()

    def list_forks(self) -> list[dict[str, Any]]:
        """List all forks of the current session."""
        state = self.load()
        if not state:
            return []

        forks = []
        for fork_file in self.forks_dir.glob("*.json"):
            try:
                data = json.loads(fork_file.read_text())
                if data.get("parent_session_id") == state.session_id:
                    forks.append({
                        "session_id": data.get("session_id"),
                        "name": data.get("name"),
                        "forked_at": data.get("forked_at"),
                        "phase": data.get("phase"),
                    })
            except (json.JSONDecodeError, TypeError):
                continue

        return sorted(forks, key=lambda x: x.get("forked_at", ""), reverse=True)

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
        if state and file_path not in state.file_changes:
            state.file_changes.append(file_path)
            self._mark_dirty()

    def update_gate(self, gate_name: str, result: dict[str, Any]) -> None:
        """Update a gate result."""
        state = self.load()
        if state:
            state.gates[gate_name] = result
            self._mark_dirty()

    def increment_tasks_completed(self) -> None:
        """Increment the tasks completed counter."""
        state = self.load()
        if state:
            state.tasks_completed += 1
            self._mark_dirty()

    # --- Cost tracking methods ---

    def add_cost(
        self,
        amount_usd: float,
        phase: str | None = None,
        model: str | None = None,
    ) -> None:
        """Add cost to the session tracking."""
        state = self.load()
        if not state:
            return

        state.cost_usd += amount_usd

        if phase:
            state.cost_by_phase[phase] = (
                state.cost_by_phase.get(phase, 0.0) + amount_usd
            )

        if model:
            state.cost_by_model[model] = (
                state.cost_by_model.get(model, 0.0) + amount_usd
            )

        self._mark_dirty()

    def set_budget(self, budget_usd: float) -> None:
        """Set the cost budget for this session."""
        state = self.load()
        if state:
            state.budget_usd = budget_usd
            self._mark_dirty()

    def is_over_budget(self) -> bool:
        """Check if the session has exceeded its budget."""
        state = self.load()
        if not state or state.budget_usd is None:
            return False
        return state.cost_usd > state.budget_usd

    def get_budget_remaining(self) -> float | None:
        """Get the remaining budget in USD."""
        state = self.load()
        if not state or state.budget_usd is None:
            return None
        return max(0.0, state.budget_usd - state.cost_usd)

    def get_cost_summary(self) -> dict[str, Any]:
        """Get a summary of session costs."""
        state = self.load()
        if not state:
            return {}

        return {
            "total_usd": state.cost_usd,
            "by_phase": state.cost_by_phase,
            "by_model": state.cost_by_model,
            "budget_usd": state.budget_usd,
            "remaining_usd": self.get_budget_remaining(),
            "over_budget": self.is_over_budget(),
        }

    # --- History methods ---

    def list_history(self) -> list[dict[str, Any]]:
        """List archived sessions."""
        sessions = []
        for file in self.history_dir.glob("*.json"):
            try:
                data = json.loads(file.read_text())
                sessions.append({
                    "session_id": data.get("session_id"),
                    "name": data.get("name"),
                    "task": data.get("task"),
                    "started_at": data.get("started_at"),
                    "last_updated": data.get("last_updated"),
                    "profile": data.get("profile"),
                    "cost_usd": data.get("cost_usd", 0.0),
                })
            except (json.JSONDecodeError, KeyError):
                continue
        return sorted(sessions, key=lambda x: x.get("started_at", ""), reverse=True)

    def get_session_info(self) -> dict[str, Any] | None:
        """Get info about the current session."""
        state = self.load()
        if not state:
            return None

        return {
            "session_id": state.session_id,
            "name": state.name,
            "task": state.task,
            "started_at": state.started_at,
            "last_updated": state.last_updated,
            "phase": state.phase,
            "iteration": state.iteration,
            "profile": state.profile,
            "tasks_completed": state.tasks_completed,
            "files_changed": len(state.file_changes),
            "commits": len(state.commits),
            "cost_usd": state.cost_usd,
            "budget_usd": state.budget_usd,
            "parent_session_id": state.parent_session_id,
            "is_fork": state.parent_session_id is not None,
        }
