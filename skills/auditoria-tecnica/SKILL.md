---
name: auditoria-tecnica
description: Ejecuta una auditoría SEO técnica completa en los 3 bloques del diploma "De Cero a SEO" (indexabilidad, velocidad/CWV, seguridad+canonical). Usa esta skill cuando haya que revisar la salud técnica de un sitio — AUNQUE el usuario no diga "auditoría técnica", p.ej. "se me cayó el tráfico y no sé por qué", "Google no me indexa", "el sitio carga lento / CWV en rojo", "voy a migrar/rediseñar", "revisa robots.txt / canonical / sitemap", u onboarding de proyecto nuevo y revisiones trimestrales. Audita POR PLANTILLAS, no página por página, y entrega issues por severidad con plan de remediación.
compatibility: Scripts opcionales: resumen de crawl (stdlib, Python 3 vía uv) y http_checks en vivo (requiere `requests`); si no, modo manual. Screaming Frog CLI (gratis hasta 500 URLs), GSC MCP (gratis) y Ahrefs MCP (pago) opcionales.
metadata:
  author: aprendoseo
  milestone: SEO skills (De Cero a SEO)
  version: "1.0"
---

> **🚫 Regla de datos (obligatoria): NUNCA inventes números.**
> No estimes, supongas ni inventes métricas o datos que no tengas: volumen de búsqueda, dificultad/KD, clics, impresiones, CTR, posición, tráfico, Core Web Vitals, backlinks, fechas, precios, etc. Si te falta un dato, **pídeselo al usuario y espera su respuesta** — que lo pegue a mano, lo exporte (Google Search Console, Ahrefs, DinoRank, Screaming Frog…) o lo conecte por MCP. Da igual de dónde venga, pero tiene que venir de una fuente real. Si aun así no hay dato, márcalo explícitamente como `pendiente de dato` y NO continúes como si lo tuvieras. Un entregable con huecos honestos vale más que uno con cifras inventadas.


> **📊 Cierre en dashboard.** Cuando trabajes sobre un sitio, además de tu entrega persiste tu salida estructurada en `.seo-audit/<sitio>/data/issues.json` (esquema en la skill `dashboard-seo`). Al cerrar el flujo SEO, genera/actualiza el dashboard con `dashboard-seo` y entrega el URL local. Tu archivo: `issues.json` (+ `inventory-summary.json`, `prior-audits.json`).

# Auditoría Técnica SEO (Diploma W12 — 3 bloques)

Actúa como auditor técnico en aprendoseo. Filosofía del diploma: *"Lo que no se rastrea, no existe"* y *"Menos es más si es lo correcto"*. No optimizas páginas sueltas: **optimizas el contenedor** (la plantilla).

> **Método completo del diploma:** los pasos detallados, las plantillas y los prompts originales de Arianna están en [`references/metodo-diploma.md`](references/metodo-diploma.md). Lee ese archivo para seguir el método exacto del curso; no improvises el método.

## Cuándo usar

- **Onboarding** de un proyecto nuevo (foto técnica inicial).
- **Caída de tráfico** orgánico sin causa de contenido evidente.
- **Revisión trimestral** o auditoría recurrente.
- Antes de una migración o rediseño.

## Entradas (qué te doy)

- **Dominio** y acceso a **Google Search Console** (idealmente).
- Lista de **plantillas** del sitio (home, categoría, producto/artículo, landing…).
- Export de crawl (**Screaming Frog**) si lo tienes, o URLs de muestra por plantilla.
- Opcional: PageSpeed Insights de URLs representativas.

## Datos (MCP opcional)

Funciona **sin MCP**: con Screaming Frog + GSC + revisión manual basta para los 3 bloques.

1. **Sin MCP (manual):**
   - Bloque 1: revisa **códigos de respuesta** (200/301/302/404), abre `dominio.com/robots.txt` (busca `Disallow: /`), revisa sitemap en GSC, usa el operador `site:dominio.com` y la etiqueta `meta robots`.
   - Bloque 2: corre **PageSpeed Insights** (LCP, INP, CLS) y filtra en Screaming Frog imágenes **>100 kb** → recomendar WebP.
   - Bloque 3: comprueba **HTTPS / contenido mixto** y `rel="canonical"` self-canonical.
