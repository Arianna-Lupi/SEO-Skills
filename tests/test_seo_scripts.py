#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["requests", "tldextract", "beautifulsoup4"]
# ///
"""
test_seo_scripts.py — Suite offline y determinística de los scripts SEO.

Cubre los 3 scripts del flujo de competencia/metadata/brief:
  - analisis-de-competidores/scripts/competitor_domains.py
  - optimizacion-on-page-meta/scripts/serp_metadata.py
  - brief-de-contenido/scripts/serp_outline.py

Estrategia (100% sin red externa, determinística):
  - Levanta 2 servidores HTTP locales (puertos efímeros) que sirven HTML FIJO,
    un redirect 302 entre ellos y un 404. Así el contenido no cambia entre
    corridas y el resultado es reproducible.
  - Tests unitarios de las funciones puras (registered_domain, extract_meta,
    extract_headings) con hostnames reales para probar la extracción de dominio
    (eTLD+1) y el parseo de metas/encabezados.
  - Tests de integración que ejecutan cada script por CLI (subprocess) contra
    los servidores locales vía --urls, y verifican:
      * estructura y valores exactos del JSON,
      * seguimiento de redirects (cambia el dominio final),
      * dedup por dominio y "Análisis de Repetición" (misma URL en 2 keywords),
      * exclusión de --own,
      * degradación limpia sin SERPAPI_API_KEY (ok:false, exit 0),
      * DETERMINISMO: 3 corridas idénticas byte a byte.

Ejecutar:
  uv run tests/test_seo_scripts.py
  # o: python3 tests/test_seo_scripts.py   (requiere requests, tldextract, bs4)
"""

import importlib.util
import json
import os
import subprocess
import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import tldextract
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
CD_PATH = ROOT / "skills/analisis-de-competidores/scripts/competitor_domains.py"
MD_PATH = ROOT / "skills/optimizacion-on-page-meta/scripts/serp_metadata.py"
SO_PATH = ROOT / "skills/brief-de-contenido/scripts/serp_outline.py"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


CD = load("competitor_domains", CD_PATH)
MD = load("serp_metadata", MD_PATH)
SO = load("serp_outline", SO_PATH)

EXTRACT = tldextract.TLDExtract(suffix_list_urls=())

# --- Fixtures HTML fijas (contenido reproducible) -------------------------
TITLE_OK = "Comprar zapatillas de running baratas online en España"  # en rango 50-60
DESC_OK = (
    "Compra zapatillas de running baratas con envío gratis. Compara marcas, "
    "tallas y precios, y encuentra tu par ideal hoy mismo. Aprovecha ya."
)  # en rango 120-155
TITLE_LONG = "Guía definitiva y completísima para elegir las mejores zapatillas de running en 2026 según tu pisada"  # >60

HTML_OK = f"""<!doctype html><html><head>
<title>  {TITLE_OK}  </title>
<meta name="description" content="{DESC_OK}">
<meta property="og:title" content="OG Zapatillas">
<meta property="og:description" content="OG desc running">
</head><body>
<h1>Zapatillas de running</h1>
<h2>Cómo elegir</h2><h3>Según tu pisada</h3>
<h2>Mejores modelos</h2>
</body></html>"""

HTML_LONG = f"""<!doctype html><html><head>
<title>{TITLE_LONG}</title>
</head><body><h1>Running 2026</h1><h2>Cómo elegir</h2><h2>Amortiguación</h2></body></html>"""

HTML_TARGET = """<!doctype html><html><head><title>Destino tras redirect</title>
</head><body><h1>Destino</h1><h2>Otra sección</h2></body></html>"""


class Handler(BaseHTTPRequestHandler):
    redirect_to = ""  # se setea tras conocer el puerto del 2º server

    def log_message(self, *a):  # silencio
        pass

    def _send(self, code, body="", headers=None):
        self.send_response(code)
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        data = body.encode("utf-8")
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/meta_ok":
            self._send(200, HTML_OK)
        elif self.path == "/meta_long":
            self._send(200, HTML_LONG)
        elif self.path == "/target":
            self._send(200, HTML_TARGET)
        elif self.path == "/redirect":
            self._send(302, "", {"Location": self.redirect_to})
        elif self.path == "/notfound":
            self._send(404, "no")
        else:
            self._send(200, HTML_OK)


_servers = []
BASE1 = BASE2 = ""


