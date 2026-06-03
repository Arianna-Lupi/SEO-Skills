---
name: auditoria-tecnica
description: Ejecuta una auditoría SEO técnica completa en los 3 bloques del diploma "De Cero a SEO" (indexabilidad, velocidad/CWV, seguridad+canonical). Usá esta skill cuando haya que revisar la salud técnica de un sitio — AUNQUE el usuario no diga "auditoría técnica", p.ej. "se me cayó el tráfico y no sé por qué", "Google no me indexa", "el sitio carga lento / CWV en rojo", "voy a migrar/rediseñar", "revisá robots.txt / canonical / sitemap", u onboarding de proyecto nuevo y revisiones trimestrales. Audita POR PLANTILLAS, no página por página, y entrega issues por severidad con plan de remediación.
compatibility: Scripts opcionales: resumen de crawl (stdlib, Python 3 vía uv) y http_checks en vivo (requiere `requests`); si no, modo manual. Screaming Frog CLI (gratis hasta 500 URLs), GSC MCP (gratis) y Ahrefs MCP (pago) opcionales.
metadata:
  author: aprendoseo
  milestone: SEO skills (De Cero a SEO)
  version: "1.0"
---

# Auditoría Técnica SEO (Diploma W12 — 3 bloques)

Actúa como auditor técnico en aprendoseo. Filosofía del diploma: *"Lo que no se rastrea, no existe"* y *"Menos es más si es lo correcto"*. No optimizas páginas sueltas: **optimizas el contenedor** (la plantilla).

> **Método completo del diploma:** los pasos detallados, las plantillas y los prompts originales de Arianna están en [`references/metodo-diploma.md`](references/metodo-diploma.md). Leé ese archivo para seguir el método exacto del curso; no improvises el método.

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

**Inventario de URLs (opcional, automático):** si el usuario no pasó el export de URLs, usa la skill `inventario-de-urls` para extraerlas — por **sitemap (cero instalación)** o con **Screaming Frog CLI (GRATIS hasta 500 URLs; licencia solo para >500 URLs / config guardada / render JS / scheduling / API)**, que además trae códigos de estado e indexabilidad para los 3 bloques. aprendoseo ya tiene esto resuelto gratis en la herramienta interna `technical-audit`.

Config de MCP: ver `../../MCP-SETUP.md`.

## Proceso

**Bloque 1 — Indexabilidad / Rastreabilidad**
1. Códigos de respuesta: mapea **200 OK**, **301/302** (¿redirecciones correctas?), **404** (rotas).
2. `robots.txt`: confirma que **no haya `Disallow: /`** ni bloqueos accidentales de recursos.
3. Sitemap: enviado y sin errores en GSC; coincide con lo indexable.
4. `site:dominio.com`: ¿cuántas URLs indexadas vs esperadas?
5. `meta robots`: detecta `noindex` no deseados.

**Bloque 2 — Velocidad / Core Web Vitals**
6. Mide **LCP**, **INP** (sustituye al antiguo FID) y **CLS** con PageSpeed Insights.
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

Si Python 3 está disponible, **ejecutá el script** para resumir el crawl: es determinista, ahorra tokens y evita leer CSV enormes en contexto. Usá su JSON como base del informe de severidad.

Ejecutá (cero instalación, resuelve deps solo):

```
# con export de Screaming Frog (preferido):
uv run skills/auditoria-tecnica/scripts/parse_sf.py --folder ./export_sf
# o, si no usás uv: python3 skills/auditoria-tecnica/scripts/parse_sf.py --folder ./export_sf
# o apuntando a archivos sueltos:
uv run skills/auditoria-tecnica/scripts/parse_sf.py --internal internal_all.csv --issues issues_overview_report.csv
```

Corré con `--help` para ver opciones. Salida: `{"ok":true,"urls_total":N,"status_codes":{...},"non_indexable":N,"by_template_hint":{...},"issues":[{"issue","severity_hint","count"}],"missing_files":[...]}`. Solo stdlib.

Si NO hay export de SF, usá el fallback en vivo (necesita `requests`):

```
uv run skills/auditoria-tecnica/scripts/http_checks.py --file urls.txt --cap 200 --concurrency 8
# o, si no usás uv: python3 skills/auditoria-tecnica/scripts/http_checks.py --file urls.txt --cap 200 --concurrency 8
```

Salida: `{"ok":true,"checked":N,"results":[{"url","status","https","redirect_to"}],"summary":{...}}`. Si falta `requests` devuelve `{"ok":false,"reason":...,"fallback":...}` (exit 0) → **modo manual**: revisá status/HTTPS con Screaming Frog o a mano.

## Gotchas

- **Auditá POR PLANTILLAS, no página por página** — un fallo de plantilla afecta a TODAS sus instancias; arreglás el contenedor y propagás el fix. Página por página = trabajo infinito.
- **Primero rastreo/indexación (lo que no se rastrea no existe), después velocidad** — no optimices CWV de páginas que Google ni siquiera puede indexar. Bloque 1 antes que Bloque 2.
- **El CLI de Screaming Frog es GRATIS hasta 500 URLs** — no asumas que necesitás licencia; solo hace falta para >500 URLs, config guardada, render JS, scheduling o API.
- **No inventes datos de un bloque sin export — marcalo incompleto** — si no hay crawl/GSC para un bloque, decilo explícito; no rellenes con suposiciones.
- **No confundas INP con FID:** FID está deprecado; medí **INP**.
- **Canonical cruzado** mal puesto consolida señales en la URL equivocada; usá self-canonical.
- **Reportar issues sin severidad ni plan = informe inútil.** Prioriza por impacto.
- **Imágenes pesadas = causa #1 de LCP malo:** filtrá **>100 kb** y pasá a WebP.
