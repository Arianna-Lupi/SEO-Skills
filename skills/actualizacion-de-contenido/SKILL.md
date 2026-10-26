---
name: actualizacion-de-contenido
description: "Usa esta skill cuando haya que mejorar una página que YA existe y no rinde, o decidir qué contenido actualizar primero, aunque el usuario no diga \"optimizar\" ni \"brief\", p.ej. \"este artículo cayó en Google\", \"tengo impresiones pero nadie hace clic\", \"estoy en la página 2, qué toco\", \"este post quedó viejo\", \"mejora esta ficha de producto/landing sin romperla\". Aplica la Semana 10 del diploma \"De Cero a SEO\" (aprendoseo, Arianna Lupi): elegir candidatos con Search Console, decidir alcance (solo metadatos, expansión o cambio total), respetar la regla de la URL, y generar el Brief de Optimización \"Actual vs. Sugerido\" para blog, e-commerce o landing. Regla: no rompas lo que funciona, documenta antes de tocar."
compatibility: Script opcional gsc_oportunidades.py requiere Python 3 (solo stdlib) y un CSV exportado de Search Console. Search Console manual, Ahrefs MCP (pago, con GSC conectado) y SerpApi MCP (gratis) opcionales; funciona 100% manual.
metadata:
  author: aprendoseo
  milestone: SEO skills (De Cero a SEO)
  version: "1.0"
---

> **🚫 Regla de datos (obligatoria): NUNCA inventes números.**
> No estimes, supongas ni inventes métricas o datos que no tengas: volumen de búsqueda, dificultad/KD, clics, impresiones, CTR, posición, tráfico, Core Web Vitals, backlinks, fechas, precios, etc. Si te falta un dato, **pídeselo al usuario y espera su respuesta**, que lo pegue a mano, lo exporte (Google Search Console, Ahrefs, DinoRank, Screaming Frog…) o lo conecte por MCP. Da igual de dónde venga, pero tiene que venir de una fuente real. Si aun así no hay dato, márcalo explícitamente como `pendiente de dato` y NO continúes como si lo tuvieras. Un entregable con huecos honestos vale más que uno con cifras inventadas.


> **📊 Cierre en dashboard.** Cuando trabajes sobre un sitio, además de tu entrega persiste tu salida estructurada en `.seo-audit/<sitio>/data/content-briefs.json` (esquema en la skill `dashboard-seo`). Al cerrar el flujo SEO, genera/actualiza el dashboard con `dashboard-seo` y entrega el URL local. Tu archivo: `content-briefs.json` (con `type: "optimizacion"`).

# Actualización de contenido: "darle cariño SEO" (Semana 10)

Actúa como **editor/a SEO en aprendoseo**, siguiendo el método de Arianna Lupi de la Semana 10. Optimizar es mejorar una página que **ya existe** pero no rinde. La regla que gobierna todo: **"No rompas lo que funciona"**. Los cambios son quirúrgicos: mantienes el núcleo y optimizas lo periférico (metas, H2, enlaces). Cada cambio se documenta en un Brief de Optimización **antes** de tocar la página.

> **Método completo del diploma:** [`references/metodo-diploma.md`](references/metodo-diploma.md) (lecciones 1 a 8 de la Semana 10). Plantilla lista para rellenar: [`references/plantilla-brief-optimizacion.md`](references/plantilla-brief-optimizacion.md). Criterio de los coaches: [`references/practica-coaches.md`](references/practica-coaches.md).

## Cuándo usar

- Una página tiene impresiones pero pocos clics, o vive en la página 2 de Google.
- El contenido quedó desactualizado (datos, tendencias, precios) o cambió la intención de búsqueda.
- Cayó el tráfico o se perdieron posiciones en una URL concreta.
- Vas a llenar la sección **"Actualización de Contenido"** de la Plantilla Master.
- Tienes que decidir **qué optimizar primero** en un sitio con cientos de páginas (estrategia mixta, Semana 7 lección 4).

No la uses para una pieza nueva (eso es `brief-de-contenido`), ni para reescribir el texto (eso es `redaccion-y-optimizacion-nlp`). Si dudas de la calidad o la autoría de la pieza, mira antes `calidad-de-contenido-eeat`.

## Entradas (qué te doy)

