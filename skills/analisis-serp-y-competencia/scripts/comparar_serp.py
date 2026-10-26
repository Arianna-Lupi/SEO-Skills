#!/usr/bin/env python3
"""
comparar_serp.py, Compara los perfiles del top de la SERP con tu página (solo stdlib).

Qué hace (determinista, sin red):
  Lee los perfiles que produce perfil_competidor.py y devuelve:
  1. Patrón común del top por keyword: lo que al menos el 60 % de las páginas
     comparte (tipo de página, rango de palabras, encabezados y temas
     frecuentes, schema, formato, E-E-A-T, frescura).
  2. Tabla comparativa de tu página frente al top.
  3. Brechas por categoría: tipo de página, cobertura de temas, estructura,
     formato, schema, E-E-A-T y frescura.
  4. Puntaje de "Costo de Oportunidad" por keyword, con fórmula explícita.
     OJO: el puntaje NO es del diplomado (el curso enseña el concepto, no una
     fórmula). Es una ayuda de este repo para ordenar y se puede ignorar.
  5. Análisis de Repetición con varias keywords: dominios y URLs que aparecen
     en más SERPs (competidor crítico: 60 % de las keywords, mínimo 2; la
     regla del curso es 3 de 5).
  6. Tareas con verbo (Semana 6 · lección 6) con prioridad por ICE.

Uso:
  python3 comparar_serp.py perfiles.json
  python3 comparar_serp.py perfiles_a.json perfiles_b.json --md reporte.md --out comparacion.json
  python3 comparar_serp.py perfiles.json --sitio ejemplo.com        # escribe competitors.json del dashboard
  python3 comparar_serp.py perfiles.json --competitors-json .seo-audit/ejemplo.com/data/competitors.json
  python3 comparar_serp.py perfiles.json --volumenes volumenes.json  # {"keyword": 1200}, dato real o nada

Entrada: uno o más JSON de perfil_competidor.py. Los perfiles con role "own" son tu página.
Salida: JSON a stdout (o --out) y, con --md, el informe en Markdown listo para pegar.
Si faltan datos, los campos dicen `pendiente de dato`; nunca se inventa volumen ni KD.

Deps: solo stdlib.
"""

import argparse
import json
import math
import os
import re
import sys
import unicodedata
from datetime import datetime, timezone

UMBRAL = 0.6  # regla de patrón común: al menos 60 % del top

NOISE_SCHEMA = {"question", "answer", "listitem", "imageobject", "postaladdress", "breadcrumblist",
                "readaction", "searchaction", "entrypoint", "person", "website", "webpage",
                "geocoordinates", "opening hours", "contactpoint", "aggregaterating", "rating",
                "review", "offer", "aggregateoffer", "itemlist"}
STOP = set("""para como esta este estos estas entre desde sobre cuando donde porque tambien pueden puede
hacer cada todo todos todas otros otras mismo misma menos mucho tiene siempre durante hasta antes despues
cual cuales mejor mejores segun debes debe ejemplo ademas que los las del una uno con por sus son más mas
qué cómo cuál guia completa paso""".split())

# peso por categoría (ayuda de este repo, no del diplomado)
PESO = {"tipo de página": 1.0, "cobertura de temas": 0.8, "formato": 0.6, "E-E-A-T": 0.6,
        "estructura": 0.5, "frescura": 0.5, "schema": 0.4}
# facilidad base 1 a 10 (supuesto editable)
FACILIDAD = {"tipo de página": 3, "cobertura de temas": 5, "formato": 6, "E-E-A-T": 6,
             "estructura": 6, "frescura": 7, "schema": 8}
SKILL_SUGERIDA = {"tipo de página": "intencion-de-busqueda", "cobertura de temas": "brief-de-contenido",
                  "formato": "brief-de-contenido", "E-E-A-T": "calidad-de-contenido-eeat",
                  "estructura": "optimizacion-on-page-meta", "frescura": "actualizacion-de-contenido",
                  "schema": "schema-jsonld"}
TIPO_LABEL = {"blog": "artículo de blog o guía", "landing": "landing", "ecommerce": "ficha de producto",
              "categoria": "página de categoría", "herramienta": "herramienta o calculadora",
              "video": "vídeo", "foro": "foro o hilo de preguntas", "otro": "sin clasificar"}
CONTENT_TYPES = {"blog", "landing", "herramienta"}


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c))


def stem(w):
    w = norm(w)
    return w[:6] if len(w) > 6 else w


def tokens(text):
    return {stem(w) for w in re.findall(r"[a-záéíóúüñ]{4,}", text.lower()) if norm(w) not in STOP}


def pct(x):
    return f"{round(100 * x)} %"


def quant(vals, q):
    s = sorted(vals)
    if not s:
        return None
    return s[int(round(q * (len(s) - 1)))]


def median(vals):
    s = sorted(vals)
    if not s:
        return None
    m = len(s) // 2
    return s[m] if len(s) % 2 else (s[m - 1] + s[m]) / 2


def pos_weight(p):
    pos = p.get("position")
    return 1.5 if isinstance(pos, int) and pos <= 3 else 1.0


def wshare(items, pred):
    tot = sum(pos_weight(p) for p in items)
    if not tot:
        return 0.0
    return sum(pos_weight(p) for p in items if pred(p)) / tot


