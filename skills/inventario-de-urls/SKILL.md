---
name: inventario-de-urls
description: Usa esta skill cuando necesites el inventario de TODAS (o casi todas) las URLs de un sitio y el usuario NO te pasó un export. Es el paso previo obligado a mapa-de-palabras-clave, auditoria-tecnica y arquitectura-y-enlazado-interno cuando falta la lista de URLs — aunque el usuario no diga "inventario", p.ej. "arma un mapa de keywords de ejemplo.com", "audita ejemplo.com", "¿cuántas páginas tiene el sitio?", "saca todas las URLs". Dos caminos: por sitemap (cero instalación, sin coste) o con Screaming Frog CLI headless (GRATIS hasta 500 URLs), que aporta códigos de estado y grafo de enlaces. No inventes URLs: extráelas de la fuente real.
compatibility: Script opcional requiere Python 3 (uv, solo stdlib). Camino sitemap por Bash/WebFetch sin instalar nada. Screaming Frog CLI opcional (GRATIS ≤500 URLs; licencia solo >500 URLs/config/JS/scheduling/API).
metadata:
  author: aprendoseo
  milestone: SEO skills (De Cero a SEO)
  version: "1.0"
---

# Inventario de URLs (paso previo de datos)

Actúa como recolector de URLs en aprendoseo. Antes de mapear keywords, auditar o diseñar arquitectura necesitas **la lista real de URLs del sitio**. Si el usuario no te la pasó, tu trabajo es extraerla de la fuente. Filosofía del diploma: *"Lo que no se rastrea, no existe"* — y para rastrearlo primero hay que **listarlo**.

## Cuándo usar

- El usuario te pide un mapa de keywords, una auditoría técnica o un plan de enlazado **pero NO adjuntó un export de URLs**.
- Necesitas alimentar `mapa-de-palabras-clave`, `auditoria-tecnica` o `arquitectura-y-enlazado-interno` con una lista de URLs.
- Quieres una foto inicial del tamaño y la estructura del sitio.

## Entradas (qué te doy)

- **Dominio** del sitio (obligatorio): `https://ejemplo.com`.
- (Opcional) Si el sitio supera **500 URLs**: confirmación de si hay **licencia de Screaming Frog** (hasta 500 URLs el CLI es gratis y no hace falta).
- (Opcional) URL directa del sitemap si la conoces.

## Datos (herramientas opcionales)

Hay **dos caminos**, ambos gratis para sitios ≤500 URLs. Por defecto usa el de **sitemap** (cero instalación); usa **Screaming Frog CLI** si quieres códigos de estado en vivo / huérfanas / grafo de enlaces.

### Camino sitemap (por defecto, cero instalación)

Sin instalar nada ni MCP. Vía **Bash (`curl`)** o **WebFetch**. Orden estricto:

1. `https://<sitio>/robots.txt` → lee las directivas **`Sitemap:`** (puede haber varias).
2. Si no hay directiva, prueba `https://<sitio>/sitemap.xml` y `https://<sitio>/sitemap_index.xml`.
3. Descarga cada sitemap; si es un **`<sitemapindex>`**, sigue cada hijo (`<sitemap><loc>`) hasta llegar a los sitemaps de URLs.
4. Parsea todos los `<loc>` → esa es tu lista de URLs.

> **Límite del camino sitemap:** solo ves URLs **publicadas en el sitemap**. NO detecta **páginas huérfanas**, NO trae **códigos de estado en vivo** ni el **grafo de enlaces internos**. Suficiente para un primer inventario; insuficiente para auditoría profunda.

### Camino Screaming Frog CLI (más rico) — GRATIS hasta 500 URLs

Rastreo **headless** que devuelve la lista completa con **código de estado, tipo de contenido e indexabilidad**, más el grafo de enlaces para detectar huérfanas. **Funciona en la versión GRATIS hasta 500 URLs** (export CSV/bulk incluidos). La **licencia (~£199/año) solo se requiere para >500 URLs, config guardada (`--config`), render JS, scheduling o integraciones de API**.

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

Detalle de instalación, binarios, prerequisitos headless y los 3 comandos completos: ver **`../../SCREAMING-FROG.md`**.

## Proceso

1. Confirma el **dominio** (y, solo si superas 500 URLs, si hay licencia de Screaming Frog).
2. **Cero instalación → camino sitemap:** robots.txt → directivas `Sitemap:` → sitemap.xml/index → parsear `<loc>`.
3. **Con Screaming Frog (GRATIS ≤500 URLs):** corre el comando headless del SO correspondiente → lee `internal_all.csv` (+ All Inlinks si necesitas huérfanas).
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

Corre con `--help` para ver opciones. Solo usa la librería estándar (sin instalar nada ni claves). Devuelve:
`{"ok": true, "source": "robots|sitemap.xml", "count": N, "urls": [...]}` — o si no encuentra sitemaps, `{"ok": false, "reason": "...", "fallback": "..."}`. Es la ruta free de cero deps; para >500 URLs, huérfanas o códigos de estado en vivo sigue usando Screaming Frog CLI.

## Gotchas

- El **sitemap solo lista lo que el sitio publicó — NO detecta páginas huérfanas ni códigos de estado en vivo** ni el grafo de enlaces; sirve para un primer inventario, no para auditoría profunda.
- Lee **robots.txt → directivas `Sitemap:` antes de adivinar `/sitemap.xml`**: a veces el sitemap está en una ruta no estándar declarada solo en robots.
- Sigue el **`<sitemapindex>`** hasta los sitemaps hijos; si te quedas en el índice pierdes las URLs reales.
- **Inventar o "adivinar" URLs, no**: extráelas siempre de robots.txt/sitemap o del crawl real.
- El **CLI de Screaming Frog es GRATIS hasta 500 URLs** (headless + export CSV/bulk/report); la licencia solo hace falta para >500 URLs, config guardada, render JS, scheduling o API — no para esto.
- Usa `--overwrite` (o `--timestamped-output`), no lo omitas: el comando falla si el output ya existe.
