#!/usr/bin/env bash
# Generates CHECKSUMS.sha256 for installer verification
set -euo pipefail

echo "# Claude Sentient v1.6.0 — File Checksums" > .claude-sentient/CHECKSUMS.sha256
echo "# Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> .claude-sentient/CHECKSUMS.sha256
echo "" >> .claude-sentient/CHECKSUMS.sha256

# Core files that get installed
find .claude/commands -name "cs-*.md" -o -name "CLAUDE.md" | sort | xargs sha256sum >> .claude-sentient/CHECKSUMS.sha256
find .claude/hooks -name "*.cjs" -o -name "README.md" | sort | xargs sha256sum >> .claude-sentient/CHECKSUMS.sha256
find .claude-sentient/profiles -name "*.yaml" -o -name "CLAUDE.md" | sort | xargs sha256sum >> .claude-sentient/CHECKSUMS.sha256
find .claude-sentient/schemas -name "*.json" | sort | xargs sha256sum >> .claude-sentient/CHECKSUMS.sha256
find .claude-sentient/templates -name "*.md" -o -name "*.json" | sort | xargs sha256sum >> .claude-sentient/CHECKSUMS.sha256
find .claude-sentient/examples -name "*.md" | sort | xargs sha256sum >> .claude-sentient/CHECKSUMS.sha256
find .claude-plugin -name "*.json" | sort | xargs sha256sum >> .claude-sentient/CHECKSUMS.sha256
find .cursor -name "*.mdc" | sort | xargs sha256sum >> .claude-sentient/CHECKSUMS.sha256
find .codex -name "*.md" | sort | xargs sha256sum >> .claude-sentient/CHECKSUMS.sha256
find .claude/skills -name "SKILL.md" -o -name "*.md" -path "*/references/*" | sort | xargs sha256sum >> .claude-sentient/CHECKSUMS.sha256
sha256sum .claude-sentient/test-utils.js >> .claude-sentient/CHECKSUMS.sha256

echo "Checksums written to .claude-sentient/CHECKSUMS.sha256"
