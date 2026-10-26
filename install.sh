#!/usr/bin/env bash
#
# Instalador de las SEO Skills de aprendoseo ("De Cero a SEO").
# Funciona con Claude Code y otros clientes compatibles con Agent Skills
# (Cursor, VS Code, OpenAI Codex, GitHub Copilot).
#
# Camino rápido (por defecto): sin preguntas, sin instalar dependencias, un solo
# archivo descargado (tarball, sin git) y menos de ~10 segundos. Es idempotente:
# puedes correrlo otra vez para actualizar.
#
# Uso (un comando):
#   curl -fsSL https://raw.githubusercontent.com/Arianna-Lupi/SEO-Skills/main/install.sh | bash
#
# Con opciones:
#   curl -fsSL https://raw.githubusercontent.com/Arianna-Lupi/SEO-Skills/main/install.sh | bash -s -- --full
#
# Flags:
#   --client ID   cliente destino: claude | cursor | agents | codex | copilot
#                 (por defecto: claude)
#   --user        Claude Code, para tu usuario (~/.claude) [por defecto en claude]
#   --project     Claude Code, solo este proyecto (./.claude)
#   --dir RUTA    instala en una carpeta concreta (crea skills/ y agents/ dentro)
#   --full        además de instalar: configura uv (para que los scripts corran solos)
#   --interactive pregunta cliente y alcance (el comportamiento antiguo)
#   --check       solo dice si hay una versión nueva; no instala nada
#   --update      alias de la instalación normal (siempre actualiza)
#   --with-uv     solo el extra de uv (parte de --full)
#   --no-uv       no chequea ni ofrece uv (es el comportamiento por defecto)
#   --ref REF     rama o etiqueta a instalar (por defecto: main)
#   -h, --help    muestra esta ayuda
#
# Requisitos: bash y curl (o wget). git solo como respaldo si no hay curl ni wget.
# Python y uv son OPCIONALES (solo para los scripts; las skills funcionan sin ellos).
# Desinstalar: uninstall.sh (mismas opciones --client/--user/--project/--dir).
set -euo pipefail

REPO="Arianna-Lupi/SEO-Skills"
REPO_URL="https://github.com/${REPO}.git"
REF="${SEO_SKILLS_REF:-main}"
# SEO_SKILLS_TARBALL_URL permite probar con un tarball local (file://) o un espejo.
TARBALL_URL_OVERRIDE="${SEO_SKILLS_TARBALL_URL:-}"
UV_SH="https://astral.sh/uv/install.sh"
MARKER=".seo-skills-version"      # versión instalada, dentro de la carpeta de skills
MANIFEST=".seo-skills-manifest"   # qué se instaló, para que uninstall borre solo eso

BLUE=""; GREEN=""; YELLOW=""; DIM=""; RST=""
if [ -t 1 ]; then BLUE=$'\033[34m'; GREEN=$'\033[32m'; YELLOW=$'\033[33m'; DIM=$'\033[2m'; RST=$'\033[0m'; fi
say()  { printf "%s\n" "$*"; }
ok()   { printf "%s✓%s %s\n" "$GREEN" "$RST" "$*"; }
warn() { printf "%s!%s %s\n" "$YELLOW" "$RST" "$*"; }
die()  { printf "Error: %s\n" "$*" >&2; exit 1; }

usage() { sed -n '3,33p' "$0" 2>/dev/null | sed 's/^# \{0,1\}//'; }

now() { date +%s; }
START="$(now)"

# Lee una URL a stdout (curl o wget); silencioso.
fetch() {
  if command -v curl >/dev/null 2>&1; then curl -fsSL --max-time 8 "$1" 2>/dev/null
  elif command -v wget >/dev/null 2>&1; then wget -qO- --timeout=8 "$1" 2>/dev/null
  fi
}
# Descarga $1 al archivo $2.
download() {
  if command -v curl >/dev/null 2>&1; then curl -fsSL --retry 2 --max-time 60 -o "$2" "$1"
  elif command -v wget >/dev/null 2>&1; then wget -q --tries=2 --timeout=60 -O "$2" "$1"
  else return 1
  fi
}
clean_ver() { printf "%s" "${1:-}" | head -n1 | tr -d '[:space:]'; }
ver_gt() {
  [ "$1" != "$2" ] || return 1
  [ "$(printf '%s\n%s\n' "$1" "$2" | sort -V | tail -n1)" = "$1" ]
}

