# Deferred Features — Future Enhancements

> **Purpose:** Features identified in V2 planning that are deferred to keep the initial implementation focused.
> **Status:** Not in scope for V1.0 of Claude Sentient
> **Review:** Revisit after core system is stable and working

---

## Overview

During the simplification of Claude Sentient from the original V2 vision, these features were identified as valuable but non-essential for the initial release. They add complexity that could slow down getting a working system.

**Principle:** Get the core working first, then add these incrementally based on actual need.

---

## Deferred: Advanced Learning Engine

### Original Vision
A sophisticated self-improvement system with:
- Auto-rule generation from mistakes (3+ occurrences triggers rule creation)
- Effectiveness tracking (rules track their prevention rate)
- Auto-pruning (rules below 50% effectiveness get removed)
- Prompt optimization (A/B testing different phrasings)
- Strategy evolution (learning which recovery strategies work)
- Cross-project pattern sharing

### Why Deferred
- The complexity of tracking effectiveness is high
- Risk of generating bad rules that degrade performance
- Can be added incrementally later

### Simplified Alternative (Current)
- Manual rule creation in `.claude/rules/auto/`
- Project knowledge in `.claude/knowledge/`

### Future Implementation Notes
If implementing later:
1. Start with simple occurrence counting
2. Add manual effectiveness ratings before auto-tracking
3. Consider human-in-the-loop for rule approval

---

## Deferred: Staff Engineer Agent

### Original Vision
An adversarial review agent that:
- Reviews all plans before execution
- Challenges assumptions
- Identifies risks and edge cases
- Requires "approval" before proceeding
- Simulates senior engineer review

### Why Deferred
- Adds friction to every task
- Most tasks don't need adversarial review
- Can slow down simple work significantly
- Claude's self-critique is often sufficient

### Simplified Alternative (Current)
- Self-critique skill for complex changes
- Manual plan mode for risky operations
- User approval for destructive actions (already in Claude Code)

### Future Implementation Notes
If implementing later:
- Make it opt-in, not default
- Trigger only for: security changes, breaking changes, large refactors
- Use as a `/cs-review-plan` command rather than automatic

---

## Deferred: Opus Permission Guardian

### Original Vision
A gatekeeper agent that:
- Evaluates operation risk levels
- Auto-approves safe operations
- Escalates risky operations to user
- Tracks permission patterns
- Uses Opus model for security-critical decisions

### Why Deferred
- Claude Code already has permission system
- Hooks can handle auto-approval for safe commands
- Over-engineering for most use cases

### Simplified Alternative (Current)
- Use Claude Code's built-in permission prompts
- Simple bash auto-approve hook for known-safe commands

---

## Deferred: Formal Event Bus Architecture

### Original Vision
A typed publish/subscribe event system:
- Formal event schemas with payloads
- Components subscribe to events
- Async event processing
- Event history for debugging
- Event-driven component communication

