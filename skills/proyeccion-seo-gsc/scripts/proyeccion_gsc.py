#!/usr/bin/env python3
"""Proyección de resultados SEO con Search Console (rangos, supuestos explícitos) y seguimiento plan vs real.

NO es una promesa: es un cálculo con la fórmula visible. Se apoya solo en datos reales de la propia web
(Search Console: clics, impresiones, CTR, posición) y en supuestos que TÚ editas y que quedan listados.
Se niega a proyectar cuando faltan datos y dice cuáles.

Subcomando `proyectar`
  --mensual   CSV de GSC por mes o por día (Fecha/Date/Mes, Clicks, Impressions, CTR, Position). Mínimo 3 meses
              completos; con 12 o más meses se calcula un índice de estacionalidad.
  --consultas CSV de GSC por consulta (Query, Clicks, Impressions, CTR, Position). Sirve para calcular la CURVA DE
              CTR POR POSICIÓN de la propia web. Se exige muestra mínima por posición (--min-impresiones).
  --paginas   CSV de GSC por página (Page, Clicks, Impressions, CTR, Position): línea base de páginas a actualizar.
  --mapa      content-map.json del plan (páginas, acción, mes, posición, volumen si lo aportaste).
  --supuestos JSON opcional que sobrescribe los escenarios (ver references/metodo.md).
  --curva-generica JSON opcional {"1":0.x,...}: SOLO si la web no tiene muestra suficiente; se rotula SUPUESTO.
Fórmulas (visibles en la salida):
  página existente  : clics_mes = impresiones_mes_página × (CTR(pos_objetivo) − CTR_actual_real) × cumplimiento × madurez(t)
  página nueva      : clics_mes = volumen_aportado × CTR(pos_objetivo) × cumplimiento × madurez(t)   (solo si aportaste volumen)
  madurez(t)        : rampa lineal de 0 a 1 entre el mes de publicación y publicación + meses_maduración
  total proyectado  : línea_base × estacionalidad(mes) + Σ clics incrementales
Salida: JSON a stdout y, con --sitio, .seo-audit/<sitio>/data/proyeccion-gsc.json.

Subcomando `seguimiento`
  --proyeccion proyeccion-gsc.json --real CSV mensual real: compara mes a mes contra el rango conservador a optimista.

Solo stdlib.
"""
import argparse
import csv
import datetime as dt
import json
import os
import re
import statistics
import sys

PEND = "pendiente de dato"
ESCENARIOS_DEF = {  # SUPUESTOS EDITABLES, no son datos. Cámbialos con --supuestos.
    "conservador": {"cumplimiento": 0.6, "posicion_objetivo": 10, "meses_maduracion": 6},
    "base": {"cumplimiento": 0.8, "posicion_objetivo": 5, "meses_maduracion": 4},
    "optimista": {"cumplimiento": 1.0, "posicion_objetivo": 3, "meses_maduracion": 3},
}


def salir(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2))
    sys.exit(0)


def rechazar(razon, falta):
    salir({"ok": False, "reason": razon, "faltan": falta, "nota": "El script se niega a proyectar sin esos datos para no inventar cifras."})


def f(x):
    if x is None or str(x).strip() == "":
        return None
    s = str(x).strip().replace("%", "").replace(" ", "")
    if "," in s and "." not in s:
        s = s.replace(",", ".")
    else:
        s = s.replace(",", "")
    try:
        return float(s)
    except ValueError:
        return None


def leer(ruta):
    with open(ruta, encoding="utf-8-sig", newline="") as fh:
        muestra = fh.read(4096)
        fh.seek(0)
        try:
            d = csv.Sniffer().sniff(muestra, delimiters=",;\t")
        except csv.Error:
            d = csv.excel
        return list(csv.DictReader(fh, dialect=d))


def col(fila, *nombres):
    bajos = {k.lower().strip(): k for k in fila}
    for n in nombres:
        if n in bajos:
            return fila[bajos[n]]
    return None


