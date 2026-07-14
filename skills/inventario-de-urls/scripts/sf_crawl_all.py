#!/usr/bin/env python3
"""
sf_crawl_all.py — Rastrea TODO un sitio con Screaming Frog GRATIS, troceando por
lotes de ≤500 URLs (el límite de la versión gratis es por crawl, no por sitio).

Idea: la versión gratis de Screaming Frog para a las 500 URLs por rastreo. En vez
de pedir licencia, este wrapper:
  1. Saca TODAS las URLs del sitio vía sitemap (robots.txt → sitemaps → <loc>),
     reutilizando inventario_urls.py (cero deps, solo stdlib).
  2. Las trocea en lotes de ≤500 (un sitemap con >500 URLs se parte solo).
  3. Corre SF en modo `--crawl-list lote.txt` por cada lote (cada lote ≤500 nunca
     toca el límite gratis) y exporta Internal:All a CSV.
  4. Junta todos los internal_all.csv en uno, deduplicando por Address.

Así se cubre un sitio entero (miles de URLs) con la versión GRATIS, sin licencia.

Binario: se ubica con la variable de entorno SCREAMING_FROG_BINARY o, si no está,
por la ruta por defecto del SO (macOS/Windows/Linux).

Uso:
  python3 sf_crawl_all.py --site https://ejemplo.com
  python3 sf_crawl_all.py --site https://ejemplo.com --sitemap https://ejemplo.com/sitemap_index.xml
  python3 sf_crawl_all.py --site https://ejemplo.com --batch-size 500 --out ./sf-out
  python3 sf_crawl_all.py --site https://ejemplo.com --dry-run   # solo planifica los lotes

Salida (JSON a stdout):
  {"ok": true, "site": "...", "urls_total": N, "batches": K, "batch_size": 500,
   "crawled": N, "merged_csv": ".../internal_all.csv", "per_batch": [...]}
  o {"ok": false, "reason": "...", "fallback": "..."} (exit 0).

Deps: solo stdlib. Requiere el binario de Screaming Frog para rastrear (no para --dry-run).
"""

import argparse
import csv
import glob
import json
import os
import subprocess
import sys
from urllib.request import Request, urlopen

# Reutiliza el inventario por sitemap (mismo dir).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inventario_urls import normalize_site, sitemaps_from_robots, collect_urls  # noqa: E402

FREE_LIMIT = 500  # tope de URLs por crawl en la versión gratis de Screaming Frog

# Rutas por defecto del binario según SO (se sobreescriben con SCREAMING_FROG_BINARY).
DEFAULT_BINARIES = [
    "/Applications/Screaming Frog SEO Spider.app/Contents/MacOS/ScreamingFrogSEOSpiderLauncher",
    "/Applications/Screaming Frog SEO Spider.app/Contents/MacOS/ScreamingFrogSEOSpider",
    r"C:\Program Files (x86)\Screaming Frog SEO Spider\ScreamingFrogSEOSpiderCli.exe",
    "screamingfrogseospider",  # Linux: en el PATH
]


def out(obj):
    print(json.dumps(obj, ensure_ascii=False))
    sys.exit(0)


def sf_binary():
    env = os.environ.get("SCREAMING_FROG_BINARY")
    if env:
        return env if (os.path.isfile(env) or "/" not in env and "\\" not in env) else None
    for cand in DEFAULT_BINARIES:
        if os.path.isfile(cand):
            return cand
    # último recurso: nombre en PATH (Linux)
    from shutil import which
    return which("screamingfrogseospider")


