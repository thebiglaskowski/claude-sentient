# DECISIONS.md — Claude Sentient Architecture Decisions

Record of significant architecture and design decisions.

---

## Decision Format

Each decision follows this structure:
- **Context:** What is the situation?
- **Decision:** What did we decide?
- **Rationale:** Why this choice?
- **Consequences:** What are the implications?
- **Alternatives:** What else was considered?

---

## Decisions

### DEC-001: Project Rename to Claude Sentient

**Date:** 2024-02-01
**Status:** Accepted

**Context:**
The original project name "claude-conductor" was already in use by other projects. Needed a unique name that reflects the V2 vision of an autonomous, self-aware development engine.

**Decision:**
Rename to "Claude Sentient" — emphasizing the self-aware, meta-cognitive nature of the system.

**Rationale:**
- "Sentient" captures self-awareness, which is the core differentiator
- Unique name not currently in use
- Maintains the "Claude" prefix for brand alignment
- Reflects the learning and adaptation capabilities

**Consequences:**
- New repository created
- All documentation updated
- Clear differentiation from V1

**Alternatives Considered:**
- Claude Cortex (brain focus)
- Claude Nexus (hub focus)
- Claude Evolve (learning focus)
- Claude Forge (building focus)

---

### DEC-002: Separate Repository from V1

**Date:** 2024-02-01
**Status:** Accepted

**Context:**
V2 is a ground-up redesign with different architecture. Need to decide whether to continue in the same repo or start fresh.

**Decision:**
Create a new repository for Claude Sentient, with V1 cloned as reference in `reference/v1/`.

**Rationale:**
- Clean git history for new architecture
- No baggage from V1 development
- Clear separation of concerns
- V1 remains available as reference
- Easier to manage versions independently

**Consequences:**
- Two repositories to maintain (temporarily)
- Must ensure V1 features are migrated
- Reference folder adds to repo size

**Alternatives Considered:**
- Continue in V1 repo with v2/ subfolder
- Complete rewrite in place
- Fork V1 and refactor

---

### DEC-003: JSON Schema as Source of Truth

**Date:** 2024-02-01
**Status:** Accepted

**Context:**
V1 used convention-based validation with Markdown frontmatter. This led to inconsistencies and made IDE support difficult.

**Decision:**
Use JSON Schema for all component definitions. Schemas are the single source of truth.

**Rationale:**
- IDE autocomplete support
- Build-time validation
- Self-documenting
- Industry standard
- Composable via $ref

**Consequences:**
- Must maintain schemas
- Build step required for validation
- Learning curve for contributors

**Alternatives Considered:**
- TypeScript types
- YAML with custom validation
- Continue with convention-based

---

### DEC-004: Event-Driven Architecture

**Date:** 2024-02-01
**Status:** Accepted

**Context:**
V1 used direct function calls and fixed hooks. This created tight coupling and made extension difficult.

**Decision:**
Implement publish/subscribe event bus. All component communication happens through events.

**Rationale:**
- Loose coupling
- Easy to extend
- Testable in isolation
- Learning system can capture everything
- Async-friendly

**Consequences:**
- Must define event schemas
- Debugging requires event tracing
- Potential for event storms

**Alternatives Considered:**
- Direct function calls
- Message queues
- RPC-style communication

---

### DEC-005: Learning as First-Class Feature

**Date:** 2024-02-01
**Status:** Accepted

**Context:**
V1 had feedback files but no systematic learning. V2 vision requires continuous self-improvement.

**Decision:**
Build learning engine as core infrastructure, not an add-on. Every action feeds into learning.

**Rationale:**
- Core differentiator from V1
- Aligns with vision of autonomous improvement
- Boris tip: "Claude writes rules for itself"
- Enables true autonomy over time

**Consequences:**
- Every component must emit learning events
- Storage required for knowledge base
- Must track effectiveness
- Complexity increase

**Alternatives Considered:**
- Optional learning module
- External learning service
- Manual feedback only

---

### DEC-006: YAML for Content, JSON for Structure

**Date:** 2024-02-01
**Status:** Accepted

**Context:**
Need to choose formats for different file types. V1 used Markdown with YAML frontmatter.

**Decision:**
- YAML for content-heavy files (skills, commands, agents, patterns)
- JSON for structured data (schemas, gates, state, config)
- Markdown for documentation and phase content

**Rationale:**
- YAML is more readable for content with prose
- JSON is stricter for data structures
- Markdown is standard for documentation
- Clear conventions reduce confusion

**Consequences:**
- Multiple parsers needed
- Must document conventions clearly