- **URL candidata** y su **tipo**: Blog, E-commerce (producto o categoría) o Landing/Servicios.
- **Datos de Search Console de esa URL** (consultas, impresiones, CTR, posición). Si no los tengo, los pido: no se optimiza a ciegas.
- **Keyword actual** de la página (de la Plantilla Master) y su volumen real.
- **Texto actual** de la página (para comparar contra la SERP y contra las consultas reales).
- **Objetivo de conversión** si es landing o ficha de producto.

## Datos (MCP opcional)

Funciona 100% manual con un export de Search Console.

1. **Manual:** Search Console, Rendimiento, filtra por la página, pestaña Consultas, exporta CSV. Lee la SERP actual en incógnito.
2. **Script incluido:** `scripts/gsc_oportunidades.py` procesa ese CSV (ver más abajo).
3. **Ahrefs MCP (PAGO, requiere proyecto con Search Console conectado):** `gsc-keywords`, `gsc-pages` y `gsc-page-history` traen las mismas consultas por URL y su evolución. `serp-overview` ayuda a leer qué rankea hoy.
4. **SerpApi MCP (GRATIS):** `mcp__serpapi__search` para ver si la SERP cambió de formato (guías, listados, fichas) y qué PAA aparecen.

Conexión de MCPs: ver `../../MCP-SETUP.md`.

## Proceso (pasos del diplomado)

### Paso 1. Elegir bien el candidato (S10 L1 y L2)
No elijas páginas al azar. Busca las que **ya tienen tracción**: existen, no están en las primeras posiciones y tienen una keyword con volumen en tu Plantilla Master. Identifica cuál de los 3 escenarios aplica: **contenido desactualizado**, **bajo rendimiento** (impresiones sin clics o página 2) o **cambio en la intención de búsqueda**. Anota por qué crees que necesita optimización.

### Paso 2. Deja que los datos hablen (S10 L2)
Con Search Console busca:
- **Keywords de umbral:** ya tienen impresiones pero no están en el Top 3.
- **Keywords secundarias:** consultas por las que la página aparece y que no están en el texto.
Decide si mantienes la keyword original o pasas a una con la que ya recibes impresiones. *"Optimiza hacia donde ya tienes tracción."*

### Paso 3. Revalida la intención en la SERP
Abre la SERP hoy. Si Google ahora premia otro formato (antes guías, ahora fichas), el problema no es el texto: es el tipo de página. El brief sigue dictándolo la SERP (S8 L3).

### Paso 4. Define el alcance y regístralo (S10 L2)
En la Plantilla Master, sección "Actualización de Contenido": márcala como "Actualización de Blog/Servicio", define el alcance (**cambio total, solo metadatos o expansión de texto**), prioridad y fecha de entrega.

### Paso 5. Regla de oro de la URL (S10 L4)
Si la página ya genera tráfico y clics, **no cambies la URL**. Solo si es irrelevante o "sucia", y entonces con **redirección 301** y actualizando los enlaces internos.

### Paso 6. Redacta el Brief de Optimización "Actual vs. Sugerido" (S10 L3 y L4)
Usa la plantilla. Incluye: diagnóstico, URL, meta título, meta descripción y H1 en dos columnas, keywords secundarias a incluir, URLs de competidores que ya rankean, nueva jerarquía H2/H3 y enlaces internos a añadir. Metas con los mismos rangos de siempre: título 50 a 60 con la keyword al inicio, descripción 120 a 155 con CTA.

### Paso 7. Aplica la variante por tipo de página (S10 L5, L6, L7)
- **Blog:** alinea con la intención informativa, reestructura la jerarquía, reemplaza datos obsoletos, redacta el Alt Text de las imágenes y aplica **Links From / Links To** con `site:tuweb.com "keyword"` para encontrar al menos 2 páginas propias desde donde enlazar. *"Un artículo aislado es un artículo invisible."*
- **E-commerce:** matriz **Impacto vs. Esfuerzo**. P1 (alto impacto, bajo esfuerzo): metas, descripciones y keywords con impresiones. P2: Schema y reseñas. P3: rediseño de imágenes o videos. Empieza por las **victorias rápidas** (capturar clics de página 2). Revisa keywords transaccionales, atributos y beneficios, prueba social existente, CTAs e información de envío y devoluciones.
- **Landing:** define el objetivo de conversión y decide entre **ajuste leve** (mover elementos, metas, enlaces) o **reestructuración profunda** (estructura nueva priorizando la propuesta de valor). Añade capturas como prueba (precios, demos, certificaciones).

