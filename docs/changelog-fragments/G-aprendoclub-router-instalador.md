# Fragmento G: enrutador `/aprendoclub`, instalación rápida, requisitos, actualización y presentaciones

Pedido de Juan (vía la sesión `kajabi-foro-tracker-e2`). Base: orden de fases del diplomado; patrones de enrutador e instalador de claude-seo (MIT) como complemento. No se hizo commit, push ni publicación.

## Skill nueva `aprendoclub` (1.0)
- `SKILL.md` con el menú de 25 subcomandos (`audit`, `technical`, `content`, `keywords`, `competitors`, `architecture`, `onpage`, `schema`, `geo`, `sitemap`, `images`, `performance`, `intent`, `update`, `quality`, `backlinks`, `local`, `ecommerce`, `plan`, `project`, `report`, `proposal`, `dashboard`, `setup`, `upgrade`, `help`), reglas de enrutamiento y el protocolo previo a cualquier script.
- `audit <sitio>`: 9 fases (0 descubrimiento, 1 técnico S3 y S12, 2 arquitectura S9, 3 keywords y contenido S4 a S8, S10, S11, 4 competencia S6, 5 GEO/AEO y off page, 6 vertical, 7 plan, 8 reporte y siempre `dashboard-seo`), checkpoints tras 0, 1, 3 y 7, paralelismo solo entre tareas independientes, puntaje con `puntaje_salud.py` guardado en `meta.json`. Detalle en `references/comandos-audit.md`.
- `references/`: `comandos-audit.md`, `comandos-tecnico.md`, `comandos-contenido.md`, `comandos-competencia-offpage.md`, `comandos-plan-entrega.md`, `comandos-config.md` (setup y update), `dependencias.md`, `metodo-diploma.md`, `complementos-claude-seo.md` (etiquetado como complemento externo).
- `update` tiene dos usos y se documentó: con URL es `actualizacion-de-contenido`; sin URL (o `upgrade`) actualiza las skills. Decisión mía para respetar los dos pedidos; Juan puede renombrar uno.
- `competitors` usa los scripts de la v1.2 (`serp.py`, `perfil_competidor.py`, `comparar_serp.py`) y `competitor_domains.py`.

## Requisitos y claves (`requisitos.json`, `aprendoclub-run`)
- `skills/aprendoclub/requisitos.json`: por cada uno de los 54 scripts, paquetes de Python (requeridos y opcionales), variables de entorno (claves y variables), herramientas externas (Node, Screaming Frog), conectores MCP (Search Console, Ahrefs, Drive, Sheets) y el modo manual. Solo nombres, jamás valores.
- `scripts/aprendoclub-run` (bash) y `aprendoclub-run.ps1`: intérprete en este orden `APRENDOCLUB_PYTHON`, `python3`, `python`, `py -3` (3.9 o superior, ignora el atajo de la Microsoft Store). Sin Python devuelve JSON con `needs` y cómo instalarlo.
- `scripts/requisitos.py` (stdlib): `--check`, `--check --all`, `--status`, `--install <script> --yes`, y ejecución con preflight. `--install` exige `--yes`, solo instala paquetes del manifiesto, en `~/.claude/aprendoclub/.venv`, con `uv` si hay o `venv` más `pip`; sin sudo. Las claves se leen del entorno o de `~/.claude/seo-skills.env` y nunca se imprimen.
- Contrato unificado: `{"ok", "needs":[{"type","name","required",...}], "reason", "fallback"}`. `reason` y `fallback` conservan el contrato antiguo de los scripts. No se editó ningún script de otras skills.
- Diferencia con el pedido: `uv` no se usa como intérprete de ejecución (`uv run` instalaría dependencias sin preguntar); se usa solo para crear el entorno aislado cuando el usuario aprobó.
- `validar_skills.py` comprueba que cada script esté en el manifiesto, que los imports de terceros y las variables de entorno coincidan con lo que declara y que haya `modo_manual` cuando hace falta.

