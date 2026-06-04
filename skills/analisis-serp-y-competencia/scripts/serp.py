#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["requests"]
# ///
"""
serp.py — Captura determinista de una SERP de Google vía SerpApi (REST).

Qué hace:
  Consulta https://serpapi.com/search.json con una query y devuelve un JSON
  COMPACTO con el top orgánico, People Also Ask (PAA), búsquedas relacionadas
  y qué features de SERP están presentes (AI Overview, featured snippet,
  knowledge panel). Así la skill razona sobre datos limpios, no sobre HTML.

Requisitos:
  - Env SERPAPI_API_KEY con tu clave de SerpApi.
  - Dep: requests (en requirements.txt). Si falta clave o dep, degrada con un
    JSON {"ok": false, ...} y exit 0 (la skill sigue en modo manual).

Uso:
  SERPAPI_API_KEY=xxx python3 serp.py "mejores zapatillas running"
  SERPAPI_API_KEY=xxx python3 serp.py "best running shoes" --gl us --hl en
  python3 serp.py "curso seo" --gl ar --hl es --num 10

Salida (JSON a stdout):
  {
    "ok": true, "query": "...",
    "top": [{"position","title","link","snippet"}, ...],
    "paa": ["pregunta?", ...],
    "related": ["búsqueda relacionada", ...],
    "features": {"ai_overview": bool, "featured_snippet": bool, "knowledge_panel": bool}
  }

Deps: requests.
"""

import argparse
import json
import os
import sys


def log(msg):
    print(msg, file=sys.stderr)


def fail(reason, fallback):
    print(json.dumps({"ok": False, "reason": reason, "fallback": fallback}, ensure_ascii=False))
    sys.exit(0)


def main():
    ap = argparse.ArgumentParser(
        description="Captura una SERP vía SerpApi y la devuelve compacta en JSON.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Ejemplo:\n  uv run serp.py "agencia seo madrid" --gl es --hl es --num 10',
    )
    ap.add_argument("query", help="Consulta de búsqueda")
    ap.add_argument("--gl", default="es", help="País (gl), default 'es'")
    ap.add_argument("--hl", default="es", help="Idioma (hl), default 'es'")
    ap.add_argument("--num", type=int, default=10, help="Nº de resultados orgánicos a devolver (default 10)")
    args = ap.parse_args()

    api_key = os.environ.get("SERPAPI_API_KEY")
    if not api_key:
        fail(
            "Falta SERPAPI_API_KEY en el entorno.",
            "modo manual: busca la query en Google en incógnito (región correcta) y anota top 10, PAA y features a mano.",
        )

    try:
        import requests  # noqa: PLC0415
    except ImportError:
        fail(
            "Falta la dependencia 'requests' (pip install -r requirements.txt).",
            "modo manual: revisa la SERP en el navegador en incógnito.",
        )

    params = {
        "engine": "google",
        "q": args.query,
        "gl": args.gl,
        "hl": args.hl,
        "num": args.num,
        "api_key": api_key,
    }
    try:
        resp = requests.get("https://serpapi.com/search.json", params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:  # noqa: BLE001
        fail(
            f"Error de red/SerpApi: {e}",
            "modo manual: revisa la SERP en el navegador en incógnito.",
        )

    if data.get("error"):
        fail(f"SerpApi devolvió error: {data['error']}", "modo manual: revisa la SERP en el navegador.")

    organic = data.get("organic_results", []) or []
    top = [
        {
            "position": r.get("position"),
            "title": r.get("title"),
            "link": r.get("link"),
            "snippet": r.get("snippet"),
        }
        for r in organic[: args.num]
    ]

    paa = [q.get("question") for q in (data.get("related_questions") or []) if q.get("question")]
    related = [r.get("query") for r in (data.get("related_searches") or []) if r.get("query")]

    features = {
        "ai_overview": "ai_overview" in data,
        "featured_snippet": "answer_box" in data,
        "knowledge_panel": "knowledge_graph" in data,
    }

    print(json.dumps({
        "ok": True,
        "query": args.query,
        "top": top,
        "paa": paa,
        "related": related,
        "features": features,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
