---
name: proyeccion-seo-gsc
description: Usa esta skill cuando el usuario quiera saber qué resultados podría tener si cumple el plan SEO, o comparar lo planeado con lo real, aunque no diga "proyección", p.ej. "cuántos clics puedo esperar si hago todo el plan", "en cuánto tiempo voy a rankear", "cuánto tráfico traería subir esta página al top 5", "cómo le explico al cliente qué esperar", "el plan va bien o mal frente a lo que dijimos", "compara lo proyectado contra Search Console". Calcula con los datos REALES de Search Console (clics, impresiones, CTR, posición) tres escenarios en rangos, con supuestos explícitos y editables, y se niega a proyectar si faltan datos. Seguimiento mensual plan vs real que alimenta reporte-seo-gsc. Proyección no es garantía.
compatibility: Script Python 3 solo con stdlib (proyeccion_gsc.py). Requiere exports CSV de Search Console (mensual, consultas y páginas) o datos equivalentes; GSC por MCP o Ahrefs gsc-* son opcionales. Sin datos suficientes no proyecta.
metadata:
  author: aprendoseo
  milestone: SEO skills (De Cero a SEO)
  version: "1.0"
---

> **🚫 Regla de datos (obligatoria): NUNCA inventes números.**
> No estimes, supongas ni inventes métricas o datos que no tengas: volumen de búsqueda, dificultad/KD, clics, impresiones, CTR, posición, tráfico, Core Web Vitals, backlinks, fechas, precios, etc. Si te falta un dato, **pídeselo al usuario y espera su respuesta**, que lo pegue a mano, lo exporte (Google Search Console, Ahrefs, DinoRank, Screaming Frog…) o lo conecte por MCP. Da igual de dónde venga, pero tiene que venir de una fuente real. Si aun así no hay dato, márcalo explícitamente como `pendiente de dato` y NO continúes como si lo tuvieras. Un entregable con huecos honestos vale más que uno con cifras inventadas.


> **📊 Cierre en dashboard.** Cuando trabajes sobre un sitio, además de tu entrega persiste tu salida estructurada en `.seo-audit/<sitio>/data/proyeccion-gsc.json` (esquema en la skill `dashboard-seo`). Al cerrar el flujo SEO, genera/actualiza el dashboard con `dashboard-seo` y entrega el URL local. Tus archivos: `proyeccion-gsc.json` y `seguimiento-proyeccion.json`.

# Proyección SEO con Search Console y seguimiento plan vs real

Actúa como **Analista SEO en aprendoseo**. El diplomado enseña a medir con las 4 métricas de Search Console (clics, impresiones, CTR, posición, Semanas 3 y 12) y a controlar expectativas del cliente (Semana 16, manejo de clientes). Esta skill añade una extensión que pidió el proyecto: estimar un **rango** de resultados "si se cumple el plan" y vigilarlo mes a mes. **Es una extensión de este repositorio, no un método del diplomado**, y se apoya en el plan de `plan-seo`.

> **Proyección no es garantía.** Se entrega como rango con supuestos visibles. Nunca como un número único ni como promesa. Si el cliente la toma como compromiso, explícale qué supone cada escenario.

> **Método y fórmulas:** [`references/metodo.md`](references/metodo.md). Fundamento en el diplomado: [`references/metodo-diploma.md`](references/metodo-diploma.md).

## Cuándo usar

- Hay un plan (`content-map.json` de `plan-seo`) y Search Console con historial.
- Hay que explicar al cliente qué esperar y en cuánto tiempo.
- Pasaron semanas desde la publicación y hay que comparar lo real con lo proyectado (alimenta `reporte-seo-gsc`).

No sirve para sitios sin Search Console o con menos de 3 meses de datos: el script lo rechaza y dice qué falta.

## Entradas

- `--mensual`: export de Search Console por mes o por día con Fecha, Clics, Impresiones, CTR y Posición. Mínimo 3 meses completos; **12 a 16 meses** para detectar estacionalidad.
- `--consultas`: export por consulta. Con él se calcula la **curva de CTR por posición de la propia web**. Exige muestra mínima (por defecto 500 impresiones y 3 consultas por posición).
- `--paginas`: export por página, línea base de las páginas a actualizar.
- `--mapa`: `content-map.json` con acción, mes de publicación y, solo para páginas nuevas, el **volumen que el usuario aporte desde su herramienta** (Ahrefs, DinoRank, Planificador). Search Console no tiene datos de keywords que aún no posicionas.
- `--supuestos`: JSON opcional para cambiar los escenarios.
- `--curva-generica`: JSON opcional, solo si la web no tiene muestra suficiente. Se rotula como **SUPUESTO DEL USUARIO**, nunca como dato. Hay un ejemplo de relleno en `evals/fixtures/curva-generica-ejemplo.json`.

