# Propuesta: skills y agentes de Claude para SEO (aprendoseo, "De Cero a SEO")

Tarea: investigar y proponer 10 skills de Claude más 2 o 3 agentes de Claude para automatizar los flujos SEO del equipo, customizados con el contexto interno del diplomado "De Cero a SEO". De cada uno se explica qué hace, qué tiene por dentro, de dónde salió y cuánto tomaría tenerlo en producción.

Estado: las 13 skills SEO (las 10 pedidas más 3 extras) más 2 skills utilitarias (`configurar-serpapi` para datos en vivo y `dashboard-seo` para el entregable final) y los 3 agentes ya están escritos como archivos reales y usables en `skills/` y `agents/`, no son solo ideas. Casi cada skill trae además un script determinista en `scripts/` que hace el paso mecánico y devuelve JSON, lo que ahorra tokens y da más precisión. Esta propuesta los resume y estima el trabajo que falta para llevarlos a producción.

---

## 1. Resumen ejecutivo

- 13 skills SEO (procedimientos de un solo propósito, deterministas y baratos): las 10 pedidas más 3 extras (`inventario-de-urls`, `optimizacion-geo-aeo`, `schema-jsonld`), más 2 skills utilitarias: `configurar-serpapi` (conecta datos en vivo guardando la API key del usuario) y `dashboard-seo` (paso de cierre: reúne todo lo encontrado en una web local y devuelve un URL). Reproducen el método del diploma, desde el keyword research hasta el reporte mensual.
- 3 agentes (coordinadores de varios pasos, cada uno con su propio contexto) que encadenan esas skills en flujos completos: investigación de keywords de principio a fin, auditoría técnica, y el flujo de contenido (SERP, brief, redacción, on-page).
- Scripts deterministas (`skills/<skill>/scripts/*.py`): cada skill con un paso mecánico trae un script Python que lo ejecuta y devuelve JSON compacto, para que el modelo razone sobre el resultado y no sobre HTML o CSV crudos. Eso ahorra tokens y da más precisión. Si falta la clave o una dependencia, no fallan: la skill sigue en modo manual.
- Todo está customizado al diploma. Usa la Plantilla Master (la hoja de Google sobre la que se apoya el método), Trello, y la terminología propia de Arianna ("punto dulce", "Duelo de Keywords", "Mapa de Palabras Clave", "Ojo Clínico", "10 de Oro", "Costo de Oportunidad", temperatura de intención, etc.).
- Sigue las buenas prácticas de agentskills.io (ver `COMPLIANCE.md`): descripciones imperativas de hasta 1024 caracteres, secciones `## Gotchas` con las correcciones del diploma, frontmatter que cumple la spec (`name`/`description`/`compatibility`/`metadata`), scripts con `--help` más PEP 723 y `uv run`, divulgación progresiva (mostrar el detalle solo cuando hace falta), y evals (`evals.json` más `eval_queries.json` de activación) en las 3 skills principales.
- MCP y herramientas opcionales. Funcionan sin conectar nada: pegas los datos y listo. Si conectás algo, en vivo: SerpApi (gratis) da SERP y PAA; GSC `mcp-gsc` (gratis) da Search Console; Ahrefs (pago) da volumen, KD, backlinks y auditoría; y el CLI de Screaming Frog (gratis hasta 500 URLs) hace los crawls. Guías: [`MCP-SETUP.md`](./MCP-SETUP.md) y [`SCREAMING-FROG.md`](./SCREAMING-FROG.md).

---

## 2. Cómo se hizo la investigación

Se cruzaron dos fuentes:

1. Contexto interno del diplomado (lo que hace que sea customizado). Se revisó el corpus real del curso (16 semanas más el Bonus, con las transcripciones y resúmenes ya cargados en la base del chatbot) para sacar el método que enseña cada semana. Por eso cada skill dice "usa el método X del diploma" en vez de dar SEO genérico. Las citas por semana están en cada skill y en la sección 5.

2. YouTube y web (ideas de agentes y skills, más el formato técnico). Se buscaron ideas de agentes SEO con IA y el formato real de skills y subagents de Claude Code. Las fuentes están en la sección 6.

