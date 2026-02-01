# Boris Cherny Tips → V2 Integration

> Mapping tips from the Claude Code creator to claude-conductor V2 enhancements

---

## Overview

Boris Cherny's tips represent **battle-tested practices** from the Claude Code team. Many align with V1 features, but several offer opportunities for V2 enhancement.

| Tip | V1 Status | V2 Enhancement |
|-----|-----------|----------------|
| Parallel worktrees | Partial (swarm) | Native worktree orchestration |
| Plan mode | Yes (plan-approval) | Staff engineer review pattern |
| CLAUDE.md self-improvement | Manual | Automatic rule generation |
| Skills creation | Yes (68 skills) | Skill scaffolding wizard |
| Bug fixes | Yes (/cc-fix) | Zero-config "just fix" mode |
| Advanced prompting | Partial | Prompting patterns library |
| Terminal setup | No | Statusline + environment skills |
| Subagents | Yes (15 agents) | Opus permission gateway |
| Data & analytics | No | Database/analytics skills |
| Learning mode | No | Explanatory output + presentations |

---

## Detailed Integration Plan

### 1. Native Git Worktree Orchestration

**Boris's Tip:** *"Spin up 3–5 git worktrees at once, each running its own Claude session in parallel."*

**V1 Gap:** Swarm mode exists but doesn't explicitly manage worktrees.

**V2 Enhancement:**

```yaml
# New skill: worktree-orchestrator
name: worktree-orchestrator
version: 1.0.0
description: Manage parallel development across git worktrees
triggers:
  - "parallel development"
  - "multiple features"
  - "worktree"

capabilities:
  - Create named worktrees (feature-a, feature-b, analysis)
  - Spawn Claude sessions per worktree
  - Coordinate results across worktrees
  - Shell aliases generation (za, zb, zc)
  - Dedicated analysis worktree for logs/queries
```

**New Commands:**
- `/cc-worktree create [name]` — Create named worktree with Claude session
- `/cc-worktree list` — Show active worktrees and their status
- `/cc-worktree sync` — Merge results from parallel worktrees
- `/cc-worktree analysis` — Dedicated read-only worktree for analysis

**Integration with Swarm:**
```
┌─────────────────────────────────────────────────────────────────┐
│                    WORKTREE ORCHESTRATOR                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   main/              feature-a/         feature-b/    analysis/ │
│   ┌─────────┐       ┌─────────┐       ┌─────────┐   ┌─────────┐│
│   │ Leader  │       │ Worker  │       │ Worker  │   │ Reader  ││
│   │ Claude  │       │ Claude  │       │ Claude  │   │ Claude  ││
│   └─────────┘       └─────────┘       └─────────┘   └─────────┘│
│        │                 │                 │              │     │
│        └─────────────────┴─────────────────┴──────────────┘     │
│                              │                                   │
│                    ┌─────────────────┐                          │
│                    │ Result Synthesis │                          │
│                    └─────────────────┘                          │
└─────────────────────────────────────────────────────────────────┘
```

---

### 2. Staff Engineer Review Pattern

**Boris's Tip:** *"One person has one Claude write the plan, then they spin up a second Claude to review it as a staff engineer."*

**V1 Gap:** Plan approval exists but doesn't have adversarial review.

**V2 Enhancement:**

```yaml
# New pattern: staff-engineer-review
name: staff-engineer-review
version: 1.0.0
description: Adversarial plan review before implementation

workflow:
  1. Claude A creates plan
  2. Claude B reviews as staff engineer (critical, finds gaps)
  3. Claude A addresses feedback
  4. Claude B approves or requests changes
  5. Only then: implementation begins

review_criteria:
  - Edge cases covered?
  - Error handling complete?
  - Security implications?
  - Performance considerations?
  - Breaking changes identified?
  - Tests specified?
  - Rollback plan exists?
```

**New Skill:**
```yaml
name: adversarial-review
triggers:
  - complex plan
  - risky changes
  - architecture decisions

behavior: |
  After creating a plan, automatically spawn a second agent
  with the "staff engineer" persona to critically review.

  The reviewer should:
  - Challenge assumptions
  - Find edge cases
  - Identify risks
  - Suggest improvements
  - Block if not production-ready
```

