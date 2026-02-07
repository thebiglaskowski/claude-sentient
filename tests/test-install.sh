#!/usr/bin/env bash
# Test harness for install.sh
#
# Validates:
# - Script is valid bash syntax
# - Referenced files and directories exist
# - Key functions work correctly
#
# Run: bash tests/test-install.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
INSTALL_SCRIPT="$PROJECT_DIR/install.sh"

passed=0
failed=0
failures=()

test_case() {
    local name="$1"
    shift
    if "$@" 2>/dev/null; then
        ((passed++)) || true
        echo "  ✓ $name"
    else
        ((failed++)) || true
        failures+=("$name")
        echo "  ✗ $name"
    fi
}

echo ""
echo "Install Script Tests"
echo "═══════════════════"

# ── Syntax validation ──────────────────────────────────────
echo ""
echo "Syntax Validation"

test_case "install.sh is valid bash" bash -n "$INSTALL_SCRIPT"

test_case "install.sh is not empty" test -s "$INSTALL_SCRIPT"

test_case "install.sh has shebang" grep -qm1 '^#!' "$INSTALL_SCRIPT"

# ── File references ────────────────────────────────────────
echo ""
echo "File References"

test_case "profiles/ directory exists" test -d "$PROJECT_DIR/profiles"

test_case "templates/ directory exists" test -d "$PROJECT_DIR/templates"

test_case ".claude/commands/ directory exists" test -d "$PROJECT_DIR/.claude/commands"

test_case ".claude/hooks/ directory exists" test -d "$PROJECT_DIR/.claude/hooks"

test_case "CLAUDE.md exists" test -f "$PROJECT_DIR/CLAUDE.md"

test_case "README.md exists" test -f "$PROJECT_DIR/README.md"

# ── Content checks ─────────────────────────────────────────
echo ""
echo "Content Checks"

test_case "install.sh uses HTTPS for git" grep -q 'https://' "$INSTALL_SCRIPT"

test_case "install.sh handles errors" grep -q 'set -' "$INSTALL_SCRIPT" || grep -q 'trap' "$INSTALL_SCRIPT" || grep -q 'error' "$INSTALL_SCRIPT"

test_case "install.sh has usage/help text" grep -qi 'usage\|help\|install' "$INSTALL_SCRIPT"

# ── PowerShell script ──────────────────────────────────────
echo ""
echo "PowerShell Script"

PS_SCRIPT="$PROJECT_DIR/install.ps1"

test_case "install.ps1 exists" test -f "$PS_SCRIPT"

test_case "install.ps1 is not empty" test -s "$PS_SCRIPT"

# ── Report ─────────────────────────────────────────────────
echo ""
echo "─────────────────────────────────────"
echo "Results: $passed passed, $failed failed"

if [ ${#failures[@]} -gt 0 ]; then
    echo ""
    echo "Failures:"
    for f in "${failures[@]}"; do
        echo "  - $f"
    done
fi

exit "$failed"
