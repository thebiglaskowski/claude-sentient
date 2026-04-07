# Feature Documentation

> One doc per feature. Claude reads the relevant doc before touching any code.
> Working on a feature? Find it in the table below and read the doc first.

## Lookup Table

| Feature | Doc | Description |
|---------|-----|-------------|
| Autonomous Loop | `documentation/01-autonomous-loop.md` | cs-loop 7-phase engine, model routing, MCP integration |
| Session Lifecycle | `documentation/02-session-lifecycle.md` | session-start/end/pre-compact hooks, state files, archive |
| Security Gates | `documentation/03-security-gates.md` | bash-validator, file-validator, dangerous patterns, protected paths |
| Context Injection | `documentation/04-context-injection.md` | context-injector, topic detection, context degradation thresholds |
| Quality Gates | `documentation/05-quality-gates.md` | gate-monitor, dod-verifier, gate_history.json, integrity checks |
| Agent Teams | `documentation/06-agent-teams.md` | cs-team, teammate-idle/task-completed hooks, team-state.json |
| Profile System | `documentation/07-profile-system.md` | 9 language profiles, detection, model routing, environment detection |
| Agent Roles | `documentation/08-agent-roles.md` | agents/*.yaml + .claude/agents/*.md dual system, 9 roles |
| Rules System | `documentation/09-rules-system.md` | 15 rule files, keyword loading, path-scoped rules |
| Command System | `documentation/10-command-system.md` | 15 cs-*.md commands, frontmatter schema, skill chaining |
| Installation | `documentation/11-installation.md` | install.sh/ps1, CHECKSUMS.sha256, global permissions |
| Worktree & Config Observability | `documentation/12-worktree-config-observability.md` | worktree-lifecycle, config-watcher hooks |
| Planning | `documentation/13-planning.md` | cs-plan, EnterPlanMode/ExitPlanMode, plan structure |
| Memory & Learning | `documentation/14-memory-learning.md` | cs-learn, learnings.md, compact-context, anchored summarization |
| Multi-Model Routing | `documentation/15-multi-model-routing.md` | cs-multi, per-phase model assignment, multi-model.json |

## Doc-First Workflow

When working on a feature:
1. Find the feature in the lookup table above
2. Read the full doc before writing any code
3. If no doc exists, run `/cs-docs "feature name"` to generate one
4. Update the doc if implementation reveals a mismatch

## Quality Bar

A good feature doc lets Claude implement the feature correctly without reading source code.
Business rules matter more than API shapes. Claude can infer patterns — it cannot infer limits,
cascade rules, permission gates, or state machines.
