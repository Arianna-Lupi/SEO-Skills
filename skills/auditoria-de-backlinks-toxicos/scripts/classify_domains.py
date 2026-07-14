#!/usr/bin/env python3
"""
classify_domains.py

Clasifica dominios referentes en 4 categorías de riesgo (Toxic / Suspicious /
Low-quality-but-safe / Neutral-OK) según la rúbrica en
../references/rubrica-clasificacion.md.

Entrada: CSV con al menos estas columnas (nombres de Ahrefs/Semrush export,
renombra tu CSV si hace falta):
  domain, domain_ascore, country, max_external_links, any_sitewide

Columna opcional:
  top_anchors  (para detectar anchor comercial repetido en masa)

Solo stdlib (csv, argparse). Sin dependencias externas.
"""
import argparse
import csv
import json
import sys

EXTERNAL_LINKS_THRESHOLD = 1000
ASCORE_TOXIC_CANDIDATE_MAX = 2
ASCORE_LOW_QUALITY_MIN = 3
ASCORE_LOW_QUALITY_MAX = 5


def to_bool(val):
    return str(val).strip().lower() in ("true", "1", "yes")


def to_int(val, default=None):
    try:
        return int(str(val).strip())
    except (ValueError, TypeError):
        return default


def classify(row, related_country, mass_anchor_domains):
    domain = row["domain"]
    ascore = to_int(row.get("domain_ascore"))
    country = (row.get("country") or "").strip().lower()
    max_ext = to_int(row.get("max_external_links"))
    any_sitewide = to_bool(row.get("any_sitewide"))
    mass_anchor = domain.lower() in mass_anchor_domains

    country_unrelated = country != related_country  # país vacío cuenta como no relacionado
    ext_over_threshold = max_ext is not None and max_ext > EXTERNAL_LINKS_THRESHOLD

    senales = []
    if ext_over_threshold:
        senales.append("external_gt_threshold")
    if any_sitewide:
        senales.append("sitewide")
    if country_unrelated:
        senales.append("country_unrelated")
    if mass_anchor:
        senales.append("manipulated_anchor")
    if ascore is not None and ascore <= ASCORE_TOXIC_CANDIDATE_MAX:
        senales.append("ascore_le2")

    # Toxic (a): disparador automático de granja de enlaces
    if ext_over_threshold and any_sitewide and country_unrelated:
        return "Toxic", senales, "spam-farm (regla 1a: external>umbral + sitewide + país no relacionado)"

    # Toxic (b): ascore<=2 + señal de riesgo adicional (país NUNCA cuenta como esa señal)
    if ascore is not None and ascore <= ASCORE_TOXIC_CANDIDATE_MAX:
        qualifying = {"sitewide", "external_gt_threshold", "manipulated_anchor"}
        others = [s for s in senales if s in qualifying]
        if others:
            return "Toxic", senales, f"ascore-le2-plus-signal (regla 1b: {', '.join(others)})"

    # Suspicious: ascore bajo solo
    if ascore is not None and ascore <= ASCORE_TOXIC_CANDIDATE_MAX:
        return "Suspicious", senales, "ascore-le2-solo (regla 2, sin otra señal de riesgo)"

    # Suspicious: anchor comercial en masa
    if mass_anchor:
        return "Suspicious", senales, "manipulated-anchor (regla 2, anchor repetido en masa)"

    # Suspicious: patrón de granja parcial (solo una de las 2 condiciones)
    if sum([ext_over_threshold, any_sitewide]) == 1:
        return "Suspicious", senales, "partial-farm-pattern (regla 2, cumple 1 de 2 condiciones)"

    # Low-quality-but-safe
    if ascore is not None and ASCORE_LOW_QUALITY_MIN <= ascore <= ASCORE_LOW_QUALITY_MAX:
        return "Low-quality-but-safe", senales, "ascore-3-5-clean (regla 3)"
    if max_ext is not None and 100 <= max_ext <= EXTERNAL_LINKS_THRESHOLD and not any_sitewide:
        return "Low-quality-but-safe", senales, "moderate-external-links (regla 3)"

    # Neutral-OK
    return "Neutral-OK", senales, "clean-profile (regla 4, sin señales de riesgo)"


def out(obj):
    print(json.dumps(obj, ensure_ascii=False))
    sys.exit(0)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", required=True, help="CSV de dominios referentes")
    ap.add_argument("--output", required=True, help="CSV de salida con categoría")
    ap.add_argument("--related-country", default="", help="Código de país 'relacionado' (ISO-2 minúsculas, ej. 'ca'). Vacío = ningún país cuenta como relacionado.")
    ap.add_argument("--mass-anchor-domain", action="append", default=[], help="Dominio(s) conocido(s) por usar un anchor comercial repetido en masa (repetible)")
    try:
        args = ap.parse_args()
    except SystemExit:
        out({"ok": False, "reason": "argumentos invalidos: usa --input y --output"})

    related_country = args.related_country.strip().lower()
    mass_anchor_domains = {d.strip().lower() for d in args.mass_anchor_domain}

    try:
        with open(args.input, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except OSError as e:
        out({"ok": False, "reason": f"no se pudo leer el archivo: {args.input}: {e}"})

    if not rows:
        out({"ok": False, "reason": "el CSV de entrada esta vacio o sin filas"})

    required_cols = {"domain", "domain_ascore", "country", "max_external_links", "any_sitewide"}
    missing = required_cols - set(rows[0].keys())
    if missing:
        out({"ok": False, "reason": f"faltan columnas requeridas en el CSV: {sorted(missing)}"})

    out_rows = []
    counts = {}
    for row in rows:
        categoria, senales, evidencia = classify(row, related_country, mass_anchor_domains)
        counts[categoria] = counts.get(categoria, 0) + 1
        out_rows.append({
            "domain": row["domain"],
            "domain_ascore": row.get("domain_ascore", ""),
            "country": row.get("country", ""),
            "senales": ";".join(senales),
            "categoria": categoria,
            "evidencia": evidencia,
        })

    fieldnames = ["domain", "domain_ascore", "country", "senales", "categoria", "evidencia"]
    try:
        with open(args.output, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(out_rows)
    except OSError as e:
        out({"ok": False, "reason": f"no se pudo escribir el archivo: {args.output}: {e}"})

    out({
        "ok": True,
        "rows": len(out_rows),
        "counts": {cat: counts.get(cat, 0) for cat in
                   ["Toxic", "Suspicious", "Low-quality-but-safe", "Neutral-OK"]},
        "output": args.output,
    })


if __name__ == "__main__":
    main()
