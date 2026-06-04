# Instalador de las SEO Skills de aprendoseo ("De Cero a SEO") para Windows / PowerShell.
# Funciona con Claude Code y otros clientes compatibles con Agent Skills
# (Cursor, VS Code, OpenAI Codex, GitHub Copilot).
#
# Uso rapido (un comando, en PowerShell):
#   irm https://raw.githubusercontent.com/Arianna-Lupi/SEO-Skills/main/install.ps1 | iex
#
# Con parametros (clona el repo y corre .\install.ps1):
#   .\install.ps1 -Client cursor
#   .\install.ps1 -Project          (Claude Code, solo este proyecto)
#   .\install.ps1 -Check            (solo dice si hay version nueva; no instala)
#   .\install.ps1 -Update           (actualiza las skills sin preguntar)
#   .\install.ps1 -WithUv           (instala uv aunque no sea interactivo)
#   .\install.ps1 -NoUv             (no chequea uv)
#   .\install.ps1 -Dir C:\ruta      (carpeta concreta: crea skills\ y agents\)
#
# Requisitos: git. Python/uv son OPCIONALES (solo para los scripts; las skills
# funcionan sin ellos, en modo manual). Si dejas que el instalador configure uv,
# los scripts corren solos sin admin ni Python del sistema.
param(
  [string]$Client = "claude",   # claude | cursor | agents | codex | copilot
  [switch]$Project,             # Claude Code: solo este proyecto
  [string]$Dir = "",            # carpeta concreta (override)
  [switch]$Check,               # solo busca actualizaciones, no instala
  [switch]$Update,              # actualiza sin preguntar
  [switch]$WithUv,              # instala uv aunque no sea interactivo
  [switch]$NoUv                 # salta el chequeo de uv
)

$ErrorActionPreference = "Stop"
$RepoUrl  = "https://github.com/Arianna-Lupi/SEO-Skills.git"
$RawBase  = "https://raw.githubusercontent.com/Arianna-Lupi/SEO-Skills/main"
$UvPs1    = "https://astral.sh/uv/install.ps1"
$Marker   = ".seo-skills-version"

function Get-RemoteVersion {
  try { return (Invoke-RestMethod -Uri "$RawBase/VERSION" -TimeoutSec 8).ToString().Trim() }
  catch { return "" }
}
# Devuelve $true si $a es mas nueva que $b (compara como [version], con fallback a texto).
function Test-Newer($a, $b) {
  if ([string]::IsNullOrEmpty($a) -or [string]::IsNullOrEmpty($b)) { return $false }
  if ($a -eq $b) { return $false }
  try { return ([version]$a -gt [version]$b) } catch { return ($a -ne $b) }
}

Write-Host ""
Write-Host "SEO Skills - aprendoseo (De Cero a SEO)" -ForegroundColor Cyan
Write-Host "13 skills + 3 agentes para Claude Code y clientes compatibles" -ForegroundColor DarkGray
Write-Host ""

