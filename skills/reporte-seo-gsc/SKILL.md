---
name: reporte-seo-gsc
description: Usa esta skill cuando haya que redactar el informe SEO mensual para un cliente a partir de las 4 métricas de Google Search Console (clics, impresiones, CTR, posición promedio), según el método del diploma "De Cero a SEO" (aprendoseo). Convierte datos de GSC en un informe ejecutivo mes vs mes con interpretación de negocio, no en una tabla cruda. Úsala al cierre de mes o cuando el cliente pida resultados — aunque no diga "reporte", p.ej. "arma el informe mensual de SEO para el cliente", "¿cómo venimos este mes?", "justifica el trabajo SEO", "pásame los resultados de Search Console".
compatibility: Script opcional requiere Python 3 (uv). GSC vía mcp-gsc (GRATIS), Ahrefs MCP (pago) o SerpApi (apoyo) — todos opcionales; funciona pegando el export CSV de GSC.
metadata:
  author: aprendoseo
  milestone: SEO skills (De Cero a SEO)
  version: "1.0"
---

# Reporte SEO Mensual desde GSC (Diploma W12)

Actúa como consultor SEO en aprendoseo que reporta a un cliente. El cliente no quiere datos: quiere **entender qué pasó y qué sigue**. Traduce las métricas a **valor de negocio** con tono ejecutivo.

> **Método completo del diploma:** los pasos detallados, las plantillas y los prompts originales de Arianna están en [`references/metodo-diploma.md`](references/metodo-diploma.md). Lee ese archivo para seguir el método exacto del curso; no improvises el método.

## Cuándo usar

- **Cierre de mes** (informe recurrente al cliente).
- El cliente **pide resultados** o justificación del trabajo.
- Necesitas detectar y explicar **cambios de rendimiento** orgánico.

## Entradas (qué te doy)

- **Datos de GSC** del periodo (mes actual) y del **mes anterior** para comparar.
- Si no hay MCP: el **export de GSC** (CSV/captura) pegado — la skill lo interpreta.
- **Tareas realizadas** en el mes (de Trello/Plantilla Master).
- Contexto del negocio: objetivos, páginas/keywords clave.

## Datos (MCP opcional)

Funciona **sin MCP**: tú pegas el export de GSC y la skill lo interpreta y redacta.

1. **Sin MCP (manual — principal si no hay conexión):** exporta de GSC las 4 métricas (Clics, Impresiones, CTR, Posición promedio) para el mes y el mes anterior; pega la tabla y la skill la analiza y redacta el informe.
1. **MCP de GSC `mcp-gsc` (GRATIS, comunitario):** trae clics/impresiones/CTR/posición e inspección de URLs en vivo directamente desde Search Console (ver `../../MCP-SETUP.md`); sin MCP se usa el export CSV de GSC (y el script `gsc_report.py`).
2. **Ahrefs MCP (PAGO — GSC conectado):** lectura directa con `mcp__claude_ai_Ahrefs__gsc-performance-history` (evolución), `...gsc-keywords` (keywords ganadoras/perdedoras), `...gsc-pages` (páginas), `...gsc-keyword-history` (histórico de una keyword). Ahrefs es de pago y requiere GSC conectado.
3. **SerpApi MCP (GRATIS — apoyo):** `mcp__serpapi__search` para contextualizar la SERP de una keyword que se movió (qué cambió arriba).

Config de MCP: ver `../../MCP-SETUP.md`.

## Proceso

1. **Reúne las 4 métricas de GSC** del mes vs mes anterior: **Clics, Impresiones, CTR, Posición promedio**.
2. **Calcula la variación** (% y absoluto) de cada métrica.
3. **Interpreta el patrón** (clave del diploma):
   - Impresiones ↑ + Clics ↓ → **problema de CTR / Meta Title** (revisar metas → usar `optimizacion-on-page-meta`).
   - Posición ↑ (mejora) + Clics ↑ → estrategia funcionando.
   - Impresiones ↓ → pérdida de visibilidad/cobertura (revisar técnica → `auditoria-tecnica`).
