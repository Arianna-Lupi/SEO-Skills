---
name: mapa-de-palabras-clave
description: Usa esta skill cuando el usuario YA tenga un sitio con URLs y quiera asignarles keywords, mapear palabras clave a sus páginas, detectar canibalización o priorizar qué páginas optimizar — aunque no diga "mapa" ni "canibalización", p.ej. "tengo varias páginas peleando por lo mismo", "qué keyword le pongo a cada URL", "cuáles páginas optimizo primero", "qué páginas de mi web actualizo". Construye el Mapa de Palabras Clave del método "De Cero a SEO" (aprendoseo, Verónica Romero): inventaria todas las URLs, evalúa su Valor SEO, asigna UNA keyword primaria por URL (1:1) para evitar canibalización, clasifica intención por temperatura y define el plan de acción y el Top 5 de quick wins.
compatibility: Script opcional requiere Python 3 (uv), solo stdlib. SerpApi/Ahrefs MCP y skill inventario-de-urls opcionales (la skill funciona 100% manual).
metadata:
  author: aprendoseo
  milestone: SEO skills (De Cero a SEO)
  version: "1.0"
---

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

**Inventario de URLs (opcional, automático):** si el usuario no pasó el export de URLs, usa la skill `inventario-de-urls` para extraerlas — por **sitemap (cero instalación)** o con **Screaming Frog CLI (GRATIS hasta 500 URLs; licencia solo para >500 URLs / config guardada / render JS / scheduling / API)** — y alimenta con ellas el mapa.

Nunca exijas un MCP. Ver `../../MCP-SETUP.md`.

## Proceso

1. **Inventariar TODAS las URLs** del sitio (Screaming Frog ≤500 free o sitemap) → tab "Mapa de Palabras Clave".
2. **Evaluar el Valor SEO** de cada URL con la pregunta test:
   > **"¿Un usuario buscaría esto en Google?"**
   - **CON valor (Sí):** páginas de servicios, blog, categorías de producto.
   - **SIN valor (No):** legales, política de privacidad, página de autor, carpetas, etiquetas, gracias/checkout.
   Marca Valor SEO = **Sí / No**. Las "No" no reciben keyword.
3. **Asignar UNA keyword primaria por URL (1:1).** Una keyword no puede repetirse en dos URLs → así se evita la **canibalización**.
4. **Clasificar intención por temperatura:**
   - **Baja** = informativa.
   - **Media** = comercial.
   - **Alta** = transaccional.
5. **Traer datos por URL:** Volumen, Dificultad, Posición actual.
6. **Plan de acción por URL:**
   - **Actualizar/Optimizar** (la URL existe pero puede rankear mejor).
   - **Eliminar/Redireccionar** (sin valor o canibaliza).
   - **Mantener** (solo si ya está en **top 3**; no la toques).
7. **Elegir el "Top 5" prioritario (quick wins), en orden:** alto volumen + baja dificultad + cerca del top 10 (ej. posiciones 8-15 listas para empujar).

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

## Salida

Tabla para la tab **"Mapa de Palabras Clave"** de la Plantilla Master:

| URL | ¿Valor SEO? | Keyword primaria | Temperatura | Volumen | Dificultad | Posición actual | Plan de acción |
|---|---|---|---|---|---|---|---|

Más, debajo, el **Top 5 priorizado** (en orden) con la razón del quick win:

1. URL — keyword — (vol / KD / posición) — por qué es quick win.

Señala explícitamente cualquier **canibalización detectada** (dos URLs con la misma keyword) y cuál redireccionar.

## Ejemplo

Sitio: tienda de café. Detectamos que `/blog/mejor-cafe` y `/cafe-de-especialidad` apuntaban ambas a "café de especialidad" → canibalización.

| URL | Valor SEO | Keyword primaria | Temperatura | Vol | KD | Pos | Plan |
|---|---|---|---|---|---|---|---|
| /cafe-de-especialidad | Sí | café de especialidad | Media | 2.400 | Media | 11 | Actualizar/Optimizar |
| /blog/mejor-cafe | Sí | cómo elegir café en grano | Baja | 600 | Baja | 14 | Actualizar (reasignar keyword) |
| /aviso-legal | No | — | — | — | — | — | Mantener (sin keyword) |
| /cafe-organico | Sí | café orgánico colombia | Alta | 880 | Baja | 9 | Mantener (top 3 cercano) |

Top 5 (orden): 1) /cafe-organico (pos 9, KD baja → empuje a top 5). 2) /cafe-de-especialidad (pos 11)…

## Gotchas

- **UNA keyword primaria por URL (1:1)**, no la misma keyword en varias URLs: eso es la canibalización que el mapa previene.
- Si la URL **ya está en top 3**, márcala como **"Mantener" y no la toques**, no la "optimices" por inercia.
- URL **sin valor SEO** (legales, política de privacidad, página de autor, etiquetas, gracias/checkout) → **no le asignes keyword ni la optimices**.
- El Top 5 son **quick wins** (cerca del top 10 + baja dificultad + buen volumen), no las keywords más difíciles.
- Inventariá **TODAS las URLs**, no solo las "bonitas": las olvidadas son donde más se esconde la canibalización.