# --- 1) localizar la fuente; clonar a temp si corre via irm|iex ---
$src = $null
$localClone = $false
if ($PSScriptRoot -and (Test-Path (Join-Path $PSScriptRoot "skills"))) {
  $src = $PSScriptRoot; $localClone = $true
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

# Version de este paquete y la ultima publicada.
$selfVersion = "0.0.0"
$vfile = Join-Path $src "VERSION"
if (Test-Path $vfile) { $selfVersion = (Get-Content $vfile -First 1).Trim() }
$remoteVersion = Get-RemoteVersion

# --- 1b) si corres un clon local viejo, avisa que hay instalador nuevo ---
if ($localClone -and (Test-Newer $remoteVersion $selfVersion)) {
  Write-Host "! Hay una version nueva del instalador y de las skills: $selfVersion -> $remoteVersion." -ForegroundColor Yellow
  Write-Host "  Para traerla: 'git pull' en el repo, o corre el comando de una linea de arriba." -ForegroundColor DarkGray
  Write-Host ""
}

# --- 2) determinar interactividad y elegir cliente ---
$interactive = [Environment]::UserInteractive -and -not [Console]::IsInputRedirected -and -not $Check
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

# Solo Claude Code distingue usuario vs proyecto.
if ($Client -eq "claude" -and -not $Project -and -not $useDir -and $interactive -and -not $clientGiven) {
  Write-Host ""
  Write-Host "Donde, dentro de Claude Code?"
  Write-Host "  1) Para tu usuario    (~/.claude)   [recomendado]"
  Write-Host "  2) Solo este proyecto (./.claude)"
  $cs = Read-Host "Opcion [1]"
  if ($cs -eq "2") { $Project = $true }
}

# --- 3) resolver carpetas destino segun cliente ---
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

# Version ya instalada en ese destino, si hay marcador previo.
$installedVersion = ""
$markerPath = Join-Path $skillsDest $Marker
if (Test-Path $markerPath) { $installedVersion = (Get-Content $markerPath -First 1).Trim() }
$target = if ($remoteVersion) { $remoteVersion } else { $selfVersion }

# --- modo -Check: informa y sale ---
if ($Check) {
  Write-Host "Cliente: $Client    Carpeta: $skillsDest" -ForegroundColor DarkGray
  if ($installedVersion) { Write-Host "Instalada:  $installedVersion" } else { Write-Host "Instalada:  (ninguna detectada aqui)" }
  Write-Host "Disponible: $target"
  if (-not $installedVersion) {
    Write-Host "! No hay instalacion previa aqui. Corre el instalador sin -Check para instalarlas." -ForegroundColor Yellow
  } elseif (Test-Newer $target $installedVersion) {
    Write-Host "! Hay una version nueva ($installedVersion -> $target). Actualiza con: -Update" -ForegroundColor Yellow
  } else {
    Write-Host "OK - Estas al dia (version $installedVersion)." -ForegroundColor Green
  }
  return
}

# --- si ya hay version instalada, avisa y pide confirmacion (salvo -Update) ---
if ($installedVersion -and -not $Update) {
  if (Test-Newer $target $installedVersion) {
    Write-Host "! Ya tienes la version $installedVersion instalada; esta es la $target." -ForegroundColor Yellow
    if ($interactive) {
      $doup = Read-Host "Actualizo las skills a la $target? [S/n]"
      if ($doup -match '^[nN]') { Write-Host "Listo, no toco nada." -ForegroundColor DarkGray; return }
    }
  } else {
    Write-Host "Ya estas en la version $installedVersion; reinstalo los archivos por si acaso." -ForegroundColor DarkGray
  }
}

New-Item -ItemType Directory -Force -Path $skillsDest | Out-Null
if ($agentsDest) { New-Item -ItemType Directory -Force -Path $agentsDest | Out-Null }

# --- 4) copiar skills (todos) y agentes (solo Claude) ---
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
if ($agentsDest) {
  Get-ChildItem (Join-Path $src "agents") -Filter *.md -ErrorAction SilentlyContinue | ForEach-Object {
    Copy-Item $_.FullName $agentsDest -Force; $ag++
  }
}

# Marcador de version para detectar futuras actualizaciones.
Set-Content -Path $markerPath -Value $selfVersion -Encoding utf8

Write-Host ""
if ($installedVersion -and $installedVersion -ne $selfVersion) {
  Write-Host "OK - Actualizadas $sk skills a la version $selfVersion en $skillsDest (antes: $installedVersion)" -ForegroundColor Green
} else {
  Write-Host "OK - Instaladas $sk skills (version $selfVersion) en $skillsDest" -ForegroundColor Green
}
if ($agentsDest) {
  Write-Host "OK - Instalados $ag agentes en $agentsDest" -ForegroundColor Green
} else {
  Write-Host "! Los subagentes son exclusivos de Claude Code; no se instalan en '$Client'. Las skills funcionan igual." -ForegroundColor Yellow
}

# --- 5) runtime para los scripts: detectar / ofrecer uv (nunca falla) ---
Write-Host ""
Write-Host "Scripts (aceleradores opcionales - las skills funcionan sin esto):" -ForegroundColor DarkGray
$uvJustInstalled = $false
if ($NoUv) {
  Write-Host "Chequeo de uv omitido (-NoUv)." -ForegroundColor DarkGray
} elseif (Get-Command uv -ErrorAction SilentlyContinue) {
  Write-Host "OK - uv detectado: los scripts corren con 'uv run' sin instalar nada." -ForegroundColor Green
} else {
  $doInstall = $false
  if ($WithUv) {
    $doInstall = $true
  } elseif ($interactive) {
    $ans = Read-Host "Instalar uv para que los scripts corran solos? [S/n]"
    if ([string]::IsNullOrEmpty($ans) -or $ans -match '^[sSyY]') { $doInstall = $true }
    else { Write-Host "Saltado. Para instalarlo luego: irm $UvPs1 | iex" -ForegroundColor DarkGray }
  } else {
    if (Get-Command python -ErrorAction SilentlyContinue) {
      Write-Host "OK - python detectado: para scripts con dependencias 'pip install requests beautifulsoup4'." -ForegroundColor Green
    }
    Write-Host "! Para que los scripts corran solos, instala uv (un binario, sin admin, trae Python):" -ForegroundColor Yellow
    Write-Host "    irm $UvPs1 | iex" -ForegroundColor Yellow
  }
  if ($doInstall) {
    Write-Host "Instalando uv..."
    try { Invoke-RestMethod $UvPs1 | Invoke-Expression; $uvJustInstalled = $true }
    catch { Write-Host "! No se pudo instalar uv automaticamente. Hazlo a mano: irm $UvPs1 | iex" -ForegroundColor Yellow }
  }
  if ($uvJustInstalled) {
    Write-Host "OK - uv instalado." -ForegroundColor Green
    Write-Host "! Quizas necesites abrir una terminal nueva para que 'uv' quede en el PATH." -ForegroundColor Yellow
  }
}

Write-Host ""
Write-Host "Listo. Reinicia tu cliente y escribe '/' (por ejemplo /brief-de-contenido)." -ForegroundColor Green
Write-Host "Para buscar actualizaciones mas adelante, corre el instalador con -Check." -ForegroundColor DarkGray
