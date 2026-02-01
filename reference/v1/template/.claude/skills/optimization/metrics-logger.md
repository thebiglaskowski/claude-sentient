---
name: metrics-logger
description: Track prompt and command usage for optimization insights
model: haiku
---

# Metrics Logger

Track prompt and command usage for optimization insights.

## Description

Logs usage of commands and skills to identify patterns and improvements.
Triggers on: "show metrics", "usage stats", "what's most used", "analytics".

## What Gets Tracked

### Command Usage
- Which `/commands` are run
- Frequency of use
- Success/failure outcomes

### Skill Activations
- Which skills auto-load
- Trigger patterns that activated them

### Session Patterns
- Session duration
- Commands per session
- Common command sequences

## Log Format

### Log File Location
`.claude/metrics/usage.log`

### Log Entry Format
```
TIMESTAMP|TYPE|NAME|OUTCOME|DURATION|NOTES
2024-01-15T10:30:00|command|/daily|success|45m|
2024-01-15T10:30:00|skill|pre-commit|activated||trigger: "ready to commit"
2024-01-15T11:15:00|command|/review|success|20m|
```

## Logging Process

### On Command Start
```markdown
<!-- Log entry -->
{timestamp}|command|{command_name}|started||
```

### On Command Complete
```markdown
<!-- Update entry -->
{timestamp}|command|{command_name}|{success/failure}|{duration}|{notes}
```

### On Skill Activation
```markdown
{timestamp}|skill|{skill_name}|activated||trigger: "{trigger_text}"
```

## Metrics Summary

When user asks for metrics:

```markdown
## Usage Metrics

**Period:** Last 30 days
**Sessions:** 45

### Most Used Commands
| Rank | Command | Count | Success Rate |
|------|---------|-------|--------------|
| 1 | /daily | 38 | 100% |
| 2 | /review | 22 | 95% |
| 3 | /test | 18 | 89% |
| 4 | /plan | 8 | 100% |
| 5 | /fix | 6 | 83% |

### Most Triggered Skills
| Rank | Skill | Activations | Common Trigger |
|------|-------|-------------|----------------|
| 1 | pre-commit | 45 | "commit" |
| 2 | model-routing | 30 | task complexity |
| 3 | gitignore-manager | 12 | "initialize" |

### Command Sequences
Common patterns:
1. `/plan` → `/daily` → `/review` (feature workflow)
2. `/fix` → `/test` → `/review` (bug fix workflow)
3. `/assess` → `/debt` → `/refactor` (maintenance workflow)

### Recommendations
- **High usage:** `/daily` - consider optimizing further
- **Low success:** `/fix` (83%) - review failure cases
- **Unused:** `/migrate`, `/postmortem` - may need better discoverability
```

## Privacy & Storage

### What's NOT Logged
- File contents
- Code snippets
- Personal information
- Credentials or secrets

### Log Rotation
```bash
# Keep last 90 days of logs
find .claude/metrics -name "*.log" -mtime +90 -delete
```

### Opt-Out
To disable metrics, add to `.claude/settings.json`:
```json
{
  "metrics": {
    "enabled": false
  }
}
```

## Implementation

### Initialize Metrics Directory
```bash
mkdir -p .claude/metrics
touch .claude/metrics/usage.log
```

### Log Helper (Conceptual)
When running commands, append to log:
```bash
echo "$(date -Iseconds)|command|$CMD|started||" >> .claude/metrics/usage.log
```

### Gitignore Metrics
Add to `.gitignore` (metrics are local, not shared):
```
.claude/metrics/
```

## Analysis Queries

### Commands by frequency
```bash
grep "|command|" .claude/metrics/usage.log | cut -d'|' -f3 | sort | uniq -c | sort -rn
```

### Failed commands
```bash
grep "|failure|" .claude/metrics/usage.log
```

### Skills by activation
```bash
grep "|skill|" .claude/metrics/usage.log | cut -d'|' -f3 | sort | uniq -c | sort -rn
```

## Insights for Optimization

Use metrics to:
1. **Identify heavy hitters** - Optimize most-used commands
2. **Find failure patterns** - Improve error handling
3. **Discover workflows** - Create compound commands for common sequences
4. **Deprecate unused** - Remove or improve undiscovered commands
