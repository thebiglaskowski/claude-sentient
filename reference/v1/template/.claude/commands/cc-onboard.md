---
name: cc-onboard
description: Create onboarding documentation
model: sonnet
argument-hint: "[role or person]"
---

# /onboard - Onboarding Documentation Generator

<context>
Effective onboarding reduces time-to-productivity and prevents knowledge silos.
New team members need clear setup instructions, codebase orientation, and a
structured path to contribution. Good onboarding documentation pays dividends
every time someone joins the team.
</context>

<role>
You are a technical documentation specialist who:
- Creates clear, step-by-step guides
- Anticipates newcomer questions
- Organizes information by timeline (Day 1, Week 1, Month 1)
- Ensures no critical setup steps are missing
- Writes for someone unfamiliar with the project
</role>

## Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `$1` | Role or person to onboard | `/onboard frontend developer` |

## Usage Examples

```
/onboard                        # General onboarding guide
/onboard frontend developer     # Frontend-specific onboarding
/onboard backend engineer       # Backend-specific onboarding
/onboard contractor             # Contractor access guide
/onboard intern                 # Simplified intern guide
```

<task>
Create comprehensive onboarding documentation by:
1. Analyzing the target role or audience
2. Documenting environment setup
3. Mapping the codebase structure
4. Creating timeline-based checklists
5. Listing key resources and contacts
</task>

<instructions>
<step number="1">
**Define audience**: Determine who the guide is for:
- Specific role (frontend, backend, fullstack)
- Experience level (senior, junior, intern)
- Engagement type (employee, contractor)
- Tailor depth and detail accordingly
</step>

<step number="2">
**Document environment setup**: Complete setup instructions:
- Required software and versions
- Repository cloning and access
- Environment variables and secrets
- Database setup and seeding
- Running the application locally
- IDE configuration and extensions
</step>

<step number="3">
**Map the codebase**: Explain project structure:
- Directory layout and purpose of each folder
- Key files and their responsibilities
- Architecture patterns used
- Data flow and entry points
- Naming conventions
- Where to find things
</step>

<step number="4">
**Create timeline checklist**: Structure by timeframe:
- **Day 1**: Access, setup, first run
- **Week 1**: Codebase tour, first contribution
- **Month 1**: Deeper understanding, independent work
</step>

<step number="5">
**List resources**: Compile essential references:
- Documentation links
- Key contacts and their roles
- Communication channels
- Recurring meetings
- Where to ask questions
</step>
</instructions>

<output_format>
# Onboarding Guide: [Role]

**Audience:** [Who this is for]
**Last Updated:** [Date]
**Estimated Time:** [Hours to complete]

---

## Pre-arrival Checklist (for manager/team)
- [ ] [Access/account setup items]

---

## Day 1

### Accounts & Access
- [ ] [Step-by-step access items]

### Environment Setup
```bash
[Commands to run]
```

### Verification
- [ ] Can run the application locally
- [ ] Can access all required systems

---

## Week 1

### Codebase Orientation

#### Directory Structure
```
[Key directories with descriptions]
```

#### Key Files
| File | Purpose |
|------|---------|
| [file] | [what it does] |

### First Contribution
- [ ] Pick a starter task
- [ ] Make first commit
- [ ] Get first PR reviewed

---

## Month 1

### Deep Dives
- [ ] [Architecture understanding items]
- [ ] [System-specific knowledge]

### Independence Milestones
- [ ] [Self-sufficiency indicators]

---

## Resources

### Documentation
| Resource | Link |
|----------|------|
| [Doc name] | [URL] |

### Key Contacts
| Person | Role | Contact |
|--------|------|---------|
| [Name] | [Role] | [How to reach] |

### Communication
- **Questions**: [Where to ask]
- **Announcements**: [Where to look]
- **Meetings**: [Recurring meetings to attend]

---

## Common Tasks

### How to: [Common task 1]
[Steps]

### How to: [Common task 2]
[Steps]
</output_format>

<examples>
<example>
<input>
/onboard frontend developer
</input>
<thinking>
1. Target: Frontend developer - focus on React/UI patterns
2. Setup: Node.js, npm, design system
3. Key areas: components, state management, styling
4. First task: bug fix or small UI feature
</thinking>
<output>
# Onboarding Guide: Frontend Developer

**Audience:** Frontend developers joining the team
**Last Updated:** 2026-01-29
**Estimated Time:** 4-6 hours for setup, ongoing learning

---

## Pre-arrival Checklist (for manager)
- [ ] Create GitHub account with repo access
- [ ] Add to Slack channels: #frontend, #dev-general
- [ ] Add to Figma team workspace
- [ ] Schedule intro meetings with design and backend leads

---

## Day 1

### Accounts & Access
- [ ] GitHub organization invitation accepted
- [ ] Figma workspace access confirmed
- [ ] Slack channels joined
- [ ] Jira/Linear project access

### Environment Setup

```bash
# 1. Clone the repository
git clone git@github.com:company/frontend-app.git
cd frontend-app

# 2. Install Node.js (use nvm for version management)
nvm install 20
nvm use 20

# 3. Install dependencies
npm install

# 4. Set up environment
cp .env.example .env.local
# Edit .env.local with values from 1Password vault

# 5. Run the development server
npm run dev

# 6. Open http://localhost:3000
```

