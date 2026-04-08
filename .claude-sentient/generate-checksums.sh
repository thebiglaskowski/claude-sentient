#!/usr/bin/env bash
# Generates CHECKSUMS.sha256 for installer verification
set -euo pipefail

echo "# Claude Sentient v1.7.1 — File Checksums" > .claude-sentient/CHECKSUMS.sha256
echo "# Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> .claude-sentient/CHECKSUMS.sha256
echo "" >> .claude-sentient/CHECKSUMS.sha256

# Only checksum git-tracked files to avoid including local-only files
git ls-files .claude/commands .claude/hooks .claude-sentient/profiles .claude-sentient/schemas \
  .claude-sentient/templates .claude-sentient/examples .claude-plugin .cursor .codex .claude/skills \
  .claude-sentient/test-utils.js \
  | sort | xargs sha256sum >> .claude-sentient/CHECKSUMS.sha256

echo "Checksums written to .claude-sentient/CHECKSUMS.sha256"
