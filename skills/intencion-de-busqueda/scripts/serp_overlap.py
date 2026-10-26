#!/usr/bin/env python3
"""
serp_overlap.py, Valida la intención de búsqueda leyendo la SERP, según el
método del diploma "De Cero a SEO" (Semana 4 · "Cómo posicionar palabras
claves" y Semana 5 · "Cómo evaluar la intención del usuario"; criterio de
Vero: si dos keywords muestran casi las mismas páginas, comparten intención y
van en UNA sola URL).

Determinista y sin red: trabaja sobre las SERP que ya capturaste (con
`analisis-serp-y-competencia/scripts/serp.py`, SerpApi/Ahrefs MCP o a mano).

Hace dos cosas:
  1. Solape de SERP entre pares de keywords (cuántas URLs del top 10 comparten)
     y qué hacer: misma URL / mismo cluster / enlazar / separar.
  2. (Opcional) Consenso de formato por keyword y desajuste con el tipo de
     página propio ("Elige el formato que Google ya premia").

Entrada (JSON, archivo o stdin con --file -):
  {
    "keywords": {
      "cafe de especialidad": ["https://a.com/x", "https://b.com/y", ...],
      "cafe en grano": {
        "urls": ["https://a.com/x", ...],
        "types": ["listado", "producto", ...],   # opcional, mismo orden que urls
        "own_type": "articulo"                     # opcional, tipo de TU página
      }
    }
  }
También vale CSV con columnas: keyword,position,url[,type]  (--format csv).

Tipos de página reconocidos (formato de la SERP): articulo, listado, producto,
categoria, servicio, landing, comparativa, local, herramienta, video, otro.

Uso:
  python3 serp_overlap.py --file serps.json
  python3 serp_overlap.py --file serps.csv --format csv --ignore-ubiquitous 2
  cat serps.json | python3 serp_overlap.py --file -

Salida (JSON a stdout):
  {"ok": true, "pairs": [{"a","b","shared","score","relation","action"}],
   "groups": [{"primary_hint","keywords":[...],"relation"}],
   "formats": [{"keyword","dominant_type","share","consensus","own_type","verdict"}],
   "summary": {...}}
  o {"ok": false, "reason": "...", "fallback": "..."} (exit 0)

Deps: solo stdlib.
"""
import argparse
import csv
import io
import json
import sys
from itertools import combinations
from urllib.parse import urlparse

# Umbrales de solape (top 10). Ajustables con flags.
SAME_URL = 7      # 7-10 URLs compartidas: misma URL
SAME_CLUSTER = 4  # 4-6: mismo cluster, posts distintos o mismo post según volumen
LINK = 2          # 2-3: cluster vecino, enlazar entre sí
# 0-1: separar

CONSENSUS_STRONG = 0.60
CONSENSUS_MIXED = 0.40

VALID_TYPES = {"articulo", "listado", "producto", "categoria", "servicio",
               "landing", "comparativa", "local", "herramienta", "video", "otro"}


def out(obj):
    print(json.dumps(obj, ensure_ascii=False))
    sys.exit(0)


def norm_url(u: str) -> str:
    u = (u or "").strip()
    if not u:
        return ""
    if "://" not in u:
        u = "https://" + u
    p = urlparse(u)
    host = p.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    path = p.path.rstrip("/")
    return host + path


def domain_of(nu: str) -> str:
    return nu.split("/", 1)[0]


def read_raw(path):
    if path in (None, "-"):
        return sys.stdin.read()
    with open(path, "r", encoding="utf-8-sig") as fh:
        return fh.read()


