# Compliance: conformidad con las best practices de agentskills.io

Este documento cruza el deliverable (14 skills SEO + 2 utilitarias `configurar-serpapi` y `dashboard-seo`, y 3 subagentes del milestone "SEO skills — De Cero a SEO") con las best practices oficiales de [agentskills.io](https://agentskills.io). Para cada práctica decimos cómo se cumple y dónde verlo.

Fuentes citadas:

- Especificación: https://agentskills.io/specification
- Best practices de creación: https://agentskills.io/skill-creation/best-practices
- Optimización de descripciones: https://agentskills.io/optimizing-descriptions
- Uso de scripts: https://agentskills.io/using-scripts
- Evaluación de calidad: https://agentskills.io/evaluating-skills

## Tabla resumen

| # | Best practice (agentskills.io) | Estado | Dónde se ve |
|---|---|---|---|
| 1 | Grounded in real expertise | ✅ | Todas las SKILL.md citan método/semanas del diploma |
| 2 | Spending context wisely (<500 líneas / <5000 tok) | ✅ | SKILL.md de 92–157 líneas; mayor ≈ 2.4k tok |
| 3 | Add what the agent lacks (no SEO genérico) | ✅ | Reglas propias del diploma (punto dulce, 3 bloques, brief lo dicta la SERP) |
| 4 | Coherent units (1 skill = 1 unidad de trabajo) | ✅ | 16 skills atómicas (14 SEO + 2 utilitarias); 3 agentes orquestan secuencias |
| 5 | Calibrating control (defaults, no menús; procedures) | ✅ | Procesos paso a paso con defaults; sin preguntar de más |
| 6 | Patterns (gotchas, templates, checklists, validation loops) | ✅ | Secciones Gotchas / Salida / Checklist / CHECKPOINT |
| 7 | Progressive disclosure (frontmatter → cuerpo → scripts) | ✅ | name+description en frontmatter; scripts en `scripts/` |
| 8 | Optimized descriptions (imperativas, pushy, ≤1024) | ✅ | 16 skills + 3 agentes; agentes 846–893 chars |
| 9 | Frontmatter spec-compliant | ✅ | name kebab == carpeta; metadata; compatibility |
| 10 | Scripts best-practices (JSON stdout, --help, PEP723) | ✅ | 14/14 scripts con argparse + json.dumps + bloque PEP723 |
| 11 | Eval scaffolding (evals/ en las flagship) | ✅ | `evals/evals.json` en las 3 flagship |
| 12 | Validación (skills-ref / linter) | ✅ | Estructura validable; JSON de evals verificado |

## Detalle por práctica

### 1. Grounded in real expertise: corpus del diploma
Cada skill está anclada en el material real de *"De Cero a SEO"* de Arianna Lupi y Diana Rodríguez, con semanas concretas y no SEO genérico de internet. Por ejemplo: `investigacion-de-keywords` (Semana 4, Cuestionario SEO, 4 métodos y "punto dulce"), `auditoria-tecnica` (Semana 12, 3 bloques) y `brief-de-contenido` (Semanas 8 y 10, "el brief lo dicta la SERP"). Citamos reglas textuales del diploma como *"mejor 100 que necesitan que 10.000 que curiosean"* y *"lo que no se rastrea, no existe"*.

### 2. Spending context wisely
Ninguna SKILL.md pasa de las 500 líneas ni de los 5000 tokens. El rango real va de 92 a 157 líneas; la más grande, `brief-de-contenido`, ronda los 2 445 tokens. El detalle pesado (parsing de crawls, expansión de keywords, esquemas de SERP) vive en `scripts/` y no en el cuerpo, así no quemamos contexto al cargar la skill.

### 3. Add what the agent lacks
Las skills no enseñan SEO genérico. Aportan el método propio del diploma, que el modelo no trae de fábrica: el "Duelo de Keywords", la selección de las "10 de Oro", la auditoría por plantillas en lugar de página por página, la jerarquía H1–H4 sin saltos, los rangos de metas (50–60 c, 120–155 c) y la Plantilla Master como destino de cada entregable.

### 4. Coherent units
Una skill es una unidad de trabajo entregable. Las 14 skills SEO son atómicas (keywords, mapa, SERP, clusters, brief, redacción, on-page, schema, auditoría, rendimiento, arquitectura, inventario, GSC, GEO/AEO), más 2 skills utilitarias (`configurar-serpapi`, `dashboard-seo`). Los 3 subagentes (`agente-investigacion-keywords`, `agente-auditoria-tecnica`, `agente-contenido`) no duplican lógica: orquestan secuencias de varias skills cuando el volumen de lectura justifica su propio contexto.

### 5. Calibrating control: defaults en vez de menús
Las skills dan procedimientos numerados con defaults sensatos en vez de menús de opciones. Definen una herramienta por defecto (por ejemplo DinoRank o Ahrefs para volumen), avanzan sin preguntar lo evidente y solo se detienen en puntos de validación reales: falta de audiencia, SERP ambigua, falta de datos de un bloque. Los agentes traen CHECKPOINTS explícitos en lugar de declaraciones vagas.

### 6. Patterns usados
- Gotchas y errores comunes: una sección en las skills (INP vs FID, metatítulo fuera de rango, auditar por URL en vez de plantilla).
- Output templates: un bloque "Salida" con la plantilla exacta a rellenar (brief, tabla de keywords, tabla de issues).
- Checklists: on-page, severidades y los 3 criterios de selección.
- Validation loops, o plan-validate-execute: CHECKPOINTS en los agentes y una "VALIDACIÓN" entre etapas del pipeline de contenido.
- Bundled scripts: 14 scripts deterministas que le quitan trabajo mecánico al LLM.

### 7. Progressive disclosure
Hay tres niveles. El frontmatter (`name` y `description`) es el único que siempre se carga. El cuerpo de la SKILL.md se lee on-demand cuando la skill se activa. Y `scripts/` se ejecuta solo si Python está disponible y el paso lo amerita. El detalle de conexión de datos se externaliza a `MCP-SETUP.md`.

### 8. Descriptions optimizadas
Las descripciones son imperativas y algo "pushy" para disparar la activación o la delegación. Listan los triggers, incluido el caso en que el usuario no nombra la skill ni el agente, y cierran con la línea de frontera "NO uses… para X". Todas quedan por debajo de 1024 caracteres; las de los 3 agentes miden 846, 867 y 893. Empiezan con un verbo de acción ("Delega a este agente cuando…", "Usa esta skill cuando…", "Ejecuta…", "Crea…").

### 9. Frontmatter spec-compliant
- `name` en kebab-case e idéntico al nombre de la carpeta (verificado).
- `description` por debajo de 1024 caracteres.
- `compatibility`: declara dependencias (Python 3 vía uv, requests, MCPs opcionales) y que la skill funciona 100% manual.
- `metadata`: bloque `author: aprendoseo`, `milestone: "SEO skills (De Cero a SEO)"`, `version: "1.0"`. Está en las skills y lo añadimos a los 3 agentes, junto a `tools` y `model`, sin tocar el cuerpo.

### 10. Scripts best-practices
Los 14 scripts siguen el patrón recomendado:
- JSON a stdout como salida principal (`json.dumps`, 14/14).
- Diagnósticos por stderr, separados del resultado.
- `--help` y argparse en todos (14/14), sin prompts interactivos, así no bloquean al agente.
- PEP 723 con `uv run`: bloque `# /// script … ///` con `requires-python` y `dependencies` embebidos, ejecutables con `uv run`.
- Graceful degradation: si falta una dependencia o una API key (por ejemplo `requests` o `SERPAPI_API_KEY`), devuelven `{"ok": false, "reason": ..., "fallback": ...}` con exit 0 y la skill cae a modo manual en vez de romper.

### 11. Eval scaffolding
Siguiendo la guía *"Evaluating skill output quality"*, las 3 skills flagship llevan `evals/evals.json` con 3 casos cada una. Cada caso varía el fraseo y el detalle e incluye un edge case, con un `prompt` realista en español, un `expected_output` y `assertions` objetivas propias del diploma (por ejemplo metatítulo 50–60 c, jerarquía H1–H3 sin saltos, responde PAA, severidad por plantilla, INP y no FID):
- `skills/brief-de-contenido/evals/evals.json`
- `skills/investigacion-de-keywords/evals/evals.json`
- `skills/auditoria-tecnica/evals/evals.json`

### 12. Validación
La estructura es validable contra la skills-ref: un directorio por skill con `SKILL.md`, `name` igual a la carpeta, frontmatter conforme y `scripts/` opcional. Los tres `evals.json` se verificaron como JSON válido y las descripciones quedaron comprobadas bajo el límite de 1024 caracteres.

## Pruebas de activación (trigger evals)

Siguiendo la guía *"Optimizing skill descriptions"* (https://agentskills.io/skill-creation/optimizing-descriptions), las 3 skills flagship incluyen un set de activación `evals/eval_queries.json` para medir si la `description` hace que el modelo active la skill correcta:

- `skills/brief-de-contenido/evals/eval_queries.json`
- `skills/investigacion-de-keywords/evals/eval_queries.json`
- `skills/auditoria-tecnica/evals/eval_queries.json`

Cada set trae 14 queries en español, casuales y formales, con typos realistas. Son 7 con `should_trigger: true` (prompts realistas, varios que no nombran el dominio, con nombres de cliente, nicho o URLs) y 7 con `should_trigger: false`, que son near-misses fuertes: comparten vocabulario pero pertenecen a otra skill. Por ejemplo "ármame el reporte mensual" cae en `reporte-seo-gsc`, "dame keywords para mi nicho" en `investigacion-de-keywords` y "audita la velocidad" en `auditoria-tecnica`.

El runner `scripts/trigger_eval.sh` corre cada query N veces vía `claude -p "$query" --output-format json`, detecta con `jq` si se disparó un `tool_use` `name=="Skill"` para esa skill y calcula el `trigger_rate` por query:

```
bash scripts/trigger_eval.sh skills/brief-de-contenido/evals/eval_queries.json brief-de-contenido 3
```

El umbral de aprobación es 0.5: los `should_trigger:true` tienen que quedar con `trigger_rate ≥ 0.5` y los near-misses (`false`) con `trigger_rate < 0.5`. Para no sobreajustar la descripción a los propios ejemplos usamos un split train/validation 60/40: iteramos la `description` (hasta 5 veces) solo contra el set de train y, al pasar, la validamos una única vez contra el 40% reservado.
