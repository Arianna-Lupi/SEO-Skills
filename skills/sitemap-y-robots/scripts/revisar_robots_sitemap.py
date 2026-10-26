#!/usr/bin/env python3
"""
revisar_robots_sitemap.py: revisa robots.txt y sitemap.xml de un sitio (solo stdlib).

Método del diplomado (S3 y S12): robots.txt sin `Disallow: /` accidental, sitemap
declarado, procesable y alineado con lo indexable. Los chequeos de límites de
sitemap, lastmod y bots de IA son complemento externo (claude-seo, MIT).

Qué hace:
  1. Descarga /robots.txt, lo interpreta (grupos, Allow/Disallow con * y $) y busca
     bloqueos graves, recursos bloqueados y directivas Sitemap.
  2. Informa qué bots de IA pueden o no rastrear el sitio según ese robots.txt.
  3. Descubre y lee los sitemaps (declarados o rutas comunes, índices y .gz), valida
     límites (50.000 URLs, 50 MB), https, lastmod y etiquetas obsoletas.
  4. Toma una MUESTRA de URLs del sitemap (--muestra, defecto 20) y comprueba status,
     redirección, noindex y canonical. No rastrea URLs que robots.txt bloquea.
  5. Prueba URLs concretas contra robots.txt con --probar (como technicalseo.com).

Uso:
  python3 revisar_robots_sitemap.py https://ejemplo.com
  python3 revisar_robots_sitemap.py https://ejemplo.com --muestra 40 --probar /blog/ /wp-admin/ --site ejemplo.com

Salida JSON a stdout; con --site también a .seo-audit/<sitio>/data/sitemap-robots.json
Ritmo: --delay segundos entre peticiones (defecto 0.7). User-Agent de navegador real.
Si no puede leer el sitio (WAF), devuelve ok:false con modo manual.
"""
import argparse
import gzip
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from urllib.parse import urljoin, urlparse

UA = os.environ.get(
    "SEO_USER_AGENT",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
)
TIMEOUT = 20
AI_BOTS = {
    "GPTBot": "OpenAI, entrenamiento",
    "OAI-SearchBot": "OpenAI, búsqueda de ChatGPT",
    "ChatGPT-User": "OpenAI, navegación a pedido del usuario",
    "ClaudeBot": "Anthropic, entrenamiento",
    "Claude-User": "Anthropic, navegación a pedido del usuario",
    "PerplexityBot": "Perplexity, índice de búsqueda",
    "Google-Extended": "Google, entrenamiento de Gemini (no afecta a Search)",
    "Applebot-Extended": "Apple, entrenamiento",
    "Bytespider": "ByteDance, entrenamiento",
    "CCBot": "Common Crawl, dataset abierto",
}
SITEMAP_PATHS = ["sitemap.xml", "sitemap_index.xml", "wp-sitemap.xml", "sitemap-index.xml", "sitemap/sitemap.xml"]
ISSUES = []


def issue(sev, where, text, fix):
    ISSUES.append({"severity": sev, "where": where, "issue": text, "fix": fix})


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


OPENER = urllib.request.build_opener(NoRedirect)


def get(url, limit=None):
    """(status, headers, body, error). No sigue redirecciones."""
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    try:
        r = OPENER.open(req, timeout=TIMEOUT)
        body = r.read(limit) if limit else r.read()
        return r.status, {k.lower(): v for k, v in r.getheaders()}, body, None
    except urllib.error.HTTPError as e:
        return e.code, {k.lower(): v for k, v in e.headers.items()}, b"", None
    except (urllib.error.URLError, ssl.SSLError, TimeoutError, OSError) as e:
        return None, {}, b"", str(e)


# ---------- robots.txt ----------
def parse_robots(text):
    groups, cur, sitemaps = [], None, []
    last_was_ua = False
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if ":" not in line:
            continue
        k, v = [x.strip() for x in line.split(":", 1)]
        k = k.lower()
        if k == "user-agent":
            if cur is None or not last_was_ua:
                cur = {"agents": [], "rules": [], "crawl_delay": None}
                groups.append(cur)
            cur["agents"].append(v.lower())
            last_was_ua = True
            continue
        last_was_ua = False
        if k == "sitemap":
            sitemaps.append(v)
        elif cur is not None and k in ("allow", "disallow"):
            cur["rules"].append((k, v))
        elif cur is not None and k == "crawl-delay":
            cur["crawl_delay"] = v
    return groups, sitemaps


