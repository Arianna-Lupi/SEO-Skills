# Fuentes

Estas son las fuentes que usamos para el entregable. Van en dos bloques: (A) el contexto interno del diplomado, que es lo que hace que las skills estén customizadas, y (B) la investigación externa: ideas de agentes, el formato técnico de Claude y las herramientas.

---

## A. Contexto interno del diplomado "De Cero a SEO" (aprendoseo)

Salido del corpus real del curso: transcripciones, resúmenes y prompts ya ingeridos en la base del chatbot (colección `chunks` en MongoDB, 16 semanas más Bonus). Instructores: Arianna Lupi (líder), Verónica Romero, Diana Rodríguez, Juan Carlos Angulo, Ibrahim Mogollón, Dana Aliaga, María Márquez (off-page) y Daniel (IA).

| Área / skill | Semana(s) del diploma |
|--------------|------------------------|
| Marco general (rastrear→indexar→posicionar, Top 3), Cuestionario SEO, Plantilla Master, Trello | W1–W2 |
| SEO técnico (fundamentos: `site:`, robots, sitemap, GSC/GA4) | W3 |
| `investigacion-de-keywords` (4 métodos, intención, clusters, "punto dulce", "Duelo de Keywords") | W4 |
| `mapa-de-palabras-clave` (Valor SEO, 1:1 anti-canibalización, temperatura, plan de acción, Top 5) | W5 |
| `analisis-serp-y-competencia` (Negocio vs SEO, "Ojo Clínico", "Análisis de Repetición", "Costo de Oportunidad") | W6 |
| `estrategia-de-contenidos-clusters` ("10 de Oro", clusters, E-E-A-T, CRO) | W7 |
| `brief-de-contenido` (dictado por la SERP; blog/landing/ecommerce; metas 50-60/120-155; jerarquía H) | W8 (+ W10 optimización) |
| `arquitectura-y-enlazado-interno` (regla 3 clics, crawl depth/width, huérfanas, link equity, tipos de enlace) | W9 |
| `redaccion-y-optimizacion-nlp` ("escribe para humanos…", NLP/entidades, los 4 análisis de Google, image SEO) | W11 |
| `optimizacion-on-page-meta` (metas + on-page) | W8 / W11 |
| `auditoria-tecnica` (3 bloques: indexabilidad / CWV / seguridad; por plantillas) | W12 |
| `reporte-seo-gsc` (Resumen→Rendimiento mes vs mes→Ganadoras→Próximos pasos; 4 métricas GSC) | W12 |
| `optimizacion-geo-aeo` (AEO; GEO/AEO para LLMs; presencia de marca) | W14 / W16 |
| Herramienta de casa: **DinoRank** (Keyword Research, TF*IDF, Rank Tracking, DinoPlugin) | Bonus |

---

## B.1 Formato técnico — skills y subagents de Claude

- Claude Code — **Skills**: https://code.claude.com/docs/en/skills
- Claude Code — **Subagents**: https://code.claude.com/docs/en/sub-agents
- Anthropic — **Agent Skills best practices**: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Anthropic — *Equipping agents for the real world with Agent Skills*: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- Estándar abierto de skills: https://agentskills.io
- Claude Code — **MCP**: https://code.claude.com/docs/en/mcp-servers
- (Comparativa skill vs subagent) The AI Architects — https://theaiarchitects.com/blog/claude-code-subagents-vs-skills · dev.to/nunc — https://dev.to/nunc/claude-code-skills-vs-subagents-when-to-use-what-4d12

**Best practices de skills (agentskills.io) — aplicadas en este entregable (ver `COMPLIANCE.md`):**
- Índice de docs: https://agentskills.io/llms.txt
- Specification: https://agentskills.io/specification
- Quickstart: https://agentskills.io/skill-creation/quickstart
- Best practices for skill creators: https://agentskills.io/skill-creation/best-practices
- Optimizing skill descriptions: https://agentskills.io/skill-creation/optimizing-descriptions
- Using scripts in skills: https://agentskills.io/skill-creation/using-scripts
- Evaluating skill output quality: https://agentskills.io/skill-creation/evaluating-skills
- Validador `skills-ref`: https://github.com/agentskills/agentskills/tree/main/skills-ref
- Skills de ejemplo (Anthropic): https://github.com/anthropics/skills

