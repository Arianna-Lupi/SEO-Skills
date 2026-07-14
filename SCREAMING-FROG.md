# Screaming Frog SEO Spider: sacar la lista de URLs por línea de comandos

Esta guía te muestra cómo usar Screaming Frog SEO Spider para conseguir el inventario de URLs de un sitio y sus datos técnicos. Esos datos alimentan las skills de aprendoseo (`inventario-de-urls`, `auditoria-tecnica`, `arquitectura-y-enlazado-interno`, `mapa-de-palabras-clave`).

Vamos a usarlo en modo CLI. CLI quiere decir línea de comandos: en vez de hacer clic en la app, le das órdenes escritas en la terminal.

> Antes de empezar, dos cosas que cambian según la versión que instales y que conviene confirmar en el momento: (1) el número exacto que lleva `eula.accepted` dentro de `spider.config`, y (2) los nombres exactos de los archivos de export que genera tu versión. Tanto las etiquetas de pestañas y filtros (`--export-tabs`) como los nombres de los CSV tienen que coincidir exactamente con tu versión del programa.

## Qué es

Screaming Frog es un rastreador (en inglés, crawler): un programa de escritorio que recorre un sitio igual que lo haría un buscador y te devuelve, para cada URL, su código de estado, tipo de contenido, indexabilidad, títulos, metas, enlaces internos y externos, y más. Puedes usarlo de dos formas: con su ventana normal (la GUI, la interfaz visual con botones) o en modo headless, que significa sin abrir ninguna ventana, todo por comandos, ideal para automatizar.

## Gratis o de pago (un matiz que conviene entender)

Lo importante: el modo headless con exportación a CSV y reportes funciona en la versión gratis, hasta 500 URLs por rastreo. No necesitas licencia para automatizar un rastreo y exportar los resultados a CSV en sitios chicos o medianos.

| Capacidad | GRATIS (hasta 500 URLs) | Requiere licencia (~£199/año) |
|---|---|---|
| Límite de URLs por crawl | **500** | >500 (ilimitado) |
| Uso por GUI | Sí | Sí |
| **CLI / headless** (`--headless --crawl`) | **Sí** | Sí |
| Exportación CSV (`--output-folder --overwrite --export-format csv`) | **Sí** | Sí |
| `--export-tabs` (pestañas/filtros) | **Sí** | Sí |
| `--bulk-export` (p. ej. `"Issues:All"`) | **Sí** | Sí |
| `--save-report` (Issues Summary/Overview…) | **Sí** | Sí |
| Configuración guardada (`--config <archivo>`) | No | **Sí** |
| Guardar crawl (`--save-crawl`) | No | **Sí** |
| Renderizado JavaScript | No | **Sí** |
| Programación (scheduling) | No | **Sí** |
| Conexión GSC / GA / PageSpeed (`--use-google-search-console`…) | No | **Sí** |

> Para resumirlo: el modo headless con export a CSV es gratis, con un tope de **500 URLs por rastreo**. Pero ese tope es por rastreo, **no por sitio**: un sitio de miles de URLs se cubre entero y gratis **troceando** — sacas todas las URLs del sitemap y las rastreas en lotes de ≤500 con `--crawl-list`, luego juntas los CSV (lo automatiza `skills/inventario-de-urls/scripts/sf_crawl_all.py`, ver "Sitio entero gratis por troceo" más abajo). Hay funciones que sí requieren licencia, pero ninguna es necesaria para el inventario ni la auditoría base: cargar una configuración guardada (`--config`), `--save-crawl`, renderizar JavaScript, scheduling y conectar APIs de Google (GSC/GA/PageSpeed).

### Una implementación ya probada (gratis)

aprendoseo ya tiene una herramienta interna que corre Screaming Frog en modo headless de forma gratuita y deja ver cómo es el flujo: `technical-audit` (un proyecto en Python, "Technical Audit Automation": SF headless + Unlighthouse + sincronización con Google Sheets). Está en la carpeta hermana `../../../technical-audit/`. Su comando real de rastreo (`src/core/crawler.py`) es este:

```bash
<binario> --headless --crawl <url> --output-folder <dir> --overwrite \
  --export-format csv \
  --save-report "Issues Summary,Issues Overview" \
  --bulk-export "Issues:All"
```

Todos esos flags corren sin licencia hasta 500 URLs. La skill `auditoria-tecnica` y el agente `agente-auditoria-tecnica` pueden reutilizar esta herramienta como punto de partida.

