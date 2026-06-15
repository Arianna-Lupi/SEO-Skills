---
name: analisis-rendimiento
description: Analiza el RENDIMIENTO de TODO un sitio con Unlighthouse (corre Lighthouse en cada ruta única, no página por página) y entrega scores de performance/accesibilidad/best-practices/SEO + Core Web Vitals de laboratorio (LCP, CLS, TBT, FCP, Speed Index), peores páginas y rendimiento por plantilla. Usa esta skill cuando el foco sea velocidad/CWV de un sitio entero — AUNQUE el usuario no diga "Unlighthouse" ni "Lighthouse", p.ej. "el sitio carga lento", "tengo los CWV en rojo", "cuánto tarda en cargar mi web", "mídeme el rendimiento de todas las páginas", "qué páginas son las más lentas", "PageSpeed me da mal", o como Bloque 2 (velocidad) de una auditoría técnica. Mide datos REALES; nunca los inventa.
compatibility: Script vía Python 3 (uv), solo stdlib. Para rastrear en vivo necesita Node.js/npx (Unlighthouse se baja solo con npx la 1ª vez); si no hay Node, modo manual con PageSpeed Insights o parseo de un ci-result.json ya exportado (`--json`). Sin claves ni red propia.
metadata:
  author: aprendoseo
  milestone: SEO skills (De Cero a SEO)
  version: "1.0"
---

> **🚫 Regla de datos (obligatoria): NUNCA inventes números.**
> Esta skill SOLO reporta mediciones reales de Lighthouse/Unlighthouse. No estimes ni supongas scores, LCP, CLS, TBT ni ningún CWV. Si no puedes ejecutar el scan (sin Node) ni te pasan un export, **pídele al usuario los números de PageSpeed Insights** (1 URL por plantilla) y vuélcalos a mano, o márcalo `pendiente de dato`. Mejor una sección honesta vacía que una métrica falsa.

> **⚠️ Laboratorio ≠ campo.** Los CWV de Lighthouse/Unlighthouse son datos de **laboratorio** (entorno simulado), perfectos para diagnosticar y priorizar fixes. El **aprobado/suspenso oficial** de Google usa datos de **campo** (CrUX / Search Console). Dilo siempre: el dashboard ya lo deja explícito en `note`.

> **📊 Cierre en dashboard.** Persiste tu salida en `.seo-audit/<sitio>/data/performance.json` (esquema en la skill `dashboard-seo`). Al cerrar el flujo SEO, genera/actualiza el dashboard con `dashboard-seo` y entrega el URL local.

# Análisis de rendimiento (Unlighthouse — sitio completo)

Actúa como especialista de rendimiento en aprendoseo. Filosofía del diploma: **audita por PLANTILLAS, no página por página** — Unlighthouse encaja perfecto porque rastrea el sitio y corre Lighthouse en cada ruta única, así ves qué *contenedor* (home, categoría, artículo, landing) está lento y arreglas una vez para propagar el fix.

Esto cubre el **Bloque 2 (Velocidad / Core Web Vitals)** de la `auditoria-tecnica` con datos reales de todo el sitio, en vez de mirar PageSpeed Insights URL por URL.

## Cuándo usar

- El sitio **carga lento** o los **CWV están en rojo** y hay que ubicar dónde.
- Quieres el rendimiento de **todas las páginas** (no una suelta) agrupado por plantilla.
- **Antes/después** de un fix de velocidad o de una migración (comparar corridas).
- Como **Bloque 2** de una auditoría técnica completa.

## Entradas (qué te doy)

- **URL del sitio** (con `https://`). Unlighthouse descubre rutas por sitemap/robots/crawl.
- Opcional: si ya corriste Unlighthouse, su **`ci-result.json`** para parsearlo sin volver a rastrear (`--json`).
- Opcional: estrategia **móvil** o escritorio, y un **límite de rutas** para sitios grandes.

## Datos (sin MCP)

No necesita ninguna API ni clave. Unlighthouse es open source y corre local con `npx`.

