---
name: analisis-de-competidores
description: Usa esta skill cuando el usuario quiera SABER QUIÉNES son sus competidores SEO reales a partir de una keyword (o unas pocas) — aunque no diga "competidores", p.ej. "quién me gana en Google con esta palabra", "sácame los dominios que rankean esto", "quiénes son los que salen arriba", "identifica a mi competencia para esta keyword". Hace el pipeline determinista: SerpApi busca la keyword → toma el top 5-10 de URLs → ENTRA a cada link (sigue redirects) → extrae el dominio registrado de cada uno → agrega, cuenta repetición ("un dominio que sale en varias SERPs = competidor crítico") y devuelve la lista de competidores priorizada. Es el paso de DESCUBRIR competidores; para el análisis profundo de gaps/ojo clínico usa `analisis-serp-y-competencia`.
compatibility: Script requiere Python 3 (uv) + requests + tldextract y SERPAPI_API_KEY (o --urls para modo manual). Sin clave/deps degrada a modo manual (Google en incógnito). Alternativa: MCP de SerpApi (ver MCP-SETUP.md).
metadata:
  author: aprendoseo
  milestone: SEO skills (De Cero a SEO)
  version: "1.0"
---

> **🚫 Regla de datos (obligatoria): NUNCA inventes números.**
> No estimes, supongas ni inventes métricas o datos que no tengas: volumen de búsqueda, dificultad/KD, clics, impresiones, CTR, posición, tráfico, backlinks, fechas, etc. Si te falta un dato, **pídeselo al usuario y espera su respuesta** — que lo pegue a mano, lo exporte (Google Search Console, Ahrefs, DinoRank, Screaming Frog…) o lo conecte por MCP. Si aun así no hay dato, márcalo como `pendiente de dato` y NO continúes como si lo tuvieras.

> **📊 Cierre en dashboard.** Cuando trabajes sobre un sitio, además de tu entrega persiste tu salida estructurada en `.seo-audit/<sitio>/data/competitors.json` (esquema en la skill `dashboard-seo`). Al cerrar el flujo SEO, genera/actualiza el dashboard con `dashboard-seo` y entrega el URL local. Tu archivo: `competitors.json`.

# Análisis de Competidores — descubrir por dominio (SerpApi)

Actúa como estratega SEO en aprendoseo (método de Arianna Lupi, "De Cero a SEO", Semana 6). Esta skill resuelve **una pregunta concreta**: dada una keyword, **¿quiénes son los dominios que compiten de verdad por ella?** No copia al rival ni analiza gaps (eso es `analisis-serp-y-competencia`); su trabajo es **descubrir y priorizar los dominios competidores** con datos reales de la SERP.

Regla clave del método: **Competidor SEO ≠ competidor de negocio.** Un dominio que rankea tu keyword es tu competidor SEO aunque no venda lo que tú (un medio, un blog, Wikipedia). Y el **"Análisis de Repetición"**: un dominio que aparece en varias de tus SERPs es un **competidor crítico**.

## Cuándo usar

- El usuario tiene una keyword (o 2-5) y quiere la **lista de dominios competidores**.
- Necesita el insumo de competidores ANTES de un análisis de gaps, un brief o metadata.
- Quiere saber qué dominios se **repiten** en varias de sus keywords (los críticos).

Después de esta skill: análisis profundo con `analisis-serp-y-competencia`, o alimenta `optimizacion-on-page-meta` (metadata) y `brief-de-contenido` (encabezados) pasándoles las URLs/competidores que salgan aquí.

## Entradas (qué te doy)

- **1 keyword** (o varias, para el Análisis de Repetición).
- País/idioma de la SERP (`gl`/`hl`, default `es`/`es`).
- Opcional: **tu propio dominio** (para excluirlo del ranking).
- Cuántos resultados mirar (top 5 o 10).

## Datos (MCP opcional)

Funciona **sin MCP** con el script (que trae su propia clave de `~/.claude/seo-skills.env`). Fallback 100% manual: Google en incógnito, copiar el top 10, anotar el dominio de cada uno y marcar los que se repiten.

- **SerpApi (GRATIS — principal aquí):** el script usa la REST de SerpApi. Alternativa MCP: `mcp__serpapi__search`.
- **Ahrefs (PAGO, enriquece):** `mcp__claude_ai_Ahrefs__site-explorer-organic-competitors` descubre rivales SEO por solapamiento de keywords; úsalo para cruzar/confirmar la lista que saca el script. No es obligatorio.

Config de MCP/clave: ver `../../MCP-SETUP.md` y la skill `configurar-serpapi`.

