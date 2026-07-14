---
name: inventario-de-urls
description: Usa esta skill cuando necesites el inventario de TODAS (o casi todas) las URLs de un sitio y el usuario NO te pasó un export. Es el paso previo obligado a mapa-de-palabras-clave, auditoria-tecnica y arquitectura-y-enlazado-interno cuando falta la lista de URLs — aunque el usuario no diga "inventario", p.ej. "arma un mapa de keywords de ejemplo.com", "audita ejemplo.com", "¿cuántas páginas tiene el sitio?", "saca todas las URLs". Dos caminos: por sitemap (cero instalación, sin coste) o con Screaming Frog CLI headless (GRATIS hasta 500 URLs), que aporta códigos de estado y grafo de enlaces. No inventes URLs: extráelas de la fuente real.
compatibility: Script opcional requiere Python 3 (uv, solo stdlib). Camino sitemap por Bash/WebFetch sin instalar nada. Screaming Frog CLI opcional (GRATIS ≤500 URLs; licencia solo >500 URLs/config/JS/scheduling/API).
metadata:
  author: aprendoseo
  milestone: SEO skills (De Cero a SEO)
  version: "1.0"
---

> **🚫 Regla de datos (obligatoria): NUNCA inventes números.**
> No estimes, supongas ni inventes métricas o datos que no tengas: volumen de búsqueda, dificultad/KD, clics, impresiones, CTR, posición, tráfico, Core Web Vitals, backlinks, fechas, precios, etc. Si te falta un dato, **pídeselo al usuario y espera su respuesta** — que lo pegue a mano, lo exporte (Google Search Console, Ahrefs, DinoRank, Screaming Frog…) o lo conecte por MCP. Da igual de dónde venga, pero tiene que venir de una fuente real. Si aun así no hay dato, márcalo explícitamente como `pendiente de dato` y NO continúes como si lo tuvieras. Un entregable con huecos honestos vale más que uno con cifras inventadas.


> **📊 Cierre en dashboard.** Cuando trabajes sobre un sitio, además de tu entrega persiste tu salida estructurada en `.seo-audit/<sitio>/data/inventory-summary.json` (esquema en la skill `dashboard-seo`). Al cerrar el flujo SEO, genera/actualiza el dashboard con `dashboard-seo` y entrega el URL local. Tu archivo: `inventory-summary.json`.

# Inventario de URLs (paso previo de datos)

Actúa como recolector de URLs en aprendoseo. Antes de mapear keywords, auditar o diseñar arquitectura necesitas **la lista real de URLs del sitio**. Si el usuario no te la pasó, tu trabajo es extraerla de la fuente. Filosofía del diploma: *"Lo que no se rastrea, no existe"* — y para rastrearlo primero hay que **listarlo**.

## Cuándo usar

- El usuario te pide un mapa de keywords, una auditoría técnica o un plan de enlazado **pero NO adjuntó un export de URLs**.
- Necesitas alimentar `mapa-de-palabras-clave`, `auditoria-tecnica` o `arquitectura-y-enlazado-interno` con una lista de URLs.
- Quieres una foto inicial del tamaño y la estructura del sitio.

## Entradas (qué te doy)

- **Dominio** del sitio (obligatorio): `https://ejemplo.com`.
- (Opcional) URL directa del sitemap si la conoces.

> **Sitios de >500 URLs SIN licencia:** no hace falta licencia. La versión gratis limita a 500 URLs **por rastreo**, no por sitio. Se cubre el sitio entero **troceando**: sacar todas las URLs del sitemap y rastrearlas en lotes de ≤500 con `--crawl-list`, luego juntar los CSV. Lo automatiza `scripts/sf_crawl_all.py` (ver abajo).

## Datos (herramientas opcionales)

Hay **dos caminos**, ambos gratis para sitios ≤500 URLs. Por defecto usa el de **sitemap** (cero instalación); usa **Screaming Frog CLI** si quieres códigos de estado en vivo / huérfanas / grafo de enlaces.

### Camino sitemap (por defecto, cero instalación)

Sin instalar nada ni MCP. Vía **Bash (`curl`)** o **WebFetch**. Orden estricto:

