#!/usr/bin/env python3
"""
comparar_corridas.py: compara dos corridas de una auditoría (solo stdlib).

Complemento externo (idea de seo-drift de claude-seo, MIT). El diplomado pide
reportar "mes actual vs mes anterior" (S12 · reporte SEO); aquí se aplica a los
elementos técnicos críticos de cada URL.

Acepta dos tipos de archivo, el mismo en ambos lados:
  A) Salida de onpage_extract.py (campo "results" con url, status, title,
     canonical, meta_robots, h1, indexability). Compara URL por URL.
  B) issues.json (campo "issues"). Compara por título: nuevos, resueltos, que subieron de severidad.

Reglas de severidad para (A):
  Crítico: noindex nuevo, canonical eliminado o cambiado, H1 eliminado, title eliminado,
           status pasa de 2xx a 4xx/5xx.
  Alto:    H1 cambia mucho (menos del 50% de parecido), URL deja de ser indexable.
  Medio:   title o canonical cambian de forma menor.

Uso:
  python3 comparar_corridas.py anterior.json actual.json
  python3 comparar_corridas.py anterior.json actual.json --site ejemplo.com
Salida JSON: {"ok","kind","summary","changes":[...]}
"""
import argparse
import difflib
import json
import os

ORDER = {"Crítico": 0, "Alto": 1, "Medio": 2, "Bajo-Medio": 3, "Bajo": 4}


def load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def h1_first(r):
    h = r.get("h1")
    if isinstance(h, list):
        return h[0] if h else ""
    return h or ""


def compare_pages(a, b):
    old = {r["url"]: r for r in a if r.get("url")}
    new = {r["url"]: r for r in b if r.get("url")}
    ch = []
    for u in sorted(set(old) | set(new)):
        o, n = old.get(u), new.get(u)
        if o is None:
            ch.append({"url": u, "severity": "Bajo", "change": "URL nueva en la corrida actual"})
            continue
        if n is None:
            ch.append({"url": u, "severity": "Medio", "change": "URL ya no aparece en la corrida actual"})
            continue
        so, sn = o.get("status") or 0, n.get("status") or 0
        if 200 <= so < 300 and sn >= 400:
            ch.append({"url": u, "severity": "Crítico", "change": "status %s a %s" % (so, sn)})
        if "noindex" in str(n.get("meta_robots") or "").lower() and "noindex" not in str(o.get("meta_robots") or "").lower():
            ch.append({"url": u, "severity": "Crítico", "change": "noindex agregado"})
        if o.get("canonical") and not n.get("canonical"):
            ch.append({"url": u, "severity": "Crítico", "change": "canonical eliminado"})
        elif o.get("canonical") and n.get("canonical") and o["canonical"].rstrip("/") != n["canonical"].rstrip("/"):
            ch.append({"url": u, "severity": "Crítico", "change": "canonical cambió: %s a %s" % (o["canonical"], n["canonical"])})
        ho, hn = h1_first(o), h1_first(n)
        if ho and not hn:
            ch.append({"url": u, "severity": "Crítico", "change": "H1 eliminado"})
        elif ho and hn and ho != hn and difflib.SequenceMatcher(None, ho, hn).ratio() < 0.5:
            ch.append({"url": u, "severity": "Alto", "change": "H1 cambió mucho: «%s» a «%s»" % (ho, hn)})
        if o.get("title") and not n.get("title"):
            ch.append({"url": u, "severity": "Crítico", "change": "title eliminado"})
        elif o.get("title") != n.get("title") and o.get("title") and n.get("title"):
            ch.append({"url": u, "severity": "Medio", "change": "title cambió"})
        if o.get("indexability") == "Indexable" and n.get("indexability") == "Non-Indexable":
            ch.append({"url": u, "severity": "Alto", "change": "la URL dejó de ser indexable (%s)" % n.get("indexability_status")})
    return ch


def compare_issues(a, b):
    old = {i.get("title") or i.get("id"): i for i in a}
    new = {i.get("title") or i.get("id"): i for i in b}
    ch = []
    for t in sorted(set(old) | set(new), key=str):
        if t not in old:
            ch.append({"issue": t, "severity": new[t].get("severity", "Bajo"), "change": "issue nuevo"})
        elif t not in new:
            ch.append({"issue": t, "severity": "Bajo", "change": "issue resuelto o ya no detectado"})
        elif ORDER.get(new[t].get("severity"), 9) < ORDER.get(old[t].get("severity"), 9):
            ch.append({"issue": t, "severity": new[t]["severity"], "change": "subió de %s a %s" % (old[t].get("severity"), new[t]["severity"])})
    return ch


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("anterior")
    ap.add_argument("actual")
    ap.add_argument("--site", help="dominio, para volcar a .seo-audit/<sitio>/data/comparacion.json")
    ap.add_argument("--root", default=".")
    a = ap.parse_args()
    try:
        x, y = load(a.anterior), load(a.actual)
        if "results" in x and "results" in y:
            kind, ch = "paginas", compare_pages(x["results"], y["results"])
        elif "issues" in x and "issues" in y:
            kind, ch = "issues", compare_issues(x["issues"], y["issues"])
        else:
            raise ValueError("los archivos deben ser ambos de onpage_extract.py (results) o ambos issues.json")
    except (OSError, ValueError, KeyError) as e:
        print(json.dumps({"ok": False, "reason": str(e), "fallback": "modo manual: compara las dos exportaciones en un Sheet"}, ensure_ascii=False))
        return
    ch.sort(key=lambda c: ORDER.get(c["severity"], 9))
    summ = {}
    for c in ch:
        summ[c["severity"]] = summ.get(c["severity"], 0) + 1
    out = {"ok": True, "kind": kind, "summary": summ, "changes": ch}
    if a.site:
        d = os.path.join(a.root, ".seo-audit", a.site, "data")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "comparacion.json"), "w", encoding="utf-8") as fh:
            json.dump(out, fh, ensure_ascii=False, indent=2)
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
