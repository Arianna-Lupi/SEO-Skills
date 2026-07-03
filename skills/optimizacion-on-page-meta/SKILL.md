---
name: optimizacion-on-page-meta
description: Optimiza metatítulos, metadescripciones y on-page de una URL según el método del diploma "De Cero a SEO" (aprendoseo). Usa esta skill cuando vayas a publicar o reoptimizar una página — AUNQUE el usuario no diga "meta" ni "on-page", p.ej. "ármame el título y la descripción de esta página", "tengo CTR bajo / no me hacen clic en Google", "mejora el on-page de esta URL", "dame variantes para A/B de CTR". Genera metatítulo (50-60 chars, keyword al inicio) y metadescripción (120-155 con CTA), variantes para A/B y un checklist on-page accionable. No publiques nada sin pasar por aquí.
compatibility: Script opcional de validación de metas requiere Python 3 (uv); si no está, modo manual con simulador de SERP. SerpApi MCP (gratis) y Ahrefs MCP (pago) opcionales.
metadata:
  author: aprendoseo
  milestone: SEO skills (De Cero a SEO)
  version: "1.0"
---

> **🚫 Regla de datos (obligatoria): NUNCA inventes números.**
> No estimes, supongas ni inventes métricas o datos que no tengas: volumen de búsqueda, dificultad/KD, clics, impresiones, CTR, posición, tráfico, Core Web Vitals, backlinks, fechas, precios, etc. Si te falta un dato, **pídeselo al usuario y espera su respuesta** — que lo pegue a mano, lo exporte (Google Search Console, Ahrefs, DinoRank, Screaming Frog…) o lo conecte por MCP. Da igual de dónde venga, pero tiene que venir de una fuente real. Si aun así no hay dato, márcalo explícitamente como `pendiente de dato` y NO continúes como si lo tuvieras. Un entregable con huecos honestos vale más que uno con cifras inventadas.


> **📊 Cierre en dashboard.** Cuando trabajes sobre un sitio, además de tu entrega persiste tu salida estructurada en `.seo-audit/<sitio>/data/content-briefs.json` (esquema en la skill `dashboard-seo`). Al cerrar el flujo SEO, genera/actualiza el dashboard con `dashboard-seo` y entrega el URL local. Tu archivo: `content-briefs.json` (meta_title / meta_desc).

# Optimización On-Page + Metas (Diploma W8 + W11)

Actúa como especialista on-page en aprendoseo. Tu trabajo es que la página **se rastree, se indexe y posicione**, y que cuando aparezca en la SERP, la gente haga clic. Recuerda el marco del diploma: *"Lo que no se rastrea, no existe"* — pero rastrear no basta si el metatítulo no convence.

> **Método completo del diploma:** los pasos detallados, las plantillas y los prompts originales de Arianna están en [`references/metodo-diploma.md`](references/metodo-diploma.md). Lee ese archivo para seguir el método exacto del curso; no improvises el método.

## Cuándo usar

- Vas a **publicar una página nueva** y necesitas sus metas + checklist on-page.
- Quieres **reoptimizar** una URL existente (CTR bajo, posición estancada, contenido viejo).
- Necesitas **variantes de metatítulo/metadescripción para A/B testing** de CTR.
- Estás llenando la pestaña **Producción** o **Auditoría** de la Plantilla Master.

## Entradas (qué te doy)

- **URL** (o borrador) + **keyword principal** y, si las hay, secundarias.
- **Intención de búsqueda** (informacional, transaccional, navegacional).
- **H1 actual** y primeras 100 palabras (si la página ya existe).
- Opcional: propuesta de valor / CTA del negocio, marca, tono.

## Datos (MCP opcional)

Esta skill **funciona sin ningún MCP**. El MCP solo enriquece con datos reales de SERP/volumen.

1. **Sin MCP (manual — siempre válido):** abre la SERP de tu keyword, copia los **títulos y metadescripciones del top 5-10** para tener un benchmark de CTR. Usa el simulador de SERP de **Mangools** para verificar que tu título no se corte en 50-60 caracteres.
2. **SerpApi MCP (GRATIS — principal):** `mcp__serpapi__search` con tu keyword → títulos/metas que ya rankean (benchmark de CTR), bloque **PAA (People Also Ask)** y *related searches* para nutrir secundarias y la metadescripción.
3. **Ahrefs MCP (PAGO):** `mcp__claude_ai_Ahrefs__keywords-explorer-overview` (volumen/dificultad de la keyword), `...keywords-explorer-related-terms` (secundarias). Ahrefs es de pago.

Config de MCP: ver `../../MCP-SETUP.md`.

## Proceso

1. **Confirma keyword e intención.** Una keyword principal por página. Si la intención no calza con el contenido, detente y avisa.
2. **Metatítulo** (*"el factor on-page más importante después del contenido"*):
   - Keyword **al inicio**.
   - **50-60 caracteres** (verifica en simulador; si se corta, recórtalo).
   - Incluye marca al final si cabe.
3. **Metadescripción:**
   - **120-155 caracteres**, persuasiva, con **CTA** explícito.
   - Recuerda: la meta **mueve CTR, no ranking directo**.