def share(items, pred):
    return sum(1 for p in items if pred(p)) / len(items) if items else 0.0


def clean_schema(p):
    return {t for t in p.get("schema_types", []) if t.lower() not in NOISE_SCHEMA}


def heading_tokens(p, levels=(2, 3)):
    toks = set()
    for h in p.get("headings", []):
        if h["level"] in levels:
            toks |= tokens(h["text"])
    return toks


def stem_names(items):
    """Mapa raíz -> palabra legible, tomado de los encabezados."""
    names = {}
    for p in items:
        for h in p.get("headings", []):
            for w in re.findall(r"[a-záéíóúüñ]{4,}", h["text"].lower()):
                names.setdefault(stem(w), w)
    return names


def own_tokens(p):
    toks = tokens(p.get("title", "")) | heading_tokens(p, (1, 2, 3))
    for t in p.get("top_terms", []):
        toks.add(stem(t))
    return toks


def load(paths):
    profiles, errors, notes = [], [], []
    for path in paths:
        with open(path, encoding="utf-8") as fh:
            d = json.load(fh)
        if isinstance(d, dict) and d.get("ok") is False:
            raise ValueError(f"{path}: perfiles con ok=false ({d.get('reason', '')})")
        profiles += d.get("profiles", []) if isinstance(d, dict) else d
        if isinstance(d, dict):
            errors += d.get("errors", [])
            notes += d.get("notes", [])
    return profiles, errors, notes


def pattern_for(top):
    """Patrón común (>= 60 %) sobre las páginas con contenido legible."""
    n = len(top)
    valid = [p for p in top if not p.get("javascript_dependent")]
    nv = len(valid)
    pat = {"paginas": n, "paginas_legibles": nv}
    types = {}
    for p in top:
        if p["page_type"] != "otro" or not p.get("javascript_dependent"):
            types[p["page_type"]] = types.get(p["page_type"], 0) + 1
    typed = sum(types.values())
    dom = max(types, key=lambda k: types[k]) if types else None
    pat["tipo_pagina"] = {
        "distribucion": types,
        "dominante": dom if dom and typed and types[dom] / typed >= UMBRAL else None,
        "consenso": ("fuerte" if typed and types[dom] / typed >= UMBRAL else
                     ("mixto" if typed and types[dom] / typed >= 0.4 else "fragmentado")) if dom else "pendiente de dato",
        "proporcion": round(types[dom] / typed, 2) if dom and typed else None,
    }
    words = [p["word_count"] for p in valid]
    pat["palabras"] = ({"min": min(words), "p25": quant(words, 0.25), "mediana": median(words),
                        "p75": quant(words, 0.75), "max": max(words)} if words else "pendiente de dato")
    if nv:
        ftoks = {}
        for p in valid:
            for t in heading_tokens(p):
                ftoks[t] = ftoks.get(t, 0) + 1
        nm = stem_names(valid)
        pat["temas_frecuentes"] = [nm.get(t, t) for t in sorted([t for t, c in ftoks.items() if c / nv >= UMBRAL],
                                                                 key=lambda t: (-ftoks[t], t))[:12]]
        hcount = {}
        for p in valid:
            seen = set()
            for h in p.get("headings", []):
                if h["level"] in (2, 3):
                    k = norm(h["text"]).strip(" ?¿:.")
                    if k not in seen:
                        seen.add(k)
                        hcount[k] = hcount.get(k, 0) + 1
        pat["encabezados_frecuentes"] = [k for k, c in sorted(hcount.items(), key=lambda kv: -kv[1])
                                         if c / nv >= UMBRAL and c >= 2][:10]
        h2 = [p["counts"]["h2"] for p in valid]
        pat["h2"] = {"mediana": median(h2), "p25": quant(h2, 0.25), "p75": quant(h2, 0.75)}
        st = {}
        for p in valid:
            for t in clean_schema(p):
                st[t] = st.get(t, 0) + 1
        pat["schema"] = sorted([t for t, c in st.items() if c / nv >= UMBRAL])
        fmt = {
            "faq": share(valid, lambda p: p["formats"]["faq"]),
            "listas": share(valid, lambda p: p["formats"]["lists"] > 0),
            "tablas": share(valid, lambda p: p["formats"]["tables"] > 0),
            "video": share(valid, lambda p: p["formats"]["video"]),
            "imagenes_3_o_mas": share(valid, lambda p: p["images"]["total"] >= 3),
        }
        pat["formato"] = {"prevalencia": {k: round(v, 2) for k, v in fmt.items()},
                          "comun": [k for k, v in fmt.items() if v >= UMBRAL]}
        ee = {
            "autor": share(valid, lambda p: p["eeat"]["author"]),
            "fecha_visible": share(valid, lambda p: p["eeat"]["date_visible"]),
            "fuentes": share(valid, lambda p: p["eeat"]["sources_cited"]),
            "datos_propios": share(valid, lambda p: p["eeat"]["own_data"]),
            "experiencia": share(valid, lambda p: p["eeat"]["first_hand_experience"]),
        }
        pat["eeat"] = {"prevalencia": {k: round(v, 2) for k, v in ee.items()},
                       "comun": [k for k, v in ee.items() if v >= UMBRAL]}
        ages = [p["dates"]["age_days"] for p in valid if p["dates"].get("age_days") is not None]
        pat["frescura"] = {
            "con_fecha": round(share(valid, lambda p: p["dates"].get("age_days") is not None), 2),
            "mediana_dias": median(ages) if ages else "pendiente de dato",
            "actualizadas_ultimo_ano": round(share(valid, lambda p: (p["dates"].get("age_days") is not None
                                                                    and p["dates"]["age_days"] <= 365)), 2),
        }
    return pat


