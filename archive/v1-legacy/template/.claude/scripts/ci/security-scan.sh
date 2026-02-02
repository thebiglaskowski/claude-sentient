#!/bin/bash
#
# Security Scan Script
# Runs Claude Code security analysis
#
# Usage: ./security-scan.sh [path]
# Options:
#   [path]          Specific path to scan (default: entire codebase)
#   --severity=X    Minimum severity to report (S0|S1|S2)
#   --ultrathink    Enable deep analysis mode
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Defaults
SCAN_PATH="."
MIN_SEVERITY="S2"
ULTRATHINK=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --severity=*)
            MIN_SEVERITY="${1#*=}"
            shift
            ;;
        --ultrathink)
            ULTRATHINK=true
            shift
            ;;
        *)
            SCAN_PATH="$1"
            shift
            ;;
    esac
done

# Check requirements
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo -e "${RED}Error: ANTHROPIC_API_KEY not set${NC}"
    exit 2
fi

echo -e "${GREEN}=== Claude Code Security Scan ===${NC}"
echo "Scan path: $SCAN_PATH"
echo "Min severity: $MIN_SEVERITY"
echo "Deep analysis: $ULTRATHINK"

# Build security prompt
if [ "$ULTRATHINK" = true ]; then
    MODEL="opus"
    ANALYSIS_DEPTH="ultrathink"
    SECURITY_PROMPT="Perform a thorough security audit with extended thinking.

Use the SECURITY_AUDIT prompt as a guide.

## Analysis Depth
- OWASP Top 10 comprehensive check
- STRIDE threat modeling
- Attack surface mapping
- Exploitation scenario analysis
- Defense in depth recommendations

## Output Requirements
For each finding:
1. Location (file:line)
2. Vulnerability type
3. Severity (S0/S1/S2)
4. Attack scenario
5. Remediation with code example
6. Verification steps"
else
    MODEL="sonnet"
    ANALYSIS_DEPTH="standard"
    SECURITY_PROMPT="Perform a security audit following the SECURITY_AUDIT prompt.

## Focus Areas
- Injection vulnerabilities (SQL, NoSQL, Command)
- Authentication/Authorization issues
- Cryptographic failures
- Sensitive data exposure
- Input validation gaps

## Output Requirements
List findings by severity:
- S0: Critical (must fix immediately)
- S1: High (fix before merge)
- S2: Medium (fix soon)

Include file:line and remediation for each."
fi

# Get files to scan
echo -e "\n${YELLOW}Identifying files to scan...${NC}"

# Focus on security-sensitive file patterns
SECURITY_PATTERNS="auth|login|password|token|session|crypto|secret|api|route|middleware|validate|sanitize"

if [ "$SCAN_PATH" = "." ]; then
    FILES_TO_SCAN=$(find . -type f \( -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.go" -o -name "*.java" \) \
        -not -path "*/node_modules/*" \
        -not -path "*/.git/*" \
        -not -path "*/dist/*" \
        -not -path "*/build/*" \
        | grep -iE "$SECURITY_PATTERNS" || find . -type f \( -name "*.ts" -o -name "*.js" \) \
        -not -path "*/node_modules/*" \
        -not -path "*/.git/*" \
        | head -100)
else
    FILES_TO_SCAN=$(find "$SCAN_PATH" -type f \( -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.go" \) \
        -not -path "*/node_modules/*")
fi

FILE_COUNT=$(echo "$FILES_TO_SCAN" | wc -l)
echo "Files to scan: $FILE_COUNT"

if [ "$FILE_COUNT" -eq 0 ]; then
    echo -e "${YELLOW}No files found to scan${NC}"
    exit 0
fi

# Create scan prompt
PROMPT_FILE=$(mktemp)
cat > "$PROMPT_FILE" << EOF
$SECURITY_PROMPT

## Scan Path
$SCAN_PATH

## Files to Analyze
$FILES_TO_SCAN

## Minimum Severity
Report issues at $MIN_SEVERITY or higher.

Please analyze the code for security vulnerabilities.
EOF

# Run security scan
echo -e "\n${YELLOW}Running security scan ($ANALYSIS_DEPTH mode)...${NC}"

SCAN_OUTPUT=$(claude -p "$(cat "$PROMPT_FILE")" --model "$MODEL" 2>&1) || {
    echo -e "${RED}Error running security scan${NC}"
    rm "$PROMPT_FILE"
    exit 3
}

rm "$PROMPT_FILE"

# Output results
echo -e "\n${GREEN}=== Security Scan Results ===${NC}\n"
echo "$SCAN_OUTPUT"

# Parse results for CI
S0_COUNT=$(echo "$SCAN_OUTPUT" | grep -c "S0\|Critical" || true)
S1_COUNT=$(echo "$SCAN_OUTPUT" | grep -c "S1\|High" || true)
S2_COUNT=$(echo "$SCAN_OUTPUT" | grep -c "S2\|Medium" || true)

echo -e "\n${GREEN}=== Summary ===${NC}"
echo "Critical (S0): $S0_COUNT"
echo "High (S1): $S1_COUNT"
echo "Medium (S2): $S2_COUNT"

# Determine exit code
if [ "$S0_COUNT" -gt 0 ]; then
    echo -e "\n${RED}FAILED: Critical vulnerabilities found${NC}"
    EXIT_CODE=1
elif [ "$S1_COUNT" -gt 0 ] && [ "${BLOCK_ON_S1:-true}" = "true" ]; then
    echo -e "\n${YELLOW}FAILED: High severity issues found${NC}"
    EXIT_CODE=1
else
    echo -e "\n${GREEN}PASSED: No blocking security issues${NC}"
    EXIT_CODE=0
fi

# GitHub Actions output
if [ -n "$GITHUB_OUTPUT" ]; then
    echo "security_status=$EXIT_CODE" >> "$GITHUB_OUTPUT"
    echo "s0_count=$S0_COUNT" >> "$GITHUB_OUTPUT"
    echo "s1_count=$S1_COUNT" >> "$GITHUB_OUTPUT"
    echo "s2_count=$S2_COUNT" >> "$GITHUB_OUTPUT"
fi

exit $EXIT_CODE
