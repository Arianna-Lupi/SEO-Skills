#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""
set_key.py, Guarda tu clave de SerpApi (u otra variable) en ~/.claude/seo-skills.env
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

Deps: solo stdlib (la validación usa urllib).
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
    import json as _json  # noqa: PLC0415
    import urllib.error  # noqa: PLC0415
    import urllib.parse  # noqa: PLC0415
    import urllib.request  # noqa: PLC0415
    url = "https://serpapi.com/account?" + urllib.parse.urlencode({"api_key": value})
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "seo-skills/1.1"}), timeout=20) as r:
            data = _json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return {"valid": False, "note": "401: clave inválida"}
        if e.code == 429:
            return {"valid": None, "note": "429: demasiadas consultas, reintenta en unos minutos"}
        return {"valid": None, "note": f"no se pudo validar: HTTP {e.code}"}
    except Exception as e:  # noqa: BLE001
        return {"valid": None, "note": f"no se pudo validar: {type(e).__name__}"}
    left = data.get("total_searches_left", data.get("plan_searches_left"))
    res = {"valid": True, "plan_searches_left": data.get("plan_searches_left"),
           "total_searches_left": data.get("total_searches_left")}
    if isinstance(left, int):
        if left <= 0:
            res["quota_warning"] = "Sin búsquedas disponibles: las skills pasan a modo manual hasta que se renueve el plan."
        elif left <= 10:
            res["quota_warning"] = f"Quedan {left} búsquedas: reserva las que quedan para keywords prioritarias (Duelo de Keywords, 10 de Oro)."
    return res


def load_saved(path, var):
    try:
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if line.startswith(var + "="):
                return line.split("=", 1)[1].strip().strip("'\"")
    except OSError:
        pass
    return None


def main():
    ap = argparse.ArgumentParser(
        description="Guarda una clave (p.ej. SERPAPI_API_KEY) en ~/.claude/seo-skills.env.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Ejemplo:\n  uv run set_key.py --key TU_CLAVE --test',
    )
    ap.add_argument("--key", help="La clave. Usa '-' para leerla por stdin. Omítela con --check-only.")
    ap.add_argument("--check-only", action="store_true", help="No guarda nada: valida la clave ya guardada y muestra la cuota.")
    ap.add_argument("--var", default="SERPAPI_API_KEY", help="Nombre de la variable (default SERPAPI_API_KEY).")
    ap.add_argument("--test", action="store_true", help="Valida la clave contra SerpApi (no gasta búsquedas).")
    args = ap.parse_args()

    if args.check_only:
        saved = load_saved(ENV_PATH, args.var)
        if not saved:
            out({"ok": False, "reason": f"no hay {args.var} guardada en {ENV_PATH}"})
        out({"ok": True, "path": ENV_PATH, "var": args.var, "masked": mask(saved), "test": test_key(saved)})
    if not args.key:
        out({"ok": False, "reason": "falta --key (o usa --check-only)"})
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