4. **Identifica keywords y páginas ganadoras** (las que más subieron).
5. **Lista tareas realizadas** y enmárcalas en su impacto.
6. **Define próximos pasos** accionables.
7. **Redacta en tono ejecutivo**, traduciendo todo a valor de negocio.

## Salida

Informe mensual en formato **Doc**, con esta estructura del diploma:

1. **Resumen Ejecutivo** (3-4 frases: qué pasó y qué significa para el negocio).
2. **Análisis de Rendimiento Orgánico** — tabla **mes vs mes** con las 4 métricas + interpretación.
3. **Keywords y Páginas Ganadoras**.
4. **Tareas Realizadas y Próximos Pasos**.

Además: **tabla mes vs mes** lista para pegar y **vínculo a Trello** para las tareas/próximos pasos.

## Ejemplo

**Resumen ejecutivo:** "En mayo el tráfico orgánico creció un 18% en clics pese a un ligero descenso en posición media, gracias a la mejora de CTR tras reescribir los metatítulos de la sección Blog. Recomendamos extender esa optimización a Producto."

**Rendimiento (mes vs mes):**

| Métrica | Abril | Mayo | Var. |
|---|---|---|---|
| Clics | 4.120 | 4.860 | +18% |
| Impresiones | 210k | 235k | +12% |
| CTR | 1,96% | 2,07% | +0,11 pp |
| Posición media | 14,2 | 14,9 | -0,7 |

**Lectura:** impresiones y clics suben juntos y el CTR mejora → la optimización de metas funciona aunque la posición media bajó levemente por nuevas keywords de cola larga entrando en el rango.

**Keywords ganadoras:** "auditoría seo técnica" (pos. 8→4), "qué es link equity" (nuevo, pos. 11).

## Script determinista (ahorro de tokens)

Si Python 3 está disponible, **ejecuta el script** para comparar mes vs. mes desde los exports de GSC: calcula deltas y aplica las reglas de interpretación del diploma de forma determinista, ahorrando tokens y evitando errores de aritmética.

Ejecuta (cero instalación, resuelve deps solo):

```
uv run skills/reporte-seo-gsc/scripts/gsc_report.py --current mayo.csv --previous abril.csv
# o, si no usas uv: python3 skills/reporte-seo-gsc/scripts/gsc_report.py --current mayo.csv --previous abril.csv
# nº de ganadores/perdedores a listar:
uv run skills/reporte-seo-gsc/scripts/gsc_report.py --current cur.csv --previous prev.csv --top 15
```

Corre con `--help` para ver opciones. Salida: `{"ok":true,"totals":{"clicks":{"cur","prev","delta_pct"},"impressions":{...},"ctr":{...},"position":{...}},"winners":[...],"losers":[...],"insights":[...]}` (p.ej. *"impresiones ↑ + clics ↓ → problema de CTR/Meta Title"*). Solo stdlib. Si falla devuelve `{"ok":false,"reason":...}` (exit 0) → **modo manual**: calcula deltas y aplica las reglas a mano. Exporta el informe de Rendimiento de GSC con columnas Query/Page, Clicks, Impressions, CTR, Position.

## Gotchas

- Interpreta: **impresiones ↑ + clics ↓ = problema de CTR / metatítulo, no de posicionamiento** (interpretación estrella del diploma → revisar metas con `optimizacion-on-page-meta`).
- GSC da **4 métricas: clics, impresiones, CTR y posición promedio** — no inventes otras ni mezcles con datos de Analytics.
- Compara **mes vs mes en UTC, sobre las mismas fechas**; no compares un mes con festivos/estacionalidad distinta sin avisarlo.
- El reporte es **para el cliente: ejecutivo y en valor de negocio, no un volcado de métricas** ni una tabla cruda de GSC.
- **Posición media que empeora ≠ mal resultado**: puede bajar al entrar keywords nuevas de cola larga; crúzala siempre con clics/impresiones.
- Cierra con **próximos pasos accionables vinculados a Trello**, no con un párrafo genérico.
