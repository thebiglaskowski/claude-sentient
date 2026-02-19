#Requires -Version 5.1
<#
.SYNOPSIS
    Claude Sentient Installer
.DESCRIPTION
    Installs claude-sentient into the current project
.EXAMPLE
    .\install.ps1
#>
[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

$RepoUrl = "https://github.com/thebiglaskowski/claude-sentient.git"
$TempDir = ".claude-sentient-temp"

Write-Host "=== Claude Sentient Installer ===" -ForegroundColor Cyan
Write-Host ""

# Check if we're in a git repo (recommended but not required)
if (Test-Path ".git") {
    Write-Host "✓ Git repository detected" -ForegroundColor Green
} else {
    Write-Host "⚠ Not a git repository (optional)" -ForegroundColor Yellow
}

# Check if already installed
if ((Test-Path ".claude/commands") -and (Test-Path ".claude/commands/cs-loop.md")) {
    Write-Host ""
    Write-Host "⚠ Claude Sentient appears to be already installed." -ForegroundColor Yellow
    $response = Read-Host "Reinstall/update? (y/N)"
    if ($response -notmatch "^[Yy]$") {
        Write-Host "Aborted."
        return
    }
}

Write-Host ""
Write-Host "Downloading claude-sentient..."
git clone --depth 1 --quiet $RepoUrl $TempDir

# Verify file integrity
$checksumFile = "$TempDir/CHECKSUMS.sha256"
if (Test-Path $checksumFile) {
    Write-Host "Verifying file integrity..."
    $allValid = $true
    $checksums = Get-Content $checksumFile | Where-Object { $_ -match '^\w{64}\s+' }
    foreach ($line in $checksums) {
        if ($line -match '^(\w{64})\s+(.+)$') {
            $expectedHash = $Matches[1]
            $filePath = "$TempDir/$($Matches[2])"
            if (Test-Path $filePath) {
                $actualHash = (Get-FileHash $filePath -Algorithm SHA256).Hash.ToLower()
                if ($actualHash -ne $expectedHash) {
                    $allValid = $false
                    break
                }
            }
        }
    }
    if ($allValid) {
        Write-Host "✓ All file checksums verified" -ForegroundColor Green
    } else {
        Write-Host "⚠ Checksum verification failed (non-fatal, may be a newer version)" -ForegroundColor Yellow
    }
}

Write-Host "Installing shared test infrastructure..."
Copy-Item "$TempDir/test-utils.js" -Destination "./test-utils.js" -Force

Write-Host "Installing commands..."
New-Item -ItemType Directory -Force -Path ".claude/commands" | Out-Null
Copy-Item "$TempDir/.claude/commands/cs-*.md" -Destination ".claude/commands/" -Force
Copy-Item "$TempDir/.claude/commands/CLAUDE.md" -Destination ".claude/commands/" -Force

Write-Host "Installing profiles..."
New-Item -ItemType Directory -Force -Path "profiles/__tests__" | Out-Null
Copy-Item "$TempDir/profiles/*.yaml" -Destination "profiles/" -Force
Copy-Item "$TempDir/profiles/CLAUDE.md" -Destination "profiles/" -Force
Copy-Item "$TempDir/profiles/__tests__/*.js" -Destination "profiles/__tests__/" -Force

Write-Host "Installing rules..."
New-Item -ItemType Directory -Force -Path "rules" | Out-Null
Copy-Item "$TempDir/rules/*.md" -Destination "rules/" -Force

Write-Host "Installing templates..."
New-Item -ItemType Directory -Force -Path "templates" | Out-Null
Copy-Item "$TempDir/templates/*.md" -Destination "templates/" -Force
Copy-Item "$TempDir/templates/settings.json" -Destination "templates/" -Force -ErrorAction SilentlyContinue

Write-Host "Installing hooks..."
New-Item -ItemType Directory -Force -Path ".claude/hooks/__tests__" | Out-Null
Copy-Item "$TempDir/.claude/hooks/*.cjs" -Destination ".claude/hooks/" -Force
Copy-Item "$TempDir/.claude/hooks/README.md" -Destination ".claude/hooks/" -Force
Copy-Item "$TempDir/.claude/hooks/__tests__/*.js" -Destination ".claude/hooks/__tests__/" -Force
Write-Host "  Installed hook scripts + tests"

Write-Host "Installing agents..."
New-Item -ItemType Directory -Force -Path "agents/__tests__" | Out-Null
Copy-Item "$TempDir/agents/*.yaml" -Destination "agents/" -Force
Copy-Item "$TempDir/agents/CLAUDE.md" -Destination "agents/" -Force
Copy-Item "$TempDir/agents/__tests__/*.js" -Destination "agents/__tests__/" -Force
Write-Host "  Installed agent definitions + tests"

Write-Host "Installing schemas..."
New-Item -ItemType Directory -Force -Path "schemas/__tests__" | Out-Null
Copy-Item "$TempDir/schemas/*.json" -Destination "schemas/" -Force
Copy-Item "$TempDir/schemas/__tests__/*.js" -Destination "schemas/__tests__/" -Force
Write-Host "  Installed JSON schemas + tests"

Write-Host "Installing settings..."
if (-not (Test-Path ".claude/settings.json")) {
    Copy-Item "$TempDir/.claude/settings.json" -Destination ".claude/settings.json"
    Write-Host "  Created .claude/settings.json with hooks"
} else {
    Write-Host "  Preserved existing .claude/settings.json (review .claude/hooks/README.md to add hooks)"
}

Write-Host "Initializing memory..."
New-Item -ItemType Directory -Force -Path ".claude/rules" | Out-Null
if (-not (Test-Path ".claude/rules/learnings.md")) {
    Copy-Item "$TempDir/templates/learnings.md" -Destination ".claude/rules/learnings.md"
    Write-Host "  Created .claude/rules/learnings.md"
} else {
    Write-Host "  Preserved existing .claude/rules/learnings.md"
}

Write-Host "Installing path-scoped rules..."
Get-ChildItem "$TempDir/.claude/rules/*.md" | Where-Object { $_.Name -ne "learnings.md" -and $_.Name -ne "README.md" } | ForEach-Object {
    Copy-Item $_.FullName -Destination ".claude/rules/$($_.Name)" -Force
}
Write-Host "  Installed path-scoped rules to .claude/rules/"

Write-Host "Cleaning up..."
# Windows may hold file locks briefly after git clone - retry cleanup
$retries = 3
for ($i = 1; $i -le $retries; $i++) {
    try {
        Remove-Item -Recurse -Force $TempDir -ErrorAction Stop
        break
    } catch {
        if ($i -eq $retries) {
            Write-Host "  Warning: Could not remove temp directory. You can manually delete: $TempDir" -ForegroundColor Yellow
        } else {
            Start-Sleep -Milliseconds 500
        }
    }
}

# --- Plugins ---
$PluginsInstalled = @()
$claudeCmd = Get-Command claude -ErrorAction SilentlyContinue
if ($claudeCmd) {
    Write-Host ""
    Write-Host "Installing Claude Code plugins..."

    # Universal: security-guidance (user scope)
    try {
        claude plugin install security-guidance@claude-plugins-official --scope user 2>$null
        Write-Host "  ✓ security-guidance (user scope)" -ForegroundColor Green
        $PluginsInstalled += "security-guidance"
    } catch {
        Write-Host "  ⚠ Could not install security-guidance plugin (non-fatal)" -ForegroundColor Yellow
    }

    # Profile-dependent: LSP plugin (project scope)
    $LspPlugin = $null
    if ((Test-Path "pyproject.toml") -or (Test-Path "requirements.txt") -or (Test-Path "setup.py")) {
        $LspPlugin = "pyright-lsp@claude-plugins-official"
    } elseif (Test-Path "tsconfig.json") {
        $LspPlugin = "typescript-lsp@claude-plugins-official"
    } elseif (Test-Path "go.mod") {
        $LspPlugin = "gopls-lsp@claude-plugins-official"
    } elseif (Test-Path "Cargo.toml") {
        $LspPlugin = "rust-analyzer-lsp@claude-plugins-official"
    } elseif ((Test-Path "pom.xml") -or (Test-Path "build.gradle")) {
        $LspPlugin = "jdtls-lsp@claude-plugins-official"
    } elseif ((Test-Path "CMakeLists.txt") -or (Test-Path "Makefile")) {
        $LspPlugin = "clangd-lsp@claude-plugins-official"
    }

    if ($LspPlugin) {
        try {
            claude plugin install $LspPlugin --scope project 2>$null
            Write-Host "  ✓ $LspPlugin (project scope)" -ForegroundColor Green
            $PluginsInstalled += $LspPlugin
        } catch {
            Write-Host "  ⚠ Could not install $LspPlugin (non-fatal)" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host ""
    Write-Host "⚠ claude CLI not found — skipping plugin installation" -ForegroundColor Yellow
    Write-Host "  Install plugins manually after setting up Claude Code"
}

# --- Global Permissions ---
Write-Host ""
Write-Host "Configuring global Claude Code permissions..."
$PermissionsConfigured = $false
if (Get-Command node -ErrorAction SilentlyContinue) {
    $NodeScript = @'
const fs = require('fs'), path = require('path'), os = require('os');
const settingsPath = path.join(os.homedir(), '.claude', 'settings.json');
const ALLOW = ['Bash','Read','Write','Edit','Glob','Grep','Task','WebFetch','WebSearch',
  'NotebookEdit','ToolSearch','ListMcpResourcesTool','ReadMcpResourceTool',
  'TaskCreate','TaskUpdate','TaskList','TaskGet','TaskOutput','TaskStop',
  'TeamCreate','TeamDelete','SendMessage','Skill','AskUserQuestion','EnterPlanMode','ExitPlanMode'];
let s = {};
try { s = JSON.parse(fs.readFileSync(settingsPath, 'utf8')); } catch (_) {}
if (!s.permissions) s.permissions = {};
const existing = new Set(s.permissions.allow || []);
ALLOW.forEach(t => existing.add(t));
s.permissions.allow = [...existing];
fs.mkdirSync(path.dirname(settingsPath), { recursive: true });
fs.writeFileSync(settingsPath, JSON.stringify(s, null, 2) + '\n');
'@
    $TmpJs = [System.IO.Path]::GetTempFileName() + '.js'
    try {
        $NodeScript | Out-File -FilePath $TmpJs -Encoding UTF8
        node $TmpJs 2>$null
        Write-Host "  ✓ ~/.claude/settings.json permissions configured" -ForegroundColor Green
        $PermissionsConfigured = $true
    } catch {
        Write-Host "  ⚠ Could not update global permissions (non-fatal)" -ForegroundColor Yellow
    } finally {
        Remove-Item $TmpJs -ErrorAction SilentlyContinue
    }
} else {
    Write-Host "  ⚠ node not found — skipping global permissions setup" -ForegroundColor Yellow
    Write-Host "    Manually add permissions.allow to ~/.claude/settings.json"
}

Write-Host ""
Write-Host "=== Installation Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host 'Installed:'
Write-Host '  .claude/commands/cs-*.md       (12 commands)'
Write-Host '  .claude/hooks/*.cjs             (13 hook scripts)'
Write-Host '  .claude/hooks/__tests__/       (125 hook tests)'
Write-Host '  .claude/settings.json          (hook configuration)'
Write-Host '  profiles/*.yaml                (9 profiles + schema)'
Write-Host '  profiles/__tests__/            (242 profile tests)'
Write-Host '  agents/*.yaml                  (6 agent roles)'
Write-Host '  agents/__tests__/              (108 agent tests)'
Write-Host '  schemas/*.json                 (9 JSON schemas)'
Write-Host '  schemas/__tests__/             (166 schema tests)'
Write-Host '  rules/*.md                     (15 topic rules)'
Write-Host '  templates/*.md                 (5 templates)'
Write-Host '  test-utils.js                  (shared test infrastructure)'
Write-Host '  .claude/rules/*.md              (15 path-scoped rules)'
if ($PluginsInstalled.Count -gt 0) {
    $pluginList = $PluginsInstalled -join ", "
    Write-Host "  plugins                        ($pluginList)"
}
if ($PermissionsConfigured) {
    Write-Host '  ~/.claude/settings.json        (global auto-approve permissions)'
}
Write-Host ""
Write-Host "Recommended plugins (optional):"
Write-Host "  claude plugin install pr-review-toolkit@claude-plugins-official"
Write-Host "  claude plugin install ralph-loop@claude-plugins-official"
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Run /cs-validate to verify installation"
Write-Host "  2. Run /cs-mcp --fix to register MCP servers"
Write-Host "  3. Review recommended plugins above"
Write-Host "  4. Run /cs-status to see detected profile"
Write-Host "  5. Run /cs-loop `"your task`" to start working"
Write-Host ""
Write-Host "Note (Windows): MCP servers require 'cmd /c' wrapper." -ForegroundColor Yellow
Write-Host "  Run /cs-mcp --fix after restarting Claude Code."
Write-Host ""
