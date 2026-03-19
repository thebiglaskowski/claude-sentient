# Python Environment Detection Matrix

Detailed reference for detecting and activating Python environments during INIT phase.

## Detection Order

Check indicators in this order (first match wins):

| Priority | Indicator File | Environment | Activation |
|----------|---------------|-------------|------------|
| 1 | `environment.yml` | Conda | `conda run -n <env> --no-capture-output <cmd>` |
| 2 | `.venv/pyvenv.cfg` | Virtualenv (local) | `. .venv/bin/activate` or use `.venv/bin/python` |
| 3 | `venv/pyvenv.cfg` | Virtualenv (local) | `. venv/bin/activate` or use `venv/bin/python` |
| 4 | `poetry.lock` | Poetry | `poetry run <cmd>` |
| 5 | `pdm.lock` | PDM | `pdm run <cmd>` |
| 6 | `Pipfile.lock` | Pipenv | `pipenv run <cmd>` |
| 7 | (none) | System Python | Direct invocation |

## Conda Environment Name Extraction

```yaml
# environment.yml
name: myproject    # <-- extract this
dependencies:
  - python=3.11
```

Parse with: look for `name:` line, extract value after colon.

## Verification

After detecting environment, verify it works:

```bash
# Conda
conda run -n <env> --no-capture-output python --version

# Virtualenv
.venv/bin/python --version

# Poetry
poetry run python --version
```

If verification fails, fall back to system Python and report: `[INIT] Environment: <type> detected but activation failed, using system python`

## Windows Differences

- Virtualenv activate: `.venv\Scripts\activate` (not `bin/activate`)
- Conda: same `conda run` command works cross-platform
- Poetry/PDM: same `poetry run`/`pdm run` works cross-platform
