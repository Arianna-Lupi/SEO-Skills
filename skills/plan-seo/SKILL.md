---
name: plan-seo
description: "Usa esta skill cuando el usuario necesite convertir un diagnóstico en un plan de trabajo SEO por meses, o definir objetivos y tareas antes de ejecutar, aunque no diga \"plan SEO\", p.ej. \"por dónde empiezo con mi web\", \"qué hago primero y qué después\", \"arma el cronograma para este cliente\", \"tengo el análisis pero no sé cómo ordenarlo\", \"ayúdame a definir objetivos y KPIs\", \"prepara el proyecto final\", \"qué contenido hago y en qué orden\", \"una keyword por página\", \"arma la Plantilla Master\", \"genera los briefs de todas las páginas\". Sigue el método de \"De Cero a SEO\" (aprendoseo, Semanas 2, 4, 5, 7, 8, 10, 12 y 13): análisis web (observación, detalle, acción), objetivos SMART, cuestionario, plan por meses, mapa de contenidos con una keyword por URL, plan de contenidos con calendario y los ARCHIVOS: la Plantilla Master completa y un brief por página. Cada observación termina en una tarea con verbo, responsable, fecha y entregable."
compatibility: Scripts en Python 3 solo con stdlib (generar_plan.py, generar_master.py, generar_briefs.py). openpyxl es opcional para el .xlsx (si falta, genera un CSV por pestaña) y python-docx es opcional para .docx. Funciona 100% manual sin ellos. Subir a Google Drive es opcional y siempre con confirmación.
metadata:
  author: aprendoseo
  milestone: SEO skills (De Cero a SEO)
  version: "1.1"
---

> **🚫 Regla de datos (obligatoria): NUNCA inventes números.**
> No estimes, supongas ni inventes métricas o datos que no tengas: volumen de búsqueda, dificultad/KD, clics, impresiones, CTR, posición, tráfico, Core Web Vitals, backlinks, fechas, precios, etc. Si te falta un dato, **pídeselo al usuario y espera su respuesta** — que lo pegue a mano, lo exporte (Google Search Console, Ahrefs, DinoRank, Screaming Frog…) o lo conecte por MCP. Da igual de dónde venga, pero tiene que venir de una fuente real. Si aun así no hay dato, márcalo explícitamente como `pendiente de dato` y NO continúes como si lo tuvieras. Un entregable con huecos honestos vale más que uno con cifras inventadas.


> **📊 Cierre en dashboard.** Cuando trabajes sobre un sitio, además de tu entrega persiste tu salida estructurada en `.seo-audit/<sitio>/data/next-steps.json` (esquema en la skill `dashboard-seo`). Al cerrar el flujo SEO, genera/actualiza el dashboard con `dashboard-seo` y entrega el URL local. Tu archivo: `next-steps.json` y `plan-seo.json`.

# Plan SEO: del diagnóstico al cronograma (S2 + S13)

Actúa como **Director de proyectos SEO en aprendoseo**. Un Plan SEO no es una lista de deseos: es el documento vivo que aterriza el análisis en tareas con fechas. Frase del curso: *"un plan sin acción es solo una ilusión"*. La prioridad manda: primero los errores técnicos que bloquean a Google, después el contenido que atrae usuarios.

> **Método completo del diploma:** [`references/metodo-diploma.md`](references/metodo-diploma.md) (lecciones citadas por semana). Plantillas de objetivos, cuestionario y entrega en [`references/plantillas.md`](references/plantillas.md).

## Cuándo usar

- Hay un análisis web o una auditoría hecha y falta ordenarlo en un cronograma.
- Arranca un proyecto nuevo (propio, ficticio, desde cero o de cliente) y hay que definir objetivos, cuestionario y plan.
- Toca preparar el **proyecto final** (Plantilla Master 100% llena + presentación de slides).
- El usuario pregunta qué hacer primero, o cuánto tardará cada fase.

Antes: `auditoria-tecnica`, `inventario-de-urls`, `analisis-serp-y-competencia` aportan las observaciones. Después: `brief-de-contenido`, `schema-jsonld`, `reporte-seo-gsc` ejecutan las tareas.

## Entradas

- URL del sitio (o descripción si es proyecto desde cero) y tipo de proyecto: **E-commerce, Servicios o Contenido**.
- Observaciones del análisis (tabla observación, detalle, acción) o los `.seo-audit/<sitio>/data/*.json` existentes (`issues.json`, `keywords.json`, `clusters.json`).
- Respuestas del cuestionario del cliente (negocio, objetivos, competencia, historial SEO, accesos).
- Horas disponibles por semana y quién ejecuta cada tarea.

## Pasos