def mes_de(txt):
    t = str(txt).strip()
    m = re.match(r"(\d{4})[-/](\d{1,2})", t)
    if m:
        return "%s-%02d" % (m.group(1), int(m.group(2)))
    for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%b %Y", "%B %Y"):
        try:
            return dt.datetime.strptime(t, fmt).strftime("%Y-%m")
        except ValueError:
            continue
    return None


def serie_mensual(ruta):
    acc = {}
    for r in leer(ruta):
        m = mes_de(col(r, "fecha", "date", "mes", "month", "fechas", "día", "dia") or "")
        c, i, p = f(col(r, "clics", "clicks", "clics totales")), f(col(r, "impresiones", "impressions")), f(col(r, "posición", "posicion", "position", "posición media"))
        if not m or c is None or i is None:
            continue
        a = acc.setdefault(m, {"clics": 0.0, "impresiones": 0.0, "pos_pond": 0.0, "dias": 0})
        a["clics"] += c
        a["impresiones"] += i
        a["pos_pond"] += (p or 0) * i
        a["dias"] += 1
    out = []
    for m in sorted(acc):
        a = acc[m]
        out.append({"mes": m, "clics": a["clics"], "impresiones": a["impresiones"],
                    "ctr": a["clics"] / a["impresiones"] if a["impresiones"] else None,
                    "posicion": a["pos_pond"] / a["impresiones"] if a["impresiones"] and a["pos_pond"] else None, "filas": a["dias"]})
    return out


