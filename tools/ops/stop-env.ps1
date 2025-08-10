<#
.SYNOPSIS
  Stop / scale-down TEC cloud resources to minimize cost.
.DESCRIPTION
  Dynamically discovers resource names produced by infra/main.bicep (which include a unique token)
  and issues:
    - Stop PostgreSQL flexible server (billing stops except storage)
    - Scale Container Apps (main + airth) to 0 min / 0 max replicas
    - (Optional) Reduce Log Analytics daily cap (commented)
  Safe to run multiple times (idempotent operations).
.PARAMETER ResourceGroup
  Azure Resource Group containing the deployment.
.EXAMPLE
  ./stop-env.ps1 -ResourceGroup tec-dev-rg
#>
param(
  [Parameter(Mandatory=$true)][string]$ResourceGroup
)

Write-Host "--- TEC Cost Optimization: STOP PHASE ---" -ForegroundColor Yellow
Write-Host "Resource Group: $ResourceGroup"

function Get-PostgresServerName {
  az postgres flexible-server list -g $ResourceGroup --query "[0].name" -o tsv
}

function Get-ContainerApps {
  az containerapp list -g $ResourceGroup --query "[].name" -o tsv
}

$pgName = Get-PostgresServerName
if (-not $pgName) {
  Write-Warning "No PostgreSQL flexible server found. Skipping."
} else {
  Write-Host "Stopping PostgreSQL server: $pgName" -ForegroundColor Cyan
  az postgres flexible-server stop -g $ResourceGroup -n $pgName | Out-Null
  Write-Host "PostgreSQL stop issued." -ForegroundColor Green
}

$apps = Get-ContainerApps
if (-not $apps) {
  Write-Warning "No Container Apps found."
} else {
  foreach ($app in $apps) {
    Write-Host "Scaling Container App '$app' to 0" -ForegroundColor Cyan
    az containerapp update -g $ResourceGroup -n $app --min-replicas 0 --max-replicas 0 | Out-Null
  }
  Write-Host "All Container Apps scaled to 0 replicas." -ForegroundColor Green
}

# OPTIONAL: Reduce Log Analytics daily cap (uncomment & adjust if needed)
# $lawName = az monitor log-analytics workspace list -g $ResourceGroup --query "[0].name" -o tsv
# if ($lawName) { az monitor log-analytics workspace update -g $ResourceGroup -n $lawName --quota 0.2 --retention-time 7 }

Write-Host "--- TEC environment is now minimized for cost. ---" -ForegroundColor Yellow