def detect_gaps(kw, top, own, pat):
    """Brechas de tu página frente al patrón. Cada una: categoría, id, evidencia, prevalencia ponderada."""
    gaps = []
    valid = [p for p in top if not p.get("javascript_dependent")]
    nv = len(valid)

    def add(cat, gid, label, pred_items, pred, detalle="", extra=None):
        pw = wshare(pred_items, pred)
        k = sum(1 for p in pred_items if pred(p))
        g = {"keyword": kw, "categoria": cat, "id": gid, "brecha": label,
             "evidencia": f"{k} de {len(pred_items)} páginas del top",
             "prevalencia": round(pw, 2), "puntaje": round(100 * pw * PESO[cat]),
             "detalle": detalle, "n_base": len(pred_items)}
        if extra:
            g.update(extra)
        gaps.append(g)

    typed = [p for p in top if p["page_type"] != "otro"]
    dom = pat["tipo_pagina"]["dominante"]
    mismatch = bool(dom and typed and own["page_type"] != dom and own["page_type"] != "otro")
    own_unknown = bool(dom and own["page_type"] == "otro")
    if mismatch:
        add("tipo de página", "tipo", f"Tu página es {TIPO_LABEL.get(own['page_type'], own['page_type'])} y la SERP premia "
            f"{TIPO_LABEL.get(dom, dom)}", typed, lambda p: p["page_type"] == dom,
            "Desajuste de tipo de página: antes de mejorar el contenido, decide si creas la página del tipo que premia Google "
            "(ver intencion-de-busqueda).", {"dominante": dom, "propio": own["page_type"]})
    elif own_unknown:
        gaps.append({"keyword": kw, "categoria": "tipo de página", "id": "tipo_sin_clasificar",
                     "brecha": "No se pudo clasificar el tipo de tu página", "evidencia": "señales insuficientes",
                     "prevalencia": 0.0, "puntaje": 0, "detalle": "Revisa a mano si coincide con el tipo dominante.",
                     "n_base": 0})
    cond = mismatch  # los demás hallazgos dependen de resolver el tipo

    if nv:
        # estructura
        words = own["word_count"]
        if dom in CONTENT_TYPES or not dom:
            add("estructura", "longitud", f"Tu página tiene {words} palabras y gran parte del top supera esa extensión",
                valid, lambda p: p["word_count"] >= words * 1.3,
                "La extensión no es un objetivo en sí; mide cobertura (ver temas).")
        add("estructura", "h2", f"Tu página tiene {own['counts']['h2']} H2 frente a una mediana de {pat['h2']['mediana']}",
            valid, lambda p: p["counts"]["h2"] >= own["counts"]["h2"] + 2)
        if own["counts"]["h1"] != 1:
            gaps.append({"keyword": kw, "categoria": "estructura", "id": "h1",
                         "brecha": f"Tu página tiene {own['counts']['h1']} H1 (debe tener uno)",
                         "evidencia": "revisión directa", "prevalencia": 1.0,
                         "puntaje": round(100 * PESO["estructura"]), "detalle": "", "n_base": nv})
        if not own["meta_description"]:
            add("estructura", "meta", "Tu página no tiene meta description", valid,
                lambda p: bool(p["meta_description"]))
        # cobertura de temas
        otoks = own_tokens(own)
        ftoks = {}
        for p in valid:
            for t in heading_tokens(p):
                ftoks.setdefault(t, set()).add(p["url"])
        # En SERPs de categoría o producto los encabezados son nombres de producto: no se mide cobertura de temas.
        missing = [] if dom in ("categoria", "ecommerce") else \
            [t for t, urls in ftoks.items() if len(urls) / nv >= UMBRAL and t not in otoks]
        names = stem_names(valid)
        for t in sorted(missing, key=lambda t: -len(ftoks[t]))[:6]:
            add("cobertura de temas", f"tema:{t}", f"Tema que el top trata en sus encabezados y tu página no: «{names.get(t, t)}»",
                valid, lambda p, t=t: t in heading_tokens(p), "", {"tema": names.get(t, t)})
        # formato
        fm = own["formats"]
        specs = [("faq", "FAQ o preguntas frecuentes", lambda p: p["formats"]["faq"], fm["faq"]),
                 ("tablas", "tablas comparativas o de datos", lambda p: p["formats"]["tables"] > 0, fm["tables"] > 0),
                 ("listas", "listas", lambda p: p["formats"]["lists"] > 0, fm["lists"] > 0),
                 ("video", "vídeo", lambda p: p["formats"]["video"], fm["video"]),
                 ("imagenes", "tres o más imágenes", lambda p: p["images"]["total"] >= 3, own["images"]["total"] >= 3)]
        for gid, label, pred, has in specs:
            if not has and share(valid, pred) >= UMBRAL:
                add("formato", gid, f"Tu página no usa {label} y la mayoría del top sí", valid, pred)
        if own["images"]["total"] > own["images"]["with_alt"] and \
                share(valid, lambda p: p["images"]["total"] and p["images"]["total"] == p["images"]["with_alt"]) >= UMBRAL:
            add("formato", "alt", "Tienes imágenes sin texto alternativo y el top las describe todas", valid,
                lambda p: p["images"]["total"] and p["images"]["total"] == p["images"]["with_alt"])
        # schema
        mine = {t.lower() for t in clean_schema(own)}
        for t in pat.get("schema", []):
            if t.lower() not in mine:
                add("schema", f"schema:{t}", f"Tu página no marca el schema «{t}»", valid,
                    lambda p, t=t: t in clean_schema(p))
        # E-E-A-T
        ee = own["eeat"]
        for gid, label, pred, has in [
                ("autor", "autor visible", lambda p: p["eeat"]["author"], ee["author"]),
                ("fuentes", "fuentes citadas", lambda p: p["eeat"]["sources_cited"], ee["sources_cited"]),
                ("datos_propios", "datos propios o pruebas", lambda p: p["eeat"]["own_data"], ee["own_data"]),
                ("experiencia", "experiencia de primera mano", lambda p: p["eeat"]["first_hand_experience"],
                 ee["first_hand_experience"])]:
            if not has and share(valid, pred) >= UMBRAL:
                add("E-E-A-T", gid, f"Tu página no muestra {label} y la mayoría del top sí", valid, pred)
        # frescura
        if not ee["date_visible"] and share(valid, lambda p: p["eeat"]["date_visible"]) >= UMBRAL:
            add("frescura", "fecha", "Tu página no muestra fecha de publicación ni actualización", valid,
                lambda p: p["eeat"]["date_visible"])
        age = own["dates"].get("age_days")
        if age is not None:
            add("frescura", "antiguedad", f"Tu página tiene {age} días desde su última fecha y el top está más fresco",
                [p for p in valid if p["dates"].get("age_days") is not None],
                lambda p: p["dates"]["age_days"] < age and p["dates"]["age_days"] <= 365)
    gaps = [g for g in gaps if g["prevalencia"] >= UMBRAL or g["id"] in ("h1", "tipo_sin_clasificar")]
    for g in gaps:
        g["depende_del_tipo"] = bool(cond and g["categoria"] != "tipo de página")
    gaps.sort(key=lambda g: -g["puntaje"])
    return gaps, mismatch


