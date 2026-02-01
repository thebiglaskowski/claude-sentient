# V2 Planning Documents (Archived)

> **Status:** Historical Reference
> **Purpose:** Original detailed planning for Claude Sentient before simplification

---

## What's Here

These documents represent the original comprehensive V2 planning before we simplified the approach. They contain valuable ideas but the scope was too large for initial implementation.

| Document | Description |
|----------|-------------|
| `BLUEPRINT.md` | Complete technical architecture with event bus, schemas, etc. |
| `GAMEPLAN.md` | Original 14-week implementation plan |
| `PLANNING.md` | Priority questionnaire and decision framework |
| `BORIS_CHERNY.md` | Tips from Claude Code creator |
| `BORIS_INTEGRATION.md` | Plan for integrating Boris's tips |
| `V1_FEATURE_INVENTORY.md` | Complete V1 feature inventory (68 skills, 37 commands, etc.) |

---

## Why Archived

The original V2 plan included:
- 99 skills, 50 commands, 20 agents
- Formal event bus with typed payloads
- Complex learning engine with auto-rule generation
- Staff-engineer adversarial review
- 14-week timeline

This was simplified to:
- 25-30 skills, 20-25 commands, 10-12 agents
- Use Claude Code hooks instead of custom event bus
- Use claude-mem for learning instead of custom engine
- 6-week timeline

---

## Still Valuable For

- Understanding the original vision
- Detailed technical specifications (if needed later)
- V1 feature inventory for migration reference
- Boris's tips (still applicable)

---

## See Also

- `../DEFERRED_FEATURES.md` — Features postponed for later
- `../v1/` — Complete V1 codebase for reference

---

*Archived 2024-02-01 during project simplification*
