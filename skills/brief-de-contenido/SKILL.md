---
name: brief-de-contenido
description: Usa esta skill cuando el usuario vaya a escribir u optimizar una pieza y necesite definir su estructura antes de redactar — aunque no diga "brief", p.ej. "qué estructura/encabezados pongo en este artículo", "cómo organizo este post", "qué meta título y descripción uso", "qué debería cubrir esta página", "voy a actualizar este artículo viejo". Crea el brief de contenido ("la brújula" del redactor) del método "De Cero a SEO" (aprendoseo, Arianna Lupi, Semanas 8 y 10): el brief lo dicta la SERP, no tu opinión. Genera los 3 tipos (Blog, Landing/Servicios, E-commerce) y el Brief de Optimización para contenido existente. No pases una keyword a redacción sin brief.
compatibility: Script opcional requiere Python 3 (uv) + requests/beautifulsoup4 (y SERPAPI_API_KEY o --urls); SerpApi/Ahrefs MCP opcionales (la skill funciona 100% manual con Headings Map).
metadata:
  author: aprendoseo
  milestone: SEO skills (De Cero a SEO)
  version: "1.0"
---

> **🚫 Regla de datos (obligatoria): NUNCA inventes números.**
> No estimes, supongas ni inventes métricas o datos que no tengas: volumen de búsqueda, dificultad/KD, clics, impresiones, CTR, posición, tráfico, Core Web Vitals, backlinks, fechas, precios, etc. Si te falta un dato, **pídeselo al usuario y espera su respuesta** — que lo pegue a mano, lo exporte (Google Search Console, Ahrefs, DinoRank, Screaming Frog…) o lo conecte por MCP. Da igual de dónde venga, pero tiene que venir de una fuente real. Si aun así no hay dato, márcalo explícitamente como `pendiente de dato` y NO continúes como si lo tuvieras. Un entregable con huecos honestos vale más que uno con cifras inventadas.


> **📊 Cierre en dashboard.** Cuando trabajes sobre un sitio, además de tu entrega persiste tu salida estructurada en `.seo-audit/<sitio>/data/content-briefs.json` (esquema en la skill `dashboard-seo`). Al cerrar el flujo SEO, genera/actualiza el dashboard con `dashboard-seo` y entrega el URL local. Tu archivo: `content-briefs.json`.

# Brief de Contenido — la brújula (W8 + W10)

Actúa como **estratega/editor SEO en aprendoseo**, siguiendo el método de Arianna Lupi de las Semanas 8 (contenido nuevo) y 10 (optimización). El brief es el **manual de instrucciones** del redactor. Regla de oro: **el brief lo dicta la SERP** — analiza el top 3 ANTES de decidir nada. Si los que rankean son guías, tu brief pide una guía.

> **Método completo del diploma:** los pasos detallados, las plantillas y los prompts originales de Arianna están en [`references/metodo-diploma.md`](references/metodo-diploma.md). Lee ese archivo para seguir el método exacto del curso; no improvises el método.

## Cuándo usar

- Tienes una keyword priorizada (de las **10 de Oro** / tab Estrategia) lista para producir.
- Vas a crear **contenido nuevo** (W8) → genera el brief según su tipo.
- Vas a **optimizar contenido existente** (W10, "darle cariño") → genera un **Brief de Optimización**.
- Necesitas alinear a redactor, diseñador y SEO en un solo documento.

Antes de esta skill: la estrategia/clusters debe estar hecha (`estrategia-de-contenidos-clusters`). Después: redacción (`redaccion-y-optimizacion-nlp`).

## Entradas (qué te doy)

- **Keyword principal** + cluster al que pertenece (pilar o spoke).
- **Tipo de página** deseado o a deducir: Blog, Landing/Servicios o E-commerce.
- **URL** (existente si es optimización; destino si es nueva).
- **Objetivo** de la pieza (informar, captar lead, vender).
- Opcional: keywords secundarias, enlaces internos disponibles del cluster, prueba social/datos de marca.

## Datos (MCP opcional)

Esta skill **funciona sin ningún MCP**, pero aquí es donde más aporta tener datos: **el brief lo dicta la SERP.**

1. **Sin MCP (manual, obligatorio mínimo):** abre Google en incógnito, busca la keyword y **lee con tus ojos el top 3**: formato, longitud aproximada, encabezados, bloque People Also Ask. Usa **Mangools** como simulador de SERP para validar metatítulo/metadescripción y **Headings Map** para extraer la jerarquía de los competidores. Documéntalo en la sección benchmark del brief.

