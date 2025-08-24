param(
    [string]$Path = "datastore/chroma"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$full = Resolve-Path -LiteralPath $Path -ErrorAction SilentlyContinue
if (-not $full) {
    Write-Host "Vector store not found at $Path (nothing to do)."
    exit 0
}

Write-Host "Removing vector store at $full"
Remove-Item -Recurse -Force -LiteralPath $full
Write-Host "Recreated empty directory"
New-Item -ItemType Directory -Path $Path | Out-Null
