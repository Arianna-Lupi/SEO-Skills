# Grupo D: off page, IA/GEO, datos estructurados y reportes

Todas son skills **mejoradas** (versión 1.0 a 1.1). Ninguna nueva. Complementos de claude-seo (MIT, agricidaniel) viven en `references/complementos-claude-seo.md` de cada skill, con la etiqueta de complemento externo.

## schema-jsonld
- Nuevo `references/metodo-diploma.md`: S3 L4 (datos estructurados como responsabilidad técnica), S10 L6 (schema es Prioridad 2 en la matriz Impacto/Esfuerzo), S14 L13 (FAQ schema para IA); práctica de coaches (Ari: "datos estructurados que no coinciden con la página").
- Corrección de vigencia: Google retiró el rich result de FAQ (7 de mayo de 2026, verificado en la documentación oficial de FAQPage) y el de HowTo (2023). El diploma sigue enseñando FAQ schema para IA; la skill lo mantiene solo con preguntas visibles y deja de prometer el desplegable (conflicto diploma vs. realidad: gana el método, queda anotado).
- Script nuevo `scripts/validate_schema.py` (stdlib), portado y simplificado desde la lógica de `skills/seo-schema` y `scripts/schema_ecommerce_validate.py` de claude-seo: detecta falta de @context, requeridas ausentes, placeholders, URLs relativas, fechas no ISO, ratings incompletos, tipos retirados; `--out` deja `schema-validation.json`.
- `schema_gen.py` avisa de FAQPage y HowTo retirados. Complemento: lista de tipos activos y retirados (`skills/seo-schema/references/deprecated-types-2024-2026.md`).
- Evals nuevos (`evals.json`, `eval_queries.json`) y fixture `fixtures/muestra.html`.

## optimizacion-geo-aeo
- Script nuevo `scripts/ai_crawlers.py` (stdlib): estado en robots.txt de GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, anthropic-ai, PerplexityBot, Google-Extended, CCBot, Bytespider, cohere-ai, Applebot-Extended, Bingbot, y presencia de llms.txt. Origen: `skills/seo-geo`, `agents/seo-geo.md`. Evalúa la ruta raíz; `--out` fusiona `crawlers` y `llms_txt` en `ai-features.json`.
- Complemento: llms.txt como opcional (Google no lo usa), separación búsqueda/entrenamiento/disparados por usuario, citabilidad por pasaje, señales de marca, notas por plataforma. Las cifras de estudios de terceros se marcan como pistas no verificadas.
- Ajuste al diploma: el primer párrafo pasa a "menos de 40 palabras" (S14 L13); 40-60 queda como margen en secciones internas.
- Paso nuevo en el proceso: Auditoría Final de Control de Ibrahim (S16 L1) con revisión de rastreadores. Checklist actualizado (FAQPage retirado en Google).
- Evals nuevos y fixture `fixtures/robots-muestra.txt`. Descartado: DataForSEO.

## auditoria-de-backlinks-toxicos
- Nuevo `metodo-diploma.md` (S12 L5, S14 L11, S16 L1). Se deja explícito que el diplomado no enseña toxicidad ni disavow y que los coaches reconocen poca experiencia en off page: derivar a Vero.
- Script nuevo `scripts/anchor_profile.py` (stdlib): distribución de anchors y concentración por dominio con banderas heurísticas; origen `skills/seo-backlinks` y `references/backlink-quality.md`. Escribe la clave `anchors` en `backlinks.json`.
- Complemento: señales extra de riesgo, criterio más conservador de disavow de claude-seo (diferencia anotada: la skill incluye nofollow tóxico, claude-seo no), regla de no dar nota con menos de 4 factores con datos, fuentes gratuitas (Bing Webmaster, Moz, Common Crawl).
- Se añadió la caja "Cierre en dashboard" que faltaba. Evals y fixture nuevos.

## link-building-y-outreach
- Nuevo `metodo-diploma.md`: S12 L5 (Guest Posting, inserción de enlaces, Planificador: Prospectar, Negociar, Seguimiento), S14 L11 (Hunter.io, personalización, Sheets), práctica de Vero (anchor limpio, rangos de DR).
- Script nuevo `scripts/verificar_enlaces.py` (stdlib, respeta robots.txt, 1 petición/s, tope 200 URLs): estado, anchor y rel de enlaces conseguidos; idea de `verify_backlinks.py`. Escribe `verificacion` en `backlinks.json`.
- Complemento: fuentes gratuitas para análisis de brecha con sus límites. Descartado: DataForSEO y tácticas masivas.
- Se aclara que el scoring de tiers es del proyecto, no del diploma. Caja "Cierre en dashboard" añadida. Evals nuevos.

## reporte-seo-gsc
- `gsc_report.py`: posición media ponderada por impresiones, `--out`, etiquetas de periodo, nota sobre el límite de 1.000 filas del export. Ejemplo del SKILL rotulado como ilustrativo.
- Script nuevo `scripts/crux_campo.py` (stdlib, `CRUX_API_KEY` gratuita): Core Web Vitals de CAMPO (LCP, INP, CLS, TTFB, FCP en p75) con umbrales de Google; sin datos devuelve `ok:false` (nunca estima). Origen `crux_history.py`. Cierra la tarea pendiente del ROADMAP sobre CWV de campo.
- Complemento: GSC API, GA4 como contexto (separado de las 4 métricas de GSC), descartes (Indexing API, Ads). La estructura del informe sigue S12 L6 y L7.
- Evals nuevos y fixtures CSV.

## dashboard-seo
- `build_dashboard.py`: secciones nuevas que se ocultan sin datos: Search Console mes vs mes, CWV de campo (separado del laboratorio), datos estructurados, backlinks (anclas, dominios, seguimiento) y rastreadores de IA. Archivos nuevos: `search-console.json`, `cwv-field.json`, `schema-validation.json`, `backlinks.json`; `ai-features.json` admite `crawlers` y `llms_txt`. Probado con fixtures en Chrome headless.

## configurar-serpapi
- `set_key.py`: validación con stdlib (ya no requiere `requests`), `--check-only` para revisar la clave guardada, aviso de cuota baja y manejo de 401/429.

## Para el agente principal
- README/ROADMAP: marcar hecho "CWV de campo"; listar los scripts nuevos (`validate_schema.py`, `ai_crawlers.py`, `anchor_profile.py`, `verificar_enlaces.py`, `crux_campo.py`) y los nuevos JSON del dashboard.
- FUENTES: añadir claude-seo (MIT) como origen de los complementos de estas 7 skills.
- install: nada nuevo (todo stdlib). `tests/`: pueden usar los fixtures de cada skill.
- Nota: las cajas "Regla de datos" y "Cierre en dashboard" conservan sus rayas largas originales para mantenerse idénticas al resto; el resto de los archivos del grupo no tiene rayas.
- Ideas descartadas: DataForSEO (de pago), RSL 1.0, Indexing API, generadores de schema de reservas/pedidos (fuera del diplomado).
