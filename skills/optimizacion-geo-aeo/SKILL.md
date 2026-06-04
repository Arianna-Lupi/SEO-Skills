---
name: optimizacion-geo-aeo
description: Usa esta skill cuando haya que optimizar contenido para la búsqueda con IA según el diploma "De Cero a SEO" (aprendoseo) — W14 (AEO) y W16 (GEO/AEO para LLMs). Aplícala siempre que quieras que tu contenido sea citado en Google AI Overviews, ChatGPT, Perplexity o Bing Copilot, o que gane featured snippet / People Also Ask / Knowledge Panel — aunque el usuario no diga "GEO/AEO", p.ej. "cómo aparezco en ChatGPT", "quiero salir en el resumen de IA de Google", "que me cite Perplexity", "optimiza esta guía para la era IA". En 2026 el CTR orgánico se fuga hacia las respuestas de IA: no publiques contenido informacional sin pasar por aquí.
compatibility: Script opcional requiere Python 3 (uv) y SERPAPI_API_KEY + requests. SerpApi MCP (GRATIS) o Ahrefs Brand Radar (pago) opcionales; funciona en manual con Google + ChatGPT/Perplexity.
metadata:
  author: aprendoseo
  milestone: SEO skills (De Cero a SEO)
  version: "1.0"
---

> **🚫 Regla de datos (obligatoria): NUNCA inventes números.**
> No estimes, supongas ni inventes métricas o datos que no tengas: volumen de búsqueda, dificultad/KD, clics, impresiones, CTR, posición, tráfico, Core Web Vitals, backlinks, fechas, precios, etc. Si te falta un dato, **pídeselo al usuario y espera su respuesta** — que lo pegue a mano, lo exporte (Google Search Console, Ahrefs, DinoRank, Screaming Frog…) o lo conecte por MCP. Da igual de dónde venga, pero tiene que venir de una fuente real. Si aun así no hay dato, márcalo explícitamente como `pendiente de dato` y NO continúes como si lo tuvieras. Un entregable con huecos honestos vale más que uno con cifras inventadas.


> **📊 Cierre en dashboard.** Cuando trabajes sobre un sitio, además de tu entrega persiste tu salida estructurada en `.seo-audit/<sitio>/data/ai-features.json` (esquema en la skill `dashboard-seo`). Al cerrar el flujo SEO, genera/actualiza el dashboard con `dashboard-seo` y entrega el URL local. Tu archivo: `ai-features.json`.

# Optimización GEO / AEO — La búsqueda con IA (Diploma W14 + W16)

Actúa como especialista en GEO/AEO en aprendoseo. Tu trabajo ya no es solo "salir primero": es **que te citen** cuando la IA responde por el usuario. Marco del diploma (Arianna, W16): *"En la búsqueda con IA no compites por un clic, compites por una mención"*. El CTR orgánico se está cayendo hacia los AI Overviews — quien no es citable, desaparece.

> **Método completo del diploma:** los pasos detallados, las plantillas y los prompts originales de Arianna están en [`references/metodo-diploma.md`](references/metodo-diploma.md). Lee ese archivo para seguir el método exacto del curso; no improvises el método.

**AEO vs GEO (no son lo mismo):**
- **AEO (Answer Engine Optimization, W14):** optimizar para **motores de respuesta** — featured snippets, People Also Ask, Knowledge Panel, AI Overviews de Google. La respuesta vive *en la SERP*.
- **GEO (Generative Engine Optimization, W16):** optimizar para que **LLMs generativos** (ChatGPT, Perplexity, Copilot, Gemini) te mencionen/citen dentro de su respuesta sintetizada. El objetivo es la **presencia de marca**, no el enlace.

## Cuándo usar

