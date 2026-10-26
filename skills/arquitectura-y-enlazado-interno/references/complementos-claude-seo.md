# Complemento externo (claude-seo, MIT), no es parte del método del diplomado

> Origen: `claude-seo` de agricidaniel (licencia MIT), `skills/seo-cluster/references/hub-spoke-architecture.md` (reglas de enlaces, límites y cuadro de mando) y `skills/seo-cluster/references/execution-workflow.md` (puntuación del cluster). Adaptado al español y a la terminología del diploma. Si algo contradice el diplomado, **gana el diplomado** (Semana 9: regla de los 3 clics, Crawl Depth y Crawl Width, 4 tipos de enlace interno).

Úsalo solo **después** de diseñar la arquitectura con el método de Juan y Vero.

## 1. Enlaces obligatorios, recomendados y opcionales por cluster

| Nivel | Regla |
|---|---|
| Obligatorio | Cada página del cluster enlaza al pilar al menos una vez en el cuerpo. El pilar enlaza a todas las páginas de sus clusters. Sin esto, la estructura está rota. |
| Recomendado | De 2 a 3 enlaces entre hermanas del mismo cluster, con anchor contextual (la keyword o una variante cercana), dentro de párrafos y no solo en una caja de "relacionados". |
| Opcional | 0 o 1 enlace entre clusters distintos, solo si hay un puente temático real. |

Esto es compatible con el diplomado: el curso pide dirigir los enlaces al pilar y los contextuales. `matriz_enlaces.py` revisa lo obligatorio.

## 2. Umbrales de entrantes y de anchors

- Cada página debería tener al menos **3 entrantes** internos; ninguna huérfana; todo alcanzable desde el pilar en 2 clics.
- Ningún anchor debe superar el **40 %** de los enlaces que llegan a una página (diversidad de anchors). Con pocos enlaces (menos de 5) el porcentaje no es fiable.
- Anchors genéricos ("haz clic aquí", "ver más") no aportan señal temática, como dice el curso.

Los números son de claude-seo y no los fija el diplomado: úsalos como guía.

## 3. Tamaño orientativo de un cluster al planificar

claude-seo sugiere un pilar con 2 a 5 clusters y 2 a 4 páginas por cluster, un pilar de 2.500 a 4.000 palabras y soportes de 1.200 a 1.800. Son rangos de un caso, no del curso. El diplomado define cantidad de clusters según capacidad mensual (Semana 7, "10 de Oro") y la práctica de Ari recomienda un cluster por mes. Úsalos solo como contraste.

## 4. Rúbrica de puntuación de la arquitectura (auxiliar de este repo)

Puntúa de 0 a 100 después del análisis, solo con datos reales:

| Criterio | Peso | Cómo se mide |
|---|---|---|
| Profundidad | 25 | % de páginas importantes a 3 clics o menos |
| Pilar y clusters conectados | 25 | % de enlaces obligatorios presentes |
| Sin huérfanas | 20 | 20 si no hay; baja proporcionalmente |
| Conversión alimentada | 15 | % de páginas de conversión con 2 o más enlaces desde contenido |
| Anchors | 15 | Sin genéricos ni concentración excesiva |

Reporta la puntuación junto con la lista de correcciones. Si faltan datos de alguna fila, déjala `pendiente de dato` y no la calcules.

## 5. Estructura de datos del cluster (para el dashboard)

Si necesitas persistir el plan, `clusters.json` del `dashboard-seo` ya recoge `{pilar, url, spokes}`. Añade tus enlaces faltantes en `issues.json` y las tareas en `next-steps.json`.
