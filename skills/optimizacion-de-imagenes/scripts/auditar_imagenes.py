#!/usr/bin/env python3
"""
auditar_imagenes.py: audita las imágenes de las páginas que le pases (solo stdlib).

Método del diplomado (S12 · Velocidad y rendimiento): peso (listar las que superan
100 kb), formato moderno (WebP), dimensiones acordes al diseño y atributo ALT en
cada imagen. Lazy loading, width/height (CLS) y AVIF son complemento externo
(claude-seo, MIT) y práctica de coaches (Juan).

Pasa UNA URL POR PLANTILLA (Home, categoría, artículo, producto): "optimiza el contenedor,
no solo el contenido". Descarga el HTML, lista las <img>/<source> y consulta el peso real
de cada archivo con una petición HEAD (o GET parcial si el servidor no responde HEAD).

Qué marca por imagen:
  - peso > 100 kb (diploma); en hero/banner el umbral de aviso es 200 kb (complemento)
  - formato JPG/PNG/GIF/BMP en vez de WebP o AVIF
  - alt ausente (atributo no existe), alt vacío (válido solo si es decorativa), alt genérico
    (nombre de archivo, "imagen", "foto") o demasiado largo (> 125 caracteres)
  - width/height ausentes (riesgo de CLS)
  - primera imagen con loading="lazy" (daña el LCP) o imágenes bajo el pliegue sin lazy
  - nombre de archivo no descriptivo (IMG_1234.jpg, DSC0001.png)

Uso:
  python3 auditar_imagenes.py https://ejemplo.com/ https://ejemplo.com/blog/articulo/
  python3 auditar_imagenes.py --file plantillas.txt --max-imagenes 40 --site ejemplo.com

Salida JSON a stdout; con --site también a .seo-audit/<sitio>/data/imagenes.json
Respeta robots.txt (no descarga páginas bloqueadas), pausa entre peticiones (--delay).
Si no puede leer el sitio (WAF), devuelve ok:false con modo manual (Screaming Frog > Images).
"""
import argparse
import json
import os
import re
import ssl
import time
import urllib.error
import urllib.request
import urllib.robotparser
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

UA = os.environ.get(
    "SEO_USER_AGENT",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
)
TIMEOUT = 20
LIMIT_KB = 100          # diplomado, S12
HERO_WARN_KB = 200      # complemento claude-seo
LEGACY = {"jpg", "jpeg", "png", "gif", "bmp"}
MODERN = {"webp", "avif"}
GENERIC_ALT = re.compile(r"^(imagen|image|foto|photo|picture|img|banner|logo)?\s*\d*$", re.I)
BAD_NAME = re.compile(r"^(img|dsc|dscn|image|foto|screenshot|captura|untitled|whatsapp)[-_ ]?\d+", re.I)


class ImgParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.imgs, self.in_picture, self.order = [], False, 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "picture":
            self.in_picture = True
        elif tag == "source" and self.in_picture:
            for k in ("srcset", "data-srcset"):
                if a.get(k):
                    self.imgs.append({"kind": "source", "src": a[k].split(",")[0].strip().split(" ")[0], "type": a.get("type")})
        elif tag == "img":
            src = a.get("src") or a.get("data-src") or a.get("data-lazy-src") or ""
            if not src and (a.get("srcset") or a.get("data-srcset")):
                src = (a.get("srcset") or a.get("data-srcset")).split(",")[0].strip().split(" ")[0]
            self.order += 1
            self.imgs.append({
                "kind": "img", "order": self.order, "src": src,
                "has_alt": "alt" in a, "alt": a.get("alt"),
                "width": a.get("width"), "height": a.get("height"),
                "loading": a.get("loading"), "fetchpriority": a.get("fetchpriority"),
                "srcset": bool(a.get("srcset") or a.get("data-srcset")),
                "js_lazy": bool(a.get("data-src") or a.get("data-lazy-src") or "lazy" in (a.get("class") or "")),
                "in_picture": self.in_picture,
            })

    def handle_endtag(self, tag):
        if tag == "picture":
            self.in_picture = False


