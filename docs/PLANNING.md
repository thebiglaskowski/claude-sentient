# Claude Conductor 2.0 — Planning & Priorities

This document captures the strategic questions and decisions needed to guide the v2 redesign. Review and fill in your priorities to shape the implementation.

---

## Table of Contents

1. [Core Principle](#core-principle)
2. [Priority Ranking](#priority-ranking)
3. [Detailed Questions by Area](#detailed-questions-by-area)
4. [V1 Pain Points](#v1-pain-points)
5. [Feature Wishlist](#feature-wishlist)
6. [Migration Strategy](#migration-strategy)
7. [Decision Log](#decision-log)

---

## Core Principle

**V2 must do everything V1 does, but better.**

This means:
- [ ] All 68 skills preserved and migrated
- [ ] All 37 commands preserved and migrated
- [ ] All 15 agents preserved and migrated
- [ ] All 15+ patterns preserved and migrated
- [ ] All 9 snippets preserved and migrated
- [ ] All 13 rules preserved and migrated
- [ ] Full 10-phase autonomous loop
- [ ] All 15 quality gates
- [ ] Swarm orchestration
- [ ] Task dependencies
- [ ] Plan approval workflow
- [ ] Evaluator-optimizer pattern
- [ ] Query classification
- [ ] Context management with instant compaction
- [ ] Multi-registry skill discovery
- [ ] Plugin support

---

## Priority Ranking

Rank these 1-6 (1 = highest priority) or mark N/A if not important:

| Priority | Area | Your Rank |
|----------|------|-----------|
| Developer Experience | Easier to add/modify components | ___ |
| Reliability | Fewer bugs, more predictable behavior | ___ |
| Performance | Faster execution, less resource usage | ___ |
| Extensibility | Better customization, shareable extensions | ___ |
| Observability | Better debugging, understanding decisions | ___ |
| Onboarding | Easier for new users to learn | ___ |

### Notes on your priorities:
```
[Your notes here]
```

---

## Detailed Questions by Area

### 1. Developer Experience

**Current V1 State:**
- Adding a skill requires updating `skills/_index.md` manually
- No IDE autocomplete when writing skills/commands
- Errors only discovered when you try to use the component
- Hard to know if a change breaks other components

**V2 Improvements Planned:**
- JSON Schema validation catches errors immediately
- IDE autocomplete from schemas (works in VS Code, etc.)
- Single source of truth — indexes are generated, not maintained
- `conductor validate` command for pre-commit checks

**Questions:**

1. How often do you add new skills or commands?
   - [ ] Daily
   - [ ] Weekly
   - [ ] Monthly
   - [ ] Rarely

2. Do you use an IDE that supports JSON Schema autocomplete?
   - [ ] VS Code
   - [ ] JetBrains (WebStorm, PyCharm, etc.)
   - [ ] Vim/Neovim
   - [ ] Other: ___________
   - [ ] Don't care about autocomplete

3. Would you run a validation command before commits?
   - [ ] Yes, manually
   - [ ] Yes, as a pre-commit hook
   - [ ] No, too much friction

4. What's your biggest frustration when adding/modifying components?
   ```
   [Your answer]
   ```

---

### 2. Reliability

**Current V1 State:**
- State files (LOOP_STATE.md) are Markdown, parsed with regex
- Dependencies between skills are implicit (mentioned in prose)
- No version constraints between components
- If something breaks, it's hard to know why

**V2 Improvements Planned:**
- JSON state with schema validation (no parsing ambiguity)
- Explicit dependencies: `depends: { "other-skill": ">=1.0.0" }`
- Version conflict detection at load time
- Dependency graph visualization

**Questions:**

1. Have you experienced state file corruption or parsing issues?
   - [ ] Yes, frequently
   - [ ] Yes, occasionally
   - [ ] No, never
   - [ ] Not sure

2. Have you had issues where skills conflicted or had missing dependencies?
   - [ ] Yes, frequently
   - [ ] Yes, occasionally
   - [ ] No, never

3. Would explicit version constraints help or add overhead?
   - [ ] Help — I want to know about conflicts
   - [ ] Overhead — I don't want to manage versions
   - [ ] Optional — Nice to have but not required

4. Any specific reliability issues you've encountered?
   ```
   [Your answer]
   ```

---

### 3. Performance

**Current V1 State:**
- All skills are potentially loaded (trigger matching on all)
- Context compaction is reactive (waits until nearly full)
- Gates run sequentially
- Large files can slow down context

**V2 Improvements Planned:**
- Lazy loading — only load skills when triggers match
- Proactive background compaction (starts at 50% capacity)
- Parallel gate execution where no dependencies
- Smarter context budgeting based on task classification

**Questions:**

1. Are loop execution times a concern?
   - [ ] Yes, loops take too long
   - [ ] Sometimes slow but acceptable
   - [ ] No, speed is fine

2. Do you hit context limits during long sessions?
   - [ ] Yes, frequently
   - [ ] Yes, occasionally
   - [ ] No, never

3. What's an acceptable time for a full loop iteration?
   - [ ] < 1 minute
   - [ ] 1-5 minutes
   - [ ] 5-15 minutes
   - [ ] Don't care, just want correctness

4. Any specific performance bottlenecks you've noticed?
   ```
   [Your answer]
   ```

---

### 4. Extensibility

**Current V1 State:**
- Customization requires modifying platform files
- No clear boundary between "platform" and "project"
- Hard to share customizations between projects
- External registries (skills.sh, aitmpl) but no local registry

**V2 Improvements Planned:**
- `.claude/extensions/` directory for project-specific additions
- Override system — patch platform components without modifying them
- Shareable extension packages
- Local registry support

**Questions:**

1. Do you customize skills/commands per project?
   - [ ] Yes, frequently
   - [ ] Yes, occasionally
   - [ ] No, I use platform defaults

2. Would you share extensions with others or between projects?
   - [ ] Yes, I'd share publicly
   - [ ] Yes, between my own projects
   - [ ] No, my customizations are project-specific

3. Do you want to override platform behavior without forking?
   - [ ] Yes, critical feature
   - [ ] Nice to have
   - [ ] Don't need this

4. What customizations have you made or wanted to make?
   ```
   [Your answer]
   ```

---

### 5. Observability

**Current V1 State:**
- Decision logging exists but not central
- Hard to trace "why did the loop make this choice"
- Metrics are available but scattered
- History is in LOOP_STATE.md but limited

**V2 Improvements Planned:**
- Event bus — every action emits events, fully traceable
- Centralized decision log with rationale
- Built-in metrics in consistent JSONL format
- Full history in state for post-mortem debugging
- Event replay for debugging

**Questions:**

1. How often do you need to debug loop decisions?
   - [ ] Frequently
   - [ ] Occasionally
   - [ ] Rarely
   - [ ] Never

2. Would you use event tracing to understand behavior?
   - [ ] Yes, very useful
   - [ ] Maybe occasionally
   - [ ] No, too complex

3. Do you analyze metrics from sessions?
   - [ ] Yes, regularly
   - [ ] Yes, occasionally
   - [ ] No, don't use metrics

4. What would help you understand "why did it do that"?
   ```
   [Your answer]
   ```

---

### 6. Onboarding

**Current V1 State:**
- 68 skills, 37 commands — can be overwhelming
- Documentation is comprehensive but dense
- Index files help but are a lot to read
- Learning curve is significant

**V2 Improvements Planned:**
- Generated docs always match implementation (never stale)
- Progressive disclosure — start simple, discover features
- Better error messages with suggested fixes
- Interactive mode possible
- Guided "first run" experience

**Questions:**

1. Do others use this platform besides you?
   - [ ] Yes, team members
   - [ ] Yes, open source community
   - [ ] No, just me

2. If yes, is onboarding them a challenge?
   - [ ] Yes, significant barrier
   - [ ] Some learning curve
   - [ ] No, they pick it up easily
   - [ ] N/A

3. Would interactive tutorials help?
   - [ ] Yes, very useful
   - [ ] Maybe for some features
   - [ ] No, documentation is enough

4. What was hardest when you first started using this?
   ```
   [Your answer]
   ```

---

## V1 Pain Points

List specific frustrations, bugs, or limitations you've encountered with V1:

### Things That Don't Work Well
```
1.
2.
3.
```

### Things That Are Missing
```
1.
2.
3.
```

### Things That Are Confusing
```
1.
2.
3.
```

### Things You Work Around
```
1.
2.
3.
```

---

## Feature Wishlist

Features you'd like in V2 that don't exist in V1:

| Feature | Priority (1-5) | Notes |
|---------|----------------|-------|
| | | |
| | | |
| | | |
| | | |
| | | |

---

## Migration Strategy

### Approach Options

Choose your preferred migration approach:

- [ ] **Big Bang** — Migrate everything at once, switch over
- [ ] **Incremental** — Migrate component by component, run both
- [ ] **Parallel** — Keep V1 working, build V2 alongside, switch when ready

### Migration Priorities

If migrating incrementally, what order?

1. [ ] Core loop and phases first
2. [ ] Most-used skills first
3. [ ] Commands first
4. [ ] Whatever's easiest first
5. [ ] Other: ___________

### Backward Compatibility

- [ ] V2 must be able to run V1 components during transition
- [ ] Clean break is fine, migrate everything before using
- [ ] Need both to work simultaneously for some period

### Timeline Expectations

- [ ] Want V2 usable within weeks
- [ ] Months is fine
- [ ] No rush, quality over speed

---

## Decision Log

Document key decisions as they're made:

| Date | Decision | Rationale | Alternatives Considered |
|------|----------|-----------|------------------------|
| | | | |
| | | | |
| | | | |

---

## Next Steps

After completing this questionnaire:

1. Review priorities and pain points
2. Update BLUEPRINT.md with focused improvements
3. Create implementation plan based on priorities
4. Begin migration of highest-priority components

---

## Notes

```
[Additional thoughts, ideas, or context]
```