**Integration with Plan Mode:**
```
User Request
     │
     ▼
┌─────────────┐
│  PLAN MODE  │
│  (Claude A) │
└─────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│     STAFF ENGINEER REVIEW           │
│     (Claude B - Adversarial)        │
│                                     │
│  "I'm reviewing this as a staff     │
│   engineer. Here are my concerns:"  │
│                                     │
│  - [ ] Edge case: empty input       │
│  - [ ] Security: SQL injection      │
│  - [ ] Performance: N+1 queries     │
│  - [ ] Missing: rollback plan       │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────┐
│  REVISION   │
│  (Claude A) │
└─────────────┘
     │
     ▼
┌─────────────┐
│  APPROVED   │
│  (Claude B) │
└─────────────┘
     │
     ▼
   EXECUTE
```

---

### 3. Automatic CLAUDE.md Self-Improvement

**Boris's Tip:** *"After every correction, end with: 'Update your CLAUDE.md so you don't make that mistake again.' Claude is eerily good at writing rules for itself."*

**V1 Gap:** Feedback system exists but doesn't auto-update CLAUDE.md.

**V2 Enhancement:**

```yaml
# New skill: self-rule-generator
name: self-rule-generator
version: 1.0.0
description: Automatically generate rules from corrections

triggers:
  - user correction
  - repeated mistake
  - "don't do that again"
  - error recovery

behavior: |
  When corrected by user:
  1. Identify the mistake pattern
  2. Generate a rule to prevent recurrence
  3. Propose addition to CLAUDE.md
  4. Track rule effectiveness over time
  5. Prune rules that don't reduce errors
```

**New Event:**
```yaml
event: correction.received
payload:
  mistake: string
  correction: string
  context: string

subscribers:
  - self-rule-generator
```

**Auto-Generated Rules Format:**
```markdown
## Auto-Generated Rules

<!-- Generated by self-rule-generator -->
<!-- Effectiveness: 94% error reduction -->

### Rule: No hardcoded API keys
- **Generated:** 2024-01-15
- **Trigger:** Corrected for including API key in commit
- **Rule:** Never include API keys, tokens, or secrets in code. Use environment variables.
- **Effectiveness:** 12 prevented / 12 opportunities = 100%

### Rule: Always run tests before commit
- **Generated:** 2024-01-10
- **Trigger:** Corrected for breaking tests
- **Rule:** Run `npm test` before every commit. Never commit with failing tests.
- **Effectiveness:** 8 prevented / 9 opportunities = 89%
```

**Effectiveness Tracking:**
```
┌─────────────────────────────────────────────────────────────────┐
│                    RULE EFFECTIVENESS                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Rule                          | Triggers | Prevented | Rate    │
│  ─────────────────────────────────────────────────────────────  │
│  No hardcoded secrets          | 12       | 12        | 100%    │
│  Run tests before commit       | 9        | 8         | 89%     │
│  Use TypeScript strict mode    | 6        | 5         | 83%     │
│  Check for null before access  | 15       | 11        | 73%     │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  Rules below 50% effectiveness are candidates for removal.       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

### 4. Skill Scaffolding Wizard

**Boris's Tip:** *"If you do something more than once a day, turn it into a skill or command."*

**V1 Gap:** Creating skills requires manual file creation and index updates.

**V2 Enhancement:**

```yaml
# New command: /cc-skill-wizard
name: skill-wizard
description: Interactive skill creation from repeated actions

workflow:
  1. Detect repeated action patterns
  2. Suggest skill creation
  3. Generate skill from template
  4. Validate against schema
  5. Auto-add to registry
  6. Test the skill
```

**Pattern Detection:**
```yaml
# New skill: repetition-detector
name: repetition-detector
triggers:
  - session end
  - manual invocation

behavior: |
  Analyze session history for repeated patterns:
  - Same command run 3+ times
  - Same file edited multiple times
  - Same search pattern used repeatedly
  - Same workflow executed multiple times

  Suggest: "I noticed you did X three times today.
           Want me to create a skill for that?"
