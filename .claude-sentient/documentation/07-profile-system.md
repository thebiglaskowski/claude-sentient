---
feature: Profile System
version: "1.0"
last_updated: 2026-03-04
dependencies: []
routes: []
status: draft
---

# Profile System

> Auto-detects project type and configures language-specific quality gates, model routing, and environment commands. Profiles eliminate manual configuration — Claude Sentient adapts to any project automatically.

## Supported Profiles

| Profile | Detection Files | Detection Extensions |
|---------|----------------|----------------------|
| `python` | `pyproject.toml`, `requirements.txt`, `setup.py`, `setup.cfg`, `tox.ini` | `.py`, `.pyi`, `.ipynb` |
| `typescript` | `tsconfig.json`, `package.json` (with TS deps) | `.ts`, `.tsx` |
| `go` | `go.mod`, `go.sum` | `.go` |
| `rust` | `Cargo.toml`, `Cargo.lock` | `.rs` |
| `java` | `pom.xml`, `build.gradle`, `build.gradle.kts` | `.java` |
| `cpp` | `CMakeLists.txt`, `Makefile` | `.cpp`, `.cc`, `.cxx`, `.c`, `.h`, `.hpp` |
| `ruby` | `Gemfile`, `Gemfile.lock` | `.rb` |
| `shell` | — | `.sh`, `.bash`, `.zsh`, `.ps1` |
| `general` | fallback (no specific indicators found) | — |

Detection is a cascade: profiles are checked in order; first match wins. `general` is always last.

## Profile YAML Structure

Each profile lives at `profiles/{name}.yaml` and is validated against `schemas/profile.schema.json`.

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Profile identifier (matches filename) |
| `description` | string | Human-readable description |
| `version` | string | Semver version |
| `detection.files` | array | Indicator filenames (any match triggers profile) |
| `detection.extensions` | array | File extensions that indicate this language |
| `gates` | object | Gate definitions (see Gate Structure below) |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `environment` | object | Runtime environment detection (Python-specific) |
| `models.by_phase` | object | Model selection per cs-loop phase |
| `thinking` | object | Extended thinking configuration |
| `web_indicators` | array | Files triggering UI rule auto-load |
| `infrastructure` | object | Docker/CI detection for cs-deploy |
| `plugins.lsp` | string\|null | LSP plugin identifier for auto-install |
| `conventions` | object | Language-specific naming/style conventions |
| `patterns` | object | Common framework patterns for this language |

## Gate Structure

Gates live under `gates:` in the profile YAML. Standard gate keys:

| Key | Purpose |
|-----|---------|
| `command` | Primary command to run |
| `fix_command` | Auto-fix command (enables VERIFY auto-fix sub-loop) |
| `alternative` | Fallback if primary tool not found |
| `detect` | File/directory that must exist for gate to apply |
| `description` | Human-readable gate description |

### Gates Per Profile

| Profile | lint | test | build | type | format | extra |
|---------|------|------|-------|------|--------|-------|
| Python | `ruff check .` | `pytest` | `python -m build` | `pyright` | `ruff format` | `nbqa` (notebooks) |
| TypeScript | `npx eslint .` | `npx vitest run` | `npx tsc --noEmit` | — | — | — |
| Go | `golangci-lint run` | `go test ./...` | `go build ./...` | — | `gofmt -l .` | — |
| Rust | `cargo clippy` | `cargo test` | `cargo build` | — | `cargo fmt --check` | — |
| Java | `mvn checkstyle:check` | `mvn test` | `mvn compile` | — | — | — |
| C/C++ | `clang-tidy` | `ctest` | `cmake --build build` | — | — | — |
| Ruby | `bundle exec rubocop` | `bundle exec rspec` | — | — | — | — |
| Shell | `shellcheck *.sh` | — | — | — | — | — |
| General | auto-detect | auto-detect | auto-detect | — | — | — |

### Auto-Fix Support

Profiles with `fix_command` on the lint gate enable the **VERIFY auto-fix sub-loop** (max 3 attempts):

