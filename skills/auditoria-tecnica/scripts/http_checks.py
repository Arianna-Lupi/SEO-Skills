#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["requests"]
# ///
"""
http_checks.py — Chequeo HTTP en vivo de una lista de URLs (fallback sin Screaming Frog).

Qué hace (determinista):
  1. Lee URLs desde --file (una por línea).
  2. Hace HEAD (o GET si HEAD falla/405) a cada URL con concurrencia limitada.
  3. Reporta status, si es https, y el destino de redirección (si la hay).
  4. Tope de seguridad (--cap, default 200) para no abusar del sitio.

Es el plan B cuando NO hay export de Screaming Frog: ve status reales y HTTPS,
pero NO reemplaza un crawl (no sigue enlaces ni detecta huérfanas).

Uso:
  python3 http_checks.py --file urls.txt
  python3 http_checks.py --file urls.txt --cap 100 --concurrency 8

Salida (JSON a stdout):
  {"ok": true, "checked": N, "results": [{"url","status","https","redirect_to"}],
   "summary": {"2xx","3xx","4xx","5xx","error","https","non_https"}}
  o: {"ok": false, "reason": "..."}

Deps: requests (ver requirements.txt). Sin requests → ok:false, exit 0.
"""

import argparse
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor

# UA de navegador real por defecto: muchos sitios (Cloudflare, WAFs) devuelven
# 403 a User-Agents que parecen bot. Se puede sobreescribir con la variable de
# entorno SEO_USER_AGENT si el sitio exige otra cosa.
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
TIMEOUT = 15


def out(obj):
    print(json.dumps(obj, ensure_ascii=False))
    sys.exit(0)


def check_one(requests, url):
    res = {"url": url, "status": None, "https": url.lower().startswith("https://"), "redirect_to": None}
    headers = BROWSER_HEADERS
    try:
        r = requests.head(url, headers=headers, allow_redirects=False, timeout=TIMEOUT)
        if r.status_code in (405, 501) or r.status_code >= 400:
            r = requests.get(url, headers=headers, allow_redirects=False, timeout=TIMEOUT, stream=True)
        res["status"] = r.status_code
        if 300 <= r.status_code < 400:
            res["redirect_to"] = r.headers.get("Location")
        try:
            r.close()
        except Exception:  # noqa: BLE001
            pass
    except Exception as e:  # noqa: BLE001
        res["status"] = "error"
        res["redirect_to"] = str(e)[:120]
    return res


def main():
    ap = argparse.ArgumentParser(
        description="Chequeo HTTP en vivo de una lista de URLs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Ejemplo:\n  uv run http_checks.py --file urls.txt --cap 200 --concurrency 8",
    )
    ap.add_argument("--file", required=True, help="archivo con una URL por línea")
    ap.add_argument("--cap", type=int, default=200, help="máximo de URLs a chequear")
    ap.add_argument("--concurrency", type=int, default=8, help="hilos concurrentes")
    args = ap.parse_args()

    try:
        import requests  # noqa: F401
    except ImportError:
        out({"ok": False, "reason": "falta la dependencia 'requests'",
             "fallback": "modo manual: usa Screaming Frog o el script parse_sf.py"})

    import requests

    try:
        with open(args.file, encoding="utf-8") as fh:
            urls = [ln.strip() for ln in fh if ln.strip()]
    except OSError as e:
        out({"ok": False, "reason": f"no se pudo leer --file: {e}"})

    # dedup preservando orden + tope
    seen, uniq = set(), []
    for u in urls:
        if u not in seen:
            seen.add(u)
            uniq.append(u)
    capped = uniq[: max(1, args.cap)]
    if not capped:
        out({"ok": False, "reason": "archivo sin URLs"})

    results = []
    with ThreadPoolExecutor(max_workers=max(1, args.concurrency)) as ex:
        results = list(ex.map(lambda u: check_one(requests, u), capped))

    summary = {"2xx": 0, "3xx": 0, "4xx": 0, "5xx": 0, "error": 0, "https": 0, "non_https": 0}
    for r in results:
        if r["https"]:
            summary["https"] += 1
        else:
            summary["non_https"] += 1
        s = r["status"]
        if isinstance(s, int):
            if 200 <= s < 300:
                summary["2xx"] += 1
            elif 300 <= s < 400:
                summary["3xx"] += 1
            elif 400 <= s < 500:
                summary["4xx"] += 1
            elif 500 <= s < 600:
                summary["5xx"] += 1
        else:
            summary["error"] += 1

    payload = {"ok": True, "checked": len(results), "results": results, "summary": summary}

    # Si TODO devolvió 403/429, casi seguro hay un WAF/anti-bot (Cloudflare):
    # avisamos para que el alumno no crea que su sitio está roto.
    statuses = [r["status"] for r in results if isinstance(r["status"], int)]
    if statuses and all(s in (403, 429) for s in statuses):
        payload["blocked"] = True
        payload["hint"] = (
            "Todas las URLs respondieron 403/429: probablemente un WAF/anti-bot "
            "(Cloudflare) bloquea el rastreo por TLS fingerprint, no por User-Agent. "
            "Si es tu sitio, crea una WAF rule que permita tu crawler o usa Screaming Frog. "
            "Prueba otro User-Agent con la variable de entorno SEO_USER_AGENT."
        )

    out(payload)


if __name__ == "__main__":
    main()
