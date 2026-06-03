#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["requests", "beautifulsoup4"]
# ///
"""
serp_outline.py — Extractor de esquemas (H1/H2/H3) de los competidores del top de la SERP.

Qué hace (determinista):
  1. Obtiene las URLs orgánicas del top N (vía SerpApi) — o usá --urls para
     pasar una lista y saltarte SerpApi.
  2. Descarga cada URL y extrae su estructura de encabezados H1/H2/H3.
  3. Junta los H2 más repetidos en un esquema sugerido y suma las preguntas
     del PAA. Devuelve todo COMPACTO en JSON para que el brief se base en la
     SERP real, no en HTML crudo.

Requisitos:
  - Para obtener URLs automáticamente: env SERPAPI_API_KEY. Alternativa sin
    clave: --urls "url1,url2,...".
  - Deps: requests + beautifulsoup4 (requirements.txt). Si falta algo, degrada
    con {"ok": false, ...} y exit 0 (la skill sigue en modo manual).

Uso:
  SERPAPI_API_KEY=xxx python3 serp_outline.py "cómo hacer un brief seo" --top 5 --gl es --hl es
  python3 serp_outline.py "cómo hacer un brief seo" --urls "https://a.com/x,https://b.com/y"

Salida (JSON a stdout):
  {
    "ok": true, "query": "...",
    "competitors": [{"url","h1","headings":["H2: ...","H3: ..."]}, ...],
    "common_questions": [...PAA...],
    "suggested_outline": [...H2 fusionados/ordenados por frecuencia...]
  }

Deps: requests, beautifulsoup4.
"""

import argparse
import json
import os
import re
import sys
from collections import Counter


def log(msg):
    print(msg, file=sys.stderr)


def fail(reason, fallback):
    print(json.dumps({"ok": False, "reason": reason, "fallback": fallback}, ensure_ascii=False))
    sys.exit(0)


def get_top_urls(query, top, gl, hl, requests):
    api_key = os.environ.get("SERPAPI_API_KEY")
    if not api_key:
        return None, "Falta SERPAPI_API_KEY y no se pasó --urls."
    params = {
        "engine": "google", "q": query, "gl": gl, "hl": hl,
        "num": max(top, 10), "api_key": api_key,
    }
    try:
        resp = requests.get("https://serpapi.com/search.json", params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:  # noqa: BLE001
        return None, f"Error de red/SerpApi: {e}"
    if data.get("error"):
        return None, f"SerpApi error: {data['error']}"
    urls = [r.get("link") for r in (data.get("organic_results") or []) if r.get("link")]
    paa = [q.get("question") for q in (data.get("related_questions") or []) if q.get("question")]
    return {"urls": urls[:top], "paa": paa}, None


def extract_headings(html, BeautifulSoup):
    soup = BeautifulSoup(html, "html.parser")
    h1 = ""
    h1_tag = soup.find("h1")
    if h1_tag:
        h1 = re.sub(r"\s+", " ", h1_tag.get_text(" ", strip=True)).strip()
    headings = []
    for tag in soup.find_all(["h2", "h3"]):
        text = re.sub(r"\s+", " ", tag.get_text(" ", strip=True)).strip()
        if text:
            headings.append(f"{tag.name.upper()}: {text}")
    return h1, headings


def main():
    ap = argparse.ArgumentParser(
        description="Extrae esquemas H1/H2/H3 de los competidores del top de la SERP.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Ejemplo:\n  uv run serp_outline.py "cómo hacer seo" --top 5 --gl es --hl es',
    )
    ap.add_argument("query", help="Consulta (usada para SerpApi y como contexto)")
    ap.add_argument("--top", type=int, default=5, help="Nº de competidores a analizar (default 5)")
    ap.add_argument("--urls", help="Lista de URLs separadas por coma (salta SerpApi)")
    ap.add_argument("--gl", default="es", help="País (gl) para SerpApi, default 'es'")
    ap.add_argument("--hl", default="es", help="Idioma (hl) para SerpApi, default 'es'")
    args = ap.parse_args()

    try:
        import requests  # noqa: PLC0415
        from bs4 import BeautifulSoup  # noqa: PLC0415
    except ImportError as e:
        fail(
            f"Falta dependencia ({e}). Instalá: pip install -r requirements.txt",
            "modo manual: abrí el top 3-5 de la SERP y copiá sus H2/H3 a mano (Headings Map).",
        )

    paa = []
    if args.urls:
        urls = [u.strip() for u in args.urls.split(",") if u.strip()][: args.top]
    else:
        res, err = get_top_urls(args.query, args.top, args.gl, args.hl, requests)
        if err:
            fail(err, "modo manual: pasá --urls con el top de la SERP, o analizá los encabezados a mano.")
        urls, paa = res["urls"], res["paa"]

    if not urls:
        fail("No hay URLs para analizar.", "modo manual: pasá --urls o revisá la query.")

    competitors = []
    all_h2 = []
    for url in urls:
        try:
            r = requests.get(url, timeout=25, headers={"User-Agent": "aprendoseo-brief/1.0"})
            r.raise_for_status()
            h1, headings = extract_headings(r.text, BeautifulSoup)
        except Exception as e:  # noqa: BLE001
            log(f"no se pudo leer {url}: {e}")
            competitors.append({"url": url, "h1": "", "headings": [], "error": str(e)})
            continue
        competitors.append({"url": url, "h1": h1, "headings": headings})
        all_h2.extend(h.split("H2: ", 1)[1] for h in headings if h.startswith("H2: "))

    # Esquema sugerido: H2 ordenados por frecuencia (normalizando minúsculas).
    norm = Counter(h.lower() for h in all_h2)
    canonical = {}
    for h in all_h2:
        canonical.setdefault(h.lower(), h)
    suggested = [canonical[k] for k, _ in norm.most_common()]

    print(json.dumps({
        "ok": True,
        "query": args.query,
        "competitors": competitors,
        "common_questions": paa,
        "suggested_outline": suggested,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