## Instalación, actualización y desinstalación
- `install.sh` e `install.ps1` reescritos: tarball de GitHub (`codeload`) sin git, sin menús ni preguntas, sin instalar nada (el menú antiguo ahora es `--interactive`; `--full` agrega uv; `--ref`; `--dir`; `--check`), idempotentes, con respaldo de lo modificado a mano (huella por skill guardada en `.seo-skills-manifest`; copias en `.seo-skills-backups/` junto a la carpeta de skills). Respaldo vía `git clone` si no hay curl ni wget. Se arregló un error del instalador anterior: al correr por `curl | bash` desde una carpeta que tuviera `skills/` instalaba esa carpeta en vez de descargar.
- `uninstall.sh` y `uninstall.ps1`: borran solo lo del manifiesto; sin manifiesto (instalación antigua) descargan la lista de nombres del repo. `--dry-run`.
- `.claude-plugin/plugin.json` y `marketplace.json` (plugin `seo-skills`, marketplace `aprendoseo`; `/plugin marketplace add Arianna-Lupi/SEO-Skills` y `/plugin install seo-skills@aprendoseo`). Sin campo `license` porque el repo no tiene archivo LICENSE: decisión pendiente de Juan.
- Actualizar = volver a correr el instalador; conserva `~/.claude/seo-skills.env`, `.seo-audit/` y skills propias. `/aprendoclub update --check` (`actualizar.py`): compara `VERSION` con la última publicada (con red, a petición del usuario; sin conexión avisa y no falla) y muestra `CHANGELOG.md`. Aviso al iniciar: opcional y apagado por defecto (`~/.claude/aprendoclub/config.json`).
- `CHANGELOG.md` nuevo, en español para alumnos. `scripts/publicar_version.py`: sube `VERSION`, `plugin.json` y `marketplace.json`, convierte "Próxima versión" del changelog, genera `docs/ANUNCIO-ACTUALIZACION.md` (3 a 6 viñetas y comandos para macOS/Linux, Windows y plugin) e imprime los pasos de git sin ejecutarlos.

## Documentación y pruebas
- README: "Inicio rápido", "Actualizar" y "Desinstalar" arriba; opciones del instalador; árbol actualizado; sección del enrutador; scripts y versión 1.2 de las skills de competencia. `docs/COMANDOS.md` nuevo. ROADMAP y FUENTES actualizados.
- Presentaciones: se quitó Slidev y se documentó el cambio a PPT Master (MIT) en ROADMAP; diseño sin implementar en `docs/diseno-presentacion-pptx.md` (leído: README, LICENSE y requirements del repo; NO el código de los scripts).
- `tests/test_aprendoclub.py` (19 pruebas, 1 con red opcional: preflight sin dependencias devuelve `needs`, claves no se imprimen, lanzador sin Python, validador, actualizador sin red) y `tests/test_instalador.py` (13: instalación rápida, idempotencia, actualización desde una versión simulada conservando config y `.seo-audit/` y creando respaldo, instalación por pipe con tarball, desinstalación, `publicar_version.py`).

## Qué no se pudo probar
- `install.ps1`, `uninstall.ps1` y `aprendoclub-run.ps1`: no hay PowerShell en esta máquina; solo revisión de lectura.
- El flujo de plugin (`/plugin marketplace add`, `/plugin install`, `/plugin update`): requiere el repo publicado y Claude Code interactivo.
- `curl | bash` contra GitHub con esta versión: el repositorio remoto `main` todavía trae la versión vieja (20 skills). Se probó con un tarball local (`SEO_SKILLS_TARBALL_URL`) y la descarga real de `main`.
- `--install` creó el entorno y bajó paquetes solo en la prueba manual (ver informe); no está en las pruebas automáticas porque necesita red.
- `/aprendoclub audit` de punta a punta con un sitio real: es instrucción para el modelo, no código; sin ejecución de ejemplo.

## Para Juan (decisiones)
- Subir `VERSION` (hoy 1.3.0, como el plugin): `python3 scripts/publicar_version.py --bump minor` cuando decida publicar.
- Añadir un archivo LICENSE y el campo `license` al plugin.
- Si el instalador debe apuntar a `main` o `develop` mientras no se haga merge: `--ref develop`.