**Alternatives Considered:**
- All JSON
- All YAML
- All Markdown with frontmatter (V1 style)

---

### DEC-007: Claude-Mem for Persistent Memory

**Date:** 2024-02-01
**Status:** Superseded by DEC-009

**Context:**
Learning persistence needs a robust solution. Options evaluated:
1. Supermemory (external service, requires Pro plan)
2. Manual local files (.claude/knowledge/)
3. Claude-Mem plugin (local, automatic, free)

**Decision:**
Use **claude-mem** plugin for persistent memory across sessions.

**Rationale:**
- Completely free (AGPL-3.0 license)
- Automatic capture via lifecycle hooks (no manual intervention)
- AI-powered compression (~10x token savings)
- SQLite + Chroma vector DB (semantic + keyword search)
- Web interface at localhost:37777 for viewing memories
- Privacy controls with `<private>` tags
- Battle-tested (15,942 stars, 1,117 forks)
- Local-only — no data leaves the machine
- Progressive disclosure reduces token usage

**Consequences:**
- Requires claude-mem plugin installation
- Dependencies: Node.js 18+, Bun, Python/uv (auto-installed)
- Port 37777 used for web interface
- Claude-sentient should auto-detect and use claude-mem when available

**Installation:**
```
/plugin marketplace add thedotmack/claude-mem
/plugin install claude-mem
```

**Alternatives Considered:**
- Supermemory (requires Pro plan subscription)
- Manual .claude/knowledge/ files (no auto-capture, no search)

---

### DEC-008: Simplify V2 Scope

**Date:** 2024-02-01
**Status:** Accepted

**Context:**
The original V2 vision included 99 skills, 50 commands, 20 agents, a complex learning engine, and 14 weeks of implementation. This was too ambitious and risked never shipping a working system.

**Decision:**
Simplify to a focused, achievable scope:
- 25-30 skills (down from 99)
- 20-25 commands (down from 50)
- 10-12 agents (down from 20)
- 8 phases (down from 10)
- 12 quality gates (8 blocking, 4 advisory)
- 6-week timeline (down from 14)
- Use Claude Code hooks instead of custom event bus

**Rationale:**
- Get a working system faster
- Avoid over-engineering
- Leverage existing Claude Code capabilities
- Can add deferred features later based on actual need
- The vision is preserved, just the scope is reduced

**Consequences:**
- Some features deferred (see reference/DEFERRED_FEATURES.md)
- Archived original planning docs to reference/v2-planning/
- Cleaner, more focused codebase
- Faster path to usable system

**Alternatives Considered:**
- Proceed with full V2 plan (rejected: too ambitious)
- Abandon V2 entirely (rejected: good ideas worth pursuing)
- Build just the loop without profiles (rejected: profile awareness is key value)

---

### DEC-009: Remove Claude-Mem Dependency

**Date:** 2026-02-01
**Status:** Accepted

**Context:**
Claude-mem was selected in DEC-007 for persistent memory, but the plugin proved unreliable and is not working as expected.

**Decision:**
Remove claude-mem from the project. Operate without persistent memory for now.

**Rationale:**
- Claude-mem is not functioning correctly
- Adding unreliable dependencies creates maintenance burden
- Core functionality works without persistent memory
- Can revisit memory solutions when stable options exist

**Consequences:**
- No automatic session memory persistence
- Simpler dependency chain
- May revisit memory solutions in the future

**Alternatives Considered:**
- Debug claude-mem issues (rejected: not worth the effort)
- Build custom memory solution (rejected: scope creep)
- Use manual .claude/knowledge/ files (can be added later if needed)

---

### DEC-010: Native-First Architecture

**Date:** 2026-02-01
**Status:** Accepted

**Context:**
The original V2 GAMEPLAN proposed custom implementations for:
- Task queue (custom work item tracking)
- Planning mode (custom planning workflow)
- Sub-agents (custom agent spawning)
- Event bus (custom pub/sub system)
- Learning engine (custom pattern detection)

Upon closer examination of Claude Code's built-in capabilities, we discovered native tools that already provide most of this functionality.

**Decision:**
Adopt a "native-first" architecture. Use Claude Code's built-in tools instead of reimplementing:

| Feature | Native Tool | Replaces |
|---------|-------------|----------|
| Task Queue | `TaskCreate`, `TaskUpdate`, `TaskList` | Custom work queue |
| Planning | `EnterPlanMode`, `ExitPlanMode` | Custom planning |
| Sub-agents | `Task` with `subagent_type` | Custom agents |
| Memory | `.claude/rules/*.md` | Custom knowledge base |
| Commands | `commands/*.md` + `Skill` | Custom command system |