4. **Genera 3-5 variantes** de metatítulo + metadescripción para A/B de CTR (ángulos distintos: beneficio, urgencia, número/dato, pregunta del PAA).
5. **Checklist on-page** (marca cada ítem):
   - [ ] Keyword en **H1** y en las **primeras 100 palabras**.
   - [ ] Jerarquía **H1-H4 sin saltos** (no pasar de H2 a H4).
   - [ ] **URL corta, sin tildes ni eñes problemáticas**, con la keyword.
   - [ ] **ALT** descriptivo en imágenes.
   - [ ] **Enlaces internos** con anchor text relevante (no "clic aquí").
   - [ ] **Densidad natural** de keyword (sin sobreoptimizar).
6. **Registra** el set elegido y el checklist en la Plantilla Master.

## Script determinista (ahorro de tokens)

Si Python 3 está disponible, **ejecuta el script** para validar las metas en vez de contar caracteres a mano: es determinista, ahorra tokens y da conteos exactos. Usa su JSON como fuente de verdad.

Ejecuta (cero instalación, resuelve deps solo):

```bash
uv run skills/optimizacion-on-page-meta/scripts/meta_check.py \
  --title "Tu metatítulo" \
  --desc "Tu metadescripción con CTA →" \
  --keyword "keyword principal"
# o, si no usas uv: python3 skills/optimizacion-on-page-meta/scripts/meta_check.py --title "..." --desc "..." --keyword "..."
```

Corre con `--help` para ver opciones. Devuelve `{"ok":true,"title":{"len","in_range_50_60","keyword_at_start"},"desc":{"len","in_range_120_155","has_cta_hint","keyword_present"},"warnings":[...]}`. Toma `warnings` como la lista de ajustes (título 50-60 con keyword al inicio; meta 120-155 con CTA y keyword). Solo stdlib, sin deps. Si Python no está disponible, valida en **modo manual** con el simulador de SERP.

## Script de benchmark de metas (competencia)

Antes de redactar, saca el **benchmark real de CTR**: entra al top de la SERP y extrae qué metatítulo y metadescripción usan los que ya rankean tu keyword. Este segundo script hace el pipeline: SerpApi busca la keyword → toma el top N → **entra a cada URL** → extrae `<title>`, `<meta name="description">`, H1 y og:*, cuenta caracteres y marca rango. Redactas TU metadata con ese benchmark delante (nunca de memoria), entendiendo primero la **intención** que revela la SERP.

```bash
uv run skills/optimizacion-on-page-meta/scripts/serp_metadata.py "sérum vitamina c natural" --top 10 --gl es --hl es
# sin SerpApi, pasando URLs a mano (p.ej. las que sacó analisis-de-competidores):
uv run skills/optimizacion-on-page-meta/scripts/serp_metadata.py "sérum vitamina c natural" --urls "https://a.com/x,https://b.com/y"
```

Devuelve `{"ok":true,"query":...,"paa":[...],"competitors":[{url,serp_title,serp_snippet,meta_title,meta_title_len,meta_title_in_range,meta_description,meta_description_len,meta_description_in_range,h1,og_title,og_description}]}`. Deps: requests + beautifulsoup4 (uv las resuelve). Sin clave/deps degrada a modo manual (copiar títulos/metas del top a mano). Flujo: **este script (benchmark) → redactas → `meta_check.py` (validas)**.

Para DESCUBRIR primero qué dominios/URLs son la competencia, usa la skill `analisis-de-competidores` y pásale aquí las URLs con `--urls`.

## Salida

- **Set de metas:** metatítulo elegido + 3-5 variantes (con conteo de caracteres) y metadescripción + variantes.
- **Checklist on-page** marcado, con los ítems pendientes señalados.
- Fila lista para pegar en la pestaña **Producción / Auditoría** de la Plantilla Master Google Sheet.

## Ejemplo

**Entrada:** URL nueva, keyword "auditoría SEO técnica", intención informacional.

**Metatítulo (58 car.):** `Auditoría SEO técnica: guía paso a paso | aprendoseo` Variantes:
- `Auditoría SEO técnica en 3 bloques (plantilla gratis)` (54)
- `Cómo hacer una auditoría SEO técnica desde cero` (48)

**Metadescripción (148 car.):** `Aprende a hacer una auditoría SEO técnica en 3 bloques: indexabilidad, velocidad y seguridad. Descarga la plantilla y detecta errores hoy. →`

**Checklist:** keyword en H1 ✅, en primeras 100 palabras ✅, URL `/auditoria-seo-tecnica` ✅, jerarquía sin saltos ✅, ALT pendiente ⬜.

## Gotchas

- **Metatítulo 50-60 chars con keyword al inicio; metadescripción 120-155 con CTA** — verifica siempre el corte en el simulador, no a ojo. Keyword al final = menos peso y menos clic.
- **La metadescripción no es factor de ranking directo, pero mueve el CTR** — escríbela para que la persona haga clic, no para "meter keyword".
- **No dupliques metas entre URLs** — cada página, su título y su descripción únicos; metas duplicadas confunden a Google y canibalizan.
- **Saltos de encabezado** (H2→H4) rompen la jerarquía y confunden al rastreador.
- **URLs con tildes/eñes o larguísimas** → menos rastreables y compartibles. Corta y sin tildes.
- **No reescribas el mismo título 5 veces igual:** las variantes A/B deben atacar **ángulos distintos** (beneficio, número, urgencia, pregunta del PAA).
