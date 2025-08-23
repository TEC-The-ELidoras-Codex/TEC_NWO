#Requires -Version 5.1
<#
.SYNOPSIS
    Clean TEC-Research folder by removing web asset folders and non-text junk.
.DESCRIPTION
    Targets a source folder (default: ./TEC-HORRORMASTERCLASS/TEC-Research).
    - Deletes directories matching *_files (saved-page assets)
    - Deletes non-text assets (.js, .css, fonts, images, .download, etc.)
    Dry-run by default; pass -Execute to apply.
.PARAMETER Source
    The research folder to clean.
.PARAMETER Execute
    Apply deletions. Without this flag, the script only previews actions.
.EXAMPLE
    pwsh tools/ops/clean_research.ps1
.EXAMPLE
    pwsh tools/ops/clean_research.ps1 -Execute
#>
param(
    [string]$Source = "./TEC-HORRORMASTERCLASS/TEC-Research",
    [switch]$Execute
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$srcPath = Resolve-Path -LiteralPath $Source -ErrorAction SilentlyContinue
if (-not $srcPath) {
    Write-Host "Source not found: $Source" -ForegroundColor Red
    exit 1
}
$src = $srcPath.Path

Write-Host "---"; Write-Host "TEC Research Cleaner (Dry-Run by default)" -ForegroundColor Yellow; Write-Host "---"
Write-Host "Source: $src"

# Directories to delete entirely
$dirPatterns = @("*_files")

# File patterns to delete (non-text assets)
$filePatterns = @(
    "*.download","*.map","*.js","*.mjs","*.cjs","*.css",
    "*.woff","*.woff2","*.ttf","*.otf",
    "*.png","*.jpg","*.jpeg","*.gif","*.svg","*.webp","*.ico","*.mp4","*.webm"
)

$dirs = New-Object System.Collections.Generic.List[System.IO.DirectoryInfo]
foreach ($pat in $dirPatterns) {
    Get-ChildItem -LiteralPath $src -Recurse -Directory -Filter $pat -ErrorAction SilentlyContinue | ForEach-Object { $dirs.Add($_) }
}

$files = New-Object System.Collections.Generic.List[System.IO.FileInfo]
foreach ($pat in $filePatterns) {
    Get-ChildItem -LiteralPath $src -Recurse -File -Filter $pat -ErrorAction SilentlyContinue | ForEach-Object { $files.Add($_) }
}

$dirCount = $dirs.Count
$fileCount = $files.Count

function Get-BytesOrZero($value) {
    if ($null -eq $value) { return 0 } else { return [double]$value }
}

$dirBytesList = @()
foreach ($d in $dirs) {
    $fileLens = Get-ChildItem -LiteralPath $d.FullName -Recurse -File -ErrorAction SilentlyContinue | ForEach-Object { $_.Length }
    $sumObj = $fileLens | Measure-Object -Sum
    $dirBytesList += (Get-BytesOrZero $sumObj.Sum)
}
$dirSizeObj = $dirBytesList | Measure-Object -Sum
$dirSize = Get-BytesOrZero $dirSizeObj.Sum
$fileLensAll = $files | ForEach-Object { $_.Length }
$fileSizeObj = $fileLensAll | Measure-Object -Sum
$fileSize = Get-BytesOrZero $fileSizeObj.Sum

Write-Host ("Will remove {0} folders (~{1:N2} MB) and {2} files (~{3:N2} MB)" -f $dirCount, (($dirSize)/1MB), $fileCount, (($fileSize)/1MB)) -ForegroundColor Cyan

if (-not $Execute) {
    Write-Host "Preview only. Re-run with -Execute to apply." -ForegroundColor Yellow
    if ($dirCount -gt 0) { Write-Host "Folders:"; $dirs | Select-Object -ExpandProperty FullName | ForEach-Object { Write-Host " - $_" } }
    if ($fileCount -gt 0) { Write-Host "Files:"; $files | Select-Object -ExpandProperty FullName | Select-Object -First 25 | ForEach-Object { Write-Host " - $_" }; if ($fileCount -gt 25) { Write-Host " ... ($fileCount total)" } }
    exit 0
}

Write-Host "Executing cleanup..." -ForegroundColor Red
foreach ($d in $dirs) {
    try { Remove-Item -LiteralPath $d.FullName -Recurse -Force -ErrorAction Stop } catch { Write-Host "Skip dir: $($d.FullName) -> $($_.Exception.Message)" -ForegroundColor DarkYellow }
}
foreach ($f in $files) {
    try { Remove-Item -LiteralPath $f.FullName -Force -ErrorAction Stop } catch { Write-Host "Skip file: $($f.FullName) -> $($_.Exception.Message)" -ForegroundColor DarkYellow }
}
Write-Host "Cleanup complete." -ForegroundColor Green
