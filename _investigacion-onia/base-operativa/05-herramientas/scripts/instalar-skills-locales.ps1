$ErrorActionPreference = 'Stop'
$sourceRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\compartibles\skills'))
$workspaceRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..\..'))
$destinationRoot = Join-Path $workspaceRoot '.agents\skills'
New-Item -ItemType Directory -Path $destinationRoot -Force | Out-Null
foreach ($skill in Get-ChildItem -LiteralPath $sourceRoot -Directory) {
    if (-not (Test-Path -LiteralPath (Join-Path $skill.FullName 'SKILL.md'))) { continue }
    $destination = Join-Path $destinationRoot $skill.Name
    if (Test-Path -LiteralPath $destination) {
        $existing = Get-Item -LiteralPath $destination -Force
        if ($existing.LinkType -ne 'Junction' -or [IO.Path]::GetFullPath([string]$existing.Target) -ne $skill.FullName) {
            throw "Destino ocupado por otra instalación: $destination"
        }
    } else {
        New-Item -ItemType Junction -Path $destination -Target $skill.FullName | Out-Null
    }
    if ((Get-FileHash -LiteralPath (Join-Path $destination 'SKILL.md')).Hash -ne (Get-FileHash -LiteralPath (Join-Path $skill.FullName 'SKILL.md')).Hash) {
        throw "El enlace no resuelve la fuente: $destination"
    }
    [PSCustomObject]@{ Skill = $skill.Name; Source = $skill.FullName; DiscoveryPath = $destination }
}
