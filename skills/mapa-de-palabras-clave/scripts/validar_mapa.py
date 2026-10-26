#!/usr/bin/env python3
"""
validar_mapa.py, Valida un Mapa de Palabras Clave contra los criterios del
diploma "De Cero a SEO" (Semana 5, Verónica Romero) antes de entregarlo:

  - 1:1: una keyword primaria por URL, sin repetirse (ni casi repetirse).
  - Valor SEO coherente: URLs con valor llevan keyword; URLs sin valor, no.
  - Plan de acción coherente con la posición (Mantener solo si ya está en top 3,
    Actualizar/Optimizar si está entre 4 y 20 o fuera del top 100).
  - Inventario limpio: sin imágenes/archivos/duplicados/basura técnica.
  - Intención (temperatura) válida: Baja, Media o Alta.

No sustituye a canibalizacion.py (que detecta keyword repetida y quick wins);
este script revisa la CALIDAD del mapa completo, como el prompt de validación
final de la Semana 5 (video 10).

Entrada: CSV o JSON con filas {url, valor_seo, keyword, temperatura, volumen?,
dificultad?, posicion?, accion?}. Los nombres de columna toleran variantes en
español e inglés (p. ej. "Palabra Clave Principal", "Intención", "Acción").

Uso:
  python3 validar_mapa.py --file mapa.csv
  cat mapa.json | python3 validar_mapa.py --file - --format json
  python3 validar_mapa.py --file mapa.csv --top-pos 3

Salida (JSON a stdout):
  {"ok": true, "issues": [{"id","severity","url","keyword","message","fix"}],
   "summary": {"rows","with_value","without_value","by_severity":{...},
               "completeness_pct","map_score"}}
  o {"ok": false, "reason": "..."} (exit 0)

map_score es una rúbrica auxiliar de este repo (100 menos 15 por cada issue
Alta, 5 por Media y 2 por Baja), no del diplomado.

Deps: solo stdlib.
"""
import argparse
import csv
import io
import json
import re
import sys
import unicodedata
from urllib.parse import urlparse

FILE_EXT = (".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".pdf", ".css", ".js",
            ".xml", ".json", ".zip", ".mp4", ".ico", ".woff", ".woff2")
TECH_PATHS = ("/tag/", "/etiqueta/", "/author/", "/autor/", "/wp-json", "/feed", "/page/",
              "/cart", "/carrito", "/checkout", "/gracias", "/thank", "/wp-admin", "/?s=")
STOP = {"de", "del", "la", "el", "los", "las", "un", "una", "para", "en", "y", "con", "por", "a", "al"}

ALIASES = {
    "url": ("url", "address", "direccion", "dirección"),
    "valor": ("valor_seo", "valor seo", "valor", "checklist", "has_value"),
    "keyword": ("keyword", "palabra clave principal", "palabra clave", "kw", "keyword primaria"),
    "temp": ("temperatura", "intencion", "intención", "intent"),
    "vol": ("volumen", "volume"),
    "kd": ("dificultad", "difficulty", "kd"),
    "pos": ("posicion", "posición", "posicion actual", "posición actual", "position"),
    "accion": ("accion", "acción", "plan de accion", "plan de acción", "action"),
}


def out(obj):
    print(json.dumps(obj, ensure_ascii=False))
    sys.exit(0)


def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def norm_kw(s):
    s = strip_accents((s or "").lower())
    toks = [t for t in re.findall(r"[a-z0-9]+", s) if t not in STOP]
    toks = [t[:-2] if len(t) > 5 and t.endswith("es") else (t[:-1] if len(t) > 3 and t.endswith("s") else t)
            for t in toks]
    return " ".join(sorted(set(toks)))


def to_float(v):
    if v in (None, ""):
        return None
    try:
        return float(str(v).replace(",", ".").replace("%", ""))
    except ValueError:
        return None


