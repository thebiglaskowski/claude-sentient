#!/bin/bash
# Post-Edit Hook
#
# Run formatting and linting after file edits.
# Automatically fixes common issues without user intervention.
#
# Hook Type: PostToolUse (matcher: tool in ["Write", "Edit"])
# Input: JSON with tool_input containing file_path
# Output: Formatting/lint status

# Read input from stdin
INPUT=$(cat)

# Extract file path from JSON input
FILE_PATH=$(echo "$INPUT" | grep -o '"file_path"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)

if [ -z "$FILE_PATH" ]; then
    # Try alternate key names
    FILE_PATH=$(echo "$INPUT" | grep -o '"path"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)
fi

if [ -z "$FILE_PATH" ] || [ ! -f "$FILE_PATH" ]; then
    exit 0  # No file to process
fi

# Get file extension
EXT="${FILE_PATH##*.}"

# Track if we made changes
formatted=false

case "$EXT" in
    js|jsx|ts|tsx|json|md|yaml|yml|css|scss|html)
        # Try Prettier
        if command -v npx &> /dev/null && [ -f "node_modules/.bin/prettier" ]; then
            npx prettier --write "$FILE_PATH" 2>/dev/null && formatted=true
        fi
        ;;
    py)
        # Try Black or Ruff
        if command -v ruff &> /dev/null; then
            ruff format "$FILE_PATH" 2>/dev/null && formatted=true
        elif command -v black &> /dev/null; then
            black -q "$FILE_PATH" 2>/dev/null && formatted=true
        fi
        ;;
    rs)
        # Try rustfmt
        if command -v rustfmt &> /dev/null; then
            rustfmt "$FILE_PATH" 2>/dev/null && formatted=true
        fi
        ;;
    go)
        # Try gofmt
        if command -v gofmt &> /dev/null; then
            gofmt -w "$FILE_PATH" 2>/dev/null && formatted=true
        fi
        ;;
    sh|bash)
        # Try shfmt
        if command -v shfmt &> /dev/null; then
            shfmt -w "$FILE_PATH" 2>/dev/null && formatted=true
        fi
        ;;
esac

if [ "$formatted" = true ]; then
    echo "[Post-Edit] Formatted: $FILE_PATH" >&2
fi

# Run quick lint check (non-blocking)
case "$EXT" in
    js|jsx|ts|tsx)
        if command -v npx &> /dev/null && [ -f "node_modules/.bin/eslint" ]; then
            errors=$(npx eslint "$FILE_PATH" --format compact 2>/dev/null | grep -c "Error" || echo "0")
            if [ "$errors" != "0" ]; then
                echo "[Post-Edit] ⚠ $errors lint errors in $FILE_PATH" >&2
            fi
        fi
        ;;
    py)
        if command -v ruff &> /dev/null; then
            errors=$(ruff check "$FILE_PATH" 2>/dev/null | wc -l || echo "0")
            if [ "$errors" != "0" ]; then
                echo "[Post-Edit] ⚠ $errors lint issues in $FILE_PATH" >&2
            fi
        fi
        ;;
esac

exit 0
