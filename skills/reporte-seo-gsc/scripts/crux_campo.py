#!/usr/bin/env python3
"""
crux_campo.py: Core Web Vitals de CAMPO (datos reales de usuarios de Chrome) desde la CrUX API.

Distinto de los datos de laboratorio de Lighthouse/Unlighthouse (skill analisis-rendimiento):
aqui son usuarios reales, percentil 75 de los ultimos 28 dias. Adaptado de crux_history.py de
claude-seo (MIT, agricidaniel), reescrito con solo stdlib. Necesita una clave GRATUITA de la
API (Google Cloud, "Chrome UX Report API"), en la variable de entorno CRUX_API_KEY.

Uso:
    CRUX_API_KEY=xxx python3 crux_campo.py https://ejemplo.com
    CRUX_API_KEY=xxx python3 crux_campo.py https://ejemplo.com/blog/post --url-level --form-factor DESKTOP
    CRUX_API_KEY=xxx python3 crux_campo.py ejemplo.com --out .seo-audit/ejemplo.com/data/cwv-field.json

Salida JSON: {"ok":true,"source":"CrUX API","scope":"origin|url","formFactor":"PHONE",
  "collection_period":{...},"metrics":{"lcp_ms":{"p75":..,"rating":"good|needs-improvement|poor",
  "good_pct":..},"inp_ms":{..},"cls":{..},"ttfb_ms":{..},"fcp_ms":{..}},"passes_cwv":bool|null,"note":".."}
Sin clave, o sin datos suficientes para ese origen/URL (HTTP 404): {"ok":false,"reason":"..."}
(exit 0). NUNCA se rellenan valores: si CrUX no tiene datos, el informe dice "pendiente de dato".
Umbrales de Google (p75): LCP 2500/4000 ms, INP 200/500 ms, CLS 0.1/0.25, TTFB 800/1800 ms, FCP 1800/3000 ms.
Deps: solo stdlib. Una peticion por ejecucion.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from urllib.parse import urlparse

API = "https://chromeuxreport.googleapis.com/v1/records:queryRecord"
METRICS = {  # clave CrUX: (nombre, bueno, pobre)
    "largest_contentful_paint": ("lcp_ms", 2500, 4000),
    "interaction_to_next_paint": ("inp_ms", 200, 500),
    "cumulative_layout_shift": ("cls", 0.1, 0.25),
    "experimental_time_to_first_byte": ("ttfb_ms", 800, 1800),
    "first_contentful_paint": ("fcp_ms", 1800, 3000),
}


def rate(v, good, poor):
    return "good" if v <= good else ("needs-improvement" if v <= poor else "poor")


def main():
    p = argparse.ArgumentParser(description="Core Web Vitals de campo (CrUX API).")
    p.add_argument("site", help="Origen o URL (ej. https://ejemplo.com).")
    p.add_argument("--url-level", action="store_true", help="Consultar la URL exacta en vez del origen.")
    p.add_argument("--form-factor", choices=["PHONE", "DESKTOP", "TABLET"], default="PHONE")
    p.add_argument("--out", help="Ruta del JSON (ej. .seo-audit/<sitio>/data/cwv-field.json).")
    a = p.parse_args()

    def fail(reason):
        print(json.dumps({"ok": False, "reason": reason,
                          "fallback": "modo manual: PageSpeed Insights (seccion 'Datos de campo') o el informe Core Web Vitals de GSC; si no hay datos, escribe 'pendiente de dato'"},
                         ensure_ascii=False))
        sys.exit(0)

    key = os.environ.get("CRUX_API_KEY")
    if not key:
        fail("falta CRUX_API_KEY (clave gratuita de la Chrome UX Report API en Google Cloud)")
    site = a.site if a.site.startswith("http") else "https://" + a.site
    o = urlparse(site)
    body = {"formFactor": a.form_factor}
    if a.url_level:
        body["url"] = site
    else:
        body["origin"] = f"{o.scheme}://{o.netloc}"
    req = urllib.request.Request(f"{API}?key={key}", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            rec = json.load(r)["record"]
    except urllib.error.HTTPError as e:
        if e.code == 404:
            fail("CrUX no tiene datos suficientes para este origen/URL (poco trafico). Dato pendiente, no lo estimes.")
        fail(f"HTTP {e.code} de la CrUX API (revisa la clave y que la API este habilitada)")
    except Exception as e:  # noqa: BLE001
        fail(str(e))

    out_m, verdicts = {}, []
    for ck, (name, good, poor) in METRICS.items():
        m = rec.get("metrics", {}).get(ck)
        if not m:
            continue
        raw = m.get("percentiles", {}).get("p75")
        if raw is None:
            continue
        v = float(raw)
        hist = m.get("histogram") or [{}]
        gp = hist[0].get("density")
        out_m[name] = {"p75": v, "rating": rate(v, good, poor),
                       "good_pct": round(float(gp) * 100, 1) if gp is not None else None}
        if name in ("lcp_ms", "inp_ms", "cls"):
            verdicts.append(out_m[name]["rating"] == "good")
    core = [k for k in ("lcp_ms", "inp_ms", "cls") if k in out_m]
    res = {"ok": True, "source": "CrUX API (datos de campo, p75, ultimos 28 dias)",
           "scope": "url" if a.url_level else "origin", "target": body.get("url") or body["origin"],
           "formFactor": a.form_factor, "collection_period": rec.get("collectionPeriod"),
           "metrics": out_m,
           "passes_cwv": (all(verdicts) if len(core) == 3 else None),
           "note": "Datos de campo reales. Los de laboratorio (Lighthouse) viven en performance.json. Si falta una metrica, CrUX no la tiene: no la estimes."}
    if a.out:
        os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
        json.dump(res, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(json.dumps(res, ensure_ascii=False))


if __name__ == "__main__":
    main()
