# Práctica de coaches: análisis de SERP y competencia

> Autoridad secundaria. Afina criterios y ejemplos del método de la Semana 6; no lo contradice. Las referencias `#NNN` son mensajes del foro de aprendoclub. Fuente: perfiles de Ari (instructora de la Semana 6) y de Vero (estrategia SEO).

## Ari (Arianna Lupi)

- **Negocio frente a SEO.** "No es una competidora SEO (no te está robando clics en Google)" (#190). Antes de analizar a un rival, pregunta si aparece en la SERP de tus keywords.
- **El competidor más pesado.** Pregunta "¿cuál consideras que es el competidor más pesado y por qué?" (#337) y ataca primero lo ganable: "las de Serie A son algo difíciles, pero veo oportunidades para las de Juventus" (#222). En el script esto se traduce en mirar la columna `facilidad` de las tareas y la `mejor_posicion` del Análisis de Repetición.
- **El documento pesa más que la tabla** (#120, #200). Pide primero el documento de análisis; las tablas y los números del script son insumo.
- **Cero es un dato.** Si la herramienta marca cero, se escribe "0" (#190). El script nunca rellena huecos: usa `pendiente de dato`.
- **Nombra el sitio correcto** en todas las secciones del reporte e incluye 3 o 4 keywords de arranque (#190, #249).
- **Llévalo al embudo** (#157): lista las 5 a 10 páginas con más tráfico de cada competidor (en `perfil_competidor.py`, las URLs del top de cada SERP; el tráfico lo aporta Ahrefs si lo tienes) y suma una columna de **Prioridad o Esfuerzo** con un quick win: "Crear y optimizar el perfil de Google Business Profile podría generar resultados locales más rápidos que escribir 10 artículos de blog".
- **Negocio físico:** Local Pack, Maps, citaciones locales y perfil de empresa (#249). Una SERP con mapa no se compara solo con páginas web: revisa la ficha de los rivales a ojo.

## Vero (Estrategia SEO)

- **Elegir bien a quién mirar.** Un sitio de prensa que vive de publicidad sirve para ideas de contenido, no para páginas de producto (#132). Un competidor de alcance muy distinto no sirve (#197). Añade dos competidores más y referentes de otros países como inspiración (#295). Si el nicho no tiene rivales con datos, busca internacionales (#827) o sitios de información cercana (#821).
- **Qué mirar en cada página:** páginas que tiene y tú no, cómo estructura servicios, precios o paquetes, FAQ, portafolio y llamados a la acción (#540); categorías y navegación (#821); imágenes de producto con texto (#256); landings por ciudad (#180). `perfil_competidor.py` cubre FAQ, imágenes, tablas, listas, schema y encabezados; el resto sigue siendo Ojo Clínico.
- **Las conclusiones responden "qué tiene el rival que tú no".** Mejorar tu velocidad es una tarea del sitio, no una conclusión sobre el competidor (#540). Una plantilla llena sin conclusiones está incompleta (#588, #682).
- **Datos de autoridad:** AR de Ahrefs en blanco si no aparece (#597); MozBar para autoridad (#369); Ahrefs Traffic Checker o el de SE Ranking según cuál devuelva datos (#612); Moz Competitive Research para posiciones top (#170); Mangools SERP Simulator para comparar metas (#600).
- **La SERP decide el tipo de contenido** (#125, #152, #788): si dos keywords muestran las mismas páginas, comparten intención (#218). Aplica igual al comparar: si el top son fichas de producto y tú tienes un artículo, el problema es el tipo de página.

## Cómo se refleja en la skill

| Criterio de coach | Dónde está |
|---|---|
| Documento antes que tabla | Paso 8 de `SKILL.md`, reporte en Markdown de `comparar_serp.py` |
| Conclusión = qué tiene el rival que no tienes | Paso 8 y gotchas |
| Prioridad o Esfuerzo y quick win | Columnas `ICE`, `facilidad` y `prioridad` de las tareas |
| Ojo Clínico antes de herramientas | Paso 4 antes del paso 5 |
| Competidor mal elegido | Paso 3 |
| Tipo de contenido según la SERP | Paso 2 y brecha "tipo de página" |