def cop_score(gaps):
    """Costo de Oportunidad (puntaje relativo 0 a 100). Fórmula en FORMULA_COP."""
    sc = sorted((g["puntaje"] for g in gaps), reverse=True)
    if not sc:
        return 0
    top5 = sc[:5]
    return min(100, round(0.5 * sc[0] + 0.5 * (sum(top5) / 5)))


FORMULA_COP = (
    "Puntaje por brecha = 100 x prevalencia ponderada x peso de categoría. La prevalencia ponderada es la fracción del "
    "top que tiene el rasgo, con peso 1,5 para las posiciones 1 a 3 y 1 para el resto. Pesos: tipo de página 1,0; "
    "cobertura de temas 0,8; formato 0,6; E-E-A-T 0,6; estructura 0,5; frescura 0,5; schema 0,4. "
    "Costo de Oportunidad de la keyword = min(100, 0,5 x brecha mayor + 0,5 x promedio de las 5 brechas mayores, "
    "dividiendo siempre entre 5). Es un puntaje RELATIVO para ordenar keywords y brechas: no son visitas, clics ni dinero. "
    "El diplomado enseña el concepto de Costo de Oportunidad (Semana 6 · lecciones 1 y 5: el tráfico que pierdes frente a "
    "tu competidor) pero no esta fórmula; es una ayuda de este repo. Para hablar de visitas necesitas el volumen real "
    "(Search Console, Ahrefs) y un CTR que tú eliges: ese dato queda en `pendiente de dato`."
)

VERBOS = {
    "tipo": ("Crear", "la página que premia la SERP para «{kw}» ({dominante}) en lugar de reforzar la actual"),
    "longitud": ("Ampliar", "el contenido de la página para «{kw}» cubriendo los temas del top, sin rellenar"),
    "h2": ("Reestructurar", "los H2 de la página para «{kw}» siguiendo el orden de los temas que usa el top"),
    "h1": ("Corregir", "el encabezado H1 de la página para «{kw}» para que haya uno solo con la keyword"),
    "meta": ("Redactar", "la meta description de la página para «{kw}» (promesa, keyword y llamado a la acción)"),
    "faq": ("Incorporar", "una sección de preguntas frecuentes a la página para «{kw}»"),
    "tablas": ("Añadir", "una tabla comparativa o de datos a la página para «{kw}»"),
    "listas": ("Convertir", "los pasos o puntos clave de la página para «{kw}» en listas"),
    "video": ("Incrustar", "un vídeo explicativo en la página para «{kw}»"),
    "imagenes": ("Añadir", "al menos tres imágenes propias con texto alternativo a la página para «{kw}»"),
    "alt": ("Completar", "el texto alternativo de las imágenes de la página para «{kw}»"),
    "autor": ("Mostrar", "autor con perfil y credenciales en la página para «{kw}»"),
    "fuentes": ("Citar", "fuentes verificables en la página para «{kw}»"),
    "datos_propios": ("Incluir", "datos propios, pruebas o casos reales en la página para «{kw}»"),
    "experiencia": ("Incorporar", "experiencia de primera mano (quién lo hizo y cómo) en la página para «{kw}»"),
    "fecha": ("Mostrar", "la fecha de publicación y de última actualización en la página para «{kw}»"),
    "antiguedad": ("Actualizar", "la página para «{kw}» con información vigente y registrar la fecha de actualización"),
}
CATEGORY_DEFAULT = {"cobertura de temas": ("Añadir", "una sección sobre «{tema}» a la página para «{kw}»"),
                    "schema": ("Implementar", "el schema {schema} en la página para «{kw}»")}


