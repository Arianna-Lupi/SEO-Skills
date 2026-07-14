#!/usr/bin/env python3
"""
detectar_canibalizacion.py — Detecta canibalización REAL (varias URLs de un
mismo sitio compitiendo hoy por la misma query en Google Search Console) y
clasifica severidad + acción recomendada.

Determinista: agrupa por query y aplica reglas numéricas sobre clics/
impresiones/posición, sin LLM (ahorra tokens, precisión exacta).

Diferencia con mapa-de-palabras-clave/scripts/canibalizacion.py: aquel detecta
canibalización PLANEADA (misma keyword asignada a 2 URLs en un mapa manual);
este detecta canibalización REAL ya ocurriendo, a partir del export de
Search Console con dimensiones Query + Página (o el MCP de GSC/Ahrefs).

Entrada: CSV o JSON con filas {query, url, clicks, impressions, position, ctr?}.

Usage:
    python3 detectar_canibalizacion.py --file gsc_query_page.csv
    python3 detectar_canibalizacion.py --file export.json
    cat export.csv | python3 detectar_canibalizacion.py --file -
    cat export.json | python3 detectar_canibalizacion.py --file - --format json

JSON output (stdout):
    {
      "ok": true,
      "cannibalization": [{
        "query": "...",
        "urls": [{"url","clicks","impressions","position"}, ...]  (orden: más clics primero),
        "total_clicks": N, "total_impressions": N,
        "dominance_ratio": 0.0-1.0 | null,
        "position_gap": float | null,
        "severity": "Alta|Media|Bajo",
        "action": "..."
      }],
      "summary": {"rows": N, "unique_queries": N, "unique_urls": N,
                  "cannibalized_queries": N, "by_severity": {"Alta":N,"Media":N,"Bajo":N}}
    }
On error: {"ok": false, "reason": "..."} (exit 0). Errores también a stderr.

Deps: stdlib only.
"""
import argparse
import csv
import io
import json
import sys

# Umbrales de severidad (ajustables al criterio del método).
DOMINANCE_ALTA_MAX = 0.60   # < 60% de los clics en la URL líder -> tráfico repartido de verdad
DOMINANCE_MEDIA_MAX = 0.90  # 60-90% -> reparto leve
POSITION_GAP_ALTA = 5       # top-2 URLs a <=5 posiciones de distancia y ambas <=20 -> agrava


def read_raw(path: str) -> str:
    if path == "-" or path is None:
        return sys.stdin.read()
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def to_float(v):
    if v in (None, ""):
        return None
    try:
        return float(str(v).replace(",", "."))
    except ValueError:
        return None


def normalize_row(d: dict) -> dict:
    low = {str(k).strip().lower(): v for k, v in d.items()}
    return {
        "query": (low.get("query") or low.get("keyword") or low.get("kw") or "").strip(),
        "url": (low.get("url") or low.get("page") or low.get("página") or "").strip(),
        "clicks": to_float(low.get("clicks") or low.get("clics")) or 0.0,
        "impressions": to_float(low.get("impressions") or low.get("impresiones")) or 0.0,
        "position": to_float(low.get("position") or low.get("posicion") or low.get("posición")),
    }


def parse_rows(raw: str, fmt: str) -> list:
    raw_stripped = raw.strip()
    if not raw_stripped:
        raise ValueError("entrada vacia")

    if fmt == "json" or (fmt == "auto" and raw_stripped[0] in "[{"):
        obj = json.loads(raw_stripped)
        if isinstance(obj, dict):
            obj = obj.get("rows") or obj.get("data") or [obj]
        if not isinstance(obj, list):
            raise ValueError("el JSON debe ser una lista de filas")
        return [normalize_row(r) for r in obj if isinstance(r, dict)]

    reader = csv.DictReader(io.StringIO(raw))
    if not reader.fieldnames:
        raise ValueError("CSV sin cabecera")
    return [normalize_row(r) for r in reader]


def classify(group_urls: list) -> tuple:
    """Devuelve (severity, action, dominance_ratio, position_gap)."""
    total_clicks = sum(u["clicks"] for u in group_urls)
    positions = [u["position"] for u in group_urls[:2] if u["position"] is not None]
    position_gap = abs(positions[0] - positions[1]) if len(positions) == 2 else None
    both_top20 = len(positions) == 2 and all(p <= 20 for p in positions)

    if total_clicks <= 0:
        return ("Bajo", "Solo impresiones (sin clics repartidos todavía): monitorear, no accionar aún.",
                None, position_gap)

    dominance_ratio = group_urls[0]["clicks"] / total_clicks

    if dominance_ratio < DOMINANCE_ALTA_MAX:
        severity = "Alta"
        action = ("Tráfico repartido entre varias URLs: fusiona el contenido en una sola URL canónica "
                   "(la de mejor posición/autoridad) y redirige 301 las demás.")
    elif dominance_ratio < DOMINANCE_MEDIA_MAX:
        severity = "Media"
        action = ("Una URL domina pero la otra sigue robando clics: diferencia la intención/keyword objetivo "
                   "de la URL débil (retitular, cambiar ángulo) o resuélvela con canonical + enlazado interno "
                   "hacia la fuerte.")
    else:
        severity = "Bajo"
        action = ("Dominancia casi total de una URL: probable ruido de cola larga, no canibalización real. "
                   "Revisa igual el <title>/H1 de la URL débil para que no compita por la misma keyword.")

    if position_gap is not None and position_gap <= POSITION_GAP_ALTA and both_top20 and severity == "Media":
        severity = "Alta"
        action += " Posiciones muy cercanas en el top 20: se pisan entre sí en la SERP, prioriza el fix."

    return (severity, action, round(dominance_ratio, 3), position_gap)


