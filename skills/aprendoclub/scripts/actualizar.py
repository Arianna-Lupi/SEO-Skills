#!/usr/bin/env python3
"""actualizar.py: compara la versión instalada de las SEO Skills con la última publicada.

Solo stdlib, Python 3.9+. NO actualiza nada: informa y devuelve el comando exacto. La actualización
la ejecuta quien corre `/aprendoclub update` después de que el usuario diga que sí.

Uso (vía el lanzador: aprendoclub-run --update-check):
  actualizar.py --check            Consulta la última versión (usa red, a petición del usuario).
  actualizar.py --check --offline  Solo muestra lo instalado, sin tocar la red.
  actualizar.py --aviso            Aviso de UNA línea al iniciar /aprendoclub. Solo corre si el
                                   usuario lo activó en ~/.claude/aprendoclub/config.json
                                   ({"avisar_actualizaciones": true}); máximo una consulta al día;
                                   nunca falla ni bloquea.

Salida JSON (--check):
  {"ok": true, "instalada": "1.3.0", "disponible": "1.4.0", "hay_novedad": true,
   "conexion": true, "modo_instalacion": "instalador|plugin|desconocido",
   "novedades": [{"version": "1.4.0", "fecha": "...", "puntos": ["..."]}],
   "comando_actualizar": {...}, "conservado": [...]}
Si no hay conexión: "conexion": false y un mensaje; ok sigue siendo true (no es un error).
Variables: SEO_SKILLS_REF (rama, por defecto main), APRENDOCLUB_HOME.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILLS_ROOT = HERE.parent.parent
REPO = "Arianna-Lupi/SEO-Skills"
REF = os.environ.get("SEO_SKILLS_REF", "main")
RAW = f"https://raw.githubusercontent.com/{REPO}/{REF}"
HOME_DIR = Path(os.environ.get("APRENDOCLUB_HOME") or os.path.expanduser("~/.claude/aprendoclub"))

COMANDOS = {
    "macos_linux": f"curl -fsSL {RAW}/install.sh | bash",
    "windows": f"irm {RAW}/install.ps1 | iex",
    "plugin": "/plugin update seo-skills@aprendoseo",
}
CONSERVADO = [
    "~/.claude/seo-skills.env (tus claves)",
    ".seo-audit/ (datos de tus proyectos)",
    "cualquier skill o agente que hayas creado tú",
    "las skills que hayas modificado a mano se copian a un respaldo antes de sobrescribir",
]


def vtuple(v: str) -> tuple:
    return tuple(int(x) for x in re.findall(r"\d+", v)[:3]) or (0,)


def installed_version() -> tuple[str, str]:
    """(versión, modo) según dónde viva esta skill."""
    marker = SKILLS_ROOT / ".seo-skills-version"
    if marker.exists():
        return marker.read_text(encoding="utf-8").strip().splitlines()[0].strip(), "instalador"
    plugin = SKILLS_ROOT.parent / ".claude-plugin" / "plugin.json"
    if plugin.exists():
        try:
            return json.loads(plugin.read_text(encoding="utf-8")).get("version", ""), "plugin"
        except ValueError:
            pass
    version_file = SKILLS_ROOT.parent / "VERSION"
    if version_file.exists():  # corriendo desde un clon del repo
        return version_file.read_text(encoding="utf-8").strip().splitlines()[0].strip(), "desconocido"
    return "", "desconocido"


def fetch(url: str, timeout: float = 8.0) -> str | None:
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "aprendoclub-update"}), timeout=timeout) as r:
            return r.read().decode("utf-8", "replace")
    except (urllib.error.URLError, OSError, ValueError):
        return None


def parse_changelog(text: str) -> list[dict]:
    """Secciones `## [1.4.0] - 2026-10-26` con sus viñetas. Ignora 'Próxima versión'."""
    out, cur = [], None
    for line in text.splitlines():
        m = re.match(r"^##\s+\[?(\d+\.\d+\.\d+)\]?\s*(?:[-\u2013\u2014]\s*(\S.*))?$", line.strip())
        if m:
            cur = {"version": m.group(1), "fecha": (m.group(2) or "").strip(), "puntos": []}
            out.append(cur)
        elif line.startswith("## "):
            cur = None
        elif cur is not None and re.match(r"^\s*[-*]\s+", line):
            cur["puntos"].append(re.sub(r"^\s*[-*]\s+", "", line).strip())
    return out


def cmd_check(offline: bool) -> dict:
    inst, modo = installed_version()
    res = {"ok": True, "instalada": inst or None, "modo_instalacion": modo, "conexion": None,
           "comando_actualizar": COMANDOS["plugin"] if modo == "plugin" else
           {"macos_linux": COMANDOS["macos_linux"], "windows": COMANDOS["windows"]},
           "conservado": CONSERVADO}
    if not inst:
        res["mensaje"] = "No encontré la marca de versión. Si instalaste a mano, corre el instalador una vez para tenerla."
    if offline:
        res["conexion"] = None
        res["mensaje"] = res.get("mensaje") or "Modo sin red: solo se muestra la versión instalada."
        return res
    latest = fetch(f"{RAW}/VERSION")
    if latest is None:
        res["conexion"] = False
        res["mensaje"] = "No pude consultar la última versión (sin conexión o GitHub no responde). No es un error: vuelve a intentarlo luego."
        return res
    disp = latest.strip().splitlines()[0].strip() if latest.strip() else ""
    res["conexion"] = True
    res["disponible"] = disp
    res["hay_novedad"] = bool(inst and disp and vtuple(disp) > vtuple(inst))
    if res["hay_novedad"] or not inst:
        cl = fetch(f"{RAW}/CHANGELOG.md")
        secs = parse_changelog(cl) if cl else []
        res["novedades"] = [s for s in secs if vtuple(s["version"]) > vtuple(inst or "0.0.0")]
        if cl is None:
            res["mensaje_novedades"] = "No pude leer CHANGELOG.md; el resumen de novedades no está disponible."
    else:
        res["mensaje"] = "Estás al día."
    return res


def cmd_aviso() -> None:
    """Una línea o nada. Nunca lanza errores."""
    try:
        cfg = json.loads((HOME_DIR / "config.json").read_text(encoding="utf-8"))
        if not cfg.get("avisar_actualizaciones"):
            return
        stamp = HOME_DIR / "ultimo-aviso.txt"
        if stamp.exists() and time.time() - stamp.stat().st_mtime < 86400:
            return
        HOME_DIR.mkdir(parents=True, exist_ok=True)
        stamp.write_text(str(int(time.time())), encoding="utf-8")
        inst, _ = installed_version()
        latest = fetch(f"{RAW}/VERSION", timeout=3.0)
        if inst and latest and vtuple(latest.strip()) > vtuple(inst):
            print(f"Hay una versión nueva de las SEO Skills ({inst} a {latest.strip()}). Escribe /aprendoclub update para verla.")
    except Exception:  # noqa: BLE001
        return


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="compara versión instalada y última")
    ap.add_argument("--offline", action="store_true", help="con --check: no usa la red")
    ap.add_argument("--aviso", action="store_true", help="aviso de una línea (solo si el usuario lo activó)")
    ns = ap.parse_args()
    if ns.aviso:
        cmd_aviso()
        return
    if not ns.check:
        ap.print_help()
        return
    print(json.dumps(cmd_check(ns.offline), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
