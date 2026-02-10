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
        exit 0
    }
}

Write-Host ""
Write-Host "Downloading claude-sentient..."
git clone --depth 1 --quiet $RepoUrl $TempDir

Write-Host "Installing commands..."
New-Item -ItemType Directory -Force -Path ".claude/commands" | Out-Null
Copy-Item "$TempDir/.claude/commands/cs-*.md" -Destination ".claude/commands/" -Force

Write-Host "Installing profiles..."
New-Item -ItemType Directory -Force -Path "profiles/__tests__" | Out-Null
Copy-Item "$TempDir/profiles/*.yaml" -Destination "profiles/" -Force
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
Copy-Item "$TempDir/.claude/hooks/*.js" -Destination ".claude/hooks/" -Force
Copy-Item "$TempDir/.claude/hooks/README.md" -Destination ".claude/hooks/" -Force
Copy-Item "$TempDir/.claude/hooks/__tests__/*.js" -Destination ".claude/hooks/__tests__/" -Force
Write-Host "  Installed hook scripts + tests"

Write-Host "Installing agents..."
New-Item -ItemType Directory -Force -Path "agents/__tests__" | Out-Null
Copy-Item "$TempDir/agents/*.yaml" -Destination "agents/" -Force
Copy-Item "$TempDir/agents/CLAUDE.md" -Destination "agents/" -Force
Copy-Item "$TempDir/agents/__tests__/*.js" -Destination "agents/__tests__/" -Force
Write-Host "  Installed agent definitions + tests"

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

Write-Host ""
Write-Host "=== Installation Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host 'Installed:'
Write-Host '  .claude/commands/cs-*.md       (12 commands)'
Write-Host '  .claude/hooks/*.js             (13 hook scripts)'
Write-Host '  .claude/hooks/__tests__/       (91 hook tests)'
Write-Host '  .claude/settings.json          (hook configuration)'
Write-Host '  profiles/*.yaml                (9 profiles + schema)'
Write-Host '  profiles/__tests__/            (242 profile tests)'
Write-Host '  agents/*.yaml                  (6 agent roles)'
Write-Host '  agents/__tests__/              (108 agent tests)'
Write-Host '  rules/*.md                     (15 topic rules)'
Write-Host '  templates/*.md                 (4 templates)'
Write-Host '  .claude/rules/*.md              (17 path-scoped rules)'
Write-Host '  .claude/rules/learnings.md'
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Run /cs-validate to verify installation"
Write-Host "  2. Run /cs-mcp --fix to register MCP servers"
Write-Host "  3. Run /cs-status to see detected profile"
Write-Host "  4. Run /cs-loop `"your task`" to start working"
Write-Host ""
Write-Host "Note (Windows): MCP servers require 'cmd /c' wrapper." -ForegroundColor Yellow
Write-Host "  Run /cs-mcp --fix after restarting Claude Code."
Write-Host ""
