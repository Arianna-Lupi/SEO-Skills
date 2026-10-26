#!/usr/bin/env python3
"""
calidad_contenido.py: revisión determinista de señales de calidad y E-E-A-T de UNA página.

Apoya la revisión de la Semana 7 (lección 5, E-E-A-T) y de la Semana 11 (valor real, escaneabilidad).
No puntúa "autoridad" ni inventa cifras: detecta señales verificables en el HTML/texto y marca lo
que falta para que lo resuelva una persona.

Detecta:
  - Autoría: byline ("por X", "autor"), enlace rel=author, bio, schema Person/Author.
  - Fechas: publicación y última actualización visibles (time, datePublished, dateModified, "actualizado").
  - Experiencia de primera mano: marcadores ("probé", "en mi experiencia", "caso", "antes y después"), imágenes/figuras.
  - Fuentes: enlaces externos y su proporción; frases con cifras sin fuente cercana.
  - Estructura: palabras, H1 únicos, párrafos largos (>4 líneas aprox. = 80 palabras), listas, tablas.
  - Contenido delgado orientativo según tipo (--tipo): suelos de cobertura de claude-seo, NO objetivos
    ni factor de ranking.
  - Confianza: enlaces a contacto, privacidad, "sobre nosotros" (solo HTML/URL).

Entradas (una):  --file archivo.html|.md|.txt   o   --url https://...   (respeta robots.txt, User-Agent de navegador,
una sola petición; detecta bloqueo WAF y pide guardar el HTML a mano).
Uso:
  python3 calidad_contenido.py --file pagina.html --tipo blog [--out .seo-audit/<sitio>/data/calidad.json]
  python3 calidad_contenido.py --url https://ejemplo.com/post --tipo servicio
Solo stdlib. Si falla: {"ok": false, "reason": ..., "fallback": "modo manual"} con exit 0.
"""
import argparse
import json
import re
import sys
import urllib.request
import urllib.robotparser
from html.parser import HTMLParser
from urllib.parse import urlparse

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
# Suelos de cobertura (claude-seo). No son objetivos ni factor de ranking.
SUELOS = {"home": 500, "servicio": 800, "blog": 1500, "producto": 300, "ubicacion": 500}
EXPERIENCIA = ["en mi experiencia", "probé", "probamos", "hemos probado", "nuestro caso", "caso real", "antes y después",
               "cuando empecé", "nos encontramos", "en nuestro taller", "resultados reales", "lo comprobé", "trabajamos con"]
CIFRA = re.compile(r"(\b\d{1,3}(?:[.,]\d+)?\s?%|\bun estudio\b|\bsegún un estudio\b|\binvestigaciones?\b)", re.I)
CITA = re.compile(r"(https?://|\[\^?\d+\]|según [A-ZÁÉÍÓÚ]|fuente:)")


class P(HTMLParser):
    def __init__(self, base):
        super().__init__(convert_charrefs=True)
        self.base = urlparse(base).netloc if base else ""
        self.skip = 0
        self.txt, self.h, self.links, self.meta, self.jsonld = [], [], [], {}, []
        self.cur = None
        self.flags = {"time": False, "figure": 0, "img": 0, "ul": 0, "table": 0, "author_rel": False}
        self._ld = False

    def handle_starttag(self, tag, at):
        d = dict(at)
        if tag in ("script", "style", "noscript", "nav", "footer", "header"):
            if tag == "script" and d.get("type") == "application/ld+json":
                self._ld = True
            else:
                self.skip += 1
        if tag in ("h1", "h2", "h3", "h4"):
            self.cur = [tag, ""]
        if tag == "a" and d.get("href"):
            self.links.append((d["href"], d.get("rel", "")))
            if "author" in d.get("rel", ""):
                self.flags["author_rel"] = True
        if tag == "meta" and d.get("name"):
            self.meta[d["name"].lower()] = d.get("content", "")
        if tag == "time":
            self.flags["time"] = True
        if tag in ("figure", "img", "table"):
            self.flags["figure" if tag == "figure" else tag] += 1
        if tag in ("ul", "ol"):
            self.flags["ul"] += 1

    def handle_endtag(self, tag):
        if tag == "script" and self._ld:
            self._ld = False
        elif tag in ("script", "style", "noscript", "nav", "footer", "header") and self.skip:
            self.skip -= 1
        if tag in ("h1", "h2", "h3", "h4") and self.cur:
            self.h.append((self.cur[0], self.cur[1].strip()))
            self.cur = None

    def handle_data(self, data):
        if self._ld:
            self.jsonld.append(data)
        elif not self.skip:
            self.txt.append(data)
            if self.cur:
                self.cur[1] += data


def fetch(url):
    pu = urlparse(url)
    rp = urllib.robotparser.RobotFileParser(f"{pu.scheme}://{pu.netloc}/robots.txt")
    try:
        rp.read()
        if not rp.can_fetch(UA, url):
            return None, "robots.txt bloquea esta URL: guarda el HTML a mano y usa --file"
    except Exception:  # noqa: BLE001
        pass
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "es,en;q=0.8"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read().decode("utf-8", "replace"), None
    except Exception as e:  # noqa: BLE001
        return None, f"No pude descargar ({e}). Posible WAF o bloqueo: guarda el HTML a mano y usa --file"


