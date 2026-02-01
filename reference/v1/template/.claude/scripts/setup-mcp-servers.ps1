<#
.SYNOPSIS
    MCP Server Setup Script for Claude Code v4.0 (Windows PowerShell)

.DESCRIPTION
    Installs and configures MCP (Model Context Protocol) servers:
    - context7: Documentation lookup via Upstash
    - memory: Persistent memory across sessions
    - github: GitHub integration for issues, PRs, etc.
    - filesystem: Secure file operations with configurable access
    - puppeteer: Browser automation capabilities

    NOTE: Windows requires "cmd /c npx" wrapper for MCP servers to work properly.

.EXAMPLE
    .\setup-mcp-servers.ps1

.EXAMPLE
    .\setup-mcp-servers.ps1 -SkipGitHub

.EXAMPLE
    .\setup-mcp-servers.ps1 -GitHubToken "ghp_xxxx"

.EXAMPLE
    .\setup-mcp-servers.ps1 -FilesystemDirs "C:\Users\me\Documents,C:\Projects"

.NOTES
    Requires: Node.js 18+, npm
    Author: Claude Code v4.0
#>

param(
    [string]$GitHubToken = "",
    [string]$FilesystemDirs = "",
    [switch]$SkipGitHub,
    [switch]$SkipFilesystem,
    [switch]$SkipPuppeteer,
    [switch]$SkipVerify,
    [switch]$Verbose
)

# Colors for output
function Write-Step { param($msg) Write-Host "`n==> $msg" -ForegroundColor Cyan }
function Write-Success { param($msg) Write-Host "  [OK] $msg" -ForegroundColor Green }
function Write-Warning { param($msg) Write-Host "  [!] $msg" -ForegroundColor Yellow }
function Write-Error { param($msg) Write-Host "  [X] $msg" -ForegroundColor Red }
function Write-Info { param($msg) Write-Host "  $msg" -ForegroundColor Gray }

# Banner
Write-Host @"

╔══════════════════════════════════════════════════════════════════╗
║           MCP Server Setup for Claude Code v4.0                  ║
║                     Windows PowerShell                            ║
╚══════════════════════════════════════════════════════════════════╝

"@ -ForegroundColor Blue

# ============================================================================
# STEP 1: Check Prerequisites
# ============================================================================
Write-Step "Checking prerequisites..."

# Check Node.js
$nodeVersion = $null
try {
    $nodeVersion = (node --version 2>$null)
    if ($nodeVersion) {
        $versionNum = [int]($nodeVersion -replace 'v(\d+)\..*', '$1')
        if ($versionNum -ge 18) {
            Write-Success "Node.js $nodeVersion (>= 18 required)"
        } else {
            Write-Error "Node.js $nodeVersion is too old. Version 18+ required."
            Write-Info "Download from: https://nodejs.org/"
            exit 1
        }
    }
} catch {
    Write-Error "Node.js is not installed"
    Write-Info "Download from: https://nodejs.org/"
    exit 1
}

# Check npm
$npmVersion = $null
try {
    $npmVersion = (npm --version 2>$null)
    if ($npmVersion) {
        Write-Success "npm $npmVersion"
    }
} catch {
    Write-Error "npm is not installed"
    exit 1
}

# Check Claude Code
$claudeInstalled = $false
try {
    $claudeVersion = (claude --version 2>$null)
    if ($claudeVersion) {
        Write-Success "Claude Code installed"
        $claudeInstalled = $true
    }
} catch {
    Write-Warning "Claude Code CLI not found in PATH"
    Write-Info "Install with: npm install -g @anthropic-ai/claude-code"
}

# ============================================================================
# STEP 2: Create Claude Config Directory
# ============================================================================
Write-Step "Setting up Claude configuration directory..."

