# Complementos de claude-seo para el inventario de URLs

> **Complemento externo (claude-seo, MIT), no es parte del método del diplomado.**
> Fuente: `skills/seo-sitemap/SKILL.md` y `scripts/sitemap_discovery.py` del repo AgriciDaniel/claude-seo. Adaptado al español. Si algo contradice el diplomado, gana el diplomado.

## Límites y calidad del sitemap que conviene saber al inventariar

- Un archivo de sitemap admite **hasta 50.000 URLs y 50 MB sin comprimir** (lo que se alcance antes). Por encima se usa un **índice de sitemaps**. Si `sitemaps_read` del script muestra un `index`, el inventario ya recorrió los hijos.
- Los sitemaps pueden venir **comprimidos** (`.xml.gz`): el script ya los descomprime.
- Rutas alternativas habituales cuando robots.txt no declara sitemap: `/sitemap.xml`, `/sitemap_index.xml`, `/wp-sitemap.xml`, `/sitemap-index.xml`, `/sitemap/sitemap.xml`. El script prueba esas cinco.
- Un sitemap sano **no incluye** URLs con redirección, con `noindex`, canonicalizadas a otra URL ni con error 4xx/5xx. Si el inventario las trae, anótalas como hallazgo para la skill `sitemap-y-robots`, no las uses sin revisar para el mapa de palabras clave.
- `<priority>` y `<changefreq>` los ignora Google. `<lastmod>` solo cuenta si es fiable: valores idénticos en todas las URLs indican que es automático y no informa.
- No reportes "no hay sitemap" hasta haber probado las declaraciones de robots.txt y las rutas alternativas. Una declaración en robots.txt no prueba que el sitemap funcione.

## Qué hacer después

1. Pasa la lista al Sheet (Plantilla Master) y cruza con `site:` o GSC para ver la brecha de indexación.
2. Si el sitemap tiene muchas menos URLs que `site:`, hay contenido indexado fuera del mapa (basura, parámetros) o un sitemap desactualizado.
3. Para huérfanas, estado en vivo y profundidad en clics, usa Screaming Frog (camino SF de esta skill).
