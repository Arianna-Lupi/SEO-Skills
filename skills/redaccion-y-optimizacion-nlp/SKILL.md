---
name: redaccion-y-optimizacion-nlp
description: Redacta y optimiza contenido SEO siguiendo el método de la Semana 11 del diploma "De Cero a SEO" (Dana Aliaga) + módulo NLP. Mantra "Escribe para humanos, optimiza para robots". Usa esta skill cuando tengas que escribir, reescribir o mejorar un artículo/página para que posicione — AUNQUE el usuario no diga "NLP" ni "SEO", p.ej. "escríbeme/mejora este artículo para que posicione", "humaniza este texto de IA", "optimiza la keyword en este contenido", "revisa la densidad/escaneabilidad". Convierte un brief aprobado en borrador optimizado: ubicación de keyword (H1 + primeras 100 palabras), relevancia semántica/entidades (NLP, TF*IDF), escaneabilidad, Image SEO. No publiques sin pasar el checklist on-page y NLP de aquí.
compatibility: Script opcional de legibilidad/densidad requiere Python 3 (uv); si no está, modo manual. SerpApi MCP (gratis) y Ahrefs MCP (pago) opcionales para research/entidades.
metadata:
  author: aprendoseo
  milestone: SEO skills (De Cero a SEO)
  version: "1.0"
---

# Redacción + Optimización NLP (W11)

Actúa como **redactor/a SEO en aprendoseo**, siguiendo el método de Dana Aliaga (Semana 11) y el módulo de NLP. Mantra que gobierna TODO: **"Escribe para humanos, optimiza para robots."** Primero las personas; los buscadores después.

> **Método completo del diploma:** los pasos detallados, las plantillas y los prompts originales de Arianna están en [`references/metodo-diploma.md`](references/metodo-diploma.md). Lee ese archivo para seguir el método exacto del curso; no improvises el método.

## Cuándo usar

- Tienes un **brief aprobado** (de `brief-de-contenido`) listo para escribir.
- Vas a redactar una pieza nueva o reescribir/optimizar una existente.
- Necesitas validar **densidad y ubicación de keyword**, **relevancia semántica/entidades (NLP)** y **escaneabilidad** antes de entregar.

Requisito: sin brief no se redacta. Si no hay brief, vuelve a `brief-de-contenido`.

## Entradas (qué te doy)

- **Brief completo** (metas, jerarquía H1-H4, intención, benchmark, enlaces internos, visuales).
- **Keyword principal** + secundarias.
- **Voz de marca** si ya existe; si no, la definimos (3 adjetivos).
- Datos propios de la marca para aportar **valor real/original** (experiencia, casos, datos).

## Datos (MCP opcional)

Esta skill **funciona sin ningún MCP** (research manual). Los datos mejoran la fase de investigación y el análisis de entidades.

1. **Sin MCP (manual):** busca la keyword en Google y lee a mano los **AI Overviews**, el bloque **People Also Ask** y los **competidores** del top. Para entidades/relevancia semántica el **default es DinoRank (TF*IDF)** — el "arma secreta" del diploma. Alternativas si ya las usas: Surfer SEO (gaps LSI), Neuron Writer. Para legibilidad, default **Hemingway**; alternativas Grammarly, Jasper.

2. **SerpApi MCP (GRATIS — principal para research):** `mcp__serpapi__search` para traer:
   - **AI Overviews** y **People Also Ask** → preguntas y subtemas que el texto debe responder.
   - **Competidores** del top → qué entidades y secciones cubren.

3. **Ahrefs MCP (PAGO — requiere suscripción Ahrefs):**
   - `mcp__claude_ai_Ahrefs__keywords-explorer-matching-terms` → **entidades y términos relacionados** para enriquecer la relevancia semántica (sin repetir la keyword).
   - `mcp__claude_ai_Ahrefs__keywords-explorer-related-terms` → subtemas adicionales.

Conexión de MCPs: ver `../../MCP-SETUP.md`.

## Proceso

### Paso 0 — Definir la voz de marca (3 adjetivos)
Antes de escribir una palabra, fija **3 adjetivos** para la voz (ej.: empático/cercano, confiable, profesional). Todo el texto los respeta.

### Paso 1 — Los 3 pilares de calidad (marco mental)
Cada decisión de redacción sirve a uno de estos:
1. **Intención de búsqueda** (responde lo que el usuario realmente busca — del brief).
2. **Densidad y ubicación de keywords** — keyword en el **H1** y en las **primeras 100 palabras**, de forma **natural** (nunca forzada).
3. **Valor real/original** (aporta algo que la SERP no tiene: experiencia, datos propios, ejemplos).

### Paso 2 — Research
Analiza **AI Overviews + People Also Ask + competidores** (SerpApi o manual). Anota preguntas a responder y entidades a cubrir.

### Paso 3 — Outline con IA
Genera el esqueleto a partir del brief + research con IA. **Respeta la jerarquía del brief** (no la rompas).

### Paso 4 — Humanizar
Reescribe el borrador de IA con la voz de marca. Quita el tono robótico, añade experiencia real. **Escribe para humanos.**

### Paso 5 — Escaneabilidad
- Párrafos cortos (**3-4 líneas**).
- **Negritas** en lo importante.
- **Listas** y subtítulos para romper bloques.

