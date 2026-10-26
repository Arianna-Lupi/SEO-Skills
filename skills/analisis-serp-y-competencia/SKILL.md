---
name: analisis-serp-y-competencia
description: "Usa esta skill cuando el usuario quiera analizar competidores a partir de lo que sale en Google para una keyword, estudiar la SERP o encontrar brechas/gaps de contenido, aunque no diga \"SERP\" ni \"competencia\", p.ej. \"quién me gana en Google\", \"por qué rankean ellos y yo no\", \"qué le falta a mi contenido frente a los primeros\", \"qué hacen los que están arriba\", \"qué temas no estoy cubriendo\", \"compara mi página con las del top\", \"en Google salen tiendas y yo tengo un blog\". Sigue el método \"De Cero a SEO\" (aprendoseo, Arianna Lupi): distingue Competidor de Negocio vs Competidor SEO, identifica rivales por 3 métodos (incluido el \"Análisis de Repetición\"), aplica el \"Ojo Clínico\" sobre el top 3, perfila cada página del top (script), la compara con la tuya, detecta brechas bajo el marco \"Costo de Oportunidad\" y las convierte en tareas con verbo y prioridad por ICE."
compatibility: perfil_competidor.py, comparar_serp.py y brechas.py usan solo Python 3 stdlib; serp.py requiere Python 3 (uv) + requests + SERPAPI_API_KEY. SerpApi y Ahrefs MCP son opcionales (la skill funciona 100% manual con Google en incógnito y HTML guardado).
metadata:
  author: aprendoseo
  milestone: SEO skills (De Cero a SEO)
  version: "1.2"
---

> **🚫 Regla de datos (obligatoria): NUNCA inventes números.**
> No estimes, supongas ni inventes métricas o datos que no tengas: volumen de búsqueda, dificultad/KD, clics, impresiones, CTR, posición, tráfico, Core Web Vitals, backlinks, fechas, precios, etc. Si te falta un dato, **pídeselo al usuario y espera su respuesta** — que lo pegue a mano, lo exporte (Google Search Console, Ahrefs, DinoRank, Screaming Frog…) o lo conecte por MCP. Da igual de dónde venga, pero tiene que venir de una fuente real. Si aun así no hay dato, márcalo explícitamente como `pendiente de dato` y NO continúes como si lo tuvieras. Un entregable con huecos honestos vale más que uno con cifras inventadas.

> **📊 Cierre en dashboard.** Cuando trabajes sobre un sitio, además de tu entrega persiste tu salida estructurada en `.seo-audit/<sitio>/data/competitors.json` (esquema en la skill `dashboard-seo`). Al cerrar el flujo SEO, genera/actualiza el dashboard con `dashboard-seo` y entrega el URL local. Tu archivo: `competitors.json`.


Actúa como estratega SEO en aprendoseo, siguiendo el método de Arianna Lupi (Semana 6 del diploma "De Cero a SEO").

> **Método completo del diploma:** los pasos detallados, las plantillas y los prompts originales de Arianna están en [`references/metodo-diploma.md`](references/metodo-diploma.md). Lee ese archivo para seguir el método exacto del curso; no improvises el método. La práctica de los coaches está en [`references/practica-coaches.md`](references/practica-coaches.md).

## Cuándo usar

- El usuario quiere saber quién compite por sus keywords y por qué rankea.
- Pide analizar la SERP, las páginas top o la estructura de los competidores.
- Busca **brechas/gaps de contenido** y oportunidades.
- Quiere comparar su página con las que salen arriba, o sospecha que Google premia otro tipo de página que la suya.
- Quiere un reporte de competencia accionable, con tareas.

Para descubrir keywords primero usa `investigacion-de-keywords`; para mapearlas a URLs propias, `mapa-de-palabras-clave`; para descubrir solo los dominios rivales, `analisis-de-competidores`.

## Entradas (qué te doy)

- 3 a 5 keywords objetivo (idealmente del punto dulce / Top 5).
- Web propia (la URL de la página que quiere posicionar para cada keyword) y, si los conoce, competidores que sospecha.
- País/idioma de la SERP.
- Opcional: HTML guardado de las páginas, exportaciones de Ahrefs o volúmenes reales (ver `references/datos-opcionales.md`).

## Datos (MCP opcional)

Funciona **sin MCP**. Fallback manual: el usuario abre Google (modo incógnito), pega el top 3-5 por keyword y describe lo que ve (o guarda el HTML con "Guardar como"); tú lo organizas con el "Ojo Clínico" y armas el reporte de gaps.

- **SerpApi MCP (GRATIS, principal aquí):** `mcp__serpapi__search` para top results, **People Also Ask**, búsquedas relacionadas y SERP features por keyword.
- **Ahrefs MCP (PAGO, enriquece):** `mcp__claude_ai_Ahrefs__serp-overview`, `...-site-explorer-organic-keywords`, `...-top-pages`, `...-domain-rating`, `...-organic-competitors`. Detalle en [`references/datos-opcionales.md`](references/datos-opcionales.md).