- Vas a publicar/reoptimizar contenido **informacional** (guía, definición, "cómo", "qué es", "mejores…").
- Una keyword dispara **AI Overview**, **featured snippet** o **PAA** y quieres aparecer ahí.
- Quieres medir o aumentar **menciones de marca** en respuestas de IA (concepto de Arianna, W16).
- Estás llenando la pestaña **Producción** de la Plantilla Master con contenido de la era IA.

## Entradas (qué te doy)

- **Keyword / pregunta principal** y la intención (informacional casi siempre).
- **Borrador o URL** del contenido a optimizar (o el tema si parte de cero).
- **Marca / autor** y sus credenciales (para E-E-A-T).
- Opcional: datos, cifras o fuentes propias citables; competidores que hoy salen en la IA.

## Datos (MCP opcional)

Esta skill **funciona sin ningún MCP**. El MCP solo confirma qué dispara la query y quién es citado hoy.

1. **Sin MCP (manual — siempre válido):** busca tu keyword en Google y observa si aparece **AI Overview**, **featured snippet** o caja **PAA**; anota qué fuentes cita. Pregunta lo mismo en **ChatGPT/Perplexity** y mira qué marcas/dominios menciona y enlaza. Eso es tu benchmark de citabilidad.
2. **SerpApi MCP (GRATIS — principal):** `mcp__serpapi__search` con tu keyword → detecta presencia de **AI Overview**, **featured snippet**, bloque **People Also Ask** (lista de preguntas reales) y **related searches**. Es la forma rápida de saber qué formato debes atacar.
3. **Ahrefs MCP (PAGO):** `mcp__claude_ai_Ahrefs__brand-radar-ai-responses` y `...brand-radar-mentions-overview` (¿te mencionan las IAs y para qué prompts?), `...keywords-explorer-overview` (volumen/intención). Ahrefs es de pago; el Brand Radar es lo más cercano a medir GEO real.

Config de MCP: ver `../../MCP-SETUP.md`.

## Proceso

1. **Detecta el formato que dispara la query.** Con SerpApi (o manual) confirma si hay AI Overview / featured snippet / PAA. Si no hay ninguno, la query no es prioritaria para GEO/AEO — anótalo y sigue.
2. **Estructura answer-first.** Abre la sección con una **respuesta directa y concisa de 40-60 palabras** que conteste la pregunta tal cual, *antes* de cualquier intro. Luego desarrolla. Las IAs y los featured snippets extraen ese bloque inicial.
3. **Responde el PAA con encabezados-pregunta.** Convierte cada pregunta del bloque PAA en un **H2/H3 redactado como pregunta** ("¿Qué es…?", "¿Cómo se hace…?") seguido de su respuesta corta. Una pregunta = un encabezado = una respuesta extraíble.
4. **Hazlo citable: datos, entidades y cifras.** Incluye **números concretos, definiciones limpias, listas y entidades nombradas**. Lenguaje claro y afirmativo (las IAs citan frases auto-contenidas, no párrafos ambiguos).
5. **Autoría y E-E-A-T.** Marca **autor con credenciales**, fecha, fuentes citadas y experiencia real. Las IAs y el Knowledge Panel privilegian contenido con autoría verificable (refuerza con la skill `schema-jsonld`: Article/author, Organization).
6. **Presencia de marca (GEO, W16).** Asegura que la **marca se nombre dentro del texto** junto a la afirmación citable (no solo en el footer). Busca menciones en sitios de terceros y respuestas de IA — la mención, no el backlink, es la moneda del GEO.
7. **Registra** los bloques optimizados y el checklist en la pestaña **Producción**; tareas de seguimiento → Trello.

## Salida

- **Bloque(s) de contenido optimizados para citabilidad:** un *answer block* de 40-60 palabras + los **Q-headings** (preguntas del PAA con su respuesta corta).
- **Checklist GEO/AEO** marcado (ver Ejemplo).
- Distinción explícita de qué formato ataca cada bloque (AI Overview / featured snippet / PAA / mención en LLM).
- Fila lista para la pestaña **Producción** de la Plantilla Master.