2. **SerpApi MCP (GRATIS — clave aquí):** `mcp__serpapi__search` para traer datos reales de la SERP sin abrir el navegador:
   - **Top 3 orgánicos** → decide formato e intención.
   - **People Also Ask (PAA)** → secciones/H2 que el contenido debe cubrir.
   - **Related searches / autocomplete** → keywords secundarias y subtemas. Es la fuente principal para "el brief lo dicta la SERP".

3. **Ahrefs MCP (PAGO — requiere suscripción Ahrefs):**
   - `mcp__claude_ai_Ahrefs__keywords-explorer-overview` → volumen/intención de la keyword y secundarias.
   - `mcp__claude_ai_Ahrefs__keywords-explorer-matching-terms` → términos a cubrir en el brief.
   - `mcp__claude_ai_Ahrefs__serp-overview` → benchmark de quién rankea y con qué.

Conexión de MCPs: ver `../../MCP-SETUP.md`.

## Proceso

No hay un formato único: primero **lee la SERP**, luego elige el **tipo de brief**.

### Paso 1 — Analizar la SERP (top 3) → decidir intención y formato
Mira los 3 primeros resultados. ¿Qué formato es? ¿Qué intención satisface (informativa, comercial, transaccional)? **El formato de tu pieza imita lo que ya rankea.** Si rankean guías largas, no propongas una landing corta.

### Paso 2 — Elegir el tipo de brief
- **Blog (informativo):** responder dudas, autoridad, captar tráfico de cola larga.
- **Landing / Servicios (conversión):** CTAs y propuesta de valor **above the fold**, prueba social, beneficios > características.
- **E-commerce (transaccional):** atributos técnicos del producto, prueba social (reseñas), **urgencia/escasez**, cross-sell / up-sell.

### Paso 3 — Rellenar los elementos del brief (plantilla)
1. **Intención de búsqueda** y formato decidido (con evidencia del top 3).
2. **Metatítulo:** keyword **al inicio**, **50-60 caracteres**.
3. **Metadescripción:** **120-155 caracteres**, persuasiva, con **CTA**.
4. **Jerarquía de encabezados H1-H4:** un solo **H1 con la keyword**; **NO saltar niveles** (H2 → H4 está prohibido). Estructura completa esqueleto.
5. **Benchmark:** qué cubren los competidores del top 3 y qué hueco vas a llenar.
6. **Enlaces internos:** definidos desde el brief, con **anchor text concreto** y URL destino (usa el cluster).
7. **Elementos visuales sugeridos** (imágenes, tablas, infografías, vídeo).

### Paso 4 (W10) — Brief de Optimización (contenido existente)
Para piezas a refrescar ("darle cariño"):
- **Identifica** páginas a refrescar (caída de posiciones, contenido viejo).
- **Documenta los cambios ANTES de tocar** la pieza (qué encabezados añadir, qué actualizar, qué enlaces nuevos, qué metas reescribir).
- Conserva lo que funciona; no reescribas desde cero lo que ya rankea.

### Paso 5 — Registrar
Vuelca el brief a la tab **"Producción"** de la Plantilla Master y crea/actualiza la tarjeta en Trello.

## Salida

Genera el **sub-template según el tipo**. **Todo brief ARRANCA con la tabla de brief** (resumen de cabecera obligatorio); después va el detalle.

```
BRIEF DE CONTENIDO — [keyword principal]
Tipo: [Blog | Landing/Servicios | E-commerce | OPTIMIZACIÓN]
Cluster: [nombre] · Rol: [Pilar/Spoke] · URL: [destino/existente]

TABLA DE BRIEF (cabecera obligatoria)
| Campo             | Contenido                                              |
|-------------------|--------------------------------------------------------|
| Keyword primaria  | [keyword principal]                                    |
| Keyword secundaria| [1-3 secundarias, coma; o `pendiente de dato`]         |
| Meta título       | [50-60c, keyword al inicio]                            |
| Meta descripción  | [120-155c, con CTA]                                    |
| H1                | [un solo H1 con la keyword]                            |
| KV                | [volumen de búsqueda real; si no hay, `pendiente de dato`] |
| Intención         | [informativa / comercial / transaccional]             |

1. INTENCIÓN Y FORMATO
   Intención: [informativa/comercial/transaccional]
   Formato (lo dicta la SERP): [guía/listado/landing/ficha...]
   Evidencia top 3: [resumen]

2. METAS
   Metatítulo (50-60c, keyword al inicio): "____"  [conteo: __ c]
   Metadescripción (120-155c, con CTA):    "____"  [conteo: __ c]

3. JERARQUÍA DE ENCABEZADOS (sin saltos de nivel)
   H1: [keyword] ____
     H2: ____
       H3: ____
     H2: ____  (cubre PAA: "____")

4. BENCHMARK (top 3): [qué cubren / hueco a llenar]

5. ENLACES INTERNOS
   - anchor "____" → [URL del cluster]
   - anchor "____" → [URL]

6. VISUALES SUGERIDOS: [____]
```

