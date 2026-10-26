# Comandos de `/aprendoclub`

`/aprendoclub` es el enrutador de las SEO Skills: decide qué skill o agente hace cada trabajo, en qué orden y con qué pausas. Todas las skills siguen funcionando por su nombre (`/auditoria-tecnica`) y por lenguaje natural ("audita mi web"). Sin comando, o con `/aprendoclub help`, muestra el menú.

Reglas que valen para todos los comandos:

- El método es el del diplomado "De Cero a SEO". Lo que viene de claude-seo (MIT) va aparte y etiquetado como complemento.
- Nunca se inventan números: lo que falta se pide, o queda como `pendiente de dato`.
- Todo comando que trabaja sobre un sitio termina con `dashboard-seo` y te da el URL local.
- Los datos se guardan en `.seo-audit/<sitio>/data/*.json` (carpeta que no se sube a git).
- Antes de correr un script se revisa lo que necesita. Si falta un paquete, se te pregunta antes de instalarlo; si falta una clave, se te pide (una sola vez). Ver [Requisitos y claves](#requisitos-y-claves).

## Auditoría completa

### `/aprendoclub audit <sitio>`
- **Qué ejecuta:** 9 fases del diplomado, con pausas para que confirmes y subagentes en paralelo cuando las tareas son independientes. 0 descubrimiento (tipo de negocio, CMS, accesos); 1 técnico (`inventario-de-urls`, luego en paralelo `sitemap-y-robots`, `auditoria-tecnica`, `analisis-rendimiento`, `optimizacion-de-imagenes`, `schema-jsonld`); 2 arquitectura (`arquitectura-y-enlazado-interno`); 3 keywords y contenido (`investigacion-de-keywords`, luego `mapa-de-palabras-clave`, `intencion-de-busqueda`, `deteccion-de-canibalizacion`, `calidad-de-contenido-eeat`); 4 competencia (`analisis-serp-y-competencia`, `analisis-de-competidores`); 5 GEO y off page (`optimizacion-geo-aeo`, `auditoria-de-backlinks-toxicos`); 6 vertical (`seo-local`, `seo-ecommerce`); 7 plan (`plan-seo`, `proyeccion-seo-gsc`); 8 reporte (`reporte-seo-gsc`) y siempre `dashboard-seo`.
- **Ejemplo:** `/aprendoclub audit midominio.com`
- **Salidas:** `issues.json`, `performance.json`, `keywords.json`, `competitors.json`, `ai-features.json`, `next-steps.json` y más en `.seo-audit/<sitio>/data/`; puntaje de salud en `meta.json` (complemento de claude-seo, solo para comparar auditorías); dashboard local.
- **Sin accesos:** si no tienes Search Console, Ahrefs ni SerpApi, igual corre; los huecos quedan marcados.

## Técnico y arquitectura

### `/aprendoclub technical <sitio>`
- **Ejecuta:** `agente-auditoria-tecnica` (Semana 12). Para una duda puntual, `auditoria-tecnica`.
- **Ejemplo:** `/aprendoclub technical midominio.com`
- **Salidas:** `issues.json` por severidad y por plantilla, plan de remediación.

### `/aprendoclub sitemap <sitio>`
- **Ejecuta:** `inventario-de-urls` y `sitemap-y-robots`.
- **Ejemplo:** `/aprendoclub sitemap midominio.com`
- **Salidas:** `inventory-summary.json` y hallazgos de robots y sitemap.

### `/aprendoclub performance <sitio>`
- **Ejecuta:** `analisis-rendimiento` (Core Web Vitals de laboratorio de todo el sitio). Necesita Node solo para medir en vivo; sin Node, PageSpeed Insights a mano.
- **Ejemplo:** `/aprendoclub performance midominio.com`
- **Salidas:** `performance.json`.

### `/aprendoclub images <url>`
- **Ejecuta:** `optimizacion-de-imagenes`.
- **Ejemplo:** `/aprendoclub images https://midominio.com/producto`
- **Salidas:** hallazgos de peso, formato, ALT y lazy loading.

### `/aprendoclub schema <url>`
- **Ejecuta:** `schema-jsonld`.
- **Ejemplo:** `/aprendoclub schema https://midominio.com/blog/articulo`
- **Salidas:** bloque JSON-LD listo para pegar, validado.

### `/aprendoclub architecture <sitio>`
- **Ejecuta:** `arquitectura-y-enlazado-interno` (Semana 9).
- **Ejemplo:** `/aprendoclub architecture midominio.com`
- **Salidas:** mapa pilar a clusters, huérfanas y enlaces sugeridos.

## Keywords y contenido

### `/aprendoclub keywords <nicho o sitio>`
- **Ejecuta:** `agente-investigacion-keywords`, luego `mapa-de-palabras-clave`.
- **Ejemplo:** `/aprendoclub keywords "café de especialidad"`
- **Salidas:** `keywords.json`, `clusters.json`, las "10 de Oro".

### `/aprendoclub intent <keyword>`
- **Ejecuta:** `intencion-de-busqueda`.
- **Ejemplo:** `/aprendoclub intent "mejor cafetera para casa"`
- **Salidas:** intención y tipo de contenido que premia la SERP.

### `/aprendoclub content <url o keyword>`
- **Ejecuta:** con keyword, `agente-contenido` (SERP, brief, borrador, on-page). Con URL, `calidad-de-contenido-eeat` y `actualizacion-de-contenido`.
- **Ejemplo:** `/aprendoclub content "cómo preparar café"`
- **Salidas:** `content-briefs.json` y el borrador en `content/<slug>.html`.

### `/aprendoclub onpage <url>`
- **Ejecuta:** `optimizacion-on-page-meta`.
- **Ejemplo:** `/aprendoclub onpage https://midominio.com/servicios`
- **Salidas:** metatítulo, metadescripción, variantes y checklist.

### `/aprendoclub quality <url>`
- **Ejecuta:** `calidad-de-contenido-eeat`.
- **Ejemplo:** `/aprendoclub quality https://midominio.com/blog/cafe`
- **Salidas:** revisión de experiencia, autoría, confianza y profundidad.

### `/aprendoclub update <url>`
- **Ejecuta:** `actualizacion-de-contenido` (Semana 10). Con una URL es contenido; sin URL actualiza las skills (ver abajo).
- **Ejemplo:** `/aprendoclub update https://midominio.com/blog/cafe`
- **Salidas:** brief de optimización de la página.

## Competencia, GEO y off page

### `/aprendoclub competitors <keyword o sitio>`
- **Ejecuta:** `analisis-serp-y-competencia` (Ojo Clínico manual primero; luego `serp.py`, `perfil_competidor.py`, `comparar_serp.py`) y `analisis-de-competidores`.
- **Ejemplo:** `/aprendoclub competitors "comprar café de especialidad"`
- **Salidas:** `competitors.json` (con `serp_analysis`), informe de brechas con costo de oportunidad (puntaje relativo, no del diplomado) y tareas con ICE.

### `/aprendoclub geo <url>`
- **Ejecuta:** `optimizacion-geo-aeo`.
- **Ejemplo:** `/aprendoclub geo https://midominio.com`
- **Salidas:** `ai-features.json`.

### `/aprendoclub backlinks <sitio>`
- **Ejecuta:** `auditoria-de-backlinks-toxicos`; `link-building-y-outreach` solo si lo pides.
- **Ejemplo:** `/aprendoclub backlinks midominio.com`
- **Salidas:** `backlinks.json`, clasificación de dominios y `disavow.txt`.

## Verticales, plan y entrega

### `/aprendoclub local`
- **Ejecuta:** `seo-local`. **Ejemplo:** `/aprendoclub local`. **Salidas:** `local-seo.json`.

### `/aprendoclub ecommerce <sitio>`
- **Ejecuta:** `seo-ecommerce`. **Ejemplo:** `/aprendoclub ecommerce mitienda.com`. **Salidas:** `ecommerce.json`.

### `/aprendoclub plan <sitio>`
- **Ejecuta:** `plan-seo` (o `agente-plan-y-entrega` si también hay propuesta). **Ejemplo:** `/aprendoclub plan midominio.com`. **Salidas:** `next-steps.json`, `plan-seo.json`, Plantilla Master y briefs.

### `/aprendoclub project`
- **Ejecuta:** `proyeccion-seo-gsc`. Necesita Search Console. No es un método del diplomado ni una garantía. **Ejemplo:** `/aprendoclub project`. **Salidas:** `proyeccion-gsc.json`.

### `/aprendoclub report <sitio>`
- **Ejecuta:** `reporte-seo-gsc`, luego `dashboard-seo`. **Ejemplo:** `/aprendoclub report midominio.com`. **Salidas:** `search-console.json`.

### `/aprendoclub proposal`
- **Ejecuta:** `propuesta-y-reporte-de-servicios-seo`. **Ejemplo:** `/aprendoclub proposal`. **Salidas:** propuesta, paquetes y explainer.

### `/aprendoclub dashboard`
- **Ejecuta:** `dashboard-seo`. **Ejemplo:** `/aprendoclub dashboard`. **Salidas:** URL local con todo lo encontrado.

## Configuración y actualización

### `/aprendoclub setup`
- **Ejecuta:** `aprendoclub-run --status` y, para las claves, `configurar-serpapi`. Muestra Python, uv, paquetes, claves (solo si existen), herramientas y conectores, y ofrece resolver cada faltante con tu confirmación.
- **Ejemplo:** `/aprendoclub setup`
- **Salidas:** tabla de estado. No instala ni guarda nada sin tu sí.

### `/aprendoclub update` y `/aprendoclub upgrade`
- **Ejecuta:** compara tu versión instalada con la última (usa la red porque lo pides; avisa si no hay conexión), muestra las novedades de `CHANGELOG.md` y actualiza solo con tu confirmación. `--check` solo mira. Sin URL, `update` actualiza las skills; con URL es el comando de contenido.
- **Ejemplos:** `/aprendoclub update --check` · `/aprendoclub update`
- **Conserva:** `~/.claude/seo-skills.env`, `.seo-audit/` y lo que hayas creado. Si modificaste una skill a mano, se guarda una copia antes de sobrescribir.

### `/aprendoclub help`
- **Ejecuta:** muestra el menú. Es el comando por defecto.

## Requisitos y claves

Todo script se corre con el lanzador `aprendoclub-run` (en `skills/aprendoclub/scripts/`; `.ps1` en Windows):

```bash
aprendoclub-run --check serp.py        # ¿puedo correrlo? devuelve JSON con "needs"
aprendoclub-run --status               # estado general
aprendoclub-run --install serp.py --yes  # instala lo que falta, en un entorno aislado, solo si tú dijiste que sí
```

- Intérprete: `APRENDOCLUB_PYTHON`, luego `python3`, `python` o `py -3` (Python 3.9+).
- `needs` lista lo que falta: paquetes de Python (`requests`, `beautifulsoup4`, `tldextract`; `openpyxl` y `python-docx` opcionales), claves (`SERPAPI_API_KEY`, `CRUX_API_KEY`, `PSI_API_KEY`), herramientas (Node, Screaming Frog) y conectores MCP (Search Console, Ahrefs, Google Drive y Sheets).
- Si no hay nada de eso, cada skill sigue en modo manual.
- Detalle del contrato y de la seguridad: `skills/aprendoclub/references/dependencias.md`. El manifiesto es `skills/aprendoclub/requisitos.json`.
