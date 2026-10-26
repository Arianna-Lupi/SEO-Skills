# Contrato de datos: perfil, comparación y tareas

Para que `plan-seo`, `brief-de-contenido` y el dashboard lean la salida de esta skill sin adivinar. Versión 1. Cambios compatibles solo añaden campos.

## 1. `perfiles.json` (salida de `perfil_competidor.py`)

```json
{"ok": true, "generated": "ISO-8601", "blocked": false, "errors": [], "notes": [],
 "profiles": [{
   "url": "...", "domain": "registrado sin www", "role": "competitor|own",
   "keyword": "keyword de la SERP o null", "position": 1,
   "title": "", "meta_description": "", "canonical": "",
   "h1": [], "headings": [{"level": 2, "text": ""}], "counts": {"h1": 1, "h2": 6, "h3": 2},
   "word_count": 0, "top_terms": [],
   "page_type": "blog|landing|ecommerce|categoria|herramienta|video|foro|otro",
   "page_type_confidence": "alta|media|baja", "page_type_signals": [],
   "schema_types": [], "schema_jsonld_errors": 0,
   "images": {"total": 0, "with_alt": 0},
   "links": {"internal": 0, "external": 0, "external_in_body": 0, "external_domains": []},
   "dates": {"published": "YYYY-MM-DD|null", "modified": "YYYY-MM-DD|null", "age_days": 0},
   "eeat": {"author": false, "author_name": null, "date_visible": false, "sources_cited": false,
            "own_data": false, "first_hand_experience": false, "about_or_org_schema": false},
   "formats": {"faq": false, "faq_schema": false, "lists": 0, "list_items": 0, "tables": 0, "video": false, "forms": 0},
   "javascript_dependent": false, "fetch": {"mode": "red|html", "status": 200}}]}
```

### Heurísticas (orientativas)

- **Tipo de página:** puntaje por señales. Schema (Product/Offer, ItemList/CollectionPage, Article/BlogPosting, SoftwareApplication, VideoObject, DiscussionForumPosting) pesa más; luego la ruta (`/blog/`, `/categoria/`, `/producto/`, `/foro/`), el dominio (YouTube, Reddit) y el contenido (precio más botón de compra = ficha de producto; varias tarjetas con precio = categoría; texto largo con autor y sin precios = blog; poco texto con llamado a la acción = landing). `page_type_signals` lista lo que decidió. `otro` o confianza baja pide revisión a ojo. Es una clasificación propia del repo (inspirada en la taxonomía de tipos de página de `seo-sxo`, ver `complementos-claude-seo.md`).
- **Palabras:** texto fuera de `nav`, `header`, `footer`, `aside` y `form`, sin scripts.
- **Depende de JavaScript:** menos de 60 palabras con varios scripts o un contenedor `#root`, `#app`, `#__next`, `#__nuxt`. Sus palabras y encabezados son parciales.
- **Autoría:** schema `author`, `meta author`, `rel=author`, o clases `author`/`byline`. **Fuentes:** 2 o más enlaces externos en el cuerpo o texto "Fuentes:". **Datos propios:** frases como "nuestro estudio", "hemos analizado", "en nuestras pruebas". **Experiencia:** "en mi experiencia", "años de experiencia", "he probado".
- **Frescura:** `dateModified` o `datePublished` del schema, meta `article:*_time` o etiquetas `<time>`.

## 2. `comparacion.json` (salida de `comparar_serp.py`)

