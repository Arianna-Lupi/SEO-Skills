# SEO skills y agentes de Claude (aprendoseo, "De Cero a SEO")

El enrutador `/aprendoclub`, 30 skills (28 de SEO + 2 utilitarias: `configurar-serpapi` y `dashboard-seo`) y 4 agentes de Claude Code para automatizar los flujos SEO del equipo, customizados con el método interno del diplomado "De Cero a SEO". Funcionan sin conectar nada y, si quieres, se conectan a SerpApi (gratis), Google Search Console (gratis) o Ahrefs (pago). **Todo flujo termina en un dashboard local** con lo encontrado.

## Inicio rápido

1. Instala (un comando, menos de 10 segundos, sin preguntas):

```bash
curl -fsSL https://raw.githubusercontent.com/Arianna-Lupi/SEO-Skills/main/install.sh | bash
```

En Windows (PowerShell): `irm https://raw.githubusercontent.com/Arianna-Lupi/SEO-Skills/main/install.ps1 | iex`

2. Reinicia Claude Code y escribe:

```
/aprendoclub audit midominio.com
```

Eso corre la auditoría completa paso a paso (descubrimiento, técnico, arquitectura, keywords y contenido, competencia, GEO y off page, vertical, plan y reporte), te pide confirmar entre fases y termina siempre en el dashboard. Escribe `/aprendoclub help` para ver todos los comandos. Lista completa, con ejemplos y salidas, en [`docs/COMANDOS.md`](docs/COMANDOS.md).

> **Alternativa como plugin de Claude Code:** `/plugin marketplace add Arianna-Lupi/SEO-Skills` y luego `/plugin install seo-skills@aprendoseo`. Usa una de las dos vías, no las dos a la vez. (El empaquetado como plugin está preparado pero todavía no se probó contra el repo publicado.)

## Actualizar

Un solo paso, el mismo para todos: vuelve a correr el comando de instalación.

```bash
curl -fsSL https://raw.githubusercontent.com/Arianna-Lupi/SEO-Skills/main/install.sh | bash
```

- Windows: `irm https://raw.githubusercontent.com/Arianna-Lupi/SEO-Skills/main/install.ps1 | iex`
- Plugin: `/plugin update seo-skills@aprendoseo`
- Para solo mirar si hay algo nuevo y qué cambió, sin tocar nada: `/aprendoclub update --check`. Para actualizar desde Claude Code: `/aprendoclub update`.

Es seguro repetirlo: **conserva** tus claves (`~/.claude/seo-skills.env`), tus carpetas `.seo-audit/` y las skills que hayas creado tú. Si habías modificado una skill a mano, guarda una copia en `.seo-skills-backups/` (junto a tu carpeta de skills) antes de sobrescribir y te dice dónde. Las novedades de cada versión están en [`CHANGELOG.md`](CHANGELOG.md).

## Desinstalar

```bash
curl -fsSL https://raw.githubusercontent.com/Arianna-Lupi/SEO-Skills/main/uninstall.sh | bash
```

Windows: `irm https://raw.githubusercontent.com/Arianna-Lupi/SEO-Skills/main/uninstall.ps1 | iex`. Borra solo lo que el instalador registró; tus otras skills y tus datos no se tocan. Con `--dry-run` solo muestra qué quitaría. Si instalaste como plugin: `/plugin uninstall seo-skills@aprendoseo`.

## Instalación: opciones

El camino rápido por defecto solo copia archivos: sin preguntas, sin instalar Python ni paquetes, y vuelve a correr sin romper nada. Descarga un solo paquete comprimido (sin git).

```bash
curl -fsSL https://raw.githubusercontent.com/Arianna-Lupi/SEO-Skills/main/install.sh | bash -s -- --full
```

