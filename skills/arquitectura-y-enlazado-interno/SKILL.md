---
name: arquitectura-y-enlazado-interno
description: Diseña la arquitectura web y el enlazado interno (pilar→clusters) según el método del diploma "De Cero a SEO" (aprendoseo). Usa esta skill cuando haya que estructurar un sitio o repartir enlaces internos, AUNQUE el usuario no diga "arquitectura" ni "enlazado interno", p.ej. "cómo organizo las páginas/categorías de mi web", "tengo páginas que no reciben enlaces / no rankean", "mi contenido está muy enterrado", "el jugo SEO no llega a las páginas que venden", o al planificar un sitio nuevo. Entrega mapa de arquitectura pilar→clusters, lista de huérfanas y sugerencias de enlaces con anchor.
compatibility: Script opcional de detección de huérfanas/depth requiere Python 3 (uv, solo stdlib) y exports de Screaming Frog; si no, modo manual. Ahrefs MCP (pago) y SerpApi MCP (gratis) opcionales.
metadata:
  author: aprendoseo
  milestone: SEO skills (De Cero a SEO)
  version: "1.1"
---

> **🚫 Regla de datos (obligatoria): NUNCA inventes números.**
> No estimes, supongas ni inventes métricas o datos que no tengas: volumen de búsqueda, dificultad/KD, clics, impresiones, CTR, posición, tráfico, Core Web Vitals, backlinks, fechas, precios, etc. Si te falta un dato, **pídeselo al usuario y espera su respuesta** — que lo pegue a mano, lo exporte (Google Search Console, Ahrefs, DinoRank, Screaming Frog…) o lo conecte por MCP. Da igual de dónde venga, pero tiene que venir de una fuente real. Si aun así no hay dato, márcalo explícitamente como `pendiente de dato` y NO continúes como si lo tuvieras. Un entregable con huecos honestos vale más que uno con cifras inventadas.


> **📊 Cierre en dashboard.** Cuando trabajes sobre un sitio, además de tu entrega persiste tu salida estructurada en `.seo-audit/<sitio>/data/issues.json` (esquema en la skill `dashboard-seo`). Al cerrar el flujo SEO, genera/actualiza el dashboard con `dashboard-seo` y entrega el URL local. Tu archivo: `issues.json` / `next-steps.json` (huérfanas, enlazado).

# Arquitectura Web y Enlazado Interno (Diploma W9)

Actúa como arquitecto de información en aprendoseo. Marco del diploma: *"Lo que no se rastrea, no existe"*, y lo que está a 6 clics, casi no se rastrea. Tu misión es que el **Link Equity ("jugo SEO")** llegue donde importa.

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
3. **SerpApi MCP (GRATIS, apoyo):** `mcp__serpapi__search` para ver cómo agrupa Google los temas (related/PAA) y validar la lógica de clusters.

**Inventario de URLs (opcional, automático):** si el usuario no pasó el export de URLs, usa la skill `inventario-de-urls` para extraerlas, por **sitemap (cero instalación)** o con **Screaming Frog CLI (GRATIS hasta 500 URLs; licencia solo para >500 URLs / config guardada / render JS / scheduling / API)**, que aporta el grafo de inlinks/outlinks para detectar huérfanas.

Config de MCP: ver `../../MCP-SETUP.md`.

## Proceso

1. **Define la jerarquía pilar→clusters:** un tema pilar amplio enlaza a sus clusters específicos, y los clusters enlazan de vuelta al pilar.
2. **Aplica la regla de los 3 clics:** toda página relevante debe alcanzarse en **≤3 clics** desde la home.
3. **Evalúa Crawl Depth vs Crawl Width:** ¿el sitio es profundo (malo, entierra contenido) o ancho/plano (mejor para rastreo)? Aplana lo profundo. **No confundas tres cosas** (práctica de Juan, Semana 9): la estructura de URL, el nivel de profundidad de carpeta (lo que muestra Octopus) y la cantidad de clics desde la home (lo que muestra Screaming Frog como Crawl Depth). La regla de los 3 clics se mide en clics, no en carpetas. Práctica de Ari: servicios y blog a un clic de la home; el lenguaje correcto es "3 niveles de profundidad, o 2".
4. **Detecta páginas huérfanas** (0 inlinks) y planifica desde dónde enlazarlas.
5. **URLs semánticas:** estructura de carpetas que refleje pilar/cluster. Criterios de los coaches: cada tipo de contenido vive en su subcarpeta (servicios, tienda, blog); el blog va categorizado (Blog > Categoría > Post) y las categorías crean los pilares; los filtros (por ejemplo la edad en una juguetería) son parámetros, no categorías; sin carpetas de año (`/2025/`) ni páginas para redes sociales; subcarpetas y no subdominios (los subdominios pueden afectar la autoridad); un solo idioma en los slugs; el home enlaza directo a los servicios principales; mira a la competencia antes de decidir. Los parámetros de URL (`?valor=0`, `?project=`) son un asunto técnico urgente que se deriva al SEO técnico.
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

## Enlazado por matriz (opcional, después de definir pilar y clusters)

