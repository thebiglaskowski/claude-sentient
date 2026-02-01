---
name: dependency-checker
description: Verify required tools are installed before running commands
model: haiku
---

# Dependency Checker

Verify required tools are installed before running commands.

## Description

Use at session start or before commands that require external tools.
Triggers on: "check dependencies", "verify setup", "initialize", "session start".

## Required Tools by Context

### Universal (Always Check)
```bash
git --version      # Version control
```

### Node.js Projects
```bash
node --version     # Runtime
npm --version      # Package manager (or yarn/pnpm)
```

### Python Projects
```bash
python --version   # Runtime (or python3)
pip --version      # Package manager
```

### Go Projects
```bash
go version         # Runtime
```

### Rust Projects
```bash
cargo --version    # Build tool
rustc --version    # Compiler
```

### Optional Tools
```bash
gh --version       # GitHub CLI (for PR operations)
docker --version   # Container operations
npx --version      # For skills.sh integration
```

## Check Process

### Step 1: Detect Project Type

```bash
# Check for project indicators
ls package.json pyproject.toml requirements.txt go.mod Cargo.toml 2>/dev/null
```

### Step 2: Verify Required Tools

Based on detected project type, check each required tool:

```bash
# Example check pattern
command -v git >/dev/null 2>&1 || echo "MISSING: git"
command -v node >/dev/null 2>&1 || echo "MISSING: node"
```

### Step 3: Report Results

```markdown
## Dependency Check

**Project Type:** Node.js + TypeScript

### Required Tools
| Tool | Status | Version |
|------|--------|---------|
| git | ✅ | 2.40.0 |
| node | ✅ | 20.10.0 |
| npm | ✅ | 10.2.0 |

### Optional Tools
| Tool | Status | Used For |
|------|--------|----------|
| gh | ✅ | PR operations |
| npx | ✅ | Skills.sh |
| docker | ❌ | Container ops |

### Missing Required Tools
None - ready to proceed!

### Missing Optional Tools
- `docker` - Install if you need container operations
```

## Failure Behavior

If required tools are missing:

1. **List all missing tools** with install instructions
2. **Provide platform-specific commands:**
   ```markdown
   ### Install Missing Tools

   **git** (required):
   - Windows: `winget install Git.Git`
   - macOS: `brew install git`
   - Linux: `sudo apt install git`

   **node** (required):
   - All platforms: https://nodejs.org or use nvm
   ```
3. **Do not proceed** with operations that require missing tools
4. **Suggest alternatives** if available

## Integration Points

### Session Start Hook
Check dependencies automatically at session start:
```json
{
  "SessionStart": [{
    "hooks": [{
      "type": "command",
      "command": "command -v git >/dev/null || echo '[WARN] git not found'"
    }]
  }]
}
```

### Before Commands
Commands that need specific tools should verify first:
- `/release` → needs `git`, `gh` (optional)
- `/scout-skills` → needs `npx`
- `/test` → needs test runner for project type

## Quick Check Script

```bash
#!/bin/bash
echo "=== Dependency Check ==="

# Universal
check() { command -v $1 >/dev/null 2>&1 && echo "✅ $1: $($1 --version 2>&1 | head -1)" || echo "❌ $1: NOT FOUND"; }

check git

# Detect and check project-specific
[ -f package.json ] && { check node; check npm; }
[ -f requirements.txt ] || [ -f pyproject.toml ] && { check python; check pip; }
[ -f go.mod ] && check go
[ -f Cargo.toml ] && { check cargo; check rustc; }

# Optional
echo "--- Optional ---"
check gh
check docker
check npx
```

## Platform Detection

```bash
# Detect OS for install instructions
case "$(uname -s)" in
  Darwin*) OS="macOS" ;;
  Linux*)  OS="Linux" ;;
  MINGW*|CYGWIN*|MSYS*) OS="Windows" ;;
  *) OS="Unknown" ;;
esac
```