def pattern_to_re(p):
    end = p.endswith("$")
    p = p[:-1] if end else p
    rx = "".join(".*" if c == "*" else re.escape(c) for c in p)
    return re.compile("^" + rx + ("$" if end else ""))


def allowed(groups, agent, path):
    """Regla de Google: el grupo más específico, la coincidencia más larga; Allow gana empates."""
    agent = agent.lower()
    best, best_len = None, -1
    for g in groups:
        for a in g["agents"]:
            if a != "*" and a in agent and len(a) > best_len:
                best, best_len = g, len(a)
    if best is None:
        best = next((g for g in groups if "*" in g["agents"]), None)
    if best is None:
        return True
    verdict, vlen = True, -1
    for kind, pat in best["rules"]:
        if not pat:
            continue
        if pattern_to_re(pat).match(path):
            n = len(pat)
            if n > vlen or (n == vlen and kind == "allow"):
                verdict, vlen = (kind == "allow"), n
    return verdict


def review_robots(base, probar):
    url = base + "/robots.txt"
    status, h, body, err = get(url, 500000)
    out = {"url": url, "status": status}
    if err:
        out["error"] = err
        issue("Alto", "robots.txt", "No se pudo descargar robots.txt: " + err, "Revisa que el sitio responda; si hay WAF, descarga el archivo a mano")
        return out, [], []
    if status == 404 or status is None:
        issue("Medio", "robots.txt", "robots.txt no existe (404)", "Crear un robots.txt mínimo con `User-agent: *` y la línea Sitemap. En sitios con código lo genera el developer")
        return out, [], []
    if status >= 400:
        issue("Alto", "robots.txt", "robots.txt responde %d" % status, "Un 5xx persistente puede frenar el rastreo; corrige el servidor")
        return out, [], []
    text = body.decode("utf-8", "replace")
    if "<html" in text[:500].lower():
        issue("Alto", "robots.txt", "robots.txt devuelve HTML (probablemente una página 404 con status 200)", "Servir un archivo de texto plano en /robots.txt")
    groups, sitemaps = parse_robots(text)
    out["groups"] = len(groups)
    out["sitemap_declarations"] = sitemaps
    if not allowed(groups, "Googlebot", "/"):
        issue("Crítico", "robots.txt", "Googlebot no puede rastrear la raíz (`Disallow: /`)", "Quitar el Disallow: / o limitarlo a las rutas realmente privadas, y pedir revisión en GSC")
    for probe, why in (("/wp-content/uploads/x.jpg", "imágenes"), ("/wp-content/themes/x/style.css", "CSS del tema"), ("/assets/app.js", "JS"), ("/author/x", "página de autor (E-E-A-T)")):
        if not allowed(groups, "Googlebot", probe):
            issue("Medio", "robots.txt", "Googlebot no puede rastrear " + why + " (" + probe + ")", "Quitar esa regla: Google necesita recursos y autores para entender la página")
    if not sitemaps:
        issue("Medio", "robots.txt", "robots.txt no declara ningún Sitemap", "Agregar la línea `Sitemap: https://dominio/sitemap.xml`")
    for s in sitemaps:
        if s.startswith("http://") and base.startswith("https://"):
            issue("Medio", "robots.txt", "Sitemap declarado con http: " + s, "Declarar la versión https")
    for g in groups:
        if g["crawl_delay"] and "*" in g["agents"]:
            out["crawl_delay"] = g["crawl_delay"]
            issue("Bajo", "robots.txt", "Crawl-delay %s en el grupo *: Google lo ignora, otros bots sí lo respetan" % g["crawl_delay"], "Mantenerlo solo si el servidor sufre con bots rápidos")
    ai = {}
    for bot, desc in AI_BOTS.items():
        ai[bot] = {"puede_rastrear_raiz": allowed(groups, bot, "/"), "uso": desc}
    out["ai_bots"] = ai
    if probar:
        out["pruebas"] = [{"ruta": p, "googlebot_permitido": allowed(groups, "Googlebot", p)} for p in probar]
    out["raw_preview"] = text[:1200]
    return out, groups, sitemaps


