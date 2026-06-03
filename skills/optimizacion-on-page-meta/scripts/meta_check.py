#!/usr/bin/env python3
"""
meta_check.py — Valida metatítulo y metadescripción según las reglas del diploma
"De Cero a SEO": metatítulo con keyword al inicio y 50-60 caracteres;
metadescripción de 120-155 caracteres con CTA.

Determinista: cuenta caracteres y posición de keyword sin LLM (ahorra tokens,
precisión exacta).

Usage:
    python3 meta_check.py --title "..." --desc "..." --keyword "..."

JSON output (stdout):
    {
      "ok": true,
      "title": {"len": N, "in_range_50_60": bool, "keyword_at_start": bool},
      "desc":  {"len": N, "in_range_120_155": bool, "has_cta_hint": bool,
                "keyword_present": bool},
      "warnings": [ ... ]
    }
On error: {"ok": false, "reason": "..."} (exit 0). Errors also go to stderr.

Deps: stdlib only.
"""
import argparse
import json
import re
import sys

# Pistas de CTA habituales en español (y la flecha → muy usada en metas).
CTA_HINTS = [
    "descarga", "descubre", "aprende", "lee", "mira", "conoce", "empieza",
    "comienza", "prueba", "consigue", "obtén", "reserva", "compra", "regístrate",
    "suscríbete", "únete", "ver más", "saber más", "haz clic", "entra", "visita",
    "→", "›", "»", "👉",
]


def normalize(s: str) -> str:
    """Minúsculas + colapsa espacios para comparar palabras de forma estable."""
    return re.sub(r"\s+", " ", s.strip().lower())


def keyword_at_start(title: str, keyword: str) -> bool:
    """True si el título empieza por la keyword (ignorando mayúsculas/espacios)."""
    t = normalize(title)
    k = normalize(keyword)
    if not k:
        return False
    return t.startswith(k)


def keyword_present(text: str, keyword: str) -> bool:
    t = normalize(text)
    k = normalize(keyword)
    return bool(k) and k in t


def has_cta_hint(desc: str) -> bool:
    d = normalize(desc)
    return any(h in d for h in CTA_HINTS)


def main() -> int:
    p = argparse.ArgumentParser(
        description="Valida metatítulo y metadescripción (reglas del diploma).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Ejemplo:\n  python3 meta_check.py --title "Guía SEO 2026" --desc "Aprendé SEO..." --keyword "seo"',
    )
    p.add_argument("--title", required=True, help="Metatítulo a validar.")
    p.add_argument("--desc", required=True, help="Metadescripción a validar.")
    p.add_argument("--keyword", required=True, help="Keyword principal.")
    try:
        args = p.parse_args()
    except SystemExit:
        print(json.dumps({"ok": False, "reason": "argumentos invalidos: se requieren --title, --desc, --keyword"}))
        return 0

    title = args.title
    desc = args.desc
    keyword = args.keyword

    title_len = len(title)
    desc_len = len(desc)

    t_in_range = 50 <= title_len <= 60
    t_kw_start = keyword_at_start(title, keyword)
    d_in_range = 120 <= desc_len <= 155
    d_cta = has_cta_hint(desc)
    d_kw = keyword_present(desc, keyword)

    warnings = []
    if not t_in_range:
        if title_len < 50:
            warnings.append(f"Metatítulo corto ({title_len} car.): apunta a 50-60.")
        else:
            warnings.append(f"Metatítulo largo ({title_len} car.): Google lo cortará; recorta a 50-60.")
    if not t_kw_start:
        warnings.append("La keyword no está al inicio del metatítulo (va al inicio para más peso y CTR).")
    if not d_in_range:
        if desc_len < 120:
            warnings.append(f"Metadescripción corta ({desc_len} car.): apunta a 120-155.")
        else:
            warnings.append(f"Metadescripción larga ({desc_len} car.): se truncará; recorta a 120-155.")
    if not d_cta:
        warnings.append("La metadescripción no parece incluir un CTA (descubre, descarga, → ...).")
    if not d_kw:
        warnings.append("La keyword no aparece en la metadescripción.")

    out = {
        "ok": True,
        "title": {
            "len": title_len,
            "in_range_50_60": t_in_range,
            "keyword_at_start": t_kw_start,
        },
        "desc": {
            "len": desc_len,
            "in_range_120_155": d_in_range,
            "has_cta_hint": d_cta,
            "keyword_present": d_kw,
        },
        "warnings": warnings,
    }
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
