# Changelog fragmento B: contenido SEO (Semanas 4, 7, 8, 10 y 11)

Autor: agente de skills grupo B. Todo lo de claude-seo (MIT, agricidaniel) va adaptado y etiquetado como "Complemento externo (claude-seo, MIT), no es parte del método del diplomado" en `references/complementos-claude-seo.md`. Donde difiere del curso, gana el diplomado y queda escrito.

## Skills mejoradas (version 1.0 a 1.1)

### brief-de-contenido
- Nuevo `references/practica-coaches.md`: orden de revisión de briefs de Diana Rodríguez y Dana Aliaga, método de feedback Problema / Por qué importa / Recomendación, contexto mínimo de entrega, errores típicos (intención mal clasificada, tipo de página equivocado, cada secundaria como H3). Fuente: práctica de coaches (perfiles diana.md y dana.md).
- Nuevo `references/complementos-claude-seo.md`: ficha de intención ampliada, tabla de competidores, tres tipos de brecha, ganancia de información, guía de keyword por sección, filtro de no competidores, plantillas extra (servicio, categoría, ubicación), modo "solo esquema". Origen: `skills/seo-content-brief` y sus references. Tabla de diferencias: meta descripción 130-150 de claude-seo frente a 120-155 del curso (gana el curso).
- Nuevo script `scripts/brief_check.py` (stdlib): valida metas con conteo, keyword al inicio, H1 único, saltos de nivel y bloques obligatorios por tipo. Fixture en `fixtures/`. Sale del criterio de la Semana 8 lecciones 4 a 6.
- SKILL.md: paso 4b de revisión como coach, enlace a `actualizacion-de-contenido` para el proceso W10 completo, gotchas nuevos. Se corrigió el ejemplo (la meta descripción de 134 c medía 112; ahora 129 c con texto ajustado).
- evals: 2 casos nuevos (revisión de brief ajeno con Problema/Por qué/Recomendación; validación con brief_check) y 2 queries.

