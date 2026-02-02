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
Copy-Item "$TempDir/commands/cs-*.md" -Destination ".claude/commands/" -Force

Write-Host "Installing profiles..."
New-Item -ItemType Directory -Force -Path "profiles" | Out-Null
Copy-Item "$TempDir/profiles/*.yaml" -Destination "profiles/" -Force

Write-Host "Installing templates..."
New-Item -ItemType Directory -Force -Path "templates" | Out-Null
Copy-Item "$TempDir/templates/*.md" -Destination "templates/" -Force

Write-Host "Initializing memory..."
New-Item -ItemType Directory -Force -Path ".claude/rules" | Out-Null
if (-not (Test-Path ".claude/rules/learnings.md")) {
    Copy-Item "$TempDir/templates/learnings.md" -Destination ".claude/rules/learnings.md"
    Write-Host "  Created .claude/rules/learnings.md"
} else {
    Write-Host "  Preserved existing .claude/rules/learnings.md"
}

Write-Host "Cleaning up..."
Remove-Item -Recurse -Force $TempDir

Write-Host ""
Write-Host "=== Installation Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "Installed:"
Write-Host "  .claude/commands/cs-*.md  (6 commands)"
Write-Host "  profiles/*.yaml           (5 profiles)"
Write-Host "  templates/*.md            (4 templates)"
Write-Host "  .claude/rules/learnings.md"
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Run /cs-validate to verify installation"
Write-Host "  2. Run /cs-mcp --fix to register MCP servers"
Write-Host "  3. Run /cs-status to see detected profile"
Write-Host "  4. Run /cs-loop `"your task`" to start working"
Write-Host ""
