# Roadmap

Estado y próximos pasos de las SEO skills (aprendoseo, "De Cero a SEO"). Issues en [GitHub](https://github.com/Arianna-Lupi/SEO-Skills/issues).

## Publicado

### Sin versión (develop), enrutador, instalación rápida y actualización
- **feat(aprendoclub):** skill enrutadora `/aprendoclub` con `audit <sitio>` (9 fases del diplomado, checkpoints, subagentes en paralelo y cierre en dashboard) y 25 subcomandos (`technical`, `content`, `keywords`, `competitors`, `architecture`, `onpage`, `schema`, `geo`, `sitemap`, `images`, `performance`, `intent`, `update`, `quality`, `backlinks`, `local`, `ecommerce`, `plan`, `project`, `report`, `proposal`, `dashboard`, `setup`, `upgrade`, `help`). Patrón del enrutador `/seo` de claude-seo (MIT) como complemento; el orden y los nombres son del diplomado. Comandos documentados en `docs/COMANDOS.md`.
- **feat(instalador):** `install.sh` e `install.ps1` reescritos: camino rápido por defecto (paquete comprimido sin git, sin preguntas, sin instalar dependencias), idempotente, `--dir`, `--full` para uv, `--interactive` para el menú antiguo. Nuevos `uninstall.sh` y `uninstall.ps1` que borran solo lo registrado en el manifiesto. Empaquetado como plugin de Claude Code (`.claude-plugin/plugin.json` y `marketplace.json`).
- **feat(actualizar):** actualizar es volver a correr el instalador; conserva claves y `.seo-audit/` y guarda copia de las skills modificadas a mano. `/aprendoclub update --check` compara versiones y muestra `CHANGELOG.md` (en español, para alumnos). `scripts/publicar_version.py` sube la versión y genera `docs/ANUNCIO-ACTUALIZACION.md` sin hacer commit, tag ni push.
- **feat(requisitos):** lanzador `aprendoclub-run` (bash y PowerShell) con manifiesto `requisitos.json`: antes de correr un script revisa Python, paquetes, claves y herramientas, devuelve `needs` en JSON, pregunta antes de instalar (entorno aislado, sin sudo) y pide las claves una sola vez. `validar_skills.py` comprueba que cada script esté en el manifiesto y que cada skill, agente y script que nombra el enrutador exista.
- **feat(competencia):** `analisis-serp-y-competencia` y `analisis-de-competidores` pasan a 1.2 con `perfil_competidor.py` y `comparar_serp.py` (detalle en `docs/changelog-fragments/F-competencia-serp.md`).
- **decisión:** las presentaciones para clientes dejan de planearse con Slidev y pasan a PPT Master (ver "Planificado").

### Sin versión (develop), ronda "diplomado primero + claude-seo"
- **feat(skills):** 10 skills nuevas, todas con base en el diplomado: `intencion-de-busqueda`, `actualizacion-de-contenido`, `calidad-de-contenido-eeat`, `sitemap-y-robots`, `optimizacion-de-imagenes`, `plan-seo`, `proyeccion-seo-gsc`, `seo-local`, `seo-ecommerce` y `propuesta-y-reporte-de-servicios-seo`. Las 20 existentes (incluidas `dashboard-seo` y `configurar-serpapi`) suben a 1.1 con pasos del diplomado, práctica de coaches, evals y scripts nuevos.
- **feat(plan):** `plan-seo` genera plan de contenidos, mapa, asignación 1 keyword por URL, calendario, la Plantilla Master (13 pestañas, `.xlsx` o CSV) y una carpeta de briefs; `proyeccion-seo-gsc` entrega escenarios con supuestos explícitos a partir de Search Console (no es un método del diplomado ni una garantía).
- **feat(agentes):** nuevo `agente-plan-y-entrega`; los 3 existentes encadenan las skills nuevas.
- **feat(dashboard):** secciones de Search Console, CWV de campo, schema, backlinks y rastreadores de IA (se ocultan sin datos).
- **fix(frontmatter):** `description` de skills y agentes con YAML inválido (dos puntos sin comillas): corregido sin cambiar el texto. Nuevo `scripts/validar_skills.py`.
- **fix(contenido):** el ejemplo del brief decía 134 caracteres de meta cuando eran 112; `brief_check.py` lo detecta.
- **docs:** `FUENTES.md` (claude-seo MIT, coaches, comunidad), `THIRD-PARTY-LICENSES.md`, y la regla "el diplomado manda".

### Sin versión (develop), canibalización
- **feat(canibalizacion):** skill `deteccion-de-canibalizacion` — diagnostica canibalización REAL (no la preventiva de `mapa-de-palabras-clave`) cruzando el rendimiento real por query+página de Google Search Console: agrupa por query, calcula cuánto se reparte el clic entre URLs (`dominance_ratio`) y clasifica severidad (Alta/Media/Bajo) con acción recomendada (fusionar+301, diferenciar intención o monitorear). Vuelca hallazgos a `.seo-audit/<sitio>/data/issues.json`.

### v1.3.0
- **feat(rendimiento):** skill `analisis-rendimiento` — rendimiento de **todo el sitio** con [Unlighthouse](https://unlighthouse.dev/) (Lighthouse en cada ruta, no página por página). Scores performance/accesibilidad/best-practices/SEO + Core Web Vitals de **laboratorio** (LCP, CLS, TBT, FCP, Speed Index), peores páginas y rendimiento **por plantilla**. Vuelca a `.seo-audit/<sitio>/data/performance.json`.
- **feat(dashboard):** sección ⚡ Rendimiento (tarjetas de scores con color por umbral, CWV medios, páginas más lentas y rendimiento por plantilla). Lee `performance.json`; se oculta si no hay datos.
- **feat(flujo):** Bloque 2 (Velocidad/CWV) de `auditoria-tecnica` ahora delega en `analisis-rendimiento` para el sitio completo. Mantiene la regla de datos (cero números inventados) y la distinción laboratorio vs. campo (CrUX/GSC).

### v1.2.0
- **fix(crawl):** User-Agent de navegador real + detección de bloqueo WAF (Cloudflare) en los scripts que rastrean en vivo (`inventario_urls.py`, `http_checks.py`, `serp_outline.py`). Override con `SEO_USER_AGENT`.
- **feat(serpapi):** skill `configurar-serpapi` — onboarding de la API key (cuenta gratis), guardada una vez en `~/.claude/seo-skills.env` y usada en cada sesión.
- **feat(dashboard):** skill `dashboard-seo` — entregable de cierre: web local con issues, keywords, clusters, competidores, AEO/GEO, auditorías, inventario y próximos pasos. Los contenidos redactados se ven como briefs con link al borrador.
- **feat(skills):** regla obligatoria *nunca inventar números* en las 13 skills y 3 agentes (se piden al usuario o se marcan `pendiente de dato`).
- **docs:** flujo completo de punta a punta que siempre termina en un dashboard.

## Planificado

### v1.4.0: Presentaciones editables para clientes con PPT Master
- **[#1](https://github.com/Arianna-Lupi/SEO-Skills/issues/1)**: skill `presentacion-pptx` (nombre tentativo; también podría ser un subcomando de `/aprendoclub report` o `/aprendoclub proposal`). Arma un documento fuente en Markdown a partir de `.seo-audit/<sitio>/data/*.json` (resumen ejecutivo, salud técnica con el puntaje, oportunidades, competencia, contenido entregado, plan, proyección con sus supuestos si hay Search Console, y próximos pasos como tareas con verbo e ICE) y lo entrega a [PPT Master](https://github.com/hugohe3/ppt-master) (licencia MIT) para producir un `.pptx` con formas y textos nativos, editable en PowerPoint, con transiciones y notas del orador.
- **Reglas:** la integración es opcional y pide confirmación antes de clonar o instalar nada (mismo flujo del lanzador: preguntar, mostrar el comando exacto, aislar). Sin PPT Master, se entrega el Markdown con instrucciones para generar el PPTX. Nunca se inventan números y las proyecciones salen siempre como escenarios con supuestos. PPT Master requiere Python 3.10 o superior.
- **Decisión:** antes se planeaba un deck con Slidev (HTML y PDF); se cambió a PPT Master porque el resultado es un archivo editable de PowerPoint, que es lo que el cliente suele pedir. Solo hay diseño escrito: [`docs/diseno-presentacion-pptx.md`](docs/diseno-presentacion-pptx.md). La implementación queda para la siguiente versión salvo que Juan la pida antes.

## Backlog / ideas (sin issue todavía)

- Enriquecer keywords con **volumen/KD reales** vía Ahrefs MCP cuando esté disponible (hoy `pendiente de dato`).
- **Dashboard**: mostrar `local-seo.json`, `ecommerce.json`, `plan-seo.json` y `proyeccion-gsc.json` (hoy solo `next-steps.json` está en su esquema).
- **Decisión pendiente**: regla de paginación (canónica a la página 1 + noindex, la de Juan, vs. la recomendación de Google); documentada en `seo-ecommerce`.
- Skills que quedaron como idea por falta de base clara en el diplomado: `seo-programatico`, `monitoreo-de-cambios`, hreflang, `seo-redes-sociales` y `analisis-de-nichos` (Semana 14, lecciones 5 y 6).
- **Tests**: añadir pruebas con las fixtures de los scripts nuevos en `tests/` (las nuevas cubren el enrutador, los requisitos y el instalador; faltan los scripts de las skills de la ronda "diplomado primero", entre ellos `perfil_competidor.py` y `comparar_serp.py`).
- **Instalación**: probar el plugin (`/plugin marketplace add` y `/plugin install`) contra el repo publicado, y `install.ps1` en Windows (no se pudo probar sin PowerShell).
- **Dashboard**: mostrar el puntaje de salud, `competitors.json → serp_analysis` y las tareas con ICE.
- **Ideas de claude-seo sin base en el diplomado** (`/aprendoclub drift`, `hreflang`, `programmatic`, `sxo`, `maps`): descartadas por ahora.
- Filtro de **boilerplate** en `serp_outline.py` (descartar headings de nav/footer al construir el outline).

> Convención de datos para todo esto: ver `skills/dashboard-seo/SKILL.md`. Regla transversal: nunca se inventan métricas, se piden al usuario.