CLIENT=""; SCOPE=""; CUSTOM_DIR=""
MODE="install"          # install | check
FULL=0; INTERACTIVE=0; WANT_UV=0
while [ $# -gt 0 ]; do
  case "$1" in
    --client) [ -n "${2:-}" ] || die "--client necesita un valor"; CLIENT="$2"; shift 2 ;;
    --user) SCOPE="user"; shift ;;
    --project) SCOPE="project"; shift ;;
    --agents) CLIENT="agents"; shift ;;   # compat: antes era un destino
    --dir) [ -n "${2:-}" ] || die "--dir necesita una ruta"; SCOPE="dir"; CUSTOM_DIR="$2"; shift 2 ;;
    --ref) [ -n "${2:-}" ] || die "--ref necesita un valor"; REF="$2"; shift 2 ;;
    --check) MODE="check"; shift ;;
    --update) shift ;;                    # compat: instalar ya actualiza sin preguntar
    --full) FULL=1; WANT_UV=1; shift ;;
    --interactive|-i) INTERACTIVE=1; shift ;;
    --with-uv) WANT_UV=1; shift ;;
    --no-uv) WANT_UV=0; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Opción desconocida: $1" >&2; exit 1 ;;
  esac
done

say ""
say "${BLUE}SEO Skills de aprendoseo (\"De Cero a SEO\")${RST}"
say "${DIM}Enrutador /aprendoclub + skills y agentes para Claude Code y clientes compatibles${RST}"
say ""

# --- 1) localizar la fuente: carpeta local si el script es un archivo del repo; si no, tarball ---
SRC=""; TMP=""
cleanup() { if [ -n "$TMP" ]; then rm -rf -- "$TMP"; fi; }
trap cleanup EXIT
SELF_DIR=""
if [ -n "${BASH_SOURCE[0]:-}" ] && [ -f "${BASH_SOURCE[0]}" ]; then
  SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fi
if [ -n "$SELF_DIR" ] && [ -d "$SELF_DIR/skills" ]; then
  SRC="$SELF_DIR"
elif [ "$MODE" = "check" ]; then
  : # --check no necesita descargar el paquete
else
  TMP="$(mktemp -d)"
  TARBALL_URL="${TARBALL_URL_OVERRIDE:-https://codeload.github.com/${REPO}/tar.gz/${REF}}"
  say "${DIM}Descargando ${REPO}@${REF}…${RST}"
  if download "$TARBALL_URL" "$TMP/pkg.tar.gz" 2>/dev/null && tar -xzf "$TMP/pkg.tar.gz" -C "$TMP" 2>/dev/null; then
    SRC="$(find "$TMP" -mindepth 1 -maxdepth 1 -type d | head -n1)"
  elif command -v git >/dev/null 2>&1; then
    warn "No pude bajar el paquete comprimido; uso git como respaldo."
    git clone --depth 1 --branch "$REF" "$REPO_URL" "$TMP/SEO-Skills" >/dev/null 2>&1 \
      || die "no pude descargar $REPO@$REF (revisa tu conexión o el nombre de --ref)."
    SRC="$TMP/SEO-Skills"
  else
    die "no pude descargar el paquete y no hay git de respaldo. Instala curl o git, o baja el ZIP desde ${REPO_URL%.git}."
  fi
  if [ -z "$SRC" ] || [ ! -d "$SRC/skills" ]; then die "el paquete descargado no trae skills/."; fi
fi

SELF_VERSION="0.0.0"
if [ -n "$SRC" ]; then SELF_VERSION="$(clean_ver "$(cat "$SRC/VERSION" 2>/dev/null || true)")"; fi
[ -n "$SELF_VERSION" ] || SELF_VERSION="0.0.0"

# --- 2) cliente y alcance: por defecto Claude Code, usuario, sin preguntar ---
if [ "$SCOPE" != "dir" ]; then
  if [ -z "$CLIENT" ]; then
    if [ "$INTERACTIVE" = "1" ] && [ -r /dev/tty ] && [ "$MODE" != "check" ]; then
      say "¿Para qué cliente las instalo?"
      say "  1) Claude Code   ${DIM}[recomendado]${RST}"
      say "  2) Cursor"
      say "  3) VS Code / Agent Skills (estándar)"
      say "  4) OpenAI Codex"
      say "  5) GitHub Copilot"
      printf "Opción [1]: "; read -r ci </dev/tty || ci=1
      case "${ci:-1}" in
        2) CLIENT="cursor" ;; 3) CLIENT="agents" ;; 4) CLIENT="codex" ;; 5) CLIENT="copilot" ;; *) CLIENT="claude" ;;
      esac
    else
      CLIENT="claude"
    fi
  fi
  if [ "$CLIENT" = "claude" ] && [ -z "$SCOPE" ]; then
    if [ "$INTERACTIVE" = "1" ] && [ -r /dev/tty ] && [ "$MODE" != "check" ]; then
      say ""
      say "¿Dónde, dentro de Claude Code?"
      say "  1) Para tu usuario    (~/.claude)   ${DIM}[recomendado, todos tus proyectos]${RST}"
      say "  2) Solo este proyecto (./.claude)"
      printf "Opción [1]: "; read -r cs </dev/tty || cs=1
      case "${cs:-1}" in 2) SCOPE="project" ;; *) SCOPE="user" ;; esac
    else
      SCOPE="user"
    fi
  fi
