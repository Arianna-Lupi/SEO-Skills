# aprendoclub-run.ps1: lanzador único de los scripts de las SEO Skills para Windows.
# Mismos comandos que aprendoclub-run (bash):
#   .\aprendoclub-run.ps1 <script> [args...]
#   .\aprendoclub-run.ps1 --check <script>|--all
#   .\aprendoclub-run.ps1 --status
#   .\aprendoclub-run.ps1 --install <script> --yes
#   .\aprendoclub-run.ps1 --update-check
# Intérprete, en este orden: APRENDOCLUB_PYTHON, py -3, python3, python (Python 3.9+; se ignora
# el atajo falso de la Microsoft Store). No instala nada por su cuenta.
$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path

function Test-Py($exe, $pre) {
  try {
    & $exe @pre -c "import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)" 2>$null
    return ($LASTEXITCODE -eq 0)
  } catch { return $false }
}

$py = $null; $pre = @()
if ($env:APRENDOCLUB_PYTHON) {
  if (Test-Py $env:APRENDOCLUB_PYTHON @()) { $py = $env:APRENDOCLUB_PYTHON }
} else {
  if ((Get-Command py -ErrorAction SilentlyContinue) -and (Test-Py "py" @("-3"))) { $py = "py"; $pre = @("-3") }
  if (-not $py) {
    foreach ($c in @("python3", "python")) {
      $cmd = Get-Command $c -ErrorAction SilentlyContinue
      if ($cmd -and $cmd.Source -notmatch "WindowsApps" -and (Test-Py $cmd.Source @())) { $py = $cmd.Source; break }
    }
  }
}

if (-not $py) {
  $msg = '{"ok": false, "reason": "no encontre Python 3.9 o superior", "fallback": "modo manual: las skills funcionan sin scripts", "needs": [{"type": "python", "name": "Python 3.9+", "required": true, "command": "winget install Python.Python.3.12", "where": "https://www.python.org/downloads/", "fallback": "modo manual"}]}'
  Write-Output $msg
  exit 3
}

if ($args.Count -gt 0 -and $args[0] -eq "--update-check") {
  & $py @pre (Join-Path $here "actualizar.py") --check @($args | Select-Object -Skip 1)
  exit $LASTEXITCODE
}
if ($args.Count -eq 0) { & $py @pre (Join-Path $here "requisitos.py") --help; exit $LASTEXITCODE }
& $py @pre (Join-Path $here "requisitos.py") @args
exit $LASTEXITCODE
