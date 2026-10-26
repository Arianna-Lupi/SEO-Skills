#!/usr/bin/env python3
"""
psi_campo.py: datos de CAMPO (usuarios reales, CrUX) y laboratorio de una URL vía la API de PageSpeed Insights.

Complemento externo (idea de claude-seo, MIT), no es parte del método del diplomado. El diplomado
pasa las 3 plantillas por PageSpeed Insights a mano (S12 · Velocidad y rendimiento); este script
hace esa misma consulta y extrae LCP, INP y CLS de campo con su veredicto.

PRIVACIDAD: envía la URL a la API pública de Google (googleapis.com). Pide permiso al usuario y
confirma con --confirmo. Clave opcional en la variable PSI_API_KEY (sin clave hay límite de cuota).

Uso:
  python3 psi_campo.py https://ejemplo.com/ https://ejemplo.com/blog/ --confirmo
  python3 psi_campo.py --file plantillas.txt --estrategia mobile --confirmo --site ejemplo.com

Salida JSON: {"ok","results":[{"url","strategy","field":{lcp_ms,inp_ms,cls,overall},"lab":{performance,lcp_ms,cls,tbt_ms}}]}
Si una URL no tiene datos de campo (poco tráfico) lo dice: "field": null. NUNCA se inventan.
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
# Umbrales de Google: (bueno, malo). Entre ambos: necesita mejora.
LIMITS = {"lcp_ms": (2500, 4000), "inp_ms": (200, 500), "cls": (0.1, 0.25)}


def verdict(name, v):
    if v is None:
        return None
    good, bad = LIMITS[name]
    return "bueno" if v <= good else "necesita mejora" if v <= bad else "malo"


def query(url, strategy, key):
    q = {"url": url, "strategy": strategy, "category": "performance"}
    if key:
        q["key"] = key
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(q), headers={"User-Agent": "seo-skills/1.0"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.load(r)


def parse(url, strategy, d):
    out = {"url": url, "strategy": strategy, "field": None, "lab": None}
    m = (d.get("loadingExperience") or {}).get("metrics") or {}
    if m:
        def p(k):
            return (m.get(k) or {}).get("percentile")
        cls = p("CUMULATIVE_LAYOUT_SHIFT_SCORE")
        f = {"lcp_ms": p("LARGEST_CONTENTFUL_PAINT_MS"), "inp_ms": p("INTERACTION_TO_NEXT_PAINT"),
             "cls": cls / 100 if cls is not None else None,
             "overall": d["loadingExperience"].get("overall_category")}
        f["verdict"] = {k: verdict(k, f[k]) for k in LIMITS}
        out["field"] = f
    lh = d.get("lighthouseResult") or {}
    if lh:
        a = lh.get("audits", {})
        def n(k):
            return (a.get(k) or {}).get("numericValue")
        out["lab"] = {"performance": round(((lh.get("categories", {}).get("performance") or {}).get("score") or 0) * 100),
                      "lcp_ms": n("largest-contentful-paint"), "cls": n("cumulative-layout-shift"),
                      "tbt_ms": n("total-blocking-time")}
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("urls", nargs="*")
    ap.add_argument("--file", help="archivo con una URL por línea (una por plantilla)")
    ap.add_argument("--estrategia", choices=["mobile", "desktop"], default="mobile")
    ap.add_argument("--confirmo", action="store_true", help="confirma que el usuario autorizó enviar las URLs a la API de Google")
    ap.add_argument("--site", help="dominio, para volcar a .seo-audit/<sitio>/data/cwv-campo.json")
    ap.add_argument("--root", default=".")
    a = ap.parse_args()
    urls = list(a.urls)
    if a.file:
        with open(a.file, encoding="utf-8") as fh:
            urls += [l.strip() for l in fh if l.strip() and not l.startswith("#")]
    fallback = "modo manual: pega cada URL en https://pagespeed.web.dev/ y copia LCP, INP y CLS de campo"
    if not urls:
        print(json.dumps({"ok": False, "reason": "sin URLs", "fallback": fallback}))
        return
    if not a.confirmo:
        print(json.dumps({"ok": False, "reason": "falta --confirmo: este script envía las URLs a la API de Google; pide permiso al usuario", "fallback": fallback}, ensure_ascii=False))
        return
    key = os.environ.get("PSI_API_KEY")
    res, errs = [], []
    for i, u in enumerate(urls[:20]):
        if i:
            time.sleep(2)
        try:
            res.append(parse(u, a.estrategia, query(u, a.estrategia, key)))
        except (urllib.error.URLError, OSError, ValueError) as e:
            errs.append({"url": u, "error": str(e)})
    out = {"ok": bool(res), "results": res, "errors": errs,
           "note": "field = usuarios reales (CrUX, percentil 75); lab = Lighthouse simulado. El veredicto oficial es el de campo."}
    if not res:
        out["fallback"] = fallback
    if a.site and res:
        d = os.path.join(a.root, ".seo-audit", a.site, "data")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "cwv-campo.json"), "w", encoding="utf-8") as fh:
            json.dump(out, fh, ensure_ascii=False, indent=2)
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
