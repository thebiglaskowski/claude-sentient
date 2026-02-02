"""Pytest fixtures for Claude Sentient SDK tests."""

import os
import tempfile
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def python_project(temp_dir: Path) -> Path:
    """Create a mock Python project structure."""
    # Create pyproject.toml
    pyproject = temp_dir / "pyproject.toml"
    pyproject.write_text("""
[project]
name = "test-project"
version = "0.1.0"

[tool.ruff]
line-length = 88
""")

    # Create a Python file
    src = temp_dir / "src"
    src.mkdir()
    (src / "__init__.py").write_text("")
    (src / "main.py").write_text("def hello(): return 'world'")

    return temp_dir


@pytest.fixture
def typescript_project(temp_dir: Path) -> Path:
    """Create a mock TypeScript project structure."""
    # Create package.json
    package_json = temp_dir / "package.json"
    package_json.write_text("""{
  "name": "test-project",
  "version": "1.0.0",
  "scripts": {
    "lint": "eslint .",
    "test": "vitest"
  }
}""")

    # Create tsconfig.json
    tsconfig = temp_dir / "tsconfig.json"
    tsconfig.write_text("""{
  "compilerOptions": {
    "target": "es2020",
    "module": "commonjs",
    "strict": true
  }
}""")

    # Create a TypeScript file
    src = temp_dir / "src"
    src.mkdir()
    (src / "index.ts").write_text("export const hello = (): string => 'world';")

    return temp_dir


@pytest.fixture
def go_project(temp_dir: Path) -> Path:
    """Create a mock Go project structure."""
    # Create go.mod
    go_mod = temp_dir / "go.mod"
    go_mod.write_text("module test-project\n\ngo 1.21")

    # Create a Go file
    (temp_dir / "main.go").write_text("""package main

func main() {
    println("Hello, World!")
}
""")

    return temp_dir


@pytest.fixture
def claude_state_dir(temp_dir: Path) -> Path:
    """Create .claude/state directory structure."""
    state_dir = temp_dir / ".claude" / "state"
    state_dir.mkdir(parents=True)
    return state_dir


@pytest.fixture
def profiles_dir() -> Path:
    """Get the real profiles directory."""
    # Navigate from sdk/python/tests to profiles/
    return Path(__file__).parent.parent.parent.parent.parent / "profiles"
