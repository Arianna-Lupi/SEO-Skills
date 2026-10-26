#!/usr/bin/env python3
"""
matriz_enlaces.py, Verifica el enlazado interno pilar -> clusters contra los
criterios de la Semana 9 del diploma "De Cero a SEO" (Verónica Romero y Juan
Carlos Angulo) y genera la matriz de enlaces que faltan.

Qué revisa (determinista, sin red):
  1. Pilar -> cada cluster y cada cluster -> pilar (el pilar recibe el jugo;
     el curso: "dirige los enlaces a las páginas pilares").
  2. Cada pieza de contenido enlaza al menos 2 contextuales a otros artículos y
     1 a una página de producto o servicio (mínimo por pieza del brief, Semana 9).
  3. Páginas de conversión infraenlazadas: reciben pocos enlaces desde contenido.
  4. Entrantes mínimos por página (--min-inlinks, default 3) y huérfanas.
  5. Anchors: genéricos ("clic aquí", "ver más") y concentración excesiva de un
     mismo anchor hacia una página (--anchor-max, default 0.40).
  6. Profundidad: clics desde la home (BFS por los enlaces) frente a la
     profundidad de carpeta, con la regla de los 3 clics.

Los umbrales 3 entrantes mínimos y 40 % de anchors son criterios de claude-seo
(complemento externo, ver references/complementos-claude-seo.md); la regla de
los 3 clics y el mínimo de 2 contextuales + 1 a producto son del diplomado.

Entrada:
  --pages  CSV con columnas: url, role, cluster
           role: home | pilar | cluster (o spoke) | producto | otro
  --links  CSV de enlaces internos (export "all_inlinks" de Screaming Frog u
           otro) con columnas Source/From, Destination/To y, si existe,
           Anchor/Anchor Text.

Uso:
  python3 matriz_enlaces.py --pages paginas.csv --links all_inlinks.csv
  python3 matriz_enlaces.py --pages paginas.csv --links all_inlinks.csv --min-inlinks 3 --anchor-max 0.4

Salida (JSON a stdout):
  {"ok": true,
   "missing_links": [{"from","to","type","reason"}],        # la matriz de lo que falta
   "low_inlinks": [{"url","role","inlinks","from_content"}],
   "orphans": [...],
   "anchor_issues": [{"url","issue","anchor","share"}],
   "pieces_below_minimum": [{"url","contextual","to_product","needs"}],
   "depth": [{"url","click_depth","folder_depth","verdict"}],
   "summary": {...}}
  o {"ok": false, "reason": "..."} (exit 0)

Deps: solo stdlib.
"""
import argparse
import csv
import json
import os
import sys
from collections import deque
from urllib.parse import urlparse

GENERIC = {"clic aqui", "click aqui", "haz clic aqui", "haz click aqui", "aqui", "ver mas", "leer mas",
           "mas informacion", "click here", "read more", "here", "este enlace", "link", "mas", "ver"}
PRODUCT_ROLES = {"producto", "servicio", "conversion", "categoria"}
CONTENT_ROLES = {"cluster", "spoke", "pilar", "blog", "articulo"}


def out(obj):
    print(json.dumps(obj, ensure_ascii=False))
    sys.exit(0)


def strip_acc(s):
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFD", s or "") if unicodedata.category(c) != "Mn")


def norm(u):
    u = (u or "").strip()
    if not u:
        return ""
    p = urlparse(u)
    host = p.netloc.lower()
    host = host[4:] if host.startswith("www.") else host
    path = p.path.rstrip("/") or ""
    return (host + path) if host else path


def find_col(fields, *cands):
    low = {strip_acc(f).strip().lower(): f for f in (fields or [])}
    for c in cands:
        if c in low:
            return low[c]
    for c in cands:
        for k, orig in low.items():
            if c in k:
                return orig
    return None


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        rd = csv.DictReader(fh)
        return rd.fieldnames, list(rd)


def folder_depth(url):
    return len([s for s in urlparse(url if "://" in url else "https://x" + url).path.split("/") if s])


