---
name: plan-approval
description: Require explicit approval before executing risky or significant changes
version: 1.0.0
triggers:
  - "requires approval"
  - "approve plan"
  - "review before executing"
  - "risky change"
  - "breaking change"
model: sonnet
tags: [orchestration, approval, safety, workflow]
context: inherit
---

# Plan Approval

Require explicit approval before executing risky, breaking, or significant changes. Provides a safety checkpoint in automated workflows.

---

## Overview

Some changes are too risky to execute automatically:

- **Schema migrations** - Could lose data
- **Breaking API changes** - Could break clients
- **Security configuration** - Could expose vulnerabilities
- **Destructive operations** - Could delete important data
- **External service integration** - Could affect third parties

Plan approval creates a checkpoint where the orchestrator (or user) must explicitly approve before proceeding.

---

## When Approval is Required

### Automatic Triggers

| Change Type | Risk Level | Approval Required |
|-------------|------------|-------------------|
| Schema migration (add table) | Medium | Yes |
| Schema migration (drop column) | High | Yes + confirmation |
| API breaking change | High | Yes |
| Delete operations (bulk) | High | Yes + confirmation |
| Security configuration | Critical | Yes + user |
| External API integration | Medium | Yes |
| Dependency major upgrade | Medium | Yes |
| Environment variable change | Low-Medium | Optional |
| New feature (non-breaking) | Low | No |
| Bug fix (isolated) | Low | No |
| Documentation update | None | No |

### Risk Assessment

```
RISK LEVEL CALCULATION:
├── Data loss potential? → +High
├── Breaking change? → +High
├── Security implications? → +Critical
├── Affects external systems? → +Medium
├── Reversible? → -Low
├── Has rollback plan? → -Low
└── Tested in staging? → -Low
```

---

## Approval Workflow

### Standard Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    PLAN APPROVAL WORKFLOW                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Worker identifies risky action                              │
│                    │                                             │
│                    ▼                                             │
│  2. Worker generates approval request                           │
│     ├── Action description                                       │
│     ├── Risk assessment                                          │
│     ├── Rollback plan                                            │
│     └── Alternative approaches                                   │
│                    │                                             │
│                    ▼                                             │
│  3. Request added to approval queue                             │
│                    │                                             │
│                    ▼                                             │
│  4. Leader reviews request                                      │
│     ├── [Approve] → Worker proceeds                             │
│     ├── [Reject] → Worker abandons or revises                   │
│     └── [Modify] → Worker adjusts and re-submits                │
│                    │                                             │
│                    ▼                                             │
│  5. Decision logged for audit trail                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### User Escalation

For critical changes, escalate to user:

```
ESCALATION RULES:
├── Risk = Critical → Always escalate to user
├── Risk = High + no rollback → Escalate to user
├── Security changes → Always escalate to user
├── Production environment → Escalate to user
└── Other cases → Leader can approve
```

---

## Approval Request Format

### In LOOP_STATE.md

```markdown
## Approval Queue

### Pending Approvals

#### APPROVAL-001
- **Requester:** worker-1 (database-expert)
- **Action:** Add sessions table with foreign key to users
- **Risk Level:** Medium
- **Submitted:** 2024-01-15T10:15:00Z

**Plan:**
1. Create `sessions` table
2. Add foreign key constraint to `users(id)`
3. Add indexes for session lookup
4. Migration is reversible (can drop table)

**Risk Assessment:**
- Data loss: None (new table)
- Breaking change: No
- Rollback: Yes (drop table)

**Alternatives Considered:**
- Store sessions in Redis (rejected: need persistence)
- Use JWT only (rejected: need revocation capability)

**Approval Status:** PENDING

---

#### APPROVAL-002
- **Requester:** worker-2 (api-designer)
- **Action:** Change user endpoint response format
- **Risk Level:** High (Breaking Change)
- **Submitted:** 2024-01-15T10:20:00Z

**Plan:**
1. Add new fields to /api/users response
2. Remove deprecated `fullName` field
3. Update API version to v2

**Risk Assessment:**
- Data loss: None
- Breaking change: YES (removing field)
- Affected clients: Unknown
- Rollback: Yes (keep v1 endpoint)

**Migration Path:**
1. Deploy v2 alongside v1
2. Deprecation notice for v1
3. Remove v1 after 30 days

**Approval Status:** PENDING (requires user confirmation)
```

