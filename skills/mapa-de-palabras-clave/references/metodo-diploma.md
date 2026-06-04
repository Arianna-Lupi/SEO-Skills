# Método del diploma — Mapa de Palabras Clave (Semana 5, Verónica Romero)

> Fuente: corpus interno "De Cero a SEO" (colección chunks, doc_type resumenes-prompts/transcripciones), Semana 5. Material de aprendoseo.

Verónica Romero dicta el cuerpo de la Semana 5; Arianna Lupi abre (video 1) y cierra (video 10, Resumen Semanal). El Mapa de Palabras Clave es el puente entre la investigación de la Semana 4 y la estructura real del sitio: asigna la keyword correcta a **cada URL que ya existe**.

## El método paso a paso (como lo enseña el curso)

La "hoja de ruta de la semana" (Arianna, video 1), ejecutada sobre la pestaña **"Mapa de Palabras Clave"** de la Plantilla Master:

1. **Inventario de URLs (video 3).** Descargar **todas** las páginas del sitio. "No podemos optimizar lo que no sabemos que existe." Herramienta recomendada: **Screaming Frog** (estándar profesional; rastrea como Google y exporta una lista limpia; versión gratis hasta 500 URLs). Alternativas: el **sitemap XML** o extensiones como **Link Klipper** (más desordenadas). Proceso: meter el dominio → dejar que el robot rastree → exportar la columna Address/URL → pegarla en la primera columna del mapa.

2. **Evaluación de Valor SEO (video 4).** Clasificar cada URL con "Sí/No" en la columna de checklist. Pregunta clave: **"¿Un usuario buscaría esto en Google?"** Si nadie busca lo que hay en la página, no tiene valor SEO. (Definiciones de qué sí y qué no, abajo.)

3. **Asignar la keyword principal a cada URL con valor (video 5).** Relación **1:1** (una keyword por URL) para evitar canibalización y darle pistas claras a Google. Proceso: analizar el contenido actual de la página → validar buscando esa idea en Google → si lo que rankea coincide con lo que ofreces, esa es la keyword principal. Filosofía: "aprovechar lo que ya tienes; a veces la keyword perfecta ya está en el texto, solo falta declararla oficialmente en el mapa".

4. **Evaluar la intención por temperatura (video 6).** Clasificar cada keyword en 3 niveles (Baja/Media/Alta — ver definiciones). Preguntarse: "¿Qué tan listo está este usuario para comprar/convertir cuando busca esto?"

5. **Analizar los datos por keyword (video 7).** Para cada keyword principal obtener **3 datos**: Volumen de búsqueda, Dificultad (KD) y **Posición Actual** de tu URL hoy. Es "refrescar" lo de la Semana 4 (Diana) pero aplicado a páginas existentes. Hallazgo común: si la herramienta dice que "ninguna página entra en las primeras 100", nada está optimizado — es el punto de partida normal, no algo malo.

6. **Definir el Plan de Acción (video 8).** Asignar a cada URL una de 3 acciones en la columna "Acción": **Actualizar/Optimizar**, **Eliminar/Redireccionar** o **Mantener** (criterios abajo). Esto cierra el ciclo y genera la lista de tareas.

7. **Elegir las mejores páginas — Top 5 (video 9).** Seleccionar las **5 URLs prioritarias** bajo 3 lentes (volumen×dificultad, intención alta, cerca del top 10) y darles un orden lógico de trabajo.

8. **Consolidar (Arianna, video 10).** Validar el mapa: inventario limpio (sin duplicados ni basura técnica), una keyword única por página, intención clara y Top 5 definido.

## Plantillas, criterios y umbrales exactos

**Columnas de la pestaña "Mapa de Palabras Clave":**

| Columna | Qué contiene |
|---|---|
| URL | Dirección de la página (del inventario de Screaming Frog) |
| Valor SEO | Sí / No (checklist) |
| Palabra Clave Principal | UNA keyword por URL (1:1) |
| Intención | Baja / Media / Alta (temperatura) |
| Volumen | Búsquedas mensuales |
| Dificultad (KD) | Competitividad de la keyword |
| Posición Actual | Lugar de la URL hoy en Google (0 / >100 = no posicionada) |
| Acción | Actualizar/Optimizar · Eliminar/Redireccionar · Mantener |

**Criterios de Valor SEO (video 4):**
- **CON valor SEO:** páginas de Servicios/Productos, Artículos de Blog (resuelven dudas/educan), Categorías de E-commerce.
- **SIN valor SEO (no optimizar):** páginas Legales (términos, privacidad), páginas de Autor (sirven a la autoridad interna pero rara vez se buscan), Carpetas de organización interna sin contenido real.