### redaccion-y-optimizacion-nlp
- Nuevo `references/practica-coaches.md` (Dana Aliaga, instructora de la Semana 11, y Diana): brief y datos SEO en el mismo documento, tono informativo vs. comercial, mito de la longitud, "la IA propone, tú validas", NLP "no indispensable" (Diana #77).
- Nuevo `references/complementos-claude-seo.md`: colocación de keyword sin cuota de densidad, términos secundarios de referencia, checklist anti contenido genérico de IA, legibilidad (Flesch no es factor de ranking). Origen: `skills/seo-content`, `seo-content-brief/references/keyword-density.md`, `scripts/content_humanize.py` y `content_quality.py`.
- Nuevo script `scripts/ai_tells.py` (stdlib): marcas de relleno en español, rayas largas, aperturas repetidas, frases largas, cifras sin fuente, exceso de keyword. No emite veredicto de autoría. Adaptación en español de los scripts en inglés de claude-seo; el reemplazo automático 1 a 1 no se trajo (la humanización la hace la persona, Semana 11 lección 3).
- SKILL.md: paso 4b, sección del script, gotchas. evals: 3 casos nuevos (carpeta `evals/` creada).

### optimizacion-on-page-meta
- Nuevo `references/practica-coaches.md`: metas con CTA, encabezados y H1, URL, local. Se señalan como criterio personal, fuera del curso, la descripción de 150 a 160 y "H1 igual a meta es redundante" de Diana (#28, #77).
- Nuevo `references/complementos-claude-seo.md`: diferencias de umbrales, colocación de keyword, severidad de metas (alta/media/baja).
- Nuevo script `scripts/meta_audit.py` (stdlib): auditoría masiva por CSV (Screaming Frog o Plantilla Master), faltantes y duplicados, rangos 50-60 y 120-155, keyword al inicio. Fixture incluida.
- SKILL.md: sección del script, enlaces a práctica y complementos, gotchas. evals: 3 casos nuevos.

### estrategia-de-contenidos-clusters
- Nuevo `references/practica-coaches.md`: cluster por categoría, no mezclar servicios, HOME no absorbe todo, blog hub para informativas, canibalización con ejemplos (cera para velas), intención con ejemplos contrastados, errores típicos de Diana y Dana.
- Nuevo `references/complementos-claude-seo.md`: clustering por solapamiento de SERP (7-10 misma página, 4-6 mismo cluster, 2-3 enlazar, 0-1 separadas), reducción de comparaciones, anti patrones, tablero de control del cluster. Origen: `skills/seo-cluster` y `references/serp-overlap-methodology.md`.
- Nuevo script `scripts/serp_overlap.py` (stdlib, no consulta ninguna SERP): matriz de pares, grupos y avisos de canibalización. Fixture incluida.
- SKILL.md: paso 3b (canibalización antes de producir), gotchas. evals: 3 casos nuevos.

## Skills nuevas (version 1.0)

### actualizacion-de-contenido
- Base: Semana 10 completa (lecciones 1 a 8). `references/metodo-diploma.md` con prompts verbatim; `plantilla-brief-optimizacion.md` (Actual vs. Sugerido); `practica-coaches.md` (Dana #37, #57, #225, #115, #198; Diana #53, #70, #74, #146).
- `complementos-claude-seo.md`: modo "improve" del brief, brechas de competencia, ganancia de información, frescura, verificación de afirmaciones, nota sobre FAQ Schema.
- Script `gsc_oportunidades.py` (stdlib): keywords de umbral, CTR bajo frente a la mediana del propio export, victorias rápidas de página 2, secundarias no cubiertas en el texto y alcance orientativo. Heurísticas declaradas, no cifras de Google. Fixtures incluidas.
- evals (3 casos) y eval_queries.

### calidad-de-contenido-eeat
- Base: Semana 7 lección 5 (E-E-A-T) y 6 (CRO), Semana 11 lecciones 2, 3, 5 y 6, Semana 14 lecciones 12 y 13. `references/metodo-diploma.md`, `rubrica-revision.md` (OK/Ajustar/Falla con severidad), `practica-coaches.md` (fuentes y veracidad de Dana, señales de confianza de Diana), `complementos-claude-seo.md` (prueba Quién/Cómo/Por qué, pesos internos de la rúbrica de claude-seo, suelos de cobertura solo orientativos, checklist anti contenido genérico).
- Script `calidad_contenido.py` (stdlib): señales de autoría, fechas, experiencia, fuentes, confianza, afirmaciones sin fuente y contenido delgado orientativo; `--url` con User-Agent de navegador, robots.txt y detección de bloqueo. No puntúa autoridad.
- evals (3 casos) y eval_queries. Persiste en `content-briefs.json` (campo `quality_review`).

## Ideas descartadas
- **seo-programatico:** no se creó. El diplomado no tiene lección de SEO programático (Semana 14 lección 2 es SEO Local y la lección 5 es nichos). Solo hay una nota de Juan en `voice-profile.md` ("carpetas por ciudad, un keyword base, buen formato para SEO programático") y la práctica de Diana de landings por localidad (#61, #62, #153). Queda anotada como idea en `estrategia-de-contenidos-clusters/references/complementos-claude-seo.md` sección 6. Origen posible: claude-seo `skills/seo-programmatic`.
- Puntuación 0-100 de calidad y de "AI Citation Readiness" de claude-seo: sin base en el curso; se sustituyó por la rúbrica OK/Ajustar/Falla.
- Objetivos de palabras por sección y por tipo de página: el curso no los fija y los coaches los desaconsejan.
- Reescritura automática de frases de IA (`content_humanize.py`): la humanización es humana en el curso.

## Para el agente principal (README, ROADMAP, FUENTES, install, tests, agents)
- Registrar 2 skills nuevas: `actualizacion-de-contenido` y `calidad-de-contenido-eeat`, y subir a 1.1 las 4 mejoradas.
- Scripts nuevos a listar y a probar en `tests/`: `brief-de-contenido/scripts/brief_check.py`, `redaccion-y-optimizacion-nlp/scripts/ai_tells.py`, `optimizacion-on-page-meta/scripts/meta_audit.py`, `estrategia-de-contenidos-clusters/scripts/serp_overlap.py`, `actualizacion-de-contenido/scripts/gsc_oportunidades.py`, `calidad-de-contenido-eeat/scripts/calidad_contenido.py`. Todos stdlib y con `--help`. Fixtures en cada carpeta `fixtures/`.
- FUENTES.md: claude-seo (MIT, agricidaniel): `skills/seo-content-brief` (autor original puneetindersingh), `skills/seo-content`, `agents/seo-content.md`, `skills/seo-cluster` (método original de Lutfiya Miller), `scripts/content_quality.py`, `content_humanize.py`, `content_verify.py`. Perfiles de coaches: dana.md y diana.md.
- install.sh e install.ps1: incluir las 2 carpetas nuevas.
- `agents/agente-contenido.md`: puede encadenar `calidad-de-contenido-eeat` después de la redacción y `actualizacion-de-contenido` para piezas existentes. Hay que decidir si se añade un `agents/` para auditoría de contenido.
- `dashboard-seo`: las dos skills nuevas persisten en `content-briefs.json` (`type: "optimizacion"` y campo `quality_review`); si el esquema no los muestra, ampliar `build_dashboard.py` (fuera de mi grupo).
- Nota de atribución: la Semana 11 la imparte Dana Aliaga, no Diana Rodríguez (Diana imparte las lecciones 8 a 15 de la Semana 4).