---

## Approval Decisions

### Approve

```markdown
#### APPROVAL-001 (APPROVED)
- **Decision:** Approved
- **Approver:** leader
- **Time:** 2024-01-15T10:18:00Z
- **Notes:** Schema looks good, proceed with migration.
```

### Reject

```markdown
#### APPROVAL-002 (REJECTED)
- **Decision:** Rejected
- **Approver:** user
- **Time:** 2024-01-15T10:25:00Z
- **Reason:** Breaking change needs client communication first.
- **Action Required:** Notify clients, set deprecation timeline, then re-submit.
```

### Modify

```markdown
#### APPROVAL-003 (MODIFY)
- **Decision:** Modify and re-submit
- **Approver:** leader
- **Time:** 2024-01-15T10:30:00Z
- **Requested Changes:**
  - Add index on created_at column
  - Include soft delete (deleted_at) column
- **Action Required:** Update plan and re-submit for approval.
```

---

## Integration with Autonomous Loop

### BUILD Phase Enhancement

```
BUILD PHASE:
├── Pick task from queue
├── Analyze required changes
├── **APPROVAL CHECK** ← New
│   ├── Is this a risky change?
│   ├── YES → Generate approval request
│   │         Wait for approval
│   │         If rejected → Handle rejection
│   │         If approved → Proceed
│   └── NO → Proceed directly
├── Execute changes
└── Continue to TEST
```

### Swarm Mode Integration

```
Worker claims task
Worker analyzes task
Worker detects risky action
Worker submits approval request
Worker status: WAITING_APPROVAL
Leader reviews and approves
Worker status: IN_PROGRESS
Worker executes approved plan
Worker completes task
```

---

## Approval Commands

### Request Approval

```
"This requires approval: [describe change]"
"Submit for approval: schema migration to add sessions table"
```

### Review Approvals

```
"Show pending approvals"
"What's waiting for approval?"

Output:
═══════════════════════════════════════
PENDING APPROVALS (2)
═══════════════════════════════════════

1. APPROVAL-001 (Medium Risk)
   Add sessions table
   Requested by: worker-1
   Waiting: 3 minutes

2. APPROVAL-002 (High Risk) ⚠️
   Breaking API change
   Requested by: worker-2
   Waiting: 8 minutes
   REQUIRES USER APPROVAL

[approve 1] [approve 2] [reject] [details]
═══════════════════════════════════════
```

### Approve/Reject

```
"Approve APPROVAL-001"
"Approve APPROVAL-001 with note: add index on user_id"
"Reject APPROVAL-002: need client notification first"
"Modify APPROVAL-003: also add soft delete column"
```

---

## Auto-Approval Rules

### Configurable Auto-Approval

Some changes can be auto-approved based on rules:

```json
// .claude/settings.json
{
  "orchestration": {
    "approval": {
      "autoApprove": {
        "addTable": true,
        "addColumn": true,
        "addIndex": true,
        "addEndpoint": true
      },
      "requireApproval": {
        "dropTable": "user",
        "dropColumn": "user",
        "breakingChange": "user",
        "securityConfig": "user",
        "bulkDelete": true,
        "externalApi": true
      },
      "escalateToUser": [
        "securityConfig",
        "production",
        "dropTable",
        "breakingChange"
      ]
    }
  }
}
```

### Safe Defaults

Without configuration, these defaults apply:

| Action | Default |
|--------|---------|
| Add table/column/index | Auto-approve |
| Add endpoint (non-breaking) | Auto-approve |
| Documentation changes | Auto-approve |
| Drop table/column | Require user |
| Breaking API change | Require user |
| Security configuration | Require user |
| Bulk delete | Require approval |
| External API call | Require approval |

---

## Audit Trail

### Approval Log

All approval decisions are logged:

```markdown
## Approval History

| ID | Action | Risk | Decision | Approver | Time |
|----|--------|------|----------|----------|------|
| 001 | Add sessions table | Medium | Approved | leader | 10:18 |
| 002 | Breaking API change | High | Rejected | user | 10:25 |
| 003 | Add auth middleware | Low | Auto-approved | system | 10:30 |
```

### Decision Linking

Approval decisions link to:

```markdown
## Decisions Log (DECISIONS_LOG.md)

### TECH-005: Sessions Table Design
- **Decision:** Use database sessions instead of JWT-only
- **Approval:** APPROVAL-001 (approved by leader)
- **Rationale:** Need revocation capability
- **Alternatives:** Redis sessions, JWT-only
```