## Proceso

El grueso lo hace el **script determinista** (abajo). Tu trabajo es interpretar y priorizar.

1. **Ejecuta el script** con la keyword (o varias separadas por `|`) y tu dominio en `--own`.
2. **Lee `competitors`** del JSON: viene ordenado por **repetición** (en cuántas keywords aparece) y luego por **mejor posición**.
3. **Prioriza:**
   - `repeticion ≥ 2` (aparece en varias SERPs) = **competidor crítico**.
   - `best_position` baja (1-3) = domina esa keyword.
   - Descarta agregadores/marketplaces irrelevantes si el objetivo es competencia directa (Amazon, YouTube, etc.), pero anótalos: a veces ES la SERP que hay que batir.
4. **Clasifica** cada dominio crítico como Competidor de Negocio y/o SEO (¿vende lo mismo o solo rankea?).
5. **Entrega** la lista priorizada y pásala como insumo a la siguiente skill.

## Script determinista (ahorro de tokens)

Si Python está disponible, EJECUTA este script: busca la SERP, **entra a cada URL del top N siguiendo redirects, extrae el dominio registrado** (`blog.x.co.uk` → `x.co.uk`), agrega y cuenta repetición. Es determinista, ahorra tokens y evita razonar sobre HTML. Si falta `SERPAPI_API_KEY` o las deps, degrada a modo manual.

Ejecuta (cero instalación, `uv` resuelve deps solo):

```bash
# 1 keyword, top 10, excluyendo tu dominio:
uv run skills/analisis-de-competidores/scripts/competitor_domains.py "agencia seo madrid" --top 10 --gl es --hl es --own midominio.com

# varias keywords para Análisis de Repetición (separadas por |):
uv run skills/analisis-de-competidores/scripts/competitor_domains.py "agencia seo madrid|consultor seo|posicionamiento web" --top 10

# sin SerpApi, pasando URLs a mano y sin entrar a los links:
uv run skills/analisis-de-competidores/scripts/competitor_domains.py "curso seo" --urls "https://a.com/x,https://b.com/y" --no-visit
```

Corre con `--help` para ver opciones. Devuelve:
`{"ok": true, "keywords": [...], "top": N, "competitors": [{domain, repeticion, best_position, positions:{kw:pos}, sample_url, title}], "own_domain": ...}`.
Ordenado por `repeticion` desc y `best_position` asc. Si falla: `{"ok": false, "reason": "...", "fallback": "modo manual: ..."}` (exit 0).

## Salida

Tabla de competidores priorizada, lista para la tab **Competencia** de la Plantilla Master:

| Dominio | Repetición (de N kw) | Mejor posición | Negocio/SEO | Directo/Indirecto | URL ejemplo |
|---|---|---|---|---|---|

Marca los `repeticion ≥ 2` como **críticos**. Debajo, 1 línea por dominio crítico diciendo por qué compite.

## Ejemplo

**Keywords:** `agencia seo madrid | consultor seo | posicionamiento web`, top 10, `--own miagencia.com`.

Script devuelve `example-seo.com` con `repeticion: 3` (sale en las 3 SERPs) y `best_position: 2`. → **competidor crítico**: domina el intent comercial local, hay que estudiarlo con `analisis-serp-y-competencia`. Un blog `revistamarketing.com` sale solo en 1 con posición 8 → competidor SEO indirecto, baja prioridad.

## Gotchas

- **El dominio sale del link, pero ENTRAR importa:** el script sigue redirects para capturar el dominio FINAL (evita quedarte con acortadores/agregadores que redirigen). No te fíes del host crudo del enlace.
- **Dominio registrado, no host:** `blog.ejemplo.com` y `ejemplo.com` son el MISMO competidor. El script normaliza a eTLD+1 (usa `tldextract`), no cuentes subdominios como rivales distintos.
- **Competidor SEO ≠ de negocio:** un dominio que rankea tu keyword compite en SEO aunque no venda lo tuyo. No lo descartes solo porque "no es competencia real de negocio".
- **Repetición = criticidad:** prioriza los dominios que salen en varias SERPs, no el que salió #1 en una sola keyword suelta.
- **SERP en incógnito / región correcta:** usa el `gl`/`hl` correcto; la personalización falsea el ranking. Si el negocio es local, la keyword debe llevar la ciudad.
- Esta skill **descubre y prioriza**; el análisis de gaps, ojo clínico y costo de oportunidad es `analisis-serp-y-competencia`. No dupliques ese trabajo aquí.
