---
name: argument-parser
description: Documents skill/command argument support with $ARGUMENTS variables
disable-model-invocation: true
---

# Argument Parser

Support for passing arguments to commands and skills.

## Overview

Commands and skills can accept arguments using special variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `$ARGUMENTS` | Full argument string | `"src/api --deep"` |
| `$0` | Command name | `review` |
| `$1` | First argument | `src/api` |
| `$2` | Second argument | `--deep` |
| `$@` | All arguments as array | `["src/api", "--deep"]` |

---

## Usage Examples

### Positional Arguments

```
/review src/api
```

In the command file:
```markdown
Review the code at: $1
```

Result:
```markdown
Review the code at: src/api
```

### Multiple Arguments

```
/test src/utils --coverage=90
```

Variables:
- `$0` = `test`
- `$1` = `src/utils`
- `$2` = `--coverage=90`
- `$ARGUMENTS` = `src/utils --coverage=90`

### Named Arguments (Flags)

```
/refactor src/auth --type=extract --dry-run
```

Parse named arguments:
```markdown
Path: $1
Type: ${type:-rename}  (default: rename)
Dry run: ${dry_run:-false}
```

---

## Argument Patterns

### Path Arguments
```
/review $1              # Review specific path
/test $1                # Test specific path
/refactor $1            # Refactor specific file
```

### Filter Arguments
```
/debt $1                # Filter debt by category
/secure $1              # Scope security audit
/daily $1               # Focus on specific area
```

### Version Arguments
```
/release $1             # Specify version number
/migrate $1             # Target version
```

### Flag Arguments
```
--deep                  # Enable deep analysis
--dry-run               # Preview only
--coverage=N            # Set threshold
--type=value            # Specify type
--security              # Include security checks
```

---

## Commands with Arguments

### /review [path] [flags]

```
/review                     # Review all changes
/review src/api             # Review specific path
/review src/api --deep      # Deep review
/review --security          # Security-focused review
```

**Supported flags:**
- `--deep` - Extended analysis
- `--security` - Security focus
- `--quick` - Fast review

### /test [path] [flags]

```
/test                       # Run all tests
/test src/utils             # Test specific path
/test --coverage=90         # Set coverage threshold
/test --watch               # Watch mode
```

**Supported flags:**
- `--coverage=N` - Coverage threshold (default: 80)
- `--watch` - Continuous testing
- `--quick` - Skip slow tests

### /refactor [path] [flags]

```
/refactor                   # Interactive refactor selection
/refactor src/utils/old.ts  # Refactor specific file
/refactor --type=rename     # Rename refactoring
/refactor --dry-run         # Preview changes
```

**Supported flags:**
- `--type=rename|extract|inline|move` - Refactoring type
- `--dry-run` - Preview without applying
- `--auto` - Apply automatically

### /fix [description|id]

```
/fix                        # Interactive bug selection
/fix "login timeout"        # Fix described bug
/fix BUG-123                # Fix by ticket ID
```

### /secure [scope] [flags]

```
/secure                     # Full security audit
/secure src/auth            # Audit specific area
/secure --severity=S0       # Only critical issues
/secure --ultrathink        # Deep analysis
```

**Supported flags:**
- `--severity=S0|S1|S2` - Minimum severity
- `--ultrathink` - Extended thinking
- `--quick` - Fast scan

### /daily [focus]

```
/daily                      # General continuation
/daily auth                 # Focus on auth feature
/daily "fix login bug"      # Specific task
```

### /debt [category]

```
/debt                       # All tech debt
/debt testing               # Testing debt only
/debt security              # Security debt only
/debt performance           # Performance debt
```

### /migrate [version]

```
/migrate                    # Interactive migration
/migrate v2.0               # Target specific version
/migrate latest             # Migrate to latest
```

### /release [version]

```
/release                    # Interactive version
/release 1.3.0              # Specific version
/release major              # Major bump
/release minor              # Minor bump
/release patch              # Patch bump
```

### /spike [timebox] [flags]

```
/spike                      # Open-ended research
/spike 2h                   # 2-hour timebox
/spike --focus="caching"    # Focused spike
```

---

## Implementing Arguments in Commands

### Basic Pattern

```markdown
# Command: /example

## Arguments
- `$1` - First argument (required/optional)
- `$2` - Second argument (optional)

## Flags
- `--flag` - Boolean flag
- `--option=value` - Value flag

## Behavior

**If no arguments:**
[Default behavior]

**If $1 provided:**
[Behavior with first argument]

**If --flag present:**
[Modified behavior]
```

### Parsing Logic

```markdown
## Argument Processing

1. Parse `$ARGUMENTS` into positional and named arguments
2. Validate required arguments present
3. Apply defaults for missing optional arguments
4. Execute with resolved values
```

### Error Handling

```markdown
## Invalid Arguments

**Missing required argument:**
> Error: /command requires [argument]
> Usage: /command <path> [--flag]

**Invalid flag value:**
> Error: --coverage must be a number between 0-100
> Got: --coverage=abc
```

---

## Default Values

When arguments are not provided, use sensible defaults:

| Command | Default Scope | Default Behavior |
|---------|---------------|------------------|
| `/review` | Changed files | Standard review |
| `/test` | All tests | 80% coverage |
| `/refactor` | Interactive | Preview first |
| `/secure` | Full codebase | All severities |
| `/debt` | All categories | List all debt |

---

## Best Practices

1. **Always document arguments** in command files
2. **Provide defaults** for optional arguments
3. **Validate early** before executing
4. **Show usage** on argument errors
5. **Support --help** flag for all commands
