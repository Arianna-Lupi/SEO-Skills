# Changelog fragmento F: análisis de competidores basado en la SERP

Pedido de Juan: análisis de competidores a partir de lo que aparece en la SERP de una keyword. Se amplió `analisis-serp-y-competencia` (1.1 a 1.2) con el flujo completo SERP, competidores, perfil, comparación, brechas y tareas, y se conectó con `analisis-de-competidores` (1.1 a 1.2). No se creó ninguna skill nueva: la base está en la Semana 6 y las demás lecciones citadas abajo, y las skills que ya existían cubren el resto.

## `analisis-serp-y-competencia` v1.2

- `SKILL.md`: flujo en 10 pasos numerados. Los pasos 1 a 4, 6 y 8 a 9 son el método del diplomado (Negocio vs SEO, 3 métodos, Análisis de Repetición, Ojo Clínico sobre el top 3, Plantilla Master con 50 a 60 %, reporte con Costo de Oportunidad, tareas con verbo). Los scripts (pasos 5, 7) quedan como acelerador, después del Ojo Clínico. Nuevo paso 2 "leer la SERP y el tipo de contenido que premia" (Semana 4 · lección 8; Semana 8 · lección 3) con remisión a `intencion-de-busqueda` cuando hay desajuste. Origen: Semana 6 · lecciones 1 a 7.
- Script nuevo `scripts/perfil_competidor.py` (solo stdlib): por URL del top extrae título, meta, H1 a H3 en orden, palabras, tipo de página con heurísticas explicadas (`page_type_signals`), schema JSON-LD, imágenes con alt, enlaces internos y externos, fechas, autoría y E-E-A-T visibles, FAQ/listas/tablas/vídeo y dependencia de JavaScript. Acepta URLs, `--urls-file`, uno o varios JSON de `serp.py` y `--html` (modo sin red, `URL=archivo`). Rastreo con User-Agent de navegador real (`SEO_USER_AGENT`), robots.txt respetado, pausa de 2 s por defecto y detección de WAF con mensaje de salida, igual que `inventario_urls.py`. Origen del patrón de rastreo: `skills/inventario-de-urls/scripts/inventario_urls.py`.
- Script nuevo `scripts/comparar_serp.py` (solo stdlib): patrón común del top (al menos 60 %), tabla tu página frente al top, brechas por categoría (tipo de página, cobertura de temas, estructura, formato, schema, E-E-A-T, frescura), puntaje de Costo de Oportunidad con fórmula escrita en el informe, Análisis de Repetición con varias keywords (dominios y URLs; crítico a partir de 60 % de las keywords, mínimo 2, por analogía con el 3 de 5 del curso), tareas con verbo e ICE, salida JSON y Markdown (`--md`).
- El puntaje de Costo de Oportunidad **no es del diplomado**: el curso enseña el concepto (tráfico que pierdes frente a tu competidor, Semana 6 · lecciones 1 y 5), no una fórmula. Está dicho en el informe, en `SKILL.md` y en `metodo-diploma.md`. Lo mismo para el umbral del 60 % de "patrón común", los pesos por categoría y los valores iniciales de impacto, confianza y facilidad (supuestos editables). Las tareas dejan plazo, recurso y responsable como `pendiente de dato` (Semana 6 · lección 6: los define quien ejecuta).
- Caso de desajuste de tipo: si el tipo dominante de la SERP (60 %) difiere del tuyo, esa brecha pesa más, las demás se marcan `depende_del_tipo` y sus tareas llevan la condición "resolver antes el desajuste de tipo de página". Origen: Semana 4 · lección 8 (Diana: si Google solo muestra tiendas, no pongas un blog) y la idea de desajuste de `seo-sxo`.
- Integración: `--sitio` o `--competitors-json` fusionan con `.seo-audit/<sitio>/data/competitors.json` sin romper el esquema de `dashboard-seo` (`by_pillar[].results[]` con `position`, `domain`, `title`, `url`; `strategic[]` con `name`, `url`) y añaden `serp_analysis`. Contrato completo en `references/contrato-datos.md`, que dice qué lee `brief-de-contenido` (tipo dominante, temas frecuentes, formato) y `plan-seo` (tareas con ICE). No se editaron esas skills.
- `references/`: `practica-coaches.md` nuevo (Ari: #190, #222, #337, #200, #120, #157, #249; Vero: #132, #197, #295, #827, #821, #540, #256, #180, #588, #682, #597, #369, #612, #170, #600, #218, #125, #152, #788), `datos-opcionales.md` nuevo (Ahrefs MCP y SerpApi como enriquecimiento etiquetado, conversión a `brechas.py`, volúmenes reales), `contrato-datos.md` nuevo, `metodo-diploma.md` ampliado (Semana 4 · lección 8, Semana 8 · lección 3, Semana 6 · lección 6 y un bloque que separa método, ayuda del repo y práctica de coaches), `complementos-claude-seo.md` ampliado (secciones 5 a 7).
- `evals/evals.json`: casos 4 (SERP dominada por tiendas y página propia en formato blog), 5 (varias keywords con Repetición y tareas con ICE) y 6 (páginas con JavaScript y 403/WAF).
- `fixtures/`: `html/` con 5 competidores ficticios (guía, métodos, SPA que depende de JavaScript, categoría x2, ficha de producto; dominios `.test`) y una página propia floja, 3 SERP en formato `serp.py` y `ejecutar_ejemplo.sh` (corre todo sin red).

## `analisis-de-competidores` v1.2

- Solo se añadió el paso final "Siguiente paso: perfilar y comparar" que enlaza a `analisis-serp-y-competencia` y aclara que `perfil_competidor.py` acepta el JSON de `serp.py` o URLs sueltas. Sin cambios en scripts ni en el resto del texto.

## Verificación (ejecutada)

- `python3 -m py_compile` y `--help` de `perfil_competidor.py` y `comparar_serp.py`: correctos.
- Punta a punta con las fixtures (`bash fixtures/ejecutar_ejemplo.sh`): 5 HTML competidores + 1 propio perfilados sobre 3 SERPs (10 perfiles, 0 errores, 1 página marcada como dependiente de JavaScript). Tipos detectados: 2 blogs con confianza alta, 1 SPA sin clasificar (baja), 1 categoría y 1 ficha de producto. Comparación: "cómo preparar café" (domina blog, Costo de Oportunidad 74, 9 brechas), "comprar café de especialidad" (domina categoría 67 %, desajuste de tipo, 61, 6 brechas con 5 marcadas como dependientes del tipo), "café en grano" (58, 10 brechas). Repetición: cafeguia.test, tostadores.test y tazadiaria.test críticos (2 de 3). 12 tareas consolidadas con verbo e ICE (la primera, "Añadir una sección sobre «francesa»...", ICE 6,7). `competitors.json` escrito con `by_pillar`, `strategic` y `serp_analysis`.
- Rastreo en vivo contra un servidor local de prueba: una página real perfilada, 403 detectado como bloqueo probable con el mensaje de WAF, y una ruta prohibida por robots.txt saltada.
- `python3 scripts/validar_skills.py`: 30 skills, 4 agentes, 0 errores, 0 avisos. `python3 tests/test_estructura_skills.py`: OK (2 tests).
- Sin rayas largas ni medias fuera de las cajas estándar en los archivos de la skill.

## Campos nuevos que el dashboard podría mostrar (no se editó `build_dashboard.py`)

- Por resultado en `by_pillar[].results[]`: `page_type`, `word_count`, `schema_types`, `javascript_dependent` (columna de tipo de página y aviso de JavaScript).
- `serp_analysis.keywords[]`: `costo_oportunidad` y `nivel_costo` (barra por keyword), `patron.tipo_pagina` (chip "SERP de tiendas / de guías") y `desajuste_tipo` (alerta).
- `serp_analysis.tasks[]`: tabla de tareas con `ice`, `prioridad`, `skill_sugerida`, `condicion`.
- `strategic[].repeticion` y `de` (por ejemplo "2 de 3 keywords").

## Ideas descartadas

- Skill nueva para el perfil o la comparación: no hizo falta, `analisis-serp-y-competencia` es la dueña natural y la Semana 6 la respalda.
- Puntuación por persona, historias de usuario y wireframes de `seo-sxo`: ya quedaron como complemento de `intencion-de-busqueda`; aquí solo se toma la taxonomía de tipos de página.
- Generar páginas "X vs Y" (`seo-competitor-pages`): sigue siendo solo idea de contenido, no está en el diplomado.
- Flujo de competidores con DataForSEO (`seo-dataforseo`): de pago y duplica lo que ya hace Ahrefs MCP; se menciona en `datos-opcionales.md`, no se implementa.
- Estimar visitas o dinero perdido con un CTR fijo: exige un supuesto que el diplomado no define y rompe la regla de datos. El Costo de Oportunidad queda como puntaje relativo y el volumen real se pasa con `--volumenes`.
- Renderizar JavaScript dentro del script: exige dependencias fuera de stdlib. Se marca la página y se pide revisarla a ojo o con un navegador real.

## Para el agente principal

- README, ROADMAP y FUENTES: subir `analisis-serp-y-competencia` y `analisis-de-competidores` a 1.2; listar los scripts nuevos `perfil_competidor.py` y `comparar_serp.py`; citar claude-seo (MIT) en FUENTES con `skills/seo-sxo/references/page-type-taxonomy.md`, `skills/seo-sxo/SKILL.md`, `skills/seo-content` (señales E-E-A-T) y `skills/seo-dataforseo/SKILL.md` (solo mención).
- `install.sh` e `install.ps1`: no cambia la lista de carpetas; confirmar que copian `fixtures/` (incluido `ejecutar_ejemplo.sh`) y `references/`.
- `tests/`: se pueden añadir pruebas para `perfil_competidor.py` y `comparar_serp.py` con `fixtures/html` y las 3 SERP (por ejemplo, tipo dominante `categoria` en "comprar café de especialidad" y `desajuste_tipo` verdadero).
- `plan-seo` y `brief-de-contenido`: valorar una línea de enlace a `references/contrato-datos.md` (no se editaron). `agente-contenido` podría llamar a `comparar_serp.py` en su etapa de análisis de SERP.
- Las fechas de las fixtures de la guía ficticia son fijas, y `age_days` se calcula contra la fecha de hoy, así que esos números cambian con el tiempo.
