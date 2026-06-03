#!/usr/bin/env python3
"""
schema_gen.py — Genera y valida JSON-LD de schema.org para los tipos más usados
en SEO (diploma "De Cero a SEO": datos estructurados solo para contenido que
existe y es visible en la página).

Determinista: construye el objeto JSON-LD y comprueba propiedades requeridas
contra un mapa interno, sin LLM (ahorra tokens, evita inventar marcado).

Tipos soportados:
    Article, BlogPosting, Product, FAQPage, HowTo, BreadcrumbList,
    LocalBusiness, Organization, WebSite

Usage:
    python3 schema_gen.py --type Article --field headline="..." --field author="..."
    python3 schema_gen.py --type Product --json '{"name":"X","offers":{...}}'
    cat data.json | python3 schema_gen.py --type FAQPage --json -

JSON output (stdout):
    {
      "ok": true,
      "type": "Article",
      "jsonld": { "@context": "https://schema.org", "@type": "Article", ... },
      "missing_required": [ ... ],
      "warnings": [ ... ]
    }
On error: {"ok": false, "reason": "..."} (exit 0). Errores también a stderr.

Deps: stdlib only.
"""
import argparse
import json
import sys

# Propiedades requeridas y recomendadas por tipo (schema.org / Google Rich Results).
SCHEMA_MAP = {
    "Article": {
        "required": ["headline"],
        "recommended": ["author", "datePublished", "image", "dateModified", "publisher"],
    },
    "BlogPosting": {
        "required": ["headline"],
        "recommended": ["author", "datePublished", "image", "dateModified", "publisher", "mainEntityOfPage"],
    },
    "Product": {
        "required": ["name"],
        "recommended": ["image", "description", "offers", "brand", "aggregateRating", "review", "sku"],
    },
    "FAQPage": {
        "required": ["mainEntity"],
        "recommended": [],
    },
    "HowTo": {
        "required": ["name", "step"],
        "recommended": ["totalTime", "supply", "tool", "image"],
    },
    "BreadcrumbList": {
        "required": ["itemListElement"],
        "recommended": [],
    },
    "LocalBusiness": {
        "required": ["name", "address"],
        "recommended": ["telephone", "openingHours", "geo", "url", "image", "priceRange"],
    },
    "Organization": {
        "required": ["name"],
        "recommended": ["url", "logo", "sameAs", "contactPoint", "description"],
    },
    "WebSite": {
        "required": ["name", "url"],
        "recommended": ["potentialAction", "description", "publisher"],
    },
}


def parse_value(raw: str):
    """Intenta interpretar el valor como JSON (objeto/array/num/bool); si no, string."""
    s = raw.strip()
    if s and s[0] in "[{\"" or s in ("true", "false", "null") or _looks_numeric(s):
        try:
            return json.loads(s)
        except (ValueError, json.JSONDecodeError):
            return raw
    return raw


def _looks_numeric(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False


def read_json_arg(value: str) -> dict:
    data = sys.stdin.read() if value == "-" else value
    obj = json.loads(data)
    if not isinstance(obj, dict):
        raise ValueError("el JSON debe ser un objeto")
    return obj


def main() -> int:
    p = argparse.ArgumentParser(
        description="Genera y valida JSON-LD de schema.org.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Ejemplo:\n  python3 schema_gen.py --type Article --field headline="Mi título" --field author="Ana"',
    )
    p.add_argument("--type", required=True, help="Tipo schema.org soportado.")
    p.add_argument("--field", action="append", default=[], metavar="k=v",
                   help="Par clave=valor (repetible). El valor puede ser JSON.")
    p.add_argument("--json", dest="json_in", default=None,
                   help="Objeto JSON con los campos. '-' = stdin.")
    try:
        args = p.parse_args()
    except SystemExit:
        print(json.dumps({"ok": False, "reason": "argumentos invalidos: se requiere --type (y --field o --json)"}))
        return 0

    stype = args.type
    if stype not in SCHEMA_MAP:
        print(f"tipo no soportado: {stype}", file=sys.stderr)
        print(json.dumps({
            "ok": False,
            "reason": f"tipo no soportado: {stype}. Soportados: {', '.join(SCHEMA_MAP)}",
        }, ensure_ascii=False))
        return 0

    fields = {}
    if args.json_in is not None:
        try:
            fields.update(read_json_arg(args.json_in))
        except (ValueError, json.JSONDecodeError) as e:
            print(f"error parseando --json: {e}", file=sys.stderr)
            print(json.dumps({"ok": False, "reason": f"--json invalido: {e}"}, ensure_ascii=False))
            return 0

    for item in args.field:
        if "=" not in item:
            print(json.dumps({"ok": False, "reason": f"--field debe ser k=v: '{item}'"}, ensure_ascii=False))
            return 0
        k, v = item.split("=", 1)
        fields[k.strip()] = parse_value(v)

    spec = SCHEMA_MAP[stype]

    jsonld = {"@context": "https://schema.org", "@type": stype}
    for k, v in fields.items():
        jsonld[k] = v

    missing_required = [r for r in spec["required"] if r not in fields or fields[r] in ("", None, [], {})]

    warnings = []
    missing_recommended = [r for r in spec["recommended"] if r not in fields]
    if missing_recommended:
        warnings.append("Propiedades recomendadas ausentes: " + ", ".join(missing_recommended) + ".")
    if stype == "FAQPage":
        warnings.append("FAQPage solo si las preguntas/respuestas son VISIBLES en la página; no marques contenido inexistente.")
    if stype == "HowTo":
        warnings.append("HowTo solo si los pasos son visibles en la página; cada 'step' debe existir en el contenido.")
    if stype in ("Article", "BlogPosting") and "publisher" in fields:
        pub = fields["publisher"]
        if isinstance(pub, dict) and "logo" not in pub:
            warnings.append("El 'publisher' debería incluir 'logo' (ImageObject) para Rich Results.")

    out = {
        "ok": True,
        "type": stype,
        "jsonld": jsonld,
        "missing_required": missing_required,
        "warnings": warnings,
    }
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
