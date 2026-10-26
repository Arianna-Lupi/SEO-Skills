#!/usr/bin/env python3
"""
chequeos_tecnicos.py: chequeos técnicos en vivo por URL (solo stdlib).

Complemento externo (idea de claude-seo, MIT) portado al estilo del repo. No es
parte del método del diplomado, que sí pide revisar HTTPS, redirecciones,
canonical y renderizado (S3 y S12); este script automatiza esa revisión.

Por cada URL (idealmente UNA POR PLANTILLA, no todo el sitio):
  - Cadena de redirecciones (saltos, 301/302, bucles) y salto http a https.
  - Cabeceras de seguridad: HSTS, CSP, X-Frame-Options, X-Content-Type-Options,
    Referrer-Policy.
  - X-Robots-Tag, meta robots y canonical del HTML crudo (sin ejecutar JS).
  - Contenido mixto (recursos http dentro de una página https).
  - Prueba SSR vs CSR: con --texto "frase visible" comprueba si ese texto está
    en el HTML crudo (como "ver código fuente + Ctrl+F" de Juan en el foro).
  - Peso del HTML (alerta si supera 2 MB, límite de lectura de Googlebot).

Uso:
  python3 chequeos_tecnicos.py https://ejemplo.com/ https://ejemplo.com/blog/
  python3 chequeos_tecnicos.py --file urls.txt --texto "Frase visible de la página" --site ejemplo.com

Salida: JSON a stdout; con --site también a .seo-audit/<sitio>/data/chequeos-tecnicos.json
Respeta el ritmo: pausa entre peticiones (--delay) y tope (--cap).
"""
import argparse
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
from urllib.parse import urljoin, urlparse

UA = os.environ.get(
    "SEO_USER_AGENT",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
)
TIMEOUT = 20
MAX_HOPS = 10
HTML_LIMIT = 2 * 1024 * 1024
SEC_HEADERS = {
    "strict-transport-security": "HSTS",
    "content-security-policy": "CSP",
    "x-frame-options": "X-Frame-Options",
    "x-content-type-options": "X-Content-Type-Options",
    "referrer-policy": "Referrer-Policy",
}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


OPENER = urllib.request.build_opener(NoRedirect)


