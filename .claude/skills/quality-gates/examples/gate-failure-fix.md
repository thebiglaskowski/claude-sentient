# Example: Fixing a Lint Gate Failure

## Scenario
Running `/cs-loop "add input validation"` hits a lint failure in VERIFY.

## Gate Output
```
$ ruff check src/
src/forms/signup.py:45:1: I001 Import block is un-sorted or un-formatted
src/forms/signup.py:78:5: E712 Comparison to True should be 'if cond:' not 'if cond == True:'
Found 2 errors.
```

## Auto-Fix Attempt 1
```
ruff check src/ --fix
```
Result: I001 fixed. E712 requires manual fix.

## Manual Fix (Attempt 2)
Read `src/forms/signup.py:78`, change `if is_valid == True:` to `if is_valid:`

## Re-Verify
```
ruff check src/
```
Result: 0 errors. Gate passes.

## Key Lesson
- `ruff --fix` handles import sorting but not all style issues
- Read the specific error before attempting manual fix
- Never suppress with `# noqa`
