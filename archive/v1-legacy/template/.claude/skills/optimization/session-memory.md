---
name: session-memory
description: Track completed actions to avoid redundant work within session
model: sonnet
---

# Session Memory

Track what's been done this session to avoid redundant work.

## Description

Maintains awareness of completed actions within the current session to prevent re-analysis and duplicate work.
Triggers on: "what have we done", "session summary", "don't repeat", "already did that".

## What Gets Remembered

### Files Analyzed
- Files that have been read and understood
- Analysis results and key findings

### Actions Taken
- Commands executed
- Changes made
- Commits created

### Decisions Made
- Architectural choices
- Approach selections
- User preferences expressed

### Context Gathered
- Tech stack identified
- Patterns discovered
- Dependencies mapped

## Session State Structure

Mental model of current session:

```markdown
## Session State

### Analyzed Files
- `src/index.ts` - Entry point, Express server setup
- `src/routes/api.ts` - REST endpoints
- `package.json` - Dependencies: Express, TypeScript, Jest

### Completed Actions
- [x] Project initialized (/gitignore, /scout-skills, /map-project)
- [x] Read STATUS.md - Current focus: authentication feature
- [x] Reviewed auth blueprint
- [x] Implemented login endpoint
- [x] Committed: "Add login endpoint"

### Active Context
- Working on: Authentication feature
- Current file: `src/auth/login.ts`
- Blocking issues: None

### User Preferences (This Session)
- Prefers functional style over classes
- Wants detailed commit messages
- Using Zod for validation

### Decisions Made
- JWT for auth tokens (decided in /plan)
- 15-minute token expiry
- Refresh tokens stored in httpOnly cookies
```

## How It Works

### Passive Tracking
As work progresses, maintain awareness of:
1. **Files touched** - Don't re-read unless changed
2. **Questions answered** - Don't re-ask
3. **Patterns identified** - Reference, don't re-discover
4. **Commands run** - Know what's already done

### Active Recall
Before taking action, check if:
- "Have I already analyzed this file?" → Use cached understanding
- "Did we already decide this?" → Reference the decision
- "Was this command already run?" → Skip or confirm re-run

## Avoiding Redundant Work

### File Re-reading
```markdown
❌ BAD: Reading package.json again to check dependencies
✅ GOOD: "Earlier we saw Express 4.18, TypeScript 5.3, Jest for testing"
```

### Re-analysis
```markdown
❌ BAD: "Let me analyze the project structure again"
✅ GOOD: "Based on our earlier analysis, this is a Next.js app with..."
```

### Repeated Questions
```markdown
❌ BAD: "What testing framework do you prefer?"
✅ GOOD: "Using Jest as you mentioned earlier"
```

## Session Boundaries

### What Persists Within Session
- All analysis and understanding
- User preferences and decisions
- Work completed

### What Doesn't Persist Across Sessions
- Session memory resets on new conversation
- PROJECT_MAP.md persists (file-based)
- STATUS.md persists (file-based)

### Handoff to Next Session
Before session ends, update persistent files:
```markdown
## Session Closeout

Update these files to preserve context:
1. **STATUS.md** - Current state and next steps
2. **CHANGELOG.md** - Work completed
3. **KNOWN_ISSUES.md** - Any blockers discovered
```

## Integration with Commands

### /daily Command
Reads STATUS.md to restore context from previous session:
```markdown
"Resuming from STATUS.md:
- Last session completed: Login endpoint
- Next up: Password reset flow
- Blockers: None noted"
```

### /closeout Command
Writes session summary to STATUS.md:
```markdown
"Updating STATUS.md with:
- Completed: Password reset implementation
- Next: Email verification
- Notes: Using SendGrid for emails"
```

## Memory Cues

Phrases that indicate memory should be used:
- "As we discussed..."
- "Earlier you mentioned..."
- "Based on our analysis..."
- "Since we already..."
- "Continuing from..."

Phrases that indicate fresh analysis needed:
- "Let's start fresh..."
- "Re-analyze this..."
- "I changed my mind about..."
- "Ignore what we said before..."

## Efficiency Gains

| Without Memory | With Memory |
|----------------|-------------|
| Re-read files each time | Reference cached understanding |
| Re-ask decided questions | Use established preferences |
| Re-discover patterns | Reference known patterns |
| Repeat setup steps | Skip completed initialization |

## Session Summary Command

User can ask: "What have we done this session?"

Response:
```markdown
## Session Summary

**Duration:** ~2 hours
**Focus:** Authentication feature

### Completed
1. Initialized project (gitignore, skills, map)
2. Reviewed auth blueprint
3. Implemented login endpoint
4. Implemented logout endpoint
5. Added JWT middleware
6. Wrote tests (85% coverage)
7. Created 3 commits

### In Progress
- Password reset flow (50% done)

### Decisions Made
- JWT with 15min expiry
- Refresh tokens in httpOnly cookies
- Zod for input validation

### Next Steps
1. Complete password reset
2. Add email verification
3. Update API documentation
```
