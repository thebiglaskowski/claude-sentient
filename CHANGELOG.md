# CHANGELOG.md — Claude Sentient

All notable changes to this project will be documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

### Added
- Shell profile (`profiles/shell.yaml`) for bash/PowerShell scripts
- 12 topic rules in `rules/` (security, testing, api-design, etc.)
- Auto-rule loading based on task keywords in `/cs-loop`
- Auto-STATUS.md updates in `/cs-loop` COMMIT phase
- Auto-CHANGELOG prompts for `feat:` and `fix:` commits
- Documentation policy with automation levels in CLAUDE.md
- Commands now in `.claude/commands/` for Claude Code recognition

### Changed
- `/cs-loop` INIT phase now loads rules based on task keywords
- `/cs-loop` COMMIT phase now auto-updates governance files
- Profiles count: 3 → 4

---

## [0.2.0] — 2026-02-01

### Added
- `/cs-loop` command - Autonomous development loop
- `/cs-plan` command - Plan before executing (uses native `EnterPlanMode`)
- `/cs-status` command - Show project status
- `/cs-learn` command - Save learnings to memory
- Python profile (`profiles/python.yaml`)
- TypeScript profile (`profiles/typescript.yaml`)
- General fallback profile (`profiles/general.yaml`)
- Governance file system (STATUS.md, CHANGELOG.md, DECISIONS.md)
- Templates for governance files (`templates/`)
- Governance file checks in `/cs-status`
- Auto-creation of governance files in `/cs-loop` init
- AskUserQuestion support for structured decision-making
- Hooks system with UserPromptSubmit and Stop hooks
- Background subagent support for parallel task execution
- Context7 integration for automatic library documentation
- reference/HOOKS.md with hook documentation and examples

### Changed
- **Major pivot to native-first architecture**
- Now uses Claude Code's built-in `TaskCreate`/`TaskUpdate` instead of custom work queue
- Now uses Claude Code's built-in `EnterPlanMode` instead of custom planning
- Now uses Claude Code's built-in `Task` subagents instead of custom agents
- Updated CLAUDE.md to v0.2.0 documenting native-first approach
- Simplified from 99 planned skills to 4 focused commands

### Removed
- Plans for custom event bus (not needed)
- Plans for custom task queue (using native)
- Plans for custom planning mode (using native)
- Plans for custom sub-agent system (using native)

---

## [0.1.0] — 2026-02-01

### Added
- Initial project structure
- Official Claude Code memory pattern (`.claude/rules/*.md`)
- Phase definitions (8 phases)
- Decision to use `cs-` prefix for commands
- CLAUDE.md, STATUS.md, DECISIONS.md

### Changed
- Removed claude-mem dependency (unreliable)
- Simplified scope from original V2 GAMEPLAN

---

## [0.0.1] — 2026-02-01

### Added
- Project initialization
- V1 reference clone in `reference/v1/`
- Original planning documents in `reference/v2-planning/`
- JSON schemas (from original vision)

---

## Version Summary

| Version | Date | Highlights |
|---------|------|------------|
| 0.2.0 | 2026-02-01 | Native-first pivot, 4 commands, 3 profiles |
| 0.1.0 | 2026-02-01 | Foundation, memory pattern, simplified scope |
| 0.0.1 | 2026-02-01 | Initial setup |