def get_urls(site, sitemap, max_urls):
    base = normalize_site(site)
    if sitemap:
        seeds, source = [sitemap], "sitemap.xml"
    else:
        seeds = sitemaps_from_robots(base)
        if seeds:
            source = "robots"
        else:
            from urllib.parse import urljoin
            seeds = [urljoin(base + "/", p) for p in ("sitemap.xml", "sitemap_index.xml")]
            source = "sitemap.xml"
    urls = sorted(collect_urls(seeds, max_urls))
    return urls, source


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def run_sf_list(binary, list_file, outdir, export_tabs, bulk_export, extra):
    """Corre SF en modo --crawl-list. Devuelve (ok, stderr)."""
    os.makedirs(outdir, exist_ok=True)
    cmd = [
        binary, "--headless",
        "--crawl-list", list_file,
        "--output-folder", outdir,
        "--overwrite",
        "--export-format", "csv",
    ]
    if export_tabs:
        cmd += ["--export-tabs", export_tabs]
    if bulk_export:
        cmd += ["--bulk-export", bulk_export]
    if extra:
        cmd += list(extra)
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
    except FileNotFoundError:
        return False, "binario de Screaming Frog no ejecutable"
    except subprocess.TimeoutExpired:
        return False, "timeout (>60 min) en un lote"
    blob = (proc.stdout or "") + (proc.stderr or "")
    if "sufficient disk space" in blob:
        return False, ("SF abortó por DISCO: la versión por defecto (storage.mode=DB) "
                       "exige 4 GB libres. Cambia a modo memoria: storage.mode=MEMORY en "
                       "~/.ScreamingFrogSEOSpider/spider.config (o GUI Configuration > System "
                       "> Storage Mode > Memory Storage) y reintenta.")
    produced = glob.glob(os.path.join(outdir, "internal_all.csv"))
    if not produced:
        return False, (blob.strip()[-600:] or "SF no generó internal_all.csv en este lote")
    return True, ""


def merge_internal(batch_dirs, dest_csv):
    """Junta los internal_all.csv de cada lote, deduplicando por Address."""
    header = None
    seen = set()
    rows = []
    addr_idx = 0
    for d in batch_dirs:
        path = os.path.join(d, "internal_all.csv")
        if not os.path.isfile(path):
            continue
        with open(path, newline="", encoding="utf-8-sig") as fh:
            reader = csv.reader(fh)
            try:
                h = next(reader)
            except StopIteration:
                continue
            if header is None:
                header = h
                low = [c.lower().strip() for c in h]
                addr_idx = low.index("address") if "address" in low else 0
            for row in reader:
                key = row[addr_idx] if len(row) > addr_idx else ",".join(row)
                if key in seen:
                    continue
                seen.add(key)
                rows.append(row)
    if header is None:
        return 0
    with open(dest_csv, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


_BROWSER_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
               "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")


def detect_shopify(base):
    """True si el sitio es Shopify (headers o HTML). Shopify rate-limita a crawlers
    con UA de bot devolviendo 4xx falsos; conviene revalidar status con UA real."""
    try:
        req = Request(base, headers={"User-Agent": _BROWSER_UA})
        with urlopen(req, timeout=15) as resp:
            hdrs = {k.lower(): v for k, v in resp.headers.items()}
            for h in ("x-shopify-stage", "x-shopid", "x-sorting-hat-shopid",
                      "x-shardid", "x-storefront-renderer-rendered"):
                if h in hdrs:
                    return True
            if "shopify" in hdrs.get("powered-by", "").lower():
                return True
            body = resp.read(60000).decode("utf-8", "replace").lower()
            return ("cdn.shopify.com" in body or "shopify.theme" in body
                    or "myshopify.com" in body)
    except Exception:  # noqa: BLE001
        return False


def _http_checks_path():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(here, "..", "..", "auditoria-tecnica",
                                         "scripts", "http_checks.py"))


