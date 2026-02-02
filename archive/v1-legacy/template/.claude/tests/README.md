# Claude Conductor Component Tests

Comprehensive test suite for validating all Claude Conductor prompt components.

## Overview

This test suite validates the structure, content, and quality of all component types:

| Component | Files | Validation |
|-----------|-------|------------|
| Commands | 37 | Frontmatter, XML sections, model values |
| Skills | 61 | Frontmatter, triggers, content depth |
| Agents | 15 | Frontmatter, tools, sections |
| Patterns | 7 | Sections, code examples, languages |
| Snippets | 5 | Sections, code blocks |
| Rules | 13 | Sections, content depth |

## Quick Start

```bash
# Install dependencies
pip install pytest pyyaml

# Run all tests
cd template/.claude/tests
pytest -v

# Run specific component tests
pytest test_commands.py -v
pytest test_skills.py -v

# Run with short output
pytest --tb=short
```

## Test Structure

```
tests/
├── conftest.py                 # pytest config and fixtures
├── validators/                 # Core validation logic
│   ├── base.py                 # BaseValidator, Severity, ValidationResult
│   ├── frontmatter.py          # YAML frontmatter parsing
│   ├── markdown.py             # Markdown section extraction
│   ├── code_blocks.py          # Code syntax validation
│   └── cross_reference.py      # Reference resolution
├── schemas/                    # Component schemas
│   ├── command_schema.py       # Command validation rules
│   ├── skill_schema.py         # Skill validation rules
│   ├── agent_schema.py         # Agent validation rules
│   ├── pattern_schema.py       # Pattern validation rules
│   ├── snippet_schema.py       # Snippet validation rules
│   └── rule_schema.py          # Rule validation rules
├── test_commands.py            # Command file tests
├── test_skills.py              # Skill file tests
├── test_agents.py              # Agent file tests
├── test_patterns.py            # Pattern file tests
├── test_snippets.py            # Snippet file tests
├── test_rules.py               # Rule file tests
├── test_cross_references.py    # Cross-reference validation
├── test_consistency.py         # Project-wide consistency
├── test_quality.py             # Content quality checks
└── README.md                   # This file
```

## Validation Categories

### 1. Structure Tests

Validates component file structure:

- **Commands**: Frontmatter (name, description, model), XML sections (context, role, task, instructions, output_format, rules)
- **Skills**: Frontmatter (name, description), optional fields (triggers, model, tags)
- **Agents**: Frontmatter (name, description, tools, disallowedTools, model), sections (Expertise, Process, Output Format, Checklist)
- **Patterns**: Sections (Intent, When to Use, When NOT to Use), code examples
- **Snippets**: Sections (Description, When to Use, Code), code blocks
- **Rules**: Sections (Core Principles), content depth

### 2. Cross-Reference Tests

Validates that references between components resolve:

- `@rules/[name]` → Rules directory
- `@patterns/[name]` → Patterns directory
- `snippet:[name]` → Snippets directory
- Agent names → Agents directory

### 3. Code Syntax Tests

Validates code blocks for syntax errors:

- Python: `ast.parse()` validation
- JavaScript/TypeScript: Balanced braces check
- SQL: Keyword recognition
- JSON/YAML: Parse validation

### 4. Consistency Tests

Validates project-wide consistency:

- No duplicate command/agent/skill names
- Index files exist for all component directories
- Consistent severity level usage (S0-S3)

### 5. Quality Tests

Validates content quality:

- No TODO/FIXME markers
- No placeholder text
- No absolute file paths
- Valid UTF-8 encoding
- No empty files

## Severity Levels

The test suite uses consistent severity levels aligned with Claude Conductor:

| Level | Code | Meaning | Blocks Tests |
|-------|------|---------|--------------|
| S0 | `S0_CRITICAL` | Blocker, prevents component from working | Yes |
| S1 | `S1_HIGH` | Major issue, should fix before use | Yes |
| S2 | `S2_MEDIUM` | Degraded but functional | No |
| S3 | `S3_LOW` | Minor issue, polish | No |

Tests fail only on S0 and S1 findings. S2 and S3 are warnings.

## Running Individual Tests

```bash
# Test a specific component type
pytest test_commands.py -v

# Test a specific file
pytest test_commands.py::TestCommandStructure::test_command_is_valid[review] -v

# Test cross-references only
pytest test_cross_references.py -v

# Test quality checks only
pytest test_quality.py -v
```

## Filtering Tests

```bash
# Run only tests matching a keyword
pytest -k "frontmatter" -v

# Run only tests in a specific class
pytest test_commands.py::TestCommandContent -v

# Skip slow tests (if any are marked)
pytest -m "not slow" -v
```

## Verbose Output

```bash
# Show all output including passed tests
pytest -v

# Show even more detail
pytest -vv

# Show local variables in tracebacks
pytest --tb=long

# Show only first failure
pytest -x
```

## Adding New Tests

### For a New Component Type

1. Create schema in `schemas/[component]_schema.py`
2. Create test file `test_[component]s.py`
3. Add parameterization in `conftest.py`

### For New Validations

1. Add validator in `validators/`
2. Update relevant schema
3. Add test assertions

## Common Issues

### Import Errors

Make sure you're running from the tests directory:

```bash
cd template/.claude/tests
pytest -v
```

### Missing pyyaml

```bash
pip install pyyaml
```

### File Not Found

Check that the component directories exist and have files:

```bash
ls ../commands/
ls ../skills/
ls ../agents/
```

## Integration with CI

Add to your GitHub Actions workflow:

```yaml
name: Validate Components

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install pytest pyyaml

      - name: Run component tests
        run: |
          cd template/.claude/tests
          pytest -v --tb=short
```

## Contributing

When adding new component types or validation rules:

1. Follow existing patterns in validators/schemas
2. Add comprehensive test coverage
3. Document severity levels appropriately
4. Update this README

## Related Documentation

- [CLAUDE.md](../CLAUDE.md) - Main project configuration
- [Commands Index](../commands/) - All command definitions
- [Skills Index](../skills/_index.md) - All skill definitions
- [Agents Index](../agents/_index.md) - All agent definitions
- [Rules Index](../rules/_index.md) - All rule definitions
