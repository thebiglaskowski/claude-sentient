# Per-Profile Gate Commands

Quick reference for gate commands across all profiles. Read from `.claude-sentient/profiles/{name}.yaml` at runtime.

## Gate Command Matrix

| Profile | Lint | Lint Fix | Test | Build |
|---------|------|----------|------|-------|
| Python | `ruff check .` | `ruff check . --fix` | `pytest` | `python -m build` |
| TypeScript | `npx eslint .` | `npx eslint . --fix` | `npx vitest run` | `npm run build` |
| Go | `golangci-lint run` | `golangci-lint run --fix` | `go test ./...` | `go build ./...` |
| Rust | `cargo clippy` | `cargo clippy --fix` | `cargo test` | `cargo build` |
| Java | `mvn checkstyle:check` | — | `mvn test` | `mvn compile` |
| C/C++ | `clang-tidy` | `clang-tidy --fix` | `ctest` | `cmake --build .` |
| Ruby | `rubocop` | `rubocop -A` | `rspec` | — |
| Shell | `shellcheck **/*.sh` | — | — | — |
| General | (auto-detect) | — | (auto-detect) | — |

## Alternative Commands

Some profiles define `alternative` commands as fallbacks:

| Profile | Gate | Alternative |
|---------|------|------------|
| TypeScript | lint | `npx biome lint .` |
| TypeScript | test | `npx jest` |
| Python | type | `mypy .` |
| Go | lint | `go vet ./...` |

## Type Checking (Advisory)

| Profile | Command |
|---------|---------|
| Python | `pyright` |
| TypeScript | `npx tsc --noEmit` |

## Environment Prefix

For Python projects with detected environments, prepend the activation prefix to all gate commands:
- Conda: `conda run -n <env> --no-capture-output ruff check .`
- Poetry: `poetry run pytest`
- PDM: `pdm run ruff check .`