$claudeConfigDir = Join-Path $env:USERPROFILE ".claude"
if (-not (Test-Path $claudeConfigDir)) {
    New-Item -ItemType Directory -Path $claudeConfigDir -Force | Out-Null
    Write-Success "Created $claudeConfigDir"
} else {
    Write-Success "Config directory exists: $claudeConfigDir"
}

# ============================================================================
# STEP 3: Pre-cache MCP Packages
# ============================================================================
Write-Step "Pre-caching MCP packages..."

Write-Info "This will download the following packages:"
Write-Info "  - @upstash/context7-mcp (documentation lookup)"
Write-Info "  - @modelcontextprotocol/server-memory (persistent memory)"
if (-not $SkipGitHub) {
    Write-Info "  - @modelcontextprotocol/server-github (GitHub integration)"
}
if (-not $SkipFilesystem) {
    Write-Info "  - @modelcontextprotocol/server-filesystem (file operations)"
}
if (-not $SkipPuppeteer) {
    Write-Info "  - @modelcontextprotocol/server-puppeteer (browser automation)"
}
Write-Host ""

# Pre-cache packages using npm cache add (doesn't run servers)
Write-Info "Caching packages (download only)..."

# Context7
try {
    Write-Info "  Caching context7..."
    $null = npm cache add @upstash/context7-mcp@latest 2>&1
    Write-Success "context7 cached"
} catch {
    Write-Warning "context7 will be downloaded on first use"
}

# Memory
try {
    Write-Info "  Caching memory server..."
    $null = npm cache add @modelcontextprotocol/server-memory 2>&1
    Write-Success "memory server cached"
} catch {
    Write-Warning "memory server will be downloaded on first use"
}

# GitHub
if (-not $SkipGitHub) {
    try {
        Write-Info "  Caching GitHub server..."
        $null = npm cache add @modelcontextprotocol/server-github 2>&1
        Write-Success "GitHub server cached"
    } catch {
        Write-Warning "GitHub server will be downloaded on first use"
    }
}

# Filesystem
if (-not $SkipFilesystem) {
    try {
        Write-Info "  Caching filesystem server..."
        $null = npm cache add @modelcontextprotocol/server-filesystem 2>&1
        Write-Success "filesystem server cached"
    } catch {
        Write-Warning "filesystem server will be downloaded on first use"
    }
}

# Puppeteer
if (-not $SkipPuppeteer) {
    try {
        Write-Info "  Caching puppeteer server..."
        $null = npm cache add @modelcontextprotocol/server-puppeteer 2>&1
        Write-Success "puppeteer server cached"
    } catch {
        Write-Warning "puppeteer server will be downloaded on first use"
    }
}

# ============================================================================
# STEP 4: Configure GitHub Token (if needed)
# ============================================================================
if (-not $SkipGitHub) {
    Write-Step "Configuring GitHub integration..."

    # Check for existing token
    $existingToken = $env:GITHUB_TOKEN

    if ($GitHubToken) {
        # Token provided via parameter
        Write-Info "Using provided GitHub token"
        $tokenToUse = $GitHubToken
    } elseif ($existingToken) {
        Write-Success "GITHUB_TOKEN already set in environment"
        $tokenToUse = $existingToken
    } else {
        Write-Warning "No GitHub token found"
        Write-Host ""
        Write-Host "  To use GitHub integration, you need a Personal Access Token:" -ForegroundColor White
        Write-Host "  1. Go to https://github.com/settings/tokens" -ForegroundColor Gray
        Write-Host "  2. Click 'Generate new token (classic)'" -ForegroundColor Gray
        Write-Host "  3. Select scopes: repo, read:org, read:user" -ForegroundColor Gray
        Write-Host "  4. Copy the token" -ForegroundColor Gray
        Write-Host ""

        $response = Read-Host "Enter your GitHub token (or press Enter to skip)"
        if ($response) {
            $tokenToUse = $response
        } else {
            Write-Warning "Skipping GitHub integration (no token provided)"
            $SkipGitHub = $true
        }
    }

    if (-not $SkipGitHub -and $tokenToUse) {
        # Set environment variable for current session
        $env:GITHUB_TOKEN = $tokenToUse

        # Offer to persist the token
        Write-Host ""
        $persist = Read-Host "Save GITHUB_TOKEN to user environment variables? (y/N)"
        if ($persist -eq 'y' -or $persist -eq 'Y') {
            [Environment]::SetEnvironmentVariable("GITHUB_TOKEN", $tokenToUse, "User")
            Write-Success "GITHUB_TOKEN saved to user environment"
            Write-Info "You may need to restart your terminal for changes to take effect"
        }
    }
}

