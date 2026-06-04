# SEO skills y agentes de Claude (aprendoseo, "De Cero a SEO")

13 skills y 3 agentes de Claude Code para automatizar los flujos SEO del equipo,
customizados con el método interno del diplomado "De Cero a SEO". Funcionan sin conectar
nada y, si quieres, se conectan a SerpApi (gratis), Google Search Console (gratis) o
Ahrefs (pago).

## Instalación (un comando)

Pega esto en tu terminal. Descarga e instala todas las skills y agentes en tu Claude Code:

```bash
curl -fsSL https://raw.githubusercontent.com/Arianna-Lupi/SEO-Skills/main/install.sh | bash
```

En Windows (PowerShell):

```powershell
irm https://raw.githubusercontent.com/Arianna-Lupi/SEO-Skills/main/install.ps1 | iex
```

Reinicia tu cliente y escribe `/` para verlas (por ejemplo `/brief-de-contenido`).

### Soporta varios clientes

El instalador funciona con Claude Code y con otros clientes que usan el estándar
Agent Skills. Si corres el comando en una terminal interactiva, te muestra un menú para
elegir. Si no, instala en Claude Code por defecto. Para elegir directo, usa `--client`
(`-Client` en PowerShell):

- `claude` — Claude Code (por defecto). Instala skills y los 3 subagentes.
- `cursor` — Cursor (`./.cursor/skills`).
- `agents` — VS Code y otros del estándar Agent Skills (`./.agents/skills`).
- `codex` — OpenAI Codex (`./.codex/skills`).
- `copilot` — GitHub Copilot (`./.github/skills`).

```bash
curl -fsSL https://raw.githubusercontent.com/Arianna-Lupi/SEO-Skills/main/install.sh | bash -s -- --client cursor
```

Las skills se instalan en todos los clientes. Los subagentes son un concepto de Claude
Code, así que solo se instalan ahí; en los demás clientes el instalador lo avisa y las
skills siguen funcionando igual.

### Requisitos (spoiler: casi nada)

- **Las skills no necesitan ningún programa.** Son instrucciones en texto: el modelo las
  lee y hace el trabajo. Sin Python, sin Node, sin nada. Si no tienes nada instalado,
  igual funcionan.
