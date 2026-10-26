#!/usr/bin/env python3
"""publicar_version.py: prepara una versión nueva de las SEO Skills para anunciarla a los alumnos.

Hace, en este orden (todo local, sin red):
  1. Sube la versión en VERSION, .claude-plugin/plugin.json y .claude-plugin/marketplace.json.
  2. Convierte la sección "## Próxima versión" de CHANGELOG.md en "## [X.Y.Z] - fecha".
     Si esa sección está vacía, propone borradores desde docs/changelog-fragments/ (para que los revises).
  3. Escribe docs/ANUNCIO-ACTUALIZACION.md: texto listo para pegar en la comunidad, con 3 a 6 viñetas
     y el comando exacto de actualización para macOS/Linux, Windows y plugin.
  4. Imprime los pasos de git para que decidas tú. NO hace commit, tag ni push.

Uso:
  python3 scripts/publicar_version.py --bump minor            # 1.3.0 -> 1.4.0
  python3 scripts/publicar_version.py --version 1.4.0
  python3 scripts/publicar_version.py --bump patch --dry-run  # muestra qué haría, sin escribir
  python3 scripts/publicar_version.py --bump minor --root /ruta/a/copia  # opera sobre otra carpeta (pruebas)

Solo stdlib, Python 3.9+.
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

REPO = "Arianna-Lupi/SEO-Skills"
RAW = f"https://raw.githubusercontent.com/{REPO}/main"


def bump(cur: str, kind: str) -> str:
    major, minor, patch = (int(x) for x in cur.split("."))
    if kind == "major":
        return f"{major + 1}.0.0"
    if kind == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


def section_bullets(text: str, heading_re: str) -> tuple[list[str], re.Match | None]:
    m = re.search(rf"^##\s+{heading_re}\s*$", text, re.M)
    if not m:
        return [], None
    rest = text[m.end():]
    nxt = re.search(r"^##\s", rest, re.M)
    body = rest[: nxt.start()] if nxt else rest
    return [re.sub(r"^\s*[-*]\s+", "", ln).strip() for ln in body.splitlines() if re.match(r"^\s*[-*]\s+", ln)], m


def fragment_drafts(root: Path) -> list[str]:
    out = []
    for f in sorted((root / "docs" / "changelog-fragments").glob("*.md")):
        first = f.read_text(encoding="utf-8").splitlines()[:1]
        title = re.sub(r"^#\s*", "", first[0]).strip() if first else f.stem
        out.append(f"(borrador, reescribe en lenguaje de alumno) {title}")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--version", help="versión nueva, por ejemplo 1.4.0")
    g.add_argument("--bump", choices=["major", "minor", "patch"], help="sube la versión actual")
    ap.add_argument("--fecha", default=datetime.date.today().isoformat(), help="fecha de la versión (AAAA-MM-DD)")
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent), help="raíz del repo")
    ap.add_argument("--dry-run", action="store_true", help="no escribe nada, solo muestra el resultado")
    ns = ap.parse_args()

    root = Path(ns.root)
    vfile = root / "VERSION"
    cur = vfile.read_text(encoding="utf-8").strip()
    new = ns.version or bump(cur, ns.bump)
    if not re.fullmatch(r"\d+\.\d+\.\d+", new):
        print(f"Versión inválida: {new}", file=sys.stderr)
        return 1
    if tuple(map(int, new.split("."))) <= tuple(map(int, cur.split("."))):
        print(f"La versión nueva ({new}) debe ser mayor que la actual ({cur}).", file=sys.stderr)
        return 1

    cl_path = root / "CHANGELOG.md"
    cl = cl_path.read_text(encoding="utf-8") if cl_path.exists() else "# Novedades\n\n## Próxima versión\n"
    bullets, m = section_bullets(cl, r"Pr[óo]xima versi[óo]n")
    usó_borradores = False
    if not bullets:
        bullets = fragment_drafts(root)
        usó_borradores = True
    if m:
        cl_new = cl[: m.start()] + f"## Próxima versión\n\n## [{new}] - {ns.fecha}" + cl[m.end():]
    else:
        cl_new = cl + f"\n## [{new}] - {ns.fecha}\n"
    if usó_borradores and bullets:
        cl_new = cl_new.replace(f"## [{new}] - {ns.fecha}", f"## [{new}] - {ns.fecha}\n\n" + "\n".join(f"- {b}" for b in bullets), 1)

    pts = bullets[:6]
    anuncio = f"""# Anuncio de actualización: SEO Skills {new}

Texto listo para pegar en la comunidad. Revisa las viñetas antes de publicar.

---

Actualicé las SEO Skills a la versión {new}.

**Qué hay de nuevo**

{chr(10).join(f"- {p}" for p in pts) if pts else "- (completa las novedades en CHANGELOG.md y vuelve a correr este script)"}

**Cómo actualizar (un solo paso)**

- macOS y Linux: pega esto en la terminal.

```bash
curl -fsSL {RAW}/install.sh | bash
```

- Windows (PowerShell):

```powershell
irm {RAW}/install.ps1 | iex
```

- Si las instalaste como plugin de Claude Code:

```
/plugin update seo-skills@aprendoseo
```

Reinicia Claude Code cuando termine. Tus claves (`~/.claude/seo-skills.env`) y tus carpetas `.seo-audit/` no se tocan. Si habías modificado una skill a mano, el instalador guarda una copia antes de actualizar.

**Cómo ver si quedó bien**

Escribe `/aprendoclub update --check`. Te dice qué versión tienes y si estás al día.
"""
    changes = [f"VERSION: {cur} -> {new}", ".claude-plugin/plugin.json: version", ".claude-plugin/marketplace.json: version",
               f"CHANGELOG.md: 'Próxima versión' pasa a [{new}] - {ns.fecha}", "docs/ANUNCIO-ACTUALIZACION.md: texto para la comunidad"]
    if not ns.dry_run:
        vfile.write_text(new + "\n", encoding="utf-8")
        for rel in (".claude-plugin/plugin.json", ".claude-plugin/marketplace.json"):
            p = root / rel
            if not p.exists():
                continue
            data = json.loads(p.read_text(encoding="utf-8"))
            if "version" in data:
                data["version"] = new
            for plug in data.get("plugins", []):
                plug["version"] = new
            p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        cl_path.write_text(cl_new, encoding="utf-8")
        (root / "docs").mkdir(exist_ok=True)
        (root / "docs" / "ANUNCIO-ACTUALIZACION.md").write_text(anuncio, encoding="utf-8")
    print(("(simulacro) " if ns.dry_run else "") + f"Versión {cur} -> {new}")
    for c in changes:
        print("  -", c)
    if usó_borradores:
        print("\nAviso: 'Próxima versión' estaba vacía; usé los fragmentos como borrador. Reescríbelos en CHANGELOG.md (lenguaje de alumno) y vuelve a correr.")
    print(f"""
Pasos siguientes (no los hice yo; decide tú):
  1. Revisa los cambios:        git diff
  2. Valida el repo:            python3 scripts/validar_skills.py && python3 -m unittest discover tests
  3. Haz el commit:             git add -A && git commit -m "release: v{new}"
  4. Pasa a main y publica:     git checkout main && git merge develop && git push origin main
  5. (Opcional) Etiqueta:       git tag v{new} && git push origin v{new}
  6. Pega docs/ANUNCIO-ACTUALIZACION.md en la comunidad.""")
    return 0


if __name__ == "__main__":
    sys.exit(main())
