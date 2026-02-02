# V1 Prompt Reference Index

When you need deeper guidance than the compact rules provide, these full prompts from v1 are available in `reference/v1/`.

> **Usage**: Load the full prompt content when working on complex tasks that require comprehensive guidance beyond what the short-form rules provide.

---

## Quick Reference

| Need | V1 Prompt | Path | When to Use |
|------|-----------|------|-------------|
| Detailed code review | CODE_REVIEW | `reference/v1/quality/` | PR reviews, audit |
| Security audit | SECURITY_AUDIT | `reference/v1/quality/` | Security-critical work |
| Full codebase audit | CODEBASE_AUDIT | `reference/v1/quality/` | Deep assessment |
| Performance audit | PERFORMANCE_AUDIT | `reference/v1/quality/` | Optimization |
| Feature specification | FEATURE_SPEC_WRITER | `reference/v1/planning/` | New feature design |
| Blueprint validation | BLUEPRINT_AUDITOR | `reference/v1/planning/` | Pre-build validation |
| Bug hunting | BUG_HUNT | `reference/v1/quality/` | Systematic debugging |
| Test coverage | TEST_COVERAGE_GATE | `reference/v1/quality/` | Coverage enforcement |
| Dependency audit | DEPENDENCY_AUDIT | `reference/v1/quality/` | Dependency review |
| Technical spike | SPIKE_RESEARCH | `reference/v1/execution/` | Research tasks |
| Refactoring | REFACTORING_ENGINE | `reference/v1/refactoring/` | Safe refactors |
| Migration planning | MIGRATION_PLANNER | `reference/v1/operations/` | System migrations |
| Incident analysis | INCIDENT_POSTMORTEM | `reference/v1/operations/` | Post-incident |
| Release checklist | RELEASE_CHECKLIST | `reference/v1/operations/` | Pre-release |
| Tech debt tracking | TECH_DEBT_TRACKER | `reference/v1/operations/` | Debt management |

---

## Agents (Specialized Expert Analysis)

| Agent | Path | Expertise |
|-------|------|-----------|
| ui-ux-expert | `reference/v1/template/.claude/agents/` | Web UI/UX, modern design |
| security-analyst | `reference/v1/template/.claude/agents/` | Security audits |
| performance-optimizer | `reference/v1/template/.claude/agents/` | Performance tuning |
| code-reviewer | `reference/v1/template/.claude/agents/` | Code review |
| test-engineer | `reference/v1/template/.claude/agents/` | Test strategy |
| documentation-writer | `reference/v1/template/.claude/agents/` | Documentation |
| database-expert | `reference/v1/template/.claude/agents/` | Database optimization |
| devops-engineer | `reference/v1/template/.claude/agents/` | CI/CD, infrastructure |
| accessibility-expert | `reference/v1/template/.claude/agents/` | WCAG compliance |
| seo-expert | `reference/v1/template/.claude/agents/` | Search optimization |

---

## Rules (Topic-Specific Standards)

| Rule | Path | Contents |
|------|------|----------|
| security | `reference/v1/template/.claude/rules/` | OWASP, auth, secrets |
| testing | `reference/v1/template/.claude/rules/` | Coverage, TDD, mocks |
| api-design | `reference/v1/template/.claude/rules/` | REST, responses |
| database | `reference/v1/template/.claude/rules/` | Schema, indexes |
| performance | `reference/v1/template/.claude/rules/` | Caching, Web Vitals |
| code-quality | `reference/v1/template/.claude/rules/` | Complexity, naming |
| documentation | `reference/v1/template/.claude/rules/` | README, changelog |
| git-workflow | `reference/v1/template/.claude/rules/` | Commits, PRs |
| error-handling | `reference/v1/template/.claude/rules/` | Error types, logging |
| logging | `reference/v1/template/.claude/rules/` | Structured logs |
| ui-ux-design | `reference/v1/template/.claude/rules/` | Spacing, typography, a11y |
| terminal-ui | `reference/v1/template/.claude/rules/` | CLI output, progress |
| prompt-engineering | `reference/v1/template/.claude/rules/` | AI prompts |

---

## How to Load Full References

When you need comprehensive guidance beyond the compact Claude Sentient rules:

```markdown
# In conversation
"Load the full CODE_REVIEW prompt from v1 for this review"

# Or reference directly
"Apply the v1 security-analyst agent guidelines for this audit"
```

The full prompts provide:
- Detailed step-by-step processes
- Comprehensive checklists
- Output format templates
- Edge case handling
- Examples and anti-patterns

---

## When to Use Full vs Compact

| Use Compact (Claude Sentient) | Use Full (V1 Reference) |
|-------------------------------|-------------------------|
| Quick tasks | Deep analysis |
| Standard patterns | Complex scenarios |
| Familiar territory | Unfamiliar domain |
| Time-constrained | Quality-critical |
| Simple features | Security/compliance |

---

## V1 Library Structure

```
reference/v1/
├── planning/          # Before building
│   ├── FEATURE_SPEC_WRITER.md
│   └── BLUEPRINT_AUDITOR.md
├── execution/         # During building
│   ├── PROJECT_EXECUTION.md
│   └── SPIKE_RESEARCH.md
├── quality/           # Verification
│   ├── CODE_REVIEW.md
│   ├── SECURITY_AUDIT.md
│   ├── CODEBASE_AUDIT.md
│   └── ...
├── operations/        # Post-build
│   ├── RELEASE_CHECKLIST.md
│   └── MIGRATION_PLANNER.md
├── refactoring/       # Code improvement
│   └── REFACTORING_ENGINE.md
├── documentation/     # Docs
│   └── ...
└── template/.claude/  # Project template
    ├── agents/        # Expert agents
    ├── rules/         # Topic rules
    ├── commands/      # Slash commands
    └── ...
```

---

## Note

Claude Sentient's compact rules (`rules/*.md`) are derived from these full v1 prompts. The compact versions cover 80% of use cases. Load full references for the remaining 20% requiring deep expertise.
