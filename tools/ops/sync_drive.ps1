<#
Synopsis: Curated sync from repo → Google Drive (dry-run by default)
Usage:
  pwsh ./tools/ops/sync_drive.ps1                                    # preview only
  pwsh ./tools/ops/sync_drive.ps1 -Target "G:\\My Drive\\TEC_NWO"   # set target
  pwsh ./tools/ops/sync_drive.ps1 -Target "G:\\My Drive\\TEC_NWO" -Execute

Notes:
  - Uses robocopy with /L for dry-run preview or actual copy when -Execute.
  - Copies only curated sources to avoid churn and duplicates.
  - Excludes caches, build outputs, temp, datastores, and hidden folders.
#>

param(
  [string]$Target = 'G:\\My Drive\\TEC_NWO',
  [switch]$Execute
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$Root = Resolve-Path -LiteralPath "$PSScriptRoot/../.." | Select-Object -ExpandProperty Path
Write-Host "Curated Drive sync from: $Root -> $Target" -ForegroundColor Cyan

if (-not (Test-Path -LiteralPath $Target)) {
  Write-Host "Target does not exist, creating: $Target" -ForegroundColor Yellow
  New-Item -ItemType Directory -Path $Target -Force | Out-Null
}

$Dry = $true
if ($Execute) { $Dry = $false }

# Directories to include (top-level relative to repo root)
$IncludeDirs = @(
  'assets', 'docs', 'lore', 'public', 'catalogs', 'notebooks'
)

# Specific files at root to include
$IncludeFiles = @(
  'README.md', 'README_ARCHITECTURE.md', 'QUICKSTART.md', 'SYSTEM_STATUS.md'
)

# Common excludes (dirs)
$ExcludeDirs = @(
  '.git', '.github', '.vscode', '.tmp.driveupload', '.tmp.drivedownload',
  'node_modules', 'dist', 'build', 'datastore', 'artifacts',
  'tec_datacore', 'tec_mcp_server', 'src', 'services', 'orchestration',
  'infra', 'infrastructure', 'prisma', 'tests', 'tools', 'scripts'
)

# Common excludes (files)
$ExcludeFiles = @('*.log', '*.tsbuildinfo', '*.lcov', '*.pyc', '*.pyo', '*.pyd')

$roboFlags = @('/E', '/FFT', '/Z', '/R:1', '/W:1', '/XD') + $ExcludeDirs + @('/XF') + $ExcludeFiles
if ($Dry) { $roboFlags = @('/L') + $roboFlags }

function Sync-Dir {
  param([string]$RelDir)
  $src = Join-Path $Root $RelDir
  if (Test-Path -LiteralPath $src) {
    $dst = Join-Path $Target $RelDir
    if (-not (Test-Path -LiteralPath $dst)) { New-Item -ItemType Directory -Path $dst -Force | Out-Null }
    Write-Host "Syncing dir: $RelDir" -ForegroundColor Green
    robocopy $src $dst @roboFlags | Out-Host
  }
}

function Sync-File {
  param([string]$RelFile)
  $src = Join-Path $Root $RelFile
  if (Test-Path -LiteralPath $src) {
    Write-Host "Syncing file: $RelFile" -ForegroundColor Green
    $dst = Join-Path $Target $RelFile
    $dstDir = Split-Path -Parent $dst
    if (-not (Test-Path -LiteralPath $dstDir)) { New-Item -ItemType Directory -Path $dstDir -Force | Out-Null }
    if ($Dry) {
      Write-Host " [DRY] robocopy $(Split-Path -Parent $src) $dstDir $(Split-Path -Leaf $src)" -ForegroundColor DarkGray
    } else {
      robocopy (Split-Path -Parent $src) $dstDir (Split-Path -Leaf $src) | Out-Host
    }
  }
}

foreach ($d in $IncludeDirs) { Sync-Dir -RelDir $d }
foreach ($f in $IncludeFiles) { Sync-File -RelFile $f }

if ($Dry) {
  Write-Host "Dry-run complete. Re-run with -Execute to copy changes." -ForegroundColor Yellow
} else {
  Write-Host "Sync complete." -ForegroundColor Cyan
}
