#!/usr/bin/env python3
"""
validate_schema.py: valida el JSON-LD de una URL, un archivo HTML o un archivo .json.

Complemento externo adaptado de claude-seo (MIT, agricidaniel), reescrito con
solo stdlib. No sustituye al Rich Results Test de Google: detecta errores
frecuentes ANTES de pegar el bloque (placeholders, URLs relativas, fechas mal
formadas, tipos retirados, propiedades requeridas ausentes).

Uso:
    python3 validate_schema.py --url https://ejemplo.com/pagina
    python3 validate_schema.py --file pagina.html
    python3 validate_schema.py --file bloque.json
    python3 validate_schema.py --url https://ejemplo.com --out .seo-audit/ejemplo.com/data/schema-validation.json

Salida (stdout, JSON):
    {"ok": true, "source": "...", "blocks": N, "types": [...],
     "findings": [{"severity": "Alto|Medio|Info", "type": "...", "rule": "...", "detail": "..."}],
     "summary": {"Alto": n, "Medio": n, "Info": n}}
Si falla: {"ok": false, "reason": "...", "fallback": "modo manual: Rich Results Test"} (exit 0).
Con --out escribe el mismo JSON (convencion .seo-audit/<sitio>/data/*.json).

Deps: solo stdlib. Descarga con User-Agent de navegador y detecta WAF basico.
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

# Tipos sin rich result en Google (verificado contra la documentacion de Google
# y la tabla de claude-seo, junio 2026). Severidad Info: el marcado no rompe nada.
RETIRED = {
    "HowTo": "Rich result retirado en septiembre de 2023. No lo uses esperando efecto en la SERP.",
    "FAQPage": "Rich result retirado para todos los sitios el 7 de mayo de 2026. Sin efecto en la SERP de Google; "
               "el diplomado (S14 L13) lo recomienda para que los motores de IA identifiquen preguntas, "
               "y eso no lo confirma Google. Mantenlo solo si las preguntas son visibles.",
    "SpecialAnnouncement": "Deprecado el 31 de julio de 2025. Sin reemplazo directo (usa Event o Article).",
    "ClaimReview": "Rich result retirado en junio de 2025.",
    "VehicleListing": "Rich result retirado en junio de 2025 (usa Product).",
    "EstimatedSalary": "Rich result retirado en junio de 2025 (usa JobPosting con baseSalary).",
    "LearningVideo": "Rich result retirado en junio de 2025 (usa VideoObject).",
    "CourseInfo": "El carrusel de Course Info se retiro en junio de 2025; la tarjeta Course sigue activa.",
    "PracticeProblem": "Soporte retirado en enero de 2026.",
}

# Propiedades requeridas por tipo (minimo util; Google puede exigir mas por rich result).
REQUIRED = {
    "Article": ["headline"], "BlogPosting": ["headline"], "NewsArticle": ["headline"],
    "Product": ["name"], "Organization": ["name"], "LocalBusiness": ["name", "address"],
    "WebSite": ["name", "url"], "BreadcrumbList": ["itemListElement"],
    "FAQPage": ["mainEntity"], "QAPage": ["mainEntity"], "HowTo": ["name", "step"],
    "Event": ["name", "startDate", "location"], "JobPosting": ["title", "datePosted", "hiringOrganization"],
    "VideoObject": ["name", "thumbnailUrl", "uploadDate"], "Person": ["name"],
    "Course": ["name", "description"], "Review": ["itemReviewed", "author"],
}

PLACEHOLDER = re.compile(r"(\[[A-Za-z ]{3,}\]|lorem ipsum|ejemplo\.com|example\.com|tu[- ]sitio|your[- ]?(site|company)|xxx+|TODO)", re.I)
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}([T ]\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:?\d{2})?)?$")
URL_KEYS = {"url", "logo", "image", "sameAs", "@id", "mainEntityOfPage", "thumbnailUrl", "contentUrl"}
DATE_KEYS = {"datePublished", "dateModified", "startDate", "endDate", "datePosted", "uploadDate", "validThrough"}


class LD(HTMLParser):
    def __init__(self):
        super().__init__()
        self.blocks, self._in, self._buf, self.micro = [], False, [], False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "script" and (a.get("type") or "").lower() == "application/ld+json":
            self._in, self._buf = True, []
        if "itemscope" in a:
            self.micro = True

    def handle_data(self, data):
        if self._in:
            self._buf.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self._in:
            self.blocks.append("".join(self._buf))
            self._in = False


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read().decode(r.headers.get_content_charset() or "utf-8", "replace")
    except urllib.error.HTTPError as e:
        if e.code in (403, 429, 503):
            raise RuntimeError(f"HTTP {e.code}: posible WAF o bloqueo. Pega el HTML o usa --file.")
        raise RuntimeError(f"HTTP {e.code}")
    except Exception as e:  # noqa: BLE001
        raise RuntimeError(str(e))


def walk(node, path, fn):
    if isinstance(node, dict):
        fn(node, path)
        for k, v in node.items():
            walk(v, f"{path}.{k}", fn)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, f"{path}[{i}]", fn)


def types_of(d):
    t = d.get("@type")
    return [t] if isinstance(t, str) else [x for x in (t or []) if isinstance(x, str)]


def validate_block(data, idx, findings, seen):
    top = data if isinstance(data, list) else [data]
    if isinstance(data, dict) and "@graph" in data:
        top = data["@graph"]
    for item in top:
        if not isinstance(item, dict):
            continue
        if "@context" not in item and not (isinstance(data, dict) and "@context" in data):
            findings.append(("Alto", "?", "sin-context", f"Bloque {idx}: falta @context (https://schema.org)."))

    def check(d, path):
        ts = types_of(d)
        for t in ts:
            seen.add(t)
            if t in RETIRED:
                findings.append(("Info", t, "tipo-retirado", f"{path}: {RETIRED[t]}"))
            for req in REQUIRED.get(t, []):
                if d.get(req) in (None, "", [], {}):
                    findings.append(("Alto", t, "requerida-ausente", f"{path}: falta la propiedad requerida '{req}'."))
            if t in ("FAQPage", "HowTo"):
                findings.append(("Medio", t, "solo-lo-visible",
                                 f"{path}: confirma que las preguntas o pasos se ven en la pagina. Marcar lo que no existe es spam."))
        if not ts and "@type" in d and not d["@type"]:
            findings.append(("Alto", "?", "type-vacio", f"{path}: @type vacio."))
        for k, v in d.items():
            if isinstance(v, str):
                if PLACEHOLDER.search(v):
                    findings.append(("Alto", ",".join(ts) or "?", "placeholder", f"{path}.{k}: texto de relleno ('{v[:50]}')."))
                if k in URL_KEYS and v and not v.startswith(("http://", "https://", "#", "mailto:", "tel:")) and k != "@id":
                    findings.append(("Medio", ",".join(ts) or "?", "url-relativa", f"{path}.{k}: usa URL absoluta ('{v[:60]}')."))
                if k in DATE_KEYS and not ISO_DATE.match(v):
                    findings.append(("Medio", ",".join(ts) or "?", "fecha-invalida", f"{path}.{k}: formato ISO 8601 esperado ('{v}')."))
            if k == "aggregateRating" and isinstance(v, dict):
                if not v.get("ratingValue") or not (v.get("reviewCount") or v.get("ratingCount")):
                    findings.append(("Alto", ",".join(ts) or "?", "rating-incompleto",
                                     f"{path}.aggregateRating: necesita ratingValue y reviewCount, y reseñas reales y visibles."))

    walk(data, f"bloque{idx}", check)


def main():
    p = argparse.ArgumentParser(description="Valida JSON-LD (URL, HTML o JSON) con solo stdlib.")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--url", help="URL a descargar.")
    g.add_argument("--file", help="Archivo .html o .json local.")
    p.add_argument("--out", help="Ruta donde escribir el JSON (ej. .seo-audit/<sitio>/data/schema-validation.json).")
    args = p.parse_args()

    def fail(reason):
        print(json.dumps({"ok": False, "reason": reason,
                          "fallback": "modo manual: Rich Results Test y validator.schema.org"}, ensure_ascii=False))
        sys.exit(0)

    try:
        if args.url:
            text, source = fetch(args.url), args.url
        else:
            with open(args.file, encoding="utf-8") as f:
                text, source = f.read(), args.file
    except (RuntimeError, OSError) as e:
        fail(str(e))

    raw_blocks, micro = [], False
    if args.file and args.file.lower().endswith(".json"):
        raw_blocks = [text]
    else:
        lp = LD()
        lp.feed(text)
        raw_blocks, micro = lp.blocks, lp.micro

    findings, seen = [], set()
    for i, rb in enumerate(raw_blocks, 1):
        try:
            validate_block(json.loads(rb), i, findings, seen)
        except json.JSONDecodeError as e:
            findings.append(("Alto", "?", "json-invalido", f"bloque{i}: JSON mal formado ({e.msg}, linea {e.lineno})."))
    if not raw_blocks:
        findings.append(("Info", "-", "sin-jsonld",
                         "No se encontro JSON-LD" + (" (hay Microdata; se prefiere JSON-LD)." if micro else ".")))

    summary = {"Alto": 0, "Medio": 0, "Info": 0}
    out_f = []
    for sev, t, rule, detail in findings:
        summary[sev] += 1
        out_f.append({"severity": sev, "type": t, "rule": rule, "detail": detail})
    res = {"ok": True, "source": source, "blocks": len(raw_blocks), "types": sorted(seen),
           "findings": out_f, "summary": summary,
           "note": "Validacion estatica. Confirma siempre en Rich Results Test y en el informe de Mejoras de GSC."}
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False, indent=2)
    print(json.dumps(res, ensure_ascii=False))


if __name__ == "__main__":
    main()