def main() -> int:
    p = argparse.ArgumentParser(
        description="Detecta canibalización real (query+página de GSC) y clasifica severidad/acción.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Ejemplo:\n  python3 detectar_canibalizacion.py --file gsc_query_page.csv\n"
               "  cat export.json | python3 detectar_canibalizacion.py --format json",
    )
    p.add_argument("--file", default="-", help="CSV o JSON con filas {query, url, clicks, impressions, position}. '-' = stdin.")
    p.add_argument("--format", choices=["auto", "csv", "json"], default="auto", help="Formato de entrada (auto detecta).")
    p.add_argument("--min-impressions", type=float, default=5.0,
                   help="Ignora URLs con menos impresiones que esto (ruido). Default: 5.")
    try:
        args = p.parse_args()
    except SystemExit:
        print(json.dumps({"ok": False, "reason": "argumentos invalidos: usa --file (o stdin)"}))
        return 0

    try:
        raw = read_raw(args.file)
    except OSError as e:
        print(f"error leyendo archivo: {e}", file=sys.stderr)
        print(json.dumps({"ok": False, "reason": f"no se pudo leer el archivo: {args.file}"}, ensure_ascii=False))
        return 0

    try:
        rows = parse_rows(raw, args.format)
    except (ValueError, json.JSONDecodeError, csv.Error) as e:
        print(f"error parseando entrada: {e}", file=sys.stderr)
        print(json.dumps({"ok": False, "reason": f"entrada invalida: {e}"}, ensure_ascii=False))
        return 0

    rows = [r for r in rows if r["query"] and r["url"] and r["impressions"] >= args.min_impressions]
    if not rows:
        print(json.dumps({"ok": False, "reason": "no hay filas validas con query y url (o todas por debajo de --min-impressions)"}, ensure_ascii=False))
        return 0

    by_query = {}
    for r in rows:
        key = r["query"].lower()
        by_query.setdefault(key, {"display": r["query"], "urls": {}})
        u = by_query[key]["urls"].setdefault(r["url"], {"url": r["url"], "clicks": 0.0, "impressions": 0.0, "position": None})
        u["clicks"] += r["clicks"]
        u["impressions"] += r["impressions"]
        # posición: promedio ponderado simple si hay varias filas para la misma url+query
        if r["position"] is not None:
            u["position"] = r["position"] if u["position"] is None else (u["position"] + r["position"]) / 2

    cannibalization = []
    by_severity = {"Alta": 0, "Media": 0, "Bajo": 0}
    for g in by_query.values():
        urls = list(g["urls"].values())
        if len(urls) < 2:
            continue
        urls.sort(key=lambda u: (-u["clicks"], -u["impressions"]))
        severity, action, dominance_ratio, position_gap = classify(urls)
        by_severity[severity] += 1
        cannibalization.append({
            "query": g["display"],
            "urls": [{"url": u["url"], "clicks": int(u["clicks"]), "impressions": int(u["impressions"]),
                      "position": round(u["position"], 1) if u["position"] is not None else None} for u in urls],
            "total_clicks": int(sum(u["clicks"] for u in urls)),
            "total_impressions": int(sum(u["impressions"] for u in urls)),
            "dominance_ratio": dominance_ratio,
            "position_gap": round(position_gap, 1) if position_gap is not None else None,
            "severity": severity,
            "action": action,
        })

    # Prioriza Alta primero, luego por más impresiones totales en juego.
    order = {"Alta": 0, "Media": 1, "Bajo": 2}
    cannibalization.sort(key=lambda c: (order[c["severity"]], -c["total_impressions"]))

    unique_urls = {u["url"] for r in rows for u in [r]}
    summary = {
        "rows": len(rows),
        "unique_queries": len(by_query),
        "unique_urls": len({r["url"] for r in rows}),
        "cannibalized_queries": len(cannibalization),
        "by_severity": by_severity,
    }

    out = {"ok": True, "cannibalization": cannibalization, "summary": summary}
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