def main():
    ap = argparse.ArgumentParser(description="Señales de calidad y E-E-A-T de una página.")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--file")
    g.add_argument("--url")
    ap.add_argument("--tipo", choices=sorted(SUELOS), help="Tipo de página para el suelo de cobertura")
    ap.add_argument("--out")
    a = ap.parse_args()
    if a.url:
        raw, err = fetch(a.url)
        if err:
            print(json.dumps({"ok": False, "reason": err, "fallback": "modo manual"}, ensure_ascii=False))
            return 0
    else:
        try:
            raw = open(a.file, encoding="utf-8").read()
        except Exception as e:  # noqa: BLE001
            print(json.dumps({"ok": False, "reason": str(e), "fallback": "modo manual"}))
            return 0
    es_html = bool(re.search(r"<html|<body|<p[ >]", raw, re.I))
    p = P(a.url or "")
    if es_html:
        p.feed(raw)
        texto = " ".join(p.txt)
        heads = p.h
        ld = " ".join(p.jsonld).lower()
    else:
        texto = raw
        heads = [(f"h{len(m.group(1))}", m.group(2)) for m in re.finditer(r"^(#{1,4})\s+(.+)$", raw, re.M)]
        ld = ""
    texto = re.sub(r"\s+", " ", texto)
    low = texto.lower()
    palabras = len(re.findall(r"\w+", texto))
    parrafos = [x for x in re.split(r"\n\s*\n", raw) if len(x.split()) > 80] if not es_html else []
    frases = [s for s in re.split(r"(?<=[.!?])\s+", texto) if len(s.split()) >= 3]
    sin_fuente = [s[:120] for s in frases if CIFRA.search(s) and not CITA.search(s)]
    ext = [h for h, rel in p.links if h.startswith("http") and (not p.base or urlparse(h).netloc != p.base)] if es_html else []

    senal = {
        "autoria": bool(re.search(r"\b[Pp]or [A-ZÁÉÍÓÚ][a-záéíóú]+ [A-ZÁÉÍÓÚ]|\bautor[a]?\b|\bescrito por\b|\brevisado por\b", texto)) or p.flags["author_rel"] or "author" in ld or '"person"' in ld,
        "bio_o_credenciales": bool(re.search(r"\b(bio|biografía|años de experiencia|certificad|licenciad|colegiad|especialista en)\b", low)),
        "fecha_publicacion": p.flags["time"] or "datepublished" in ld or bool(re.search(r"publicado|publicación", low)),
        "fecha_actualizacion": "datemodified" in ld or bool(re.search(r"actualizad[oa]|última actualización|revisado el", low)),
        "experiencia_primera_mano": any(m in low for m in EXPERIENCIA) or p.flags["figure"] > 0,
        "enlaces_a_fuentes_externas": len(ext) > 0,
        "enlace_contacto_privacidad_nosotros": bool(re.search(r"contacto|privacidad|nosotros|quienes|quiénes|about|privacy|contact", low + " " + " ".join(h for h, _ in p.links).lower())) if es_html else None,
    }
    flags = []
    if not senal["autoria"]:
        flags.append({"sev": "alta", "msg": "No veo autoría visible (byline, bio o schema Person): Semana 7, E-E-A-T. Pon nombre, foto y credenciales reales."})
    if not senal["fecha_actualizacion"]:
        flags.append({"sev": "media", "msg": "Sin fecha de actualización visible: si el tema cambia, añádela y revisa los datos."})
    if not senal["experiencia_primera_mano"]:
        flags.append({"sev": "media", "msg": "Sin marcadores de experiencia propia (casos, pruebas, fotos): aporta algo que la SERP no tenga."})
    if sin_fuente:
        flags.append({"sev": "alta", "msg": f"{len(sin_fuente)} afirmación(es) con cifra o estudio sin fuente cercana: cita fuente primaria o elimina el dato.", "ejemplos": sin_fuente[:3]})
    if es_html and not ext:
        flags.append({"sev": "baja", "msg": "No hay enlaces a fuentes externas de autoridad (relevante en temas sensibles)."})
    h1s = [t for tag, t in heads if tag == "h1"]
    if len(h1s) != 1:
        flags.append({"sev": "alta", "msg": f"Debe haber un solo H1; hay {len(h1s)}."})
    if parrafos:
        flags.append({"sev": "baja", "msg": f"{len(parrafos)} párrafo(s) muy largos: divide en 3 o 4 líneas, usa negritas y listas."})
    suelo = SUELOS.get(a.tipo) if a.tipo else None
    if suelo and palabras < suelo:
        flags.append({"sev": "baja", "msg": f"{palabras} palabras, por debajo del suelo orientativo de {suelo} para '{a.tipo}'. Es una señal de revisar cobertura, no un objetivo: 600 palabras que resuelven la intención superan a 3000 de relleno (práctica de coaches)."})
    res = {"ok": True, "palabras": palabras, "h1": h1s, "encabezados": [f"{t.upper()}: {x}" for t, x in heads][:40],
           "listas": p.flags["ul"] if es_html else None, "tablas": p.flags["table"] if es_html else None,
           "imagenes": p.flags["img"] if es_html else None, "senales": senal, "flags": flags,
           "nota": "Señales detectables, no una nota de autoridad. La decisión final es humana."}
    out = json.dumps(res, ensure_ascii=False, indent=2)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(out)
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