> Nota honesta sobre "buscar videos de YouTube": la búsqueda web devolvió sobre todo blogs, repos y plantillas (n8n), más que páginas de video con título y canal verificables. Los patrones de agentes que circulan en YouTube sí quedaron capturados (el equipo "director más especialistas", o los flujos research, brief y publish en n8n con Claude y SerpApi/DataForSEO) y están corroborados por las fuentes no-video que sí cito. No inventé títulos ni URLs de videos.

---

## 3. Las skills (vista de tabla)

10 skills núcleo (1 a 10) más 3 extras (11 a 13). La columna Script indica el ayudante determinista que trae cada una.

| # | Skill | Qué hace | Script determinista | Origen (diploma) | Origen (externo) | A producción |
|---|-------|----------|---------------------|------------------|------------------|--------------|
| 1 | `investigacion-de-keywords` | Semilla → lista de keywords con intención, clusters, métricas y "punto dulce"/"Duelo de Keywords" | `expand_keywords.py` | W4 (Arianna, Diana) | Ahrefs *AI Agents for SEO*; repos seo-claude-skills | ~3 h |
| 2 | `mapa-de-palabras-clave` | Inventario de URLs → 1:1 keyword↔URL (anti-canibalización) + plan de acción | `canibalizacion.py` | W5 (Verónica) | Mapeo de contenido (Ahrefs/Surfer) | ~3 h |
| 3 | `analisis-serp-y-competencia` | SERP + competidores (Negocio vs SEO), gaps, "Costo de Oportunidad" | `serp.py` | W6 (Arianna) | SerpApi SERP/PAA; serp-analysis skills | ~3 h |
| 4 | `estrategia-de-contenidos-clusters` | "10 de Oro" → 3–5 clusters + E-E-A-T + CRO | `cluster.py` | W7 (Arianna) | Topical maps con IA (BlogSEO, SEL) | ~3 h |
| 5 | `brief-de-contenido` ⭐ | Brief dictado por la SERP; 3 tipos (blog/landing/ecommerce) + brief de optimización | `serp_outline.py` | W8/W10 | Ahrefs/Backlinko/Surfer/SEOmonitor briefs | ~4 h |
| 6 | `redaccion-y-optimizacion-nlp` | Borrador humanizado + optimización semántica/entidades (NLP) | `readability.py` | W11 (Dana) | Surfer/NeuronWriter; content-writer skills | ~4 h |
| 7 | `optimizacion-on-page-meta` | Variantes de metatítulo/metadescripción (CTR) + checklist on-page | `meta_check.py` | W8/W11 | meta-tags-optimizer skills | ~2 h |
| 8 | `auditoria-tecnica` | Auditoría en 3 bloques (indexabilidad/CWV/seguridad) por plantillas | `parse_sf.py`, `http_checks.py` | W12 | Ahrefs Site Audit; seo-technical skills | ~4 h |
| 9 | `arquitectura-y-enlazado-interno` | Arquitectura (regla 3 clics), huérfanas, enlaces internos + anchors | `orphans.py` | W9 | internal-linking agents (Ahrefs) | ~3 h |
| 10 | `reporte-seo-gsc` | Informe mensual ejecutivo sobre las 4 métricas de GSC | `gsc_report.py` | W12 | performance-reporter skills | ~3 h |
| 11 | `inventario-de-urls` (extra) | Extrae todas/la mayoría de las URLs si no hay export: sitemap (gratis) o Screaming Frog CLI | `inventario_urls.py` | W5/W9/W12 (crawl) | Screaming Frog user guide; `technical-audit` interno | ~2 h |
| 12 | `optimizacion-geo-aeo` (extra) | Optimiza para AI Overviews/ChatGPT/Perplexity + featured snippets/PAA (AEO/GEO) | `ai_features.py` | W14/W16 | SearchEngineLand; Synscribe; seo-geo/aeo skills | ~3 h |
| 13 | `schema-jsonld` (extra) | Genera + valida JSON-LD por tipo de página (Article/Product/FAQ/HowTo…) | `schema_gen.py` | SEO técnico | seo-schema skills | ~2 h |

⭐ = la de más valor en el día a día ("un brief bien hecho es el 50% del éxito", dice Arianna). (extra) = añadidas sobre las 10 pedidas, justificadas por las fuentes o el diploma.

