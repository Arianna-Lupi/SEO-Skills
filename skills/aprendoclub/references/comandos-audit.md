# `/aprendoclub audit <sitio>`: las 9 fases

Orden basado en el diplomado "De Cero a SEO". Las rutas de scripts son relativas a la raíz de skills instaladas (`~/.claude/skills/` o `./.claude/skills/`) o a `skills/` en el repo. `<sitio>` es el dominio sin protocolo. Toda salida va a `.seo-audit/<sitio>/data/`.

## Fase 0. Descubrimiento (Semanas 1 y 2)

Método: Cuestionario SEO de la Semana 2 · lección 12 ("nunca empieces a trabajar a ciegas"). Pregunta, en un solo mensaje:

1. **Tipo de negocio:** local con ubicación, e-commerce, servicios o marca personal, o contenido/blog. Define la fase 6.
2. **CMS y stack:** WordPress, Shopify, Webflow, a medida. Define qué es realizable.
3. **Accesos:** Search Console (propiedad), Ahrefs (MCP), SerpApi (clave), export de Screaming Frog. Qué hay y qué no.
4. **País e idioma** del mercado, y 2 a 3 competidores de negocio que el usuario ya conoce.
5. **Objetivo** (vender, generar contactos, ganar lectores) y expectativas.

Acciones:
- Detecta SerpApi: variable `SERPAPI_API_KEY` o archivo `~/.claude/seo-skills.env`. Si falta y el usuario quiere SERP en vivo, ofrece `configurar-serpapi` (explica qué se envía a SerpApi: las keywords; pide confirmación).
- Crea `.seo-audit/<sitio>/data/meta.json` con `site`, `business_type`, `cms`, `market`, `data_sources` y `pending_data`.
- Comprueba que `.gitignore` ignore `.seo-audit/`.

**CHECKPOINT 0:** resume lo entendido y qué datos faltan. Sin tipo de negocio y objetivo no hay auditoría.

## Fase 1. Técnico (Semanas 3 y 12)

1. **Primero, en serie:** `inventario-de-urls` (`inventario_urls.py https://<sitio>`). Escribe `inventory-summary.json`. Si devuelve `"blocked": true`, sigue sus instrucciones (exportar URLs desde Search Console o usar Screaming Frog).
2. **Después, en paralelo** (una tarea por subagente):
   - `sitemap-y-robots`: robots.txt, sitemap, bloqueos accidentales.
   - `auditoria-tecnica` (o `agente-auditoria-tecnica` si hay crawls grandes): 3 bloques, por plantillas. Escribe `issues.json`.
   - `analisis-rendimiento`: Core Web Vitals de laboratorio de todo el sitio. Escribe `performance.json`. Si no hay Node, modo manual con PageSpeed Insights.
   - `optimizacion-de-imagenes`: peso, formato, ALT, lazy loading.
   - `schema-jsonld`: diagnóstico de datos estructurados de las plantillas clave.
3. **Puntaje de salud:** `python3 auditoria-tecnica/scripts/puntaje_salud.py .seo-audit/<sitio>/data/issues.json [--previo corrida-anterior.json]`. Guarda `score` y `grade` en `meta.json → summary.health_score`. Aclara que es un complemento de claude-seo (MIT) para comparar auditorías.

**CHECKPOINT 1:** críticos y altos en máximo 8 líneas, puntaje y qué quedó `pendiente de dato`. Pregunta si se corrige algo antes de seguir.

## Fase 2. Arquitectura (Semana 9)

`arquitectura-y-enlazado-interno`: regla de 3 clics, huérfanas, pilar a clusters. Necesita `internal_all.csv` y `all_inlinks.csv` de Screaming Frog; si no existen, ofrece correrlo (`SCREAMING-FROG.md`) o hace la revisión manual con el inventario. Es independiente de la fase 1: puede lanzarse en paralelo con ella.

## Fase 3. Keywords y contenido (Semanas 4 a 8, 10 y 11)

1. **Primero:** `investigacion-de-keywords` (o `agente-investigacion-keywords` para un nicho grande). Escribe `keywords.json`. Volumen y KD solo si vienen de una fuente real; si no, `pendiente`.
2. **Después, en paralelo:**
   - `mapa-de-palabras-clave`: una keyword primaria por URL y quick wins.
   - `intencion-de-busqueda`: valida la intención de las keywords y las URLs prioritarias.
   - `deteccion-de-canibalizacion`: solo si hay export de Search Console (query y página). Sin él, se omite y se anota.
   - `calidad-de-contenido-eeat`: muestra de las 5 a 10 URLs con más potencial o más tráfico.
3. `estrategia-de-contenidos-clusters` si el usuario quiere priorizar qué escribir (las "10 de Oro" y los clusters).

**CHECKPOINT 2:** confirmar las keywords objetivo y los pilares antes de gastar búsquedas de SERP en la fase 4.

## Fase 4. Competencia (Semana 6)

Por cada pilar de keywords, una pareja de tareas:
- `analisis-serp-y-competencia`: Negocio vs SEO, Ojo Clínico sobre el top 3. Scripts: `serp.py`, `perfil_competidor.py`, `comparar_serp.py` (escribe `competitors.json`).
- `analisis-de-competidores`: dominios por Análisis de Repetición (`competitor_domains.py`).

SerpApi y Ahrefs envían datos a terceros: confirma antes (ver regla en `SKILL.md`).

## Fase 5. GEO/AEO y off page (Semanas 14 y 16)

En paralelo:
- `optimizacion-geo-aeo`: features de IA en la SERP, rastreadores de IA, llms.txt (opcional). Escribe `ai-features.json`.
- `auditoria-de-backlinks-toxicos`: requiere un export de backlinks (Ahrefs u otro). Sin export, `pendiente de dato`. Escribe `backlinks.json`.

## Fase 6. Vertical (Semana 14), si aplica

- Local o servicios con zona: `seo-local` (`verificar_nap.py`). Escribe `local-seo.json`.
- Tienda online: `seo-ecommerce` (`auditar_producto.py` sobre 1 a 3 fichas). Escribe `ecommerce.json`.
- Puede aplicar más de una. Si el negocio es solo contenido, se omite la fase.

## Fase 7. Plan (Semanas 2 y 13)

1. `plan-seo`: junta los hallazgos de las fases 1 a 6 en un plan por meses con tareas que empiezan con verbo, ICE y Plantilla Master. Escribe `next-steps.json` y `plan-seo.json`.
2. `proyeccion-seo-gsc`: solo si hay Search Console. Escenarios con supuestos explícitos; no es garantía ni método del diplomado.

**CHECKPOINT 3:** presenta el plan y pregunta si va a entregarse a un cliente. En ese caso ofrece `propuesta-y-reporte-de-servicios-seo` (o `agente-plan-y-entrega`).

## Fase 8. Reporte y cierre (Semana 12)

1. `reporte-seo-gsc` si hay Search Console (4 métricas, mes contra mes).
2. **SIEMPRE** `dashboard-seo`: `python3 dashboard-seo/scripts/build_dashboard.py --site <sitio>` y entrega el URL local (`http://127.0.0.1:8787/`). Lista qué quedó `pendiente de dato`.

## Modo rápido sin accesos

Si el usuario no tiene Search Console, Ahrefs ni SerpApi, el flujo igual corre: fases 0, 1, 2, 4 (manual, con el Ojo Clínico), 5 (solo rastreadores de IA y schema), 6 y 7, con los huecos marcados. No se bloquea el flujo por una clave que falta.
