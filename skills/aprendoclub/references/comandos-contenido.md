# Comandos de keywords y contenido

## `/aprendoclub keywords <nicho o sitio>`

- **Ejecuta:** `agente-investigacion-keywords` (Semana 4): semillas, expansión, intención, clusters, punto dulce, Duelo de Keywords y "10 de Oro". Luego `mapa-de-palabras-clave` (Semana 5) si ya hay URLs. Con Search Console, suma `deteccion-de-canibalizacion`.
- **Para una duda suelta** (una sola keyword) usa `investigacion-de-keywords` directamente.
- **Ejemplo:** `/aprendoclub keywords "café de especialidad"`
- **Salidas:** `keywords.json`, `clusters.json`.
- **Datos:** volumen y KD solo reales (Ahrefs, DinoRank, export). Si no, `pendiente`.

## `/aprendoclub intent <keyword>`

- **Ejecuta:** `intencion-de-busqueda` (Semana 4 y 5): clasifica la intención y la valida contra la SERP.
- **Ejemplo:** `/aprendoclub intent "mejor cafetera para casa"`
- **Salidas:** intención y tipo de contenido que premia la SERP, para `brief-de-contenido`.

## `/aprendoclub content <url o keyword>`

- **Si recibe una keyword:** `agente-contenido` (Semanas 6, 8 y 11): SERP, brief del tipo correcto, borrador humanizado y checklist on-page, con un checkpoint para revisar el brief antes de redactar.
- **Si recibe una URL:** `calidad-de-contenido-eeat` y, si la página ya existe y no rinde, `actualizacion-de-contenido`.
- **Ejemplos:** `/aprendoclub content "cómo preparar café"` · `/aprendoclub content https://midominio.com/blog/cafe`
- **Salidas:** `content-briefs.json` y `content/<slug>.html`.

## `/aprendoclub onpage <url>`

- **Ejecuta:** `optimizacion-on-page-meta` (Semanas 8 y 11): metatítulo de 50 a 60 caracteres con la keyword al inicio, metadescripción de 120 a 155 con CTA, variantes A/B y checklist.
- **Ejemplo:** `/aprendoclub onpage https://midominio.com/servicios`
- **Salidas:** metas propuestas en `content-briefs.json`.

## `/aprendoclub quality <url>`

- **Ejecuta:** `calidad-de-contenido-eeat` (Semanas 7, 11 y 14): experiencia, autoría, confianza, profundidad y señales de texto genérico.
- **Ejemplo:** `/aprendoclub quality https://midominio.com/blog/cafe`

## `/aprendoclub update <url>`

- **Ejecuta:** `actualizacion-de-contenido` (Semana 10): brief de optimización de una página existente, con oportunidades de Search Console si hay export.
- **Ejemplo:** `/aprendoclub update https://midominio.com/blog/cafe`

Skills relacionadas que `agente-contenido` encadena y que también se pueden pedir por nombre: `brief-de-contenido`, `redaccion-y-optimizacion-nlp`, `estrategia-de-contenidos-clusters`.