def main():
    ap = argparse.ArgumentParser(
        description="Matriz de enlaces pilar -> clusters y chequeos de enlazado interno.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Ejemplo:\n  python3 matriz_enlaces.py --pages paginas.csv --links all_inlinks.csv",
    )
    ap.add_argument("--pages", required=True, help="CSV con url, role, cluster")
    ap.add_argument("--links", required=True, help="CSV de enlaces internos (Source, Destination, Anchor)")
    ap.add_argument("--min-inlinks", type=int, default=3, help="Entrantes mínimos por página (default 3)")
    ap.add_argument("--anchor-max", type=float, default=0.40, help="Máx. proporción del mismo anchor hacia una página (default 0.40)")
    ap.add_argument("--max-clicks", type=int, default=3, help="Regla de clics desde la home (default 3)")
    try:
        args = ap.parse_args()
    except SystemExit as e:
        if e.code == 0:
            raise
        out({"ok": False, "reason": "argumentos invalidos: usa --pages y --links"})

    for p in (args.pages, args.links):
        if not os.path.isfile(p):
            out({"ok": False, "reason": f"no existe el archivo: {p}"})

    try:
        pf, prow = read_csv(args.pages)
        uc, rc, cc = find_col(pf, "url", "address"), find_col(pf, "role", "rol", "tipo"), find_col(pf, "cluster", "grupo")
        if not uc or not rc:
            out({"ok": False, "reason": "paginas.csv necesita columnas url y role"})
        pages = {}
        for r in prow:
            u = norm(r.get(uc))
            if u:
                role = strip_acc(r.get(rc) or "otro").strip().lower()
                pages[u] = {"url": (r.get(uc) or "").strip(), "role": "cluster" if role == "spoke" else role,
                            "cluster": (r.get(cc) or "").strip().lower() if cc else ""}
        lf, lrow = read_csv(args.links)
        sc = find_col(lf, "source", "from", "origen")
        dc = find_col(lf, "destination", "to", "destino", "target")
        ac = find_col(lf, "anchor", "texto")
        if not sc or not dc:
            out({"ok": False, "reason": "links.csv necesita columnas Source y Destination"})
    except (OSError, csv.Error) as e:
        out({"ok": False, "reason": f"error leyendo archivos: {e}"})

    links = []
    for r in lrow:
        s, d = norm(r.get(sc)), norm(r.get(dc))
        if s and d and s != d:
            links.append((s, d, strip_acc(r.get(ac) or "").strip().lower() if ac else ""))
    link_set = {(s, d) for s, d, _ in links}

    # --- 1. matriz pilar <-> clusters
    missing = []
    pilars = [u for u, p in pages.items() if p["role"] == "pilar"]
    for pu in pilars:
        pc = pages[pu]["cluster"]
        for u, p in pages.items():
            if p["role"] == "cluster" and (not pc or p["cluster"] == pc):
                if (pu, u) not in link_set:
                    missing.append({"from": pages[pu]["url"], "to": p["url"], "type": "pilar->cluster",
                                    "reason": "El pilar debe enlazar a cada página de su cluster."})
                if (u, pu) not in link_set:
                    missing.append({"from": p["url"], "to": pages[pu]["url"], "type": "cluster->pilar",
                                    "reason": "Cada página del cluster debe devolver el enlace al pilar (Link Equity)."})

    # --- 2. mínimos por pieza de contenido
    below = []
    for u, p in pages.items():
        if p["role"] in ("cluster", "blog", "articulo"):
            outs = [d for s, d, _ in links if s == u and d in pages]
            ctx = sum(1 for d in outs if pages[d]["role"] in CONTENT_ROLES)
            prod = sum(1 for d in outs if pages[d]["role"] in PRODUCT_ROLES)
            needs = []
            if ctx < 2:
                needs.append(f"{2 - ctx} enlace(s) contextual(es) a otros artículos")
            if prod < 1:
                needs.append("1 enlace contenido->producto o servicio")
            if needs:
                below.append({"url": p["url"], "contextual": ctx, "to_product": prod, "needs": needs})

    # --- 3 y 4. entrantes
    inl = {u: [] for u in pages}
    for s, d, _ in links:
        if d in inl:
            inl[d].append(s)
    low, orphans = [], []
    for u, srcs in inl.items():
        role = pages[u]["role"]
        if role == "home":
            continue
        n = len(set(srcs))
        from_content = len({s for s in srcs if s in pages and pages[s]["role"] in CONTENT_ROLES})
        if n == 0:
            orphans.append(pages[u]["url"])
        elif n < args.min_inlinks or (role in PRODUCT_ROLES and from_content < 2):
            low.append({"url": pages[u]["url"], "role": role, "inlinks": n, "from_content": from_content})

    # --- 5. anchors
    anchor_issues = []
    if ac:
        by_dest = {}
        for s, d, a in links:
            if d in pages and a:
                by_dest.setdefault(d, []).append(a)
        for d, anchors in by_dest.items():
            total = len(anchors)
            counts = {}
            for a in anchors:
                counts[a] = counts.get(a, 0) + 1
            for a, n in counts.items():
                if a in GENERIC:
                    anchor_issues.append({"url": pages[d]["url"], "issue": "anchor genérico", "anchor": a, "share": round(n / total, 2)})
                elif total >= 5 and n / total > args.anchor_max:
                    anchor_issues.append({"url": pages[d]["url"], "issue": "anchor repetido en exceso", "anchor": a, "share": round(n / total, 2)})

    # --- 6. profundidad en clics (BFS desde la home) y de carpeta
    home = next((u for u, p in pages.items() if p["role"] == "home"), None)
    depth_rows = []
    if home:
        adj = {}
        for s, d, _ in links:
            adj.setdefault(s, set()).add(d)
        dist = {home: 0}
        q = deque([home])
        while q:
            cur = q.popleft()
            for nx in adj.get(cur, ()):
                if nx not in dist:
                    dist[nx] = dist[cur] + 1
                    q.append(nx)
        for u, p in pages.items():
            if u == home:
                continue
            cd = dist.get(u)
            fd = folder_depth(p["url"])
            if cd is None:
                verdict = "inalcanzable desde la home por los enlaces dados"
            elif cd > args.max_clicks:
                verdict = f"enterrada: {cd} clics (regla de {args.max_clicks})"
            elif fd >= 4:
                verdict = "carpeta profunda pero a pocos clics: no es problema de rastreo"
            else:
                continue
            depth_rows.append({"url": p["url"], "click_depth": cd, "folder_depth": fd, "verdict": verdict})

    out({"ok": True, "missing_links": missing, "low_inlinks": low, "orphans": orphans,
         "anchor_issues": anchor_issues, "pieces_below_minimum": below, "depth": depth_rows,
         "summary": {"pages": len(pages), "links": len(links), "pilars": len(pilars),
                     "missing_links": len(missing), "orphans": len(orphans), "low_inlinks": len(low),
                     "pieces_below_minimum": len(below), "anchor_issues": len(anchor_issues),
                     "home_found": bool(home)}})


if __name__ == "__main__":
    main()
