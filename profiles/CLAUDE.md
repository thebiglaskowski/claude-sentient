# Profiles — Claude Sentient

> Context for working on language profile YAML files.

## Profile Detection

Sentient auto-detects project type by scanning for indicator files:

| Profile | Detected By | Lint | Test | Build |
|---------|-------------|------|------|-------|
| Python | `pyproject.toml`, `*.py`, `*.ipynb` | ruff check | pytest | python -m build |
| TypeScript | `tsconfig.json`, `*.ts` | eslint | vitest | tsc |
| Go | `go.mod`, `*.go` | golangci-lint run | go test ./... | go build ./... |
| Rust | `Cargo.toml` | cargo clippy | cargo test | cargo build |
| Java | `pom.xml`, `build.gradle` | mvn checkstyle:check | mvn test | mvn compile |
| C/C++ | `CMakeLists.txt`, `Makefile` | clang-tidy | ctest | cmake --build build |
| Ruby | `Gemfile` | rubocop | rspec | — |
| Shell | `*.sh`, `*.ps1` | shellcheck | — | — |
| General | (fallback) | auto-detect | auto-detect | auto-detect |

---

## Profile YAML Structure

Every profile must have these fields:

```yaml
name: python
description: Python project profile
version: "1.0"

detection:
  files: [pyproject.toml, setup.py, requirements.txt]
  extensions: [.py, .pyi]

gates:
  lint:
    command: ruff check .
    detect: pyproject.toml
  test:
    command: pytest
    detect: tests/
  build:
    command: python -m build
    detect: pyproject.toml

conventions:
  naming: snake_case
  # ... language-specific conventions
```

### Gate Structure

All gates use standardized keys:

| Key | Purpose |
|-----|---------|
| `command` | Primary command to run |
| `alternative` | Fallback if primary tool not available |
| `detect` | File/dir that indicates this gate applies |

**Important:** Gate keys were standardized in v0.4.0:
- Java: `maven_command`/`gradle_command` → `command`/`alternative`
- C++: `cmake_command`/`make_command` → `command`/`alternative`
- Shell: `powershell_command` → `alternative`

---

## Model Routing

Models are automatically selected by phase for cost optimization:

| Phase | Model | Rationale |
|-------|-------|-----------|
| INIT | haiku | Fast context loading |
| UNDERSTAND | sonnet | Standard analysis |
| PLAN | sonnet/opus | opus for "architecture"/"security" keywords |
| EXECUTE | sonnet | Code generation |
| VERIFY | sonnet | Quality checks |
| COMMIT | haiku | Simple git operations |
| EVALUATE | haiku | Quick assessment |

**Override triggers:**
- Task contains "security", "auth", "vulnerability" → opus for PLAN and VERIFY
- Task contains "architecture", "refactor" → opus for PLAN

---

## Web Project Detection

Profiles can include `web_indicators` for auto-loading UI/UX rules:

| Indicators | Profile | Auto-loaded Rule |
|------------|---------|-----------------|
| next.config, vite.config, react, vue, svelte | TypeScript Web | ui-ux-design |
| templates/, django, flask, jinja2 | Python Web | ui-ux-design |

---

## Adding a New Profile

1. Create `profiles/{language}.yaml` with required fields
2. Add detection rules (files + extensions)
3. Define gates (lint, test, build minimum)
4. Add conventions section
5. Add `models` and `thinking` sections
6. Run `node profiles/__tests__/test-profiles.js` to validate
