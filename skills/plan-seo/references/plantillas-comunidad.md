# Plantillas de la comunidad: esquemas de la Master y de los briefs

> Fuente: enlaces públicos de Google Sheets y Docs que los alumnos comparten en los canales de la comunidad (exportación `data/channels/*.json`), leídos para extraer **solo la estructura**: nombres de pestañas, encabezados y su orden, secciones de los briefs. **No se copió ningún dato de proyecto, cliente, dominio ni persona**; los ejemplos de abajo son genéricos. Se contrastó con el diplomado: Semana 4 · "Tutorial de la plantilla Master"; Semana 5 (mapa); Semana 7 (estrategia); Semana 8 · "Elementos de un brief", "Tipos de brief", briefs de blog, landing y e-commerce; Semana 10 · briefs de contenido existente; Semana 12 · informe SEO. Esta es la especificación de `generar_master.py` y `generar_briefs.py`.

## Plantilla Master: pestañas y encabezados (en orden)

La Master que circula en la comunidad tiene estas pestañas (la numeración salta a propósito: las pares son documentos auxiliares):

| Pestaña | Fila de título | Encabezados (orden real) |
|---|---|---|
| Indice | Índice | Documento · Detalle · (columna lateral: Semana · Recurso con enlace "Aquí") |
| Herramientas SEO | Herramientas Gratuitas y Pagas SEO | Area · Herramienta · Link · Uso · Area |
| 1. Plan de SEO | Plan de SEO | Mes · Tarea · Objetivo · Dueño · Horas · fecha de Entrega · Estatus · Links |
| 2. Ejemplo de plan de SEO | Plan de SEO | (igual que la 1, con un ejemplo resuelto) |
| 3. Investigación de Palabras Clave | Investigación de palabras claves | Palabra Clave · Intención de Busqueda · Cluster · URL sugerido · Volúmen de búsqueda · Dificultad (Keyword Difficulty) · Tasa de Conversion · Idea de contenido · H1 sugerido · Primer Lugar (ejemplo) · Aprobación del cliente |
| 5. Mapa de palabras clave | Modelo de contenido | url sugerido · ¿Página SEO? · Palabra clave · Intención · Volumen · Dificultad de la palabra clave · Posición · Tipo · ¿Dejar, actualizar o eliminar? · Prioridad · Notas |
| 7. Análisis de Competidores | Reporte de análisis de competidores | Disposición transpuesta: una fila por métrica y una columna por sitio (el propio y Competidor 1 a 4). Filas: Sitio web · Estadísticas clave (Autoridad de Dominio DR/DA, Ranking Ahrefs AR, Dominios referidos RD, Tráfico orgánico estimado mensual, Valor del tráfico, ¿Tienen un blog?) · Tráfico por País (País 1 a 5) · Palabra 1 a 5 · Fragmentos destacados (número) · Páginas principales + palabra clave principal (Página Top 1 a 5) · Contenido más enlazado (1 a 5) |
| 9. Estrategia de Contenido | Estrategia y Plan de contenido | # · Mes · Palabra Clave · Cluster · Tipo de contenido · Titulo H1 · Volumen · Trafico Potencial · Dificultad · Tasa de conversión · Intención de búsqueda · Idea · Inspiración #1 en el SERP · Aprobado? · Notas · Pagina · Estatus |
| 11. Producción | Producción de contenido | Palabra Clave · Tipo de pagina · Cluster · URL sugerido · H1 Sugerido · Estatus · Fecha de entrega · Gdoc · Autor · Notas. Se agrupa con filas separadoras "Mes #1", "Mes #2", etc. |
| Actualización de Contenidos | Actualización de Contenidos o Content Updates | URL · Palabra Clave · Posición · Meta Titulo Existente · Meta Titulo Nuevo · Meta Descripcion Existente · Meta Descripcion Nueva · Gdoc Contenido nuevo · Status · Metas |
| 13. Tareas Revisión Técnica | (sin título) | ASPECTO A REVISAR · ESTATUS · FOTO · COMENTARIO · LINK · Tasks encontrados. Agrupada por bloques con filas de sección: 1. Indexabilidad y rastreabilidad (Robot, Sitemap, Arquitectura, Breadcrumbs, Indexación, GSC, Datos estructurados, Screaming Frog, Page Speed Insights, Móvil, Botones, Contenido), Paso 3 HTTPS y Seguridad, Paso 4 Optimización de imágenes, Paso 5 Canonicalización, Bonus Quick wins |
| 15. Auditoría técnica | Auditoría técnica SEO | Recomendación · Prioridad · Impacto · Confianza · Facilidad · Puntuación ICE · Área de impacto · Estatus |
| 17. Plan Especialista SEO | Plan Especialista SEO | # · Área de especialista SEO · Meta · Compromiso · Plazo de tiempo · Acción |
| 19. Servicios SEO | (nombre del especialista) | Categoría · Servicio · Descripción · Tiempo Estimado · Frecuencia · Tiempo promedio · Precio por Hora · Precio |

### Listas desplegables y fórmulas (inferidas de los valores de los ejemplos; la exportación CSV no trae las reglas de validación)