2. **MCP de GSC `mcp-gsc` (GRATIS):** aporta cobertura/indexación e inspección de URLs en vivo desde Search Console (ver `../../MCP-SETUP.md`).
3. **Ahrefs MCP (PAGO — ideal aquí):** `mcp__claude_ai_Ahrefs__site-audit-projects` (proyecto), `...site-audit-issues` (issues por severidad), `...site-audit-page-explorer` (filtrar por plantilla/segmento), `...site-audit-page-content`. Para cobertura/rendimiento real: `...gsc-pages`, `...gsc-performance-history`. Ahrefs es de pago.
3. **SerpApi MCP (GRATIS — limitado aquí):** `mcp__serpapi__search` solo sirve para validar indexación con `site:` u observar la SERP; **no audita técnica**.

**Inventario de URLs (opcional, automático):** si el usuario no pasó el export de URLs, usa la skill `inventario-de-urls` para extraerlas — por **sitemap (cero instalación)** o con **Screaming Frog CLI** (gratis), que además trae códigos de estado e indexabilidad para los 3 bloques. El tope gratis de SF es de **500 URLs por rastreo, no por sitio**: para sitios grandes, `inventario-de-urls/scripts/sf_crawl_all.py` trocea en lotes de ≤500 y junta los CSV, cubriendo todo el sitio sin licencia.

Config de MCP: ver `../../MCP-SETUP.md`.

## Proceso

**Bloque 1 — Indexabilidad / Rastreabilidad**
1. Códigos de respuesta: mapea **200 OK**, **301/302** (¿redirecciones correctas?), **404** (rotas).
2. `robots.txt`: confirma que **no haya `Disallow: /`** ni bloqueos accidentales de recursos.
3. Sitemap: enviado y sin errores en GSC; coincide con lo indexable.
4. `site:dominio.com`: ¿cuántas URLs indexadas vs esperadas?
5. `meta robots`: detecta `noindex` no deseados.

**Bloque 2 — Velocidad / Core Web Vitals**
6. Mide **LCP**, **INP** (sustituye al antiguo FID) y **CLS**. Para una URL suelta, PageSpeed Insights. Para **todo el sitio agrupado por plantilla**, delega en la skill **`analisis-rendimiento`** (Unlighthouse corre Lighthouse en cada ruta y deja `performance.json`); recuerda que son datos de **laboratorio** (el veredicto oficial de Google es de campo/CrUX).
7. Imágenes **>100 kb** (Screaming Frog) → convertir a **WebP**.
8. **Audita por plantillas, no página por página**: arregla el contenedor y propagas el fix.

**Bloque 3 — Seguridad + Canonicalización**
9. **HTTPS** activo y sin **contenido mixto** (recursos http en página https).
10. `rel="canonical"` **self-canonical** correcto; sin canonicals cruzados raros.
11. Clasifica cada issue por **severidad** (Crítico / Alto / Medio / Bajo) y **por plantilla**.
12. Vuelca todo en la pestaña **Auditoría** de la Plantilla Master.

## Salida

- **Informe de auditoría** estructurado en los 3 bloques.
- Tabla de **issues por severidad y por plantilla** (no por URL suelta).
- **Plan de remediación** priorizado (qué arreglar primero y en qué plantilla).
- Registro en la pestaña **"Auditoría"** de la Plantilla Master; tareas → Trello.

## Ejemplo

| Bloque | Issue | Plantilla | Severidad | Acción |
|---|---|---|---|---|
| 1 | `Disallow: /blog/` en robots.txt | Artículo | Crítico | Quitar regla; reindexar |
| 1 | 38 URLs 404 enlazadas | Producto | Alto | 301 a equivalente |
| 2 | LCP 4.8s (hero sin optimizar) | Categoría | Alto | Comprimir hero a WebP en el contenedor |
| 3 | Contenido mixto (img http) | Home | Medio | Servir recursos por https |

## Script determinista (ahorro de tokens)

Si Python 3 está disponible, **ejecuta el script** para resumir el crawl: es determinista, ahorra tokens y evita leer CSV enormes en contexto. Usa su JSON como base del informe de severidad.

Ejecuta (cero instalación, resuelve deps solo):

```
# con export de Screaming Frog (preferido):
uv run skills/auditoria-tecnica/scripts/parse_sf.py --folder ./export_sf
# o, si no usas uv: python3 skills/auditoria-tecnica/scripts/parse_sf.py --folder ./export_sf
# o apuntando a archivos sueltos:
uv run skills/auditoria-tecnica/scripts/parse_sf.py --internal internal_all.csv --issues issues_overview_report.csv
```

Corre con `--help` para ver opciones. Salida: `{"ok":true,"urls_total":N,"status_codes":{...},"non_indexable":N,"by_template_hint":{...},"issues":[{"issue","severity_hint","count"}],"missing_files":[...]}`. Solo stdlib.