Nunca exijas un MCP. Ver `../../MCP-SETUP.md`.

## Proceso (flujo completo: SERP, competidores, perfil, comparación, brechas, tareas)

Los pasos 1 a 4 y 6 a 8 son el método del diplomado. Los scripts (pasos 5, 7 y 9) son un acelerador que no reemplaza el criterio ni el Ojo Clínico.

1. **Distinguir tipos de competidor** (Semana 6 · lección 2):
   - **Competidor de Negocio:** vende lo mismo que tú.
   - **Competidor SEO:** quien **rankea tus keywords**, aunque NO venda lo mismo (Wikipedia, un blog, un medio). En SEO importan estos.
   - Subdivide cada uno en **Directos** vs **Indirectos**.
2. **Leer la SERP y el tipo de contenido que premia** (Semana 4 · lección 8; Semana 8 · lección 3, el brief lo dicta la SERP): busca cada keyword en incógnito y anota qué tipo de página domina (blog, categoría, ficha de producto, servicio, landing, herramienta, vídeo, foro). Si Google solo muestra tiendas, un artículo de blog no va a posicionar ahí. Si el tipo de la SERP no coincide con tu página, **para y pasa por `intencion-de-busqueda`** antes de hablar de brechas de contenido.
3. **Identificar competidores por 3 métodos** (Semana 6 · lección 3):
   - **Búsqueda directa en Google** de tus keywords (incógnito).
   - **Herramientas SEO** (Ahrefs/SEMrush/SimilarWeb).
   - **"Análisis de Repetición":** un dominio que aparece en **3 de tus 5 keywords = competidor crítico**. `analisis-de-competidores` lo calcula con la SERP; `comparar_serp.py` también lo hace con los perfiles.
   - **Elige 3-4 competidores** para analizar. Criterios de los coaches: un sitio de prensa que vive de publicidad sirve para ideas de contenido, no para comparar páginas de producto; un competidor de alcance muy distinto al tuyo no sirve; si tu nicho no tiene rivales con datos, amplía a sitios del mismo tema o a referentes de otros países. Ataca primero lo ganable (Ari: "las de Serie A son difíciles, pero veo oportunidades con las de Juventus").
4. **Ejercicio manual "Ojo Clínico" (PRIMERO, antes de herramientas):** para 3-5 keywords, abre el **top 3** y anota:
   - Navegación y diseño.
   - Encabezados (H1/H2) y estructura del contenido.
   - Presencia de blog.
   - CTAs y propuesta de valor.
   - Qué páginas tienen ellos y tú no; cómo estructuran servicios, precios o paquetes; FAQ, portafolio y landings por ciudad (práctica de Vero).
   - Si el negocio es físico, revisa también Local Pack y Maps (práctica de Ari).
5. **Perfilar cada página del top (acelerador, opcional):** con `scripts/perfil_competidor.py` obtienes, por URL del top, título, meta, H1 a H3, palabras, tipo de página, schema, imágenes, enlaces, fecha, señales de autoría y E-E-A-T, FAQ/listas/tablas/vídeo y si depende de JavaScript. Convierte tu Ojo Clínico en datos comparables; no lo sustituye. Las páginas que dependen de JavaScript quedan marcadas: míralas a ojo. Ver "Scripts" abajo.
6. **Volcar a la Plantilla Master (tab Competencia)** para 2-3 competidores (Semana 6 · lección 4):
   - **Keywords Top** que rankean.
   - **Páginas Top** (las que más tráfico/posiciones traen).
   - **Autoridad / Estructura** (DR, arquitectura, tipos de contenido).
   Con llenar el 50-60 % de los datos de al menos 2 competidores hay base sólida. Si un competidor no tiene datos, simplifica las keywords o amplía el nicho; si Ahrefs no muestra el AR, deja la celda en blanco o usa MozBar (práctica de Vero). Los datos de dominio de pago son opcionales (`references/datos-opcionales.md`).
