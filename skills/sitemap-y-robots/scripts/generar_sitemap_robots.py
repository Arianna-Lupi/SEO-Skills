#!/usr/bin/env python3
"""
generar_sitemap_robots.py: genera sitemap.xml (y un robots.txt base) a partir de una lista de URLs (solo stdlib).

Úsalo SOLO cuando el CMS no genere el sitemap solo y el usuario necesite un archivo
para pasárselo a un developer (S13 · ticket técnico) o subirlo a mano. En WordPress
usa Rank Math o Yoast; en Shopify el sitemap se crea solo y no se edita.

Reglas que aplica (diplomado + práctica de coaches):
  - Solo URLs del mismo dominio y con https, sin fragmentos, sin duplicados.
  - Solo lo que quieres posicionar: excluye con --excluir (URLs con noindex, paginadas,
    redirigidas, carpetas privadas). "Menos es más si es lo correcto".
  - NO inventa fechas: sin --lastmod no escribe <lastmod>. Con --lastmod-csv usa fechas reales.
  - Parte en archivos de 50.000 URLs con un sitemap índice.

Uso:
  python3 generar_sitemap_robots.py --base https://ejemplo.com --urls urls.txt --out ./salida
  python3 generar_sitemap_robots.py --base https://ejemplo.com --urls urls.txt --excluir excluir.txt \\
      --lastmod-csv fechas.csv --robots --ia permitir --out ./salida

  --lastmod-csv: CSV con columnas url,lastmod (AAAA-MM-DD), de un export real del CMS.
  --robots: crea también robots.txt. --ia: permitir | bloquear-entrenamiento | bloquear-todo
Salida JSON: {"ok","urls_written","files":[...],"skipped":{motivo:cantidad}}
"""
import argparse
import csv
import json
import os
import re
import sys
from urllib.parse import urldefrag, urlparse
from xml.sax.saxutils import escape

TRAIN_BOTS = ["GPTBot", "ClaudeBot", "Google-Extended", "Applebot-Extended", "Bytespider", "CCBot"]
ALL_AI = TRAIN_BOTS + ["OAI-SearchBot", "ChatGPT-User", "Claude-User", "PerplexityBot"]
CHUNK = 50000


def read_lines(path):
    with open(path, encoding="utf-8") as fh:
        return [l.strip() for l in fh if l.strip() and not l.startswith("#")]


def build_robots(base, index_name, ia):
    lines = ["User-agent: *", "Allow: /", "# Agrega aquí solo rutas realmente privadas, por ejemplo:", "# Disallow: /wp-admin/", "# Allow: /wp-admin/admin-ajax.php", ""]
    bots = ALL_AI if ia == "bloquear-todo" else TRAIN_BOTS if ia == "bloquear-entrenamiento" else []
    for b in bots:
        lines += ["User-agent: " + b, "Disallow: /", ""]
    lines.append("Sitemap: %s/%s" % (base, index_name))
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", required=True, help="https://ejemplo.com")
    ap.add_argument("--urls", required=True, help="archivo con una URL por línea")
    ap.add_argument("--excluir", help="archivo con URLs a excluir (una por línea)")
    ap.add_argument("--lastmod-csv", help="CSV url,lastmod con fechas reales")
    ap.add_argument("--robots", action="store_true", help="genera también robots.txt")
    ap.add_argument("--ia", choices=["permitir", "bloquear-entrenamiento", "bloquear-todo"], default="permitir")
    ap.add_argument("--out", default="./salida")
    a = ap.parse_args()
    p = urlparse(a.base)
    if p.scheme != "https":
        print(json.dumps({"ok": False, "reason": "--base debe empezar por https://", "fallback": "modo manual: usa la plantilla de references/metodo-diploma.md"}))
        return
    host = p.netloc
    try:
        raw = read_lines(a.urls)
        excl = {u.rstrip("/") for u in read_lines(a.excluir)} if a.excluir else set()
        lastmod = {}
        if a.lastmod_csv:
            with open(a.lastmod_csv, encoding="utf-8") as fh:
                for r in csv.DictReader(fh):
                    if re.match(r"^\d{4}-\d{2}-\d{2}", r.get("lastmod", "")):
                        lastmod[r["url"].strip().rstrip("/")] = r["lastmod"].strip()
    except OSError as e:
        print(json.dumps({"ok": False, "reason": str(e), "fallback": "modo manual: revisa las rutas de los archivos"}))
        return
    skipped, seen, urls = {}, set(), []

    def skip(why):
        skipped[why] = skipped.get(why, 0) + 1

    for u in raw:
        u = urldefrag(u)[0]
        q = urlparse(u)
        if q.netloc != host:
            skip("otro dominio")
        elif q.scheme != "https":
            skip("no https")
        elif u.rstrip("/") in excl:
            skip("excluida")
        elif u in seen:
            skip("duplicada")
        else:
            seen.add(u)
            urls.append(u)
    os.makedirs(a.out, exist_ok=True)
    files, names = [], []
    chunks = [urls[i:i + CHUNK] for i in range(0, len(urls), CHUNK)] or [[]]
    for n, ch in enumerate(chunks, 1):
        name = "sitemap.xml" if len(chunks) == 1 else "sitemap-%d.xml" % n
        body = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
        for u in ch:
            lm = lastmod.get(u.rstrip("/"))
            body.append("  <url><loc>%s</loc>%s</url>" % (escape(u), "<lastmod>%s</lastmod>" % lm if lm else ""))
        body.append("</urlset>")
        with open(os.path.join(a.out, name), "w", encoding="utf-8") as fh:
            fh.write("\n".join(body) + "\n")
        names.append(name)
        files.append(os.path.join(a.out, name))
    index_name = names[0]
    if len(names) > 1:
        index_name = "sitemap_index.xml"
        body = ['<?xml version="1.0" encoding="UTF-8"?>', '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
        body += ["  <sitemap><loc>%s/%s</loc></sitemap>" % (a.base.rstrip("/"), n) for n in names]
        body.append("</sitemapindex>")
        with open(os.path.join(a.out, index_name), "w", encoding="utf-8") as fh:
            fh.write("\n".join(body) + "\n")
        files.append(os.path.join(a.out, index_name))
    if a.robots:
        with open(os.path.join(a.out, "robots.txt"), "w", encoding="utf-8") as fh:
            fh.write(build_robots(a.base.rstrip("/"), index_name, a.ia))
        files.append(os.path.join(a.out, "robots.txt"))
    print(json.dumps({"ok": True, "urls_written": len(urls), "files": files, "skipped": skipped,
                      "next": "Sube los archivos a la raíz del sitio (o pásalos al developer), prueba el robots.txt en technicalseo.com/tools/robots-txt y envía el sitemap en GSC > Sitemaps."}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
