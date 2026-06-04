#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["requests"]
# ///
"""
set_key.py — Guarda tu clave de SerpApi (u otra variable) en ~/.claude/seo-skills.env
para que TODAS las SEO skills/scripts la usen automáticamente en cada sesión, sin
re-exportarla. Opcionalmente la valida contra SerpApi sin gastar búsquedas.

Qué hace (determinista):
  1. Escribe/actualiza la variable en ~/.claude/seo-skills.env (formato KEY=valor),
     conservando las demás líneas. Permisos 600 (solo tu usuario).
  2. NO imprime la clave completa: la enmascara (solo últimos 4 chars).
  3. Con --test: consulta https://serpapi.com/account (no consume créditos de
     búsqueda) y reporta si la clave es válida y los créditos restantes.

Los scripts que usan SerpApi (serp.py, expand_keywords.py, serp_outline.py,
ai_features.py) cargan este archivo solos antes de leer SERPAPI_API_KEY.

Uso:
  python3 set_key.py --key TU_CLAVE_SERPAPI
  python3 set_key.py --key TU_CLAVE_SERPAPI --test
  echo "TU_CLAVE" | python3 set_key.py --key -            # por stdin (evita dejarla en el historial)
  python3 set_key.py --key TU_CLAVE --var OTRA_VARIABLE

Salida (JSON a stdout):
  {"ok": true, "path": "...", "var": "SERPAPI_API_KEY", "masked": "…ab12",
   "test": {"valid": true, "plan_searches_left": N} | null}
  o: {"ok": false, "reason": "..."}

Deps: stdlib (requests solo si usas --test).
"""
import argparse
import json
import os
import sys

ENV_PATH = os.path.expanduser("~/.claude/seo-skills.env")


def out(obj):
    print(json.dumps(obj, ensure_ascii=False))
    sys.exit(0)


def mask(v):
    v = v.strip()
    return ("…" + v[-4:]) if len(v) > 4 else "…"


def write_var(path, var, value):
    lines = []
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            lines = f.read().splitlines()
    out_lines, replaced = [], False
    for ln in lines:
        if ln.strip().startswith(f"{var}=") or ln.strip().startswith(f"{var} ="):
            out_lines.append(f"{var}={value}")
            replaced = True
        else:
            out_lines.append(ln)
    if not replaced:
        out_lines.append(f"{var}={value}")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines) + "\n")
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass


def test_key(value):
    try:
        import requests  # noqa: PLC0415
    except ImportError:
        return {"valid": None, "note": "no se pudo validar: falta 'requests'"}
    try:
        r = requests.get("https://serpapi.com/account", params={"api_key": value}, timeout=20)
        if r.status_code == 401:
            return {"valid": False, "note": "401: clave inválida"}
        r.raise_for_status()
        data = r.json()
        return {
            "valid": True,
            "plan_searches_left": data.get("plan_searches_left"),
            "total_searches_left": data.get("total_searches_left"),
        }
    except Exception as e:  # noqa: BLE001
        return {"valid": None, "note": f"no se pudo validar: {e}"}


def main():
    ap = argparse.ArgumentParser(
        description="Guarda una clave (p.ej. SERPAPI_API_KEY) en ~/.claude/seo-skills.env.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Ejemplo:\n  uv run set_key.py --key TU_CLAVE --test',
    )
    ap.add_argument("--key", required=True, help="La clave. Usa '-' para leerla por stdin.")
    ap.add_argument("--var", default="SERPAPI_API_KEY", help="Nombre de la variable (default SERPAPI_API_KEY).")
    ap.add_argument("--test", action="store_true", help="Valida la clave contra SerpApi (no gasta búsquedas).")
    args = ap.parse_args()

    value = sys.stdin.read().strip() if args.key == "-" else args.key.strip()
    if not value:
        out({"ok": False, "reason": "clave vacía"})

    write_var(ENV_PATH, args.var, value)
    result = {"ok": True, "path": ENV_PATH, "var": args.var, "masked": mask(value), "test": None}
    if args.test and args.var == "SERPAPI_API_KEY":
        result["test"] = test_key(value)
    out(result)


if __name__ == "__main__":
    main()