def revalidate_statuses(merged_csv, concurrency):
    """Revalida las URLs marcadas 4xx/5xx con http_checks.py (UA de navegador real +
    baja concurrencia = throttle). Corrige el Status Code en el CSV con el status real
    y devuelve stats. Esto deshace los 4xx falsos por rate-limit (Shopify/WAF)."""
    from shutil import which
    checker = _http_checks_path()
    if not os.path.isfile(checker):
        return {"ok": False, "reason": f"no se encontró http_checks.py en {checker}"}

    with open(merged_csv, newline="", encoding="utf-8-sig") as fh:
        reader = csv.reader(fh)
        header = next(reader, None)
        rows = list(reader)
    if not header:
        return {"ok": False, "reason": "CSV vacío"}
    low = [c.lower().strip() for c in header]
    addr_i = low.index("address") if "address" in low else 0
    code_i = low.index("status code") if "status code" in low else None
    if code_i is None:
        return {"ok": False, "reason": "el CSV no trae columna Status Code"}

    suspect = sorted({r[addr_i] for r in rows
                      if len(r) > code_i and (r[code_i] or "").strip()[:1] in ("4", "5")})
    if not suspect:
        return {"ok": True, "revalidated": 0, "fixed": 0, "still_bad": 0}

    import tempfile
    tf = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8")
    tf.write("\n".join(suspect) + "\n")
    tf.close()
    cmd = ([("uv"), "run", checker] if which("uv") else [sys.executable, checker])
    cmd += ["--file", tf.name, "--cap", str(len(suspect)), "--concurrency", str(concurrency)]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        data = json.loads(proc.stdout.strip().splitlines()[-1])
    except Exception as e:  # noqa: BLE001
        os.unlink(tf.name)
        return {"ok": False, "reason": f"http_checks falló: {e}"}
    finally:
        if os.path.isfile(tf.name):
            os.unlink(tf.name)
    if not data.get("ok"):
        return {"ok": False, "reason": data.get("reason", "http_checks ok:false"),
                "fallback": data.get("fallback")}

    real = {r["url"]: r["status"] for r in data.get("results", []) if r.get("status")}
    fixed = still = 0
    recovered = []  # URLs que pasaron de 4xx/5xx a 2xx: SF no parseó su HTML → enriquecer
    for r in rows:
        if len(r) <= code_i:
            continue
        url = r[addr_i]
        if url in real:
            new = str(real[url])
            old = (r[code_i] or "").strip()
            if old[:1] in ("4", "5"):
                if new[:1] not in ("4", "5"):
                    fixed += 1
                    if new[:1] == "2":
                        recovered.append(url)
                else:
                    still += 1
            r[code_i] = new
    with open(merged_csv, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)
    return {"ok": True, "revalidated": len(suspect), "fixed": fixed, "still_bad": still,
            "recovered_urls": recovered,
            "note": ("Status corregidos con UA de navegador real. 'fixed' eran 4xx/5xx "
                     "FALSOS por rate-limit; 'still_bad' son roturas reales.")}


