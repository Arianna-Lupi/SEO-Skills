---
name: arquitectura-y-enlazado-interno
description: Diseña la arquitectura web y el enlazado interno (pilar→clusters) según el método del diploma "De Cero a SEO" (aprendoseo). Usa esta skill cuando haya que estructurar un sitio o repartir enlaces internos — AUNQUE el usuario no diga "arquitectura" ni "enlazado interno", p.ej. "cómo organizo las páginas/categorías de mi web", "tengo páginas que no reciben enlaces / no rankean", "mi contenido está muy enterrado", "el jugo SEO no llega a las páginas que venden", o al planificar un sitio nuevo. Entrega mapa de arquitectura pilar→clusters, lista de huérfanas y sugerencias de enlaces con anchor.
compatibility: Script opcional de detección de huérfanas/depth requiere Python 3 (uv, solo stdlib) y exports de Screaming Frog; si no, modo manual. Ahrefs MCP (pago) y SerpApi MCP (gratis) opcionales.
metadata:
  author: aprendoseo
  milestone: SEO skills (De Cero a SEO)
  version: "1.0"
---

# Arquitectura Web y Enlazado Interno (Diploma W9)

Actúa como arquitecto de información en aprendoseo. Marco del diploma: *"Lo que no se rastrea, no existe"* — y lo que está a 6 clics, casi no se rastrea. Tu misión es que el **Link Equity ("jugo SEO")** llegue donde importa.

> **Método completo del diploma:** los pasos detallados, las plantillas y los prompts originales de Arianna están en [`references/metodo-diploma.md`](references/metodo-diploma.md). Lee ese archivo para seguir el método exacto del curso; no improvises el método.

## Cuándo usar

- **Planificas un sitio nuevo** o una sección (defines la estructura desde cero).
- Detectas **páginas huérfanas** (sin enlaces internos entrantes).
- Hay contenido **enterrado a más de 3 clics** de la home.
- Las páginas que **convierten** no reciben suficiente link equity.

## Entradas (qué te doy)

- **Dominio** o sitemap actual (o el listado de URLs/temas planificados).
- **Temas pilar** y subtemas (clusters) del proyecto.
- **Páginas de conversión** prioritarias (producto, servicio, landing).
- Export de **Screaming Frog** (crawl depth, inlinks) si lo tienes.

## Datos (MCP opcional)

Funciona **sin MCP**: con un crawl de Screaming Frog y **Octopus.do** para el mapa visual basta.

1. **Sin MCP (manual):** crawl con **Screaming Frog** → revisa **Crawl Depth** (clics desde home) y **inlinks**; las URLs con 0 inlinks son **huérfanas**. Dibuja la estructura pilar→clusters en **Octopus.do** (sitemap visual).
2. **Ahrefs MCP (PAGO):** `mcp__claude_ai_Ahrefs__site-explorer-pages-by-internal-links` (qué páginas reciben más/menos enlaces internos), `...site-explorer-linked-anchors-internal` (anchors internos usados), `...site-audit-issues` (detecta **huérfanas** y profundidad excesiva). Ahrefs es de pago.
3. **SerpApi MCP (GRATIS — apoyo):** `mcp__serpapi__search` para ver cómo agrupa Google los temas (related/PAA) y validar la lógica de clusters.

**Inventario de URLs (opcional, automático):** si el usuario no pasó el export de URLs, usa la skill `inventario-de-urls` para extraerlas — por **sitemap (cero instalación)** o con **Screaming Frog CLI (GRATIS hasta 500 URLs; licencia solo para >500 URLs / config guardada / render JS / scheduling / API)**, que aporta el grafo de inlinks/outlinks para detectar huérfanas.

Config de MCP: ver `../../MCP-SETUP.md`.

## Proceso