fi

# --- 3) carpetas destino ---
AGENTS_DEST=""
if [ "$SCOPE" = "dir" ]; then
  SKILLS_DEST="$CUSTOM_DIR/skills"; AGENTS_DEST="$CUSTOM_DIR/agents"
  CLIENT="${CLIENT:-claude}"
else
  case "$CLIENT" in
    claude)
      if [ "$SCOPE" = "project" ]; then
        SKILLS_DEST="$(pwd)/.claude/skills"; AGENTS_DEST="$(pwd)/.claude/agents"
      else
        SKILLS_DEST="$HOME/.claude/skills"; AGENTS_DEST="$HOME/.claude/agents"
      fi ;;
    cursor)  SKILLS_DEST="$(pwd)/.cursor/skills" ;;
    agents)  SKILLS_DEST="$(pwd)/.agents/skills" ;;
    codex)   SKILLS_DEST="$(pwd)/.codex/skills" ;;
    copilot) SKILLS_DEST="$(pwd)/.github/skills" ;;
    *) die "cliente desconocido: $CLIENT (usa claude|cursor|agents|codex|copilot)" ;;
  esac
fi
INSTALLED_VERSION="$(clean_ver "$(cat "$SKILLS_DEST/$MARKER" 2>/dev/null || true)")"

# --- modo --check: informa y sale ---
if [ "$MODE" = "check" ]; then
  REMOTE_VERSION="$(clean_ver "$(fetch "https://raw.githubusercontent.com/${REPO}/${REF}/VERSION" || true)")"
  say "${DIM}Cliente:${RST} $CLIENT    ${DIM}Carpeta:${RST} $SKILLS_DEST"
  if [ -n "$INSTALLED_VERSION" ]; then say "Instalada:  ${INSTALLED_VERSION}"; else say "Instalada:  (ninguna detectada aquí)"; fi
  TARGET="${REMOTE_VERSION:-$SELF_VERSION}"
  say "Disponible: ${TARGET}"
  if [ -z "$INSTALLED_VERSION" ]; then
    warn "No hay una instalación previa en esta carpeta. Corre el instalador sin --check."
  elif ver_gt "$TARGET" "$INSTALLED_VERSION"; then
    warn "Hay una versión nueva (${INSTALLED_VERSION} → ${TARGET}). Vuelve a correr el instalador para actualizar."
  else
    ok "Estás al día (versión ${INSTALLED_VERSION})."
  fi
  exit 0
fi

mkdir -p "$SKILLS_DEST"
if [ -n "$AGENTS_DEST" ]; then mkdir -p "$AGENTS_DEST"; fi