1. **Elegir el sujeto de estudio y copiar la Plantilla Master.** Sitio existente, ficticio o desde cero (los tres valen, S2 L5 a L8). Sin acceso al sitio también se puede analizar lo visible.
2. **Cuestionario SEO.** Si hay cliente, no empieces a ciegas: negocio, objetivos, competencia, historial SEO (penalizaciones) y accesos (Search Console, Analytics, CMS). Plantilla en `references/plantillas.md`. Detecta objetivos incoherentes ("quiero tráfico" cuando necesita ventas de un producto concreto).
3. **Análisis web con formato observación, detalle, acción.** Cada hallazgo registra qué se vio, por qué afecta y qué tarea lo corrige. Revisa contenido y uso de keywords, arquitectura a **menos de 3 clics**, UX y conversión. No es un checklist: sin acción no hay hallazgo (práctica de coaches).
4. **Definir objetivos y métricas.** Un objetivo principal alineado al modelo: **E-commerce vende, Servicios genera leads, Contenido suma lectores o suscriptores**. Redáctalo SMART y anota las métricas base reales (clics, impresiones, posiciones, conversiones). Si no existen, márcalas `pendiente de dato`: nunca inventes la línea base.
5. **Pasar cada acción al plan.** Cada tarea: empieza con verbo, responde a un objetivo, tiene responsable, fecha, horas estimadas y enlace a su entregable. Una tarea que no responde a ningún objetivo se descarta.
6. **Ordenar por meses con la lógica del diplomado** (adapta, es 100% flexible):
   - **Mes 1, bases y estrategia:** base técnica, estrategia, herramientas, keywords y clusters.
   - **Mes 2, producción:** briefs de contenido nuevo y de optimización, redacción SEO.
   - **Mes 3, autoridad y publicación:** E-E-A-T, subida al CMS.
   - **Mes 4, análisis:** reporte final de resultados.
   Añade pasos propios si hacen falta (por ejemplo diseño web o ficha local). Si el sitio es local o ecommerce, inserta las tareas de `seo-local` o `seo-ecommerce`.
7. **Priorizar.** Alta: lo que impide rastrear, indexar o convertir (botones rotos, noindex por error, H1 ausente). Media: contenido y enlazado. Baja: detalles cosméticos (alt faltante en imágenes decorativas). La prioridad se afina con la práctica; justifica cada una en una línea.
8. **Revisión semanal.** Marca avances en Trello/tablero y ajusta. Un plan sin revisión se muere.
9. **Entrega (proyecto final, S13 L2).** Plantilla Master completa (investigación, auditoría, plan de contenidos, briefs, reportes) y slides: Portada, Objetivos, Auditoría técnica, Estrategia de contenidos, Conclusión. Para el discurso a cliente usa `propuesta-y-reporte-de-servicios-seo`.

## Del plan a los archivos (contenidos, Master y briefs)

Esta parte convierte el plan en entregables que el cliente o el alumno puede abrir. Estructura de las pestañas y de los briefs: [`references/plantillas-comunidad.md`](references/plantillas-comunidad.md) (esquemas anonimizados de lo que comparte la comunidad, contrastados con el diplomado).

**Carpeta de salida:** `.seo-audit/<sitio>/entregables/{00-master, briefs/blog, briefs/landings, briefs/ecommerce, briefs/actualizacion, reportes}`.

1. **Plan de contenidos y mapa (S4, S5, S7).** Parte de `keywords.json`, `clusters.json` y `issues.json`. Construye `content-map.json` (una fila por URL): URL actual o propuesta, keyword principal y secundarias, intención, tipo (Home, Categoría, Blog, Landing, Ecommerce), cluster y rol (Pilar o Spoke), acción (Crear, Actualizar, Dejar, Eliminar), Impacto, Confianza y Facilidad. **Puntuación ICE = promedio de los tres** (como en la pestaña 15 de la Master). Para asignar keywords usa `mapa-de-palabras-clave` y `deteccion-de-canibalizacion`; no los dupliques aquí.
2. **Una keyword = una URL.** `generar_master.py` valida el mapa y avisa de: keyword repetida en varias URLs (canibalización), URL con varias keywords principales, páginas sin keyword y mezcla de intención y tipo (por ejemplo keyword transaccional en un blog). Si `mapa-de-palabras-clave/scripts/canibalizacion.py` está instalado, lo ejecuta y adjunta su resultado en `validacion-mapa.json`.
3. **Calendario.** Orden: primero pilares y páginas que venden (Home, Categoría, Landing, Ecommerce), luego por ICE; los spokes nunca van antes del pilar de su cluster. La cadencia es un **supuesto editable** (`--por-mes`, por defecto 4) y las fechas solo salen si das `--inicio`. Práctica de coaches: un cluster por mes, páginas de servicio al inicio.
4. **Plantilla Master completa.**

