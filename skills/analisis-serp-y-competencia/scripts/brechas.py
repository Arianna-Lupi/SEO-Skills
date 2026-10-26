#!/usr/bin/env python3
"""
brechas.py, Detecta brechas de contenido (keywords que los competidores
posicionan y tu sitio no) a partir de las posiciones por dominio. Es el paso
"Detectar brechas" de la Semana 6 del diploma "De Cero a SEO" (Arianna Lupi),
ordenado bajo el marco "Costo de Oportunidad".

Determinista y sin red: trabaja con datos que ya tienes (export de Ahrefs,
SERP capturadas con serp.py o anotadas a mano). No inventa volúmenes: si la
columna volumen no viene, queda vacía y el orden usa solo la repetición.

Entrada: CSV o JSON con filas {keyword, domain, position, url?, volume?}.
  - Una fila por (keyword, dominio) con la posición de ese dominio.
  - Pasa tu dominio con --own para separarlo de los competidores.

Qué calcula por keyword:
  - gap:        tu dominio no aparece (o está fuera de --max-pos) y hay
                competidores dentro del top --max-pos.
  - weak:       apareces, pero algún competidor te supera por --weak-gap o
                más posiciones (oportunidad de mejora).
  - defended:   estás por delante de todos los competidores analizados.
  - repetition: cuántos competidores posicionan la keyword (la señal del
                "Análisis de Repetición" del curso aplicada a keywords).
  - effort:     esfuerzo estimado de cerrar la brecha (columna "Prioridad o
                Esfuerzo" que pide Ari): bajo si apareces en 11 a 20 o algún
                competidor está fuera del top 10; alto si todos los
                competidores están en el top 3; medio en el resto.
  - Páginas: si hay url, agrupa las páginas de los competidores que cubren
    más de una brecha (candidatas al "Ojo Clínico").

Uso:
  python3 brechas.py --file posiciones.csv --own midominio.com
  python3 brechas.py --file posiciones.json --own midominio.com --max-pos 20 --weak-gap 5
  cat posiciones.csv | python3 brechas.py --file - --own midominio.com

Salida (JSON a stdout):
  {"ok": true, "own": "...", "gaps": [...], "weak": [...], "defended": [...],
   "top_pages": [{"domain","url","covers":[kw...]}], "summary": {...}}
  o {"ok": false, "reason": "...", "fallback": "..."} (exit 0)

Deps: solo stdlib.
"""
import argparse
import csv
import io
import json
import sys
from urllib.parse import urlparse


def out(obj):
    print(json.dumps(obj, ensure_ascii=False))
    sys.exit(0)


def dom(d):
    d = (d or "").strip().lower()
    if "://" in d:
        d = urlparse(d).netloc
    d = d.split("/")[0]
    return d[4:] if d.startswith("www.") else d


def f(v):
    if v in (None, ""):
        return None
    try:
        return float(str(v).replace(",", "."))
    except ValueError:
        return None


def load(raw, fmt):
    s = raw.strip()
    if not s:
        raise ValueError("entrada vacia")
    if fmt == "json" or (fmt == "auto" and s[0] in "[{"):
        obj = json.loads(s)
        if isinstance(obj, dict):
            obj = obj.get("rows") or obj.get("data") or [obj]
        rows = obj
    else:
        rd = csv.DictReader(io.StringIO(raw))
        if not rd.fieldnames:
            raise ValueError("CSV sin cabecera")
        rows = list(rd)
    res = []
    for r in rows:
        if not isinstance(r, dict):
            continue
        low = {str(k).strip().lower(): v for k, v in r.items()}
        kw = str(low.get("keyword") or low.get("query") or "").strip().lower()
        d = dom(str(low.get("domain") or low.get("dominio") or low.get("url") or ""))
        pos = f(low.get("position") or low.get("posicion") or low.get("posición"))
        if kw and d:
            res.append({"keyword": kw, "domain": d, "position": pos,
                        "url": str(low.get("url") or "").strip(), "volume": f(low.get("volume") or low.get("volumen"))})
    if not res:
        raise ValueError("no hay filas validas (keyword, domain, position)")
    return res