Claude Sentient becomes a thin orchestration layer that coordinates these native tools, rather than a parallel implementation.

**Rationale:**
- Don't reinvent the wheel — native tools are tested and maintained
- Simpler codebase — 4 commands instead of 99 skills
- Zero external dependencies
- Works out of the box — no setup required
- Aligns with Claude Code's design philosophy
- Easier to maintain and update

**Consequences:**
- Dramatically simpler implementation
- Dependent on Claude Code's tool availability
- Less control over internal behavior
- Must document which native tools are used
- Original V2 GAMEPLAN is now reference material, not the plan

**Alternatives Considered:**
- Proceed with full custom implementation (rejected: too complex, duplicates native functionality)
- Hybrid approach with some custom, some native (rejected: inconsistent architecture)
- Abandon project (rejected: orchestration layer still provides value)

---

### DEC-011: Self-Improvement via CLAUDE.md Updates

**Date:** 2026-02-01
**Status:** Accepted

**Context:**
Boris Cherny (Claude Code creator) recommends: *"After every correction, end with: 'Update your CLAUDE.md so you don't make that mistake again.' Claude is eerily good at writing rules for itself."*

We needed a mechanism for Claude to learn from corrections and avoid repeating mistakes across sessions.

**Decision:**
Add a self-improvement instruction to CLAUDE.md that tells Claude to:
1. Acknowledge corrections
2. Fix the immediate issue
3. Propose a rule to prevent recurrence (in `.claude/rules/learnings.md` or `CLAUDE.md`)
4. Apply the update (with confirmation for CLAUDE.md changes)

This applies to both claude-sentient itself and any project using claude-sentient via the template.

**Rationale:**
- Simplest implementation — just an instruction, no hooks or custom code
- Works within Claude Code's native architecture
- Self-perpetuating — the rule teaches Claude to add more rules
- Persists across sessions via `.claude/rules/` files
- Follows the Boris Cherny pattern that's proven effective

**Consequences:**
- Claude will propose learnings.md updates after corrections
- Users may see more rule-writing activity
- Rules accumulate over time (may need pruning)
- Projects using claude-sentient inherit this behavior

**Alternatives Considered:**
- Hook-based approach (rejected: hooks can't invoke Claude)
- Separate `/cs-reflect` command (rejected: manual, not automatic)
- Custom reflection in `/cs-loop` (rejected: adds complexity, not always relevant)

---

### DEC-012: Claude Agent SDK Integration

**Date:** 2026-02-01
**Status:** Superseded (removed in v1.3.0 — SDK/dashboard stripped from project)

**Context:**
Claude Sentient was originally designed as a CLI-first orchestration layer using slash commands. However, users needed:
- Session persistence across terminal closures
- Programmatic control for CI/CD, webhooks, and scheduled tasks
- SDK-based orchestration instead of text commands

The Claude Agent SDK provides the infrastructure for these capabilities.

**Decision:**
Implement dual-mode support: maintain CLI compatibility while adding SDK capabilities.

| Mode | Entry Point | Use Case |
|------|-------------|----------|
| CLI | `/cs-loop`, `/cs-plan` | Interactive development |
| SDK | `ClaudeSentient.loop()` | Production automation |

The SDK is implemented in both Python and TypeScript:
- `sdk/python/claude_sentient/` - Python package
- `sdk/typescript/src/` - TypeScript package

**Rationale:**
- Enables production deployment (CI/CD, webhooks, scheduled tasks)
- Session persistence allows resuming work across terminal closures
- Programmatic control enables integration with existing toolchains
- Dual-mode ensures backward compatibility with existing CLI workflows
- Both languages provide first-class SDK support

**Consequences:**
- Additional maintenance for two SDK implementations
- SDK users need to install separate packages
- Session state stored in `.claude/state/session.json`
- Quality gates run as SDK hooks, not just CLI commands

**Alternatives Considered:**
- SDK only (rejected: breaks existing CLI workflows)
- Python only (rejected: TypeScript projects need native SDK)
- External session service (rejected: adds infrastructure dependency)

---

## Pending Decisions

None currently.

---

## Decision Template

```markdown
### DEC-XXX: Title

**Date:** YYYY-MM-DD
**Status:** Proposed/Accepted/Deprecated/Superseded

**Context:**
What is the situation that requires a decision?

**Decision:**
What is the decision that was made?

**Rationale:**
Why was this decision made?

**Consequences:**
What are the positive and negative implications?

**Alternatives Considered:**
What other options were evaluated?
```

---

*Decisions are permanent record. Mark as superseded rather than deleting.*