### Why Deferred
- Claude Code's hook system already provides lifecycle events
- Additional abstraction layer adds complexity
- State files provide sufficient coordination
- YAGNI (You Aren't Gonna Need It)

### Simplified Alternative (Current)
- Use Claude Code hooks (SessionStart, PostToolUse, etc.)
- State stored in JSON files
- Direct skill/command invocation

### Future Implementation Notes
If implementing later:
- Consider only for multi-agent swarm coordination
- Keep it simple: just a message log file agents can read/write

---

## Deferred: Git Worktree Orchestrator

### Original Vision
Parallel development using git worktrees:
- Spawn workers in separate worktrees
- Parallel feature development
- Automatic merge coordination
- Conflict resolution assistance

### Why Deferred
- Complex git state management
- Risk of merge conflicts
- Most tasks don't benefit from parallelism
- Claude Code subagents can work in sequence effectively

### Simplified Alternative (Current)
- Sequential task execution
- Manual worktree use if needed

---

## Deferred: Presentation Generator

### Original Vision
Auto-generate presentations from code:
- Code walkthrough slides
- Architecture diagrams
- Change summaries for stakeholders

### Why Deferred
- Not core to development workflow
- Can be done manually when needed
- Low frequency use case

---

## Deferred: Database Analytics Agent

### Original Vision
A data-analyst agent for:
- Query generation
- Schema analysis
- Performance optimization
- Migration assistance

### Why Deferred
- Specialized use case
- Can use general researcher agent + database rules
- Add when actually needed

### Simplified Alternative (Current)
- Database rules file with best practices
- Use researcher agent for DB questions

---

## Deferred: Multi-Registry Skill Discovery

### Original Vision
Intelligent discovery across skill registries:
- Search skills.sh (33,000+ skills)
- Search aitmpl.com (200+ skills)
- Intelligent scoring and ranking
- Auto-install based on confidence

### Why Deferred
- Focus on curated, tested skills first
- External registry quality varies
- Adds dependency on external services

### Simplified Alternative (Current)
- Curated set of 25-30 skills
- Manual skill addition as needed
- Reference V1 skill inventory for expansion

---

## Deferred: Extended Component Counts

### Original Targets vs. Iterative MVP

| Component | Original | Simplified | MVP (Phase 1) | Deferred |
|-----------|----------|------------|---------------|----------|
| Skills | 99 | 25-30 | 5-6 | ~90 |
| Commands | 50 | 20-25 | 3-4 | ~45 |
| Agents | 20 | 10-12 | 3-4 | ~15 |
| Gates | 18 | 12 | 4 blocking | 8+ |
| Phases | 10 | 8 | 8 (defined) | 0 |

### MVP Components (Phase 1)

**Commands:**
- `/cs-loop` — Core autonomous loop
- `/cs-plan` — Plan before executing
- `/cs-status` — Show current state

**Skills:**
- profile-detector — Detect project type
- context-loader — Load profile and inject context
- checkpoint — Create verified commits
- error-recovery — Handle failures gracefully
- queue-manager — Manage task queue
- definition-of-done — Check completion criteria

**Gates (Blocking):**
- LINT — Zero lint errors
- TEST — Tests pass
- BUILD — Project builds
- GIT — Clean git state

**Agents:**
- researcher — Explore codebase, answer questions
- code-reviewer — Review changes for quality
- test-writer — Generate tests for code

### Deferred Skills (from V1)
These V1 skills are not in initial scope but can be added later:

**Orchestration (deferred):**
- visual-diff
- parallel-exploration
- extended-thinking (complex reasoning)
- argument-parser (CLI syntax)

**Optimization (deferred):**
- file-watcher
- auto-update-checker
- dry-run-mode
- undo-history

**Project Management (deferred):**
- health-dashboard
- frontmatter-generator
- cross-project-patterns
- team-sharing
- template-registry

**CI/CD (deferred):**
- prompt-testing
- ci-cd-integration (full version)

### Deferred Commands (from V1)
- `/cs-terminal` (terminal UI audit)
- `/cs-seo` (SEO audit)
- `/cs-sync` (frontend-backend sync)
- `/cs-postmortem` (incident analysis)
- `/cs-standup` (standup summary)
- `/cs-retro` (retrospective)
- `/cs-prompt` (prompt generation)
- `/cs-onboard` (onboarding guide)

### Deferred for Post-MVP (Phase 2+)
These commands are defined but deferred until core loop is working:
- `/cs-review` (code review) — Phase 2
- `/cs-test` (run tests) — Phase 2
- `/cs-fix` (fix specific issue) — Phase 2
- `/cs-commit` (manual checkpoint) — Phase 2
- `/cs-docs` (documentation) — Phase 3
- `/cs-security` (security audit) — Phase 3
- `/cs-refactor` (refactoring) — Phase 3

### Deferred Agents
- terminal-ui-expert
- seo-expert
- prompt-engineer
- migration-specialist (keep database-expert instead)
- brownfield-expert (merge into researcher)

---

## Deferred: Complex Swarm Orchestration

### Original Vision
Full swarm mode with:
- Self-organizing workers
- Task claiming from shared pool
- Inter-agent messaging
- Result synthesis
- Dependency-aware scheduling

### Why Deferred
- Claude Code subagents handle most parallelism needs
- Complex coordination adds failure modes
- Sequential execution is often sufficient and safer

### Simplified Alternative (Current)
- Use Claude Code Task tool with subagents
- Simple task queue in state file
- Leader-worker pattern when needed

---

## Priority Order for Future Implementation

When the core system is stable, consider adding in this order:

### High Value, Lower Complexity
1. Additional skills from V1 (one at a time, as needed)
2. More project profiles (Ruby, Rust, Java, etc.)
3. Visual diff for UI verification
4. Extended quality gates

### Medium Value, Medium Complexity
5. Worktree orchestration (for parallel work)
6. Simple effectiveness tracking for rules
7. Database analytics agent
8. CI/CD integration hooks

### High Value, High Complexity
9. Learning engine improvements
10. Swarm orchestration
11. Multi-registry discovery

### Low Priority
12. Presentation generator
13. SEO/Terminal UI experts
14. Team sharing features

---

## Migration Path

When adding deferred features:

1. **Check if still needed** — Requirements change over time
2. **Start minimal** — Add simplest version first
3. **Test thoroughly** — Don't break working system
4. **Document** — Update relevant docs
5. **Get feedback** — Use for a week before finalizing

---

## Related Documents

- `reference/v2-planning/` — Original detailed planning docs
- `reference/v1/` — V1 implementation for reference
- `docs/V1_FEATURE_INVENTORY.md` — Complete V1 feature list

---

*This document is a parking lot, not a backlog. Features here may never be implemented if the simplified system proves sufficient.*
