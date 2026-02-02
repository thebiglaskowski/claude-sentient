#!/bin/bash
#
# Prompt Validation Script
# Checks prompt files for required structure and content
#
# Usage: ./prompt-check.sh [path]
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Default path
PROMPTS_PATH="${1:-.claude/commands}"
ERRORS=0
WARNINGS=0

echo -e "${GREEN}=== Prompt Structure Validation ===${NC}"
echo "Path: $PROMPTS_PATH"

# Required sections for command prompts
REQUIRED_SECTIONS=("Description" "Trigger" "Process\|Steps\|Checklist")

# Check each markdown file
for file in "$PROMPTS_PATH"/*.md; do
    if [ ! -f "$file" ]; then
        continue
    fi

    FILENAME=$(basename "$file")
    FILE_ERRORS=0

    # Check for required sections
    for section in "${REQUIRED_SECTIONS[@]}"; do
        if ! grep -qE "^#+ .*($section)" "$file"; then
            echo -e "${RED}[$FILENAME] Missing section: $section${NC}"
            ((FILE_ERRORS++))
            ((ERRORS++))
        fi
    done

    # Check for title (H1)
    if ! grep -q "^# " "$file"; then
        echo -e "${YELLOW}[$FILENAME] Warning: No H1 title found${NC}"
        ((WARNINGS++))
    fi

    # Check for empty file
    if [ ! -s "$file" ]; then
        echo -e "${RED}[$FILENAME] Error: File is empty${NC}"
        ((ERRORS++))
    fi

    # Check for very short content
    LINE_COUNT=$(wc -l < "$file")
    if [ "$LINE_COUNT" -lt 10 ]; then
        echo -e "${YELLOW}[$FILENAME] Warning: Very short content ($LINE_COUNT lines)${NC}"
        ((WARNINGS++))
    fi

    # Check for broken links (basic)
    if grep -oE '\[.*\]\(.*\)' "$file" | grep -q '()'; then
        echo -e "${YELLOW}[$FILENAME] Warning: Possibly broken links${NC}"
        ((WARNINGS++))
    fi

    if [ "$FILE_ERRORS" -eq 0 ]; then
        echo -e "${GREEN}[$FILENAME] OK${NC}"
    fi
done

# Summary
echo -e "\n${GREEN}=== Summary ===${NC}"
echo "Errors: $ERRORS"
echo "Warnings: $WARNINGS"

if [ "$ERRORS" -gt 0 ]; then
    echo -e "\n${RED}Validation FAILED${NC}"
    exit 1
else
    echo -e "\n${GREEN}Validation PASSED${NC}"
    exit 0
fi
