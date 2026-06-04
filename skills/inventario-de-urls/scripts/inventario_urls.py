#!/usr/bin/env python3
"""
inventario_urls.py — Inventario GRATIS de URLs de un sitio vía sitemap (cero deps).

Qué hace (determinista):
  1. Descarga /robots.txt y lee las directivas `Sitemap:`.
  2. Si no hay directiva, prueba /sitemap.xml y /sitemap_index.xml.
  3. Sigue los <sitemapindex> (hijos <sitemap><loc>) hasta los sitemaps de URLs.
  4. Junta todos los <loc> de URLs, deduplica y ordena.

Solo usa la librería estándar (urllib + xml.etree). No necesita claves ni
instalar nada. Para >500 URLs, páginas huérfanas o códigos de estado en vivo,
usar Screaming Frog CLI (gratis hasta 500 URLs) — ESTE script es la ruta
free de cero dependencias y solo ve URLs publicadas en el sitemap.

Uso:
  python3 inventario_urls.py https://ejemplo.com
  python3 inventario_urls.py https://ejemplo.com --sitemap https://ejemplo.com/sitemap_index.xml
  python3 inventario_urls.py https://ejemplo.com --max 2000

Salida (JSON a stdout):
  {"ok": true, "source": "robots|sitemap.xml", "count": N, "urls": [...]}
  o en error/sin datos:
  {"ok": false, "reason": "...", "fallback": "modo manual: ..."}

Deps: solo stdlib.
"""

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

USER_AGENT = "aprendoseo-inventario-urls/1.0 (+sitemap-reader)"
TIMEOUT = 20


def log(msg):
    print(msg, file=sys.stderr)


def fetch(url):
    """Devuelve (bytes, None) o (None, error_str)."""
    try:
        req = Request(url, headers={"User-Agent": USER_AGENT})
        with urlopen(req, timeout=TIMEOUT) as resp:
            return resp.read(), None
    except Exception as e:  # noqa: BLE001 - degradación controlada
        return None, str(e)


def normalize_site(site):
    if not re.match(r"^https?://", site):
        site = "https://" + site
    p = urlparse(site)
    return f"{p.scheme}://{p.netloc}"


def sitemaps_from_robots(base):
    """Lee robots.txt y extrae las URLs de los Sitemap:."""
    data, err = fetch(urljoin(base + "/", "robots.txt"))
    if err or not data:
        log(f"robots.txt no disponible: {err}")
        return []
    text = data.decode("utf-8", "replace")
    found = re.findall(r"(?im)^\s*sitemap:\s*(\S+)\s*$", text)
    return [u.strip() for u in found]


def strip_ns(tag):
    return tag.split("}", 1)[-1] if "}" in tag else tag


def parse_sitemap(xml_bytes):
    """Devuelve (kind, locs) donde kind es 'index' o 'urlset'."""
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError as e:
        log(f"XML inválido: {e}")
        return None, []
    kind = "index" if strip_ns(root.tag) == "sitemapindex" else "urlset"
    locs = [
        loc.text.strip()
        for loc in root.iter()
        if strip_ns(loc.tag) == "loc" and loc.text and loc.text.strip()
    ]
    return kind, locs


def collect_urls(seed_sitemaps, max_urls):
    """BFS por los sitemaps; sigue índices. Devuelve set de URLs."""
    seen_maps, urls, queue = set(), set(), list(seed_sitemaps)
    while queue and len(urls) < max_urls:
        sm = queue.pop(0)
        if sm in seen_maps:
            continue
        seen_maps.add(sm)
        data, err = fetch(sm)
        if err or not data:
            log(f"sitemap no descargado {sm}: {err}")
            continue
        kind, locs = parse_sitemap(data)
        if kind == "index":
            queue.extend(loc for loc in locs if loc not in seen_maps)
        elif kind == "urlset":
            urls.update(locs)
    return urls


def main():
    ap = argparse.ArgumentParser(
        description="Inventario de URLs vía sitemap (free, stdlib).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Ejemplo:\n  python3 inventario_urls.py https://ejemplo.com --max 50000",
    )
    ap.add_argument("site", help="Dominio del sitio, p.ej. https://ejemplo.com")
    ap.add_argument("--sitemap", help="URL de sitemap conocida (salta robots.txt)")
    ap.add_argument("--max", type=int, default=50000, help="Tope de URLs (default 50000)")
    args = ap.parse_args()

    base = normalize_site(args.site)

    if args.sitemap:
        seeds, source = [args.sitemap], "sitemap.xml"
    else:
        seeds = sitemaps_from_robots(base)
        if seeds:
            source = "robots"
        else:
            seeds = [urljoin(base + "/", p) for p in ("sitemap.xml", "sitemap_index.xml")]
            source = "sitemap.xml"

    urls = collect_urls(seeds, args.max)

    if not urls:
        print(json.dumps({
            "ok": False,
            "reason": "No se encontraron sitemaps válidos ni URLs (robots.txt sin Sitemap: y sitemap.xml ausente o vacío).",
            "fallback": "modo manual: prueba rutas de sitemap no estándar, o usa Screaming Frog CLI (gratis ≤500 URLs) para rastrear el sitio.",
        }, ensure_ascii=False))
        return

    out = sorted(urls)
    print(json.dumps({
        "ok": True,
        "source": source,
        "count": len(out),
        "urls": out,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
