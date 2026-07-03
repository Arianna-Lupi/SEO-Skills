#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["requests", "beautifulsoup4"]
# ///
"""
serp_metadata.py — Extrae metatítulo y metadescripción de los competidores del top de la SERP.

Qué hace (determinista):
  1. Obtiene las URLs orgánicas del top N (vía SerpApi) — o usa --urls para
     pasar una lista y saltarte SerpApi.
  2. ENTRA a cada URL y extrae su <title>, su <meta name="description"> y, de
     apoyo, el H1 y los og:title/og:description.
  3. Cuenta caracteres de cada meta y marca si caen en rango (título 50-60,
     descripción 120-155). Devuelve todo COMPACTO en JSON para que redactes la
     metadata de tu keyword con el benchmark real de CTR delante, no de memoria.

Este script NO redacta tu metadata: te da el benchmark de la competencia. La
redacción (título 50-60 con keyword al inicio, descripción 120-155 con CTA) la
haces tú y la validas con meta_check.py.

Requisitos:
  - Para sacar URLs automáticamente: env SERPAPI_API_KEY. Alternativa: --urls.
  - Deps: requests + beautifulsoup4 (uv las resuelve solas). Si falta algo,
    degrada con {"ok": false, ...} y exit 0 (la skill sigue en modo manual).

Uso:
  SERPAPI_API_KEY=xxx python3 serp_metadata.py "sérum vitamina c" --top 10 --gl es --hl es
  python3 serp_metadata.py "sérum vitamina c" --urls "https://a.com/x,https://b.com/y"

Salida (JSON a stdout):
  {
    "ok": true, "query": "...",
    "paa": [...preguntas People Also Ask...],
    "competitors": [
      {"url","serp_title","serp_snippet",
       "meta_title","meta_title_len","meta_title_in_range",
       "meta_description","meta_description_len","meta_description_in_range",
       "h1","og_title","og_description"}, ...
    ]
  }

Deps: requests, beautifulsoup4.
"""

import argparse
import json
import os
import re
import sys

DEFAULT_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
)
USER_AGENT = os.environ.get("SEO_USER_AGENT", DEFAULT_UA)
BROWSER_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
}


def log(msg):
    print(msg, file=sys.stderr)


def fail(reason, fallback):
    print(json.dumps({"ok": False, "reason": reason, "fallback": fallback}, ensure_ascii=False))
    sys.exit(0)


def _load_seo_env():
    """Carga ~/.claude/seo-skills.env (KEY=valor por linea) en el entorno si existe.
    Asi la SERPAPI_API_KEY que guardo la skill configurar-serpapi se usa en cada
    sesion sin re-exportarla. No pisa variables ya presentes en el entorno."""
    path = os.path.expanduser("~/.claude/seo-skills.env")
    try:
        with open(path, encoding="utf-8") as fh:
            for raw in fh:
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                if k and k not in os.environ:
                    os.environ[k] = v.strip().strip('"').strip("'")
    except OSError:
        pass


def get_top(query, top, gl, hl, requests):
    _load_seo_env()
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
    results = [
        {"link": r.get("link"), "title": r.get("title"), "snippet": r.get("snippet")}
        for r in (data.get("organic_results") or []) if r.get("link")
    ]
    paa = [q.get("question") for q in (data.get("related_questions") or []) if q.get("question")]
    return {"results": results[:top], "paa": paa}, None


def clean(text):
    return re.sub(r"\s+", " ", text or "").strip()


def extract_meta(html, BeautifulSoup):
    soup = BeautifulSoup(html, "html.parser")
    title = clean(soup.title.get_text()) if soup.title else ""
    def meta(attr, val):
        tag = soup.find("meta", attrs={attr: val})
        return clean(tag.get("content")) if tag and tag.get("content") else ""
    desc = meta("name", "description")
    og_title = meta("property", "og:title")
    og_desc = meta("property", "og:description")
    h1_tag = soup.find("h1")
    h1 = clean(h1_tag.get_text(" ", strip=True)) if h1_tag else ""
    return title, desc, h1, og_title, og_desc


def main():
    ap = argparse.ArgumentParser(
        description="Extrae metatítulo y metadescripción de los competidores del top de la SERP.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Ejemplo:\n  uv run serp_metadata.py "sérum vitamina c natural" --top 10 --gl es --hl es',
    )
    ap.add_argument("query", help="Keyword (usada para SerpApi y como contexto)")
    ap.add_argument("--top", type=int, default=10, help="Nº de competidores a analizar (default 10)")
    ap.add_argument("--urls", help="Lista de URLs por coma (salta SerpApi)")
    ap.add_argument("--gl", default="es", help="País (gl) para SerpApi, default 'es'")
    ap.add_argument("--hl", default="es", help="Idioma (hl) para SerpApi, default 'es'")
    args = ap.parse_args()

    try:
        import requests  # noqa: PLC0415
        from bs4 import BeautifulSoup  # noqa: PLC0415
    except ImportError as e:
        fail(
            f"Falta dependencia ({e}). Con uv se resuelve sola; si no, pip install requests beautifulsoup4.",
            "modo manual: abre el top 10 de la SERP y copia el título y la metadescripción de cada uno (usa el simulador de Mangools).",
        )

    paa = []
    serp_meta = {}  # url -> (serp_title, serp_snippet)
    if args.urls:
        urls = [u.strip() for u in args.urls.split(",") if u.strip()][: args.top]
    else:
        res, err = get_top(args.query, args.top, args.gl, args.hl, requests)
        if err:
            fail(err, "modo manual: pasa --urls con el top de la SERP, o revisa tu clave con configurar-serpapi.")
        urls = [r["link"] for r in res["results"]]
        paa = res["paa"]
        serp_meta = {r["link"]: (r["title"], r["snippet"]) for r in res["results"]}

    if not urls:
        fail("No hay URLs para analizar.", "modo manual: pasa --urls o revisa la query.")

    competitors = []
    for url in urls:
        s_title, s_snippet = serp_meta.get(url, ("", ""))
        try:
            r = requests.get(url, timeout=25, headers=BROWSER_HEADERS, allow_redirects=True)
            r.raise_for_status()
            m_title, m_desc, h1, og_t, og_d = extract_meta(r.text, BeautifulSoup)
        except Exception as e:  # noqa: BLE001
            log(f"no se pudo entrar a {url}: {e}")
            competitors.append({"url": url, "serp_title": s_title, "serp_snippet": s_snippet, "error": str(e)})
            continue
        tl = len(m_title)
        dl = len(m_desc)
        competitors.append({
            "url": url,
            "serp_title": s_title,
            "serp_snippet": s_snippet,
            "meta_title": m_title,
            "meta_title_len": tl,
            "meta_title_in_range": 50 <= tl <= 60,
            "meta_description": m_desc,
            "meta_description_len": dl,
            "meta_description_in_range": 120 <= dl <= 155,
            "h1": h1,
            "og_title": og_t,
            "og_description": og_d,
        })

    print(json.dumps({
        "ok": True,
        "query": args.query,
        "paa": paa,
        "competitors": competitors,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
