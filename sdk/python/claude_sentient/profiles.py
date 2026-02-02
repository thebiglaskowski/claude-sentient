"""Profile detection and loading for Claude Sentient SDK."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class GateConfig:
    """Configuration for a quality gate."""

    command: str
    blocking: bool = True
    timeout: int = 300  # seconds


@dataclass
class Profile:
    """Project profile configuration."""

    name: str
    detect_files: list[str] = field(default_factory=list)
    detect_extensions: list[str] = field(default_factory=list)
    gates: dict[str, GateConfig] = field(default_factory=dict)
    conventions: dict[str, Any] = field(default_factory=dict)
    tools: list[str] = field(default_factory=list)


class ProfileLoader:
    """Load and detect project profiles."""

    # Default profile definitions (fallback if YAML files not found)
    DEFAULT_PROFILES: dict[str, dict[str, Any]] = {
        "python": {
            "detect_files": ["pyproject.toml", "setup.py", "requirements.txt"],
            "detect_extensions": [".py"],
            "gates": {
                "lint": {"command": "ruff check .", "blocking": True},
                "test": {"command": "pytest", "blocking": True},
                "type": {"command": "pyright", "blocking": False},
            },
        },
        "typescript": {
            "detect_files": ["tsconfig.json", "package.json"],
            "detect_extensions": [".ts", ".tsx"],
            "gates": {
                "lint": {"command": "npm run lint", "blocking": True},
                "test": {"command": "npm test", "blocking": True},
                "type": {"command": "npx tsc --noEmit", "blocking": True},
            },
        },
        "go": {
            "detect_files": ["go.mod"],
            "detect_extensions": [".go"],
            "gates": {
                "lint": {"command": "golangci-lint run", "blocking": True},
                "test": {"command": "go test ./...", "blocking": True},
            },
        },
        "rust": {
            "detect_files": ["Cargo.toml"],
            "detect_extensions": [".rs"],
            "gates": {
                "lint": {"command": "cargo clippy", "blocking": True},
                "test": {"command": "cargo test", "blocking": True},
            },
        },
        "general": {
            "detect_files": [],
            "detect_extensions": [],
            "gates": {},
        },
    }

    def __init__(self, profiles_dir: str | Path | None = None):
        self.profiles_dir = Path(profiles_dir) if profiles_dir else None
        self._profiles_cache: dict[str, Profile] = {}

    def detect(self, cwd: str | Path) -> str:
        """Auto-detect project profile from files in cwd."""
        cwd = Path(cwd)

        # Check for profile-specific files in priority order
        profile_priority = ["python", "typescript", "go", "rust", "java", "ruby", "shell"]

        for profile_name in profile_priority:
            profile = self.load(profile_name)
            if profile:
                # Check detection files
                for detect_file in profile.detect_files:
                    if (cwd / detect_file).exists():
                        return profile_name

                # Check for files with detection extensions
                for ext in profile.detect_extensions:
                    if list(cwd.glob(f"*{ext}")):
                        return profile_name

        return "general"

    def load(self, profile_name: str) -> Profile | None:
        """Load a profile by name."""
        if profile_name in self._profiles_cache:
            return self._profiles_cache[profile_name]

        profile_data: dict[str, Any] | None = None

        # Try to load from YAML file
        if self.profiles_dir:
            yaml_file = self.profiles_dir / f"{profile_name}.yaml"
            if yaml_file.exists():
                try:
                    profile_data = yaml.safe_load(yaml_file.read_text())
                except yaml.YAMLError:
                    pass

        # Fall back to defaults
        if not profile_data:
            profile_data = self.DEFAULT_PROFILES.get(profile_name)

        if not profile_data:
            return None

        # Parse gates into GateConfig objects
        gates = {}
        for gate_name, gate_config in profile_data.get("gates", {}).items():
            if isinstance(gate_config, dict):
                gates[gate_name] = GateConfig(
                    command=gate_config.get("command", ""),
                    blocking=gate_config.get("blocking", True),
                    timeout=gate_config.get("timeout", 300),
                )
            elif isinstance(gate_config, str):
                gates[gate_name] = GateConfig(command=gate_config)

        profile = Profile(
            name=profile_name,
            detect_files=profile_data.get("detect_files", []),
            detect_extensions=profile_data.get("detect_extensions", []),
            gates=gates,
            conventions=profile_data.get("conventions", {}),
            tools=profile_data.get("tools", []),
        )

        self._profiles_cache[profile_name] = profile
        return profile

    def get_gate_command(self, profile_name: str, gate_name: str) -> str | None:
        """Get the command for a specific gate."""
        profile = self.load(profile_name)
        if profile and gate_name in profile.gates:
            return profile.gates[gate_name].command
        return None

    def is_gate_blocking(self, profile_name: str, gate_name: str) -> bool:
        """Check if a gate is blocking."""
        profile = self.load(profile_name)
        if profile and gate_name in profile.gates:
            return profile.gates[gate_name].blocking
        return True  # Default to blocking