## Pasos

1. **Reúne los exports** de GSC (o pídelos). Con MCP de GSC o `gsc-performance-history`, `gsc-pages` y `gsc-keywords` de Ahrefs puedes traerlos; si no hay conexión, el usuario los exporta. Nunca estimes.
2. **Corre la proyección:**

```bash
python3 scripts/proyeccion_gsc.py proyectar --mensual gsc-mensual.csv --consultas gsc-consultas.csv \
  --paginas gsc-paginas.csv --mapa .seo-audit/<sitio>/data/content-map.json --sitio <sitio>
```

3. **Si se niega a proyectar**, entrega al usuario la lista de lo que falta (`faltan` en la salida). No intentes completar con estimaciones.
4. **Lee el resultado en rangos:** línea base real (promedio de 3 meses, desestacionalizada si hay 12 o más), curva de CTR y su origen, tres escenarios (conservador, base, optimista) con `cumplimiento`, `posicion_objetivo` y `meses_maduracion`, y `rango_por_mes` (mínimo, base, máximo). Las páginas sin dato aparecen en `paginas_sin_dato` y no suman clics.
5. **Presenta los supuestos primero**, el rango después. Pregunta al usuario si quiere editarlos (`--supuestos`) y vuelve a correr. Muestra la fórmula si el cliente la pide.
6. **Seguimiento mensual:**

```bash
python3 scripts/proyeccion_gsc.py seguimiento --proyeccion .seo-audit/<sitio>/data/proyeccion-gsc.json \
  --real gsc-mes-nuevo.csv --sitio <sitio>
```

   Devuelve por mes: real, mínimo, base, máximo, desvío contra el base y estado (dentro del rango, por debajo del conservador, por encima del optimista). Antes de culpar al algoritmo, revisa si el plan se cumplió (páginas publicadas frente al mapa). Usa las filas como bloque "plan vs real" en `reporte-seo-gsc`.
7. **Cierre.** Persiste `proyeccion-gsc.json` y `seguimiento-proyeccion.json` y entrega el dashboard con `dashboard-seo`.

## Salida

```
PROYECCIÓN (no es garantía) · Línea base: [clics/mes real, meses usados]
Curva de CTR: [origen: real o SUPUESTO]
Escenario | Cumplimiento | Pos. objetivo | Maduración | Rango de clics a 6 y 12 meses
Páginas sin dato: [lista y motivo]
Supuestos a revisar: [lista]
Seguimiento: mes | real | rango | estado
```

## Reglas

- Solo datos reales de Search Console para la línea base, el CTR actual y la curva. Lo demás son supuestos rotulados.
- Volumen de búsqueda y KD no vienen de GSC: si el usuario no los tiene, las páginas nuevas quedan `pendiente de dato` y no suman.
- Nunca un número único ni un porcentaje de crecimiento sin rango y sin supuestos.
- Rechaza con menos de 3 meses o sin muestra para la curva (a menos que el usuario acepte explícitamente una curva genérica como supuesto suyo).
- La estacionalidad con un solo año de historial es un supuesto a revisar, no una ley.

## Complementos opcionales (claude-seo)

Después del método, [`references/complementos-claude-seo.md`](references/complementos-claude-seo.md) explica qué ofrece claude-seo (reportes con datos de Google y planificación de keywords) y por qué no se importó ninguna proyección.

## Gotchas

- Un mes parcial al final del export diario infla o deprime la base: el script lo descarta si tiene muy pocas filas.
- Impresiones suben y clics bajan: problema de CTR o de Meta Title, no de la proyección (regla del informe mensual, Semana 12).
- Poner la posición objetivo en 1 casi siempre produce cifras irreales: apunta a posiciones que tu propia curva respalda.
- Una página que ya está en el top 3 casi no tiene recorrido: el script resta su CTR actual real y no suma nada si ya supera el objetivo.