- `--full`: además prepara [uv](https://astral.sh/uv) (para que los scripts corran solos). Es el único extra que instala el instalador, y solo si lo pides. (PowerShell: `-Full`.)
- `--dir RUTA`: instala en una carpeta concreta (crea `skills/` y `agents/` dentro).
- `--project`: Claude Code, solo el proyecto actual (`./.claude`). `--user` (por defecto): tu usuario (`~/.claude`).
- `--client ID`: otro cliente (`cursor`, `agents`, `codex`, `copilot`; `claude` por defecto).
- `--interactive`: pregunta cliente y alcance con un menú (el comportamiento antiguo).
- `--check`: dice si hay versión nueva, sin instalar. `--ref RAMA`: instala otra rama o etiqueta.

### Soporta varios clientes

- `claude` — Claude Code (por defecto). Instala skills y los 4 subagentes.
- `cursor` — Cursor (`./.cursor/skills`).
- `agents` — VS Code y otros del estándar Agent Skills (`./.agents/skills`).
- `codex` — OpenAI Codex (`./.codex/skills`).
- `copilot` — GitHub Copilot (`./.github/skills`).

Las skills se instalan en todos los clientes. Los subagentes son un concepto de Claude Code, así que solo se instalan ahí; en los demás clientes el instalador lo avisa y las skills siguen funcionando igual.

### Requisitos (spoiler: casi nada)

- **Las skills no necesitan ningún programa.** Son instrucciones en texto: el modelo las lee y hace el trabajo. Si no tienes nada instalado, igual funcionan en "modo manual".
- **Para instalar** solo hace falta `bash` y `curl` (o `wget`). `git` solo como respaldo.
- **Los scripts** (aceleradores opcionales) necesitan Python 3.9 o superior. Casi todos usan solo la biblioteca estándar; unos pocos piden `requests`, `beautifulsoup4` o `tldextract`. Antes de correr uno, el lanzador `aprendoclub-run` revisa qué falta: si falta un paquete **te pregunta antes de instalarlo** (en un entorno aislado, sin sudo) y si falta una clave **te la pide** (una sola vez) explicando para qué sirve y qué alternativa manual existe. Si dices que no, sigues en modo manual. `/aprendoclub setup` muestra el estado de todo. Detalle en [`docs/COMANDOS.md`](docs/COMANDOS.md#requisitos-y-claves).

Si prefieres clonar primero y mirar el código antes de correrlo:

```bash
git clone https://github.com/Arianna-Lupi/SEO-Skills.git
cd SEO-Skills
./install.sh                    # Claude Code, tu usuario (~/.claude), recomendado
# ./install.sh --project        # Claude Code, solo el proyecto actual (./.claude)
# ./install.sh --client cursor  # otro cliente (cursor | agents | codex | copilot)
```

> ¿Qué hace el instalador? Copia cada skill (con su `SKILL.md`, `scripts/` y `references/`) a `~/.claude/skills/` y cada agente a `~/.claude/agents/`, y deja una marca de versión y una lista de lo instalado para poder actualizar o desinstalar con precisión. No pide permisos de administrador ni toca nada más.

## Qué hay aquí

```
SEO-Skills/             ← raíz del repo
├── install.sh / install.ps1      ← instalador rápido (un comando; también actualiza)
├── uninstall.sh / uninstall.ps1  ← desinstalador (borra solo lo que instaló)
├── .claude-plugin/     ← plugin.json y marketplace.json (instalar como plugin de Claude Code)
├── VERSION, CHANGELOG.md ← versión y novedades en español para alumnos
├── PROPUESTA.md        ← propuesta original: skills, internals, fuentes y tiempos
├── FUENTES.md          ← todas las fuentes (diploma + externas + herramientas)
├── COMPLIANCE.md       ← cómo cumple las best practices de agentskills.io
├── MCP-SETUP.md        ← conectar SerpApi (gratis) / GSC mcp-gsc (gratis) / Ahrefs (pago)
├── SCREAMING-FROG.md   ← usar el CLI de Screaming Frog (gratis hasta 500 URLs)
├── ROADMAP.md          ← qué viene (próxima: presentaciones editables en PowerPoint con PPT Master, #1)
├── requirements.txt    ← deps de los scripts (o `uv run` con PEP 723, cero instalación)
├── docs/               ← COMANDOS.md, diseno-presentacion-pptx.md y fragmentos de changelog
├── scripts/            ← validar_skills.py, publicar_version.py, trigger_eval.sh
├── tests/              ← pruebas (estructura, scripts, enrutador, instalador)
├── skills/             ← 31 carpetas; cada una: SKILL.md (+ scripts/ y references/)
│   ├── aprendoclub/                      (enrutador; scripts/aprendoclub-run, requisitos.py, actualizar.py; requisitos.json)
│   ├── investigacion-de-keywords/        (SKILL.md + scripts/expand_keywords.py)
│   ├── mapa-de-palabras-clave/           (+ scripts/canibalizacion.py)
│   ├── deteccion-de-canibalizacion/      (+ scripts/detectar_canibalizacion.py)
│   ├── analisis-serp-y-competencia/      (+ scripts/serp.py, perfil_competidor.py, comparar_serp.py)
│   ├── analisis-de-competidores/         (+ scripts/competitor_domains.py)
│   ├── estrategia-de-contenidos-clusters/(+ scripts/cluster.py)
│   ├── brief-de-contenido/               (+ scripts/serp_outline.py)
│   ├── redaccion-y-optimizacion-nlp/     (+ scripts/readability.py)
│   ├── optimizacion-on-page-meta/        (+ scripts/meta_check.py, serp_metadata.py)
│   ├── auditoria-tecnica/                (+ scripts/parse_sf.py, http_checks.py, puntaje_salud.py)
│   ├── analisis-rendimiento/             (+ scripts/run_unlighthouse.py)
│   ├── arquitectura-y-enlazado-interno/  (+ scripts/orphans.py)
│   ├── reporte-seo-gsc/                  (+ scripts/gsc_report.py)
│   ├── auditoria-de-backlinks-toxicos/   (+ scripts/classify_domains.py, generate_disavow.py)
│   ├── link-building-y-outreach/         (referencia: metodologia-scoring.md)
│   ├── inventario-de-urls/               (+ scripts/inventario_urls.py)
│   ├── optimizacion-geo-aeo/             (+ scripts/ai_features.py)
│   ├── schema-jsonld/                    (+ scripts/schema_gen.py)
│   ├── (y otras 10 de la ronda "diplomado primero": intencion-de-busqueda, actualizacion-de-contenido,
│   │    calidad-de-contenido-eeat, sitemap-y-robots, optimizacion-de-imagenes, plan-seo, proyeccion-seo-gsc,
│   │    seo-local, seo-ecommerce, propuesta-y-reporte-de-servicios-seo)
│   ├── configurar-serpapi/               (+ scripts/set_key.py)           [config]
│   └── dashboard-seo/                    (+ scripts/build_dashboard.py)   [cierre]
└── agents/             ← 4 subagentes (pueden ejecutar los scripts vía Bash)
    ├── agente-investigacion-keywords.md
    ├── agente-auditoria-tecnica.md
    ├── agente-contenido.md
    └── agente-plan-y-entrega.md
```

## Instalación manual (alternativa)

Si no quieres usar `install.sh`, cópialas a mano desde el repo clonado:

```bash
# Skills y agentes a nivel usuario (todos tus proyectos):
cp -R skills/* ~/.claude/skills/
cp agents/*.md ~/.claude/agents/

# o solo en el proyecto actual:
mkdir -p .claude/skills .claude/agents
cp -R skills/* .claude/skills/ && cp agents/*.md .claude/agents/
```

Reinicia Claude Code y verifica:
- Skills: escribe `/` y deberían aparecer (por ejemplo, `/brief-de-contenido`).
- Agentes: Claude delega solo según su `description`, o se lo pides directo ("usa el agente-contenido para esta keyword").

Scripts deterministas (opcional, pero recomendado): los scripts ahorran tokens y dan más precisión. La forma más simple es instalar [uv](https://astral.sh/uv) y correrlos con `uv run` (resuelve las dependencias solo, cero instalación). Si prefieres pip:

```bash
pip install -r requirements.txt
# (los scripts de SerpApi usan la variable de entorno SERPAPI_API_KEY; sin ella, modo manual)
```

## Cómo se usan (ejemplos)

- Un brief rápido: con `/brief-de-contenido` te pide la keyword objetivo y arma el brief (analiza la SERP, decide el formato, redacta las metas, la jerarquía de encabezados y los enlaces).
- Investigación completa: pide "usa el `agente-investigacion-keywords` para el nicho X" y te devuelve la tabla lista para la Plantilla Master, los clusters y los 10 de Oro.
- Flujo de contenido: el `agente-contenido` va de SERP a brief, borrador y on-page, con un checkpoint para que revises el brief antes de redactar.

## Flujo completo → siempre termina en un dashboard

El proceso está pensado para que, sin importar por dónde entres, **siempre termines con un dashboard local** que reúne todo lo encontrado.

1. **Datos del sitio.** `inventario-de-urls` saca las URLs; si hace falta SERP en vivo, `configurar-serpapi` guarda tu API key (una vez).
2. **Investigación y estrategia.** `investigacion-de-keywords` → `mapa-de-palabras-clave` → `analisis-de-competidores` → `analisis-serp-y-competencia` → `estrategia-de-contenidos-clusters`. (O el `agente-investigacion-keywords` de una.)
3. **Contenido.** `brief-de-contenido` → `redaccion-y-optimizacion-nlp` → `optimizacion-on-page-meta` → `schema-jsonld`. (O el `agente-contenido`.)
4. **Técnico.** `auditoria-tecnica` + `analisis-rendimiento` (CWV de todo el sitio) + `arquitectura-y-enlazado-interno` + `reporte-seo-gsc` + `deteccion-de-canibalizacion` (con datos reales de GSC) + `optimizacion-geo-aeo`. (O el `agente-auditoria-tecnica`.)
5. **Cierre.** Cada skill/agente deja su salida estructurada en `.seo-audit/<sitio>/data/*.json`; `dashboard-seo` lo une y te devuelve el **URL local**.

Reglas que sostienen el flujo:
- **Datos estructurados, no prosa perdida.** Cada paso persiste su JSON en `.seo-audit/<sitio>/data/` (carpeta gitignored, datos del cliente). El dashboard funciona con lo que haya: las secciones sin datos se ocultan.
- **Cero números inventados.** Lo que no tengas real (GSC, volumen/KD, Core Web Vitals…) se pide al usuario o se marca `pendiente` — nunca se rellena.
- **Pídelo cuando quieras.** "haz SEO a ejemplo.com y muéstrame el dashboard" dispara el flujo de punta a punta.

## Referencia: qué hace cada skill

Cada skill es una carpeta con un `SKILL.md` (las instrucciones que lee el modelo) y un script Python determinista en `scripts/` (hace las cuentas exactas sin gastar tokens). **No necesitas correr los scripts a mano**: la skill los invoca sola. Aquí abajo se documentan igual por si quieres usarlos sueltos o entender qué devuelven.

Convenciones:
- **Invocar la skill**: escribe el `/comando` en Claude Code, o pídelo en lenguaje natural (la skill se activa sola por su `description`).
- **Correr el script suelto**: `uv run <script>.py …` (recomendado, cero instalación) o `python3 <script>.py …` si ya tienes las deps de `requirements.txt`.
- **Salida de los scripts**: siempre JSON por `stdout`. Si algo falla, devuelven `{"ok": false, "reason": "...", "fallback": "..."}` y salen con código 0 (nunca rompen el flujo: te dicen cómo seguir en modo manual).

> **🚫 Regla de datos: nunca se inventan números.** Todas las skills y agentes tienen prohibido estimar o inventar métricas (volumen, KD, clics, impresiones, CTR, posición, tráfico, CWV, backlinks…). Si falta un dato, te lo piden y esperan tu respuesta: lo pegas a mano, lo exportas (GSC, Ahrefs, DinoRank, Screaming Frog…) o lo conectas por MCP. Si no hay dato, lo marcan como `pendiente de dato` — nunca rellenan con cifras falsas. Un entregable con huecos honestos vale más que uno inventado.

> **Rastreo de sitios protegidos.** Los scripts que piden páginas en vivo (`inventario_urls.py`, `http_checks.py`, `serp_outline.py`) mandan un User-Agent de navegador real, así que rastrean la mayoría de los sitios. Si un sitio está tras Cloudflare u otro WAF que bloquea por *TLS fingerprint*, devolverán `"blocked": true` con instrucciones (whitelistear tu crawler en Cloudflare, exportar URLs desde GSC, o usar Screaming Frog). Puedes forzar otro User-Agent con la variable de entorno `SEO_USER_AGENT`.

### Entrada: el enrutador

**`aprendoclub`**: un solo punto de entrada que decide qué skill o agente hace cada trabajo.
- **Invocar**: `/aprendoclub audit midominio.com` (flujo completo), `/aprendoclub help` (menú) o cualquier subcomando: `technical`, `content`, `keywords`, `competitors`, `architecture`, `onpage`, `schema`, `geo`, `sitemap`, `images`, `performance`, `intent`, `update`, `quality`, `backlinks`, `local`, `ecommerce`, `plan`, `project`, `report`, `proposal`, `dashboard`, `setup`. Cada uno, con ejemplo y salidas, en [`docs/COMANDOS.md`](docs/COMANDOS.md).
- **Devuelve**: el resultado de la skill o el agente al que delega; `audit` recorre 9 fases con pausas para que confirmes, subagentes en paralelo donde las tareas son independientes, puntaje de salud (complemento de claude-seo) y cierre en dashboard.
- **Scripts**: `aprendoclub-run <script>` (lanzador que revisa Python, paquetes y claves antes de correr y pregunta antes de instalar), `requisitos.py` (preflight), `actualizar.py` (comparar versiones). Manifiesto: `requisitos.json`.
- **Base**: orden de las fases del diplomado; patrón del enrutador `/seo` de claude-seo (MIT) como complemento.

### Fase 1 — Investigación y estrategia

**`investigacion-de-keywords`** — investiga y clasifica keywords desde cero.
- **Invocar**: `/investigacion-de-keywords` · "qué términos podría posicionar", "no sé por dónde empezar con SEO".
- **Devuelve**: lista de keywords con intención y clusters, el "punto dulce" (volumen medio-alto × dificultad baja) y las "10 de Oro" para la Plantilla Master.
- **Script**: `expand_keywords.py --seed "<semilla>"` (repetible) o `--file semillas.txt` `[--gl es] [--hl es]`. Expande semillas vía SerpApi (autocomplete + related). Sin `SERPAPI_API_KEY` → modo manual con fallback.

**`mapa-de-palabras-clave`** — asigna 1 keyword primaria por URL y detecta canibalización.
- **Invocar**: `/mapa-de-palabras-clave` · "qué keyword le pongo a cada URL", "tengo páginas peleando por lo mismo".
- **Devuelve**: mapa 1:1 URL↔keyword, lista de canibalización, intención por temperatura y Top 5 de quick wins.
- **Script**: `canibalizacion.py --file mapa.csv` (o `--file -` para stdin, `--format csv|json|auto`). CSV/JSON con filas `{url, keyword, volume?, difficulty?, position?}`. Salida: `cannibalization`, `quick_wins`, `summary`. Stdlib pura.

**`analisis-serp-y-competencia`** — estudia la SERP y encuentra brechas vs. competidores.
- **Invocar**: `/analisis-serp-y-competencia` · "quién me gana en Google", "qué temas no estoy cubriendo".
- **Devuelve**: Competidor de Negocio vs SEO, top 3 con "Ojo Clínico" y reporte de brechas bajo "Costo de Oportunidad".
- **Scripts** (v1.2): `serp.py "<query>" [--gl es] [--hl es] [--num 10]` trae top orgánico, PAA y features vía SerpApi (sin key → modo manual). `perfil_competidor.py` perfila cada página del top (título, encabezados, palabras, tipo de página, schema, señales E-E-A-T, dependencia de JavaScript; acepta URLs, el JSON de `serp.py` o HTML guardado). `comparar_serp.py` compara con tu página: patrón común, brechas, puntaje de Costo de Oportunidad (relativo, no es del diplomado), Análisis de Repetición y tareas con ICE; escribe `competitors.json`. Solo stdlib, rastreo con User-Agent de navegador real y respetando robots.txt. El Ojo Clínico manual va primero; los scripts son el acelerador.

**`analisis-de-competidores`** — descubre por dominio quiénes son tus competidores SEO de una keyword.
- **Invocar**: `/analisis-de-competidores` · "quiénes rankean esta palabra", "sácame los dominios de mi competencia".
- **Devuelve**: lista de dominios priorizada por repetición (aparecer en varias SERPs = crítico) y mejor posición. Desde la v1.2 apunta a `perfil_competidor.py` y `comparar_serp.py` como siguiente paso.
- **Script**: `competitor_domains.py "<kw1|kw2>" [--top 10] [--own midominio.com] [--urls ...] [--no-visit]`. Busca la SERP, entra a cada URL siguiendo redirects y extrae el dominio registrado (eTLD+1). Sin key → modo manual. Deps: requests + tldextract.

**`estrategia-de-contenidos-clusters`** — prioriza qué escribir y arma Topic Clusters.
- **Invocar**: `/estrategia-de-contenidos-clusters` · "ya investigué keywords, ¿ahora qué escribo primero?".
- **Devuelve**: 3-5 clusters (pilar + spokes), las "10 de Oro" priorizadas y la tab "Estrategia" (con E-E-A-T y CRO).
- **Script**: `cluster.py --file keywords.txt` (o `--json`) `[--threshold 0.34]`. Agrupa por similitud Jaccard. Salida: `clusters`, `unclustered`, `count`. Stdlib pura.

**`intencion-de-busqueda`** — Usa esta skill cuando haya que clasificar o VALIDAR la intención de búsqueda de una keyword o de una URL, aunque el usuario no diga "intención", p.ej.
- **Invocar**: `/intencion-de-busqueda` (o pídelo en lenguaje natural; se activa por su `description`).
- **Scripts**: `serp_overlap.py` (todos con `--help`; salida JSON).
- **Base**: diplomado S4 (lecciones 3, 4, 5 y 14) y S5 (lección 6); práctica de Vero y Diana. Complemento claude-seo en `references/`.

### Fase 2 — Producción de contenido

**`brief-de-contenido`** — crea el brief ("la brújula" del redactor) que dicta la SERP.
- **Invocar**: `/brief-de-contenido` · "qué estructura/encabezados pongo", "voy a actualizar este artículo viejo".
- **Devuelve**: brief del tipo correcto (Blog, Landing/Servicios, E-commerce, u Optimización), con encabezados, preguntas y enlaces.
- **Script**: `serp_outline.py "<query>" [--top 5] [--urls url1,url2] [--gl es]`. Analiza los encabezados de los competidores y propone un outline. Con `--urls` salta SerpApi y lee esas URLs directo.

**`redaccion-y-optimizacion-nlp`** — convierte un brief en borrador optimizado y humano.
- **Invocar**: `/redaccion-y-optimizacion-nlp` · "escríbeme/mejora este artículo", "humaniza este texto de IA".
- **Devuelve**: borrador con keyword en H1 + primeras 100 palabras, entidades/NLP, escaneabilidad e Image SEO; pasa el checklist on-page.
- **Script**: `readability.py --keyword "<kw>" [--file art.md | stdin]`. Salida: `word_count`, `keyword_density_pct`, `headings`, `flags` (alerta keyword stuffing, frases largas, etc.). Stdlib pura.

**`optimizacion-on-page-meta`** — genera metatítulo, metadescripción y checklist on-page.
- **Invocar**: `/optimizacion-on-page-meta` · "ármame el título y la descripción", "tengo CTR bajo en Google".
- **Devuelve**: metatítulo (50-60, keyword al inicio), metadescripción (120-155 con CTA), variantes A/B y checklist.
- **Scripts**: `meta_check.py --title "<t>" --desc "<d>" --keyword "<kw>"` valida longitudes y posición de keyword (stdlib pura). `serp_metadata.py "<kw>" [--top 10] [--urls ...]` entra al top de la SERP y extrae metatítulo/metadescripción/H1 de los competidores para tener el benchmark de CTR antes de redactar (deps: requests + beautifulsoup4).

**`schema-jsonld`** — genera datos estructurados Schema.org en JSON-LD válidos.
- **Invocar**: `/schema-jsonld` · "quiero que me salgan las estrellas en Google", "habilita el desplegable de FAQ".
- **Devuelve**: bloque `<script>` JSON-LD listo para pegar, con propiedades requeridas/recomendadas chequeadas.
- **Script**: `schema_gen.py --type <Tipo> [--field k=v …] [--json -]`. Tipos: Article, BlogPosting, Product, FAQPage, HowTo, BreadcrumbList, LocalBusiness, Organization, WebSite. Salida: `jsonld`, `missing_required`, `warnings`. Stdlib pura.

**`actualizacion-de-contenido`** — Usa esta skill cuando haya que mejorar una página que YA existe y no rinde, o decidir qué contenido actualizar primero, aunque el usuario no diga "optimizar" ni "brief", p.ej.
- **Invocar**: `/actualizacion-de-contenido` (o pídelo en lenguaje natural; se activa por su `description`).
- **Scripts**: `gsc_oportunidades.py` (todos con `--help`; salida JSON).
- **Base**: diplomado S10 completa (brief de optimización de contenido existente). Complemento claude-seo en `references/`.

**`calidad-de-contenido-eeat`** — Usa esta skill para revisar la calidad real de una pieza de contenido (borrador o publicada) antes o después de publicar, aunque el usuario no diga "E-E-A-T", p.ej.
- **Invocar**: `/calidad-de-contenido-eeat` (o pídelo en lenguaje natural; se activa por su `description`).
- **Scripts**: `calidad_contenido.py` (todos con `--help`; salida JSON).
- **Base**: diplomado S7 (E-E-A-T), S11 y S14; práctica de Dana y Diana. Complemento claude-seo en `references/`.

### Fase 3 — Técnico, arquitectura y datos en vivo

**`inventario-de-urls`** — saca todas las URLs de un sitio (paso previo a otras skills).
- **Invocar**: `/inventario-de-urls` · "¿cuántas páginas tiene el sitio?", "saca todas las URLs de ejemplo.com".
- **Devuelve**: lista de URLs vía sitemap/robots. Si el sitio bloquea (WAF), `"blocked": true` con instrucciones.
- **Script**: `inventario_urls.py <https://sitio.com> [--sitemap url] [--max 50000]`. Salida: `source`, `count`, `urls`. Stdlib pura (sin claves).

**`auditoria-tecnica`** — auditoría técnica en los 3 bloques (indexabilidad, CWV, seguridad).
- **Invocar**: `/auditoria-tecnica` · "se me cayó el tráfico", "Google no me indexa", "revisa robots.txt / canonical".
- **Devuelve**: issues por severidad, auditoría por plantillas (no página por página) y plan de remediación.
- **Scripts (2)**: `parse_sf.py --folder <carpeta SF>` (o `--internal internal_all.csv --issues issues.csv`) digiere exports de Screaming Frog → status codes, no-indexables, hint por plantilla. `http_checks.py --file urls.txt [--cap 200] [--concurrency 8]` chequea status/HTTPS/redirecciones en vivo cuando no hay export. Ambos detectan bloqueo WAF.

**`analisis-rendimiento`** — rendimiento de TODO el sitio con Unlighthouse (Lighthouse en cada ruta).
- **Invocar**: `/analisis-rendimiento` · "el sitio carga lento", "tengo los CWV en rojo", "qué páginas son las más lentas", "mídeme el rendimiento de todas las páginas".
- **Devuelve**: scores performance/accesibilidad/best-practices/SEO + Core Web Vitals de **laboratorio** (LCP, CLS, TBT, FCP, Speed Index), peores páginas y rendimiento **por plantilla**. Cubre el Bloque 2 de `auditoria-tecnica` a escala de sitio.
- **Script**: `run_unlighthouse.py --site https://sitio.com [--mobile] [--max-routes N]` (corre Unlighthouse vía npx) o `--json ci-result.json` para parsear un export. Escribe `performance.json`. Sin Node → modo manual (PageSpeed Insights). Solo stdlib (Node solo para rastrear en vivo). Laboratorio ≠ campo (CrUX/GSC).

**`arquitectura-y-enlazado-interno`** — diseña arquitectura pilar→clusters y enlazado.
- **Invocar**: `/arquitectura-y-enlazado-interno` · "cómo organizo mis categorías", "el jugo SEO no llega a las páginas que venden".
- **Devuelve**: mapa pilar→clusters, lista de huérfanas y sugerencias de enlaces internos con anchor.
- **Script**: `orphans.py --internal internal_all.csv --inlinks all_inlinks.csv [--low 3]`. Detecta huérfanas, pocos inlinks y profundidad >3 desde exports de Screaming Frog. Stdlib pura.

**`reporte-seo-gsc`** — informe SEO mensual ejecutivo a partir de las 4 métricas de GSC.
- **Invocar**: `/reporte-seo-gsc` · "arma el informe mensual", "¿cómo venimos este mes?".
- **Devuelve**: informe mes vs mes (clics, impresiones, CTR, posición) con interpretación de negocio, ganadores/perdedores e insights.
- **Script**: `gsc_report.py --current cur.csv --previous prev.csv [--top 10]`. CSV de GSC (Query/Clicks/Impressions/CTR/Position). Salida: `totals` con deltas, `winners`, `losers`, `insights`. Stdlib pura.

**`deteccion-de-canibalizacion`** — diagnostica canibalización REAL con datos de ranking (GSC query+página).
- **Invocar**: `/deteccion-de-canibalizacion` · "dos artículos míos se turnan en Google", "esta keyword no despega", "¿fusiono o redirijo estas dos páginas?".
- **Devuelve**: queries con tráfico repartido entre varias URLs, severidad (Alta/Media/Bajo) y acción recomendada (fusionar+301, diferenciar intención o solo monitorear).
- **Script**: `detectar_canibalizacion.py --file gsc_query_page.csv` (o `--file -` para stdin, `--format csv|json|auto`, `--min-impressions N`). CSV/JSON con filas `{query, url, clicks, impressions, position}` (export de GSC con dimensiones Query+Página). Salida: `cannibalization` (con `dominance_ratio`, `severity`, `action`), `summary`. Stdlib pura.

**`optimizacion-geo-aeo`** — optimiza para ser citado en buscadores con IA (AEO/GEO).
- **Invocar**: `/optimizacion-geo-aeo` · "cómo aparezco en ChatGPT", "quiero salir en el resumen de IA de Google".
- **Devuelve**: ajustes para AI Overviews, ChatGPT, Perplexity, Bing Copilot, featured snippet, PAA y Knowledge Panel.
- **Script**: `ai_features.py "<query>" [--gl es] [--hl es]`. Detecta qué features de IA dispara la query vía SerpApi. Sin key → modo manual.

**`sitemap-y-robots`** — Revisa y genera el robots.txt y el sitemap.xml de un sitio, y comprueba que no haya bloqueos accidentales, noindex ni canonicals que contradigan al sitemap.
- **Invocar**: `/sitemap-y-robots` (o pídelo en lenguaje natural; se activa por su `description`).
- **Scripts**: `generar_sitemap_robots.py`, `revisar_robots_sitemap.py` (todos con `--help`; salida JSON).
- **Base**: diplomado S3 y S12 (indexabilidad); práctica de Juan. Complemento claude-seo en `references/`.

**`optimizacion-de-imagenes`** — Audita y optimiza las imágenes de un sitio para SEO y velocidad: peso (más de 100 kb), formato moderno (WebP), dimensiones, texto ALT, nombres de archivo y lazy loading.
- **Invocar**: `/optimizacion-de-imagenes` (o pídelo en lenguaje natural; se activa por su `description`).
- **Scripts**: `auditar_imagenes.py` (todos con `--help`; salida JSON).
- **Base**: diplomado S11/S12 (image SEO, velocidad); complemento claude-seo en `references/`.

### Fase 4 — Link building

**`auditoria-de-backlinks-toxicos`** — clasifica el perfil de backlinks por riesgo y genera el disavow.
- **Invocar**: `/auditoria-de-backlinks-toxicos` · "auditoría de backlinks", "necesito un disavow", "tengo un export de Ahrefs de backlinks", "se me cayó el tráfico y sospecho de link spam".
- **Devuelve**: cada dominio referente clasificado en Toxic/Suspicious/Low-quality-but-safe/Neutral-OK con evidencia auditable, y `disavow.txt` listo para subir a Search Console.
- **Script**: `classify_domains.py --input domain-signals.csv --output domain-classification.csv --related-country ca` + `generate_disavow.py --input domain-classification.csv --output disavow.txt --site midominio.com`. Stdlib pura. Rúbrica completa en `references/rubrica-clasificacion.md`.
- Corre esta skill **antes** de `link-building-y-outreach` — no construyas sobre un perfil sin limpiar.

**`link-building-y-outreach`** — pipeline de enlaces nuevos: fuentes candidatas, gap de competencia, scoring y outreach.
- **Invocar**: `/link-building-y-outreach` · "consígueme backlinks", "qué directorios me faltan", "analiza los enlaces de mi competencia", "hazme un plan de outreach".
- **Devuelve**: pool de fuentes candidatas por categoría, tabla de brecha vs. competencia, tabla maestra con scoring (relevancia/autoridad/viabilidad) por tier, y contenido de outreach ready-to-send para el tier Alto.
- **Metodología**: `references/metodologia-scoring.md`. Ahrefs MCP opcional para el gap (`site-explorer-referring-domains`, `organic-competitors`).

### Fase 5 — Planificación, proyección y verticales

Skills que apoyan el plan SEO completo (contenidos, mapa, Plantilla Master y briefs), la proyección con Search Console y las verticales del diplomado (local, ecommerce, servicios). Se apoyan en la Semana 2, 13, 14 y 16.

**`plan-seo`** — Usa esta skill cuando el usuario necesite convertir un diagnóstico en un plan de trabajo SEO por meses, o definir objetivos y tareas antes de ejecutar, aunque no diga "plan SEO", p.ej.
- **Invocar**: `/plan-seo` (o pídelo en lenguaje natural; se activa por su `description`).
- **Scripts**: `generar_briefs.py`, `generar_master.py`, `generar_plan.py` (todos con `--help`; salida JSON).
- **Base**: diplomado S2, S4, S5, S7, S8, S10 y S13; estructura de la Plantilla Master y de los briefs tomada de lo que comparte la comunidad (solo encabezados, sin datos de nadie).

**`proyeccion-seo-gsc`** — Usa esta skill cuando el usuario quiera saber qué resultados podría tener si cumple el plan SEO, o comparar lo planeado con lo real, aunque no diga "proyección", p.ej.
- **Invocar**: `/proyeccion-seo-gsc` (o pídelo en lenguaje natural; se activa por su `description`).
- **Scripts**: `proyeccion_gsc.py` (todos con `--help`; salida JSON).
- **Base**: extensión pedida por Juan, NO es un método del diplomado: escenarios con supuestos explícitos a partir de Search Console. No es una garantía.

**`seo-local`** — Usa esta skill cuando el negocio tenga ubicación física o atienda a clientes de una zona, o cuando el sitio ofrezca servicios profesionales o marca personal, aunque el usuario no diga "SEO local", p.ej.
- **Invocar**: `/seo-local` (o pídelo en lenguaje natural; se activa por su `description`).
- **Scripts**: `verificar_nap.py` (todos con `--help`; salida JSON).
- **Base**: diplomado S14 (SEO local, servicios, marca personal y negocios pequeños); complemento claude-seo en `references/`.

**`seo-ecommerce`** — Usa esta skill cuando el sitio sea una tienda online o tenga productos y colecciones, aunque el usuario no diga "SEO de ecommerce", p.ej.
- **Invocar**: `/seo-ecommerce` (o pídelo en lenguaje natural; se activa por su `description`).
- **Scripts**: `auditar_producto.py` (todos con `--help`; salida JSON).
- **Base**: diplomado S14 (SEO de ecommerce) y práctica de Juan sobre Shopify; complemento claude-seo en `references/`.

**`propuesta-y-reporte-de-servicios-seo`** — Usa esta skill cuando el usuario quiera vender, empaquetar o entregar servicios SEO a un cliente, aunque no diga "propuesta" ni "paquete", p.ej.
- **Invocar**: `/propuesta-y-reporte-de-servicios-seo` (o pídelo en lenguaje natural; se activa por su `description`).
- **Scripts**: ninguno a propósito; reutiliza otras skills.
- **Base**: diplomado S16 (empaquetar servicios, manejo de clientes) y la voz de Ari sobre negocio y clientes.

### Configuración y cierre

**`dashboard-seo`** — el entregable final: una web local con TODO lo encontrado.
- **Invocar**: `/dashboard-seo` · "muéstrame todo junto", "un panel con los resultados", "una web local con la auditoría". También es el **paso de cierre** automático de cualquier auditoría/investigación/flujo de contenido.
- **Devuelve**: un **URL local** (`http://127.0.0.1:8787/`) con issues por severidad, keywords, 10 de Oro, clusters, competidores, AEO/GEO, auditorías previas, inventario y próximos pasos. Las secciones sin datos se ocultan; lo pendiente se marca, no se inventa.
- **Script**: `build_dashboard.py --site <sitio> [--serve] [--port 8787]`. Lee `.seo-audit/<sitio>/data/*.json` (que escriben las demás skills/agentes) y genera `index.html`. La carpeta `.seo-audit/` va en `.gitignore` (datos del cliente). Stdlib pura.

**`configurar-serpapi`** — conecta datos en vivo de SerpApi (una vez, persistente).
- **Invocar**: `/configurar-serpapi` · "no tengo clave", "quiero datos reales de Google", "aquí está mi api key", "conecta SerpApi". También se ofrece sola cuando otra skill se queda sin datos por falta de clave.
- **Devuelve**: tu API key guardada en `~/.claude/seo-skills.env` (permisos `600`) y validada; a partir de ahí **todas** las skills la usan solas en cada sesión.
- **Script**: `set_key.py --key "<tu_clave>" [--test] [--var SERPAPI_API_KEY]` (o `--key -` por stdin). Guarda/actualiza la variable conservando otras, enmascara la clave en la salida (no la imprime), y con `--test` valida contra SerpApi sin gastar búsquedas. Cuenta gratis: 100 búsquedas/mes sin tarjeta en [serpapi.com](https://serpapi.com/users/sign_up).

## Referencia: los 4 agentes

Los agentes son subagentes de Claude Code que encadenan varias skills en su propio contexto (digieren más datos sin saturar tu chat). Claude delega solo según su `description`, o se lo pides directo ("usa el `agente-…`").

**`agente-investigacion-keywords`** — investigación de keywords completa y a escala.
- **Cuándo**: "ármame el keyword research del nicho X", "lléname la tab de Investigación".
- **Hace**: toma un nicho/semillas, expande y enriquece decenas de keywords, lee varias SERPs, clasifica intención y agrupa en clusters.
- **Devuelve**: lista final con métricas, intención, clusters, "punto dulce", "Duelo de Keywords" y las "10 de Oro" para la Plantilla Master.
- **No** uses para asignar 1 keyword a 1 URL (eso es la skill `mapa-de-palabras-clave`) ni para una duda suelta.

**`agente-contenido`** — pipeline de contenido de punta a punta (Semanas 6 → 8 → 11).
- **Cuándo**: "escríbeme el artículo para esta keyword", "del brief al borrador publicable".
- **Hace**: SERP/competencia → brief del tipo correcto → borrador humanizado (NLP/entidades) → checklist on-page/metas, con un checkpoint para que revises el brief antes de redactar.
- **Devuelve**: borrador optimizado y publicable + metas, encadenando 4 skills.
- **No** uses para solo las metas, un brief sin redacción, u optimizar algo ya escrito (usa la skill suelta correspondiente).

**`agente-auditoria-tecnica`** — auditoría técnica completa de un sitio (Semana 12).
- **Cuándo**: "audita mi web", "por qué cayó mi tráfico", "tengo este export de Screaming Frog/GSC".
- **Hace**: digiere crawls grandes (Screaming Frog/GSC/Ahrefs), audita por plantillas los 3 bloques, compara contra la corrida anterior (diff).
- **Devuelve**: issues clasificados por severidad y plan de remediación priorizado.
- **No** uses para una duda puntual de una etiqueta/canonical/redirección (eso es la skill `auditoria-tecnica`).

**`agente-plan-y-entrega`** — Delega en este agente cuando el usuario quiera pasar del diagnóstico a la ENTREGA a un cliente (Semanas 2, 13, 14 y 16): aunque NO lo nombre: ordenar hallazgos en un plan SEO por meses con objetivos, aplicar la capa vertical que corresponda (tienda online, negocio local o sitio de servicios), y…
- **Hace**: encadena `plan-seo`, `proyeccion-seo-gsc`, las verticales (`seo-local`, `seo-ecommerce`) y `propuesta-y-reporte-de-servicios-seo` en su propio contexto.

## Datos en vivo (opcional)

Sin conectar nada, pegas los datos y listo. Si quieres datos en vivo:
- SerpApi (gratis): SERP, People Also Ask y autocompletar. Conéctalo primero.
- GSC `mcp-gsc` (gratis): Search Console en vivo (reportes y cobertura).
- Ahrefs (pago): volumen, KD, backlinks y auditoría.
- Screaming Frog CLI (gratis hasta 500 URLs): crawl para inventario, auditoría y huérfanas.

Guías: [`MCP-SETUP.md`](./MCP-SETUP.md) para los MCP y [`SCREAMING-FROG.md`](./SCREAMING-FROG.md) para el crawl.

## Customización al diploma

No son skills genéricas: reproducen el método de "De Cero a SEO". Usan la Plantilla Master (la hoja de Google con los tabs Investigación, Mapa, Competencia, Estrategia, Producción y Auditoría), Trello, y la terminología de Arianna ("punto dulce", "Duelo de Keywords", "Mapa de Palabras Clave", "Ojo Clínico", "10 de Oro", "Costo de Oportunidad", temperatura de intención, los 3 tipos de brief, el módulo de NLP y entidades, y el reporte sobre las 4 métricas de GSC).

> Detalle completo, fuentes y estimación de tiempo en [`PROPUESTA.md`](./PROPUESTA.md).

## Fuentes y créditos

- **El diplomado manda.** Cada skill sigue el método de "De Cero a SEO" y lo cita (`references/metodo-diploma.md`, Semana y lección). Lo que viene de otras fuentes va aparte en `references/complementos-claude-seo.md`, etiquetado como complemento externo, y nunca sustituye al método.
- **claude-seo** (MIT, © 2026 agricidaniel, https://github.com/AgriciDaniel/claude-seo): complementos adaptados al español y al método del diplomado. Detalle por skill en [`FUENTES.md`](FUENTES.md) y licencia en [`THIRD-PARTY-LICENSES.md`](THIRD-PARTY-LICENSES.md).
- **Práctica de los coaches de la comunidad** (Vero, Ibra, Diana, Dana, Ari y Juan): `references/practica-coaches.md` en las skills que la usan.
- **Validar el repo**: `python3 scripts/validar_skills.py` (frontmatter, enlaces, scripts, evals y referencias de agentes).
