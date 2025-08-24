param(
    [string]$Path = "datastore/chroma"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if (Test-Path -LiteralPath $Path) {
    Write-Host "Removing vector store at $Path"
    Remove-Item -Recurse -Force $Path
}
New-Item -ItemType Directory -Path $Path | Out-Null
Write-Host "Vector store reset at $(Resolve-Path $Path)"
