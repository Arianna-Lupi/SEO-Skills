# Datos de dominio opcionales (complemento, de pago o con clave)

> **Complemento opcional, no es parte del método del diplomado.** El diplomado enseña a trabajar con las versiones gratuitas de las herramientas y a llenar solo el 50 a 60 % de los datos de 2 competidores (Semana 6 · lección 4). Todo lo de abajo enriquece el análisis cuando el usuario ya tiene la herramienta. Sin claves, la skill funciona en modo manual.

Regla de datos: si una herramienta no devuelve el dato, escribe `pendiente de dato` (o 0 si la herramienta marcó cero). Nunca estimes volumen, KD, tráfico ni backlinks.

## Qué aporta cada fuente

| Dato | Fuente | Cómo se usa |
|---|---|---|
| Top de la SERP, PAA, features | SerpApi (`serp.py` o `mcp__serpapi__search`) | Entrada de `perfil_competidor.py --serp-json` |
| Top de la SERP con métricas | Ahrefs MCP `serp-overview` | Posiciones, tráfico y DR por resultado; pasa las URLs a `perfil_competidor.py` |
| Keywords orgánicas por competidor | Ahrefs MCP `site-explorer-organic-keywords` | Alimenta "Keywords Top" de la tab Competencia y el CSV de `brechas.py` |
| Páginas top por competidor | Ahrefs MCP `site-explorer-top-pages` | "Páginas Top": candidatas a perfilar con `perfil_competidor.py` |
| Competidores orgánicos | Ahrefs MCP `site-explorer-organic-competitors` | Cruza con el Análisis de Repetición |
| Autoridad | Ahrefs MCP `site-explorer-domain-rating` | "Autoridad/Estructura" (un solo indicador no resume al competidor) |
| Backlinks por competidor | Ahrefs MCP `site-explorer-backlinks-stats`, `site-explorer-referring-domains` | Columna de enlaces entrantes; para el análisis detallado de enlaces usa `link-building-y-outreach` |
| Volumen real | Ahrefs `keywords-explorer-overview` o Search Console | Se pasa a `comparar_serp.py --volumenes volumenes.json` |

Antes de llamar a una herramienta de Ahrefs, usa su herramienta `doc` para ver los parámetros. Cuesta unidades de la suscripción del usuario: pide permiso antes de lanzar consultas masivas.

## De Ahrefs a `brechas.py`

`brechas.py` espera `keyword,domain,position[,url,volume]`. Con `site-explorer-organic-keywords` por competidor arma una fila por keyword y dominio con la posición que devuelve la herramienta y el volumen que trae. Si falta un valor, deja la celda vacía.

## Volúmenes en `comparar_serp.py`

```json
{"cómo preparar café": 1900, "comprar café de especialidad": 720}
```

El script solo los muestra al lado de cada keyword. No calcula visitas porque eso exige un CTR que tú eliges. Si quieres una estimación para el reporte, hazla a mano, rotúlala como supuesto y cita la fuente del CTR.

## DataForSEO (claude-seo)

claude-seo (MIT) trae un flujo de competidores con DataForSEO de pago (`skills/seo-dataforseo`, sección "Domain & Competitor Analysis"): dominios competidores con solape de keywords, tráfico estimado y keywords rankeadas. Es un equivalente al de Ahrefs. No se incluye aquí; si el usuario ya lo tiene, sus resultados entran por el mismo CSV de `brechas.py`.
