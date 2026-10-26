#!/usr/bin/env python3
"""
anchor_profile.py: distribucion de anchor text y concentracion por dominio de un export de backlinks.

Complemento externo adaptado de claude-seo (MIT, agricidaniel), reescrito con solo stdlib.
Los rangos son heuristicas de terceros, no del diplomado: usalos para levantar banderas,
no como veredicto. La regla del diplomado/coaches (Vero) es mas simple: anchor limpio con la
keyword principal, sin numeros ni adornos (coaches/vero.md, Off page).

Uso:
    python3 anchor_profile.py --input backlinks.csv --brand "aprendoseo,aprendo seo" --keywords "seo,curso de seo"
    python3 anchor_profile.py --input backlinks.csv --brand marca --out .seo-audit/sitio.com/data/backlinks.json

Entrada CSV (nombres de columna flexibles, sin distinguir mayusculas):
    anchor / texto de anclaje ; source / url de origen / dominio referente ; opcional nofollow / rel
Salida JSON: {"ok":true,"total":N,"distribution":{tipo:{count,pct}},"top_domains":[...],
              "flags":[...],"benchmarks":{...},"note":"..."}
Con --out se FUSIONA la clave "anchors" en el JSON existente (backlinks.json) sin pisar el resto.
Deps: solo stdlib.
"""
import argparse
import csv
import json
import os
import re
import sys
from collections import Counter
from urllib.parse import urlparse

GENERIC = {"click here", "aqui", "aquí", "haz clic aqui", "haz clic aquí", "clic aqui", "ver mas", "ver más",
           "leer mas", "leer más", "mas informacion", "más información", "este sitio", "sitio web", "pagina web",
           "página web", "web", "enlace", "link", "visita", "pincha aqui", "pincha aquí", "source", "fuente",
           "read more", "learn more", "website", "here", "this"}
BENCH = {"marca": "30 a 50%", "url": "15 a 25%", "generico": "10 a 20%",
         "exacta": "3 a 10% (revisar si pasa de 15%)", "parcial": "5 a 15% (revisar si pasa de 25%)"}


def col(fields, *names):
    low = {f.lower().strip(): f for f in fields or []}
    for n in names:
        if n in low:
            return low[n]
    for n in names:
        for k, o in low.items():
            if n in k:
                return o
    return None


def classify(anchor, brands, kws):
    a = anchor.strip().lower()
    if not a:
        return "vacio"
    if re.match(r"^(https?://|www\.)", a) or re.match(r"^[\w.-]+\.[a-z]{2,}(/.*)?$", a):
        return "url"
    if any(b and b in a for b in brands):
        return "marca"
    if a in GENERIC:
        return "generico"
    if a in kws:
        return "exacta"
    if any(k and k in a for k in kws):
        return "parcial"
    return "natural"


def main():
    p = argparse.ArgumentParser(description="Distribucion de anchors y concentracion por dominio.")
    p.add_argument("--input", required=True, help="CSV de backlinks.")
    p.add_argument("--brand", default="", help="Terminos de marca separados por coma.")
    p.add_argument("--keywords", default="", help="Keywords objetivo separadas por coma (anchor exacto/parcial).")
    p.add_argument("--out", help="JSON donde fusionar la clave 'anchors' (ej. .../data/backlinks.json).")
    a = p.parse_args()
    brands = [b.strip().lower() for b in a.brand.split(",") if b.strip()]
    kws = [k.strip().lower() for k in a.keywords.split(",") if k.strip()]
    try:
        with open(a.input, encoding="utf-8-sig", newline="") as f:
            sample = f.read(4096)
            f.seek(0)
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t") if sample else csv.excel
            rd = csv.DictReader(f, dialect=dialect)
            ca = col(rd.fieldnames, "anchor", "texto de anclaje", "texto ancla")
            cs = col(rd.fieldnames, "source", "url de origen", "referring page", "dominio referente", "domain", "from")
            if not ca:
                raise ValueError("no encuentro columna de anchor")
            rows = list(rd)
    except (OSError, ValueError, csv.Error) as e:
        print(json.dumps({"ok": False, "reason": str(e),
                          "fallback": "modo manual: cuenta anchors por tipo en la hoja de calculo"}, ensure_ascii=False))
        return
    types, doms = Counter(), Counter()
    for r in rows:
        types[classify(r.get(ca, ""), brands, kws)] += 1
        if cs and r.get(cs):
            v = r[cs].strip()
            d = urlparse(v if "//" in v else "//" + v).netloc.lower() or v.lower()
            doms[d.removeprefix("www.")] += 1
    n = len(rows) or 1
    dist = {t: {"count": c, "pct": round(100 * c / n, 1)} for t, c in types.most_common()}
    flags = []
    pct = lambda t: dist.get(t, {}).get("pct", 0)  # noqa: E731
    if kws and pct("exacta") > 15:
        flags.append(f"Anchor exacto en {pct('exacta')}%: revisar patron antinatural (heuristica: mas de 15%).")
    if kws and pct("parcial") > 25:
        flags.append(f"Anchor parcial en {pct('parcial')}%: revisar (heuristica: mas de 25%).")
    if brands and pct("marca") < 15:
        flags.append(f"Anchor de marca en {pct('marca')}%: perfil poco natural (heuristica: menos de 15%).")
    top = [{"domain": d, "count": c, "pct": round(100 * c / n, 1)} for d, c in doms.most_common(10)]
    if top and top[0]["pct"] > 10:
        flags.append(f"Un dominio concentra {top[0]['pct']}% de los enlaces ({top[0]['domain']}): revisar.")
    res = {"ok": True, "total": len(rows), "distribution": dist, "top_domains": top, "flags": flags,
           "benchmarks": BENCH,
           "note": "Rangos heuristicos de terceros (claude-seo). No son del diplomado ni verdades de Google."}
    if a.out:
        ex = {}
        if os.path.exists(a.out):
            try:
                ex = json.load(open(a.out, encoding="utf-8"))
            except ValueError:
                ex = {}
        ex["anchors"] = {k: res[k] for k in ("total", "distribution", "top_domains", "flags", "benchmarks", "note")}
        os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
        json.dump(ex, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(json.dumps(res, ensure_ascii=False))


if __name__ == "__main__":
    main()
