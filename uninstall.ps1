#Requires -Version 5.1
<#
.SYNOPSIS
    Claude Sentient Uninstaller
.DESCRIPTION
    Cleanly removes claude-sentient from the current project
.PARAMETER Purge
    Remove everything including learnings.md
.PARAMETER KeepSettings
    Don't touch .claude/settings.json
.PARAMETER DryRun
    Show what would be removed without removing
.EXAMPLE
    .\uninstall.ps1
.EXAMPLE
    .\uninstall.ps1 -Purge
.EXAMPLE
    .\uninstall.ps1 -DryRun
#>
[CmdletBinding()]
param(
    [switch]$Purge,
    [switch]$KeepSettings,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$script:removed = 0
$script:backedUp = 0

function Remove-FileItem {
    param([string]$Path)
    if (Test-Path $Path -PathType Leaf) {
        if ($DryRun) {
            Write-Host "  [remove] $Path"
        } else {
            Remove-Item $Path -Force
        }
        $script:removed++
    }
}

function Remove-DirItem {
    param([string]$Path)
    if (Test-Path $Path -PathType Container) {
        if ($DryRun) {
            Write-Host "  [remove] $Path/"
        } else {
            Remove-Item $Path -Recurse -Force
        }
        $script:removed++
    }
}

function Remove-DirIfEmpty {
    param([string]$Path)
    if ((Test-Path $Path -PathType Container) -and
        ((Get-ChildItem $Path -Force | Measure-Object).Count -eq 0)) {
        if ($DryRun) {
            Write-Host "  [remove] $Path/ (empty)"
        } else {
            Remove-Item $Path -Force
        }
    }
}

Write-Host "=== Claude Sentient Uninstaller ===" -ForegroundColor Cyan
Write-Host ""

# Detect installation
if (-not (Test-Path ".claude/commands/cs-loop.md")) {
    Write-Host "Claude Sentient does not appear to be installed in this directory."
    exit 0
}

if ($DryRun) {
    Write-Host "[DRY RUN] Showing what would be removed..." -ForegroundColor Yellow
    Write-Host ""
}

# Confirm (skip for dry run)
if (-not $DryRun) {
    $response = Read-Host "Remove Claude Sentient from this project? (y/N)"
    if ($response -notmatch "^[Yy]$") {
        Write-Host "Aborted."
        exit 0
    }
    Write-Host ""
}

# --- Shared test infrastructure ---
Remove-FileItem "test-utils.js"

# --- Commands ---
Write-Host "Removing commands..."
Get-ChildItem ".claude/commands/cs-*.md" -ErrorAction SilentlyContinue | ForEach-Object {
    Remove-FileItem $_.FullName
}
Remove-FileItem ".claude/commands/CLAUDE.md"

# --- Hooks ---
Write-Host "Removing hooks..."
Get-ChildItem ".claude/hooks/*.js" -ErrorAction SilentlyContinue | ForEach-Object {
    Remove-FileItem $_.FullName
}
Remove-FileItem ".claude/hooks/README.md"
Remove-DirItem ".claude/hooks/__tests__"
Remove-DirIfEmpty ".claude/hooks"

# --- Profiles ---
Write-Host "Removing profiles..."
Remove-DirItem "profiles"

# --- Agents ---
Write-Host "Removing agents..."
Remove-DirItem "agents"

# --- Rules (project root) ---
Write-Host "Removing rules..."
Remove-DirItem "rules"

# --- Templates ---
Write-Host "Removing templates..."
Remove-DirItem "templates"

# --- Schemas ---
Write-Host "Removing schemas..."
Remove-DirItem "schemas"

# --- Dashboard ---
Write-Host "Removing dashboard..."
Remove-DirItem "dashboard"

# --- Path-scoped rules (.claude/rules/) ---
Write-Host "Removing path-scoped rules..."
$scopedRules = @(
    "security.md", "testing.md", "api-design.md", "database.md",
    "ui-ux-design.md", "error-handling.md", "performance.md", "logging.md",
    "terminal-ui.md", "documentation.md", "prompt-structure.md", "git-workflow.md",
    "anthropic-patterns.md", "code-quality.md", "README.md"
)
foreach ($rule in $scopedRules) {
    Remove-FileItem ".claude/rules/$rule"
}

# --- Learnings ---
if (-not $Purge) {
    if (Test-Path ".claude/rules/learnings.md") {
        Write-Host "Preserving .claude/rules/learnings.md (use -Purge to remove)" -ForegroundColor Yellow
    }
} else {
    Write-Host "Removing learnings..."
    Remove-FileItem ".claude/rules/learnings.md"
}

# --- Settings ---
if ($KeepSettings) {
    if (Test-Path ".claude/settings.json") {
        Write-Host "Preserving .claude/settings.json (-KeepSettings)" -ForegroundColor Yellow
    }
} else {
    if (Test-Path ".claude/settings.json") {
        Write-Host "Backing up and removing settings..."
        if ($DryRun) {
            Write-Host "  [backup] .claude/settings.json -> .claude/settings.json.bak"
            Write-Host "  [remove] .claude/settings.json"
        } else {
            Copy-Item ".claude/settings.json" ".claude/settings.json.bak" -Force
            Remove-Item ".claude/settings.json" -Force
            $script:backedUp++
        }
        $script:removed++
    }
}

# --- State directory ---
Remove-DirItem ".claude/state"

# --- Plugins (project-scoped only) ---
$claudeCmd = Get-Command claude -ErrorAction SilentlyContinue
if ($claudeCmd) {
    Write-Host "Removing project-scoped plugins..."
    $lspPlugins = @(
        "pyright-lsp@claude-plugins-official",
        "typescript-lsp@claude-plugins-official",
        "gopls-lsp@claude-plugins-official",
        "rust-analyzer-lsp@claude-plugins-official",
        "jdtls-lsp@claude-plugins-official",
        "clangd-lsp@claude-plugins-official"
    )
    foreach ($plugin in $lspPlugins) {
        try { claude plugin uninstall $plugin --scope project 2>$null } catch {}
    }
    Write-Host "  Note: security-guidance (user scope) preserved — benefits all projects" -ForegroundColor Yellow
}

# --- Clean up empty directories ---
Write-Host "Cleaning up..."
Remove-DirIfEmpty ".claude/rules"
Remove-DirIfEmpty ".claude/commands"
Remove-DirIfEmpty ".claude"

Write-Host ""
Write-Host "=== Uninstall Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "Removed $($script:removed) items."
if ($script:backedUp -gt 0) {
    Write-Host "Backed up: .claude/settings.json -> .claude/settings.json.bak" -ForegroundColor Yellow
}
if ((-not $Purge) -and (Test-Path ".claude/rules/learnings.md" -ErrorAction SilentlyContinue)) {
    Write-Host "Preserved: .claude/rules/learnings.md" -ForegroundColor Yellow
}
Write-Host ""
Write-Host "Note: CLAUDE.md was not modified. Remove it manually if desired."
Write-Host ""