def fetch(url, read_body=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*;q=0.8"})
    try:
        r = OPENER.open(req, timeout=TIMEOUT)
        body = r.read(HTML_LIMIT + 1) if read_body else b""
        return r.status, dict((k.lower(), v) for k, v in r.getheaders()), body, None
    except urllib.error.HTTPError as e:
        body = b""
        if read_body:
            try:
                body = e.read(HTML_LIMIT + 1)
            except Exception:
                pass
        return e.code, dict((k.lower(), v) for k, v in e.headers.items()), body, None
    except (urllib.error.URLError, ssl.SSLError, TimeoutError, OSError) as e:
        return None, {}, b"", str(e)


def follow(url):
    """Sigue redirecciones a mano. Devuelve cadena, respuesta final y errores."""
    chain, seen = [], set()
    cur = url
    for _ in range(MAX_HOPS + 1):
        if cur in seen:
            return chain, None, "bucle de redirecciones"
        seen.add(cur)
        status, headers, body, err = fetch(cur, read_body=True)
        if err:
            return chain, None, err
        chain.append({"url": cur, "status": status})
        if status in (301, 302, 303, 307, 308) and headers.get("location"):
            cur = urljoin(cur, headers["location"])
            continue
        return chain, {"url": cur, "status": status, "headers": headers, "body": body}, None
    return chain, None, "más de %d saltos" % MAX_HOPS


def meta(html, name):
    m = re.search(r'<meta[^>]+name=["\']%s["\'][^>]*content=["\']([^"\']*)' % name, html, re.I) or \
        re.search(r'<meta[^>]+content=["\']([^"\']*)["\'][^>]+name=["\']%s["\']' % name, html, re.I)
    return m.group(1).strip() if m else None


def canonical(html):
    for tag in re.findall(r"<link\b[^>]*>", html, re.I):
        if re.search(r'rel=["\']canonical["\']', tag, re.I):
            m = re.search(r'href=["\']([^"\']+)', tag, re.I)
            return m.group(1).strip() if m else None
    return None


def check(url, texto):
    out = {"url": url, "findings": []}
    f = out["findings"]
    chain, final, err = follow(url)
    out["redirect_chain"] = chain
    if err or not final:
        out["error"] = err
        f.append({"severity": "Crítico", "issue": "No se pudo cargar la URL: %s" % err})
        return out
    out["final_url"], out["status"] = final["url"], final["status"]
    hops = len(chain) - 1
    if hops > 1:
        f.append({"severity": "Medio", "issue": "Cadena de %d redirecciones (debe ser 1 salto como máximo)" % hops})
    if any(c["status"] in (302, 303, 307) for c in chain[:-1]):
        f.append({"severity": "Medio", "issue": "Redirección temporal (302/307) donde suele corresponder 301"})
    if final["status"] >= 400:
        f.append({"severity": "Alto", "issue": "La URL final responde %d" % final["status"]})
    h = final["headers"]
    final_https = final["url"].startswith("https://")
    out["https"] = final_https
    if not final_https:
        f.append({"severity": "Crítico", "issue": "La URL final no usa HTTPS"})
    sec = {label: (key in h) for key, label in SEC_HEADERS.items()}
    out["security_headers"] = sec
    if final_https:
        missing = [k for k, v in sec.items() if not v]
        if "HSTS" in missing:
            f.append({"severity": "Medio", "issue": "Falta Strict-Transport-Security (HSTS)"})
        others = [m for m in missing if m != "HSTS"]
        if others:
            f.append({"severity": "Bajo", "issue": "Faltan cabeceras de seguridad: " + ", ".join(others)})
    if "x-robots-tag" in h:
        out["x_robots_tag"] = h["x-robots-tag"]
        if "noindex" in h["x-robots-tag"].lower():
            f.append({"severity": "Crítico", "issue": "X-Robots-Tag con noindex en la cabecera HTTP"})
    body = final["body"]
    out["html_bytes"] = len(body)
    if len(body) > HTML_LIMIT:
        f.append({"severity": "Alto", "issue": "El HTML supera 2 MB: Googlebot lee solo los primeros 2 MB"})
    html = body[:HTML_LIMIT].decode("utf-8", "replace")
    mr = meta(html, "robots")
    out["meta_robots"] = mr
    if mr and "noindex" in mr.lower():
        f.append({"severity": "Crítico", "issue": "meta robots con noindex en el HTML crudo"})
    can = canonical(html)
    out["canonical"] = can
    if not can:
        f.append({"severity": "Medio", "issue": "Sin rel=canonical en el HTML crudo (usa self-canonical)"})
    elif urljoin(final["url"], can).rstrip("/") != final["url"].rstrip("/"):
        f.append({"severity": "Alto", "issue": "El canonical apunta a otra URL: " + can + " (confirma que es intencional)"})
    if final_https:
        res = re.findall(r'<(?:img|script|iframe|source|video|audio)\b[^>]*\bsrc=["\'](http://[^"\']+)', html, re.I)
        res += re.findall(r'<link\b[^>]*\bhref=["\'](http://[^"\']+)', html, re.I)
        out["mixed_content"] = res[:10]
        if res:
            f.append({"severity": "Medio", "issue": "Contenido mixto: %d recurso(s) http en página https" % len(res)})
    if texto:
        present = texto.lower() in html.lower()
        out["texto_en_html_crudo"] = present
        if not present:
            f.append({"severity": "Alto", "issue": "El texto de prueba NO está en el HTML crudo: probable CSR. Google lo verá solo tras renderizar"})
    # salto http a https del mismo host
    p = urlparse(final["url"])
    if final_https:
        hc, hfinal, herr = follow("http://" + p.netloc + "/")
        out["http_to_https"] = bool(hfinal and hfinal["url"].startswith("https://"))
        if not herr and hfinal and not hfinal["url"].startswith("https://"):
            f.append({"severity": "Crítico", "issue": "La versión http:// no redirige a https://"})
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("urls", nargs="*", help="URLs a revisar (una por plantilla)")
    ap.add_argument("--file", help="archivo con una URL por línea")
    ap.add_argument("--texto", help="frase visible de la página para probar SSR vs CSR")
    ap.add_argument("--cap", type=int, default=30, help="máximo de URLs (defecto 30)")
    ap.add_argument("--delay", type=float, default=1.0, help="segundos entre URLs (defecto 1)")
    ap.add_argument("--site", help="dominio, para volcar a .seo-audit/<sitio>/data/")
    ap.add_argument("--root", default=".", help="raíz del proyecto (defecto .)")
    a = ap.parse_args()
    urls = list(a.urls)
    if a.file:
        with open(a.file, encoding="utf-8") as fh:
            urls += [l.strip() for l in fh if l.strip() and not l.startswith("#")]
    if not urls:
        print(json.dumps({"ok": False, "reason": "sin URLs", "fallback": "modo manual: revisa redirecciones y cabeceras con el navegador (pestaña Red) o securityheaders.com"}))
        return
    results = []
    for i, u in enumerate(urls[: a.cap]):
        if i:
            time.sleep(a.delay)
        results.append(check(u, a.texto))
    sev = {}
    for r in results:
        for x in r["findings"]:
            sev[x["severity"]] = sev.get(x["severity"], 0) + 1
    out = {"ok": True, "checked": len(results), "truncated": len(urls) > a.cap, "by_severity": sev, "results": results}
    if a.site:
        d = os.path.join(a.root, ".seo-audit", a.site, "data")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "chequeos-tecnicos.json"), "w", encoding="utf-8") as fh:
            json.dump(out, fh, ensure_ascii=False, indent=2)
        out["written"] = os.path.join(d, "chequeos-tecnicos.json")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