```

**Skill Templates:**
```yaml
templates:
  - automation: "Run X when Y happens"
  - workflow: "Multi-step process for Z"
  - checker: "Validate X meets criteria"
  - generator: "Create X from template"
  - transformer: "Convert X to Y"
```

---

### 5. Zero-Config "Just Fix" Mode

**Boris's Tip:** *"Just say 'Go fix the failing CI tests.' Don't micromanage how."*

**V1 Gap:** /cc-fix exists but requires context specification.

**V2 Enhancement:**

```yaml
# Enhanced skill: zero-config-fix
name: zero-config-fix
version: 2.0.0
description: Fix issues with minimal input

triggers:
  - "fix"
  - "fix it"
  - "just fix"
  - "go fix"

intelligence:
  - Detect what's broken (CI, tests, lint, build)
  - Identify root cause
  - Apply fix
  - Verify fix works
  - No questions asked (unless truly ambiguous)
```

**Context Detection:**
```
User says: "fix"

Engine detects:
├── CI failing? → Read CI logs, fix failures
├── Tests failing? → Run tests, fix failures
├── Lint errors? → Run linter, fix errors
├── Build broken? → Check build output, fix
├── Bug report pasted? → Parse, reproduce, fix
├── Error in terminal? → Analyze, fix
└── Nothing obvious? → Ask "What should I fix?"
```

**MCP Integration (Slack/Discord):**
```yaml
# New skill: bug-thread-fixer
name: bug-thread-fixer
triggers:
  - slack thread pasted
  - discord thread pasted
  - bug report pasted

behavior: |
  1. Parse the bug thread/report
  2. Extract:
     - Error messages
     - Steps to reproduce
     - Expected vs actual behavior
     - Environment details
  3. Reproduce locally
  4. Identify root cause
  5. Implement fix
  6. Verify fix
  7. Create PR with context from thread
```

---

### 6. Prompting Patterns Library

**Boris's Tip:** *"Challenge Claude. Say 'Grill me on these changes...' or 'Knowing everything you know now, scrap this and implement the elegant solution.'"*

**V1 Gap:** No formalized prompting patterns.

**V2 Enhancement:**

```yaml
# New: patterns/prompting/
patterns:
  - name: adversarial-review
    prompt: "Grill me on these changes and don't make a PR until I pass your test."
    use_when: "Before finalizing changes"

  - name: prove-it-works
    prompt: "Prove to me this works by diffing behavior between main and this branch."
    use_when: "Verifying feature changes"

  - name: elegant-redo
    prompt: "Knowing everything you know now, scrap this and implement the elegant solution."
    use_when: "After mediocre first attempt"

  - name: rubber-duck
    prompt: "Explain this code to me like I'm a junior developer."
    use_when: "Understanding complex code"

  - name: edge-case-hunt
    prompt: "What edge cases am I missing? Be exhaustive."
    use_when: "Before marking complete"

  - name: security-mindset
    prompt: "You're a malicious attacker. How would you exploit this?"
    use_when: "Security review"

  - name: future-proof
    prompt: "What will make this code painful to maintain in 6 months?"
    use_when: "Architecture decisions"
```

**Prompting Skill:**
```yaml
name: smart-prompting
triggers:
  - quality gate failed
  - stuck in loop
  - mediocre output

behavior: |
  Automatically apply appropriate prompting pattern:

  - Output not good enough? → elegant-redo
  - Missing edge cases? → edge-case-hunt
  - Security concern? → security-mindset
  - Verification needed? → prove-it-works
```

---

### 7. Terminal & Environment Skills

**Boris's Tip:** *"Use /statusline to customize your status bar... Use voice dictation."*

**V1 Gap:** No terminal setup skills.

**V2 Enhancement:**

```yaml
# New skill: environment-optimizer
name: environment-optimizer
version: 1.0.0
description: Optimize terminal and environment setup

capabilities:
  - Statusline configuration
  - Shell aliases generation
  - Terminal tab naming
  - Tmux configuration
  - Voice dictation awareness
  - Git worktree shortcuts
