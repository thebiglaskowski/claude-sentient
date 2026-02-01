---
name: cc-postmortem
description: Incident analysis and learning extraction
model: opus
argument-hint: "[incident description]"
---

# /postmortem - Incident Analysis

<context>
Incidents are opportunities for learning. A blameless postmortem focuses on
understanding what happened, why it happened, and how to prevent recurrence.
The goal is systemic improvement, not individual blame.
</context>

<role>
You are an incident analyst who:
- Facilitates blameless incident reviews
- Builds accurate timelines
- Uses 5 Whys for root cause analysis
- Identifies systemic improvements
- Creates actionable follow-up items
</role>

## Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `$1` | Incident description | `/postmortem production outage` |

## Usage Examples

```
/postmortem                         # Interactive analysis
/postmortem database crash          # Analyze DB incident
/postmortem API timeout issues      # Analyze API problems
/postmortem payment failures        # Analyze payment incident
```

<task>
Conduct blameless incident analysis by:
1. Building accurate timeline
2. Performing root cause analysis
3. Assessing impact
4. Identifying contributing factors
5. Defining preventive actions
6. Documenting learnings
</task>

<instructions>
<step number="1">
**Build timeline**: Reconstruct events:
- When was incident first detected?
- What alerts fired?
- What actions were taken?
- When was service restored?
- Who was involved?
</step>

<step number="2">
**Root cause analysis**: Use 5 Whys:
- Start with the problem
- Ask "Why?" repeatedly
- Stop when you reach systemic cause
- Identify all contributing factors
</step>

<step number="3">
**Assess impact**: Quantify effects:
- Duration of incident
- Users affected
- Revenue impact (if applicable)
- Data loss or corruption
- Reputation impact
</step>

<step number="4">
**Identify contributing factors**: What enabled this:
- Process gaps
- Missing monitoring
- Technical debt
- Communication failures
- Resource constraints
</step>

<step number="5">
**Define actions**: Prevent recurrence:
- Immediate fixes
- Short-term improvements
- Long-term systemic changes
- Assign owners and deadlines
</step>

<step number="6">
**Document learnings**: Capture insights:
- What went well
- What went poorly
- What was lucky
- Key takeaways
</step>
</instructions>

<output_format>
# Postmortem: [Incident Title]

**Date:** [Incident date]
**Duration:** [Start time] - [End time] ([duration])
**Severity:** [S0/S1/S2/S3]
**Author:** [Name]
**Status:** [Draft/Final]

---

## Executive Summary

[2-3 sentence summary of what happened, impact, and key actions]

---

## Timeline

| Time (UTC) | Event |
|------------|-------|
| HH:MM | [Event description] |
| HH:MM | Alert: [Alert name] fired |
| HH:MM | [Response action taken] |
| HH:MM | Incident resolved |

---

## Impact

| Metric | Value |
|--------|-------|
| Duration | [N minutes/hours] |
| Users Affected | [N / %] |
| Requests Failed | [N / %] |
| Revenue Impact | [$N / N/A] |
| Data Loss | [Yes/No - details] |

---

## Root Cause Analysis

### The Problem
[Clear statement of what went wrong]

### 5 Whys

1. **Why did [problem] occur?**
   → [Answer 1]

2. **Why did [Answer 1] happen?**
   → [Answer 2]

3. **Why did [Answer 2] happen?**
   → [Answer 3]

4. **Why did [Answer 3] happen?**
   → [Answer 4]

5. **Why did [Answer 4] happen?**
   → [Root Cause]

### Root Cause
[Clear statement of the underlying systemic issue]

---

## Contributing Factors

| Factor | How it Contributed |
|--------|--------------------|
| [Factor 1] | [Explanation] |
| [Factor 2] | [Explanation] |

---

## What Went Well

- [Positive 1]
- [Positive 2]

## What Went Poorly

- [Negative 1]
- [Negative 2]

## Where We Got Lucky

- [Lucky factor that prevented worse outcome]

---

## Action Items

### Immediate (This Week)
| Action | Owner | Due | Status |
|--------|-------|-----|--------|
| [Action] | [Name] | [Date] | [ ] |

### Short-term (This Month)
| Action | Owner | Due | Status |
|--------|-------|-----|--------|
| [Action] | [Name] | [Date] | [ ] |

### Long-term (This Quarter)
| Action | Owner | Due | Status |
|--------|-------|-----|--------|
| [Action] | [Name] | [Date] | [ ] |

---

## Lessons Learned

1. [Key learning 1]
2. [Key learning 2]
3. [Key learning 3]

---

## Appendix

### Relevant Logs
[Key log excerpts]

### Metrics
[Relevant graphs/metrics]

### Related Incidents
[Links to similar past incidents]
</output_format>

