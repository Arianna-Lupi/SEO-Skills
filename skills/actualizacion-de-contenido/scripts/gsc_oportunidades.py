#!/usr/bin/env python3
"""
gsc_oportunidades.py: detecta oportunidades de actualización a partir de un export de Search Console.

Método del diplomado (Semana 10, lección 2): "deja que los datos hablen". Busca:
  - Keywords de umbral: ya tienen impresiones pero no están en el Top 3 (posición > 3).
  - Páginas con muchas impresiones y CTR bajo (candidatas a "solo metadatos").
  - Keywords secundarias: consultas por las que la página ya aparece y que NO están en su texto
    (si pasas --texto con el contenido actual de la URL).
Y sugiere un alcance orientativo (solo metadatos / expansión / cambio total) para el Brief de Optimización.

Entrada: CSV exportado de Search Console (Rendimiento > Consultas, filtrado por UNA página) o
un CSV con columnas de consulta y, si es de varias páginas, una columna de página.
Columnas reconocidas (español o inglés): consulta|query|consultas principales, página|page,
clics|clicks, impresiones|impressions, ctr, posición|position.

Uso:
  python3 gsc_oportunidades.py --file consultas.csv [--texto pagina-actual.txt] [--min-impresiones 10] \
      [--out .seo-audit/<sitio>/data/actualizacion.json]

Los umbrales (--min-impresiones, posición 4 a 20, CTR comparado con la mediana del propio export)
son heurísticas de trabajo, no cifras de Google. Solo stdlib. Si falla: {"ok": false, ...} exit 0.
"""
import argparse
import csv
import json
import re
import statistics
import sys
from collections import defaultdict

ALIAS = {
    "q": ("consulta", "consultas principales", "query", "top queries", "keyword"),
    "page": ("página", "pagina", "page", "url", "páginas principales", "top pages"),
    "clicks": ("clics", "clicks"),
    "impr": ("impresiones", "impressions"),
    "ctr": ("ctr",),
    "pos": ("posición", "posicion", "position", "posición media"),
}


def num(v):
    v = (v or "").strip().replace("%", "").replace(" ", "")
    if not v:
        return None
    if "," in v and "." in v:
        v = v.replace(".", "").replace(",", ".")
    elif "," in v:
        v = v.replace(",", ".")
    try:
        return float(v)
    except ValueError:
        return None


def main():
    ap = argparse.ArgumentParser(description="Oportunidades de actualización desde un export de Search Console.")
    ap.add_argument("--file", required=True)
    ap.add_argument("--texto", help="Texto actual de la página (para detectar secundarias no cubiertas)")
    ap.add_argument("--min-impresiones", type=int, default=10)
    ap.add_argument("--out")
    a = ap.parse_args()
    try:
        rows = list(csv.DictReader(open(a.file, encoding="utf-8-sig")))
        low = {h.strip().lower(): h for h in rows[0].keys()}
    except Exception as e:  # noqa: BLE001
        print(json.dumps({"ok": False, "reason": str(e), "fallback": "modo manual: en Search Console filtra por la página y revisa impresiones, CTR y posición"}))
        return 0
    c = {k: next((low[x] for x in v if x in low), None) for k, v in ALIAS.items()}
    if not (c["q"] and c["impr"] and c["pos"]):
        print(json.dumps({"ok": False, "reason": "Faltan columnas consulta, impresiones o posición", "columnas": list(low)}))
        return 0
    texto = ""
    if a.texto:
        try:
            texto = open(a.texto, encoding="utf-8").read().lower()
        except Exception as e:  # noqa: BLE001
            print(json.dumps({"ok": False, "reason": f"No pude leer --texto: {e}"}))
            return 0

    paginas = defaultdict(list)
    for r in rows:
        impr, pos = num(r.get(c["impr"])), num(r.get(c["pos"]))
        if impr is None or pos is None:
            continue
        paginas[(r.get(c["page"]) or "(export de una sola página)") if c["page"] else "(export de una sola página)"].append({
            "consulta": r[c["q"]], "impresiones": impr, "posicion": pos,
            "clics": num(r.get(c["clicks"])) if c["clicks"] else None,
            "ctr": num(r.get(c["ctr"])) if c["ctr"] else None})

    salida = []
    for pag, qs in paginas.items():
        umbral = sorted([q for q in qs if 3 < q["posicion"] <= 20 and q["impresiones"] >= a.min_impresiones],
                        key=lambda q: -q["impresiones"])
        ctrs = [q["ctr"] for q in qs if q["ctr"] is not None and q["impresiones"] >= a.min_impresiones]
        med = statistics.median(ctrs) if ctrs else None
        ctr_bajo = [q for q in qs if med is not None and q["ctr"] is not None and q["posicion"] <= 10
                    and q["impresiones"] >= a.min_impresiones and q["ctr"] < med / 2]
        no_cubiertas = [q["consulta"] for q in umbral if texto and q["consulta"].lower() not in texto] if texto else None
        fruta = [q for q in umbral if 8 <= q["posicion"] <= 20]
        # alcance orientativo
        if no_cubiertas and len(no_cubiertas) >= 3:
            alcance = "expansión: añade secciones (H2/H3) para las consultas no cubiertas"
        elif ctr_bajo or fruta:
            alcance = "solo metadatos y H2: hay visibilidad que no se convierte en clic (victoria rápida)"
        elif not umbral:
            alcance = "revisa la intención en la SERP: sin impresiones útiles puede ser cambio total o no optimizar"
        else:
            alcance = "ajuste leve: metas, H2 y enlaces internos"
        salida.append({"pagina": pag, "consultas": len(qs),
                       "keywords_umbral": [{"consulta": q["consulta"], "impresiones": q["impresiones"], "posicion": q["posicion"]} for q in umbral[:15]],
                       "ctr_bajo_vs_mediana": [q["consulta"] for q in ctr_bajo[:10]],
                       "secundarias_no_cubiertas_en_el_texto": no_cubiertas[:15] if no_cubiertas is not None else "pasa --texto para calcularlo",
                       "victorias_rapidas_pagina_2": [q["consulta"] for q in fruta[:10]],
                       "alcance_orientativo": alcance})
    res = {"ok": True, "paginas": salida, "umbral_impresiones": a.min_impresiones,
           "nota": "Heurísticas de trabajo. Valida la intención en la SERP antes de cambiar la keyword y no cambies la URL si ya tiene tráfico (Semana 10, lección 4)."}
    out = json.dumps(res, ensure_ascii=False, indent=2)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(out)
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