1. `https://<sitio>/robots.txt` → lee las directivas **`Sitemap:`** (puede haber varias).
2. Si no hay directiva, prueba `https://<sitio>/sitemap.xml` y `https://<sitio>/sitemap_index.xml`.
3. Descarga cada sitemap; si es un **`<sitemapindex>`**, sigue cada hijo (`<sitemap><loc>`) hasta llegar a los sitemaps de URLs.
4. Parsea todos los `<loc>` → esa es tu lista de URLs.

> **Límite del camino sitemap:** solo ves URLs **publicadas en el sitemap**. NO detecta **páginas huérfanas**, NO trae **códigos de estado en vivo** ni el **grafo de enlaces internos**. Suficiente para un primer inventario; insuficiente para auditoría profunda.

> **Si el sitio bloquea el rastreo (`"blocked": true`):** el script ya manda un User-Agent de navegador real, así que pasa la mayoría de los sitios. Si aun así devuelve `"blocked": true`, hay un WAF/anti-bot (típicamente **Cloudflare**) que bloquea por *TLS fingerprint*, no por User-Agent — ningún cliente HTTP plano lo evita. **No insistas ni intentes evadirlo.** Guía al usuario: (1) si es **su** sitio, que cree una WAF rule en Cloudflare que permita su rastreo (por IP o User-Agent) o que exporte las URLs desde **Google Search Console** (Sitemaps / Páginas indexadas); (2) si no es suyo, usa **Screaming Frog** (motor de navegador real) o el sitemap obtenido vía GSC; (3) opcionalmente, prueba otro User-Agent con la variable de entorno `SEO_USER_AGENT`.

### Camino Screaming Frog CLI (más rico) — GRATIS, sin tope de sitio

Rastreo **headless** que devuelve la lista completa con **código de estado, tipo de contenido e indexabilidad**, más el grafo de enlaces para detectar huérfanas. La versión gratis limita a **500 URLs por rastreo**, pero **no por sitio**: para sitios grandes se trocea (más abajo) y se cubre todo gratis. (Nota técnica: hay funciones que sí piden licencia — config guardada con `--config`, render JS, scheduling e integraciones de API —, pero nada de eso hace falta para el inventario.)

> **Disco / modo de almacenamiento:** por defecto SF usa almacenamiento en base de datos y **exige 4 GB de disco libre**, o aborta con `FATAL - You do not have sufficient disk space`. Con disco justo, cambia a **modo memoria/RAM**: `storage.mode=MEMORY` en `~/.ScreamingFrogSEOSpider/spider.config` (o GUI `Configuration > System > Storage Mode > Memory Storage`). Para ≤500 URLs sobra. Detalle en `../../SCREAMING-FROG.md`.

El binario se resuelve por la variable `SCREAMING_FROG_BINARY` o por los defaults del SO. Comando núcleo (rastrear → exportar todas las URLs internas a CSV), por SO:

- **macOS:**
  ```bash
  "/Applications/Screaming Frog SEO Spider.app/Contents/MacOS/ScreamingFrogSEOSpiderLauncher" \
    --headless --crawl https://ejemplo.com \
    --output-folder ./sf-out --overwrite \
    --export-format csv --export-tabs "Internal:All"
  ```
- **Linux:**
  ```bash
  screamingfrogseospider --headless --crawl https://ejemplo.com \
    --output-folder ./sf-out --overwrite \
    --export-format csv --export-tabs "Internal:All"
  ```
- **Windows:**
  ```bat
  "C:\Program Files (x86)\Screaming Frog SEO Spider\ScreamingFrogSEOSpiderCLI.exe" ^
    --headless --crawl https://ejemplo.com ^
    --output-folder .\sf-out --overwrite ^
    --export-format csv --export-tabs "Internal:All"
  ```

> aprendoseo ya tiene una herramienta interna que ejecuta este flujo **gratis**: `technical-audit` (`../../../technical-audit/`, `src/core/crawler.py`). Su patrón real combina `--save-report "Issues Summary,Issues Overview"` y `--bulk-export "Issues:All"`.