| Profile | fix_command |
|---------|-------------|
| Python | `ruff check . --fix` |
| TypeScript | `npx eslint . --fix` |
| Go | `golangci-lint run --fix` |
| Rust | `cargo clippy --fix --allow-dirty` |
| Ruby | `bundle exec rubocop -a` |
| C/C++ | `clang-tidy --fix` |

## Python Environment Detection

Python profiles include an `environment` section that detects virtual environments to prefix all gate commands:

| Signal | Detected By | Command Prefix |
|--------|------------|----------------|
| conda | `environment.yml` | `conda run -n {env_name} --no-capture-output` |
| venv | `.venv/` or `venv/` directory | `source .venv/bin/activate &&` |
| poetry | `poetry.lock` | `poetry run` |
| pdm | `pdm.lock` | `pdm run` |
| system | fallback | (none) |

Environment detection is reported during INIT phase: `[INIT] Python env: {type}`.

## Model Routing

Default model assignment per cs-loop phase (from `models.by_phase` in each profile):

| Phase | Default Model | Rationale |
|-------|--------------|-----------|
| INIT | haiku | Fast context loading, minimal reasoning |
| UNDERSTAND | sonnet | Standard analysis |
| PLAN | sonnet | Architecture reasoning |
| EXECUTE | sonnet | Code generation |
| VERIFY | sonnet | Quality analysis |
| COMMIT | haiku | Simple git operations |
| EVALUATE | haiku | Quick pass/fail assessment |

**Keyword overrides** (applied globally across all profiles):
- Task contains `security`, `auth`, `vulnerability` → **opus** for PLAN and VERIFY

These can be customized per-project via `/cs-multi`. See `documentation/15-multi-model-routing.md`.

## Web Project Detection

Profiles with `web_indicators` auto-load the `ui-ux-design` rule when indicators are found:

| Profile | Indicators |
|---------|-----------|
| TypeScript | `next.config.*`, `vite.config.*`, react/vue/svelte in `package.json` |
| Python | `templates/` directory, django/flask/jinja2 in requirements |

## Infrastructure Detection

The `infrastructure` section powers `/cs-deploy` checks:

```yaml
infrastructure:
  docker:
    indicators: [Dockerfile, docker-compose.yml]
    commands:
      build: docker build -t {project_name} .
      up: docker-compose up -d
      test: docker-compose run --rm app {test_command}
  ci:
    indicators: [.github/workflows/, .gitlab-ci.yml]
    type: auto-detect
```

## Plugin Auto-Install

Each profile declares `plugins.lsp` — the LSP plugin installed project-scoped during setup:

| Profile | Plugin |
|---------|--------|
| python | `pyright-lsp@claude-plugins-official` |
| typescript | `typescript-lsp@claude-plugins-official` |
| go | `gopls-lsp@claude-plugins-official` |
| rust | `rust-analyzer-lsp@claude-plugins-official` |
| java | `jdtls-lsp@claude-plugins-official` |
| cpp | `clangd-lsp@claude-plugins-official` |
| ruby/shell/general | null (no LSP) |

The `security-guidance@claude-plugins-official` plugin is always installed user-scoped (all profiles).

## Business Rules

- **Detection cascade**: Profiles checked in priority order; `general` is always the fallback.
- **Gate applicability**: Gates with a `detect` field only run if the specified file/directory exists.
- **Alt commands**: If primary lint/test tool isn't installed, try `alternative` command.
- **VERIFY auto-fix**: Only attempts fix if `fix_command` is defined. Max 3 attempts. Reverts if error count increases.
- **Plugin installs**: Non-fatal — `|| true` wrapping means missing `claude` CLI doesn't block setup.
- **Profile schema validation**: Run `node profiles/__tests__/test-profiles.js` to validate YAML. Enforces required fields, version consistency, gate structure.

## Edge Cases

- **No profile matched**: Falls back to `general` profile with auto-detect gates.
- **Multiple indicators**: First matching profile in priority order wins. Go project with Python scripts → detected as Go (go.mod takes precedence).
- **Missing gate tool**: Gate skipped with advisory warning, not blocking error.
- **Python notebooks**: `nbqa` gate runs if `.ipynb` files detected.
- **Windows paths**: Gates use cross-platform commands. No hardcoded `/` separators.
