#!/usr/bin/env python3
"""
readability.py — Analiza la legibilidad y la optimización on-page de un artículo
en español (heurísticas del diploma "De Cero a SEO": frases cortas, párrafos
cortos, densidad y colocación de la keyword).

Determinista: conteos y densidad por regex, sin LLM (ahorra tokens, precisión).
Acepta Markdown o texto plano.

Usage:
    python3 readability.py --keyword "..." --file ruta/al/articulo.md
    cat articulo.md | python3 readability.py --keyword "..." --file -

JSON output (stdout):
    {
      "ok": true,
      "word_count": N,
      "sentence_count": N,
      "avg_sentence_words": x,
      "long_sentences": N,            # frases > 25 palabras
      "paragraphs": N,
      "keyword_density_pct": x,
      "keyword_in_first_100_words": bool,
      "headings": {"h1": N, "h2": N, "h3": N, "h4": N, "h5": N, "h6": N},
      "flags": [ ... ]
    }
On error: {"ok": false, "reason": "..."} (exit 0). Errors también a stderr.

Deps: stdlib only.
"""
import argparse
import json
import re
import sys

LONG_SENTENCE_WORDS = 25
MAX_PARAGRAPH_WORDS = 150  # párrafo largo según heurística de legibilidad


def read_input(path: str) -> str:
    if path == "-" or path is None:
        return sys.stdin.read()
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def count_headings(text: str) -> dict:
    """Cuenta encabezados Markdown (# .. ######) y HTML (<h1>..<h6>)."""
    h = {f"h{i}": 0 for i in range(1, 7)}
    for line in text.splitlines():
        m = re.match(r"^(#{1,6})\s+\S", line)
        if m:
            h[f"h{len(m.group(1))}"] += 1
    for i in range(1, 7):
        h[f"h{i}"] += len(re.findall(rf"<h{i}\b", text, flags=re.IGNORECASE))
    return h


def strip_markup(text: str) -> str:
    """Quita marcas Markdown/HTML básicas para el análisis de prosa."""
    t = re.sub(r"<[^>]+>", " ", text)              # tags HTML
    t = re.sub(r"^#{1,6}\s+", "", t, flags=re.MULTILINE)  # encabezados md
    t = re.sub(r"[*_`>#-]{1,}", " ", t)            # énfasis / viñetas / citas
    t = re.sub(r"!\?\[[^\]]*\]\([^)]*\)", " ", t)  # imágenes
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t) # enlaces -> texto
    return t


def split_words(text: str) -> list:
    return re.findall(r"[0-9A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+", text)


def split_sentences(text: str) -> list:
    parts = re.split(r"(?<=[.!?…])\s+|\n{2,}", text)
    return [s.strip() for s in parts if s.strip()]


def split_paragraphs(text: str) -> list:
    parts = re.split(r"\n\s*\n", text.strip())
    return [p.strip() for p in parts if p.strip()]


def normalize(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower())


def count_keyword_occurrences(words_lower: list, keyword: str) -> int:
    """Cuenta ocurrencias de la keyword (uni o multipalabra) como secuencia."""
    k = split_words(normalize(keyword))
    if not k:
        return 0
    n = len(k)
    if n == 1:
        return sum(1 for w in words_lower if w == k[0])
    count = 0
    for i in range(len(words_lower) - n + 1):
        if words_lower[i:i + n] == k:
            count += 1
    return count


def main() -> int:
    p = argparse.ArgumentParser(
        description="Analiza legibilidad y on-page de un artículo en español.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Ejemplo:\n  python3 readability.py --keyword "seo" --file articulo.md\n  cat articulo.md | python3 readability.py --keyword "seo"',
    )
    p.add_argument("--keyword", required=True, help="Keyword principal.")
    p.add_argument("--file", default="-", help="Ruta del artículo (md o txt). '-' o omitir = stdin.")
    try:
        args = p.parse_args()
    except SystemExit:
        print(json.dumps({"ok": False, "reason": "argumentos invalidos: se requiere --keyword (y --file o stdin)"}))
        return 0

    try:
        raw = read_input(args.file)
    except OSError as e:
        print(f"error leyendo archivo: {e}", file=sys.stderr)
        print(json.dumps({"ok": False, "reason": f"no se pudo leer el archivo: {args.file}"}))
        return 0

    if not raw.strip():
        print(json.dumps({"ok": False, "reason": "entrada vacia"}))
        return 0

    headings = count_headings(raw)
    paragraphs = split_paragraphs(raw)

    prose = strip_markup(raw)
    words = split_words(prose)
    words_lower = [w.lower() for w in words]
    word_count = len(words)

    sentences = split_sentences(prose)
    sentence_count = len(sentences)

    sentence_word_counts = [len(split_words(s)) for s in sentences]
    long_sentences = sum(1 for c in sentence_word_counts if c > LONG_SENTENCE_WORDS)
    avg_sentence_words = round(word_count / sentence_count, 2) if sentence_count else 0.0

    kw_occurrences = count_keyword_occurrences(words_lower, args.keyword)
    keyword_density_pct = round((kw_occurrences / word_count) * 100, 2) if word_count else 0.0

    first_100 = words_lower[:100]
    kw_in_first_100 = count_keyword_occurrences(first_100, args.keyword) > 0

    long_paragraphs = sum(1 for para in paragraphs if len(split_words(strip_markup(para))) > MAX_PARAGRAPH_WORDS)

    flags = []
    if avg_sentence_words > 20:
        flags.append(f"Frases promedio largas ({avg_sentence_words} palabras): apunta a ~15-20.")
    if long_sentences:
        flags.append(f"{long_sentences} frase(s) con más de {LONG_SENTENCE_WORDS} palabras: divídelas.")
    if long_paragraphs:
        flags.append(f"{long_paragraphs} párrafo(s) muy largos (> {MAX_PARAGRAPH_WORDS} palabras): trocea.")
    if kw_occurrences == 0:
        flags.append("La keyword no aparece en el cuerpo.")
    elif keyword_density_pct > 2.5:
        flags.append(f"Densidad de keyword alta ({keyword_density_pct}%): riesgo de keyword stuffing, baja de 2.5%.")
    elif keyword_density_pct < 0.5:
        flags.append(f"Densidad de keyword baja ({keyword_density_pct}%): refuerza de forma natural.")
    if not kw_in_first_100:
        flags.append("La keyword no aparece en las primeras 100 palabras.")
    if headings["h1"] == 0:
        flags.append("No se detectó H1.")
    elif headings["h1"] > 1:
        flags.append(f"Hay {headings['h1']} H1: debe haber solo uno.")
    if headings["h2"] == 0 and word_count > 300:
        flags.append("No hay H2: usa subtítulos para estructurar el contenido.")

    out = {
        "ok": True,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "avg_sentence_words": avg_sentence_words,
        "long_sentences": long_sentences,
        "paragraphs": len(paragraphs),
        "keyword_density_pct": keyword_density_pct,
        "keyword_in_first_100_words": kw_in_first_100,
        "headings": headings,
        "flags": flags,
    }
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
