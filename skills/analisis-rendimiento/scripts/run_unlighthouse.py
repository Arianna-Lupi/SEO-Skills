#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# ///
"""
run_unlighthouse.py — Análisis de rendimiento de TODO el sitio con Unlighthouse
(Lighthouse en cada ruta) y vuelco a .seo-audit/<sitio>/data/performance.json,
el esquema que consume el dashboard (skill dashboard-seo).

Unlighthouse rastrea el sitio (sitemap/robots/crawl) y corre Lighthouse en cada
ruta única, no página por página a mano. Este wrapper lo ejecuta vía npx, parsea
su salida JSON de forma defensiva (el esquema cambia entre versiones) y agrega:
scores medios (performance/accessibility/best-practices/seo), Core Web Vitals de
LABORATORIO (LCP, CLS, TBT, FCP, Speed Index), peores páginas y agrupación por
plantilla (primer segmento de la ruta).

REGLA DE DATOS: todo lo que escribe son MEDICIONES REALES de Lighthouse. No inventa
nada. Si Node/npx/Unlighthouse no están o el scan falla, devuelve {"ok":false,...}
con exit 0 y el modo manual (PageSpeed Insights), sin escribir números falsos.

IMPORTANTE: los CWV de Lighthouse son datos de LABORATORIO (entorno simulado), no
datos de campo (CrUX/Search Console). Útiles para diagnosticar y priorizar, pero el
"aprobado/suspenso" oficial de Google usa datos de campo. El JSON lo deja explícito.

Uso:
  # rastrear y medir un sitio en vivo (descarga Unlighthouse con npx la 1ª vez):
  uv run run_unlighthouse.py --site https://ejemplo.com
  uv run run_unlighthouse.py --site https://ejemplo.com --max-routes 40 --mobile

  # o parsear una salida de Unlighthouse que ya tengas (sin volver a rastrear):
  uv run run_unlighthouse.py --site https://ejemplo.com --json .unlighthouse/ci-result.json

  # elegir dominio para la carpeta .seo-audit (default: host del --site):
  uv run run_unlighthouse.py --site https://ejemplo.com --slug ejemplo.com

Salida (JSON a stdout): {"ok":true, "written": ".../data/performance.json",
  "pages_scanned": N, "avg_performance": 0-100, ...}
o {"ok":false, "reason":"...", "fallback":"manual", "manual":"..."} (exit 0).

Deps: stdlib. Requiere Node/npx en runtime solo para el modo --site (no para --json).
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import date, datetime, timezone
from urllib.parse import urlparse

# Audits de Lighthouse → claves del JSON de salida. numericValue en ms salvo CLS.
METRIC_AUDITS = {
    "largest-contentful-paint": "lcp_ms",
    "cumulative-layout-shift": "cls",
    "total-blocking-time": "tbt_ms",
    "first-contentful-paint": "fcp_ms",
    "speed-index": "si_ms",
    "interactive": "tti_ms",
}
CATEGORY_KEYS = {
    "performance": "performance",
    "accessibility": "accessibility",
    "best-practices": "best_practices",
    "best practices": "best_practices",
    "seo": "seo",
}
# Umbrales "buenos" de Google (referencia, no veredicto de campo).
CWV_GOOD = {"lcp_ms": 2500, "cls": 0.1, "tbt_ms": 200, "fcp_ms": 1800}


def _num(v):
    try:
        f = float(v)
        return f if f == f else None  # descarta NaN
    except (TypeError, ValueError):
        return None


def _score_to_100(v):
    """Lighthouse da score 0..1; normaliza a 0..100 int. Acepta ya-0..100."""
    n = _num(v)
    if n is None:
        return None
    if n <= 1.0:
        n *= 100
    return int(round(n))


def _deep_find_categories(obj):
    """Busca un dict 'categories' en cualquier nivel y devuelve {key: score_0_100}."""
    found = {}

    def walk(node):
        if isinstance(node, dict):
            cats = node.get("categories")
            if isinstance(cats, dict):
                for raw_k, raw_v in cats.items():
                    k = CATEGORY_KEYS.get(str(raw_k).lower())
                    if not k:
                        continue
                    # value puede ser número o {score: ...}
                    score = raw_v.get("score") if isinstance(raw_v, dict) else raw_v
                    s = _score_to_100(score)
                    if s is not None and k not in found:
                        found[k] = s
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk(obj)
    return found


def _deep_find_metrics(obj):
    """Extrae numericValue de los audits de CWV, sea dict {id:{}} o lista [{id}]."""
    out = {}

    def take(audit_id, entry):
        key = METRIC_AUDITS.get(str(audit_id).lower())
        if not key or key in out:
            return
        if isinstance(entry, dict):
            val = entry.get("numericValue", entry.get("value"))
        else:
            val = entry
        n = _num(val)
        if n is not None:
            out[key] = round(n, 3) if key == "cls" else int(round(n))

    def walk(node):
        if isinstance(node, dict):
            for container_key in ("audits", "metrics"):
                c = node.get(container_key)
                if isinstance(c, dict):
                    for aid, entry in c.items():
                        take(aid, entry)
                elif isinstance(c, list):
                    for entry in c:
                        if isinstance(entry, dict):
                            take(entry.get("id") or entry.get("key") or entry.get("name"), entry)
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk(obj)
    return out


def _url_to_path(u):
    """Normaliza una URL completa a su ruta (con query); deja paths tal cual."""
    if not isinstance(u, str) or not u:
        return None
    if u.startswith("http://") or u.startswith("https://"):
        pr = urlparse(u)
        return (pr.path or "/") + (("?" + pr.query) if pr.query else "")
    return u


def _route_path(obj):
    """Saca la ruta/URL de un nodo de ruta de Unlighthouse (varios esquemas)."""
    if not isinstance(obj, dict):
        return None
    # esquemas ci-result (path/route/url) y LHR completo (finalUrl/requestedUrl)
    for k in ("path", "route", "url", "finalDisplayedUrl", "finalUrl", "mainDocumentUrl", "requestedUrl"):
        v = obj.get(k)
        if isinstance(v, str) and v:
            return _url_to_path(v)
        if isinstance(v, dict):
            for kk in ("path", "url"):
                if isinstance(v.get(kk), str) and v[kk]:
                    return _url_to_path(v[kk])
    return None


def _iter_route_nodes(data):
    """Normaliza la salida de Unlighthouse a una lista de nodos-de-ruta.

    Soporta: lista top-level de rutas; {routes:[...]} / {reports:[...]} / {data:[...]}.
    """
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for k in ("routes", "reports", "results", "data"):
            if isinstance(data.get(k), list):
                return data[k]
        # quizá sea un único LHR (un solo informe)
        if "categories" in data or "audits" in data:
            return [data]
    return []


# Audits de Lighthouse a IGNORAR en la lista de errores (no accionables / ruido).
_SKIP_DISPLAY = {"informative", "notApplicable", "manual", "error"}
# Las métricas en sí (ya van en core_web_vitals); no son "errores accionables".
_SKIP_AUDIT_IDS = set(METRIC_AUDITS) | {"interactive", "max-potential-fid",
                                        "first-meaningful-paint", "metrics", "screenshot-thumbnails",
                                        "final-screenshot", "largest-contentful-paint-element"}


def _find_audits_dict(node):
    """Devuelve el dict de audits de un LHR completo (puede estar anidado)."""
    if isinstance(node, dict):
        a = node.get("audits")
        if isinstance(a, dict) and a:
            return a
        for v in node.values():
            r = _find_audits_dict(v)
            if r:
                return r
    return None


def collect_failing_audits(node):
    """Lista de audits de Lighthouse que NO pasan (score<0.9), con ahorro estimado."""
    audits = _find_audits_dict(node)
    if not audits:
        return []
    out = []
    for aid, a in audits.items():
        if not isinstance(a, dict):
            continue
        if aid in _SKIP_AUDIT_IDS:
            continue
        if a.get("scoreDisplayMode") in _SKIP_DISPLAY:
            continue
        score = a.get("score")
        if score is None:
            continue
        s = _num(score)
        if s is None or s >= 0.9:  # 0.9..1 = aprobado
            continue
        det = a.get("details") if isinstance(a.get("details"), dict) else {}
        out.append({
            "id": aid,
            "title": a.get("title") or aid,
            "score": _score_to_100(s),
            "savings_ms": _num(det.get("overallSavingsMs")),
            "savings_kb": (round(_num(det.get("overallSavingsBytes")) / 1024) if _num(det.get("overallSavingsBytes")) else None),
            "display": a.get("displayValue") or "",
        })
    return out


def _sev_from_score(s):
    if s is None:
        return "Medio"
    return "Alto" if s < 50 else "Medio" if s < 80 else "Bajo-Medio"


def aggregate_issues(pages_audits):
    """Agrupa los audits fallidos por id a lo largo de todas las páginas.

    pages_audits: lista de (path, [audits]). Devuelve lista ordenada por impacto.
    """
    by_id = {}
    for path, audits in pages_audits:
        for a in audits:
            e = by_id.setdefault(a["id"], {
                "id": a["id"], "title": a["title"], "pages": 0,
                "scores": [], "savings_ms": [], "savings_kb": [], "examples": [],
            })
            e["pages"] += 1
            if a["score"] is not None:
                e["scores"].append(a["score"])
            if a["savings_ms"]:
                e["savings_ms"].append(a["savings_ms"])
            if a["savings_kb"]:
                e["savings_kb"].append(a["savings_kb"])
            if len(e["examples"]) < 3:
                e["examples"].append(path)
    issues = []
    for e in by_id.values():
        worst = min(e["scores"]) if e["scores"] else None
        issues.append({
            "id": e["id"],
            "title": e["title"],
            "pages_affected": e["pages"],
            "worst_score": worst,
            "severity": _sev_from_score(worst),
            "avg_savings_ms": _avg_int(e["savings_ms"]) if e["savings_ms"] else None,
            "max_savings_kb": (max(e["savings_kb"]) if e["savings_kb"] else None),
            "examples": e["examples"],
        })
    # ordena por nº de páginas afectadas, luego peor score
    issues.sort(key=lambda x: (-x["pages_affected"], x["worst_score"] if x["worst_score"] is not None else 100))
    return issues


def parse_unlighthouse_json(data):
    """Devuelve (pages, pages_audits). pages = métricas por ruta; pages_audits = (path, [audits])."""
    pages = []
    pages_audits = []
    for node in _iter_route_nodes(data):
        cats = _deep_find_categories(node)
        mets = _deep_find_metrics(node)
        if not cats and not mets:
            continue
        path = _route_path(node) or "(desconocida)"
        page = {"path": path}
        page.update(cats)
        page.update(mets)
        pages.append(page)
        audits = collect_failing_audits(node)
        if audits:
            pages_audits.append((path, audits))
    return pages, pages_audits


def _avg(vals):
    vals = [v for v in vals if v is not None]
    return round(sum(vals) / len(vals), 3) if vals else None


def _avg_int(vals):
    a = _avg(vals)
    return int(round(a)) if a is not None else None


def _template_hint(path):
    p = (path or "").split("?")[0].split("#")[0].strip("/")
    if not p:
        return "home"
    return p.split("/")[0]


def aggregate(pages, pages_audits, site, source_label, mobile):
    perf = [p.get("performance") for p in pages]
    cwv = {
        "lcp_ms_avg": _avg_int(p.get("lcp_ms") for p in pages),
        "cls_avg": _avg(p.get("cls") for p in pages),
        "tbt_ms_avg": _avg_int(p.get("tbt_ms") for p in pages),
        "fcp_ms_avg": _avg_int(p.get("fcp_ms") for p in pages),
        "si_ms_avg": _avg_int(p.get("si_ms") for p in pages),
        "note": ("Datos de LABORATORIO (Lighthouse, " + ("móvil" if mobile else "escritorio")
                 + "), no de campo/CrUX. Refer.: LCP<2.5s, CLS<0.1, TBT<200ms."),
    }
    # cuántas páginas fallan cada umbral
    fail = {}
    for key, good in CWV_GOOD.items():
        bad = [p for p in pages if p.get(key) is not None and p[key] > good]
        if bad:
            fail[key] = len(bad)

    worst = sorted(
        [p for p in pages if p.get("performance") is not None],
        key=lambda p: p["performance"],
    )[:10]
    worst_pages = [{
        "path": p["path"],
        "performance": p.get("performance"),
        "lcp_ms": p.get("lcp_ms"),
        "cls": p.get("cls"),
        "tbt_ms": p.get("tbt_ms"),
    } for p in worst]

    by_template = {}
    for p in pages:
        by_template.setdefault(_template_hint(p["path"]), []).append(p.get("performance"))
    by_template_hint = {
        t: {"pages": len(v), "avg_performance": _avg_int(v)}
        for t, v in sorted(by_template.items())
    }

    issues = aggregate_issues(pages_audits)
    issues_note = (None if pages_audits else
                   "Lista de errores no disponible: la salida de Unlighthouse no traía "
                   "los audits completos (solo scores). Vuelve a correr conservando los "
                   "informes por ruta o revisa el HTML de Unlighthouse.")

    return {
        "source": source_label,
        "site": site,
        "strategy": "mobile" if mobile else "desktop",
        "summary": {
            "pages_scanned": len(pages),
            "avg_performance": _avg_int(perf),
            "avg_accessibility": _avg_int(p.get("accessibility") for p in pages),
            "avg_best_practices": _avg_int(p.get("best_practices") for p in pages),
            "avg_seo": _avg_int(p.get("seo") for p in pages),
            "issues_found": len(issues),
        },
        "core_web_vitals": cwv,
        "cwv_pages_failing": fail,
        "worst_pages": worst_pages,
        "by_template_hint": by_template_hint,
        "issues": issues,
        "issues_note": issues_note,
        "note": ("Medición real con Unlighthouse (Lighthouse en cada ruta). "
                 "CWV = laboratorio; el veredicto oficial de Google usa datos de campo."),
    }


def find_root(start):
    d = os.path.abspath(start)
    while True:
        if os.path.isdir(os.path.join(d, ".git")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return os.path.abspath(start)
        d = parent


def _collect_results(outdir):
    """Recoge la salida de Unlighthouse (varias versiones/reporters).

    Prefiere ci-result.json (resumen por ruta). Si no, junta los LHR completos
    por ruta (reports/**/lighthouse.json). Devuelve un objeto que entiende
    parse_unlighthouse_json, o None.
    """
    import glob
    # 1) Preferimos los LHR completos por ruta: traen los audits (lista de errores).
    lhrs = []
    for p in sorted(glob.glob(os.path.join(outdir, "**", "lighthouse.json"), recursive=True)):
        try:
            with open(p, encoding="utf-8") as f:
                d = json.load(f)
            if isinstance(d, dict) and (d.get("audits") or d.get("categories")):
                lhrs.append(d)
        except (OSError, ValueError):
            continue
    if len(lhrs) >= 1:
        return lhrs
    # 2) Fallback: ci-result.json (scores + métricas, sin audits completos).
    ci = sorted(glob.glob(os.path.join(outdir, "**", "ci-result.json"), recursive=True))
    if ci:
        with open(ci[0], encoding="utf-8") as f:
            return json.load(f)
    return None


def run_unlighthouse(site, outdir, max_routes, mobile, throttle, extra):
    """Ejecuta unlighthouse-ci vía npx. Devuelve (raw_obj|None, stderr)."""
    if not shutil.which("npx"):
        return None, "npx no encontrado (instala Node.js)"
    cmd = [
        "npx", "-y", "unlighthouse-ci",
        "--site", site,
        "--output-path", outdir,
    ]
    if mobile:
        cmd += ["--mobile"]
    else:
        cmd += ["--desktop"]
    if throttle:
        cmd += ["--throttle"]
    if extra:
        cmd += list(extra)

    env = dict(os.environ)
    if max_routes:
        # límite de rutas vía env (no hay flag estable en todas las versiones)
        env["UNLIGHTHOUSE_SCANNER_MAXROUTES"] = str(max_routes)
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=2700)
    except FileNotFoundError:
        return None, "npx no ejecutable"
    except subprocess.TimeoutExpired:
        return None, "timeout (>45 min) — usa --max-routes para acotar"

    # unlighthouse-ci puede devolver exit !=0 por presupuestos; igual buscamos el JSON.
    raw = _collect_results(outdir)
    if raw:
        return raw, proc.stderr
    return None, (proc.stderr or proc.stdout or "Unlighthouse no generó resultados JSON")[-800:]


MANUAL = (
    "Modo manual (sin Unlighthouse): corre PageSpeed Insights "
    "(https://pagespeed.web.dev/) en 1 URL por plantilla (home, categoría, "
    "artículo/producto, landing) y pásame LCP/INP/CLS + score. Pega los números y "
    "los vuelco a performance.json sin inventar nada. Para el sitio entero, instala "
    "Node.js y reintenta `--site`, o expórtame el ci-result.json de Unlighthouse y "
    "úsalo con `--json`."
)


def main():
    ap = argparse.ArgumentParser(
        description="Rendimiento de todo el sitio con Unlighthouse → performance.json del dashboard.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Ejemplo:\n  uv run run_unlighthouse.py --site https://ejemplo.com --max-routes 40 --mobile",
    )
    ap.add_argument("--site", required=True, help="URL del sitio (con http/https), p.ej. https://ejemplo.com")
    ap.add_argument("--slug", help="Dominio para la carpeta .seo-audit (default: host del --site)")
    ap.add_argument("--json", dest="json_path", help="Parsear este ci-result.json en vez de rastrear")
    ap.add_argument("--root", help="Raíz del repo (default: detecta .git o cwd)")
    ap.add_argument("--max-routes", type=int, default=0, help="Límite de rutas a rastrear (0 = sin límite)")
    ap.add_argument("--mobile", action="store_true", help="Emular móvil (default: escritorio)")
    ap.add_argument("--throttle", action="store_true", help="Aplicar throttling de red/CPU")
    ap.add_argument("--keep", action="store_true", help="No borrar la salida cruda de Unlighthouse")
    ap.add_argument("extra", nargs="*", help="Args extra que se pasan tal cual a unlighthouse-ci")
    args = ap.parse_args()

    root = args.root or find_root(os.getcwd())
    slug = args.slug or (urlparse(args.site).hostname or args.site).lstrip(".")
    datadir = os.path.join(root, ".seo-audit", slug, "data")
    os.makedirs(datadir, exist_ok=True)
    out_json = os.path.join(datadir, "performance.json")

    today = date.today().isoformat()
    tmpdir = None
    try:
        if args.json_path:
            if not os.path.isfile(args.json_path):
                print(json.dumps({"ok": False, "reason": f"No existe {args.json_path}",
                                  "fallback": "manual", "manual": MANUAL}, ensure_ascii=False))
                return
            with open(args.json_path, encoding="utf-8") as f:
                raw = json.load(f)
            source = f"Unlighthouse (Lighthouse) — {args.json_path} — {today}"
        else:
            tmpdir = tempfile.mkdtemp(prefix="unlighthouse-")
            raw, err = run_unlighthouse(
                args.site, tmpdir, args.max_routes, args.mobile, args.throttle, args.extra)
            if not raw:
                print(json.dumps({"ok": False, "reason": err, "fallback": "manual",
                                  "manual": MANUAL}, ensure_ascii=False))
                return
            if args.keep:
                dest = os.path.join(datadir, "unlighthouse-raw")
                shutil.rmtree(dest, ignore_errors=True)
                shutil.copytree(tmpdir, dest)
            source = f"Unlighthouse (Lighthouse en cada ruta) — {today}"

        pages, pages_audits = parse_unlighthouse_json(raw)
        if not pages:
            print(json.dumps({"ok": False, "reason": "No se pudo extraer ninguna ruta del JSON",
                              "fallback": "manual", "manual": MANUAL}, ensure_ascii=False))
            return

        report = aggregate(pages, pages_audits, args.site, source, args.mobile)
        report["generated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        s = report["summary"]
        print(json.dumps({
            "ok": True, "written": out_json, "site": args.site, "slug": slug,
            "pages_scanned": s["pages_scanned"], "avg_performance": s["avg_performance"],
            "avg_seo": s["avg_seo"], "issues_found": s.get("issues_found", 0),
            "cwv_pages_failing": report["cwv_pages_failing"],
            "hint": "Genera el dashboard: uv run skills/dashboard-seo/scripts/build_dashboard.py --site " + slug,
            "cleanup": "Al terminar: pkill -f 'http.server'; pkill -f 'Chrome for Testing'; pkill -f unlighthouse",
        }, ensure_ascii=False))
    finally:
        if tmpdir and not args.keep:
            shutil.rmtree(tmpdir, ignore_errors=True)


if __name__ == "__main__":
    main()
