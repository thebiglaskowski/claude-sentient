"""Profile detection and loading for Claude Sentient SDK."""

import contextlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from .datatypes import ModelTier, Phase


@dataclass
class GateConfig:
    """Configuration for a quality gate."""

    command: str
    blocking: bool = True
    timeout: int = 300  # seconds


@dataclass
class ModelConfig:
    """Model routing configuration."""

    default: ModelTier = ModelTier.SONNET
    planning: ModelTier = ModelTier.OPUS
    exploration: ModelTier = ModelTier.HAIKU
    security: ModelTier = ModelTier.OPUS
    # Phase-specific overrides
    by_phase: dict[str, ModelTier] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ModelConfig":
        """Create from dictionary."""
        by_phase = {}
        for phase_name, model_name in data.get("by_phase", {}).items():
            try:
                by_phase[phase_name] = ModelTier(model_name)
            except ValueError:
                pass  # Skip invalid model names

        return cls(
            default=ModelTier(data.get("default", "sonnet")),
            planning=ModelTier(data.get("planning", "opus")),
            exploration=ModelTier(data.get("exploration", "haiku")),
            security=ModelTier(data.get("security", "opus")),
            by_phase=by_phase,
        )

    def get_model_for_phase(self, phase: Phase) -> ModelTier:
        """Get the model to use for a specific phase."""
        # Check phase-specific override first
        if phase.value in self.by_phase:
            return self.by_phase[phase.value]

        # Default phase routing
        phase_defaults = {
            Phase.INIT: ModelTier.HAIKU,
            Phase.UNDERSTAND: ModelTier.SONNET,
            Phase.PLAN: self.planning,
            Phase.EXECUTE: ModelTier.SONNET,
            Phase.VERIFY: ModelTier.SONNET,
            Phase.COMMIT: ModelTier.HAIKU,
            Phase.EVALUATE: ModelTier.HAIKU,
        }

        return phase_defaults.get(phase, self.default)


@dataclass
class ThinkingConfig:
    """Extended thinking configuration."""

    max_tokens: int = 16000
    extended_for: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ThinkingConfig":
        """Create from dictionary."""
        return cls(
            max_tokens=data.get("max_tokens", data.get("maxTokens", 16000)),
            extended_for=data.get("extended_for", data.get("extendedFor", [])),
        )

    def should_extend(self, task_description: str) -> bool:
        """Check if extended thinking should be used for this task."""
        task_lower = task_description.lower()
        return any(keyword.lower() in task_lower for keyword in self.extended_for)


@dataclass
class Profile:
    """Project profile configuration."""

    name: str
    detect_files: list[str] = field(default_factory=list)
    detect_extensions: list[str] = field(default_factory=list)
    gates: dict[str, GateConfig] = field(default_factory=dict)
    conventions: dict[str, Any] = field(default_factory=dict)
    tools: list[str] = field(default_factory=list)
    models: ModelConfig = field(default_factory=ModelConfig)
    thinking: ThinkingConfig = field(default_factory=ThinkingConfig)


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
            "models": {
                "default": "sonnet",
                "planning": "opus",
                "exploration": "haiku",
                "security": "opus",
            },
            "thinking": {
                "max_tokens": 16000,
                "extended_for": ["architecture", "security", "complex-refactoring"],
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
            "models": {
                "default": "sonnet",
                "planning": "opus",
                "exploration": "haiku",
                "security": "opus",
            },
            "thinking": {
                "max_tokens": 16000,
                "extended_for": ["architecture", "security", "complex-refactoring"],
            },
        },
        "go": {
            "detect_files": ["go.mod"],
            "detect_extensions": [".go"],
            "gates": {
                "lint": {"command": "golangci-lint run", "blocking": True},
                "test": {"command": "go test ./...", "blocking": True},
            },
            "models": {
                "default": "sonnet",
                "planning": "opus",
                "exploration": "haiku",
                "security": "opus",
            },
            "thinking": {
                "max_tokens": 16000,
                "extended_for": ["architecture", "security", "concurrency"],
            },
        },
        "rust": {
            "detect_files": ["Cargo.toml"],
            "detect_extensions": [".rs"],
            "gates": {
                "lint": {"command": "cargo clippy", "blocking": True},
                "test": {"command": "cargo test", "blocking": True},
            },
            "models": {
                "default": "sonnet",
                "planning": "opus",
                "exploration": "haiku",
                "security": "opus",
            },
            "thinking": {
                "max_tokens": 16000,
                "extended_for": ["architecture", "security", "lifetime-issues", "unsafe"],
            },
        },
        "general": {
            "detect_files": [],
            "detect_extensions": [],
            "gates": {},
            "models": {
                "default": "sonnet",
                "planning": "opus",
                "exploration": "haiku",
                "security": "opus",
            },
            "thinking": {
                "max_tokens": 16000,
                "extended_for": ["architecture", "security"],
            },
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

                # Check for files with detection extensions (early exit on first match)
                for ext in profile.detect_extensions:
                    if next(cwd.glob(f"*{ext}"), None):
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
                with contextlib.suppress(yaml.YAMLError):
                    profile_data = yaml.safe_load(yaml_file.read_text())

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

        # Parse models config
        models_data = profile_data.get("models", {})
        if models_data:
            models = ModelConfig.from_dict(models_data)
        else:
            models = ModelConfig()

        # Parse thinking config
        thinking_data = profile_data.get("thinking", {})
        if thinking_data:
            thinking = ThinkingConfig.from_dict(thinking_data)
        else:
            thinking = ThinkingConfig()

        profile = Profile(
            name=profile_name,
            detect_files=profile_data.get("detect_files", profile_data.get("detection", {}).get("files", [])),
            detect_extensions=profile_data.get("detect_extensions", []),
            gates=gates,
            conventions=profile_data.get("conventions", {}),
            tools=profile_data.get("tools", []),
            models=models,
            thinking=thinking,
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

    def get_model_for_phase(
        self,
        profile_name: str,
        phase: Phase,
        task_keywords: list[str] | None = None,
    ) -> ModelTier:
        """Get the model to use for a specific phase and task."""
        profile = self.load(profile_name)
        if not profile:
            return ModelTier.SONNET

        # Check for security-related keywords
        if task_keywords:
            security_keywords = ["security", "vulnerability", "auth", "permission", "encrypt"]
            if any(kw in security_keywords for kw in task_keywords):
                return profile.models.security

        return profile.models.get_model_for_phase(phase)

    def should_use_extended_thinking(
        self,
        profile_name: str,
        task_description: str,
    ) -> bool:
        """Check if extended thinking should be used for this task."""
        profile = self.load(profile_name)
        if not profile:
            return False

        return profile.thinking.should_extend(task_description)

    def get_thinking_tokens(self, profile_name: str) -> int:
        """Get the max thinking tokens for a profile."""
        profile = self.load(profile_name)
        if not profile:
            return 16000

        return profile.thinking.max_tokens