def pick(row, key):
    low = {strip_accents(str(k)).strip().lower(): v for k, v in row.items()}
    for a in ALIASES[key]:
        k = strip_accents(a).lower()
        if k in low and low[k] not in (None,):
            return str(low[k]).strip()
    return ""


def yes(v):
    return strip_accents(v).strip().lower() in ("si", "sí", "yes", "true", "1", "y", "s")


def no(v):
    return strip_accents(v).strip().lower() in ("no", "false", "0", "n")


def action_kind(a):
    a = strip_accents(a).lower()
    if not a:
        return ""
    if "manten" in a or "conserv" in a:
        return "mantener"
    if "unific" in a or "redirec" in a or "fusion" in a:
        return "unificar"
    if "elimin" in a or "borrar" in a:
        return "eliminar"
    if "actualiz" in a or "optimiz" in a:
        return "actualizar"
    return "otra"


def load(raw, fmt):
    s = raw.strip()
    if not s:
        raise ValueError("entrada vacia")
    if fmt == "json" or (fmt == "auto" and s[0] in "[{"):
        obj = json.loads(s)
        if isinstance(obj, dict):
            obj = obj.get("rows") or obj.get("data") or [obj]
        return [r for r in obj if isinstance(r, dict)]
    rd = csv.DictReader(io.StringIO(raw))
    if not rd.fieldnames:
        raise ValueError("CSV sin cabecera")
    return list(rd)


