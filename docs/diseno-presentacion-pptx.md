# Diseño: presentación editable para clientes con PPT Master

Estado: **solo diseño, sin implementar**. La implementación queda para la versión siguiente, salvo que Juan la pida antes. Reemplaza la idea anterior de usar Slidev (issue #1 del ROADMAP).

## Objetivo

Convertir lo que dejó una auditoría en `.seo-audit/<sitio>/data/*.json` en una presentación `.pptx` editable (formas y textos nativos de PowerPoint, no imágenes) para entregar a un cliente. Nombre tentativo: skill `presentacion-pptx`. Alternativa: subcomando de `/aprendoclub report` o `/aprendoclub proposal`. Decisión pendiente de Juan: esta documentación no la toma.

## Qué es PPT Master (lo que se leyó y lo que no)

Fuente: README, `LICENSE` y `skills/ppt-master/requirements.txt` del repo https://github.com/hugohe3/ppt-master, leídos el 2026-10-26. **No se leyó el código de los scripts**, así que lo que sigue es lo que el proyecto dice de sí mismo, no una auditoría.

- **Qué hace:** skill para un agente de IA. Convierte PDF, DOCX, imágenes, HTML, EPUB, notebooks, texto pegado o una URL en un `.pptx` con formas, textos e imágenes nativos, con transiciones y notas del orador. Salida en `exports/<nombre>_<fecha>.pptx`; también deja vistas previas SVG en `svg_final/`.
- **Licencia:** MIT, "Copyright (c) 2025-2026 Hugo He", sin condiciones extra. Obligación: conservar el aviso de copyright y de permiso si se copia código o texto suyo.
- **Requisitos:** Python 3.10 o superior (este repo exige 3.9: ver "Compatibilidad"). Dependencias en `skills/ppt-master/requirements.txt`. Núcleo de la conversión a PPTX: `python-pptx` (y `XlsxWriter`). El resto es opcional y varía según el formato de entrada: `PyMuPDF` (PDF; **licencia AGPL-3.0**, pesada), `mammoth` (DOCX), `nbconvert` (pesada), `Pillow`, `numpy`, `skia-pathops` y `uharfbuzz` (binarios nativos), `edge-tts` (voz), `google-genai` (imágenes con Gemini), `flask` (editor SVG local). Pandoc solo para formatos antiguos.
- **Instalación según su README:** `git clone https://github.com/hugohe3/ppt-master.git` y `pip install -r requirements.txt`; o `npx skills add hugohe3/ppt-master`; o en Claude Code `/plugin marketplace add hugohe3/ppt-master` y `/plugin install ppt-master@ppt-master`. Actualizar: `python3 skills/ppt-master/scripts/update_repo.py` (hace `git pull`).
- **Red:** el README afirma que todo corre en local, salvo los modelos de IA y los servicios de imágenes, búsqueda o voz que se activen. `image_gen.py` pide clave de un proveedor; `image_search.py` consulta Openverse y Wikimedia Commons sin clave (y Pexels o Pixabay si hay clave); `update_repo.py` hace `git pull`. Hay un `.env.example` para esas claves.
- **Aviso:** el README trae muchos enlaces de patrocinio o afiliados de proveedores de API. No condicionan nada, pero hay que elegir proveedor con criterio propio.

## Principios de la integración

1. **Opcional.** Las SEO Skills funcionan igual sin PPT Master. Nada del flujo de auditoría depende de él.
2. **Confirmación antes de instalar.** Mismo protocolo que el lanzador `aprendoclub-run`: detectar, preguntar, mostrar el comando exacto y qué instala, aislar, y solo entonces ejecutar. Nunca clonar ni instalar sin un sí explícito de Juan o del usuario.
3. **Aislamiento.** Clon en `~/.claude/aprendoclub/ppt-master/` y dependencias en un entorno propio (`~/.claude/aprendoclub/.venv-ppt`), nunca globales, nunca con sudo. Instalar solo el núcleo (`python-pptx` y lo que pida el formato de entrada que usaremos, que es Markdown). **No instalar `PyMuPDF`** (AGPL, y no hace falta si la entrada es Markdown).
4. **Caída elegante.** Si el usuario no tiene PPT Master o dice que no, la skill entrega el **documento fuente en Markdown** (el mismo que habría recibido PPT Master) y una guía corta para generar el PPTX por su cuenta: instalar PPT Master o pegar el Markdown en la herramienta de presentaciones que prefiera.
5. **La regla de datos manda.** Nunca se inventan números. La presentación solo contiene lo que está en `data/*.json`; lo que falta aparece como `pendiente de dato`. Las proyecciones se muestran siempre como escenarios con sus supuestos a la vista y la aclaración de que no son una garantía ni un método del diplomado.

## Flujo propuesto

1. **Chequeo de requisitos.** Se amplía `requisitos.json` con una herramienta `ppt-master` (comando de detección: existencia de `~/.claude/aprendoclub/ppt-master/skills/ppt-master/SKILL.md`; paquetes necesarios; Python 3.10+; riesgo de red declarado). `aprendoclub-run --check` devuelve un `needs` de tipo `tool` con `required: false` y el `fallback` de arriba.
2. **Documento fuente.** Un script nuevo `generar_fuente_presentacion.py` (solo stdlib) lee `.seo-audit/<sitio>/data/*.json` y escribe `.seo-audit/<sitio>/entregables/presentacion-fuente.md`. Un encabezado `##` por diapositiva, notas del orador bajo cada una.
3. **Revisión humana.** Se muestra el Markdown al usuario. Se corrige, se quita lo que no quiera enseñar. Sin ese visto bueno no se avanza.
4. **Generación.** Con PPT Master instalado y confirmado, se le entrega ese Markdown con la instrucción de usar la plantilla de aprendoseo y el modo sin imágenes generadas ni búsqueda de imágenes. Salida: `.seo-audit/<sitio>/entregables/presentacion.pptx`.
5. **Cierre.** Se ofrece abrir el archivo y se vuelve a `dashboard-seo` como siempre.

## Estructura del documento fuente

| Diapositiva | Sale de | Notas |
|-------------|---------|-------|
| Resumen ejecutivo | `meta.json` | Qué se auditó, fecha, 3 hallazgos principales en lenguaje de negocio |
| Salud técnica | `issues.json` y puntaje de `meta.json` | Críticos y altos por plantilla. El puntaje se rotula como complemento de claude-seo, no como dato de Google |
| Rendimiento | `performance.json`, `cwv-field.json` | Laboratorio y campo separados y rotulados |
| Oportunidades de contenido | `keywords.json`, `clusters.json` | Volumen y KD solo si son reales; si no, `pendiente de dato` |
| Competencia | `competitors.json` (incluye `serp_analysis`) | Brechas y puntaje de costo de oportunidad, rotulado como puntaje relativo |
| IA y GEO | `ai-features.json` | Solo lo observado |
| Contenido entregado | `content-briefs.json` | Títulos, keyword, estado |
| Plan | `next-steps.json`, `plan-seo.json` | Tareas que empiezan con verbo, con ICE y mes |
| Proyección | `proyeccion-gsc.json` | Escenarios con supuestos explícitos, solo si hay Search Console |
| Próximos pasos | `next-steps.json` | Las 5 primeras tareas |

## Marca de aprendoseo

Las plantillas se adaptan al estilo de marca de aprendoseo con PPT Master (que permite crear una plantilla a partir de referencias o usar un `.pptx` propio como plantilla). **Pendiente de dato:** colores, tipografías, logo y ejemplos de diapositivas que Juan quiera como referencia. No se inventan. Hasta tenerlos, se usa el diseño libre de PPT Master con un tema neutro.

## Datos que nunca salen de la máquina del usuario

- Exports crudos de Search Console, Ahrefs o Screaming Frog, listas de URLs completas del cliente, correos, nombres de personas y cualquier archivo fuera de `data/*.json`.
- Claves de API (`~/.claude/seo-skills.env`). El `.env` de PPT Master queda sin claves.
- Imágenes del cliente.

Lo que sí ve el modelo de IA es el Markdown fuente que el usuario aprobó, igual que cualquier otro contenido de la conversación. Se desactivan por defecto la generación de imágenes (`image_gen.py`), la búsqueda de imágenes (`image_search.py`) y la narración por voz (`edge-tts`): son los puntos donde PPT Master puede mandar datos a terceros. Si el usuario quiere alguno, se explica qué se enviaría y se pide confirmación aparte.

## Compatibilidad

PPT Master pide Python 3.10 o superior; las SEO Skills piden 3.9. El chequeo debe avisar y ofrecer `uv python install` o el modo Markdown. No se sube el mínimo de las SEO Skills por esto.

## Créditos y licencias

Si la integración solo **invoca** PPT Master como herramienta externa, basta mencionarlo en `FUENTES.md`. Si algún día se copia código o texto suyo al repo, se agrega a `THIRD-PARTY-LICENSES.md` el texto de su licencia MIT con "Copyright (c) 2025-2026 Hugo He". `PyMuPDF` (AGPL-3.0) no se incorpora ni se instala.

## Qué falta decidir con Juan

1. ¿Skill propia (`presentacion-pptx`) o subcomando de `report` o `proposal`?
2. Marca: colores, tipografías, logo y diapositivas de referencia.
3. ¿Se acepta la dependencia de Python 3.10 solo para esta función opcional?
4. ¿Idioma de las diapositivas: solo español, o también inglés?
5. Antes de implementar: leer el código de los scripts que se van a ejecutar (`svg_to_pptx.py` y el flujo de `SKILL.md`), porque hoy solo se revisó la documentación.
