#!/usr/bin/env bash
#
# Instalador de las SEO Skills de aprendoseo ("De Cero a SEO").
# Funciona con Claude Code y otros clientes compatibles con Agent Skills
# (Cursor, VS Code, OpenAI Codex, GitHub Copilot).
#
# Uso rápido (un comando):
#   curl -fsSL https://raw.githubusercontent.com/Arianna-Lupi/SEO-Skills/main/install.sh | bash
#
# Flags (saltan el menú interactivo):
#   --client ID   cliente destino: claude | cursor | agents | codex | copilot
#                 (por defecto: claude)
#   --user        Claude Code, para tu usuario (~/.claude) [por defecto en claude]
#   --project     Claude Code, solo este proyecto (./.claude)
#   --dir RUTA    instala en una carpeta concreta (crea skills/ y agents/ dentro)
#   --with-uv     instala uv aunque no haya terminal interactiva (para los scripts)
#   --no-uv       no chequea ni ofrece uv
#   -h, --help    muestra esta ayuda
#
# Requisitos: bash y git. Python/uv son OPCIONALES (solo para los scripts; las
# skills funcionan sin ellos, en "modo manual"). Si dejás que el instalador
# configure uv, los scripts corren solos sin admin ni Python del sistema.
set -euo pipefail

REPO_URL="https://github.com/Arianna-Lupi/SEO-Skills.git"
UV_SH="https://astral.sh/uv/install.sh"

BLUE=""; GREEN=""; YELLOW=""; DIM=""; RST=""
if [ -t 1 ]; then BLUE=$'\033[34m'; GREEN=$'\033[32m'; YELLOW=$'\033[33m'; DIM=$'\033[2m'; RST=$'\033[0m'; fi
say()  { printf "%s\n" "$*"; }
ok()   { printf "%s✓%s %s\n" "$GREEN" "$RST" "$*"; }
warn() { printf "%s!%s %s\n" "$YELLOW" "$RST" "$*"; }

CLIENT=""; SCOPE=""; CUSTOM_DIR=""; UV_PREF=""   # UV_PREF: "" auto | force | skip
while [ $# -gt 0 ]; do
  case "$1" in
    --client) CLIENT="${2:-}"; shift 2 ;;
    --user) SCOPE="user"; shift ;;
    --project) SCOPE="project"; shift ;;
    --agents) CLIENT="agents"; shift ;;   # compat: antes era un destino
    --dir) SCOPE="dir"; CUSTOM_DIR="${2:-}"; shift 2 ;;
    --with-uv) UV_PREF="force"; shift ;;
    --no-uv) UV_PREF="skip"; shift ;;
    -h|--help) sed -n '2,28p' "$0"; exit 0 ;;
    *) echo "Opción desconocida: $1" >&2; exit 1 ;;
  esac
done

say ""
say "${BLUE}SEO Skills — aprendoseo (\"De Cero a SEO\")${RST}"
say "${DIM}13 skills + 3 agentes para Claude Code y clientes compatibles${RST}"
say ""

# --- 1) localizar la fuente; clonar a temp si corre vía curl|bash ---
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

# --- 2) elegir cliente (menú si es interactivo y no hubo flags de destino) ---
# Si pasaron --dir, manda --dir y no se pregunta nada.
if [ "$SCOPE" != "dir" ]; then
  if [ -z "$CLIENT" ]; then
    if [ -t 0 ]; then
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
      CLIENT="claude"   # piped (curl|bash, no TTY): por defecto Claude Code
    fi
  fi

  # Solo Claude Code distingue usuario vs proyecto.
  if [ "$CLIENT" = "claude" ] && [ -z "$SCOPE" ]; then
    if [ -t 0 ]; then
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

# --- 3) resolver carpetas destino según cliente ---
# AGENTS_DEST vacío = ese cliente no recibe agentes.
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
    *) echo "Cliente desconocido: $CLIENT (usá claude|cursor|agents|codex|copilot)" >&2; exit 1 ;;
  esac
fi

mkdir -p "$SKILLS_DEST"
[ -n "$AGENTS_DEST" ] && mkdir -p "$AGENTS_DEST"

# --- 4) copiar skills (todos los clientes) y agentes (solo Claude) ---
SK=0
for d in "$SRC"/skills/*/; do
  [ -f "$d/SKILL.md" ] || continue
  name="$(basename "$d")"; rm -rf "$SKILLS_DEST/$name"; cp -R "$d" "$SKILLS_DEST/$name"; SK=$((SK+1))
done
AG=0
if [ -n "$AGENTS_DEST" ]; then
  for f in "$SRC"/agents/*.md; do [ -f "$f" ] || continue; cp "$f" "$AGENTS_DEST/"; AG=$((AG+1)); done
fi

say ""
ok "Instaladas ${SK} skills en ${SKILLS_DEST}"
if [ -n "$AGENTS_DEST" ]; then
  ok "Instalados ${AG} agentes en ${AGENTS_DEST}"
else
  warn "Los subagentes son exclusivos de Claude Code; no se instalan en '${CLIENT}'. Las skills funcionan igual."
fi

# --- 5) runtime para los scripts: detectar / ofrecer uv (nunca falla) ---
say ""
say "${DIM}Scripts (aceleradores opcionales — las skills funcionan sin esto):${RST}"
UV_JUST_INSTALLED=0
if [ "$UV_PREF" = "skip" ]; then
  say "${DIM}Chequeo de uv omitido (--no-uv).${RST}"
elif command -v uv >/dev/null 2>&1; then
  ok "uv detectado — los scripts corren con 'uv run' sin instalar nada."
else
  install_uv() {
    if command -v curl >/dev/null 2>&1; then
      curl -LsSf "$UV_SH" | sh && UV_JUST_INSTALLED=1
    elif command -v wget >/dev/null 2>&1; then
      wget -qO- "$UV_SH" | sh && UV_JUST_INSTALLED=1
    else
      warn "No hay curl ni wget para instalar uv. Instalalo a mano: curl -LsSf $UV_SH | sh"
    fi
  }
  if [ "$UV_PREF" = "force" ]; then
    say "Instalando uv…"; install_uv || true
  elif [ -t 0 ]; then
    printf "¿Instalar uv para que los scripts corran solos? [S/n]: "
    read -r ans </dev/tty || ans="s"
    case "${ans:-s}" in
      [nN]*) say "${DIM}Saltado. Para instalarlo luego: curl -LsSf $UV_SH | sh${RST}" ;;
      *) say "Instalando uv…"; install_uv || true ;;
    esac
  else
    # piped, sin --with-uv: no instalamos software en silencio; mostramos el comando.
    if command -v python3 >/dev/null 2>&1; then
      ok "python3 detectado — para scripts con dependencias: 'pip install requests beautifulsoup4'."
    fi
    warn "Para que los scripts corran solos, instalá uv (un binario, sin admin, trae Python):"
    say  "    curl -LsSf $UV_SH | sh"
  fi
  if [ "$UV_JUST_INSTALLED" = "1" ]; then
    ok "uv instalado."
    warn "Quizás necesités abrir una terminal nueva para que 'uv' quede en el PATH."
  fi
fi

say ""
say "${GREEN}Listo.${RST} Reiniciá tu cliente y escribí \"/\" (por ejemplo /brief-de-contenido)."
say "${DIM}Datos en vivo opcionales (SerpApi gratis / GSC / Ahrefs): ver MCP-SETUP.md.${RST}"
