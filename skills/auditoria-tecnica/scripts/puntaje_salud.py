#!/usr/bin/env python3
"""
puntaje_salud.py: puntaje de salud técnica a partir de issues.json (solo stdlib).

Complemento externo (idea de claude-seo, MIT), NO es método del diplomado. El
diplomado prioriza por severidad y plantilla ("menos es más si es lo correcto");
este puntaje solo sirve para comparar una auditoría con la anterior. No es una
métrica de Google ni un dato real de rendimiento.

Rúbrica (resta desde 100, con tope por severidad para que un solo tipo no hunda todo):
  Crítico 15 c/u (tope 60) | Alto 8 (tope 32) | Medio 3 (tope 18)
  Bajo-Medio 2 (tope 8)    | Bajo 1 (tope 6)
Cuenta una vez por issue (que es por plantilla, no por URL).

Uso:
  python3 puntaje_salud.py .seo-audit/ejemplo.com/data/issues.json
  python3 puntaje_salud.py issues.json --previo issues-anterior.json
Salida JSON: {"ok","score","grade","by_severity","by_block","delta"}
"""
import argparse
import json
import sys

WEIGHTS = {"Crítico": (15, 60), "Alto": (8, 32), "Medio": (3, 18), "Bajo-Medio": (2, 8), "Bajo": (1, 6)}


def score(path):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    issues = data.get("issues", data if isinstance(data, list) else [])
    by_sev, by_block = {}, {}
    for i in issues:
        if str(i.get("status", "")).lower() in ("resuelto", "resolved", "cerrado"):
            continue
        s = i.get("severity", "Bajo")
        by_sev[s] = by_sev.get(s, 0) + 1
        b = str(i.get("block", "sin bloque"))
        by_block[b] = by_block.get(b, 0) + 1
    pen = 0
    for s, n in by_sev.items():
        w, cap = WEIGHTS.get(s, (1, 6))
        pen += min(w * n, cap)
    sc = max(0, 100 - pen)
    grade = "Sana" if sc >= 85 else "Atención" if sc >= 65 else "Deficiente" if sc >= 40 else "Crítica"
    return {"score": sc, "grade": grade, "by_severity": by_sev, "by_block": by_block, "open_issues": sum(by_sev.values())}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("issues", help="issues.json de la auditoría actual")
    ap.add_argument("--previo", help="issues.json de la auditoría anterior para calcular el cambio")
    a = ap.parse_args()
    try:
        out = {"ok": True, **score(a.issues)}
        if a.previo:
            prev = score(a.previo)
            out["previous_score"] = prev["score"]
            out["delta"] = out["score"] - prev["score"]
    except (OSError, ValueError) as e:
        out = {"ok": False, "reason": str(e), "fallback": "modo manual: cuenta los issues abiertos por severidad"}
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