def enrich_onpage(urls, outroot, concurrency):
    """Recupera la data on-page (title/meta/canonical/encabezados) de las URLs que SF
    no pudo parsear (las rate-limitadas), vía onpage_extract.py con UA real + throttle.
    Escribe onpage_enriched.json y onpage_enriched.csv en outroot."""
    from shutil import which
    here = os.path.dirname(os.path.abspath(__file__))
    extractor = os.path.normpath(os.path.join(here, "..", "..", "auditoria-tecnica",
                                              "scripts", "onpage_extract.py"))
    if not os.path.isfile(extractor):
        return {"ok": False, "reason": f"no se encontró onpage_extract.py en {extractor}"}
    import tempfile
    tf = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8")
    tf.write("\n".join(urls) + "\n")
    tf.close()
    json_out = os.path.join(outroot, "onpage_enriched.json")
    csv_out = os.path.join(outroot, "onpage_enriched.csv")
    cmd = ([("uv"), "run", extractor] if which("uv") else [sys.executable, extractor])
    cmd += ["--file", tf.name, "--cap", str(len(urls)),
            "--concurrency", str(concurrency), "--csv", csv_out]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        data = json.loads(proc.stdout.strip().splitlines()[-1])
    except Exception as e:  # noqa: BLE001
        os.unlink(tf.name)
        return {"ok": False, "reason": f"onpage_extract falló: {e}"}
    finally:
        if os.path.isfile(tf.name):
            os.unlink(tf.name)
    if not data.get("ok"):
        return {"ok": False, "reason": data.get("reason", "onpage_extract ok:false"),
                "fallback": data.get("fallback")}
    with open(json_out, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    indexable = sum(1 for r in data["results"] if r.get("indexability") == "Indexable")
    return {"ok": True, "enriched": data["checked"], "indexable": indexable,
            "json": json_out, "csv": csv_out,
            "note": ("Data on-page (title/meta/canonical/H1/H2/hreflang/word_count) de las "
                     "URLs que SF no pudo parsear. NO incluye inlinks/grafo (eso pide crawl).")}


def main():
    ap = argparse.ArgumentParser(
        description="Rastrea un sitio entero con Screaming Frog GRATIS, troceando por lotes ≤500.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Ejemplo:\n  python3 sf_crawl_all.py --site https://ejemplo.com",
    )
    ap.add_argument("--site", required=True, help="Dominio, p.ej. https://ejemplo.com")
    ap.add_argument("--sitemap", help="URL de sitemap conocida (salta robots.txt)")
    ap.add_argument("--out", default="./sf-out", help="Carpeta de salida (default ./sf-out)")
    ap.add_argument("--batch-size", type=int, default=FREE_LIMIT,
                    help=f"URLs por lote (default {FREE_LIMIT}; no subas de {FREE_LIMIT} sin licencia)")
    ap.add_argument("--max", type=int, default=50000, help="Tope total de URLs (default 50000)")
    ap.add_argument("--export-tabs", default="Internal:All",
                    help='Pestañas a exportar (default "Internal:All")')
    ap.add_argument("--bulk-export", default="",
                    help='Bulk export opcional, p.ej. "Issues:All" (requiere coincidir con tu versión)')
    ap.add_argument("--dry-run", action="store_true", help="Solo planifica los lotes; no corre SF")
    ap.add_argument("--revalidate", dest="revalidate", action="store_true", default=None,
                    help="Forzar revalidación de 4xx/5xx con UA real (auto si detecta Shopify)")
    ap.add_argument("--no-revalidate", dest="revalidate", action="store_false",
                    help="No revalidar aunque sea Shopify")
    ap.add_argument("--revalidate-concurrency", type=int, default=4,
                    help="Concurrencia de la revalidación (default 4; bajo = más amable con el WAF)")
    ap.add_argument("--enrich", dest="enrich", action="store_true", default=None,
                    help="Recuperar data on-page (title/meta/canonical/encabezados) de las URLs "
                         "que SF no pudo parsear (auto si detecta Shopify y recupera alguna)")
    ap.add_argument("--no-enrich", dest="enrich", action="store_false",
                    help="No enriquecer on-page aunque haya URLs recuperadas")
    ap.add_argument("--enrich-concurrency", type=int, default=4,
                    help="Concurrencia del enriquecimiento on-page (default 4)")
    ap.add_argument("extra", nargs="*", help="Args extra que se pasan tal cual a SF")
    args = ap.parse_args()

    if args.batch_size < 1:
        out({"ok": False, "reason": "--batch-size debe ser ≥1"})
    if args.batch_size > FREE_LIMIT:
        # aviso, no error: con licencia puede ser válido subirlo.
        print(f"[aviso] --batch-size {args.batch_size} > {FREE_LIMIT}: la versión gratis "
              f"recorta a {FREE_LIMIT}/lote. Solo súbelo si tienes licencia.", file=sys.stderr)

    urls, source = get_urls(args.site, args.sitemap, args.max)
    if not urls:
        out({"ok": False,
             "reason": "No se obtuvieron URLs del sitemap (robots.txt sin Sitemap: y "
                       "sitemap.xml ausente/vacío, o WAF bloqueando).",
             "fallback": "Pasa un sitemap directo con --sitemap, o exporta las URLs desde "
                         "Google Search Console (Sitemaps / Páginas indexadas) y rastrea con "
                         "--crawl-list manualmente en lotes de ≤500."})

    batches = list(chunks(urls, args.batch_size))
    plan = [{"batch": i + 1, "urls": len(b)} for i, b in enumerate(batches)]

    if args.dry_run:
        out({"ok": True, "dry_run": True, "site": args.site, "source": source,
             "urls_total": len(urls), "batches": len(batches),
             "batch_size": args.batch_size, "per_batch": plan})

    binary = sf_binary()
    if not binary:
        out({"ok": False,
             "reason": "No se encontró el binario de Screaming Frog.",
             "fallback": "Instálalo desde screamingfrog.co.uk o define SCREAMING_FROG_BINARY "
                         "con la ruta al ejecutable. Detalle en SCREAMING-FROG.md."})

    outroot = os.path.abspath(args.out)
    os.makedirs(outroot, exist_ok=True)
    batch_dirs = []
    per_batch = []
    for i, batch in enumerate(batches, 1):
        bdir = os.path.join(outroot, f"batch_{i:03d}")
        os.makedirs(bdir, exist_ok=True)
        list_file = os.path.join(bdir, "urls.txt")
        with open(list_file, "w", encoding="utf-8") as fh:
            fh.write("\n".join(batch) + "\n")
        ok, err = run_sf_list(binary, list_file, bdir, args.export_tabs,
                              args.bulk_export, args.extra)
        per_batch.append({"batch": i, "urls": len(batch), "ok": ok,
                          "error": err if not ok else None})
        if ok:
            batch_dirs.append(bdir)
        else:
            # error de disco/modo: cortar y reportar (todos los lotes fallarían igual).
            if "DISCO" in err or "binario" in err:
                out({"ok": False, "reason": err, "batches_done": i - 1,
                     "per_batch": per_batch})

    merged_csv = os.path.join(outroot, "internal_all.csv")
    crawled = merge_internal(batch_dirs, merged_csv)

    # Revalidación de 4xx/5xx: SF usa UA de bot y algunos sitios (Shopify y otros WAF)
    # lo rate-limitan devolviendo 4xx FALSOS. Con UA de navegador real + baja
    # concurrencia se obtiene el status verdadero. Auto-activado si se detecta Shopify.
    reval = None
    enrich = None
    if crawled:
        is_shopify = detect_shopify(normalize_site(args.site))
        do_reval = args.revalidate if args.revalidate is not None else is_shopify
        if do_reval:
            reval = revalidate_statuses(merged_csv, args.revalidate_concurrency)
            reval["shopify_detected"] = is_shopify
            reval["triggered_by"] = ("flag --revalidate" if args.revalidate
                                     else "auto (Shopify detectado)")
            # Enriquecer on-page las URLs recuperadas (SF nunca parseó su HTML).
            recovered = reval.get("recovered_urls") or []
            do_enrich = (args.enrich if args.enrich is not None
                         else (is_shopify and bool(recovered)))
            if do_enrich and recovered:
                enrich = enrich_onpage(recovered, outroot, args.enrich_concurrency)
                enrich["urls"] = len(recovered)
            # No volcar la lista entera de URLs en el JSON de salida (puede ser enorme).
            reval.pop("recovered_urls", None)

    out({
        "ok": crawled > 0,
        "site": args.site,
        "source": source,
        "urls_total": len(urls),
        "batches": len(batches),
        "batch_size": args.batch_size,
        "crawled": crawled,
        "merged_csv": merged_csv if crawled else None,
        "per_batch": per_batch,
        "revalidation": reval,
        "onpage_enrichment": enrich,
        "hint": ("Resume el crawl: python3 ../auditoria-tecnica/scripts/parse_sf.py "
                 f"--internal {merged_csv}") if crawled else None,
    })


if __name__ == "__main__":
    main()
