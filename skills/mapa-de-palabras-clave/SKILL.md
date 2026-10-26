---
name: mapa-de-palabras-clave
description: "Usa esta skill cuando el usuario YA tenga un sitio con URLs y quiera asignarles keywords, mapear palabras clave a sus páginas, detectar canibalización o priorizar qué páginas optimizar, aunque no diga \"mapa\" ni \"canibalización\", p.ej. \"tengo varias páginas peleando por lo mismo\", \"qué keyword le pongo a cada URL\", \"cuáles páginas optimizo primero\", \"qué páginas de mi web actualizo\". Construye el Mapa de Palabras Clave del método \"De Cero a SEO\" (aprendoseo, Verónica Romero): inventaria todas las URLs, evalúa su Valor SEO, asigna UNA keyword primaria por URL (1:1) para evitar canibalización, clasifica intención por temperatura y define el plan de acción y el Top 5 de quick wins."
compatibility: Scripts opcionales requieren Python 3 (uv), solo stdlib. SerpApi/Ahrefs MCP y skill inventario-de-urls opcionales (la skill funciona 100% manual).
metadata:
  author: aprendoseo
  milestone: SEO skills (De Cero a SEO)
  version: "1.1"
---

> **🚫 Regla de datos (obligatoria): NUNCA inventes números.**
> No estimes, supongas ni inventes métricas o datos que no tengas: volumen de búsqueda, dificultad/KD, clics, impresiones, CTR, posición, tráfico, Core Web Vitals, backlinks, fechas, precios, etc. Si te falta un dato, **pídeselo al usuario y espera su respuesta** — que lo pegue a mano, lo exporte (Google Search Console, Ahrefs, DinoRank, Screaming Frog…) o lo conecte por MCP. Da igual de dónde venga, pero tiene que venir de una fuente real. Si aun así no hay dato, márcalo explícitamente como `pendiente de dato` y NO continúes como si lo tuvieras. Un entregable con huecos honestos vale más que uno con cifras inventadas.

> **📊 Cierre en dashboard.** Cuando trabajes sobre un sitio, además de tu entrega persiste tu salida estructurada en `.seo-audit/<sitio>/data/next-steps.json` (esquema en la skill `dashboard-seo`). Al cerrar el flujo SEO, genera/actualiza el dashboard con `dashboard-seo` y entrega el URL local. Tu archivo: `next-steps.json` (quick wins) y/o `keywords.json`.


Actúa como especialista en arquitectura de keywords en aprendoseo, siguiendo el método de Verónica Romero (Semana 5 del diploma "De Cero a SEO").

> **Método completo del diploma:** los pasos detallados, las plantillas y los prompts originales de Verónica están en [`references/metodo-diploma.md`](references/metodo-diploma.md). Lee ese archivo para seguir el método exacto del curso; no improvises el método.

## Cuándo usar

- El usuario YA tiene un sitio con URLs y quiere asignarles keywords.
- Sospecha de **canibalización** (varias URLs compitiendo por lo mismo).
- Quiere decidir qué páginas actualizar, eliminar/redireccionar o mantener.
- Necesita un **Top 5** de quick wins priorizado.

Si todavía no tiene keywords descubiertas, usa primero `investigacion-de-keywords`. Para competidores/SERP, usa `analisis-serp-y-competencia`.

## Entradas (qué te doy)

- Lista de URLs del sitio (o el dominio + acceso a sitemap/Screaming Frog).
- Lista de keywords candidatas (idealmente de la tab "Investigación de palabras clave").
- (Opcional) Posición actual, volumen y dificultad por keyword/URL.

## Datos (MCP opcional)

Funciona **sin MCP**. Fallback manual: el usuario exporta URLs con Screaming Frog (≤500 URLs gratis) o desde el sitemap, y pega volumen/dificultad/posición desde DinoRank o GSC; tú razonas Valor SEO, asignación 1:1 y plan de acción.

- **SerpApi MCP (GRATIS):** `mcp__serpapi__search` para verificar qué URL del sitio rankea hoy por una keyword (detecta canibalización real) y confirmar la SERP/intención.
- **Ahrefs MCP (PAGO):** `mcp__claude_ai_Ahrefs__site-explorer-organic-keywords` y `...-top-pages` (qué keywords/posiciones tiene cada URL), `...-keywords-explorer-overview` (volumen/KD), y **GSC** `mcp__claude_ai_Ahrefs__gsc-keywords` / `gsc-pages` (posición real propia). Ideal para llenar Posición actual y Volumen.