## B.2 Ideas de agentes/skills SEO con IA (YouTube + web)

| Idea | Fuente |
|------|--------|
| Keyword research agent | Ahrefs — *AI Agents for SEO*: https://ahrefs.com/blog/ai-agents-for-seo/ |
| Content brief generator | rzlt.io — *The Agentic SEO Playbook*: https://www.rzlt.io/blog/the-agentic-seo-playbook-how-ai-powered-seo-agents-handle-keyword-research-briefs-publishing |
| SERP analyzer | GitHub aaron-he-zhu/seo-geo-claude-skills: https://github.com/aaron-he-zhu/seo-geo-claude-skills |
| Topical map / clusters con IA | BlogSEO: https://www.blogseo.io/blog/seo-topical-maps-build-them-automatically-with-ai · Search Engine Land — *Agentic AI in SEO*: https://searchengineland.com/guide/agentic-ai-in-seo |
| Content writer/optimizer | GitHub Bhanunamikaze/Agentic-SEO-Skill: https://github.com/Bhanunamikaze/Agentic-SEO-Skill |
| Internal-linking agent | Ahrefs *AI Agents for SEO* |
| Technical-SEO audit agent | GitHub Bhanunamikaze (seo-technical) |
| Content-gap / refresh | Ahrefs *AI Agents for SEO* |
| Schema / JSON-LD | GitHub Bhanunamikaze (seo-schema); aaron-he-zhu (schema-markup-generator) |
| Meta-tags optimizer | GitHub aaron-he-zhu (meta-tags-optimizer) |
| GEO/AEO optimizer | GitHub Bhanunamikaze (seo-geo/seo-aeo) · Synscribe — *Automate Claude Search Optimization*: https://www.synscribe.com/blog/geo-automation-claude-seo |
| Rank tracker / performance reporter | GitHub aaron-he-zhu (rank-tracker / performance-reporter) |
| Competitor analysis | GitHub aaron-he-zhu (competitor-analysis) |
| Strategic SEO planner ("6 Circles") | mcpmarket: https://mcpmarket.com/tools/skills/keyword-research-planning |
| Multi-agente "director + especialistas" | n8n template: https://n8n.io/workflows/11109-generate-complete-seo-strategy-reports-with-serpapi-data-and-gpt-4-agent-team/ |
| Pipeline research→brief→draft con Claude Code | Ahrefs — *Content Engineering with Claude Code*: https://ahrefs.com/blog/how-i-do-content-engineering-with-claude-code/ |
| Keyword research agent en n8n | n8nlab.io: https://n8nlab.io/blog/build-ai-keyword-research-agent-n8n · DataForSEO: https://dataforseo.com/help-center/automate-keyword-research-with-n8n-and-dataforseo |

> **Nota honesta sobre YouTube:** la búsqueda devolvió sobre todo blogs, repos y flujos de n8n, más que páginas de video con título o canal verificables. Lo que recogí son los patrones de agente que circulan en esos videos (el equipo "director + especialistas", los pipelines research→brief→publish), y los corroboré con las fuentes no-video de arriba. No inventé títulos ni URLs de videos.

## B.3 Repos SEO de referencia (inventario de skills/agentes)

- AgriciDaniel/claude-seo (25 skills + 18 agentes): https://github.com/AgriciDaniel/claude-seo
- aaron-he-zhu/seo-geo-claude-skills: https://github.com/aaron-he-zhu/seo-geo-claude-skills
- Bhanunamikaze/Agentic-SEO-Skill: https://github.com/Bhanunamikaze/Agentic-SEO-Skill
- deeployCO/youtube-seo-skills: https://github.com/deeployCO/youtube-seo-skills

## B.4 Briefs y keyword research (cross-check del método)

