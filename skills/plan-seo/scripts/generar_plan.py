#!/usr/bin/env python3
"""Genera el Plan SEO por meses a partir de hallazgos (observacion, detalle, accion).

Método del diploma "De Cero a SEO" (Semana 2, lecciones 5 y 14): cada observación
termina en una tarea con verbo; el plan se reparte en Mes 1 (bases), Mes 2
(contenido), Mes 3 (autoridad y publicación) y Mes 4 (análisis).

Entrada (JSON):
  {"objetivo": "...", "hallazgos": [
     {"observacion": "...", "detalle": "...", "accion": "Corregir ...",
      "area": "tecnica|estrategia|contenido|autoridad|conversion",
      "prioridad": "Alta|Media|Baja", "horas": 2, "responsable": "..."}]}

Salida (stdout, JSON): {"ok": true, "plan": [...], "avisos": [...]}
Con --sitio escribe .seo-audit/<sitio>/data/next-steps.json y plan-seo.json.
Con --md escribe una tabla Markdown lista para la Plantilla Master.
Solo stdlib. Nunca inventa horas ni fechas: lo que falta queda "pendiente de dato".
"""
import argparse
import json
import os
import sys
import unicodedata

VERBOS = (
    "agregar anadir actualizar analizar asignar auditar completar configurar corregir crear "
    "definir disenar documentar eliminar enlazar escribir implementar instalar investigar "
    "medir mejorar migrar optimizar publicar redactar redirigir reclamar registrar reparar "
    "revisar solicitar subir validar verificar comprimir consolidar construir presentar "
    "preparar reportar priorizar ordenar reducir reescribir reunir reemplazar habilitar "
    "ajustar bloquear desindexar indexar duplicar enviar generar identificar incluir "
    "mapear monitorear planificar probar quitar resolver simplificar sustituir traducir"
).split()

AREA_MES = {"tecnica": 1, "estrategia": 1, "conversion": 2, "contenido": 2, "autoridad": 3}
PRIO_ORDEN = {"alta": 0, "media": 1, "baja": 2}
AREA_ORDEN = {"tecnica": 0, "estrategia": 1, "conversion": 2, "contenido": 3, "autoridad": 4}


def sin_acentos(texto):
    return "".join(c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn")


def empieza_con_verbo(accion):
    primera = sin_acentos(accion.strip().split(" ")[0].lower()) if accion.strip() else ""
    # Infinitivo (-ar, -er, -ir) o imperativo habitual; aceptamos la lista y las terminaciones.
    return primera in VERBOS or primera.endswith(("ar", "er", "ir"))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("entrada", help="JSON con objetivo y hallazgos")
    ap.add_argument("--sitio", help="Dominio; si se da, escribe .seo-audit/<sitio>/data/*.json")
    ap.add_argument("--horas-semana", type=float, help="Horas disponibles por semana (para avisar de sobrecarga)")
    ap.add_argument("--md", help="Ruta de salida Markdown")
    ap.add_argument("--raiz", default=".", help="Raíz donde vive .seo-audit (por defecto, cwd)")
    args = ap.parse_args()

    try:
        with open(args.entrada, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError) as exc:
        print(json.dumps({"ok": False, "reason": f"No se pudo leer la entrada: {exc}",
                          "fallback": "modo manual: usa la tabla de references/plantillas.md"}, ensure_ascii=False))
        return 0

    hallazgos = data.get("hallazgos", [])
    avisos, plan = [], []
    for i, h in enumerate(hallazgos, 1):
        accion = (h.get("accion") or "").strip()
        area = sin_acentos((h.get("area") or "estrategia").lower())
        prio = (h.get("prioridad") or "Media").capitalize()
        if not accion:
            avisos.append(f"Hallazgo {i}: sin acción. Un hallazgo sin acción no entra al plan.")
            continue
        if not empieza_con_verbo(accion):
            avisos.append(f"Hallazgo {i}: la acción debe empezar con verbo: '{accion[:40]}'")
        if area not in AREA_MES:
            avisos.append(f"Hallazgo {i}: área '{area}' desconocida, se usa 'estrategia'.")
            area = "estrategia"
        horas = h.get("horas")
        plan.append({
            "id": i, "mes": AREA_MES[area], "area": area, "prioridad": prio,
            "observacion": h.get("observacion", ""), "detalle": h.get("detalle", ""),
            "tarea": accion, "responsable": h.get("responsable") or "pendiente de dato",
            "fecha": h.get("fecha") or "pendiente de dato",
            "horas": horas if isinstance(horas, (int, float)) else "pendiente de dato",
            "entregable": h.get("entregable") or "pendiente de dato",
        })

    # Técnica primero, luego prioridad, luego área (regla del diploma).
    plan.sort(key=lambda t: (t["mes"], PRIO_ORDEN.get(t["prioridad"].lower(), 1), AREA_ORDEN[t["area"]]))

    if args.horas_semana:
        for mes in sorted({t["mes"] for t in plan}):
            total = sum(t["horas"] for t in plan if t["mes"] == mes and isinstance(t["horas"], (int, float)))
            if total > args.horas_semana * 4:
                avisos.append(f"Mes {mes}: {total} h estimadas superan {args.horas_semana * 4:.0f} h disponibles. Mueve tareas al mes siguiente.")

    resultado = {"ok": True, "objetivo": data.get("objetivo", "pendiente de dato"), "plan": plan, "avisos": avisos}

    if args.sitio:
        carpeta = os.path.join(args.raiz, ".seo-audit", args.sitio, "data")
        os.makedirs(carpeta, exist_ok=True)
        esfuerzo = lambda t: "pendiente de dato" if t["horas"] == "pendiente de dato" else f'{t["horas"]} h'
        pasos = [{"prio": t["prioridad"], "area": t["area"], "action": t["tarea"],
                  "impact": t["detalle"] or t["observacion"], "effort": esfuerzo(t)} for t in plan]
        with open(os.path.join(carpeta, "next-steps.json"), "w", encoding="utf-8") as fh:
            json.dump({"steps": pasos}, fh, ensure_ascii=False, indent=2)
        with open(os.path.join(carpeta, "plan-seo.json"), "w", encoding="utf-8") as fh:
            json.dump(resultado, fh, ensure_ascii=False, indent=2)

    if args.md:
        nombres = {1: "Mes 1, bases y estrategia", 2: "Mes 2, producción de contenido",
                   3: "Mes 3, autoridad y publicación", 4: "Mes 4, análisis de resultados"}
        lineas = [f"# Plan SEO\n\nObjetivo: {resultado['objetivo']}\n"]
        for mes in sorted({t["mes"] for t in plan} | {4}):
            lineas.append(f"\n## {nombres[mes]}\n")
            if mes == 4 and not any(t["mes"] == 4 for t in plan):
                lineas.append("- Reportar resultados del plan con `reporte-seo-gsc` y revisar objetivos.\n")
                continue
            lineas.append("| Área | Tarea | Prioridad | Responsable | Fecha | Horas | Entregable |\n|---|---|---|---|---|---|---|")
            for t in (x for x in plan if x["mes"] == mes):
                lineas.append(f"| {t['area']} | {t['tarea']} | {t['prioridad']} | {t['responsable']} | {t['fecha']} | {t['horas']} | {t['entregable']} |")
        with open(args.md, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lineas) + "\n")

    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
