#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["requests"]
# ///
"""
ai_features.py — Detecta features de IA/respuesta de una SERP (AEO/GEO) vía SerpApi.

Qué hace (determinista):
  Consulta SerpApi para una query y detecta si la SERP tiene AI Overview,
  featured snippet (y de qué tipo: párrafo, lista, tabla), answer box y PAA.
  Añade una recomendación basada en reglas para optimizar contenido (answer-
  first, listas, tablas, FAQ). Devuelve JSON compacto para que la skill
  GEO/AEO actúe sobre la señal, no sobre HTML.

Requisitos:
  - Env SERPAPI_API_KEY. Dep: requests (requirements.txt). Si falta clave/dep,
    degrada con {"ok": false, ...} y exit 0 (la skill sigue en modo manual).

Uso:
  SERPAPI_API_KEY=xxx python3 ai_features.py "qué es el seo"
  SERPAPI_API_KEY=xxx python3 ai_features.py "best crm software" --gl us --hl en

Salida (JSON a stdout):
  {
    "ok": true, "query": "...",
    "ai_overview": bool,
    "featured_snippet": {"present": bool, "type": "paragraph|list|table|null"},
    "paa": [...],
    "answer_box": bool,
    "recommendation": "..."
  }

Deps: requests.
"""

import argparse
import json
import os
import sys


def fail(reason, fallback):
    print(json.dumps({"ok": False, "reason": reason, "fallback": fallback}, ensure_ascii=False))
    sys.exit(0)


def classify_answer_box(ab):
    """Devuelve el tipo de featured snippet: list, table o paragraph."""
    if not isinstance(ab, dict):
        return None
    box_type = (ab.get("type") or "").lower()
    if "list" in box_type or ab.get("list"):
        return "list"
    if "table" in box_type or ab.get("table"):
        return "table"
    return "paragraph"


def build_recommendation(ai_overview, fs_present, fs_type, has_paa):
    parts = []
    if fs_present and fs_type == "list":
        parts.append("Hay featured snippet de lista → estructurá tu respuesta como lista numerada de N pasos/ítems, con frase-respuesta directa antes de la lista.")
    elif fs_present and fs_type == "table":
        parts.append("Hay featured snippet de tabla → incluí una tabla comparativa clara con encabezados de columna.")
    elif fs_present and fs_type == "paragraph":
        parts.append("Hay featured snippet de párrafo → respondé la pregunta en 40-55 palabras al inicio (answer-first), tono directo.")
    if ai_overview:
        parts.append("Hay AI Overview → reforzá E-E-A-T (autoría + fecha), datos citables y respuestas atómicas para que la IA te cite.")
    if has_paa:
        parts.append("Hay People Also Ask → convertí esas preguntas en H2/H3 literales con respuesta breve debajo de cada una.")
    if not parts:
        parts.append("SERP sin features de IA destacadas → igual aplicá answer-first y estructura por preguntas para captar futuros snippets.")
    return " ".join(parts)


def main():
    ap = argparse.ArgumentParser(
        description="Detecta features de IA/respuesta (AEO/GEO) de una SERP vía SerpApi.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Ejemplo:\n  uv run ai_features.py "qué es el seo" --gl es --hl es',
    )
    ap.add_argument("query", help="Consulta de búsqueda")
    ap.add_argument("--gl", default="es", help="País (gl), default 'es'")
    ap.add_argument("--hl", default="es", help="Idioma (hl), default 'es'")
    args = ap.parse_args()

    api_key = os.environ.get("SERPAPI_API_KEY")
    if not api_key:
        fail(
            "Falta SERPAPI_API_KEY en el entorno.",
            "modo manual: buscá la query en Google (incógnito) y verificá AI Overview / featured snippet / PAA a ojo, y validá en ChatGPT/Perplexity.",
        )

    try:
        import requests  # noqa: PLC0415
    except ImportError:
        fail(
            "Falta la dependencia 'requests' (pip install -r requirements.txt).",
            "modo manual: verificá las features de IA en el navegador.",
        )

    params = {"engine": "google", "q": args.query, "gl": args.gl, "hl": args.hl, "api_key": api_key}
    try:
        resp = requests.get("https://serpapi.com/search.json", params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:  # noqa: BLE001
        fail(f"Error de red/SerpApi: {e}", "modo manual: verificá las features en el navegador.")

    if data.get("error"):
        fail(f"SerpApi error: {data['error']}", "modo manual: verificá las features en el navegador.")

    ai_overview = "ai_overview" in data
    ab = data.get("answer_box")
    fs_present = ab is not None
    fs_type = classify_answer_box(ab)
    paa = [q.get("question") for q in (data.get("related_questions") or []) if q.get("question")]

    print(json.dumps({
        "ok": True,
        "query": args.query,
        "ai_overview": ai_overview,
        "featured_snippet": {"present": fs_present, "type": fs_type},
        "paa": paa,
        "answer_box": fs_present,
        "recommendation": build_recommendation(ai_overview, fs_present, fs_type, bool(paa)),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