def setUpModule():
    global BASE1, BASE2
    s1 = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    s2 = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    _servers.extend([s1, s2])
    p1 = s1.server_address[1]
    p2 = s2.server_address[1]
    BASE1 = f"http://127.0.0.1:{p1}"
    BASE2 = f"http://127.0.0.1:{p2}"
    Handler.redirect_to = f"{BASE2}/target"
    for s in _servers:
        threading.Thread(target=s.serve_forever, daemon=True).start()


def tearDownModule():
    for s in _servers:
        s.shutdown()


def run(script, *args, env=None):
    """Ejecuta un script por CLI y devuelve (stdout_str, parsed_json)."""
    e = dict(os.environ)
    # aislar: sin clave real ni env de skills, para que --urls sea la única fuente
    e.pop("SERPAPI_API_KEY", None)
    e["HOME"] = "/tmp/seo-test-nohome"
    if env:
        e.update(env)
    r = subprocess.run(
        [sys.executable, str(script), *args],
        capture_output=True, text=True, env=e, timeout=60,
    )
    assert r.returncode == 0, f"exit {r.returncode}: {r.stderr}"
    return r.stdout, json.loads(r.stdout)


def dom(url):
    return CD.registered_domain(url, EXTRACT)


# ==========================================================================
# 1) Unit: extracción de dominio registrado (eTLD+1)
# ==========================================================================
class TestRegisteredDomain(unittest.TestCase):
    def test_subdomain_collapses_to_root(self):
        self.assertEqual(dom("https://blog.hubspot.es/marketing/x"), "hubspot.es")

    def test_www_stripped(self):
        self.assertEqual(dom("https://www.semrush.com/blog/"), "semrush.com")

    def test_multilevel_tld(self):
        self.assertEqual(dom("https://sub.example.co.uk/p"), "example.co.uk")

    def test_case_insensitive(self):
        self.assertEqual(dom("https://WWW.Example.COM/A"), "example.com")

    def test_garbage_returns_empty(self):
        self.assertEqual(dom("garbage"), "")

    def test_deterministic(self):
        vals = {dom("https://a.b.example.com/x") for _ in range(5)}
        self.assertEqual(vals, {"example.com"})


# ==========================================================================
# 2) Unit: parseo de metas y encabezados
# ==========================================================================
class TestParsers(unittest.TestCase):
    def test_extract_meta_all_fields(self):
        title, desc, h1, ogt, ogd = MD.extract_meta(HTML_OK, BeautifulSoup)
        self.assertEqual(title, TITLE_OK)  # clean() colapsa los espacios extra
        self.assertEqual(desc, DESC_OK)
        self.assertEqual(h1, "Zapatillas de running")
        self.assertEqual(ogt, "OG Zapatillas")
        self.assertEqual(ogd, "OG desc running")

    def test_meta_ranges_are_len_based(self):
        self.assertTrue(50 <= len(TITLE_OK) <= 60)
        self.assertTrue(120 <= len(DESC_OK) <= 155)
        self.assertFalse(50 <= len(TITLE_LONG) <= 60)

    def test_extract_meta_missing_description(self):
        title, desc, h1, ogt, ogd = MD.extract_meta(HTML_LONG, BeautifulSoup)
        self.assertEqual(title, TITLE_LONG)
        self.assertEqual(desc, "")

    def test_extract_headings(self):
        h1, headings = SO.extract_headings(HTML_OK, BeautifulSoup)
        self.assertEqual(h1, "Zapatillas de running")
        self.assertEqual(headings, ["H2: Cómo elegir", "H3: Según tu pisada", "H2: Mejores modelos"])


