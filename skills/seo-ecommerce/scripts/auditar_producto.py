#!/usr/bin/env python3
"""Audita la ficha de producto de una tienda (un solo fetch).

Método del diploma "De Cero a SEO" (Semana 14, SEO de ecommerce): título con la
keyword, descripción persuasiva, FAQ, prueba social y alt text. Los criterios de
schema Product vienen de references/complementos-claude-seo.md (complemento externo).

Revisa: título y meta (longitud), H1 único, canónica, JSON-LD Product (campos
obligatorios y recomendados, precio numérico, disponibilidad como URL), BreadcrumbList,
imágenes sin alt y señal de FAQ.

Salida (stdout, JSON): {"ok": true, "url", "title", "meta", "h1", "canonical",
"producto": {...}, "hallazgos": [{"severidad","mensaje"}]}
Si hay 403/WAF: {"ok": false, "fallback": "modo manual: ..."}.
Solo stdlib. Respeta robots.txt. Con --sitio guarda .seo-audit/<sitio>/data/ecommerce.json.
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from html.parser import HTMLParser

UA = os.environ.get(
    "SEO_USER_AGENT",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
)


class Pagina(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title, self.h1, self.meta, self.canonical = "", [], "", ""
        self.imgs_total, self.imgs_sin_alt = 0, 0
        self.ld, self._buf, self._en = [], "", None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("title", "h1"):
            self._en, self._buf = tag, ""
        elif tag == "meta" and (a.get("name") or "").lower() == "description":
            self.meta = a.get("content") or ""
        elif tag == "link" and "canonical" in (a.get("rel") or "").lower():
            self.canonical = a.get("href") or ""
        elif tag == "img":
            self.imgs_total += 1
            if not (a.get("alt") or "").strip():
                self.imgs_sin_alt += 1
        elif tag == "script" and "ld+json" in (a.get("type") or "").lower():
            self._en, self._buf = "ld", ""

    def handle_data(self, data):
        if self._en:
            self._buf += data

    def handle_endtag(self, tag):
        if self._en == tag or (self._en == "ld" and tag == "script"):
            if self._en == "title":
                self.title = self._buf.strip()
            elif self._en == "h1":
                self.h1.append(self._buf.strip())
            elif self._en == "ld":
                try:
                    self.ld.append(json.loads(self._buf.strip()))
                except ValueError:
                    pass
            self._en = None


def permitido(url):
    p = urllib.parse.urlparse(url)
    rp = urllib.robotparser.RobotFileParser()
    try:
        req = urllib.request.Request(f"{p.scheme}://{p.netloc}/robots.txt", headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=15) as r:
            rp.parse(r.read().decode("utf-8", "replace").splitlines())
    except (urllib.error.URLError, OSError):
        return True
    return rp.can_fetch(UA, url)


def buscar_tipo(nodo, tipo, salida):
    if isinstance(nodo, list):
        for x in nodo:
            buscar_tipo(x, tipo, salida)
    elif isinstance(nodo, dict):
        t = nodo.get("@type")
        if t == tipo or (isinstance(t, list) and tipo in t):
            salida.append(nodo)
        for v in nodo.values():
            buscar_tipo(v, tipo, salida)


def revisar_producto(prod, h):
    def add(sev, msg):
        h.append({"severidad": sev, "mensaje": msg})

    for campo in ("name", "image", "offers"):
        if not prod.get(campo):
            add("Alto", f"Product sin '{campo}' (obligatorio).")
    for campo in ("description", "sku", "brand"):
        if not prod.get(campo):
            add("Bajo", f"Product sin '{campo}' (recomendado).")
    if not (prod.get("gtin") or prod.get("gtin13") or prod.get("gtin14") or prod.get("mpn")):
        add("Bajo", "Product sin gtin ni mpn (recomendado).")
    ofertas = prod.get("offers") or []
    ofertas = ofertas if isinstance(ofertas, list) else [ofertas]
    for o in ofertas:
        if not isinstance(o, dict):
            continue
        if o.get("@type") == "AggregateOffer":
            add("Medio", "Usa 'Offer' y no 'AggregateOffer' en un listado de comerciante.")
        precio = str(o.get("price", ""))
        if not precio:
            add("Alto", "Offer sin 'price'.")
        elif not re.fullmatch(r"\d+([.,]\d+)?", precio):
            add("Medio", f"'price' debe ser numérico sin símbolo de moneda: '{precio}'.")
        if not o.get("priceCurrency"):
            add("Alto", "Offer sin 'priceCurrency' (ISO 4217).")
        disp = str(o.get("availability", ""))
        if not disp.startswith("https://schema.org/") and not disp.startswith("http://schema.org/"):
            add("Medio", "'availability' debe ser la URL completa de schema.org (por ejemplo https://schema.org/InStock).")
    rating = prod.get("aggregateRating")
    if isinstance(rating, dict) and not (rating.get("ratingValue") and (rating.get("reviewCount") or rating.get("ratingCount"))):
        add("Medio", "aggregateRating requiere ratingValue y reviewCount.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url", help="URL de la ficha de producto")
    ap.add_argument("--sitio", help="Dominio; escribe .seo-audit/<sitio>/data/ecommerce.json")
    ap.add_argument("--raiz", default=".", help="Raíz donde vive .seo-audit")
    args = ap.parse_args()

    if not permitido(args.url):
        print(json.dumps({"ok": False, "reason": "robots.txt no permite rastrear esta URL.",
                          "fallback": "modo manual: revisa la ficha con el checklist de SKILL.md."}, ensure_ascii=False))
        return 0
    try:
        req = urllib.request.Request(args.url, headers={"User-Agent": UA, "Accept-Language": "es,en;q=0.8"})
        with urllib.request.urlopen(req, timeout=20) as r:
            html = r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        motivo = "El sitio rechazó la petición (posible WAF/anti-bot)." if exc.code in (403, 429) else f"HTTP {exc.code}"
        print(json.dumps({"ok": False, "reason": motivo,
                          "fallback": "modo manual: usa el checklist de SKILL.md o un export de Screaming Frog."}, ensure_ascii=False))
        return 0
    except (urllib.error.URLError, OSError) as exc:
        print(json.dumps({"ok": False, "reason": str(exc), "fallback": "modo manual: revisa la URL."}, ensure_ascii=False))
        return 0

    p = Pagina()
    p.feed(html)
    hallazgos = []

    def add(sev, msg):
        hallazgos.append({"severidad": sev, "mensaje": msg})

    if not p.title:
        add("Alto", "Falta la etiqueta title.")
    elif not 30 <= len(p.title) <= 60:
        add("Bajo", f"Title de {len(p.title)} caracteres; apunta a 50-60 con la keyword al inicio.")
    if not p.meta:
        add("Medio", "Falta la meta descripción (transaccional: atributo, precio o envío).")
    elif not 120 <= len(p.meta) <= 155:
        add("Bajo", f"Meta descripción de {len(p.meta)} caracteres; apunta a 120-155.")
    if len(p.h1) == 0:
        add("Alto", "No hay H1.")
    elif len(p.h1) > 1:
        add("Medio", f"Hay {len(p.h1)} H1; debe haber uno solo con el nombre del producto.")
    if not p.canonical:
        add("Medio", "No hay canonical (en Shopify se añade en el tema con canonical_url).")
    if p.imgs_sin_alt:
        add("Medio", f"{p.imgs_sin_alt} de {p.imgs_total} imágenes sin alt.")

    productos, migas = [], []
    for bloque in p.ld:
        buscar_tipo(bloque, "Product", productos)
        buscar_tipo(bloque, "BreadcrumbList", migas)
    if not productos:
        add("Alto", "No hay JSON-LD Product: genera el bloque con la skill schema-jsonld (solo con datos visibles).")
    for prod in productos[:1]:
        revisar_producto(prod, hallazgos)
    if not migas:
        add("Bajo", "No hay BreadcrumbList en la ficha (migas de pan).")
    if not re.search(r"preguntas frecuentes|faq|\?</", html, re.I):
        add("Bajo", "No se detecta sección de preguntas frecuentes en la ficha.")

    resultado = {"ok": True, "url": args.url, "title": p.title, "meta": p.meta, "h1": p.h1,
                 "canonical": p.canonical, "imagenes": {"total": p.imgs_total, "sin_alt": p.imgs_sin_alt},
                 "producto": productos[0] if productos else None, "hallazgos": hallazgos}
    if args.sitio:
        carpeta = os.path.join(args.raiz, ".seo-audit", args.sitio, "data")
        os.makedirs(carpeta, exist_ok=True)
        with open(os.path.join(carpeta, "ecommerce.json"), "w", encoding="utf-8") as fh:
            json.dump(resultado, fh, ensure_ascii=False, indent=2)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
