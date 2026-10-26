# Complemento externo (claude-seo, MIT), no es parte del método del diplomado

> Origen: `claude-seo` de agricidaniel (licencia MIT), `skills/seo-sxo/SKILL.md` (análisis de la SERP al revés y consenso), `skills/seo-competitor-pages/SKILL.md` (páginas de comparación y alternativas) y `skills/seo-cluster/references/` (cuadro de mando). Adaptado al español y a la terminología del diploma. Si algo de aquí contradice el diplomado, **gana el diplomado** (Semana 6).

Úsalo solo **después** del Ojo Clínico y del reporte de Costo de Oportunidad.

## 1. Lectura del consenso de la SERP

Para cada keyword de tu top 3-5, anota para los 10 resultados: dominio, tipo de página (artículo, listado, categoría, producto, servicio, comparativa, local, herramienta), formato (guía larga, lista, tutorial, video), profundidad aproximada y rasgos de la SERP (fragmento destacado, "La gente también pregunta", video, imágenes, mapa, AI Overview).

- Consenso fuerte: más del 60 % comparte tipo. Mixto: 40 a 60 %. Fragmentado: menos del 40 %.
- Con consenso fuerte, tu página debe ser de ese tipo (ver `../../intencion-de-busqueda/`). Con SERP fragmentada hay hueco para diferenciarte.
- Los anuncios revelan disparadores comerciales; las preguntas de "La gente también pregunta" revelan dudas que el competidor no cubre y que son brechas de contenido.

Esto amplía el "Ojo Clínico" con datos de la SERP y no lo reemplaza.

## 2. Matriz de brecha de contenido

Una forma de ordenar las brechas del paso 5 con criterios explícitos. Puntúa cada brecha de 0 a 3 con datos reales (no inventes: si falta el dato, déjalo `pendiente de dato`):

| Criterio | 0 | 3 |
|---|---|---|
| Repetición (en cuántos competidores aparece) | 1 | 3 o más |
| Cercanía de tu posición actual | no apareces | 11 a 20 |
| Intención de negocio (temperatura) | baja | alta |
| Esfuerzo | alto (todos en el top 3) | bajo (algún competidor débil) |

La suma ordena la lista de tareas. Es un apoyo para priorizar; el criterio final sigue siendo el Costo de Oportunidad. `scripts/brechas.py` calcula repetición y esfuerzo.

## 3. Cuándo conviene una página de comparación o de alternativas

Si la SERP de tu keyword premia páginas de tipo "A vs B", "alternativas a X" o "los mejores X", y tu sitio no tiene ninguna, es una brecha de formato. Reglas útiles de claude-seo para construirlas con honestidad:

- Todo dato del competidor debe poder verificarse en una fuente pública; los precios llevan la fecha ("a fecha de ...").
- Declara cuál producto es el tuyo y reconoce las fortalezas del otro. No hagas afirmaciones falsas ni engañosas sobre competidores.
- Tabla de criterios clara, veredicto o "mejor para" y enlaces cruzados entre comparativas.
- Si falta un dato público, escribe "no disponible públicamente" en lugar de adivinar.
- Revisa el contenido cada trimestre o cuando el competidor cambie algo importante.

El diplomado no enseña páginas de comparación como método; trátalas como una idea de contenido derivada de una brecha. Para el brief usa `brief-de-contenido`.

## 4. Autoridad: cuidado con el dato único

Un solo indicador de autoridad (DR, AR u otro) no resume al competidor. Combínalo con la estructura, los tipos de contenido y el tráfico aproximado. Si la versión gratuita no devuelve el dato, déjalo vacío (práctica de Vero).

## 5. Taxonomía de tipos de página (base del perfilador)

`seo-sxo/references/page-type-taxonomy.md` clasifica cada resultado en 8 tipos (landing, artículo, ficha de producto, página de servicio, página de comparación, categoría, página de ubicación, herramienta) con señales primarias y señales de SERP, y marca como desajuste crítico, por ejemplo, un artículo que apunta a una keyword de landing o una landing que apunta a un "cómo hacer". Adaptación en esta skill: `perfil_competidor.py` usa 7 tipos que coinciden con los del diplomado (Semana 4 · lección 8) más vídeo, foro y herramienta (blog, landing, ecommerce, categoría, herramienta, vídeo, foro). Las heurísticas son propias (schema, ruta, contenido) y se explican en `page_type_signals`. No se importan las reglas de severidad por pares de tipos; el comparador solo marca desajuste cuando el tipo dominante (60 %) difiere del tuyo, y lo trata como la brecha más pesada.

## 6. Señales de E-E-A-T medibles en el HTML

`seo-content` y `seo-sxo` de claude-seo listan señales observables: autor con credenciales, fechas de publicación y actualización, fuentes citadas, datos o pruebas propias, experiencia de primera mano. `perfil_competidor.py` detecta una versión simple de cada una (marcado de autor, fechas, 2 o más enlaces externos en el cuerpo, frases de datos propios y de experiencia). Son indicios, no una puntuación de E-E-A-T: para evaluar la calidad real usa `calidad-de-contenido-eeat`. El diplomado trata la autoridad por separado (Semana 6 · lección 4, "Autoridad y Estructura").

## 7. Lo que claude-seo no cubre

claude-seo no tiene un flujo de análisis de competidores a partir de la SERP sin DataForSEO de pago (`skills/seo-dataforseo`, sección "Domain & Competitor Analysis": dominios competidores, solape de keywords, tráfico estimado). `seo-competitor-pages` genera páginas "X vs Y" y no analiza, y `seo-sxo` lee la SERP al revés para detectar desajustes de tipo de página. Este flujo (perfilar, comparar, brechas, tareas con ICE) es de este repo y se apoya en el diplomado; de claude-seo solo se toma la taxonomía de tipos de página y la lectura del consenso de la SERP (secciones 1 y 5).
