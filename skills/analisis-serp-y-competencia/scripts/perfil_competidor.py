#!/usr/bin/env python3
"""
perfil_competidor.py, Perfil de cada página del top de una SERP (solo stdlib).

Qué hace (determinista):
  Por cada URL del top de una SERP extrae lo que se ve en el HTML original:
  título, meta description, H1 a H3 en orden, palabras, tipo de página, schema
  JSON-LD, imágenes (con alt), enlaces internos y externos, fecha, señales de
  autoría y E-E-A-T, uso de FAQ, listas, tablas y vídeo, y si el contenido
  depende de JavaScript. Es el paso "Ojo Clínico" hecho dato; no lo reemplaza
  (el diplomado pide mirar el top 3 a ojo primero, Semana 6 · lección 2).

Entradas (combinables):
  - URLs sueltas como argumentos.
  - --urls-file archivo.txt        una URL por línea.
  - --serp-json serp.json [...]    salida de serp.py (usa top[].link y query).
  - --html archivo.html            HTML guardado (modo sin red). Formato
                                   `URL=archivo.html` para asociarlo a una URL
                                   de la SERP; sin URL, usa el canonical.
  - --own-url / --own-html         tu propia página, rol "own".

Rastreo (solo con URLs sin HTML guardado):
  - User-Agent de navegador real (SEO_USER_AGENT lo sobreescribe).
  - Respeta robots.txt (si un robots.txt prohíbe la URL, la salta y lo dice).
    --ignorar-robots solo para sitios propios.
  - Ritmo: --pausa segundos entre peticiones (por defecto 2).
  - Detección de WAF (403, 429, 503 con página de desafío): devuelve blocked.

Uso:
  python3 perfil_competidor.py https://a.com/x https://b.com/y --out perfiles.json
  python3 perfil_competidor.py --serp-json serp1.json serp2.json --own-url https://mio.com/p
  python3 perfil_competidor.py --serp-json s.json --html https://a.test/x=a.html --sin-red

Salida (JSON a stdout o --out):
  {"ok": true, "profiles": [{...}], "errors": [...], "blocked": false, "notes": [...]}
  Si nada se pudo perfilar: {"ok": false, "reason": "...", "fallback": "modo manual: ..."} (exit 0).

Deps: solo stdlib.
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen
from urllib.robotparser import RobotFileParser

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
TIMEOUT = 20
MAX_BYTES = 3_000_000

TWO_PART_SLDS = {"co", "com", "org", "net", "gov", "edu", "ac"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
        "param", "source", "track", "wbr"}
SKIP_TEXT = {"script", "style", "noscript", "template", "svg", "head"}
BOILER = {"nav", "header", "footer", "aside", "form"}
WAF_MARKERS = ("just a moment", "attention required", "cf-chl", "captcha",
               "access denied", "request unsuccessful", "verify you are human",
               "enable javascript and cookies")
SPA_ROOTS = {"root", "app", "__next", "__nuxt", "___gatsby", "svelte"}

OWN_DATA_RE = re.compile(
    r"(nuestro estudio|hemos analizado|hemos probado|analizamos|datos propios|"
    r"nuestra encuesta|encuesta propia|caso real|caso de estudio|case study|"
    r"nuestros datos|en nuestras pruebas|probamos|testeamos|our study|we tested)",
    re.I)
EXPERIENCE_RE = re.compile(
    r"(en mi experiencia|llevo \d+ años|tras \d+ años|años de experiencia|"
    r"he probado|mi método|nuestro equipo de|barista|tostador|certificad)", re.I)
SOURCE_RE = re.compile(r"(fuentes?:|según un estudio|referencias|bibliograf|segun un estudio)", re.I)
PRICE_RE = re.compile(r"(\d+[.,]\d{2}\s?(€|eur|usd|\$|mxn|ars|clp|cop)|(€|\$)\s?\d+[.,]?\d*)", re.I)
CTA_RE = re.compile(r"(añadir al carrito|agregar al carrito|comprar|add to cart|buy now|"
                    r"solicitar|reservar|pedir presupuesto|contratar|empieza|regístrate|suscríbete)", re.I)
STOPWORDS = set("""para como esta este estos estas entre desde sobre cuando donde porque tambien pueden puede
hacer cada todo todos todas otros otras mismo misma menos mucho muchos tiene tienen siempre durante hasta
antes despues cuanto cual cuales mejor mejores segun puedes debes debe ejemplo ademas aunque tener nuestro
nuestra nuestros nuestras haber sido cuyo cuya donde which about their there would these other""".split())
DATE_RE = re.compile(r"(\d{4})-(\d{2})-(\d{2})")


def log(msg):
    print(msg, file=sys.stderr)


def registered_domain(url):
    host = (urlparse(url).hostname or "").lower()
    if host.startswith("www."):
        host = host[4:]
    parts = host.split(".")
    if len(parts) >= 3 and len(parts[-1]) == 2 and parts[-2] in TWO_PART_SLDS:
        return ".".join(parts[-3:])
    if len(parts) >= 2:
        return ".".join(parts[-2:])
    return host


class PageParser(HTMLParser):
    """Recoge señales del HTML sin ejecutar JavaScript."""

    def __init__(self, base_url):
        super().__init__(convert_charrefs=True)
        self.base = base_url
        self.host = registered_domain(base_url) if base_url else ""
        self.stack = []
        self.title = ""
        self.meta = {}
        self.canonical = ""
        self.headings = []          # [(nivel, texto)]
        self._cur_heading = None
        self._in_title = False
        self.jsonld_raw = []
        self._in_jsonld = False
        self.images = 0
        self.images_alt = 0
        self.links_int = 0
        self.links_ext = 0
        self.links_ext_body = 0
        self.ext_domains = set()
        self.lists = 0
        self.list_items = 0
        self.tables = 0
        self.details = 0
        self.video_tags = 0
        self.video_embeds = 0
        self.forms = 0
        self.buttons_cta = 0
        self.times = []             # [(datetime_attr, es_modificado)]
        self.author_markup = False
        self.rel_author = False
        self.main_words = []
        self.all_words = []
        self.body_chars = 0
        self.script_tags = 0
        self.script_src = 0
        self.root_ids = set()
        self.has_main = False
        self.text_chunks = []
        self.price_hits = 0
        self.product_cards = 0
        self.class_hits = {"author": 0, "byline": 0, "comment": 0, "thread": 0}

    def _boiler_depth(self):
        return sum(1 for t in self.stack if t in BOILER)

    def _in_skip(self):
        return any(t in SKIP_TEXT for t in self.stack)

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if tag not in VOID:
            self.stack.append(tag)
        cls = (a.get("class", "") + " " + a.get("id", "")).lower()
        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            key = (a.get("name") or a.get("property") or a.get("itemprop") or "").lower()
            if key:
                self.meta[key] = a.get("content", "")
        elif tag == "link":
            if "canonical" in a.get("rel", "").lower():
                self.canonical = a.get("href", "")
        elif tag in ("h1", "h2", "h3"):
            self._cur_heading = [int(tag[1]), []]
        elif tag == "script":
            self.script_tags += 1
            if a.get("src"):
                self.script_src += 1
            if "ld+json" in a.get("type", "").lower():
                self._in_jsonld = True
                self.jsonld_raw.append("")
        elif tag == "img":
            self.images += 1
            if a.get("alt", "").strip():
                self.images_alt += 1
        elif tag == "a":
            href = a.get("href", "")
            if "author" in a.get("rel", "").lower():
                self.rel_author = True
            if href and not href.startswith(("#", "mailto:", "tel:", "javascript:")):
                full = urljoin(self.base, href) if self.base else href
                dom = registered_domain(full)
                if urlparse(full).scheme in ("http", "https"):
                    if self.host and dom == self.host:
                        self.links_int += 1
                    elif not self.host and not urlparse(href).netloc:
                        self.links_int += 1
                    else:
                        self.links_ext += 1
                        self.ext_domains.add(dom)
                        if self._boiler_depth() == 0:
                            self.links_ext_body += 1
                elif not urlparse(href).scheme:
                    self.links_int += 1
        elif tag in ("ul", "ol"):
            if self._boiler_depth() == 0:
                self.lists += 1
        elif tag == "li":
            if self._boiler_depth() == 0:
                self.list_items += 1
        elif tag == "table":
            self.tables += 1
        elif tag == "details":
            self.details += 1
        elif tag == "video":
            self.video_tags += 1
        elif tag == "iframe":
            src = a.get("src", "") + a.get("data-src", "")
            if re.search(r"youtube|youtu\.be|vimeo|wistia|loom|dailymotion", src, re.I):
                self.video_embeds += 1
        elif tag == "form":
            self.forms += 1
        elif tag in ("button", "a") and a.get("class", ""):
            if re.search(r"(btn|button|cta)", a.get("class", ""), re.I):
                self.buttons_cta += 1
        elif tag == "time":
            self.times.append((a.get("datetime", ""),
                               "modif" in cls or "updated" in cls or a.get("itemprop", "") == "dateModified"))
        elif tag == "main":
            self.has_main = True
        if tag == "div" and a.get("id", "").lower() in SPA_ROOTS:
            self.root_ids.add(a.get("id", "").lower())
        if tag in ("div", "section", "article", "li", "span", "p", "a") and cls:
            if re.search(r"\bauthor|autor", cls):
                self.author_markup = True
                self.class_hits["author"] += 1
            if "byline" in cls:
                self.class_hits["byline"] += 1
            if re.search(r"comment|comentario", cls):
                self.class_hits["comment"] += 1
            if re.search(r"thread|topic|hilo|forum|foro", cls):
                self.class_hits["thread"] += 1
            if re.search(r"product-card|product-item|producto|product__|grid-product|item-product", cls):
                self.product_cards += 1
        if a.get("itemprop", "").lower() == "author":
            self.author_markup = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag in ("h1", "h2", "h3") and self._cur_heading:
            txt = re.sub(r"\s+", " ", "".join(self._cur_heading[1])).strip()
            if txt:
                self.headings.append((self._cur_heading[0], txt))
            self._cur_heading = None
        elif tag == "script":
            self._in_jsonld = False
        if tag in self.stack:
            while self.stack:
                t = self.stack.pop()
                if t == tag:
                    break

    def handle_data(self, data):
        if self._in_title:
            self.title += data
            return
        if self._in_jsonld and self.jsonld_raw:
            self.jsonld_raw[-1] += data
            return
        if self._in_skip():
            return
        if self._cur_heading is not None:
            self._cur_heading[1].append(data)
        words = re.findall(r"[\wáéíóúüñÁÉÍÓÚÜÑ'-]+", data)
        if not words:
            return
        self.body_chars += len(data)
        self.all_words.extend(words)
        if self._boiler_depth() == 0:
            self.main_words.extend(words)
            self.text_chunks.append(data)
        if PRICE_RE.search(data):
            self.price_hits += 1


def read_text(path):
    with open(path, "rb") as fh:
        raw = fh.read()
    return decode(raw)


def decode(raw):
    for enc in ("utf-8", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", "replace")


def flatten_jsonld(obj, out):
    """Aplana @graph y listas; devuelve lista de nodos (dict)."""
    if isinstance(obj, list):
        for it in obj:
            flatten_jsonld(it, out)
    elif isinstance(obj, dict):
        if "@graph" in obj:
            flatten_jsonld(obj["@graph"], out)
        out.append(obj)
        for v in obj.values():
            if isinstance(v, (dict, list)):
                flatten_jsonld(v, out)
    return out


def types_of(node):
    t = node.get("@type")
    if isinstance(t, str):
        return [t]
    if isinstance(t, list):
        return [x for x in t if isinstance(x, str)]
    return []


def parse_date(text):
    if not text:
        return None
    m = DATE_RE.search(text)
    if not m:
        return None
    try:
        return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)), tzinfo=timezone.utc)
    except ValueError:
        return None


def classify_page(url, p, schema_types, words, h1_count):
    """Tipo de página por puntaje de señales. Devuelve (tipo, confianza, señales)."""
    sc = {k: 0.0 for k in ("blog", "landing", "ecommerce", "categoria", "herramienta", "video", "foro")}
    sig = {k: [] for k in sc}
    path = (urlparse(url).path or "/").lower()
    host = (urlparse(url).hostname or "").lower()
    st = {s.lower() for s in schema_types}

    def add(kind, pts, why):
        sc[kind] += pts
        sig[kind].append(why)

    # schema (señal más fiable)
    if st & {"product", "offer", "aggregateoffer"}:
        add("ecommerce", 4, "schema Product/Offer")
    if st & {"itemlist", "collectionpage", "offercatalog"}:
        add("categoria", 3, "schema ItemList/CollectionPage")
    if st & {"article", "blogposting", "newsarticle", "techarticle"}:
        add("blog", 3, "schema Article/BlogPosting")
    if st & {"howto"}:
        add("blog", 1, "schema HowTo")
    if st & {"softwareapplication", "webapplication", "mobileapplication"}:
        add("herramienta", 3, "schema SoftwareApplication/WebApplication")
    if st & {"videoobject"}:
        add("video", 2, "schema VideoObject")
    if st & {"discussionforumposting", "qapage", "question"}:
        add("foro", 3, "schema DiscussionForumPosting/QAPage")
    if st & {"service", "localbusiness", "professionalservice"}:
        add("landing", 2, "schema Service/LocalBusiness")

    # URL y dominio
    if re.search(r"/(blog|articulos?|noticias|guias?|guia|recursos|magazine|post)/", path):
        add("blog", 2, "ruta /blog/ o similar")
    if re.search(r"/(categoria|categorias|collections?|coleccion|c|shop|tienda|catalogo)/", path):
        add("categoria", 2, "ruta de categoría o colección")
    if re.search(r"/(producto|productos|product|products|p|item)/", path):
        add("ecommerce", 2, "ruta de producto")
    if re.search(r"/(herramienta|herramientas|tool|tools|calculadora|calculator|generador)/?", path):
        add("herramienta", 2, "ruta de herramienta o calculadora")
    if re.search(r"/(foro|foros|forum|hilo|thread|topic|comunidad|questions?)/", path) or \
            re.search(r"(^|\.)(reddit|quora|forocoches|stackexchange|stackoverflow)\.", host):
        add("foro", 3, "ruta o dominio de foro")
    if re.search(r"(^|\.)(youtube|youtu|vimeo|tiktok)\.", host) or "/watch" in path:
        add("video", 4, "dominio o ruta de vídeo")

    # contenido
    if p.price_hits >= 1 and p.buttons_cta + len(CTA_RE.findall(" ".join(p.text_chunks[:400]))) >= 1 \
            and p.product_cards < 3:
        add("ecommerce", 2, "precio visible más botón de compra")
    if p.product_cards >= 3 or (p.price_hits >= 4 and p.list_items >= 6):
        add("categoria", 3, "varias tarjetas o precios de producto")
    if p.meta.get("og:type", "").lower() == "article":
        add("blog", 2, "og:type article")
    if p.meta.get("og:type", "").lower() in ("product", "og:product"):
        add("ecommerce", 2, "og:type product")
    if p.meta.get("og:type", "").lower().startswith("video"):
        add("video", 2, "og:type video")
    if words >= 700 and p.author_markup:
        add("blog", 1, "texto largo con autor")
    if words >= 500 and not p.price_hits:
        add("blog", 1, "texto largo sin precios")
    elif words >= 200 and not p.price_hits and not p.product_cards:
        add("blog", 1, "texto informativo sin precios (señal débil)")
    if p.class_hits["comment"] >= 2 or (p.class_hits["thread"] >= 2 and p.class_hits["comment"] >= 1):
        add("foro", 2, "comentarios o hilo en el marcado")
    if p.forms and words < 500 and not p.price_hits:
        add("landing", 1, "formulario y poco texto")
    if words < 600 and (p.buttons_cta >= 2 or CTA_RE.search(" ".join(p.text_chunks[:200]))) \
            and not p.price_hits:
        add("landing", 2, "llamado a la acción y poco texto")
    if p.video_tags + p.video_embeds >= 1 and words < 250:
        add("video", 2, "vídeo principal y poco texto")
    if p.forms and re.search(r"(calcula|calculadora|simulador|convertidor|generador)", p.title.lower()):
        add("herramienta", 2, "formulario con título de herramienta")

    best = max(sc, key=lambda k: sc[k])
    if sc[best] <= 0:
        return "otro", "baja", ["sin señales claras"]
    ordered = sorted(sc.values(), reverse=True)
    margin = ordered[0] - ordered[1]
    conf = "alta" if (sc[best] >= 4 and margin >= 2) else ("media" if sc[best] >= 3 else "baja")
    return best, conf, sig[best]


def build_profile(url, html, role="competitor", keyword=None, position=None, fetch_info=None):
    p = PageParser(url or "")
    try:
        p.feed(html)
        p.close()
    except Exception as e:  # noqa: BLE001 - HTML roto: seguimos con lo recogido
        log(f"HTML con errores en {url}: {e}")

    schema_types, schema_nodes, jsonld_errors = [], [], 0
    for raw in p.jsonld_raw:
        raw = raw.strip()
        if not raw:
            continue
        try:
            nodes = flatten_jsonld(json.loads(raw), [])
        except json.JSONDecodeError:
            jsonld_errors += 1
            continue
        for n in nodes:
            schema_nodes.append(n)
            for t in types_of(n):
                if t not in schema_types:
                    schema_types.append(t)

    words = len(p.main_words) if p.main_words else len(p.all_words)
    text = " ".join(p.text_chunks)
    h1s = [t for lvl, t in p.headings if lvl == 1]

    # fechas
    published = modified = None
    for n in schema_nodes:
        if not published:
            published = parse_date(str(n.get("datePublished", "")))
        if not modified:
            modified = parse_date(str(n.get("dateModified", "")))
    published = published or parse_date(p.meta.get("article:published_time", "")) \
        or parse_date(p.meta.get("datepublished", "")) or parse_date(p.meta.get("date", ""))
    modified = modified or parse_date(p.meta.get("article:modified_time", "")) \
        or parse_date(p.meta.get("og:updated_time", "")) or parse_date(p.meta.get("datemodified", ""))
    for dt, is_mod in p.times:
        d = parse_date(dt)
        if d:
            if is_mod and not modified:
                modified = d
            elif not is_mod and not published:
                published = d

    # autoría y E-E-A-T
    author_name = None
    for n in schema_nodes:
        au = n.get("author")
        if isinstance(au, dict) and au.get("name"):
            author_name = str(au["name"])
        elif isinstance(au, list) and au and isinstance(au[0], dict) and au[0].get("name"):
            author_name = str(au[0]["name"])
        elif isinstance(au, str):
            author_name = au
        if author_name:
            break
    author_name = author_name or p.meta.get("author") or None
    has_author = bool(author_name or p.author_markup or p.rel_author)
    has_date = bool(published or modified)
    has_sources = p.links_ext_body >= 2 or bool(SOURCE_RE.search(text))
    own_data = bool(OWN_DATA_RE.search(text))
    experience = bool(EXPERIENCE_RE.search(text))
    has_about_link = bool(re.search(r"(sobre nosotros|quiénes somos|about us|about)", text, re.I)) \
        and p.links_int > 0

    # formatos
    faq_schema = any(t.lower() == "faqpage" for t in schema_types)
    faq_heading = any(re.search(r"(preguntas frecuentes|faq|dudas frecuentes|preguntas y respuestas)",
                                t, re.I) for _, t in p.headings)
    faq = faq_schema or faq_heading or p.details >= 3
    # JavaScript
    spa_marker = bool(p.root_ids)
    js_dep = bool(
        (words < 60 and (p.script_tags >= 3 or spa_marker))
        or (words < 120 and spa_marker and p.script_src >= 2)
        or "noscript" in html.lower() and words < 40 and p.script_tags >= 2
    )

    ptype, conf, signals = classify_page(url or "", p, schema_types, words, len(h1s))
    if js_dep:
        conf = "baja"
        signals = signals + ["HTML original casi vacío: el tipo puede cambiar al renderizar"]

    h = [{"level": lvl, "text": t} for lvl, t in p.headings]
    freq = {}
    for w in p.main_words:
        k = re.sub(r"[^\wáéíóúüñ]", "", w.lower())
        if len(k) >= 5 and k not in STOPWORDS and not k.isdigit():
            freq[k] = freq.get(k, 0) + 1
    top_terms = [k for k, _ in sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))[:40]]
    now = datetime.now(timezone.utc)
    ref = modified or published
    age_days = (now - ref).days if ref else None

    profile = {
        "url": url,
        "domain": registered_domain(url) if url else "",
        "role": role,
        "keyword": keyword,
        "position": position,
        "title": re.sub(r"\s+", " ", p.title).strip(),
        "meta_description": re.sub(r"\s+", " ", p.meta.get("description", "")).strip(),
        "canonical": p.canonical,
        "h1": h1s,
        "headings": h,
        "counts": {
            "h1": len(h1s),
            "h2": sum(1 for x in h if x["level"] == 2),
            "h3": sum(1 for x in h if x["level"] == 3),
        },
        "word_count": words,
        "top_terms": top_terms,
        "page_type": ptype,
        "page_type_confidence": conf,
        "page_type_signals": signals,
        "schema_types": schema_types,
        "schema_jsonld_errors": jsonld_errors,
        "images": {"total": p.images, "with_alt": p.images_alt},
        "links": {"internal": p.links_int, "external": p.links_ext,
                  "external_in_body": p.links_ext_body,
                  "external_domains": sorted(p.ext_domains)[:30]},
        "dates": {"published": published.date().isoformat() if published else None,
                  "modified": modified.date().isoformat() if modified else None,
                  "age_days": age_days},
        "eeat": {
            "author": has_author, "author_name": author_name,
            "date_visible": has_date, "sources_cited": has_sources,
            "own_data": own_data, "first_hand_experience": experience,
            "about_or_org_schema": has_about_link or bool(
                {"organization", "person", "localbusiness"} & {s.lower() for s in schema_types}),
        },
        "formats": {
            "faq": faq, "faq_schema": faq_schema,
            "lists": p.lists, "list_items": p.list_items,
            "tables": p.tables,
            "video": (p.video_tags + p.video_embeds) > 0,
            "forms": p.forms,
        },
        "javascript_dependent": js_dep,
        "fetch": fetch_info or {"mode": "html"},
    }
    return profile


# ---------- Red ----------

FETCH_ERRORS = []
ROBOTS_CACHE = {}


def robots_allows(url, ignore):
    if ignore:
        return True
    p = urlparse(url)
    base = f"{p.scheme}://{p.netloc}"
    if base not in ROBOTS_CACHE:
        rp = RobotFileParser()
        try:
            req = Request(base + "/robots.txt", headers=BROWSER_HEADERS)
            with urlopen(req, timeout=TIMEOUT) as resp:
                rp.parse(decode(resp.read(500_000)).splitlines())
        except HTTPError as e:
            # 4xx en robots.txt = sin restricciones; 5xx = prudencia, permitimos y avisamos
            rp = None
            if e.code >= 500:
                log(f"robots.txt devolvió {e.code} en {base}; se continúa con prudencia")
        except Exception:  # noqa: BLE001
            rp = None
        ROBOTS_CACHE[base] = rp
    rp = ROBOTS_CACHE[base]
    if rp is None:
        return True
    return rp.can_fetch(USER_AGENT, url) or rp.can_fetch("*", url)


def fetch(url):
    """Devuelve (html, info, error). info: status, final_url, bytes, waf."""
    try:
        req = Request(url, headers=BROWSER_HEADERS)
        with urlopen(req, timeout=TIMEOUT) as resp:
            raw = resp.read(MAX_BYTES)
            status = resp.status
            final = resp.geturl()
        html = decode(raw)
        low = html[:4000].lower()
        waf = any(m in low for m in WAF_MARKERS) and len(html) < 20000
        return html, {"mode": "red", "status": status, "final_url": final,
                      "bytes": len(raw), "waf_suspected": waf}, None
    except HTTPError as e:
        FETCH_ERRORS.append(f"{url}: HTTP {e.code}")
        return None, {"mode": "red", "status": e.code}, f"HTTP {e.code}"
    except (URLError, TimeoutError, OSError) as e:
        FETCH_ERRORS.append(f"{url}: {e}")
        return None, {"mode": "red"}, str(e)


def looks_blocked():
    return any(("HTTP 403" in e) or ("HTTP 429" in e) or ("HTTP 503" in e) for e in FETCH_ERRORS)


# ---------- Entradas ----------

def load_serp(path):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    if isinstance(data, dict) and data.get("ok") is False:
        raise ValueError(f"{path}: serp.json con ok=false ({data.get('reason', '')})")
    q = data.get("query") or os.path.splitext(os.path.basename(path))[0]
    items = []
    for i, it in enumerate(data.get("top", []), 1):
        link = it.get("link") or it.get("url")
        if link:
            items.append((link, q, it.get("position") or i))
    return items


def main():
    ap = argparse.ArgumentParser(
        description="Perfil de las páginas del top de una SERP (título, headings, palabras, tipo, "
                    "schema, E-E-A-T, formatos, dependencia de JS). Solo stdlib.")
    ap.add_argument("urls", nargs="*", help="URLs a perfilar")
    ap.add_argument("--urls-file", help="archivo con una URL por línea")
    ap.add_argument("--serp-json", nargs="+", default=[], help="salida(s) de serp.py")
    ap.add_argument("--top", type=int, default=10, help="máximo de resultados por SERP (default 10)")
    ap.add_argument("--keyword", help="keyword para las URLs sueltas")
    ap.add_argument("--html", nargs="+", default=[],
                    help="HTML guardado: archivo.html o URL=archivo.html (modo sin red)")
    ap.add_argument("--own-url", help="URL de tu propia página (rol own)")
    ap.add_argument("--own-html", help="HTML guardado de tu propia página")
    ap.add_argument("--own-label", default="https://propio.local/pagina",
                    help="URL ficticia para --own-html (default https://propio.local/pagina)")
    ap.add_argument("--sin-red", action="store_true",
                    help="no hace peticiones: las URLs sin HTML guardado se reportan como error")
    ap.add_argument("--pausa", type=float, default=2.0, help="segundos entre peticiones (default 2)")
    ap.add_argument("--ignorar-robots", action="store_true",
                    help="no consulta robots.txt (solo para sitios propios)")
    ap.add_argument("--out", help="escribe el JSON aquí además de imprimirlo")
    args = ap.parse_args()

    targets = []  # (url, keyword, position)
    for u in args.urls:
        targets.append((u, args.keyword, None))
    if args.urls_file:
        with open(args.urls_file, encoding="utf-8") as fh:
            for i, line in enumerate((l.strip() for l in fh), 1):
                if line and not line.startswith("#"):
                    targets.append((line, args.keyword, None))
    for sj in args.serp_json:
        try:
            for link, q, pos in load_serp(sj)[: args.top]:
                targets.append((link, q, pos))
        except (OSError, ValueError, json.JSONDecodeError) as e:
            print(json.dumps({"ok": False, "reason": str(e),
                              "fallback": "modo manual: pega las URLs del top de Google en incógnito"},
                             ensure_ascii=False))
            return

    saved = {}  # url -> ruta
    anon = []   # rutas sin URL
    for spec in args.html:
        if "=" in spec and re.match(r"^https?://", spec):
            u, f = spec.rsplit("=", 1)
            saved[u] = f
        else:
            anon.append(spec)

    profiles, errors, notes = [], [], []
    cache = {}
    fetched_any = False

    def profile_for(url, kw, pos, role="competitor"):
        nonlocal fetched_any
        key = (url, role)
        if key in cache:
            prof = json.loads(json.dumps(cache[key]))
            prof["keyword"], prof["position"] = kw, pos
            return prof
        if url in saved:
            try:
                html = read_text(saved[url])
            except OSError as e:
                errors.append({"url": url, "error": f"no se pudo leer {saved[url]}: {e}"})
                return None
            prof = build_profile(url, html, role, kw, pos, {"mode": "html", "file": saved[url]})
        elif args.sin_red:
            errors.append({"url": url, "error": "sin HTML guardado y --sin-red activo"})
            return None
        else:
            if not robots_allows(url, args.ignorar_robots):
                errors.append({"url": url, "error": "robots.txt no permite rastrear esta URL (se respeta)"})
                return None
            if fetched_any and args.pausa > 0:
                time.sleep(args.pausa)
            fetched_any = True
            html, info, err = fetch(url)
            if err or html is None:
                errors.append({"url": url, "error": err or "sin respuesta"})
                return None
            if info.get("waf_suspected"):
                errors.append({"url": url, "error": "posible desafío de WAF (página de verificación)"})
                FETCH_ERRORS.append(f"{url}: HTTP 403 (desafío)")
            prof = build_profile(url, html, role, kw, pos, info)
        cache[key] = prof
        return prof

    for url, kw, pos in targets:
        prof = profile_for(url, kw, pos)
        if prof:
            profiles.append(prof)

    for f in anon:
        try:
            html = read_text(f)
        except OSError as e:
            errors.append({"url": f, "error": str(e)})
            continue
        m = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)', html, re.I)
        url = m.group(1) if m else "file://" + os.path.abspath(f)
        profiles.append(build_profile(url, html, "competitor", args.keyword, None,
                                      {"mode": "html", "file": f}))

    if args.own_url:
        prof = profile_for(args.own_url, None, None, role="own")
        if prof:
            profiles.append(prof)
    if args.own_html:
        try:
            html = read_text(args.own_html)
            profiles.append(build_profile(args.own_label, html, "own", None, None,
                                          {"mode": "html", "file": args.own_html}))
        except OSError as e:
            errors.append({"url": args.own_html, "error": str(e)})

    blocked = looks_blocked()
    if blocked:
        notes.append("Hay respuestas 403/429/503: probable WAF o anti-bot. Si es tu sitio, permite tu rastreo "
                     "en el WAF; si no, guarda el HTML desde el navegador y usa --html, o exporta con "
                     "Screaming Frog (motor de navegador real). Prueba otro User-Agent con SEO_USER_AGENT.")
    js_pages = [p["url"] for p in profiles if p["javascript_dependent"]]
    if js_pages:
        notes.append("Páginas que dependen de JavaScript (HTML original casi vacío): sus conteos de palabras y "
                     "encabezados son parciales. Revísalas a ojo en el navegador (Ojo Clínico) o renderízalas "
                     "con un navegador real. URLs: " + ", ".join(js_pages))
    if not profiles:
        print(json.dumps({
            "ok": False, "blocked": blocked,
            "reason": "No se pudo perfilar ninguna URL." + (" " + "; ".join(e["error"] for e in errors[:3]) if errors else ""),
            "errors": errors,
            "fallback": "modo manual: abre cada URL del top en incógnito y anota título, H1 a H3, tipo de página, "
                        "palabras aproximadas, FAQ, tablas, vídeo y fecha en la tabla del Ojo Clínico; "
                        "o guarda el HTML y usa --html.",
        }, ensure_ascii=False, indent=2))
        return

    out = {"ok": True, "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "blocked": blocked, "profiles": profiles, "errors": errors, "notes": notes}
    text = json.dumps(out, ensure_ascii=False, indent=2)
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
    print(text)


if __name__ == "__main__":
    main()
