<#
Synopsis: Safe workspace cleanup for TEC_NWO (preview by default)
Usage:
	pwsh ./tools/cleanup/clean_workspace.ps1              # preview only
	pwsh ./tools/cleanup/clean_workspace.ps1 -Execute     # actually delete

This script removes transient caches, logs, build outputs, and large throwaway files
while preserving source, docs, and canonical assets. It is conservative by default
and supports a dry-run preview.
#>

param(
	[switch]$Execute,
	[switch]$VerboseLog
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$Root = Resolve-Path -LiteralPath "$PSScriptRoot/../.." | Select-Object -ExpandProperty Path
Write-Host "TEC_NWO cleanup starting at: $Root" -ForegroundColor Cyan

# Patterns to delete (relative to repo root)
$DeleteDirs = @(
	'node_modules',
	'dist', 'build',
	'.pytest_cache', '.mypy_cache', '.ruff_cache', '.ipynb_checkpoints',
	'__pycache__',
	'.nyc_output', 'coverage',
	'.azure',
	'logs', 'tmp', 'temp', 'pids'
)

$DeleteFiles = @(
	'*.log', '*.pid', '*.pid.lock', '*.seed',
	'*.tsbuildinfo', '*.lcov',
	'*.pyc', '*.pyo', '*.pyd'
)

# Targeted large local-only data/artifacts (safe to remove)
$DeletePaths = @(
	'tec_datacore/datastore',
	'tec_datacore/data',
	'artifacts',
	'.tmp.driveupload',
	'.tmp.drivedownload'
)

# Exclusions (never touch)
$HardExcludes = @(
	'.git', '.github', '.vscode',
	'assets', 'public', 'docs'
)

function Test-ExcludePath {
	param([string]$Path)
	foreach ($ex in $HardExcludes) {
		if ($Path -like "$Root/$ex*" -or $Path -like "$Root\$ex*") { return $true }
	}
	return $false
}

$toDelete = New-Object System.Collections.Generic.List[string]

# Gather directories
foreach ($d in $DeleteDirs) {
	Get-ChildItem -LiteralPath $Root -Recurse -Directory -Force -ErrorAction SilentlyContinue |
		Where-Object { $_.Name -ieq $d -and -not (Test-ExcludePath $_.FullName) } |
		ForEach-Object { $toDelete.Add($_.FullName) }
}

# Gather files by pattern (top-level and nested)
foreach ($pattern in $DeleteFiles) {
	Get-ChildItem -LiteralPath $Root -Recurse -File -Include $pattern -Force -ErrorAction SilentlyContinue |
		Where-Object { -not (Test-ExcludePath $_.DirectoryName) } |
		ForEach-Object { $toDelete.Add($_.FullName) }
}

# Add explicit paths
foreach ($p in $DeletePaths) {
	$full = Join-Path $Root $p
		if (Test-Path -LiteralPath $full) {
			if (-not (Test-ExcludePath $full)) { $toDelete.Add($full) }
	}
}

$toDelete = $toDelete | Sort-Object -Unique

Write-Host "Preview of items to remove (" ($toDelete.Count) "):" -ForegroundColor Yellow
foreach ($item in $toDelete) { Write-Host " - $item" }

if (-not $Execute) {
	Write-Host "Dry-run complete. Re-run with -Execute to apply." -ForegroundColor Yellow
	exit 0
}

Write-Host "Executing cleanup..." -ForegroundColor Red
foreach ($item in $toDelete) {
	try {
		if (Test-Path -LiteralPath $item -PathType Container) {
			Remove-Item -LiteralPath $item -Recurse -Force -ErrorAction Stop
		} elseif (Test-Path -LiteralPath $item -PathType Leaf) {
			Remove-Item -LiteralPath $item -Force -ErrorAction Stop
		}
		if ($VerboseLog) { Write-Host "Removed: $item" -ForegroundColor DarkGray }
	} catch {
		Write-Host "Skip (error): $item -> $($_.Exception.Message)" -ForegroundColor DarkYellow
	}
}

Write-Host "Cleanup complete." -ForegroundColor Green