**Inventario de URLs (opcional, automático):** si el usuario no pasó el export de URLs, usa la skill `inventario-de-urls` para extraerlas, por **sitemap (cero instalación)** o con **Screaming Frog CLI (GRATIS hasta 500 URLs; licencia solo para >500 URLs / config guardada / render JS / scheduling / API)**, y alimenta con ellas el mapa.

Nunca exijas un MCP. Ver `../../MCP-SETUP.md`.

## Proceso

1. **Inventariar TODAS las URLs** del sitio (Screaming Frog ≤500 free o sitemap) → tab "Mapa de Palabras Clave". Práctica de Vero: rastrea el **dominio en modo Spider**, no el sitemap; si el sitemap es un índice, carga cada archivo por separado; **filtra a URLs de contenido** (fuera imágenes y archivos). En un proyecto real analiza todas; en un ejercicio basta un subconjunto.
2. **Evaluar el Valor SEO** de cada URL con la pregunta test:
> **"¿Un usuario buscaría esto en Google?"**
   - **CON valor (Sí):** páginas de servicios, blog, categorías de producto.
   - **SIN valor (No):** legales, política de privacidad, página de autor, carpetas, etiquetas, gracias/checkout. Marca Valor SEO = **Sí / No**. Las "No" no reciben keyword.
3. **Asignar UNA keyword primaria por URL (1:1).** Una keyword no puede repetirse en dos URLs → así se evita la **canibalización**. Valida con Google que lo que rankea coincide con lo que ofreces. Si dos keywords muestran casi las mismas páginas en la SERP, comparten intención: una sola URL, la secundaria va como H2, FAQ o variante en el texto (criterio de Vero; usa la skill `intencion-de-busqueda`). Si la SERP muestra páginas distintas, se separan.
4. **Clasificar intención por temperatura:**
   - **Baja** = informativa.
   - **Media** = comercial.
   - **Alta** = transaccional.
5. **Traer datos por URL:** Volumen, Dificultad, Posición actual.
6. **Plan de acción por URL:**
   - **Actualizar/Optimizar** (la URL existe pero puede rankear mejor).
   - **Eliminar/Redireccionar** (sin valor o canibaliza).
   - **Mantener** (solo si ya está en **top 3**; no la toques).
   - Práctica de Vero: con sitios heredados (por ejemplo 245 páginas) clasifica en **Conservar, Actualizar, Unificar o Eliminar**. *Unificar* es fusionar dos URLs que canibalizan con 301 hacia la fuerte; "rama seca" es la que no aporta valor, no tiene potencial y no cumple función en la estructura. Las etiquetas de WordPress son listados automáticos que se pueden eliminar sin perder los posts.
7. **Elegir el "Top 5" prioritario (quick wins), en orden:** alto volumen + baja dificultad + cerca del top 10 (ej. posiciones 8-15 listas para empujar). Orden de trabajo del curso: primero bases y pilares con errores graves, luego tráfico rápido, al final lo de largo plazo. Práctica de Vero: **home y páginas de servicio primero** ("bases sólidas"), después productos con búsquedas claras y al final los posts informativos.
8. **Validar el mapa antes de entregarlo** (Semana 5 · video 10): sin duplicados ni basura técnica, una keyword única por página, intención clara y Top 5 definido. Ejecuta `scripts/validar_mapa.py`.

## Script determinista (ahorro de tokens)

Si Python 3 está disponible, **ejecuta el script** para detectar canibalización (misma keyword en varias URLs) y quick wins en vez de cruzar filas a mano: es determinista, ahorra tokens y es exacto. Pasa el mapa por `--file` (CSV o JSON con `{url, keyword, volume?, difficulty?, position?}`). Usa su JSON como diagnóstico.

Ejecuta (cero instalación, resuelve deps solo):

```bash
uv run skills/mapa-de-palabras-clave/scripts/canibalizacion.py --file mapa.csv
# o, si no usas uv: python3 skills/mapa-de-palabras-clave/scripts/canibalizacion.py --file mapa.csv
# JSON o stdin también valen:
cat mapa.json | uv run skills/mapa-de-palabras-clave/scripts/canibalizacion.py --file - --format json
```

