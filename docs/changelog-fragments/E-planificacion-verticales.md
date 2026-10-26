# Fragmento de changelog: Grupo E, planificación y verticales

Base: Semanas 2, 13, 14, 15 y 16 del diplomado; práctica de coaches (Ibra, Ari, perfil de Juan); claude-seo (MIT) solo como complemento.

## Skills nuevas (4) y un agente nuevo

### `plan-seo` (1.0)
- Pasos del plan: cuestionario, análisis web (observación, detalle, acción), objetivos SMART por modelo de negocio, plan por meses (Mes 1 a 4), revisión semanal y entrega del proyecto final. Fuente: Semana 2 · lecciones 4, 5 a 8, 9, 12, 14; Semana 13 · "Entrega de Proyecto SEO".
- Reparto de prioridades (técnica antes que contenido, realizable según el CMS, calendario realista): práctica de coaches (Ibra #620, #618; Ari #237, #302, #157; Juan).
- `scripts/generar_plan.py` (stdlib): valida que cada acción empiece con verbo, reparte por mes y prioridad, avisa de sobrecarga de horas y escribe `next-steps.json` (esquema de `dashboard-seo`), `plan-seo.json` y un Markdown para la Plantilla Master. Nada se inventa: lo que falta queda `pendiente de dato`.
- `references/plantillas.md`: cuestionario, objetivo SMART, tabla de análisis, plan por meses, esquema de slides.
- `references/complementos-claude-seo.md` (origen: `skills/seo-plan`): fases por semanas, tabla de KPI con horizontes, puerta de calidad de páginas de ubicación. Descartado: plantillas SaaS y editorial (el diplomado clasifica en E-commerce, Servicios y Contenido).
- Evals: `evals.json` (3 casos), `eval_queries.json`, fixture `evals/fixtures/hallazgos-ejemplo.json`.

### `seo-local` (1.0)
- Ficha de Google Business Profile, tres pilares (proximidad, relevancia, prominencia), NAP consistente, plan de reseñas, una página por servicio, keywords "[servicio] en [ciudad]", medición con "¿Cómo nos conociste?". Fuente: Semana 14 · "¿Qué es el SEO Local?" y "SEO para servicios, marcas personales y negocios pequeños".
- **Decisión sobre `seo-para-servicios-y-marca-personal`:** NO se creó skill aparte. La lección de la Semana 14 es corta (una página por servicio, atribución, keywords con ciudad) y se combina con SEO local, así que quedó integrada en `seo-local` y en su `references/metodo-diploma.md`.
- Criterio "toda la web debe apuntar a la keyword local, no solo la ficha", citaciones y barrios en keywords: práctica de coaches (Ari #284, #249, #172, #174; Ibra #274, #378).
- `scripts/verificar_nap.py` (stdlib): un solo fetch con User-Agent de navegador, respeta robots.txt, detecta 403/WAF, extrae teléfonos visibles, enlaces `tel:` y JSON-LD local, y compara con los datos de la ficha que pegue el usuario. Salida a `local-seo.json`.
- `references/complementos-claude-seo.md` (origen: `skills/seo-local`, `skills/seo/references/local-schema-types.md`, `skills/seo-maps`): rúbrica de puntaje por dimensiones, prueba del intercambio de ciudad, subtipos de schema, Bing Places. Lo de Maps con DataForSEO queda como opcional de pago, con permiso del usuario. Descartado: estadísticas de conversión de IA local y "Domain Authority" por no ser verificables.
- Evals: `evals.json` (3 casos), `eval_queries.json`, fixture `evals/fixtures/contacto.html`.

### `seo-ecommerce` (1.0)
- Keywords transaccionales, las tres páginas críticas (colecciones, productos, soporte), checklist de ficha (título, descripción persuasiva, FAQ, prueba social, alt). Fuente: Semana 14 · "¿Qué es el SEO de ecommerce?"; Semana 2 L9 (objetivo vender).
- Estructura de colecciones, canónicas en Shopify, variantes, paginación y filtros: práctica de coaches (perfil de Juan; Ibra #113, #194, #327; Ari #167, #237). `references/estructura-tienda.md` lo marca como NO cubierto por el diplomado.
- **Discrepancia anotada:** la práctica de Juan (paginación con canónica a la página principal más noindex) difiere de la recomendación de Google y de claude-seo (autocanónica por página). Quedó escrito para decidir con el cliente. Ibra también matiza "la colección no es una página SEO"; el curso manda (colecciones críticas).
- `scripts/auditar_producto.py` (stdlib): un fetch, revisa title y meta, H1, canónica, JSON-LD `Product` (obligatorios, recomendados, precio numérico, disponibilidad como URL, `aggregateRating`), migas, alt y FAQ. Salida a `ecommerce.json`.
- `references/complementos-claude-seo.md` (origen: `skills/seo-ecommerce`, `scripts/schema_ecommerce_validate.py`): puntaje de ficha, reglas de validación, brechas con Google Shopping (pago, opcional). Descartado: precios de Amazon/Shopping y verificador UCP por ser de pago o inmaduros.
- Evals: 3 casos, `eval_queries.json`, fixture `evals/fixtures/producto.html`.

### `propuesta-y-reporte-de-servicios-seo` (1.0)
- Propuesta con los 3 pilares (PV, confianza, beneficios mutuos), paquetes Bronce/Plata/Oro, cobro por hora y luego por paquete, ética, onboarding con cuestionario y accesos, cadencia de updates, manejo de expectativas, correo de crisis y encuesta de 3 preguntas. Fuente: Semana 2 L11 y L12; Semana 13 L3; Semana 16 L2, L3 y L4; Bonus L9.
- Explainer para el cliente (qué es, por qué importa, cómo se soluciona) y evidencia antes/después: perfil de Juan; criterios de presentación (capturas, cifras creíbles): Ari #219, #205, #322; Ibra #609, #618, #616.
- No duplica nada: el informe mensual lo hace `reporte-seo-gsc`, el entregable visual `dashboard-seo`, y la presentación en Slidev sigue en el ROADMAP (issue #1). Sin scripts a propósito.
- No se inventan tarifas ni cifras: quedan `pendiente de dato`.
- `references/complementos-claude-seo.md`: claude-seo casi no cubre el tema, y se dice así; solo se tomó la estructura de entregables con horizonte.

### Agente nuevo `agente-plan-y-entrega` (1.0)
Orquesta `plan-seo`, la capa vertical (`seo-ecommerce`/`seo-local`) y `propuesta-y-reporte-de-servicios-seo`, con dos checkpoints y cierre en dashboard.

## Agentes mejorados (1.0 a 1.1)
- `agente-auditoria-tecnica`: añade `sitemap-y-robots`, `schema-jsonld`, `analisis-rendimiento`, `inventario-de-urls`, `optimizacion-de-imagenes`, verticales (`seo-ecommerce`, `seo-local`) como bloque aparte y paso de entrega con `plan-seo` y `propuesta-y-reporte-de-servicios-seo`.
- `agente-contenido`: añade `intencion-de-busqueda`, `calidad-de-contenido-eeat`, `schema-jsonld`, `actualizacion-de-contenido`, `optimizacion-de-imagenes`, verticales y `plan-seo`; nuevo paso 5 de calidad y schema, con ruta de actualización para piezas existentes.
- `agente-investigacion-keywords`: añade `intencion-de-busqueda`, verticales y `plan-seo`.
- Verificado con `ls skills/` el 2026-10-26: existen todas las skills referenciadas. Aún NO existen `monitoreo-de-cambios` ni `seo-programatico`, así que no se referenciaron.

## Qué debe actualizar el agente principal
- **README:** listar `plan-seo`, `seo-local`, `seo-ecommerce`, `propuesta-y-reporte-de-servicios-seo` y `agente-plan-y-entrega`; subir el conteo de skills y agentes.
- **Agentes:** si llegan `monitoreo-de-cambios` (útil para el diff del agente de auditoría) y `seo-programatico` (útil junto a `seo-local` para páginas por zona, con la puerta de calidad), añadirlos a los agentes.
- **FUENTES.md:** añadir Semanas 2, 13, 14 y 16 y Bonus L9 como fuentes; claude-seo (MIT, agricidaniel): `skills/seo-plan`, `seo-local`, `seo-maps`, `seo-ecommerce`, `scripts/schema_ecommerce_validate.py`, `skills/seo/references/local-schema-types.md`.
- **ROADMAP:** nota de que la presentación de cliente (issue #1) se apoyará en `propuesta-y-reporte-de-servicios-seo`.
- **dashboard-seo:** `local-seo.json`, `ecommerce.json` y `plan-seo.json` no están en su esquema; solo `next-steps.json` lo está. Decidir si se añaden secciones.
- **install.sh / install.ps1 / tests:** incluir las 4 carpetas nuevas y `agente-plan-y-entrega.md`; los tres scripts nuevos pasan `py_compile` y `--help`.
- **Dependencia externa:** ninguna (todo stdlib). Nada de pago es obligatorio.

## Ideas descartadas
- Skill `seo-para-servicios-y-marca-personal` aparte (material insuficiente, integrada en `seo-local`).
- Lecciones de Semana 14 de redes sociales y de nichos (L5, L6): sin equivalente de skill pedida en este grupo; quedan como idea futura (`seo-redes-sociales`, `analisis-de-nichos`) con base real en el diplomado.
- Semana 15 (LinkedIn, portafolio, entrevistas): carrera profesional, no skill de SEO operativo.
- Maps, Shopping, UCP y precios de marketplace de claude-seo: de pago o sin base en el diplomado.
- Matriz ICE: no aparece en el diplomado ni en el repo, no se usó.

---

# Ampliación de `plan-seo` (pedido directo de Juan): contenidos, Master, briefs y proyección

`plan-seo` sube a **1.1** y se crea una skill hermana **`proyeccion-seo-gsc` 1.0** (el alcance de proyección es distinto y tiene su propio script).

## De dónde sale cada cosa
- **Comunidad (solo estructura, anonimizada):** nombres de pestañas, encabezados y orden de la Plantilla Master (13 pestañas leídas de un Google Sheet público compartido en los canales; se extrajeron únicamente encabezados), y secciones de los briefs de blog, landing y contenido existente (Docs públicos del canal de contenido). Queda en `plan-seo/references/plantillas-comunidad.md`. No se copió ningún dato, dominio, nombre ni correo de proyectos. Los ejemplos y fixtures son inventados (clínica ficticia, `ejemplo-clinica.test`).
- **Diplomado:** Semana 4 (Tutorial de la plantilla Master), Semana 5 (mapa 1 keyword por URL, posición de partida), Semana 7 (clusters y orden de contenido), Semana 8 (elementos y tipos de brief, blog, landing, e-commerce), Semana 10 (briefs de contenido existente, URL actual vs sugerida, matriz impacto vs esfuerzo), Semanas 3 y 12 (4 métricas de GSC y reporte), Semana 2 (objetivos, plan), Semana 16 (expectativas). **ICE** (promedio de Impacto, Confianza y Facilidad) sale de la pestaña de auditoría de la Master; corrijo mi nota anterior: sí aparece en la comunidad, no en los resúmenes del diplomado.
- **Mecánicas del repositorio (no del diplomado ni de la comunidad):** validación automática 1 keyword = 1 URL, calendario por cadencia, derivación de un borrador de mapa desde keywords y clusters, umbrales de prioridad por ICE (Alta 8 o más, Media 6 o más), y toda la proyección.
- **claude-seo (complemento):** nada nuevo se importó. Se anotó en `complementos-claude-seo.md` que sus entregables en `.md` se reemplazan por la Master y los briefs.

## `plan-seo` 1.1
- `scripts/generar_master.py`: lee `.seo-audit/<sitio>/data/*.json` y escribe la Master con 13 pestañas (xlsx con openpyxl y listas desplegables; CSV por pestaña más `LEEME.md` si no hay openpyxl o con `--csv`). Valida el mapa y reutiliza `mapa-de-palabras-clave/scripts/canibalizacion.py` si está. Escribe `content-map.json` (con mes y fecha) y `validacion-mapa.json`.
- `scripts/generar_briefs.py`: un Markdown por página en `entregables/briefs/{blog,landings,ecommerce,actualizacion}` más `00-indice.md`; `.docx` opcional con python-docx. No redacta contenido creativo ni inventa cifras; cuenta caracteres de metas.
- `scripts/_plan_comun.py`: funciones compartidas (ICE, slug, calendario, validación).
- `references/plantillas-comunidad.md` (especificación de los generadores) y `references/publicar-en-google-drive.md` (tres vías opcionales; regla de mostrar y pedir confirmación; nunca público por defecto; el repo no guarda credenciales).
- Estructura de entrega: `.seo-audit/<sitio>/entregables/{00-master, briefs/..., reportes}`.
- Evals: casos 4 a 6 y fixtures en `evals/fixtures/proyecto-ejemplo/data/` (incluye una canibalización a propósito).

## `proyeccion-seo-gsc` 1.0
- `scripts/proyeccion_gsc.py` con `proyectar` y `seguimiento`. Línea base y CTR de la propia web a partir de GSC; curva de CTR por posición calculada de las consultas (muestra mínima); tres escenarios con supuestos editables (`--supuestos`); rangos con fórmulas visibles; estacionalidad solo con 12 meses o más (tendencia lineal restada). **Se niega a proyectar** con menos de 3 meses, sin muestra para la curva (salvo `--curva-generica` rotulada como supuesto del usuario) y no suma páginas nuevas sin volumen aportado (`pendiente de dato`).
- Salida a `proyeccion-gsc.json` y `seguimiento-proyeccion.json` (formato plan vs real para `reporte-seo-gsc`; no edité archivos del grupo D).
- **Aviso honesto:** la proyección no es un método del diplomado, es una extensión pedida por Juan; está rotulada así en la skill. Sin garantía.
- Fixtures sintéticos en `evals/fixtures/` (claramente falsos), 4 evals y `eval_queries.json`.

## Verificado
`py_compile` y `--help` de todos los scripts; corrida de punta a punta con fixtures (Master xlsx de 13 pestañas, CSV de respaldo, 5 briefs de los 4 tipos más 3 `.docx`, avisos de canibalización, proyección en rangos, rechazo con 2 meses y sin consultas, seguimiento). No verificado: carga del `.xlsx` en Google Sheets, ni el formato exacto de la plantilla de brief de e-commerce de la comunidad (no se encontró un ejemplo público).

## Qué debe actualizar el agente principal (adicional)
- README/ROADMAP/FUENTES/install: añadir `proyeccion-seo-gsc` (skill 1.0) y los nuevos scripts de `plan-seo`; `openpyxl` y `python-docx` como dependencias opcionales en `requirements.txt` (nada obligatorio).
- `dashboard-seo`: considerar secciones para `proyeccion-gsc.json`, `seguimiento-proyeccion.json`, `content-map.json` y `validacion-mapa.json` (hoy no las lee).
- `reporte-seo-gsc` (grupo D): puede leer `seguimiento-proyeccion.json` para un bloque "plan vs real".
- `.gitignore`: los entregables viven en `.seo-audit/`, ya ignorado.
- Privacidad: los Sheets y Docs de la comunidad que se leyeron son de alumnos; aquí solo quedaron encabezados.