```

**Statusline Integration:**
```yaml
# New skill: smart-statusline
name: smart-statusline
triggers:
  - session start
  - context change
  - branch change

display:
  - Context usage: [████████░░] 80%
  - Current branch: feature/auth
  - Phase: EXECUTE (4/10)
  - Work items: 3 remaining
  - Model: sonnet
```

**Voice Dictation Awareness:**
```yaml
# New skill: voice-input-handler
name: voice-input-handler
triggers:
  - long natural language input
  - conversational tone
  - dictation artifacts

behavior: |
  Detect voice-dictated input (longer, more conversational)
  and extract structured intent:

  Input: "Okay so I need you to go ahead and fix that
         authentication bug we talked about earlier,
         you know the one where users can't log in
         after their session expires"

  Extracted: {
    action: "fix",
    target: "authentication bug",
    context: "session expiration login failure"
  }
```

---

### 8. Opus Permission Gateway

**Boris's Tip:** *"Route permission requests to Opus 4.5 via a hook — let it scan for attacks and auto-approve the safe ones."*

**V1 Gap:** Permission handling is manual or basic auto-approve.

**V2 Enhancement:**

```yaml
# New hook: opus-permission-gateway
name: opus-permission-gateway
event: PermissionRequest
model: opus

behavior: |
  For every permission request:
  1. Analyze the requested action
  2. Check for:
     - Injection attacks
     - Data exfiltration
     - Destructive operations
     - Scope creep
  3. If safe: auto-approve
  4. If suspicious: escalate to user
  5. If dangerous: block and alert

safety_checks:
  - Command injection patterns
  - File system escape attempts
  - Network exfiltration
  - Credential access
  - Destructive git operations
  - Production environment detection
```

**Decision Matrix:**
```
┌─────────────────────────────────────────────────────────────────┐
│                  OPUS PERMISSION GATEWAY                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Request Type        │ Risk Level │ Action                      │
│  ────────────────────┼────────────┼─────────────────────────────│
│  Read local file     │ Low        │ Auto-approve                │
│  Write to project    │ Low        │ Auto-approve                │
│  Run tests           │ Low        │ Auto-approve                │
│  Git commit          │ Low        │ Auto-approve                │
│  Install package     │ Medium     │ Check package, then approve │
│  Run arbitrary bash  │ Medium     │ Analyze command first       │
│  Access .env         │ High       │ Escalate to user            │
│  Push to main        │ High       │ Escalate to user            │
│  Delete files        │ High       │ Escalate to user            │
│  Network request     │ Variable   │ Check destination           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

### 9. Database & Analytics Skills

**Boris's Tip:** *"Ask Claude Code to use the bq CLI to pull and analyze metrics... I haven't written a line of SQL in 6+ months."*

**V1 Gap:** No database/analytics skills.

**V2 Enhancement:**

```yaml
# New skill category: analytics/
skills:
  - name: bigquery-analyst
    description: BigQuery queries via bq CLI
    capabilities:
      - Write and run BQ queries
      - Analyze results
      - Generate reports
      - Create visualizations

  - name: postgres-analyst
    description: PostgreSQL via psql
    capabilities:
      - Query databases
      - Analyze schemas
      - Optimize queries
      - Generate migrations

  - name: sqlite-analyst
    description: SQLite analysis
    capabilities:
      - Local database queries
      - Schema exploration
      - Data export

  - name: metrics-dashboard
    description: Pull and visualize metrics
    capabilities:
      - Connect to data sources
      - Build dashboards
      - Anomaly detection
      - Trend analysis
```

**Universal Database Skill:**
```yaml
name: universal-db-analyst
triggers:
  - "query"
  - "analyze data"
  - "metrics"
  - "database"

detection:
  - BigQuery: Look for bq CLI, GCP config
  - PostgreSQL: Look for psql, DATABASE_URL
  - MySQL: Look for mysql CLI, connection config
  - SQLite: Look for .db files
  - MongoDB: Look for mongosh, connection strings

behavior: |
  1. Detect available databases
  2. Understand schema
  3. Write appropriate query
  4. Execute via CLI/MCP
  5. Analyze and visualize results
  6. Explain findings
```

