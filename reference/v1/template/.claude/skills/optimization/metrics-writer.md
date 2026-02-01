---
name: metrics-writer
description: Write structured metrics to JSONL files for analysis
version: 1.0.0
triggers:
  - "log metric"
  - "record metric"
  - "write to metrics"
  - "track this"
model: haiku
tags: [optimization, metrics, logging]
context: inherit
---

# Metrics Writer

<context>
Structured metrics enable data-driven decisions about prompt effectiveness,
command usage, and development patterns. JSONL format allows easy querying
with tools like jq while remaining human-readable.
</context>

<role>
You are a metrics recording system that:
- Writes structured JSONL entries to appropriate files
- Maintains consistent schemas per metric type
- Timestamps all entries automatically
- Preserves data integrity
</role>

---

## File Structure

```
.claude/metrics/
├── commands.jsonl      # Command usage metrics
├── skills.jsonl        # Skill activation metrics
├── agents.jsonl        # Agent spawn and results
├── sessions.jsonl      # Session summaries
├── quality.jsonl       # Quality gate results
├── performance.jsonl   # Performance measurements
└── feedback.jsonl      # Prompt feedback events
```

---

## Metric Schemas

<schemas>

### Command Metric
```jsonl
{"ts":"2026-01-29T10:30:00Z","type":"command","name":"/review","status":"success","duration_ms":45000,"model":"sonnet","files_touched":3}
```

### Skill Metric
```jsonl
{"ts":"2026-01-29T10:30:00Z","type":"skill","name":"pre-commit","trigger":"ready to commit","activated":true}
```

### Agent Metric
```jsonl
{"ts":"2026-01-29T10:30:00Z","type":"agent","name":"security-analyst","status":"complete","findings":{"s0":0,"s1":2,"s2":5},"duration_ms":120000}
```

### Session Metric
```jsonl
{"ts":"2026-01-29T10:30:00Z","type":"session","id":"abc123","duration_min":45,"commands":12,"tokens_in":50000,"tokens_out":25000}
```

### Quality Metric
```jsonl
{"ts":"2026-01-29T10:30:00Z","type":"quality","gate":"test-coverage","passed":true,"value":87,"threshold":80}
```

### Performance Metric
```jsonl
{"ts":"2026-01-29T10:30:00Z","type":"perf","operation":"build","duration_ms":3200,"improved":true,"baseline_ms":4500}
```

### Feedback Metric
```jsonl
{"ts":"2026-01-29T10:30:00Z","type":"feedback","prompt":"/secure","outcome":"failure","root_cause":"missing_example","severity":"medium"}
```

</schemas>

---

## Writing Metrics

<instructions>

<step number="1">
**Determine metric type** based on what's being recorded:
- Command completion → commands.jsonl
- Skill activation → skills.jsonl
- Agent results → agents.jsonl
- Session end → sessions.jsonl
- Quality check → quality.jsonl
- Performance measurement → performance.jsonl
- Prompt feedback → feedback.jsonl
</step>

<step number="2">
**Build the JSONL entry** with required fields:
```json
{
  "ts": "[ISO 8601 timestamp]",
  "type": "[metric type]",
  // ... type-specific fields
}
```
</step>

<step number="3">
**Append to the appropriate file**:
```bash
echo '{"ts":"2026-01-29T10:30:00Z",...}' >> .claude/metrics/[type].jsonl
```
</step>

<step number="4">
**Verify entry** was written (optional for critical metrics):
```bash
tail -1 .claude/metrics/[type].jsonl | jq .
```
</step>

</instructions>

---

## Auto-Recording

### After Command Completion
```
Automatically append to commands.jsonl:
{
  "ts": "[now]",
  "type": "command",
  "name": "[command]",
  "status": "[success|failure]",
  "duration_ms": [elapsed],
  "model": "[model used]",
  "files_touched": [count]
}
```

