# Instalador de las SEO Skills de aprendoseo para Claude Code (Windows / PowerShell).
#
# Uso rapido (un comando, en PowerShell):
#   irm https://raw.githubusercontent.com/Arianna-Lupi/SEO-Skills/main/install.ps1 | iex
#
# O desde el repo clonado:  .\install.ps1   (o  .\install.ps1 -Project)
#
# Requisitos: git. Python/uv son OPCIONALES (solo para los scripts; las skills
# funcionan sin ellos, en modo manual).
param([switch]$Project)

$ErrorActionPreference = "Stop"
$RepoUrl = "https://github.com/Arianna-Lupi/SEO-Skills.git"

Write-Host ""
Write-Host "SEO Skills - aprendoseo (De Cero a SEO)" -ForegroundColor Cyan
Write-Host "13 skills + 3 agentes para Claude Code" -ForegroundColor DarkGray
Write-Host ""

# Localizar la fuente (clonar si se corre via irm|iex)
$src = $null
if ($PSScriptRoot -and (Test-Path (Join-Path $PSScriptRoot "skills"))) {
  $src = $PSScriptRoot
} else {
  if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "Necesitas git para descargar el repo. Instala git y reintenta."
    return
  }
  $tmp = Join-Path ([System.IO.Path]::GetTempPath()) ("seo-skills-" + [guid]::NewGuid())
  Write-Host "Descargando SEO-Skills..."
  git clone --depth 1 $RepoUrl $tmp 2>$null | Out-Null
  $src = $tmp
}
if (-not (Test-Path (Join-Path $src "skills"))) { Write-Error "No encontre skills/ en $src"; return }

# Destino
$base = if ($Project) { Join-Path (Get-Location) ".claude" } else { Join-Path $HOME ".claude" }
$skillsDest = Join-Path $base "skills"
$agentsDest = Join-Path $base "agents"
New-Item -ItemType Directory -Force -Path $skillsDest, $agentsDest | Out-Null

# Copiar skills y agentes (no requiere python/node)
$sk = 0
Get-ChildItem (Join-Path $src "skills") -Directory | ForEach-Object {
  if (Test-Path (Join-Path $_.FullName "SKILL.md")) {
    $dst = Join-Path $skillsDest $_.Name
    if (Test-Path $dst) { Remove-Item $dst -Recurse -Force }
    Copy-Item $_.FullName $dst -Recurse
    $sk++
  }
}
$ag = 0
Get-ChildItem (Join-Path $src "agents") -Filter *.md -ErrorAction SilentlyContinue | ForEach-Object {
  Copy-Item $_.FullName $agentsDest -Force; $ag++
}

Write-Host ""
Write-Host "OK - Instaladas $sk skills en $skillsDest" -ForegroundColor Green
Write-Host "OK - Instalados $ag agentes en $agentsDest" -ForegroundColor Green

# Chequeo opcional de runtime (nunca falla)
Write-Host ""
Write-Host "Scripts (aceleradores opcionales - las skills funcionan sin esto):" -ForegroundColor DarkGray
if (Get-Command uv -ErrorAction SilentlyContinue) {
  Write-Host "OK - uv detectado: los scripts corren con 'uv run' sin instalar nada." -ForegroundColor Green
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
  Write-Host "OK - python detectado: para los scripts con dependencias 'pip install requests beautifulsoup4'." -ForegroundColor Green
} else {
  Write-Host "! No hay Python ni uv. Las skills funcionan igual (modo manual); los scripts no correran." -ForegroundColor Yellow
  Write-Host "! Si queres los scripts: instala uv -> https://astral.sh/uv" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Listo. Reinicia Claude Code y escribi '/' (por ejemplo /brief-de-contenido)." -ForegroundColor Green