def sumar_meses(m, n):
    y, mm = int(m[:4]), int(m[5:])
    t = y * 12 + (mm - 1) + n
    return "%d-%02d" % (t // 12, t % 12 + 1)


def curva_ctr(ruta_consultas, min_imp):
    """CTR real por posición redondeada (1..10) ponderado por impresiones, solo con muestra suficiente."""
    b = {}
    for r in leer(ruta_consultas):
        c, i, p = f(col(r, "clics", "clicks")), f(col(r, "impresiones", "impressions")), f(col(r, "posición", "posicion", "position"))
        if None in (c, i, p) or p < 0.5 or p >= 10.5:
            continue
        k = int(round(p))
        x = b.setdefault(k, {"c": 0.0, "i": 0.0, "n": 0})
        x["c"] += c
        x["i"] += i
        x["n"] += 1
    curva, descartadas = {}, []
    for k in range(1, 11):
        x = b.get(k)
        if x and x["i"] >= min_imp and x["n"] >= 3:
            curva[k] = x["c"] / x["i"]
        else:
            descartadas.append({"posicion": k, "impresiones": x["i"] if x else 0, "consultas": x["n"] if x else 0})
    return curva, descartadas


def ctr_en(curva, pos):
    """Interpolación lineal sobre las posiciones con dato; fuera del rango usa el extremo."""
    ks = sorted(curva)
    if not ks:
        return None
    if pos <= ks[0]:
        return curva[ks[0]]
    if pos >= ks[-1]:
        return curva[ks[-1]]
    for a, b in zip(ks, ks[1:]):
        if a <= pos <= b:
            return curva[a] + (curva[b] - curva[a]) * (pos - a) / (b - a)
    return None


def madurez(t, maduracion):
    """t = meses desde publicación (0 = mes de publicación)."""
    if t < 0:
        return 0.0
    return min(1.0, t / float(max(1, maduracion)))


def cmd_proyectar(a):
    if not a.mensual:
        rechazar("Falta el export mensual de Search Console.", ["--mensual (CSV con fecha, clics, impresiones, CTR, posición)"])
    serie = serie_mensual(a.mensual)
    # El último mes puede venir incompleto: se descarta si tiene muchos menos días que el anterior (export diario).
    if len(serie) >= 2 and serie[-1]["filas"] < 0.7 * serie[-2]["filas"] and serie[-2]["filas"] > 1:
        serie = serie[:-1]
    if len(serie) < 3:
        rechazar("Hay menos de 3 meses completos de historial en Search Console (%d)." % len(serie),
                 ["al menos 3 meses; idealmente 12 a 16 para detectar estacionalidad"])
    supuestos = json.loads(open(a.supuestos, encoding="utf-8").read()) if a.supuestos else {}
    esc = {k: {**ESCENARIOS_DEF[k], **(supuestos.get(k) or {})} for k in ESCENARIOS_DEF}

    # Línea base: promedio de los últimos 3 meses completos.
    ult = serie[-3:]
    base_clics = statistics.mean(x["clics"] for x in ult)
    base_imp = statistics.mean(x["impresiones"] for x in ult)
    estacional = {}
    est_nota = "Sin estacionalidad: hay menos de 12 meses de historial."
    if len(serie) >= 12:
        ventana = serie[-12:]
        xs = list(range(len(ventana)))
        mx, my = statistics.mean(xs), statistics.mean(x["clics"] for x in ventana)
        den = sum((x - mx) ** 2 for x in xs) or 1.0
        pend = sum((x - mx) * (v["clics"] - my) for x, v in zip(xs, ventana)) / den
        por_mes = {}
        for x, v in zip(xs, ventana):
            tendencia = my + pend * (x - mx)
            por_mes.setdefault(v["mes"][5:], []).append(v["clics"] / tendencia if tendencia > 0 else 1.0)
        estacional = {k: statistics.mean(v) for k, v in por_mes.items()}
        est_nota = ("Índice de estacionalidad por mes calendario: clics del mes / tendencia lineal de 12 meses (así el crecimiento no se confunde con estacionalidad). "
                    "Con un solo año el patrón puede ser coincidencia; tómalo como supuesto a revisar.")
        # La línea base se des-estacionaliza para no arrastrar el pico o valle de los últimos 3 meses.
        base_clics = statistics.mean(x["clics"] / (estacional.get(x["mes"][5:]) or 1.0) for x in ult)

    # Curva de CTR por posición.
    curva, descartadas, origen_curva = {}, [], None
    if a.consultas:
        curva, descartadas = curva_ctr(a.consultas, a.min_impresiones)
        origen_curva = "real: calculada de las consultas de tu Search Console"
    if len(curva) < 3:
        if a.curva_generica:
            g = json.loads(open(a.curva_generica, encoding="utf-8").read())
            curva = {int(k): float(v) for k, v in g.items() if k.isdigit()}
            origen_curva = "SUPUESTO DEL USUARIO (curva genérica de %s): no es un dato de tu web. Reemplázala cuando tengas muestra." % a.curva_generica
        else:
            rechazar("La web no tiene muestra suficiente para calcular su propia curva de CTR por posición (menos de 3 posiciones con %d impresiones y 3 consultas)." % a.min_impresiones,
                     ["--consultas con más consultas/impresiones por posición, o --curva-generica <json> aceptando que es un supuesto"])

    mapa = (json.load(open(a.mapa, encoding="utf-8")) if a.mapa else {}).get("pages", [])
    paginas_gsc = {}
    if a.paginas:
        for r in leer(a.paginas):
            u = col(r, "página", "pagina", "page", "páginas principales", "top pages")
            c, i, p = f(col(r, "clics", "clicks")), f(col(r, "impresiones", "impressions")), f(col(r, "posición", "posicion", "position"))
            if u and None not in (c, i, p):
                paginas_gsc[u.strip().rstrip("/")] = {"clics": c, "impresiones": i, "posicion": p}
    meses_periodo = max(1, min(a.meses_paginas or len(serie), len(serie)))

    inicio = a.inicio or sumar_meses(serie[-1]["mes"], 1)
    horizonte = a.horizonte
    meses = [sumar_meses(inicio, i) for i in range(horizonte)]
    detalle_paginas, sin_dato = [], []
    for p in mapa:
        if p.get("accion") not in ("Actualizar", "Crear"):
            continue
        n_mes = int(re.sub(r"\D", "", str(p.get("mes", ""))) or 0)
        if not n_mes:
            sin_dato.append({"url": p.get("url"), "motivo": "sin mes de publicación en el mapa"})
            continue
        pub = sumar_meses(inicio, n_mes - 1)
        if p.get("accion") == "Actualizar":
            g = paginas_gsc.get((p.get("url") or "").rstrip("/"))
            if not g:
                sin_dato.append({"url": p.get("url"), "motivo": "página a actualizar sin fila en --paginas (no hay línea base real)"})
                continue
            base = {"tipo": "existente", "impresiones_mes": g["impresiones"] / meses_periodo,
                    "ctr_actual": g["clics"] / g["impresiones"] if g["impresiones"] else 0.0, "posicion_actual": g["posicion"]}
        else:
            vol = f(p.get("volumen"))
            if vol is None:
                sin_dato.append({"url": p.get("url"), "motivo": "página nueva sin volumen aportado: GSC no tiene datos de keywords que aún no posicionas (%s)" % PEND})
                continue
            base = {"tipo": "nueva", "volumen_mes": vol}
        detalle_paginas.append({"url": p.get("url"), "keyword": p.get("keyword"), "publicacion": pub, **base})

    resultado_esc = {}
    for nombre, s in esc.items():
        ctr_obj = ctr_en(curva, s["posicion_objetivo"])
        filas = []
        for m in meses:
            inc = 0.0
            for pg in detalle_paginas:
                t = (int(m[:4]) * 12 + int(m[5:])) - (int(pg["publicacion"][:4]) * 12 + int(pg["publicacion"][5:]))
                mad = madurez(t, s["meses_maduracion"])
                if pg["tipo"] == "existente":
                    delta = max(0.0, ctr_obj - pg["ctr_actual"]) if ctr_obj is not None else 0.0
                    inc += pg["impresiones_mes"] * delta * s["cumplimiento"] * mad
                else:
                    inc += pg["volumen_mes"] * (ctr_obj or 0.0) * s["cumplimiento"] * mad
            est = estacional.get(m[5:], 1.0) if estacional else 1.0
            filas.append({"mes": m, "base": round(base_clics * est, 1), "incremental": round(inc, 1), "total": round(base_clics * est + inc, 1)})
        resultado_esc[nombre] = {"supuestos": s, "ctr_objetivo": round(ctr_obj, 4) if ctr_obj is not None else None, "meses": filas}

    rangos = [{"mes": m, "minimo": resultado_esc["conservador"]["meses"][i]["total"], "base": resultado_esc["base"]["meses"][i]["total"],
               "maximo": resultado_esc["optimista"]["meses"][i]["total"]} for i, m in enumerate(meses)]
    out = {
        "ok": True,
        "advertencia": "Proyección NO es garantía. Es un rango calculado con supuestos explícitos y editables. Mide siempre con las 4 métricas de Search Console (clics, impresiones, CTR, posición).",
        "linea_base": {"clics_mes": round(base_clics, 1), "impresiones_mes": round(base_imp, 1), "meses_usados": [x["mes"] for x in ult],
                       "historial_meses": len(serie), "estacionalidad": est_nota},
        "curva_ctr": {"origen": origen_curva, "valores": {str(k): round(v, 4) for k, v in sorted(curva.items())}, "posiciones_sin_muestra": descartadas},
        "formulas": ["página existente: clics_mes = impresiones_mes × (CTR(pos_objetivo) − CTR_actual_real) × cumplimiento × madurez(t)",
                     "página nueva: clics_mes = volumen_aportado × CTR(pos_objetivo) × cumplimiento × madurez(t)",
                     "madurez(t) = min(1, t / meses_maduración); total = base × estacionalidad + Σ incrementales"],
        "escenarios": resultado_esc, "rango_por_mes": rangos,
        "paginas_incluidas": detalle_paginas, "paginas_sin_dato": sin_dato,
        "supuestos_a_revisar": ["cumplimiento del plan, posición objetivo y meses de maduración por escenario (editables con --supuestos)",
                                "las páginas nuevas sin volumen aportado NO suman clics (%s)" % PEND]}
    if a.sitio:
        carpeta = os.path.join(a.raiz, ".seo-audit", a.sitio, "data")
        os.makedirs(carpeta, exist_ok=True)
        with open(os.path.join(carpeta, "proyeccion-gsc.json"), "w", encoding="utf-8") as fh:
            json.dump(out, fh, ensure_ascii=False, indent=2)
    salir(out)


def cmd_seguimiento(a):
    proy = json.load(open(a.proyeccion, encoding="utf-8"))
    if not proy.get("ok"):
        rechazar("La proyección de entrada no es válida.", ["un proyeccion-gsc.json generado por `proyectar`"])
    real = {x["mes"]: x for x in serie_mensual(a.real)}
    filas, ins = [], []
    for r in proy["rango_por_mes"]:
        x = real.get(r["mes"])
        if not x:
            filas.append({"mes": r["mes"], "real": PEND, "estado": "sin dato real todavía"})
            continue
        if x["clics"] < r["minimo"]:
            est = "por debajo del rango conservador"
        elif x["clics"] > r["maximo"]:
            est = "por encima del rango optimista"
        else:
            est = "dentro del rango"
        filas.append({"mes": r["mes"], "real": round(x["clics"], 1), "minimo": r["minimo"], "base": r["base"], "maximo": r["maximo"],
                      "desvio_vs_base_pct": round((x["clics"] - r["base"]) / r["base"] * 100, 1) if r["base"] else None, "estado": est,
                      "impresiones_reales": round(x["impresiones"], 1), "ctr_real": round(x["ctr"], 4) if x["ctr"] is not None else None})
    medidos = [f_ for f_ in filas if f_.get("real") != PEND]
    if medidos:
        ult = medidos[-1]
        ins.append("%s: clics reales %s, %s (rango %s a %s)." % (ult["mes"], ult["real"], ult["estado"], ult["minimo"], ult["maximo"]))
        if ult["estado"].startswith("por debajo"):
            ins.append("Revisa primero si el plan se cumplió (páginas publicadas vs mapa) antes de culpar al algoritmo; luego impresiones vs CTR (regla del reporte mensual).")
    out = {"ok": True, "seguimiento": filas, "insights": ins, "nota": "Alimenta reporte-seo-gsc: usa estas filas como 'plan vs real'."}
    if a.sitio:
        carpeta = os.path.join(a.raiz, ".seo-audit", a.sitio, "data")
        os.makedirs(carpeta, exist_ok=True)
        with open(os.path.join(carpeta, "seguimiento-proyeccion.json"), "w", encoding="utf-8") as fh:
            json.dump(out, fh, ensure_ascii=False, indent=2)
    salir(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("proyectar", help="Proyecta clics en tres escenarios")
    p.add_argument("--mensual")
    p.add_argument("--consultas")
    p.add_argument("--paginas")
    p.add_argument("--mapa")
    p.add_argument("--supuestos")
    p.add_argument("--curva-generica")
    p.add_argument("--min-impresiones", type=int, default=500, help="Impresiones mínimas por posición para fiarse de su CTR (por defecto 500)")
    p.add_argument("--meses-paginas", type=int, help="Meses que cubre el export de --paginas (por defecto, los del historial mensual)")
    p.add_argument("--inicio", help="Primer mes proyectado AAAA-MM (por defecto, el mes siguiente al último dato)")
    p.add_argument("--horizonte", type=int, default=12)
    p.add_argument("--sitio")
    p.add_argument("--raiz", default=".")
    s = sub.add_parser("seguimiento", help="Compara proyección vs real")
    s.add_argument("--proyeccion", required=True)
    s.add_argument("--real", required=True)
    s.add_argument("--sitio")
    s.add_argument("--raiz", default=".")
    a = ap.parse_args()
    (cmd_proyectar if a.cmd == "proyectar" else cmd_seguimiento)(a)


if __name__ == "__main__":
    main()