Para una próxima tanda quedan `seo-local` (W14), `reescritura-refresh` (W10), `rank-tracker` y `content-gap`. El diploma y las fuentes las cubren, pero quedan fuera de este alcance.

### 3.5 Scripts deterministas (ahorran tokens y dan precisión)

Cada skill con un paso mecánico trae un script Python en `skills/<skill>/scripts/` que ejecuta ese paso y devuelve JSON compacto, para que el modelo razone sobre el resultado y no sobre HTML o CSV crudos. Todos imprimen JSON a stdout, leen claves del entorno (por ejemplo `SERPAPI_API_KEY`) y no se rompen si falta algo: cuando no hay clave o dependencia devuelven `{"ok":false,...}` y la skill sigue en modo manual. Las dependencias están en `requirements.txt` (`requests`, `beautifulsoup4`); el resto es la librería estándar de Python 3.

| Script | Hace (determinista) | Deps |
|--------|---------------------|------|
| `inventario_urls.py` | robots.txt → sitemap.xml → todas las `<loc>` (gratis) | stdlib |
| `serp.py` | SERP/PAA/related/features vía SerpApi | requests |
| `serp_outline.py` | extrae H1/H2/H3 de los que rankean → outline sugerido | requests+bs4 |
| `ai_features.py` | detecta AI Overview/featured snippet/PAA + recomendación | requests |
| `expand_keywords.py` | expande semillas (autocomplete/related/PAA) | requests |
| `cluster.py` | agrupa keywords por solapamiento de tokens (Jaccard) | stdlib |
| `canibalizacion.py` | detecta canibalización + quick wins desde CSV/JSON | stdlib |
| `meta_check.py` | valida largos/posición de metatítulo y metadescripción | stdlib |
| `readability.py` | legibilidad ES + densidad/colocación de keyword | stdlib |
| `schema_gen.py` | genera + valida JSON-LD por tipo | stdlib |
| `parse_sf.py` / `http_checks.py` | resume export de Screaming Frog / chequeo HTTP sin SF | stdlib / requests |
| `orphans.py` | huérfanas + inlinks + profundidad desde exports SF | stdlib |
| `gsc_report.py` | deltas mes vs mes + ganadoras/perdedoras + insights | stdlib |

Los 3 agentes pueden correr estos scripts por su cuenta con Bash (lo tienen entre sus herramientas).

---

## 4. Detalle de cada skill (qué tiene por dentro)

> El archivo completo de cada una está en `skills/<nombre>/SKILL.md`. Cada skill tiene su frontmatter (`name`, `description`) y las secciones Cuándo usar, Entradas, Datos (MCP opcional), Proceso, Salida, Ejemplo y Errores comunes.

1. `investigacion-de-keywords`. Por dentro: cuestionario SEO (audiencia), 4 métodos de descubrimiento (brainstorming, autocomplete, competencia, IA), un mínimo de 30 keywords, intención y clusters, métricas (Volumen, Tráfico, KD), criterios de limpieza ("punto dulce"), "Duelo de Keywords" y columnas de ejecución (URL, H1, idea). La salida va al tab "Investigación de palabras clave" de la Plantilla Master. MCP: SerpApi autocomplete (gratis) o Ahrefs volumen y KD (pago).

2. `mapa-de-palabras-clave`. Inventario de URLs (Screaming Frog o sitemap), el test "¿un usuario buscaría esto?" (Valor SEO sí o no), una relación 1:1 entre keyword y URL, temperatura de intención, plan de acción (optimizar, redireccionar, eliminar o mantener) y el Top 5 de quick wins. La salida va al tab "Mapa de Palabras Clave". Es algo distintivo del diploma.

3. `analisis-serp-y-competencia`. Competidor de Negocio frente a competidor de SEO, directos e indirectos, identificación (búsqueda directa, herramientas, "Análisis de Repetición"), el "Ojo Clínico" manual, una tabla de competidores, los gaps y el reporte de "Costo de Oportunidad". MCP: SerpApi (lo ideal aquí, gratis) o Ahrefs serp-overview (pago).

4. `estrategia-de-contenidos-clusters`. De los "10 de Oro" salen 3 a 5 clusters (pilar y spokes), luego E-E-A-T (autoría, "Sobre nosotros"), CRO (CTAs, PUV, reducir fricción) y el calendario. La salida va al tab "Estrategia".