def parse_json(raw):
    obj = json.loads(raw)
    kws = obj.get("keywords") if isinstance(obj, dict) else None
    if not isinstance(kws, dict) or not kws:
        raise ValueError("el JSON debe traer un objeto 'keywords' con al menos una keyword")
    res = {}
    for kw, val in kws.items():
        if isinstance(val, list):
            val = {"urls": val}
        if not isinstance(val, dict) or not isinstance(val.get("urls"), list):
            raise ValueError(f"keyword '{kw}': falta la lista 'urls'")
        urls = [norm_url(u) for u in val["urls"]]
        types = val.get("types") or []
        types = [str(t).strip().lower() for t in types]
        res[kw.strip().lower()] = {
            "urls": urls,
            "types": types if len(types) == len(urls) else [],
            "own_type": (val.get("own_type") or "").strip().lower(),
        }
    return res


def parse_csv(raw):
    reader = csv.DictReader(io.StringIO(raw))
    low = {(f or "").strip().lower(): f for f in (reader.fieldnames or [])}
    kc = low.get("keyword") or low.get("query")
    uc = low.get("url") or low.get("link")
    pc = low.get("position") or low.get("posicion") or low.get("posición")
    tc = low.get("type") or low.get("tipo")
    if not kc or not uc:
        raise ValueError("el CSV necesita columnas keyword y url")
    rows = {}
    for r in reader:
        kw = (r.get(kc) or "").strip().lower()
        if not kw:
            continue
        try:
            pos = float(r.get(pc)) if pc and r.get(pc) else len(rows.get(kw, [])) + 1
        except ValueError:
            pos = len(rows.get(kw, [])) + 1
        rows.setdefault(kw, []).append((pos, norm_url(r.get(uc)), (r.get(tc) or "").strip().lower() if tc else ""))
    res = {}
    for kw, items in rows.items():
        items.sort(key=lambda x: x[0])
        types = [t for _, _, t in items]
        res[kw] = {"urls": [u for _, u, _ in items],
                   "types": types if all(types) else [], "own_type": ""}
    if not res:
        raise ValueError("CSV sin filas validas")
    return res


def relation(score, args):
    if score >= args.same_url:
        return ("misma_url", "Comparten intención: una sola URL. La keyword de mejor ratio volumen/dificultad "
                             "va en URL y H1; la otra entra como H2, FAQ o variante en el texto.")
    if score >= args.same_cluster:
        return ("mismo_cluster", "Intención cercana: mismo cluster. Decide si son dos posts distintos "
                                 "(revisa volumen y formato) o una sola página con secciones.")
    if score >= args.link:
        return ("enlazar", "Temas vecinos: páginas separadas que se enlazan entre sí.")
    return ("separar", "Intención distinta: páginas separadas (la excepción de Vero: si la SERP muestra "
                       "páginas distintas, se separan).")