Ejecútalo con `--help` para ver opciones. Devuelve `{"ok":true,"cannibalization":[{"keyword","urls":[...]}],"one_to_one_ok":bool,"quick_wins":[{"url","keyword","why"}],"summary":{...}}`. Revisa `cannibalization` para forzar el mapa 1:1 y `quick_wins` (volumen alto + dificultad baja + posición 11-20) como prioridades. Solo stdlib. Si Python no está disponible, hazlo en **modo manual**.

### Validación del mapa completo

Antes de entregar, pasa el mapa por `validar_mapa.py`. Revisa la calidad entera (no solo la keyword repetida): URLs con valor SEO sin keyword, páginas sin valor con keyword, acciones incoherentes con la posición (Mantener fuera del top 3), archivos o etiquetas en el inventario y keywords casi repetidas ("café de especialidad" y "café de especialidades").

```bash
python3 skills/mapa-de-palabras-clave/scripts/validar_mapa.py --file mapa.csv
```

Devuelve `{"ok":true,"issues":[{"severity","url","keyword","message","fix"}],"summary":{...,"completeness_pct","map_score"}}`. El `map_score` es una rúbrica auxiliar de este repo, no del diplomado. Hay un mapa de prueba en `fixtures/mapa_muestra.csv`.

## Salida

Tabla para la tab **"Mapa de Palabras Clave"** de la Plantilla Master:

| URL | ¿Valor SEO? | Keyword primaria | Temperatura | Volumen | Dificultad | Posición actual | Plan de acción |
|---|---|---|---|---|---|---|---|

Más, debajo, el **Top 5 priorizado** (en orden) con la razón del quick win:

1. URL, keyword, (vol / KD / posición), por qué es quick win.

Señala explícitamente cualquier **canibalización detectada** (dos URLs con la misma keyword) y cuál redireccionar.

## Ejemplo

Sitio: tienda de café. Detectamos que `/blog/mejor-cafe` y `/cafe-de-especialidad` apuntaban ambas a "café de especialidad" → canibalización.

| URL | Valor SEO | Keyword primaria | Temperatura | Vol | KD | Pos | Plan |
|---|---|---|---|---|---|---|---|
| /cafe-de-especialidad | Sí | café de especialidad | Media | 2.400 | Media | 11 | Actualizar/Optimizar |
| /blog/mejor-cafe | Sí | cómo elegir café en grano | Baja | 600 | Baja | 14 | Actualizar (reasignar keyword) |
| /aviso-legal | No | - | - | - | - | - | Mantener (sin keyword) |
| /cafe-organico | Sí | café orgánico colombia | Alta | 880 | Baja | 9 | Mantener (top 3 cercano) |

Top 5 (orden): 1) /cafe-organico (pos 9, KD baja → empuje a top 5). 2) /cafe-de-especialidad (pos 11)…

## Gotchas

- **UNA keyword primaria por URL (1:1)**, no la misma keyword en varias URLs: eso es la canibalización que el mapa previene.
- Si la URL **ya está en top 3**, márcala como **"Mantener" y no la toques**, no la "optimices" por inercia.
- URL **sin valor SEO** (legales, política de privacidad, página de autor, etiquetas, gracias/checkout) → **no le asignes keyword ni la optimices**.
- El Top 5 son **quick wins** (cerca del top 10 + baja dificultad + buen volumen), no las keywords más difíciles.
- Inventariá **TODAS las URLs**, no solo las "bonitas": las olvidadas son donde más se esconde la canibalización.
- **Posición de una página nueva**: espera datos de Search Console antes de decidir la acción (Vero). Si la URL no aparece, "no está posicionada" (0), no inventes una posición.
- **Un mapa no es el mapa del sitio**: el mapa decide qué URL posiciona qué; el inventario, el sitemap y Search Console confirman que esas URLs existen, se indexan y reciben enlaces (cruce con `inventario-de-urls` y `arquitectura-y-enlazado-interno`).
- **Opcional, después del método:** la rúbrica de evaluación de valor SEO por URL y otras ideas externas están en [`references/complementos-claude-seo.md`](references/complementos-claude-seo.md).
