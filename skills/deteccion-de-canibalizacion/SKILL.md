---
name: deteccion-de-canibalizacion
description: Usa esta skill cuando haya que diagnosticar canibalización REAL (varias URLs de un sitio ya existente compitiendo hoy por la misma query, con datos de Google Search Console/Ahrefs), no la prevención al armar un mapa nuevo — aunque el usuario no diga "canibalización", p.ej. "por qué no despega esta keyword si tengo contenido bueno", "dos artículos míos aparecen turnándose en Google", "las posiciones suben y bajan sin razón", "¿debería fusionar o redirigir estas dos páginas?", "tengo un export de Search Console con query y página". Agrupa por query, calcula cuánto se reparte el clic entre URLs, clasifica severidad (Alta/Media/Bajo) y recomienda fusionar+301, diferenciar intención o solo monitorear.
compatibility: Script requiere Python 3 (uv), solo stdlib. Datos vía export de GSC (Query+Página) o MCP de GSC/Ahrefs; SerpApi MCP opcional para verificar la SERP en vivo. Funciona 100% manual pegando el export.
metadata:
  author: aprendoseo
  milestone: SEO skills (De Cero a SEO)
  version: "1.0"
---

> **🚫 Regla de datos (obligatoria): NUNCA inventes números.**
> No estimes, supongas ni inventes métricas o datos que no tengas: clics, impresiones, CTR, posición, volumen, dificultad, backlinks, etc. Si te falta un dato, **pídeselo al usuario y espera su respuesta** — que lo pegue a mano, lo exporte (Google Search Console, Ahrefs, DinoRank…) o lo conecte por MCP. Si aun así no hay dato, márcalo explícitamente como `pendiente de dato` y NO continúes como si lo tuvieras.

> **📊 Cierre en dashboard.** Cuando trabajes sobre un sitio, además de tu entrega persiste tu salida estructurada en `.seo-audit/<sitio>/data/issues.json` (esquema en la skill `dashboard-seo`, uno por query canibalizada con `severity`). Al cerrar el flujo SEO, genera/actualiza el dashboard con `dashboard-seo` y entrega el URL local.

# Detección de canibalización (real, con datos de ranking)

Actúa como especialista en canibalización SEO en aprendoseo. Tu trabajo: mirar **qué está pasando de verdad hoy en Google** (no un mapa planeado) y decidir, con datos, si dos o más URLs se están pisando por la misma query.

**Diferencia clave con `mapa-de-palabras-clave`:** esa skill *previene* la canibalización asignando 1 keyword por URL al planificar. Esta skill la *diagnostica* en un sitio que ya existe, cruzando el rendimiento real por query+página (clics, impresiones, posición) — la única forma de confirmar si de verdad hay tráfico repartido o si solo lo parece.

## Cuándo usar

- Sospechas que **dos o más URLs compiten** por la misma búsqueda (Google alterna cuál muestra).
- Una keyword **no despega** pese a tener contenido bueno — puede estar repartida entre varias páginas.
- Vas a decidir si **fusionar, redirigir (301) o diferenciar** dos piezas de contenido similares.
- Antes de un **refresh de contenido** o una migración, para no arrastrar el problema.

Si el sitio todavía no tiene keywords asignadas ni URLs mapeadas, usa primero `mapa-de-palabras-clave`. Para verificar posiciones puntuales en la SERP, apóyate en `analisis-serp-y-competencia`.

## Entradas (qué te doy)

- **Export de Google Search Console** con dimensiones **Query + Página** (Rendimiento → exportar, o pegado a mano): columnas `query, url, clicks, impressions, position`.
- (Opcional) Rango de fechas (últimos 28-90 días recomendado; más días = más señal, menos ruido de variación diaria).
- (Opcional) Lista de URLs sospechosas si ya las identificaste a ojo.

## Datos (MCP opcional)

Funciona **100% manual**: el usuario exporta de GSC (Rendimiento → Páginas Y Consultas, agrupado por ambas dimensiones) y pega la tabla.

- **MCP de GSC por usuario** (`mcp__mcp-hub__gsc-<owner>-get-advanced-search-analytics`, GRATIS): trae clics/impresiones/posición con dimensiones `query` + `page` directo de Search Console, sin exportar a mano.
- **Ahrefs MCP (PAGO — GSC conectado):** `mcp__claude_ai_Ahrefs__gsc-pages` y `...gsc-keywords` para cruzar qué páginas y qué keywords se solapan; `...site-explorer-organic-keywords` por URL para ver el solape de keywords orgánicas entre dos URLs sin depender de GSC.
- **SerpApi MCP (GRATIS):** `mcp__serpapi__search` para confirmar **qué URL muestra Google ahora mismo** en la query sospechosa (a veces GSC promedia semanas y la SERP actual ya cambió cuál gana).

Nunca exijas un MCP. Ver `../../MCP-SETUP.md`.

## Proceso

