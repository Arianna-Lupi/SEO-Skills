#!/usr/bin/env python3
"""
serp_overlap.py: agrupa keywords por solapamiento real de SERP (complemento externo, adaptado).

Idea: dos keywords que devuelven casi las mismas URLs en el top 10 se resuelven con
la MISMA página; si no comparten resultados, necesitan páginas distintas. Esto evita
la canibalización antes de producir y afina los clusters de la Semana 7.

NO consulta ninguna SERP: tú le pasas las URLs ya obtenidas (SerpApi, Ahrefs, a mano).

Entrada (JSON): {"keyword a": ["https://x.com/1", "https://y.com/2", ...], "keyword b": [...]}
Uso:
  python3 serp_overlap.py --file serps.json [--ignorar-dominios wikipedia.org,youtube.com]
  python3 serp_overlap.py --file serps.json --out serp-overlap.json

Umbrales (de claude-seo, valores de partida; el criterio final lo pones tú):
  7 a 10 URLs compartidas : misma página (fusionar, una keyword principal)
  4 a 6                   : mismo cluster (páginas distintas del mismo tema)
  2 a 3                   : enlazar entre ellas (clusters vecinos)
  0 a 1                   : separadas

Salida JSON: matriz de pares, grupos "misma_pagina" y "mismo_cluster", y avisos de
canibalización. Solo stdlib. Si el archivo no existe: {"ok": false, ...} con exit 0.
"""
import argparse
import itertools
import json
import sys
from urllib.parse import urlparse


def norm(u):
    p = urlparse(u.strip())
    host = p.netloc.lower().removeprefix("www.")
    return host + p.path.rstrip("/").lower()


def host_of(u):
    return urlparse(u.strip()).netloc.lower().removeprefix("www.")


class UF:
    def __init__(self, items):
        self.p = {i: i for i in items}

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        self.p[self.find(a)] = self.find(b)


def relacion(n):
    if n >= 7:
        return "misma_pagina"
    if n >= 4:
        return "mismo_cluster"
    if n >= 2:
        return "enlazar"
    return "separadas"


def main():
    ap = argparse.ArgumentParser(description="Clustering por solapamiento de SERP (top 10 por keyword).")
    ap.add_argument("--file", required=True, help="JSON {keyword: [urls]}")
    ap.add_argument("--ignorar-dominios", default="", help="Dominios que aparecen en todo (coma). Se quitan antes de contar.")
    ap.add_argument("--out", help="Ruta de salida JSON (p.ej. .seo-audit/<sitio>/data/serp-overlap.json)")
    a = ap.parse_args()
    try:
        data = json.load(open(a.file, encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print(json.dumps({"ok": False, "reason": str(e), "fallback": "modo manual: compara los 10 primeros resultados de cada par en la SERP"}))
        return 0
    ign = {d.strip().lower().removeprefix("www.") for d in a.ignorar_dominios.split(",") if d.strip()}
    sets = {k: {norm(u) for u in v if host_of(u) not in ign} for k, v in data.items()}
    kws = list(sets)
    pares, uf_p, uf_c = [], UF(kws), UF(kws)
    for x, y in itertools.combinations(kws, 2):
        n = len(sets[x] & sets[y])
        rel = relacion(n)
        pares.append({"a": x, "b": y, "compartidas": n, "relacion": rel})
        if rel == "misma_pagina":
            uf_p.union(x, y)
        if rel in ("misma_pagina", "mismo_cluster"):
            uf_c.union(x, y)

    def grupos(uf):
        g = {}
        for k in kws:
            g.setdefault(uf.find(k), []).append(k)
        return [v for v in g.values() if len(v) > 1]

    avisos = [f"Canibalización probable: '{p['a']}' y '{p['b']}' comparten {p['compartidas']} URLs. Una sola página con una keyword principal."
              for p in pares if p["relacion"] == "misma_pagina"]
    res = {"ok": True, "keywords": len(kws), "pares": sorted(pares, key=lambda p: -p["compartidas"]),
           "misma_pagina": grupos(uf_p), "mismo_cluster": grupos(uf_c), "avisos": avisos,
           "nota": "Los umbrales son valores de partida de claude-seo; el cluster final lo decide la intención y el negocio (Semana 7)."}
    out = json.dumps(res, ensure_ascii=False, indent=2)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(out)
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