SKILL_POR_ID = {"longitud": "brief-de-contenido", "h2": "brief-de-contenido", "h1": "optimizacion-on-page-meta",
                "meta": "optimizacion-on-page-meta", "tipo": "intencion-de-busqueda"}


def make_task(g, n_valid):
    gid = g["id"]
    if gid.startswith("schema:"):
        verbo, rest = CATEGORY_DEFAULT["schema"]
        rest = rest.format(schema=gid.split(":", 1)[1], kw=g["keyword"])
    elif gid.startswith("tema:"):
        verbo, rest = CATEGORY_DEFAULT["cobertura de temas"]
        rest = rest.format(tema=g.get("tema", gid), kw=g["keyword"])
    elif gid in VERBOS:
        verbo, rest = VERBOS[gid]
        rest = rest.format(kw=g["keyword"], dominante=TIPO_LABEL.get(g.get("dominante", ""), g.get("dominante", "")))
    else:
        return None
    impacto = max(1, min(10, round(g["puntaje"] / 10)))
    conf = 8 if n_valid >= 5 else 6 if n_valid >= 3 else 4 if n_valid == 2 else 3
    if g.get("depende_del_tipo"):
        conf = max(2, conf - 2)
    facil = FACILIDAD[g["categoria"]]
    ice = round((impacto + conf + facil) / 3, 1)
    return {
        "tarea": f"{verbo} {rest}",
        "categoria": g["categoria"], "brecha_id": gid, "keywords": [g["keyword"]],
        "por_que": g["brecha"] + f" ({g['evidencia']}).",
        "skill_sugerida": SKILL_POR_ID.get(gid, SKILL_SUGERIDA[g["categoria"]]),
        "impacto": impacto, "confianza": conf, "facilidad": facil, "ice": ice,
        "prioridad": "alta" if ice >= 7 else "media" if ice >= 5 else "baja",
        "condicion": "resolver antes el desajuste de tipo de página" if g.get("depende_del_tipo") else "",
        "plazo": "pendiente de dato", "recurso": "pendiente de dato", "responsable": "pendiente de dato",
    }


def consolidate(tasks):
    """Une tareas idénticas en varias keywords: sube confianza por repetición (Análisis de Repetición)."""
    out = {}
    for t in tasks:
        key = (t["brecha_id"], t["categoria"], t["tarea"].rsplit("«", 1)[0])
        if key not in out:
            out[key] = dict(t)
        else:
            o = out[key]
            o["keywords"] = sorted(set(o["keywords"]) | set(t["keywords"]))
            if not t["condicion"]:
                o["condicion"] = ""
            o["impacto"] = max(o["impacto"], t["impacto"])
            o["confianza"] = min(10, max(o["confianza"], t["confianza"]) + 1)
            o["ice"] = round((o["impacto"] + o["confianza"] + o["facilidad"]) / 3, 1)
            o["prioridad"] = "alta" if o["ice"] >= 7 else "media" if o["ice"] >= 5 else "baja"
    res = list(out.values())
    for t in res:
        if len(t["keywords"]) > 1:
            head, _, tail = t["tarea"].rpartition("«")
            t["tarea"] = f"{head}«{t['keywords'][0]}» (y {len(t['keywords']) - 1} más)" + tail.split("»", 1)[1]
            t["por_que"] += f" Aparece en {len(t['keywords'])} keywords."
    res.sort(key=lambda t: (-t["ice"], t["categoria"]))
    for i, t in enumerate(res, 1):
        t["id"] = f"T{i:02d}"
    return res


