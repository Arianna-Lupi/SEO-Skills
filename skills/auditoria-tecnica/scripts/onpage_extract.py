#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["requests"]
# ///
"""
onpage_extract.py — Extrae la data ON-PAGE de una lista de URLs con User-Agent de
navegador real + throttle (concurrencia baja). Recupera los datos que Screaming
Frog gratis NO consigue en sitios que lo rate-limitan (Shopify y otros WAF, que
devuelven 429 a su UA de bot y nunca le entregan el HTML real).

Qué saca por URL (descargando y parseando el HTML, sin LLM, solo stdlib + requests):
  - status, content_type, https, redirect_to (sin seguir la redirección)
  - title, title_len
  - meta_description, meta_description_len
  - meta_robots (index/noindex, follow/nofollow)
  - canonical (URL del rel=canonical) y self_canonical (bool)
  - h1 (lista) y h2_count
  - hreflang (lista de hreflang declarados)
  - lang (atributo <html lang>), viewport (bool), og_title, og_description
  - word_count (texto visible aprox.)
  - indexability ("Indexable" / "Non-Indexable") + indexability_status (motivo),
    inferida igual que en Screaming Frog (noindex, canonicalizada a otra URL, no-200).

NO reemplaza un crawl completo: no calcula inlinks, grafo de enlaces ni profundidad
(eso requiere rastrear el sitio). Cubre la capa on-page por URL.

Uso:
  uv run onpage_extract.py --file urls.txt
  uv run onpage_extract.py --url https://ejemplo.com/pagina --concurrency 4
  uv run onpage_extract.py --file urls.txt --csv onpage.csv   # además vuelca CSV

Salida (JSON a stdout): {"ok":true,"checked":N,"results":[{...}]}
  o {"ok":false,"reason":"...","fallback":"..."} (exit 0, p.ej. si falta requests).

Deps: requests (uv lo resuelve solo). Parseo HTML con stdlib (html.parser).
"""
import argparse
import concurrent.futures as cf
import csv as csvmod
import json
import re
import sys
from html.parser import HTMLParser
from urllib.parse import urldefrag, urljoin, urlparse

BROWSER_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
HEADERS = {
    "User-Agent": BROWSER_UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
}
TIMEOUT = 25


def out(obj):
    print(json.dumps(obj, ensure_ascii=False))
    sys.exit(0)


