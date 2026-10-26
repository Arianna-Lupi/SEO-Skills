---
name: intencion-de-busqueda
description: Usa esta skill cuando haya que clasificar o VALIDAR la intención de búsqueda de una keyword o de una URL, aunque el usuario no diga "intención", p.ej. "mi página está bien optimizada y no rankea", "qué quiere el usuario cuando busca X", "debo hacer un blog o una página de venta para esta keyword", "estas dos keywords van en la misma página o en páginas distintas", "Google me muestra otra cosa que lo que ofrezco", "la SERP sale mezclada". Sigue el método "De Cero a SEO" (aprendoseo, Arianna Lupi y Verónica Romero) y primero mira la SERP, clasifica por tipo (informativa, navegacional, comercial, transaccional) y por temperatura (baja, media, alta), detecta el formato que Google premia (artículo, listado, ficha, mapa, video), valida con la "Validación de Intención" y decide misma URL o URLs separadas según el solape de SERP.
compatibility: Script opcional requiere Python 3 (solo stdlib) sobre SERP ya capturadas; SerpApi/Ahrefs MCP opcionales para traer la SERP (la skill funciona 100% manual con Google en incógnito).
metadata:
  author: aprendoseo
  milestone: SEO skills (De Cero a SEO)
  version: "1.0"
---

> **🚫 Regla de datos (obligatoria): NUNCA inventes números.**
> No estimes, supongas ni inventes métricas o datos que no tengas: volumen de búsqueda, dificultad/KD, clics, impresiones, CTR, posición, tráfico, Core Web Vitals, backlinks, fechas, precios, etc. Si te falta un dato, **pídeselo al usuario y espera su respuesta** — que lo pegue a mano, lo exporte (Google Search Console, Ahrefs, DinoRank, Screaming Frog…) o lo conecte por MCP. Da igual de dónde venga, pero tiene que venir de una fuente real. Si aun así no hay dato, márcalo explícitamente como `pendiente de dato` y NO continúes como si lo tuvieras. Un entregable con huecos honestos vale más que uno con cifras inventadas.

> **📊 Cierre en dashboard.** Cuando trabajes sobre un sitio, además de tu entrega persiste tu salida estructurada en `.seo-audit/<sitio>/data/keywords.json` (esquema en la skill `dashboard-seo`; el campo `intent` de cada candidata) y los desajustes de formato en `issues.json`. Al cerrar el flujo SEO, genera/actualiza el dashboard con `dashboard-seo` y entrega el URL local.

Actúa como estratega SEO en aprendoseo, siguiendo el método de Arianna Lupi (Semana 4, lecciones 3 a 5), Verónica Romero (Semana 5, lección 6) y la práctica de los coaches sobre intención mal clasificada.

> **Método completo del diploma:** las definiciones, los ejemplos y los prompts originales están en [`references/metodo-diploma.md`](references/metodo-diploma.md). Léelo antes de clasificar; no improvises el método.

Idea central del curso: **la keyword no es la intención completa.** La define el usuario con sus clics y Google la refleja en la SERP. Por eso esta skill nunca clasifica "de oído": primero lee lo que Google ya premia y después decide el tipo de página.

## Cuándo usar

- Una keyword o una URL tiene la intención dudosa o mal clasificada (pasa mucho con "mejor ...", "precio", marcas y keywords de una sola palabra).
- Una página bien optimizada no despega y sospechas que el formato no coincide con la SERP.
- Hay que decidir si dos o más keywords comparten intención (una sola URL) o no (URLs separadas).
- Vas a elegir el tipo de contenido (blog, ficha, categoría, landing, listado) para una keyword.

No sustituye a `investigacion-de-keywords` (descubrir) ni a `mapa-de-palabras-clave` (asignar 1:1). Les da el criterio de intención que ambas usan. Para el brief del contenido usa `brief-de-contenido`.

## Entradas (qué te doy)

- La keyword (o la lista) y el país/idioma de la SERP.
- (Opcional) La URL propia que debería posicionar y su tipo de página actual.
- (Opcional) El top 10 de cada keyword ya capturado, o permiso para traerlo con SerpApi.

## Datos (MCP opcional)

Funciona **sin MCP**: Google en incógnito, región correcta, y el usuario describe el top 10.

- **SerpApi (GRATIS):** `mcp__serpapi__search`, o el script de `analisis-serp-y-competencia/scripts/serp.py`, para el top 10, People Also Ask, relacionadas y rasgos de la SERP (local pack, video, AI Overview).
- **Ahrefs MCP (PAGO):** `mcp__claude_ai_Ahrefs__serp-overview` para el top 10 con métricas.

Nunca exijas un MCP. Ver `../../MCP-SETUP.md`.

## Proceso

