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
**Status:** Accepted

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

## Pending Decisions
- Sync complexity

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
