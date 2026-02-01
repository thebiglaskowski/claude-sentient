# Terminal UI Rules

## Core Principles

1. **Instant Feedback** — Never leave users waiting without indication
2. **Visual Clarity** — Important info stands out
3. **Graceful Degradation** — Works everywhere, shines in modern terminals
4. **Helpful Errors** — Tell users what went wrong AND how to fix it
5. **Consistent Style** — Same patterns across all commands

---

## Output Standards

### Status Indicators

```
✓ Success (green)
✗ Error (red)
⚠ Warning (yellow)
ℹ Info (blue)
○ Pending (gray)
● Active (cyan)
```

### Progress Feedback

| Duration | Feedback Type |
|----------|---------------|
| < 0.5s | None needed |
| 0.5-3s | Spinner |
| > 3s | Progress bar (if countable) or spinner with status |

### Spinners

```
⠋ ⠙ ⠹ ⠸ ⠼ ⠴ ⠦ ⠧ ⠇ ⠏  (dots)
◐ ◓ ◑ ◒  (circle)
⣾ ⣽ ⣻ ⢿ ⡿ ⣟ ⣯ ⣷  (braille)
```

### Progress Bars

```
[████████████████░░░░░░░░] 67%
Processing... ▓▓▓▓▓▓▓▓░░░░ 67%
```

---

## Color Usage

### Semantic Colors

| Color | Meaning |
|-------|---------|
| Green | Success, complete, positive |
| Red | Error, failure, destructive |
| Yellow | Warning, caution, attention |
| Blue | Info, neutral highlight |
| Cyan | Active, in-progress |
| Magenta | Special, highlight |
| Gray/Dim | Secondary, less important |

### Color Rules

- Use color to convey meaning, not decoration
- Always support NO_COLOR environment variable
- Don't rely on color alone (use symbols too)
- High contrast: bright on dark, or vice versa

---

## Message Formatting

### Success Output

```
✓ Build complete

  Output: dist/bundle.js (245 KB)
  Time: 2.3s
```

### Error Output

```
✗ Error: Configuration file not found

  Expected: ./config.json
  Current directory: /home/user/project

  Hint: Run `init` to create a configuration file
```

### Warning Output

```
⚠ Warning: Deprecated API usage detected

  Found in: src/api/legacy.js:45
  Will be removed in: v3.0.0

  Migration guide: https://docs.example.com/migrate
```

### Info Output

```
ℹ Using default configuration

  Config file: none found
  Defaults applied: timeout=30s, retries=3
```

---

## Tables

### When to Use

- Comparing multiple items
- Displaying structured data
- Showing status of multiple operations

### Format

```
┌──────────┬──────────┬────────┐
│ Name     │ Status   │ Time   │
├──────────┼──────────┼────────┤
│ Build    │ ✓ Pass   │ 2.3s   │
│ Test     │ ✓ Pass   │ 5.1s   │
│ Deploy   │ ○ Pending│ -      │
└──────────┴──────────┴────────┘
```

Or simpler:

```
Name       Status      Time
────       ──────      ────
Build      ✓ Pass      2.3s
Test       ✓ Pass      5.1s
Deploy     ○ Pending   -
```

---

## Interactive Prompts

### Confirmation

```
? Delete all files in /tmp? (y/N)
```

### Selection

```
? Select environment:
  ○ Development
  ● Production (selected)
  ○ Staging
```

### Text Input

```
? Enter project name: my-project
```

### Multi-select

```
? Select features to enable:
  ◉ Authentication
  ◯ Analytics
  ◉ Notifications
  ◯ Dark mode
```

---

## Boxed Messages

### Important Notices

```
╭──────────────────────────────────────╮
│                                      │
│  ⚠ Breaking changes in v2.0         │
│                                      │
│  Please review the migration guide   │
│  before upgrading.                   │
│                                      │
╰──────────────────────────────────────╯
```

### Success Summary

```
┌─────────────────────────────────────┐
│         Build Successful ✓          │
├─────────────────────────────────────┤
│  Files:    42 compiled              │
│  Size:     1.2 MB                   │
│  Time:     3.4s                     │
│                                     │
│  Output:   dist/                    │
└─────────────────────────────────────┘
```

---

## Error Handling

### Good Error Message Structure

1. **What** went wrong (clear statement)
2. **Where** it happened (file, line, command)
3. **Why** it might have happened (if known)
4. **How** to fix it (actionable suggestion)

### Example

```
✗ Error: Cannot connect to database

  Host: localhost:5432
  Database: myapp_dev

  Possible causes:
  • PostgreSQL is not running
  • Wrong credentials in .env
  • Port 5432 is blocked

  Try:
  • Start PostgreSQL: brew services start postgresql
  • Check .env file: DATABASE_URL=...
```

---

## Summary Statistics

### End of Command

```
───────────────────────────────────────
Summary

  ✓ 12 files processed
  ✓ 3 files created
  ⚠ 1 warning
  ✗ 0 errors

  Completed in 2.3s
───────────────────────────────────────
```

---

## Environment Compatibility

### Required Support

- NO_COLOR environment variable
- TERM=dumb (no formatting)
- Piped output (no TTY)
- CI environments

### Detection Pattern

```javascript
const isInteractive = process.stdout.isTTY && !process.env.CI;
const supportsColor = !process.env.NO_COLOR && isInteractive;
```

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Misuse/invalid arguments |
| 126 | Permission denied |
| 127 | Command not found |
| 130 | Interrupted (Ctrl+C) |

---

## Anti-Patterns

### Avoid

- Silent long-running operations
- Unformatted error dumps
- Cryptic error messages
- No confirmation for destructive actions
- Inconsistent output format
- Missing exit codes
- Ignoring NO_COLOR

### Prefer

- Progress feedback for anything >0.5s
- Structured, helpful errors
- Clear suggestions for fixes
- Confirmation prompts for danger
- Consistent formatting throughout
- Meaningful exit codes
- Respecting color preferences