def main():
    ap = argparse.ArgumentParser(
        description="Solape de SERP y consenso de formato para validar la intención de búsqueda.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Ejemplo:\n  python3 serp_overlap.py --file serps.json --ignore-ubiquitous 2",
    )
    ap.add_argument("--file", default="-", help="JSON o CSV con las SERP capturadas ('-' = stdin).")
    ap.add_argument("--format", choices=["auto", "json", "csv"], default="auto")
    ap.add_argument("--top", type=int, default=10, help="Cuántas posiciones comparar (default 10).")
    ap.add_argument("--ignore-ubiquitous", type=int, default=0, metavar="N",
                    help="Ignora los N dominios que más se repiten en todas las SERP "
                         "(Wikipedia, YouTube, grandes marketplaces) antes de puntuar.")
    ap.add_argument("--same-url", type=int, default=SAME_URL)
    ap.add_argument("--same-cluster", type=int, default=SAME_CLUSTER)
    ap.add_argument("--link", type=int, default=LINK)
    try:
        args = ap.parse_args()
    except SystemExit as e:
        if e.code == 0:
            raise
        out({"ok": False, "reason": "argumentos invalidos", "fallback": "usa --file serps.json (ver --help)"})

    try:
        raw = read_raw(args.file)
        fmt = args.format
        if fmt == "auto":
            fmt = "json" if raw.lstrip()[:1] in "{[" else "csv"
        data = parse_json(raw) if fmt == "json" else parse_csv(raw)
    except (OSError, ValueError, json.JSONDecodeError, csv.Error) as e:
        out({"ok": False, "reason": f"entrada invalida: {e}",
             "fallback": "modo manual: busca cada keyword en Google (incógnito), anota el top 10 y "
                         "cuenta a mano cuántas URLs se repiten entre pares."})

    for d in data.values():
        d["urls"] = d["urls"][:args.top]
        d["types"] = d["types"][:args.top] if d["types"] else []

    # Dominios ubicuos
    ubiquitous = []
    if args.ignore_ubiquitous > 0:
        freq = {}
        for d in data.values():
            for dom in {domain_of(u) for u in d["urls"] if u}:
                freq[dom] = freq.get(dom, 0) + 1
        ubiquitous = [dom for dom, _ in sorted(freq.items(), key=lambda x: -x[1])[:args.ignore_ubiquitous]]

    sets = {}
    for kw, d in data.items():
        sets[kw] = {u for u in d["urls"] if u and domain_of(u) not in ubiquitous}

    pairs = []
    for a, b in combinations(sorted(sets), 2):
        shared = sorted(sets[a] & sets[b])
        rel, action = relation(len(shared), args)
        pairs.append({"a": a, "b": b, "shared": shared, "score": len(shared),
                      "relation": rel, "action": action})
    pairs.sort(key=lambda p: -p["score"])

    # Grupos "misma_url" por componentes conexas (union-find)
    parent = {k: k for k in sets}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for p in pairs:
        if p["relation"] == "misma_url":
            parent[find(p["a"])] = find(p["b"])
    comp = {}
    for k in sets:
        comp.setdefault(find(k), []).append(k)
    groups = [{"keywords": sorted(v), "relation": "misma_url"} for v in comp.values() if len(v) > 1]

    # Consenso de formato
    formats = []
    for kw, d in data.items():
        if not d["types"]:
            continue
        counts = {}
        for t in d["types"]:
            t = t if t in VALID_TYPES else "otro"
            counts[t] = counts.get(t, 0) + 1
        dom_t, n = max(counts.items(), key=lambda x: x[1])
        share = n / len(d["types"])
        consensus = ("fuerte" if share > CONSENSUS_STRONG
                     else "mixto" if share >= CONSENSUS_MIXED else "fragmentado")
        own = d["own_type"]
        if not own:
            verdict = "sin_tipo_propio"
        elif own == dom_t:
            verdict = "alineado"
        elif consensus == "fragmentado":
            verdict = "serp_fragmentada: hay espacio para diferenciarte, valida con el Ojo Clínico"
        elif consensus == "mixto":
            verdict = f"posible_desajuste: la SERP está mezclada ({dom_t} lidera), revisa si tu formato aparece"
        else:
            verdict = (f"DESAJUSTE: la SERP premia '{dom_t}' ({round(share*100)}%) y tu página es '{own}'. "
                       "Cambia el formato o ataca otra keyword; Google ya decidió la intención.")
        formats.append({"keyword": kw, "dominant_type": dom_t, "share": round(share, 2),
                        "consensus": consensus, "own_type": own or None, "verdict": verdict})

    summary = {
        "keywords": len(sets),
        "pairs": len(pairs),
        "misma_url": sum(1 for p in pairs if p["relation"] == "misma_url"),
        "mismo_cluster": sum(1 for p in pairs if p["relation"] == "mismo_cluster"),
        "enlazar": sum(1 for p in pairs if p["relation"] == "enlazar"),
        "separar": sum(1 for p in pairs if p["relation"] == "separar"),
        "ubiquitous_ignored": ubiquitous,
        "mismatches": sum(1 for f in formats if f["verdict"].startswith("DESAJUSTE")),
    }
    out({"ok": True, "pairs": pairs, "groups": groups, "formats": formats, "summary": summary})


if __name__ == "__main__":
    main()