def repetition(by_kw):
    kws = list(by_kw)
    k = len(kws)
    thr = max(2, math.ceil(UMBRAL * k)) if k > 1 else None
    doms, urls = {}, {}
    for kw, top in by_kw.items():
        for p in top:
            d = doms.setdefault(p["domain"], {"domain": p["domain"], "keywords": {}, "urls": set(), "types": set()})
            d["keywords"][kw] = p.get("position")
            d["urls"].add(p["url"])
            d["types"].add(p["page_type"])
            u = urls.setdefault(p["url"], {"url": p["url"], "domain": p["domain"], "keywords": {}, "page_type": p["page_type"]})
            u["keywords"][kw] = p.get("position")
    dl = []
    for d in doms.values():
        n = len(d["keywords"])
        pos = [x for x in d["keywords"].values() if isinstance(x, int)]
        dl.append({"domain": d["domain"], "repeticion": n, "de": k, "critico": bool(thr and n >= thr),
                   "mejor_posicion": min(pos) if pos else None, "keywords": d["keywords"],
                   "tipos_de_pagina": sorted(d["types"]), "urls": sorted(d["urls"])[:5]})
    dl.sort(key=lambda x: (-x["repeticion"], x["mejor_posicion"] if x["mejor_posicion"] is not None else 99))
    ul = [{"url": u["url"], "domain": u["domain"], "repeticion": len(u["keywords"]), "keywords": u["keywords"],
           "page_type": u["page_type"]} for u in urls.values() if len(u["keywords"]) >= 2]
    ul.sort(key=lambda x: -x["repeticion"])
    return {"keywords": k, "umbral_critico": thr, "dominios": dl, "urls_repetidas": ul,
            "regla": "Competidor crítico: aparece en 60 % de tus keywords, mínimo 2 (el curso lo enseña como 3 de 5, Semana 6 · lección 3)."
            if k > 1 else "Con una sola keyword no hay Análisis de Repetición: añade 3 a 5 keywords."}


def own_table(own, pat):
    if not own or not isinstance(pat.get("palabras"), dict):
        return []
    P = pat
    rows = [
        ("Tipo de página", own["page_type"], P["tipo_pagina"]["dominante"] or "sin consenso"),
        ("Palabras", own["word_count"], f"mediana {P['palabras']['mediana']} (rango {P['palabras']['p25']} a {P['palabras']['p75']})"),
        ("H2", own["counts"]["h2"], f"mediana {P['h2']['mediana']}"),
        ("Schema", ", ".join(sorted(clean_schema(own))) or "ninguno", ", ".join(P["schema"]) or "ninguno común"),
        ("FAQ", "sí" if own["formats"]["faq"] else "no", pct(P["formato"]["prevalencia"]["faq"])),
        ("Tablas", "sí" if own["formats"]["tables"] else "no", pct(P["formato"]["prevalencia"]["tablas"])),
        ("Listas", "sí" if own["formats"]["lists"] else "no", pct(P["formato"]["prevalencia"]["listas"])),
        ("Vídeo", "sí" if own["formats"]["video"] else "no", pct(P["formato"]["prevalencia"]["video"])),
        ("Imágenes (con alt)", f"{own['images']['total']} ({own['images']['with_alt']})", pct(P["formato"]["prevalencia"]["imagenes_3_o_mas"]) + " con 3 o más"),
        ("Autor visible", "sí" if own["eeat"]["author"] else "no", pct(P["eeat"]["prevalencia"]["autor"])),
        ("Fecha visible", "sí" if own["eeat"]["date_visible"] else "no", pct(P["eeat"]["prevalencia"]["fecha_visible"])),
        ("Fuentes citadas", "sí" if own["eeat"]["sources_cited"] else "no", pct(P["eeat"]["prevalencia"]["fuentes"])),
        ("Datos propios", "sí" if own["eeat"]["own_data"] else "no", pct(P["eeat"]["prevalencia"]["datos_propios"])),
        ("Días desde la última fecha", own["dates"].get("age_days") if own["dates"].get("age_days") is not None else "sin fecha",
         f"mediana {P['frescura']['mediana_dias']}"),
    ]
    return [{"metrica": a, "tu_pagina": b, "top": c} for a, b, c in rows]