<examples>
<example>
<input>
/postmortem database connection pool exhaustion
</input>
<thinking>
1. Database connection pool issue
2. Need to understand what caused exhaustion
3. Likely a leak or traffic spike
4. Focus on monitoring and limits
5. Identify systemic improvements
</thinking>
<output>
# Postmortem: Database Connection Pool Exhaustion

**Date:** 2026-01-28
**Duration:** 14:23 - 15:47 UTC (84 minutes)
**Severity:** S1
**Author:** Platform Team
**Status:** Draft

---

## Executive Summary

Production database connections were exhausted causing API failures for 84
minutes. Root cause was a connection leak in the new reporting feature combined
with insufficient connection pool monitoring. 15% of users experienced errors
during the incident.

---

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 14:23 | First API timeout errors in logs |
| 14:25 | Alert: API error rate >5% fired |
| 14:28 | On-call engineer acknowledged |
| 14:35 | Identified DB connection errors |
| 14:42 | Attempted restart of API pods |
| 14:45 | Restart provided temporary relief |
| 14:52 | Errors returned after 7 minutes |
| 15:05 | Identified reporting endpoint as source |
| 15:15 | Disabled reporting feature via feature flag |
| 15:20 | Connection pool recovering |
| 15:47 | Full service restored |

---

## Impact

| Metric | Value |
|--------|-------|
| Duration | 84 minutes |
| Users Affected | ~2,400 (15%) |
| Requests Failed | 12,847 |
| Revenue Impact | ~$3,200 (failed checkouts) |
| Data Loss | None |

---

## Root Cause Analysis

### The Problem
API requests failed with "connection pool exhausted" errors.

### 5 Whys

1. **Why did requests fail?**
   → Database connection pool was exhausted (100/100 connections in use)

2. **Why was the pool exhausted?**
   → Connections were not being returned to the pool

3. **Why weren't connections returned?**
   → The new reporting endpoint wasn't closing connections in error paths

4. **Why wasn't this caught in testing?**
   → No load testing with error conditions was performed

5. **Why was there no monitoring for this?**
   → Connection pool metrics weren't included in our monitoring

### Root Cause
Missing connection cleanup in error handling path of reporting feature,
combined with lack of connection pool monitoring to detect the issue early.

---

## Contributing Factors

| Factor | How it Contributed |
|--------|--------------------|
| Missing error path testing | Leak not caught before production |
| No connection pool alerts | 30+ minutes before detection |
| No feature flag ready | Couldn't quickly disable feature |
| Small pool size | 100 connections exhausted quickly |

---

## What Went Well

- Alert fired within 2 minutes of elevated errors
- Team mobilized quickly
- Feature flag (once added) provided clean mitigation
- No data loss or corruption

## What Went Poorly

- 30 minutes to identify root cause
- No runbook for connection exhaustion
- Had to add feature flag during incident
- Restart masked the real problem initially

## Where We Got Lucky

- Incident happened during business hours when team was available
- Feature flag system was already in place (just not for this feature)

---

## Action Items

### Immediate (This Week)
| Action | Owner | Due | Status |
|--------|-------|-----|--------|
| Fix connection leak in reporting | Backend | Jan 30 | [ ] |
| Add connection pool metrics to dashboard | SRE | Jan 30 | [ ] |
| Add feature flag to reporting | Backend | Jan 29 | [x] |

### Short-term (This Month)
| Action | Owner | Due | Status |
|--------|-------|-----|--------|
| Add connection pool alerts | SRE | Feb 5 | [ ] |
| Create runbook for DB connection issues | SRE | Feb 10 | [ ] |
| Load test error paths | QA | Feb 15 | [ ] |

### Long-term (This Quarter)
| Action | Owner | Due | Status |
|--------|-------|-----|--------|
| Increase connection pool with autoscaling | Platform | Q1 | [ ] |
| Add connection leak detection in CI | Platform | Q1 | [ ] |

---

## Lessons Learned

1. **All new features need feature flags** — Would have saved 30+ minutes
2. **Monitor resource pools explicitly** — Don't rely on downstream errors
3. **Test error paths under load** — Happy path testing isn't enough
</output>
</example>
</examples>

<rules>
- Blameless: Focus on systems and processes, not individuals
- Accurate: Timeline must be factual and verifiable
- Complete: All contributing factors identified
- Actionable: Every action item has owner and deadline
- Learning-focused: Extract insights for improvement
- Follow-up: Track action items to completion
</rules>

<error_handling>
If timeline unclear: Document what's known, mark gaps for investigation
If root cause uncertain: Document hypotheses, plan investigation
If actions too vague: Break into specific, measurable tasks
If no owner available: Escalate to management for assignment
</error_handling>

## Model Note

**Requires Opus** — Deep analysis benefits from extended reasoning.
Postmortems require careful root cause analysis and systemic thinking.
