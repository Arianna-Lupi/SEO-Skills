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

> Para resumirlo: si el sitio tiene 500 URLs o menos, haces todo gratis por línea de comandos en modo headless, exportando a CSV. La licencia solo hace falta para rastreos de más de 500 URLs, para cargar una configuración guardada (`--config`), para `--save-crawl`, para renderizar JavaScript, para programar rastreos automáticos (scheduling) y para conectar APIs de Google (GSC/GA/PageSpeed). Si el sitio pasa de 500 URLs y no tienes licencia, completa el inventario con el plan B gratis por sitemap que está más abajo.

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

- **Licencia (solo si te hace falta):** para más de 500 URLs, config guardada, render JS, scheduling o API, tiene que existir el archivo `~/ScreamingFrogSEOSpider/licence.txt`. Para el flujo gratis (hasta 500 URLs, con export CSV/bulk/report) no hace falta.
- **EULA ya aceptada:** los términos de uso van pre-aceptados en `~/ScreamingFrogSEOSpider/spider.config` con `eula.accepted=N` (el número N depende de la versión, confirmalo al instalar).
- **Binario:** ubícalo con `SCREAMING_FROG_BINARY` o por la ruta por defecto de tu sistema (ver arriba).
- **Linux sin pantalla:** si el servidor no tiene entorno gráfico, puede que necesites poner `xvfb-run` delante del comando (te arma una pantalla virtual para que el programa arranque).
- **No pisar resultados:** usa `--overwrite` o `--timestamped-output` para que no falle si la carpeta de salida ya existe.

## Plan B por sitemap, sin instalar nada (o para más de 500 URLs sin licencia)

Si no quieres instalar Screaming Frog, o el sitio supera las 500 URLs y no tienes licencia, consigue el inventario de URLs publicadas así, en este orden:

1. Abre `https://<sitio>/robots.txt` y lee las directivas `Sitemap:`.
2. Descarga cada sitemap que aparezca ahí (o prueba con `sitemap.xml` o `sitemap_index.xml`).
3. Si es un `<sitemapindex>`, sigue cada hijo hasta llegar a los sitemaps que tienen las URLs.
4. Saca todos los `<loc>`.

Ten en cuenta el límite: así solo ves las URLs publicadas en el sitemap. No detecta huérfanas, no trae códigos de estado en vivo ni el grafo de enlaces. Para más detalle, mira la skill `skills/inventario-de-urls/SKILL.md`.

## Fuentes

- https://www.screamingfrog.co.uk/seo-spider/user-guide/general/ — guía de uso, modo CLI/headless y flags (el CLI funciona en la versión gratis hasta 500 URLs).
- https://www.screamingfrog.co.uk/seo-spider/pricing/ — la licencia (~£199/año) se requiere para más de 500 URLs, config guardada, render JS, scheduling e integraciones de API; hasta 500 URLs es gratis.
- Implementación de referencia interna: `../../../technical-audit/` (`src/core/crawler.py`) — SF headless gratis con export CSV/bulk/report.