- **Para instalar** solo hace falta `git` (el instalador lo usa para descargar).
- **Los scripts siempre pueden correr** si dejas que el instalador configure
  [uv](https://astral.sh/uv): es un paso extra, sin permisos de administrador y sin
  Python del sistema (uv trae su propio Python y resuelve las dependencias solo). En una
  terminal interactiva el instalador te pregunta si quieres instalarlo; si corres el
  comando piped (curl|bash), no instala nada en silencio pero te muestra el comando, o lo
  fuerzas con `--with-uv` (`-WithUv` en PowerShell). Si no quieres uv, las skills siguen en
  "modo manual" y no se rompe nada. Para saltar el chequeo: `--no-uv` (`-NoUv`).

Eso instala a nivel usuario (`~/.claude/`), así las tienes en todos tus proyectos. Si
prefieres clonar primero y mirar el código antes de correrlo:

```bash
git clone https://github.com/Arianna-Lupi/SEO-Skills.git
cd SEO-Skills
./install.sh                    # Claude Code, tu usuario (~/.claude) — recomendado
# ./install.sh --project        # Claude Code, solo el proyecto actual (./.claude)
# ./install.sh --client cursor  # otro cliente (cursor | agents | codex | copilot)
# ./install.sh --with-uv        # además configura uv para que los scripts corran solos
```

> ¿Qué hace el instalador? Copia cada skill (con su `SKILL.md`, `scripts/` y
> `references/`) a `~/.claude/skills/` y cada agente a `~/.claude/agents/`. No pide
> permisos de administrador ni toca nada más.

## Actualizar

El instalador deja una marca de versión en tu carpeta de skills, así que sabe
cuándo salió algo nuevo. Para ver si hay actualización sin tocar nada:

```bash
curl -fsSL https://raw.githubusercontent.com/Arianna-Lupi/SEO-Skills/main/install.sh | bash -s -- --check
# Windows:  & ([scriptblock]::Create((irm https://raw.githubusercontent.com/Arianna-Lupi/SEO-Skills/main/install.ps1))) -Check
```

Te dice qué versión tienes instalada y cuál es la última. Si hay una nueva,
vuelve a correr el comando de instalación: detecta tu versión anterior, te
avisa y te pregunta antes de sobrescribir. Para actualizar sin que pregunte,
usa `--update` (PowerShell: `-Update`). Si instalaste desde un clon del repo,
trae primero los cambios con `git pull` y vuelve a correr `./install.sh`.

## Qué hay aquí

```
SEO-Skills/             ← raíz del repo
├── install.sh          ← instalador de un comando
├── PROPUESTA.md        ← LÉEME PRIMERO: 13 skills + 3 agentes, internals,
│                          fuentes y tiempos (el entregable de la tarea)
├── FUENTES.md          ← todas las fuentes (diploma + externas + herramientas)
├── COMPLIANCE.md       ← cómo cumple las best practices de agentskills.io
├── MCP-SETUP.md        ← conectar SerpApi (gratis) / GSC mcp-gsc (gratis) / Ahrefs (pago)
├── SCREAMING-FROG.md   ← usar el CLI de Screaming Frog (gratis hasta 500 URLs)
├── requirements.txt    ← deps de los scripts (o usá `uv run` con PEP 723, cero instalación)
├── scripts/trigger_eval.sh ← runner de pruebas de activación de descripciones
├── README.md           ← este archivo
├── skills/             ← 13 carpetas; cada una: SKILL.md + scripts/<script>.py
│   ├── investigacion-de-keywords/        (SKILL.md + scripts/expand_keywords.py)
│   ├── mapa-de-palabras-clave/           (+ scripts/canibalizacion.py)
│   ├── analisis-serp-y-competencia/      (+ scripts/serp.py)
│   ├── estrategia-de-contenidos-clusters/(+ scripts/cluster.py)
│   ├── brief-de-contenido/               (+ scripts/serp_outline.py)
│   ├── redaccion-y-optimizacion-nlp/     (+ scripts/readability.py)
│   ├── optimizacion-on-page-meta/        (+ scripts/meta_check.py)
│   ├── auditoria-tecnica/                (+ scripts/parse_sf.py, http_checks.py)
│   ├── arquitectura-y-enlazado-interno/  (+ scripts/orphans.py)
│   ├── reporte-seo-gsc/                  (+ scripts/gsc_report.py)
│   ├── inventario-de-urls/               (+ scripts/inventario_urls.py)   [extra]
│   ├── optimizacion-geo-aeo/             (+ scripts/ai_features.py)       [extra]
│   └── schema-jsonld/                    (+ scripts/schema_gen.py)        [extra]
└── agents/             ← 3 subagentes (pueden ejecutar los scripts vía Bash)
    ├── agente-investigacion-keywords.md
    ├── agente-auditoria-tecnica.md
    └── agente-contenido.md
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
- Agentes: Claude delega solo según su `description`, o se lo pides directo ("usa el
  agente-contenido para esta keyword").

Scripts deterministas (opcional, pero recomendado): los scripts ahorran tokens y dan más
precisión. La forma más simple es instalar [uv](https://astral.sh/uv) y correrlos con
`uv run` (resuelve las dependencias solo, cero instalación). Si prefieres pip:

```bash
pip install -r requirements.txt
# (los scripts de SerpApi usan la variable de entorno SERPAPI_API_KEY; sin ella, modo manual)
```

## Cómo se usan (ejemplos)

- Un brief rápido: con `/brief-de-contenido` te pide la keyword objetivo y arma el brief
  (analiza la SERP, decide el formato, redacta las metas, la jerarquía de encabezados y
  los enlaces).
- Investigación completa: pide "usa el `agente-investigacion-keywords` para el nicho X" y
  te devuelve la tabla lista para la Plantilla Master, los clusters y los 10 de Oro.
- Flujo de contenido: el `agente-contenido` va de SERP a brief, borrador y on-page, con
  un checkpoint para que revises el brief antes de redactar.

## Datos en vivo (opcional)

Sin conectar nada, pegas los datos y listo. Si quieres datos en vivo:
- SerpApi (gratis): SERP, People Also Ask y autocompletar. Conéctalo primero.
- GSC `mcp-gsc` (gratis): Search Console en vivo (reportes y cobertura).
- Ahrefs (pago): volumen, KD, backlinks y auditoría.
- Screaming Frog CLI (gratis hasta 500 URLs): crawl para inventario, auditoría y
  huérfanas.

Guías: [`MCP-SETUP.md`](./MCP-SETUP.md) para los MCP y
[`SCREAMING-FROG.md`](./SCREAMING-FROG.md) para el crawl.

## Customización al diploma

No son skills genéricas: reproducen el método de "De Cero a SEO". Usan la Plantilla
Master (la hoja de Google con los tabs Investigación, Mapa, Competencia, Estrategia,
Producción y Auditoría), Trello, y la terminología de Arianna ("punto dulce", "Duelo de
Keywords", "Mapa de Palabras Clave", "Ojo Clínico", "10 de Oro", "Costo de Oportunidad",
temperatura de intención, los 3 tipos de brief, el módulo de NLP y entidades, y el
reporte sobre las 4 métricas de GSC).

> Detalle completo, fuentes y estimación de tiempo en [`PROPUESTA.md`](./PROPUESTA.md).
