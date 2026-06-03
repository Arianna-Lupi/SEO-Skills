#!/usr/bin/env bash
#
# Instalador de las SEO Skills de aprendoseo ("De Cero a SEO") para Claude Code.
# Copia las skills y los agentes a tu Claude Code para que aparezcan con "/".
#
# Uso rápido (un comando, sin clonar nada):
#   curl -fsSL https://raw.githubusercontent.com/Arianna-Lupi/SEO-Skills/main/install.sh | bash
#
# O si ya clonaste el repo:
#   ./install.sh                 # instala para tu usuario (~/.claude) — todos tus proyectos
#   ./install.sh --project       # instala solo en el proyecto actual (./.claude)
#   ./install.sh --dir /ruta     # instala en una carpeta .claude concreta
#
set -euo pipefail

REPO_URL="https://github.com/Arianna-Lupi/SEO-Skills.git"

# --- parse args ---
SCOPE="user"
CUSTOM_DIR=""
while [ $# -gt 0 ]; do
  case "$1" in
    --project) SCOPE="project"; shift ;;
    --dir) CUSTOM_DIR="${2:-}"; shift 2 ;;
    -h|--help)
      sed -n '2,18p' "$0" 2>/dev/null || echo "Ver el README para opciones."
      exit 0 ;;
    *) echo "Opción desconocida: $1" >&2; exit 1 ;;
  esac
done

# --- locate the source (clone if running via curl|bash) ---
SRC=""
SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd || true)"
if [ -n "$SELF_DIR" ] && [ -d "$SELF_DIR/skills" ]; then
  SRC="$SELF_DIR"
else
  command -v git >/dev/null 2>&1 || { echo "Necesitás git instalado." >&2; exit 1; }
  TMP="$(mktemp -d)"
  trap 'rm -rf "$TMP"' EXIT
  echo "Descargando SEO-Skills…"
  git clone --depth 1 "$REPO_URL" "$TMP/SEO-Skills" >/dev/null 2>&1
  SRC="$TMP/SEO-Skills"
fi

[ -d "$SRC/skills" ] || { echo "No encontré la carpeta skills/ en $SRC" >&2; exit 1; }

# --- choose destination ---
if [ -n "$CUSTOM_DIR" ]; then
  DEST="$CUSTOM_DIR"
elif [ "$SCOPE" = "project" ]; then
  DEST="$(pwd)/.claude"
else
  DEST="$HOME/.claude"
fi

mkdir -p "$DEST/skills" "$DEST/agents"

# --- copy skills (cada carpeta con su SKILL.md, scripts y references) ---
SKILL_COUNT=0
for d in "$SRC"/skills/*/; do
  [ -f "$d/SKILL.md" ] || continue
  name="$(basename "$d")"
  rm -rf "$DEST/skills/$name"
  cp -R "$d" "$DEST/skills/$name"
  SKILL_COUNT=$((SKILL_COUNT + 1))
done

# --- copy agents ---
AGENT_COUNT=0
if [ -d "$SRC/agents" ]; then
  for f in "$SRC"/agents/*.md; do
    [ -f "$f" ] || continue
    cp "$f" "$DEST/agents/"
    AGENT_COUNT=$((AGENT_COUNT + 1))
  done
fi

echo ""
echo "Listo. Instaladas $SKILL_COUNT skills y $AGENT_COUNT agentes en:"
echo "  $DEST/skills/"
echo "  $DEST/agents/"
echo ""
echo "Reiniciá Claude Code y escribí \"/\" para verlas (p.ej. /brief-de-contenido)."
echo ""
echo "Opcional (datos en vivo): conectá SerpApi / GSC / Ahrefs — ver MCP-SETUP.md."
echo "Opcional (scripts): instalá uv (https://astral.sh/uv) para correr los scripts"
echo "con 'uv run' sin instalar dependencias, o 'pip install -r requirements.txt'."