---

## Timeout Handling

### Approval Timeout

If approval not received within timeout:

```
TIMEOUT BEHAVIOR:
├── Low risk: Continue waiting (no timeout)
├── Medium risk: Reminder after 5 minutes
├── High risk: Reminder after 2 minutes, escalate after 5
├── Critical risk: Immediate user notification

If worker is in swarm mode:
├── Worker moves to WAITING_APPROVAL status
├── Worker releases task (others can claim different tasks)
├── When approved: Worker reclaims and continues
```

### Stale Approval

If change context has changed since approval requested:

```
STALE DETECTION:
├── Files mentioned in plan have changed
├── Dependencies have been updated
├── More than 1 hour since request

If stale:
├── Mark approval as STALE
├── Require re-submission with updated context
```

---

## Examples

### Example 1: Schema Migration (Auto-Approve)

```
Worker: I need to add a `sessions` table.

System checks:
├── Action: Add table
├── Risk: Medium
├── Auto-approve rule: addTable = true
└── Result: Auto-approved

Worker proceeds immediately.

Log: APPROVAL-001 | Add sessions table | Auto-approved | system
```

### Example 2: Breaking Change (User Required)

```
Worker: I need to remove the deprecated `fullName` field from the API.

System checks:
├── Action: Remove field from API
├── Risk: High (breaking change)
├── Auto-approve rule: breakingChange = "user"
└── Result: Requires user approval

System creates approval request:
┌─────────────────────────────────────────┐
│ APPROVAL REQUIRED                       │
├─────────────────────────────────────────┤
│ Worker: worker-2                        │
│ Action: Remove fullName from /api/users │
│ Risk: HIGH (Breaking Change)            │
│                                         │
│ This will break clients using fullName. │
│                                         │
│ Migration plan:                         │
│ 1. Add firstName + lastName fields      │
│ 2. Deprecate fullName                   │
│ 3. Remove after 30 days                 │
│                                         │
│ [Approve] [Reject] [Modify]             │
└─────────────────────────────────────────┘

User: "Approve, but extend deprecation to 60 days"

System: Approved with modification. Worker proceeds with 60-day timeline.
```

### Example 3: Security Change (User Escalation)

```
Worker: I need to change the JWT signing algorithm from HS256 to RS256.

System checks:
├── Action: Security configuration change
├── Risk: Critical
├── Auto-approve rule: securityConfig = "user"
└── Result: Escalate to user immediately

System notification:
⚠️ SECURITY CHANGE REQUIRES YOUR APPROVAL

Worker wants to change JWT algorithm from HS256 to RS256.

This affects: Authentication for all users
Risk: Critical (security configuration)
Reversible: Yes (keep both algorithms temporarily)

Do you approve this change?
[Approve] [Reject] [Need More Info]
```

---

## Best Practices

### Do

- Provide clear rollback plans
- Explain why the change is needed
- List alternatives considered
- Include risk assessment
- Respond to approvals promptly

### Don't

- Skip approval for risky changes
- Leave approvals pending too long
- Approve without reading the plan
- Auto-approve critical changes
- Forget to log decisions

---

## Configuration Reference

```json
{
  "orchestration": {
    "approval": {
      "enabled": true,
      "timeoutMinutes": 10,
      "escalateToUser": ["critical", "security", "production"],
      "autoApprove": {
        "addTable": true,
        "addColumn": true,
        "addIndex": true,
        "addEndpoint": true,
        "documentation": true
      },
      "requireApproval": {
        "dropTable": "user",
        "dropColumn": "user",
        "breakingChange": "user",
        "securityConfig": "user",
        "bulkDelete": true,
        "externalApi": true,
        "majorDependencyUpgrade": true
      },
      "staleAfterMinutes": 60,
      "auditLog": true
    }
  }
}
```

---

## Summary

Plan approval provides a safety net for autonomous execution:

| Without Approval | With Approval |
|------------------|---------------|
| Risky changes execute immediately | Checkpoint before risky changes |
| No visibility into decisions | Clear approval audit trail |
| Can't review before execution | Review and modify plans |
| All-or-nothing automation | Selective automation with oversight |

Use plan approval for risky, breaking, or security-sensitive changes. Let low-risk changes auto-approve for efficiency.
