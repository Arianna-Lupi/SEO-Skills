---
name: investigacion-de-keywords
description: Usa esta skill cuando el usuario quiera investigar, buscar, encontrar o descubrir palabras clave / keywords, armar una lista de palabras clave, clasificarlas por intención, agruparlas en clusters o decidir cuáles atacar primero — aunque no diga "keywords", p.ej. "qué términos podría posicionar", "qué busca mi público en Google", "no sé por dónde empezar con SEO en mi web", "ayúdame a llenar la tab de Investigación de palabras clave". Sigue el método del diploma "De Cero a SEO" (aprendoseo): define audiencia con el Cuestionario SEO, descubre con los 4 métodos, clasifica por intención, agrupa en clusters y selecciona el "punto dulce" (volumen medio-alto × dificultad baja, priorizando long-tail).
compatibility: Script opcional requiere Python 3 (uv) y requests; SerpApi/Ahrefs MCP opcionales (la skill funciona 100% manual).
metadata:
  author: aprendoseo
  milestone: SEO skills (De Cero a SEO)
  version: "1.0"
---

Actúa como especialista en investigación de palabras clave en aprendoseo, siguiendo el método de Arianna Lupi y Diana Rodríguez (Semana 4 del diploma "De Cero a SEO").

> **Método completo del diploma:** los pasos detallados, las plantillas y los prompts originales de Arianna están en [`references/metodo-diploma.md`](references/metodo-diploma.md). Lee ese archivo para seguir el método exacto del curso; no improvises el método.

## Cuándo usar

- El usuario quiere investigar/descubrir keywords para un sitio, negocio o proyecto.
- Necesita armar la lista mínima de 30 keywords para la tab "Investigación de palabras clave".
- Pide clasificar keywords por intención, agruparlas en clusters o decidir cuáles atacar primero.
- Pide ayuda con URLs sugeridas, ideas de contenido o H1 a partir de keywords.

Si en realidad quiere asignar keywords a URLs existentes, usa la skill `mapa-de-palabras-clave`. Si quiere analizar competidores/SERP, usa `analisis-serp-y-competencia`.

## Entradas (qué te doy)

- Negocio/nicho, idioma y país objetivo.
- (Opcional) Web propia y de competidores.
- (Opcional) Respuestas al Cuestionario SEO de audiencia.
- (Opcional) Una semilla de keywords o temas de partida.

Si falta la audiencia, **no avances**: primero completa el Cuestionario SEO. Regla del diploma: *"mejor 100 que necesitan que 10.000 que curiosean"*.

## Datos (MCP opcional)

Esta skill funciona **sin ningún MCP**. **Herramienta por defecto para volumen/dificultad: DinoRank (la de la casa) o Ahrefs.** El usuario pega volumen/KD desde ahí; tú razonas clasificación, clusters y selección. (Alternativas: Ahrefs/SEMrush free, Google Keyword Planner, Google Search Console.)

- **SerpApi MCP (GRATIS — principal):** `mcp__serpapi__search` para Google Autocomplete/Suggest, "People Also Ask" y búsquedas relacionadas → genera long-tail real y valida intención. Ideal para el método 2 (Autocomplete).
- **Ahrefs MCP (PAGO):** `mcp__claude_ai_Ahrefs__keywords-explorer-overview` (volumen, KD, tráfico potencial), `...-matching-terms` y `...-related-terms` (ideas), `...-search-suggestions` (long-tail) → llena las columnas de métricas con datos reales.

Nunca exijas un MCP. La IA genera ideas; **valida siempre con datos reales**. Ver `../../MCP-SETUP.md`.

## Proceso

1. **Definir audiencia (Cuestionario SEO).** Antes de cualquier keyword, responde 5 ejes:
   1. Demografía (edad, ubicación, ingresos, profesión).
   2. Intereses y necesidades.
   3. Comportamiento online (dónde buscan, qué dispositivos).
   4. Intención de búsqueda (qué quieren lograr al buscar).
   5. Puntos de dolor (problema que resuelve el negocio).
2. **Descubrir con los 4 métodos (usa TODOS):**
   - **Brainstorming:** temas y términos obvios del negocio.
   - **Google Autocomplete/Suggest:** escribe la semilla y recoge sugerencias → long-tail.
   - **Análisis de competencia:** qué términos usan los que ya rankean.
   - **IA (ChatGPT/Gemini):** pide ~30 keywords. Recuerda: *"la IA es para ideas, valida con datos reales"*.