def fetch(url, method="GET", limit=None, headers=None):
    h = {"User-Agent": UA, "Accept": "*/*"}
    h.update(headers or {})
    req = urllib.request.Request(url, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            body = r.read(limit) if (method == "GET" and limit) else (r.read() if method == "GET" else b"")
            return r.status, {k.lower(): v for k, v in r.getheaders()}, body, None
    except urllib.error.HTTPError as e:
        return e.code, {k.lower(): v for k, v in e.headers.items()}, b"", None
    except (urllib.error.URLError, ssl.SSLError, TimeoutError, OSError) as e:
        return None, {}, b"", str(e)


def weight_kb(url):
    """Peso real en kb: HEAD; si no hay content-length, GET con Range 0-0 (content-range)."""
    st, h, _, err = fetch(url, "HEAD")
    if st and "content-length" in h:
        return round(int(h["content-length"]) / 1024, 1), h.get("content-type"), st
    st, h, _, err = fetch(url, "GET", 1, {"Range": "bytes=0-0"})
    m = re.search(r"/(\d+)$", h.get("content-range", ""))
    if m:
        return round(int(m.group(1)) / 1024, 1), h.get("content-type"), st
    return None, h.get("content-type"), st


def ext_of(url):
    path = urlparse(url).path.lower()
    m = re.search(r"\.([a-z0-9]+)$", path)
    e = m.group(1) if m else ""
    q = urlparse(url).query.lower()
    f = re.search(r"(?:format|fm)=([a-z0-9]+)", q)
    return f.group(1) if f else e


def audit_page(page, max_imgs, delay, robots):
    out = {"page": page, "images": [], "findings": []}
    f = out["findings"]
    path = urlparse(page).path or "/"
    if robots and not robots.can_fetch("*", page):
        out["error"] = "bloqueada por robots.txt, no se rastreó"
        return out
    st, h, body, err = fetch(page, "GET", 3 * 1024 * 1024)
    if err or st != 200:
        out["error"] = err or "status %s" % st
        return out
    p = ImgParser()
    p.feed(body.decode("utf-8", "replace"))
    imgs = [i for i in p.imgs if i.get("src") and not i["src"].startswith("data:")]
    seen, rows = set(), []
    for i in imgs:
        i["abs"] = urljoin(page, i["src"])
        if i["abs"] in seen:
            continue
        seen.add(i["abs"])
        rows.append(i)
    out["total_img_tags"] = len([i for i in p.imgs if i["kind"] == "img"])
    for idx, i in enumerate(rows[:max_imgs]):
        time.sleep(delay)
        kb, ctype, st_img = weight_kb(i["abs"])
        ext = ext_of(i["abs"])
        row = {"src": i["abs"], "kind": i["kind"], "kb": kb, "format": ext or (ctype or ""), "status": st_img, "problems": []}
        pr = row["problems"]
        is_first = i["kind"] == "img" and i.get("order") == 1
        limit = HERO_WARN_KB if is_first else LIMIT_KB
        if kb is not None and kb > LIMIT_KB:
            pr.append("pesa %.0f kb (más de %d kb)" % (kb, LIMIT_KB))
        if ext in LEGACY or (ctype and re.search(r"image/(jpeg|png|gif|bmp)", ctype)):
            pr.append("formato %s: convertir a WebP (o AVIF si el CMS lo admite)" % (ext or ctype))
        if st_img and st_img >= 400:
            pr.append("la imagen responde %d" % st_img)
        if i["kind"] == "img":
            row.update({"alt": i["alt"], "width": i["width"], "height": i["height"], "loading": i["loading"]})
            if not i["has_alt"]:
                pr.append("sin atributo alt")
            elif i["alt"] is not None and not i["alt"].strip():
                row["alt_vacio"] = True
            elif i["alt"] and (GENERIC_ALT.match(i["alt"].strip()) or re.search(r"\.(jpe?g|png|webp|gif)$", i["alt"], re.I)):
                pr.append("alt genérico o nombre de archivo")
            elif i["alt"] and len(i["alt"]) > 125:
                pr.append("alt de más de 125 caracteres")
            if not (i["width"] and i["height"]):
                pr.append("sin width/height (riesgo de CLS)")
            if is_first and i["loading"] == "lazy":
                pr.append("la primera imagen tiene loading=lazy (daña el LCP)")
            if idx >= 3 and not i["loading"] and not i["js_lazy"]:
                pr.append("bajo el pliegue sin lazy loading")
        fname = os.path.basename(urlparse(i["abs"]).path)
        if BAD_NAME.match(fname):
            pr.append("nombre de archivo no descriptivo (%s)" % fname)
        out["images"].append(row)
    n = max(1, len(out["images"]))
    def count(txt):
        return sum(1 for r in out["images"] if any(txt in x for x in r["problems"]))
    heavy, legacy, noalt, nodim = count("pesa"), count("formato"), count("sin atributo alt"), count("sin width")
    if heavy:
        f.append({"severity": "Alto", "issue": "%d de %d imágenes pesan más de %d kb" % (heavy, n, LIMIT_KB), "fix": "Comprimir (Squoosh) y reducir dimensiones al tamaño real del diseño"})
    if legacy:
        f.append({"severity": "Medio", "issue": "%d de %d imágenes en JPG/PNG/GIF" % (legacy, n), "fix": "Convertir a WebP. En Shopify no se sube WebP: se comprime el archivo (la plataforma entrega WebP sola)"})
    if noalt:
        f.append({"severity": "Bajo", "issue": "%d de %d imágenes sin alt" % (noalt, n), "fix": "Describir la imagen en una frase; vacío solo si es decorativa"})
    if nodim:
        f.append({"severity": "Medio", "issue": "%d de %d imágenes sin width/height" % (nodim, n), "fix": "Declarar dimensiones para reservar espacio y evitar saltos (CLS)"})
    if count("loading=lazy (daña"):
        f.append({"severity": "Alto", "issue": "La imagen principal usa lazy loading", "fix": "Quitar loading=lazy del hero; añadir fetchpriority=high"})
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("urls", nargs="*", help="páginas a auditar (una por plantilla)")
    ap.add_argument("--file", help="archivo con una URL por línea")
    ap.add_argument("--max-imagenes", type=int, default=40, help="imágenes máx. por página (defecto 40)")
    ap.add_argument("--delay", type=float, default=0.4)
    ap.add_argument("--site", help="dominio para volcar a .seo-audit/<sitio>/data/imagenes.json")
    ap.add_argument("--root", default=".")
    a = ap.parse_args()
    urls = list(a.urls)
    if a.file:
        with open(a.file, encoding="utf-8") as fh:
            urls += [l.strip() for l in fh if l.strip() and not l.startswith("#")]
    fb = "modo manual: Screaming Frog > pestaña Images (filtra por 'Over 100 kb' y 'Missing Alt Text') o PageSpeed Insights > 'Sirve imágenes con formatos modernos'"
    if not urls:
        print(json.dumps({"ok": False, "reason": "sin URLs", "fallback": fb}))
        return
    robots = None
    try:
        p0 = urlparse(urls[0])
        robots = urllib.robotparser.RobotFileParser()
        st, _, body, err = fetch("%s://%s/robots.txt" % (p0.scheme, p0.netloc), "GET", 500000)
        robots.parse(body.decode("utf-8", "replace").splitlines() if st == 200 else [])
    except Exception:
        robots = None
    pages = []
    for i, u in enumerate(urls[:15]):
        if i:
            time.sleep(a.delay)
        pages.append(audit_page(u, a.max_imagenes, a.delay, robots))
    if all(p.get("error") for p in pages):
        print(json.dumps({"ok": False, "reason": pages[0]["error"], "pages": pages, "fallback": fb}, ensure_ascii=False))
        return
    out = {"ok": True, "pages": pages, "truncated": len(urls) > 15,
           "note": "El peso sale de los encabezados del servidor (HEAD). Es el peso transferido real, no una estimación."}
    if a.site:
        d = os.path.join(a.root, ".seo-audit", a.site, "data")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "imagenes.json"), "w", encoding="utf-8") as fh:
            json.dump(out, fh, ensure_ascii=False, indent=2)
        out["written"] = os.path.join(d, "imagenes.json")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