# ==========================================================================
# 3) Integración: competitor_domains.py
# ==========================================================================
class TestCompetitorDomains(unittest.TestCase):
    def test_dedup_and_repetition(self):
        # misma URL en 2 keywords -> repeticion 2; 2 dominios distintos (puertos)
        _, d = run(CD_PATH, "kw1|kw2", "--urls", f"{BASE1}/meta_ok,{BASE2}/meta_ok")
        self.assertTrue(d["ok"])
        comps = {c["domain"]: c for c in d["competitors"]}
        self.assertEqual(set(comps), {dom(BASE1 + "/meta_ok"), dom(BASE2 + "/meta_ok")})
        for c in d["competitors"]:
            self.assertEqual(c["repeticion"], 2)  # aparece en kw1 y kw2

    def test_ranking_by_best_position(self):
        _, d = run(CD_PATH, "kw", "--urls", f"{BASE1}/meta_ok,{BASE2}/meta_ok")
        # primer dominio de --urls sale en posición 1 -> va primero
        self.assertEqual(d["competitors"][0]["domain"], dom(BASE1 + "/meta_ok"))
        self.assertEqual(d["competitors"][0]["best_position"], 1)

    def test_follows_redirect_changes_domain(self):
        # BASE1/redirect -> 302 -> BASE2/target ; el dominio final debe ser el de BASE2
        _, d = run(CD_PATH, "kw", "--urls", f"{BASE1}/redirect")
        self.assertEqual(len(d["competitors"]), 1)
        self.assertEqual(d["competitors"][0]["domain"], dom(BASE2 + "/target"))

    def test_no_visit_keeps_original_domain(self):
        # con --no-visit NO sigue el redirect: se queda con el dominio de BASE1
        _, d = run(CD_PATH, "kw", "--urls", f"{BASE1}/redirect", "--no-visit")
        self.assertEqual(d["competitors"][0]["domain"], dom(BASE1 + "/redirect"))

    def test_own_excluded(self):
        own = dom(BASE1 + "/meta_ok")
        _, d = run(CD_PATH, "kw", "--urls", f"{BASE1}/meta_ok,{BASE2}/meta_ok", "--own", own)
        doms = {c["domain"] for c in d["competitors"]}
        self.assertNotIn(own, doms)
        self.assertIn(dom(BASE2 + "/meta_ok"), doms)

    def test_degrades_without_key(self):
        _, d = run(CD_PATH, "kw sin urls ni clave")
        self.assertFalse(d["ok"])
        self.assertIn("SERPAPI_API_KEY", d["reason"])

    def test_deterministic(self):
        outs = [run(CD_PATH, "kw1|kw2", "--urls", f"{BASE1}/meta_ok,{BASE2}/meta_ok")[0] for _ in range(3)]
        self.assertEqual(len(set(outs)), 1)


# ==========================================================================
# 4) Integración: serp_metadata.py
# ==========================================================================
class TestSerpMetadata(unittest.TestCase):
    def test_extracts_meta_in_range(self):
        _, d = run(MD_PATH, "zapatillas", "--urls", f"{BASE1}/meta_ok")
        c = d["competitors"][0]
        self.assertEqual(c["meta_title"], TITLE_OK)
        self.assertEqual(c["meta_title_len"], len(TITLE_OK))
        self.assertTrue(c["meta_title_in_range"])
        self.assertEqual(c["meta_description"], DESC_OK)
        self.assertTrue(c["meta_description_in_range"])
        self.assertEqual(c["h1"], "Zapatillas de running")
        self.assertEqual(c["og_title"], "OG Zapatillas")

    def test_out_of_range_and_missing_desc(self):
        _, d = run(MD_PATH, "zapatillas", "--urls", f"{BASE1}/meta_long")
        c = d["competitors"][0]
        self.assertFalse(c["meta_title_in_range"])
        self.assertEqual(c["meta_description"], "")
        self.assertFalse(c["meta_description_in_range"])

    def test_404_yields_error_not_crash(self):
        _, d = run(MD_PATH, "zapatillas", "--urls", f"{BASE1}/notfound")
        self.assertTrue(d["ok"])
        self.assertIn("error", d["competitors"][0])

    def test_degrades_without_key(self):
        _, d = run(MD_PATH, "kw sin urls")
        self.assertFalse(d["ok"])

    def test_deterministic(self):
        outs = [run(MD_PATH, "kw", "--urls", f"{BASE1}/meta_ok,{BASE1}/meta_long")[0] for _ in range(3)]
        self.assertEqual(len(set(outs)), 1)


# ==========================================================================
# 5) Integración: serp_outline.py (encabezados del brief)
# ==========================================================================
class TestSerpOutline(unittest.TestCase):
    def test_headings_and_suggested_outline(self):
        # "Cómo elegir" aparece en ambas páginas -> primero en el outline por frecuencia
        _, d = run(SO_PATH, "zapatillas", "--urls", f"{BASE1}/meta_ok,{BASE2}/meta_long")
        self.assertTrue(d["ok"])
        self.assertEqual(len(d["competitors"]), 2)
        self.assertEqual(d["suggested_outline"][0], "Cómo elegir")

    def test_degrades_without_key(self):
        _, d = run(SO_PATH, "kw sin urls")
        self.assertFalse(d["ok"])

    def test_deterministic(self):
        outs = [run(SO_PATH, "kw", "--urls", f"{BASE1}/meta_ok,{BASE2}/meta_long")[0] for _ in range(3)]
        self.assertEqual(len(set(outs)), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
