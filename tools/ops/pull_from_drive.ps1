#Requires -Version 5.1
<#
.SYNOPSIS
    Curated pull from Google Drive into the repo with dry-run and report.
.DESCRIPTION
    Copies useful research files from a Drive folder into the repository under
    tec_datacore/data/raw/research, excluding temp/Drive-chunk/caches.
    Defaults to dry-run and generates a JSON report; pass -Execute to copy.
.PARAMETER Source
    Drive folder to pull from. Default: G:\My Drive\TEC_NWO\TEC-HORRORMASTERCLASS\TEC-Research
.PARAMETER Dest
    Destination path (relative or absolute). Default: tec_datacore/data/raw/research
.PARAMETER Execute
    When set, performs the actual copy. Otherwise runs in preview mode.
.PARAMETER ReportOnly
    When set, only generates a report (no copy), regardless of -Execute.
.EXAMPLE
    pwsh tools/ops/pull_from_drive.ps1 -ReportOnly
.EXAMPLE
    pwsh tools/ops/pull_from_drive.ps1 -Execute
.NOTES
    Safe by default. Excludes: .tmp.driveupload, .tmp.drivedownload, caches, venvs, DBs.
#>
Param(
    [string]$Source = "G:\\My Drive\\TEC_NWO\\TEC-HORRORMASTERCLASS\\TEC-Research",
    [string]$Dest = "tec_datacore\\data\\raw\\research",
    [switch]$Execute,
    [switch]$ReportOnly
)

function Resolve-RepoRoot {
    $scriptPath = $MyInvocation.MyCommand.Path
    if ([string]::IsNullOrWhiteSpace($scriptPath)) {
        return (Get-Location).Path
    }
    $here = Split-Path -Parent $scriptPath
    # tools/ops -> tools -> repo root
    return (Split-Path -Parent (Split-Path -Parent $here))
}

function New-PathIfMissing([string]$path) {
    if (!(Test-Path -LiteralPath $path)) { [void](New-Item -ItemType Directory -Path $path) }
}

function Get-IncludePatterns {
    @("*.md","*.markdown","*.txt","*.pdf","*.docx","*.doc","*.rtf","*.json","*.csv","*.vtt","*.html","*.htm")
}
function Get-ExcludeDirs {
    @(".git",".venv","__pycache__","node_modules","datastore","artifacts",".tmp.driveupload",".tmp.drivedownload",".ipynb_checkpoints","*_files")
}
function Get-ExcludeFiles {
    @("Thumbs.db","desktop.ini","*.tmp","*.part","*.log","*.db","*.sqlite","*.pyc","*.map","*.js","*.mjs","*.cjs","*.css","*.woff","*.woff2","*.ttf","*.otf","*.png","*.jpg","*.jpeg","*.gif","*.svg","*.webp","*.ico","*.mp4","*.webm")
}

function Write-DriveReport([string]$src, [string]$reportPath) {
    if (!(Test-Path -LiteralPath $src)) {
        Write-Host "Source not found: $src" -ForegroundColor Red
        return $null
    }
    $includes = Get-IncludePatterns
    $excludeDirs = Get-ExcludeDirs | ForEach-Object { $_.ToLowerInvariant() }
    $excludeFiles = Get-ExcludeFiles

    $files = Get-ChildItem -LiteralPath $src -Recurse -File -ErrorAction SilentlyContinue |
        Where-Object { $rel = $_.FullName.Substring($src.Length).TrimStart('\\');
            -not ($excludeDirs | Where-Object { $rel.ToLowerInvariant().Contains("$_") }) } |
        Where-Object { $name = $_.Name; $match = $false; foreach ($pat in $includes) { if ($name -like $pat) { $match = $true; break } }; $match } |
        Where-Object { $n = $_.Name; -not ($excludeFiles | Where-Object { $n -like $_ }) }

    $total = ($files | Measure-Object Length -Sum).Sum
    $top = $files | Sort-Object Length -Descending | Select-Object -First 25 |
        Select-Object @{n='path';e={$_.FullName}}, @{n='size_bytes';e={$_.Length}}

    $report = [ordered]@{
        generated_at = (Get-Date).ToString("o")
        source = $src
        file_count = ($files | Measure-Object).Count
        total_bytes = $total
        total_mb = [Math]::Round(($total/1MB),2)
        top_largest = $top
    }
    $dir = Split-Path -Parent $reportPath
    New-PathIfMissing $dir
    $report | ConvertTo-Json -Depth 5 | Out-File -FilePath $reportPath -Encoding UTF8
    Write-Host "Report written: $reportPath" -ForegroundColor Green
    return $files
}

function Invoke-CuratedCopy([string]$src, [string]$dst, [switch]$doCopy) {
    $includes = Get-IncludePatterns
    $excludeDirs = Get-ExcludeDirs
    $excludeFiles = Get-ExcludeFiles

    # Build robocopy args
    $rcArgs = @()
    $rcArgs += $src
    $rcArgs += $dst
    # Add file masks to restrict to document types (each is its own argument)
    foreach ($pat in $includes) { $rcArgs += $pat }
    $rcArgs += '/E','/R:1','/W:1','/NFL','/NDL','/NJH','/NJS','/NP'

    foreach ($pat in $excludeFiles) { $rcArgs += '/XF'; $rcArgs += $pat }
    foreach ($dir in $excludeDirs) { $rcArgs += '/XD'; $rcArgs += $dir }

    if (-not $doCopy) { $rcArgs += '/L' } # list only (dry-run)

    Write-Host ("robocopy " + ($rcArgs | ForEach-Object { if ($_ -match '\\s') { '"' + $_ + '"' } else { $_ } }) -join ' ') -ForegroundColor DarkGray
    & robocopy @rcArgs | Out-Host
}

# Entry
$repo = Resolve-RepoRoot
$absDest = if ([System.IO.Path]::IsPathRooted($Dest)) { $Dest } else { Join-Path $repo $Dest }

Write-Host "---"; Write-Host "TEC Drive Pull (Dry-Run by default)" -ForegroundColor Yellow; Write-Host "---"
Write-Host "Source: $Source"
Write-Host "Dest:   $absDest"

# Generate report under artifacts/reports
$reportsDir = Join-Path $repo 'artifacts/reports'
New-PathIfMissing $reportsDir
$reportPath = Join-Path $reportsDir 'drive_research_report.json'
$files = Write-DriveReport -src $Source -reportPath $reportPath

if ($ReportOnly) {
    $cnt = if ($files) { ($files | Measure-Object).Count } else { 0 }
    Write-Host "Report-only mode. Files matched: $cnt. No copy attempted." -ForegroundColor Cyan
    exit 0
}

if ($null -eq $files) { exit 1 }

New-PathIfMissing $absDest
Invoke-CuratedCopy -src $Source -dst $absDest -doCopy:$Execute

if ($Execute) {
    Write-Host "Copy completed. You can now run the Datacore ingest to index new research files." -ForegroundColor Green
}
