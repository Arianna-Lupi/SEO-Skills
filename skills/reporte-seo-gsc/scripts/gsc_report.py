#!/usr/bin/env python3
"""
gsc_report.py — Compara mes vs. mes desde exports de Google Search Console (determinista).

Qué hace:
  1. Lee dos CSV de "Rendimiento" de GSC (--current y --previous). Columnas
     esperadas: Query o Page (dimensión), Clicks, Impressions, CTR, Position.
  2. Calcula totales y deltas % de clics, impresiones, CTR y posición.
  3. Empareja filas por la dimensión (query/página) y saca ganadores y
     perdedores por variación de clics.
  4. Genera insights con las reglas de interpretación del diploma
     (impresiones ↑ + clics ↓ = problema de CTR/Meta Title, etc.).

Mapeo de columnas case-insensitive y tolerante a CTR con "%" y posición con coma.

Uso:
  python3 gsc_report.py --current mayo.csv --previous abril.csv
  python3 gsc_report.py --current pages_cur.csv --previous pages_prev.csv --top 15

Salida (JSON a stdout):
  {"ok": true, "totals": {"clicks":{"cur","prev","delta_pct"}, "impressions":{...},
   "ctr":{...}, "position":{...}}, "winners":[...], "losers":[...], "insights":[...]}
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


def to_float(val):
    if val is None:
        return 0.0
    s = str(val).strip().replace("%", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return 0.0


def to_int(val):
    return int(round(to_float(val)))


def load(path):
    rows = {}  # dim -> {"clicks","impressions","ctr","position"}
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        dim_c = find_col(reader.fieldnames, "Query", "Consulta", "Page", "Página", "Pagina", "URL")
        clk_c = find_col(reader.fieldnames, "Clicks", "Clics")
        imp_c = find_col(reader.fieldnames, "Impressions", "Impresiones")
        ctr_c = find_col(reader.fieldnames, "CTR")
        pos_c = find_col(reader.fieldnames, "Position", "Posición", "Posicion")
        if not dim_c:
            raise ValueError("sin columna de dimensión (Query/Page)")
        for row in reader:
            dim = (row.get(dim_c) or "").strip()
            if not dim:
                continue
            rows[dim] = {
                "clicks": to_int(row.get(clk_c)) if clk_c else 0,
                "impressions": to_int(row.get(imp_c)) if imp_c else 0,
                "ctr": to_float(row.get(ctr_c)) if ctr_c else 0.0,
                "position": to_float(row.get(pos_c)) if pos_c else 0.0,
            }
    return rows


def delta_pct(cur, prev):
    if prev == 0:
        return None if cur == 0 else 100.0
    return round((cur - prev) / prev * 100, 1)


def totals_of(rows):
    clicks = sum(r["clicks"] for r in rows.values())
    impressions = sum(r["impressions"] for r in rows.values())
    ctr = round(clicks / impressions * 100, 2) if impressions else 0.0
    poss = [r["position"] for r in rows.values() if r["position"] > 0]
    position = round(sum(poss) / len(poss), 1) if poss else 0.0
    return clicks, impressions, ctr, position


def main():
    ap = argparse.ArgumentParser(
        description="Reporte GSC mes vs. mes con insights del diploma.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Ejemplo:\n  python3 gsc_report.py --current actual.csv --previous anterior.csv --top 10",
    )
    ap.add_argument("--current", required=True, help="CSV del periodo actual")
    ap.add_argument("--previous", required=True, help="CSV del periodo anterior")
    ap.add_argument("--top", type=int, default=10, help="cuántos ganadores/perdedores listar")
    args = ap.parse_args()

    for p in (args.current, args.previous):
        if not os.path.isfile(p):
            out({"ok": False, "reason": f"no existe el archivo: {p}"})

    try:
        cur = load(args.current)
        prev = load(args.previous)
    except Exception as e:  # noqa: BLE001
        out({"ok": False, "reason": f"error leyendo CSV: {e}"})

    c_clk, c_imp, c_ctr, c_pos = totals_of(cur)
    p_clk, p_imp, p_ctr, p_pos = totals_of(prev)

    totals = {
        "clicks": {"cur": c_clk, "prev": p_clk, "delta_pct": delta_pct(c_clk, p_clk)},
        "impressions": {"cur": c_imp, "prev": p_imp, "delta_pct": delta_pct(c_imp, p_imp)},
        "ctr": {"cur": c_ctr, "prev": p_ctr, "delta_pct": delta_pct(c_ctr, p_ctr)},
        # posición: baja = mejora; delta en puntos (no %)
        "position": {"cur": c_pos, "prev": p_pos, "delta_pts": round(c_pos - p_pos, 1)},
    }

    # ganadores / perdedores por variación de clics
    diffs = []
    for dim in set(cur) | set(prev):
        cc = cur.get(dim, {}).get("clicks", 0)
        pc = prev.get(dim, {}).get("clicks", 0)
        diffs.append({"dim": dim, "clicks_cur": cc, "clicks_prev": pc, "delta": cc - pc})
    winners = sorted([d for d in diffs if d["delta"] > 0], key=lambda d: -d["delta"])[: args.top]
    losers = sorted([d for d in diffs if d["delta"] < 0], key=lambda d: d["delta"])[: args.top]

    # reglas de interpretación del diploma
    insights = []
    di = totals["impressions"]["delta_pct"]
    dc = totals["clicks"]["delta_pct"]
    dpos = totals["position"]["delta_pts"]
    if di is not None and dc is not None:
        if di > 0 and dc <= 0:
            insights.append("impresiones ↑ + clics ↓ → problema de CTR/Meta Title: reescribe titles y meta descriptions.")
        elif di > 0 and dc > 0:
            insights.append("impresiones ↑ + clics ↑ → crecimiento sano: refuerza el contenido que sube.")
        elif di <= 0 and dc <= 0:
            insights.append("impresiones ↓ + clics ↓ → posible pérdida de posiciones o estacionalidad: revisa ranking y canibalización.")
    if dpos is not None:
        if dpos < -0.3:
            insights.append("posición media mejora (sube en SERP): consolida con enlazado interno a esas URLs.")
        elif dpos > 0.3:
            insights.append("posición media empeora: revisa contenido desactualizado y competidores que te superaron.")
    if c_imp > 0 and c_ctr > 0 and c_pos and c_pos <= 10 and c_ctr < 3:
        insights.append("estás en top 10 pero con CTR bajo (<3%): el snippet no atrae clics; prioriza optimizar title/description.")
    if not insights:
        insights.append("sin variaciones relevantes mes vs. mes; mantené la estrategia y monitorea.")

    out({"ok": True, "totals": totals, "winners": winners, "losers": losers, "insights": insights})


if __name__ == "__main__":
    main()
