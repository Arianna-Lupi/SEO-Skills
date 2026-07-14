---
name: auditoria-de-backlinks-toxicos
description: Analiza y clasifica el perfil de backlinks de un sitio en 4 categorías de riesgo (Toxic/Suspicious/Low-quality-but-safe/Neutral-OK) con evidencia auditable, y genera el disavow.txt listo para subir a Google Search Console. Usa esta skill cuando el usuario pida "auditoría de backlinks", "revisa mi perfil de enlaces", "necesito un disavow", "tengo un export de Ahrefs/Semrush de backlinks", "se me cayó el tráfico y sospecho de link spam", o al hacer limpieza de un perfil de enlaces heredado (dominio comprado, cliente nuevo con historial SEO desconocido). NO uses esta skill para conseguir enlaces nuevos ni outreach (eso es `link-building-y-outreach`).
compatibility: Requiere export de backlinks/dominios referentes (Ahrefs, Semrush o similar) en CSV. Script determinista (stdlib, Python 3 vía uv). Ahrefs MCP opcional para traer los datos en vivo.
metadata:
  author: aprendoseo
  milestone: SEO skills (link building)
  version: "1.0"
---

> **🚫 Regla de datos (obligatoria): NUNCA inventes números.**
> No estimes ni asumas ascore, external links, sitewide, país, ni ningún otro dato del perfil de backlinks. Si te falta un dato, pedíselo al usuario (export de Ahrefs/Semrush/Moz) y espera su respuesta. Sin dato real, marca `pendiente de dato` — nunca completes con supuestos.

# Auditoría de Backlinks Tóxicos y Disavow

Analiza el perfil de enlaces entrantes de un sitio, clasifica cada dominio referente por nivel de riesgo con evidencia citable, y produce el archivo de desautorización (`disavow.txt`) listo para Google Search Console. Es el primer paso obligatorio antes de cualquier estrategia de link building: no tiene sentido construir enlaces nuevos sobre un perfil que arrastra spam sin limpiar.

## Cuándo usar

- Cliente nuevo con historial SEO desconocido (dominio comprado, agencia anterior sin buenas prácticas).
- Caída de tráfico orgánico sin causa de contenido/técnica evidente — sospecha de link spam o penalización manual.
- Antes de lanzar una campaña de link building nueva (limpia primero, construí después).
- Revisión periódica de perfil de enlaces en sitios con mucho tiempo online.

## Entradas (qué necesitas)

- Export de **backlinks individuales** (CSV): origen, destino, anchor, nofollow, first/last seen.
- Export de **dominios referentes** (CSV): dominio, ascore/DR, país, external_links máximo por página, sitewide (sí/no).
- Fuente: Ahrefs, Semrush, Moz o el MCP de Ahrefs si el usuario lo tiene conectado (`mcp__claude_ai_Ahrefs__site-explorer-referring-domains`, `...all-backlinks`, `...anchors`).

## Proceso

1. **Normaliza los exports.** Verifica conteos reales con el CSV (no confíes en `wc -l` sin restar encabezado, ni asumas que el conteo del export coincide exacto entre backlinks y dominios — documenta cualquier diferencia).
2. **Aplica la rúbrica de clasificación** (ver [`references/rubrica-clasificacion.md`](references/rubrica-clasificacion.md)) a nivel de **dominio primero**, con `scripts/classify_domains.py`.
3. **Propaga la categoría a cada backlink individual** del dominio. Marca overrides caso a caso si un backlink diverge claramente del patrón de su dominio.
4. **Consolida duplicados** exactos (mismo origen+destino) en una fila con `instance_count`.
5. **Genera el disavow.txt** con `scripts/generate_disavow.py` — solo dominios Toxic, agrupados en clusters temáticos legibles (blogspot/granja, venta de backlinks, manipulación de anchor, otro).
6. **Entrega tabla maestra** con columnas: `domain, backlink_url, risk_type, recommended_action, notes, instance_count` — acción recomendada es `Disavow` solo para Toxic; el resto queda documentado pero no se desautoriza.

## Script determinista (ahorro de tokens)

```
uv run skills/auditoria-de-backlinks-toxicos/scripts/classify_domains.py \
  --input domain-signals.csv --output domain-classification.csv \
  --related-country ca --mass-anchor-domain dominio-competidor-ejemplo.ca
```

Escribe el CSV (`domain, domain_ascore, country, senales, categoria, evidencia`) y devuelve JSON por stdout: `{"ok":true,"rows":N,"counts":{"Toxic":N,...},"output":"domain-classification.csv"}`.

```
uv run skills/auditoria-de-backlinks-toxicos/scripts/generate_disavow.py \
  --input domain-classification.csv --output disavow.txt --site midominio.com
```

Escribe `disavow.txt` en formato exacto de Google (`domain:ejemplo.com`), agrupado en clusters con comentarios `#`. Devuelve JSON: `{"ok":true,"generated":true,"total_domains":N,"clusters":{...},"output":"disavow.txt"}` (o `"generated":false` si no hay dominios Toxic).

Si no hay `uv`: `python3 skills/auditoria-de-backlinks-toxicos/scripts/classify_domains.py --help`.

## Salida

- **`domain-classification.csv`** y **`backlink-classification.csv`** (evidencia auditable por fila).
- **`disavow.txt`** listo para subir en [Google Search Console → Disavow links](https://search.google.com/search-console/disavow-links).
- **Tabla maestra** con acción recomendada por backlink.
- Resumen ejecutivo: % Toxic/Suspicious/Low-quality/Neutral, y los 2-3 clusters de spam más grandes.

## Gotchas

- **País vacío o distinto al "relacionado" NUNCA descalifica solo** — necesita señal co-ocurrente (sitewide, external>umbral, anchor en masa). Clasificar por país solo genera falsos positivos masivos.
- **Nunca Toxic por ascore solo** — un sitio nuevo legítimo puede tener ascore bajo sin ser spam. Ascore bajo sin otra señal es Suspicious, no Toxic.
- **Nofollow desde dominio tóxico se incluye igual en el disavow** — no protege del todo contra el efecto del enlace.
- **Domain-first, no backlink-first** — clasifica el dominio completo primero; el override por backlink individual es la excepción, no la regla.
- **El disavow es domain-level, no URL-level**, salvo caso puntual documentado — es la práctica recomendada por Google (evita desautorizar de más si el dominio cambia de estructura).
- **Nunca subestimes verificando manualmente antes de entregar** — antes de subir el disavow al cliente, cuenta dos veces los dominios Toxic y confirma que el CSV de origen no cambió entre la clasificación y la generación del archivo.
- **Esta skill limpia, no construye.** Para conseguir enlaces nuevos, encadena con la skill `link-building-y-outreach` después de limpiar.
