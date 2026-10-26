# Changelog fragmento, grupo C: keywords, competencia y arquitectura

Base: Semanas 4, 5, 6 y 9 del diplomado, práctica de coaches (Vero, Ari, Diana, Dana, Juan) y complementos de claude-seo (MIT) solo en `references/complementos-claude-seo.md` de cada skill.

## Skill nueva (1)

### `intencion-de-busqueda` v1.0
- Decisión: se crea porque el diplomado la respalda con lecciones propias (Semana 4 · lecciones 3, 4 y 5; Semana 5 · lección 6; "Validación de Intención" de la Semana 4 · lección 14) y ninguna skill existente era dueña del trabajo "validar intención y formato contra la SERP". No duplica: `investigacion-de-keywords` y `mapa-de-palabras-clave` la invocan.
- `SKILL.md`: método en 8 pasos (buscar primero en Google, tipo, temperatura, formato que premia la SERP, consenso, Validación de Intención, misma URL o separadas, registro). Fuente: Semana 4 · lecciones 3 a 5 y 14, Semana 5 · lección 6.
- `references/metodo-diploma.md`: definiciones, ejemplos (matcha, hamburguesas, peluquería), tips de Arianna y 2 prompts verbatim, más práctica de coaches (Vero #218, #729, #125, #152, #788; Ari #254, #304, #155).
- `references/complementos-claude-seo.md`: umbrales de solape de SERP (7+ misma URL, 4 a 6 mismo cluster, 2 a 3 enlazar, 0 a 1 separar), taxonomía de tipos de página, severidad de desajuste, historias de usuario y puntuación por persona. Origen: `skills/seo-sxo/*` y `skills/seo-cluster/references/serp-overlap-methodology.md`.
- Script nuevo `scripts/serp_overlap.py` (stdlib, sin red): solape de SERP entre pares, grupos "misma URL", consenso de formato y veredicto de desajuste, `--ignore-ubiquitous`. Fixture `fixtures/serps_muestra.json`.
- `evals/evals.json` (3 casos) y `evals/eval_queries.json` (10 consultas).

## Skills mejoradas (6, todas a 1.1)

### `investigacion-de-keywords`
- Práctica de Vero y Ari incorporada en `SKILL.md` y `metodo-diploma.md`: intención antes que volumen, keywords sin datos no se borran (SERP con más de 3 artículos o 5 páginas), volumen sin ciudad y ciudad en el H1, tildes y plurales, frases de copy y secciones del sitio no son keywords, ejes para ampliar listas, "Idea de contenido" con formato (Vero #99, #134, #135, #96, #133, #815, #806; Ari #254, #304, #151).
- Paso de "Validación de Intención" enlaza a la nueva `intencion-de-busqueda`.
- Corregido un defecto de formato: la caja "Cierre en dashboard" estaba dentro del bloque de código; ahora va tras la caja de regla de datos, como en las demás skills.
- Nuevo `references/complementos-claude-seo.md` (agrupar por solape de SERP, pregrupación para listas grandes). Origen: `skills/seo-cluster/references/serp-overlap-methodology.md`.
- Eval 4 nuevo (keyword que atrae otra audiencia, frase de copy, volumen 0).

### `mapa-de-palabras-clave`
- Pasos afinados con la práctica de Vero: inventario con Spider y no sitemap, filtrar a contenido, SERP duplicada = una URL, acciones Conservar, Actualizar, Unificar, Eliminar, "rama seca", prioridad home y servicios, posición de páginas nuevas (Vero #75, #401, #675, #218, #673, #840, #805, #280, #845, #865).
- Paso 8 nuevo: validar el mapa antes de entregarlo (Semana 5 · video 10).
- Script nuevo `scripts/validar_mapa.py` (stdlib): valida 1:1 con casi duplicados, Valor SEO coherente, plan de acción frente a posición (Mantener solo top 3), inventario con archivos o etiquetas, temperatura, completitud y `map_score` (rúbrica auxiliar del repo, no del diplomado). Fixture `fixtures/mapa_muestra.csv`.
- `references/complementos-claude-seo.md`: rúbrica de Valor SEO por URL (5 señales), reglas anti canibalización al planificar y comprobaciones de calidad. Origen: `skills/seo-cluster/references/hub-spoke-architecture.md` y `skills/seo-sxo`.
- Caja "Cierre en dashboard" reubicada fuera del bloque de código. `evals/evals.json` nuevo (3 casos).

### `analisis-serp-y-competencia`
- Criterios de Vero y Ari: competidor mal elegido (prensa para ideas, no para producto), conclusiones que dicen "qué tiene el rival que tú no", AR en blanco, documento antes que tabla, columna Prioridad o Esfuerzo, top 5 a 10 páginas por competidor, Local Pack (Vero #132, #197, #540, #597; Ari #190, #157, #222, #249).
- Paso 7 nuevo: convertir ideas en tareas con verbo, plazo, recurso y responsable (Semana 6 · video 6) y los umbrales de 50 a 60 % de datos en 2 competidores (video 4), antes ausentes de `SKILL.md`.
- Script nuevo `scripts/brechas.py` (stdlib): brechas, mejoras (`weak`), defendidas, esfuerzo, páginas de competidores que cubren varias brechas y competidores críticos. No inventa volumen. Fixture `fixtures/posiciones_muestra.csv`.
- `references/complementos-claude-seo.md`: lectura de consenso de SERP, matriz de brecha 0 a 3, páginas de comparación y alternativas con reglas de equidad. Origen: `skills/seo-sxo`, `skills/seo-competitor-pages`.
- Caja de dashboard reubicada; `evals/evals.json` nuevo (3 casos).

### `analisis-de-competidores`
- Faltaba `references/metodo-diploma.md`: creado con Semana 6 · lecciones 1 a 4 (Negocio vs SEO, Directo vs Indirecto, 3 métodos, Análisis de Repetición, 3 a 4 competidores), prompt verbatim de la lección 3 y práctica de Vero y Ari.
- `competitor_domains.py`: nuevos campos `critical` (regla del curso, 3 de 5 = 60 %; con menos de 3 keywords, repetición de 2) y `type_hint` (plataformas conocidas). Cambio aditivo; los 25 tests de `tests/test_seo_scripts.py` siguen pasando (se corrieron con `uv run --with requests --with tldextract --with beautifulsoup4 --with lxml`).
- `SKILL.md`: criterios de selección de los coaches, gotchas sobre términos cortos (Semana 6 · video 3) y plataformas.
- `references/complementos-claude-seo.md`: dominios ubicuos, clasificación por tipo de sitio, tipos de página que premia la SERP. `evals/evals.json` nuevo (2 casos).

### `deteccion-de-canibalizacion`
- Faltaba `references/metodo-diploma.md`: creado. Recoge lo que el diplomado sí dice (Semana 3 · lección 16 y Bonus · lección 1 DinoRank + GSC, Semana 4 · lecciones 4 y 14, Semana 5 · lecciones 1, 5, 8 y 10) y deja explícito que el diplomado no tiene lección propia de canibalización. Práctica de Vero, Diana y Dana (una intención, una URL; "Madrid" no canibaliza si la intención difiere; keyword que será solo H2).
- Script `detectar_canibalizacion.py` con señales finas: `leader_changes` (columna opcional `date`, Google alterna), `slug_similarity`, `--brand` (consultas navegacionales quedan en Bajo) y `suggested_target`. Aditivo. Fixture `fixtures/gsc_muestra.csv`.
- `references/complementos-claude-seo.md`: matriz de decisión (misma intención × contenido parecido), cómo elegir URL ganadora, plan de redirecciones y medición a 4 a 8 semanas. Origen: reglas de canibalización de `skills/seo-cluster/*` (claude-seo solo la cubre como prevención).
- `evals/evals.json` nuevo (3 casos).

### `arquitectura-y-enlazado-interno`
- Distinción de profundidad de carpeta, clics desde la home y estructura de URL (práctica de Juan); "servicios y blog a un clic", "3 niveles o 2" (Ari #346); criterios de Juan (blog categorizado, filtros no son categorías, subcarpetas y no subdominios, sin carpetas de año); checklist plana vs profunda en `SKILL.md`.
- `orphans.py`: nuevas claves `depth_detail` y `depth_mismatch` (clics frente a carpeta). Aditivo. Fixtures `internal_all_muestra.csv` y `all_inlinks_muestra.csv`.
- Script nuevo `scripts/matriz_enlaces.py` (stdlib): matriz de enlaces faltantes pilar a cluster y cluster a pilar, mínimo por pieza (2 contextuales + 1 a producto, Semana 9), conversión infraenlazada, huérfanas, anchors genéricos o concentrados, profundidad en clics por BFS. Fixtures `paginas_muestra.csv` y `enlaces_muestra.csv`.
- `references/complementos-claude-seo.md`: enlaces obligatorios, recomendados y opcionales, umbrales 3 entrantes y 40 % de anchors, rúbrica de puntuación 0 a 100 (auxiliar del repo). Origen: `skills/seo-cluster/references/hub-spoke-architecture.md`.
- `metodo-diploma.md` ampliado con práctica de Juan, Ari, Vero y Dana. `evals/evals.json` nuevo (3 casos).

## Ideas descartadas
- Generar páginas de comparación y de alternativas como skill propia (`seo-competitor-pages`): no están en el diplomado. Quedan como idea de contenido en el complemento de `analisis-serp-y-competencia`.
- Puntuación por persona y wireframes IST/SOLL (`seo-sxo`): solo como complemento opcional en `intencion-de-busqueda`; el diplomado no los enseña.
- Plantillas HTML y esquema `cluster-plan.json` de `seo-cluster`: ya existen `estrategia-de-contenidos-clusters` y `dashboard-seo` con su propio esquema.
- Rangos de palabras por pilar y soporte de claude-seo: contradicen el enfoque de capacidad mensual del curso (Semana 7); solo contraste.

## Para el agente principal
- README, ROADMAP y FUENTES: añadir `intencion-de-busqueda` (v1.0) y subir a 1.1 las otras 6; listar scripts nuevos: `serp_overlap.py`, `validar_mapa.py`, `brechas.py`, `matriz_enlaces.py`. Citar claude-seo (MIT) en FUENTES con los archivos de origen indicados arriba.
- `install.sh` e `install.ps1`: incluir la carpeta `skills/intencion-de-busqueda`.
- `agents/`: valorar que `agente-investigacion-keywords` use `intencion-de-busqueda` en su validación de intención.
- `tests/`: sin tests nuevos; se pueden añadir pruebas para `serp_overlap.py`, `validar_mapa.py`, `brechas.py` y `matriz_enlaces.py` con sus fixtures.
- Hallazgo transversal: el `description:` del frontmatter de varias skills existentes (incluidas `auditoria-tecnica` y `brief-de-contenido`) contiene `: ` sin comillas y no parsea como YAML estricto. Lo dejé como estaba en las skills existentes de mi grupo; la nueva sí es válida.
- Las cajas "Regla de datos" y "Cierre en dashboard" conservan sus rayas largas originales para mantenerse idénticas entre skills; el resto de archivos del grupo no tiene rayas largas ni medias.
