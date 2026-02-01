---
name: compound-commands
description: Chain multiple commands for common workflows
disable-model-invocation: true
---

# Compound Commands

Chain multiple commands for common workflows.

## Description

Combine existing commands into powerful workflow shortcuts.
Triggers on: "ship", "full review", "complete feature", "quick fix", "workflow".

## Available Compound Commands

### `/ship` - Ship a Feature
Complete workflow from test to merge:

```markdown
## /ship Workflow

Runs in sequence:
1. `/test` - Verify test coverage
2. `/review` - Code review
3. Pre-commit checks
4. Commit changes
5. Push to remote
6. Create PR (optional)

**Usage:**
"Ship this feature"
"/ship"
"Ready to ship"
```

**Process:**
```
┌─────────┐    ┌─────────┐    ┌──────────┐    ┌────────┐    ┌──────┐
│  /test  │ → │ /review │ → │ pre-commit│ → │ commit │ → │ push │
└─────────┘    └─────────┘    └──────────┘    └────────┘    └──────┘
     │              │               │              │
     ▼              ▼               ▼              ▼
  Pass?          Pass?          Pass?         Message?
```

**Abort Conditions:**
- Tests fail → Stop, show failures
- Review finds S0/S1 → Stop, show issues
- Pre-commit fails → Stop, show problems

---

### `/quick-fix` - Rapid Bug Fix
Fast path for small fixes:

```markdown
## /quick-fix Workflow

Runs in sequence:
1. Make the fix
2. Run related tests only
3. Quick review (focused)
4. Commit with "fix:" prefix
5. Push

**Usage:**
"Quick fix for the login bug"
"/quick-fix"
```

**Optimizations:**
- Runs only affected tests (not full suite)
- Review focuses on changed lines only
- Uses Haiku for speed

---

### `/full-review` - Comprehensive Review
Deep review for critical changes:

```markdown
## /full-review Workflow

Runs in sequence:
1. `/review` - Standard code review
2. `/secure` - Security audit
3. `/test` - Coverage verification
4. Pre-merge checklist

**Usage:**
"Full review before merge"
"/full-review"
```

**When to Use:**
- Before merging to main
- Security-sensitive changes
- Public API changes

---

### `/start-feature` - Begin New Feature
Set up for new feature work:

```markdown
## /start-feature Workflow

Runs in sequence:
1. Create feature branch
2. `/plan` - Create spec
3. `/audit-blueprint` - Validate plan
4. Update STATUS.md
5. Ready to code

**Usage:**
"/start-feature user-authentication"
"Start working on the payment feature"
```

---

### `/finish-feature` - Complete Feature
Wrap up feature work:

```markdown
## /finish-feature Workflow

Runs in sequence:
1. `/test` - Final test run
2. `/review` - Final review
3. Update CHANGELOG
4. `/closeout` - Update docs
5. Create PR

**Usage:**
"/finish-feature"
"Finish the authentication feature"
```

---

### `/maintenance` - Maintenance Workflow
Regular codebase maintenance:

```markdown
## /maintenance Workflow

Runs in sequence:
1. `/assess` - Codebase audit
2. `/debt` - Identify tech debt
3. `/secure` - Security scan
4. Update KNOWN_ISSUES.md
5. Create maintenance tasks

**Usage:**
"/maintenance"
"Run maintenance checks"
```

**Recommended:** Weekly or before releases

---

### `/onboard-project` - Full Project Setup
Complete new project initialization:

```markdown
## /onboard-project Workflow

Runs in sequence:
1. `/gitignore` - Setup gitignore
2. `/scout-skills` - Install skills
3. `/map-project` - Generate context
4. `/assess` - Initial audit
5. Create STATUS.md
6. Create CHANGELOG.md

**Usage:**
"/onboard-project"
"Set up this project completely"
```

---

### `/release-prep` - Prepare Release
Get ready for release:

```markdown
## /release-prep Workflow

Runs in sequence:
1. `/test` - Full test suite
2. `/secure` - Security audit
3. Generate changelog
4. `/release` - Release checklist
5. Update version numbers
6. Create release PR

**Usage:**
"/release-prep 1.3.0"
"Prepare release for version 2.0"
```

---

### `/loop` - Autonomous Development Loop
Exhaustive loop until all quality gates pass:

```markdown
## /loop Workflow

Runs continuously until ALL gates pass:
1. `/assess` - Analyze codebase state
2. Plan/prioritize work
3. Implement fixes/features
4. `/test` - Verify all tests pass
5. `/review` - Code quality check
6. `/secure` - Security audit
7. Evaluate → Loop if issues remain

**Exit Conditions:**
- All tests passing ✅
- Coverage ≥ 80% ✅
- No S0/S1 issues ✅
- No security vulnerabilities ✅
- Documentation complete ✅

**Usage:**
"/loop"
"/loop security"  # Focus on security only
"/loop --max-iterations=20"
"Work until done"
"No stone unturned"
```

**Pause Conditions:**
- User direction needed
- Breaking changes required
- Multiple valid approaches
- New dependencies needed

**Safety:**
- Commits after each iteration
- Never installs to base conda env
- Max iterations prevent infinite loop
- Stall detection (no progress = pause)

---

## Custom Compound Commands

### Define Your Own
Add to `.claude/commands/`:

```markdown
# /my-workflow - Custom Workflow

## Steps
1. [First command or action]
2. [Second command or action]
3. [Third command or action]

## Abort Conditions
- [When to stop]

## Usage
"my-workflow"
"/my-workflow"
```

### Example: Deploy Workflow
```markdown
# /deploy - Deploy to Production

## Steps
1. `/release` - Verify release checklist
2. Run build: `npm run build`
3. Run deploy: `npm run deploy`
4. Verify deployment
5. Update STATUS.md

## Abort Conditions
- Release checklist fails
- Build fails
- Deploy fails
```

## Workflow Execution

### Sequential Execution
Commands run one after another:
```
Step 1 → Step 2 → Step 3 → Done
   ↓        ↓        ↓
 Fail?    Fail?    Fail?
   ↓        ↓        ↓
 Stop     Stop     Stop
```

### Progress Reporting
```markdown
## Workflow: /ship

[■■■□□] Step 2/5: Running /review...

✅ Step 1: /test - Passed (45 tests, 92% coverage)
🔄 Step 2: /review - In progress...
⏳ Step 3: Pre-commit checks
⏳ Step 4: Commit
⏳ Step 5: Push
```

### Failure Handling
```markdown
## Workflow: /ship - STOPPED

✅ Step 1: /test - Passed
❌ Step 2: /review - Failed

### Issues Found
- S1: SQL injection vulnerability in userQuery
- S1: Missing input validation

### Options
1. Fix issues and restart workflow
2. Skip review (not recommended)
3. Abort workflow
```

## Configuration

### Default Workflows
All compound commands work out of the box.

### Customization
Override behavior in project settings:
```json
{
  "workflows": {
    "ship": {
      "skipReview": false,
      "requireTests": true,
      "autoPush": true,
      "createPR": false
    }
  }
}
```

## Benefits

| Individual Commands | Compound Commands |
|--------------------|--------------------|
| Run manually each time | Single command |
| Easy to forget steps | All steps included |
| Inconsistent order | Consistent process |
| Manual abort decisions | Automatic abort on failure |
