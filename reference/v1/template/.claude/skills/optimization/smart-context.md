---
name: smart-context
description: Intelligently load and manage context with proactive compaction
version: 2.0.0
model: sonnet
triggers:
  - "load context"
  - "what do I need to know"
  - "relevant files"
  - "focus on"
  - "context budget"
  - "summarize context"
tags: [optimization, context, memory, compaction]
---

# Smart Context Management v2.0

Intelligently load, monitor, and compact context with proactive background summarization.

**v2.0 Enhancements (from Anthropic Cookbook):**
- Instant compaction with background summarization
- Soft thresholds trigger before hitting limits
- Context budget monitoring with visual indicators
- Prompt caching for 80% cost reduction on compaction

---

## Description

Manages context window intelligently through:
1. **Selective Loading** — Load only relevant sections based on task type
2. **Budget Monitoring** — Track usage with soft/hard thresholds
3. **Proactive Compaction** — Summarize in background before hitting limits
4. **Instant Recovery** — Pre-built summaries swap in with zero wait time

---

## Context Budget Monitoring

### Threshold Levels

| Level | Usage | Indicator | Action |
|-------|-------|-----------|--------|
| **Green** | <50% | ✅ | Normal operation |
| **Yellow** | 50-70% | ⚠️ | Start background compaction |
| **Orange** | 70-85% | 🟠 | Background summary ready, consider swap |
| **Red** | >85% | 🔴 | Swap to compacted context immediately |

### Visual Budget Display

```
Context Budget: ████████████░░░░░░░░ 62% (Yellow)
├── Essential: 2,000 tokens (fixed)
├── Task Context: 4,500 tokens
├── History: 5,800 tokens ← compaction target
└── Available: 7,700 tokens

Background Summary: ✓ Ready (1,200 tokens)
Potential Savings: 4,600 tokens
```

---

## Instant Compaction (v2.0)

### The Problem with Traditional Compaction

Traditional approach waits until context is full, then blocks while summarizing:
```
User message → Context full → WAIT (5-10s) → Summary → Continue
                              ↑ Bad UX
```

### Instant Compaction Solution

Proactive approach builds summaries in background before needed:
```
Yellow threshold (50%) → Start background summary
Orange threshold (70%) → Summary ready, on standby
Red threshold (85%) → Instant swap, no wait

Background thread runs independently, no user-facing latency
```

### Implementation Pattern

```markdown
## Compaction State

### Background Summarization
- Trigger: Context usage > 50%
- Status: In progress / Ready / Not needed
- Last snapshot: [timestamp]
- Summary size: [tokens]

### Compaction Queue
1. Session history (oldest first)
2. Completed task context
3. Stale file contents
4. Resolved discussions

### Preservation Priority (Never Compact)
- Current task context
- Active file contents
- User corrections and preferences (verbatim)
- Incomplete work state
- Error context under investigation
```

---

## Session Memory Preservation

When compacting, preserve critical information:

### Always Preserve (Verbatim)
```markdown
- Exact user requests and refinements (quote directly)
- User corrections — "these represent learned preferences"
- File paths, IDs, names mentioned
- Technical constraints discovered
- Active work in progress with precise state
```

### Safe to Summarize
```markdown
- Completed tasks (keep outcome, compress process)
- Exploration that led nowhere
- Verbose tool outputs
- Redundant explanations
```

### Compaction Prompt Template

```markdown
Summarize this session history for continuity. Preserve:
1. **Exact user requests** — Quote their words
2. **Completed work** — What files changed, what was achieved
3. **User corrections** — Verbatim, these are preferences
4. **Current state** — What's in progress, what's next
5. **Key constraints** — Technical limitations discovered

Compress:
- Exploration that didn't lead anywhere
- Verbose outputs (keep conclusions)
- Repeated explanations

Output format:
## Session Summary
[Concise summary with quoted user requests]

## Completed Work
[List of achievements with file paths]

## Learned Preferences
[User corrections, quoted]

## Current State
[What's in progress, what's next]

## Key Context
[Technical constraints, important decisions]
```

---

## Task-Based Context Loading

### Problem