**Analytics Workflows:**
```yaml
# New command: /cc-analytics
name: analytics
description: Run analytics queries and generate insights

subcommands:
  - /cc-analytics query "show me daily active users"
  - /cc-analytics trend "signups over last 30 days"
  - /cc-analytics anomaly "detect unusual patterns"
  - /cc-analytics report "weekly metrics summary"
```

---

### 10. Learning & Explanation Mode

**Boris's Tip:** *"Enable the 'Explanatory' output style... Have Claude generate a visual HTML presentation explaining unfamiliar code."*

**V1 Gap:** No learning/explanatory mode.

**V2 Enhancement:**

```yaml
# New config option: output_style
output_styles:
  - name: concise
    description: Minimal output, just results
    default: true

  - name: explanatory
    description: Explain the why behind every change
    use_when: "learning new codebase"

  - name: teaching
    description: Detailed explanations for learning
    use_when: "onboarding, education"

  - name: documentation
    description: Generate docs alongside changes
    use_when: "building documentation"
```

**Presentation Generator:**
```yaml
# New skill: presentation-generator
name: presentation-generator
triggers:
  - "explain this code"
  - "create presentation"
  - "help me understand"
  - "teach me"

output_formats:
  - HTML slides (reveal.js)
  - Markdown presentation
  - ASCII diagrams
  - Interactive notebook

capabilities:
  - Code walkthrough with annotations
  - Architecture diagrams
  - Flow visualizations
  - Before/after comparisons
```

**ASCII Diagram Generator:**
```yaml
# New skill: diagram-generator
name: diagram-generator
triggers:
  - "draw diagram"
  - "visualize"
  - "show architecture"

diagram_types:
  - Sequence diagrams
  - Architecture diagrams
  - Flow charts
  - Entity relationships
  - State machines
  - Dependency graphs

output: |
  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
  │   Client    │────▶│   Server    │────▶│  Database   │
  └─────────────┘     └─────────────┘     └─────────────┘
        │                   │                    │
        │    HTTP POST      │    SQL INSERT      │
        │   /api/users      │   users table      │
        ▼                   ▼                    ▼
```

**Spaced Repetition Learning:**
```yaml
# New skill: learning-companion
name: learning-companion
triggers:
  - "teach me"
  - "help me learn"
  - "quiz me"

workflow:
  1. User explains their understanding
  2. Claude identifies gaps
  3. Claude asks targeted questions
  4. Claude provides feedback
  5. Store for spaced repetition
  6. Revisit at optimal intervals
```

---

## Implementation Priority

Based on impact and alignment with V2 vision:

### P0 — Critical for V2 Launch

| Enhancement | Rationale |
|-------------|-----------|
| Automatic CLAUDE.md self-improvement | Core to continuous learning vision |
| Staff engineer review pattern | Core to quality and autonomy |
| Zero-config "just fix" mode | Core to minimal intervention vision |
| Opus permission gateway | Core to autonomous safety |

### P1 — High Value

| Enhancement | Rationale |
|-------------|-----------|
| Skill scaffolding wizard | Enables extensibility vision |
| Prompting patterns library | Improves output quality |
| Database/analytics skills | Swiss army knife completeness |

### P2 — Nice to Have

| Enhancement | Rationale |
|-------------|-----------|
| Native worktree orchestration | Power user productivity |
| Learning/explanation mode | Onboarding and education |
| Terminal/environment skills | Developer experience |

---

## Summary

Boris's tips reinforce our V2 vision and identify specific gaps:

| V2 Principle | Boris Alignment | Gap Identified |
|--------------|-----------------|----------------|
| Autonomous by default | "Just say fix" | Zero-config fixes |
| Self-aware meta-cognition | Staff engineer review | Adversarial self-review |
| Continuous self-improvement | CLAUDE.md rules | Auto rule generation |
| Swiss army knife | Database skills | Analytics capabilities |
| Minimal intervention | Permission gateway | Opus auto-approve |

**Key Insight:** Boris's tips come from real-world usage patterns. V2 should make these patterns **first-class features**, not workarounds.

---

*Integration plan based on Boris Cherny's Claude Code tips*
