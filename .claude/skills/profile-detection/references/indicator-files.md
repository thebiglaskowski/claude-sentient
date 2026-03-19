# Project Type Indicator Files

Mapping from indicator files to detected profile. Used during INIT phase when `session_start.json` is missing or stale.

## Profile Detection Matrix

| Profile | Primary Indicators | Secondary Indicators |
|---------|-------------------|---------------------|
| Python | `pyproject.toml`, `setup.py`, `requirements.txt` | `*.py`, `Pipfile`, `environment.yml` |
| TypeScript | `tsconfig.json` | `*.ts`, `*.tsx`, `package.json` (with TS deps) |
| Go | `go.mod` | `*.go`, `go.sum` |
| Rust | `Cargo.toml` | `*.rs`, `Cargo.lock` |
| Java | `pom.xml`, `build.gradle`, `build.gradle.kts` | `*.java`, `.mvn/` |
| C/C++ | `CMakeLists.txt`, `Makefile` | `*.c`, `*.cpp`, `*.h`, `*.hpp` |
| Ruby | `Gemfile` | `*.rb`, `Rakefile`, `.ruby-version` |
| Shell | (no primary — fallback when `*.sh` or `*.ps1` dominate) | `*.sh`, `*.bash`, `*.ps1` |
| General | (fallback when no other profile matches) | — |

## Web Project Sub-Detection

After primary profile detection, check for web framework indicators:

| Framework Indicator | Profile Modifier | Rules Auto-loaded |
|--------------------|-----------------|-------------------|
| `next.config.*` | TypeScript Web | ui-ux-design |
| `vite.config.*` | TypeScript Web | ui-ux-design |
| `package.json` with `react`/`vue`/`svelte` dep | TypeScript Web | ui-ux-design |
| `templates/` + `django`/`flask` in deps | Python Web | ui-ux-design |

## Detection Priority

When multiple indicators exist (e.g., `pyproject.toml` AND `tsconfig.json`):
1. Check `session_start.json` first — user may have set profile explicitly
2. Use the profile whose indicator appears at project root (not in subdirectory)
3. If ambiguous, prefer the profile with more indicator matches
4. Report: `[INIT] Multiple profiles detected: python, typescript. Using: python`