# ============================================================================
# STEP 5: Configure Filesystem Directories
# ============================================================================
if (-not $SkipFilesystem) {
    Write-Step "Configuring filesystem access..."

    if (-not $FilesystemDirs) {
        # Default to user profile
        $FilesystemDirs = $env:USERPROFILE
        Write-Info "Using default filesystem directory: $FilesystemDirs"
        Write-Host ""
        $extraDirs = Read-Host "Add additional directories? (comma-separated, or Enter for default)"
        if ($extraDirs) {
            $FilesystemDirs = "$FilesystemDirs,$extraDirs"
        }
    }

    Write-Success "Filesystem directories: $FilesystemDirs"
}

# ============================================================================
# STEP 6: Create/Update Claude Code Settings
# ============================================================================
Write-Step "Configuring Claude Code MCP settings..."

$settingsPath = Join-Path $claudeConfigDir "settings.json"

# IMPORTANT: Windows requires "cmd /c npx" wrapper for MCP servers to work
# This is because npx.cmd is a batch file and Node's spawn doesn't handle it directly

# Build filesystem args array (with cmd /c wrapper)
$fsArgs = @("/c", "npx", "-y", "@modelcontextprotocol/server-filesystem")
if ($FilesystemDirs) {
    $dirs = $FilesystemDirs -split ","
    foreach ($dir in $dirs) {
        $fsArgs += $dir.Trim()
    }
}

# Build MCP config with cmd /c wrappers for Windows
$mcpConfig = @{
    mcpServers = @{
        context7 = @{
            command = "cmd"
            args = @("/c", "npx", "-y", "@upstash/context7-mcp@latest")
            env = @{}
        }
        memory = @{
            command = "cmd"
            args = @("/c", "npx", "-y", "@modelcontextprotocol/server-memory")
            env = @{}
        }
    }
}

if (-not $SkipGitHub) {
    $mcpConfig.mcpServers.github = @{
        command = "cmd"
        args = @("/c", "npx", "-y", "@modelcontextprotocol/server-github")
        env = @{
            GITHUB_TOKEN = "`${GITHUB_TOKEN}"
        }
    }
}

if (-not $SkipFilesystem) {
    $mcpConfig.mcpServers.filesystem = @{
        command = "cmd"
        args = $fsArgs
        env = @{}
    }
}

if (-not $SkipPuppeteer) {
    $mcpConfig.mcpServers.puppeteer = @{
        command = "cmd"
        args = @("/c", "npx", "-y", "@modelcontextprotocol/server-puppeteer")
        env = @{}
    }
}

# Check if settings file exists
if (Test-Path $settingsPath) {
    Write-Info "Existing settings.json found"
    try {
        $existingSettings = Get-Content $settingsPath -Raw | ConvertFrom-Json -AsHashtable

        # Merge MCP servers
        if (-not $existingSettings.mcpServers) {
            $existingSettings.mcpServers = @{}
        }

        foreach ($server in $mcpConfig.mcpServers.Keys) {
            $existingSettings.mcpServers[$server] = $mcpConfig.mcpServers[$server]
        }

        # Backup and write
        Copy-Item $settingsPath "$settingsPath.backup"
        $existingSettings | ConvertTo-Json -Depth 10 | Set-Content $settingsPath -Encoding UTF8
        Write-Success "Updated existing settings.json with MCP servers"
        Write-Info "Backup saved to $settingsPath.backup"
    } catch {
        Write-Warning "Could not parse existing settings.json"
        Write-Info "Creating backup and writing new settings..."
        Copy-Item $settingsPath "$settingsPath.backup"
        $mcpConfig | ConvertTo-Json -Depth 10 | Set-Content $settingsPath -Encoding UTF8
        Write-Success "Created new settings.json (backup saved)"
    }
} else {
    $mcpConfig | ConvertTo-Json -Depth 10 | Set-Content $settingsPath -Encoding UTF8
    Write-Success "Created new settings.json"
}

