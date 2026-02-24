#!/usr/bin/env bash
# Generates CHECKSUMS.sha256 for installer verification
set -euo pipefail

echo "# Claude Sentient v1.4.0 — File Checksums" > CHECKSUMS.sha256
echo "# Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> CHECKSUMS.sha256
echo "" >> CHECKSUMS.sha256

# Core files that get installed
find .claude/commands -name "cs-*.md" -o -name "CLAUDE.md" | sort | xargs sha256sum >> CHECKSUMS.sha256
find .claude/hooks -name "*.cjs" -o -name "README.md" | sort | xargs sha256sum >> CHECKSUMS.sha256
find profiles -name "*.yaml" -o -name "CLAUDE.md" | sort | xargs sha256sum >> CHECKSUMS.sha256
find agents -name "*.yaml" -o -name "CLAUDE.md" | sort | xargs sha256sum >> CHECKSUMS.sha256
find schemas -name "*.json" | sort | xargs sha256sum >> CHECKSUMS.sha256
find rules -name "*.md" | sort | xargs sha256sum >> CHECKSUMS.sha256
sha256sum test-utils.js >> CHECKSUMS.sha256

echo "Checksums written to CHECKSUMS.sha256"
