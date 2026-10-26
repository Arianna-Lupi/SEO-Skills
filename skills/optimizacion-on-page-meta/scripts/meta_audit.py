#!/usr/bin/env python3
"""
meta_audit.py: auditoría masiva de metas desde un CSV (por plantillas, no página a página).

Revisa, para todas las URLs a la vez, lo que el diplomado fija (Semana 8, lecciones 4 a 6):
  - Meta título 50 a 60 caracteres. Meta descripción 120 a 155.
  - Faltantes y duplicados entre URLs (cada página, su título y su descripción únicos).
  - Keyword al inicio del título (si pasas la columna keyword).
Agrupa por severidad: alta (falta o duplicado), media (fuera de rango), baja (sin keyword al inicio).

CSV de entrada con cabecera. Columnas reconocidas (español o inglés):
  url | address, title | meta_titulo | title 1, description | meta_descripcion | meta description 1,
  keyword (opcional), h1 (opcional)
Sirve el export de Screaming Frog (Page Titles + Meta Description) o una hoja de la Plantilla Master.

Uso:
  python3 meta_audit.py --file metas.csv [--out .seo-audit/<sitio>/data/meta-audit.json]

Solo stdlib. Sin archivo válido: {"ok": false, ...} con exit 0.
"""
import argparse
import csv
import json
import sys
from collections import defaultdict

ALIAS = {
    "url": ("url", "address", "página", "pagina", "page"),
    "title": ("title", "titulo", "título", "meta_titulo", "meta título", "title 1", "metatítulo"),
    "desc": ("description", "descripcion", "descripción", "meta_descripcion", "meta description 1", "meta description", "metadescripción"),
    "keyword": ("keyword", "palabra clave", "kw"),
    "h1": ("h1", "h1-1"),
}


def col(header, key):
    low = {h.strip().lower(): h for h in header}
    for alias in ALIAS[key]:
        if alias in low:
            return low[alias]
    return None


def main():
    ap = argparse.ArgumentParser(description="Auditoría masiva de metas (longitud, faltantes, duplicados).")
    ap.add_argument("--file", required=True)
    ap.add_argument("--out")
    a = ap.parse_args()
    try:
        rows = list(csv.DictReader(open(a.file, encoding="utf-8-sig")))
        header = list(rows[0].keys())
    except Exception as e:  # noqa: BLE001
        print(json.dumps({"ok": False, "reason": str(e), "fallback": "modo manual: revisa cada meta con un simulador de SERP"}))
        return 0
    cu, ct, cd, ck, ch = (col(header, k) for k in ("url", "title", "desc", "keyword", "h1"))
    if not (cu and (ct or cd)):
        print(json.dumps({"ok": False, "reason": "No encuentro columnas url y title/description", "columnas": header}))
        return 0
    flags, por_titulo, por_desc = [], defaultdict(list), defaultdict(list)
    for r in rows:
        u = (r.get(cu) or "").strip()
        t = (r.get(ct) or "").strip() if ct else ""
        d = (r.get(cd) or "").strip() if cd else ""
        k = (r.get(ck) or "").strip().lower() if ck else ""
        if ct:
            if not t:
                flags.append({"url": u, "sev": "alta", "campo": "title", "msg": "Falta el meta título"})
            else:
                por_titulo[t.lower()].append(u)
                if not 50 <= len(t) <= 60:
                    flags.append({"url": u, "sev": "media", "campo": "title", "msg": f"{len(t)} caracteres (rango 50 a 60)"})
                if k and not t.lower().startswith(k) and k not in t.lower()[: len(k) + 12]:
                    flags.append({"url": u, "sev": "baja", "campo": "title", "msg": "La keyword no está al inicio"})
        if cd:
            if not d:
                flags.append({"url": u, "sev": "alta", "campo": "description", "msg": "Falta la meta descripción"})
            else:
                por_desc[d.lower()].append(u)
                if not 120 <= len(d) <= 155:
                    flags.append({"url": u, "sev": "media", "campo": "description", "msg": f"{len(d)} caracteres (rango 120 a 155)"})
    for campo, mapa in (("title", por_titulo), ("description", por_desc)):
        for txt, urls in mapa.items():
            if len(urls) > 1:
                for u in urls:
                    flags.append({"url": u, "sev": "alta", "campo": campo, "msg": f"Duplicado en {len(urls)} URLs: '{txt[:50]}'"})
    orden = {"alta": 0, "media": 1, "baja": 2}
    flags.sort(key=lambda f: (orden[f["sev"]], f["url"]))
    res = {"ok": True, "urls": len(rows), "resumen": {s: sum(1 for f in flags if f["sev"] == s) for s in orden}, "flags": flags}
    out = json.dumps(res, ensure_ascii=False, indent=2)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(out)
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
