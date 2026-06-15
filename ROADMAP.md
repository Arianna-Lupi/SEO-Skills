# Roadmap

Estado y próximos pasos de las SEO skills (aprendoseo, "De Cero a SEO"). Issues en [GitHub](https://github.com/Arianna-Lupi/SEO-Skills/issues).

## Publicado

### v1.3.0 (actual)
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

### v1.4.0 — Presentaciones para clientes con Slidev
- **[#1](https://github.com/Arianna-Lupi/SEO-Skills/issues/1)** — Skill `presentacion-slidev` (o `dashboard-seo --slides`) que genera un deck [Slidev](https://sli.dev/) (`slides.md`) a partir de la convención `.seo-audit/<sitio>/data/*.json`. Orientado a cliente (resumen ejecutivo, salud técnica, oportunidades, competencia, contenido entregado, próximos pasos), con export a **PDF/PPTX** para enviar. Mantiene la regla de datos (cero números inventados) y `.seo-audit/` gitignored. Bilingüe ES/EN.

## Backlog / ideas (sin issue todavía)

- Sección de **GSC** en el dashboard (clics/impresiones/CTR/posición mes vs mes) cuando el usuario conecte/exporte Search Console — hoy se marca como pendiente.
- Enriquecer keywords con **volumen/KD reales** vía Ahrefs MCP cuando esté disponible (hoy `pendiente de dato`).
- **Core Web Vitals de CAMPO** (CrUX / Search Console) en el dashboard, junto a los de laboratorio que ya da `analisis-rendimiento`.
- Filtro de **boilerplate** en `serp_outline.py` (descartar headings de nav/footer al construir el outline).

> Convención de datos para todo esto: ver `skills/dashboard-seo/SKILL.md`. Regla transversal: nunca se inventan métricas, se piden al usuario.