def to_md(res):
    L = []
    w = L.append
    w("# Comparación de la SERP: tu página frente al top")
    w("")
    w(f"Generado: {res['generated']}. Keywords analizadas: {len(res['keywords'])}.")
    if not res["tiene_pagina_propia"]:
        w("")
        w("> No hay perfil de tu página (rol `own`). El informe muestra solo el patrón del top. Perfila tu URL con "
          "`perfil_competidor.py --own-url` para calcular brechas.")
    for k in res["keywords"]:
        w("")
        w(f"## Keyword: {k['keyword']}")
        pat = k["patron"]
        tp = pat["tipo_pagina"]
        w("")
        w(f"Volumen: {k['volumen']}. Páginas perfiladas: {pat['paginas']} (legibles sin JavaScript: {pat['paginas_legibles']}).")
        w("")
        w("### Patrón común del top (al menos 60 %)")
        w("")
        dist = ", ".join(f"{TIPO_LABEL.get(a, a)}: {b}" for a, b in tp["distribucion"].items())
        w(f"- Tipo de página: consenso {tp['consenso']}"
          + (f", domina {TIPO_LABEL.get(tp['dominante'], tp['dominante'])} ({pct(tp['proporcion'])})" if tp["dominante"] else "")
          + f". Distribución: {dist}.")
        if isinstance(pat["palabras"], dict):
            pw = pat["palabras"]
            w(f"- Palabras: mediana {pw['mediana']}, rango habitual {pw['p25']} a {pw['p75']} (mín. {pw['min']}, máx. {pw['max']}).")
            w(f"- Temas que se repiten en los encabezados: {', '.join(pat['temas_frecuentes']) or 'ninguno común'}.")
            w(f"- Encabezados repetidos: {', '.join(pat['encabezados_frecuentes']) or 'ninguno idéntico'}.")
            w(f"- Schema común: {', '.join(pat['schema']) or 'ninguno común'}.")
            w(f"- Formato común: {', '.join(pat['formato']['comun']) or 'ninguno común'}.")
            w(f"- E-E-A-T común: {', '.join(pat['eeat']['comun']) or 'ninguno común'}.")
            fr = pat["frescura"]
            w(f"- Frescura: {pct(fr['con_fecha'])} muestra fecha, mediana {fr['mediana_dias']} días, "
              f"{pct(fr['actualizadas_ultimo_ano'])} con fecha del último año.".replace("pendiente de dato días", "pendiente de dato"))
        if k["tabla"]:
            w("")
            w("### Tu página frente al top")
            w("")
            w("| Métrica | Tu página | Top |")
            w("|---|---|---|")
            for r in k["tabla"]:
                w(f"| {r['metrica']} | {r['tu_pagina']} | {r['top']} |")
        if k["brechas"]:
            w("")
            w("### Brechas")
            w("")
            w("| Categoría | Brecha | Evidencia | Puntaje |")
            w("|---|---|---|---|")
            for g in k["brechas"]:
                flag = " (tras resolver el tipo)" if g.get("depende_del_tipo") else ""
                w(f"| {g['categoria']} | {g['brecha']}{flag} | {g['evidencia']} | {g['puntaje']} |")
            w("")
            w(f"**Costo de Oportunidad (puntaje relativo): {k['costo_oportunidad']} de 100, {k['nivel_costo']}.**")
        elif res["tiene_pagina_propia"]:
            w("")
            w("Sin brechas sobre el umbral de 60 %: tu página ya coincide con el patrón. Revisa a ojo el top 3 (Ojo Clínico).")
    rep = res["repeticion"]
    w("")
    w("## Análisis de Repetición")
    w("")
    w(rep["regla"])
    crit = [d for d in rep["dominios"] if d["repeticion"] > 1]
    if crit:
        w("")
        w("| Dominio | Aparece en | Mejor posición | Tipos de página | Crítico |")
        w("|---|---|---|---|---|")
        for d in crit:
            w(f"| {d['domain']} | {d['repeticion']} de {d['de']} | {d['mejor_posicion']} | {', '.join(d['tipos_de_pagina'])} | {'sí' if d['critico'] else 'no'} |")
    if rep["urls_repetidas"]:
        w("")
        w("URLs que aparecen en más de una SERP (candidatas al Ojo Clínico):")
        w("")
        for u in rep["urls_repetidas"][:10]:
            w(f"- {u['url']} ({u['repeticion']} keywords)")
    if res["tareas"]:
        w("")
        w("## Tareas (de la brecha al verbo)")
        w("")
        w("Cada tarea empieza con un verbo (Semana 6 · lección 6). Impacto, confianza y facilidad son supuestos editables; "
          "ICE es su promedio. Plazo, recurso y responsable los defines tú.")
        w("")
        w("| ID | Tarea | Keywords | Impacto | Confianza | Facilidad | ICE | Prioridad | Skill |")
        w("|---|---|---|---|---|---|---|---|---|")
        for t in res["tareas"]:
            cond = f" (condición: {t['condicion']})" if t["condicion"] else ""
            w(f"| {t['id']} | {t['tarea']}{cond} | {', '.join(t['keywords'])} | {t['impacto']} | {t['confianza']} | {t['facilidad']} | {t['ice']} | {t['prioridad']} | `{t['skill_sugerida']}` |")
    w("")
    w("## Cómo se calcula el puntaje de Costo de Oportunidad")
    w("")
    w(res["formula_costo_oportunidad"])
    if res["notas"]:
        w("")
        w("## Límites de este análisis")
        w("")
        for n in res["notas"]:
            w(f"- {n}")
    return "\n".join(L) + "\n"


def write_competitors(path, res, by_kw, pilares):
    data = {}
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
        except (OSError, json.JSONDecodeError):
            data = {}
    by_pillar = [bp for bp in data.get("by_pillar", []) if bp.get("query") not in by_kw]
    for kw, top in by_kw.items():
        by_pillar.append({
            "pillar": pilares.get(kw, kw), "query": kw,
            "results": [{"position": p.get("position"), "domain": p["domain"], "title": p.get("title", ""),
                         "url": p["url"], "page_type": p["page_type"], "word_count": p["word_count"],
                         "schema_types": p.get("schema_types", []),
                         "javascript_dependent": p.get("javascript_dependent", False)}
                        for p in sorted(top, key=lambda x: (x.get("position") is None, x.get("position") or 0))]})
    strategic = {s.get("name"): s for s in data.get("strategic", []) if isinstance(s, dict)}
    for d in res["repeticion"]["dominios"]:
        if d["critico"]:
            strategic[d["domain"]] = {"name": d["domain"], "url": d["urls"][0] if d["urls"] else "",
                                      "repeticion": d["repeticion"], "de": d["de"], "critical": True}
    data["by_pillar"] = by_pillar
    data["strategic"] = list(strategic.values())
    data["serp_analysis"] = {
        "generated": res["generated"], "contract": "contrato-datos.md v1",
        "keywords": [{k: v for k, v in kw.items() if k != "tabla"} | {"tabla": kw["tabla"]} for kw in res["keywords"]],
        "repeticion": res["repeticion"], "tasks": res["tareas"],
        "formula_costo_oportunidad": res["formula_costo_oportunidad"], "notas": res["notas"]}
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)