5. `brief-de-contenido` ⭐. El brief lo dicta la SERP, así que primero se analiza el top
   3. La plantilla cubre intención y formato, metatítulo (keyword al inicio, 50 a 60 caracteres), metadescripción (120 a 155 con CTA), jerarquía H1 a H4 sin saltos, un benchmark, los enlaces internos con su anchor y los visuales. Hay 3 tipos (blog, landing, e-commerce) más un brief de optimización (W10). La salida va al tab "Producción".

6. `redaccion-y-optimizacion-nlp`. "Escribe para humanos, optimiza para robots": keyword en el H1 y en las primeras 100 palabras, 3 adjetivos de marca, el flujo research, outline, humanizar, escaneabilidad y reposo, el módulo NLP (entidades y los 4 análisis de Google) y el SEO de imágenes. Herramientas: Hemingway, Surfer, NeuronWriter.

7. `optimizacion-on-page-meta`. De 3 a 5 variantes de metatítulo y metadescripción para hacer A/B de CTR, más un checklist on-page (encabezados, URL, ALT, anchors, densidad). MCP: SerpApi para comparar contra los títulos que ya rankean.

8. `auditoria-tecnica`. Tres bloques: (1) indexabilidad y rastreabilidad (códigos, robots.txt, sitemap, `site:`), (2) velocidad y Core Web Vitals (LCP, INP, CLS, PageSpeed, WebP, revisado por plantillas), y (3) seguridad y canonicalización. Devuelve los problemas por severidad y un plan. MCP: Ahrefs Site Audit (pago, lo ideal).

9. `arquitectura-y-enlazado-interno`. La regla de los 3 clics, profundidad y amplitud del crawl, URLs semánticas, páginas huérfanas, link equity, los 4 tipos de enlace interno y los anchors que vienen del brief. Herramienta: Octopus.do.

10. `reporte-seo-gsc`. Resumen ejecutivo, rendimiento mes contra mes, keywords y páginas ganadoras, y tareas y próximos pasos, todo sobre las 4 métricas de GSC y con interpretación (por ejemplo, "más impresiones y menos clics = problema de CTR o de Meta Title"). MCP: Ahrefs gsc-* (pago) o el export manual de Search Console (gratis).

---

## 5. Los 3 agentes (qué tienen por dentro)

> Los archivos completos están en `agents/<nombre>.md`: el frontmatter (`name`/`description`/`tools`) y el cuerpo, que es el system prompt con el procedimiento, los puntos de validación y el "qué devuelvo". Conviene un agente, y no una skill, cuando hay varios pasos, decisiones a validar, o lectura pesada que mejor se aísla en su propio contexto.

1. `agente-investigacion-keywords` (estratega SEO senior). Coordina el flujo W4, W5 y W7 de principio a fin: del nicho o las semillas pasa a expandir (4 métodos), enriquecer métricas, clasificar la intención, armar clusters, aplicar el "punto dulce" y el "Duelo de Keywords", sacar los "10 de Oro" y asignar URL, H1 e idea a cada keyword. Es un agente porque lee decenas de keywords y SERPs. Usa las skills 1, 2, 3 y 4. MCP: SerpApi (gratis) más Ahrefs (pago). Devuelve una tabla lista para pegar en la Plantilla Master, los clusters y los 10 de Oro. A producción: 1 día y medio aproximadamente.

2. `agente-auditoria-tecnica` (especialista en SEO técnico). Corre la auditoría de 3 bloques por plantillas, la clasifica por severidad, la compara contra la corrida anterior (el diff) y entrega un plan de remediación. Es un agente porque la lectura es pesada (crawls, site audit), así que conviene su propio contexto con herramientas de solo lectura. Usa la skill 8 (más la 9 para las huérfanas). MCP: Ahrefs Site Audit y GSC (pago); sin MCP, con el export de Screaming Frog o GSC. A producción: 1 día y medio a 2 días.

