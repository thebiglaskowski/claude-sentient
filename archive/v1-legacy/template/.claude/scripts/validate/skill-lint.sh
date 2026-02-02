#!/bin/bash
#
# Skill Linting Script
# Validates YAML frontmatter in skill files
#
# Usage: ./skill-lint.sh [path]
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Default path
SKILLS_PATH="${1:-.claude/skills}"
ERRORS=0
WARNINGS=0

echo -e "${GREEN}=== Skill Frontmatter Validation ===${NC}"
echo "Path: $SKILLS_PATH"

# Required frontmatter fields
REQUIRED_FIELDS=("name" "description" "version" "triggers" "model" "tags")

# Valid model values
VALID_MODELS=("haiku" "sonnet" "opus")

# Check each skill file
for file in "$SKILLS_PATH"/*.md; do
    if [ ! -f "$file" ]; then
        continue
    fi

    FILENAME=$(basename "$file")
    FILE_ERRORS=0

    # Check for frontmatter delimiters
    if ! head -1 "$file" | grep -q "^---$"; then
        echo -e "${RED}[$FILENAME] Missing frontmatter (no opening ---)${NC}"
        ((ERRORS++))
        continue
    fi

    # Extract frontmatter
    FRONTMATTER=$(sed -n '2,/^---$/p' "$file" | head -n -1)

    if [ -z "$FRONTMATTER" ]; then
        echo -e "${RED}[$FILENAME] Empty or invalid frontmatter${NC}"
        ((ERRORS++))
        continue
    fi

    # Check required fields
    for field in "${REQUIRED_FIELDS[@]}"; do
        if ! echo "$FRONTMATTER" | grep -q "^$field:"; then
            echo -e "${RED}[$FILENAME] Missing required field: $field${NC}"
            ((FILE_ERRORS++))
            ((ERRORS++))
        fi
    done

    # Validate model value
    MODEL_VALUE=$(echo "$FRONTMATTER" | grep "^model:" | cut -d'"' -f2)
    if [ -n "$MODEL_VALUE" ]; then
        VALID_MODEL=false
        for valid in "${VALID_MODELS[@]}"; do
            if [ "$MODEL_VALUE" = "$valid" ]; then
                VALID_MODEL=true
                break
            fi
        done
        if [ "$VALID_MODEL" = false ]; then
            echo -e "${YELLOW}[$FILENAME] Warning: Invalid model '$MODEL_VALUE' (valid: ${VALID_MODELS[*]})${NC}"
            ((WARNINGS++))
        fi
    fi

    # Check version format (should be semver-like)
    VERSION=$(echo "$FRONTMATTER" | grep "^version:" | cut -d'"' -f2)
    if [ -n "$VERSION" ] && ! echo "$VERSION" | grep -qE "^[0-9]+\.[0-9]+\.[0-9]+"; then
        echo -e "${YELLOW}[$FILENAME] Warning: Version '$VERSION' not in semver format${NC}"
        ((WARNINGS++))
    fi

    # Check triggers is an array
    if echo "$FRONTMATTER" | grep -q "^triggers:$"; then
        # Multi-line triggers
        TRIGGER_COUNT=$(echo "$FRONTMATTER" | grep -c "^  - ")
        if [ "$TRIGGER_COUNT" -eq 0 ]; then
            echo -e "${YELLOW}[$FILENAME] Warning: No triggers defined${NC}"
            ((WARNINGS++))
        fi
    elif echo "$FRONTMATTER" | grep -q "^triggers: \[\]"; then
        echo -e "${YELLOW}[$FILENAME] Warning: Empty triggers array${NC}"
        ((WARNINGS++))
    fi

    # Check for context field (optional but should be valid)
    CONTEXT=$(echo "$FRONTMATTER" | grep "^context:" | cut -d'"' -f2)
    if [ -n "$CONTEXT" ] && [ "$CONTEXT" != "inherit" ] && [ "$CONTEXT" != "fork" ]; then
        echo -e "${YELLOW}[$FILENAME] Warning: Invalid context '$CONTEXT' (valid: inherit, fork)${NC}"
        ((WARNINGS++))
    fi

    # Check for boolean fields
    for bool_field in "arguments" "disable_model_invocation" "extended_thinking"; do
        VALUE=$(echo "$FRONTMATTER" | grep "^$bool_field:" | awk '{print $2}')
        if [ -n "$VALUE" ] && [ "$VALUE" != "true" ] && [ "$VALUE" != "false" ]; then
            echo -e "${YELLOW}[$FILENAME] Warning: $bool_field should be boolean, got '$VALUE'${NC}"
            ((WARNINGS++))
        fi
    done

    if [ "$FILE_ERRORS" -eq 0 ]; then
        echo -e "${GREEN}[$FILENAME] OK${NC}"
    fi
done

# Summary
echo -e "\n${GREEN}=== Summary ===${NC}"
echo "Errors: $ERRORS"
echo "Warnings: $WARNINGS"

if [ "$ERRORS" -gt 0 ]; then
    echo -e "\n${RED}Linting FAILED${NC}"
    exit 1
else
    echo -e "\n${GREEN}Linting PASSED${NC}"
    exit 0
fi
