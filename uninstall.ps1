# Desinstalador de las SEO Skills de aprendoseo para Windows / PowerShell.
# Borra SOLO lo que el instalador registro en .seo-skills-manifest (skills y agentes).
# Si la instalacion es antigua y no tiene manifiesto, descarga la lista de nombres del
# repo y borra unicamente esas carpetas. No toca nada mas de tu carpeta de skills.
#
# Uso:
#   irm https://raw.githubusercontent.com/Arianna-Lupi/SEO-Skills/main/uninstall.ps1 | iex
#   .\uninstall.ps1 -Project        (Claude Code, solo este proyecto)
#   .\uninstall.ps1 -Dir C:\ruta    (carpeta usada al instalar con -Dir)
#   .\uninstall.ps1 -DryRun         (muestra que borraria, sin borrar)
#
# Si instalaste como plugin, usa en su lugar:
#   /plugin uninstall seo-skills@aprendoseo
#   /plugin marketplace remove aprendoseo
param(
  [string]$Client = "claude",
  [switch]$Project,
  [string]$Dir = "",
  [string]$Ref = "main",
  [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"
$Repo     = "Arianna-Lupi/SEO-Skills"
$Marker   = ".seo-skills-version"
$Manifest = ".seo-skills-manifest"

$agentsDest = $null
if ($Dir) {
  $skillsDest = Join-Path $Dir "skills"; $agentsDest = Join-Path $Dir "agents"
} else {
  switch ($Client) {
    "claude" {
      $base = if ($Project) { Join-Path (Get-Location) ".claude" } else { Join-Path $HOME ".claude" }
      $skillsDest = Join-Path $base "skills"; $agentsDest = Join-Path $base "agents"
    }
    "cursor"  { $skillsDest = Join-Path (Get-Location) ".cursor\skills" }
    "agents"  { $skillsDest = Join-Path (Get-Location) ".agents\skills" }
    "codex"   { $skillsDest = Join-Path (Get-Location) ".codex\skills" }
    "copilot" { $skillsDest = Join-Path (Get-Location) ".github\skills" }
    default   { Write-Error "Cliente desconocido: $Client"; return }
  }
}

if (-not (Test-Path $skillsDest)) { Write-Host "No hay carpeta de skills en $skillsDest. Nada que quitar."; return }

$skillNames = @(); $agentPaths = @()
$manifestPath = Join-Path $skillsDest $Manifest
if (Test-Path $manifestPath) {
  foreach ($line in Get-Content $manifestPath) {
    if ($line -match '^skill (\S+)') { $skillNames += $Matches[1] }
    elseif ($line -match '^agent \S+ (.+)$') { $agentPaths += $Matches[1] }
  }
} else {
  Write-Host "! No encontre $Manifest (instalacion antigua). Descargo la lista de nombres del repo." -ForegroundColor Yellow
  $tmp = Join-Path ([System.IO.Path]::GetTempPath()) ("seo-skills-" + [guid]::NewGuid())
  New-Item -ItemType Directory -Force -Path $tmp | Out-Null
  try {
    $zip = Join-Path $tmp "p.zip"
    Invoke-WebRequest -Uri "https://codeload.github.com/$Repo/zip/$Ref" -OutFile $zip -UseBasicParsing
    Expand-Archive -Path $zip -DestinationPath $tmp -Force
    $root = (Get-ChildItem $tmp -Directory | Select-Object -First 1).FullName
    Get-ChildItem (Join-Path $root "skills") -Directory | ForEach-Object { $skillNames += $_.Name }
    if ($agentsDest) {
      Get-ChildItem (Join-Path $root "agents") -Filter *.md -ErrorAction SilentlyContinue |
        ForEach-Object { $agentPaths += (Join-Path $agentsDest $_.Name) }
    }
  } finally { Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue }
}

$rs = 0; $ra = 0
foreach ($name in $skillNames) {
  if ([string]::IsNullOrWhiteSpace($name) -or $name -match '[\\/]' -or $name -eq '.' -or $name -eq '..') { continue }
  $p = Join-Path $skillsDest $name
  if (Test-Path $p) {
    if ($DryRun) { Write-Host "  (simulacro) quitaria $p" } else { Remove-Item $p -Recurse -Force; Write-Host "  Quitada: $p" }
    $rs++
  }
}
foreach ($f in $agentPaths) {
  if (Test-Path $f) {
    if ($DryRun) { Write-Host "  (simulacro) quitaria $f" } else { Remove-Item $f -Force; Write-Host "  Quitado: $f" }
    $ra++
  }
}
if (-not $DryRun) {
  Remove-Item (Join-Path $skillsDest $Marker), $manifestPath -Force -ErrorAction SilentlyContinue
  foreach ($d in @($skillsDest, $agentsDest)) {
    if ($d -and (Test-Path $d) -and -not (Get-ChildItem $d -Force | Select-Object -First 1)) { Remove-Item $d -Force -ErrorAction SilentlyContinue }
  }
}

if ($rs -eq 0 -and $ra -eq 0) {
  Write-Host "Nada que quitar: no parece que las SEO Skills esten instaladas en $skillsDest."
  Write-Host "Si las instalaste como plugin, usa /plugin uninstall seo-skills@aprendoseo."
} else {
  Write-Host "OK - Desinstaladas $rs skills y $ra agentes de aprendoseo." -ForegroundColor Green
}