Con la lista de páginas (rol: home, pilar, cluster, producto) y los enlaces internos, `matriz_enlaces.py` devuelve **la matriz de lo que falta**: pilar a cada cluster y de vuelta, mínimo por pieza (2 contextuales a otros artículos y 1 a producto o servicio, el mínimo del brief de la Semana 9), páginas de conversión infraenlazadas, huérfanas, anchors genéricos y la profundidad en clics frente a la de carpeta.

```bash
python3 skills/arquitectura-y-enlazado-interno/scripts/matriz_enlaces.py --pages paginas.csv --links all_inlinks.csv
```

Hay ejemplos en `fixtures/paginas_muestra.csv` y `fixtures/enlaces_muestra.csv`. Los umbrales de 3 entrantes mínimos y de 40 % de anchors repetidos son un complemento externo (ver abajo); la regla de los 3 clics y el mínimo por pieza son del diplomado.

## Checklist plana frente a profunda

Antes de entregar el mapa, revisa:

- [ ] Servicios, categorías y blog a 1 clic de la home; cualquier contenido importante a 3 clics o menos (pilares a 2).
- [ ] No hay niveles intermedios que falten (home a producto sin categoría) ni páginas de login o home repetida en el flujo principal.
- [ ] La anchura por nivel no diluye: un menú gigante enlaza todo con todo, no es plano, es ruido.
- [ ] La profundidad de carpeta refleja pilar y cluster, sin que obligue a más de 3 clics.
- [ ] Cada página importante tiene al menos 1 enlace entrante desde contenido relacionado y ninguna queda huérfana.
- [ ] Los enlaces contenido a producto existen desde el brief.
- [ ] Mejoras escritas: al menos 3 concretas antes de tocar el sitio ("analiza antes de cambiar").

## Complementos opcionales

Después del método del diploma, [`references/complementos-claude-seo.md`](references/complementos-claude-seo.md) añade: reglas de enlaces obligatorios y recomendados por cluster, umbrales de entrantes y diversidad de anchors, y una rúbrica de puntuación de la arquitectura. Es material externo (claude-seo, MIT), no parte del método del diplomado.

## Script determinista (ahorro de tokens)

Si Python 3 está disponible, **ejecuta el script** para detectar huérfanas y analizar el enlazado interno desde los exports de Screaming Frog: es determinista, ahorra tokens y no requiere leer los CSV en contexto.

Ejecuta (cero instalación, resuelve deps solo):

```
uv run skills/arquitectura-y-enlazado-interno/scripts/orphans.py --internal internal_all.csv --inlinks all_inlinks.csv
# o, si no usas uv: python3 skills/arquitectura-y-enlazado-interno/scripts/orphans.py --internal internal_all.csv --inlinks all_inlinks.csv
# umbral de pocos inlinks ajustable (default <3):
uv run skills/arquitectura-y-enlazado-interno/scripts/orphans.py --internal internal_all.csv --inlinks all_inlinks.csv --low 5
```

Corre con `--help` para ver opciones. Salida: `{"ok":true,"orphans":[...],"low_inlinks":[{"url","inlinks"}],"depth_gt3":[...],"depth_detail":[...],"depth_mismatch":[...],"summary":{...}}`. `depth_detail` y `depth_mismatch` (v1.1) comparan los clics desde la home con la profundidad de carpeta: una carpeta profunda a pocos clics no es un problema de rastreo; una ruta corta enterrada a muchos clics sí. Solo stdlib. Si falla (archivo o columna ausente) devuelve `{"ok":false,"reason":...}` (exit 0) → **modo manual**: cruza internal_all vs. all_inlinks a ojo.

## Gotchas

- **Regla de los 3 clics desde la home**, toda página relevante debe alcanzarse en ≤3 clics; estructura demasiado profunda (>3) entierra contenido y diluye el jugo SEO.
- **Una página huérfana (sin enlaces internos) no se rastrea bien, detéctala**, toda URL con 0 inlinks es invisible; dale al menos un inlink relevante.
- **Define los enlaces internos y su anchor DESDE el brief, no después**, entran en la planificación de la pieza, no se improvisan al final.
- **No concentres todo el link equity en una sola página**, reparte hacia las páginas de conversión infraenlazadas; over-linking (todo con todo) también diluye. Sé selectivo y jerárquico.
- **Anchors descriptivos, no genéricos** ("clic aquí", "ver más") desperdician la señal temática.
- **No olvides los enlaces contenido→producto:** sin ellos el tráfico informacional nunca llega a convertir.
- **No confundas Crawl Depth** (profundidad de clics) con **Crawl Width** (amplitud por nivel).
- **Profundidad de carpeta no es profundidad de clics.** Una URL `/blog/categoria/post/` puede estar a un clic de la home si el menú la enlaza. Mide los clics con Screaming Frog, no contando barras.
- **Los filtros no son categorías**: duplican contenido. Usa parámetros o facetas controladas.
- **El enlazado interno no entra en la auditoría técnica** (práctica de Juan): va en este entregable, separado.
- **El entregable separa qué hace quien edita el sitio y qué hace el desarrollador o dueño** (parámetros de URL, sitemaps, CMS), como pide Ari.