Si NO hay export de SF, usa el fallback en vivo (necesita `requests`):

```
uv run skills/auditoria-tecnica/scripts/http_checks.py --file urls.txt --cap 200 --concurrency 8
# o, si no usas uv: python3 skills/auditoria-tecnica/scripts/http_checks.py --file urls.txt --cap 200 --concurrency 8
```

Salida: `{"ok":true,"checked":N,"results":[{"url","status","https","redirect_to"}],"summary":{...}}`. Si falta `requests` devuelve `{"ok":false,"reason":...,"fallback":...}` (exit 0) → **modo manual**: revisa status/HTTPS con Screaming Frog o a mano.

**Data on-page de URLs que un crawler no pudo leer (Shopify/WAF) — `onpage_extract.py`:** cuando SF (u otro crawler con UA de bot) es rate-limitado y devuelve 4xx falsos, no llega a parsear el HTML, así que faltan **title, meta description, canonical, encabezados, robots, hreflang**. Este script las recupera bajando el HTML con **UA de navegador real + throttle** y parseando on-page:

```
uv run skills/auditoria-tecnica/scripts/onpage_extract.py --file urls.txt --concurrency 4 --csv onpage.csv
```

Salida: `{"ok":true,"checked":N,"results":[{"url","status","title","meta_description","meta_robots","canonical","self_canonical","h1","h2_count","hreflang","lang","word_count","indexability","indexability_status",...}]}`. Recupera la capa **on-page por URL**; NO calcula inlinks/grafo/profundidad (eso requiere un crawl). `sf_crawl_all.py` lo invoca solo en sitios Shopify para enriquecer las URLs recuperadas (deja `onpage_enriched.json`).

## Gotchas

- **Audita POR PLANTILLAS, no página por página** — un fallo de plantilla afecta a TODAS sus instancias; arreglas el contenedor y propagas el fix. Página por página = trabajo infinito.
- **Primero rastreo/indexación (lo que no se rastrea no existe), después velocidad** — no optimices CWV de páginas que Google ni siquiera puede indexar. Bloque 1 antes que Bloque 2.
- **El CLI de Screaming Frog es GRATIS hasta 500 URLs** — no asumas que necesitas licencia; solo hace falta para >500 URLs, config guardada, render JS, scheduling o API.
- **Si SF aborta con `FATAL - You do not have sufficient disk space`** — por defecto usa almacenamiento en base de datos y exige **4 GB de disco libre**. En equipos con disco justo, cambia a **modo memoria/RAM**: `storage.mode=MEMORY` en `~/.ScreamingFrogSEOSpider/spider.config` (o GUI `Configuration > System > Storage Mode > Memory Storage`) y relanza. Para ≤500 URLs el modo memoria sobra. Detalle en `../../SCREAMING-FROG.md`.
- **4xx masivos en una tienda Shopify (o sitio con WAF) = rate-limit, NO roturas** — SF usa UA de bot y Shopify lo bloquea con 4xx/429/430 falsos. Antes de reportar páginas rotas, **revalida con UA de navegador real**: `http_checks.py` (concurrencia baja) o deja que `sf_crawl_all.py` lo haga solo (detecta Shopify y revalida). Solo las URLs que sigan 4xx tras revalidar son roturas reales. Caso real: una tienda Shopify marcó cientos de 4xx en el crawl inicial → solo una fracción eran roturas reales tras revalidar. Detalle en `../../SCREAMING-FROG.md`.
- **El status corregido NO trae la data on-page** — revalidar solo arregla el código; canonical/title/metas/encabezados de esas URLs siguen vacíos porque SF nunca parseó su HTML. Recupéralos con `onpage_extract.py` (UA real + throttle); `sf_crawl_all.py` ya lo hace automático en Shopify y deja `onpage_enriched.json`. El grafo de inlinks/profundidad de un Shopify solo lo da SF con licencia.
- **No inventes datos de un bloque sin export — márcalo incompleto** — si no hay crawl/GSC para un bloque, dilo explícito; no rellenes con suposiciones.
- **No confundas INP con FID:** FID está deprecado; mide **INP**.
- **Canonical cruzado** mal puesto consolida señales en la URL equivocada; usa self-canonical.
- **Reportar issues sin severidad ni plan = informe inútil.** Prioriza por impacto.
- **Imágenes pesadas = causa #1 de LCP malo:** filtra **>100 kb** y pasa a WebP.