3. `agente-contenido` (director, el Content Manager). Lleva el flujo de SERP a brief, redacción y on-page (W6, W8, W11): analiza la SERP y la competencia (eso dicta el formato), genera el brief del tipo correcto, hace un checkpoint humano opcional, redacta un borrador humanizado (NLP) y pasa el checklist on-page y de metas. Valida cada paso. Usa las skills 3, 5, 6 y 7. MCP: SerpApi (gratis, con clave) más Ahrefs (pago). Devuelve un borrador publicable, el brief, las metas y el checklist, listo para Producción o Trello. A producción: 2 días aproximadamente.

---

## 6. Fuentes (de dónde salió)

Contexto del diploma (la parte customizada): corpus "De Cero a SEO". W4 (keyword research), W5 (mapa de palabras clave), W6 (competencia), W7 (estrategia, clusters, EEAT y CRO), W8 y W10 (briefs), W9 (arquitectura), W11 (redacción y NLP), W12 (auditoría técnica y reporte GSC), Bonus (DinoRank y TF*IDF), W14 y W16 (AEO y GEO).

Ideas de agentes y skills SEO (YouTube y web):

| Idea | Fuente |
|------|--------|
| Keyword research agent | Ahrefs — *AI Agents for SEO* (ahrefs.com/blog/ai-agents-for-seo) |
| Content brief generator | rzlt.io — *The Agentic SEO Playbook* |
| SERP analyzer / serp-analysis | GitHub aaron-he-zhu/seo-geo-claude-skills |
| Topical map / clusters con IA | BlogSEO; Search Engine Land — *Agentic AI in SEO* |
| Content writer/optimizer | GitHub Bhanunamikaze/Agentic-SEO-Skill; aaron-he-zhu |
| Internal-linking agent | Ahrefs *AI Agents for SEO*; aaron-he-zhu (internal-linking-optimizer) |
| Technical-SEO audit agent | GitHub Bhanunamikaze (seo-technical) |
| Content-gap / refresh | Ahrefs; aaron-he-zhu (content-gap/refresher) |
| Schema / JSON-LD | GitHub Bhanunamikaze (seo-schema); aaron-he-zhu |
| Meta-tags optimizer | GitHub aaron-he-zhu (meta-tags-optimizer) |
| GEO/AEO optimizer | GitHub Bhanunamikaze (seo-geo/seo-aeo); Synscribe |
| Rank tracker / reporter | GitHub aaron-he-zhu (rank-tracker/performance-reporter) |
| Multi-agente "director + especialistas" | n8n template (SerpApi + GPT-4 agent team) |
| research→brief→draft pipeline | Ahrefs — *Content Engineering with Claude Code* |

Repos de referencia (inventario de skills): `AgriciDaniel/claude-seo` (25 skills y 18 agentes), `aaron-he-zhu/seo-geo-claude-skills`, `Bhanunamikaze/Agentic-SEO-Skill`, `deeployCO/youtube-seo-skills`.

Formato técnico (skills frente a subagents): la documentación de Claude Code (code.claude.com/docs/en/skills y /sub-agents), el *Agent Skills best practices* de Anthropic, y el estándar abierto agentskills.io.

Briefs y keyword research (para contrastar): Ahrefs, Backlinko, Surfer, SEOmonitor, Semrush.

---

## 7. Estimación de tiempo

Esta tarea (investigación más borradores): unas 3 a 4 horas, dentro del rango de 2 a 5 horas pedido. El resultado son 10 skills y 3 agentes ya escritos y usables.

Llevar todo a producción (probarlo con un proyecto real, conectar el MCP, ajustar las salidas a la Plantilla Master del equipo y validarlo con Arianna):

| Bloque | Esfuerzo |
|--------|----------|
| 10 skills (refinar + probar c/u) | ~31 h (≈2–4 h c/u) |
| 3 agentes (encadenan skills + validación) | ~5 días |
| Conectar SerpApi (gratis) + (opc.) Ahrefs | ~1–2 h |
| **Total a producción** | **~2 semanas de trabajo enfocado** |

Orden sugerido, lo de mayor valor primero: `brief-de-contenido`, después `investigacion-de-keywords`, luego `analisis-serp-y-competencia`, después `agente-contenido`, y por último el resto.

---

## 8. Cómo usarlo

Ver [`README.md`](./README.md) para instalar las skills y agentes en Claude Code, y [`MCP-SETUP.md`](./MCP-SETUP.md) para conectar SerpApi o Ahrefs (opcional).
