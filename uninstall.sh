#!/usr/bin/env bash
#
# Desinstalador de las SEO Skills de aprendoseo.
# Borra SOLO lo que el instalador registró en .seo-skills-manifest (skills y agentes).
# Si la instalación es antigua y no tiene manifiesto, descarga la lista de nombres del
# repo y borra únicamente esas carpetas. No toca nada más de tu carpeta de skills.
#
# Uso:
#   curl -fsSL https://raw.githubusercontent.com/Arianna-Lupi/SEO-Skills/main/uninstall.sh | bash
#
# Flags (mismos que install.sh):
#   --client ID   claude | cursor | agents | codex | copilot (por defecto: claude)
#   --user        Claude Code, tu usuario (~/.claude) [por defecto]
#   --project     Claude Code, solo este proyecto (./.claude)
#   --dir RUTA    carpeta concreta usada al instalar con --dir
#   --dry-run     muestra qué borraría, sin borrar nada
#   -h, --help    esta ayuda
#
# Si instalaste como plugin, usa en su lugar:
#   /plugin uninstall seo-skills@aprendoseo
#   /plugin marketplace remove aprendoseo
set -euo pipefail

REPO="Arianna-Lupi/SEO-Skills"
REF="${SEO_SKILLS_REF:-main}"
MARKER=".seo-skills-version"
MANIFEST=".seo-skills-manifest"

say()  { printf "%s\n" "$*"; }
warn() { printf "! %s\n" "$*"; }
die()  { printf "Error: %s\n" "$*" >&2; exit 1; }
usage() { sed -n '3,22p' "$0" 2>/dev/null | sed 's/^# \{0,1\}//'; }

CLIENT="claude"; SCOPE="user"; CUSTOM_DIR=""; DRY=0
while [ $# -gt 0 ]; do
  case "$1" in
    --client) [ -n "${2:-}" ] || die "--client necesita un valor"; CLIENT="$2"; shift 2 ;;
    --user) SCOPE="user"; shift ;;
    --project) SCOPE="project"; shift ;;
    --dir) [ -n "${2:-}" ] || die "--dir necesita una ruta"; SCOPE="dir"; CUSTOM_DIR="$2"; shift 2 ;;
    --dry-run) DRY=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Opción desconocida: $1" >&2; exit 1 ;;
  esac
done

AGENTS_DEST=""
if [ "$SCOPE" = "dir" ]; then
  SKILLS_DEST="$CUSTOM_DIR/skills"; AGENTS_DEST="$CUSTOM_DIR/agents"
else
  case "$CLIENT" in
    claude)
      if [ "$SCOPE" = "project" ]; then SKILLS_DEST="$(pwd)/.claude/skills"; AGENTS_DEST="$(pwd)/.claude/agents"
      else SKILLS_DEST="$HOME/.claude/skills"; AGENTS_DEST="$HOME/.claude/agents"; fi ;;
    cursor)  SKILLS_DEST="$(pwd)/.cursor/skills" ;;
    agents)  SKILLS_DEST="$(pwd)/.agents/skills" ;;
    codex)   SKILLS_DEST="$(pwd)/.codex/skills" ;;
    copilot) SKILLS_DEST="$(pwd)/.github/skills" ;;
    *) die "cliente desconocido: $CLIENT" ;;
  esac
fi

[ -d "$SKILLS_DEST" ] || { say "No hay carpeta de skills en $SKILLS_DEST. Nada que quitar."; exit 0; }
case "$SKILLS_DEST" in ""|"/"|"$HOME"|"$HOME/") die "ruta de skills sospechosa: '$SKILLS_DEST'";; esac

SKILL_NAMES=""; AGENT_PATHS=""
if [ -f "$SKILLS_DEST/$MANIFEST" ]; then
  SKILL_NAMES="$(awk '$1=="skill"{print $2}' "$SKILLS_DEST/$MANIFEST")"
  AGENT_PATHS="$(awk '$1=="agent"{ $1=""; $2=""; sub(/^  /,""); print }' "$SKILLS_DEST/$MANIFEST")"
else
  warn "No encontré $MANIFEST (instalación antigua). Descargo la lista de nombres del repo."
  TMP="$(mktemp -d)"; trap 'rm -rf -- "$TMP"' EXIT
  URL="https://codeload.github.com/${REPO}/tar.gz/${REF}"
  if command -v curl >/dev/null 2>&1; then curl -fsSL --max-time 60 -o "$TMP/p.tgz" "$URL" || die "no pude descargar la lista."
  elif command -v wget >/dev/null 2>&1; then wget -q -O "$TMP/p.tgz" "$URL" || die "no pude descargar la lista."
  else die "necesito curl o wget para obtener la lista de nombres."; fi
  LIST="$(tar -tzf "$TMP/p.tgz")"
  SKILL_NAMES="$(printf "%s\n" "$LIST" | awk -F/ 'NF>=4 && $2=="skills" && $4=="SKILL.md"{print $3}' | sort -u)"
  if [ -n "$AGENTS_DEST" ]; then
    AGENT_PATHS="$(printf "%s\n" "$LIST" | awk -F/ -v d="$AGENTS_DEST" 'NF==3 && $2=="agents" && $3 ~ /\.md$/{print d "/" $3}' | sort -u)"
  fi
fi

RS=0; RA=0
for name in $SKILL_NAMES; do
  case "$name" in */*|""|.|..) continue;; esac
  if [ -d "$SKILLS_DEST/$name" ]; then
    if [ "$DRY" = "1" ]; then say "  (simulacro) quitaría $SKILLS_DEST/$name"; else rm -rf -- "${SKILLS_DEST:?}/$name"; say "  Quitada: $SKILLS_DEST/$name"; fi
    RS=$((RS+1))
  fi
done
OLDIFS="$IFS"; IFS=$'\n'
for f in $AGENT_PATHS; do
  [ -f "$f" ] || continue
  if [ "$DRY" = "1" ]; then say "  (simulacro) quitaría $f"; else rm -f -- "$f"; say "  Quitado: $f"; fi
  RA=$((RA+1))
done
IFS="$OLDIFS"

if [ "$DRY" != "1" ]; then
  rm -f -- "$SKILLS_DEST/$MARKER" "$SKILLS_DEST/$MANIFEST"
  rmdir "$SKILLS_DEST" 2>/dev/null || true
  if [ -n "$AGENTS_DEST" ]; then rmdir "$AGENTS_DEST" 2>/dev/null || true; fi
fi

if [ "$RS" -eq 0 ] && [ "$RA" -eq 0 ]; then
  say "Nada que quitar: no parece que las SEO Skills estén instaladas en $SKILLS_DEST."
  say "Si las instalaste como plugin, usa /plugin uninstall seo-skills@aprendoseo."
else
  say "✓ Desinstaladas ${RS} skills y ${RA} agentes de aprendoseo."
fi
