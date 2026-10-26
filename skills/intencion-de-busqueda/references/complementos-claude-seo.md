# Complemento externo (claude-seo, MIT), no es parte del método del diplomado

> Origen: `claude-seo` de agricidaniel (licencia MIT), `skills/seo-sxo/` (SKILL.md y `references/page-type-taxonomy.md`, `user-story-framework.md`, `persona-scoring.md`) y `skills/seo-cluster/references/serp-overlap-methodology.md`. Adaptado al español y a la terminología del diploma. Si algo de aquí contradice el diplomado, **gana el diplomado**.

Úsalo solo **después** de haber hecho los pasos 1 a 6 del `SKILL.md`.

## 1. Solape de SERP con umbrales (apoya el criterio de Vero)

El diplomado dice "si salen casi las mismas páginas, una URL". Una forma de hacerlo medible es contar cuántas URLs del top 10 comparten dos keywords:

| URLs compartidas | Relación | Qué hacer |
|---|---|---|
| 7 a 10 | Misma URL | Una sola página; la keyword de mejor ratio volumen/dificultad manda en URL y H1 |
| 4 a 6 | Mismo cluster | Misma familia temática; decide entre dos posts o una página con secciones según volumen y formato |
| 2 a 3 | Enlazar | Clusters vecinos; páginas separadas que se enlazan |
| 0 a 1 | Separar | Intención distinta |

Desempate cuando el solape cae entre 3 y 4: mira si los dominios se repiten aunque las páginas cambien, si el formato es el mismo y si una keyword tiene mucho más volumen que la otra (la de mucho más volumen suele merecer su propia página). Ante la duda, mantén el mismo cluster con posts separados.

Cautelas:
- No agrupes por parecido de texto: "entrenamiento de perros" y "clases de adiestramiento" pueden tener SERP distintas.
- No ignores los rasgos de la SERP: si una keyword dispara mapa local y otra un fragmento destacado, necesitan formatos distintos aunque se solapen URLs.
- Quita los dominios que aparecen en casi todas las SERP (Wikipedia, YouTube, grandes marketplaces) antes de puntuar. El script lo hace con `--ignore-ubiquitous N`.
- Con muchas keywords el número de pares crece rápido (40 keywords son 780 pares). Agrupa antes por intención y por término principal y compara solo dentro del grupo, verificando por muestreo.

## 2. Taxonomía de tipos de página (para clasificar el formato)

Clasifica cada resultado de la SERP y tu página en un solo tipo. Equivalencias con los formatos que nombra el curso:

| Tipo | Señales principales | Formato del curso |
|---|---|---|
| Artículo | autor, fecha, cuerpo largo, migas con /blog/ | Artículo, guía |
| Listado | "los 10 mejores", títulos numerados, varias opciones | Listado de "los mejores" |
| Comparativa | "vs", tabla de características, pros y contras | Investigación comercial |
| Producto | precio, botón de compra, reseñas, SKU | Ficha de producto |
| Categoría | grilla de productos, filtros | Categoría de e-commerce |
| Servicio | proceso, casos, formulario de contacto | Página de servicios |
| Landing | una propuesta de valor, CTA principal, navegación mínima | Landing |
| Local | dirección, mapa, teléfono, horarios | Ficha local, Maps |
| Herramienta | campos de entrada, calculadora o generador | Herramienta |
| Video | reproductor como contenido principal | Video |

Prioridad cuando una página muestra señales de varios tipos: herramienta, local, comparativa, producto, landing, servicio, mixto (educativo con CTA) y, por defecto, artículo.

## 3. Consenso y severidad del desajuste

- Consenso fuerte: más del 60 % de los resultados comparten tipo. Mixto: entre 40 % y 60 %. Fragmentado: menos del 40 %.
- Severidad del desajuste entre tu tipo de página y el que premia la SERP:

| Tu página | La SERP premia | Severidad |
|---|---|---|
| Artículo | Producto o Categoría | Crítica |
| Artículo | Comparativa o Listado | Alta |
| Producto | Artículo | Alta |
| Landing | Herramienta | Alta |
| Servicio | Resultados locales | Media |
| Mismo tipo | Mismo tipo | Alineado: céntrate en profundidad y UX |

Con SERP fragmentada hay hueco para diferenciarte: valida con el Ojo Clínico de la Semana 6 antes de decidir.

## 4. Historias de usuario desde la SERP (opcional, para briefs)

Señales que se leen en la SERP y qué revelan:
- Preguntas de "La gente también pregunta": dudas y objeciones.
- Anuncios: disparadores comerciales y propuestas de valor.
- Búsquedas relacionadas: el recorrido (qué buscan antes y después).
- Formato del fragmento destacado: estructura de respuesta esperada.

Plantilla: "Como [persona], quiero [objetivo] porque [motivo emocional], pero me frena [barrera]". Genera de 3 a 5 historias y úsalas como insumo del `brief-de-contenido`. No las cites como método del curso.

## 5. Puntuación por persona (opcional)

Para una página que ya existe y tiene un desajuste leve, puntúa de 0 a 25 cada una de estas dimensiones por persona de la SERP: relevancia, claridad (la respuesta se encuentra en 10 segundos), confianza y acción (siguiente paso claro). Ordena las mejoras empezando por la persona con menor puntuación. Es una ayuda cualitativa: no inventes puntajes sin haber leído la página.