def main():
    ap = argparse.ArgumentParser(
        description="Valida la calidad de un Mapa de Palabras Clave (criterios de la Semana 5).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Ejemplo:\n  python3 validar_mapa.py --file mapa.csv",
    )
    ap.add_argument("--file", default="-", help="CSV o JSON del mapa ('-' = stdin).")
    ap.add_argument("--format", choices=["auto", "csv", "json"], default="auto")
    ap.add_argument("--top-pos", type=float, default=3, help="Posición máxima para 'Mantener' (default 3).")
    try:
        args = ap.parse_args()
    except SystemExit as e:
        if e.code == 0:
            raise
        out({"ok": False, "reason": "argumentos invalidos: usa --file mapa.csv"})

    try:
        raw = sys.stdin.read() if args.file == "-" else open(args.file, encoding="utf-8-sig").read()
        rows = load(raw, args.format)
    except (OSError, ValueError, json.JSONDecodeError, csv.Error) as e:
        out({"ok": False, "reason": f"entrada invalida: {e}"})

    issues = []

    def add(sev, url, kw, msg, fix):
        issues.append({"id": len(issues) + 1, "severity": sev, "url": url, "keyword": kw,
                       "message": msg, "fix": fix})

    seen_urls = {}
    kw_urls = {}
    with_value = without_value = complete = 0

    for r in rows:
        url = pick(r, "url")
        if not url:
            continue
        low = url.lower()
        valor = pick(r, "valor")
        kw = pick(r, "keyword")
        temp = strip_accents(pick(r, "temp")).lower()
        pos = to_float(pick(r, "pos"))
        act = action_kind(pick(r, "accion"))

        if url in seen_urls:
            add("Media", url, kw, "URL duplicada en el inventario.", "Deja una sola fila por URL.")
        seen_urls[url] = True

        path = low.split("?")[0]
        if path.endswith(FILE_EXT):
            add("Baja", url, kw, "El inventario incluye un archivo o imagen, no una página.",
                "Filtra el inventario a URLs de contenido (Vero: descarta imágenes y archivos).")
            continue
        if any(t in low for t in TECH_PATHS) and yes(valor):
            add("Media", url, kw, "Página técnica (etiqueta, autor, paginación, carrito) marcada con valor SEO.",
                "Márcala Valor SEO = No y sin keyword; las etiquetas de WordPress son listados automáticos.")
        if "?" in low and yes(valor):
            add("Baja", url, kw, "URL con parámetros marcada con valor SEO.",
                "Trabaja la versión limpia y revisa canonical; los parámetros son asunto técnico.")
        if re.search(r"[A-Z]", urlparse(url).path):
            add("Baja", url, kw, "La ruta tiene mayúsculas.", "Usa rutas en minúsculas y sin tildes.")

        if yes(valor):
            with_value += 1
            if not kw:
                add("Alta", url, kw, "URL con valor SEO sin keyword primaria.",
                    "Asigna UNA keyword (1:1) validando en Google que lo que rankea coincide con lo que ofreces.")
            else:
                kw_urls.setdefault(norm_kw(kw), []).append((url, kw))
                if temp and temp not in ("baja", "media", "alta"):
                    add("Baja", url, kw, f"Temperatura no válida: '{temp}'.", "Usa Baja, Media o Alta.")
                if not temp:
                    add("Baja", url, kw, "Falta la temperatura (intención).", "Clasifica Baja, Media o Alta.")
                if pos is None and pick(r, "pos") == "":
                    add("Baja", url, kw, "Falta la posición actual.",
                        "Anota la posición o 0 si no está posicionada; no la inventes.")
                if kw and pick(r, "vol") == "":
                    add("Baja", url, kw, "Falta el volumen (pendiente de dato).",
                        "Trae el dato de DinoRank, Ahrefs o GSC; si no hay, déjalo como pendiente.")
            if kw and act:
                complete += 1
        elif no(valor):
            without_value += 1
            if kw:
                add("Media", url, kw, "URL sin valor SEO con keyword asignada.",
                    "Quita la keyword: las páginas sin valor no se optimizan.")
            if act in ("actualizar",):
                add("Media", url, kw, "URL sin valor SEO marcada para Actualizar/Optimizar.",
                    "Cámbiala a Mantener (sin keyword) o Eliminar/Redireccionar si ensucia el rastreo.")
        else:
            add("Media", url, kw, "Valor SEO sin definir (Sí/No).",
                "Aplica la pregunta test: ¿un usuario buscaría esto en Google?")

        if yes(valor):
            if not act:
                add("Media", url, kw, "Falta el plan de acción.",
                    "Elige Actualizar/Optimizar, Eliminar/Redireccionar o Mantener (y Unificar si fusionas).")
            elif pos is not None:
                if act == "mantener" and pos > args.top_pos:
                    add("Media", url, kw, f"Mantener con posición {pos:g}: no está en el top {args.top_pos:g}.",
                        "Si está en 4 a 20, Actualizar/Optimizar; Mantener solo para top 3.")
                if act != "mantener" and 0 < pos <= args.top_pos and act in ("actualizar",):
                    add("Baja", url, kw, f"Optimizar una URL en posición {pos:g} (top {args.top_pos:g}).",
                        "Mantén y no la toques por inercia, salvo que el contenido esté desactualizado.")

    for key, items in kw_urls.items():
        if len(items) > 1:
            urls = [u for u, _ in items]
            add("Alta", " | ".join(urls), items[0][1],
                f"Keyword repetida o casi repetida en {len(items)} URLs (canibalización planificada).",
                "Deja una URL por keyword (1:1): reasigna la débil a otra keyword o únela con 301 a la fuerte.")

    sev = {"Alta": 0, "Media": 0, "Baja": 0}
    for i in issues:
        sev[i["severity"]] += 1
    score = max(0, 100 - 15 * sev["Alta"] - 5 * sev["Media"] - 2 * sev["Baja"])
    order = {"Alta": 0, "Media": 1, "Baja": 2}
    issues.sort(key=lambda i: (order[i["severity"]], i["id"]))
    out({"ok": True, "issues": issues,
         "summary": {"rows": len(seen_urls), "with_value": with_value, "without_value": without_value,
                     "by_severity": sev,
                     "completeness_pct": round(100 * complete / with_value) if with_value else None,
                     "map_score": score}})


if __name__ == "__main__":
    main()