Para huérfanas / grafo de enlaces interno, añade:
```
--bulk-export "All Inlinks,All Outlinks"
```

**Cómo leer el resultado:** se genera `internal_all.csv` en el `--output-folder`. Léelo (Bash/Read) y úsalo como lista maestra: columnas clave **Address** (URL), **Status Code**, **Content Type**, **Indexability**. El bulk export produce los CSV de inlinks/outlinks (lista de aristas) para cruzar y encontrar URLs sin inlinks (huérfanas).

### Sitio entero GRATIS por troceo (>500 URLs, sin licencia)

El límite de 500 es **por rastreo**, no por sitio. `scripts/sf_crawl_all.py` saca todas las URLs del sitemap, las trocea en lotes de ≤500 (un sitemap con >500 URLs se parte solo), corre SF en modo `--crawl-list` por cada lote y junta los CSV en un único `internal_all.csv` (dedup por Address):

```
# rastrea TODO el sitio en lotes de 500 (gratis):
python3 skills/inventario-de-urls/scripts/sf_crawl_all.py --site https://ejemplo.com --out ./sf-out

# planifica los lotes sin correr SF (cuántos lotes y de cuántas URLs):
python3 skills/inventario-de-urls/scripts/sf_crawl_all.py --site https://ejemplo.com --dry-run

# pasar un sitemap directo y/o exportar también los issues:
python3 skills/inventario-de-urls/scripts/sf_crawl_all.py --site https://ejemplo.com \
  --sitemap https://ejemplo.com/sitemap_index.xml --bulk-export "Issues:All"
```

Salida: `{"ok":true,"urls_total":N,"batches":K,"crawled":N,"merged_csv":".../internal_all.csv","per_batch":[...],"revalidation":{...}}`. Si SF aborta por disco, avisa que cambies a `storage.mode=MEMORY`. Si no hay sitemap, cae a modo manual (pasar `--sitemap` o exportar URLs de GSC). El `merged_csv` se pasa tal cual a `parse_sf.py` / `auditoria-tecnica`.

> **Tiendas Shopify y otros WAF — 4xx FALSOS por rate-limit:** SF usa User-Agent de bot; Shopify (y otros WAF) lo rate-limitan devolviendo **4xx/429/430 falsos** en URLs que en el navegador abren bien. Es bloqueo, no roturas. `sf_crawl_all.py` **detecta Shopify** (headers `x-shopify-*`, `cdn.shopify.com`) y hace **dos pasos automáticos**:
> 1. **Revalida** los 4xx/5xx con `http_checks.py` (UA real + baja concurrencia = throttle), corrigiendo el `Status Code` en el CSV. Salida: `"revalidation": {"revalidated":N, "fixed":<falsos>, "still_bad":<roturas reales>}`.
> 2. **Enriquece on-page** las URLs recuperadas con `onpage_extract.py` (baja el HTML con UA real y saca **title, meta description, robots, canonical, H1/H2, hreflang, word count, indexability**), porque cuando SF las vio como 4xx **nunca parseó su HTML** y esas columnas quedaron vacías. Salida: `"onpage_enrichment": {"enriched":N, "indexable":M, "json":"...onpage_enriched.json", "csv":"...onpage_enriched.csv"}`.
>
> Flags: `--revalidate`/`--no-revalidate`, `--enrich`/`--no-enrich`, `--revalidate-concurrency`/`--enrich-concurrency` (default 4; baja a 2 si aún bloquea). **Límite:** el enriquecimiento recupera lo on-page por URL, NO el grafo de inlinks/profundidad (eso requiere crawl; en Shopify SF gratis se bloquea, haría falta licencia). **Caso real:** una tienda Shopify marcó cientos de 4xx en el crawl inicial; tras revalidar, la gran mayoría eran falsos por rate-limit y el resto se recuperó con su data on-page completa. Detalle en `../../SCREAMING-FROG.md` ("4xx masivos en tiendas Shopify").

Detalle de instalación, binarios, prerequisitos headless y los 3 comandos completos: ver **`../../SCREAMING-FROG.md`**.

## Proceso