Full PROJECT_MAP.md can be large. Loading everything wastes context window on irrelevant information.

### Solution

Map task types to relevant context sections:

| Task Type | Relevant Context |
|-----------|------------------|
| Feature work | Entry points, related components, types |
| Bug fix | Error location, dependencies, tests |
| Refactoring | Target files, dependents, patterns |
| Testing | Test setup, mocks, fixtures |
| API work | Routes, controllers, types, middleware |
| UI work | Components, styles, state management |
| Database | Models, migrations, queries |
| Auth | Auth files, middleware, session handling |
| DevOps | Config files, scripts, CI/CD |

| Task Type | Relevant Context |
|-----------|------------------|
| Feature work | Entry points, related components, types |
| Bug fix | Error location, dependencies, tests |
| Refactoring | Target files, dependents, patterns |
| Testing | Test setup, mocks, fixtures |
| API work | Routes, controllers, types, middleware |
| UI work | Components, styles, state management |
| Database | Models, migrations, queries |
| Auth | Auth files, middleware, session handling |
| DevOps | Config files, scripts, CI/CD |

## Context Loading Strategy

### Step 1: Identify Task Type

From user request, determine task category:
- "Add a button to..." → UI work
- "Fix the login bug" → Auth + Bug fix
- "Optimize the query" → Database
- "Add new endpoint" → API work

### Step 2: Select Relevant Sections

Based on task type, load from PROJECT_MAP.md:

```markdown
## For API Work, Load:
- Entry Points > API section
- Directory Structure > src/api/, src/routes/
- Key Patterns > API patterns
- Important Files > API-related files

## Skip:
- UI components
- Styling patterns
- Frontend state
```

### Step 3: Load Supporting Context

Based on what's selected, also load:
- Direct dependencies of relevant files
- Shared types/interfaces
- Related tests

## PROJECT_MAP.md Section Markers

Structure PROJECT_MAP.md with clear sections for selective loading:

```markdown
# Project Map

## Overview
[Always load - small, essential]

## Tech Stack
[Always load - small, essential]

<!-- SECTION: structure -->
## Directory Structure
[Load based on task area]
<!-- /SECTION: structure -->

<!-- SECTION: api -->
## API Layer
[Load for API tasks]
<!-- /SECTION: api -->

<!-- SECTION: ui -->
## UI Components
[Load for UI tasks]
<!-- /SECTION: ui -->

<!-- SECTION: data -->
## Data Layer
[Load for database tasks]
<!-- /SECTION: data -->

<!-- SECTION: auth -->
## Authentication
[Load for auth tasks]
<!-- /SECTION: auth -->

<!-- SECTION: testing -->
## Testing
[Load for test tasks]
<!-- /SECTION: testing -->

## Commands
[Always load - small, useful]
```

## Task → Context Mapping

### Feature Development
```markdown
Load:
- Overview (always)
- Tech Stack (always)
- Directory Structure (relevant subdirs)
- Related section (api/ui/data based on feature)
- Key Patterns
- Commands
```

### Bug Investigation
```markdown
Load:
- Overview (always)
- Tech Stack (always)
- Section containing bug location
- Testing section
- Error handling patterns
```

### Code Review
```markdown
Load:
- Overview (always)
- Key Patterns (for style checking)
- Testing (for coverage check)
- Relevant section for changed files
```

### Refactoring
```markdown
Load:
- Full Directory Structure
- Key Patterns
- Section being refactored
- Dependent sections
```

## Dynamic Context Requests

As task progresses, load additional context on-demand:

```markdown
User: "Now I need to update the database schema"

Response: "Loading data layer context..."
[Load: data section, migrations, models]
```

## Context Budget

### Priorities
1. **Essential** (always load): Overview, Tech Stack, Commands (~500 tokens)
2. **Primary** (task-specific): Main relevant section (~1000 tokens)
3. **Supporting** (if space): Dependencies, tests (~500 tokens)
4. **Reference** (on-demand): Other sections as needed

### Budget Allocation
```markdown
Total budget: ~3000 tokens for context
- Essential: 500 (fixed)
- Primary: 1500 (variable)
- Supporting: 500 (variable)
- Buffer: 500 (on-demand)
```

