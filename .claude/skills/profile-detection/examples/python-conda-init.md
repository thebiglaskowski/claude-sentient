# Example: Python Conda Environment Detection

## Scenario
Project has `environment.yml` with `name: ml-pipeline` and `pyproject.toml`.

## Detection Flow
1. session-start.cjs detects `pyproject.toml` -> profile: `python`
2. profile-detection skill checks for Python environment:
   - `environment.yml` found -> extract `name: ml-pipeline`
   - Set prefix: `conda run -n ml-pipeline --no-capture-output`
3. All gate commands prepended with conda prefix

## Report
```
[INIT] Profile: python, Tools: ruff, pytest
[INIT] Environment: conda (ml-pipeline)
[INIT] Rules loaded: code-quality, testing
```

## Gotcha
If `conda run` fails with "environment not found", the env may need creation:
```
conda env create -f environment.yml
```
