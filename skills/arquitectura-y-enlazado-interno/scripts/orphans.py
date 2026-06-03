#!/usr/bin/env python3
"""
orphans.py — Detecta páginas huérfanas y analiza enlazado interno desde exports de Screaming Frog.

Qué hace (determinista):
  1. Lee internal_all.csv (todas las URLs rastreables) y all_inlinks.csv
     (todos los enlaces internos: Source → Destination).
  2. Huérfanas = URLs en internal_all que NUNCA aparecen como Destination
     en all_inlinks (nadie las enlaza internamente).
  3. Cuenta inlinks por URL; marca las de pocos inlinks (--low, default <3).
  4. Si internal_all trae columna de profundidad de rastreo (Crawl Depth),
     lista las URLs con profundidad > 3 (regla del diploma: clics desde home).

Mapeo de columnas case-insensitive ("Address", "Destination", "Source",
"Crawl Depth"/"Depth") para tolerar exports en inglés.

Uso:
  python3 orphans.py --internal internal_all.csv --inlinks all_inlinks.csv
  python3 orphans.py --internal internal_all.csv --inlinks all_inlinks.csv --low 5

Salida (JSON a stdout):
  {"ok": true, "orphans": [...], "low_inlinks": [{"url","inlinks"}],
   "depth_gt3": [...], "summary": {...}}
  o: {"ok": false, "reason": "..."}

Deps: solo stdlib (csv).
"""

import argparse
import csv
import json
import os
import sys


def out(obj):
    print(json.dumps(obj, ensure_ascii=False))
    sys.exit(0)


def find_col(fieldnames, *candidates):
    low = {fn.lower().strip(): fn for fn in (fieldnames or [])}
    for c in candidates:
        if c.lower() in low:
            return low[c.lower()]
    for c in candidates:
        for k, orig in low.items():
            if c.lower() in k:
                return orig
    return None


def open_csv(path):
    return open(path, newline="", encoding="utf-8-sig")


def main():
    ap = argparse.ArgumentParser(
        description="Huérfanas + enlazado interno desde exports de SF.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Ejemplo:\n  python3 orphans.py --internal internal_all.csv --inlinks all_inlinks.csv --low 3",
    )
    ap.add_argument("--internal", required=True, help="ruta a internal_all.csv")
    ap.add_argument("--inlinks", required=True, help="ruta a all_inlinks.csv")
    ap.add_argument("--low", type=int, default=3, help="umbral de pocos inlinks (default <3)")
    args = ap.parse_args()

    for p in (args.internal, args.inlinks):
        if not os.path.isfile(p):
            out({"ok": False, "reason": f"no existe el archivo: {p}"})

    # 1) URLs del crawl + profundidad
    internal_urls = []
    depth_by_url = {}
    try:
        with open_csv(args.internal) as fh:
            reader = csv.DictReader(fh)
            addr_c = find_col(reader.fieldnames, "Address", "URL")
            depth_c = find_col(reader.fieldnames, "Crawl Depth", "Depth")
            if not addr_c:
                out({"ok": False, "reason": "internal_all sin columna Address/URL"})
            for row in reader:
                url = (row.get(addr_c) or "").strip()
                if not url:
                    continue
                internal_urls.append(url)
                if depth_c:
                    d = (row.get(depth_c) or "").strip()
                    try:
                        depth_by_url[url] = int(float(d))
                    except ValueError:
                        pass
    except Exception as e:  # noqa: BLE001
        out({"ok": False, "reason": f"error leyendo internal: {e}"})

    internal_set = set(internal_urls)

    # 2) inlinks: conteo por Destination
    inlink_count = {u: 0 for u in internal_set}
    destinations = set()
    try:
        with open_csv(args.inlinks) as fh:
            reader = csv.DictReader(fh)
            dest_c = find_col(reader.fieldnames, "Destination", "Target", "To")
            if not dest_c:
                out({"ok": False, "reason": "all_inlinks sin columna Destination"})
            for row in reader:
                dest = (row.get(dest_c) or "").strip()
                if not dest:
                    continue
                destinations.add(dest)
                if dest in inlink_count:
                    inlink_count[dest] += 1
                else:
                    inlink_count[dest] = inlink_count.get(dest, 0) + 1
    except Exception as e:  # noqa: BLE001
        out({"ok": False, "reason": f"error leyendo inlinks: {e}"})

    # 3) huérfanas: en el crawl pero nunca destino de un enlace interno
    orphans = sorted(u for u in internal_set if u not in destinations)

    # 4) pocos inlinks (solo URLs del crawl)
    low_inlinks = sorted(
        ({"url": u, "inlinks": inlink_count.get(u, 0)} for u in internal_set
         if inlink_count.get(u, 0) < args.low and u not in set(orphans)),
        key=lambda x: (x["inlinks"], x["url"]),
    )

    # profundidad > 3
    depth_gt3 = sorted(u for u, d in depth_by_url.items() if d > 3)

    summary = {
        "urls_total": len(internal_set),
        "orphans": len(orphans),
        "low_inlinks": len(low_inlinks),
        "low_threshold": args.low,
        "depth_gt3": len(depth_gt3),
        "has_depth_column": bool(depth_by_url),
    }

    out({"ok": True, "orphans": orphans, "low_inlinks": low_inlinks,
         "depth_gt3": depth_gt3, "summary": summary})


if __name__ == "__main__":
    main()
