#!/usr/bin/env python3
"""
generate_disavow.py

Lee el CSV de salida de classify_domains.py, filtra los dominios "Toxic",
los agrupa en clusters temáticos legibles y escribe un disavow.txt en el
formato exacto que exige Google:
https://support.google.com/webmasters/answer/2648487

Solo dominios (no URLs individuales) salvo que se pida --url-level.
Stdlib only.
"""
import argparse
import csv
import datetime
import json
import sys


def out(obj):
    print(json.dumps(obj, ensure_ascii=False))
    sys.exit(0)


def assign_bucket(domain, evidencia):
    d = domain.lower()
    if "blogspot" in d:
        return "blogspot", "Blogspot / cluster de granja de enlaces"
    if any(s in d for s in ("backlink", "buyrank", "seo-", "-seo", "traffic")):
        return "selling", "Dominios de venta de backlinks / spam SEO"
    if "manipulated_anchor" in evidencia or "manipulated-anchor" in evidencia:
        return "anchor", "Cluster de manipulación de anchor text"
    return "other", "Otro spam tóxico / directorios masivos"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", required=True, help="CSV de classify_domains.py")
    ap.add_argument("--output", required=True, help="Ruta de salida disavow.txt")
    ap.add_argument("--site", required=True, help="Dominio del sitio auditado (para el encabezado)")
    try:
        args = ap.parse_args()
    except SystemExit:
        out({"ok": False, "reason": "argumentos invalidos: usa --input, --output y --site"})

    try:
        with open(args.input, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = [r for r in reader if r.get("categoria") == "Toxic"]
    except OSError as e:
        out({"ok": False, "reason": f"no se pudo leer el archivo: {args.input}: {e}"})

    if not rows:
        out({"ok": True, "generated": False,
             "reason": "sin dominios Toxic en el CSV: no se genera disavow.txt, revisa la clasificación"})

    buckets = {}
    titles = {}
    order = []
    for row in rows:
        key, title = assign_bucket(row["domain"], row.get("evidencia", ""))
        if key not in buckets:
            buckets[key] = []
            titles[key] = title
            order.append(key)
        buckets[key].append(row["domain"].lower())

    for key in buckets:
        buckets[key] = sorted(set(buckets[key]))

    total = sum(len(v) for v in buckets.values())

    lines = [
        f"# Disavow file - {args.site}",
        f"# Generated {datetime.date.today().isoformat()}",
        f"# Source: clasificación de riesgo ({total} dominios Toxic)",
        "# Format: domain-level entries only, per https://support.google.com/webmasters/answer/2648487",
        "#",
    ]
    for key in order:
        domains = buckets[key]
        lines.append(f"# {titles[key]} ({len(domains)} dominios)")
        for d in domains:
            lines.append(f"domain:{d}")
        lines.append("")

    while lines and lines[-1] == "":
        lines.pop()

    try:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    except OSError as e:
        out({"ok": False, "reason": f"no se pudo escribir el archivo: {args.output}: {e}"})

    out({
        "ok": True,
        "generated": True,
        "total_domains": total,
        "clusters": {titles[key]: len(buckets[key]) for key in order},
        "output": args.output,
    })


if __name__ == "__main__":
    main()