class OnPageParser(HTMLParser):
    """Extrae head/SEO de un HTML sin libs externas. Tolerante a HTML roto."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = None
        self._in_title = False
        self.meta_description = None
        self.meta_robots = None
        self.canonical = None
        self.h1 = []
        self.h2_count = 0
        self._cur_h = None
        self._h_buf = []
        self.hreflang = []
        self.lang = None
        self.viewport = False
        self.og_title = None
        self.og_description = None
        self._text_parts = []
        self._skip = 0  # dentro de script/style/noscript

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "html" and a.get("lang"):
            self.lang = a["lang"].strip()
        elif tag == "title":
            self._in_title = True
        elif tag == "meta":
            name = a.get("name", "").lower()
            prop = a.get("property", "").lower()
            content = a.get("content", "")
            if name == "description" and self.meta_description is None:
                self.meta_description = content.strip()
            elif name == "robots" and self.meta_robots is None:
                self.meta_robots = content.strip()
            elif name == "viewport":
                self.viewport = True
            elif prop == "og:title" and self.og_title is None:
                self.og_title = content.strip()
            elif prop == "og:description" and self.og_description is None:
                self.og_description = content.strip()
        elif tag == "link":
            rel = a.get("rel", "").lower()
            if "canonical" in rel and self.canonical is None:
                self.canonical = (a.get("href") or "").strip()
            if "alternate" in rel and a.get("hreflang"):
                self.hreflang.append(a["hreflang"].strip())
        elif tag in ("script", "style", "noscript"):
            self._skip += 1
        elif tag == "h1":
            self._cur_h = "h1"
            self._h_buf = []
        elif tag == "h2":
            self.h2_count += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag in ("script", "style", "noscript") and self._skip:
            self._skip -= 1
        elif tag == "h1" and self._cur_h == "h1":
            txt = " ".join("".join(self._h_buf).split())
            if txt:
                self.h1.append(txt)
            self._cur_h = None

    def handle_data(self, data):
        if self._in_title:
            self.title = ((self.title or "") + data).strip() or None
        if self._cur_h == "h1":
            self._h_buf.append(data)
        if not self._skip:
            self._text_parts.append(data)

    def word_count(self):
        text = " ".join(self._text_parts)
        return len(re.findall(r"\w+", text, flags=re.UNICODE))


def _norm(u):
    """Normaliza para comparar canonical vs URL (quita fragmento y slash final)."""
    if not u:
        return ""
    u = urldefrag(u)[0]
    return u.rstrip("/").lower()


def extract_one(requests, url):
    res = {"url": url, "status": None, "content_type": None,
           "https": url.lower().startswith("https://"), "redirect_to": None,
           "title": None, "title_len": 0, "meta_description": None,
           "meta_description_len": 0, "meta_robots": None, "canonical": None,
           "self_canonical": None, "h1": [], "h2_count": 0, "hreflang": [],
           "lang": None, "viewport": False, "og_title": None, "og_description": None,
           "word_count": None, "indexability": None, "indexability_status": None,
           "error": None}
    try:
        r = requests.get(url, headers=HEADERS, allow_redirects=False,
                         timeout=TIMEOUT, stream=True)
    except Exception as e:  # noqa: BLE001
        res["error"] = str(e)
        res["indexability"] = "Non-Indexable"
        res["indexability_status"] = "No Response"
        return res
    res["status"] = r.status_code
    res["content_type"] = (r.headers.get("Content-Type") or "").split(";")[0].strip() or None

    if 300 <= r.status_code < 400:
        res["redirect_to"] = r.headers.get("Location")
        res["indexability"] = "Non-Indexable"
        res["indexability_status"] = "Redirected"
        r.close()
        return res
    if r.status_code != 200 or "html" not in (res["content_type"] or ""):
        res["indexability"] = "Non-Indexable"
        res["indexability_status"] = ("Client Error" if 400 <= r.status_code < 500
                                      else "Server Error" if r.status_code >= 500
                                      else "Non-HTML")
        r.close()
        return res

    try:
        raw = r.raw.read(3_000_000, decode_content=True)
        # requests asume ISO-8859-1 cuando el header Content-Type no declara charset
        # (RFC 2616), aunque la página real sea UTF-8 — habitual en sitios sin ese
        # detalle. Prioriza el <meta charset>/http-equiv real del HTML sobre r.encoding.
        header_declares_charset = "charset=" in (r.headers.get("Content-Type") or "").lower()
        meta_match = re.search(rb'charset=["\']?\s*([\w-]+)', raw[:2048], re.IGNORECASE)
        meta_charset = meta_match.group(1).decode("ascii", "ignore") if meta_match else None
        enc = meta_charset or (r.encoding if header_declares_charset else None) or "utf-8"
        try:
            html = raw.decode(enc, "strict")
        except (LookupError, UnicodeDecodeError):
            html = raw.decode("utf-8", "replace")
    except Exception:  # noqa: BLE001
        html = r.text
    finally:
        r.close()

    p = OnPageParser()
    try:
        p.feed(html)
    except Exception:  # noqa: BLE001
        pass

    res["title"] = p.title
    res["title_len"] = len(p.title or "")
    res["meta_description"] = p.meta_description
    res["meta_description_len"] = len(p.meta_description or "")
    res["meta_robots"] = p.meta_robots
    canon_abs = urljoin(url, p.canonical) if p.canonical else None
    res["canonical"] = canon_abs
    res["self_canonical"] = (_norm(canon_abs) == _norm(url)) if canon_abs else None
    res["h1"] = p.h1
    res["h2_count"] = p.h2_count
    res["hreflang"] = p.hreflang
    res["lang"] = p.lang
    res["viewport"] = p.viewport
    res["og_title"] = p.og_title
    res["og_description"] = p.og_description
    res["word_count"] = p.word_count()

    robots = (p.meta_robots or "").lower()
    if "noindex" in robots:
        res["indexability"] = "Non-Indexable"
        res["indexability_status"] = "noindex"
    elif canon_abs and _norm(canon_abs) != _norm(url):
        res["indexability"] = "Non-Indexable"
        res["indexability_status"] = "Canonicalised"
    else:
        res["indexability"] = "Indexable"
        res["indexability_status"] = ""
    return res


CSV_COLS = ["url", "status", "content_type", "indexability", "indexability_status",
            "title", "title_len", "meta_description", "meta_description_len",
            "meta_robots", "canonical", "self_canonical", "h1", "h2_count",
            "hreflang", "lang", "viewport", "word_count", "redirect_to"]


def write_csv(path, results):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csvmod.writer(fh)
        w.writerow(CSV_COLS)
        for r in results:
            w.writerow([
                r.get("url"), r.get("status"), r.get("content_type"),
                r.get("indexability"), r.get("indexability_status"),
                r.get("title"), r.get("title_len"), r.get("meta_description"),
                r.get("meta_description_len"), r.get("meta_robots"),
                r.get("canonical"), r.get("self_canonical"),
                " | ".join(r.get("h1") or []), r.get("h2_count"),
                ",".join(r.get("hreflang") or []), r.get("lang"),
                r.get("viewport"), r.get("word_count"), r.get("redirect_to"),
            ])


def main():
    ap = argparse.ArgumentParser(
        description="Extrae data on-page (title/meta/canonical/encabezados) con UA real + throttle.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Ejemplo:\n  uv run onpage_extract.py --file urls.txt --concurrency 4 --csv onpage.csv",
    )
    ap.add_argument("--file", help="archivo con una URL por línea")
    ap.add_argument("--url", help="una sola URL (alternativa a --file)")
    ap.add_argument("--cap", type=int, default=2000, help="máximo de URLs (default 2000)")
    ap.add_argument("--concurrency", type=int, default=4,
                    help="hilos concurrentes (default 4; bajo = throttle, evita 429)")
    ap.add_argument("--csv", dest="csv_path", help="además, vuelca un CSV a esta ruta")
    args = ap.parse_args()

    try:
        import requests
    except ImportError:
        out({"ok": False, "reason": "falta la dependencia 'requests'",
             "fallback": "instala requests (pip install requests) o corre con `uv run`."})

    urls = []
    if args.url:
        urls = [args.url.strip()]
    elif args.file:
        try:
            with open(args.file, encoding="utf-8") as fh:
                urls = [ln.strip() for ln in fh if ln.strip()]
        except OSError as e:
            out({"ok": False, "reason": f"no se pudo leer {args.file}: {e}"})
    else:
        out({"ok": False, "reason": "pasa --file o --url"})

    urls = [u for u in urls if urlparse(u).scheme in ("http", "https")][:args.cap]
    if not urls:
        out({"ok": False, "reason": "no hay URLs http/https válidas"})

    results = [None] * len(urls)
    workers = max(1, min(args.concurrency, len(urls)))
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(extract_one, requests, u): i for i, u in enumerate(urls)}
        for fut in cf.as_completed(futs):
            results[futs[fut]] = fut.result()

    if args.csv_path:
        write_csv(args.csv_path, results)

    out({"ok": True, "checked": len(results),
         "csv": args.csv_path if args.csv_path else None,
         "results": results})


if __name__ == "__main__":
    main()
