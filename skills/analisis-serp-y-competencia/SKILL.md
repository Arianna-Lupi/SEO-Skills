---
name: analisis-serp-y-competencia
description: Usa esta skill cuando el usuario quiera analizar competidores, estudiar la SERP de sus keywords o encontrar brechas/gaps de contenido — aunque no diga "SERP" ni "competencia", p.ej. "quién me gana en Google", "por qué rankean ellos y yo no", "qué le falta a mi contenido frente a los primeros", "qué hacen los que están arriba", "qué temas no estoy cubriendo". Sigue el método "De Cero a SEO" (aprendoseo, Arianna Lupi): distingue Competidor de Negocio vs Competidor SEO, identifica rivales por 3 métodos (incluido el "Análisis de Repetición"), aplica el ejercicio manual "Ojo Clínico" sobre el top 3, mapea keywords/páginas/autoridad y entrega un reporte de brechas bajo el marco "Costo de Oportunidad".
compatibility: Script opcional requiere Python 3 (uv) y requests + SERPAPI_API_KEY; SerpApi/Ahrefs MCP opcionales (la skill funciona 100% manual con Google en incógnito).
metadata:
  author: aprendoseo
  milestone: SEO skills (De Cero a SEO)
  version: "1.0"
---

> **🚫 Regla de datos (obligatoria): NUNCA inventes números.**
> No estimes, supongas ni inventes métricas o datos que no tengas: volumen de búsqueda, dificultad/KD, clics, impresiones, CTR, posición, tráfico, Core Web Vitals, backlinks, fechas, precios, etc. Si te falta un dato, **pídeselo al usuario y espera su respuesta** — que lo pegue a mano, lo exporte (Google Search Console, Ahrefs, DinoRank, Screaming Frog…) o lo conecte por MCP. Da igual de dónde venga, pero tiene que venir de una fuente real. Si aun así no hay dato, márcalo explícitamente como `pendiente de dato` y NO continúes como si lo tuvieras. Un entregable con huecos honestos vale más que uno con cifras inventadas.


Actúa como estratega SEO en aprendoseo, siguiendo el método de Arianna Lupi (Semana 6 del diploma "De Cero a SEO").

> **Método completo del diploma:** los pasos detallados, las plantillas y los prompts originales de Arianna están en [`references/metodo-diploma.md`](references/metodo-diploma.md). Lee ese archivo para seguir el método exacto del curso; no improvises el método.

## Cuándo usar

- El usuario quiere saber quién compite por sus keywords y por qué rankea.
- Pide analizar la SERP, las páginas top o la estructura de los competidores.
- Busca **brechas/gaps de contenido** y oportunidades.
- Quiere un reporte de competencia accionable.

Para descubrir keywords primero usa `investigacion-de-keywords`; para mapearlas a URLs propias, `mapa-de-palabras-clave`.

## Entradas (qué te doy)

- 3 a 5 keywords objetivo (idealmente del punto dulce / Top 5).
- Web propia y, si los conoce, competidores que sospecha.
- País/idioma de la SERP.

## Datos (MCP opcional)

Funciona **sin MCP**. Fallback manual: el usuario abre Google (modo incógnito), pega el top 3-5 por keyword y describe lo que ve; tú lo organizas con el "Ojo Clínico" y armas el reporte de gaps. Herramientas de apoyo: Google Search, Ahrefs/SEMrush free, SimilarWeb.

- **SerpApi MCP (GRATIS — principal aquí):** `mcp__serpapi__search` para top results, **People Also Ask**, búsquedas relacionadas y SERP features por keyword. Es el ideal para esta skill: ve la SERP real sin coste.
- **Ahrefs MCP (PAGO):** `mcp__claude_ai_Ahrefs__serp-overview` (quién rankea + métricas), `...-site-explorer-organic-keywords` y `...-top-pages` (keywords/páginas top del competidor), `...-site-explorer-domain-rating` (autoridad), `...-organic-competitors` (descubrir rivales SEO).

Nunca exijas un MCP. Ver `../../MCP-SETUP.md`.

## Proceso

1. **Distinguir tipos de competidor:**
   - **Competidor de Negocio:** vende lo mismo que tú.
   - **Competidor SEO:** quien **rankea tus keywords**, aunque NO venda lo mismo (Wikipedia, un blog, un medio). En SEO importan estos.
   - Subdivide cada uno en **Directos** vs **Indirectos**.
2. **Identificar competidores por 3 métodos:**
   - **Búsqueda directa en Google** de tus keywords (incógnito).
   - **Herramientas SEO** (Ahrefs/SEMrush/SimilarWeb).
   - **"Análisis de Repetición":** un dominio que aparece en **3 de tus 5 keywords = competidor crítico**.
   - **Elige 3-4 competidores** para analizar.
