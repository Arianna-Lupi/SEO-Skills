#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["requests"]
# ///
"""
expand_keywords.py — Expande semillas de keywords vía SerpApi (Autocomplete + Related/PAA).

Qué hace (determinista):
  1. Toma una o más semillas (--seed repetible) o un archivo (--file, una por línea).
  2. Por cada semilla consulta SerpApi:
       - engine=google_autocomplete → sugerencias de Google (método 2 del diploma).
       - engine=google → "related_searches" y "related_questions" (PAA).
  3. Deduplica candidatos y etiqueta su origen (autocomplete|related|paa).

NO devuelve volumen ni KD: esos datos reales vienen del MCP de Ahrefs
(keywords-explorer-overview), NO de este script. Esto solo genera ideas long-tail.

Uso:
  SERPAPI_API_KEY=... python3 expand_keywords.py --seed "rutina facial" --seed "serum vitamina c"
  SERPAPI_API_KEY=... python3 expand_keywords.py --file semillas.txt --gl es --hl es

Salida (JSON a stdout):
  {"ok": true, "seeds": [...], "candidates": [{"keyword","source"}], "count": N}
  o en error/sin clave:
  {"ok": false, "reason": "...", "fallback": "modo manual: ..."}

Deps: requests (ver requirements.txt). Sin requests o sin SERPAPI_API_KEY → ok:false, exit 0.
"""

import argparse
import json
import os
import sys

SERPAPI_URL = "https://serpapi.com/search.json"


def log(msg):
    print(msg, file=sys.stderr)


def out(obj):
    print(json.dumps(obj, ensure_ascii=False))
    sys.exit(0)


def read_seeds(args):
    seeds = list(args.seed or [])
    if args.file:
        try:
            with open(args.file, encoding="utf-8") as fh:
                for line in fh:
                    s = line.strip()
                    if s:
                        seeds.append(s)
        except OSError as e:
            out({"ok": False, "reason": f"no se pudo leer --file: {e}",
                 "fallback": "modo manual: pega las semillas con --seed"})
    # dedup preservando orden
    seen, uniq = set(), []
    for s in seeds:
        k = s.lower().strip()
        if k and k not in seen:
            seen.add(k)
            uniq.append(s.strip())
    return uniq


def serp_get(requests, params, key):
    params = dict(params)
    params["api_key"] = key
    try:
        r = requests.get(SERPAPI_URL, params=params, timeout=30)
        if r.status_code != 200:
            log(f"SerpApi HTTP {r.status_code} para {params.get('q')}")
            return None
        return r.json()
    except Exception as e:  # noqa: BLE001
        log(f"error SerpApi: {e}")
        return None


def main():
    ap = argparse.ArgumentParser(
        description="Expande semillas con SerpApi (autocomplete + related + PAA).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Ejemplo:\n  uv run expand_keywords.py --seed "seo" --seed "linkbuilding" --gl es --hl es',
    )
    ap.add_argument("--seed", action="append", help="semilla (repetible)")
    ap.add_argument("--file", help="archivo con una semilla por línea")
    ap.add_argument("--gl", default="es", help="país (geo), p.ej. es, mx, ar")
    ap.add_argument("--hl", default="es", help="idioma, p.ej. es")
    args = ap.parse_args()

    try:
        import requests  # noqa: F401
    except ImportError:
        out({"ok": False, "reason": "falta la dependencia 'requests'",
             "fallback": "modo manual: usa el MCP de SerpApi o pega sugerencias de Google Autocomplete a mano"})

    import requests

    key = os.environ.get("SERPAPI_API_KEY")
    if not key:
        out({"ok": False, "reason": "falta SERPAPI_API_KEY en el entorno",
             "fallback": "modo manual: usa mcp__serpapi__search o Google Autocomplete manualmente"})

    seeds = read_seeds(args)
    if not seeds:
        out({"ok": False, "reason": "no se dieron semillas",
             "fallback": "pasa --seed o --file"})

    seen = set()
    candidates = []

    def add(keyword, source):
        k = (keyword or "").strip()
        if not k:
            return
        low = k.lower()
        if low in seen:
            return
        seen.add(low)
        candidates.append({"keyword": k, "source": source})

    for seed in seeds:
        seen.add(seed.lower())  # no devolver la semilla como candidata

    for seed in seeds:
        # 1) Autocomplete
        ac = serp_get(requests, {"engine": "google_autocomplete", "q": seed, "gl": args.gl, "hl": args.hl}, key)
        if ac:
            for s in ac.get("suggestions", []) or []:
                add(s.get("value"), "autocomplete")
        # 2) Búsqueda normal → related_searches + related_questions (PAA)
        g = serp_get(requests, {"engine": "google", "q": seed, "gl": args.gl, "hl": args.hl}, key)
        if g:
            for rs in g.get("related_searches", []) or []:
                add(rs.get("query"), "related")
            for rq in g.get("related_questions", []) or []:
                add(rq.get("question"), "paa")

    out({"ok": True, "seeds": seeds, "candidates": candidates, "count": len(candidates)})


if __name__ == "__main__":
    main()