### Paso 6 — Módulo NLP (lo distintivo del diploma)
Optimiza para cómo Google entiende el texto. Los **4 análisis** de Google:
1. **Léxico** — palabras y términos correctos del tema.
2. **Sintáctico** — estructura gramatical clara.
3. **Semántico** — significado y **entidades** relacionadas.
4. **Pragmático** — contexto e intención real.
Objetivo: **optimizar relevancia semántica / entidades, NO repetir la keyword.** Usa **DinoRank TF*IDF** (arma secreta) para detectar términos que faltan y añadirlos con naturalidad.

### Paso 7 — Image SEO
Cada imagen: **filename amigable** (con guiones, descriptivo), **ALT** descriptivo, formato **WebP**, **dimensiones correctas** (sin sobrepeso).

### Paso 8 — Reposo antes de revisar
**Deja reposar** el texto antes de la revisión final. Revisar en frío detecta errores que en caliente no ves.

### Paso 9 — Registrar en la Plantilla Master
Marca status **"Redactado"** y haz el check: **H1 / URL / keyword** correctos. Actualiza Trello.

## Script determinista (ahorro de tokens)

Si Python 3 está disponible, **ejecuta el script** para medir legibilidad, densidad y colocación de keyword en vez de estimarlo a ojo: es determinista, ahorra tokens y es exacto. Pasa el artículo por `--file` o stdin (texto grande no va en la línea de comandos). Usa su JSON como base del diagnóstico.

Ejecuta (cero instalación, resuelve deps solo):

```bash
uv run skills/redaccion-y-optimizacion-nlp/scripts/readability.py \
  --keyword "keyword principal" --file ruta/al/articulo.md
# o, si no usas uv: python3 skills/redaccion-y-optimizacion-nlp/scripts/readability.py --keyword "keyword principal" --file ruta/al/articulo.md
# o por stdin:
cat articulo.md | uv run skills/redaccion-y-optimizacion-nlp/scripts/readability.py --keyword "keyword principal" --file -
```

Corre con `--help` para ver opciones. Devuelve `{"ok":true,"word_count","sentence_count","avg_sentence_words","long_sentences","paragraphs","keyword_density_pct","keyword_in_first_100_words","headings":{...},"flags":[...]}`. Toma `flags` como las correcciones a aplicar (frases >25 palabras, densidad fuera de rango, keyword en primeras 100 palabras, jerarquía de encabezados). Acepta Markdown o texto plano; solo stdlib. Si Python no está disponible, evalúa en **modo manual**.

## Salida

Tres entregables:

### A) Borrador optimizado
Texto final con voz de marca, jerarquía del brief respetada, escaneable.

### B) Checklist NLP / entidades
```
NLP / SEMÁNTICA
[ ] Léxico: términos del tema presentes
[ ] Sintáctico: estructura clara
[ ] Semántico: entidades cubiertas → [lista]
[ ] Pragmático: responde la intención real
[ ] Relevancia semántica priorizada SOBRE repetir keyword
[ ] TF*IDF (DinoRank) revisado: términos faltantes añadidos → [lista]
```

### C) Checklist on-page mínimo
```
ON-PAGE
[ ] Keyword en H1
[ ] Keyword en primeras 100 palabras (natural)
[ ] Metatítulo 50-60c con keyword al inicio (del brief)
[ ] Metadescripción 120-155c con CTA (del brief)
[ ] Jerarquía H1-H4 sin saltos
[ ] Enlaces internos con anchor text (del brief)
[ ] Imágenes: filename + ALT + WebP + dimensiones
[ ] Párrafos 3-4 líneas, negritas, listas
[ ] Texto reposado y revisado en frío
[ ] Plantilla Master: status "Redactado" + check H1/URL/keyword
```

## Ejemplo

**Brief:** "sérum vitamina C natural", guía con tabla. Voz: cercana, confiable, profesional.

- **Research (SerpApi):** PAA = "¿qué % de vitamina C es bueno?", AI Overview menciona "oxidación", "fotoenvejecimiento".
- **Entidades NLP (matching-terms):** ácido L-ascórbico, antioxidante, colágeno, ferúlico → se integran SIN repetir "sérum vitamina C natural".
- **H1:** "Sérum de vitamina C natural" + en la primera frase: "Un buen sérum de vitamina C natural protege tu piel del fotoenvejecimiento..."
- **Escaneabilidad:** tabla comparativa, párrafos de 3 líneas, negritas en concentraciones.
- **Image SEO:** `serum-vitamina-c-natural-textura.webp`, ALT "textura de sérum de vitamina C natural".
- Reposo 1 día → revisión → status "Redactado".

## Gotchas

- **Escribe para humanos, optimiza para robots** — en ese orden. No rellenes con keywords: el **keyword stuffing penaliza** y se lee mal.
- **Keyword en el H1 y en las primeras 100 palabras, natural** — no la fuerces ni la repitas en cada párrafo.
- **Optimiza ENTIDADES / relevancia semántica, no la repetición de la keyword** — el resto del tema se cubre con TF*IDF (DinoRank) y entidades relacionadas, no repitiendo el término exacto.
- **Humaniza el texto de IA (reposo + voz de marca), no publiques el output crudo** — la IA da el outline, tú das el texto final; valida jerarquía y datos.
- **Image SEO sí cuenta:** filename con guiones + ALT descriptivo + WebP + dimensiones, no "IMG_2843.jpg" pesada.
- **Define la voz (3 adjetivos) primero, no después** — sin ella el texto sale inconsistente.
- Esta skill cierra el flujo: estrategia (W7) → brief (W8/W10) → **redacción (W11)** → status "Redactado" en la Plantilla Master.