**Criterios del Plan de Acción (video 8) — combinado con el prompt del video 8:**
- **Actualizar / Optimizar:** la página tiene valor SEO pero su posición es baja o inexistente (>100), o el contenido está desactualizado. Objetivo: mejorar texto, encabezados y relevancia para subir. (El prompt sugiere el rango orientativo **posición 4-20**.)
- **Eliminar / Redireccionar:** la página no tiene valor SEO, tiene contenido duplicado, hay canibalización, o "ensucia" el rastreo. Objetivo: limpiar para que Google se concentre en lo importante.
- **Mantener (dejar como está):** la página ya está posicionada en los primeros lugares (el prompt orienta **top 3**) y cumple su función.

**Criterios para el Top 5 (video 9):**
1. **Alto Volumen + Baja Dificultad** — las "frutas bajas" (low-hanging fruit), tráfico rápido.
2. **Intención Alta (conversión)** — aunque tengan menos tráfico, son las que venden; impactan el negocio.
3. **Cerca del Top 10** — una URL en posición 12-15 con un ajuste pequeño salta a la página 1.

**Orden lógico de trabajo (video 9):** 1) arreglar bases / pilares con errores graves; 2) oportunidades de tráfico rápido (alto volumen / baja dificultad); 3) bajo potencial o largo plazo.

## Prompts originales que da el curso (verbatim)

**Inicio del mapa (Arianna, video 1):**
> 🎯 Prompt: Arquitecto de Mapas de Palabras Clave "Actúa como un Consultor SEO Senior en aprendoseo. Ayúdame a iniciar la creación de mi Mapa de Palabras Clave para aprendoseo. Explícame cómo descargar todas las URLs de mi sitio y cómo evaluarlas usando el checklist de valor SEO. Guíame para asignar una palabra clave principal y una intención de búsqueda a cada página existente, de modo que pueda definir un plan de acción claro: ¿debo optimizar, redireccionar o borrar cada URL para maximizar el tráfico orgánico?"

**Mapeo y auditoría (Verónica, video 2):**
> 🎯 Prompt: Estratega de Mapeo y Auditoría de Contenidos "Actúa como un Consultor SEO Senior en aprendoseo. Ayúdame a transformar mi lista de URLs de aprendoseo en un Mapa de Palabras Clave estratégico. Sigue este proceso: Auditoría de Valor: Clasifica mis páginas actuales para identificar cuáles tienen 'Valor SEO' y cuáles no. Mapeo 1:1: Asigna una palabra clave principal y una intención de búsqueda específica a cada URL para evitar la canibalización. Análisis de Brechas: Compara mi estructura con la competencia para ver qué contenidos me faltan. Plan de Acción: Define para cada URL si debemos Optimizar, Redireccionar o Eliminar, basándote en su potencial de posicionamiento."

**Extracción de URLs (video 3):**
> 🎯 Prompt: Especialista en Extracción de Datos y URLs "Actúa como un Estratega SEO Técnico en aprendoseo. Ayúdame a realizar la extracción completa de las URLs de mi proyecto en aprendoseo. Guíame paso a paso para utilizar Screaming Frog (u otras alternativas como el sitemap XML) para obtener el listado de todas las direcciones de mi sitio. Enséñame a limpiar y organizar esta lista en mi Plantilla Master para que cada URL sea la base de mi futuro Mapa de Palabras Clave."

**Evaluar valor SEO (video 4):**
> 🎯 Prompt: Especialista en Evaluación de Valor SEO "Actúa como un Auditor SEO en aprendoseo. Analiza mi lista de URLs de aprendoseo y clasifica cuáles tienen Valor SEO basándote en si responden a una intención de búsqueda clara, tienen potencial de tráfico o ayudan a la conversión. Identifica las páginas administrativas o internas que debemos ignorar para centrar nuestra estrategia solo en el contenido que posiciona."

**Asignar keyword (video 5):**
> 🎯 Prompt: Estratega de Asignación de Keywords "Actúa como un Estratega SEO en aprendoseo. Ayúdame a asignar la Palabra Clave Principal a cada URL con valor SEO de mi proyecto aprendoseo. Analiza el contenido actual de cada página y selecciona el término que mejor represente su temática, asegurándote de que sea una palabra que los usuarios realmente busquen y que no se repita en otras URLs para evitar la canibalización."

**Intención por niveles (video 6):**
> 🎯 Prompt: Analista de Intención y Niveles de Conversión "Actúa como un Estratega SEO en aprendoseo. Ayúdame a clasificar las palabras clave de mi mapa de aprendoseo según su nivel de intención: Baja (informativa), Media (investigación) o Alta (transaccional/decisión). Analiza qué espera encontrar el usuario con cada término y asegúrate de que el contenido de la URL asignada responda exactamente a esa expectativa para garantizar que Google nos posicione en los primeros lugares."

