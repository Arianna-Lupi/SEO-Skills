"""Funciones compartidas por generar_master.py y generar_briefs.py (solo stdlib).

Convención de datos: .seo-audit/<sitio>/data/*.json (ver la skill dashboard-seo).
El mapa de contenidos vive en content-map.json:
  {"pages": [{"url", "url_estado": "existente|propuesta", "keyword", "secundarias": [],
     "intencion", "tipo": "Home|Categoría|Blog|Landing|Ecommerce", "cluster", "rol": "Pilar|Spoke",
     "accion": "Crear|Actualizar|Dejar|Eliminar", "impacto", "confianza", "facilidad",
     "volumen", "kd", "posicion", "h1", "meta_title", "meta_desc", "estado",
     "responsable", "mes", "fecha"}]}
Todo campo ausente se trata como `pendiente de dato`. Nunca se inventan cifras.
"""
import csv
import datetime as dt
import json
import os
import re
import unicodedata

PEND = "pendiente de dato"
INTENCIONES = ("Informacional", "Comercial", "Transaccional", "Navegacional")
TIPOS = ("Home", "Categoría", "Blog", "Landing", "Ecommerce")
ACCIONES = ("Crear", "Actualizar", "Dejar", "Eliminar")
ESTATUS = ("Pendiente", "En proceso", "En revisión", "Aprobado", "En vivo", "Terminado")
TIPOS_QUE_VENDEN = ("Landing", "Ecommerce", "Home", "Categoría")


def sin_acentos(t):
    return "".join(c for c in unicodedata.normalize("NFD", str(t)) if unicodedata.category(c) != "Mn")


def slug(t, largo=60):
    s = re.sub(r"[^a-z0-9]+", "-", sin_acentos(t).lower()).strip("-")
    return s[:largo].strip("-") or "pagina"


def norm_kw(t):
    """Forma canónica para detectar keywords repetidas o casi repetidas (orden y acentos)."""
    palabras = re.sub(r"[^a-z0-9 ]+", " ", sin_acentos(t).lower()).split()
    return " ".join(sorted(p for p in palabras if p not in ("de", "en", "la", "el", "los", "las", "para", "y", "a", "un", "una")))


