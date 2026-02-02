#!/bin/bash
#
# Test Gate Script
# Verifies test coverage meets requirements
#
# Usage: ./test-gate.sh [options]
# Options:
#   --threshold=N   Coverage threshold (default: 80)
#   --strict        Fail if coverage decreases
#   --report        Generate detailed report
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Defaults
THRESHOLD=80
STRICT=false
GENERATE_REPORT=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --threshold=*)
            THRESHOLD="${1#*=}"
            shift
            ;;
        --strict)
            STRICT=true
            shift
            ;;
        --report)
            GENERATE_REPORT=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 2
            ;;
    esac
done

echo -e "${GREEN}=== Claude Code Test Gate ===${NC}"
echo "Coverage threshold: $THRESHOLD%"
echo "Strict mode: $STRICT"

# Detect test framework
detect_test_framework() {
    if [ -f "package.json" ]; then
        if grep -q "jest" package.json; then
            echo "jest"
        elif grep -q "vitest" package.json; then
            echo "vitest"
        elif grep -q "mocha" package.json; then
            echo "mocha"
        else
            echo "npm"
        fi
    elif [ -f "pyproject.toml" ] || [ -f "requirements.txt" ]; then
        echo "pytest"
    elif [ -f "go.mod" ]; then
        echo "go"
    else
        echo "unknown"
    fi
}

FRAMEWORK=$(detect_test_framework)
echo "Test framework: $FRAMEWORK"

# Run tests with coverage
echo -e "\n${YELLOW}Running tests with coverage...${NC}"

case $FRAMEWORK in
    jest)
        npm test -- --coverage --coverageReporters=json-summary 2>&1 || {
            echo -e "${RED}Tests failed${NC}"
            exit 1
        }
        COVERAGE_FILE="coverage/coverage-summary.json"
        if [ -f "$COVERAGE_FILE" ]; then
            COVERAGE=$(cat "$COVERAGE_FILE" | grep -o '"pct":[0-9.]*' | head -1 | cut -d: -f2)
        fi
        ;;
    vitest)
        npx vitest run --coverage 2>&1 || {
            echo -e "${RED}Tests failed${NC}"
            exit 1
        }
        COVERAGE_FILE="coverage/coverage-summary.json"
        if [ -f "$COVERAGE_FILE" ]; then
            COVERAGE=$(cat "$COVERAGE_FILE" | grep -o '"pct":[0-9.]*' | head -1 | cut -d: -f2)
        fi
        ;;
    pytest)
        pytest --cov --cov-report=json 2>&1 || {
            echo -e "${RED}Tests failed${NC}"
            exit 1
        }
        if [ -f "coverage.json" ]; then
            COVERAGE=$(cat coverage.json | grep -o '"totals":.*"percent_covered":[0-9.]*' | grep -o '[0-9.]*$')
        fi
        ;;
    go)
        go test -coverprofile=coverage.out ./... 2>&1 || {
            echo -e "${RED}Tests failed${NC}"
            exit 1
        }
        COVERAGE=$(go tool cover -func=coverage.out | grep total | awk '{print $3}' | tr -d '%')
        ;;
    *)
        echo -e "${YELLOW}Unknown framework, running npm test${NC}"
        npm test 2>&1 || {
            echo -e "${RED}Tests failed${NC}"
            exit 1
        }
        COVERAGE="unknown"
        ;;
esac

# Parse coverage
echo -e "\n${GREEN}=== Coverage Results ===${NC}"

if [ "$COVERAGE" = "unknown" ] || [ -z "$COVERAGE" ]; then
    echo -e "${YELLOW}Could not determine coverage${NC}"

    if [ "${REQUIRE_COVERAGE:-false}" = "true" ]; then
        echo -e "${RED}Coverage required but not available${NC}"
        exit 1
    fi

    echo "Tests passed (coverage not available)"
    exit 0
fi

# Round coverage to integer for comparison
COVERAGE_INT=$(printf "%.0f" "$COVERAGE")
echo "Current coverage: ${COVERAGE}%"
echo "Required threshold: ${THRESHOLD}%"

# Check threshold
if [ "$COVERAGE_INT" -lt "$THRESHOLD" ]; then
    echo -e "\n${RED}FAILED: Coverage ${COVERAGE}% is below threshold ${THRESHOLD}%${NC}"
    EXIT_CODE=1
else
    echo -e "\n${GREEN}PASSED: Coverage ${COVERAGE}% meets threshold ${THRESHOLD}%${NC}"
    EXIT_CODE=0
fi

# Strict mode: check for decrease
if [ "$STRICT" = true ] && [ -f ".claude/metrics/last-coverage.txt" ]; then
    LAST_COVERAGE=$(cat .claude/metrics/last-coverage.txt)
    if [ "$COVERAGE_INT" -lt "$LAST_COVERAGE" ]; then
        echo -e "\n${RED}FAILED: Coverage decreased from ${LAST_COVERAGE}% to ${COVERAGE}%${NC}"
        EXIT_CODE=1
    fi
fi

# Save current coverage for next run
mkdir -p .claude/metrics
echo "$COVERAGE_INT" > .claude/metrics/last-coverage.txt

# Generate detailed report
if [ "$GENERATE_REPORT" = true ]; then
    echo -e "\n${YELLOW}Generating coverage analysis...${NC}"

    REPORT_PROMPT="Analyze this test coverage report and provide:

1. Areas with low coverage that need tests
2. Critical paths that are untested
3. Recommendations for improving coverage
4. Estimated effort to reach ${THRESHOLD}% threshold

Coverage: ${COVERAGE}%
Threshold: ${THRESHOLD}%"

    if [ -f "$COVERAGE_FILE" ]; then
        REPORT_PROMPT="$REPORT_PROMPT

Coverage data:
$(cat "$COVERAGE_FILE" 2>/dev/null | head -100)"
    fi

    REPORT=$(claude -p "$REPORT_PROMPT" --model haiku 2>&1) || true

    echo -e "\n${GREEN}=== Coverage Analysis ===${NC}\n"
    echo "$REPORT"
fi

# GitHub Actions output
if [ -n "$GITHUB_OUTPUT" ]; then
    echo "coverage=$COVERAGE" >> "$GITHUB_OUTPUT"
    echo "threshold=$THRESHOLD" >> "$GITHUB_OUTPUT"
    echo "coverage_status=$EXIT_CODE" >> "$GITHUB_OUTPUT"
fi

exit $EXIT_CODE
