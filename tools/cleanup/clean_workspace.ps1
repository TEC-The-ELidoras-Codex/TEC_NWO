# Cleans local workspace clutter (venvs, caches, tmp, artifacts). Run from repo root.
param(
  [switch]$Aggressive
)

Write-Host "Cleaning workspace..."
$paths = @(
  ".pytest_cache", ".mypy_cache", "__pycache__", ".ipynb_checkpoints",
  "artifacts", "datastore", "tmp", "temp", ".tmp.driveupload"
)
foreach ($p in $paths) {
  if (Test-Path $p) { Write-Host "Removing $p" -ForegroundColor Yellow; Remove-Item $p -Recurse -Force -ErrorAction SilentlyContinue }
}

# Optional aggressive: remove venvs and node_modules (careful)
if ($Aggressive) {
  foreach ($p in @(".venv", "venv", "node_modules")) {
    if (Test-Path $p) { Write-Host "Removing $p (aggressive)" -ForegroundColor Red; Remove-Item $p -Recurse -Force -ErrorAction SilentlyContinue }
  }
}

Write-Host "Done." -ForegroundColor Green
