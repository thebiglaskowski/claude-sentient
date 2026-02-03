"""Tests for Claude Sentient SDK profile detection and loading."""

from pathlib import Path

from claude_sentient.profiles import GateConfig, Profile, ProfileLoader


class TestGateConfig:
    """Tests for GateConfig dataclass."""

    def test_gate_config_defaults(self):
        """GateConfig should have sensible defaults."""
        config = GateConfig(command="ruff check .")
        assert config.command == "ruff check ."
        assert config.timeout == 300  # Default from actual implementation
        assert config.blocking is True

    def test_gate_config_custom_timeout(self):
        """GateConfig should accept custom timeout."""
        config = GateConfig(command="pytest", timeout=600, blocking=True)
        assert config.timeout == 600

    def test_gate_config_non_blocking(self):
        """GateConfig can be set to non-blocking."""
        config = GateConfig(command="mypy .", timeout=60, blocking=False)
        assert config.blocking is False


class TestProfile:
    """Tests for Profile dataclass."""

    def test_profile_creation(self):
        """Profile should be created with name and gates."""
        profile = Profile(
            name="python",
            detect_files=["pyproject.toml"],
            detect_extensions=[".py"],
            gates={
                "lint": GateConfig(command="ruff check ."),
                "test": GateConfig(command="pytest"),
            },
        )
        assert profile.name == "python"
        assert "pyproject.toml" in profile.detect_files
        assert ".py" in profile.detect_extensions
        assert "lint" in profile.gates
        assert "test" in profile.gates
        assert profile.gates["lint"].command == "ruff check ."

    def test_profile_empty_gates(self):
        """Profile can have no gates."""
        profile = Profile(name="empty")
        assert profile.gates == {}
        assert profile.detect_files == []
        assert profile.detect_extensions == []


class TestProfileLoader:
    """Tests for ProfileLoader class."""

    def test_detect_python_by_pyproject(self, python_project: Path):
        """ProfileLoader should detect Python by pyproject.toml."""
        loader = ProfileLoader()
        profile_name = loader.detect(python_project)
        assert profile_name == "python"

    def test_detect_typescript_by_tsconfig(self, typescript_project: Path):
        """ProfileLoader should detect TypeScript by tsconfig.json."""
        loader = ProfileLoader()
        profile_name = loader.detect(typescript_project)
        assert profile_name == "typescript"

    def test_detect_go_by_gomod(self, go_project: Path):
        """ProfileLoader should detect Go by go.mod."""
        loader = ProfileLoader()
        profile_name = loader.detect(go_project)
        assert profile_name == "go"

    def test_detect_general_fallback(self, temp_dir: Path):
        """ProfileLoader should fall back to 'general' for unknown projects."""
        loader = ProfileLoader()
        profile_name = loader.detect(temp_dir)
        assert profile_name == "general"

    def test_detect_python_by_py_files(self, temp_dir: Path):
        """ProfileLoader should detect Python by .py files."""
        (temp_dir / "main.py").write_text("print('hello')")
        loader = ProfileLoader()
        profile_name = loader.detect(temp_dir)
        assert profile_name == "python"

    def test_detect_typescript_by_ts_files(self, temp_dir: Path):
        """ProfileLoader should detect TypeScript by .ts files."""
        (temp_dir / "index.ts").write_text("const x: number = 1;")
        loader = ProfileLoader()
        profile_name = loader.detect(temp_dir)
        assert profile_name == "typescript"

    def test_load_python_profile(self):
        """ProfileLoader should load Python profile with defaults."""
        loader = ProfileLoader()
        profile = loader.load("python")

        assert profile is not None
        assert profile.name == "python"
        assert "lint" in profile.gates
        assert "test" in profile.gates
        assert profile.gates["lint"].command == "ruff check ."

    def test_load_typescript_profile(self):
        """ProfileLoader should load TypeScript profile with defaults."""
        loader = ProfileLoader()
        profile = loader.load("typescript")

        assert profile is not None
        assert profile.name == "typescript"
        assert "lint" in profile.gates
        assert "test" in profile.gates
        assert "type" in profile.gates

    def test_load_general_profile(self):
        """ProfileLoader should load general profile (empty gates)."""
        loader = ProfileLoader()
        profile = loader.load("general")

        assert profile is not None
        assert profile.name == "general"
        assert profile.gates == {}

    def test_load_nonexistent_returns_none(self):
        """ProfileLoader should return None for unknown profile."""
        loader = ProfileLoader()
        profile = loader.load("nonexistent-profile")
        assert profile is None

    def test_profile_caching(self):
        """ProfileLoader should cache loaded profiles."""
        loader = ProfileLoader()
        profile1 = loader.load("python")
        profile2 = loader.load("python")
        assert profile1 is profile2  # Same object

    def test_get_gate_command(self):
        """ProfileLoader should get gate command by name."""
        loader = ProfileLoader()
        cmd = loader.get_gate_command("python", "lint")
        assert cmd == "ruff check ."

    def test_get_gate_command_missing(self):
        """ProfileLoader should return None for missing gate."""
        loader = ProfileLoader()
        cmd = loader.get_gate_command("python", "nonexistent")
        assert cmd is None

    def test_is_gate_blocking(self):
        """ProfileLoader should check if gate is blocking."""
        loader = ProfileLoader()
        assert loader.is_gate_blocking("python", "lint") is True
        assert loader.is_gate_blocking("python", "type") is False


class TestProfileDetectionPriority:
    """Tests for profile detection priority."""

    def test_pyproject_takes_priority(self, temp_dir: Path):
        """pyproject.toml should take priority over .py files."""
        (temp_dir / "pyproject.toml").write_text("[project]\nname='test'")
        (temp_dir / "script.py").write_text("pass")
        (temp_dir / "script.ts").write_text("const x = 1;")

        loader = ProfileLoader()
        assert loader.detect(temp_dir) == "python"

    def test_tsconfig_takes_priority_over_ts_files(self, temp_dir: Path):
        """tsconfig.json should take priority."""
        (temp_dir / "tsconfig.json").write_text("{}")
        (temp_dir / "script.ts").write_text("const x = 1;")

        loader = ProfileLoader()
        assert loader.detect(temp_dir) == "typescript"

    def test_cargo_toml_for_rust(self, temp_dir: Path):
        """Cargo.toml should detect Rust."""
        (temp_dir / "Cargo.toml").write_text('[package]\nname = "test"')

        loader = ProfileLoader()
        assert loader.detect(temp_dir) == "rust"

    def test_go_mod_for_go(self, temp_dir: Path):
        """go.mod should detect Go."""
        (temp_dir / "go.mod").write_text("module test")

        loader = ProfileLoader()
        assert loader.detect(temp_dir) == "go"
