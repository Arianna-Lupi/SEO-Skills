# Comandos de configuración y actualización

## `/aprendoclub setup`

Muestra el estado del entorno y ofrece resolver lo que falte, siempre con confirmación.

1. Corre `aprendoclub-run --status` (en Windows, `aprendoclub-run.ps1 --status`). Devuelve Python y versión, si existe `uv`, el entorno aislado, los paquetes, las claves (solo si existen o no, nunca su valor), las herramientas (Node, Screaming Frog) y los conectores MCP.
2. Resume en una tabla corta: qué está listo y qué falta. Todo lo que falta es opcional: sin eso, cada skill sigue en modo manual.
3. Ofrece resolver cada faltante, uno por uno:
   - **Paquetes de Python:** pregunta, muestra el comando exacto y qué paquetes son, e instala solo con un sí (`aprendoclub-run --install <script> --yes`, entorno aislado, sin sudo).
   - **Claves** (`SERPAPI_API_KEY`, `CRUX_API_KEY`, `PSI_API_KEY`): pídelas explicando para qué sirven y que hay alternativa manual; guárdalas con `configurar-serpapi` (por stdin, permisos 600). Nunca las imprimas.
   - **Python o herramientas:** muestra el comando y espera la decisión del usuario.
   - **Conectores MCP** (Search Console, Ahrefs, Google Drive y Sheets): no se pueden detectar desde la terminal. Indica revisar con `/mcp` y dirige a `MCP-SETUP.md`.
4. Termina con el estado actualizado.

## `/aprendoclub update` (sin URL) y `/aprendoclub upgrade`

Actualiza las propias skills. Con una URL, `update` es la actualización de contenido (ver `comandos-contenido.md`).

1. Corre `aprendoclub-run --update-check` (usa la red porque el usuario lo pidió; si no hay conexión lo dice y no es un error). Con `--offline` solo muestra lo instalado.
2. Muestra: versión instalada, versión disponible y "qué hay de nuevo" (viene de `CHANGELOG.md`, en lenguaje de alumno). Si ya está al día, dilo y termina.
3. Con `--check`, termina aquí: no se cambia nada.
4. Sin `--check`, pregunta si actualiza. Con un sí, ejecuta el comando según el modo de instalación que devolvió el chequeo:
   - **Instalador:** `curl -fsSL https://raw.githubusercontent.com/Arianna-Lupi/SEO-Skills/main/install.sh | bash` (Windows: `irm https://raw.githubusercontent.com/Arianna-Lupi/SEO-Skills/main/install.ps1 | iex`).
   - **Plugin:** indícale al usuario que escriba `/plugin update seo-skills@aprendoseo` (es un comando de Claude Code, no de la terminal).
5. Explica qué se conserva: `~/.claude/seo-skills.env` (claves) y `.seo-audit/` no se tocan, y si el usuario había modificado una skill a mano, el instalador guarda una copia antes de sobrescribir (te dice dónde). Pide reiniciar Claude Code.

Aviso al iniciar (opcional, apagado por defecto): con `{"avisar_actualizaciones": true}` en `~/.claude/aprendoclub/config.json`, `/aprendoclub` muestra una línea si hay versión nueva, como máximo una consulta al día, sin bloquear.