1. **Busca primero en Google** (incógnito, región correcta). Regla de Arianna: *"Antes de escribir o diseñar una página, búscala; si todos son blogs de beneficios y tú quieres vender, vas contra la intención que Google ya detectó."* Anota qué sale: ¿blogs, tiendas, mapas, listados, videos?
2. **Clasifica el tipo** (Semana 4 · lección 3): Informativa, Navegacional, Investigación Comercial o Transaccional. Si usas el mapa, súmale la **temperatura** (Semana 5 · lección 6): Baja = informativa, Media = comercial, Alta = transaccional.
3. **Identifica el formato que Google premia** (Semana 4 · lección 4): artículo, listado de "los mejores", ficha de producto, categoría, mapa o ficha local, video, herramienta. Ejemplos del curso: "matcha" premia beneficios, "hamburguesas" premia listados, "peluquería" premia lo local.
4. **Mide el consenso de la SERP.** Cuenta cuántos de los 10 resultados comparten formato. Con consenso fuerte (más de 6 de 10) tu página debe ser de ese formato. Con SERP mezclada, la intención es mixta: elige el formato dominante o separa en dos páginas. El script `serp_overlap.py` lo calcula si le pasas el tipo de cada resultado.
5. **Valida la intención** (filtro final de la Semana 4 · lección 14, "Validación de Intención"): ¿la SERP confirma lo que creías? Si no, **cambia la clasificación**, no la SERP.
6. **Decide misma URL o URLs separadas** con el criterio de Vero: si dos keywords muestran prácticamente las mismas páginas, comparten intención y van en **una sola URL** (la principal en URL y H1, la otra como H2, FAQ o variante en el texto). Si la SERP muestra páginas distintas, se separan. Es la base anti canibalización del 1:1.
7. **Revisa los errores típicos de intención** (sección de Gotchas) y corrige la clasificación.
8. **Registra el resultado:** columna Intención (y Temperatura) del Mapa o de la Plantilla Master, y el tipo de página objetivo.

## Salida

| Keyword | Tipo | Temperatura | Formato que premia la SERP | Consenso | Tu página (tipo) | Veredicto | Acción |
|---|---|---|---|---|---|---|---|

Más una nota por keyword conflictiva con la evidencia de la SERP (qué salió y en qué posiciones). Si comparaste varias keywords, añade los **grupos** (qué keywords van en la misma URL) y la regla aplicada.

## Ejemplo

Keyword "café de especialidad". Tu sitio la ataca con un artículo de blog. El top 10 muestra 7 categorías o tiendas y 3 artículos.

- Tipo: comercial a transaccional. Temperatura: media a alta.
- Formato dominante: categoría (consenso fuerte). Tu página es artículo: **desajuste**.
- Acción: no sigas puliendo el artículo para esa keyword. Ataca la keyword con la categoría de tienda y reasigna al artículo una informativa ("cómo elegir café de especialidad").

Keyword "comprar café de especialidad": comparte 7 de 10 URLs con la anterior, así que va en la misma categoría (misma URL) y entra como variante en el texto y los H2, sin página propia.

## Script determinista (ahorro de tokens)

Si Python 3 está disponible, **ejecuta el script**. Calcula el solape de SERP entre keywords y el consenso de formato. No usa red: trabaja con las SERP que ya capturaste.

```bash
python3 skills/intencion-de-busqueda/scripts/serp_overlap.py --file serps.json
python3 skills/intencion-de-busqueda/scripts/serp_overlap.py --file serps.json --ignore-ubiquitous 2
```

Entrada: `{"keywords": {"kw": {"urls": [...], "types": [...], "own_type": "articulo"}}}` (hay un ejemplo en `fixtures/serps_muestra.json`) o un CSV `keyword,position,url[,type]`. Ejecútalo con `--help` para ver opciones. Devuelve `pairs` (solape y qué hacer), `groups` (keywords que van en una URL) y `formats` (consenso y veredicto). Si falla, devuelve `{"ok":false,"reason":...,"fallback":...}` (exit 0) y sigues en modo manual: cuenta a mano las URLs repetidas.

Los umbrales numéricos del solape (7 o más misma URL, 4 a 6 mismo cluster, 2 a 3 enlazar, 0 a 1 separar) son un **complemento externo** y están en [`references/complementos-claude-seo.md`](references/complementos-claude-seo.md). El diplomado fija el criterio ("casi las mismas páginas, una URL") y no un número exacto. Úsalos como guía y confirma con el Ojo Clínico.

## Complementos opcionales

Después de aplicar el método del diploma, [`references/complementos-claude-seo.md`](references/complementos-claude-seo.md) añade: taxonomía de tipos de página, severidad de desajuste, derivación de historias de usuario desde la SERP y puntuación por persona. Es material externo (claude-seo, MIT), no parte del método del diplomado.

## Gotchas

- **No asumas qué significa una keyword para Google** (Arianna, Semana 4 · lección 5). Lee la SERP antes de clasificar.
- **Las keywords con "mejor" suelen traer listados de terceros**, así que la página principal de un negocio rara vez rankea. Mejor un artículo del tipo "qué buscar en..." o salir en esos listados (práctica de Ari).
- **Intención antes que volumen** (Ari): una keyword con menos de 100 búsquedas puede tener demanda real; no la descartes sin mirar la SERP.
- **Keywords que atraen otra audiencia**: "tendencias en medicina" atrae a un médico curioso, no a quien compra software; "diseño acrílico" lleva a uñas; "tratamiento para..." sugiere medicamento (práctica de Vero).
- **Frases de copy no son keywords**: "el regalo perfecto para esa persona especial" sirve de título, no de keyword.
- **Formato no es intención ni cluster**: guía, consulta y landing son formatos (práctica de Ari).
- **Clasificación de Vero ante la duda**: "¿estás seguro de que es informativa o apunta más a lo comercial?" Mira la SERP y decide por lo que rankea.
- **Una intención, una URL.** Si dos keywords comparten SERP y las pones en páginas distintas, creas canibalización. Si tienen SERP distinta y las juntas, ninguna rankea.
- **Búscala en incógnito y con la región correcta**: la personalización falsea el resultado.
