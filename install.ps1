# Instalador de las SEO Skills de aprendoseo ("De Cero a SEO") para Windows / PowerShell.
# Funciona con Claude Code y otros clientes compatibles con Agent Skills
# (Cursor, VS Code, OpenAI Codex, GitHub Copilot).
#
# Camino rapido (por defecto): sin preguntas, sin instalar dependencias, un solo
# archivo descargado (zip, sin git). Es idempotente: puedes correrlo otra vez para actualizar.
#
# Uso rapido (un comando, en PowerShell):
#   irm https://raw.githubusercontent.com/Arianna-Lupi/SEO-Skills/main/install.ps1 | iex
#
# Con parametros (descarga el script y corre .\install.ps1):
#   .\install.ps1 -Client cursor
#   .\install.ps1 -Project          (Claude Code, solo este proyecto)
#   .\install.ps1 -Dir C:\ruta      (carpeta concreta: crea skills\ y agents\)
#   .\install.ps1 -Full             (ademas instala uv para que los scripts corran solos)
#   .\install.ps1 -Interactive      (pregunta cliente y alcance: el comportamiento antiguo)
#   .\install.ps1 -Check            (solo dice si hay version nueva; no instala)
#   .\install.ps1 -Ref develop      (rama o etiqueta; por defecto main)
#
# Requisitos: PowerShell 5.1 o superior. git solo como respaldo.
# Python y uv son OPCIONALES (solo para los scripts; las skills funcionan sin ellos).
# Desinstalar: uninstall.ps1 (mismas opciones -Client/-Project/-Dir).
param(
  [string]$Client = "claude",   # claude | cursor | agents | codex | copilot
  [switch]$Project,             # Claude Code: solo este proyecto
  [string]$Dir = "",            # carpeta concreta (override)
  [string]$Ref = "main",        # rama o etiqueta
  [switch]$Full,                # ademas instala uv
  [switch]$Interactive,         # pregunta cliente y alcance
  [switch]$Check,               # solo busca actualizaciones, no instala
  [switch]$Update,              # compat: instalar ya actualiza sin preguntar
  [switch]$WithUv,              # solo el extra de uv
  [switch]$NoUv                 # compat: es el comportamiento por defecto
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"   # Invoke-WebRequest es mucho mas rapido sin barra
$Repo     = "Arianna-Lupi/SEO-Skills"
$RepoUrl  = "https://github.com/$Repo.git"
$UvPs1    = "https://astral.sh/uv/install.ps1"
$Marker   = ".seo-skills-version"
$Manifest = ".seo-skills-manifest"
$start    = Get-Date
if ($env:SEO_SKILLS_REF) { $Ref = $env:SEO_SKILLS_REF }

function Test-Newer($a, $b) {
  if ([string]::IsNullOrEmpty($a) -or [string]::IsNullOrEmpty($b)) { return $false }
  if ($a -eq $b) { return $false }
  try { return ([version]$a -gt [version]$b) } catch { return ($a -ne $b) }
}

Write-Host ""
Write-Host "SEO Skills de aprendoseo (De Cero a SEO)" -ForegroundColor Cyan
Write-Host "Enrutador /aprendoclub + skills y agentes para Claude Code y clientes compatibles" -ForegroundColor DarkGray
Write-Host ""

# --- 1) localizar la fuente: carpeta local si el script es un archivo del repo; si no, zip ---
$src = $null
$tmp = $null
if ($PSScriptRoot -and (Test-Path (Join-Path $PSScriptRoot "skills"))) {
  $src = $PSScriptRoot
} elseif (-not $Check) {
  $tmp = Join-Path ([System.IO.Path]::GetTempPath()) ("seo-skills-" + [guid]::NewGuid())
  New-Item -ItemType Directory -Force -Path $tmp | Out-Null
  $zipUrl = if ($env:SEO_SKILLS_ZIP_URL) { $env:SEO_SKILLS_ZIP_URL } else { "https://codeload.github.com/$Repo/zip/$Ref" }
  Write-Host "Descargando $Repo@$Ref..." -ForegroundColor DarkGray
  try {
    $zip = Join-Path $tmp "pkg.zip"
    Invoke-WebRequest -Uri $zipUrl -OutFile $zip -UseBasicParsing
    Expand-Archive -Path $zip -DestinationPath $tmp -Force
    $src = (Get-ChildItem $tmp -Directory | Select-Object -First 1).FullName
  } catch {
    if (Get-Command git -ErrorAction SilentlyContinue) {
      Write-Host "! No pude bajar el zip; uso git como respaldo." -ForegroundColor Yellow
      git clone --depth 1 --branch $Ref $RepoUrl (Join-Path $tmp "SEO-Skills") 2>$null | Out-Null
      $src = Join-Path $tmp "SEO-Skills"
    } else {
      Write-Error "No pude descargar el paquete y no hay git de respaldo."
      return
    }
  }
  if (-not $src -or -not (Test-Path (Join-Path $src "skills"))) { Write-Error "El paquete descargado no trae skills/."; return }
}

$selfVersion = "0.0.0"
if ($src) {
  $vfile = Join-Path $src "VERSION"
  if (Test-Path $vfile) { $selfVersion = (Get-Content $vfile -First 1).Trim() }
}

# --- 2) cliente y alcance: por defecto Claude Code, usuario, sin preguntar ---
$interactive = $Interactive -and [Environment]::UserInteractive -and -not [Console]::IsInputRedirected -and -not $Check
$clientGiven = $PSBoundParameters.ContainsKey('Client')
$useDir = -not [string]::IsNullOrEmpty($Dir)

if (-not $useDir -and -not $clientGiven -and $interactive) {
  Write-Host "Para que cliente las instalo?"
  Write-Host "  1) Claude Code   [recomendado]"
  Write-Host "  2) Cursor"
  Write-Host "  3) VS Code / Agent Skills (estandar)"
  Write-Host "  4) OpenAI Codex"
  Write-Host "  5) GitHub Copilot"
  $ci = Read-Host "Opcion [1]"
  switch ($ci) {
    "2" { $Client = "cursor" }
    "3" { $Client = "agents" }
    "4" { $Client = "codex" }
    "5" { $Client = "copilot" }
    default { $Client = "claude" }
  }
}
if ($Client -eq "claude" -and -not $Project -and -not $useDir -and $interactive -and -not $clientGiven) {
  Write-Host ""
  Write-Host "Donde, dentro de Claude Code?"
  Write-Host "  1) Para tu usuario    (~/.claude)   [recomendado]"
  Write-Host "  2) Solo este proyecto (./.claude)"
  $cs = Read-Host "Opcion [1]"
  if ($cs -eq "2") { $Project = $true }
}

# --- 3) carpetas destino ---
$agentsDest = $null
if ($useDir) {
  $skillsDest = Join-Path $Dir "skills"
  $agentsDest = Join-Path $Dir "agents"
} else {
  switch ($Client) {
    "claude" {
      $base = if ($Project) { Join-Path (Get-Location) ".claude" } else { Join-Path $HOME ".claude" }
      $skillsDest = Join-Path $base "skills"
      $agentsDest = Join-Path $base "agents"
    }
    "cursor"  { $skillsDest = Join-Path (Get-Location) ".cursor\skills" }
    "agents"  { $skillsDest = Join-Path (Get-Location) ".agents\skills" }
    "codex"   { $skillsDest = Join-Path (Get-Location) ".codex\skills" }
    "copilot" { $skillsDest = Join-Path (Get-Location) ".github\skills" }
    default   { Write-Error "Cliente desconocido: $Client (usa claude|cursor|agents|codex|copilot)"; return }
  }
}

$installedVersion = ""
$markerPath = Join-Path $skillsDest $Marker
if (Test-Path $markerPath) { $installedVersion = (Get-Content $markerPath -First 1).Trim() }

# --- modo -Check ---
if ($Check) {
  $remoteVersion = ""
  try { $remoteVersion = (Invoke-RestMethod -Uri "https://raw.githubusercontent.com/$Repo/$Ref/VERSION" -TimeoutSec 8).ToString().Trim() } catch { }
  $target = if ($remoteVersion) { $remoteVersion } else { $selfVersion }
  Write-Host "Cliente: $Client    Carpeta: $skillsDest" -ForegroundColor DarkGray
  if ($installedVersion) { Write-Host "Instalada:  $installedVersion" } else { Write-Host "Instalada:  (ninguna detectada aqui)" }
  Write-Host "Disponible: $target"
  if (-not $installedVersion) {
    Write-Host "! No hay instalacion previa aqui. Corre el instalador sin -Check." -ForegroundColor Yellow
  } elseif (Test-Newer $target $installedVersion) {
    Write-Host "! Hay una version nueva ($installedVersion -> $target). Vuelve a correr el instalador para actualizar." -ForegroundColor Yellow
  } else {
    Write-Host "OK - Estas al dia (version $installedVersion)." -ForegroundColor Green
  }
  return
}

New-Item -ItemType Directory -Force -Path $skillsDest | Out-Null
if ($agentsDest) { New-Item -ItemType Directory -Force -Path $agentsDest | Out-Null }

# --- 4) copiar skills (todos) y agentes (solo Claude) ---
# Huella de una carpeta (nombres y contenido, sin __pycache__): detecta si modificaste una skill a mano.
function Get-DirHash($path) {
  $root = (Resolve-Path $path).Path
  $sb = New-Object System.Text.StringBuilder
  Get-ChildItem $root -Recurse -File | Where-Object { $_.FullName -notmatch '__pycache__' -and $_.Extension -ne '.pyc' -and $_.Name -ne '.DS_Store' } |
    Sort-Object FullName | ForEach-Object {
      $rel = $_.FullName.Substring($root.Length).Replace('\', '/')
      [void]$sb.Append($rel).Append(':').Append((Get-FileHash $_.FullName -Algorithm SHA256).Hash).Append("`n")
    }
  $sha = [System.Security.Cryptography.SHA256]::Create()
  return ([BitConverter]::ToString($sha.ComputeHash([Text.Encoding]::UTF8.GetBytes($sb.ToString()))) -replace '-', '')
}
$oldManifestPath = Join-Path $skillsDest $Manifest
$recorded = @{}
if (Test-Path $oldManifestPath) {
  foreach ($line in Get-Content $oldManifestPath) {
    if ($line -match '^skill (\S+) (\S+)$') { $recorded["skill:" + $Matches[1]] = $Matches[2] }
    elseif ($line -match '^agent (\S+) (.+)$') { $recorded["agent:" + $Matches[2]] = $Matches[1] }
  }
}
$backupDir = Join-Path (Split-Path $skillsDest -Parent) (".seo-skills-backups\" + (Get-Date -Format "yyyyMMdd-HHmmss"))
$mod = 0
$manifestLines = New-Object System.Collections.Generic.List[string]
$sk = 0
Get-ChildItem (Join-Path $src "skills") -Directory | ForEach-Object {
  if (Test-Path (Join-Path $_.FullName "SKILL.md")) {
    $dst = Join-Path $skillsDest $_.Name
    $newHash = Get-DirHash $_.FullName
    if (Test-Path $dst) {
      $oldHash = Get-DirHash $dst
      $rec = $recorded["skill:" + $_.Name]
      if ($oldHash -ne $newHash -and $oldHash -ne $rec) {
        New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
        Copy-Item $dst (Join-Path $backupDir $_.Name) -Recurse
        $mod++
      }
      Remove-Item $dst -Recurse -Force
    }
    Copy-Item $_.FullName $dst -Recurse
    $manifestLines.Add("skill $($_.Name) $newHash")
    $sk++
  }
}
Get-ChildItem $skillsDest -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue |
  ForEach-Object { Remove-Item $_.FullName -Recurse -Force -ErrorAction SilentlyContinue }
$ag = 0
if ($agentsDest) {
  Get-ChildItem (Join-Path $src "agents") -Filter *.md -ErrorAction SilentlyContinue | ForEach-Object {
    $af = Join-Path $agentsDest $_.Name
    $newAh = (Get-FileHash $_.FullName -Algorithm SHA256).Hash
    if (Test-Path $af) {
      $oldAh = (Get-FileHash $af -Algorithm SHA256).Hash
      if ($oldAh -ne $newAh -and $oldAh -ne $recorded["agent:" + $af]) {
        New-Item -ItemType Directory -Force -Path (Join-Path $backupDir "agents") | Out-Null
        Copy-Item $af (Join-Path $backupDir "agents") -Force
        $mod++
      }
    }
    Copy-Item $_.FullName $agentsDest -Force
    $manifestLines.Add("agent $newAh $af")
    $ag++
  }
}
Set-Content -Path $markerPath -Value $selfVersion -Encoding utf8
Set-Content -Path (Join-Path $skillsDest $Manifest) -Value $manifestLines -Encoding utf8

Write-Host ""
if ($installedVersion -and $installedVersion -ne $selfVersion) {
  Write-Host "OK - Actualizadas $sk skills a la version $selfVersion en $skillsDest (antes: $installedVersion)" -ForegroundColor Green
} else {
  Write-Host "OK - Instaladas $sk skills (version $selfVersion) en $skillsDest" -ForegroundColor Green
}
if ($mod -gt 0) {
  Write-Host "! Detecte $mod skill(s) o agente(s) con cambios hechos a mano (o de una version sin registro). Guarde una copia antes de actualizar en: $backupDir" -ForegroundColor Yellow
}
if ($agentsDest) {
  Write-Host "OK - Instalados $ag agentes en $agentsDest" -ForegroundColor Green
} else {
  Write-Host "! Los subagentes son exclusivos de Claude Code; no se instalan en '$Client'. Las skills funcionan igual." -ForegroundColor Yellow
}

# --- 5) extras opcionales, solo con -Full / -WithUv ---
if (($Full -or $WithUv) -and -not $NoUv) {
  Write-Host ""
  if (Get-Command uv -ErrorAction SilentlyContinue) {
    Write-Host "OK - uv ya esta instalado: los scripts corren con 'uv run'." -ForegroundColor Green
  } else {
    Write-Host "Instalando uv (script oficial de $UvPs1; lo pediste con -Full)..."
    try { Invoke-RestMethod $UvPs1 | Invoke-Expression; Write-Host "OK - uv instalado. Quizas necesites abrir una terminal nueva." -ForegroundColor Green }
    catch { Write-Host "! No se pudo instalar uv. Hazlo a mano: irm $UvPs1 | iex" -ForegroundColor Yellow }
  }
}

# --- 6) cierre ---
if ($tmp -and (Test-Path $tmp)) { Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue }
$elapsed = [int]((Get-Date) - $start).TotalSeconds
Write-Host ""
Write-Host "Listo en $elapsed s. Reinicia tu cliente y prueba:" -ForegroundColor Green
Write-Host "    /aprendoclub help"
Write-Host "    /aprendoclub audit midominio.com"
if (-not (Get-Command python -ErrorAction SilentlyContinue) -and -not (Get-Command py -ErrorAction SilentlyContinue)) {
  Write-Host "No encontre Python: los scripts no correran y las skills usaran el modo manual." -ForegroundColor DarkGray
}
if (-not $Full) {
  Write-Host "Extras opcionales (uv para los scripts): vuelve a correr con -Full. Datos en vivo: MCP-SETUP.md." -ForegroundColor DarkGray
}
if ($Client -eq "claude" -and -not $useDir) {
  Write-Host "Alternativa como plugin: /plugin marketplace add $Repo y /plugin install seo-skills@aprendoseo (no lo combines con esta instalacion)." -ForegroundColor DarkGray
}
Write-Host "Para quitarlas: uninstall.ps1. Para buscar actualizaciones: -Check." -ForegroundColor DarkGray
