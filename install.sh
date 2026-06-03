#!/usr/bin/env bash
#
# Instalador de las SEO Skills de aprendoseo ("De Cero a SEO") para Claude Code
# y otros clientes compatibles con el estándar Agent Skills.
#
# Uso rápido (un comando):
#   curl -fsSL https://raw.githubusercontent.com/Arianna-Lupi/SEO-Skills/main/install.sh | bash
#
# Flags (saltan el menú interactivo):
#   --user        instala en ~/.claude (Claude Code, todos tus proyectos) [por defecto]
#   --project     instala en ./.claude (solo el proyecto actual)
#   --agents      instala en ./.agents/skills (estándar Agent Skills: VS Code, etc.)
#   --dir RUTA    instala en una carpeta concreta (debe tener skills/ y agents/)
#
# Requisitos: bash y git. Python/uv son OPCIONALES (solo para los scripts; las
# skills funcionan sin ellos, en "modo manual").
set -euo pipefail

REPO_URL="https://github.com/Arianna-Lupi/SEO-Skills.git"
BLUE=""; GREEN=""; YELLOW=""; DIM=""; RST=""
if [ -t 1 ]; then BLUE=$'\033[34m'; GREEN=$'\033[32m'; YELLOW=$'\033[33m'; DIM=$'\033[2m'; RST=$'\033[0m'; fi
say()  { printf "%s\n" "$*"; }
ok()   { printf "%s✓%s %s\n" "$GREEN" "$RST" "$*"; }
warn() { printf "%s!%s %s\n" "$YELLOW" "$RST" "$*"; }

MODE=""; CUSTOM_DIR=""
while [ $# -gt 0 ]; do
  case "$1" in
    --user) MODE="user"; shift ;;
    --project) MODE="project"; shift ;;
    --agents) MODE="agents"; shift ;;
    --dir) MODE="dir"; CUSTOM_DIR="${2:-}"; shift 2 ;;
    -h|--help) sed -n '2,20p' "$0"; exit 0 ;;
    *) echo "Opción desconocida: $1" >&2; exit 1 ;;
  esac
done

say ""
say "${BLUE}SEO Skills — aprendoseo (\"De Cero a SEO\")${RST}"
say "${DIM}13 skills + 3 agentes para Claude Code${RST}"
say ""

# --- 1) requisito mínimo: git (solo si hay que clonar) ---
SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd || true)"
if [ -n "$SELF_DIR" ] && [ -d "$SELF_DIR/skills" ]; then
  SRC="$SELF_DIR"
else
  if ! command -v git >/dev/null 2>&1; then
    echo "Necesitás git para descargar el repo. Instalá git y reintentá," >&2
    echo "o bajá el ZIP desde $REPO_URL y corré ./install.sh dentro." >&2
    exit 1
  fi
  TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
  say "Descargando SEO-Skills…"
  git clone --depth 1 "$REPO_URL" "$TMP/SEO-Skills" >/dev/null 2>&1
  SRC="$TMP/SEO-Skills"
fi
[ -d "$SRC/skills" ] || { echo "No encontré skills/ en $SRC" >&2; exit 1; }

# --- 2) elegir destino (menú si es interactivo y no hubo flag) ---
if [ -z "$MODE" ]; then
  if [ -t 0 ]; then
    say "¿Dónde las instalo?"
    say "  1) Claude Code, para tu usuario   (~/.claude)        ${DIM}[recomendado]${RST}"
    say "  2) Claude Code, solo este proyecto (./.claude)"
    say "  3) Estándar Agent Skills           (./.agents/skills) ${DIM}VS Code y otros${RST}"
    printf "Opción [1]: "; read -r choice </dev/tty || choice=1
    case "${choice:-1}" in
      2) MODE="project" ;; 3) MODE="agents" ;; *) MODE="user" ;;
    esac
  else
    MODE="user"   # piped (curl|bash, no TTY): por defecto usuario
  fi
fi

case "$MODE" in
  user)    SKILLS_DEST="$HOME/.claude/skills"; AGENTS_DEST="$HOME/.claude/agents" ;;
  project) SKILLS_DEST="$(pwd)/.claude/skills"; AGENTS_DEST="$(pwd)/.claude/agents" ;;
  agents)  SKILLS_DEST="$(pwd)/.agents/skills"; AGENTS_DEST="$(pwd)/.agents/agents" ;;
  dir)     SKILLS_DEST="$CUSTOM_DIR/skills"; AGENTS_DEST="$CUSTOM_DIR/agents" ;;
esac
mkdir -p "$SKILLS_DEST" "$AGENTS_DEST"

# --- 3) copiar skills y agentes (no requiere python/node) ---
SK=0
for d in "$SRC"/skills/*/; do
  [ -f "$d/SKILL.md" ] || continue
  name="$(basename "$d")"; rm -rf "$SKILLS_DEST/$name"; cp -R "$d" "$SKILLS_DEST/$name"; SK=$((SK+1))
done
AG=0
for f in "$SRC"/agents/*.md; do [ -f "$f" ] || continue; cp "$f" "$AGENTS_DEST/"; AG=$((AG+1)); done

say ""
ok "Instaladas ${SK} skills en ${SKILLS_DEST}"
ok "Instalados ${AG} agentes en ${AGENTS_DEST}"

# --- 4) chequeo OPCIONAL de runtime para los scripts (nunca falla) ---
say ""
say "${DIM}Scripts (aceleradores opcionales — las skills funcionan sin esto):${RST}"
if command -v uv >/dev/null 2>&1; then
  ok "uv detectado — los scripts corren con 'uv run' sin instalar nada."
elif command -v python3 >/dev/null 2>&1; then
  ok "python3 detectado — para los scripts con dependencias: 'pip install requests beautifulsoup4' (o instalá uv)."
else
  warn "No hay Python ni uv. Las skills funcionan igual (modo manual); los scripts no correrán."
  warn "Si querés los scripts: instalá uv → https://astral.sh/uv (un binario, trae Python)."
fi

say ""
say "${GREEN}Listo.${RST} Reiniciá Claude Code y escribí \"/\" (por ejemplo /brief-de-contenido)."
say "${DIM}Datos en vivo opcionales (SerpApi gratis / GSC / Ahrefs): ver MCP-SETUP.md.${RST}"
