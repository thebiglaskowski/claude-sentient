# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project setup

### Changed

### Fixed

### Removed

---

## [4.3.0] - 2026-01-31

### Added
- **Multi-Registry Discovery**: `/cc-scout-skills` now searches multiple registries
  - skills.sh (33,000+ skills, multi-agent)
  - aitmpl.com (Claude Code-specific: skills, agents, commands, hooks, MCPs)
- **Intelligent Scoring**: Resources ranked 0-100 based on technology match, reputation, specificity
- **Auto-Install Tiers**: High-confidence (≥80) vs recommended (50-79) vs manual
- **Deduplication Logic**: Best resource selected when duplicates exist across registries
- **Resource Types**: Now discovers skills, agents, commands, hooks, MCPs, and settings
- **Registry Configuration**: `.claude/config/registries.md` for extensible registry management
- **Automation Clarity**: Documentation clearly indicates automated vs manual steps

### Changed
- `skill-scout.md` upgraded to v2.0 with multi-registry support
- `cc-scout-skills.md` command expanded with scoring, deduplication, and resource types
- `template-registry.md` aligned with new architecture (manual browsing vs automated discovery)
- Updated CLAUDE.md with v4.3 features
- Updated QUICK_REFERENCE.md with new Skill Registries section

---

## [4.2.0] - 2026-01-31

### Added
- **Plugin Support**: Full documentation for Claude Code plugins
- **Supermemory Integration**: Persistent memory across sessions
- `PLUGINS.md`: Complete plugin installation and configuration guide
- Plugin troubleshooting section in TROUBLESHOOTING.md
- Plugin quick reference in QUICK_REFERENCE.md

### Changed
- Updated SETUP.md with plugin installation section
- Updated CLAUDE.md with v4.2 features and plugin references
- Updated TROUBLESHOOTING.md table of contents

---

## [4.1.0] - 2026-01-31

### Added
- **Swarm Mode**: Self-organizing workers for parallel task execution (`--swarm` flag)
- **Task Dependencies**: `blockedBy`/`blocks` fields for automatic pipeline unblocking
- **Plan Approval**: Leader approval workflow for risky/breaking changes
- **Worker Claiming**: Atomic task claiming from shared pool with priority ordering
- New skills:
  - `swarm-mode`: Self-organizing worker coordination
  - `task-dependencies`: Automatic pipeline progression
  - `plan-approval`: Safety gates for risky changes
- `--workers=N` flag to configure number of swarm workers
- Dependency-aware prioritization in queue manager
- Swarm status tracking in LOOP_STATE.md
- `SWARM_ARCHITECTURE.md` documentation

### Changed
- `queue-manager` upgraded to v3.0 with dependency support
- `meta-cognition` enhanced with orchestration decision tree
- `_index.md` updated with new skills (67 total)
- `CLAUDE.md` updated with v4.1 swarm documentation
- `cc-loop.md` command now supports `--swarm` and `--workers` flags

### Fixed
- Queue manager now properly handles blocked tasks

---

## [4.0.0] - 2026-01-29

### Added
- Namespaced commands (`/cc-*` prefix)
- Pattern library with 15+ reusable patterns
- Snippet registry with indexed code templates
- Smart revert functionality
- Brownfield analyzer for existing codebases
- 10 loop phases including META-COGNITION
- 15 quality gates (all blocking)
- Parallel agent execution
- Context budget monitor
- Decision logger

### Changed
- All commands now use `cc-` namespace
- Skills increased to 64 across 9 categories

---

## [3.0.0] - 2026-01-15

### Added
- Modular rules system (`@rules/[name]`)
- Specialized agents with model routing
- Comprehensive hook system (12 hooks)
- CI/CD integration scripts
- YAML frontmatter for skills

### Changed
- Skills reorganized by category
- Commands support arguments

---

<!--
## [1.0.0] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes to existing features

### Fixed
- Bug fixes

### Removed
- Removed features

### Security
- Security fixes
-->
