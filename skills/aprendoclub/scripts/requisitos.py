#!/usr/bin/env python3
"""requisitos.py: preflight de dependencias, claves y herramientas de los scripts de las SEO Skills.

Lo invoca el lanzador `aprendoclub-run` (bash o PowerShell). Solo stdlib, Python 3.9+.
La fuente de verdad es `requisitos.json` (al lado de la carpeta scripts/): por script, sus
paquetes de Python, claves de entorno, herramientas externas y el modo manual alternativo.

Comandos (vía el lanzador):
  aprendoclub-run --check <script>        ¿puedo correr este script? Devuelve JSON con `needs`.
  aprendoclub-run --check --all           Lo mismo para todos los scripts, sin repetidos.
  aprendoclub-run --status                Resumen para `/aprendoclub setup` (Python, uv, paquetes, claves, conectores).
  aprendoclub-run --install <script> --yes
                                          Instala SOLO los paquetes que faltan y están en el manifiesto,
                                          en un venv aislado (~/.claude/aprendoclub/.venv). Sin --yes
                                          solo muestra el plan. Nunca usa sudo ni instala globalmente.
  aprendoclub-run <script> [args...]      Preflight + ejecuta el script (con tus claves de
                                          ~/.claude/seo-skills.env). Si falta algo requerido, no corre.

<script> puede ser `serp.py`, `analisis-serp-y-competencia/serp.py` o una ruta al archivo.

Salida: JSON a stdout. Contrato unificado con los scripts:
  {"ok": true|false, "script": "...", "python": "...", "needs": [...],
   "reason": "...", "fallback": "..."}            (reason y fallback solo si ok es false)
Cada elemento de `needs`:
  {"type": "python_dep", "name": "requests", "required": true, "packages": ["requests"], "command": "..."}
  {"type": "api_key", "name": "SERPAPI_API_KEY", "required": false, "where": "...", "fallback": "...", "save": "..."}
  {"type": "tool", "name": "node", "required": false, "where": "...", "fallback": "..."}
`ok` es false solo si falta algo `required`. Las claves nunca se imprimen, solo si existen.

Variables: APRENDOCLUB_PYTHON (intérprete a usar), APRENDOCLUB_HOME (por defecto ~/.claude/aprendoclub),
APRENDOCLUB_REQUISITOS (ruta a otro manifiesto, para pruebas).
Códigos de salida: 0 normal; 3 cuando `run`/`--install` se detiene porque falta algo; el resto es el del script.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILLS_ROOT = HERE.parent.parent
MANIFEST = Path(os.environ.get("APRENDOCLUB_REQUISITOS") or HERE.parent / "requisitos.json")
ENV_FILE = Path(os.path.expanduser("~/.claude/seo-skills.env"))
HOME_DIR = Path(os.environ.get("APRENDOCLUB_HOME") or os.path.expanduser("~/.claude/aprendoclub"))
VENV = HOME_DIR / ".venv"
PY_MIN = (3, 9)


def emit(obj: dict, code: int = 0) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=2))
    sys.exit(code)


def load_manifest() -> dict:
    try:
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        emit({"ok": False, "reason": f"no pude leer el manifiesto {MANIFEST}: {exc}",
              "fallback": "reinstala las SEO Skills (install.sh) para restaurar requisitos.json",
              "needs": []}, 3)
        raise  # pragma: no cover


def read_env_file() -> dict:
    out = {}
    try:
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip().strip('"').strip("'")
    except OSError:
        pass
    return out


def key_state(name: str, file_env: dict) -> str | None:
    """Dónde está la clave ('entorno' o 'archivo'); None si falta. Nunca devuelve el valor."""
    if os.environ.get(name):
        return "entorno"
    if file_env.get(name):
        return "archivo"
    return None


def venv_python() -> Path | None:
    for rel in ("bin/python", "Scripts/python.exe"):
        p = VENV / rel
        if p.exists():
            return p
    return None


def missing_modules(py: str, mods: list[str]) -> list[str]:
    """Módulos que NO se pueden importar con el intérprete `py`."""
    if not mods:
        return []
    if os.path.realpath(py) == os.path.realpath(sys.executable):
        return [m for m in mods if importlib.util.find_spec(m) is None]
    code = ("import importlib.util,sys\n"
            "print(' '.join(m for m in sys.argv[1:] if importlib.util.find_spec(m) is None))")
    try:
        r = subprocess.run([py, "-c", code, *mods], capture_output=True, text=True, timeout=30)
        return r.stdout.split() if r.returncode == 0 else list(mods)
    except (OSError, subprocess.SubprocessError):
        return list(mods)


def resolve_script(man: dict, name: str) -> str | None:
    scripts = man.get("scripts", {})
    if name in scripts:
        return name
    p = Path(name)
    if p.exists():
        parts = p.resolve().parts
        if len(parts) >= 3 and parts[-2] == "scripts":
            cand = f"{parts[-3]}/{parts[-1]}"
            if cand in scripts:
                return cand
    base = [k for k in scripts if k.split("/")[-1] == Path(name).name]
    return base[0] if len(base) == 1 else None


def pip_for(man: dict, module: str) -> str:
    return man.get("paquetes", {}).get(module, {}).get("pip", module)


def pick_runtime(man: dict, req_mods: list[str]) -> tuple[str, list[str]]:
    """Elige el intérprete que correrá el script y devuelve (ruta, módulos requeridos que faltan)."""
    cands: list[str] = []
    if os.environ.get("APRENDOCLUB_PYTHON"):
        cands.append(os.environ["APRENDOCLUB_PYTHON"])
    cands.append(sys.executable)
    vp = venv_python()
    if vp:
        cands.append(str(vp))
    best, best_missing = cands[0], list(req_mods)
    for py in cands:
        miss = missing_modules(py, req_mods)
        if not miss:
            return py, []
        if len(miss) < len(best_missing):
            best, best_missing = py, miss
    return best, best_missing


def check_script(man: dict, key: str, file_env: dict) -> dict:
    spec = man["scripts"][key]
    needs: list[dict] = []
    req_mods = list(spec.get("python", []))
    opt_mods = list(spec.get("python_opcional", []))
    py, miss_req = pick_runtime(man, req_mods)
    miss_opt = missing_modules(py, opt_mods)
    for mods, required in ((miss_req, True), (miss_opt, False)):
        if mods:
            pkgs = sorted({pip_for(man, m) for m in mods})
            needs.append({
                "type": "python_dep", "name": ", ".join(pkgs), "required": required, "packages": pkgs,
                "command": f"aprendoclub-run --install {key} --yes",
                "detail": f"crea {VENV} y instala {' '.join(pkgs)} solo ahí (sin sudo, sin tocar el Python del sistema)",
                "fallback": spec.get("modo_manual", "modo manual"),
            })
    for name, level in sorted(spec.get("env", {}).items()):
        meta = man.get("claves", {}).get(name)
        if meta is None or key_state(name, file_env):
            continue
        needs.append({
            "type": "api_key", "name": name, "required": level == "requerida",
            "purpose": meta.get("para", ""), "where": meta.get("donde", ""),
            "fallback": meta.get("alternativa", spec.get("modo_manual", "modo manual")),
            "save": f"skill configurar-serpapi: set_key.py --key - --var {name} (la clave entra por stdin, nunca por argumento)",
        })
    for tool in spec.get("herramientas", []):
        meta = man.get("herramientas", {}).get(tool, {})
        cmds = meta.get("comandos", [tool])
        if any(shutil.which(c) for c in cmds):
            continue
        needs.append({
            "type": "tool", "name": tool, "required": meta.get("requerida_en", {}).get(key, False),
            "where": meta.get("donde", ""), "fallback": meta.get("alternativa", spec.get("modo_manual", "modo manual")),
        })
    blocking = [n for n in needs if n["required"]]
    res = {"ok": not blocking, "script": key, "python": py, "needs": needs}
    if blocking:
        res["reason"] = "faltan requisitos: " + ", ".join(n["name"] for n in blocking)
        res["fallback"] = spec.get("modo_manual", "modo manual")
    return res


def cmd_check(man: dict, target: str | None, all_: bool) -> None:
    file_env = read_env_file()
    if all_:
        results = [check_script(man, k, file_env) for k in sorted(man["scripts"])]
        merged: dict[tuple, dict] = {}
        for r in results:
            for n in r["needs"]:
                k2 = (n["type"], n["name"])
                cur = merged.setdefault(k2, dict(n, used_by=[]))
                cur["required"] = cur["required"] or n["required"]
                cur["used_by"].append(r["script"])
        needs = sorted(merged.values(), key=lambda n: (not n["required"], n["type"], n["name"]))
        emit({"ok": not any(n["required"] for n in needs), "scripts": len(results), "needs": needs})
    key = resolve_script(man, target or "")
    if not key:
        emit({"ok": False, "reason": f"el script '{target}' no está en requisitos.json (o el nombre es ambiguo: usa skill/script.py)",
              "fallback": "revisa el nombre con `ls skills/*/scripts`", "needs": []})
    emit(check_script(man, key, file_env))


def cmd_status(man: dict) -> None:
    file_env = read_env_file()
    py_ok = sys.version_info >= PY_MIN
    uv = shutil.which("uv")
    vp = venv_python()
    modules = sorted(man.get("paquetes", {}))
    rt = os.environ.get("APRENDOCLUB_PYTHON") or sys.executable
    pkg_state = {}
    for m in modules:
        in_sys = not missing_modules(sys.executable, [m])
        in_venv = bool(vp) and not missing_modules(str(vp), [m])
        pkg_state[pip_for(man, m)] = "disponible" if (in_sys or in_venv) else "falta"
    keys = {}
    for name, meta in sorted(man.get("claves", {}).items()):
        st = key_state(name, file_env)
        keys[name] = {"estado": st or "falta", "para": meta.get("para", ""), "donde": meta.get("donde", "")}
    tools = {}
    for name, meta in sorted(man.get("herramientas", {}).items()):
        found = [c for c in meta.get("comandos", [name]) if shutil.which(c)]
        tools[name] = {"estado": "disponible" if found else "falta", "donde": meta.get("donde", "")}
    conectores = [{"id": c["id"], "nombre": c["nombre"], "opcional": c.get("opcional", True),
                   "estado": "no detectable desde la terminal: revisa con /mcp en Claude Code",
                   "guia": c.get("guia", "MCP-SETUP.md"), "alternativa": c.get("alternativa", "")}
                  for c in man.get("conectores_mcp", [])]
    faltantes = []
    if not py_ok:
        faltantes.append({"type": "python", "name": f"Python {PY_MIN[0]}.{PY_MIN[1]}+", "required": False})
    faltantes += [{"type": "python_dep", "name": k, "required": False} for k, v in pkg_state.items() if v == "falta"]
    faltantes += [{"type": "api_key", "name": k, "required": False} for k, v in keys.items() if v["estado"] == "falta"]
    faltantes += [{"type": "tool", "name": k, "required": False} for k, v in tools.items() if v["estado"] == "falta"]
    emit({
        "ok": True,
        "python": {"ruta": rt, "version": ".".join(map(str, sys.version_info[:3])), "cumple_minimo": py_ok},
        "uv": {"ruta": uv or None},
        "venv": {"ruta": str(VENV), "existe": bool(vp)},
        "paquetes": pkg_state, "claves": keys, "herramientas": tools, "conectores_mcp": conectores,
        "needs": faltantes,
        "nota": "Todo lo que falta es opcional: sin eso, cada skill sigue en modo manual. Pregunta al usuario antes de instalar o guardar nada.",
    })


def cmd_install(man: dict, target: str, yes: bool, with_optional: bool) -> None:
    key = resolve_script(man, target)
    if not key:
        emit({"ok": False, "reason": f"el script '{target}' no está en requisitos.json", "needs": []}, 3)
    spec = man["scripts"][key]
    mods = list(spec.get("python", [])) + (list(spec.get("python_opcional", [])) if with_optional else [])
    py, _ = pick_runtime(man, [])
    miss = missing_modules(os.environ.get("APRENDOCLUB_PYTHON") or sys.executable, mods)
    vp = venv_python()
    if vp:
        miss = [m for m in miss if m in missing_modules(str(vp), [m])]
    if not miss:
        emit({"ok": True, "installed": [], "note": "no falta ningún paquete para este script"})
    pkgs = sorted({pip_for(man, m) for m in miss})
    allowed = {v.get("pip", k) for k, v in man.get("paquetes", {}).items()}
    if not set(pkgs) <= allowed:
        emit({"ok": False, "reason": "paquetes fuera del manifiesto; no instalo nada", "needs": []}, 3)
    uv = shutil.which("uv")
    base_py = os.environ.get("APRENDOCLUB_PYTHON") or sys.executable
    plan = {"venv": str(VENV), "packages": pkgs,
            "steps": ([f"uv venv {VENV}", f"uv pip install --python {VENV}/bin/python {' '.join(pkgs)}"] if uv else
                      [f"{base_py} -m venv {VENV}", f"{VENV}/bin/python -m pip install {' '.join(pkgs)}"])}
    if not yes:
        emit({"ok": False, "reason": "falta confirmación: pregunta al usuario y vuelve a correr con --yes", "plan": plan, "needs": []}, 3)
    HOME_DIR.mkdir(parents=True, exist_ok=True)
    try:
        if not venv_python():
            subprocess.run(["uv", "venv", str(VENV)] if uv else [base_py, "-m", "venv", str(VENV)],
                           check=True, capture_output=True, text=True, timeout=300)
        vp = venv_python()
        cmd = (["uv", "pip", "install", "--python", str(vp), *pkgs] if uv else [str(vp), "-m", "pip", "install", *pkgs])
        subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=600)
    except (OSError, subprocess.SubprocessError) as exc:
        detail = getattr(exc, "stderr", "") or str(exc)
        emit({"ok": False, "reason": f"la instalación falló: {detail.strip()[-300:]}",
              "fallback": spec.get("modo_manual", "modo manual"), "plan": plan, "needs": []}, 3)
    still = missing_modules(str(venv_python()), mods)
    emit({"ok": not still, "installed": pkgs, "venv": str(VENV), "still_missing": still, "needs": []})


def cmd_run(man: dict, target: str, args: list[str]) -> None:
    key = resolve_script(man, target)
    if not key:
        emit({"ok": False, "reason": f"el script '{target}' no está en requisitos.json (o es ambiguo: usa skill/script.py)",
              "fallback": "revisa el nombre con `ls skills/*/scripts`", "needs": []}, 3)
    file_env = read_env_file()
    res = check_script(man, key, file_env)
    if not res["ok"]:
        emit(res, 3)
    for n in res["needs"]:
        print(f"aviso: falta {n['name']} (opcional): {n.get('fallback', '')}", file=sys.stderr)
    skill, name = key.split("/")
    path = SKILLS_ROOT / skill / "scripts" / name
    if not path.exists():
        emit({"ok": False, "reason": f"no encuentro {path}", "needs": res["needs"]}, 3)
    env = dict(os.environ)
    for k, v in file_env.items():
        env.setdefault(k, v)
    sys.exit(subprocess.call([res["python"], str(path), *args], env=env))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="solo comprueba requisitos de un script (o --all)")
    ap.add_argument("--all", action="store_true", help="con --check: todos los scripts")
    ap.add_argument("--status", action="store_true", help="estado general para /aprendoclub setup")
    ap.add_argument("--install", action="store_true", help="instala en el venv aislado los paquetes que faltan")
    ap.add_argument("--yes", action="store_true", help="confirmación explícita del usuario para --install")
    ap.add_argument("--with-optional", action="store_true", help="con --install: incluye paquetes opcionales")
    ap.add_argument("script", nargs="?", help="script (serp.py, skill/script.py o ruta)")
    ap.add_argument("args", nargs=argparse.REMAINDER, help="argumentos para el script")
    ns = ap.parse_args()
    if ns.install or ns.check or ns.status:
        # argparse deja las banderas que van DESPUÉS del script dentro de `args`; aquí son nuestras.
        for flag, attr in (("--yes", "yes"), ("--with-optional", "with_optional"), ("--all", "all")):
            if flag in ns.args:
                setattr(ns, attr, True)
                ns.args = [a for a in ns.args if a != flag]
    man = load_manifest()
    if ns.status:
        cmd_status(man)
    if ns.check:
        cmd_check(man, ns.script, ns.all)
    if ns.install:
        if not ns.script:
            ap.error("--install necesita un script")
        cmd_install(man, ns.script, ns.yes, ns.with_optional)
    if not ns.script:
        ap.print_help()
        sys.exit(0)
    cmd_run(man, ns.script, ns.args)


if __name__ == "__main__":
    main()