# --- 4) copiar skills (todos los clientes) y agentes (solo Claude) ---
# Huella de una carpeta (nombres y contenido, sin __pycache__): detecta si modificaste una skill a mano.
dir_hash() {
  ( cd "$1" && find . -type f ! -path '*/__pycache__/*' ! -name '*.pyc' ! -name '.DS_Store' \
      | LC_ALL=C sort | while IFS= read -r f; do printf '%s\n' "$f"; cat "$f"; done | cksum | awk '{print $1 "-" $2}' )
}
OLD_MANIFEST="$SKILLS_DEST/$MANIFEST"
TS="$(date +%Y%m%d-%H%M%S)"
BACKUP_DIR="$(dirname "$SKILLS_DEST")/.seo-skills-backups/$TS"
MOD=0
TMP_MANIFEST="$(mktemp)"
SK=0
for d in "$SRC"/skills/*/; do
  [ -f "${d}SKILL.md" ] || continue
  name="$(basename "$d")"
  dst="$SKILLS_DEST/$name"
  new_h="$(dir_hash "$d")"
  if [ -d "$dst" ]; then
    old_h="$(dir_hash "$dst")"
    rec_h=""
    if [ -f "$OLD_MANIFEST" ]; then rec_h="$(awk -v n="$name" '$1=="skill" && $2==n {print $3}' "$OLD_MANIFEST")"; fi
    if [ "$old_h" != "$new_h" ] && [ "$old_h" != "$rec_h" ]; then
      mkdir -p "$BACKUP_DIR" && cp -R "$dst" "$BACKUP_DIR/$name"
      MOD=$((MOD+1))
    fi
  fi
  rm -rf "${SKILLS_DEST:?}/$name"
  cp -R "$d" "$dst"
  printf "skill %s %s\n" "$name" "$new_h" >> "$TMP_MANIFEST"
  SK=$((SK+1))
done
# Limpieza de basura de desarrollo que no hace falta en el destino.
find "$SKILLS_DEST" -type d -name __pycache__ -prune -exec rm -rf {} + 2>/dev/null || true
find "$SKILLS_DEST" -name '.DS_Store' -delete 2>/dev/null || true
AG=0
if [ -n "$AGENTS_DEST" ]; then
  for f in "$SRC"/agents/*.md; do
    [ -f "$f" ] || continue
    base="$(basename "$f")"; af="$AGENTS_DEST/$base"
    new_ah="$(cksum < "$f" | awk '{print $1 "-" $2}')"
    if [ -f "$af" ]; then
      old_ah="$(cksum < "$af" | awk '{print $1 "-" $2}')"
      rec_ah=""
      if [ -f "$OLD_MANIFEST" ]; then rec_ah="$(awk -v p="$af" '$1=="agent" && $3==p {print $2}' "$OLD_MANIFEST")"; fi
      if [ "$old_ah" != "$new_ah" ] && [ "$old_ah" != "$rec_ah" ]; then
        mkdir -p "$BACKUP_DIR/agents" && cp "$af" "$BACKUP_DIR/agents/"
        MOD=$((MOD+1))
      fi
    fi
    cp "$f" "$AGENTS_DEST/"
    printf "agent %s %s\n" "$new_ah" "$af" >> "$TMP_MANIFEST"
    AG=$((AG+1))
  done
fi
printf "%s\n" "$SELF_VERSION" > "$SKILLS_DEST/$MARKER" 2>/dev/null || true
mv "$TMP_MANIFEST" "$SKILLS_DEST/$MANIFEST" 2>/dev/null || rm -f "$TMP_MANIFEST"

say ""
if [ -n "$INSTALLED_VERSION" ] && [ "$INSTALLED_VERSION" != "$SELF_VERSION" ]; then
  ok "Actualizadas ${SK} skills a la versión ${SELF_VERSION} en ${SKILLS_DEST} (antes: ${INSTALLED_VERSION})"
else
  ok "Instaladas ${SK} skills (versión ${SELF_VERSION}) en ${SKILLS_DEST}"
fi
if [ "$MOD" -gt 0 ]; then
  warn "Detecté ${MOD} skill(s) con cambios hechos a mano (o de una versión sin registro). Guardé una copia antes de actualizar en: ${BACKUP_DIR}"
fi
if [ -n "$AGENTS_DEST" ]; then
  ok "Instalados ${AG} agentes en ${AGENTS_DEST}"
else
  warn "Los subagentes son exclusivos de Claude Code; no se instalan en '${CLIENT}'. Las skills funcionan igual."
fi

# --- 5) extras opcionales, solo con --full / --with-uv ---
if [ "$WANT_UV" = "1" ]; then
  say ""
  if command -v uv >/dev/null 2>&1; then
    ok "uv ya está instalado: los scripts corren con 'uv run' sin instalar nada más."
  elif command -v curl >/dev/null 2>&1; then
    say "Instalando uv (script oficial de $UV_SH; lo pediste con --full)…"
    if curl -LsSf "$UV_SH" | sh >/dev/null 2>&1; then
      ok "uv instalado. Quizás necesites abrir una terminal nueva."
    else
      warn "No pude instalar uv. Hazlo a mano: curl -LsSf $UV_SH | sh"
    fi
  else
    warn "No hay curl para instalar uv. Hazlo a mano: curl -LsSf $UV_SH | sh"
  fi
fi

# --- 6) cierre ---
ELAPSED=$(( $(now) - START ))
say ""
say "${GREEN}Listo en ${ELAPSED} s.${RST} Reinicia tu cliente y prueba:"
say "    /aprendoclub help"
say "    /aprendoclub audit midominio.com"
if ! command -v python3 >/dev/null 2>&1; then
  say "${DIM}No encontré python3: los scripts no correrán y las skills usarán el modo manual.${RST}"
fi
if [ "$FULL" != "1" ]; then
  say "${DIM}Extras opcionales (uv para los scripts): vuelve a correr con --full. Datos en vivo: MCP-SETUP.md.${RST}"
fi
if [ "$CLIENT" = "claude" ] && [ "$SCOPE" != "dir" ]; then
  say "${DIM}Alternativa como plugin: /plugin marketplace add ${REPO} y /plugin install seo-skills@aprendoseo (no lo combines con esta instalación).${RST}"
fi
say "${DIM}Para quitarlas: uninstall.sh. Para buscar actualizaciones: --check.${RST}"