def main():
    ap = argparse.ArgumentParser(
        description="Brechas de contenido: qué posicionan los competidores y tú no.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Ejemplo:\n  python3 brechas.py --file posiciones.csv --own midominio.com",
    )
    ap.add_argument("--file", default="-", help="CSV o JSON ('-' = stdin).")
    ap.add_argument("--format", choices=["auto", "csv", "json"], default="auto")
    ap.add_argument("--own", required=True, help="Tu dominio (para separarlo de los competidores).")
    ap.add_argument("--max-pos", type=float, default=10, help="Posición máxima para contar a un competidor (default 10).")
    ap.add_argument("--weak-gap", type=float, default=5, help="Diferencia de posiciones para marcar 'weak' (default 5).")
    try:
        args = ap.parse_args()
    except SystemExit as e:
        if e.code == 0:
            raise
        out({"ok": False, "reason": "argumentos invalidos", "fallback": "usa --file posiciones.csv --own tudominio.com"})

    try:
        raw = sys.stdin.read() if args.file == "-" else open(args.file, encoding="utf-8-sig").read()
        rows = load(raw, args.format)
    except (OSError, ValueError, json.JSONDecodeError, csv.Error) as e:
        out({"ok": False, "reason": f"entrada invalida: {e}",
             "fallback": "modo manual: tabla keyword x competidor con la posición de cada uno (Plantilla Master, tab Competencia)."})

    own = dom(args.own)
    by_kw = {}
    for r in rows:
        by_kw.setdefault(r["keyword"], {"own": None, "comp": {}, "vol": None})
        e = by_kw[r["keyword"]]
        if r["volume"] is not None:
            e["vol"] = r["volume"]
        if r["domain"] == own:
            e["own"] = r["position"] if r["position"] is not None else e["own"]
        else:
            e["comp"][r["domain"]] = {"pos": r["position"], "url": r["url"]}

    gaps, weak, defended = [], [], []
    pages = {}
    for kw, e in by_kw.items():
        comp = {d: v for d, v in e["comp"].items() if v["pos"] is not None and v["pos"] <= args.max_pos}
        if not comp:
            continue
        best = min(v["pos"] for v in comp.values())
        worst = max(v["pos"] for v in comp.values())
        item = {"keyword": kw, "repetition": len(comp), "best_competitor_position": best,
                "competitors": sorted(comp), "own_position": e["own"], "volume": e["vol"]}
        mine = e["own"]
        if mine is None or mine > args.max_pos:
            item["effort"] = "alto" if worst <= 3 else ("bajo" if (worst > 10 or (mine is not None and mine <= 20)) else "medio")
            item["why"] = ("No apareces en el top %g y %d competidor(es) sí: brecha de contenido." % (args.max_pos, len(comp))
                           if mine is None else
                           "Estás en la posición %g, fuera del top %g, y %d competidor(es) están dentro." % (mine, args.max_pos, len(comp)))
            gaps.append(item)
            for d, v in comp.items():
                if v["url"]:
                    pages.setdefault((d, v["url"]), []).append(kw)
        elif best + args.weak_gap <= mine:
            item["effort"] = "bajo" if mine <= 20 else "medio"
            item["why"] = "Apareces en %g y un competidor está en %g: mejora de contenido, no página nueva." % (mine, best)
            weak.append(item)
        else:
            item["why"] = "Estás al nivel o por delante de los competidores analizados."
            defended.append(item)

    key = lambda x: (-x["repetition"], -(x["volume"] or 0), x["best_competitor_position"], x["keyword"])
    gaps.sort(key=key)
    weak.sort(key=key)
    top_pages = [{"domain": d, "url": u, "covers": sorted(k)} for (d, u), k in pages.items() if len(k) >= 1]
    top_pages.sort(key=lambda p: (-len(p["covers"]), p["url"]))
    out({"ok": True, "own": own, "gaps": gaps, "weak": weak, "defended": defended,
         "top_pages": top_pages[:20],
         "summary": {"keywords": len(by_kw), "gaps": len(gaps), "weak": len(weak),
                     "defended": len(defended),
                     "critical_competitors": sorted({d for g in gaps for d in g["competitors"]
                                                     if sum(1 for x in gaps if d in x["competitors"]) >= 3})}})


if __name__ == "__main__":
    main()