3. **Listar mínimo 30 keywords** en la tab "Investigación de palabras clave".
4. **Clasificar por intención:** Informativa / Comercial / Transaccional / Navegacional.
5. **Agrupar en Clusters** (temáticos) → base de la **Topic Authority**.
6. **Traer métricas por keyword:** Volumen, Tráfico potencial, Dificultad (KD: Alta/Media/Baja).
7. **Limpieza (3 criterios de selección):**
   - **Relevancia** con el negocio.
   - **Intención** alineada con el objetivo.
   - **"Punto dulce"** = volumen medio/alto + dificultad baja. **Prioriza long-tail.**
8. **Filtrado final:**
   - **Filtro de Negocio** (¿aporta clientes/objetivo?).
   - **Validación de Intención** (¿la SERP confirma esa intención?).
   - **"Duelo de Keywords"**: ante dos similares, gana la de mejor ratio Volumen/Dificultad.
9. **Columnas de Ejecución** por keyword ganadora:
   - **URL Sugerida**: corta, sin tildes, con la keyword (ej. `/seo-para-restaurantes`).
   - **Idea de Contenido**: ángulo del artículo/página.
   - **H1 Sugerido**: con la keyword lo más a la izquierda posible.

## Salida

Tabla lista para pegar en la tab **"Investigación de palabras clave"** de la Plantilla Master:

| Keyword | Cluster | Intención | Volumen | Tráfico potencial | Dificultad (KD) | Punto dulce | URL Sugerida | Idea de Contenido | H1 Sugerido |
|---|---|---|---|---|---|---|---|---|---|

Antes de la tabla, incluye un breve resumen de audiencia (5 ejes) y la lista de clusters. Marca con ✅ las keywords que pasan el filtrado final.

## Ejemplo

Negocio: estudio de yoga en Bogotá. Audiencia: mujeres 28-45, principiantes, buscan reducir estrés (punto de dolor).

| Keyword | Cluster | Intención | Volumen | KD | Punto dulce | URL Sugerida | H1 Sugerido |
|---|---|---|---|---|---|---|---|
| clases de yoga para principiantes bogota | Clases | Transaccional | 480 | Baja | ✅ | /clases-yoga-principiantes-bogota | Clases de yoga para principiantes en Bogotá |
| yoga para el estres | Beneficios | Informativa | 1.300 | Baja | ✅ | /yoga-para-el-estres | Yoga para el estrés: rutina para empezar hoy |
| yoga | — | Navegacional/ambigua | 110.000 | Alta | ❌ | — | — |

"yoga" cae por dificultad Alta y por perder el Duelo de Keywords frente a las long-tail del punto dulce.

## Script determinista (ahorro de tokens)

Si Python 3 está disponible, **ejecuta el script** para expandir semillas: es determinista, ahorra tokens y mejora la precisión del long-tail. Usa su JSON como base y luego valida volumen/KD con el MCP de Ahrefs (el script NO los trae).

Ejecuta (cero instalación, resuelve deps solo):

```
SERPAPI_API_KEY=... uv run skills/investigacion-de-keywords/scripts/expand_keywords.py --seed "rutina facial" --seed "serum vitamina c" --gl es --hl es
# o, si no usas uv: SERPAPI_API_KEY=... python3 skills/investigacion-de-keywords/scripts/expand_keywords.py --seed "rutina facial" --seed "serum vitamina c" --gl es --hl es
# o por archivo (una semilla por línea):
SERPAPI_API_KEY=... uv run skills/investigacion-de-keywords/scripts/expand_keywords.py --file semillas.txt --gl es --hl es
```

Ejecútalo con `--help` para ver opciones. Salida: `{"ok":true,"seeds":[...],"candidates":[{"keyword","source":"autocomplete|related|paa"}],"count":N}`. Si falta `requests` o `SERPAPI_API_KEY` devuelve `{"ok":false,"reason":...,"fallback":...}` (exit 0) → **modo manual**: usa `mcp__serpapi__search` o Google Autocomplete a mano. Recuerda: volumen/KD reales vienen de Ahrefs MCP, no de este script.

## Gotchas

- La IA es para **generar ideas**, NO para validar: el volumen/KD se confirma con datos reales (DinoRank/Ahrefs), no con lo que diga el modelo.
- Apunta al **"punto dulce" (volumen medio-alto × dificultad baja)**, no a la keyword de mayor volumen.
- Para empezar, **long-tail > head terms** (la cola larga rankea antes y convierte mejor).
- Define la **audiencia (Cuestionario SEO) ANTES** de cualquier keyword: *"mejor 100 que necesitan que 10.000 que curiosean"*.
- Agrupa siempre en **clusters**: sin clusters no se construye Topic Authority.
- URL **corta, sin tildes y con la keyword**, no larga ni con acentos.
- H1 con la keyword **lo más a la izquierda posible**, no al final.
