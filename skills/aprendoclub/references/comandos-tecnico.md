# Comandos técnicos y de arquitectura

Cada comando carga la skill destino, sigue su `SKILL.md` y termina con `dashboard-seo`.

## `/aprendoclub technical <sitio>`

- **Ejecuta:** `agente-auditoria-tecnica` cuando se trata de una auditoría completa o de crawls grandes (Semana 12). Para una duda puntual de una etiqueta, canonical o redirección usa `auditoria-tecnica` directamente.
- **Antes:** `inventario-de-urls` si no hay lista de URLs.
- **Después:** `puntaje_salud.py` sobre `issues.json`.
- **Ejemplo:** `/aprendoclub technical midominio.com`
- **Salidas:** `issues.json`, `inventory-summary.json`, `prior-audits.json`, `meta.json`.

## `/aprendoclub sitemap <sitio>`

- **Ejecuta:** `inventario-de-urls` y `sitemap-y-robots` (Semanas 3 y 12).
- **Ejemplo:** `/aprendoclub sitemap midominio.com`
- **Salidas:** `inventory-summary.json`, hallazgos de robots y sitemap dentro de `issues.json`.

## `/aprendoclub performance <sitio>`

- **Ejecuta:** `analisis-rendimiento` (Unlighthouse en cada ruta; modo manual con PageSpeed Insights si no hay Node). Core Web Vitals de laboratorio. Para datos de campo usa `psi_campo.py` o `crux_campo.py` si el usuario los pide.
- **Ejemplo:** `/aprendoclub performance midominio.com`
- **Salidas:** `performance.json` (y `cwv-field.json` si hay campo).

## `/aprendoclub images <url>`

- **Ejecuta:** `optimizacion-de-imagenes` (peso mayor a 100 kb, WebP, dimensiones, ALT, nombres, lazy loading).
- **Ejemplo:** `/aprendoclub images https://midominio.com/producto`
- **Salidas:** hallazgos en `issues.json`.

## `/aprendoclub schema <url>`

- **Ejecuta:** `schema-jsonld`: diagnostica el marcado actual y genera el bloque JSON-LD listo para pegar. No marques contenido que no exista en la página.
- **Ejemplo:** `/aprendoclub schema https://midominio.com/blog/articulo`
- **Salidas:** bloque `<script>`, `schema-validation.json` si se valida.

## `/aprendoclub architecture <sitio>`

- **Ejecuta:** `arquitectura-y-enlazado-interno` (Semana 9): regla de 3 clics, huérfanas, pilar a clusters, anchors.
- **Datos:** exports `internal_all.csv` y `all_inlinks.csv` de Screaming Frog; sin ellos, revisión manual con el inventario.
- **Ejemplo:** `/aprendoclub architecture midominio.com`
- **Salidas:** `clusters.json` y tareas para `next-steps.json`.