1. Confirma el **dominio**.
2. **Cero instalación → camino sitemap:** robots.txt → directivas `Sitemap:` → sitemap.xml/index → parsear `<loc>`.
3. **Con Screaming Frog (GRATIS):** sitio de ≤500 URLs → comando headless directo; sitio de >500 URLs → `sf_crawl_all.py` (trocea en lotes de ≤500 y junta los CSV). Lee el `internal_all.csv` resultante (+ All Inlinks si necesitas huérfanas).
4. **Normaliza:** quita duplicados, descarta parámetros de tracking si procede, ordena.
5. **Entrega** la lista/tabla y deja claro de qué camino vino (y por tanto qué límites tiene).

## Salida

Una **lista o tabla de URLs** lista para alimentar las otras skills:

| URL | Código de estado | Tipo | Fuente |
|---|---|---|---|
| https://ejemplo.com/ | 200 | text/html | SF |
| https://ejemplo.com/blog/ | 200 | text/html | SF |

- Si vino del **sitemap**: solo columna URL (sin código/tipo) + nota del límite (no huérfanas, no estado en vivo).
- Si vino de **Screaming Frog (CLI, gratis ≤500 URLs)**: URL + código de estado + tipo + indexabilidad, y opcionalmente la lista de huérfanas.

Pasa la lista a `mapa-de-palabras-clave`, `auditoria-tecnica` y/o `arquitectura-y-enlazado-interno`.

## Ejemplo

Usuario: *"Haz un mapa de keywords de ejemplo.com"* (sin adjuntar URLs).

1. No hay Screaming Frog instalado → camino sitemap.
2. `curl https://ejemplo.com/robots.txt` → `Sitemap: https://ejemplo.com/sitemap_index.xml`.
3. El index lista `post-sitemap.xml` y `page-sitemap.xml` → se siguen y se parsean los `<loc>`.
4. Resultado: 84 URLs. Se entrega la lista y se avisa: *"Faltan posibles huérfanas y no hay códigos de estado en vivo; para eso, Screaming Frog CLI (gratis hasta 500 URLs)."*
5. Se alimenta `mapa-de-palabras-clave` con las 84 URLs.

## Script determinista (ahorro de tokens)

Si Python está disponible, EJECUTA este script para el paso mecánico del **camino sitemap** (es determinista, ahorra tokens y mejora precisión) y usa su salida JSON en vez de leer robots.txt/XML crudo. Si falta una dependencia o algo falla, sigue en modo manual.

Ejecuta (cero instalación, resuelve deps solo):

```bash
uv run scripts/inventario_urls.py https://ejemplo.com
# o, si no usas uv: python3 scripts/inventario_urls.py https://ejemplo.com
# opcional: --sitemap https://ejemplo.com/sitemap_index.xml   --max 2000
```

Corre con `--help` para ver opciones. Solo usa la librería estándar (sin instalar nada ni claves). Devuelve: `{"ok": true, "source": "robots|sitemap.xml", "count": N, "urls": [...]}` — o si no encuentra sitemaps, `{"ok": false, "reason": "...", "fallback": "..."}`. Es la ruta free de cero deps; para >500 URLs, huérfanas o códigos de estado en vivo sigue usando Screaming Frog CLI.

## Gotchas

- El **sitemap solo lista lo que el sitio publicó — NO detecta páginas huérfanas ni códigos de estado en vivo** ni el grafo de enlaces; sirve para un primer inventario, no para auditoría profunda.
- Lee **robots.txt → directivas `Sitemap:` antes de adivinar `/sitemap.xml`**: a veces el sitemap está en una ruta no estándar declarada solo en robots.
- Sigue el **`<sitemapindex>`** hasta los sitemaps hijos; si te quedas en el índice pierdes las URLs reales.
- **Inventar o "adivinar" URLs, no**: extráelas siempre de robots.txt/sitemap o del crawl real.
- El **CLI de Screaming Frog es GRATIS hasta 500 URLs** (headless + export CSV/bulk/report); la licencia solo hace falta para >500 URLs, config guardada, render JS, scheduling o API — no para esto.
- Usa `--overwrite` (o `--timestamped-output`), no lo omitas: el comando falla si el output ya existe.