1. **Define la jerarquía pilar→clusters:** un tema pilar amplio enlaza a sus clusters específicos, y los clusters enlazan de vuelta al pilar.
2. **Aplica la regla de los 3 clics:** toda página relevante debe alcanzarse en **≤3 clics** desde la home.
3. **Evalúa Crawl Depth vs Crawl Width:** ¿el sitio es profundo (malo, entierra contenido) o ancho/plano (mejor para rastreo)? Aplana lo profundo.
4. **Detecta páginas huérfanas** (0 inlinks) y planifica desde dónde enlazarlas.
5. **URLs semánticas:** estructura de carpetas que refleje pilar/cluster.
6. **Define los tipos de enlace interno** en el brief:
   - **Contextuales** (dentro del cuerpo del texto, máximo valor temático).
   - **Contenido → Producto** (de artículo a página de conversión).
   - **Producto → Producto** (cross-sell entre páginas comerciales).
   - **Navegación** (menú / footer).
7. **Redistribuye el Link Equity:** dirige enlaces desde páginas con autoridad hacia las de conversión que estén infraenlazadas.
8. **Asigna anchor text** descriptivo a cada enlace sugerido.

## Salida

- **Mapa de arquitectura** pilar→clusters (formato Octopus.do o esquema).
- **Lista de páginas huérfanas** y desde dónde enlazarlas.
- **Sugerencias de enlaces internos** con su **anchor text** y tipo (contextual / contenido→producto / etc.).
- **Plan de redistribución de link equity** hacia páginas de conversión.
- Registro en la Plantilla Master; tareas → Trello.

## Ejemplo

**Pilar:** `/seo-tecnico/` → clusters: `/seo-tecnico/auditoria/`, `/seo-tecnico/core-web-vitals/`, `/seo-tecnico/robots-txt/`.

- Huérfana detectada: `/seo-tecnico/robots-txt/` (0 inlinks). → Enlazar desde el pilar y desde `/auditoria/` con anchor `bloquear rastreo con robots.txt`.
- Conversión infraenlazada: `/curso-seo/` recibe solo 2 inlinks. → Añadir enlaces **contenido→producto** desde los 3 artículos pilar con anchor `aprende SEO desde cero`.
- Crawl depth de `/robots-txt/` = 5 clics → mover bajo el pilar para bajar a 2.

## Script determinista (ahorro de tokens)

Si Python 3 está disponible, **ejecuta el script** para detectar huérfanas y analizar el enlazado interno desde los exports de Screaming Frog: es determinista, ahorra tokens y no requiere leer los CSV en contexto.

Ejecuta (cero instalación, resuelve deps solo):

```
uv run skills/arquitectura-y-enlazado-interno/scripts/orphans.py --internal internal_all.csv --inlinks all_inlinks.csv
# o, si no usas uv: python3 skills/arquitectura-y-enlazado-interno/scripts/orphans.py --internal internal_all.csv --inlinks all_inlinks.csv
# umbral de pocos inlinks ajustable (default <3):
uv run skills/arquitectura-y-enlazado-interno/scripts/orphans.py --internal internal_all.csv --inlinks all_inlinks.csv --low 5
```

Corre con `--help` para ver opciones. Salida: `{"ok":true,"orphans":[...],"low_inlinks":[{"url","inlinks"}],"depth_gt3":[...],"summary":{...}}`. Solo stdlib. Si falla (archivo o columna ausente) devuelve `{"ok":false,"reason":...}` (exit 0) → **modo manual**: cruza internal_all vs. all_inlinks a ojo.

## Gotchas

- **Regla de los 3 clics desde la home** — toda página relevante debe alcanzarse en ≤3 clics; estructura demasiado profunda (>3) entierra contenido y diluye el jugo SEO.
- **Una página huérfana (sin enlaces internos) no se rastrea bien — detéctala** — toda URL con 0 inlinks es invisible; dale al menos un inlink relevante.
- **Define los enlaces internos y su anchor DESDE el brief, no después** — entran en la planificación de la pieza, no se improvisan al final.
- **No concentres todo el link equity en una sola página** — reparte hacia las páginas de conversión infraenlazadas; over-linking (todo con todo) también diluye. Sé selectivo y jerárquico.
- **Anchors descriptivos, no genéricos** ("clic aquí", "ver más") desperdician la señal temática.
- **No olvides los enlaces contenido→producto:** sin ellos el tráfico informacional nunca llega a convertir.
- **No confundas Crawl Depth** (profundidad de clics) con **Crawl Width** (amplitud por nivel).