### Verification
- [ ] App runs without errors at localhost:3000
- [ ] Can log in with test credentials
- [ ] Hot reload works when editing a component

---

## Week 1

### Codebase Orientation

#### Directory Structure
```
src/
├── components/     # Reusable UI components
│   ├── ui/         # Base design system components
│   └── features/   # Feature-specific components
├── pages/          # Next.js pages (routes)
├── hooks/          # Custom React hooks
├── lib/            # Utilities and API clients
├── styles/         # Global styles, theme config
└── types/          # TypeScript type definitions
```

#### Key Files
| File | Purpose |
|------|---------|
| `src/components/ui/Button.tsx` | Example of base component pattern |
| `src/lib/api.ts` | API client with auth handling |
| `src/hooks/useAuth.ts` | Authentication hook |
| `tailwind.config.js` | Design tokens and theme |

### Coding Standards
- Components use TypeScript with explicit prop types
- Styling via Tailwind CSS (no inline styles)
- State management: React Query for server state, Zustand for client
- Tests required for components with logic

### First Contribution
1. Find a `good-first-issue` in Jira/Linear
2. Create a feature branch: `feature/TICKET-123-description`
3. Make changes with tests
4. Open PR and request review from mentor

---

## Month 1

### Deep Dives
- [ ] Understand the authentication flow
- [ ] Learn the design system patterns
- [ ] Review API integration patterns
- [ ] Study state management approach

### Independence Milestones
- [ ] Complete 3+ tickets independently
- [ ] Review someone else's PR
- [ ] Present a component in team meeting

---

## Resources

### Documentation
| Resource | Link |
|----------|------|
| Design System | /docs/design-system |
| API Documentation | /api/docs |
| Component Storybook | localhost:6006 |
| Figma Designs | [Figma link] |

### Key Contacts
| Person | Role | Contact |
|--------|------|---------|
| Alex Chen | Frontend Lead | @alex on Slack |
| Sam Park | Design Lead | @sam on Slack |
| Jordan Lee | Backend Lead | @jordan on Slack |

### Communication
- **Questions**: #frontend channel or DM your mentor
- **Design questions**: #design channel
- **Meetings**: Frontend sync Tue/Thu 10am, Design review Wed 2pm

---

## Common Tasks

### How to: Add a new component
1. Create file in `src/components/ui/` or `features/`
2. Export from index.ts
3. Add Storybook story in same folder
4. Add unit tests if component has logic

### How to: Connect to API
```typescript
import { api } from '@/lib/api';

const { data, isLoading } = useQuery({
  queryKey: ['users'],
  queryFn: () => api.get('/users')
});
```

### How to: Debug issues
1. Check browser console for errors
2. Check Network tab for failed requests
3. Use React DevTools for component state
4. Check #frontend Slack for known issues
</output>
</example>

<example>
<input>
/onboard contractor
</input>
<output>
# Onboarding Guide: Contractor

**Audience:** External contractors
**Last Updated:** 2026-01-29
**Estimated Time:** 2-3 hours for setup

---

## Pre-arrival Checklist (for hiring manager)
- [ ] NDA signed and on file
- [ ] Create limited-access GitHub account
- [ ] Create contractor Slack account
- [ ] Define scope of accessible repositories
- [ ] Set contract end date for access review

---

## Day 1

### Accounts & Access
- [ ] GitHub invitation accepted (limited repos only)
- [ ] Slack access to project-specific channels
- [ ] Time tracking system access
- [ ] Project management tool access

### Important Policies
- **Code ownership**: All code belongs to the company
- **Confidentiality**: Do not share code or discuss project externally
- **Communication**: Use company Slack, not personal email
- **Time tracking**: Log hours daily in [system]

### Environment Setup
[Same as employee setup, limited to accessible repos]

### Verification
- [ ] Can clone assigned repository
- [ ] Can run the project locally
- [ ] Can access Slack project channels
- [ ] Understand time reporting process

---

## Resources

### Key Contacts
| Person | Role | Contact |
|--------|------|---------|
| [Manager] | Project Manager | Primary contact |
| [Tech Lead] | Technical Lead | Code questions |

### Communication
- **Questions**: Project Slack channel
- **Blockers**: Escalate to project manager
- **Hours**: Submit weekly by Friday 5pm

---

## Contract End Process
- Return any company equipment
- Ensure all code is committed and pushed
- Document any work in progress
- Access will be revoked on contract end date
</output>
</example>
</examples>

<rules>
- Verify all setup steps actually work before documenting
- Include exact commands and versions where possible
- Don't assume prior knowledge of the project
- Include troubleshooting for common setup issues
- Keep the guide updated as the project evolves
- Test the guide with actual new team members
</rules>

<error_handling>
If role not specified: "Who is this onboarding guide for? (e.g., frontend developer, backend engineer, contractor)"
If project too complex: Break into multiple specialized guides
If no codebase access: Document what's needed for complete guide
If setup steps unknown: Mark as TODO and flag for team input
</error_handling>
