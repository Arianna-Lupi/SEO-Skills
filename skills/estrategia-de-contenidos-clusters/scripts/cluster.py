#!/usr/bin/env python3
"""
cluster.py — Agrupa una lista de keywords en clusters temáticos (determinista, sin API).

Qué hace:
  1. Normaliza cada keyword (minúsculas, sin tildes, sin stopwords ES).
  2. Calcula tokens significativos por keyword.
  3. Agrupa por solapamiento de tokens (Jaccard >= --threshold) usando un
     algoritmo greedy estable (orden alfabético para reproducibilidad).
  4. Elige un pilar por cluster: el de mayor volumen si se da, si no el head
     term más corto (menos tokens; desempate por longitud y alfabético).

Volumen opcional: con --json puedes pasar [{"keyword","volume"}] para que el
pilar use el volumen real (que viene de Ahrefs MCP, no de este script).

Uso:
  python3 cluster.py --file keywords.txt
  python3 cluster.py --file keywords.txt --threshold 0.34
  python3 cluster.py --json '[{"keyword":"rutina facial","volume":1200}, ...]'

Salida (JSON a stdout):
  {"ok": true, "clusters": [{"pilar","keywords":[...]}], "unclustered": [...], "count": N}
  o en error:
  {"ok": false, "reason": "..."}

Deps: solo stdlib.
"""

import argparse
import json
import re
import sys
import unicodedata

# Stopwords ES (lista compacta inline — suficiente para agrupar keywords).
STOPWORDS = {
    "a", "al", "algo", "ante", "como", "con", "contra", "cual", "cuando", "de",
    "del", "desde", "donde", "el", "ella", "ello", "en", "entre", "es", "esa",
    "ese", "eso", "esta", "este", "esto", "hacia", "hasta", "la", "las", "lo",
    "los", "mas", "me", "mi", "mucho", "muy", "no", "nos", "o", "para", "pero",
    "por", "porque", "que", "se", "segun", "ser", "si", "sin", "sobre", "su",
    "sus", "te", "tu", "tus", "un", "una", "uno", "unos", "unas", "y", "ya",
    "le", "les", "mejor", "mejores", "vs",
}


def out(obj):
    print(json.dumps(obj, ensure_ascii=False))
    sys.exit(0)


def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def tokens_of(keyword):
    norm = strip_accents(keyword.lower())
    raw = re.findall(r"[a-z0-9ñ]+", norm)
    return {t for t in raw if t not in STOPWORDS and len(t) > 1}


def jaccard(a, b):
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def read_items(args):
    items = []  # list of {"keyword","volume"}
    if args.json:
        try:
            data = json.loads(args.json)
        except json.JSONDecodeError as e:
            out({"ok": False, "reason": f"--json inválido: {e}"})
        for it in data:
            if isinstance(it, str):
                items.append({"keyword": it, "volume": None})
            elif isinstance(it, dict) and it.get("keyword"):
                items.append({"keyword": it["keyword"], "volume": it.get("volume")})
    elif args.file:
        try:
            with open(args.file, encoding="utf-8") as fh:
                for line in fh:
                    s = line.strip()
                    if s:
                        items.append({"keyword": s, "volume": None})
        except OSError as e:
            out({"ok": False, "reason": f"no se pudo leer --file: {e}"})
    else:
        out({"ok": False, "reason": "pasa --file o --json"})
    # dedup por keyword normalizada
    seen, uniq = set(), []
    for it in items:
        k = strip_accents(it["keyword"].lower().strip())
        if k and k not in seen:
            seen.add(k)
            uniq.append(it)
    return uniq


def pick_pilar(members):
    # members: list of {"keyword","volume","tokens"}
    with_vol = [m for m in members if isinstance(m.get("volume"), (int, float))]
    if with_vol:
        return max(with_vol, key=lambda m: m["volume"])["keyword"]
    # head term: menos tokens, luego menos caracteres, luego alfabético
    return min(members, key=lambda m: (len(m["tokens"]), len(m["keyword"]), m["keyword"].lower()))["keyword"]


def main():
    ap = argparse.ArgumentParser(
        description="Agrupa keywords en clusters por solapamiento de tokens.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Ejemplo:\n  python3 cluster.py --file keywords.txt --threshold 0.34",
    )
    ap.add_argument("--file", help="archivo con una keyword por línea")
    ap.add_argument("--json", help="JSON con lista de strings o {keyword,volume}")
    ap.add_argument("--threshold", type=float, default=0.34, help="umbral Jaccard (0-1), default 0.34")
    args = ap.parse_args()

    items = read_items(args)
    if not items:
        out({"ok": False, "reason": "sin keywords"})

    for it in items:
        it["tokens"] = tokens_of(it["keyword"])

    # orden estable para reproducibilidad
    items.sort(key=lambda m: m["keyword"].lower())

    clusters = []  # list of {"members":[...], "tokenset": set}
    unclustered = []

    for it in items:
        if not it["tokens"]:
            unclustered.append(it["keyword"])
            continue
        best, best_sim = None, 0.0
        for cl in clusters:
            sim = jaccard(it["tokens"], cl["tokenset"])
            if sim > best_sim:
                best, best_sim = cl, sim
        if best is not None and best_sim >= args.threshold:
            best["members"].append(it)
            best["tokenset"] |= it["tokens"]
        else:
            clusters.append({"members": [it], "tokenset": set(it["tokens"])})

    result = []
    for cl in clusters:
        members = cl["members"]
        pilar = pick_pilar(members)
        kws = [m["keyword"] for m in members]
        result.append({"pilar": pilar, "keywords": kws})

    # clusters más grandes primero
    result.sort(key=lambda c: (-len(c["keywords"]), c["pilar"].lower()))

    out({"ok": True, "clusters": result, "unclustered": unclustered, "count": len(items)})


if __name__ == "__main__":
    main()