7. **Comparar y detectar brechas** (Semana 6 · lecciones 4 y 5): con `scripts/comparar_serp.py` sacas el patrón común del top (lo que tiene al menos el 60 %), la tabla tu página frente al top y las brechas por categoría: tipo de página, cobertura de temas, estructura, formato, schema, E-E-A-T y frescura. La **meta** del análisis es la brecha (lo que ellos cubren y tú no), no copiar al rival: **adapta, no copies**.
8. **Redactar el reporte** (Google Doc) enmarcado en **"Costo de Oportunidad"**: qué tráfico/clientes se pierden por no cerrar cada gap. Enfoque positivo, 3 conclusiones clave y gráficos de la brecha si tienes datos. Las **conclusiones responden "qué tiene el rival que yo no"**, no describen tu propio sitio (corrección típica de Vero). Mejorar tu velocidad es una tarea del sitio, no una conclusión sobre el competidor. Una plantilla llena sin conclusiones está incompleta.
9. **Convertir cada brecha en una tarea con verbo** (Semana 6 · lección 6): cada insight se vuelve una tarea que empieza con verbo ("Añadir una tabla comparativa a la página X", no "analizar tablas"), con **plazo, recurso y responsable** (los defines tú) y prioridad por **ICE** (impacto, confianza, facilidad; promedio, como en `plan-seo`). Empieza por lo fácil o lo que ya dominas. Añade una columna de **Prioridad o Esfuerzo** y un quick win (Ari: crear el perfil de Google Business Profile puede dar resultados locales antes que escribir 10 artículos). `comparar_serp.py` propone el borrador de tareas con ICE; edítalo con el usuario.
10. **Entregar a las demás skills:** las tareas de contenido van a `brief-de-contenido` (el brief lo dicta la SERP, Semana 8), las de schema a `schema-jsonld`, las de metas a `optimizacion-on-page-meta`, las de autoría y E-E-A-T a `calidad-de-contenido-eeat`, las de frescura a `actualizacion-de-contenido` y todo el conjunto a `plan-seo`. El contrato de datos está en [`references/contrato-datos.md`](references/contrato-datos.md).

## Salida

**(A) Tab "Competencia" de la Plantilla Master:**

| Competidor | Negocio/SEO | Directo/Indirecto | Repetición (de 5 kw) | Keywords Top | Páginas Top | Autoridad/Estructura |
|---|---|---|---|---|---|---|

**(B) Notas "Ojo Clínico"** por keyword (navegación, encabezados, blog, CTAs).

**(C) Reporte (Google Doc), "Costo de Oportunidad":**
- Competidores críticos (por Análisis de Repetición).
- **Brechas de contenido** priorizadas, por categoría.
- Por cada brecha: oportunidad estimada y costo de no actuar (con volumen real o `pendiente de dato`).
- Tareas con verbo, ICE, plazo, recurso y responsable.

**(D) Archivos (si usaste los scripts):** `perfiles.json`, `comparacion.json`, el Markdown listo para pegar y `.seo-audit/<sitio>/data/competitors.json`.

## Ejemplo

Keywords: "café de especialidad", "café en grano", "cómo preparar café", "café orgánico", "tienda de café online".

Análisis de Repetición: `revistacafe.com` aparece en 3 de las 5 → **competidor SEO crítico** (es un medio, no vende café, pero domina lo informativo).

Ojo Clínico (top 3 de "cómo preparar café"): los 3 tienen blog extenso con H2 por método (V60, prensa, espresso) y video; tu sitio no tiene blog → **gap claro**.

Perfilado del top: los 3 son guías de 800 a 1.300 palabras con autor, fecha, FAQ y schema Article; tu página tiene 250 palabras, un H2 y nada de eso. Tareas: "Ampliar la guía cubriendo prensa francesa y V60" (ICE alto), "Mostrar autor y fecha", "Incorporar una sección de preguntas frecuentes".

Caso de desajuste: en "comprar café de especialidad" el top son categorías y fichas de producto, y tu página es un blog. La brecha mayor no es de contenido sino de tipo de página: la tarea es "Crear la página de categoría", y las demás pasan a segundo plano.

Reporte: "No tener guías de preparación cede el tráfico informativo a revistacafe.com. Costo de oportunidad: visitas/mes `pendiente de dato` hasta cruzar el volumen real de Search Console o Ahrefs."

## Scripts (aceleradores deterministas)

Todos con `--help`. Ejemplo sin red con datos de muestra: `bash fixtures/ejecutar_ejemplo.sh`.

**1. Capturar la SERP (`serp.py`, SerpApi).** Si falta `SERPAPI_API_KEY` o `requests`, sigue en modo manual (Google en incógnito).

```bash
SERPAPI_API_KEY=xxx uv run scripts/serp.py "tu keyword" --gl es --hl es --num 10 > serp1.json
```

Devuelve `{"ok": true, "query": ..., "top": [{position,title,link,snippet}], "paa": [...], "related": [...], "features": {...}}`. Si falla, `{"ok": false, "reason": "...", "fallback": "modo manual: ..."}` (exit 0).

**2. Perfilar el top (`perfil_competidor.py`, solo stdlib).** Entra a cada URL con User-Agent de navegador real, respeta robots.txt, espera 2 segundos entre peticiones y detecta WAF (403/429/desafío: te dice qué hacer). También trabaja sin red con HTML guardado.