```json
{"ok": true, "generated": "", "umbral_patron": 0.6, "tiene_pagina_propia": true, "pagina_propia": "url",
 "keywords": [{"keyword": "", "volumen": 1900 | "pendiente de dato",
   "patron": {"paginas": 3, "paginas_legibles": 2, "tipo_pagina": {"distribucion": {}, "dominante": "blog|null", "consenso": "fuerte|mixto|fragmentado", "proporcion": 0.67},
              "palabras": {"min": 0, "p25": 0, "mediana": 0, "p75": 0, "max": 0}, "temas_frecuentes": [], "encabezados_frecuentes": [],
              "h2": {}, "schema": [], "formato": {"prevalencia": {}, "comun": []}, "eeat": {"prevalencia": {}, "comun": []}, "frescura": {}},
   "tabla": [{"metrica": "", "tu_pagina": "", "top": ""}],
   "brechas": [{"keyword": "", "categoria": "tipo de página|cobertura de temas|estructura|formato|schema|E-E-A-T|frescura",
                "id": "tipo|longitud|h2|h1|meta|faq|tablas|listas|video|imagenes|alt|autor|fuentes|datos_propios|experiencia|fecha|antiguedad|tema:<raíz>|schema:<Tipo>",
                "brecha": "", "evidencia": "2 de 3 páginas del top", "prevalencia": 0.67, "puntaje": 0, "depende_del_tipo": false}],
   "desajuste_tipo": false, "costo_oportunidad": 0, "nivel_costo": "alto|medio|bajo"}],
 "repeticion": {"keywords": 3, "umbral_critico": 2, "dominios": [{"domain": "", "repeticion": 2, "de": 3, "critico": true, "mejor_posicion": 1, "keywords": {}, "tipos_de_pagina": [], "urls": []}], "urls_repetidas": []},
 "tareas": [{"id": "T01", "tarea": "Verbo + qué + dónde", "categoria": "", "brecha_id": "", "keywords": [], "por_que": "",
             "skill_sugerida": "brief-de-contenido|schema-jsonld|optimizacion-on-page-meta|intencion-de-busqueda|calidad-de-contenido-eeat|actualizacion-de-contenido",
             "impacto": 1, "confianza": 1, "facilidad": 1, "ice": 0.0, "prioridad": "alta|media|baja", "condicion": "",
             "plazo": "pendiente de dato", "recurso": "pendiente de dato", "responsable": "pendiente de dato"}],
 "formula_costo_oportunidad": "texto", "notas": []}
```

## 3. `.seo-audit/<sitio>/data/competitors.json` (convención de `dashboard-seo`)

`comparar_serp.py --sitio ejemplo.com` (o `--competitors-json ruta`) fusiona con el archivo existente:

- `by_pillar[]`: una entrada por keyword (`pillar` = keyword salvo que pases `--pilares`), `query` = keyword y `results[]` con los campos que ya lee el dashboard (`position`, `domain`, `title`, `url`) más `page_type`, `word_count`, `schema_types`, `javascript_dependent`.
- `strategic[]`: dominios críticos (`name`, `url`) más `repeticion`, `de`, `critical`.
- `serp_analysis` (nuevo): `generated`, `keywords` (patrón, tabla, brechas, Costo de Oportunidad), `repeticion`, `tasks`, `formula_costo_oportunidad`, `notas`.

El dashboard ignora claves que no conoce, así que añadir esto no rompe nada.

## 4. Quién consume qué

| Consumidor | Qué lee | Cómo |
|---|---|---|
| `brief-de-contenido` | `serp_analysis.keywords[].patron` (tipo dominante, rango de palabras, `temas_frecuentes`, `encabezados_frecuentes`, formato común, schema) | El tipo de brief lo dicta la SERP (Semana 8 · lección 3): usa `tipo_pagina.dominante` para elegir el tipo y `temas_frecuentes` para la lista de H2. El rango de palabras es contexto, no meta |
| `plan-seo` | `tareas[]` | Cada tarea entra a la pestaña de tareas con `ice`, `prioridad`, `skill_sugerida` y los campos `plazo`, `recurso`, `responsable` que el usuario completa |
| `dashboard-seo` | `by_pillar`, `strategic` | Sin cambios |
| `intencion-de-busqueda` | `desajuste_tipo` y `tipo_pagina.distribucion` | Si hay desajuste, se valida la intención antes de tocar el contenido |

Todo número viene de la página perfilada o del usuario. Volumen, KD y tráfico quedan en `pendiente de dato` si el usuario no los aporta.