def leer_json(ruta, defecto=None):
    try:
        with open(ruta, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return defecto


def cargar_datos(carpeta):
    """Lee los JSON de la convención de dashboard-seo; devuelve dict con los que existan."""
    nombres = ("meta", "keywords", "clusters", "issues", "competitors", "next-steps", "plan-seo", "content-map", "inventory-summary")
    datos = {n: leer_json(os.path.join(carpeta, n + ".json")) for n in nombres}
    return {k: v for k, v in datos.items() if v is not None}


def num(v):
    """Devuelve float o None. Acepta '260', '10-100', '<100', 'pendiente'."""
    if isinstance(v, (int, float)):
        return float(v)
    m = re.fullmatch(r"\s*(\d+(?:[.,]\d+)?)\s*", str(v or ""))
    return float(m.group(1).replace(",", ".")) if m else None


def ice(p):
    """Puntuación ICE = promedio de Impacto, Confianza y Facilidad (1 a 10), como en la Master (pestaña 15)."""
    vals = [num(p.get(k)) for k in ("impacto", "confianza", "facilidad")]
    return round(sum(vals) / 3, 2) if all(v is not None for v in vals) else None


def prioridad(p):
    s = ice(p)
    if s is not None:
        return "Alta" if s >= 8 else "Media" if s >= 6 else "Baja"
    return p.get("prioridad") or PEND


def derivar_mapa(datos):
    """Mapa borrador desde keywords.json + clusters.json cuando no hay content-map.json.
    Es una PROPUESTA (estado 'Borrador'): URL propuesta = /slug, sin volumen ni KD inventados."""
    kws = (datos.get("keywords") or {})
    cands = kws.get("candidates") or []
    oro = {(g.get("kw") or "").lower(): g for g in (kws.get("golden") or [])}
    cl_por_kw = {}
    pilares = {}
    for c in (datos.get("clusters") or {}).get("clusters", []):
        pilares[c.get("pilar", "")] = c.get("url")
        cl_por_kw[(c.get("pilar") or "").lower()] = (c.get("pilar"), "Pilar")
        for s in c.get("spokes") or []:
            nombre = s if isinstance(s, str) else s.get("keyword") or s.get("kw") or ""
            cl_por_kw[nombre.lower()] = (c.get("pilar"), "Spoke")
    paginas, vistas = [], set()
    candidatos = [c for c in cands if c.get("keyword")] or [{"keyword": g.get("kw"), "intent": None} for g in (kws.get("golden") or [])]
    for c in candidatos:
        kw = c["keyword"]
        if norm_kw(kw) in vistas:
            continue
        vistas.add(norm_kw(kw))
        cluster, rol = cl_por_kw.get(kw.lower(), (((oro.get(kw.lower()) or {}).get("cluster")) or PEND, "Spoke"))
        intent = (c.get("intent") or "").capitalize() or PEND
        tipo = "Landing" if intent == "Transaccional" else "Blog"
        paginas.append({"url": "/" + slug(kw), "url_estado": "propuesta", "keyword": kw, "intencion": intent,
                        "tipo": tipo, "cluster": cluster, "rol": rol, "accion": "Crear",
                        "volumen": c.get("volume", PEND), "kd": c.get("kd", PEND), "oro": kw.lower() in oro,
                        "estado": "Borrador"})
    return paginas


def pagina_calendario(paginas, por_mes=4, inicio=None):
    """Asigna mes y fecha. Orden: pilares y páginas que venden primero, luego por ICE, luego los spokes.
    Una página de apoyo nunca queda antes que el pilar de su cluster (los pilares ordenan primero).
    `por_mes` es un supuesto editable (--por-mes); fechas solo si hay --inicio."""
    def clave(p):
        grupo = 0 if p.get("rol") == "Pilar" else 1 if p.get("tipo") in TIPOS_QUE_VENDEN else 2
        s = ice(p)
        return (grupo, 0 if p.get("oro") else 1, -(s if s is not None else -1))
    pendientes = [p for p in paginas if p.get("accion") in ("Crear", "Actualizar")]
    for i, p in enumerate(sorted(pendientes, key=clave)):
        if not p.get("mes"):
            p["mes"] = "Mes %d" % (i // max(1, por_mes) + 1)
        if inicio and not p.get("fecha"):
            n = int(re.sub(r"\D", "", str(p["mes"])) or 1)
            base = inicio + dt.timedelta(days=30 * (n - 1))
            p["fecha"] = (base + dt.timedelta(days=7 * (i % max(1, por_mes)))).strftime("%d/%m/%Y")
    return paginas


def validar_mapa(paginas):
    """Una keyword = una URL. Devuelve lista de avisos {severidad, regla, detalle}."""
    av = []
    por_kw, por_url = {}, {}
    for p in paginas:
        kw, url = (p.get("keyword") or "").strip(), (p.get("url") or "").strip()
        if not kw:
            if p.get("tipo") in ("Blog", "Landing", "Ecommerce", "Categoría", "Home") and p.get("accion") != "Eliminar":
                av.append({"severidad": "Alto", "regla": "pagina-sin-keyword", "detalle": f"{url or '(sin URL)'} no tiene keyword principal"})
            continue
        por_kw.setdefault(norm_kw(kw), {}).setdefault(url, kw)
        por_url.setdefault(url, []).append(kw)
        if p.get("intencion") not in INTENCIONES and p.get("intencion") not in (None, PEND):
            av.append({"severidad": "Bajo", "regla": "intencion-no-reconocida", "detalle": f"'{p.get('intencion')}' en {url}"})
        if p.get("intencion") == "Transaccional" and p.get("tipo") == "Blog":
            av.append({"severidad": "Medio", "regla": "intencion-vs-tipo", "detalle": f"'{kw}' es transaccional pero la página es Blog: la SERP suele pedir Landing o Ecommerce"})
        if p.get("intencion") == "Informacional" and p.get("tipo") in ("Landing", "Ecommerce"):
            av.append({"severidad": "Medio", "regla": "intencion-vs-tipo", "detalle": f"'{kw}' es informacional pero la página es {p.get('tipo')}: revisa la SERP"})
    for k, urls in por_kw.items():
        if len(urls) > 1:
            av.append({"severidad": "Crítico", "regla": "keyword-repetida", "detalle": "Canibalización: %d URLs comparten keyword: %s" % (len(urls), "; ".join("%s (%s)" % (u, urls[u]) for u in sorted(urls)))})
    for url, kws in por_url.items():
        if len({norm_kw(k) for k in kws}) > 1:
            av.append({"severidad": "Alto", "regla": "url-con-varias-keywords", "detalle": f"{url} tiene {len(kws)} keywords principales distintas; deja una y mueve las demás a secundarias"})
    return av


def leer_csv(ruta):
    with open(ruta, encoding="utf-8-sig", newline="") as fh:
        muestra = fh.read(4096)
        fh.seek(0)
        try:
            d = csv.Sniffer().sniff(muestra, delimiters=",;\t")
        except csv.Error:
            d = csv.excel
        return list(csv.DictReader(fh, dialect=d))


def asegurar_dir(ruta):
    os.makedirs(ruta, exist_ok=True)
    return ruta