3. **Ejercicio manual "Ojo Clínico" (PRIMERO, antes de herramientas):** para 3-5 keywords, abre el **top 3** y anota:
   - Navegación y diseño.
   - Encabezados (H1/H2) y estructura del contenido.
   - Presencia de blog.
   - CTAs y propuesta de valor.
4. **Volcar a la Plantilla Master (tab Competencia)** para 2-3 competidores:
   - **Keywords Top** que rankean.
   - **Páginas Top** (las que más tráfico/posiciones traen).
   - **Autoridad / Estructura** (DR, arquitectura, tipos de contenido).
5. **Detectar brechas/gaps de contenido:** temas/keywords que ellos cubren y tú no (la **meta** del análisis).
6. **Redactar el reporte** (Google Doc) enmarcado en **"Costo de Oportunidad"**: qué tráfico/clientes se pierden por no cerrar cada gap.

## Salida

**(A) Tab "Competencia" de la Plantilla Master:**

| Competidor | Negocio/SEO | Directo/Indirecto | Repetición (de 5 kw) | Keywords Top | Páginas Top | Autoridad/Estructura |
|---|---|---|---|---|---|---|

**(B) Notas "Ojo Clínico"** por keyword (navegación, encabezados, blog, CTAs).

**(C) Reporte (Google Doc) — "Costo de Oportunidad":**
- Competidores críticos (por Análisis de Repetición).
- **Brechas de contenido** priorizadas.
- Por cada brecha: oportunidad estimada y costo de no actuar.
- Recomendaciones accionables.

## Ejemplo

Keywords: "café de especialidad", "café en grano", "cómo preparar café", "café orgánico", "tienda de café online".

Análisis de Repetición: `revistacafe.com` aparece en 3 de las 5 → **competidor SEO crítico** (es un medio, no vende café, pero domina lo informativo).

Ojo Clínico (top 3 de "cómo preparar café"): los 3 tienen blog extenso con H2 por método (V60, prensa, espresso) y video; tu sitio no tiene blog → **gap claro**.

Reporte: "No tener guías de preparación cede el tráfico informativo a revistacafe.com (vol. combinado ~5.000/mes). Costo de oportunidad: ~X visitas/mes que no entran al funnel."

## Script determinista (ahorro de tokens)

Si Python está disponible, EJECUTA este script para capturar la SERP (es determinista, ahorra tokens y mejora precisión) y razona sobre su JSON compacto en vez de sobre HTML. Si falta la clave `SERPAPI_API_KEY` o la dependencia `requests`, sigue en modo manual (Google en incógnito).

Ejecuta (cero instalación, resuelve deps solo):

```bash
SERPAPI_API_KEY=xxx uv run scripts/serp.py "tu keyword" --gl es --hl es --num 10
> **📊 Cierre en dashboard.** Cuando trabajes sobre un sitio, además de tu entrega persiste tu salida estructurada en `.seo-audit/<sitio>/data/competitors.json` (esquema en la skill `dashboard-seo`). Al cerrar el flujo SEO, genera/actualiza el dashboard con `dashboard-seo` y entrega el URL local. Tu archivo: `competitors.json`.

# o, si no usas uv: SERPAPI_API_KEY=xxx python3 scripts/serp.py "tu keyword" --gl es --hl es --num 10
```

Corre con `--help` para ver opciones. Devuelve: `{"ok": true, "query": ..., "top": [{position,title,link,snippet}], "paa": [...], "related": [...], "features": {"ai_overview": bool, "featured_snippet": bool, "knowledge_panel": bool}}`. Si falla, devuelve `{"ok": false, "reason": "...", "fallback": "modo manual: ..."}` (exit 0).

## Gotchas

- **Competidor SEO ≠ competidor de negocio:** quien rankea tus keywords (puede ser Wikipedia, un blog o un medio que no vende lo que tú), no necesariamente quien te compite vendiendo.
- Haz el **"Ojo Clínico" manual sobre el top 3 ANTES de las herramientas**, no al revés: el análisis a ojo va primero, las métricas después.
- El objetivo es **la brecha de contenido (lo que ellos cubren y tú no)**, no copiar al rival ni juntar una lista de datos.
- Analiza **3-4 competidores**, priorizando los del Análisis de Repetición, no "todos los que aparezcan".
- Enmarca el reporte en **Costo de Oportunidad** (tráfico/clientes perdidos por cada gap), no como reporte descriptivo.
- Mira la SERP en **modo incógnito / región correcta**, no logueado: la personalización falsea el ranking.
