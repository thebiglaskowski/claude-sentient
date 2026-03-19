# Error Classification & Fix Strategies

Detailed mapping from error types to fix strategies for the auto-fix sub-loop.

## Classification Decision Tree

```
Gate output received
├── Contains "import" + ("sort" | "order" | "unused") → Import Error
├── Contains "type" + ("error" | "mismatch" | "incompatible") → Type Error
├── Contains "indent" | "whitespace" | "trailing" → Format Error
├── Contains "undefined" | "not defined" | "undeclared" → Reference Error
├── Contains "FAILED" | "AssertionError" | "expected" → Test Failure
├── Contains "cannot find module" | "not found" → Build/Import Error
├── Contains "syntax error" | "unexpected token" → Syntax Error
└── Other → Unknown (attempt WebSearch)
```

## Fix Strategy Details

### Import Errors
- **Auto-fix**: Run `fix_command` from profile (e.g., `ruff check . --fix --select I`)
- **Manual**: Read the file, reorder imports per project convention
- **Common trap**: Don't just remove unused imports — check if they're needed for side effects

### Type Errors
- **Auto-fix**: None (type errors require manual reasoning)
- **Manual**: Read file at error line, understand expected vs actual type, fix annotation or logic
- **Common trap**: Don't add `# type: ignore` or `as any` — fix the actual type

### Test Failures
- **CRITICAL**: Never modify test assertions or expected values
- **Manual**: Read failing test to understand expected behavior, then read source under test, fix the source logic
- **Escalation**: If the test itself is wrong (testing outdated behavior), report to user — don't "fix" the test

### Build Errors
- **Manual**: Read compiler output, identify missing dependency or syntax issue
- **Common trap**: Don't add dependencies without checking if they're already available under a different import path

## Error Count Tracking

Track error count after each fix attempt:

```
Attempt 1: 5 errors → fix applied → re-run → 3 errors (improving, continue)
Attempt 2: 3 errors → fix applied → re-run → 4 errors (REGRESSION — revert)
```

If error count increases: revert the last fix immediately and try a different strategy.