def main():
    ap = argparse.ArgumentParser(
        description="Compara los perfiles del top de la SERP con tu página: patrón común (60 %), tabla, brechas, "
                    "Costo de Oportunidad (puntaje relativo), Análisis de Repetición y tareas con ICE. Solo stdlib.")
    ap.add_argument("perfiles", nargs="+", help="JSON de perfil_competidor.py (uno o varios)")
    ap.add_argument("--out", help="guarda el JSON completo aquí")
    ap.add_argument("--md", help="guarda el informe en Markdown aquí ('-' lo imprime)")
    ap.add_argument("--sitio", help="dominio del sitio: escribe .seo-audit/<sitio>/data/competitors.json")
    ap.add_argument("--competitors-json", help="ruta explícita de competitors.json (fusiona con el existente)")
    ap.add_argument("--pilares", help="JSON {keyword: pilar} para by_pillar (por defecto la propia keyword)")
    ap.add_argument("--volumenes", help="JSON {keyword: volumen} con datos reales; sin él queda 'pendiente de dato'")
    args = ap.parse_args()

    try:
        profiles, errors, notes = load(args.perfiles)
    except (OSError, ValueError, json.JSONDecodeError) as e:
        print(json.dumps({"ok": False, "reason": str(e),
                          "fallback": "modo manual: llena la tabla del Ojo Clínico a mano y compara con tu página"},
                         ensure_ascii=False))
        return

    own_list = [p for p in profiles if p.get("role") == "own"]
    own = own_list[0] if own_list else None
    comp = [p for p in profiles if p.get("role") != "own"]
    if not comp:
        print(json.dumps({"ok": False, "reason": "No hay perfiles de competidores.",
                          "fallback": "modo manual: ejecuta perfil_competidor.py con las URLs del top"}, ensure_ascii=False))
        return

    by_kw = {}
    for p in comp:
        by_kw.setdefault(p.get("keyword") or "(sin keyword)", []).append(p)
    # una URL por keyword
    for kw, items in by_kw.items():
        seen, uniq = set(), []
        for p in items:
            if p["url"] not in seen:
                seen.add(p["url"])
                uniq.append(p)
        by_kw[kw] = uniq

    vols = {}
    if args.volumenes:
        with open(args.volumenes, encoding="utf-8") as fh:
            vols = json.load(fh)
    pilares = {}
    if args.pilares:
        with open(args.pilares, encoding="utf-8") as fh:
            pilares = json.load(fh)

    kw_out, all_tasks, global_notes = [], [], []
    for kw, top in by_kw.items():
        pat = pattern_for(top)
        gaps, mismatch = ([], False)
        if own and isinstance(pat.get("palabras"), dict):
            gaps, mismatch = detect_gaps(kw, top, own, pat)
        elif own:
            global_notes.append(f"«{kw}»: todas las páginas del top dependen de JavaScript; sin brechas de contenido calculables.")
        cop = cop_score(gaps)
        nvalid = pat["paginas_legibles"]
        for g in gaps:
            t = make_task(g, nvalid)
            if t:
                all_tasks.append(t)
        v = vols.get(kw)
        kw_out.append({
            "keyword": kw, "volumen": v if v is not None else "pendiente de dato",
            "patron": pat, "tabla": own_table(own, pat) if own else [], "brechas": gaps,
            "desajuste_tipo": mismatch, "costo_oportunidad": cop,
            "nivel_costo": "alto" if cop >= 50 else "medio" if cop >= 25 else "bajo"})

    tasks = consolidate(all_tasks)
    notes_all = list(dict.fromkeys(notes + global_notes))
    notes_all.append("Los porcentajes se calculan sobre las páginas legibles del top; con menos de 5 páginas el patrón es orientativo.")
    notes_all.append("La cobertura de temas compara palabras de encabezados y términos frecuentes del texto; no mide calidad. "
                     "Confírmala con el Ojo Clínico sobre el top 3.")
    if errors:
        notes_all.append(f"{len(errors)} URL(s) no se pudieron perfilar (ver perfiles.json > errors).")
    res = {"ok": True, "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "umbral_patron": UMBRAL, "tiene_pagina_propia": bool(own),
           "pagina_propia": own["url"] if own else None, "keywords": kw_out,
           "repeticion": repetition(by_kw), "tareas": tasks,
           "formula_costo_oportunidad": FORMULA_COP, "notas": notes_all}

    path = args.competitors_json or (f".seo-audit/{args.sitio}/data/competitors.json" if args.sitio else None)
    if path:
        write_competitors(path, res, by_kw, pilares)
        res["competitors_json"] = os.path.abspath(path)

    text = json.dumps(res, ensure_ascii=False, indent=2)
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
    md = to_md(res)
    if args.md == "-":
        print(md)
    else:
        if args.md:
            os.makedirs(os.path.dirname(os.path.abspath(args.md)), exist_ok=True)
            with open(args.md, "w", encoding="utf-8") as fh:
                fh.write(md)
        print(text)


if __name__ == "__main__":
    main()
