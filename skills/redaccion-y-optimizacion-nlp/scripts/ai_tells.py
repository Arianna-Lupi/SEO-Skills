#!/usr/bin/env python3
"""
ai_tells.py: detector de marcas de texto genérico de IA en español (complemento externo, adaptado).

Apoya el paso "Humanizar" de la Semana 11 ("la IA propone, tú validas"). NO decide si un
texto fue escrito por IA: señala frases de relleno, aperturas típicas, estructuras repetidas
y afirmaciones con cifras sin fuente, para que la persona las edite. Ningún detector es
infalible: la revisión final es humana.

Revisa:
  - Frases de relleno y muletillas típicas de borrador de IA (lista editable abajo).
  - Rayas largas y medias (U+2014 y U+2013): señal visual frecuente, el repo pide comas o dos puntos.
  - Aperturas repetidas: muchas frases seguidas que empiezan con la misma palabra.
  - Cifras o estudios sin fuente cercana (enlace, "según X", nota).
  - Parrafos y frases largas (>25 palabras).
  - Si pasas --keyword: repetición de la keyword exacta por cada 100 palabras (alerta de relleno).

Uso:
  python3 ai_tells.py --file articulo.md [--keyword "x"] [--out .seo-audit/<sitio>/data/ai-tells.json]
Solo stdlib.
"""
import argparse
import json
import re
import sys
from collections import Counter

FRASES = [
    "en el mundo actual", "en la era digital", "en el vertiginoso mundo", "hoy en día", "en conclusión",
    "es importante destacar", "cabe destacar", "cabe mencionar", "es fundamental", "sin lugar a dudas",
    "en el panorama actual", "a lo largo de este artículo", "en este artículo exploraremos",
    "sumérgete", "desbloquea", "potencia tu", "lleva tu", "un abanico de", "un sinfín de", "te invito a",
    "en resumen", "no es ningún secreto", "el camino hacia", "navegar por", "un tapiz", "juega un papel crucial",
    "juega un papel fundamental", "es un testimonio de", "ya sea que", "ya seas",
]
CONTEO_CITA = re.compile(r"(\[[^\]]+\]\(https?://|\[\^?\d+\]|según [A-ZÁÉÍÓÚ]|de acuerdo con [A-ZÁÉÍÓÚ]|https?://|fuente:)")
CIFRA = re.compile(r"(\b\d{1,3}(?:[.,]\d+)?\s?%|\b\d+\s?(?:millones|mil millones|veces)\b|\bestudio\b|\binvestigaci[oó]n\b)", re.I)


def main():
    ap = argparse.ArgumentParser(description="Marcas de texto genérico de IA en español.")
    ap.add_argument("--file", required=True, help="Ruta (.md/.txt) o '-' para stdin")
    ap.add_argument("--keyword")
    ap.add_argument("--out")
    a = ap.parse_args()
    try:
        text = sys.stdin.read() if a.file == "-" else open(a.file, encoding="utf-8").read()
    except Exception as e:  # noqa: BLE001
        print(json.dumps({"ok": False, "reason": str(e), "fallback": "modo manual: lee en voz alta y marca lo genérico"}))
        return 0
    plano = re.sub(r"```.*?```", " ", text, flags=re.S)
    plano = re.sub(r"^#{1,6}\s.*$", " ", plano, flags=re.M)
    low = plano.lower()
    palabras = re.findall(r"\w+", plano, flags=re.U)
    flags = []

    for f in FRASES:
        n = low.count(f)
        if n:
            flags.append({"tipo": "relleno", "sev": "media" if n > 1 else "baja", "msg": f"'{f}' aparece {n} vez/veces: reescribe con un dato o ejemplo concreto"})

    n_raya = len(re.findall("[\u2014\u2013]", text))
    if n_raya:
        flags.append({"tipo": "rayas", "sev": "baja", "msg": f"{n_raya} raya(s) larga(s) o media(s): sustituye por coma, dos puntos o paréntesis"})

    frases = [s.strip() for s in re.split(r"(?<=[.!?¿?])\s+", plano) if len(s.split()) >= 3]
    largas = [s for s in frases if len(s.split()) > 25]
    if largas:
        flags.append({"tipo": "frases_largas", "sev": "baja", "msg": f"{len(largas)} frase(s) de más de 25 palabras", "ejemplo": largas[0][:140]})

    ini = Counter(s.split()[0].lower() for s in frases if s.split())
    for palabra, n in ini.most_common(3):
        if len(frases) >= 8 and n / len(frases) > 0.25:
            flags.append({"tipo": "aperturas_repetidas", "sev": "media", "msg": f"{n} de {len(frases)} frases empiezan con '{palabra}': varía el ritmo"})

    sin_fuente = []
    for s in frases:
        if CIFRA.search(s) and not CONTEO_CITA.search(s):
            sin_fuente.append(s[:120])
    if sin_fuente:
        flags.append({"tipo": "afirmaciones_sin_fuente", "sev": "alta", "msg": f"{len(sin_fuente)} frase(s) con cifra o estudio sin fuente cercana: añade la fuente primaria o elimina el dato (no inventes cifras)", "ejemplos": sin_fuente[:3]})

    kw_info = None
    if a.keyword and palabras:
        n = low.count(a.keyword.lower())
        por100 = round(n * 100 / len(palabras), 2)
        kw_info = {"apariciones_exactas": n, "por_cada_100_palabras": por100}
        if n >= 6 and por100 > 1.5:
            flags.append({"tipo": "keyword", "sev": "media", "msg": f"La keyword exacta aparece {n} veces ({por100} por 100 palabras): prioriza entidades y sinónimos, no repetición"})

    res = {"ok": True, "palabras": len(palabras), "frases": len(frases), "keyword": kw_info, "flags": flags,
           "nota": "Heurística de apoyo. La validación final es humana; no es un veredicto de autoría."}
    out = json.dumps(res, ensure_ascii=False, indent=2)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(out)
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
