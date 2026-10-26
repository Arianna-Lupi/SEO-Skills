# Changelog, grupo A: SEO técnico

Base: Semana 3 y Semana 12 del diplomado, práctica de coaches (Juan Angulo, `data/voice-profile.md`; Vero, Diana) y complementos de claude-seo (MIT, agricidaniel). Todo lo de claude-seo vive en `references/complementos-claude-seo.md` de cada skill y se referencia en `SKILL.md` como opcional, después del método.

## Skills mejoradas (versión 1.0 a 1.1)

### auditoria-tecnica
- Pasos nuevos en el Bloque 1: brecha `site:` y señal de basura indexada (S3 · "Cómo aparecer en Google"), prueba SSR vs CSR con "ver código fuente + Ctrl+F" (S3 · "Cómo funciona Google" y práctica de Juan), regla de 3 clics (S3 · estructuración), delegación a `sitemap-y-robots`. Bloque 2 delega imágenes en `optimizacion-de-imagenes`.
- Paso de paginación (canonical a la principal, no autocanónica; práctica de Juan) y paso 13: tareas con verbo, explainer, evidencia, ICE, listas de URLs en Sheet y ticket para developer (S13 · "El Rol del SEO Técnico"; práctica de coaches).
- `references/metodo-diploma.md` ampliado con lecciones de S3, S13 y práctica de coaches (realizable según CMS, Screaming Frog vs GSC, HTTP vs HTTPS, caché).
- `references/complementos-claude-seo.md` (nuevo): umbrales CWV vigentes con INP, cabeceras de seguridad (con severidad baja a media y la aclaración de que solo HTTPS es señal confirmada), cadenas de redirección, casos límite de renderizado JS (canonical y noindex en crudo vs inyectado, no render en no-200, límite de 2 MB), paginación, bots de IA (remite a `sitemap-y-robots`), rúbrica de severidad y puntaje. Origen: `skills/seo-technical/SKILL.md` y `skills/seo-drift/references/comparison-rules.md`.
- Scripts nuevos (stdlib): `chequeos_tecnicos.py` (redirecciones, cabeceras de seguridad, X-Robots-Tag, canonical, noindex, contenido mixto, SSR/CSR; idea de `fetch_page.py` y `seo-technical`), `puntaje_salud.py` (puntaje 0 a 100 desde `issues.json`, rúbrica propia), `comparar_corridas.py` (diff de `onpage_extract.py` o `issues.json`; idea de `drift_baseline.py`/`drift_compare.py`).
- Evals: 2 casos nuevos (CSR para developer; comparar corridas) y 1 consulta de disparo.
- Gotchas nuevos: realizable según CMS, 404 solo visibles en Screaming Frog, explainer y evidencia obligatorios.

### analisis-rendimiento
- Nuevo `references/metodo-diploma.md` (S12 · "Velocidad y rendimiento", S3 · herramientas, prompt oficial y práctica de Juan con Unlighthouse/PageSpeed).
- Nuevo `references/complementos-claude-seo.md`: umbrales LCP 2,5 s / INP 200 ms / CLS 0,1 con rangos intermedios y malo, INP vs FID, tabla de causas probables por métrica. Origen: `skills/seo-technical/SKILL.md` (sección CWV), `pagespeed_check.py`, `crux_history.py`.
- Script nuevo `psi_campo.py` (stdlib): consulta la API de PageSpeed para datos de campo (CrUX). Exige `--confirmo` porque envía las URLs a Google; sin ello devuelve modo manual.
- `SKILL.md`: tareas ejecutables (verbo, explainer, ICE), nota de hero con lazy, umbrales. Evals nuevos (3 casos).

### inventario-de-urls
- Nuevo `references/metodo-diploma.md` (S5 · "Cómo obtener las URLs de un sitio web", S3 sitemap y `site:`, práctica de Vero, Ibra y Juan: Spider vs sitemap, índices por partes, Octopus).
- `references/complementos-claude-seo.md`: límites de 50.000 URLs/50 MB, calidad de sitemap (sin redirigidas, noindex ni canonicalizadas), lastmod fiable, no declarar "no hay sitemap" sin probar alternativas. Origen: `seo-sitemap`, `sitemap_discovery.py`.
- `inventario_urls.py`: descomprime `.xml.gz`, prueba 5 rutas alternativas (incluye `wp-sitemap.xml`), devuelve `sitemaps_read` con el conteo por archivo.
- `SKILL.md`: entrega en Sheet, cruce con `site:`, gotchas (una sola URL en Screaming Frog = modo lista).

## Skills nuevas (versión 1.0)

