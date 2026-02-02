# Claude Code Template Installer (PowerShell)
# Usage: .\install.ps1 [target-directory]

param(
    [string]$TargetDir = "."
)

$ErrorActionPreference = "Stop"

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$TemplateDir = Join-Path $ScriptDir "template\.claude"

# Target paths
$TargetClaude = Join-Path $TargetDir ".claude"

Write-Host "Claude Code Template Installer" -ForegroundColor Green
Write-Host "================================"
Write-Host ""

# Check if template exists
if (-not (Test-Path $TemplateDir)) {
    Write-Host "Error: Template not found at $TemplateDir" -ForegroundColor Red
    exit 1
}

# Check if target already has .claude
if (Test-Path $TargetClaude) {
    Write-Host "Warning: .claude folder already exists in $TargetDir" -ForegroundColor Yellow
    $response = Read-Host "Overwrite? (y/N)"
    if ($response -ne "y" -and $response -ne "Y") {
        Write-Host "Aborted."
        exit 0
    }
    Remove-Item -Recurse -Force $TargetClaude
}

# Copy template
Write-Host "Copying template to $TargetClaude..."
Copy-Item -Recurse $TemplateDir $TargetClaude

# Copy project state files if they don't exist
$StatusMd = Join-Path $TargetDir "STATUS.md"
if (-not (Test-Path $StatusMd)) {
    Write-Host "Creating STATUS.md..."
    Copy-Item (Join-Path $ScriptDir "template\STATUS.md") $StatusMd
}

$ChangelogMd = Join-Path $TargetDir "CHANGELOG.md"
if (-not (Test-Path $ChangelogMd)) {
    Write-Host "Creating CHANGELOG.md..."
    Copy-Item (Join-Path $ScriptDir "template\CHANGELOG.md") $ChangelogMd
}

$KnownIssuesMd = Join-Path $TargetDir "KNOWN_ISSUES.md"
if (-not (Test-Path $KnownIssuesMd)) {
    Write-Host "Creating KNOWN_ISSUES.md..."
    Copy-Item (Join-Path $ScriptDir "template\KNOWN_ISSUES.md") $KnownIssuesMd
}

# Update the prompts library path
$ClaudeMd = Join-Path $TargetClaude "CLAUDE.md"
if (Test-Path $ClaudeMd) {
    $content = Get-Content $ClaudeMd -Raw
    $content = $content -replace [regex]::Escape("C:\scripts\prompts\"), "$ScriptDir\"
    Set-Content $ClaudeMd $content
}

Write-Host ""
Write-Host "✓ Template installed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps (run in your terminal):" -ForegroundColor White
Write-Host ""
Write-Host "  cd $TargetDir" -ForegroundColor Yellow
Write-Host "  claude --init" -ForegroundColor Yellow
Write-Host ""
Write-Host "Then, inside Claude Code, type:" -ForegroundColor White
Write-Host ""
Write-Host "  initialize this project" -ForegroundColor Green
Write-Host ""
Write-Host "This will automatically install skills and generate project context."
Write-Host ""