**Analizar datos (video 7):**
> 🎯 Prompt: Analista de Métricas y Posicionamiento "Actúa como un Estratega SEO en aprendoseo. Ayúdame a investigar el Volumen de búsqueda, la Dificultad (KD) y la Posición actual de las palabras clave de mi mapa para aprendoseo. Identifica qué páginas no están posicionando (fuera del top 100) para detectar oportunidades críticas de optimización y vuelca estos datos en mi Plantilla Master para priorizar mis esfuerzos."

**Plan de acción (video 8):**
> 🎯 Prompt: Estratega de Decisiones y Plan de Acción SEO "Actúa como un Director SEO en aprendoseo. Ayúdame a definir el Plan de Acción para cada URL de mi mapa en aprendoseo. Analiza los datos de posición y relevancia para decidir si debemos Mantener (si está en top 3), Optimizar (si está entre 4 y 20), Eliminar (si no tiene valor) o Redireccionar (si hay canibalización), asegurando que cada movimiento mejore el rendimiento global del sitio."

**Priorización / quick wins (video 9):**
> 🎯 Prompt: Estratega de Priorización y Quick Wins "Actúa como un SEO Lead en aprendoseo. Ayúdame a seleccionar las 5 URLs prioritarias de mi mapa de aprendoseo para empezar la ejecución. Filtra las páginas que tengan el mejor equilibrio entre Volumen de búsqueda, Baja dificultad y Relevancia de negocio. Define un orden lógico de trabajo (Quick Wins primero) para que mi estrategia de contenido genere tráfico en el menor tiempo posible."

**Validación final (Arianna, video 10):**
> 🎯 Prompt: Estratega de Consolidación y Mapa Maestro "Actúa como un Líder SEO en aprendoseo. Ayúdame a validar mi Mapa de Palabras Clave final para aprendoseo. Revisa que haya limpiado correctamente las URLs (sin duplicados ni basura técnica), asignado una keyword única por página para evitar canibalización y definido acciones claras (Optimizar, Redireccionar o Eliminar). Asegúrate de que mis 5 prioridades estén alineadas con la intención de búsqueda para maximizar el impacto de mi estrategia."

## Términos del diploma (definiciones)

- **Mapa de Palabras Clave** (también "modelo de contenido" o "auditoría de contenido"): proceso de extraer todas las URLs de un sitio para identificar cuáles tienen oportunidad de SEO y cuáles no, asignando keyword + intención + acción a cada una.
- **Valor SEO:** propiedad de una página capaz de atraer tráfico orgánico porque responde a una intención de búsqueda clara. "Si nadie busca lo que hay en esa página, esa página no tiene valor SEO."
- **Canibalización:** dos o más páginas tuyas intentando posicionar por la misma palabra, robándose tráfico entre sí. El mapeo 1:1 (una keyword por URL) la previene.
- **Temperatura / niveles de intención (video 6):**
  - **Baja (Informativa):** el usuario busca aprender; está lejos de comprar (ej: "¿qué es el marketing digital?"). No despreciarlas: traen el mayor volumen al ecosistema.
  - **Media (Investigación Comercial):** ya sabe qué necesita y compara opciones/lugares (ej: "cursos de marketing digital en Barcelona").
  - **Alta (Transaccional):** necesidad urgente/específica, listo para actuar (ej: "contratar asesoría de marketing", página de curso con precio y botón). Son "el dinero".
- **URL:** dirección física de una página en el mundo digital; se compone de protocolo (https), subdominio (www), dominio y extensión (.com/.es).
- **"Frutas bajas" (low-hanging fruit):** páginas con alto volumen y baja dificultad — tráfico rápido si se optimizan bien.
- **Plan de Acción:** las 3 decisiones por URL (Actualizar/Optimizar, Eliminar/Redireccionar, Mantener) que transforman los datos en tareas.

## Ejemplos del curso

- **Página de servicios de consultoría (video 5):** la página habla de consultorías → se busca "Asesorías de marketing digital" / "Asesoramiento en marketing digital" → como la búsqueda refleja exactamente el servicio, esa se vuelve la Keyword Principal en la plantilla.
- **Diagnóstico "posición >100" (video 7):** al meter las keywords en la herramienta, "ninguna página entra en las primeras 100" → no es malo, es el punto de partida; permite medir el éxito real de futuras optimizaciones ("pasar de no existir a estar en la página 1").
- **Reporte para clientes (video 8):** el mapa es una herramienta de venta y autoridad: "Analizamos página por página y detectamos qué actualizar, qué eliminar y qué está funcionando bien".
- **"Eliminar" da miedo pero es necesario (tip video 8):** si una página no ayuda al usuario ni al SEO, solo consume recursos; al quitarla, das más fuerza a tus páginas de Intención Alta.
- **Si no tienes web aún (video 2):** practica el mapeo con cualquier sitio con muchas URLs de tu nicho; lo importante es dominar la metodología.