### sitemap-y-robots
- Base en el diplomado: S3 · "Cómo funciona Google", "Cuáles son las herramientas" y "Cómo aparecer en Google"; S12 · "Indexabilidad y rastreabilidad"; S13 · "El Rol del SEO Técnico" (ticket al developer). No hay una lección única de estos archivos, por eso `metodo-diploma.md` junta las cuatro.
- Criterio de coaches (Juan): robots.txt es una guía y no una barrera, sitios con código necesitan sitemap/robots generados por developer, probar en technicalseo.com, Cloudflare bloquea bots de IA, Rank Math/Yoast en WordPress, Shopify (robots editable, sitemap no), Octopus IA inventa el mapa.
- Complemento claude-seo (`seo-sitemap`, `seo-technical`, agente `seo-sitemap`): validación de límites, lastmod, tags obsoletos, sitemaps de imagen/video/noticias, barreras para páginas a escala, tabla de bots de IA con aclaraciones (Google-Extended no afecta a Search), descubrimiento con casos límite.
- Scripts: `revisar_robots_sitemap.py` (intérprete robots con comodines, estado por bot de IA, `--probar`, lectura de índices y gz, muestra con status/noindex/canonical, no rastrea lo que robots bloquea, ritmo lento) y `generar_sitemap_robots.py` (no inventa fechas, parte a 50.000, `--ia`).
- Evals: 5 casos y 12 consultas. Fixtures de prueba en `fixtures/`.

### optimizacion-de-imagenes
- Base en el diplomado: S12 · "Velocidad y rendimiento" (100 kb, WebP, ALT, dimensiones, acción de Trello), S1, S10, S11 (nombre amistoso + ALT), S14 (alt en producto).
- Práctica de coaches: Squoosh, Shopify no admite WebP/AVIF, verificación de `loading=lazy`, prioridad (pesadas alta, alt baja), tablas en HTML.
- Complemento claude-seo (`seo-images`): umbrales por tipo, AVIF y `<picture>`, srcset, `fetchpriority`, `decoding`, CLS con width/height, detección de lazy por JS.
- Script `auditar_imagenes.py` (stdlib): peso real por HEAD, formato, alt, dimensiones, lazy en la imagen principal, nombres de archivo; respeta robots.txt.
- Evals: 4 casos y 11 consultas.

## Ideas descartadas o pendientes

- **monitoreo-de-cambios (seo-drift): NO se crea como skill.** El diplomado solo enseña monitoreo vía Search Console y el reporte "mes actual vs mes anterior" (S12 · "¿Cómo empezar un informe SEO?" y "Cómo hacer un reporte SEO", S13 · rol del SEO técnico). No enseña línea base de elementos de página. Lo útil se incorporó como complemento en `auditoria-tecnica` (`comparar_corridas.py` y sección 8 del complemento). Si el curso añade el tema, se puede promover a skill.
- **hreflang e internacionalización:** idea para el futuro, no está en el diplomado. No se creó skill (referencia: `seo-hreflang` de claude-seo).
- **IndexNow, llms.txt, Agent-UX/WebMCP, back-button hijacking, Search Console/GA4 por API, DataForSEO:** no son parte del curso y envían datos a terceros o requieren cuentas de pago. Solo se mencionan en los complementos.

## Para el agente principal (README, ROADMAP, FUENTES, install)

- README/ROADMAP: añadir 2 skills nuevas (`sitemap-y-robots`, `optimizacion-de-imagenes`), versiones 1.1 de las tres existentes, y 7 scripts nuevos (`chequeos_tecnicos.py`, `puntaje_salud.py`, `comparar_corridas.py`, `psi_campo.py`, `revisar_robots_sitemap.py`, `generar_sitemap_robots.py`, `auditar_imagenes.py`).
- FUENTES: citar claude-seo (MIT) para `seo-technical`, `seo-sitemap`, `seo-images`, `seo-drift`, `pagespeed_check.py`, `sitemap_discovery.py`.
- install.sh/install.ps1: copiar las dos carpetas nuevas. `tests/`: considerar pruebas para los scripts nuevos (fixtures en `skills/sitemap-y-robots/fixtures` y `skills/optimizacion-de-imagenes/fixtures`).
- `agents/agente-auditoria-tecnica.md`: puede invocar `sitemap-y-robots` y `optimizacion-de-imagenes` en los bloques 1 y 2.
- `dashboard-seo`: archivos nuevos en `.seo-audit/<sitio>/data/`: `chequeos-tecnicos.json`, `comparacion.json`, `cwv-campo.json`, `sitemap-robots.json`, `imagenes.json` (el dashboard actual no los lee).
- COMPLIANCE: `psi_campo.py` envía URLs a la API de Google solo con `--confirmo`.