¿Qué es el binario? Es el archivo que ejecuta el programa. Se ubica con la variable de entorno `SCREAMING_FROG_BINARY` (una variable de entorno es un dato guardado en tu sistema que los programas pueden leer) y, si no está esa variable, se busca en la ruta por defecto según tu sistema operativo:

- **macOS:** `/Applications/Screaming Frog SEO Spider.app/Contents/MacOS/ScreamingFrogSEOSpiderLauncher` (también `.../ScreamingFrogSEOSpider`)
- **Windows:** `C:\Program Files (x86)\Screaming Frog SEO Spider\ScreamingFrogSEOSpiderCLI.exe`
- **Linux:** `screamingfrogseospider` en el PATH

## Instalación y binarios según tu sistema

Descárgalo desde screamingfrog.co.uk. Como dijimos, el binario se ubica con la variable `SCREAMING_FROG_BINARY` o, si no está, en la ruta por defecto de tu sistema:

- **macOS:** `/Applications/Screaming Frog SEO Spider.app/Contents/MacOS/ScreamingFrogSEOSpiderLauncher` (también `.../ScreamingFrogSEOSpider`)
- **Windows:** `C:\Program Files (x86)\Screaming Frog SEO Spider\ScreamingFrogSEOSpiderCLI.exe`
- **Linux:** `screamingfrogseospider` en el PATH

## Comandos listos para usar

### 1) Rastreo headless y exportar todas las URLs internas a CSV

```bash
screamingfrogseospider --crawl https://ejemplo.com --headless \
  --output-folder ./sf-out \
  --export-tabs "Internal:All" --export-format csv --overwrite
```

(En macOS, cambia `screamingfrogseospider` por la ruta completa del `ScreamingFrogSEOSpiderLauncher`; en Windows, por `ScreamingFrogSEOSpiderCli.exe`.)

Esto produce `internal_all.csv`: la lista maestra de URLs con Address, Status Code, Content Type, Indexability y demás.

### 2) Páginas huérfanas y grafo de enlaces internos (lista de enlaces origen → destino)

```bash
screamingfrogseospider --crawl https://ejemplo.com --headless \
  --output-folder ./sf-out \
  --bulk-export "All Inlinks,All Outlinks" --export-format csv --overwrite
```

Produce los CSV de inlinks y outlinks (enlaces de origen hacia destino). Crúzalos contra `internal_all.csv`: las URLs que no reciben ningún inlink son las huérfanas (páginas a las que no apunta ningún enlace interno).

### 3) Códigos de respuesta (errores 4xx y redirecciones 3xx)

```bash
screamingfrogseospider --crawl https://ejemplo.com --headless \
  --output-folder ./sf-out \
  --export-tabs "Response Codes:Client Error (4xx),Response Codes:Redirection (3xx)" \
  --export-format csv --overwrite
```

> Las cadenas de `--export-tabs` y los filtros tienen que coincidir exactamente con las etiquetas que ves en la GUI de tu versión.

### 4) Issues completos más reportes (el patrón de la herramienta `technical-audit`, gratis)

```bash
<binario> --headless --crawl https://ejemplo.com \
  --output-folder ./sf-out --overwrite \
  --export-format csv \
  --save-report "Issues Summary,Issues Overview" \
  --bulk-export "Issues:All"
```

Este es el comando real que usa la implementación interna (`technical-audit/src/core/crawler.py`). `--save-report` genera los reportes de resumen de issues, y `--bulk-export "Issues:All"` vuelca a CSV todos los problemas detectados. Todo corre gratis hasta 500 URLs.

### Otros flags que vienen bien

- `--crawl-list <archivo>` — rastrea una lista concreta de URLs en lugar de hacer un crawl completo.
- `--config <archivo>` — carga una configuración guardada (**requiere licencia**).
- `--save-crawl` — guarda `crawl.seospider` para reabrirlo después en la GUI (**requiere licencia**).
- `--timestamped-output` — pone la salida en una carpeta con fecha y hora (sirve para no pisar resultados y guardar histórico).
- `--create-sitemap` — genera un sitemap XML a partir del crawl.
- `--use-google-search-console` / `--use-google-analytics` / `--use-pagespeed` — enriquece los datos con esas APIs (**requiere licencia**).

## Qué archivos te deja y cómo leerlos

- `internal_all.csv` — la lista maestra de URLs (Address, Status Code, Content Type, Indexability…). Es la fuente principal para `inventario-de-urls` y `mapa-de-palabras-clave`.
- CSV de All Inlinks / All Outlinks — los enlaces internos, para detectar páginas huérfanas y medir profundidad (`arquitectura-y-enlazado-interno`).
- CSV de Response Codes — los 4xx y 3xx para `auditoria-tecnica`.