- Ahrefs — *How to Create Content Briefs (6 Templates)*: https://ahrefs.com/blog/content-briefs/
- Backlinko — *How to Create a Content Brief*: https://backlinko.com/content-briefs
- Surfer — *How To Create Content Briefs in 8 Steps*: https://surferseo.com/blog/content-brief/
- SEOmonitor — *The Perfect SEO Content Brief Template*: https://www.seomonitor.com/learning-hub/the-perfect-seo-content-brief-template
- Semrush — *SEO Content Template*: https://www.semrush.com/kb/590-seo-content-template

---

## C. Herramientas, MCPs y APIs

- **SerpApi** (GRATIS ~100/mes) — SERP/PAA/autocomplete en vivo. MCP remoto: `https://mcp.serpapi.com/TU_TOKEN/mcp`. Cuenta/token: https://serpapi.com/manage
- **Ahrefs** (PAGO) — volumen/KD/backlinks/auditoría/GSC. Vía conector claude.ai: https://claude.ai/customize/connectors · API: https://ahrefs.com/api
- **GSC MCP `mcp-gsc`** (GRATIS, comunitario) — Search Console en vivo (clics/impresiones/CTR/posición, inspección de URLs, sitemaps). Python/`uvx`: https://github.com/AminForou/mcp-gsc
- **Screaming Frog SEO Spider CLI** — crawl headless + export CSV **GRATIS hasta 500 URLs** (licencia £199/año solo para >500 URLs / config guardada / render JS / scheduling / API). Docs: https://www.screamingfrog.co.uk/seo-spider/user-guide/general/ · precios: https://www.screamingfrog.co.uk/seo-spider/pricing/ · referencia interna que ya lo usa gratis: `../../technical-audit/` (aprendoseo).
- **Unlighthouse** — escanea TODO el sitio corriendo Google Lighthouse en cada ruta (open source, vía `npx unlighthouse-ci`). Base de la skill `analisis-rendimiento`. Docs: https://unlighthouse.dev/ · Lighthouse: https://developer.chrome.com/docs/lighthouse/overview · CWV (campo vs laboratorio): https://web.dev/articles/vitals
- **uv / uvx** (para correr `mcp-gsc`): https://astral.sh/uv
- Dependencias de los scripts deterministas: `requests`, `beautifulsoup4` (ver `requirements.txt`); el resto es stdlib de Python 3.

---

## D. Cómo se construyó el entregable

1. Minado del corpus del diplomado (método real por semana) → grounding de cada skill.
2. Investigación externa (B) → ideas de agentes + formato técnico correcto.
3. Validación del CLI de Screaming Frog contra un proyecto interno real que ya lo corre gratis (`../../technical-audit/`) → corrección del framing free/paid.
4. Datos de conexión de MCPs verificados contra docs oficiales / READMEs.

---

## C. Complementos externos: claude-seo (MIT, agricidaniel)

Repo: https://github.com/AgriciDaniel/claude-seo · Licencia en [`THIRD-PARTY-LICENSES.md`](THIRD-PARTY-LICENSES.md). Se usó para traer lo que el diplomado no detalla (rúbricas, umbrales vigentes, checklists, scripts), siempre adaptado al español y al método del diplomado. **Regla**: si claude-seo contradice al diplomado, gana el diplomado; todo lo importado vive en `references/complementos-claude-seo.md` de cada skill, etiquetado como complemento externo.