```bash
python3 scripts/perfil_competidor.py --serp-json serp1.json serp2.json --own-url https://tusitio.com/pagina --out perfiles.json
# sin red: guarda el HTML desde el navegador
python3 scripts/perfil_competidor.py --serp-json serp1.json --html https://rival.com/x=rival.html --own-html mia.html --sin-red --out perfiles.json
```

Devuelve `profiles[]` con título, meta, `headings`, `word_count`, `page_type` (con `page_type_signals` que explican la heurística), `schema_types`, imágenes, enlaces, fechas, `eeat`, `formats` y `javascript_dependent`. Las heurísticas de tipo de página están explicadas en `page_type_signals` y en `references/contrato-datos.md`; son orientativas (confianza alta, media o baja).

**3. Comparar y priorizar (`comparar_serp.py`, solo stdlib).**

```bash
python3 scripts/comparar_serp.py perfiles.json --md reporte.md --out comparacion.json --sitio tusitio.com
```

Produce el patrón común (60 %), la tabla tu página frente al top, las brechas por categoría, el puntaje de Costo de Oportunidad por keyword, el Análisis de Repetición (dominios y URLs en más SERPs), las tareas con verbo e ICE, y escribe `.seo-audit/<sitio>/data/competitors.json` (fusiona con lo que ya exista). El **puntaje de Costo de Oportunidad no es del diplomado**: es una ayuda relativa de este repo con la fórmula explicada en el informe; no son visitas ni dinero. Sin tu página propia, solo entrega el patrón.

**4. Brechas por posición (`brechas.py`, opcional).** Con las posiciones de tu dominio y las de los competidores por keyword (export de Ahrefs, `serp.py` o a mano):

```bash
python3 scripts/brechas.py --file posiciones.csv --own midominio.com
```

Entrada: CSV `keyword,domain,position[,url,volume]`. Devuelve `gaps`, `weak`, `defended`, `top_pages` y los competidores críticos. Ejemplo en `fixtures/posiciones_muestra.csv`.

## Complementos opcionales

Después del método del diploma, [`references/complementos-claude-seo.md`](references/complementos-claude-seo.md) añade: lectura del consenso de la SERP, matriz de brecha de contenido con puntuación, taxonomía de tipos de página y desajuste, y cuándo conviene una página de comparación o de alternativas. Es material externo (claude-seo, MIT), no parte del método del diplomado. Los datos de dominio de pago (Ahrefs, SerpApi) están en [`references/datos-opcionales.md`](references/datos-opcionales.md).

## Gotchas

- **Competidor SEO ≠ competidor de negocio:** quien rankea tus keywords (puede ser Wikipedia, un blog o un medio que no vende lo que tú), no necesariamente quien te compite vendiendo.
- Haz el **"Ojo Clínico" manual sobre el top 3 ANTES de las herramientas y los scripts**, no al revés: el análisis a ojo va primero, las métricas después.
- **Si la SERP está dominada por otro tipo de página que la tuya**, la brecha principal es de tipo, no de contenido: decide con `intencion-de-busqueda` si creas la página que Google premia. Las demás brechas esperan.
- El objetivo es **la brecha de contenido (lo que ellos cubren y tú no)**, no copiar al rival ni juntar una lista de datos.
- Analiza **3-4 competidores**, priorizando los del Análisis de Repetición, no "todos los que aparezcan".
- Enmarca el reporte en **Costo de Oportunidad** (tráfico/clientes perdidos por cada gap), no como reporte descriptivo. Sin volumen real, escribe `pendiente de dato`; nunca estimes visitas.
- Mira la SERP en **modo incógnito / región correcta**, no logueado: la personalización falsea el ranking.
- **Conclusiones de competencia que miran tu propio sitio**: deben decir qué tiene el rival que tú no (Vero). Una plantilla sin conclusiones está incompleta.
- **Competidor mal elegido**: prensa o modelos de negocio distintos sirven para ideas de contenido, no para copiar páginas de producto.
- **Herramienta que devuelve cero o vacío**: escribe 0 o deja en blanco; no estimes (regla de datos).
- **Documento antes que tabla**: el análisis escrito pesa más que la tabla (Ari). El reporte debe nombrar el sitio correcto en todas las secciones.
- **Páginas que dependen de JavaScript**: el HTML original casi vacío da conteos parciales. Revísalas en el navegador y no las cuentes en rangos de palabras.
- **Sitio con WAF** (403/429): no insistas con el script. Guarda el HTML desde el navegador (`--html`) o usa un rastreador con navegador real; el script respeta robots.txt y limita el ritmo, no lo desactives en sitios ajenos.
- **Más palabras no es mejor:** el rango de palabras del top describe lo que cubren, no una meta. Cubre los temas; la extensión sale sola.
- **Antes de comparar, intención**: si la SERP premia otro formato que el tuyo, usa `intencion-de-busqueda` antes de hablar de brechas de contenido.
