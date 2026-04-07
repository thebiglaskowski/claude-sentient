# Restructure to .claude-sentient/ Directory

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move all non-essential root-level directories into `.claude-sentient/` so installing Claude Sentient into a project doesn't pollute the project root with 10+ foreign directories.

**Architecture:** The restructuring moves `profiles/`, `agents/` (yaml), `rules/` (reference copies), `schemas/`, `templates/`, `examples/`, `documentation/`, `integration/`, `test-utils.js`, `generate-checksums.sh`, `CHECKSUMS.sha256`, `STATUS.md`, `CHANGELOG.md`, and `DECISIONS.md` into a new `.claude-sentient/` directory. The `.claude/` directory (Claude Code native: commands, hooks, skills, agents/*.md, rules, settings, state) stays untouched. A `CS_DIR` constant in `utils.cjs` provides the single resolution point for the new path. ~276 path references across ~21 files need updating.

**Tech Stack:** Bash/PowerShell (installers), Node.js CJS (hooks/tests), Markdown (commands/skills/docs)

**Design decisions applied:**
1. Installers stay at root (entry point for users)
2. `rules/` reference copies are **eliminated** — `.claude/rules/` is the single source of truth
3. `agents/*.yaml` are **eliminated** — hooks/skills read from `.claude/agents/*.md` directly
4. Hook path resolution uses `CS_DIR` constant in `utils.cjs`
5. Source repo layout matches install footprint
6. Tests move with their parent directories into `.claude-sentient/`

---

## File Structure

### Deleted Files/Directories (eliminated duplicates)
| Path | Reason |
|------|--------|
| `rules/*.md` | Duplicates `.claude/rules/*.md` — eliminated per decision #2 |
| `agents/*.yaml` | Duplicates `.claude/agents/*.md` — eliminated per decision #3 |
| `agents/CLAUDE.md` | Moves to `.claude-sentient/agents-CLAUDE.md` or eliminated |
| `agents/__tests__/test-agents.js` | Rewritten to test `.claude/agents/*.md` instead |

### Moved Files (root → .claude-sentient/)
| From | To |
|------|-----|
| `profiles/` | `.claude-sentient/profiles/` |
| `schemas/` | `.claude-sentient/schemas/` |
| `templates/` | `.claude-sentient/templates/` |
| `examples/` | `.claude-sentient/examples/` |
| `documentation/` | `.claude-sentient/documentation/` |
| `integration/` | `.claude-sentient/integration/` |
| `test-utils.js` | `.claude-sentient/test-utils.js` |
| `generate-checksums.sh` | `.claude-sentient/generate-checksums.sh` |
| `CHECKSUMS.sha256` | `.claude-sentient/CHECKSUMS.sha256` |
| `STATUS.md` | `.claude-sentient/STATUS.md` |
| `CHANGELOG.md` | `.claude-sentient/CHANGELOG.md` |
| `DECISIONS.md` | `.claude-sentient/DECISIONS.md` |

### Modified Files
| File | What Changes |
|------|-------------|
| `.claude/hooks/utils.cjs` | Add `CS_DIR` constant |
| `.claude/hooks/agent-tracker.cjs` | Read `.claude/agents/*.md` instead of `agents/*.yaml` |
| `.claude/hooks/__tests__/test-hooks.js` | Update `require()` path for test-utils.js |
| `.claude/commands/__tests__/test-commands.js` | Update `require()` path for test-utils.js |
| `install.sh` | All copy destinations change; drop rules/ and agents/*.yaml copies |
| `install.ps1` | Mirror install.sh |
| `uninstall.sh` | All removal paths change; drop rules/ and agents/ removals |
| `uninstall.ps1` | Mirror uninstall.sh |
| `CLAUDE.md` | Path references to profiles/, documentation/, rules/ |
| `README.md` | Path references, tree diagram, test commands |
| `.claude/commands/cs-loop.md` | References to `rules/_index.md`, `profiles/`, `documentation/` |
| `.claude/commands/cs-team.md` | References to `agents/*.yaml` |
| `.claude/commands/CLAUDE.md` | Reference to `rules/_index.md` |
| `.claude/skills/profile-detection/SKILL.md` | References to `profiles/CLAUDE.md`, `rules/_index.md` |
| `.claude/skills/quality-gates/references/gate-commands.md` | Reference to `profiles/{name}.yaml` |
| All `documentation/*.md` files | Internal cross-references |
| `.claude-sentient/integration/__tests__/test-integration.js` | All path assertions |
| `.claude-sentient/generate-checksums.sh` | All find paths |

### Unchanged
| File | Why |
|------|-----|
| `.claude/` (entire tree except above) | Claude Code native — not our concern |
| `.claude/hooks/session-start.cjs` | Detects profiles by marker files (pyproject.toml, etc.), not by reading profiles/*.yaml |
| `.claude/hooks/context-injector.cjs` | No hardcoded paths to moved directories |
| `.gitignore` | No paths to moved directories need updating |
| `.cursor/`, `.codex/`, `.claude-plugin/` | IDE/plugin conventions — stay at root |

---

## Task 1: Add CS_DIR Constant to utils.cjs

**Why first:** Every subsequent task depends on this constant existing.

**Files:**
- Modify: `.claude/hooks/utils.cjs`

- [ ] **Step 1: Read utils.cjs and find the constants section**

Run: `git show HEAD:.claude/hooks/utils.cjs | head -90`

The constants section starts around line 72 with `const MAX_PROMPT_HISTORY = 50;`

- [ ] **Step 2: Add CS_DIR constant**

In `.claude/hooks/utils.cjs`, add after the `getProjectRoot()` function (around line 68) and before the named constants block:

```javascript
/**
 * Resolve the .claude-sentient directory path.
 * All Claude Sentient project files (profiles, schemas, templates, docs)
 * live here to avoid polluting the project root.
 * @returns {string} Absolute path to .claude-sentient/
 */
function getCSDir() {
    return path.join(getProjectRoot(), '.claude-sentient');
}
```

Add `getCSDir` to the `module.exports` object.

- [ ] **Step 3: Run hook tests to verify no regressions**

Run: `bash --norc --noprofile -c "node .claude/hooks/__tests__/test-hooks.js" 2>/dev/null`
Expected: All tests PASS (new function, nothing calls it yet)

- [ ] **Step 4: Commit**

```bash
git add .claude/hooks/utils.cjs
git commit -m "feat: add getCSDir() constant to utils.cjs for .claude-sentient/ path resolution"
```

---

## Task 2: Move Source Directories to .claude-sentient/

**Why:** This is the physical file move. Everything else is path fixups.

**Files:**
- Move: 12 directories/files from root to `.claude-sentient/`
- Delete: `rules/` (reference copies — eliminated)
- Delete: `agents/*.yaml`, `agents/CLAUDE.md`, `agents/__tests__/` (eliminated — `.claude/agents/*.md` is the source of truth)

- [ ] **Step 1: Create .claude-sentient/ and move directories**

```bash
mkdir -p .claude-sentient

# Move directories that exist
git mv profiles .claude-sentient/profiles
git mv schemas .claude-sentient/schemas
git mv templates .claude-sentient/templates
git mv examples .claude-sentient/examples
git mv documentation .claude-sentient/documentation
git mv integration .claude-sentient/integration

# Move individual files
git mv test-utils.js .claude-sentient/test-utils.js
git mv generate-checksums.sh .claude-sentient/generate-checksums.sh
git mv CHECKSUMS.sha256 .claude-sentient/CHECKSUMS.sha256
git mv STATUS.md .claude-sentient/STATUS.md
git mv CHANGELOG.md .claude-sentient/CHANGELOG.md
git mv DECISIONS.md .claude-sentient/DECISIONS.md
```

If any directories don't exist on disk (deleted in working tree), restore from git first:
```bash
git checkout HEAD -- profiles/ schemas/ templates/ examples/ documentation/ integration/ test-utils.js generate-checksums.sh CHECKSUMS.sha256 STATUS.md CHANGELOG.md DECISIONS.md rules/ agents/
```
Then move them.

- [ ] **Step 2: Delete eliminated duplicates**

```bash
# rules/ reference copies — .claude/rules/ is the single source now
git rm -r rules/

# agents/*.yaml and agents support files — .claude/agents/*.md is the single source now
git rm -r agents/
```

- [ ] **Step 3: Move the plans directory too**

```bash
git mv docs .claude-sentient/docs 2>/dev/null || true
```

- [ ] **Step 4: Commit the move**

```bash
git add -A
git commit -m "refactor: move project files to .claude-sentient/, eliminate rules/ and agents/*.yaml duplicates"
```

---

## Task 3: Update agent-tracker.cjs to Read .claude/agents/*.md

**Why:** The hook currently reads `agents/*.yaml` (line 69) which no longer exists. It needs to read `.claude/agents/*.md` and parse YAML frontmatter instead of full YAML files.

**Files:**
- Modify: `.claude/hooks/agent-tracker.cjs`

- [ ] **Step 1: Read the current agent-tracker.cjs**

Run: `git show HEAD:.claude/hooks/agent-tracker.cjs`

The key function is `detectAgentRole()` around line 59. It:
1. Resolves `agents/` dir via `path.resolve(__dirname, '..', '..', 'agents')`
2. Lists `*.yaml` files
3. Reads each YAML file looking for `name:` and `expertise:` fields

- [ ] **Step 2: Update detectAgentRole() to read .claude/agents/*.md**

Replace the agents directory resolution and file reading:

```javascript
// Old: const agentsDir = path.resolve(__dirname, '..', '..', 'agents');
// New: Read native agent definitions from .claude/agents/*.md
const agentsDir = path.resolve(__dirname, '..', 'agents');
```

Change the file filter from `*.yaml` to `*.md`:
```javascript
// Old: const agentFiles = fs.readdirSync(agentsDir).filter(f => f.endsWith('.yaml'));
// New:
const agentFiles = fs.readdirSync(agentsDir).filter(f => f.endsWith('.md'));
```

The YAML frontmatter parsing stays the same — both `.yaml` files and `.md` frontmatter use `name:` and `expertise:` fields with the same regex patterns.

- [ ] **Step 3: Run hook tests**

Run: `bash --norc --noprofile -c "node .claude/hooks/__tests__/test-hooks.js" 2>/dev/null`
Expected: PASS

- [ ] **Step 4: Commit**

```bash
git add .claude/hooks/agent-tracker.cjs
git commit -m "fix: agent-tracker reads .claude/agents/*.md instead of eliminated agents/*.yaml"
```

---

## Task 4: Update Test require() Paths

**Why:** Test files that `require('../../../test-utils')` need updated paths since test-utils.js moved.

**Files:**
- Modify: `.claude/commands/__tests__/test-commands.js`
- Modify: `.claude/hooks/__tests__/test-hooks.js`
- Modify: `.claude/hooks/__tests__/test-notification.js`
- Modify: `.claude-sentient/profiles/__tests__/test-profiles.js`
- Modify: `.claude-sentient/schemas/__tests__/test-schemas.js`
- Modify: `.claude-sentient/integration/__tests__/test-integration.js`

- [ ] **Step 1: Update .claude/ test files**

For tests inside `.claude/` (commands, hooks), the path to test-utils.js changes from `../../../test-utils` to `../../../.claude-sentient/test-utils`:

In `.claude/commands/__tests__/test-commands.js`:
```javascript
// Old: const { test, suite, summary, getResults } = require('../../../test-utils');
// New:
const { test, suite, summary, getResults } = require('../../../.claude-sentient/test-utils');
```

Same change in `.claude/hooks/__tests__/test-hooks.js` and `.claude/hooks/__tests__/test-notification.js`.

- [ ] **Step 2: Update .claude-sentient/ test files**

For tests inside `.claude-sentient/` (profiles, schemas, integration), the path to test-utils.js changes from relative root to relative `.claude-sentient/`:

In `.claude-sentient/profiles/__tests__/test-profiles.js`:
```javascript
// Old: const { test, suite, summary, getResults } = require('../../test-utils');
// New:
const { test, suite, summary, getResults } = require('../../test-utils');
```

Wait — since `test-utils.js` moved WITH the profiles directory (both now under `.claude-sentient/`), the relative path `../../test-utils` means `.claude-sentient/test-utils.js` which is correct. **No change needed for these files.**

For `.claude-sentient/integration/__tests__/test-integration.js`, same logic — `../../test-utils` resolves to `.claude-sentient/test-utils.js`. **No change needed.**

- [ ] **Step 3: Update agents test file**

The agents test file at `.claude-sentient/agents/__tests__/test-agents.js` was deleted (agents/*.yaml eliminated). We need a NEW test that validates `.claude/agents/*.md` files instead. But this test should live in `.claude/agents/__tests__/` since that's where the files are. 

Actually — the agents test file tested the YAML schema validation of `agents/*.yaml`. Since we eliminated those files, the test file is no longer needed. The agent `.md` files are tested by their YAML frontmatter parsing in the hook tests. Skip this.

- [ ] **Step 4: Run all available tests**

```bash
bash --norc --noprofile -c "node .claude/hooks/__tests__/test-notification.js" 2>/dev/null
bash --norc --noprofile -c "node .claude/hooks/__tests__/test-hooks.js" 2>/dev/null
bash --norc --noprofile -c "node .claude/commands/__tests__/test-commands.js" 2>/dev/null
bash --norc --noprofile -c "node .claude-sentient/profiles/__tests__/test-profiles.js" 2>/dev/null
bash --norc --noprofile -c "node .claude-sentient/schemas/__tests__/test-schemas.js" 2>/dev/null
bash --norc --noprofile -c "node .claude-sentient/integration/__tests__/test-integration.js" 2>/dev/null
```

Expected: `.claude/` tests PASS. `.claude-sentient/` tests may fail on path assertions (fixed in Task 7).

- [ ] **Step 5: Commit**

```bash
git add .claude/commands/__tests__/ .claude/hooks/__tests__/
git commit -m "fix: update test-utils.js require paths after move to .claude-sentient/"
```

---

## Task 5: Update Install Scripts

**Why:** Install scripts control where files land in the target project. Every copy destination must change.

**Files:**
- Modify: `install.sh`
- Modify: `install.ps1`

- [ ] **Step 1: Update install.sh copy destinations**

Read `install.sh`. Apply these changes:

**Source paths** (where install.sh reads from the temp download dir): These also change because the source repo now has files under `.claude-sentient/`.

```bash
# Old:
echo "Installing shared test infrastructure..."
cp "$TEMP_DIR"/test-utils.js ./test-utils.js

# New:
echo "Installing shared test infrastructure..."
mkdir -p .claude-sentient
cp "$TEMP_DIR"/.claude-sentient/test-utils.js .claude-sentient/test-utils.js
```

```bash
# Old:
echo "Installing profiles..."
mkdir -p profiles/__tests__
cp "$TEMP_DIR"/profiles/*.yaml profiles/
cp "$TEMP_DIR"/profiles/CLAUDE.md profiles/
cp "$TEMP_DIR"/profiles/__tests__/*.js profiles/__tests__/

# New:
echo "Installing profiles..."
mkdir -p .claude-sentient/profiles/__tests__
cp "$TEMP_DIR"/.claude-sentient/profiles/*.yaml .claude-sentient/profiles/
cp "$TEMP_DIR"/.claude-sentient/profiles/CLAUDE.md .claude-sentient/profiles/
cp "$TEMP_DIR"/.claude-sentient/profiles/__tests__/*.js .claude-sentient/profiles/__tests__/
```

**Remove rules/ copy section entirely** (eliminated):
```bash
# DELETE these lines:
echo "Installing rules..."
mkdir -p rules
cp "$TEMP_DIR"/rules/*.md rules/
```

**Update templates:**
```bash
# Old:
echo "Installing templates..."
mkdir -p templates
cp "$TEMP_DIR"/templates/*.md templates/
cp "$TEMP_DIR"/templates/settings.json templates/ 2>/dev/null || true

# New:
echo "Installing templates..."
mkdir -p .claude-sentient/templates
cp "$TEMP_DIR"/.claude-sentient/templates/*.md .claude-sentient/templates/
cp "$TEMP_DIR"/.claude-sentient/templates/settings.json .claude-sentient/templates/ 2>/dev/null || true
```

**Remove agents/*.yaml copy section** (eliminated):
```bash
# DELETE these lines:
echo "Installing agents..."
mkdir -p agents/__tests__
cp "$TEMP_DIR"/agents/*.yaml agents/
cp "$TEMP_DIR"/agents/CLAUDE.md agents/
cp "$TEMP_DIR"/agents/__tests__/*.js agents/__tests__/
```

**Update examples:**
```bash
# Old:
mkdir -p examples
cp "$TEMP_DIR"/examples/*.md examples/

# New:
mkdir -p .claude-sentient/examples
cp "$TEMP_DIR"/.claude-sentient/examples/*.md .claude-sentient/examples/
```

**Update schemas:**
```bash
# Old:
mkdir -p schemas/__tests__
cp "$TEMP_DIR"/schemas/*.json schemas/
cp "$TEMP_DIR"/schemas/__tests__/*.js schemas/__tests__/

# New:
mkdir -p .claude-sentient/schemas/__tests__
cp "$TEMP_DIR"/.claude-sentient/schemas/*.json .claude-sentient/schemas/
cp "$TEMP_DIR"/.claude-sentient/schemas/__tests__/*.js .claude-sentient/schemas/__tests__/
```

**Update settings copy** (template source path):
```bash
# Old:
cp "$TEMP_DIR"/templates/settings.json .claude/settings.json

# New:
cp "$TEMP_DIR"/.claude-sentient/templates/settings.json .claude/settings.json
```

**Update learnings.md template source:**
```bash
# Old:
cp "$TEMP_DIR"/templates/learnings.md .claude/rules/learnings.md

# New:
cp "$TEMP_DIR"/.claude-sentient/templates/learnings.md .claude/rules/learnings.md
```

**Update CLAUDE.local.md template source:**
```bash
# Old:
cp "$TEMP_DIR"/templates/CLAUDE.local.md ./CLAUDE.local.md

# New:
cp "$TEMP_DIR"/.claude-sentient/templates/CLAUDE.local.md ./CLAUDE.local.md
```

**Update hook path patching** (reads settings.json from template):
```bash
# The node heredoc that patches hook paths — update the template source path
```

**Update install summary output:**
```bash
# Change all paths in echo statements:
echo "  .claude-sentient/profiles/*.yaml    (9 profiles + schema)"
echo "  .claude-sentient/schemas/*.json     (12 JSON schemas)"
echo "  .claude-sentient/templates/         (templates + settings.json)"
echo "  .claude-sentient/test-utils.js      (shared test infrastructure)"
echo "  .claude-sentient/examples/          (example CLAUDE.md templates)"
# Remove: profiles/__tests__/, agents/*.yaml, agents/__tests__/, rules/*.md
```

- [ ] **Step 2: Mirror all changes in install.ps1**

Apply the same path changes using PowerShell syntax (`New-Item`, `Copy-Item`, `Write-Host`).

- [ ] **Step 3: Commit**

```bash
git add install.sh install.ps1
git commit -m "refactor: update install scripts for .claude-sentient/ directory structure"
```

---

## Task 6: Update Uninstall Scripts

**Files:**
- Modify: `uninstall.sh`
- Modify: `uninstall.ps1`

- [ ] **Step 1: Update uninstall.sh removal paths**

```bash
# Old:
remove_file "test-utils.js"
remove_dir "profiles"
remove_dir "agents"
remove_dir "rules"
remove_dir "templates"
remove_dir "schemas"
remove_dir "examples"

# New — remove entire .claude-sentient/ directory:
remove_dir ".claude-sentient"
```

This is simpler — one removal instead of seven.

- [ ] **Step 2: Mirror in uninstall.ps1**

```powershell
# Old: multiple Remove-DirItem calls
# New:
Remove-DirItem ".claude-sentient"
```

- [ ] **Step 3: Commit**

```bash
git add uninstall.sh uninstall.ps1
git commit -m "refactor: update uninstall scripts for .claude-sentient/ directory"
```

---

## Task 7: Update Integration Tests

**Why:** Integration tests assert file existence at specific paths. All path assertions must change.

**Files:**
- Modify: `.claude-sentient/integration/__tests__/test-integration.js`

- [ ] **Step 1: Read the test file and update all path references**

The test file has ~22 path references. Key changes:

```javascript
// Old: profiles/${yamlName}.yaml
// New: .claude-sentient/profiles/${yamlName}.yaml

// Old: rules/${ruleName}.md
// DELETED — rules/ reference copies no longer exist
// Update tests to check .claude/rules/ instead

// Old: agents/${agentName}.yaml
// DELETED — agents/*.yaml no longer exist
// Update tests to check .claude/agents/${agentName}.md instead

// Old: test-utils.js
// New: .claude-sentient/test-utils.js

// Old: generate-checksums.sh
// New: .claude-sentient/generate-checksums.sh
```

For the `fileExists()` glob checks:
```javascript
// Old:
{ glob: 'profiles/python.yaml', desc: 'profiles' },
{ glob: 'profiles/typescript.yaml', desc: 'profiles' },
{ glob: 'rules/_index.md', desc: 'rules index' },
{ glob: 'test-utils.js', desc: 'shared test infrastructure' },

// New:
{ glob: '.claude-sentient/profiles/python.yaml', desc: 'profiles' },
{ glob: '.claude-sentient/profiles/typescript.yaml', desc: 'profiles' },
{ glob: '.claude/rules/_index.md', desc: 'rules index' },
{ glob: '.claude-sentient/test-utils.js', desc: 'shared test infrastructure' },
```

**Remove or rewrite the `rules/` tests:**
- The test "all rules in rules/_index.md exist in rules/ directory" should check `.claude/rules/` instead
- The "learnings.md special case" test needs updating — learnings.md lives only in `.claude/rules/`, never had a copy in `rules/`

**Remove or rewrite the `agents/*.yaml` tests:**
- Tests that checked `agents/${name}.yaml` existence should check `.claude/agents/${name}.md` instead
- YAML field validation tests need rewriting to parse frontmatter from `.md` files

**Update installer parity checks:**
- Tests that count "profiles" in install.sh output should match new path strings
- Remove checks for `rules/` and `agents/` copy sections

- [ ] **Step 2: Run integration tests**

Run: `bash --norc --noprofile -c "node .claude-sentient/integration/__tests__/test-integration.js" 2>/dev/null`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add .claude-sentient/integration/
git commit -m "fix: update integration tests for .claude-sentient/ directory structure"
```

---

## Task 8: Update generate-checksums.sh

**Files:**
- Modify: `.claude-sentient/generate-checksums.sh`

- [ ] **Step 1: Update all find paths**

```bash
# Old:
find profiles -name "*.yaml" -o -name "CLAUDE.md"
find agents -name "*.yaml" -o -name "CLAUDE.md"
find schemas -name "*.json"
find rules -name "*.md"
find templates -name "*.md" -o -name "*.json"
find examples -name "*.md"
sha256sum test-utils.js >> CHECKSUMS.sha256

# New:
find .claude-sentient/profiles -name "*.yaml" -o -name "CLAUDE.md"
# DELETE: agents/*.yaml line (eliminated)
find .claude-sentient/schemas -name "*.json"
# DELETE: rules/*.md line (eliminated)
find .claude-sentient/templates -name "*.md" -o -name "*.json"
find .claude-sentient/examples -name "*.md"
sha256sum .claude-sentient/test-utils.js >> .claude-sentient/CHECKSUMS.sha256
```

Also update the output path:
```bash
# Old: > CHECKSUMS.sha256
# New: > .claude-sentient/CHECKSUMS.sha256
```

- [ ] **Step 2: Run the script**

```bash
bash .claude-sentient/generate-checksums.sh
```

- [ ] **Step 3: Commit**

```bash
git add .claude-sentient/generate-checksums.sh .claude-sentient/CHECKSUMS.sha256
git commit -m "fix: update generate-checksums.sh paths for .claude-sentient/"
```

---

## Task 9: Update Command and Skill Files

**Why:** Commands reference `profiles/*.yaml`, `agents/*.yaml`, `rules/_index.md`, `documentation/`, and `templates/` in their instructions.

**Files:**
- Modify: `.claude/commands/cs-loop.md`
- Modify: `.claude/commands/cs-team.md`
- Modify: `.claude/commands/CLAUDE.md`
- Modify: `.claude/skills/profile-detection/SKILL.md`
- Modify: `.claude/skills/quality-gates/references/gate-commands.md`
- Modify: `.claude/skills/profile-detection/references/indicator-files.md`

- [ ] **Step 1: Update cs-loop.md**

Search and replace:
- `profiles/*.yaml` → `.claude-sentient/profiles/*.yaml`
- `profiles/CLAUDE.md` → `.claude-sentient/profiles/CLAUDE.md`
- `rules/_index.md` → `.claude/rules/_index.md` (rules now only in .claude/)
- `documentation/` → `.claude-sentient/documentation/`
- `templates/` → `.claude-sentient/templates/`

- [ ] **Step 2: Update cs-team.md**

Search and replace:
- `agents/*.yaml` → `.claude/agents/*.md`
- `agents/*.yaml files` → `.claude/agents/*.md files`

- [ ] **Step 3: Update commands CLAUDE.md**

Search and replace:
- `rules/_index.md` → `.claude/rules/_index.md`

- [ ] **Step 4: Update profile-detection SKILL.md**

Search and replace:
- `profiles/CLAUDE.md` → `.claude-sentient/profiles/CLAUDE.md`
- `profiles/{name}.yaml` → `.claude-sentient/profiles/{name}.yaml`
- `rules/_index.md` → `.claude/rules/_index.md`

- [ ] **Step 5: Update gate-commands.md**

Search and replace:
- `profiles/{name}.yaml` → `.claude-sentient/profiles/{name}.yaml`

- [ ] **Step 6: Update indicator-files.md**

Search and replace:
- `templates/` → `.claude-sentient/templates/`

- [ ] **Step 7: Commit**

```bash
git add .claude/commands/ .claude/skills/
git commit -m "refactor: update command and skill path references for .claude-sentient/"
```

---

## Task 10: Update Root Documentation (CLAUDE.md, README.md)

**Files:**
- Modify: `CLAUDE.md`
- Modify: `README.md`

- [ ] **Step 1: Update CLAUDE.md**

Read `CLAUDE.md`. Apply these changes:

```markdown
# Old: profiles/CLAUDE.md
# New: .claude-sentient/profiles/CLAUDE.md

# Old: profiles/*.yaml
# New: .claude-sentient/profiles/*.yaml

# Old: agents/CLAUDE.md
# REMOVE this row — agents CLAUDE.md eliminated

# Old: documentation/16-native-tips.md
# New: .claude-sentient/documentation/16-native-tips.md

# Old: See @rules/_index.md
# New: See @.claude/rules/_index.md (or just remove the @ prefix since it's in .claude/)
```

Update the Nested Context Architecture table — remove the `agents/CLAUDE.md` row, update `profiles/CLAUDE.md` path.

- [ ] **Step 2: Update README.md**

Read `README.md`. Apply these changes:

Update badge links:
```markdown
# Old: [![Profiles](https://img.shields.io/badge/profiles-9-orange.svg)](profiles/)
# New: [![Profiles](https://img.shields.io/badge/profiles-9-orange.svg)](.claude-sentient/profiles/)
```

Update profile table links:
```markdown
# Old: [python.yaml](profiles/python.yaml)
# New: [python.yaml](.claude-sentient/profiles/python.yaml)
# (repeat for all 9 profiles)
```

Update tree diagram:
```markdown
# Old:
├── profiles/*.yaml          # 9 language profiles
├── agents/*.yaml            # 9 specialized agent roles
├── schemas/*.json           # 12 JSON schemas
├── templates/*.md           # Governance templates
├── test-utils.js            # Shared test infrastructure
└── rules/*.md               # 15 topic rules

# New:
├── .claude-sentient/        # Claude Sentient project files
│   ├── profiles/*.yaml      # 9 language profiles
│   ├── schemas/*.json       # 12 JSON schemas
│   ├── templates/           # Governance templates
│   ├── documentation/       # Feature documentation
│   ├── examples/            # Example CLAUDE.md templates
│   └── test-utils.js        # Shared test infrastructure
```

Update test commands:
```markdown
# Old: node profiles/__tests__/test-profiles.js
# New: node .claude-sentient/profiles/__tests__/test-profiles.js

# Old: node agents/__tests__/test-agents.js
# REMOVE (eliminated)

# Old: node schemas/__tests__/test-schemas.js
# New: node .claude-sentient/schemas/__tests__/test-schemas.js

# Old: node integration/__tests__/test-integration.js
# New: node .claude-sentient/integration/__tests__/test-integration.js
```

Update reference links:
```markdown
# Old: [profiles/](profiles/)
# New: [profiles/](.claude-sentient/profiles/)

# Old: [rules/](rules/)
# REMOVE or change to: [rules/](.claude/rules/)

# Old: [templates/](templates/)
# New: [templates/](.claude-sentient/templates/)
```

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md README.md
git commit -m "docs: update CLAUDE.md and README.md path references for .claude-sentient/"
```

---

## Task 11: Update Governance and Documentation Files

**Files:**
- Modify: `.claude-sentient/STATUS.md`
- Modify: `.claude-sentient/CHANGELOG.md`
- Modify: `.claude-sentient/DECISIONS.md`
- Modify: All `.claude-sentient/documentation/*.md` files that reference moved paths

- [ ] **Step 1: Update STATUS.md**

Search and replace:
- `profiles/*.yaml` → `.claude-sentient/profiles/*.yaml`
- `profiles/__tests__/` → `.claude-sentient/profiles/__tests__/`
- `agents/*.yaml` → `.claude/agents/*.md`
- `agents/__tests__/` → removed (tests eliminated with yaml)
- `schemas/__tests__/` → `.claude-sentient/schemas/__tests__/`
- `integration/__tests__/` → `.claude-sentient/integration/__tests__/`
- `templates/` references → `.claude-sentient/templates/`
- `rules/_index.md` → `.claude/rules/_index.md`
- `generate-checksums.sh` → `.claude-sentient/generate-checksums.sh`

- [ ] **Step 2: Update CHANGELOG.md**

This file has ~27 historical references. For historical entries, leave them as-is (they describe what happened at that version). Only update the v1.6.0 entry and any forward-looking text.

Add a new entry at the top:

```markdown
## v1.7.0 - Directory Restructuring

### Changed
- All project files moved to `.claude-sentient/` directory (profiles, schemas, templates, examples, documentation, integration tests)
- `rules/` reference copies eliminated — `.claude/rules/` is the single source of truth
- `agents/*.yaml` eliminated — `.claude/agents/*.md` is the single source of truth
- Uninstall simplified: single `rm -rf .claude-sentient/` replaces 7 directory removals
- `getCSDir()` in utils.cjs provides centralized path resolution

### Migration
If upgrading from v1.6.0, run `install.sh` — it will create `.claude-sentient/` and populate it. Manually remove old root directories: `rm -rf profiles/ agents/ rules/ schemas/ templates/ examples/ documentation/ integration/ test-utils.js`
```

- [ ] **Step 3: Update documentation files**

For each file in `.claude-sentient/documentation/`, search and replace:
- `profiles/*.yaml` → `.claude-sentient/profiles/*.yaml`
- `profiles/{name}.yaml` → `.claude-sentient/profiles/{name}.yaml`
- `agents/*.yaml` → `.claude/agents/*.md`
- `rules/_index.md` → `.claude/rules/_index.md`
- `schemas/` → `.claude-sentient/schemas/`
- `templates/` → `.claude-sentient/templates/`
- `documentation/` → `.claude-sentient/documentation/`

Key files with the most references:
- `documentation/01-autonomous-loop.md` (4 references)
- `documentation/05-quality-gates.md` (1 reference)
- `documentation/07-profile-system.md` (3 references)
- `documentation/08-agent-roles.md` (6 references)
- `documentation/09-rules-system.md` (3 references)
- `documentation/11-installation.md` (7 references)
- `documentation/12-worktree-config-observability.md` (1 reference)
- `documentation/_index.md` (update any paths in the index)

- [ ] **Step 4: Update DECISIONS.md**

Minimal changes — most references are to `.claude/rules/` which stays. Update any `rules/` (without `.claude/` prefix) references.

- [ ] **Step 5: Commit**

```bash
git add .claude-sentient/
git commit -m "docs: update all documentation path references for .claude-sentient/"
```

---

## Task 12: Update .claude/rules/learnings.md References

**Why:** The learnings file has references to old paths in historical entries and path conventions.

**Files:**
- Modify: `.claude/rules/learnings.md`

- [ ] **Step 1: Update forward-looking path references**

In the learnings file, update any conventions/rules that reference the old paths:
- "learnings.md special case: Lives only in `.claude/rules/`..., NOT in `rules/`" → update to note `rules/` no longer exists
- Any reference to `agents/*.yaml` → `.claude/agents/*.md`
- Any reference to `profiles/*.yaml` → `.claude-sentient/profiles/*.yaml`

Leave historical entries (dates before today) as-is — they document what was true at that time.

- [ ] **Step 2: Commit**

```bash
git add .claude/rules/learnings.md
git commit -m "docs: update learnings.md path references for restructuring"
```

---

## Task 13: Update MEMORY.md and Add Migration Learning

**Files:**
- Modify: `/home/joe/.claude/projects/-home-joe-github-claude-sentient/memory/MEMORY.md`

- [ ] **Step 1: Update Key File Locations in MEMORY.md**

```markdown
## Key File Locations
- Commands: `.claude/commands/cs-*.md` (19 commands)
- Hooks: `.claude/hooks/*.cjs` (17 hooks + utils.cjs)
- Profiles: `.claude-sentient/profiles/*.yaml` (9 language profiles)
- Agents: `.claude/agents/*.md` (9 native agent definitions — single source of truth)
- Schemas: `.claude-sentient/schemas/*.json` (12 JSON schemas)
- Tests: `.claude-sentient/profiles/__tests__/`, `.claude/hooks/__tests__/`, `.claude/commands/__tests__/`, `.claude-sentient/schemas/__tests__/`, `.claude-sentient/integration/__tests__/`
- Install: `install.sh`, `install.ps1`, `uninstall.sh`, `uninstall.ps1`, `.claude-sentient/generate-checksums.sh`
```

Update test commands:
```bash
bash --norc --noprofile -c "node .claude-sentient/profiles/__tests__/test-profiles.js" 2>/dev/null
bash --norc --noprofile -c "node .claude/hooks/__tests__/test-hooks.js" 2>/dev/null
bash --norc --noprofile -c "node .claude/commands/__tests__/test-commands.js" 2>/dev/null
bash --norc --noprofile -c "node .claude-sentient/schemas/__tests__/test-schemas.js" 2>/dev/null
bash --norc --noprofile -c "node .claude-sentient/integration/__tests__/test-integration.js" 2>/dev/null
```

Add to Lessons Learned:
```
- **agents/*.yaml eliminated**: v1.7.0 removed agents/*.yaml — .claude/agents/*.md is the single source of truth. agent-tracker.cjs reads from .claude/agents/ now.
- **rules/ reference copies eliminated**: v1.7.0 removed rules/ directory — .claude/rules/ is the single source of truth
- **CS_DIR constant**: Use getCSDir() from utils.cjs to resolve .claude-sentient/ path. Never hardcode it.
- **Test count reduced**: Agent tests (108) were eliminated with agents/*.yaml. 5 test suites remain.
```

- [ ] **Step 2: No commit needed** (memory files are outside the git repo)

---

## Task 14: Final Verification and Version Bump

**Files:**
- Modify: `CLAUDE.md` (version bump to 1.7.0)
- Modify: `.claude-sentient/CHANGELOG.md` (already updated in Task 11)
- Modify: `.claude-sentient/STATUS.md` (component counts)
- Run: `.claude-sentient/generate-checksums.sh`

- [ ] **Step 1: Bump version**

In `CLAUDE.md`: change `**Version:** 1.6.0` to `**Version:** 1.7.0`

- [ ] **Step 2: Run all test suites**

```bash
bash --norc --noprofile -c "node .claude/hooks/__tests__/test-notification.js" 2>/dev/null
bash --norc --noprofile -c "node .claude/hooks/__tests__/test-hooks.js" 2>/dev/null
bash --norc --noprofile -c "node .claude/commands/__tests__/test-commands.js" 2>/dev/null
bash --norc --noprofile -c "node .claude-sentient/profiles/__tests__/test-profiles.js" 2>/dev/null
bash --norc --noprofile -c "node .claude-sentient/schemas/__tests__/test-schemas.js" 2>/dev/null
bash --norc --noprofile -c "node .claude-sentient/integration/__tests__/test-integration.js" 2>/dev/null
```

Expected: ALL PASS. Fix any failures before proceeding.

- [ ] **Step 3: Regenerate checksums**

```bash
bash .claude-sentient/generate-checksums.sh
```

- [ ] **Step 4: Commit**

```bash
git add CLAUDE.md .claude-sentient/CHECKSUMS.sha256 .claude-sentient/STATUS.md
git commit -m "chore: bump to v1.7.0, verify restructuring, regenerate checksums"
```

---

## Self-Review Checklist

### Spec Coverage
- [x] Task 1: CS_DIR constant in utils.cjs
- [x] Task 2: Physical file moves + duplicate elimination
- [x] Task 3: agent-tracker.cjs reads .claude/agents/*.md
- [x] Task 4: Test require() paths updated
- [x] Task 5: Install scripts updated
- [x] Task 6: Uninstall scripts updated
- [x] Task 7: Integration test path assertions
- [x] Task 8: generate-checksums.sh paths
- [x] Task 9: Command and skill file references
- [x] Task 10: CLAUDE.md and README.md
- [x] Task 11: Governance docs and documentation/*.md
- [x] Task 12: learnings.md references
- [x] Task 13: MEMORY.md update
- [x] Task 14: Version bump and final verification

### Design Decisions Applied
- [x] Decision 1: Installers stay at root
- [x] Decision 2: rules/ reference copies eliminated (Tasks 2, 7, 9, 10, 11)
- [x] Decision 3: agents/*.yaml eliminated (Tasks 2, 3, 7, 9, 10, 11)
- [x] Decision 4: CS_DIR constant (Task 1)
- [x] Decision 5: Source repo matches install footprint (Task 2)
- [x] Decision 6: Tests move with parent dirs (Tasks 2, 4)

### Path Consistency
- `.claude-sentient/profiles/` used consistently (not `profiles/`)
- `.claude/agents/*.md` used consistently (not `agents/*.yaml`)
- `.claude/rules/` used consistently (not `rules/`)
- `getCSDir()` used in hooks (not hardcoded `.claude-sentient/`)
