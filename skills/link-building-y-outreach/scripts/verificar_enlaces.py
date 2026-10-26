#!/usr/bin/env python3
"""
verificar_enlaces.py: comprueba si los enlaces conseguidos siguen publicados y con que atributos.

Cubre el paso "Seguimiento" del Planificador de Outreach (S12 L5): confirmar que el enlace se
publico, con el anchor adecuado y sin rel="sponsored"/"nofollow" cuando se pacto Do-Follow.
Idea adaptada de verify_backlinks.py de claude-seo (MIT, agricidaniel), reescrita con solo stdlib.

Uso:
    python3 verificar_enlaces.py --target https://miweb.com --links enlaces.csv
    python3 verificar_enlaces.py --target miweb.com --links enlaces.csv --out .seo-audit/miweb.com/data/backlinks.json

CSV de entrada: columna source (URL donde deberia estar el enlace); opcional anchor_esperado.
Salida JSON: {"ok":true,"results":[{"source","status":"presente|ausente|error|bloqueado-robots",
              "http","anchor","rel","dofollow":bool|null,"anchor_ok":bool|null}],"summary":{...}}
Con --out se FUSIONA la clave "verificacion" en el JSON existente.
Respeta robots.txt de cada sitio, 1 peticion por segundo, maximo 200 URLs. User-Agent de navegador.
Deps: solo stdlib.
"""
import argparse
import csv
import json
import os
import time
import urllib.error
import urllib.request
import urllib.robotparser
from html.parser import HTMLParser
from urllib.parse import urlparse

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
MAX_URLS = 200


class Links(HTMLParser):
    def __init__(self, host):
        super().__init__()
        self.host, self.found, self._cur, self._txt = host, [], None, []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            a = dict(attrs)
            h = (a.get("href") or "")
            if self.host in urlparse(h).netloc.lower().removeprefix("www."):
                self._cur, self._txt = (h, (a.get("rel") or "").lower()), []

    def handle_data(self, d):
        if self._cur:
            self._txt.append(d)

    def handle_endtag(self, tag):
        if tag == "a" and self._cur:
            self.found.append((self._cur[0], self._cur[1], " ".join("".join(self._txt).split())))
            self._cur = None


def robots_ok(url, cache):
    o = urlparse(url)
    base = f"{o.scheme}://{o.netloc}"
    if base not in cache:
        rp = urllib.robotparser.RobotFileParser()
        try:
            rq = urllib.request.Request(base + "/robots.txt", headers={"User-Agent": UA})
            rp.parse(urllib.request.urlopen(rq, timeout=10).read().decode("utf-8", "replace").splitlines())
        except Exception:  # noqa: BLE001
            rp = None
        cache[base] = rp
    rp = cache[base]
    return True if rp is None else rp.can_fetch(UA, url)


def main():
    p = argparse.ArgumentParser(description="Verifica que los enlaces conseguidos sigan publicados.")
    p.add_argument("--target", required=True, help="Tu dominio o URL (ej. miweb.com).")
    p.add_argument("--links", required=True, help="CSV con columna 'source' y opcional 'anchor_esperado'.")
    p.add_argument("--out", help="JSON donde fusionar la clave 'verificacion'.")
    a = p.parse_args()
    host = (urlparse(a.target if "//" in a.target else "//" + a.target).netloc or a.target).lower().removeprefix("www.")
    try:
        with open(a.links, encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
    except OSError as e:
        print(json.dumps({"ok": False, "reason": str(e), "fallback": "modo manual: abre cada URL y busca tu enlace"}))
        return
    results, cache = [], {}
    for r in rows[:MAX_URLS]:
        src = (r.get("source") or r.get("Source") or "").strip()
        exp = (r.get("anchor_esperado") or "").strip().lower()
        if not src:
            continue
        res = {"source": src, "status": "error", "http": None, "anchor": None, "rel": None,
               "dofollow": None, "anchor_ok": None}
        if not robots_ok(src, cache):
            res["status"] = "bloqueado-robots"
        else:
            try:
                rq = urllib.request.Request(src, headers={"User-Agent": UA})
                with urllib.request.urlopen(rq, timeout=20) as resp:
                    res["http"] = resp.status
                    html = resp.read(2_000_000).decode("utf-8", "replace")
                lp = Links(host)
                lp.feed(html)
                if lp.found:
                    href, rel, txt = lp.found[0]
                    res.update(status="presente", anchor=txt, rel=rel or None,
                               dofollow=not any(x in rel for x in ("nofollow", "sponsored", "ugc")))
                    if exp:
                        res["anchor_ok"] = exp in txt.lower()
                else:
                    res["status"] = "ausente"
            except urllib.error.HTTPError as e:
                res["http"] = e.code
                res["status"] = "error"
            except Exception:  # noqa: BLE001
                res["status"] = "error"
        results.append(res)
        time.sleep(1)
    summ = {}
    for r in results:
        summ[r["status"]] = summ.get(r["status"], 0) + 1
    out = {"ok": True, "target": host, "results": results, "summary": summ,
           "note": "Solo verifica la pagina indicada. Un 'error' puede ser un WAF: revisa a mano antes de reclamar."}
    if a.out:
        ex = {}
        if os.path.exists(a.out):
            try:
                ex = json.load(open(a.out, encoding="utf-8"))
            except ValueError:
                ex = {}
        ex["verificacion"] = {"results": results, "summary": summ}
        os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
        json.dump(ex, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
