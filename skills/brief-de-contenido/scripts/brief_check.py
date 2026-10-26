#!/usr/bin/env python3
"""
brief_check.py: valida un brief de contenido ya redactado (Markdown o texto).

Comprueba, de forma determinista, lo que el diplomado exige en el brief
(Semana 8, lecciones 4, 5 y 6):
  - Meta título 50 a 60 caracteres, con la keyword al inicio.
  - Meta descripción 120 a 155 caracteres, con CTA.
  - Un solo H1, con la keyword, y sin saltos de nivel (H2 a H4 prohibido).
  - Presencia de los bloques mínimos: intención, benchmark, enlaces internos.
  - Opcional: bloques extra según el tipo (--tipo blog|landing|ecommerce|optimizacion).

NOTA: no uses "# " para el título del documento (contaría como H1); usa texto plano.
Formatos de encabezado que reconoce:  "# Título", "## Título" o "H1: texto", "H2: texto".
Metas: busca líneas con "meta título", "metatítulo" o "meta descripción" y toma el
texto entre comillas, o lo que viene después de los dos puntos / barra vertical.

Uso:
  python3 brief_check.py --file brief.md --keyword "sérum vitamina c natural" [--tipo blog]
  cat brief.md | python3 brief_check.py --file - --keyword "..."

Salida: JSON a stdout. Si falla, {"ok": false, "reason": ...} con exit 0.
Solo stdlib.
"""
import argparse
import json
import re
import sys

CTA_HINTS = (
    "descubre", "aprende", "conoce", "compra", "solicita", "pide", "reserva", "cotiza",
    "descarga", "empieza", "comienza", "prueba", "llama", "contacta", "agenda", "elige",
    "ahorra", "mira", "lee", "visita", "consulta", "hoy", "ya", "ahora", "gratis",
)
EXTRA = {
    "blog": ["visual", "enlace"],
    "landing": ["above the fold", "prueba social", "cta"],
    "ecommerce": ["atributo", "reseña", "urgencia", "cross"],
    "optimizacion": ["actual", "sugerido", "conserva", "url"],
}


def norm(s):
    return re.sub(r"\s+", " ", s.strip().lower())


def extract_meta(text, labels):
    """Devuelve el primer texto de meta encontrado para alguna de las etiquetas."""
    for line in text.splitlines():
        low = line.lower()
        if any(l in low for l in labels):
            q = re.search(r"[\"“«]([^\"”»]{5,})[\"”»]", line)
            if q:
                return q.group(1).strip()
            parts = re.split(r"[:|]", line, maxsplit=1)
            if len(parts) == 2:
                cand = re.sub(r"\[.*?\]|\(\d+\s*c\)", "", parts[1]).strip(" *`_|")
                if cand and not cand.startswith("-"):
                    return cand
    return None


def extract_headings(text):
    out = []
    for line in text.splitlines():
        m = re.match(r"^\s*(#{1,6})\s+(.+)$", line)
        if m:
            out.append((len(m.group(1)), m.group(2).strip()))
            continue
        m = re.match(r"^\s*[-*]?\s*H([1-6])\s*[:\-]\s*(.+)$", line)
        if m:
            out.append((int(m.group(1)), m.group(2).strip()))
    return out


def main():
    ap = argparse.ArgumentParser(description="Valida un brief de contenido (metas, jerarquía, bloques).")
    ap.add_argument("--file", required=True, help="Ruta al brief (.md/.txt) o '-' para stdin")
    ap.add_argument("--keyword", required=True, help="Keyword principal")
    ap.add_argument("--tipo", choices=sorted(EXTRA), help="Tipo de brief para validar bloques extra")
    a = ap.parse_args()
    try:
        text = sys.stdin.read() if a.file == "-" else open(a.file, encoding="utf-8").read()
    except Exception as e:  # noqa: BLE001
        print(json.dumps({"ok": False, "reason": str(e), "fallback": "modo manual: cuenta caracteres con un simulador de SERP"}))
        return 0

    kw = norm(a.keyword)
    flags = []
    title = extract_meta(text, ("meta título", "metatítulo", "meta titulo", "metatitulo"))
    desc = extract_meta(text, ("meta descripción", "metadescripción", "meta descripcion", "metadescripcion"))

    t = {"texto": title, "len": len(title) if title else None}
    if not title:
        flags.append({"sev": "alta", "msg": "Falta el meta título: un brief sin meta título está incompleto."})
    else:
        t["en_rango_50_60"] = 50 <= len(title) <= 60
        t["keyword_al_inicio"] = norm(title).startswith(kw) or norm(title)[: len(kw) + 12].find(kw) != -1
        if not t["en_rango_50_60"]:
            flags.append({"sev": "media", "msg": f"Meta título de {len(title)} caracteres, el rango es 50 a 60."})
        if not t["keyword_al_inicio"]:
            flags.append({"sev": "media", "msg": "La keyword no está al inicio del meta título."})

    d = {"texto": desc, "len": len(desc) if desc else None}
    if not desc:
        flags.append({"sev": "alta", "msg": "Falta la meta descripción."})
    else:
        d["en_rango_120_155"] = 120 <= len(desc) <= 155
        d["tiene_cta"] = any(h in norm(desc) for h in CTA_HINTS)
        if not d["en_rango_120_155"]:
            flags.append({"sev": "media", "msg": f"Meta descripción de {len(desc)} caracteres, el rango es 120 a 155."})
        if not d["tiene_cta"]:
            flags.append({"sev": "baja", "msg": "La meta descripción no muestra un CTA claro."})

    heads = extract_headings(text)
    h1s = [h for lvl, h in heads if lvl == 1]
    jumps = []
    prev = None
    for lvl, h in heads:
        if prev is not None and lvl > prev + 1:
            jumps.append(f"salto de H{prev} a H{lvl}: {h[:60]}")
        prev = lvl
    if len(h1s) != 1:
        flags.append({"sev": "alta", "msg": f"Debe haber un solo H1; se encontraron {len(h1s)}."})
    elif kw not in norm(h1s[0]):
        flags.append({"sev": "media", "msg": "El H1 no contiene la keyword principal completa."})
    for j in jumps:
        flags.append({"sev": "alta", "msg": "Jerarquía rota, " + j})
    kw_h2 = [h for lvl, h in heads if lvl == 2 and kw in norm(h)]
    if len([1 for lvl, _ in heads if lvl == 2]) >= 4 and len(kw_h2) > len([1 for lvl, _ in heads if lvl == 2]) / 2:
        flags.append({"sev": "baja", "msg": "La keyword completa se repite en más de la mitad de los H2: varía con sinónimos."})

    low = norm(text)
    bloques = {
        "intencion": "intenci" in low,
        "benchmark": "benchmark" in low or "top 3" in low,
        "enlaces_internos": "enlace" in low and ("anchor" in low or "ancla" in low),
    }
    for k, ok in bloques.items():
        if not ok:
            flags.append({"sev": "media", "msg": f"Falta el bloque obligatorio: {k.replace('_', ' ')}."})
    if a.tipo:
        for k in EXTRA[a.tipo]:
            if k not in low:
                flags.append({"sev": "media", "msg": f"Para el tipo {a.tipo} falta mencionar: {k}."})

    print(json.dumps({"ok": True, "keyword": a.keyword, "meta_titulo": t, "meta_descripcion": d,
                      "encabezados": [f"H{l}: {h}" for l, h in heads], "h1": h1s,
                      "bloques": bloques, "flags": flags, "aprobado": not any(f["sev"] == "alta" for f in flags)},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