- **Intención:** Informacional, Comercial, Transaccional (y Navegacional).
- **Estatus de producción y tareas:** Pendiente, En proceso, En revisión, Aprobado, En vivo, Terminado.
- **Prioridad en la auditoría:** Crítico, Alta, Media, Baja. **Impacto, Confianza y Facilidad:** 1 a 10.
- **Puntuación ICE** = promedio de Impacto, Confianza y Facilidad (por ejemplo 10, 9 y 8 dan 9,00). Es lo que el diplomado y la Master usan para priorizar. Alta si es 8 o más, Media de 6 a menos de 8, Baja por debajo (criterio de las skills de este repo, no de la Master).
- **Mapa:** la columna "¿Dejar, actualizar o eliminar?" usa Dejarla, Actualizarla, Eliminarla; "¿Página SEO?" es Sí/No (casilla). El tipo parece una lista (en los ejemplos aparecen, entre otros, Página de aterrizaje y Producto).
- Hay columnas que parecen calculadas (en la pestaña 9, "Trafico Potencial" muestra #N/A cuando falta el volumen); las fórmulas no se pudieron leer desde la exportación CSV. El generador **no inventa** esos valores: deja `pendiente de dato`.

### Extensión del generador

`generar_master.py` conserva esos encabezados tal cual. Donde el proyecto necesita más datos, añade columnas **al final** de la pestaña 5 (Keywords secundarias, Cluster, Impacto, Confianza, Facilidad, Puntuación ICE, Estado, Responsable, Fecha calendario) y una columna "Bloque" al inicio de la pestaña 13. Si importas el archivo a tu copia oficial de la Master, pega solo las columnas originales o conserva las extra: ninguna fórmula original depende de ellas.

## Briefs: secciones por tipo

Todos los briefs de la comunidad arrancan igual: título del tipo de brief, "Equipo de SEO", Fecha, Brief (keyword), Escritor, y un cuerpo numerado con tablas de dos columnas (**Elemento de la página | Sugerencias**).

### Blog ("Brief SEO de Blog", Semana 8 L8)
I. Elementos de la página: Búsqueda (intención de búsqueda y meta del contenido) · Palabras clave (principal + volumen; secundarias + intención) · URL sugerida · Metas (meta título y meta descripción sugeridos) · H1 sugerido · NLP Report (puntuación, contenido del reporte, conteo de palabras, ejemplos/inspiración).
II. Imágenes y media: Recomendaciones de imágenes (nombre de archivo y ALT con la palabra clave) · Otras sugerencias de SEO (legibilidad, párrafos cortos).
III. Links internos: páginas que mencionan a ESTA página (URL y Anchor) · páginas que se mencionan en esta (URL y Anchor).
Sugerencias de la estructura: jerarquía H1, H2, H3 completa, con las preguntas PAA como H2.

### Landing o página de servicio ("Brief de páginas de venta o Landing Page", Semana 8 L9)
I. Palabras clave: vertical · principal + volumen · secundarias · top competidores.
II. Información de la página: URL · H1 · Meta título · Meta descripción.
III. Servicio: servicio principal · tipo de servicio · propuesta(s) de valor · objetivo de la página · beneficios (corto, mediano y largo plazo) · prueba social · llamado a la acción · público objetivo.
IV. NLP (reporte).
V. Internal links: de otras páginas hacia esta y desde esta hacia otras (URL y Anchor).
Más estructura de encabezados y, por diplomado, propuesta de valor y CTA **above the fold**.

### E-commerce (producto o categoría, Semana 8 L10)
Del diplomado (no se encontró un ejemplo público de la comunidad para verificar el formato exacto): palabras clave transaccionales de alta intención, atributos técnicos (especificaciones, medidas, materiales), beneficios directos, etapa del embudo, prueba social (reseñas, valoraciones), garantías y devoluciones, urgencia y escasez, cross-sell y up-sell (productos relacionados), preguntas frecuentes, información de envío, CTA, más las secciones comunes de metas, H1, NLP, imágenes y links internos.

### Contenido existente ("Brief SEO de contenido existente", Semana 10)
Misma estructura que el brief nuevo pero con pares **actual / sugerido**: URL actual y URL sugerida (regla de oro: si la página genera tráfico y clics, no se cambia; un cambio exige 301), meta título actual y sugerido, meta descripción actual y sugerida, H1 actual y sugerido, NLP, ejemplos/inspiración, imágenes, links internos y nueva jerarquía de H2/H3. Para e-commerce se suma una matriz de **impacto vs esfuerzo**: prioridad 1 metas y keywords con impresiones; 2 schema y reseñas; 3 rediseño de imágenes o videos. Lema: "no rompas lo que funciona".

## Dónde se desvía la comunidad del diplomado

- La comunidad usa la Master con tantas filas como páginas; el mapa de la pestaña 5 incluye todas las URL del inventario (hasta cientos), no solo las que se van a producir. El generador mantiene esa idea: una fila por URL del mapa.
- El diplomado habla de "Plantilla Master" con pestañas de Producción y Estrategia; la numeración (1, 3, 5, 7, 9, 11, 13, 15, 17, 19) es de la copia oficial que circula en los canales.
- Los alumnos suelen dejar el volumen como "<100" o rangos ("10-100"); el generador lo conserva como texto y no lo usa en cálculos.
