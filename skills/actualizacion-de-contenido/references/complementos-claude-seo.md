# Complementos de claude-seo para actualización de contenido

> **Complemento externo (claude-seo, MIT), no es parte del método del diplomado.** Autor: agricidaniel (modo "improve" del brief con base en `skills/seo-content-brief`, autor original puneetindersingh; scripts `content_quality.py` y `content_verify.py`). Adaptado al español y a la terminología del diplomado. Si algo de aquí contradice al curso, gana el curso.

## 1. Modo "mejorar" del brief (origen: skills/seo-content-brief)
Coincide con el curso en lo esencial: lee la página existente, identifica qué ya es fuerte (se conserva), qué falta, está delgado o desactualizado, y distingue "mantener/reforzar" de "añadir" en el esquema. Aporta, además:
- **Puntuación de brechas de la competencia:** puntúa de 1 a 10 a cada competidor real en Profundidad, Formato, SEO y UX, e identifica tres tipos de brecha: **de tema** (subtemas que nadie cubre), **de profundidad** (cubiertos de forma superficial) y **de calidad** (datos viejos, sin perspectiva experta, mal formateados). Úsalo para llenar la sección "Competencia / inspiración" de la plantilla. Son juicios cualitativos tuyos: no los presentes como datos de herramienta.
- **Filtra los no competidores** antes de comparar: enciclopedias, redes, foros, marketplaces, agregadores, directorios, herramientas SEO, medios y dominios .gov/.edu no son competencia de negocio aunque rankeen. En una SERP en español, añade los equivalentes locales.
- **Regla de relevancia del sitio:** cada H2, subtema y pregunta que sugieras debe poder cumplirlo la web de verdad. No copies la estructura de un competidor si cubre algo que tu cliente no ofrece.
- **Regla de cobertura de estructura** (páginas hub o "tipos de"): el esquema menciona cada categoría o servicio que existe en el sitio, cada una con su enlace interno, sin inventar categorías.

## 2. Ganancia de información (origen: seo-content-brief)
Cada brief de optimización debe decir **qué valor nuevo aporta** que ninguna página del top tiene: datos propios, un caso real con resultado, cita de experto, un marco original. "Más detalle" o "mejor formato" no cuentan. Se alinea con "valor real" de la Semana 11 y con el pilar de Experiencia de la Semana 7.

## 3. Frescura (origen: seo-content)
- Fecha de publicación visible y, si el contenido se revisó, **fecha de última actualización** visible.
- Marca para revisión el contenido de más de 12 meses en temas que cambian rápido.
- No cambies la fecha sin cambiar el contenido: es una señal falsa.

## 4. Verificación de afirmaciones antes de publicar (origen: scripts/content_verify.py)
Idea portable: extrae del texto las afirmaciones verificables (porcentajes, cifras, "según un estudio", años) y marca las que no tienen una fuente cercana. En esta skill lo cubre `redaccion-y-optimizacion-nlp/scripts/ai_tells.py` y `calidad-de-contenido-eeat/scripts/calidad_contenido.py` (sección afirmaciones sin fuente). Regla del diplomado (Semana 14, lección 12): verifica cada dato estadístico o nombre técnico antes de publicar.

## 5. Umbrales de metas: diferencia con el curso
claude-seo sugiere meta título 50 a 60 (igual que el curso) y **meta descripción 130 a 150**. **Gana el diplomado: 120 a 155.** Si ves el rango de claude-seo en otra herramienta, trátalo como un caso particular dentro del rango del curso.

## 6. Nota sobre FAQ y Schema
El curso (Semana 10, lección 6, prioridad P2; Semana 14, lección 13) recomienda Schema y FAQ. claude-seo documenta que Google retiró los resultados enriquecidos de FAQ para la mayoría de sitios y que no hay beneficio de ranking confirmado. Decisión: sigue el curso para el marcado válido y coherente con el texto visible, pero **no prometas rich results de FAQ al cliente**; confirma el estado vigente en la documentación oficial de Google antes de comprometerte. Para el marcado usa la skill `schema-jsonld`.

## Ideas que no se trajeron
- Generación automática de "word count objetivo por sección" de claude-seo: el curso no fija longitudes y la práctica de coaches advierte contra perseguir una cifra (600 palabras que resuelven la intención superan a 3000 de relleno, Dana #159).
