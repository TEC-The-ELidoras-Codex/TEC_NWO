param(
    [string]$Python = "py",
    [string]$Version = "3.11",
    [string]$VenvPath = ".venv"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Invoke-Cmd([string]$cmd) {
    Write-Host "→ $cmd"
    iex $cmd
}

if (Test-Path $VenvPath) {
    Write-Host "Removing existing venv at $VenvPath"
    Remove-Item -Recurse -Force $VenvPath
}

# Prefer Windows launcher (py -3.11) then python fallback
$py311 = "$Python -$Version"
try {
    Invoke-Cmd "$py311 -V"
} catch {
    Write-Host "Python $Version not found via launcher; trying 'python'"
    $Python = "python"
}

Invoke-Cmd "$Python -m venv $VenvPath"
& "$VenvPath/Scripts/Activate.ps1"

Invoke-Cmd "python -m pip install --upgrade pip setuptools wheel"

# Core deps
if (Test-Path "tec_datacore/requirements.txt") {
    Invoke-Cmd "pip install -r tec_datacore/requirements.txt"
}
if (Test-Path "tec_mcp_server/requirements.txt") {
    Invoke-Cmd "pip install -r tec_mcp_server/requirements.txt"
}

# Extras for FastAPI server path
Invoke-Cmd "pip install 'fastapi>=0.112,<0.116' 'uvicorn>=0.30,<0.33' 'pydantic>=2.7,<2.10' 'chromadb>=0.5.4,<0.6' 'numpy<2.2' rapidfuzz"

Write-Host "Python environment ready: $(Resolve-Path $VenvPath)"