Write-Info "Settings file: $settingsPath"

# ============================================================================
# STEP 7: Summary
# ============================================================================
Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                    Setup Complete!                                ║" -ForegroundColor Green
Write-Host "╚══════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Write-Host "MCP Servers Configured (with Windows cmd /c wrapper):" -ForegroundColor White

# context7
Write-Host "  " -NoNewline
Write-Host "●" -ForegroundColor Green -NoNewline
Write-Host " context7    - Documentation lookup"

# memory
Write-Host "  " -NoNewline
Write-Host "●" -ForegroundColor Green -NoNewline
Write-Host " memory      - Persistent memory"

# github
if (-not $SkipGitHub) {
    Write-Host "  " -NoNewline
    Write-Host "●" -ForegroundColor Green -NoNewline
    Write-Host " github      - GitHub integration"
} else {
    Write-Host "  " -NoNewline
    Write-Host "○" -ForegroundColor Gray -NoNewline
    Write-Host " github      - Skipped"
}

# filesystem
if (-not $SkipFilesystem) {
    Write-Host "  " -NoNewline
    Write-Host "●" -ForegroundColor Green -NoNewline
    Write-Host " filesystem  - File operations"
} else {
    Write-Host "  " -NoNewline
    Write-Host "○" -ForegroundColor Gray -NoNewline
    Write-Host " filesystem  - Skipped"
}

# puppeteer
if (-not $SkipPuppeteer) {
    Write-Host "  " -NoNewline
    Write-Host "●" -ForegroundColor Green -NoNewline
    Write-Host " puppeteer   - Browser automation"
} else {
    Write-Host "  " -NoNewline
    Write-Host "○" -ForegroundColor Gray -NoNewline
    Write-Host " puppeteer   - Skipped"
}

Write-Host ""
Write-Host "Configuration file:" -ForegroundColor White
Write-Host "  $settingsPath" -ForegroundColor Gray

Write-Host ""
Write-Host "Windows Note:" -ForegroundColor Yellow
Write-Host "  All MCP servers are configured with 'cmd /c npx' wrapper" -ForegroundColor Gray
Write-Host "  This is required for npx to work properly on Windows" -ForegroundColor Gray

Write-Host ""
Write-Host "Next Steps:" -ForegroundColor White
Write-Host "  1. Restart Claude Code for changes to take effect" -ForegroundColor Gray
Write-Host "  2. MCP servers will auto-start when needed" -ForegroundColor Gray
Write-Host "  3. Use 'context7' for documentation lookups" -ForegroundColor Gray
Write-Host "  4. Memory persists across sessions automatically" -ForegroundColor Gray

if (-not $SkipGitHub -and -not $env:GITHUB_TOKEN) {
    Write-Host ""
    Write-Host "To enable GitHub integration later:" -ForegroundColor Yellow
    Write-Host "  `$env:GITHUB_TOKEN = 'your_token_here'" -ForegroundColor Gray
    Write-Host "  # Or run: .\setup-mcp-servers.ps1 -GitHubToken 'your_token'" -ForegroundColor Gray
}

Write-Host ""
Write-Host "For troubleshooting, see:" -ForegroundColor White
Write-Host "  https://modelcontextprotocol.io/docs" -ForegroundColor Gray
Write-Host ""
