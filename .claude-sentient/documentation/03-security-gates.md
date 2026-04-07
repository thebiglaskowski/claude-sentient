---
feature: Security Gates
version: "1.0"
last_updated: 2026-03-04
dependencies: []
routes: []
status: draft
---

# Security Gates

> Two PreToolUse hooks intercept Bash and file Write/Edit/Create commands before they execute, blocking dangerous operations and protected paths. Both run synchronously; both use `hookSpecificOutput.permissionDecision` format.

## Hook Overview

| Hook | Event | Tools Intercepted | Sync |
|------|-------|-------------------|------|
| `bash-validator.cjs` | PreToolUse/Bash | All Bash commands | sync |
| `file-validator.cjs` | PreToolUse/Write, Edit, Create | All file writes | sync |

## Output Format (v2.0.0+)

Both hooks use the current `hookSpecificOutput` schema:

```json
{
  "hookSpecificOutput": {
    "permissionDecision": "allow" | "deny",
    "permissionDecisionReason": "optional explanation"
  }
}
```

Old `{ decision, reason }` top-level fields are deprecated (removed in Claude Code v2.0.0).

---

## bash-validator.cjs

### Dangerous Patterns (DENY)

| Category | Pattern | Example |
|----------|---------|---------|
| Recursive deletion | `rm -rf` with any path | `rm -rf /`, `rm -rf --` |
| Disk overwrite | Write to `/dev/sd*`, `/dev/hd*` | `> /dev/sda` |
| Filesystem format | `mkfs` | `mkfs.ext4` |
| Fork bomb | `:(){ :|:& };:` | any variant |
| Pipe-to-interpreter | `curl \| sh`, `wget \| bash` | download-then-execute |
| Base64 decode + execute | `base64 -d \| sh` | `echo <b64> \| base64 -d \| bash` |
| Eval with shell substitution | `eval $(...)`, `eval \`...\`` | command injection |
| Sudo shell escalation | `sudo bash`, `sudo sh`, `sudo su` | privilege escalation |
| Find + xargs delete | `find ... \| xargs rm` | mass deletion |
| Python/Node/Perl/Ruby one-liners | interpreter with eval/exec | code injection |
| Download-then-execute chains | `curl ... -o ... && chmod +x ... && ./...` | — |

### Oversized Input Block

Commands with input exceeding a size threshold (TODO: confirm exact byte limit from source) are blocked to prevent command injection through oversized payloads.

### Allow + Warnings

Safe commands pass through. If any advisory pattern is detected (e.g., use of `sudo` for non-shell commands), a warning is attached to the response.

### eval Pattern

`/(^|[|;&{(=]\s*)eval\b/` — only matches `eval` as a shell command (start of command or after a separator character). `node --eval`, `git commit -m "...eval..."` are allowed.

### normalizeCommand()

Strips `$(...)` wrapping, backticks, and `${}` substitutions before pattern matching. This prevents bypass via command substitution wrapping.

---

## file-validator.cjs

### Protected Paths (DENY)

Writes to any path matching these prefixes/patterns are blocked:

| Category | Pattern |
|----------|---------|
| System directories | `/etc/`, `/usr/`, `/bin/`, `/sbin/` |
| Windows system | `C:\Windows`, `C:\System32` |
| SSH/GPG keys | `.ssh/`, `.gnupg/` |
| Cloud credentials | `.aws/credentials`, `.kube/config`, `.docker/config.json`, `.cargo/credentials` |
| Production secrets | `.env.production` |
| Git internals | `.git/config`, `.git/hooks/` |
| Shell config | `.bashrc`, `.zshrc`, `.gitconfig` |

### Sensitive Files (WARN only)

Writes proceed but a warning is attached:

`.env`, `.env.local`, `secrets.*`, `credentials.*`, `password*`, `api-key*`, `.pem`, `.key`, `id_rsa`, `.npmrc`

### Path Validation Rules

`validateFilePath()` blocks:

- Empty or null paths
- Paths with control characters (`\x00-\x08\x0b\x0c\x0e-\x1f`) — note: tab (`\x09`) and newline (`\x0a`) are in the blocked range via the exclusion pattern
- Paths with embedded newlines (separate check)

**Important**: Use `absolutePath = path.resolve(resolvedPath)` for comparisons against absolute hook dirs. `resolvedPath` stays relative when both the file and its parent directory don't exist (common in test isolation).

### Hook Self-Protection

file-validator blocks writes to `.claude/hooks/*.cjs` during active sessions. To edit hooks:
1. `cp .claude/hooks/hook.cjs /tmp/hook.cjs`
2. Edit `/tmp/hook.cjs`
3. `cp /tmp/hook.cjs .claude/hooks/hook.cjs` (via Bash, not Write tool)

Test files (`*.js`) are not blocked.

### Cross-Platform /tmp

Uses `os.tmpdir()` only — no hardcoded `/tmp` — for Windows compatibility.

---

## Shared Input Shape (PreToolUse)

Both hooks receive:

```json
{
  "tool": "Bash" | "Write" | "Edit",
  "toolInput": {
    "command": "...",       // Bash
    "file_path": "...",     // Write/Edit
    "content": "..."        // Write
  },
  "sessionId": "uuid"
}
```

Input is sanitized via `sanitizeJson()` before processing to prevent prototype pollution.

## Business Rules

- **No bypass**: Never use `--force` flags or `FORCE_INSTALL=true` patterns to skip security checks
- **Commit messages**: Messages referencing dangerous patterns (e.g. `rm -rf`, pipe-to-interpreter) trigger bash-validator. Write to `/tmp/commit-msg.txt` and use `git commit -F /tmp/commit-msg.txt`
- **Secret patterns ordering**: Specific prefixed patterns (GCP `ya29.`, PyPI `pypi-`) must come BEFORE broad catch-all patterns in `SECRET_PATTERNS` — the catch-all partially consumes tokens, preventing subsequent specific patterns from matching