- **Grupo A** (A-tecnico): citar claude-seo (MIT) para `seo-technical`, `seo-sitemap`, `seo-images`, `seo-drift`, `pagespeed_check.py`, `sitemap_discovery.py`.
- **Grupo B** (B-contenido): claude-seo (MIT, agricidaniel): `skills/seo-content-brief` (autor original puneetindersingh), `skills/seo-content`, `agents/seo-content.md`, `skills/seo-cluster` (método original de Lutfiya Miller), `scripts/content_quality.py`, `content_humanize.py`, `content_verify.py`. Perfiles de coaches: dana.md y diana.md.
- **Grupo C** (C-keywords-competencia): - README, ROADMAP y FUENTES: añadir `intencion-de-busqueda` (v1.0) y subir a 1.1 las otras 6; listar scripts nuevos: `serp_overlap.py`, `validar_mapa.py`, `brechas.py`, `matriz_enlaces.py`. Citar claude-seo (MIT) en FUENTES con los archivos de origen indicados arriba.
- **Grupo D** (D-offpage-ia-reportes): añadir claude-seo (MIT) como origen de los complementos de estas 7 skills.
- **Grupo E** (E-planificacion-verticales): ** añadir Semanas 2, 13, 14 y 16 y Bonus L9 como fuentes; claude-seo (MIT, agricidaniel): `skills/seo-plan`, `seo-local`, `seo-maps`, `seo-ecommerce`, `scripts/schema_ecommerce_validate.py`, `skills/seo/references/local-schema-types.md`.

## D. Práctica de los coaches y de la comunidad

Perfiles construidos con los mensajes reales de los coaches en los canales del foro (Verónica Romero, Ibraim Mogollón, Dana Aliaga, Diana Rodríguez, Arianna Lupi y Juan Angulo) y cruzados con los resúmenes del diplomado. Usados como autoridad secundaria (nunca contradicen el curso) en `references/practica-coaches.md` y en ejemplos. De la comunidad solo se tomó la **estructura** de las plantillas compartidas (encabezados de pestañas y secciones de briefs), sin datos de alumnos ni clientes.

- Semanas del diplomado añadidas como fuente en esta ronda: S2, S4, S5, S7, S8, S10, S11, S12, S13, S14 y S16, y el Bonus (DinoRank).
- Instructoras según los resúmenes: Diana Rodríguez imparte las lecciones 8 a 15 de la Semana 4; la Semana 11 la imparte Dana Aliaga.

## E. Enrutador, instalador y presentaciones (ronda aprendoclub)

- **Diplomado (autoridad):** el orden de las fases de `/aprendoclub audit` sale de las Semanas 1 a 4, 6, 9 y 12 a 16 (detalle por fase en `skills/aprendoclub/references/metodo-diploma.md`). Los comandos y sus nombres son del repo.
- **claude-seo (MIT, © 2026 agricidaniel)**, como patrón y no como texto copiado, licencia en [`THIRD-PARTY-LICENSES.md`](THIRD-PARTY-LICENSES.md):
  - `skills/seo/SKILL.md` y `skills/seo-audit/SKILL.md`: orquestador `/seo <comando> <argumento>`, tabla de comandos, auditoría con subagentes en paralelo y subagentes condicionales según el tipo de negocio.
  - `install.sh`, `install.ps1`, `uninstall.sh`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` y el flujo `/plugin marketplace add` más `/plugin install`: instalación rápida, desinstalación y empaquetado como plugin.
  - `bin/claude-seo` y `scripts/runtime.py`: idea del lanzador estable que resuelve el intérprete de Python y falla con un mensaje claro (adaptado a `aprendoclub-run`, sin entorno administrado ni dependencias pesadas).
  - `skills/seo-audit/SKILL.md`: puntaje de salud 0 a 100 (ya en `auditoria-tecnica/scripts/puntaje_salud.py`).
  - Competencia v1.2 (grupo F): `skills/seo-sxo/references/page-type-taxonomy.md`, `skills/seo-sxo/SKILL.md`, `skills/seo-content` (señales E-E-A-T) y `skills/seo-dataforseo/SKILL.md` (solo mención, de pago y no implementado).
- **PPT Master** (https://github.com/hugohe3/ppt-master, MIT, © 2025-2026 Hugo He): herramienta externa prevista para las presentaciones editables (v1.4.0). Solo se menciona y se invoca como herramienta externa, previa confirmación; no se incorpora su código ni su texto, así que no está en `THIRD-PARTY-LICENSES.md`. Si eso cambia, se agrega allí su licencia. Diseño y lo que se leyó de su repositorio: [`docs/diseno-presentacion-pptx.md`](docs/diseno-presentacion-pptx.md). Se descartó Slidev como base de las presentaciones.
