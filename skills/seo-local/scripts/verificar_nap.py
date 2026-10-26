#!/usr/bin/env python3
"""Compara el NAP (Nombre, Dirección, Teléfono) visible de una página con su JSON-LD local.

Método del diploma "De Cero a SEO" (Semana 14, SEO Local): el NAP debe ser idéntico
en la web, redes y Google Maps. Este script cubre la parte web: texto visible vs
schema. La ficha de Google y las redes se comparan a mano con --ficha-nombre,
--ficha-telefono y --ficha-direccion (datos que pega el usuario).

Salida (stdout, JSON): {"ok": true, "url", "telefonos_visibles", "enlaces_tel",
"schema": [...], "comparacion": [...], "hallazgos": [...]}
Si el sitio rechaza la petición (403/WAF) devuelve {"ok": false, "fallback": "modo manual: ..."}.
Solo stdlib. Un único fetch de la página, respeta robots.txt.
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser

UA = os.environ.get(
    "SEO_USER_AGENT",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
)
TEL_RE = re.compile(r"(?:\+?\d{1,3}[\s.\-]?)?(?:\(\d{2,4}\)[\s.\-]?)?\d{2,4}[\s.\-]\d{3,4}(?:[\s.\-]\d{2,4})?")
LD_RE = re.compile(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.S | re.I)
TAG_RE = re.compile(r"<(script|style)[^>]*>.*?</\1>|<[^>]+>", re.S | re.I)
TIPOS_LOCALES = ("LocalBusiness", "Restaurant", "Dentist", "MedicalClinic", "LegalService", "Store",
                 "Locksmith", "Plumber", "Electrician", "HVACBusiness", "BarOrPub", "CafeOrCoffeeShop",
                 "Bakery", "HairSalon", "BeautySalon", "AutoRepair", "AutoDealer", "RealEstateAgent",
                 "Physician", "Pharmacy", "Optician", "GeneralContractor", "MovingCompany", "ProfessionalService")


def solo_digitos(texto):
    return re.sub(r"\D", "", texto or "")


def norm_texto(texto):
    return re.sub(r"\s+", " ", (texto or "").strip().lower())


def permitido(url):
    p = urllib.parse.urlparse(url)
    rp = urllib.robotparser.RobotFileParser()
    try:
        req = urllib.request.Request(f"{p.scheme}://{p.netloc}/robots.txt", headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=15) as r:
            rp.parse(r.read().decode("utf-8", "replace").splitlines())
    except (urllib.error.URLError, OSError):
        return True
    return rp.can_fetch(UA, url)


def aplanar(nodo, salida):
    if isinstance(nodo, list):
        for x in nodo:
            aplanar(x, salida)
    elif isinstance(nodo, dict):
        tipo = nodo.get("@type")
        tipos = tipo if isinstance(tipo, list) else [tipo]
        if any(t in TIPOS_LOCALES for t in tipos if isinstance(t, str)):
            salida.append(nodo)
        for v in nodo.values():
            aplanar(v, salida)


def direccion_texto(addr):
    if isinstance(addr, str):
        return addr
    if isinstance(addr, dict):
        partes = [addr.get(k, "") for k in ("streetAddress", "addressLocality", "addressRegion", "postalCode", "addressCountry")]
        return ", ".join(str(p) for p in partes if p)
    return ""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url", help="Página con el NAP (contacto, footer o Home)")
    ap.add_argument("--sitio", help="Dominio; escribe .seo-audit/<sitio>/data/local-seo.json")
    ap.add_argument("--raiz", default=".", help="Raíz donde vive .seo-audit")
    ap.add_argument("--ficha-nombre", help="Nombre tal como aparece en Google Business Profile")
    ap.add_argument("--ficha-telefono", help="Teléfono de la ficha")
    ap.add_argument("--ficha-direccion", help="Dirección de la ficha")
    args = ap.parse_args()

    if not permitido(args.url):
        print(json.dumps({"ok": False, "reason": "robots.txt no permite rastrear esta URL.",
                          "fallback": "modo manual: copia el NAP de la página a mano."}, ensure_ascii=False))
        return 0
    try:
        req = urllib.request.Request(args.url, headers={"User-Agent": UA, "Accept-Language": "es,en;q=0.8"})
        with urllib.request.urlopen(req, timeout=20) as r:
            html = r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        motivo = "El sitio rechazó la petición (posible WAF/anti-bot)." if exc.code in (403, 429) else f"HTTP {exc.code}"
        print(json.dumps({"ok": False, "reason": motivo,
                          "fallback": "modo manual: abre la página, copia nombre, dirección y teléfono, y pásalos con --ficha-*."},
                         ensure_ascii=False))
        return 0
    except (urllib.error.URLError, OSError) as exc:
        print(json.dumps({"ok": False, "reason": str(exc), "fallback": "modo manual: revisa la URL."}, ensure_ascii=False))
        return 0

    bloques = []
    for m in LD_RE.finditer(html):
        try:
            aplanar(json.loads(m.group(1).strip()), bloques)
        except ValueError:
            continue
    schema = [{"tipo": b.get("@type"), "nombre": b.get("name"), "telefono": b.get("telephone"),
               "direccion": direccion_texto(b.get("address")), "url": b.get("url")} for b in bloques]

    visible = TAG_RE.sub(" ", html)
    telefonos = sorted({t.strip() for t in TEL_RE.findall(visible) if 8 <= len(solo_digitos(t)) <= 14})
    enlaces_tel = sorted({urllib.parse.unquote(h).replace("tel:", "").strip()
                          for h in re.findall(r'href=["\'](tel:[^"\']+)', html, re.I)})

    hallazgos, comparacion = [], []
    if not schema:
        hallazgos.append("No hay JSON-LD LocalBusiness en la página: crear el bloque con la skill schema-jsonld.")
    if not enlaces_tel:
        hallazgos.append("No hay enlace tel: para llamar con un toque en móvil.")
    if not telefonos and not enlaces_tel:
        hallazgos.append("No se detectó teléfono visible: el NAP debe estar en texto HTML (footer o contacto).")

    vis_digitos = {solo_digitos(t) for t in telefonos}
    tel_digitos = {solo_digitos(t) for t in enlaces_tel}

    def coincide_tel(a, conjunto):
        return any(a[-8:] == b[-8:] for b in conjunto)

    if vis_digitos and tel_digitos and not any(coincide_tel(t, vis_digitos) for t in tel_digitos):
        hallazgos.append("El enlace tel: no coincide con el teléfono visible en el texto.")
    for s in schema:
        d = solo_digitos(s["telefono"])
        if d and vis_digitos and not coincide_tel(d, vis_digitos):
            hallazgos.append(f"El teléfono del schema ({s['telefono']}) no coincide con el visible.")
        if s["nombre"] and norm_texto(s["nombre"]) not in norm_texto(visible):
            hallazgos.append(f"El nombre del schema ('{s['nombre']}') no aparece igual en el texto visible.")
        if s["direccion"]:
            calle = norm_texto(s["direccion"].split(",")[0])
            if calle and calle not in norm_texto(visible):
                hallazgos.append("La calle del schema no aparece igual en el texto visible.")

    ref = schema[0] if schema else {}
    for campo, ficha, web in (("nombre", args.ficha_nombre, ref.get("nombre")),
                              ("telefono", args.ficha_telefono, ref.get("telefono")),
                              ("direccion", args.ficha_direccion, ref.get("direccion"))):
        if ficha:
            if campo == "telefono":
                coincide = bool(web) and solo_digitos(ficha)[-8:] == solo_digitos(web)[-8:]
            else:
                coincide = bool(web) and (norm_texto(ficha) in norm_texto(web) or norm_texto(web) in norm_texto(ficha))
            comparacion.append({"campo": campo, "ficha": ficha, "web_schema": web, "coincide": bool(coincide)})
            if not coincide:
                hallazgos.append(f"{campo}: la ficha ('{ficha}') difiere del schema ('{web}'). Unifica a una sola forma.")

    resultado = {"ok": True, "url": args.url, "telefonos_visibles": telefonos, "enlaces_tel": enlaces_tel,
                 "schema": schema, "comparacion": comparacion, "hallazgos": hallazgos,
                 "nota": "Redes sociales y directorios se comparan a mano."}
    if args.sitio:
        carpeta = os.path.join(args.raiz, ".seo-audit", args.sitio, "data")
        os.makedirs(carpeta, exist_ok=True)
        with open(os.path.join(carpeta, "local-seo.json"), "w", encoding="utf-8") as fh:
            json.dump(resultado, fh, ensure_ascii=False, indent=2)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
