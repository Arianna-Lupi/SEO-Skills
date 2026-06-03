#!/usr/bin/env python3
"""
canibalizacion.py — Detecta canibalización de keywords (una keyword apuntando a
varias URLs) y propone quick wins, según el método del diploma "De Cero a SEO"
(mapa de keywords 1:1, una keyword principal por URL).

Determinista: agrupa por keyword y aplica reglas numéricas, sin LLM
(ahorra tokens, precisión exacta).

Entrada: CSV o JSON con filas {url, keyword, volume?, difficulty?, position?}.

Usage:
    python3 canibalizacion.py --file mapa.csv
    python3 canibalizacion.py --file mapa.json
    cat mapa.csv | python3 canibalizacion.py --file -          # asume CSV en stdin
    cat mapa.json | python3 canibalizacion.py --file - --format json

JSON output (stdout):
    {
      "ok": true,
      "cannibalization": [{"keyword": "...", "urls": ["...", "..."]}],
      "one_to_one_ok": bool,
      "quick_wins": [{"url": "...", "keyword": "...", "why": "..."}],
      "summary": {"rows": N, "unique_keywords": N, "unique_urls": N,
                  "cannibalized_keywords": N, "quick_wins": N}
    }
On error: {"ok": false, "reason": "..."} (exit 0). Errores también a stderr.

Quick win: volumen alto + dificultad baja + posición 11-20 (cerca del top 10).

Deps: stdlib only.
"""
import argparse
import csv
import io
import json
import sys

# Umbrales de quick win (ajustables al criterio del diploma).
QW_MIN_VOLUME = 200      # "alto" volumen
QW_MAX_DIFFICULTY = 30   # "baja" dificultad (KD 0-100)
QW_POS_MIN = 11          # justo fuera del top 10
QW_POS_MAX = 20


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
        "url": (low.get("url") or "").strip(),
        "keyword": (low.get("keyword") or low.get("kw") or "").strip(),
        "volume": to_float(low.get("volume") or low.get("vol")),
        "difficulty": to_float(low.get("difficulty") or low.get("kd") or low.get("dificultad")),
        "position": to_float(low.get("position") or low.get("pos") or low.get("posicion")),
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


def main() -> int:
    p = argparse.ArgumentParser(
        description="Detecta canibalización y quick wins en un mapa de keywords.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Ejemplo:\n  python3 canibalizacion.py --file mapa.csv --format csv\n  cat mapa.json | python3 canibalizacion.py --format json",
    )
    p.add_argument("--file", default="-", help="CSV o JSON con filas {url, keyword, volume?, difficulty?, position?}. '-' = stdin.")
    p.add_argument("--format", choices=["auto", "csv", "json"], default="auto", help="Formato de entrada (auto detecta).")
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

    rows = [r for r in rows if r["keyword"] and r["url"]]
    if not rows:
        print(json.dumps({"ok": False, "reason": "no hay filas validas con url y keyword"}, ensure_ascii=False))
        return 0

    # Agrupar URLs por keyword (case-insensitive en la keyword).
    by_keyword = {}
    for r in rows:
        key = r["keyword"].lower()
        by_keyword.setdefault(key, {"display": r["keyword"], "urls": []})
        if r["url"] not in by_keyword[key]["urls"]:
            by_keyword[key]["urls"].append(r["url"])

    cannibalization = [
        {"keyword": g["display"], "urls": g["urls"]}
        for g in by_keyword.values() if len(g["urls"]) > 1
    ]
    one_to_one_ok = len(cannibalization) == 0

    quick_wins = []
    for r in rows:
        vol, diff, pos = r["volume"], r["difficulty"], r["position"]
        if pos is None or not (QW_POS_MIN <= pos <= QW_POS_MAX):
            continue
        if vol is None or vol < QW_MIN_VOLUME:
            continue
        if diff is None or diff > QW_MAX_DIFFICULTY:
            continue
        quick_wins.append({
            "url": r["url"],
            "keyword": r["keyword"],
            "why": (f"posición {int(pos)} (cerca del top 10), volumen {int(vol)} alto "
                    f"y dificultad {int(diff)} baja: pequeño empujón puede entrar al top 10."),
        })

    unique_urls = {r["url"] for r in rows}
    summary = {
        "rows": len(rows),
        "unique_keywords": len(by_keyword),
        "unique_urls": len(unique_urls),
        "cannibalized_keywords": len(cannibalization),
        "quick_wins": len(quick_wins),
    }

    out = {
        "ok": True,
        "cannibalization": cannibalization,
        "one_to_one_ok": one_to_one_ok,
        "quick_wins": quick_wins,
        "summary": summary,
    }
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
