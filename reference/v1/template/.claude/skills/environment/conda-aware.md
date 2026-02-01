---
name: conda-aware
description: Check for conda environments before installing packages
model: haiku
---

# Conda Environment Awareness

Automatically check for conda/virtual environments before installing packages.

## Description

CRITICAL: Never install packages into the base conda environment or system Python. This skill activates before ANY package installation to verify the correct environment is active.

Triggers on: "pip install", "install package", "add dependency", "npm install", "conda install"

## Pre-Install Checklist

Before running ANY install command, verify:

```
┌─────────────────────────────────────────────────────────┐
│           ENVIRONMENT CHECK (REQUIRED)                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. Is conda/mamba available?                          │
│     $ conda --version                                   │
│                                                         │
│  2. What environment is active?                        │
│     $ conda info --envs | grep '*'                     │
│     $ echo $CONDA_DEFAULT_ENV                          │
│                                                         │
│  3. Is it the BASE environment?                        │
│     ⚠️  If yes, STOP and create project env            │
│                                                         │
│  4. Does project have environment config?              │
│     - environment.yml                                   │
│     - environment.yaml                                  │
│     - conda.yaml                                        │
│     - requirements.txt (with venv)                     │
│     - pyproject.toml                                    │
│     - .python-version                                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Decision Tree

```
Is conda available?
├── NO → Check for venv/virtualenv
│        ├── venv active? → ✅ Proceed with pip
│        └── No venv? → ⚠️ Create one first
│
└── YES → Check active environment
         │
         ├── base environment?
         │   └── 🛑 STOP - Create project environment
         │
         ├── Project env exists & active?
         │   └── ✅ Proceed with install
         │
         └── Project env exists but not active?
             └── ⚠️ Activate it first
```

## Environment Detection Commands

### Check Conda Status
```bash
# Is conda available?
which conda || echo "Conda not found"

# Current environment
echo $CONDA_DEFAULT_ENV
conda info --envs | grep '*'

# Is it base?
if [ "$CONDA_DEFAULT_ENV" = "base" ]; then
    echo "WARNING: Base environment active!"
fi
```

### Check for Project Environment Config
```bash
# Look for environment files
ls -la environment.yml environment.yaml conda.yaml 2>/dev/null

# Look for Python version specification
cat .python-version 2>/dev/null

# Look for pyproject.toml
grep -l "dependencies" pyproject.toml 2>/dev/null
```

### Check Virtual Environment
```bash
# Is venv active?
echo $VIRTUAL_ENV

# Does .venv exist?
ls -la .venv/bin/activate 2>/dev/null
```

## Actions by Scenario

### Scenario 1: Base Conda Environment Active
```
🛑 STOP! Do not install packages.

Action Required:
1. Check if project environment exists:
   $ conda env list | grep <project-name>

2. If exists, activate it:
   $ conda activate <project-name>

3. If not exists, create it:
   $ conda create -n <project-name> python=3.11 -y
   $ conda activate <project-name>

4. Or use environment.yml if present:
   $ conda env create -f environment.yml
   $ conda activate <env-name-from-yml>
```

### Scenario 2: No Environment Manager
```
⚠️ WARNING: No virtual environment detected.

Action Required:
1. Create a virtual environment:
   $ python -m venv .venv

2. Activate it:
   # Windows
   $ .venv\Scripts\activate

   # macOS/Linux
   $ source .venv/bin/activate

3. Then proceed with install
```

### Scenario 3: Correct Environment Active
```
✅ Project environment active: <env-name>

Proceed with installation:
$ pip install <package>
# or
$ conda install <package>
```

### Scenario 4: Environment Exists But Not Active
```
⚠️ Project environment exists but not active.

Action Required:
$ conda activate <project-name>
# or
$ source .venv/bin/activate

Then proceed with installation.
```

## Creating Project Environment

### From Scratch (Conda)
```bash
# Create with specific Python version
conda create -n myproject python=3.11 -y

# Activate
conda activate myproject

# Install packages
pip install -r requirements.txt
# or
conda install <packages>

# Export for reproducibility
conda env export > environment.yml
```

### From environment.yml
```bash
# Create from file
conda env create -f environment.yml

# Activate (name from yml file)
conda activate <env-name>
```

### From requirements.txt (venv)
```bash
# Create venv
python -m venv .venv

# Activate
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install
pip install -r requirements.txt
```

## Integration with Package Commands

### Before pip install
```
1. Run environment check
2. If base/system Python → STOP
3. If correct env → proceed
4. After install → update requirements.txt or environment.yml
```

### Before conda install
```
1. Run environment check
2. If base → STOP
3. If correct env → proceed
4. After install → conda env export > environment.yml
```

### Before npm install
```
1. Check for node_modules in project (not global)
2. Verify package.json exists
3. Proceed with local install (no -g unless explicitly needed)
```

## Warning Messages

### Base Environment Warning
```
╔══════════════════════════════════════════════════════════════╗
║  ⚠️  WARNING: CONDA BASE ENVIRONMENT ACTIVE                  ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Installing packages into base environment is discouraged.   ║
║  This can cause conflicts and is hard to reproduce.          ║
║                                                              ║
║  Please create/activate a project-specific environment:      ║
║                                                              ║
║    conda create -n <project> python=3.11                     ║
║    conda activate <project>                                  ║
║                                                              ║
║  Or if environment.yml exists:                               ║
║                                                              ║
║    conda env create -f environment.yml                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### No Environment Warning
```
╔══════════════════════════════════════════════════════════════╗
║  ⚠️  WARNING: NO VIRTUAL ENVIRONMENT DETECTED                ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Installing packages system-wide is discouraged.             ║
║                                                              ║
║  Please create a virtual environment first:                  ║
║                                                              ║
║    python -m venv .venv                                      ║
║    source .venv/bin/activate                                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

## Environment File Templates

### environment.yml (Conda)
```yaml
name: myproject
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.11
  - pip
  - pip:
    - package-from-pip
```

### requirements.txt
```
# Core dependencies
package1>=1.0.0,<2.0.0
package2~=2.1.0

# Development dependencies
# pip install -r requirements-dev.txt
```

## Always Remember

1. **NEVER install into base conda environment**
2. **NEVER install globally unless absolutely necessary**
3. **ALWAYS verify environment before install commands**
4. **ALWAYS update environment files after adding packages**
5. **ALWAYS use reproducible version specifications**