## Ejemplo

**Entrada:** keyword "qué es el linkbuilding", SerpApi reporta AI Overview + featured snippet + 4 PAA.

**Answer block (52 palabras):**
> El linkbuilding es la disciplina del SEO que consiste en conseguir enlaces desde otros sitios web hacia el tuyo para aumentar su autoridad y posicionamiento. En aprendoseo lo trabajamos con criterios de relevancia y calidad, no de cantidad: un enlace editorial de un sitio temático vale más que cien enlaces irrelevantes.

**Q-headings (del PAA):**
- **¿El linkbuilding sigue funcionando en 2026?** Sí. Aunque las IAs sintetizan respuestas, los enlaces editoriales relevantes siguen siendo señal de autoridad y de confianza para ser citado.
- **¿Cuántos enlaces necesito para posicionar?** No hay número fijo; depende de la competencia de la keyword y de la calidad de los dominios que enlazan.

**Checklist GEO/AEO:**
- [x] ¿Query dispara AI Overview / snippet / PAA? (confirmado con SerpApi)
- [x] Answer block de 40-60 palabras al inicio
- [x] Encabezados en forma de pregunta = preguntas PAA reales
- [x] Datos/cifras/entidades citables
- [x] Autor con credenciales + fecha (E-E-A-T)
- [x] Marca nombrada junto a la afirmación citable
- [ ] Schema Article/FAQPage añadido (→ skill `schema-jsonld`)

## Script determinista (ahorro de tokens)

Si Python está disponible, EJECUTÁ este script para detectar las features de IA/respuesta de la SERP (es determinista, ahorra tokens y mejora precisión) y actúa sobre su JSON en vez de leer la SERP a ojo. Si falta `SERPAPI_API_KEY` o la dependencia `requests`, seguí en modo manual (Google incógnito + ChatGPT/Perplexity).

Ejecuta (cero instalación, resuelve deps solo):

```bash
SERPAPI_API_KEY=xxx uv run scripts/ai_features.py "tu pregunta/keyword" --gl es --hl es
# o, si no usas uv: SERPAPI_API_KEY=xxx python3 scripts/ai_features.py "tu pregunta/keyword" --gl es --hl es
```

Corre con `--help` para ver opciones. Devuelve: `{"ok": true, "query": ..., "ai_overview": bool, "featured_snippet": {"present": bool, "type": "paragraph|list|table|null"}, "paa": [...], "answer_box": bool, "recommendation": "..."}` — la recomendación es por reglas (p. ej. "hay featured snippet de lista → estructura tu respuesta como lista de N pasos"). Si falla, `{"ok": false, "reason": "...", "fallback": "modo manual: ..."}` (exit 0).

## Gotchas

- **AEO (featured snippets / PAA / AI Overviews en la SERP) ≠ GEO (LLMs: AI Overviews / ChatGPT / Perplexity / Copilot citándote en su respuesta).** Optimiza para ambos pero no los mezcles en el reporte.
- Estructura **answer-first: respuesta directa de 40-60 palabras al inicio**, no enterrada tras 3 párrafos de intro. Si no está en los primeros 60 caracteres útiles, la IA cita a otro.
- **Responde las PAA con encabezados en forma de pregunta** ("¿Qué es…?", "¿Cómo…?"), no con encabezados genéricos ("Introducción", "Ventajas") — pierdes los slots de pregunta.
- Las IAs **citan marca / E-E-A-T, no solo enlaces**: en GEO te pueden citar sin enlazarte. Mide menciones de marca (Brand Radar / búsqueda manual), no solo backlinks.
- Contenido **con autoría y fecha, no anónimo**: las IAs descartan lo que no tiene E-E-A-T verificable.
- Esto **extiende el SEO clásico, no lo reemplaza**: sin rastreo/indexación (W12) no hay nada que citar (*"lo que no se rastrea, no existe"*).