```bash
python3 scripts/generar_master.py --sitio ejemplo.com --por-mes 4 --inicio 2026-11-02
```

   Rellena las 13 pestañas con los encabezados reales (Plan de SEO, Investigación, Mapa, Competidores, Estrategia, Producción, Actualización, Tareas de revisión técnica, Auditoría técnica con ICE, Plan Especialista, Servicios, Herramientas). Escribe `Master-<sitio>.xlsx` con listas desplegables, o un CSV por pestaña más `LEEME.md` si no hay openpyxl (`--csv` lo fuerza). Lo que falta dice `pendiente de dato`: **nunca** inventa volumen, KD, clics, tráfico ni precios. Si no existe `content-map.json`, deriva un **borrador** de keywords y clusters y lo marca como tal: revísalo con el usuario antes de entregar.
5. **Briefs, uno por página.**

```bash
python3 scripts/generar_briefs.py --sitio ejemplo.com [--docx]
```

   Crea un Markdown por fila del mapa en `briefs/blog`, `landings`, `ecommerce` y `actualizacion` (acción Actualizar, Semana 10) más `briefs/00-indice.md`, con las secciones exactas de la plantilla (Elemento de la página, Sugerencias, links internos, estructura H1 a H3). No redacta el contenido creativo: rellena lo que el mapa trae, cuenta caracteres de metas (50-60 y 120-155) y deja guías con el criterio del diplomado donde falta. Después vuelve a correr `generar_master.py` para que la columna Gdoc apunte a cada brief.
6. **Verifica antes de entregar.** Revisa `validacion-mapa.json` (cero avisos Críticos), que cada brief tenga keyword y URL, y que ninguna cifra haya salido de la imaginación.
7. **Proyección con Search Console (opcional).** Si hay acceso a GSC, usa la skill hermana [`proyeccion-seo-gsc`](../proyeccion-seo-gsc/SKILL.md): rangos "si se cumple el plan" con supuestos explícitos y seguimiento plan vs real. Proyección no es garantía.
8. **Google Drive (opcional).** Todo lo anterior es local. Para subirlo a Drive, ver [`references/publicar-en-google-drive.md`](references/publicar-en-google-drive.md): tres vías (archivos locales, conectores de Drive y Sheets, API propia) y regla obligatoria de mostrar y confirmar antes de crear o compartir nada; nunca público por defecto.

## Script del plan por meses

`scripts/generar_plan.py` convierte una lista de hallazgos (JSON) en el plan por meses: valida que cada acción empiece con verbo, ordena por prioridad y área, reparte en meses y escribe `.seo-audit/<sitio>/data/next-steps.json` (esquema de `dashboard-seo`) y `plan-seo.json`, más un Markdown pegable en la Plantilla Master.

```bash
python3 scripts/generar_plan.py --help
python3 scripts/generar_plan.py hallazgos.json --sitio ejemplo.com --horas-semana 6 --md plan.md
```

Entrada: `{"objetivo": "...", "hallazgos": [{"observacion","detalle","accion","area","prioridad","horas"}]}`. Áreas: `tecnica`, `estrategia`, `contenido`, `autoridad`, `conversion`. Si falta `horas`, queda `pendiente de dato`.

## Salida

```
PLAN SEO: [sitio] · Tipo: [E-commerce | Servicios | Contenido]
Objetivo principal (SMART): ...
Métricas base: [real o `pendiente de dato`]
| Mes | Área | Tarea (verbo) | Prioridad | Responsable | Fecha | Horas | Entregable (enlace) |
Riesgos y dependencias: ...
Próxima revisión: ...
```

## Reglas

- Una keyword principal por URL; el mapa se valida antes de generar archivos.
- Cada tarea nace de una observación y responde a un objetivo. Sin trazabilidad no entra.
- Tareas con verbo, accionables y separadas (no "mejorar el SEO").
- Técnica primero, contenido después, salvo que el sitio no tenga nada que indexar.
- Nada de metas numéricas de tráfico sin línea base real.
- Realizable según el CMS: lo que no se pueda hacer en Wix o Shopify se difiere al developer (práctica de coaches).

## Complementos opcionales (claude-seo)

Después del método del diploma, puedes tomar de [`references/complementos-claude-seo.md`](references/complementos-claude-seo.md) la rúbrica de puntaje de salud, las fases por semanas y las plantillas por tipo de negocio. No sustituyen el plan por meses.

## Gotchas

- Un plan que intenta abarcar todo a la vez no se ejecuta: prioriza.
- Objetivos sin métricas base son deseos; objetivos con cifras inventadas son peores.
- Si el cliente dice "quiero tráfico", pregunta qué venta o contacto necesita.
- La línea de tiempo es una guía de aprendizaje, no una promesa de resultados: educa al cliente en plazos reales.
