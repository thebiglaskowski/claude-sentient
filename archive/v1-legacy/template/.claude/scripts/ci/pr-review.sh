#!/bin/bash
#
# PR Review Script
# Runs Claude Code review on pull request changes
#
# Usage: ./pr-review.sh [options]
# Options:
#   --deep      Enable deep analysis
#   --security  Include security checks
#   --quick     Fast review mode
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default settings
REVIEW_LEVEL="standard"
INCLUDE_SECURITY=false
MAX_FILES=50

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --deep)
            REVIEW_LEVEL="deep"
            shift
            ;;
        --quick)
            REVIEW_LEVEL="quick"
            shift
            ;;
        --security)
            INCLUDE_SECURITY=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 2
            ;;
    esac
done

# Check requirements
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo -e "${RED}Error: ANTHROPIC_API_KEY not set${NC}"
    exit 2
fi

if ! command -v claude &> /dev/null; then
    echo -e "${RED}Error: claude CLI not found${NC}"
    echo "Install with: npm install -g @anthropic/claude-code"
    exit 2
fi

echo -e "${GREEN}=== Claude Code PR Review ===${NC}"
echo "Review level: $REVIEW_LEVEL"
echo "Include security: $INCLUDE_SECURITY"

# Get changed files
echo -e "\n${YELLOW}Analyzing changed files...${NC}"

if [ -n "$GITHUB_BASE_REF" ]; then
    # GitHub Actions context
    BASE_BRANCH="origin/$GITHUB_BASE_REF"
elif [ -n "$CI_MERGE_REQUEST_TARGET_BRANCH_NAME" ]; then
    # GitLab CI context
    BASE_BRANCH="origin/$CI_MERGE_REQUEST_TARGET_BRANCH_NAME"
else
    # Local or fallback
    BASE_BRANCH="origin/main"
fi

CHANGED_FILES=$(git diff --name-only "$BASE_BRANCH"...HEAD 2>/dev/null || git diff --name-only HEAD~1)
FILE_COUNT=$(echo "$CHANGED_FILES" | wc -l)

echo "Files changed: $FILE_COUNT"

if [ "$FILE_COUNT" -gt "$MAX_FILES" ]; then
    echo -e "${YELLOW}Warning: Large PR ($FILE_COUNT files). Consider splitting.${NC}"
fi

# Build review prompt based on level
case $REVIEW_LEVEL in
    quick)
        REVIEW_PROMPT="Quick code review of these changes. Focus only on:
- Obvious bugs
- Security issues (S0/S1 only)
- Breaking changes

Be concise. Skip style suggestions."
        MODEL="haiku"
        ;;
    deep)
        REVIEW_PROMPT="Deep code review following the CODE_REVIEW prompt.

For each file, analyze:
1. Logic and correctness
2. Security implications
3. Test coverage
4. Error handling
5. Performance
6. Maintainability

Provide detailed findings with line numbers."
        MODEL="opus"
        ;;
    *)
        REVIEW_PROMPT="Code review following the CODE_REVIEW prompt.

Review for:
- Bugs and logic errors
- Security issues
- Missing tests
- Error handling
- Code quality

Categorize findings by severity (S0-S3)."
        MODEL="sonnet"
        ;;
esac

if [ "$INCLUDE_SECURITY" = true ]; then
    REVIEW_PROMPT="$REVIEW_PROMPT

Additionally, perform security analysis:
- Check OWASP Top 10
- Look for injection vulnerabilities
- Verify authentication/authorization
- Check for secrets in code"
fi

# Get diff for review
DIFF=$(git diff "$BASE_BRANCH"...HEAD 2>/dev/null || git diff HEAD~1)

# Create temp file for prompt
PROMPT_FILE=$(mktemp)
cat > "$PROMPT_FILE" << EOF
$REVIEW_PROMPT

## Changed Files
$CHANGED_FILES

## Diff
\`\`\`diff
$DIFF
\`\`\`
EOF

# Run Claude review
echo -e "\n${YELLOW}Running Claude review...${NC}"

REVIEW_OUTPUT=$(claude -p "$(cat "$PROMPT_FILE")" --model "$MODEL" 2>&1) || {
    echo -e "${RED}Error running Claude review${NC}"
    rm "$PROMPT_FILE"
    exit 3
}

rm "$PROMPT_FILE"

# Output results
echo -e "\n${GREEN}=== Review Results ===${NC}\n"
echo "$REVIEW_OUTPUT"

# Check for blocking issues
if echo "$REVIEW_OUTPUT" | grep -qE "S0|Critical|CRITICAL"; then
    echo -e "\n${RED}=== BLOCKING: Critical issues found (S0) ===${NC}"
    EXIT_CODE=1
elif echo "$REVIEW_OUTPUT" | grep -qE "S1|High|HIGH"; then
    echo -e "\n${YELLOW}=== WARNING: High severity issues found (S1) ===${NC}"
    # Check config for whether S1 blocks
    if [ "${BLOCK_ON_S1:-true}" = "true" ]; then
        EXIT_CODE=1
    else
        EXIT_CODE=0
    fi
else
    echo -e "\n${GREEN}=== Review complete: No blocking issues ===${NC}"
    EXIT_CODE=0
fi

# Output for CI systems
if [ -n "$GITHUB_OUTPUT" ]; then
    echo "review_status=$EXIT_CODE" >> "$GITHUB_OUTPUT"
    echo "has_blocking_issues=$( [ $EXIT_CODE -eq 0 ] && echo 'false' || echo 'true' )" >> "$GITHUB_OUTPUT"
fi

exit $EXIT_CODE