## Implementation Pattern

When starting a task:

```markdown
## Context Loading

**Task:** Add password reset endpoint

**Loading:**
1. ✅ Overview (essential)
2. ✅ Tech Stack (essential)
3. ✅ API Layer (primary - API task)
4. ✅ Authentication (supporting - auth-related)
5. ⏭️ UI Components (skipped - backend only)
6. ⏭️ Data Layer (load if needed)

**Relevant Files Identified:**
- src/routes/auth.ts
- src/controllers/authController.ts
- src/services/emailService.ts
- src/types/auth.ts
```

## Refresh Triggers

Reload context when:
- Task type changes significantly
- Moving to different area of codebase
- User explicitly asks for broader context
- Error suggests missing context

## Benefits

| Without Smart Context | With Smart Context v2.0 |
|----------------------|-------------------------|
| Load 5000 token PROJECT_MAP | Load 1500 relevant tokens |
| Generic understanding | Focused, detailed understanding |
| May miss task-specific details | Prioritizes task-relevant info |
| Same context for all tasks | Tailored context per task |
| Block on compaction | Instant swap from background |
| Lose important details | Preserve user preferences verbatim |

---

## Cost Optimization

### Prompt Caching for Background Summarization

When triggering background compaction, the conversation prefix is already cached from the main chat. This means:

```
Background summarization cost breakdown:
├── Cached prefix: 90% discount (already in cache)
├── New instruction: Full price (only the summarization prompt)
└── Total savings: ~80% vs fresh summarization

This makes proactive compaction economically viable.
```

### Cache Availability Check

Not all deployments support prompt caching. Before relying on cost savings:

```markdown
## Cache Availability

Check before enabling cache-dependent optimizations:

| Deployment | Prompt Caching | Action |
|------------|----------------|--------|
| Claude API (direct) | ✅ Supported | Enable cache reuse |
| Claude.ai (web) | ✅ Automatic | Already cached |
| AWS Bedrock | ⚠️ Check tier | Verify in console |
| Google Vertex | ⚠️ Check tier | Verify in console |
| Self-hosted | ❌ Not available | Disable cache reuse |

Configuration fallback:
├── If caching available → Use cache reuse (80% savings)
├── If caching unavailable → Disable cache reuse
└── Compaction still works, just without cost optimization
```

### Enabling/Disabling Cache Reuse

```json
// .claude/settings.json
{
  "optimization": {
    "context": {
      "compactionCacheReuse": true,  // Set false if caching unavailable
      "fallbackToDirectCompaction": true  // Still compact, just full price
    }
  }
}
```

### When to Trigger Compaction

| Trigger | Action |
|---------|--------|
| Context > 50% | Start background summary generation |
| Context > 70% | Summary should be ready |
| Context > 85% | Swap to summary immediately |
| Task type change | Refresh context for new task |
| User says "summarize" | Force immediate compaction |

---

## Integration with Loop

### At Iteration Start

```markdown
1. Check context budget
2. If Yellow+ threshold → Ensure background summary running
3. If Red threshold → Swap to summary before continuing
4. Load task-relevant context
5. Display budget indicator
```

### During Work

```markdown
1. Monitor context growth
2. If crossing Yellow → Start background summary
3. If crossing Orange → Log "summary ready for swap"
4. Continue work normally
```

### At Iteration End

```markdown
1. Update context budget tracking
2. Refresh background summary if stale
3. Mark completed task context as "compactable"
```

---

## Configuration

### In .claude/settings.json

```json
{
  "optimization": {
    "context": {
      "softThreshold": 0.50,
      "warnThreshold": 0.70,
      "hardThreshold": 0.85,
      "backgroundCompaction": true,
      "preserveUserCorrections": true,
      "compactionCacheReuse": true
    }
  }
}
```

---

## Related Skills

| Skill | Integration |
|-------|-------------|
| `context-budget-monitor` | Provides threshold tracking |
| `session-memory` | Avoids redundant analysis |
| `prompt-feedback` | Learns from compaction quality |
| `autonomous-loop` | Uses context budget in decisions |