**Variantes por tipo:**
- **Landing/Servicios:** añade bloque "Above the fold: propuesta de valor + CTA principal" y "Prueba social".
- **E-commerce:** añade "Atributos técnicos", "Reseñas/prueba social", "Urgencia/escasez", "Cross/Up-sell".
- **Optimización (W10):** añade bloque "CAMBIOS A REALIZAR (documentados antes de tocar)" y "Qué se conserva".

## Ejemplo

**Keyword:** "sérum vitamina C natural" (cluster Ingredientes activos, spoke). SerpApi top 3 = guías comparativas con tablas.

```
Tipo: Blog · Cluster: Ingredientes activos · Rol: Spoke
1. Intención: informativa-comercial · Formato: guía con tabla comparativa (lo dicta la SERP).
2. Metatítulo: "Sérum vitamina C natural: guía para elegir el mejor" (52 c)
   Metadescripción: "Descubre cómo elegir un sérum de vitamina C natural según tu piel. Compara ingredientes y empieza tu rutina hoy." (134 c)
3. H1: Sérum vitamina C natural
     H2: ¿Para qué sirve la vitamina C en la piel?
     H2: Cómo elegir tu sérum (PAA: "¿qué % de vitamina C es bueno?")
       H3: Concentración recomendada
     H2: Tabla comparativa
4. Benchmark: top 3 no explican concentración por tipo de piel → hueco a llenar.
5. Enlaces internos: anchor "ácido hialurónico" → /que-es-acido-hialuronico (pilar).
6. Visuales: tabla comparativa + foto de textura del producto.
```

## Script determinista (ahorro de tokens)

Si Python está disponible, EJECUTA este script para extraer el esquema (H1/H2/H3) de los competidores del top de la SERP (es determinista, ahorra tokens y mejora precisión) y usa su JSON como base del brief — recuerda que el brief lo dicta la SERP. Si falta `SERPAPI_API_KEY` o las dependencias `requests`/`beautifulsoup4`, sigue en modo manual (Headings Map a mano), o pasa `--urls` para saltarte SerpApi.

Ejecuta (cero instalación, resuelve deps solo):

```bash
SERPAPI_API_KEY=xxx uv run scripts/serp_outline.py "tu keyword" --top 5 --gl es --hl es
# o, si no usas uv: SERPAPI_API_KEY=xxx python3 scripts/serp_outline.py "tu keyword" --top 5 --gl es --hl es
# sin SerpApi: uv run scripts/serp_outline.py "tu keyword" --urls "https://a.com/x,https://b.com/y"
```

Corre con `--help` para ver opciones. Devuelve: `{"ok": true, "query": ..., "competitors": [{url,h1,headings:["H2: ...","H3: ..."]}], "common_questions": [...PAA...], "suggested_outline": [...H2 fusionados por frecuencia...]}`. Si falla, `{"ok": false, "reason": "...", "fallback": "modo manual: ..."}` (exit 0). Valida la jerarquía a mano antes de entregar.

Para elegir PRIMERO qué dominios/URLs son la competencia real de la keyword, corre la skill `analisis-de-competidores` y pásale sus URLs a este script con `--urls`.

## Gotchas

- **El brief lo dicta la SERP, no tu opinión:** analiza el top 3 ANTES de definir formato. Si rankean guías largas, no propongas una landing corta. Sin top 3 analizado, no hay brief.
- **Metatítulo 50-60 caracteres con la keyword al inicio**, no al final ni fuera de rango; **metadescripción 120-155 caracteres con CTA**, no sin llamada a la acción. Cuenta los caracteres siempre.
- Jerarquía **H1 → H2 → H3 sin saltar niveles** (H2 → H4 está prohibido): un solo H1 con la keyword, estructura completa.
- **La IA rompe la jerarquía de encabezados** e inventa estructura: valida la jerarquía a mano (Headings Map) antes de entregar, no confíes en el output crudo.
- Los **enlaces internos se definen desde el brief** (anchor text + URL del cluster), no se los dejes "al redactor".
- En W10 (optimización), **documenta los cambios ANTES de tocar la pieza** y conserva lo que ya rankea; no reescribas desde cero ni toques sin trazabilidad.
- Recuerda: **"un brief bien hecho es el 50% del éxito"** (Arianna) — invierte aquí el tiempo.
