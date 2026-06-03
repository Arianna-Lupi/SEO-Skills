#!/usr/bin/env python3
"""
parse_sf.py — Resume exports de Screaming Frog en un sumario de severidad (determinista).

Qué hace:
  1. Lee internal_all.csv (o autodetecta dentro de --folder) y cuenta URLs,
     códigos de estado (200/3xx/4xx/5xx) y no indexables.
  2. Agrupa por "template hint" según el primer segmento del path de la URL
     (p.ej. /blog/, /producto/, raíz) para detectar dónde se concentran problemas.
  3. Si se da un CSV de issues (--issues, p.ej. issues_overview_report.csv),
     lista issue + conteo + severity_hint (mapeo heurístico por palabra clave).
  4. Reporta archivos esperados que faltan.

Mapeo de columnas robusto: case-insensitive sobre "Address", "Status Code",
"Indexability" (y variantes), así sirve para exports en inglés.

Uso:
  python3 parse_sf.py --folder ./export_sf
  python3 parse_sf.py --internal internal_all.csv --issues issues_overview_report.csv

Salida (JSON a stdout):
  {"ok": true, "urls_total": N, "status_codes": {...}, "non_indexable": N,
   "by_template_hint": {...}, "issues": [{"issue","severity_hint","count"}],
   "missing_files": [...]}
  o: {"ok": false, "reason": "..."}

Deps: solo stdlib (csv).
"""

import argparse
import csv
import json
import os
import sys
from urllib.parse import urlparse

EXPECTED = ["internal_all.csv", "all_inlinks.csv", "issues_overview_report.csv"]

SEVERITY_RULES = [
    ("high", ["5xx", "broken", "404", "4xx", "no response", "redirect chain",
              "redirect loop", "missing", "canonical", "noindex", "duplicate"]),
    ("medium", ["3xx", "redirect", "long", "multiple", "missing alt",
                "title", "meta description", "h1", "h2"]),
    ("low", ["over", "short", "outside", "low content"]),
]


def out(obj):
    print(json.dumps(obj, ensure_ascii=False))
    sys.exit(0)


def find_col(fieldnames, *candidates):
    low = {fn.lower().strip(): fn for fn in (fieldnames or [])}
    for c in candidates:
        if c.lower() in low:
            return low[c.lower()]
    # match parcial
    for c in candidates:
        for k, orig in low.items():
            if c.lower() in k:
                return orig
    return None


def open_csv(path):
    # SF usa UTF-8 (a veces con BOM)
    return open(path, newline="", encoding="utf-8-sig")


def template_hint(url):
    try:
        p = urlparse(url)
        segs = [s for s in p.path.split("/") if s]
        if not segs:
            return "/(home)"
        return "/" + segs[0] + "/"
    except Exception:  # noqa: BLE001
        return "(desconocido)"


def severity_for(issue):
    low = issue.lower()
    for sev, kws in SEVERITY_RULES:
        if any(k in low for k in kws):
            return sev
    return "info"


def parse_internal(path):
    status = {"200": 0, "3xx": 0, "4xx": 0, "5xx": 0, "other": 0}
    by_template = {}
    non_indexable = 0
    total = 0
    with open_csv(path) as fh:
        reader = csv.DictReader(fh)
        addr_c = find_col(reader.fieldnames, "Address", "URL")
        code_c = find_col(reader.fieldnames, "Status Code", "Status")
        idx_c = find_col(reader.fieldnames, "Indexability")
        for row in reader:
            total += 1
            url = (row.get(addr_c) or "").strip() if addr_c else ""
            code = (row.get(code_c) or "").strip() if code_c else ""
            try:
                ci = int(code)
                if ci == 200:
                    status["200"] += 1
                elif 300 <= ci < 400:
                    status["3xx"] += 1
                elif 400 <= ci < 500:
                    status["4xx"] += 1
                elif 500 <= ci < 600:
                    status["5xx"] += 1
                else:
                    status["other"] += 1
            except ValueError:
                status["other"] += 1
            if idx_c:
                indexability = (row.get(idx_c) or "").strip().lower()
                if indexability and indexability != "indexable":
                    non_indexable += 1
            if url:
                h = template_hint(url)
                by_template[h] = by_template.get(h, 0) + 1
    return total, status, non_indexable, by_template


def parse_issues(path):
    issues = []
    with open_csv(path) as fh:
        reader = csv.DictReader(fh)
        name_c = find_col(reader.fieldnames, "Issue Name", "Issue", "Name")
        cnt_c = find_col(reader.fieldnames, "URLs", "Count", "No. URLs", "Number")
        sev_c = find_col(reader.fieldnames, "Issue Priority", "Priority", "Severity")
        for row in reader:
            name = (row.get(name_c) or "").strip() if name_c else ""
            if not name:
                continue
            cnt = 0
            if cnt_c:
                try:
                    cnt = int(float((row.get(cnt_c) or "0").replace(",", "").strip() or 0))
                except ValueError:
                    cnt = 0
            sev = (row.get(sev_c) or "").strip().lower() if sev_c else ""
            sev_hint = sev if sev in ("high", "medium", "low") else severity_for(name)
            issues.append({"issue": name, "severity_hint": sev_hint, "count": cnt})
    sev_order = {"high": 0, "medium": 1, "low": 2, "info": 3}
    issues.sort(key=lambda i: (sev_order.get(i["severity_hint"], 9), -i["count"]))
    return issues


def main():
    ap = argparse.ArgumentParser(
        description="Resume exports de Screaming Frog.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Ejemplo:\n  python3 parse_sf.py --folder ./sf_export\n  python3 parse_sf.py --internal internal_all.csv --issues issues_overview_report.csv",
    )
    ap.add_argument("--folder", help="carpeta con los CSV de SF")
    ap.add_argument("--internal", help="ruta a internal_all.csv")
    ap.add_argument("--issues", help="ruta a issues_overview_report.csv")
    args = ap.parse_args()

    internal = args.internal
    issues_path = args.issues
    missing = []

    if args.folder:
        files = {f.lower(): os.path.join(args.folder, f)
                 for f in os.listdir(args.folder)} if os.path.isdir(args.folder) else {}
        if not internal:
            internal = files.get("internal_all.csv")
        if not issues_path:
            issues_path = files.get("issues_overview_report.csv")
        for exp in EXPECTED:
            if exp not in files:
                missing.append(exp)

    if not internal or not os.path.isfile(internal):
        out({"ok": False, "reason": "falta internal_all.csv (usa --internal o --folder)",
             "missing_files": missing})

    try:
        total, status, non_indexable, by_template = parse_internal(internal)
    except Exception as e:  # noqa: BLE001
        out({"ok": False, "reason": f"error leyendo internal: {e}"})

    issues = []
    if issues_path and os.path.isfile(issues_path):
        try:
            issues = parse_issues(issues_path)
        except Exception as e:  # noqa: BLE001
            issues = []
            missing.append(f"issues ilegible: {e}")

    out({
        "ok": True,
        "urls_total": total,
        "status_codes": status,
        "non_indexable": non_indexable,
        "by_template_hint": dict(sorted(by_template.items(), key=lambda kv: -kv[1])),
        "issues": issues,
        "missing_files": missing,
    })


if __name__ == "__main__":
    main()