El agente lee estos CSV después del crawl (con Bash o Read) y los procesa como datos de entrada.

## Lo que tiene que estar listo para correr headless

- **Espacio en disco / modo de almacenamiento (causa #1 de fallo al arrancar):** por defecto Screaming Frog usa **almacenamiento en base de datos** (`storage.mode=DB` en `~/.ScreamingFrogSEOSpider/spider.config`) y **exige al menos 4 GB de disco libre**, o aborta sin rastrear con `FATAL - You do not have sufficient disk space to run the SEO Spider`. Si tienes poco disco, cámbialo a **modo memoria (RAM)**, que no pide esos 4 GB y va perfecto para crawls ≤500 URLs: pon `storage.mode=MEMORY` en `spider.config` (o, en la GUI, `Configuration > System > Storage Mode > Memory Storage`) y relanza. El modo memoria queda limitado por la RAM disponible para crawls muy grandes; para ≤500 URLs es la opción recomendada en equipos con disco justo.
- **Licencia (solo si te hace falta):** para más de 500 URLs, config guardada, render JS, scheduling o API, tiene que existir el archivo `~/ScreamingFrogSEOSpider/licence.txt`. Para el flujo gratis (hasta 500 URLs, con export CSV/bulk/report) no hace falta.
- **EULA ya aceptada:** los términos de uso van pre-aceptados en `~/ScreamingFrogSEOSpider/spider.config` con `eula.accepted=N` (el número N depende de la versión, confirmalo al instalar).
- **Binario:** ubícalo con `SCREAMING_FROG_BINARY` o por la ruta por defecto de tu sistema (ver arriba).
- **Linux sin pantalla:** si el servidor no tiene entorno gráfico, puede que necesites poner `xvfb-run` delante del comando (te arma una pantalla virtual para que el programa arranque).
- **No pisar resultados:** usa `--overwrite` o `--timestamped-output` para que no falle si la carpeta de salida ya existe.

## Sitio entero gratis por troceo (más de 500 URLs, sin licencia)

El tope de 500 es **por rastreo**, no por sitio. Para cubrir un sitio grande gratis: saca todas las URLs del sitemap, trocéalas en lotes de ≤500 y rastrea cada lote con `--crawl-list` (que nunca toca el límite), luego junta los CSV. Lo automatiza un script:

```bash
# rastrea TODO el sitio en lotes de 500 y deja un internal_all.csv unificado:
python3 skills/inventario-de-urls/scripts/sf_crawl_all.py --site https://ejemplo.com --out ./sf-out

# ver el plan de lotes sin rastrear (cuántos lotes, de cuántas URLs):
python3 skills/inventario-de-urls/scripts/sf_crawl_all.py --site https://ejemplo.com --dry-run
```

El script:
1. Obtiene las URLs vía sitemap (robots.txt → sitemaps → `<loc>`).
2. Las parte en lotes de ≤500 (un sitemap con más de 500 URLs se divide solo).
3. Corre `--headless --crawl-list lote.txt --export-tabs "Internal:All" --export-format csv` por cada lote.
4. Junta todos los `internal_all.csv` en uno, deduplicando por Address.

Opcionales: `--sitemap <url>` para pasar un sitemap directo, `--bulk-export "Issues:All"` para exportar también los issues, `--batch-size N` (default 500). Requiere el binario de SF (vía `SCREAMING_FROG_BINARY` o ruta por defecto). El `internal_all.csv` resultante se pasa tal cual a `parse_sf.py` y la skill `auditoria-tecnica`.

## 4xx masivos en tiendas Shopify (y otros WAF): rate-limit, NO roturas

**Síntoma:** SF devuelve una proporción altísima de **4xx** en un sitio que en el navegador abre perfecto (p.ej. una tienda Shopify donde el 60-80% de las URLs salen 4xx). Casi siempre **no son páginas rotas**: el sitio detecta el **User-Agent de bot de SF** y/o su velocidad y lo **rate-limita** devolviendo 4xx/429/430 falsos. Shopify lo hace de forma agresiva.

**Cómo confirmarlo:** revalida una muestra de esas URLs con `http_checks.py`, que usa **User-Agent de navegador real** y concurrencia baja (eso es el "throttle"):

```bash
uv run skills/auditoria-tecnica/scripts/http_checks.py --file urls_4xx.txt --cap 50 --concurrency 4
```

Si vuelven **200/301**, eran falsos por rate-limit. Solo las que sigan 4xx tras revalidar son roturas reales.

**Importante — el status NO es toda la data:** `http_checks.py` solo corrige el **Status Code** (+ https + redirect). Las URLs que SF vio como 4xx **nunca tuvieron su HTML parseado**, así que en el `internal_all.csv` les faltan **title, meta description, canonical, encabezados, robots, hreflang**. Para recuperar esa capa on-page se usa un segundo paso: `onpage_extract.py`.

**Automático (2 pasos):** `sf_crawl_all.py` **detecta Shopify** (headers `x-shopify-*`, `cdn.shopify.com`) y:
1. **Revalida** los 4xx/5xx con `http_checks.py` (UA real + baja concurrencia), corrigiendo el `Status Code` en `internal_all.csv`.
2. **Enriquece on-page** las URLs recuperadas (las que eran 4xx falsos y ahora dan 200) con `onpage_extract.py`: baja el HTML con UA real + throttle y extrae **title, meta description, meta robots, canonical (+ self-canonical), H1/H2, hreflang, lang, word count, indexability**. Lo deja en `onpage_enriched.json` y `onpage_enriched.csv` junto al CSV.

Flags: `--revalidate` / `--no-revalidate`, `--enrich` / `--no-enrich`, `--revalidate-concurrency` y `--enrich-concurrency` (default 4; baja a 2 si aún bloquea).

```bash
# crawl + revalidación de status + enriquecimiento on-page (todo auto en Shopify):
python3 skills/inventario-de-urls/scripts/sf_crawl_all.py --site https://tienda.com --out ./sf-out
# salida → "revalidation": {"fixed":<falsos>,"still_bad":<rotas reales>},
#          "onpage_enrichment": {"enriched":N,"indexable":M,"json":"...","csv":"..."}

# extraer on-page de una lista de URLs a mano (sin SF):
uv run skills/auditoria-tecnica/scripts/onpage_extract.py --file urls.txt --concurrency 4 --csv onpage.csv
```

**Límite honesto:** `onpage_extract.py` recupera la capa **on-page por URL**, pero NO los **inlinks / grafo de enlaces internos / profundidad de crawl** — eso requiere rastrear el sitio, y SF gratis se bloquea en Shopify. Para el grafo completo de un Shopify hace falta SF con licencia (`--config` con 1 hilo + UA real).

**Throttle nativo en SF (opcional, se setea una vez):** SF headless gratis no expone velocidad ni User-Agent por CLI (esa config es de la GUI y `--config` requiere licencia). Si quieres que el propio crawl no se bloquee: abre SF una vez en la GUI, pon `Configuration > User-Agent` en **Chrome** y `Configuration > Speed` en **1-2 hilos / 1-2 URL por segundo**, y guarda. Esa config por defecto persiste en `~/.ScreamingFrogSEOSpider/spider.config` y la respetan también los rastreos headless. Aun así, revalidar con `http_checks.py` es el camino fiable y automatizable.

## Plan B por sitemap, sin instalar nada (solo URLs publicadas)

Si no quieres instalar Screaming Frog (o solo necesitas las URLs publicadas, sin códigos de estado ni huérfanas), consigue el inventario así, en este orden:

1. Abre `https://<sitio>/robots.txt` y lee las directivas `Sitemap:`.
2. Descarga cada sitemap que aparezca ahí (o prueba con `sitemap.xml` o `sitemap_index.xml`).
3. Si es un `<sitemapindex>`, sigue cada hijo hasta llegar a los sitemaps que tienen las URLs.
4. Saca todos los `<loc>`.

Ten en cuenta el límite: así solo ves las URLs publicadas en el sitemap. No detecta huérfanas, no trae códigos de estado en vivo ni el grafo de enlaces. Para más detalle, mira la skill `skills/inventario-de-urls/SKILL.md`.

## Fuentes

- https://www.screamingfrog.co.uk/seo-spider/user-guide/general/ — guía de uso, modo CLI/headless y flags (el CLI funciona en la versión gratis hasta 500 URLs).
- https://www.screamingfrog.co.uk/seo-spider/pricing/ — la licencia (~£199/año) se requiere para más de 500 URLs, config guardada, render JS, scheduling e integraciones de API; hasta 500 URLs es gratis.
- Implementación de referencia interna: `../../../technical-audit/` (`src/core/crawler.py`) — SF headless gratis con export CSV/bulk/report.