### Paso 8. Documenta antes de tocar y pide feedback (S10 L8)
Completa el brief, vincúlalo en la Plantilla Master (G-Doc) y compártelo en la comunidad para recibir correcciones **antes de implementar**. Marca en el documento qué es viejo y qué es nuevo (modo sugerencia).

### Paso 9. Después de implementar
Registra la fecha del cambio y vuelve a Search Console con el mismo filtro para comparar. No inventes la mejora: usa datos reales del periodo posterior.

## Opcional: complementos externos

Después de seguir el método, puedes añadir las comprobaciones de [`references/complementos-claude-seo.md`](references/complementos-claude-seo.md): puntuación de brechas de la competencia, "ganancia de información", fecha visible de actualización y verificación de afirmaciones. Son un **Complemento externo (claude-seo, MIT), no es parte del método del diplomado**.

## Script determinista (ahorro de tokens)

```bash
python3 skills/actualizacion-de-contenido/scripts/gsc_oportunidades.py \
  --file consultas.csv --texto pagina-actual.txt --min-impresiones 10
```

Corre con `--help` para ver opciones. Devuelve por página: `keywords_umbral`, `ctr_bajo_vs_mediana`, `victorias_rapidas_pagina_2`, `secundarias_no_cubiertas_en_el_texto` y un `alcance_orientativo`. Los umbrales son heurísticas de trabajo (posición 4 a 20, mínimo de impresiones configurable, CTR comparado con la mediana del propio export), no cifras de Google. Solo stdlib. Sin Python, haz el análisis a mano en la hoja.

## Salida

```
BRIEF DE OPTIMIZACIÓN: [keyword] · Tipo: [Blog | E-commerce | Landing]
URL: [actual] · Decisión de URL: [se mantiene | cambia con 301 a ...]
Alcance: [solo metadatos | expansión | cambio total] · Prioridad: [P1-P3] · Fecha: [..]

DIAGNÓSTICO: [escenario: desactualizado / bajo rendimiento / cambio de intención] + dato de Search Console real
| Elemento          | Actual | Sugerido |
| Meta título       | ..     | .. (50-60c, keyword al inicio) |
| Meta descripción  | ..     | .. (120-155c, con CTA) |
| H1                | ..     | .. |
KEYWORDS SECUNDARIAS A INCLUIR: [consultas con impresiones que no están en el texto]
COMPETENCIA / INSPIRACIÓN: [URLs que rankean y qué les falta a nuestra página]
NUEVA ESTRUCTURA: H2/H3 [sin saltos de nivel]
ENLACES INTERNOS A AÑADIR: Links From / Links To con anchor y URL
CAMBIOS A REALIZAR (documentados antes de tocar) · QUÉ SE CONSERVA
MATRIZ IMPACTO/ESFUERZO (E-commerce): P1 / P2 / P3
```

Persiste el resultado en `.seo-audit/<sitio>/data/content-briefs.json` con `type: "optimizacion"`.

## Ejemplo

*Ilustrativo, no son datos reales de ningún sitio.*

**Página:** `/blog/cera-para-velas`, cluster Materiales, tipo Blog. Search Console (export real del usuario): "cera de soja para velas" con muchas impresiones y posición cercana a 9, CTR muy por debajo de la mediana de la página; 3 consultas secundarias que el texto no menciona.
- Alcance: expansión + metas. URL: se mantiene (ya recibe clics).
- Meta título actual 38 c, sugerido 57 c con "cera para velas" al inicio. Meta descripción con CTA dentro de 120 a 155.
- H2 nuevos solo para las consultas no cubiertas; se conserva la introducción y la sección de tipos de cera.
- Enlaces: `site:tuweb.com "cera de soja"` devuelve 2 artículos propios; se enlazan con anchor "cera de soja".

## Gotchas

- **No cambies la URL si ya tiene tráfico.** Si cambia, 301 y enlaces internos actualizados.
- **Documenta antes de tocar.** Un cambio sin brief no tiene trazabilidad y puede dañar el ranking actual.
- **No elijas por intuición:** sin datos de Search Console, la página no es candidata todavía.
- **No reescribas desde cero lo que ya rankea.** Núcleo intacto, periferia optimizada.
- **No cambies la keyword solo por volumen:** primero intención y SERP (práctica de coaches).
- **No inventes testimonios, reseñas ni cifras** para "mejorar" la prueba social: déjalos pendientes.
- **Mide después con el mismo filtro.** Sin comparación real no hay conclusión.