### After Skill Activation
```
Automatically append to skills.jsonl:
{
  "ts": "[now]",
  "type": "skill",
  "name": "[skill]",
  "trigger": "[what triggered it]",
  "activated": true
}
```

### After Agent Completion
```
Automatically append to agents.jsonl:
{
  "ts": "[now]",
  "type": "agent",
  "name": "[agent]",
  "status": "[complete|timeout|error]",
  "findings": { "s0": N, "s1": N, "s2": N },
  "duration_ms": [elapsed]
}
```

---

## Querying Metrics

<examples>

<example>
<input>Show command success rate</input>
<output>
```bash
cat .claude/metrics/commands.jsonl | jq -s '
  group_by(.name) |
  map({
    command: .[0].name,
    total: length,
    success: [.[] | select(.status=="success")] | length,
    rate: ([.[] | select(.status=="success")] | length) / length * 100
  })'
```
</output>
</example>

<example>
<input>Find slowest commands</input>
<output>
```bash
cat .claude/metrics/commands.jsonl | jq -s '
  sort_by(-.duration_ms) |
  .[0:5] |
  .[] | {name, duration_ms, ts}'
```
</output>
</example>

<example>
<input>Get agent findings summary</input>
<output>
```bash
cat .claude/metrics/agents.jsonl | jq -s '
  {
    total_runs: length,
    s0_total: [.[].findings.s0] | add,
    s1_total: [.[].findings.s1] | add,
    s2_total: [.[].findings.s2] | add
  }'
```
</output>
</example>

<example>
<input>Track quality gate trends</input>
<output>
```bash
cat .claude/metrics/quality.jsonl | jq -s '
  group_by(.gate) |
  map({
    gate: .[0].gate,
    pass_rate: ([.[] | select(.passed)] | length) / length * 100,
    avg_value: ([.[].value] | add) / length
  })'
```
</output>
</example>

</examples>

---

## Aggregation Reports

### Daily Summary
```bash
# Get today's metrics
TODAY=$(date +%Y-%m-%d)
cat .claude/metrics/*.jsonl | jq -s --arg date "$TODAY" '
  [.[] | select(.ts | startswith($date))] |
  group_by(.type) |
  map({
    type: .[0].type,
    count: length
  })'
```

### Weekly Report
```bash
# Generate weekly summary
cat .claude/metrics/commands.jsonl | jq -s '
  {
    period: "last 7 days",
    total_commands: length,
    unique_commands: [.[].name] | unique | length,
    success_rate: ([.[] | select(.status=="success")] | length) / length * 100,
    avg_duration_ms: ([.[].duration_ms] | add) / length
  }'
```

---

## Initialization

When setting up metrics for a project:

```bash
# Create metrics directory
mkdir -p .claude/metrics

# Initialize empty files
touch .claude/metrics/commands.jsonl
touch .claude/metrics/skills.jsonl
touch .claude/metrics/agents.jsonl
touch .claude/metrics/sessions.jsonl
touch .claude/metrics/quality.jsonl
touch .claude/metrics/performance.jsonl
touch .claude/metrics/feedback.jsonl

# Add to gitignore (metrics are local)
echo ".claude/metrics/" >> .gitignore
```

---

## Rotation Policy

<rules>
- Keep last 90 days of metrics by default
- Archive older metrics to `.claude/metrics/archive/`
- Compress archived files with gzip
- Delete archives older than 1 year
</rules>

```bash
# Rotation script
find .claude/metrics -name "*.jsonl" -mtime +90 -exec gzip {} \; -exec mv {}.gz .claude/metrics/archive/ \;
find .claude/metrics/archive -name "*.gz" -mtime +365 -delete
```

---

## Privacy

<rules>
- Never log file contents or code snippets
- Never log credentials, tokens, or secrets
- Sanitize file paths (relative only)
- Aggregate personal patterns (no raw queries)
- Respect opt-out via settings.json
</rules>

### Check Opt-Out
```bash
# In settings.json
{
  "metrics": {
    "enabled": false  # Disables all metric writing
  }
}
```
