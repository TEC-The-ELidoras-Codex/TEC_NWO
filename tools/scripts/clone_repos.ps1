# Requires: Git CLI available on PATH. Optionally GitHub CLI (gh) if you prefer.
param(
    [string]$Root = "external",
    [switch]$Update
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Ensure-Dir([string]$path) {
    if (-not (Test-Path -LiteralPath $path)) {
        New-Item -ItemType Directory -Path $path | Out-Null
    }
}

function Clone-Or-Update([string]$repo, [string]$dest) {
    $name = ($repo -split '/')[-1]
    $target = Join-Path $dest $name
    if (Test-Path -LiteralPath $target) {
        if ($Update) {
            Write-Host "Updating $repo in $target"
            git -C $target fetch --all --prune
            git -C $target pull --ff-only
        } else {
            Write-Host "Exists: $target (use -Update to pull)"
        }
        return
    }
    Write-Host "Cloning $repo into $target"
    git clone --depth 1 "https://github.com/$repo.git" $target
}

# Layout
$msftDocs = Join-Path $Root 'msft-docs'
$msftRepos = Join-Path $Root 'msft-repos'
$azureRepos = Join-Path $Root 'azure'
$githubRepos = Join-Path $Root 'github-examples'
Ensure-Dir $Root
Ensure-Dir $msftDocs
Ensure-Dir $msftRepos
Ensure-Dir $azureRepos
Ensure-Dir $githubRepos

# Repos requested/common
$docsRepos = @(
    'MicrosoftDocs/azure-docs',
    'MicrosoftDocs/azure-ai-docs',
    'MicrosoftDocs/sql-docs'
)
$exampleRepos = @(
    'microsoft/Conversation-Knowledge-Mining-Solution-Accelerator'
)
$mcpRepos = @(
    'github/github-mcp-server'
)
$azureAiRepos = @(
    'azure/ai-app-templates'
)

foreach ($r in $docsRepos) { Clone-Or-Update $r $msftDocs }
foreach ($r in $exampleRepos) { Clone-Or-Update $r $msftRepos }
foreach ($r in $mcpRepos) { Clone-Or-Update $r $githubRepos }
foreach ($r in $azureAiRepos) { Clone-Or-Update $r $azureRepos }

Write-Host "Done. Repos under: $(Resolve-Path $Root)"
