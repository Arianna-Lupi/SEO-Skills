#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["requests", "tldextract"]
# ///
"""
competitor_domains.py — Descubre competidores SEO por dominio desde la SERP.

Qué hace (determinista):
  1. Consulta la SERP de una o varias keywords vía SerpApi.
  2. Toma el top N de URLs orgánicas de cada keyword.
  3. ENTRA a cada URL (sigue redirects) y extrae el DOMINIO REGISTRADO final
     (blog.ejemplo.co.uk -> ejemplo.co.uk), no el subdominio ni el host crudo.
  4. Agrega los dominios, cuenta en cuántas keywords aparece cada uno
     ("Análisis de Repetición": un dominio en varias SERPs = competidor crítico)
     y los ordena por repetición y mejor posición.

Requisitos:
  - Env SERPAPI_API_KEY (o --urls para saltarte SerpApi con una lista manual).
  - Deps: requests + tldextract (uv las resuelve solas). Si falta clave o dep,
    degrada con {"ok": false, ...} y exit 0 (la skill sigue en modo manual).

Uso:
  SERPAPI_API_KEY=xxx python3 competitor_domains.py "agencia seo madrid" --top 10 --gl es --hl es
  # varias keywords para repetición (separadas por |):
  python3 competitor_domains.py "agencia seo madrid|consultor seo|posicionamiento web" --top 10
  # excluir tu propio dominio del ranking:
  python3 competitor_domains.py "curso seo" --own midominio.com
  # sin SerpApi, pasando URLs a mano:
  python3 competitor_domains.py "curso seo" --urls "https://a.com/x,https://b.com/y" --no-visit

Salida (JSON a stdout):
  {
    "ok": true,
    "keywords": ["..."],
    "top": 10,
    "competitors": [
      {"domain","repeticion","best_position","positions":{"kw":pos},
       "sample_url","title"}, ...
    ],
    "own_domain": "midominio.com" | null
  }

Deps: requests, tldextract.
"""

import argparse
import json
import os
import re
import sys
from urllib.parse import urlparse

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


def registered_domain(url, extract):
    """Dominio registrado (eTLD+1) en minúsculas, o '' si no se puede parsear."""
    try:
        ext = extract(url)
    except Exception:  # noqa: BLE001
        return ""
    if not ext.domain or not ext.suffix:
        # p.ej. IPs o hosts raros: cae al netloc sin www
        net = urlparse(url).netloc.lower()
        return net[4:] if net.startswith("www.") else net
    return f"{ext.domain}.{ext.suffix}".lower()


def serp_urls(query, top, gl, hl, requests):
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
    out = []
    for r in (data.get("organic_results") or []):
        link = r.get("link")
        if link:
            out.append((r.get("position"), link))
    return out[:top], None


TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)


def visit(url, requests):
    """Sigue redirects, devuelve (url_final, title) o (url, '') si falla."""
    try:
        r = requests.get(url, timeout=20, headers=BROWSER_HEADERS, allow_redirects=True)
        final = r.url or url
        m = TITLE_RE.search(r.text or "")
        title = re.sub(r"\s+", " ", m.group(1)).strip() if m else ""
        return final, title
    except Exception as e:  # noqa: BLE001
        log(f"no se pudo entrar a {url}: {e}")
        return url, ""


def main():
    ap = argparse.ArgumentParser(
        description="Descubre competidores SEO por dominio desde la SERP.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Ejemplo:\n  uv run competitor_domains.py "agencia seo madrid|consultor seo" --top 10 --gl es',
    )
    ap.add_argument("keywords", help="Keyword, o varias separadas por | para análisis de repetición")
    ap.add_argument("--top", type=int, default=10, help="Nº de URLs orgánicas por keyword (default 10)")
    ap.add_argument("--gl", default="es", help="País (gl) para SerpApi, default 'es'")
    ap.add_argument("--hl", default="es", help="Idioma (hl) para SerpApi, default 'es'")
    ap.add_argument("--own", default="", help="Tu propio dominio, para excluirlo del ranking")
    ap.add_argument("--urls", help="Lista de URLs por coma (salta SerpApi; usa 1 sola keyword)")
    ap.add_argument("--no-visit", action="store_true", help="No entrar a las URLs (usa el dominio del link crudo)")
    args = ap.parse_args()

    _load_seo_env()

    try:
        import requests  # noqa: PLC0415
        import tldextract  # noqa: PLC0415
    except ImportError as e:
        fail(
            f"Falta dependencia ({e}). Con uv se resuelve sola; si no, pip install requests tldextract.",
            "modo manual: busca la keyword en Google en incógnito, copia el top 10, anota el dominio de cada uno y marca los que se repiten.",
        )

    # extractor offline (usa snapshot embebido, no descarga la PSL en cada corrida)
    extract = tldextract.TLDExtract(suffix_list_urls=())

    keywords = [k.strip() for k in args.keywords.split("|") if k.strip()]
    if not keywords:
        fail("No se pasó ninguna keyword.", "modo manual: define al menos una keyword.")

    # url_map: dominio -> {positions:{kw:pos}, sample_url, title}
    agg = {}
    own = registered_domain("http://" + args.own, extract) if args.own else None

    for kw in keywords:
        if args.urls:
            pairs = [(i + 1, u.strip()) for i, u in enumerate(args.urls.split(",")) if u.strip()][: args.top]
        else:
            pairs, err = serp_urls(kw, args.top, args.gl, args.hl, requests)
            if err:
                fail(err, "modo manual: pasa --urls con el top de la SERP, o revisa tu clave con configurar-serpapi.")
        if not pairs:
            log(f"sin URLs para '{kw}'")
            continue

        seen_this_kw = set()
        for pos, url in pairs:
            final_url, title = (url, "") if args.no_visit else visit(url, requests)
            dom = registered_domain(final_url, extract)
            if not dom or (own and dom == own):
                continue
            entry = agg.setdefault(dom, {"positions": {}, "sample_url": final_url, "title": title})
            # dentro de una misma keyword, quédate con la mejor (menor) posición
            if kw not in entry["positions"] or (pos and pos < entry["positions"][kw]):
                entry["positions"][kw] = pos
            if dom not in seen_this_kw and not entry["title"] and title:
                entry["title"] = title
            seen_this_kw.add(dom)

    competitors = []
    for dom, e in agg.items():
        positions = e["positions"]
        best = min((p for p in positions.values() if p), default=None)
        competitors.append({
            "domain": dom,
            "repeticion": len(positions),
            "best_position": best,
            "positions": positions,
            "sample_url": e["sample_url"],
            "title": e["title"],
        })

    # orden: más repetición primero, luego mejor posición
    competitors.sort(key=lambda c: (-c["repeticion"], c["best_position"] if c["best_position"] else 999))

    print(json.dumps({
        "ok": True,
        "keywords": keywords,
        "top": args.top,
        "competitors": competitors,
        "own_domain": own,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