# ---------- sitemap ----------
def strip_ns(t):
    return t.split("}", 1)[-1]


def read_sitemap(url):
    status, h, body, err = get(url)
    if err or status != 200 or not body:
        return None, status, err, 0
    size = len(body)
    if body[:2] == b"\x1f\x8b":
        try:
            body = gzip.decompress(body)
        except OSError:
            return None, status, "gzip inválido", size
    try:
        root = ET.fromstring(body)
    except ET.ParseError as e:
        return None, status, "XML inválido: %s" % e, size
    return root, status, None, len(body)


def review_sitemaps(base, declared, groups, muestra, delay):
    cands = list(declared) or [urljoin(base + "/", p) for p in SITEMAP_PATHS]
    queue, seen, urls, files = list(cands), set(), [], []
    found_any = False
    while queue and len(files) < 60:
        u = queue.pop(0)
        if u in seen:
            continue
        seen.add(u)
        time.sleep(delay)
        root, st, err, size = read_sitemap(u)
        if root is None:
            if u in declared:
                issue("Alto", u, "Sitemap declarado que no se puede leer (%s)" % (err or st), "Corregir la URL o regenerar el sitemap; confirma en GSC > Sitemaps")
            continue
        found_any = True
        kind = "index" if strip_ns(root.tag) == "sitemapindex" else "urlset"
        locs, lastmods, deprecated = [], [], set()
        for el in root.iter():
            t = strip_ns(el.tag)
            if t == "loc" and el.text:
                locs.append(el.text.strip())
            elif t == "lastmod" and el.text:
                lastmods.append(el.text.strip())
            elif t in ("priority", "changefreq"):
                deprecated.add(t)
        info = {"url": u, "kind": kind, "entries": len(locs), "bytes_uncompressed": size}
        files.append(info)
        if kind == "index":
            queue.extend(l for l in locs if l not in seen)
            continue
        urls.extend(locs)
        if len(locs) > 50000 or size > 50 * 1024 * 1024:
            issue("Crítico", u, "El sitemap supera 50.000 URLs o 50 MB", "Dividir en varios sitemaps con un índice")
        if lastmods:
            bad = [l for l in lastmods if not re.match(r"^\d{4}-\d{2}-\d{2}(T[\d:.]+(Z|[+-]\d{2}:\d{2})?)?$", l)]
            if bad:
                issue("Bajo", u, "lastmod con formato inválido (ej. %s)" % bad[0], "Usar formato W3C: AAAA-MM-DD")
            if len(lastmods) > 20 and len(set(lastmods)) == 1:
                issue("Bajo", u, "Todos los lastmod son idénticos", "Usar la fecha real del último cambio significativo o quitar lastmod")
        if deprecated:
            issue("Bajo", u, "Usa " + ", ".join(sorted(deprecated)) + ": Google los ignora", "Se pueden quitar")
        http_urls = [l for l in locs if l.startswith("http://")]
        if http_urls and base.startswith("https://"):
            issue("Medio", u, "%d URLs con http dentro del sitemap" % len(http_urls), "Listar solo las versiones https")
    if not found_any:
        issue("Alto", "sitemap", "No se encontró ningún sitemap legible (declarado ni en rutas comunes)", "Crear uno (plugin Rank Math o Yoast en WordPress; developer en sitios con código) y enviarlo en GSC")
        return {"found": False, "files": files}, []
    urls = list(dict.fromkeys(urls))
    out = {"found": True, "files": files, "total_urls": len(urls)}
    if not urls:
        issue("Alto", "sitemap", "El sitemap no contiene URLs", "Revisar la generación del sitemap")
        return out, []
    # muestra
    step = max(1, len(urls) // max(1, muestra))
    sample = urls[::step][:muestra]
    rows, bad = [], {"no_200": 0, "redirect": 0, "noindex": 0, "canonical_otra": 0, "bloqueada_por_robots": 0}
    for u in sample:
        path = urlparse(u).path or "/"
        if groups and not allowed(groups, "Googlebot", path):
            bad["bloqueada_por_robots"] += 1
            rows.append({"url": u, "nota": "bloqueada por robots.txt, no se rastreó"})
            continue
        time.sleep(delay)
        st, h, body, err = get(u, 400000)
        row = {"url": u, "status": st}
        if err or st is None:
            row["error"] = err
            bad["no_200"] += 1
        elif 300 <= st < 400:
            bad["redirect"] += 1
            row["redirect_to"] = h.get("location")
        elif st != 200:
            bad["no_200"] += 1
        else:
            html = body.decode("utf-8", "replace")
            mr = re.search(r'<meta[^>]+name=["\']robots["\'][^>]*content=["\']([^"\']*)', html, re.I)
            if "noindex" in h.get("x-robots-tag", "").lower() or (mr and "noindex" in mr.group(1).lower()):
                bad["noindex"] += 1
                row["noindex"] = True
            for tag in re.findall(r"<link\b[^>]*>", html, re.I):
                if re.search(r'rel=["\']canonical["\']', tag, re.I):
                    m = re.search(r'href=["\']([^"\']+)', tag, re.I)
                    if m and urljoin(u, m.group(1)).rstrip("/") != u.rstrip("/"):
                        bad["canonical_otra"] += 1
                        row["canonical"] = m.group(1)
                    break
        rows.append(row)
    out["sample"] = {"checked": len(rows), "problems": bad, "rows": rows}
    n = max(1, len(rows))
    msgs = {
        "no_200": ("Alto", "no responden 200", "Quitarlas del sitemap o corregirlas"),
        "redirect": ("Medio", "redirigen", "Poner la URL final en el sitemap"),
        "noindex": ("Alto", "tienen noindex", "Quitarlas del sitemap o quitar el noindex si fue un error"),
        "canonical_otra": ("Medio", "tienen canonical a otra URL", "Dejar en el sitemap solo la URL canónica"),
        "bloqueada_por_robots": ("Alto", "están bloqueadas por robots.txt", "Alinear robots.txt y sitemap: o se rastrea o no está en el sitemap"),
    }
    for k, c in bad.items():
        if c:
            sev, t, fx = msgs[k]
            issue(sev, "sitemap", "%d de %d URLs de la muestra del sitemap %s" % (c, n, t), fx)
    return out, urls


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url", help="sitio a revisar, ej. https://ejemplo.com")
    ap.add_argument("--muestra", type=int, default=20, help="URLs del sitemap a comprobar (defecto 20)")
    ap.add_argument("--probar", nargs="*", default=[], help="rutas a probar contra robots.txt, ej. /blog/ /wp-admin/")
    ap.add_argument("--delay", type=float, default=0.7)
    ap.add_argument("--site", dest="slug", help="dominio para volcar a .seo-audit/<sitio>/data/")
    ap.add_argument("--root", default=".")
    a = ap.parse_args()
    site = a.url if re.match(r"^https?://", a.url) else "https://" + a.url
    p = urlparse(site)
    base = "%s://%s" % (p.scheme, p.netloc)
    robots, groups, declared = review_robots(base, a.probar)
    if robots.get("error") and not groups:
        blocked = any(x in str(robots.get("error")) for x in ("403", "Forbidden", "429"))
        print(json.dumps({"ok": False, "blocked": blocked, "reason": robots["error"],
                          "fallback": "modo manual: abre /robots.txt y /sitemap.xml en el navegador, pega el contenido y pruébalo en technicalseo.com/tools/robots-txt. Si hay Cloudflare, exporta el sitemap desde GSC"}, ensure_ascii=False))
        return
    sm, urls = review_sitemaps(base, declared, groups, a.muestra, a.delay)
    order = {"Crítico": 0, "Alto": 1, "Medio": 2, "Bajo": 3}
    ISSUES.sort(key=lambda i: order.get(i["severity"], 9))
    out = {"ok": True, "site": base, "robots": robots, "sitemap": sm, "issues": ISSUES}
    if a.slug:
        d = os.path.join(a.root, ".seo-audit", a.slug, "data")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "sitemap-robots.json"), "w", encoding="utf-8") as fh:
            json.dump(out, fh, ensure_ascii=False, indent=2)
        out["written"] = os.path.join(d, "sitemap-robots.json")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
