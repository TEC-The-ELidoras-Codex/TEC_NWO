<#
.SYNOPSIS
  Start / scale-up TEC cloud resources for active development.
.DESCRIPTION
  Reverses stop-env.ps1: starts PostgreSQL server and scales Container Apps to baseline.
.PARAMETER ResourceGroup
  Azure Resource Group containing the deployment.
.PARAMETER MainMin
  Min replicas for primary app (default 1)
.PARAMETER AirthMin
  Min replicas for Airth agent (default 1)
.EXAMPLE
  ./start-env.ps1 -ResourceGroup tec-dev-rg -MainMin 1 -AirthMin 1
#>
param(
  [Parameter(Mandatory=$true)][string]$ResourceGroup,
  [int]$MainMin = 1,
  [int]$AirthMin = 1
)

Write-Host "--- TEC Environment START ---" -ForegroundColor Yellow
Write-Host "Resource Group: $ResourceGroup"

function Get-PostgresServerName { az postgres flexible-server list -g $ResourceGroup --query "[0].name" -o tsv }
function Get-ContainerApps { az containerapp list -g $ResourceGroup --query "[].name" -o tsv }

$pgName = Get-PostgresServerName
if ($pgName) {
  Write-Host "Starting PostgreSQL server: $pgName" -ForegroundColor Cyan
  az postgres flexible-server start -g $ResourceGroup -n $pgName | Out-Null
  Write-Host "PostgreSQL start issued." -ForegroundColor Green
} else { Write-Warning "No PostgreSQL server located." }

# Heuristic: Identify main vs airth by substring
$apps = Get-ContainerApps
foreach ($app in $apps) {
  if ($app -match 'airth') {
    Write-Host "Scaling Airth app '$app' to $AirthMin" -ForegroundColor Cyan
    az containerapp update -g $ResourceGroup -n $app --min-replicas $AirthMin --max-replicas ([Math]::Max($AirthMin,2)) | Out-Null
  } else {
    Write-Host "Scaling primary app '$app' to $MainMin" -ForegroundColor Cyan
    az containerapp update -g $ResourceGroup -n $app --min-replicas $MainMin --max-replicas ([Math]::Max($MainMin,3)) | Out-Null
  }
}

Write-Host "--- TEC environment baseline capacity restored. ---" -ForegroundColor Yellow
