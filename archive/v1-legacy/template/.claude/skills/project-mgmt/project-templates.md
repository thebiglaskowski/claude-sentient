---
name: project-templates
description: Scaffold new projects with best practices built-in
model: sonnet
---

# Project Templates

Scaffold new projects with best practices built-in.

## Description

Create new projects with full setup: structure, config, gitignore, and Claude integration.
Triggers on: "new project", "scaffold", "create project", "start new", "bootstrap".

## Available Templates

### 1. Node.js/TypeScript API
```
node-api/
├── src/
│   ├── index.ts           # Entry point
│   ├── routes/            # API routes
│   ├── controllers/       # Request handlers
│   ├── services/          # Business logic
│   ├── middleware/        # Express middleware
│   ├── types/             # TypeScript types
│   └── utils/             # Utilities
├── tests/
│   ├── unit/
│   └── integration/
├── .claude/               # Claude Code setup
├── .gitignore
├── package.json
├── tsconfig.json
├── jest.config.js
├── .env.example
└── README.md
```

### 2. Next.js App
```
nextjs-app/
├── src/
│   ├── app/               # App Router
│   ├── components/        # React components
│   ├── lib/               # Utilities
│   └── types/             # TypeScript types
├── public/
├── tests/
├── .claude/
├── .gitignore
├── package.json
├── next.config.js
├── tailwind.config.js
└── README.md
```

### 3. Python FastAPI
```
python-api/
├── src/
│   ├── main.py            # Entry point
│   ├── routers/           # API routes
│   ├── services/          # Business logic
│   ├── models/            # Pydantic models
│   └── utils/             # Utilities
├── tests/
├── .claude/
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── .env.example
└── README.md
```

### 4. CLI Tool (Node.js)
```
node-cli/
├── src/
│   ├── index.ts           # Entry point
│   ├── commands/          # CLI commands
│   ├── utils/             # Utilities
│   └── types/             # TypeScript types
├── tests/
├── .claude/
├── .gitignore
├── package.json
├── tsconfig.json
└── README.md
```

### 5. Monorepo (Turborepo)
```
monorepo/
├── apps/
│   ├── web/               # Next.js app
│   └── api/               # Node API
├── packages/
│   ├── ui/                # Shared components
│   ├── config/            # Shared config
│   └── types/             # Shared types
├── .claude/
├── .gitignore
├── package.json
├── turbo.json
└── README.md
```

## Template Features

All templates include:

### Claude Code Integration
- `.claude/CLAUDE.md` - Project instructions
- `.claude/commands/` - All standard commands
- `.claude/skills/` - All standard skills
- `.claude/context/` - For PROJECT_MAP.md

### Git Setup
- Comprehensive `.gitignore` for stack
- `.env.example` with documented vars
- Pre-configured for conventional commits

### Testing Setup
- Test framework configured (Jest/Pytest/etc.)
- Example tests included
- Coverage configuration

### Code Quality
- Linter configured (ESLint/Ruff/etc.)
- Formatter configured (Prettier/Black/etc.)
- Pre-commit hooks ready

### Documentation
- README.md with setup instructions
- STATUS.md initialized
- CHANGELOG.md template

## Scaffold Process

### Step 1: Choose Template
```markdown
What type of project?
1. Node.js/TypeScript API
2. Next.js App
3. Python FastAPI
4. CLI Tool
5. Monorepo
6. Custom (describe your needs)
```

### Step 2: Configure
```markdown
Project name: my-awesome-api
Description: REST API for managing widgets
Author: Your Name

Features to include:
- [x] TypeScript
- [x] Jest testing
- [x] ESLint + Prettier
- [x] Docker support
- [ ] Database (Prisma)
- [ ] Authentication (JWT)
```

### Step 3: Generate
```bash
# Create directory
mkdir my-awesome-api && cd my-awesome-api

# Initialize git
git init

# Create structure
mkdir -p src/{routes,controllers,services,middleware,types,utils}
mkdir -p tests/{unit,integration}
mkdir -p .claude/{commands,skills,context}

# Create files
# [Generated based on template + config]
```

### Step 4: Initialize
```bash
# Install dependencies
npm install

# Copy Claude setup
cp -r C:\scripts\prompts\template\.claude\* .claude/

# Run project init
# "Initialize this project"
```

## Quick Scaffold Commands

### Via Claude
```
"Create a new Next.js project called my-app"
"Scaffold a Python API for user management"
"Bootstrap a CLI tool for file processing"
```

### Via Script (Future)
```bash
# Potential future CLI
npx @prompts/scaffold nextjs-app my-app
```

## Custom Templates

### Creating Custom Templates
1. Create template in `C:\scripts\prompts\templates\`
2. Include `template.json` with metadata
3. Use placeholders for customization

### Template Placeholders
```
{{PROJECT_NAME}}     - Project name
{{DESCRIPTION}}      - Project description
{{AUTHOR}}           - Author name
{{YEAR}}             - Current year
{{NODE_VERSION}}     - Node.js version
{{PYTHON_VERSION}}   - Python version
```

### Example template.json
```json
{
  "name": "node-api",
  "description": "Node.js TypeScript API template",
  "stack": ["node", "typescript", "express"],
  "files": [
    {"src": "package.json.template", "dest": "package.json"},
    {"src": "tsconfig.json", "dest": "tsconfig.json"},
    {"src": "src/index.ts.template", "dest": "src/index.ts"}
  ],
  "postCreate": [
    "npm install",
    "git init",
    "Initialize this project"
  ]
}
```

## Post-Scaffold Checklist

After scaffolding:
- [ ] Review generated files
- [ ] Update README with project specifics
- [ ] Configure environment variables
- [ ] Run `npm install` / `pip install`
- [ ] Run tests to verify setup
- [ ] Make initial commit
- [ ] Initialize Claude (`/scout-skills`, `/map-project`)

## Benefits

| Manual Setup | Template Scaffold |
|--------------|-------------------|
| 30+ minutes | 2 minutes |
| Miss best practices | Best practices built-in |
| Inconsistent structure | Consistent structure |
| Manual Claude setup | Auto Claude integration |
| Forget gitignore entries | Complete gitignore |