1. **Consigue el export** de GSC con Query + Página (o usa el MCP de GSC del owner correspondiente). Filtra por sección/carpeta si el sitio es grande.
2. **Ejecuta el script** (`scripts/detectar_canibalizacion.py`) para agrupar por query, calcular cuánto domina la URL líder (`dominance_ratio`) y clasificar severidad.
3. **Lee `cannibalization`**, priorizado por severidad:
   - **Alta** — el clic se reparte de verdad (ninguna URL domina >60%) o las dos están a ≤5 posiciones en el top 20: canibalización real, actuando.
   - **Media** — una URL domina (60-90% del clic) pero la otra sigue robando: riesgo, vale la pena resolver.
   - **Bajo** — dominancia casi total (>90%) o solo impresiones sin clics: probable ruido de cola larga, monitorear.
4. **Verifica en vivo** los casos Alta/Media con `mcp__serpapi__search`: confirma cuál URL rankea hoy y si de verdad son la misma intención de búsqueda o dos ángulos distintos.
5. **Diagnostica la causa** mirando título/H1/contenido de cada URL del grupo:
   - Contenido casi duplicado apuntando a lo mismo → **fusionar + redirigir 301** la débil hacia la fuerte.
   - Intención distinta pero títulos/keywords calcados (p.ej. informativa vs. transaccional) → **diferenciar**: retitular, cambiar keyword objetivo de la débil, reforzar enlazado interno hacia la pilar.
   - Solape mínimo / long-tail natural → **mantener**, solo vigilar.
6. **Devuelve el fix a las skills que corrigen la causa raíz:** `mapa-de-palabras-clave` (reasignar 1 keyword : 1 URL) y `arquitectura-y-enlazado-interno` (redirigir enlaces internos hacia la URL ganadora).
7. **Cierra en dashboard** (`dashboard-seo`): cada query canibalizada como un issue con su severidad.

## Salida

Tabla de canibalización detectada, priorizada por severidad:

| Query | URLs en conflicto | Clics/Impresiones | Dominancia | Severidad | Acción recomendada |
|---|---|---|---|---|---|

Más un resumen: cuántas queries canibalizadas por severidad, y el Top 3 a resolver primero (mayor impresiones en juego).

## Ejemplo

Export de GSC de `tienda-cafe.com` (90 días):

| Query | URL | Clics | Impresiones | Posición |
|---|---|---|---|---|
| café de especialidad | /cafe-de-especialidad | 40 | 900 | 6 |
| café de especialidad | /blog/mejor-cafe | 35 | 850 | 7 |
| cómo hacer pan | /blog/como-hacer-pan | 100 | 1200 | 3 |
| cómo hacer pan | /recetas/pan-casero | 2 | 60 | 25 |

Script → "café de especialidad": dominancia 0.53 (reparto real), posiciones a 1 puesto de distancia → **Alta**, fusionar `/blog/mejor-cafe` en `/cafe-de-especialidad` y redirigir 301. "cómo hacer pan": dominancia 0.98 → **Bajo**, ruido de cola larga, no tocar.

## Gotchas

- **Sin datos de query+página no hay diagnóstico real.** Un mapa de keywords planeado (`mapa-de-palabras-clave`) NO prueba canibalización; solo el rendimiento real en GSC/Ahrefs la confirma.
- **Impresiones sin clics no siempre son canibalización** — puede ser una URL apareciendo por variantes de long-tail relacionadas. Revisa `dominance_ratio` antes de actuar.
- **Antes de fusionar/redirigir, decide cuál URL "gana"** (mejor posición media, más autoridad/backlinks, más reciente) — redirige siempre la débil hacia la fuerte, nunca al revés.
- **90 días de datos** dan más señal que 7-28: la posición diaria fluctúa y puede simular canibalización que no es tal.
- No confundas con **metas duplicadas** (`optimizacion-on-page-meta`): dos títulos iguales sin URLs compitiendo en ranking real no es esta skill.

## Script determinista (ahorro de tokens)

Si Python 3 está disponible, **ejecuta el script** para agrupar por query, calcular dominancia y clasificar severidad en vez de cruzar filas a mano: es determinista, ahorra tokens y es exacto. Pasa el export por `--file` (CSV o JSON con `{query, url, clicks, impressions, position}`).

Ejecuta (cero instalación, resuelve deps solo):

```bash
uv run skills/deteccion-de-canibalizacion/scripts/detectar_canibalizacion.py --file gsc_query_page.csv

# o, si no usas uv: python3 skills/deteccion-de-canibalizacion/scripts/detectar_canibalizacion.py --file gsc_query_page.csv
# JSON o stdin también valen:
cat export.json | uv run skills/deteccion-de-canibalizacion/scripts/detectar_canibalizacion.py --file - --format json
```

Ejecútalo con `--help` para ver opciones (incluye `--min-impressions` para filtrar ruido). Devuelve `{"ok":true,"cannibalization":[{"query","urls":[{"url","clicks","impressions","position"}],"total_clicks","total_impressions","dominance_ratio","position_gap","severity","action"}],"summary":{...}}`. Solo stdlib. Si Python no está disponible, hazlo en **modo manual** agrupando la tabla por query.