- **Con Node.js:** el script lo ejecuta solo (`npx -y unlighthouse-ci`), mide cada ruta y agrega.
- **Sin Node.js (manual):** pide al usuario PageSpeed Insights (https://pagespeed.web.dev/) de **1 URL por plantilla** (home, categoría, artículo/producto, landing) con LCP/INP/CLS + score, y vuélcalo a mano a `performance.json`. Nunca inventes los números.
- **Datos de campo reales:** si el usuario los tiene, el MCP de **GSC** (`mcp-gsc`, GRATIS) y Ahrefs aportan CWV de campo (CrUX); esos sí son el veredicto de Google. Esta skill da laboratorio; el de campo se marca aparte.

## Proceso

1. **Confirma la URL** del sitio y si quieres móvil o escritorio (Google prioriza móvil).
2. Para sitios grandes, acota con `--max-routes` (evita scans eternos; dilo si recortas).
3. **Ejecuta el scan** (script de abajo). Unlighthouse rastrea + corre Lighthouse por ruta.
4. **Lee el `performance.json`** generado: scores medios, CWV de laboratorio, peores páginas y rendimiento por plantilla.
5. **Diagnostica por plantilla:** identifica el contenedor más lento (p.ej. "Artículo" con LCP 4.8s) y la causa probable (hero sin optimizar, JS de terceros, imágenes >100 kb → WebP, CLS por fuentes/anuncios sin reserva de espacio).
6. **Prioriza** por impacto × páginas afectadas (arreglar la plantilla con más instancias y peor score primero).
7. **Cierra en dashboard** (`dashboard-seo`) y entrega el URL local.

## Salida

- **`performance.json`** en `.seo-audit/<sitio>/data/` con: `summary` (páginas, performance/accesibilidad/best-practices/SEO medios + `issues_found`), `core_web_vitals` (LCP/CLS/TBT/FCP/Speed Index medios, de laboratorio), `cwv_pages_failing`, `worst_pages` (top 10 más lentas), `by_template_hint` e **`issues`** — la lista de TODOS los audits de Lighthouse que no pasan (errores y oportunidades), con `id`, `title`, `severity`, `pages_affected`, `worst_score`, ahorro estimado (`avg_savings_ms`/`max_savings_kb`) y `examples`.
- **Reporte final con la lista completa de errores** ordenada por impacto (páginas afectadas × severidad), para ir arreglando uno a uno. Los audits-métrica (LCP, TBT, Speed Index…) NO se listan como errores: ya van en CWV.
- **Diagnóstico por plantilla** con causa probable y fix recomendado, priorizado.
- Todo renderizado en el **dashboard** (sección ⚡ Rendimiento + tabla 🐞 Errores y oportunidades) con colores por umbral/severidad.

> **🧹 Limpieza de recursos.** Al terminar el scan y entregar el reporte, **cierra el dashboard** (`pkill -f "http.server"`) y mata cualquier Chrome headless colgado de Unlighthouse (`pkill -f "Chrome for Testing"; pkill -f unlighthouse`) para no consumir CPU/RAM de fondo. El usuario puede re-servir el dashboard cuando quiera con el `serve_cmd`.

## Ejemplo

| Plantilla | Páginas | Performance media | Causa probable | Fix |
|---|---|---|---|---|
| Artículo | 42 | 48 | Hero sin optimizar (LCP 4.8s) | Comprimir hero a WebP en el contenedor |
| Categoría | 12 | 61 | JS de terceros bloqueante (TBT 410ms) | Diferir/quitar scripts no críticos |
| Home | 1 | 78 | CLS 0.21 (fuente sin `font-display`) | Reservar espacio + `font-display:swap` |

> Datos de laboratorio. Para el veredicto oficial, contrasta con CrUX/Search Console.

## Script determinista (ahorro de tokens)

`scripts/run_unlighthouse.py` — ejecuta Unlighthouse vía npx, parsea su JSON (de forma defensiva; el esquema cambia entre versiones) y escribe `performance.json` con el esquema del dashboard. Solo stdlib; Node/npx solo hace falta para rastrear en vivo.

Ejecuta (cero instalación de Python, resuelve deps solo):

```
# rastrear y medir un sitio entero (baja Unlighthouse con npx la 1ª vez):
uv run skills/analisis-rendimiento/scripts/run_unlighthouse.py --site https://ejemplo.com
# o sin uv:
python3 skills/analisis-rendimiento/scripts/run_unlighthouse.py --site https://ejemplo.com

# emular móvil y acotar a 40 rutas (sitios grandes):
uv run skills/analisis-rendimiento/scripts/run_unlighthouse.py --site https://ejemplo.com --mobile --max-routes 40

# parsear un ci-result.json que ya tengas (sin volver a rastrear):
uv run skills/analisis-rendimiento/scripts/run_unlighthouse.py --site https://ejemplo.com --json .unlighthouse/ci-result.json
```

Corre con `--help` para ver opciones (`--slug`, `--throttle`, `--keep`, `--root`).

Salida OK: `{"ok":true,"written":"...","pages_scanned":N,"avg_performance":0-100,"avg_seo":...,"cwv_pages_failing":{...},"hint":"..."}`.
Si falta Node/npx o falla el scan: `{"ok":false,"reason":...,"fallback":"manual","manual":"..."}` (exit 0) → **modo manual** con PageSpeed Insights (pide los números, no los inventes).

## Gotchas

- **Laboratorio ≠ campo.** Nunca digas que el sitio "aprueba/suspende" CWV de Google con estos datos: eso es campo (CrUX/GSC). Esto diagnostica, no dictamina.
- **Audita POR PLANTILLAS** — usa `by_template_hint` y `worst_pages` para hallar el contenedor lento; arregla el contenedor, no cada URL.
- **Sitios grandes = scans lentos.** Acota con `--max-routes` y avisa al usuario que recortaste (no es "todo el sitio" si limitaste).
- **Móvil primero.** Google indexa mobile-first; corre `--mobile` salvo que el sitio sea solo escritorio.
- **Necesita Node solo para rastrear.** Sin Node, no falla en silencio: pasa a modo manual (PageSpeed Insights) o parsea un export con `--json`.
- **No confundas INP con FID/TBT.** Lighthouse de laboratorio no mide INP directamente (es de campo); el **TBT** es su mejor proxy. Si necesitas INP real, es dato de campo (CrUX).
- **`.seo-audit/` va en `.gitignore`** (datos del cliente). El `--keep` guarda la salida cruda de Unlighthouse; bórrala antes de compartir.
- **Imágenes pesadas = causa #1 de LCP malo.** Cruza con el filtro de imágenes >100 kb de `auditoria-tecnica` → WebP.
